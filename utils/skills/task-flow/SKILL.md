---
name: task-flow
description: >
  Gestiona las tareas del proyecto en el directorio `tareas/`: la cola del usuario (`tareas.md`, con
  flujo "una tarea, una rama, un commit" y tiempos), la bandeja `revisar.md` y la revisión por áreas
  `auditoria.md`. Asiste en crearlas: propone, afina enunciados y recomienda prioridad.
  **Actívalo solo si el proyecto ya tiene ese directorio, o si el usuario pide montarlo.** Cubre:
  abrir y cerrar tareas ("qué sigue", "listo, ya está", "commit y merge"), pausar o bloquear, anotar,
  priorizar y consultar; aparcar en "por revisar" y ascender; revisar el proyecto completo; extraer
  tareas de la conversación o de un archivo de otro skill; archivar al cerrar cada tarea; poner al
  día el formato de un sistema de tareas ya existente (`--actualizar`); y montar el sistema donde no
  existe. NO lo uses para TODOs efímeros de la sesión (esa es la lista interna de Claude Code), para
  issues de GitHub/Jira/Linear, ni para pendientes sin esta estructura; si no existe y el usuario no
  pidió nada de tareas, no lo actives ni lo propongas.
argument-hint: "[--init | --revisar | --auditoria | --ingerir | --actualizar]"
metadata:
  version: 1.5.0
---

# Gestión de tareas por rama (task-flow)

El cuello de botella de trabajar con asistencia de IA no es saber **qué** hay que hacer, sino **hacer
una cosa a la vez, con el contexto corto y el tiempo medible**. Este skill gobierna eso, y **asiste en
crear** las tareas: propone, afina, observa y recomienda prioridad — no solo marca filas.

**Este archivo es el núcleo: solo lo que toda operación necesita.** El detalle de cada modo vive en
`references/` y se lee **uno**, el del modo invocado.

## Qué leer según lo que se pida

| Si el usuario… | Lee |
| --- | --- |
| abre, cierra, pausa, crea, prioriza o consulta una tarea | `references/modo-gestion.md` |
| pide montar el sistema, o no existe `tareas/` | `references/modo-inicio.md` |
| aparca algo, o asciende de la bandeja | `references/modo-revisar.md` |
| pide revisar el proyecto completo (`--auditoria`) | `references/modo-auditoria.md` |
| pasa un archivo de tareas, o pide extraerlas de la conversación (`--ingerir`) | `references/modo-ingesta.md` |
| pide poner al día el formato, o el Paso 0 detecta una convención desactualizada (`--actualizar`) | `references/modo-actualizacion.md` |
| cierra una tarea, o el archivo está largo | `references/archivado.md` |
| pide ver o gestionar el catálogo de secciones | `references/secciones-catalogo.md` |
| va a abrir el detalle de un comentario archivado | `references/historial-lectura.md` |

**Se lee la referencia del modo invocado y ninguna más.** Las de apoyo —`contextualizacion`,
`redaccion-tareas`, `estados`, `tiempos`, `seccionamiento`, `secciones-catalogo`, `formato-tablas`—
solo cuando la del modo las cite para el paso que estás ejecutando. Cargarlas «por si acaso» es el
error que convierte este skill en su propio problema: el núcleo pesa ~2.600 tokens y cada referencia
suma otros ~1.000-1.500.

## Paso 0 · Precondición (siempre, antes de todo)

1. **Resolver el artefacto.** Sube hasta la raíz del repo y busca ahí:

   ```bash
   RAIZ=$(git rev-parse --show-toplevel)
   ls -d "$RAIZ"/tareas/ 2>/dev/null            # ¿existe el layout esperado?
   find "$RAIZ" -maxdepth 2 -name '*.md' -exec grep -l '^## Ahora' {} + 2>/dev/null
   ```

   **Lo que identifica el artefacto es la estructura** —un archivo con `## Ahora` y su tabla de
   punteros—, no el nombre. En macOS el sistema de archivos no distingue mayúsculas: `tareas.md` y
   `TAREAS.md` son el mismo archivo, así que no busques por variantes de nombre. Tres desenlaces:

   - **Existe `tareas/`** → paso 2.
   - **Existe un archivo plano con `## Ahora`** (típicamente `tareas.md` en la raíz): es el **formato
     antiguo**. Dilo en una línea, **opera sobre el archivo donde está** y ofrece migrarlo
     (`modo-inicio.md`). No escribas en una ruta que aún no existe.
   - **No existe nada** → `modo-inicio.md` si el usuario pidió algo de tareas; **retírate en silencio**
     si no pidió nada, sin mencionarlo ni ofrecerlo.

2. **Verificar git.** `git rev-parse --git-dir`. **Sin git el skill se detiene y lo explica** en una
   línea: el flujo se apoya en la rama por tarea y en tiempos verificables contra `git reflog`. No
   propongas un modo degradado.
3. **Leer las secciones** con `grep -n '^## '` sobre el archivo resuelto —no sobre una ruta supuesta—.
   Son las que hay: no inventes ni reordenes sin confirmación. Si hay umbral anotado
   (`<!-- task-flow: umbral … -->`), respétalo.

## Las tres listas

```text
tareas/
├── tareas.md      Lista principal · manda el USUARIO · con ceremonia completa
├── revisar.md     Por revisar    · la IA propone libremente · ligera
├── auditoria.md   Revisión completa · la IA, por áreas, bajo petición · ligera
├── secciones.md   Catálogo de secciones · nombre y ámbito, nunca tareas
└── historial/     AAAA-MM.md · comentarios y filas cerradas, siempre al cerrar (no solo al mes)
```

`tareas.md` se mantiene limpio: `## Ahora` más solo las secciones con trabajo activo confirmado por
el usuario. Lo que separa las tres listas no es el tema, es **quién decide y cuánto cuesta anotar**:

| | `tareas.md` | `revisar.md` | `auditoria.md` |
| --- | --- | --- | --- |
| **Decide qué entra** | El usuario, siempre | El usuario aprueba; la IA propone a discreción | El usuario aprueba; la IA propone bajo petición |
| **Ceremonia** | Rama, tiempos, una confirmación de cierre | Ninguna | Ninguna |
| **Columnas** | secciones: `Estado \| Tarea \| Inicio \| Completada \| Duración \| Comentarios`<br>`## Ahora`: `# \| Tarea \| Sección \| Estado \| Inicio \| Nota` | `Tarea \| Origen \| Motivo \| Notas` | `Tarea \| Área \| Severidad \| Motivo` |
| **Cola `## Ahora`** | Sí | No | No |
| **Cómo sale** | Se cierra con commit y merge, en cadena | Asciende con aprobación, o se descarta | Igual |

`tareas.md` archiva **al cerrar cada tarea**, no al cumplir un mes: solo queda ahí lo abierto o por
abrirse en breve. `secciones.md` guarda el catálogo de secciones aunque una se quede sin tareas
activas — y es un catálogo abierto, no la lista cerrada de lo que puede existir. De `revisar.md` y
`auditoria.md` las filas se descartan o ascienden.

## Los cinco estados

**No se inventa un sexto**: si algo no cabe, va en la Nota o en Comentarios.

| Estado | Cuándo | Mueve la fila |
| --- | --- | --- |
| `Pendiente` | Anotada, sin rama ni Inicio. | No |
| `🔵 En curso` | Rama creada e Inicio anotado. Solo una a la vez. | No |
| `Pausada` | Detenida por tiempo. | No |
| `Bloqueada` | Detenida por una dependencia. Nota **obligatoria**. | No |
| `✅ Completada` | Cerrada con la confirmación de cierre. Terminal. | Sí: sale de `tareas.md` al historial |

**Solo `🔵 En curso` y `✅ Completada` llevan icono, e icono *y* texto, nunca el icono a secas** —
`grep "En curso"` tiene que seguir funcionando y la columna debe leerse sin renderizar el emoji. El
estado se cambia **en los dos sitios** mientras la tarea está en `## Ahora`. Detalle: `estados.md`.

## Comunicación ejecutiva

El análisis es profundo; **lo que el usuario lee, no**. Un skill que justifica cada fila con tres
párrafos hace más caro anotar una tarea que hacerla.

- **Una propuesta cabe en 2–4 líneas**; una observación, en una.
- **No recapitules el contexto leído.** Se usa, no se narra.
- **Tablas antes que prosa** cuando hay varias tareas.
- **Sin preámbulos ni cierres de cortesía.** El visto bueno se pide en una pregunta corta.
- **La justificación larga vive en la fila, no en el chat.**

Lo que **no** se recorta: el cierre es **una** confirmación, y con ella corre la cadena completa
—fila, commit, merge— sin pausas. Los únicos altos son `main` sucia/desactualizada, un conflicto de
merge, o cambios ajenos a la tarea; fuera de eso, no hay una segunda ni tercera pregunta.

> Propongo: **Corregir el desplegable del menú en móvil** (`AppHeader.vue`) → sección General.
> Afecta a todo el sitio, así que va como una sola tarea. ¿La creo?

## Reglas invariantes

1. La IA **no añade filas a `tareas.md` ni reordena `## Ahora`** por iniciativa propia; las
   transiciones de una tarea ya acordada sí, tras el visto bueno.
2. El ascenso **mueve, no copia**, y siempre con aprobación.
3. **Ninguna fila se escribe sin visto bueno**, en ninguna de las tres listas.
4. **Una tarea a la vez** en `🔵 En curso`.
5. **Se completa una tarea y se para**; sugerir la siguiente sí, empezarla no.
6. **Las secciones no se reordenan**, y una sección sin ninguna fila activa **desaparece** de
   `tareas.md` — sus tareas cerradas ya están en el historial, no en un limbo dentro del archivo.
7. **Sin git, el skill se detiene**; no hay modo degradado.
8. **Solo se archiva `✅ Completada`**, y ocurre **en el mismo momento del cierre**, como parte de la
   cadena de cierre — no es un paso aparte que pida su propio visto bueno.
9. **El texto no se pierde, se mueve**: al archivar, la fila y su comentario íntegro van al mensual;
   en `tareas.md` no queda rastro por fila, y el total acumulado de la sección se lee en
   `secciones.md`.
10. **Si la tarea aprueba o publica contenido, su `estado:` se actualiza en el archivo fuente**,
    dentro de la misma cadena de cierre y sin pregunta aparte (`archivado.md`).
11. **Del historial se lee la sección del ancla, nunca el archivo entero** (`archivado.md`).
12. **Se lee la referencia del modo invocado y ninguna más.**

## Manejo de errores del Paso 0

| Situación | Qué hacer |
| --- | --- |
| No hay `tareas/` y no se pidió nada de tareas | Retírate en silencio. No lo menciones. |
| No hay git | Detente y dilo en una línea. Sin modo degradado. |
| Hay un `tareas.md` plano en la raíz | Formato antiguo: opera sobre él y ofrece migrarlo (`modo-inicio.md`). |
| Falta `revisar.md` o `auditoria.md` | Ofrece crearla desde su esqueleto; nacen vacías. |
| Falta `tareas.md` (están las otras dos) | No se instancia de un esqueleto: lleva secciones. Ve a `modo-inicio.md`. |
| Falta `secciones.md` (existe `tareas.md`) | Dilo en una línea y ofrece `modo-actualizacion.md`; se crea desde los headers `##` ya presentes. |
| Convención de formato desactualizada (leyenda en una línea, archivado por antigüedad, etc.) | Dilo en una línea y ofrece `modo-actualizacion.md`. No lo corrijas aquí mismo. |

Los errores propios de cada modo están en su referencia.

## Idioma

Español neutro con el usuario. El contenido de las listas, en el idioma del proyecto. Los nombres de
estado **tal cual están en el archivo**: traducirlos rompe el `grep`.
