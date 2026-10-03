# Migrar un repo (`--migrar`)

Dos formatos anteriores, y cada uno se migra en una pasada, en una rama y con **un** visto bueno.
`M=utils/skills/tarea-repo/scripts/migrar_a_toggl.py`.

## Desde utils 5 (`toggl.md`, `para-claude.md`)

Se reconoce porque existe `tareas/toggl.md` y no `config.md`.

1. **Mostrar** lo que haría `python3 $M a-config tareas/` (solo lee): `toggl.md` → `config.md`, las
   entradas de `para-claude.md` → `pendientes.md` (`Por hacer`, con el porqué «delegada en
   revisión»).
2. **Repasar Toggl.** Las tareas abiertas del proyecto (`cola.py leer --vista pendientes --proyecto
   <ID>`) que en realidad **ejecuta Claude** —objetivos que Claude hacía casi enteros, al modo de
   utils 4.7— se proponen **una por una**: con el sí, pasan a `pendientes.md` (`Por hacer`, o
   `A medias` si tienen rama) y se archivan en Toggl (`tasks bulk-archive`). Lo que hace el usuario se
   queda en Toggl, tal cual: es suyo.
3. **Aplicar**, con el sí: `python3 $M a-config tareas/ --aplicar`, `git add -A tareas/`, y en el
   `CLAUDE.md` del repo el bloque de tareas se reemplaza por `assets/claude-md-puntero.md` (la regla
   de ramas ya no se copia: la impone la guardia de git).
4. Commit en la rama, y el cierre normal (`modo-gestion.md`). Una línea: «Migrado a utils 6: 3
   pendientes, 2 tareas sacadas de Toggl».

## Desde el formato antiguo (`tareas.md`, `revisar.md`, `secciones.md`)

1. **Enlazar el proyecto.** Si `tareas.md` trae el marcador `<!-- tarea: toggl … -->`, ese es el
   proyecto; si no, se busca o se crea como en `modo-inicio.md`, paso 2.
2. **Armar la carga:** `python3 $M armar tareas/ --proyecto ID --usuario UID`. Lee `tareas.md`,
   `revisar.md` y `secciones.md` y devuelve, sin tocar nada:
   - las tareas abiertas en orden (`## Ahora` primero), con su área, comentario, coste, vence y
     estado, y las que **ya tienen `<!-- toggl:id -->`** aparte;
   - la bandeja (`bandeja`): **no va a Toggl**; `python3 $M por-revisar tareas/` la escribe en
     `tareas/por-revisar.md`;
   - las áreas, desde `secciones.md`.
3. **Repartir.** Por cada tarea, Claude propone de quién es:
   - **del usuario y le ocupa tiempo** → Toggl (las que ya tienen id, se actualizan);
   - **de Claude** → `tareas/pendientes.md`, `Por hacer`, con su comentario como «qué falta»;
   - **una decisión** → `pendientes.md`, `Espera tu decisión`.
   Las dependencias por número de fila («necesita la 3») se reescriben con el nombre.
4. **Mostrarla** en una tabla corta (cuántas a Toggl, cuántas a `pendientes.md`, cuántas a la
   bandeja, las áreas y los pares dudosos de `## Ahora`) y **pedir el visto bueno una vez**.
5. **Enviar**, con el sí: `tasks bulk-create` / `bulk-patch` solo con lo del usuario, validados antes
   con `dry_run: true`.
6. **Limpiar el repo**, en una rama y un commit:
   - `git rm` de `tareas/tareas.md`, `revisar.md` y `secciones.md`;
   - `tareas/por-revisar.md` con la bandeja y `tareas/pendientes.md` desde su esqueleto, con lo de
     Claude;
   - `python3 $M config-md tareas/ … [--rama preview]` escribe `tareas/config.md` (la rama destino
     es `main` salvo que el usuario diga otra);
   - **el historial no se toca**; `auditoria.md` se queda;
   - el bloque de tareas del `CLAUDE.md`, como en utils 5, paso 3.
7. `cola.py invalidar`, y una línea: «Migrado: 6 a Toggl, 12 a `pendientes.md`, 6 a la bandeja».

## Hallazgos de la API (26 y 28-09-2026)

| Hecho | Consecuencia |
| --- | --- |
| Un solo cronómetro por persona | Claude no cronometra: el timer es del usuario |
| Cada escritura pide un código de confirmación | Lo resuelve el skill: el visto bueno ya lo cubre |
| Límite: ~30 consultas por hora | Todo va en bloque |
| `start_date` sin `end_date` (o al revés) se rechaza | Van siempre juntas |
| Toggl 2.0 no acepta token de API: solo la sesión OAuth del conector | `cola.py` lee esa sesión y nunca la renueva |
| Subproyectos se ven al mismo nivel que el resto | Sin subproyectos: el área es una etiqueta |
