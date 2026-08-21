# Nota de diseño: `documentar-proceso`

Estado: **en discusión, sin construir todavía**. Este archivo registra las decisiones tomadas
hasta ahora y los descubrimientos de exploración, para retomar la conversación sin perder
contexto. No es un `SKILL.md` — cuando se construya la skill, este archivo puede borrarse o
convertirse en el `SKILL.md` final.

## Origen del problema

En una conversación previa sobre mejorar el aprendizaje del registro de tareas de `task-flow`,
surgió la idea de generar una "bitácora de proceso" a partir de las tareas ya cerradas. La
pregunta de diseño era si esto debía vivir dentro de `task-flow` o ser algo aparte.

## Por qué NO va dentro de `task-flow`

`task-flow` responde "¿qué hay que hacer y en qué estado está?" a nivel de una fila. Lo que se
busca acá es responder "¿cómo se hace bien este tipo de trabajo, aprendido de haberlo hecho varias
veces?" — eso opera a nivel de patrón repetible cruzando tareas, proyectos y tiempo. Son preguntas
de naturaleza distinta.

Ejemplo concreto: el ciclo completo de "crear una página" cruza el workspace ODC (contenido) y
`odc-clusters` (construcción) — dos sistemas de tareas independientes por diseño (cada proyecto
con su propio `tareas/`). Ninguna bitácora de proceso puede vivir dentro de un solo `tareas.md`
sin romper esa independencia.

Razones adicionales:
- `task-flow` ya tiene una responsabilidad clara y cerrada (las listas de un proyecto). Añadirle
  "extraer aprendizaje cruzando proyectos" le suma una dimensión —multi-proyecto, multi-tiempo,
  multi-tarea— que ninguna otra parte de la skill tiene hoy.
- La señal correcta: si esto viviera dentro de `task-flow`, requeriría columnas nuevas en los
  registros existentes para relacionar tareas entre sí — ese es exactamente el tipo de
  acoplamiento que infla una skill y la hace frágil (cada campo nuevo en `tareas.md` es una carga
  que el resto del sistema debe respetar para siempre, aunque el 95% de las tareas no participe de
  ningún proceso documentable).

Frase de deslinde (estilo ya usado en `seo-change-tracker`: *"Generar un reporte NO es registrar:
es una lectura agregada de lo ya registrado"*): **"Documentar un proceso NO es gestionar tareas:
es una lectura posterior sobre tareas ya cerradas."**

## Diseño de la skill nueva

Nombre acordado: **`documentar-proceso`** (se descartó `bitacora-proceso`/`proceso-aprendido`
porque "bitácora" ya es, en rigor, el registro de tareas que produce `task-flow` — esta skill no
crea una bitácora nueva, aprende de la que ya existe).

Características:

1. **Solo lectura** sobre uno o más directorios `tareas/` (de uno o varios proyectos indicados
   por el usuario). No escribe en `tareas.md`, `revisar.md` ni `auditoria.md` — `task-flow` no
   necesita saber que esta skill existe.
2. **Sin vínculo estructural entre tareas.** No se pide marcar de antemano "esta tarea es del
   proceso X" (columna nueva, acoplamiento permanente). La relación se establece al momento de
   redactar la bitácora de proceso: el usuario (o la IA a su pedido) señala qué tareas —de qué
   proyectos— correspondieron a una misma instancia del proceso (p. ej. "crear la página de
   triple negativo" = estas 3 tareas en ODC + estas 2 en `odc-clusters`), y la skill construye el
   documento a partir de ahí. Es una relación ad hoc y retrospectiva, no un campo que todas las
   filas deban cargar.
3. **Produce un artefacto de conocimiento**, no una tarea más: un documento Markdown por proceso
   repetible (pasos, decisiones, dónde se atascó, qué se automatizaría).
4. **Activación explícita únicamente** ("documenta el proceso de esta página", "qué aprendimos de
   esto") — nunca automática, igual que `--auditoria` en `task-flow`.
5. Concesión mínima opcional a futuro: el Comentario de una tarea cerrada (ya es texto libre en
   `task-flow`) podría mencionar a qué proceso perteneció, igual que ya menciona decisiones y
   trampas — sin cambiar el formato actual.

### Ubicación del artefacto de salida

Cada workspace de cliente resuelve su raíz subiendo desde el directorio activo hasta encontrar
`contexto/` (convención ya documentada en el `CLAUDE.md` raíz del marketplace: "shared truth lives
once at the client root"). El documento de proceso vive en **`contexto/procesos/`**, un directorio
nuevo, siguiendo el precedente directo de `contexto/seo-tracking/` (producido por
`seo-change-tracker`):

- Es "continua, sin período" — a diferencia de `web/seo/datos/{periodo}/`, no se versiona por mes
  porque el conocimiento de proceso no caduca por mes, es acumulativo.
- Un documento Markdown por proceso repetible, nombrado por slug (a definir: `{slug}.md` vs
  `AAAA-MM-DD-slug.md` — pendiente de decidir con el usuario).
- Notación para documentar la carpeta nueva en el `CLAUDE.md` del cliente, copiando el estilo ya
  usado: `carpeta/  descripción corta  (produce: <skill>; leen: <consumidores>)`.

### Resolución flexible frente a `task-flow` (que puede cambiar de formato)

`task-flow` está en desarrollo activo (el usuario lo está editando en paralelo a esta discusión).
Para no romperse si el formato de `tareas.md`/`revisar.md`/`auditoria.md` cambia, `documentar-proceso`
debe **resolver por rol/estructura, no por nombre de columna exacto** — mismo patrón ya usado en
`seo-change-tracker` frente a `contexto/configuracion.md`: "resuelve por rol y ofrece migrar; no
asume un alias fijo." Busca "una tarea cerrada con su comentario de cierre", no un esquema de
columnas congelado. Si no encuentra lo esperado, degrada explícitamente (avisa, no falla en
silencio, no asume).

### Formato de entrada (pendiente de reconfirmar una vez que `task-flow` esté estable)

Falta releer `tareas.md`/`revisar.md`/`auditoria.md` una vez que el usuario termine sus ediciones
actuales a `task-flow`, para confirmar:
- Campos exactos de una tarea cerrada (¿tiene ya un campo "Comentario" de texto libre?).
- Si el resolver por rol es viable con la estructura real o necesita ajuste.

## Patrones de diseño reutilizables (de exploración de otras skills)

### `claude-activity-log` (plugin `utils`) — la más parecida en espíritu

Archivo: `utils/skills/claude-activity-log/SKILL.md`.

Frontmatter mezcla triggers explícitos citados textualmente entre comillas con una frase que abre
paso a lo proactivo, pero incluso lo proactivo termina en "ofrece", nunca "escribe directamente":

> También aplica de forma proactiva al finalizar un plan de trabajo, completar una tarea
> significativa, cerrar una sesión, concluir un hito, o antes de cambiar de proyecto o de cuenta:
> en esos momentos ofrece registrar la actividad.

Regla de oro citada en `references/momentos-registro.md`: **"No se escribe silenciosamente porque
el log vive fuera del repo de trabajo"** — siempre se ofrece en una línea y se espera confirmación,
incluso en los disparadores proactivos. Aplica igual a `documentar-proceso`: nunca generar el
documento de proceso sin que el usuario lo confirme primero.

Formato de salida en capas: `resumen.md` (tabla consolidada) + `detalle.md` (un bloque `##
{id}` por entrada, mismo id como ancla). Los archivos nuevos se generan desde plantillas
(`assets/resumen.header.md`, `assets/detalle.template.md`) — patrón de "artefacto producido bajo
confirmación, desde plantilla" reutilizable acá.

Declara explícitamente un modo de solo consulta: *"No reescribas los archivos en este modo: es
solo lectura."*

### Redacción de activación explícita / retirada silenciosa

`task-flow/SKILL.md`:
> Actívalo solo si el proyecto ya tiene ese directorio, o si el usuario pide montarlo.
> [...] si no existe y el usuario no pidió nada de tareas, no lo actives ni lo propongas.

Y en el cuerpo: *"No hay `tareas/` y no se pidió nada de tareas → Retírate en silencio. No lo
menciones."* — patrón a replicar en `documentar-proceso` cuando no hay procesos cerrados que
documentar.

### Mecanismo anti-acoplamiento del marketplace (por qué esto es seguro aunque `task-flow` cambie)

Del `CLAUDE.md` raíz del marketplace: los archivos compartidos viven una sola vez y se leen **por
puntero, nunca por copia**; si el productor cambia de formato o ubicación, el consumidor "resuelve
por rol y ofrece migrar; no asume un alias fijo." Ejemplos concretos de esta postura:
- `page-cro`: *"This skill requires a page snapshot to operate. If the page snapshot doesn't
  exist, the skill will ask the user to generate it first... Do not attempt to operate without
  it."*
- `site-snapshot`: el productor declara *"This skill extracts data only — it does not diagnose,
  recommend, or interpret"*, separando limpiamente rol de productor y de consumidor.

## Decisiones pendientes / próximos pasos

1. Confirmar formato de nombre de archivo dentro de `contexto/procesos/`: `{slug}.md` vs
   `AAAA-MM-DD-slug.md`.
2. Esperar a que el usuario termine de editar `task-flow` antes de fijar el mecanismo exacto de
   "resolver por rol" sobre `tareas.md`/`revisar.md`/`auditoria.md`.
3. Redactar el `SKILL.md` real de `documentar-proceso` (frontmatter con triggers explícitos +
   sección "cuándo NO activarse", siguiendo el estilo de `task-flow` y `claude-activity-log`).
4. Documentar `contexto/procesos/` en el `CLAUDE.md` del cliente (ODC) cuando la skill exista,
   con la notación `carpeta/  descripción  (produce: ...; leen: ...)`.
