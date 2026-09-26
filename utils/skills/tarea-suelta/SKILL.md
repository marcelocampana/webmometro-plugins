---
name: tarea-suelta
description: >
  Carril suelto del sistema de tareas: las tareas que no viven en ningún repositorio ni terminan en
  commit —facturar, reuniones, llamadas, trámites, responder correos, revisar algo—, registradas
  solo en Toggl 2.0 y medidas con la presencia real del usuario. Crea, empieza, pausa y termina
  tareas diciéndoselo a Claude desde cualquier sesión, sin git ni ramas, y envía el tiempo a Toggl
  en bloque al terminar. La entrada es el skill `tarea`, que decide el carril; este se usa
  directamente cuando ya está claro que es trabajo suelto ("empiezo la facturación", "terminé la
  reunión", "anota que tengo que llamar a X", "estuve 40 min en una llamada", "qué sueltas tengo").
  NO lo uses para trabajo que cambia archivos de un repo y termina en commit (eso es `tarea-repo`),
  para la vista de hoy (`agenda`) ni para planificar (`plan-semanal`).
argument-hint: "[crear | empezar | pausar | terminar | registrar | abiertas]"
metadata:
  version: 1.0.0
---

# Tareas sueltas (tarea-suelta)

Hay trabajo que ocupa tiempo y no deja commit: facturar, una reunión, una llamada, un trámite. Si no
se registra, desaparece del balance y parece que la semana rindió menos de lo que rindió. Este
carril lo mide **con la misma exactitud que el de repositorio, sin su ceremonia**.

`P=utils/skills/tarea/scripts/presencia.py` (en el repo del plugin o en su caché). En las marcas
locales, estas tareas usan `--repo suelta` y su id de Toggl.

## Dónde viven

**Solo en Toggl.** No hay fila en ningún `tareas.md`: ese markdown es la memoria de cada repo, y
estas tareas no pertenecen a ninguno.

- **Proyecto:** el del cliente al que corresponde (Toggl: cliente › proyecto), por ejemplo
  «Webmómetro › Administración». Si no existe, se propone crearlo en una línea; si ningún cliente
  encaja, se ofrece crear uno (igual que al conectar un repo: `tarea-repo/references/toggl-conexion.md`).
- **Etiqueta `suelta`** en Toggl: es lo que permite a la entrada, a `plan-semanal` y a `balance`
  distinguirlas de las de repositorio. Se crea la primera vez, con visto bueno.
- **Recurrentes** (facturar cada mes): se crea una por vez, o el usuario usa la recurrencia de la app
  de Toggl; en los dos casos llevan la etiqueta.

## El ciclo

| Momento | Toggl | Local |
| --- | --- | --- |
| **Crear** («anota que tengo que facturar») | 1 llamada: tarea con proyecto, etiqueta `suelta`, estimación si la hay y, si hay fecha, `start_date` + `end_date` | `P marca --repo suelta --tarea ID --evento crear --coste …` |
| **Empezar** («empiezo la facturación») | Nada | `P marca --repo suelta --tarea ID --evento abrir`. Si no existía, se crea antes (1 llamada) |
| **Pausar / retomar** | Nada | `--evento pausar` / `retomar` |
| **Terminar** («listo», «terminé la reunión») | 2 llamadas: registros y estado Done | `--evento cerrar`, `P tramos --repo suelta --tarea ID`, envío, `--evento enviado` |

**Terminar no pide confirmación aparte**: «listo» ya es la confirmación. No hay commit ni merge que
proteger.

**Varias abiertas a la vez** se permite (una llamada mientras factura), pero se avisa en una línea:
el tiempo de proyecto contará las dos, y el del usuario, una vez (`balance`).

## Trabajo fuera del computador

Una reunión presencial o una llamada no deja teclado ni mensajes: la presencia la daría por
ausencia y el tramo se descontaría entero. Por eso, **al terminar, si `tramos` descuenta más de
10 min**, se pregunta una sola vez:

> Descontaría 45 min sin actividad en el Mac. ¿Estuviste en la reunión fuera del computador?

- **Sí** → `P tramos … --completo`: se envía el tramo abierto entero (de `abrir` a `cerrar`).
- **No** → se envía lo medido.

## Registrar después

«Estuve 40 min en una llamada con X» (ya pasó): se crea la tarea si no existe y un registro con esa
duración terminando ahora, o a la hora que diga el usuario. Es tiempo **declarado, no medido**: la
descripción del registro lo dice («declarado»), y `balance` no lo usa para calibrar estimaciones.

## Consultar

«Qué sueltas tengo»: `P abiertas --repo suelta` para lo abierto o en pausa, más las tareas de Toggl
con la etiqueta `suelta` que no están `Done` (1 llamada). Una lista corta: nombre, proyecto, estado.

## Cuando pasa a hacerlo Claude

Si el usuario delega una tarea suelta y Claude la hace sin tocar ningún repo (preparar facturas con
un conector, redactar correos), **sigue siendo suelta**: mismo ciclo. Si empieza a producir commits,
cambia de carril (lo decide la entrada `tarea`).

## Reglas invariantes

1. **Nunca se escribe en ningún `tareas.md`.**
2. **Nada en Toggl sin visto bueno** al crear proyectos, clientes o la etiqueta; crear, empezar y
   terminar tareas se hace con lo que el usuario dijo.
3. **Tiempo medido y tiempo declarado no se mezclan**: el declarado se marca como tal.
4. **Las mismas llamadas que el carril de repo**: nada al empezar ni al pausar; 2 al terminar.
5. **Si Toggl falla**, las marcas locales quedan y el siguiente cierre lo envía; se dice en una línea.

## Idioma

Español neutro. Nombres de tareas y proyectos, tal cual.
