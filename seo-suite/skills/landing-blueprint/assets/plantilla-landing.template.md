---
tipo: plantilla-landing
cliente: "{cliente}"
patron: "{nombre del patrón — p. ej. 'landing de tratamiento'}"
aprendida_de: []          # URLs o page-snapshots de los que se derivó el esqueleto
fecha_creacion: "{AAAA-MM-DD}"
ultima_actualizacion: "{AAAA-MM-DD}"
landings_que_la_usan: []  # slugs
version: 1
---

# Plantilla de landing: {nombre del patrón}

Esqueleto estructural compartido por las landings de este patrón. **Verdad compartida a nivel de
sitio**: vive una sola vez en `contexto/plantilla-landing.md` y las landings la leen por puntero, en
vez de re-derivarla en cada corrida.

Este archivo describe **qué slots existen**, no qué contiene cada landing. Las decisiones por
servicio (usar / suprimir / adaptar) viven en el blueprint de cada landing.

> **Cómo se modifica:** un slot nuevo o eliminado afecta a todas las landings del patrón — es una
> decisión de lote. Las solicitudes de cambio se emiten desde el blueprint de una landing concreta y,
> una vez aprobadas, se registran aquí en el changelog. Nunca se edita este archivo sin confirmación
> del usuario.

---

## Slots

| # | Slot | Función de conversión | Obligatoriedad | Componente / restricción |
|---|---|---|---|---|
| 1 | {nombre del slot} | {qué hace por la conversión} | {fijo\|opcional\|suprimible} | {del sistema de diseño, o "sin restricción documentada"} |

**Obligatoriedad:**
- **Fijo** — está en todas las landings del patrón; no se suprime sin cambiar la plantilla.
- **Opcional** — existe en el esqueleto y cada landing decide si lo usa.
- **Suprimible** — está por defecto pero puede quitarse cuando el servicio no lo justifica.

---

## Restricciones transversales

{Reglas que aplican a todas las landings del patrón, independientes del servicio: una sola
conversión primaria, navegación reducida o completa, posición fija del formulario, requisitos de
compliance del rubro, etc.}

---

## Cómo se aprendió este esqueleto

| Fuente | Qué aportó | Fecha |
|---|---|---|
| {page-snapshot o URL hermana} | {slots identificados} | {fecha} |

{Si el esqueleto se derivó de landings existentes, dejar constancia de cuáles y de qué se observó:
árbol de encabezados, inventario de acciones de conversión, orden de bloques.}

---

## Changelog

| Fecha | Versión | Cambio | Origen | Aprobado por |
|---|---|---|---|---|
| {AAAA-MM-DD} | 1 | Esqueleto inicial | {de dónde se aprendió} | {usuario} |
