#!/usr/bin/env python3
"""Pruebas de pendientes.py: captura idempotente de ramas sin mergear, plan, cambios sin commitear y listado."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import os  # noqa: E402

import pendientes as p  # noqa: E402

PLAN = """<!-- tarea: plan · slug arreglar-menu · rama arreglar-menu · área General · coste ~30m -->

# Arreglar el menú en móvil

## Pasos

| # | Paso | Skill | Contexto | Hecho |
| --- | --- | --- | --- | --- |
| 1 | Reproducir | ninguna | AppHeader.vue | ✓ commit a1b2c3 |
| 2 | Corregir | ninguna | AppHeader.vue | |
| 3 | Probar | ninguna | — | |
"""


def sh(raiz, *args):
    subprocess.run(["git", "-C", str(raiz), *args], check=True, capture_output=True)


class Repo(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.r = Path(self.tmp.name)
        sh(self.r, "init", "-q", "-b", "main")
        sh(self.r, "config", "user.email", "t@t")
        sh(self.r, "config", "user.name", "t")
        (self.r / "tareas").mkdir()
        (self.r / "tareas" / "config.md").write_text("# Configuración · X\n\n## Rama destino\n\n`main`\n", encoding="utf-8")
        (self.r / "README.md").write_text("x\n", encoding="utf-8")
        sh(self.r, "add", "-A")
        sh(self.r, "commit", "-qm", "inicio")

    def tearDown(self):
        self.tmp.cleanup()

    def rama_con_plan(self, nombre="arreglar-menu"):
        sh(self.r, "switch", "-qc", nombre)
        (self.r / "tareas" / "planes").mkdir(exist_ok=True)
        (self.r / "tareas" / "planes" / (nombre + ".md")).write_text(PLAN, encoding="utf-8")
        sh(self.r, "add", "-A")
        sh(self.r, "commit", "-qm", "plan")
        sh(self.r, "switch", "-q", "main")

    def pendientes(self):
        return (self.r / "tareas" / "pendientes.md").read_text(encoding="utf-8")

    def test_rama_sin_mergear_entra_una_sola_vez(self):
        self.rama_con_plan()
        self.assertEqual(p.capturar(self.r, "2026-10-02"), ["arreglar-menu"])
        texto = self.pendientes()
        a_medias = texto.split("## A medias")[1].split("## Espera")[0]
        self.assertIn("- **Arreglar el menú en móvil** · General · rama `arreglar-menu` · plan `tareas/planes/arreglar-menu.md`", a_medias)
        self.assertIn("faltan 2 de 3 pasos · sesión cerrada sin cierre", a_medias)
        self.assertEqual(p.capturar(self.r, "2026-10-02"), [])
        self.assertEqual(self.pendientes(), texto)

    def test_plan_del_modo_plan_en_la_carpeta_de_claude(self):
        planes = Path(self.tmp.name) / "plans"
        planes.mkdir()
        os.environ["PLANES_CLAUDE"] = str(planes)
        try:
            repo = self.r.name
            texto = PLAN.replace("<!-- tarea: plan · slug arreglar-menu · rama arreglar-menu",
                                 "<!-- tarea: plan · repo %s · rama otro-arreglo" % repo)
            (planes / "shimmering-wombat.md").write_text(texto, encoding="utf-8")
            (planes / "ajeno.md").write_text("<!-- tarea: plan · repo otro · rama otro-arreglo -->\n# Ajeno\n", encoding="utf-8")
            sh(self.r, "switch", "-qc", "otro-arreglo")
            sh(self.r, "commit", "-q", "--allow-empty", "-m", "x")
            sh(self.r, "switch", "-q", "main")
            self.assertEqual(p.capturar(self.r, "2026-10-03"), ["otro-arreglo"])
            a_medias = self.pendientes().split("## A medias")[1]
            self.assertIn("**Arreglar el menú en móvil** · General · rama `otro-arreglo`", a_medias)
            self.assertIn("plan `%s`" % (planes / "shimmering-wombat.md"), a_medias)
            self.assertIn("faltan 2 de 3 pasos", a_medias)
        finally:
            del os.environ["PLANES_CLAUDE"]

    def test_marcador_exige_el_nombre_entero(self):
        marca = "<!-- tarea: plan · repo webmometro-web-reports · rama utils/copia-toggl · área utils -->"
        self.assertTrue(p.marcador_de(marca, "webmometro-web-reports", "utils/copia-toggl"))
        self.assertFalse(p.marcador_de(marca, "webmometro", "utils/copia-toggl"))
        self.assertFalse(p.marcador_de(marca, "webmometro-web-reports", "utils"))
        self.assertTrue(p.marcador_de("<!-- plan · repo r · rama x-->", "r", "x"))

    def test_lo_capturado_sale_al_mergearse(self):
        self.rama_con_plan()
        self.rama_con_plan("otra")
        self.assertEqual(p.capturar(self.r, "2026-10-02"), ["arreglar-menu", "otra"])
        sh(self.r, "merge", "-q", "--no-ff", "-m", "Merge arreglar-menu: listo", "arreglar-menu")
        sh(self.r, "branch", "-d", "arreglar-menu")          # borrada: cuenta el merge en la base
        sh(self.r, "merge", "-q", "--no-ff", "-m", "integra", "otra")  # viva: cuenta que sea ancestro
        self.assertEqual(p.capturar(self.r, "2026-10-03"), [])
        a_medias = self.pendientes().split("## A medias")[1].split("## Espera")[0]
        self.assertEqual(a_medias.strip(), "")

    def test_lo_escrito_a_mano_no_se_retira(self):
        self.rama_con_plan()
        a_mano = "- **Arreglar el menú** · General · rama `arreglar-menu` · plan — · 2026-10-01 — falta probar"
        (self.r / "tareas" / "pendientes.md").write_text(
            p.ESQUELETO.read_text(encoding="utf-8").replace("## A medias\n", "## A medias\n\n" + a_mano + "\n"),
            encoding="utf-8")
        sh(self.r, "merge", "-q", "--no-ff", "-m", "Merge arreglar-menu", "arreglar-menu")
        p.capturar(self.r, "2026-10-03")
        self.assertIn(a_mano, self.pendientes())

    def test_rama_borrada_sin_merge_no_se_retira(self):
        self.rama_con_plan()
        p.capturar(self.r, "2026-10-02")
        sh(self.r, "branch", "-D", "arreglar-menu")
        p.capturar(self.r, "2026-10-03")
        self.assertIn("rama `arreglar-menu`", self.pendientes())

    def test_rama_mergeada_no_entra(self):
        self.rama_con_plan()
        sh(self.r, "merge", "-q", "--no-ff", "-m", "merge", "arreglar-menu")
        self.assertEqual(p.capturar(self.r), [])
        self.assertFalse((self.r / "tareas" / "pendientes.md").exists())

    def test_rama_nueva_con_cambios_sin_commitear(self):
        sh(self.r, "switch", "-qc", "probar-algo")
        (self.r / "README.md").write_text("cambiado\n", encoding="utf-8")
        self.assertEqual(p.capturar(self.r, "2026-10-02"), ["probar-algo"])
        self.assertIn("sin plan; cambios sin commitear", self.pendientes())

    def test_rama_destino_declarada_no_se_captura(self):
        (self.r / "tareas" / "config.md").write_text("## Rama destino\n\n`preview`\n", encoding="utf-8")
        sh(self.r, "commit", "-qam", "destino")
        sh(self.r, "branch", "preview")
        sh(self.r, "switch", "-qc", "otra")
        (self.r / "x.txt").write_text("x", encoding="utf-8")
        sh(self.r, "add", "-A")
        sh(self.r, "commit", "-qm", "x")
        sh(self.r, "switch", "-q", "preview")
        self.assertEqual(p.capturar(self.r), ["otra"])

    def test_sin_carpeta_tareas_no_hace_nada(self):
        with tempfile.TemporaryDirectory() as d:
            sh(Path(d), "init", "-q")
            self.assertEqual(p.capturar(d), [])
            self.assertFalse((Path(d) / "tareas").exists())

    def test_formato_antiguo_no_se_toca(self):
        (self.r / "tareas" / "config.md").unlink()
        (self.r / "tareas" / "tareas.md").write_text("## Ahora\n", encoding="utf-8")
        sh(self.r, "add", "-A")
        sh(self.r, "commit", "-qm", "formato antiguo")
        self.rama_con_plan()
        self.assertEqual(p.capturar(self.r), [])
        self.assertFalse((self.r / "tareas" / "pendientes.md").exists())

    def test_utils5_con_toggl_md_si_se_captura(self):
        (self.r / "tareas" / "config.md").rename(self.r / "tareas" / "toggl.md")
        sh(self.r, "add", "-A")
        sh(self.r, "commit", "-qm", "utils 5")
        self.rama_con_plan()
        self.assertEqual(p.capturar(self.r), ["arreglar-menu"])

    def test_listar_ordena_por_antiguedad(self):
        (self.r / "tareas" / "pendientes.md").write_text(
            "# Pendientes\n\n## Por hacer\n\n- **A** · G · rama — · plan — · 2026-09-30 — x · y\n"
            "- **B** · G · rama — · plan — · 2026-09-01 — x · y\n\n## A medias\n\n## Espera tu decisión\n",
            encoding="utf-8")
        (self.r / "tareas" / "por-revisar.md").write_text(
            "# Bandeja\n\n- **Idea** · G · origen · 2026-08-15 — porque\n", encoding="utf-8")
        r = p.listar(self.r, "2026-10-02")
        self.assertEqual([e["texto"][:5] for e in r["pendientes"]["Por hacer"]], ["**B**", "**A**"])
        self.assertEqual(r["pendientes"]["Por hacer"][0]["dias"], 31)
        self.assertEqual(r["bandeja"], {"entradas": 1, "mas_antigua": "2026-08-15"})
        self.assertFalse(r["sin_migrar"])

    def test_insertar_respeta_las_otras_secciones(self):
        texto = "## Por hacer\n\n- uno\n\n## A medias\n\n## Espera tu decisión\n\n- dos\n"
        nuevo = p.insertar(texto, "A medias", ["- tres"])
        self.assertEqual(nuevo, "## Por hacer\n\n- uno\n\n## A medias\n\n- tres\n\n## Espera tu decisión\n\n- dos\n")


if __name__ == "__main__":
    unittest.main()
