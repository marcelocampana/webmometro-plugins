---
name: agenda
description: >
  Compone la **vista diaria del usuario cruzando todos sus repos**: lee la cola `## Ahora` de cada
  `tareas/` registrado y responde qué toca hoy y si cabe en el tiempo disponible. Úsalo cuando el
  usuario pregunte "qué me toca hoy", "mi agenda", "qué tengo pendiente en todos los proyectos",
  "cuánto me cabe hoy", "cómo voy", o cuando una rutina programada pida el resumen diario. Avisa de
  lo vencido, de lo que vence hoy, de varias tareas abiertas a la vez y de las filas sin `Coste`.
  **Solo lee: nunca escribe en ninguna lista de tareas ni reordena ninguna cola.** NO lo uses para
  abrir, cerrar, crear, priorizar ni mover una tarea —eso es `tarea`, dentro del repo que
  corresponda—, ni para el detalle de un proyecto concreto. Si no hay configuración de repos, lo dice
  y ofrece crearla; no la inventa.
argument-hint: "[--hoy | --config]"
metadata:
  version: 1.2.0
---

# Agenda diaria cross-repo (agenda)

`tarea` gobierna **un** repo. El día del usuario no es un repo: es la suma de varios, cada uno con
su `tareas/`. Este skill responde a una sola pregunta —**qué toca hoy y si cabe en el tiempo que
hay**— y no hace nada más.

## Solo lee. Esa es la garantía, no un detalle

**No escribe en ningún `tareas.md`, `revisar.md`, `auditoria.md`, `secciones.md` ni `historial/`.** El
único archivo que puede crear o modificar es su propia configuración, y solo si el usuario lo pide.

Es lo que le permite correr desatendido desde una rutina: un skill que solo lee no puede dejar una
cola corrupta, ni duplicar una fila, ni pisar un cierre a medias. Cuando algo hay que cambiar —un
coste que falta, un orden que no cuadra—, **lo dice y remite a `tarea` en ese repo**; no lo
arregla.

De ahí la segunda mitad: **no reordena nada**. El orden de `## Ahora` es del usuario, igual que en
`tarea`. La agenda puede decir «por orden esto cae el viernes y vence el miércoles»; subirlo, no.

## Paso 0 · Resolver la configuración (siempre, antes de todo)

```bash
CFG="${AGENDA_CONFIG:-$HOME/Github/AI-kit/config/context/agenda.md}"
[ -f "$CFG" ] && cat "$CFG"
```

- **Existe** → paso 1.
- **No existe** → dilo en una línea y **ofrece crearla** desde `assets/agenda.esqueleto.md`, con los
  repos que el usuario nombre. **No se adivina el registro** escaneando el disco: un `tareas/` de un
  proyecto archivado metería ruido en la agenda todos los días.

**Si el usuario nombra un archivo, manda ese**, y `AGENDA_CONFIG` por delante de la ruta por
defecto: es lo que permite a una rutina apuntar a otra configuración sin tocar el skill.

La configuración lleva dos cosas: el **registro de repos** (ruta y etiqueta corta) y la **capacidad
diaria**, que es global —el día es uno solo, no uno por repo—. Su formato está en el esqueleto; una
ruta relativa se resuelve **respecto al propio archivo de configuración**, nunca respecto al
directorio desde el que se invoca.

**El orden del registro es el único orden entre repos que el usuario ha declarado**, y por eso es el
que se usa para repartir el día. No se infiere otro de la actividad reciente ni del tamaño de la cola.

## Paso 1 · Leer poco

De cada repo se lee **solo el bloque `## Ahora`**, que son filas de una línea:

```bash
sed -n '/^## Ahora/,/^---$/p' "$REPO/tareas/tareas.md" | grep '^| [0-9]'
```

**Nunca el archivo entero, nunca las secciones, nunca `historial/`, nunca `revisar.md` completo** —en
un proyecto vivo ese archivo pasa de 25 KB y no aporta nada a la vista de hoy; de él solo se cuentan
las filas. Las columnas se localizan **por nombre en la cabecera, no por posición**: hay repos en el
formato anterior, sin `Vence` ni `Coste` (`references/contrato-formato.md`).

**Un repo conectado a Toggl** (su `tareas.md` empieza con el marcador `<!-- tarea: toggl … -->`) no
tiene `Vence` ni `Coste` en la tabla: salen de Toggl con una consulta por repo, y las horas del día,
del registro de presencia (`references/toggl.md`). Sin Toggl, la agenda sigue y lo dice.

Si una ruta del registro ya no existe, **se dice en una línea al pie y se sigue con las demás**. Un
repo movido no puede dejar al usuario sin agenda.

## Paso 2 · Componer la vista

`references/vista-diaria.md`: qué entra y en qué orden, cómo se llena la capacidad, qué avisos se dan
y la plantilla de salida.

**Cabe en una pantalla.** Si necesita scroll, está fallando: la agenda no es el backlog, es lo que
toca hoy. Lo que no entra en la capacidad no se lista, se cuenta.

## Cuando la dispara una rutina

**Nadie está delante.** Una pregunta sin respuesta deja la rutina colgada y el día sin agenda, así
que corriendo desatendida el skill **no pregunta: informa y termina**. Si falta la configuración, si
una ruta no existe o si un `tareas.md` no se deja leer, eso *es* la salida de ese día.

No hace falta ninguna salvaguarda más, y ese es el argumento de que sea solo lectura: **lo peor que
puede pasar en una ejecución desatendida es un informe incompleto**, nunca una cola tocada.

La rutina se monta fuera del repo, como tarea programada del usuario, y su prompt puede pedir más
cosas —una bandeja externa, un tablero— que **no son asunto de este skill**: él entrega la vista y el
resto lo compone la rutina. Precedente en este marketplace: `seo-suite` declara sus MCP como
prerrequisito en vez de traerlos dentro.

**Lee el árbol de trabajo, no lo commiteado.** Una tarea abierta hace un minuto y sin commitear ya
sale en la agenda de mañana; un repo parado en una rama de tarea muestra el estado de esa rama.

## Qué leer según lo que se pida

| Si el usuario… | Lee |
| --- | --- |
| pide la agenda, el día, o qué le toca (por defecto) | `references/vista-diaria.md` |
| pide crear o cambiar la configuración (`--config`) | `assets/agenda.esqueleto.md` |
| tiene un repo cuya tabla no encaja, o pregunta qué columnas se leen | `references/contrato-formato.md` |
| algún repo registrado lleva el marcador `<!-- tarea: toggl … -->` | `references/toggl.md` |

## Reglas invariantes

1. **No escribe en ninguna lista de tareas ni en Toggl**, ni siquiera para corregir un error evidente.
2. **No reordena ninguna cola**, ni propone reordenar sin decir en qué repo y en qué posición.
3. **No inventa un coste.** Una fila sin `Coste` se cuenta aparte, nunca se estima aquí: estimar es de
   `tarea`, que tiene delante el historial de ese repo.
4. **No abre tareas.** Sugerir por dónde empezar sí; empezar, no.
5. **Una ruta rota no aborta la agenda**; se reporta y se sigue.

## Idioma

Español neutro. Los nombres de las tareas y de los estados, **tal cual están en cada archivo**.
