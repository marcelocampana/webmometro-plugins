# El ciclo de una tarea con Toggl

Solo en repos con marcador (`toggl-conexion.md`). **Toggl mide el tiempo de proyecto; el registro de
presencia, el tiempo del usuario.** Las dos medidas no se suman nunca: con dos sesiones en paralelo,
las dos tareas cuentan el mismo tramo y el usuario lo vivió una sola vez.

`P=utils/skills/tarea/scripts/presencia.py` (en el repo del plugin, o en su caché). `R` es el
nombre del repo y `ID`, el de la tarea en Toggl.

## Toggl se escribe solo al crear y al cerrar, en bloque

| Momento | En `tareas.md` | Toggl | Local |
| --- | --- | --- | --- |
| Crear | Fila, con visto bueno | 1 llamada: la tarea con proyecto, etiqueta de sección, `estimated_mins` y, si hay `Vence`, `end_date` + `start_date` = hoy. Se escribe `<!-- toggl:ID -->` | `P marca --evento crear --coste … --vence …` |
| Abrir, retomar | Rama, estado | **Nada** | `P marca --evento abrir` (o `retomar`) |
| Pausar, bloquear | Estado, Nota | **Nada** | `P marca --evento pausar` |
| Cerrar | Cadena de cierre | 2 llamadas: registros y estado Done | `P marca --evento cerrar`, luego `tramos`, luego `enviado` |

**Al cerrar**, en este orden y dentro de la misma cadena, sin pregunta aparte:

1. `P marca --repo R --tarea ID --evento cerrar`.
2. `P tramos --repo R --tarea ID`: devuelve `registros` (los tramos en que la tarea estuvo abierta
   **y** el usuario presente), `inicio`, `fin`, `duracion`, `descontado`, `coste` y `vence`.
3. `time-entries bulk-create` con esos `registros` y `task_id` = ID. Una llamada.
4. `tasks bulk-patch` con el estado Done. Una llamada.
5. `P marca --evento enviado`: lo siguiente que se envíe empieza después.
6. La fila del historial se arma con esos datos (`archivado.md`); no se lee Toggl.

**No se usa cronómetro**: Toggl admite uno solo por persona, y dos sesiones en paralelo se lo
quitarían. **El cálculo lo hace el script, no el modelo**: las mismas marcas dan siempre los mismos
tramos, y cada registro en Toggl tiene inicio y duración revisables.

**Si hay `descontado`**, se dice en la línea de cierre: «descontados 25 min sin actividad; si
estabas, lo mantengo». Si el usuario lo pide, se envía también ese tramo.

**Sin registros** (se trabajó fuera del Mac, o faltaba el registro de presencia): la Duración sale
de git como siempre, con su `~` (`tiempos.md`), y se dice.

**Lotes, solo si el usuario crea varias tareas relacionadas:** una tarea madre con sus subtareas en
una llamada (`create-task` con `subtasks`); al cerrar la última, registros de todas en una llamada y
estados en otra. Los pasos de un plan de Claude **no** son un lote: son una sola tarea
(`modo-gestion.md`, «Cuándo dividir»).

## Imprevistos

Si `P resumen` del día muestra atención en este repo sin tarea abierta, se dice al activarse el
skill: «llevas 40 min en este proyecto sin tarea abierta». Entonces:

- **Menos de `imprevisto_min` (30) y sin commit**: un registro suelto en Toggl
  (`create-taskless`), en el proyecto del repo, etiqueta `imprevisto`, con una descripción. Sin fila.
- **Con commit o flujo de tareas, o si pasa del tope**: es una tarea normal —visto bueno, rama,
  posición en `## Ahora` que decide el usuario—, con la etiqueta `imprevisto` en Toggl. Su marca
  `abrir` lleva `--hora` de cuando empezó de verdad, para que el tiempo ya hecho no se pierda.

## Aviso de pausa

Al abrir, pausar o cerrar, `P sesion`: si la sesión continua pasa de `sesion_min` (90), una línea:
«Llevas 2h 10m seguidas; toca una pausa». No bloquea nada. El mismo aviso llega a cualquier
conversación por el gancho de mensajes (`tarea/assets/presencia-instalacion.md`).

**Al crear varias tareas de una vez**, se suma su `Coste` y se dice: «suman ~2h 40m». Si pasa de
`sesion_min`, se avisa de antemano y se propone una pausa cerca de la mitad. Sin base para estimar,
se pregunta; no se inventa.

## Si Toggl falla

La parte del markdown y de git se hace igual y se dice qué quedó sin enviar. Las marcas siguen en el
registro local: el siguiente cierre o `--toggl` lo envía. **Con error 402 por límite** (distinto del
402 de plan), se avisa y no se reintenta en bucle.
