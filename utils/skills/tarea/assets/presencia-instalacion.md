# Instalar el registro de presencia

Dos piezas, las dos locales y sin credenciales. **Cada paso cambia la configuración del usuario:
se propone y se espera su visto bueno en el momento**, nunca se instala de pasada.

## 1. Arranque al encender el Mac (actividad y aplicación)

```bash
SCRIPT="$HOME/Github/AI-kit/plugins/webmometro-plugins/utils/skills/tarea/scripts/presencia.py"
sed "s#{{RUTA_SCRIPT}}#$SCRIPT#" "$(dirname "$SCRIPT")/../assets/presencia.plist.ejemplo" \
  > ~/Library/LaunchAgents/com.webmometro.tarea.presencia.plist
launchctl load ~/Library/LaunchAgents/com.webmometro.tarea.presencia.plist
```

Se usa la ruta del repo, no la del caché del plugin: el caché cambia con cada versión y dejaría el
arranque apuntando a un archivo borrado.

**Comprobar:** tras dos minutos, `tail -2 ~/.local/share/tarea/presencia/$(date +%F).log` muestra
líneas `mac`.

Este mismo arranque da el **aviso de pausa como notificación de macOS** cuando la sesión continua pasa
de `sesion_min`, aunque el usuario no le esté escribiendo a Claude. Comparte estado con el gancho del
paso 2: el aviso sale por uno o por otro, nunca por los dos. La primera vez macOS puede pedir permiso
de notificaciones para «Editor de Scripts»; sin él, el aviso queda solo en la conversación. Se apaga
con `notificar_mac` = 0 en la configuración global.

**Quitar:** `launchctl unload ~/Library/LaunchAgents/com.webmometro.tarea.presencia.plist` y borrar
el archivo. Los registros de `~/.local/share/tarea/presencia/` se conservan hasta que se borren.

## 2. Gancho de mensajes y aviso de pausa

En `~/.claude/settings.json` —compartido por todas las cuentas y aplicaciones de Claude Code del
Mac—, dentro de `hooks`:

```json
"UserPromptSubmit": [
  { "hooks": [ { "type": "command",
    "command": "python3 \"$HOME/Github/AI-kit/plugins/webmometro-plugins/utils/skills/tarea/scripts/presencia.py\" mensaje" } ] }
]
```

Si ya hay otros `UserPromptSubmit`, se añade al lado; no se reemplazan. El gancho nunca falla hacia
fuera ni bloquea el mensaje: en el peor caso no anota nada.

**Comprobar:** tras enviar un mensaje, el log del día tiene una línea `mensaje` con el proyecto.

**Quitar:** borrar esa entrada de `settings.json`.

## 3. El registro de tiempo de Claude

**El tiempo de Claude no va a Toggl** (Toggl es solo del usuario). `presencia.py asentar` lo escribe
en `~/Obsidian/global/claude/registro-tiempo/<proyecto>-AAAA-MM.md` (o `CLAUDE_TIEMPO_DIR`): un
archivo por proyecto de Toggl y mes, una fila por tramo, con la tarea que estaba abierta en el repo o
`—`. Corre al cerrar cada tarea y, además, **el mismo agente de launchd lo lanza una vez al día**: así
nada se pierde aunque pasen semanas sin cerrar nada, antes de que Claude Code borre sus sesiones (30
días). Es idempotente: solo añade lo nuevo desde el último asiento.

**Comprobar:** `presencia.py asentar` y abrir el archivo del proyecto del mes.

La rutina nocturna que enviaba este tiempo a Toggl (`enviar-claude-sin-tarea`) ya no hace falta.
**Tu tiempo frente al computador tampoco se envía**: lo cronometras tú, y `mi-tiempo` queda como
consulta local.

## Qué no hace

No lee títulos de ventana, contenido de mensajes ni la pantalla. No habla con Toggl: a Toggl solo
escribe el skill `tarea` (tus tareas y sus estados), desde una sesión.
