#!/usr/bin/env python3
"""Pruebas de guardia_git.py: ramas protegidas, permiso de un solo uso por sesión, vencimiento,
variantes del comando, autoprotección y que falla cerrado."""

import io
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from contextlib import redirect_stderr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import guardia_git as g  # noqa: E402


def sh(cwd, *args):
    subprocess.run(["git", "-C", str(cwd), *args], check=True, capture_output=True)


class Guardia(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        os.environ["GUARDIA_APROBACIONES"] = str(base / "aprobaciones")
        os.environ["GUARDIA_PLUGINS"] = str(base / "plugins")
        self.remoto = base / "remoto.git"
        sh(base, "init", "-q", "--bare", "-b", "main", str(self.remoto))
        self.r = base / "repo"
        self.r.mkdir()
        sh(self.r, "init", "-q", "-b", "main")
        sh(self.r, "config", "user.email", "t@t")
        sh(self.r, "config", "user.name", "t")
        (self.r / "README.md").write_text("x\n", encoding="utf-8")
        (self.r / "tareas").mkdir()
        (self.r / "tareas" / "pendientes.md").write_text("# P\n", encoding="utf-8")
        sh(self.r, "add", "-A")
        sh(self.r, "commit", "-qm", "inicio")
        sh(self.r, "remote", "add", "origin", str(self.remoto))
        sh(self.r, "push", "-q", "-u", "origin", "main")

    def tearDown(self):
        self.tmp.cleanup()

    def bloquea(self, cmd, sesion="s1", ahora=None):
        with self.assertRaises(g.Bloqueo):
            g.revisar_bash(cmd, str(self.r), sesion, ahora)

    def pasa(self, cmd, sesion="s1", ahora=None):
        g.revisar_bash(cmd, str(self.r), sesion, ahora)

    def main_adelantada(self):
        """main con un merge local que aún no está en el remoto: hay algo que subir."""
        self.rama_con_trabajo()
        sh(self.r, "merge", "-q", "--no-ff", "-m", "merge", "arreglo")

    def rama_con_trabajo(self, nombre="arreglo"):
        sh(self.r, "switch", "-qc", nombre)
        (self.r / "a.txt").write_text("a\n", encoding="utf-8")
        sh(self.r, "add", "-A")
        sh(self.r, "commit", "-qm", "trabajo")
        sh(self.r, "switch", "-q", "main")

    # ── commits ──
    def test_commit_en_main_se_bloquea(self):
        (self.r / "README.md").write_text("y\n", encoding="utf-8")
        sh(self.r, "add", "-A")
        self.bloquea('git commit -m "cambio; con punto y coma"')

    def test_commit_en_una_rama_pasa(self):
        sh(self.r, "switch", "-qc", "trabajo")
        (self.r / "README.md").write_text("y\n", encoding="utf-8")
        sh(self.r, "add", "-A")
        self.pasa("git commit -m x")

    def test_commit_de_solo_pendientes_en_main_pasa(self):
        (self.r / "tareas" / "pendientes.md").write_text("# P\n- algo\n", encoding="utf-8")
        sh(self.r, "add", "-A")
        self.pasa("git commit -m 'tareas: pendientes'")

    def test_commit_am_que_arrastra_otros_archivos_se_bloquea(self):
        (self.r / "tareas" / "pendientes.md").write_text("# P\n- algo\n", encoding="utf-8")
        sh(self.r, "add", "tareas/pendientes.md")
        (self.r / "README.md").write_text("y\n", encoding="utf-8")
        self.bloquea("git commit -am 'tareas: pendientes'")

    def test_primer_commit_de_un_repo_vacio_pasa(self):
        vacio = Path(self.tmp.name) / "vacio"
        vacio.mkdir()
        sh(vacio, "init", "-q", "-b", "main")
        g.revisar_bash("git commit -m inicio", str(vacio), "s1")

    def test_rama_destino_declarada_tambien_se_protege(self):
        (self.r / "tareas" / "toggl.md").write_text("## Rama destino\n\n`preview`\n", encoding="utf-8")
        sh(self.r, "switch", "-qc", "preview")
        (self.r / "README.md").write_text("y\n", encoding="utf-8")
        sh(self.r, "add", "README.md")
        self.bloquea("git commit -m x")

    # ── merge y push ──
    def test_merge_y_push_a_main_se_bloquean(self):
        self.rama_con_trabajo()
        self.bloquea("git merge --no-ff arreglo")
        sh(self.r, "merge", "-q", "--no-ff", "-m", "merge", "arreglo")
        self.bloquea("git push origin main")
        self.bloquea("git push")

    def test_variantes_del_comando(self):
        self.rama_con_trabajo()
        afuera = Path(self.tmp.name)
        g.revisar_bash("ls", str(afuera), "s1")
        with self.assertRaises(g.Bloqueo):
            g.revisar_bash("git -C %s merge arreglo" % self.r, str(afuera), "s1")
        with self.assertRaises(g.Bloqueo):
            g.revisar_bash("cd %s && git merge arreglo" % self.r, str(afuera), "s1")
        sh(self.r, "switch", "-q", "arreglo")
        self.bloquea("git push origin HEAD:main")
        self.bloquea("git push origin +arreglo:refs/heads/main")
        self.bloquea("git push --all origin")
        self.bloquea("gh pr merge 12 --squash")
        self.pasa("git push -u origin arreglo")

    def test_aprobacion_da_un_merge_y_un_push_una_sola_vez(self):
        self.rama_con_trabajo()
        g.registrar_aprobacion("s1")
        self.pasa("git merge --no-ff arreglo")
        self.bloquea("git merge --no-ff otra")
        sh(self.r, "merge", "-q", "--no-ff", "-m", "merge", "arreglo")
        self.pasa("git push origin main")
        self.bloquea("git push origin main")

    def test_aprobacion_de_otra_sesion_no_sirve(self):
        self.rama_con_trabajo()
        g.registrar_aprobacion("otra-sesion")
        self.bloquea("git merge arreglo", sesion="s1")

    def test_aprobacion_vence_a_los_10_minutos(self):
        self.rama_con_trabajo()
        g.registrar_aprobacion("s1", ahora=time.time() - 601)
        self.bloquea("git merge arreglo")

    def test_aprobacion_queda_atada_al_primer_repo(self):
        self.rama_con_trabajo()
        otro = Path(self.tmp.name) / "otro"
        otro.mkdir()
        sh(otro, "init", "-q", "-b", "main")
        sh(otro, "config", "user.email", "t@t")
        sh(otro, "config", "user.name", "t")
        sh(otro, "commit", "-q", "--allow-empty", "-m", "i")
        sh(otro, "switch", "-qc", "b")
        sh(otro, "commit", "-q", "--allow-empty", "-m", "b")
        sh(otro, "switch", "-q", "main")
        g.registrar_aprobacion("s1")
        self.pasa("git merge arreglo")
        with self.assertRaises(g.Bloqueo):
            g.revisar_bash("git merge b", str(otro), "s1")

    def test_frase_de_aprobacion(self):
        self.assertTrue(g.es_aprobacion("Se ve bien. Apruebo el merge"))
        self.assertTrue(g.es_aprobacion("APRUEBO  EL MERGE"))
        self.assertFalse(g.es_aprobacion("no apruebo el merge"))
        self.assertFalse(g.es_aprobacion("complétala y haz el merge"))

    def test_push_de_solo_pendientes_a_main_pasa_sin_permiso(self):
        (self.r / "tareas" / "pendientes.md").write_text("# P\n- algo\n", encoding="utf-8")
        sh(self.r, "commit", "-qam", "tareas: pendientes")
        self.pasa("git push origin main")

    def test_ponerse_al_dia_con_el_remoto_pasa(self):
        self.pasa("git pull")
        self.pasa("git pull origin main")
        self.pasa("git merge --ff-only origin/main")
        self.pasa("git fetch && git status")

    def test_forzar_o_borrar_main_se_bloquea(self):
        self.bloquea("git branch -f main HEAD~1")
        self.bloquea("git switch -C main")
        self.bloquea("git push origin :main")
        self.bloquea("git update-ref refs/heads/main HEAD")

    # ── autoprotección y fallo cerrado ──
    def test_escribir_en_los_permisos_se_bloquea(self):
        aprob = os.environ["GUARDIA_APROBACIONES"]
        self.bloquea("echo '{}' > %s/s1.json" % aprob)
        self.bloquea("rm -rf ~/.claude/plugins/cache/x")
        with self.assertRaises(g.Bloqueo):
            g.revisar_edicion(aprob + "/s1.json")
        self.pasa("ls %s 2>/dev/null" % aprob)

    def test_mensaje_del_usuario_registra_el_permiso(self):
        entrada = json.dumps({"session_id": "s9", "prompt": "apruebo el merge"})
        sys_stdin = sys.stdin
        try:
            sys.stdin = io.StringIO(entrada)
            with redirect_stderr(io.StringIO()):
                import contextlib
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(g.main(["mensaje"]), 0)
        finally:
            sys.stdin = sys_stdin
        self.assertTrue(g.archivo_permiso("s9").exists())

    def test_falla_cerrado(self):
        entrada = json.dumps({"tool_name": "Bash", "session_id": "s1", "cwd": str(self.r),
                              "tool_input": {"command": "git status"}})
        os.environ["GUARDIA_FORZAR_ERROR"] = "1"
        sys_stdin = sys.stdin
        try:
            sys.stdin = io.StringIO(entrada)
            with redirect_stderr(io.StringIO()) as err:
                self.assertEqual(g.main(["pre"]), 2)
            self.assertIn("bloqueo", err.getvalue())
        finally:
            sys.stdin = sys_stdin
            del os.environ["GUARDIA_FORZAR_ERROR"]

    def test_comando_ajeno_a_git_pasa(self):
        self.pasa("python3 -m unittest && ls -la")


if __name__ == "__main__":
    unittest.main()
