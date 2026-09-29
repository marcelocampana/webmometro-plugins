---
name: tarea-repo
description: >
  La parte de repositorio del sistema de tareas: para las tareas de un proyecto de Toggl enlazado a
  un repo (su `tareas/toggl.md`), pone la ceremonia de git —rama por tarea, commit, merge, push—,
  lleva el plan de Claude de cada tarea (`tareas/planes/`) y guarda la memoria del repo: el
  historial de lo cerrado y por qué (`tareas/historial/`), la revisión por áreas (`auditoria.md`) y la configuración del repo en Toggl (`toggl.md`: enlace, áreas, reglas). La lista
  de pendientes vive en Toggl y la gobierna `tarea`; este skill entra al abrir y al cerrar una tarea
  de repo, y para: montar `tareas/` en un repo nuevo (`--init`), migrar un repo con el formato
  anterior de `tareas.md` a Toggl (`--migrar`), revisar el proyecto completo (`--auditoria`), extraer
  tareas de una conversación o un archivo (`--ingerir`), ver o ascender la bandeja `por-revisar`
  (`--revisar`) y reenviar a Toggl lo que quedó pendiente (`--toggl`). Estima el coste de una tarea
  desde el historial del repo. NO lo uses para tareas de un proyecto sin repo (eso es solo `tarea`),
  para TODOs efímeros de la sesión, ni para issues de GitHub/Jira/Linear; si no existe `tareas/` y el
  usuario no pidió nada de tareas, no lo actives.
argument-hint: "[--init | --migrar | --auditoria | --ingerir | --revisar | --toggl]"
metadata:
  version: 4.4.0
---

# Tareas de repositorio (tarea-repo)

**Los pendientes viven en Toggl** (skill `tarea`). El repo guarda lo que ya se hizo y por qué, y el
trabajo de repo lleva su ceremonia: **una tarea, una rama**, y al cerrar, historial, commit y merge.
Así Claude sabe qué se ha venido haciendo sin leer una lista de pendientes en cada repo.

**Este archivo es el núcleo.** El detalle de cada modo vive en `references/`, y se lee **uno**.

## Qué leer según lo que se pida

| Si el usuario… | Lee |
| --- | --- |
| abre o cierra una tarea de este repo, o crea una | `references/modo-gestion.md` |
| pide montar `tareas/`, o no existe y pidió algo de tareas (`--init`) | `references/modo-inicio.md` |
| el repo aún tiene `tareas/tareas.md`, o pide migrar (`--migrar`) | `references/modo-migracion.md` |
| aparca algo, o asciende de la bandeja (`--revisar`) | `references/modo-revisar.md` |
| pide revisar el proyecto completo (`--auditoria`) | `references/modo-auditoria.md` |
| pasa un archivo de tareas, o pide extraerlas de la conversación (`--ingerir`) | `references/modo-ingesta.md` |

Las de apoyo —`archivado`, `contextualizacion`, `redaccion-tareas`, `estimacion`,
`historial-lectura`, `impacto-documental`— **solo cuando la del modo las cite**
para el paso que estás ejecutando. El ciclo en Toggl (crear, abrir, cerrar, registros de tiempo) es
de `tarea/references/ciclo.md`: aquí no se repite.

## Paso 0 · Precondición (siempre, antes de todo)

```bash
RAIZ=$(git rev-parse --show-toplevel) && ls "$RAIZ"/tareas/ 2>/dev/null
```

- **Existe `tareas/toggl.md`** → el repo está enlazado; lee su marcador
  (`<!-- tarea: toggl · proyecto ID «Nombre» · cliente ID «Nombre» -->`) y sus áreas.
- **Existe `tareas/tareas.md`** (o un `tareas.md` plano con `## Ahora`) → **formato anterior, sin
  migrar**. Dilo en una línea y ofrece `--migrar`. Hasta entonces, no escribas pendientes ahí.
- **No existe nada** → `modo-inicio.md` si el usuario pidió algo de tareas; **retírate en silencio**
  si no.
- **Sin git** (`git rev-parse --git-dir` falla) → el skill se detiene y lo explica en una línea.

## Qué hay en `tareas/`

```text
tareas/
├── toggl.md       Configuración del repo en Toggl: enlace, áreas, reglas y comentarios
├── auditoria.md   Hallazgos de una revisión por áreas, bajo petición
├── planes/        <id>-<slug>.md · el plan de Claude para cada tarea: pasos, skill y contexto
└── historial/     AAAA-MM.md · lo cerrado y su porqué, escrito en el mismo cierre
```

No hay lista de pendientes en el repo. La cola, la bandeja (etiqueta `por-revisar`) y los estados
están en Toggl; se leen con `tarea/scripts/cola.py leer --proyecto <ID del marcador>`.

## La ceremonia, en corto

- **Planificar:** con el usuario, qué hace falta para lograr la tarea. Los pasos de Claude, con su
  skill y su contexto, van al plan (`tareas/planes/`); lo que le toca al usuario, como subtareas en
  Toggl, que cronometra él. **Se aprueba una vez** y eso cubre la ejecución y el cierre.
- **Abrir:** `main` limpia y actualizada, y una rama nueva que describa la tarea. **Nunca se trabaja
  sobre `main`.** En Toggl, lo de `tarea`.
- **Cerrar:** **una sola confirmación**, y con ella corre la cadena entera sin pausas: tiempo y estado
  de Claude en Toggl, entrada en el historial, commit, merge y push. Solo la paran `main` sucia o desactualizada, un
  conflicto de merge o cambios ajenos a la tarea. Si el usuario encargó la tarea completa, ese encargo
  ya es el visto bueno.
- **Los pasos del plan** se encadenan sin preguntar; cada uno puede llevar su commit y se marca hecho
  en el plan, con evidencia. Al retomar, el estado en 2–3 líneas: el usuario no relee el plan.

## Comunicación ejecutiva

- **Una propuesta cabe en 2–4 líneas**; una observación, en una. Tablas antes que prosa.
- **No recapitules el contexto leído.** Se usa, no se narra.
- **La justificación larga vive en la descripción de la tarea o en el historial, no en el chat.**

> Propongo: **Corregir el desplegable del menú en móvil** (`AppHeader.vue`), área General, ~20m. ¿La creo?

## Reglas invariantes

1. **Ninguna tarea se crea sin visto bueno**; la IA no reordena la cola del usuario.
2. **Se completa una tarea y se para**; sugerir la siguiente sí, empezarla no. Los pasos de Claude no
   son tareas: viven en el plan y se encadenan hasta el cierre **sin preguntar por el siguiente paso**.
3. **El historial se escribe en el mismo cierre**, dentro de la cadena, nunca como paso aparte.
4. **Del historial se lee la sección del ancla, nunca el archivo entero** (`historial-lectura.md`).
5. **Las áreas salen de `toggl.md`**: un área nueva se añade ahí con visto bueno, no se inventa.

## Idioma

Español neutro con el usuario. El contenido del historial y de las tareas, en el idioma del proyecto.
