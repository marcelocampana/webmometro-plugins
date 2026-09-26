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


if __name__ == "__main__":
    unittest.main()
