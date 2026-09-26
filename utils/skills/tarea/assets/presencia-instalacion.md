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

## Qué no hace

No lee títulos de ventana, contenido de mensajes ni la pantalla. No habla con Toggl: a Toggl solo
escribe el skill `tarea`, desde una sesión, al cerrar.
