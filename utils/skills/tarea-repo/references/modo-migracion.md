# Migrar un repo al modelo de Toggl (`--migrar`)

Un repo con el formato anterior tiene su cola en `tareas/tareas.md` (`## Ahora` y secciones), la
bandeja en `revisar.md` y el catálogo en `secciones.md`. Migrar es pasar lo pendiente a Toggl y dejar
en el repo solo la memoria. **En una pasada y con un solo visto bueno.**

`M=utils/skills/tarea-repo/scripts/migrar_a_toggl.py`.

1. **Enlazar el proyecto.** Si `tareas.md` trae el marcador `<!-- tarea: toggl … -->`, ese es el
   proyecto; si no, se busca o se crea como en `modo-inicio.md`, paso 2.
2. **Armar la carga:** `python3 $M armar tareas/ --proyecto ID --usuario UID`. Lee `tareas.md`,
   `revisar.md` y `secciones.md` y devuelve, sin tocar nada:
   - las tareas abiertas en orden (`## Ahora` primero, después las `Pendiente` de cada sección),
     con `Área: <sección>` y el comentario en la descripción, la estimación desde `Coste`, el vence
     desde `Vence` y el estado;
   - la bandeja con la etiqueta `por-revisar`, sin fecha ni asignación;
   - las que **ya tienen `<!-- toggl:id -->`**, aparte: se actualizan (descripción, área) en vez de
     crearse de nuevo;
   - el contenido de `tareas/toggl.md` (marcador y áreas con su ámbito, desde `secciones.md`).
3. **Mostrarla** en una tabla corta (cuántas crear, cuántas actualizar, cuántas a la bandeja, y las
   áreas) y **pedir el visto bueno una vez**. Los pares dudosos de `## Ahora` con su sección los
   resuelve el script con `emparejar_ahora.py`; los `dudoso` se muestran en la misma tabla.
4. **Enviar**, con el sí: `tasks bulk-create` para las nuevas (una llamada) y `tasks bulk-patch` para
   las que ya existían (otra). Validar antes con `dry_run: true`.
5. **Limpiar el repo**, en una rama y un commit:
   - `git rm` de `tareas/tareas.md`, `tareas/revisar.md` y `tareas/secciones.md`;
   - escribir `tareas/toggl.md` (`python3 $M toggl-md …` lo genera);
   - **el historial no se toca**; `auditoria.md` se queda;
   - actualizar el bloque de tareas del `CLAUDE.md` del repo con `assets/claude-md-puntero.md`.
6. `cola.py invalidar`, y una línea de cierre: «Migrado: 18 tareas a Toggl, 6 a la bandeja».

## Reconciliar (`--toggl`)

Si Toggl no respondía en un cierre, o una sesión se cortó, `presencia.py tramos` sigue teniendo lo
pendiente: `--toggl` **envía lo que falte** (registros sin marca `enviado`, estados que no
coinciden) y lo dice en una línea. No reescribe lo ya enviado.

## Hallazgos de la API (26 y 28-09-2026)

| Hecho | Consecuencia |
| --- | --- |
| Un solo cronómetro por persona | No se usan cronómetros en vivo |
| Registros superpuestos de la misma persona: se aceptan | Dos tareas en paralelo cuentan las dos |
| Cada escritura pide un código de confirmación | Lo resuelve el skill: el visto bueno ya lo cubre |
| Límite: ~30 consultas por hora | Todo va en bloque |
| `start_date` sin `end_date` (o al revés) se rechaza | Van siempre juntas |
| Toggl 2.0 no acepta token de API: solo la sesión OAuth del conector | `cola.py` lee esa sesión y nunca la renueva |
| Subproyectos y etiquetas se ven al mismo nivel que el resto | No hay secciones en Toggl: el área va en la descripción |
