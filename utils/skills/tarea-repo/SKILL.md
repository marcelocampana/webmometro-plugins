---
name: tarea-repo
description: >
  Carril de repositorio del sistema de tareas: las tareas que viven en un repo con git, en su
  directorio `tareas/`, y terminan en commit. La entrada es el skill `tarea`, que decide el carril;
  este se usa directamente cuando ya está claro que el trabajo es de repositorio. Gestiona la cola del
  usuario (`tareas.md`, con flujo "una tarea, una rama, un commit" y tiempos), la bandeja
  `revisar.md` y la revisión por áreas `auditoria.md`, y asiste en crearlas: propone, afina
  enunciados y recomienda prioridad. **Solo si el proyecto ya tiene ese directorio, o si el usuario
  pide montarlo.** Cubre: abrir y cerrar tareas ("qué sigue", "listo, ya está", "commit y merge"),
  pausar o bloquear, anotar, priorizar y consultar; estimar cuánto cuesta y para cuándo vence;
  aparcar en "por revisar" y ascender; revisar el proyecto completo; extraer tareas de la
  conversación o de un archivo; archivar al cerrar; poner al día el formato (`--actualizar`); montar
  el sistema donde no existe; y, si el repo está conectado a Toggl (o se pide: `--toggl`), registrar
  el tiempo de cada tarea recortado por la presencia real del usuario. NO lo uses para tareas que no
  viven en ningún repo (eso es `tarea-suelta`), para TODOs efímeros de la sesión, ni para issues de
  GitHub/Jira/Linear; si no existe `tareas/` y el usuario no pidió nada de tareas, no lo actives.
argument-hint: "[--init | --revisar | --auditoria | --ingerir | --actualizar | --toggl]"
metadata:
  version: 3.1.0
---

# Tareas de repositorio (tarea-repo)

El cuello de botella de trabajar con asistencia de IA no es saber **qué** hay que hacer, sino **hacer
una cosa a la vez, con el contexto corto y el tiempo medible**. Este skill gobierna eso y **asiste en
crear** las tareas: propone, afina y recomienda prioridad — no solo marca filas.

Es el carril de **repositorio**: trabajo que cambia archivos de un repo y termina en commit. Lo que
no vive en ningún repo (facturar, reuniones, trámites) va por `tarea-suelta`, y la entrada `tarea`
decide cuál corresponde.

**Este archivo es el núcleo: solo lo que toda operación necesita.** El detalle de cada modo vive en
`references/`, y se lee **uno**.

## Qué leer según lo que se pida

| Si el usuario… | Lee |
| --- | --- |
| abre, cierra, pausa, crea, prioriza o consulta una tarea | `references/modo-gestion.md` |
| pide montar el sistema, o no existe `tareas/` | `references/modo-inicio.md` |
| aparca algo, o asciende de la bandeja | `references/modo-revisar.md` |
| pide revisar el proyecto completo (`--auditoria`) | `references/modo-auditoria.md` |
| pasa un archivo de tareas, o pide extraerlas de la conversación (`--ingerir`) | `references/modo-ingesta.md` |
| pide poner al día el formato, o el Paso 0 detecta una convención desactualizada (`--actualizar`) | `references/modo-actualizacion.md` |
| pide conectar el repo con Toggl, o reconciliar lo pendiente (`--toggl`) | `references/toggl-conexion.md` |

**Se lee la del modo invocado y ninguna más.** Las de apoyo —`archivado`, `contextualizacion`,
`redaccion-tareas`, `estados`, `tiempos`, `estimacion`, `toggl`, `seccionamiento`, `secciones-catalogo`,
`historial-lectura`, `formato-tablas`, `cierre-contenido`, `impacto-documental`— solo cuando la del
modo las cite para el paso que estás
ejecutando. Cargarlas «por si acaso» convierte este skill en su propio problema: el núcleo pesa ~2.400
tokens y cada referencia suma otros ~500-1.700.

## Paso 0 · Precondición (siempre, antes de todo)

1. **Resolver el artefacto.** Sube hasta la raíz del repo y busca ahí:

   ```bash
   RAIZ=$(git rev-parse --show-toplevel)
   ls -d "$RAIZ"/tareas/ 2>/dev/null            # ¿existe el layout esperado?
   find "$RAIZ" -maxdepth 2 -name '*.md' -exec grep -l '^## Ahora' {} + 2>/dev/null
   ```

   **Lo identifica la estructura** —un archivo con `## Ahora` y su tabla de punteros—, **no el
   nombre**; y en macOS `tareas.md` y `TAREAS.md` son el mismo archivo, así que buscar variantes de
   nombre no sirve de nada. Tres desenlaces:

   - **Existe `tareas/`** → paso 2.
   - **Existe un archivo plano con `## Ahora`** (típicamente `tareas.md` en la raíz): es el **formato
     antiguo**. Dilo en una línea, **opera sobre el archivo donde está** y ofrece migrarlo
     (`modo-inicio.md`). No escribas en una ruta que aún no existe.
   - **No existe nada** → `modo-inicio.md` si el usuario pidió algo de tareas; **retírate en silencio**
     si no pidió nada, sin mencionarlo ni ofrecerlo.

2. **Verificar git.** `git rev-parse --git-dir`. **Sin git el skill se detiene y lo explica** en una
   línea —el flujo se apoya en la rama por tarea y en tiempos verificables—. Sin modo degradado.
3. **Leer las secciones** con `grep -n '^## '` sobre el archivo resuelto, no sobre una ruta supuesta.
   Son las que hay: no inventes ni reordenes sin confirmación. Respeta el umbral si está anotado
   (`<!-- tarea: umbral … -->`; el marcador antiguo `<!-- task-flow: … -->` vale igual y no se
   reescribe sin permiso). Con el marcador `<!-- tarea: toggl … -->` el repo está conectado: sus
   tablas no llevan columnas de tiempo y crear, abrir, pausar y cerrar siguen además `toggl.md`.

## Las tres listas

```text
tareas/
├── tareas.md      Lista principal · la del usuario · con ceremonia completa
├── revisar.md     Bandeja de entrada · la IA propone libremente · ligera
├── auditoria.md   Revisión por áreas · la IA, bajo petición · ligera
├── secciones.md   Catálogo de secciones · nombre y ámbito, nunca tareas
└── historial/     AAAA-MM.md · comentarios y filas cerradas, siempre al cerrar (no solo al mes)
```

`tareas.md` se mantiene limpio: `## Ahora` más solo las secciones con trabajo activo confirmado por
el usuario. Lo que separa las tres listas no es el tema, es **quién decide y cuánto cuesta anotar**:

| | `tareas.md` | `revisar.md` | `auditoria.md` |
| --- | --- | --- | --- |
| **Decide qué entra** | El usuario, siempre | El usuario aprueba; la IA propone a discreción | El usuario aprueba; la IA propone bajo petición |
| **Ceremonia** | Rama, tiempos, una confirmación de cierre | Ninguna | Ninguna |
| **Cola `## Ahora`** | Sí | No | No |
| **Cómo sale** | Se cierra con commit y merge, en cadena | Asciende con aprobación, o se descarta | Igual |

Las columnas de las cuatro tablas, verbatim, están en `formato-tablas.md`.

`tareas.md` archiva **al cerrar cada tarea**, no al cumplir un mes: solo queda ahí lo abierto o por
abrirse en breve. `secciones.md` guarda el catálogo aunque una sección se quede sin tareas activas — y
es un catálogo abierto, no la lista cerrada de lo que puede existir. De `revisar.md` y `auditoria.md`
las filas se descartan o ascienden.

## Los cinco estados

`Pendiente` · `🔵 En curso` · `Pausada` · `Bloqueada` · `✅ Completada`. **No se inventa un sexto**: si
algo no cabe, va en la Nota o en Comentarios. **Solo una puede estar `🔵 En curso`**, y solo
`✅ Completada` mueve la fila —sale de `tareas.md` al historial—; los cuatro abiertos la dejan donde
está.

**Solo `🔵 En curso` y `✅ Completada` llevan icono, e icono *y* texto, nunca el icono a secas** —
`grep "En curso"` tiene que seguir funcionando y la columna debe leerse sin renderizar el emoji. El
estado se cambia **en los dos sitios** mientras la tarea está en `## Ahora`. Cuándo se entra y se sale
de cada uno: `estados.md`.

## Planificar sin sesión de planificación

**No se asignan días: se asignan orden y coste, y el día sale solo.** Toda la planificación cabe en la
pregunta que ya se hacía al crear una tarea —«¿en qué posición va?»—, ahora con el coste puesto.

- **`Coste`** manda: horas de trabajo, **lo propone el skill** desde el historial (`estimacion.md`) y
  el usuario lo confirma. Sin base suficiente va `—`; no se inventa.
- **`Vence`** es raro y solo para compromisos externos. **No decide el día: audita el orden.**

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
merge, o cambios ajenos a la tarea; fuera de eso, no hay una segunda ni tercera pregunta. **Si el
usuario encargó la tarea completa, ese encargo ya es el visto bueno del cierre.**

> Propongo: **Corregir el desplegable del menú en móvil** (`AppHeader.vue`) → General. ¿La creo?

## Reglas invariantes

1. La IA **no añade filas a `tareas.md` ni reordena `## Ahora`** por iniciativa propia; las
   transiciones de una tarea ya acordada sí, tras el visto bueno.
2. El ascenso **mueve, no copia**, y siempre con aprobación.
3. **Ninguna fila se escribe sin visto bueno**, en ninguna de las tres listas.
4. **Se completa una tarea y se para**; sugerir la siguiente sí, empezarla no.
5. **Las secciones no se reordenan**, y una sin ninguna fila activa **desaparece** de `tareas.md`.
6. **Solo se archiva `✅ Completada`**, y **en el mismo momento del cierre**, dentro de la cadena — no
   es un paso aparte que pida su propio visto bueno.
7. **El texto no se pierde, se mueve**: al archivar, la fila y su comentario íntegro van al mensual;
   en `tareas.md` no queda rastro por fila, y el total de la sección se lee en `secciones.md`.
8. **Si la tarea aprueba o publica contenido, su `estado:` se actualiza en el archivo fuente**,
    dentro de la misma cadena de cierre y sin pregunta aparte (`cierre-contenido.md`).
9. **Del historial se lee la sección del ancla, nunca el archivo entero** (`archivado.md`).

## Manejo de errores del Paso 0

Los tres desenlaces de resolver el artefacto ya están arriba. Lo que falta:

| Situación | Qué hacer |
| --- | --- |
| Falta `revisar.md` o `auditoria.md` | Ofrece crearla desde su esqueleto; nacen vacías. |
| Falta `tareas.md` (están las otras dos) | No se instancia de un esqueleto: lleva secciones. Ve a `modo-inicio.md`. |
| Falta `secciones.md` (existe `tareas.md`) | Dilo en una línea y ofrece `modo-actualizacion.md`; se crea desde los headers `##` ya presentes. |
| Convención de formato desactualizada (columnas viejas, leyenda en una línea, archivado por antigüedad) | Dilo en una línea y ofrece `modo-actualizacion.md`. No lo corrijas aquí mismo. |

Los errores propios de cada modo están en su referencia.

## Idioma

Español neutro con el usuario. El contenido de las listas, en el idioma del proyecto. Los nombres de
estado **tal cual están en el archivo**: traducirlos rompe el `grep`.
