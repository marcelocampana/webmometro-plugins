<!-- tarea: plan · slug completar-bien-el-trabajo · rama completar-bien-el-trabajo -->

## Estado

Van 9 de 9 pasos (el cierre espera «apruebo el merge»). Sigue: verificar la guardia en vivo tras
instalar 6.0.0 (en `pendientes.md`). Espera de ti: revisar el resultado.

# utils 6.0.0 · Completar bien el trabajo: Toggl lo llevas tú, y nada de lo decidido se pierde

## Contexto

El objetivo no es organizar las tareas del usuario, sino **completar bien el trabajo**: que lo
decidido se haga y, si no se hace, que quede escrito por qué; que las buenas ideas no se pierdan; y
que se note el avance.

Entre el 26 y el 29 de septiembre, utils pasó de la 2.1 a la 5.0, en buena parte para medir y para
decidir dónde vive cada cosa. El usuario se dio cuenta de algo más: cuando Claude administraba Toggl,
las tareas le resultaban ajenas. **Ahora lleva Toggl él mismo, a mano**: crea sus tareas, planifica,
corre y para el timer, y cierra.

**Qué hace Claude en Toggl a partir de ahora:**

1. **Proponer tareas para el usuario.** Al final de su plan, Claude agrega la sección **«Esto te toca
   a ti»**: una lista numerada con lo que Claude no puede hacer y que ocupa tiempo del usuario. El
   usuario elige («la 1, la 3, la 7 y la 8 a Toggl») y Claude crea solo esas.
   - Si el trabajo salió de una tarea que el usuario ya tenía en Toggl, se crean como subtareas de
     esa tarea.
   - Si no, se crean como tareas sueltas, con una línea que dice de qué trabajo salen.
2. **Verificar los registros cuando el usuario lo pide** («¿a qué hora dejé de trabajar?»):
   `presencia.py verificar`, sin cambios.

**Qué no hace Claude en Toggl:** abrir, pausar o cerrar tareas, cambiar estados, planificar, ni
escribir nada sobre su propio trabajo. **Las decisiones no van a Toggl**: se piden en el momento
(«necesito tu decisión sobre X») y, si quedan abiertas, se anotan en `pendientes.md`.

**El flujo de Claude no cambia.** Arma su plan como siempre, lo ejecuta en una rama y cierra con
historial, commit y merge, este último con la aprobación del usuario. Este cambio solo agrega dos
cosas: la sección «Esto te toca a ti» y que nada de lo decidido se pierda.

## El sistema

| Pregunta | Dónde |
| --- | --- |
| ¿Qué hago yo? | **Toggl**, que lleva el usuario. Claude solo crea las tareas que el usuario eligió de «Esto te toca a ti» |
| ¿Qué hace Claude ahora? | **La rama y su plan** (el de modo plan, guardado en `tareas/planes/<slug>.md`). Sin id de Toggl |
| ¿Qué ideas hay sin decidir? | **`tareas/por-revisar.md`**, sin cambios |
| ¿Qué está decidido y no se ha hecho? | **`tareas/pendientes.md`** (nuevo; absorbe `para-claude.md`), con tres secciones: `Por hacer`, `A medias` (con el motivo) y `Espera tu decisión` |
| ¿Qué se hizo, qué se descartó y por qué? | **`tareas/historial/`** + una sección nueva, `Descartadas` |

**Nada sale sin rastro.** Cada entrada de `pendientes.md` sale de una sola forma: al historial, como
hecha o como descartada con su motivo.

**Captura sin depender de la memoria de Claude:**

- **Al cerrar una tarea, o si el plan no cabe en la sesión:** lo que queda entra en `pendientes.md`,
  con el motivo y el plan.
- **Fuera de un cierre:** `pendientes.py capturar` se ejecuta en el gancho `SessionEnd` del plugin y
  una vez al día desde el agente de launchd que ya existe. Busca las ramas sin mergear y anota en
  `A medias` las que aún no figuran, con los pasos que faltan y si hay cambios sin commitear. Es
  idempotente y no commitea nada.
- **Leer lo pendiente:** solo cuando el usuario lo pide.

**Guardia de git, que no depende de ninguna instrucción.** El usuario trabaja en modo automático, y
en ese modo Claude Code no muestra avisos de permiso. Por eso la regla de ramas la impone un gancho
`PreToolUse` del plugin utils (activado globalmente), en **todo repo git**, tenga o no `tareas/`:

- **Ramas protegidas:** `main`, `master`, la rama por defecto del remoto y la rama destino si
  `tareas/config.md` declara una (o `tareas/toggl.md` en un repo que aún no se migra).
- **Commit sobre una rama protegida:** bloqueado. Si el trabajo empezó sin rama, esto obliga a
  crearla.
- **Merge y push hacia una rama protegida:** bloqueados, salvo que exista un **permiso de un solo
  uso**:
  - lo crea un gancho `UserPromptSubmit` cuando el usuario escribe «apruebo el merge»;
  - vale solo para ese repo y **esa sesión** (`session_id`), y vence a los 10 minutos;
  - Claude no puede crearlo.
- **Push de la rama de trabajo:** libre.
- **Excepciones:** el primer commit de un repo vacío, y los commits que solo tocan `por-revisar.md`
  o `pendientes.md`.
- **El mensaje de rechazo es la instrucción:** dice qué hacer y prohíbe rodear el bloqueo.
- **Falla cerrado:** ante cualquier error del script, bloquea.
- **Cubre las variantes del comando:** `git -C <ruta>`, `HEAD:<rama>`, `--all`, `gh pr merge`, y
  todo push que se haga estando en una rama protegida.
- **Se protege a sí mismo:** bloquea las ediciones (Write, Edit o Bash) de sus propios archivos y
  del archivo de permisos.

Límite: el gancho revisa el texto de los comandos. Un merge desde la web de GitHub no pasa por él.

**El avance a la vista:** `balance`, que es lo que el usuario usa cada semana, suma la sección **«Lo
abierto»**:

- lo que se cerró en la semana;
- `pendientes.md` ordenado por antigüedad;
- lo que espera una decisión;
- la bandeja;
- las ramas sin mergear.

Es de solo lectura.

## Pasos (rama `completar-bien-el-trabajo`, desde `main`)

Se hace todo en una sola fase: el gancho y «Lo abierto» quedan disponibles desde el principio,
aunque `balance` no se revise cada semana.

1. **`tarea` (núcleo + `references/ciclo.md`):**
   - el ciclo en el que Claude abre, pausa y cierra en Toggl se reemplaza por dos funciones: crear
     las tareas que el usuario elige y verificar los registros;
   - criterio: solo lo que ocupa tiempo del usuario; una decisión no va;
   - subtarea si el trabajo salió de una tarea del usuario en Toggl; si no, tarea suelta con su
     origen;
   - el núcleo queda bastante más corto que ahora.
2. **`tarea-repo`:**
   - **`modo-gestion.md`:**
     - el plan se guarda en `tareas/planes/<slug>.md` y termina con «Esto te toca a ti»;
     - abrir y cerrar no tocan Toggl;
     - la cadena de cierre queda así: tiempo de Claude a su registro local, historial, commit, merge
       con aprobación y push;
     - lo que quede abierto va a `pendientes.md`.
   - **`modo-claude.md` pasa a ser `modo-pendientes.md`:** anotar, retomar (estado en 2–3 líneas),
     cerrar o descartar con motivo, y consultar.
   - **`modo-revisar.md`:**
     - «Para Claude» va a `pendientes.md`;
     - «Para ti» va a Toggl solo si el usuario lo elige;
     - «Descartar» deja el motivo en el historial.
   - **`archivado.md`:** formato de `Descartadas`.
   - **Núcleo y referencias al pasar** (nombres de archivo y papel de Toggl): `modo-inicio`,
     `modo-ingesta`, `redaccion-tareas`, `contextualizacion`, `modo-auditoria`,
     `impacto-documental` y `estimacion`.
   - Se retira `--toggl` (reconciliar estados con Toggl), que ya no tiene sentido.
3. **Captura:**
   - `tarea-repo/scripts/pendientes.py` (solo stdlib) con `capturar` y `listar`, y
     `test_pendientes.py`;
   - `utils/hooks/hooks.json` (`SessionEnd`, `${CLAUDE_PLUGIN_ROOT}`);
   - la línea diaria en el agente de launchd (`tarea/assets/presencia-instalacion.md`).
4. **Assets:**
   - `para-claude.esqueleto.md` pasa a ser `pendientes.esqueleto.md`;
   - `historial.esqueleto.md` con `Descartadas`;
   - `plan.esqueleto.md` con el marcador `slug` y la sección «Esto te toca a ti»;
   - `claude-md-puntero.md` ya no copia la regla de ramas: queda en una línea que remite al gancho.
4b. **Guardia de git:**
   - `utils/hooks/guardia_git.py` (solo stdlib) y `test_guardia_git.py`, que cubren commit, merge y
     push sobre ramas protegidas, el permiso de un solo uso, su vencimiento y las excepciones;
   - registro de los ganchos `PreToolUse` (Bash) y `UserPromptSubmit` en `utils/hooks/hooks.json`;
   - el permiso se guarda en `~/.claude/utils/aprobaciones/<repo>.json`;
   - una línea en el cierre de `tarea-repo` («el merge y el push los desbloquea tu "apruebo el
     merge"»);
   - 3–4 líneas en `~/.claude/CLAUDE.md`: el gancho existe, se trabaja en rama, se pide la frase
     después de mostrar el resultado y no se rodea el bloqueo;
   - en `CLAUDE.md` de este repo, la sección «Cómo avanzamos» deja de copiar la regla.
5. **Migración (`modo-migracion.md`, `migrar_a_toggl.py` y su test):**
   - desde el formato antiguo, a Toggl va solo lo que hace el usuario; el resto va a `pendientes.md`;
   - submodo **5.0 → 6.0**:
     - renombrar `para-claude.md`;
     - proponer, una por una y con tu sí, qué tareas de Toggl que ejecuta Claude pasan a
       `pendientes.md`;
     - actualizar el bloque del `CLAUDE.md`.
6. **`balance`:** agregar «Lo abierto» y que «plan contra realidad» se omita en silencio si no hay un
   plan guardado. **`agenda` y `plan-semanal`:** solo cambia el nombre del archivo; quedan en reposo,
   porque el usuario planifica a mano. Evals que nombran `para-claude` o el ciclo de Toggl.
7. **Este repo y el global:**
   - se crea `tareas/pendientes.md` vacío;
   - se anota en `tareas/por-revisar.md` la idea sin decidir: «Obligar a decidir las entradas de
     `pendientes.md` con más de 3–4 semanas (hacer o descartar con motivo)»;
   - `~/Obsidian/Global/para-claude.md` pasa a `pendientes.md`;
   - `tareas/toggl.md` pasa a llamarse `tareas/config.md`, y su marcador
     (`<!-- tarea: toggl · … -->`) se mantiene tal cual;
   - en `tareas/config.md` § Reglas, **congelado hasta 2026-10-16**: solo arreglos, y las molestias
     se anotan en la bandeja.
7b. **Renombrar `toggl.md` a `config.md` en todo utils:**
   - skills, referencias y el asset (`toggl.esqueleto.md` pasa a ser `config.esqueleto.md`, en
     `tarea` y en `tarea-repo`);
   - scripts (`cola.py`, `presencia.py`, `migrar_a_toggl.py`, `pendientes.py`, la guardia) y sus
     tests;
   - **los scripts leen `config.md` y, si no existe, `toggl.md`**, así los repos sin migrar siguen
     funcionando;
   - el submodo de migración 5.0 → 6.0 renombra el archivo;
   - **detección:** si en el Paso 0 de `tarea-repo` existe `toggl.md` y no `config.md`, el repo
     está en 5.0. Se dice en una línea y se propone la migración (con `para-claude.md`, igual), como
     hoy se hace con el formato antiguo de `tareas.md`.
8. **Documentación y versiones:**
   - `CLAUDE.md` (párrafo de utils y «Cómo avanzamos»), `docs/skills.md` y `README.md`;
   - `plugin.json` y `marketplace.json` pasan a **6.0.0**;
   - `metadata.version` sube a 6.0.0 en `tarea`, `tarea-repo`, `balance`, `agenda` y `plan-semanal`.
9. **Cierre:** historial, commit, y merge + push **con tu visto bueno después de ver el resultado**.

Los otros repos (CDZ, web-reports y odc-clusters) se migran con `--migrar` cuando los abras, cada uno
en su rama.

## Verificación

- `python3 -m json.tool` sobre `marketplace.json`, `plugin.json` y `hooks.json`; comprobar que la
  versión es la misma en `plugin.json` y `marketplace.json`.
- `python3 -m unittest` en `tarea/scripts/` y `tarea-repo/scripts/`.
- `pendientes.py capturar` sobre una copia en el scratchpad, con una rama sin mergear y un plan a
  medias:
  - crea una sola entrada;
  - ejecutado otra vez, no la duplica;
  - con la rama ya mergeada, no añade nada.
- `grep -rn "para-claude\|In Progress\|objetivo del usuario" utils docs CLAUDE.md README.md` solo debe
  devolver menciones históricas.
- `wc -c` del cuerpo de cada `SKILL.md` y de cada referencia tocada, dentro del presupuesto.
- La guardia, en un repo de prueba dentro del scratchpad, **en modo automático**:
  - un commit en `main` se bloquea;
  - en una rama, el commit pasa;
  - `git merge` y `git push` a `main` se bloquean;
  - tras escribir «apruebo el merge», pasan una sola vez;
  - pasados 10 minutos, el permiso vence;
  - un permiso creado en otra sesión no destraba el merge;
  - con un error forzado en el script, el comando se bloquea;
  - `git -C`, `HEAD:main` y `gh pr merge` se bloquean;
  - escribir en el archivo de permisos se bloquea;
  - con solo `toggl.md` (un repo sin migrar), la rama destino se sigue leyendo.
- Si el bloqueo no se aplica en modo automático, la tarea no se cierra y se avisa.
- Este mismo plan termina con su propia sección «Esto te toca a ti».

## Esto te toca a ti

1. Desde hoy, abrir, cronometrar y cerrar tus tareas a mano en Toggl (~5 min al día).
2. Después de la migración, revisar en Toggl las tareas que ejecuta Claude y confirmar cuáles pasan a
   `pendientes.md` (~15 min, una vez).
3. El 16 de octubre, revisar la bandeja con las molestias de estas dos semanas y decidir los ajustes
   (~30 min).

## Notas

- `tarea/assets/toggl.esqueleto.md` no se renombró: es la configuración **global** de Toggl, no la
  del repo; el nombre es correcto.
- Las versiones de los skills son independientes (regla de `CLAUDE.md`): `tarea` y `tarea-repo`
  6.0.0, `balance` 1.7.0, `agenda` 2.1.1, `plan-semanal` 2.0.5.
- El comentario de `cola.py` no se tocó: «subtareas, lo que te toca a ti» sigue siendo cierto.
- La guardia deja pasar sin permiso el push de commits que solo tocan la bandeja, los pendientes o
  el historial, para no pedir aprobación por cada anotación.
- La captura diaria corrió en vivo durante el trabajo (el agente de launchd ejecuta el
  `presencia.py` del repo, en la rama que esté activa) y escribió un `pendientes.md` sin versionar en
  odc-clusters, que todavía usa el formato antiguo. Se borró, y la captura quedó limitada a los repos
  en utils 5 o 6.
- La guardia no se pudo probar en vivo: los ganchos del plugin se cargan desde la versión
  instalada. Las 20 pruebas cubren lo verificable; la prueba en vivo quedó en `pendientes.md`.

