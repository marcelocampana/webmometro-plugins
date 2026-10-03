<!-- tarea: toggl · proyecto 3968609 «Plugins IA» · cliente 762706 «Interno» -->

# Configuración · Plugins IA

Configuración del sistema de tareas en este repo: la rama destino (la lee también la guardia de
git), las áreas, el proyecto de Toggl donde van las tareas que el usuario elige y las reglas propias.

## Rama destino

`main`

## Áreas

Cada plan, pendiente y fila del historial lleva una de estas áreas; las tareas que van a Toggl la
llevan como etiqueta y en la primera línea de la descripción (`Área: <nombre>`).

| Área | Qué abarca |
| --- | --- |
| General | Documentación raíz (`README.md`, `CLAUDE.md`, `docs/`), configuración y todo lo transversal a los cuatro plugins. |
| Manifests | `.claude-plugin/marketplace.json` y los cuatro `plugin.json`. Vive aparte porque un bump de versión toca dos archivos a la vez: es una sola tarea aquí, nunca una fila duplicada por plugin. |
| brand-voice-pro | Los skills, agents, commands y el `.mcp.json` del plugin. Es el único con las cuatro piezas. |
| design-system | Los tres skills del plugin: `carousel-design`, `design-system` e `image-prompt`. |
| seo-suite | Los diez skills de la suite SEO y el flujo que los encadena (snapshots → análisis → tracking). |
| utils | Los skills del plugin: `agenda`, `balance`, `plan-semanal`, `tarea` y `tarea-repo`. |

## Reglas

- **utils congelado hasta el 2026-10-16.** Solo se arreglan fallos; las molestias con el sistema de
  tareas se anotan en `por-revisar.md` y se ajustan juntas después de esa fecha, con evidencia.

## Comentarios

<!-- Opcional. -->
