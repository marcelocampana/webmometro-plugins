#!/usr/bin/env python3
"""Pruebas de cola.py: sesión sin renovar, recorte de campos, vistas, copia y caídas de Toggl.

    python3 -m unittest test_cola.py      (desde esta carpeta)

Ninguna prueba toca la red: `pedir` se reemplaza por una función que devuelve páginas armadas.
"""

import io
import json
import os
import sys
import tempfile
import unittest
import urllib.error
from contextlib import redirect_stdout
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cola  # noqa: E402

AHORA = datetime(2026, 9, 28, 15, 0, tzinfo=timezone.utc)
DIA = date(2026, 9, 28)   # lunes


def cruda(id, nombre="Tarea", tipo="todo", inicio=None, fin=None, descripcion=None, notas=None, **extra):
    """Una tarea como la devuelve Toggl, con su relleno técnico."""
    t = {
        "id": id, "name": nombre, "project_id": 1, "project": {"id": 1, "name": "Webmómetro", "color": "#fff",
                                                              "permissions": ["a", "b"]},
        "client": {"id": 9, "name": "Webmómetro"}, "status": {"name": tipo.title(), "type": tipo},
        "start_date": inicio, "end_date": fin, "estimated_mins": 30, "priority": "none", "position": 65536,
        "tags": [{"id": 5, "name": "utils", "color": "#000"}], "assignee_user_ids": [7],
        "description": descripcion, "notes": notas, "time_block_total_count": 0, "metadata": {"all_day": False},
    }
    t.update(extra)
    return t


def paginas(*lotes, total=None):
    total = total if total is not None else sum(len(l) for l in lotes)

    def pedir(_sesion, pagina):
        lote = lotes[pagina - 1] if pagina <= len(lotes) else []
        return {"page": pagina, "data": lote, "total": total}
    return pedir


SESION = {"token": "x", "url": "https://focus.toggl.com", "organizacion": 1, "espacio": 2, "usuario": 7}


class Base(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        os.environ["TAREA_COLA"] = str(Path(self.dir.name) / "cola.json")
        os.environ["TOGGL_SESION"] = str(Path(self.dir.name) / "focus-tools.json")

    def tearDown(self):
        os.environ.pop("TAREA_COLA", None)
        os.environ.pop("TOGGL_SESION", None)
        self.dir.cleanup()

    def escribir_sesion(self, expira, activo="p1", token="secreto"):
        datos = {"profiles": {"p1": {"access_token": token, "refresh_token": "r", "expires_at": expira,
                                     "organization_id": 1, "workspace_id": 2, "user_id": 7,
                                     "focus_api_url": "https://focus.toggl.com/"}},
                 "active": {"mcp": activo}}
        Path(os.environ["TOGGL_SESION"]).write_text(json.dumps(datos), encoding="utf-8")


class Sesion(Base):
    def test_lee_el_perfil_activo_sin_la_barra_final(self):
        self.escribir_sesion(AHORA.timestamp() + 3600)
        s = cola.leer_sesion(momento=AHORA)
        self.assertEqual((s["organizacion"], s["espacio"], s["url"]), (1, 2, "https://focus.toggl.com"))

    def test_caducada_no_se_renueva(self):
        self.escribir_sesion(AHORA.timestamp() + 30)   # dentro del margen: se trata como caducada
        with self.assertRaises(cola.SinSesion):
            cola.leer_sesion(momento=AHORA)

    def test_sin_archivo_o_sin_perfil_activo(self):
        with self.assertRaises(cola.SinSesion):
            cola.leer_sesion(momento=AHORA)
        self.escribir_sesion(AHORA.timestamp() + 3600, activo="otro")
        with self.assertRaises(cola.SinSesion):
            cola.leer_sesion(momento=AHORA)

    def test_el_token_nunca_sale_en_el_mensaje(self):
        self.escribir_sesion(AHORA.timestamp() - 10, token="token-muy-secreto")
        with self.assertRaises(cola.SinSesion) as e:
            cola.leer_sesion(momento=AHORA)
        self.assertNotIn("token-muy-secreto", str(e.exception))


class Reducir(unittest.TestCase):
    def test_deja_lo_util_y_quita_el_relleno(self):
        t = cola.reducir(cruda(1, descripcion="Área: Informes\nQué se espera: algo", notas="Necesita la 3"))
        self.assertEqual(t["proyecto"], "Webmómetro")
        self.assertEqual(t["area"], "utils")   # la etiqueta manda sobre la descripción
        self.assertEqual(t["etiquetas"], ["utils"])

        self.assertEqual(t["notas"], "Necesita la 3")
        self.assertTrue(t["asignada"])
        texto = json.dumps(t)
        self.assertNotIn("permissions", texto)
        self.assertNotIn("color", texto)
        self.assertLess(len(texto), len(json.dumps(cruda(1))) + 60)

    def test_sin_etiqueta_de_area_usa_la_descripcion(self):
        cr = cruda(1, descripcion="Área: Informes\nAlgo")
        cr["tags"] = [{"id": 9, "name": "por-revisar"}]
        self.assertEqual(cola.reducir(cr)["area"], "Informes")
        cr["tags"] = [{"id": 8, "name": "claude"}]         # la etiqueta del tiempo de Claude no es un área
        self.assertEqual(cola.reducir(cr)["area"], "Informes")
        cr["tags"] = []
        self.assertEqual(cola.reducir(cr)["area"], "Informes")

    def test_sin_area_declarada(self):
        self.assertIsNone(cola.area_de("Qué se espera: algo"))
        self.assertIsNone(cola.area_de(None))
        self.assertEqual(cola.area_de("area: Pagos"), "Pagos")


class Vistas(unittest.TestCase):
    def setUp(self):
        crudas = [
            cruda(1, "Hoy", inicio="2026-09-28", fin="2026-09-28"),
            cruda(2, "Vencida", inicio="2026-09-25", fin="2026-09-25"),
            cruda(3, "En curso sin día", tipo="in_progress"),
            cruda(4, "Jueves", inicio="2026-10-01", fin="2026-10-01"),
            cruda(5, "Próxima semana", inicio="2026-10-06", fin="2026-10-06"),
            cruda(6, "Hecha", tipo="done", inicio="2026-09-28", fin="2026-09-28"),
            cruda(7, "Sin día"),
            cruda(8, "Madre que cruza", inicio="2026-09-27", fin="2026-10-02"),
        ]
        self.tareas = [cola.reducir(t) for t in crudas]

    def ids(self, vista, **k):
        return [t["id"] for t in cola.filtrar(self.tareas, vista, DIA, **k)]

    def test_hoy_en_curso_primero_luego_vencidas_y_las_del_dia(self):
        self.assertEqual(self.ids("hoy"), [3, 2, 1, 8])

    def test_semana_de_lunes_a_domingo_mas_lo_vencido(self):
        self.assertEqual(self.ids("semana"), [3, 2, 1, 4, 8])

    def test_pendientes_no_incluye_lo_hecho(self):
        self.assertNotIn(6, self.ids("pendientes"))
        self.assertEqual(len(self.ids("pendientes")), 7)

    def test_la_tarea_y_tu_subtarea_salen_en_el_dia(self):
        # La tarea es tu objetivo (y lleva el tiempo de Claude); la subtarea, lo que haces tú.
        tarea = cola.reducir(cruda(20, "Tarea", inicio="2026-09-28", fin="2026-09-28", sub_task_total_count=1))
        tuya = cola.reducir(cruda(21, "Tuya", inicio="2026-09-28", fin="2026-09-28", parent_task_id=20))
        tareas = [tarea, tuya]
        self.assertEqual([t["id"] for t in cola.filtrar(tareas, "hoy", DIA)], [20, 21])
        self.assertEqual([t["id"] for t in cola.filtrar(tareas, "pendientes", DIA)], [20, 21])

    def test_filtro_por_proyecto(self):
        self.assertEqual(self.ids("pendientes", proyecto="999"), [])


class Texto(unittest.TestCase):
    def test_hoy_muestra_todo_y_semana_solo_la_primera_linea(self):
        t = cola.reducir(cruda(1, "Pagar", descripcion="Área: Pagos\nPrimera\nSegunda", notas="Nota larga"))
        completo = cola.texto([t], completo=True)
        breve = cola.texto([t], completo=False)
        self.assertIn("área utils", completo)
        self.assertNotIn("#utils", completo)   # el área no se repite como etiqueta
        self.assertIn("Segunda", completo)
        self.assertIn("Nota larga", completo)
        self.assertIn("Primera", breve)
        self.assertNotIn("Segunda", breve)
        self.assertNotIn("Nota larga", breve)

    def test_formato_de_minutos_y_dias(self):
        self.assertEqual(cola.fmt_min(90), "1h 30m")
        self.assertEqual(cola.fmt_min(None), "—")
        self.assertEqual(cola.fmt_dia({"inicio": "2026-09-30", "fin": "2026-10-06"}), "30-09 a 06-10")


class Obtener(Base):
    def test_trae_todas_las_paginas(self):
        pedir = paginas([cruda(1), cruda(2)], [cruda(3)], total=3)
        tareas, origen, _ = cola.obtener(10, False, AHORA, pedir, SESION)
        self.assertEqual([t["id"] for t in tareas], [1, 2, 3])
        self.assertIn("recién", origen)

    def test_reutiliza_la_copia_reciente_sin_ir_a_la_red(self):
        cola.obtener(10, False, AHORA, paginas([cruda(1)]), SESION)

        def no_debe_llamarse(*_):
            raise AssertionError("fue a la red con una copia reciente")
        tareas, origen, _ = cola.obtener(10, False, AHORA, no_debe_llamarse, SESION)
        self.assertEqual(origen, "copia de hace 0 min")
        self.assertEqual(len(tareas), 1)

    def test_invalidar_obliga_a_ir_a_la_red(self):
        cola.obtener(10, False, AHORA, paginas([cruda(1)]), SESION)
        with redirect_stdout(io.StringIO()):
            cola.main(["invalidar"])
        tareas, origen, _ = cola.obtener(10, False, AHORA, paginas([cruda(1), cruda(2)]), SESION)
        self.assertIn("recién", origen)
        self.assertEqual(len(tareas), 2)

    def test_si_toggl_falla_usa_la_copia_y_lo_avisa(self):
        cola.obtener(10, False, AHORA, paginas([cruda(1)]), SESION)

        def caida(*_):
            raise urllib.error.URLError("sin red")
        tareas, origen, aviso = cola.obtener(10, True, AHORA, caida, SESION)
        self.assertEqual(len(tareas), 1)
        self.assertIn("no respondió", aviso)

    def test_un_401_es_sesion_caducada(self):
        def rechazo(*_):
            raise urllib.error.HTTPError("u", 401, "Unauthorized", {}, None)
        with self.assertRaises(cola.SinSesion):
            cola.obtener(10, True, AHORA, rechazo, SESION)


if __name__ == "__main__":
    unittest.main()
