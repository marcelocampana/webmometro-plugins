# Inicio: montar `tareas/` en un repo (`--init`)

Dos vías de entrada: **explícita** (`--init`, «monta el sistema de tareas aquí») o **detectada** (el
usuario pide algo de tareas y el repo no tiene `tareas/`; dilo en una línea y ofrécelo, **solo ante
una petición de tareas**). Si lo que hay es un `tareas.md` con `## Ahora`, no es esto: es
`modo-migracion.md`.

1. **Contextualizar** (`contextualizacion.md`): qué es el proyecto, su estructura, su deuda declarada
   y `git log`.
2. **Enlazar el proyecto de Toggl** (donde irán las tareas que el usuario elija). `projects list`
   con el nombre del repo; si hay uno que encaja:
   «Este repo parece del proyecto X (cliente Y). ¿Lo uso?». Si no, se propone crearlo, con los
   clientes de `clients list`, y si ningún cliente encaja se ofrece crear uno. **Los proyectos se
   crean públicos**: los privados son de pago (402). Nada se crea en Toggl sin visto bueno.
   **El nombre del proyecto es el del repo, sin guiones y con mayúscula inicial**: el repo
   `webmometro-web-reports` es el proyecto «Webmometro web reports». Así todos siguen el mismo
   estándar y se reconoce qué repo es cada proyecto. Los proyectos que ya existían con otro nombre
   (como «Plugins de IA») se dejan como están.
3. **Proponer las áreas** en una tabla corta —área y qué abarca—, derivadas de la estructura del
   proyecto y de lo que el usuario ya nombró. **Un área se gana su sitio**: si solo tendría una tarea,
   va en `General`. Pocas y estables.
4. **Crear**, con el visto bueno:
   - `tareas/config.md` desde `assets/config.esqueleto.md`, con el marcador, las áreas acordadas y
     la rama destino (`main` salvo que el usuario diga otra, como `preview`).
   - `tareas/auditoria.md` desde `assets/auditoria.esqueleto.md`.
   - `tareas/historial/` vacío.
   - `tareas/por-revisar.md` y `tareas/pendientes.md` desde sus esqueletos: lo anotado sin decidir
     y lo decidido sin hacer, que nunca van a Toggl.
5. **Ofrecer, en una línea:** el puntero para `CLAUDE.md` (`assets/claude-md-puntero.md`). La regla
   de ramas no se copia: la impone la guardia de git del plugin.

Lo que el usuario ya nombró como trabajo de Claude va a `pendientes.md`; lo suyo que ocupa tiempo,
a Toggl si lo elige (`tarea`).
