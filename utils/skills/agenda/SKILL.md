---
name: agenda
description: >
  Compone la **vista diaria del usuario cruzando todos sus repos**: lee la cola `## Ahora` de cada
  `tareas/` registrado y responde qué toca hoy y si cabe en el tiempo disponible. Úsalo cuando el
  usuario pregunte "qué me toca hoy", "mi agenda", "qué tengo pendiente en todos los proyectos",
  "cuánto me cabe hoy", "cómo voy", o cuando una rutina programada pida el resumen diario. Avisa de
  lo vencido, de lo que vence hoy, de varias tareas abiertas a la vez y de las filas sin `Coste`.
  **Solo lee: nunca escribe en ninguna lista de tareas ni reordena ninguna cola.** NO lo uses para
  abrir, cerrar, crear, priorizar ni mover una tarea —eso es `task-flow`, dentro del repo que
  corresponda—, ni para el detalle de un proyecto concreto. Si no hay configuración de repos, lo dice
  y ofrece crearla; no la inventa.
argument-hint: "[--hoy | --config]"
metadata:
  version: 1.0.0
---

# Agenda diaria cross-repo (agenda)

`task-flow` gobierna **un** repo. El día del usuario no es un repo: es la suma de varios, cada uno con
su `tareas/`. Este skill responde a una sola pregunta —**qué toca hoy y si cabe en el tiempo que
hay**— y no hace nada más.

## Solo lee. Esa es la garantía, no un detalle

**No escribe en ningún `tareas.md`, `revisar.md`, `auditoria.md`, `secciones.md` ni `historial/`.** El
único archivo que puede crear o modificar es su propia configuración, y solo si el usuario lo pide.

Es lo que le permite correr desatendido desde una rutina: un skill que solo lee no puede dejar una
cola corrupta, ni duplicar una fila, ni pisar un cierre a medias. Cuando algo hay que cambiar —un
coste que falta, un orden que no cuadra—, **lo dice y remite a `task-flow` en ese repo**; no lo
arregla.

De ahí la segunda mitad: **no reordena nada**. El orden de `## Ahora` es del usuario, igual que en
`task-flow`. La agenda puede decir «por orden esto cae el viernes y vence el miércoles»; subirlo, no.

## Paso 0 · Resolver la configuración (siempre, antes de todo)

```bash
CFG="${AGENDA_CONFIG:-$HOME/Documents/config/claude/agenda.md}"
[ -f "$CFG" ] || CFG="$HOME/.claude/agenda.md"
[ -f "$CFG" ] && cat "$CFG"
```

- **Existe** → paso 1.
- **No existe** → dilo en una línea y **ofrece crearla** desde `assets/agenda.esqueleto.md`, con los
  repos que el usuario nombre. **No se adivina el registro** escaneando el disco: un `tareas/` de un
  proyecto archivado metería ruido en la agenda todos los días.

**Si el usuario nombra un archivo, manda ese**, y `AGENDA_CONFIG` por delante de las dos rutas por
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

Si una ruta del registro ya no existe, **se dice en una línea al pie y se sigue con las demás**. Un
repo movido no puede dejar al usuario sin agenda.

## Paso 2 · Componer la vista

`references/vista-diaria.md`: qué entra y en qué orden, cómo se llena la capacidad, qué avisos se dan
y la plantilla de salida.

**Cabe en una pantalla.** Si necesita scroll, está fallando: la agenda no es el backlog, es lo que
toca hoy. Lo que no entra en la capacidad no se lista, se cuenta.

## Qué leer según lo que se pida

| Si el usuario… | Lee |
| --- | --- |
| pide la agenda, el día, o qué le toca (por defecto) | `references/vista-diaria.md` |
| pide crear o cambiar la configuración (`--config`) | `assets/agenda.esqueleto.md` |
| tiene un repo cuya tabla no encaja, o pregunta qué columnas se leen | `references/contrato-formato.md` |

## Reglas invariantes

1. **No escribe en ninguna lista de tareas**, ni siquiera para corregir un error evidente.
2. **No reordena ninguna cola**, ni propone reordenar sin decir en qué repo y en qué posición.
3. **No inventa un coste.** Una fila sin `Coste` se cuenta aparte, nunca se estima aquí: estimar es de
   `task-flow`, que tiene delante el historial de ese repo.
4. **No abre tareas.** Sugerir por dónde empezar sí; empezar, no.
5. **Una ruta rota no aborta la agenda**; se reporta y se sigue.

## Idioma

Español neutro. Los nombres de las tareas y de los estados, **tal cual están en cada archivo**.
