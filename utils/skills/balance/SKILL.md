---
name: balance
description: >
  Revisión del trabajo para mejorar: cruza Toggl (tiempo de proyecto), el registro de presencia
  (tiempo real del usuario, pausas y aplicaciones) y los historiales de `tareas/` para responder a
  dónde se fue el tiempo, cuánto se desvían las estimaciones, qué se repite y se podría automatizar,
  y cómo va la salud (horas frente al computador, sesiones sin pausa). Úsalo cuando el usuario pida
  "mi balance", "revisión semanal", "cómo me fue esta semana", "en qué se me va el tiempo", "cuánto le
  dedico a cada cliente", "estadísticas de Toggl", "cuánto trabajé", "cuánto tiempo frente al
  computador", "qué aplicaciones uso más", "qué podría automatizar", "cuánto trabajó Claude solo",
  "estimo bien?", o cuando una rutina programada pida el resumen de la semana. **Solo lee: nunca
  escribe en Toggl ni en ninguna lista de tareas**; lo que haya que cambiar lo propone para
  `revisar.md` y lo deja a `tarea`. NO lo uses para la vista de hoy (eso es `agenda`), ni para abrir,
  cerrar o crear tareas (eso es `tarea`).
argument-hint: "[--semana | --mes | --desde AAAA-MM-DD --hasta AAAA-MM-DD]"
metadata:
  version: 1.0.0
---

# Balance del trabajo (balance)

`agenda` responde qué toca hoy; `tarea`, qué se hace ahora. Este skill mira hacia atrás para que lo
siguiente salga mejor: **dónde se fue el tiempo, qué se estimó mal, qué se repite y cómo está el
cuerpo**. Por defecto, la semana pasada de lunes a domingo; `--mes` o un rango, si se pide.

## Solo lee

No escribe en Toggl, ni en `tareas.md`, `revisar.md` ni el historial. Así puede correr desatendido
desde una rutina: lo peor que puede pasar es un informe incompleto. Si de la revisión sale algo que
hacer —automatizar una familia de tareas, partir mejor—, **lo propone para `revisar.md`** en una
línea y lo deja a `tarea`.

## Dos medidas que nunca se suman

| Medida | Qué es | De dónde |
| --- | --- | --- |
| **Tiempo de proyecto** | Cuánto ocupó cada tarea, proyecto y cliente | Toggl: registros de tiempo |
| **Tu tiempo** | Cuánto estuvo trabajando el usuario, y en qué | `presencia.py resumen` |

Con dos sesiones en paralelo, las dos tareas cuentan el mismo tramo y el usuario lo vivió una vez.
**Sumar tiempo de proyecto para obtener horas trabajadas es el error que este skill existe para no
cometer.** Si hubo paralelo, se dice: «30h de proyecto con 18h tuyas: 1,7× en paralelo».

## Paso 0 · Qué hay

```bash
P="$HOME/Github/AI-kit/plugins/webmometro-plugins/utils/skills/tarea/scripts/presencia.py"
python3 "$P" resumen --desde "$DESDE" --hasta "$HASTA"   # tu tiempo, atención, apps, sesiones
python3 "$P" claude  --desde "$DESDE" --hasta "$HASTA"   # Claude trabajando solo
```

- **Toggl**: los registros del período en una consulta (`time-entries list` con `date_from` y
  `date_to`, 100 por página) y, si hacen falta nombres, `projects list` y `clients list`. Nunca
  registro por registro. Sin el MCP en la sesión o sin respuesta: se dice y se sigue con lo demás.
- **Sin registro de presencia** (no se instaló, o el período es anterior): se dice, y se omiten tu
  tiempo, salud y aplicaciones. No se sustituyen por Toggl: serían tiempo de proyecto.
- **Historiales**: de cada repo de la configuración de `agenda`, solo la zona `## Tareas archivadas`
  de los mensuales del período (nunca `## Comentarios`, nunca el archivo entero).

## Paso 1 · Componer

`references/informe.md`: las siete secciones, cómo se calcula cada una y la plantilla. **Cabe en una
pantalla**: cada sección, dos o tres líneas; lo que no informa, no sale.

## Reglas invariantes

1. **No escribe** en Toggl ni en ninguna lista.
2. **Nunca suma tiempo de proyecto para dar horas trabajadas.**
3. **Mediana, no media**, y **solo duraciones medidas** (sin `~`) para hablar de estimación.
4. **Sin datos, se dice**: no se rellena un hueco con un número plausible.
5. **El sesgo se enuncia en palabras**, no solo como número: «subestimas las de alinear en 2×».

## Idioma

Español neutro. Nombres de tareas, proyectos y aplicaciones, tal cual vienen. Números a la chilena:
`1h 20m`, `1,7×`.
