#!/usr/bin/env python3
"""Pruebas de migrar_a_toggl.py: orden de la cola, áreas, bandeja, ids ya existentes y toggl.md.

    python3 -m unittest test_migrar_a_toggl.py      (desde esta carpeta)
"""

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import migrar_a_toggl as m  # noqa: E402

TAREAS = """<!-- tarea: umbral 40000 chars -->

# Tareas

## Ahora

| # | Tarea | Sección | Estado | Vence | Coste | Nota |
| :--: | --- | --- | --- | --- | --- | --- |
| 1 | Corregir el menú móvil | Componentes | 🔵 En curso | — | ~45m | — |
| 2 | Probar un pago real | Pagos | Bloqueada | 2026-10-10 | 2h 30m | Necesita la URL pública |

---

## General

Configuración.

| Estado | Tarea | Vence | Coste | Inicio | Completada | Duración | Comentarios |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Pendiente | Limpiar datos de prueba | — | — | — | — | — | Hay compras falsas. |
| ✅ Completada | Algo ya hecho | — | — | — | — | — | — |

## Componentes

| Estado | Tarea | Vence | Coste | Inicio | Completada | Duración | Comentarios |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 🔵 En curso | Corregir el menú móvil | — | ~45m | — | — | — | `AppHeader.vue` no cierra. [detalle](#x) |

## Pagos

| Estado | Tarea | Vence | Coste | Inicio | Completada | Duración | Comentarios |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Bloqueada | Probar un pago real de punta a punta con credenciales de producción <!-- toggl:777 --> | 2026-10-10 | 2h 30m | — | — | — | Mercado Pago. |
"""

REVISAR = """# Por revisar

| Tarea | Origen | Motivo | Notas |
| --- | --- | --- | --- |
| Revisar el contraste de los botones | auditoría del 20-09 | Falla AA | — |
"""

SECCIONES = """# Secciones

Catálogo.

## General

Configuración y datos de prueba.

**Cerradas: 1h** · 2 archivadas

---

## Componentes

Los componentes compartidos.

---

## Pagos

Cobro y checkout.
"""


class Migracion(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        c = Path(self.dir.name)
        (c / "tareas.md").write_text(TAREAS, encoding="utf-8")
        (c / "revisar.md").write_text(REVISAR, encoding="utf-8")
        (c / "secciones.md").write_text(SECCIONES, encoding="utf-8")
        self.c = c
        self.r = m.armar(c, 42, 7, {"todo": 1, "in_progress": 2, "blocked": 3}, "2026-09-28",
                         {"Componentes": 11, "General": 10})

    def tearDown(self):
        self.dir.cleanup()

    def todas(self):
        return self.r["crear"] + self.r["actualizar"]

    def test_orden_ahora_primero_y_sin_las_cerradas(self):
        nombres = [t["nombre"] for t in self.r["crear"]]
        self.assertEqual(nombres, ["Corregir el menú móvil", "Limpiar datos de prueba"])
        self.assertNotIn("Algo ya hecho", [t["nombre"] for t in self.todas()])

    def test_la_que_ya_tiene_id_se_actualiza_con_el_nombre_corto(self):
        [t] = self.r["actualizar"]
        self.assertEqual(t["toggl_id"], 777)
        self.assertEqual(t["nombre"], "Probar un pago real")
        self.assertIn("con credenciales de producción", t["descripcion"])
        self.assertIn("Necesita la URL pública", t["descripcion"])
        self.assertEqual(t["payload"]["id"], 777)

    def test_area_estado_coste_y_vence(self):
        menu = self.r["crear"][0]
        self.assertTrue(menu["descripcion"].startswith("Área: Componentes\n"))
        self.assertIn("AppHeader.vue no cierra", menu["descripcion"])
        self.assertNotIn("detalle", menu["descripcion"])
        self.assertEqual(menu["payload"]["status_id"], 2)
        self.assertEqual(menu["payload"]["estimated_mins"], 45)
        self.assertEqual(menu["payload"]["assignee_user_ids"], [7])
        self.assertEqual(menu["payload"]["tag_ids"], [11])
        pago = self.r["actualizar"][0]["payload"]
        self.assertEqual((pago["start_date"], pago["end_date"], pago["status_id"]), ("2026-09-28", "2026-10-10", 3))
        self.assertEqual(pago["estimated_mins"], 150)

    def test_la_bandeja_no_va_a_toggl_sino_a_por_revisar_md(self):
        self.assertNotIn("Revisar el contraste de los botones", [t["nombre"] for t in self.todas()])
        [b] = self.r["bandeja"]
        self.assertEqual((b["nombre"], b["area"], b["origen"]), ("Revisar el contraste de los botones", "General", "auditoría del 20-09"))
        self.assertEqual(m.main(["por-revisar", str(self.c), "--hoy", "2026-09-29"]), 0)
        texto = (self.c / "por-revisar.md").read_text()
        self.assertIn("- **Revisar el contraste de los botones** · General · auditoría del 20-09 · 2026-09-29 — Falla AA", texto)
        self.assertNotIn("AppHeader.vue:88", texto)   # el ejemplo del esqueleto no se copia

    def test_areas_desde_el_catalogo(self):
        self.assertEqual([a["nombre"] for a in self.r["areas"]], ["General", "Componentes", "Pagos"])
        self.assertEqual(self.r["areas"][0]["ambito"], "Configuración y datos de prueba.")

    def test_pares_no_exactos_se_devuelven_para_confirmar(self):
        self.assertEqual([p["ahora"] for p in self.r["dudosos"]], ["Probar un pago real"])

    def test_minutos(self):
        self.assertEqual(m.minutos("~45m"), 45)
        self.assertEqual(m.minutos("2h 30m"), 150)
        self.assertEqual(m.minutos("1h"), 60)
        self.assertIsNone(m.minutos("—"))

    def test_toggl_md_se_escribe_una_vez(self):
        salida = io.StringIO()
        with redirect_stdout(salida):
            codigo = m.main(["toggl-md", str(self.c), "--proyecto", "42", "--nombre", "Sitio",
                             "--cliente", "9", "--cliente-nombre", "Cliente"])
        self.assertEqual(codigo, 0)
        texto = (self.c / "config.md").read_text(encoding="utf-8")
        self.assertIn("proyecto 42 «Sitio» · cliente 9 «Cliente»", texto)
        self.assertIn("| Pagos | Cobro y checkout. |", texto)
        self.assertIn("## Rama destino\n\n`main`", texto)
        with redirect_stdout(io.StringIO()):
            self.assertEqual(m.main(["toggl-md", str(self.c), "--proyecto", "42", "--nombre", "Sitio",
                                     "--cliente", "9", "--cliente-nombre", "Cliente"]), 2)

    def test_toggl_md_con_rama_destino(self):
        with redirect_stdout(io.StringIO()):
            m.main(["toggl-md", str(self.c), "--proyecto", "42", "--nombre", "Sitio",
                    "--cliente", "9", "--cliente-nombre", "Cliente", "--rama", "preview"])
        self.assertIn("## Rama destino\n\n`preview`", (self.c / "config.md").read_text(encoding="utf-8"))


class AConfig(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.c = Path(self.tmp.name)
        (self.c / "toggl.md").write_text("<!-- tarea: toggl · proyecto 1 «P» -->\n\n# Toggl · P\n\n## Rama destino\n\n`preview`\n", encoding="utf-8")
        (self.c / "para-claude.md").write_text(
            "# Para Claude\n\nEjemplo: `- **X** · A · o · delegada 2026-01-01 — y`.\n\n## Pendientes\n\n"
            "- **Corregir el menú** · General · auditoria.md:12 · delegada 2026-09-30 — que no se corte en móvil\n"
            "- una línea libre\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_sin_aplicar_no_toca_nada(self):
        r = m.a_config(self.c)
        self.assertEqual(len(r["cambios"]), 2)
        self.assertTrue((self.c / "toggl.md").exists())
        self.assertFalse((self.c / "pendientes.md").exists())

    def test_aplicar_renombra_y_convierte(self):
        m.a_config(self.c, aplicar=True)
        self.assertFalse((self.c / "toggl.md").exists())
        self.assertFalse((self.c / "para-claude.md").exists())
        config = (self.c / "config.md").read_text(encoding="utf-8")
        self.assertIn("# Configuración · P", config)
        self.assertIn("`preview`", config)
        pend = (self.c / "pendientes.md").read_text(encoding="utf-8")
        por_hacer = pend.split("## Por hacer")[1].split("## A medias")[0]
        self.assertIn("- **Corregir el menú** · General · rama — · plan — · 2026-09-30 — que no se corte en móvil"
                      " · delegada en revisión (auditoria.md:12)", por_hacer)
        self.assertIn("- una línea libre", por_hacer)

    def test_aplicar_dos_veces_no_duplica(self):
        m.a_config(self.c, aplicar=True)
        r = m.a_config(self.c, aplicar=True)
        self.assertEqual(r["cambios"], [])


if __name__ == "__main__":
    unittest.main()
