# Lo pendiente: `pendientes.md`

Lo **decidido** que aún no se hace vive en **`tareas/pendientes.md`** (sin repo,
`~/Obsidian/Global/pendientes.md`, una sección `## <Proyecto>` por proyecto). Es solo de Claude: lo
del usuario está en Toggl, y lo que aún no se decide, en `por-revisar.md`. Si no existe, se crea
desde `assets/pendientes.esqueleto.md` al anotar la primera entrada.

## Las tres secciones

| Sección | Qué va |
| --- | --- |
| `Por hacer` | Decidido y no empezado: lo que delegó una revisión, lo que no cupo en la sesión |
| `A medias` | Empezado y detenido: tiene rama viva y plan con pasos sin hacer |
| `Espera tu decisión` | No se puede seguir sin una decisión del usuario |

Una entrada por línea:

```text
- **Título** · Área · rama `<rama>` o — · plan `planes/<slug>.md` o — · AAAA-MM-DD — qué falta · por qué quedó
```

**El porqué es obligatorio**: «decisión tuya», «bloqueo: <qué>», «sin tiempo en la sesión»,
«delegada en revisión», «sesión cerrada sin cierre» (lo escribe la captura). Sin él, en un mes no se
sabe si conviene seguir.

## Anotar

- **Claude**, cuando su trabajo se detiene sin cerrarse, o al cerrar con algo que quedó decidido y
  sin hacer: **sin preguntar**, y lo dice en una línea.
- **Una revisión de la bandeja** que decide «Para Claude» (`modo-revisar.md`).
- **La captura automática** (`scripts/pendientes.py capturar`, al cerrar la sesión y una vez al
  día): cada rama sin mergear que no figura aquí entra en `A medias`, con los pasos que faltan y si
  hay cambios sin commitear. Al retomarla, Claude completa el porqué con el usuario.

Lo que ya está aquí, en la bandeja o en el historial no se repite (`redaccion-tareas.md`).

## Retomar

Solo cuando el usuario lo pide («qué quedó pendiente», «sigue con X»):

1. `python3 scripts/pendientes.py listar` (o leer el archivo) y, de la entrada elegida, su plan.
2. **El estado en 2–3 líneas**: cuántos pasos van, cuál sigue, qué espera al usuario. No se le pide
   releer el plan.
3. Se sigue **en su rama** (`git switch <rama>`, al día con la destino si hace falta) o, si no la
   tiene, con la ceremonia de `modo-gestion.md`. `presencia.py marca --evento abrir` con el slug.

## Salir

Una entrada sale de una sola forma, y siempre **al historial**:

- **Hecha** → la entrada del historial del cierre (`modo-gestion.md`).
- **Descartada** → `## Descartadas` del mensual (`archivado.md`), con el motivo; si tenía rama, se
  borra solo con el sí del usuario.

## Git

Cambios a este archivo o a la bandeja **fuera de un trabajo abierto**: commit directo sobre la rama
destino con solo esos archivos y el mensaje `tareas: pendientes` (la guardia de git lo permite). Con
un trabajo abierto, van en su rama.

## Consultar

«Qué tiene Claude pendiente»: las tres secciones, tal cual, más el global si se pide todo.
`balance` las muestra cada semana en «Lo abierto», ordenadas por antigüedad.
