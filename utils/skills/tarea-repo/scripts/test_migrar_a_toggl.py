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
        self.r = m.armar(c, 42, 7, {"todo": 1, "in_progress": 2, "blocked": 3}, 99, "2026-09-28")

    def tearDown(self):
        self.dir.cleanup()

    def todas(self):
        return self.r["crear"] + self.r["actualizar"]

    def test_orden_ahora_primero_y_sin_las_cerradas(self):
        nombres = [t["nombre"] for t in self.r["crear"] if not t["bandeja"]]
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
        pago = self.r["actualizar"][0]["payload"]
        self.assertEqual((pago["start_date"], pago["end_date"], pago["status_id"]), ("2026-09-28", "2026-10-10", 3))
        self.assertEqual(pago["estimated_mins"], 150)

    def test_bandeja_con_etiqueta_sin_asignar_ni_fecha(self):
        [b] = [t for t in self.r["crear"] if t["bandeja"]]
        self.assertEqual(b["payload"]["tag_ids"], [99])
        self.assertNotIn("assignee_user_ids", b["payload"])
        self.assertIn("Origen: auditoría del 20-09", b["descripcion"])

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
        texto = (self.c / "toggl.md").read_text(encoding="utf-8")
        self.assertIn("proyecto 42 «Sitio» · cliente 9 «Cliente»", texto)
        self.assertIn("| Pagos | Cobro y checkout. |", texto)
        with redirect_stdout(io.StringIO()):
            self.assertEqual(m.main(["toggl-md", str(self.c), "--proyecto", "42", "--nombre", "Sitio",
                                     "--cliente", "9", "--cliente-nombre", "Cliente"]), 2)


if __name__ == "__main__":
    unittest.main()
