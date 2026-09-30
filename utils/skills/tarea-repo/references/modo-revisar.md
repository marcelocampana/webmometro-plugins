# La bandeja: `por-revisar.md` (`--revisar`)

La bandeja es **`tareas/por-revisar.md`** (sin repo, `~/Obsidian/global/por-revisar.md`, una sección
por proyecto). **Solo guarda**: no es cola, no tiene fecha ni dueño y no está en Toggl. Si no existe,
se crea desde `assets/por-revisar.esqueleto.md` al anotar la primera entrada.

## Anotar

Tres vías, y ninguna decide nada:

1. **La IA anota lo que detecta de paso** trabajando en otra tarea: un `TODO`, una deuda, un efecto
   colateral, algo que el diff deja a medias. Se dice **en una línea y se sigue**.
2. **La IA sugiere tareas derivadas** de lo ya ejecutado (al cerrar, lo que quedó pendiente según el
   historial), o las propone `balance`: se proponen y, con el sí, se anotan.
3. **El usuario aparca una idea**, o escribe en el archivo a mano.

Cada entrada, una línea: `- **Título** · Área · origen · AAAA-MM-DD — por qué`. **El origen dice de
dónde salió** —la tarea, el commit o el archivo con su línea—: sin eso, en dos semanas no se sabe por
qué está ahí. El área es una de `toggl.md`. Una sugerencia sin ancla verificable no se anota, y lo
que ya está en el archivo, en `para-claude.md` o en el historial tampoco (`redaccion-tareas.md`).

## Revisar

Es un paso aparte: el usuario lo hace a mano o pide «revisemos la bandeja». Se leen las entradas y,
**por cada una, decide el usuario** (Claude puede recomendar, en una línea):

| Decisión | Qué se hace |
| --- | --- |
| **Dejar** | Sigue en el archivo. Revisar no obliga a decidir todo |
| **Para ti** | Tarea en Toggl (`tarea`), asignada al usuario, con estimación; se revisa el enunciado (`redaccion-tareas.md`). Sale del archivo |
| **Para Claude** | Pasa a `para-claude.md` con la fecha de delegación y qué se espera. Sale de este archivo. Nada va a Toggl |
| **Descartar** | Sale del archivo. Si el porqué importa, una línea en el comentario del commit |

## Git: commit directo y acotado

Los cambios a `por-revisar.md` y `para-claude.md` **fuera de una tarea** van en un commit directo
sobre la rama destino —solo esos dos archivos, mensaje `tareas: bandeja`— y push. Es la única
excepción a «nunca se trabaja sobre la destino»: texto de una línea por entrada, sin código. **Con
una tarea abierta**, lo anotado va en la rama de esa tarea, con su commit. Si la destino está sucia
con otros cambios, se commitean solo esos dos archivos, nunca `git add -A`.
