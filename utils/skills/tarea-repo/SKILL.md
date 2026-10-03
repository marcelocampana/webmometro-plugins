---
name: tarea-repo
description: >
  La parte de repositorio del sistema de tareas: el trabajo de Claude en un repo con `tareas/`. Pone
  la ceremonia de git —rama por tarea, commits como puntos de guardado, merge y push con la
  aprobación del usuario—, sigue el plan de Claude (el del modo plan, en `~/.claude/plans/`, con
  su tabla de pasos y «Esto te toca a ti») y la memoria del repo: el historial de lo cerrado y lo descartado, con su
  porqué (`tareas/historial/`), lo decidido que aún no se hace o quedó a medias
  (`tareas/pendientes.md`), la bandeja de lo anotado sin decidir (`tareas/por-revisar.md`), la
  revisión por áreas (`auditoria.md`) y la configuración del repo (`config.md`: rama destino, áreas,
  enlace a Toggl, reglas). Toggl es del usuario y lo lleva él: aquí no se abre ni se cierra nada
  allá. Úsalo al empezar o cerrar trabajo en un repo con `tareas/`, cuando el usuario pregunte "qué
  quedó pendiente", "sigue con X", "anota esto", "revisemos la bandeja", y para: montar `tareas/` en
  un repo nuevo (`--init`), migrar un repo con un formato anterior (`--migrar`: el `tareas.md`
  antiguo o el `toggl.md` de utils 5), revisar el proyecto completo (`--auditoria`) y extraer tareas
  de una conversación o un archivo (`--ingerir`). Estima el coste de una tarea desde el historial
  del repo. NO lo uses para lo que solo toca Toggl (eso es `tarea`), para TODOs efímeros de la
  sesión, ni para issues de GitHub/Jira/Linear; si no existe `tareas/` y el usuario no pidió nada de
  tareas, no lo actives.
argument-hint: "[--init | --migrar | --auditoria | --ingerir | --revisar]"
metadata:
  version: 6.1.1
---

# Tareas de repositorio (tarea-repo)

El trabajo de Claude en un repo se organiza con **su plan y su rama**; lo que queda sin hacer, en
`pendientes.md`; lo hecho y lo descartado, con su porqué, en el historial. **Nada de lo decidido se
pierde**: cada pendiente sale de una sola forma, al historial. Toggl es del usuario (`tarea`).

**Este archivo es el núcleo.** El detalle de cada modo vive en `references/`, y se lee **uno**.

## Qué leer según lo que se pida

| Si el usuario… | Lee |
| --- | --- |
| empieza o cierra trabajo de Claude en este repo | `references/modo-gestion.md` |
| pregunta qué quedó pendiente, o pide retomar algo | `references/modo-pendientes.md` |
| pide montar `tareas/`, o no existe y pidió algo de tareas (`--init`) | `references/modo-inicio.md` |
| el repo tiene un formato anterior, o pide migrar (`--migrar`) | `references/modo-migracion.md` |
| anota o aparca algo, o revisa la bandeja (`--revisar`) | `references/modo-revisar.md` |
| pide revisar el proyecto completo (`--auditoria`) | `references/modo-auditoria.md` |
| pasa un archivo de tareas, o pide extraerlas de la conversación (`--ingerir`) | `references/modo-ingesta.md` |

Las de apoyo —`archivado`, `contextualizacion`, `redaccion-tareas`, `estimacion`,
`historial-lectura`, `impacto-documental`— **solo cuando la del modo las cite**. Crear en Toggl y
el tiempo de Claude son de `tarea/references/ciclo.md`: aquí no se repiten.

## Paso 0 · Precondición (siempre, antes de todo)

```bash
RAIZ=$(git rev-parse --show-toplevel) && ls "$RAIZ"/tareas/ 2>/dev/null
```

- **Existe `tareas/config.md`** → el repo está al día; lee su rama destino y sus áreas.
- **Existe `tareas/toggl.md` y no `config.md`** (o un `para-claude.md`) → **utils 5, sin migrar**.
  Dilo en una línea y ofrece `--migrar`. Hasta entonces, se lee `toggl.md` como si fuera `config.md`.
- **Existe `tareas/tareas.md`** (o un `tareas.md` plano con `## Ahora`) → **formato antiguo**.
  Dilo en una línea y ofrece `--migrar`.
- **No existe nada** → `modo-inicio.md` si el usuario pidió algo de tareas; **retírate en silencio**
  si no.
- **Sin git** (`git rev-parse --git-dir` falla) → el skill se detiene y lo explica en una línea.

## Qué hay en `tareas/`

```text
tareas/
├── config.md      Rama destino, áreas, enlace al proyecto de Toggl y reglas del repo
├── pendientes.md  Lo decidido sin hacer: Por hacer · A medias (con motivo) · Espera tu decisión
├── por-revisar.md La bandeja: lo anotado sin decidir. Solo guarda
├── auditoria.md   Hallazgos de una revisión por áreas, bajo petición
├── planes/        Solo los planes anteriores a utils 6.1; el plan vive en ~/.claude/plans/
└── historial/     AAAA-MM.md · lo cerrado y lo descartado, con su porqué
```

## La ceremonia, en corto

- **Planificar:** un solo plan, el del modo plan (en `~/.claude/plans/`, sin copia en el repo), con
  la tabla «Pasos» y un marcador con el repo y la rama; termina
  con **«Esto te toca a ti»** si hay algo del usuario que le ocupa tiempo (`tarea`). Se aprueba una
  vez, y eso cubre la ejecución.
- **Abrir:** la **rama destino** (`config.md` § Rama destino; `main` si no la declara) limpia y
  actualizada, y una rama nueva que salga de ella. **Nunca se trabaja sobre la destino ni sobre
  `main`**: la guardia de git del plugin bloquea esos commits.
- **Los pasos** se encadenan sin preguntar; cada uno puede llevar su commit en la rama (un punto de
  guardado) y se marca hecho en el plan, con evidencia.
- **Si no se termina**, lo que falta va a `pendientes.md` con su motivo, y la rama queda viva.
- **Cerrar:** **una sola confirmación, después de que el usuario vea el resultado**. El merge y el
  push los desbloquea solo su mensaje «apruebo el merge» (la guardia de git). Con él corre la cadena
  entera: tiempo de Claude a su registro, historial, commit, merge a la destino y push.

## Comunicación ejecutiva

- **Una propuesta cabe en 2–4 líneas**; una observación, en una. Tablas antes que prosa.
- **No recapitules el contexto leído.** Se usa, no se narra.
- **La justificación larga vive en el plan o en el historial, no en el chat.**

## Reglas invariantes

1. **Nada se crea en Toggl sin que el usuario lo elija**; la IA no reordena su cola.
2. **Se completa un trabajo y se para**; sugerir el siguiente sí, empezarlo no. Los pasos del plan
   se encadenan **sin preguntar por el siguiente**.
3. **Nada sale sin rastro.** Lo que no se termina va a `pendientes.md` con su motivo; lo que se
   descarta, al historial con el suyo.
4. **El historial se escribe en el mismo cierre**, dentro de la cadena.
5. **Del historial se lee la sección del ancla, nunca el archivo entero** (`historial-lectura.md`).
6. **Las áreas salen de `config.md`**: un área nueva se añade ahí con visto bueno.
7. **Ningún merge a la rama destino ni a `main` sin «apruebo el merge»**, escrito por el usuario
   después de ver el resultado. **Nunca se rodea la guardia** (ni con otro comando, ni editándola).

## Idioma

Español neutro con el usuario. El contenido del historial y de los planes, en el idioma del proyecto.
