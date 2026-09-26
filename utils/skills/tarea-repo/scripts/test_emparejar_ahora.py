#!/usr/bin/env python3
"""Pruebas de emparejar_ahora.py: exacto, corto contra largo, reescrito, sin pareja y ids de Toggl.

    python3 -m unittest test_emparejar_ahora.py      (desde esta carpeta)
"""

import io
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import emparejar_ahora as e  # noqa: E402

TAREAS = """# Tareas

## Ahora

| # | Tarea | Sección | Estado | Vence | Coste | Nota |
| :--: | --- | --- | --- | --- | --- | --- |
| 1 | Corregir el menú móvil | General | Pendiente | — | — | — |
| 2 | Probar un pago real de punta a punta | Pagos | Pendiente | — | — | — |
| 3 | Pegar la plantilla del enlace mágico | Pagos | Pendiente | — | — | — |
| 4 | Tarea que no existe en su sección | General | Pendiente | — | — | — |
| 5 | Documentar el README <!-- toggl:123 --> | General | Pendiente | — | — | — |

---

## General

| Estado | Tarea | Vence | Coste | Inicio | Completada | Duración | Comentarios |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Pendiente | Corregir el menú móvil | — | — | — | — | — | x |
| Pendiente | Documentar el README <!-- toggl:123 --> | — | — | — | — | — | x |

## Pagos

| Estado | Tarea | Vence | Coste | Inicio | Completada | Duración | Comentarios |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Pendiente | Probar un pago real de punta a punta con las credenciales de producción | — | — | — | — | — | x |
| Pendiente | Copiar `templates/enlace.html` en las plantillas Magic Link y Confirm | — | — | — | — | — | x |
"""


class Emparejar(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8")
        self.tmp.write(TAREAS)
        self.tmp.close()
        self.pares = {p["n"]: p for p in e.emparejar(*e.leer(self.tmp.name))}

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_exacto(self):
        self.assertEqual(self.pares["1"]["tipo"], "exacto")
        self.assertNotIn("nombre_unico", self.pares["1"])

    def test_corto_contra_largo_propone_el_corto_y_mueve_el_detalle(self):
        p = self.pares["2"]
        self.assertEqual(p["tipo"], "parecido")
        self.assertEqual(p["nombre_unico"], "Probar un pago real de punta a punta")
        self.assertEqual(p["detalle_a_comentarios"], "con las credenciales de producción")

    def test_reescrito_queda_dudoso_para_confirmar(self):
        self.assertEqual(self.pares["3"]["tipo"], "dudoso")

    def test_sin_pareja(self):
        self.assertEqual(self.pares["4"]["tipo"], "sin_pareja")
        self.assertIsNone(self.pares["4"]["seccion_tarea"])

    def test_ignora_el_id_de_toggl_al_comparar(self):
        self.assertEqual(self.pares["5"]["tipo"], "exacto")

    def test_salida_1_si_hay_algo_que_confirmar(self):
        from contextlib import redirect_stdout
        with redirect_stdout(io.StringIO()):
            self.assertEqual(e.main(["x", self.tmp.name]), 1)


if __name__ == "__main__":
    unittest.main()
