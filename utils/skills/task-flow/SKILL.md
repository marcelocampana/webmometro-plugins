---
name: task-flow
description: >
  Gestiona las tareas del proyecto en el directorio `tareas/`: la cola del usuario (`tareas.md`, con
  flujo "una tarea, una rama, un commit" y tiempos), la bandeja `revisar.md` y la revisión por áreas
  `auditoria.md`. Asiste en crearlas: propone, afina enunciados y recomienda prioridad.
  **Actívalo solo si el proyecto ya tiene ese directorio, o si el usuario pide montarlo.** Cubre:
  abrir y cerrar tareas ("qué sigue", "listo, ya está", "commit y merge"), pausar o bloquear, anotar,
  priorizar y consultar; aparcar en "por revisar" y ascender; revisar el proyecto completo; extraer
  tareas de la conversación o de un archivo de otro skill; archivar lo antiguo o aligerar un archivo
  largo; y montar el sistema donde no existe. NO lo uses para TODOs efímeros de la sesión (esa es la
  lista interna de Claude Code), para issues de GitHub/Jira/Linear, ni para pendientes sin esta
  estructura; si no existe y el usuario no pidió nada de tareas, no lo actives ni lo propongas.
argument-hint: "[--init | --revisar | --auditoria | --ingerir]"
metadata:
  version: 1.2.0
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
| cierra una tarea, o el archivo está largo | `references/archivado.md` |
| va a abrir el detalle de un comentario archivado | `references/historial-lectura.md` |

**Se lee la referencia del modo invocado y ninguna más.** Las de apoyo —`contextualizacion`,
`redaccion-tareas`, `estados`, `tiempos`, `seccionamiento`, `formato-tablas`— solo cuando la del modo
las cite para el paso que estás ejecutando. Cargarlas «por si acaso» es el error que convierte este
skill en su propio problema: el núcleo son ~2.100 tokens y cada referencia suma ~1.000.

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
└── auditoria.md   Revisión completa · la IA, por áreas, bajo petición · ligera
└── historial/     AAAA-MM.md · comentarios y filas cerradas (solo de tareas.md)
```

Lo que las separa no es el tema, es **quién decide y cuánto cuesta anotar**:

| | `tareas.md` | `revisar.md` | `auditoria.md` |
| --- | --- | --- | --- |
| **Decide qué entra** | El usuario, siempre | El usuario aprueba; la IA propone a discreción | El usuario aprueba; la IA propone bajo petición |
| **Ceremonia** | Rama, tiempos, tres confirmaciones | Ninguna | Ninguna |
| **Columnas** | secciones: `Estado \| Tarea \| Inicio \| Completada \| Duración \| Comentarios`<br>`## Ahora`: `# \| Tarea \| Sección \| Estado \| Inicio \| Nota` | `Tarea \| Origen \| Motivo \| Notas` | `Tarea \| Área \| Severidad \| Motivo` |
| **Cola `## Ahora`** | Sí | No | No |
| **Cómo sale** | Se cierra con commit y merge | Asciende con aprobación, o se descarta | Igual |

Solo `tareas.md` tiene historial; de las otras dos las filas se descartan o ascienden.

## Los cinco estados

**No se inventa un sexto**: si algo no cabe, va en la Nota o en Comentarios.

| Estado | Cuándo | Mueve la fila |
| --- | --- | --- |
| `Pendiente` | Anotada, sin rama ni Inicio. | No |
| `🔵 En curso` | Rama creada e Inicio anotado. Solo una a la vez. | No |
| `Pausada` | Detenida por tiempo. | No |
| `Bloqueada` | Detenida por una dependencia. Nota **obligatoria**. | No |
| `✅ Completada` | Cerradas las tres confirmaciones. Terminal. | Sí: al final de su sección |

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

Lo que **no** se recorta: las tres confirmaciones de cierre son tres preguntas separadas.

> Propongo: **Corregir el desplegable del menú en móvil** (`AppHeader.vue`) → sección General.
> Afecta a todo el sitio, así que va como una sola tarea. ¿La creo?

## Reglas invariantes

1. La IA **no añade filas a `tareas.md` ni reordena `## Ahora`** por iniciativa propia; las
   transiciones de una tarea ya acordada sí, tras el visto bueno.
2. El ascenso **mueve, no copia**, y siempre con aprobación.
3. **Ninguna fila se escribe sin visto bueno**, en ninguna de las tres listas.
4. **Una tarea a la vez** en `🔵 En curso`.
5. **Se completa una tarea y se para**; sugerir la siguiente sí, empezarla no.
6. **Las secciones no se reordenan**, y lo abierto va arriba de lo `Completada`.
7. **Sin git, el skill se detiene**; no hay modo degradado.
8. **Las filas no se archivan sin confirmación**, y solo se archiva `✅ Completada`.
9. **El texto no se pierde, se mueve**: al archivar un comentario queda su resumen y su enlace.
10. **Del historial se lee la sección del ancla, nunca el archivo entero** (`archivado.md`).
11. **Se lee la referencia del modo invocado y ninguna más.**

## Manejo de errores del Paso 0

| Situación | Qué hacer |
| --- | --- |
| No hay `tareas/` y no se pidió nada de tareas | Retírate en silencio. No lo menciones. |
| No hay git | Detente y dilo en una línea. Sin modo degradado. |
| Hay un `tareas.md` plano en la raíz | Formato antiguo: opera sobre él y ofrece migrarlo (`modo-inicio.md`). |
| Falta `revisar.md` o `auditoria.md` | Ofrece crearla desde su esqueleto; nacen vacías. |
| Falta `tareas.md` (están las otras dos) | No se instancia de un esqueleto: lleva secciones. Ve a `modo-inicio.md`. |

Los errores propios de cada modo están en su referencia.

## Idioma

Español neutro con el usuario. El contenido de las listas, en el idioma del proyecto. Los nombres de
estado **tal cual están en el archivo**: traducirlos rompe el `grep`.
