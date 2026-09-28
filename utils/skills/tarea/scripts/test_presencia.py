#!/usr/bin/env python3
"""Pruebas de presencia.py: ausencias, noches, trabajo desde el iPad, paralelo y envíos parciales.

    python3 -m unittest test_presencia.py      (desde esta carpeta)
"""

import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import presencia  # noqa: E402

TZ = datetime.now().astimezone().tzinfo


def t(texto):
    return datetime.fromisoformat("2026-09-26T" + texto).replace(tzinfo=TZ) if "T" not in texto \
        else datetime.fromisoformat(texto).replace(tzinfo=TZ)


def correr(*args):
    salida = io.StringIO()
    with redirect_stdout(salida):
        presencia.main(list(args))
    texto = salida.getvalue().strip()
    try:
        return json.loads(texto)
    except ValueError:
        return texto


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        os.environ["TAREA_PRESENCIA_DIR"] = self.tmp.name
        os.environ["TOGGL_CONFIG"] = os.path.join(self.tmp.name, "no-existe.md")
        os.environ["CLAUDE_PROYECTOS_DIR"] = os.path.join(self.tmp.name, "claude")

    def tearDown(self):
        self.tmp.cleanup()

    def mac(self, desde, hasta, app="Claude"):
        m = t(desde)
        while m < t(hasta):
            presencia.anotar(m, "mac", 5, app)
            m += timedelta(minutes=1)

    def mensajes(self, desde, hasta, proyecto, cada=3):
        m = t(desde)
        while m < t(hasta):
            presencia.anotar(m, "mensaje", proyecto)
            m += timedelta(minutes=cada)

    def marca(self, tarea, evento, hora, **extra):
        args = ["marca", "--repo", "repo", "--tarea", tarea, "--evento", evento, "--hora", t(hora).isoformat()]
        for k, v in extra.items():
            args += ["--" + k, v]
        correr(*args)

    def tramos(self, tarea, hasta, *mas):
        return correr("tramos", "--repo", "repo", "--tarea", tarea, "--hasta", t(hasta).isoformat(), *mas)


class Tramos(Base):
    def test_ausencia_larga_se_descuenta(self):
        self.marca("1", "crear", "09:55", coste="45m")
        self.marca("1", "abrir", "10:00")
        self.mac("10:00", "10:20")
        self.mac("10:45", "11:00")
        self.marca("1", "cerrar", "11:00")
        r = self.tramos("1", "11:00")
        self.assertEqual(r["duracion"], "35m")
        self.assertEqual(r["descontado"], "25m")
        self.assertEqual(len(r["registros"]), 2)
        self.assertEqual(r["coste"], "45m")

    def test_completo_no_recorta_una_reunion_fuera_del_mac(self):
        self.marca("R", "abrir", "10:00")
        self.mac("10:00", "10:05")
        self.marca("R", "cerrar", "10:50")
        self.assertEqual(self.tramos("R", "10:50")["duracion"], "5m")
        self.assertEqual(self.tramos("R", "10:50", "--completo")["duracion"], "50m")

    def test_hueco_corto_sigue_siendo_presencia(self):
        self.marca("1", "abrir", "10:00")
        self.mac("10:00", "10:10")
        self.mac("10:15", "10:30")
        self.marca("1", "cerrar", "10:30")
        r = self.tramos("1", "10:30")
        self.assertEqual(len(r["registros"]), 1)
        self.assertEqual(r["duracion"], "30m")

    def test_mensajes_desde_el_ipad_cuentan(self):
        self.marca("1", "abrir", "10:00")
        self.mensajes("10:00", "10:21", "repo")
        self.marca("1", "cerrar", "10:21")
        r = self.tramos("1", "10:21")
        # El último mensaje es 10:18: lo que sigue sin ninguna señal no se puede afirmar.
        self.assertEqual(r["duracion"], "19m")

    def test_noche_no_cuenta(self):
        self.marca("1", "abrir", "18:00")
        self.mac("18:00", "18:30")
        self.mac("2026-09-27T09:00", "2026-09-27T09:30")
        self.marca("1", "cerrar", "2026-09-27T09:30")
        r = self.tramos("1", "2026-09-27T09:30")
        self.assertEqual(r["duracion"], "1h 0m")

    def test_pausa_y_envio_parcial(self):
        self.marca("1", "abrir", "10:00")
        self.mac("10:00", "10:20")
        self.marca("1", "pausar", "10:20")
        self.assertEqual(len(self.tramos("1", "10:20")["registros"]), 1)
        self.marca("1", "enviado", "10:20")
        self.marca("1", "retomar", "11:00")
        self.mac("11:00", "11:10")
        self.marca("1", "cerrar", "11:10")
        r = self.tramos("1", "11:10")
        self.assertEqual(len(r["registros"]), 1)
        self.assertEqual(r["registros"][0]["duration"], 600)
        self.assertEqual(r["duracion"], "30m")
        self.assertEqual(len(self.tramos("1", "11:10", "--todo")["registros"]), 2)

    def test_determinista(self):
        self.marca("1", "abrir", "10:00")
        self.mac("10:00", "10:40")
        self.assertEqual(self.tramos("1", "10:40"), self.tramos("1", "10:40"))


class Paralelo(Base):
    def test_dos_tareas_no_duplican_tu_tiempo(self):
        self.marca("A", "abrir", "10:00")
        self.marca("B", "abrir", "10:00")
        self.mac("10:00", "10:30")
        self.mensajes("10:00", "10:15", "repo-a")
        self.mensajes("10:15", "10:30", "repo-b")
        self.marca("A", "cerrar", "10:30")
        self.marca("B", "cerrar", "10:30")
        self.assertEqual(self.tramos("A", "10:30")["duracion"], "30m")
        self.assertEqual(self.tramos("B", "10:30")["duracion"], "30m")
        r = correr("resumen", "--desde", "2026-09-26", "--hasta", "2026-09-26")
        self.assertEqual(r["total_min"], 30)
        atencion = r["dias"]["2026-09-26"]["atencion"]
        self.assertEqual(atencion["repo-a"], 15)
        self.assertEqual(atencion["repo-b"], 15)
        self.assertEqual(r["dias"]["2026-09-26"]["apps"]["Claude"], 30)


class TiempoDeClaude(Base):
    def sesion(self, nombre, lineas, proyecto="repo"):
        """lineas: (hora, tipo) con tipo `a` (respuesta de Claude) o `r` (resultado de un comando)."""
        ruta = Path(os.environ["CLAUDE_PROYECTOS_DIR"]) / "-x-" / (nombre + ".jsonl")
        ruta.parent.mkdir(parents=True, exist_ok=True)
        with open(ruta, "a", encoding="utf-8") as f:
            for hora, tipo in lineas:
                d = {"timestamp": t(hora).isoformat(), "cwd": "/no-existe/" + proyecto}
                if tipo == "a":
                    d["type"] = "assistant"
                else:
                    d.update(type="user", message={"content": [{"type": "tool_result"}]})
                f.write(json.dumps(d) + "\n")

    def cada(self, desde, hasta, minutos=2):
        m, salida = t(desde), []
        while m < t(hasta):
            salida.append((m.strftime("%H:%M"), "a"))
            m += timedelta(minutes=minutos)
        return salida

    def test_separa_con_el_usuario_y_solo(self):
        self.marca("1", "abrir", "10:00")
        self.mac("10:00", "10:20")
        self.sesion("s1", self.cada("10:00", "10:50"))
        self.marca("1", "cerrar", "11:00")
        c = self.tramos("1", "11:00")["claude"]
        self.assertEqual(c["claude"], "49m")
        self.assertEqual(c["con_usuario"], "20m")
        self.assertEqual(c["solo"], "29m")

    def test_sesiones_en_paralelo_cuentan_una_vez(self):
        self.marca("1", "abrir", "10:00")
        self.sesion("s1", self.cada("10:00", "10:30"))
        self.sesion("s2", self.cada("10:01", "10:31"))
        self.marca("1", "cerrar", "11:00")
        self.assertEqual(self.tramos("1", "11:00")["claude"]["claude"], "30m")  # por separado sumarían 58m

    def test_un_comando_largo_cuenta_entero(self):
        self.marca("1", "abrir", "10:00")
        self.sesion("s1", [("10:00", "a"), ("10:20", "r"), ("10:21", "a")])
        self.marca("1", "cerrar", "11:00")
        self.assertEqual(self.tramos("1", "11:00")["claude"]["claude"], "22m")

    def test_solo_cuenta_el_repo_y_el_tiempo_abierto(self):
        self.marca("1", "abrir", "10:00")
        self.sesion("s1", self.cada("09:00", "09:30"))
        self.sesion("s2", self.cada("10:00", "10:30"), proyecto="otro-repo")
        self.marca("1", "cerrar", "11:00")
        self.assertEqual(self.tramos("1", "11:00")["claude"]["claude_s"], 0)

    def test_resumen_por_proyecto(self):
        self.mac("10:00", "10:10")
        self.sesion("s1", self.cada("10:00", "10:30"))
        r = correr("claude", "--desde", "2026-09-26", "--hasta", "2026-09-26")["proyectos"]["repo"]
        self.assertEqual((r["claude"], r["con_usuario"], r["solo"]), ("29m", "10m", "19m"))


class Aviso(Base):
    def test_avisa_una_vez_pasado_el_umbral(self):
        ajustes = presencia.leer_ajustes()
        self.mac("09:00", "10:40")
        self.assertIsNotNone(presencia.aviso_pausa(t("10:40"), ajustes))
        self.assertIsNone(presencia.aviso_pausa(t("10:41"), ajustes))

    def test_sin_aviso_tras_una_pausa(self):
        ajustes = presencia.leer_ajustes()
        self.mac("08:00", "09:40")
        self.mac("10:00", "10:30")
        self.assertIsNone(presencia.aviso_pausa(t("10:30"), ajustes))
        self.assertEqual(presencia.sesion_actual(t("10:30"), ajustes)["minutos"], 30)


class AvisoDesdeElMac(Base):
    def setUp(self):
        super().setUp()
        self.enviadas = []
        self._notificar = presencia.notificar
        presencia.notificar = lambda titulo, texto: self.enviadas.append((titulo, texto))

    def tearDown(self):
        presencia.notificar = self._notificar
        super().tearDown()

    def test_notifica_sin_mensajes_a_claude(self):
        ajustes = presencia.leer_ajustes()
        self.mac("09:00", "10:40", app="Figma")
        presencia.avisar_desde_el_mac(t("10:40"), 5, ajustes)
        self.assertEqual(len(self.enviadas), 1)
        self.assertIn("1h 4", self.enviadas[0][1])

    def test_gancho_y_notificacion_no_avisan_dos_veces(self):
        ajustes = presencia.leer_ajustes()
        self.mac("09:00", "10:40")
        presencia.avisar_desde_el_mac(t("10:40"), 5, ajustes)
        self.assertIsNone(presencia.aviso_pausa(t("10:41"), ajustes))
        presencia.avisar_desde_el_mac(t("10:42"), 5, ajustes)
        self.assertEqual(len(self.enviadas), 1)

    def test_sin_nadie_frente_al_mac_no_notifica(self):
        ajustes = presencia.leer_ajustes()
        self.mac("09:00", "10:40")
        presencia.avisar_desde_el_mac(t("10:40"), 300, ajustes)
        self.assertEqual(self.enviadas, [])

    def test_se_puede_apagar(self):
        ajustes = dict(presencia.leer_ajustes(), notificar_mac=0)
        self.mac("09:00", "10:40")
        presencia.avisar_desde_el_mac(t("10:40"), 5, ajustes)
        self.assertEqual(self.enviadas, [])


class Plan(Base):
    SEMANA = "2026-W40"  # lunes 28-09 a domingo 04-10

    def guardar(self, tareas, hora="2026-09-27T20:00"):
        import io as _io
        viejo = sys.stdin
        sys.stdin = _io.StringIO(json.dumps(tareas))
        try:
            return correr("plan", "guardar", "--semana", self.SEMANA, "--hasta", t(hora).isoformat())
        finally:
            sys.stdin = viejo

    def test_guarda_versiones_y_compara_con_la_original(self):
        self.guardar([{"repo": "repo", "tarea": "A", "nombre": "A", "dia": "2026-09-28", "estimado_min": 60},
                      {"repo": "repo", "tarea": "B", "nombre": "B", "dia": "2026-09-29", "estimado_min": 30}])
        self.guardar([{"repo": "repo", "tarea": "B", "nombre": "B", "dia": "2026-09-30", "estimado_min": 30}],
                     hora="2026-09-29T09:00")
        self.assertEqual(len(correr("plan", "leer", "--semana", self.SEMANA)["tareas"]), 2)
        self.assertEqual(len(correr("plan", "leer", "--semana", self.SEMANA, "--vigente")["tareas"]), 1)

        self.marca("A", "abrir", "2026-09-28T10:00")
        self.mac("2026-09-28T10:00", "2026-09-28T10:40")
        self.marca("A", "cerrar", "2026-09-28T10:40")
        self.marca("C", "abrir", "2026-09-28T11:00")
        self.mac("2026-09-28T11:00", "2026-09-28T11:20")
        self.marca("C", "pausar", "2026-09-28T11:20")

        r = correr("plan", "comparar", "--semana", self.SEMANA, "--hasta", t("2026-10-04T23:00").isoformat())
        self.assertTrue(r["hay_plan"])
        self.assertEqual(r["planificado_min"], 90)
        self.assertEqual(r["real_en_plan_min"], 40)
        self.assertEqual(r["real_fuera_min"], 20)
        self.assertEqual(r["porcentaje_planificado"], 67)
        self.assertEqual((r["cumplidas"], r["planificadas"]), (1, 2))
        a = [f for f in r["tareas"] if f["tarea"] == "A"][0]
        self.assertEqual((a["real_en_su_dia_min"], a["cerrada"], a["cumplida"]), (40, "2026-09-28", True))
        self.assertEqual([f["tarea"] for f in r["fuera_de_plan"]], ["C"])

    def test_sin_plan_no_inventa(self):
        r = correr("plan", "comparar", "--semana", self.SEMANA, "--hasta", t("2026-10-04T23:00").isoformat())
        self.assertFalse(r["hay_plan"])
        self.assertIsNone(r["porcentaje_planificado"])


class Abiertas(Base):
    def test_lista_abiertas_y_pausadas_no_cerradas(self):
        self.marca("A", "abrir", "10:00")
        self.marca("B", "abrir", "10:05")
        self.marca("B", "pausar", "10:30")
        self.marca("C", "abrir", "10:10")
        self.marca("C", "cerrar", "10:40")
        self.marca("C", "enviado", "10:41")
        r = correr("abiertas", "--hasta", t("11:00").isoformat())
        self.assertEqual([(x["tarea"], x["estado"]) for x in r], [("A", "abierta"), ("B", "pausada")])
        self.assertEqual(correr("abiertas", "--repo", "otro", "--hasta", t("11:00").isoformat()), [])


if __name__ == "__main__":
    unittest.main()
