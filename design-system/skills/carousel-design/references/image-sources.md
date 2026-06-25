# Fuentes de imágenes — Resolución por tipo

Este archivo cubre cómo resolver imágenes que no están en el directorio local del carrusel.

## Orden de preferencia

1. **Carpeta local del carrusel** (`{raiz}/[cliente]/rrss/[carrusel]/assets/`) — siempre primero
2. **Carpeta local indicada por el usuario** — si da otra ruta, usarla
3. **Google Photos / Google Drive** — ver sección abajo
4. **Pausa** — si el usuario no tiene las imágenes listas

## Google Photos / Google Drive

Acceder usando el primer mecanismo disponible en este orden:

1. **Conector de Claude para Google** (si está activo en la sesión) — opción preferida porque está integrada nativamente.
2. **CLI local instalada** (`rclone`, `gphoto`, `gdrive` u otra disponible en `$PATH`) — segunda opción, estable.
3. **MCP de Google** (`mcp__google-photos`, `mcp__google-drive` o equivalentes).

Si ninguno está disponible: informar al usuario que la integración no está activa y pedirle que descargue las imágenes a una carpeta local antes de continuar.

Una vez obtenidas las imágenes, guardarlas en `assets/` del carrusel antes de continuar. Toda referencia desde el HTML final debe ser por ruta local — nunca URL remota.

## Pausa sin imágenes

Si el usuario indica que aún no tiene las imágenes listas: pausar el flujo aquí. No avanzar a la propuesta ni a la producción. Reanudar cuando el usuario confirme que las imágenes están disponibles.
