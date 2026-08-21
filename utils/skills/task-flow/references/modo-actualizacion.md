# Modo 5 · Actualización de formato (`--actualizar`)

Para proyectos que **ya tienen `tareas/`** con su estructura de directorio, pero alguna convención de
formato quedó de una versión anterior del skill: sin `secciones.md`, con la leyenda de estados en una
sola línea, con el archivado por antigüedad de un mes en vez de inmediato al cierre, o cualquier otra
discrepancia futura entre lo que el proyecto tiene y lo que `SKILL.md`/`references/` documentan hoy.

**No es lo mismo que `modo-inicio.md`.** Ese modo migra un `tareas.md` plano **sin** estructura de
directorio a la estructura completa — es el salto de "no hay `tareas/`" a "hay `tareas/`". Este modo
asume que **ya existe** `tareas/` y corrige convenciones dentro de ella. Son entradas distintas y se
mantienen separadas: mezclarlas obligaría a `modo-inicio.md` a saber leer formatos que no le
corresponden.

**No toca contenido semántico.** Solo forma y estructura: qué archivos existen, qué formato tiene un
bloque, cómo se agrupan las filas archivadas. Nunca reescribe el enunciado de una tarea, ni cambia un
estado, ni reinterpreta un comentario.

## Cómo se dispara

- **Explícito**: `--actualizar`, «pon el sistema de tareas al día», «actualiza el formato de tareas».
- **Detectado**: el Paso 0, al leer el archivo resuelto, encuentra una discrepancia de formato contra
  lo documentado (ver checklist abajo). **El Paso 0 solo detecta y ofrece — nunca ejecuta.** Dilo en
  una línea («el formato de la leyenda es el antiguo; ¿lo actualizo?») y, si el usuario acepta, pasa
  la ejecución a este modo. No dupliques aquí la lógica de detección: vive una sola vez, en el Paso 0.

## El patrón general (para esta migración y las futuras)

Este modo es el punto de entrada genérico para cualquier discrepancia de formato, no solo la de esta
sesión. El patrón es siempre el mismo:

1. **Comparar** lo que hay en el proyecto contra lo que la referencia correspondiente documenta hoy
   (`SKILL.md`, o el `references/*.md` dueño de esa convención).
2. **Listar las discrepancias encontradas**, una por una, en una tabla corta: qué está desactualizado,
   qué archivo lo tiene, a qué formato debe pasar.
3. **Proponer el ajuste de cada una y esperar confirmación** — igual que cualquier escritura en este
   skill, se propone y se espera; puede aceptarse una por una o todas a la vez, pero nunca se aplican
   sin que el usuario las haya visto.
4. **Aplicar solo lo confirmado**, sin tocar nada más del archivo.

## Checklist de convenciones verificadas

| Convención | Cómo se detecta desactualizada | A qué formato pasa |
| --- | --- | --- |
| Catálogo de secciones | No existe `tareas/secciones.md` | Se crea desde los headers `##` ya presentes en `tareas.md` (`secciones-catalogo.md`) |
| Leyenda de estados | El pie de `tareas.md` tiene la leyenda en una sola línea con "·" | Lista `-`, un estado por línea (`estados.md`) |
| Momento del archivado | Hay filas `✅ Completada` conviviendo dentro de una sección en `tareas.md` | Se archivan de inmediato (`archivado.md`); no hay «filas pendientes de migrar» por antigüedad — el archivado inmediato aplica desde ya a los próximos cierres |
| Cualquier otra convención de `SKILL.md`/`references/` | Se detecta comparando el archivo contra la referencia dueña de esa convención | Se ajusta al formato que esa referencia documenta |

La última fila sostiene el "patrón general": cuando una futura versión del skill cambie otra
convención, este modo no necesita rediseño — solo añadir una fila al checklist.

## Ejemplo de cierre de este modo

Un proyecto con `tareas.md` cuya leyenda está en una línea y sin `secciones.md`:

1. Detecta las dos discrepancias, las lista.
2. Propone: crear `secciones.md` con una entrada por cada `##` de `tareas.md` (nombre + ámbito
   inferido del contenido de la sección + total ya presente si lo hay), y reescribir la leyenda al
   formato de lista.
3. Con el visto bueno, aplica ambas. No reescribe ninguna fila de tarea.

## Errores

| Situación | Qué hacer |
| --- | --- |
| No hay discrepancias | Dilo en una línea: el formato ya está al día. No fuerces cambios. |
| El usuario acepta solo algunas de las discrepancias listadas | Aplica solo esas; deja constancia de cuáles quedaron pendientes. |
| Una convención nueva no está en el checklist todavía | No inventes el formato correcto: señala la referencia que debería documentarla y pregunta antes de aplicar nada. |
