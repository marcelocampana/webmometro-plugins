<!-- tarea: toggl · proyecto 3968609 «Plugins de IA» · cliente 741361 «Webmómetro» -->

# Toggl · Plugins de IA

Configuración de este repo en Toggl. Los pendientes viven allí; aquí, cómo se ordenan. Lo común a
todos los repos está en la configuración global de Toggl.

## Áreas

La primera línea de la descripción de cada tarea es `Área: <nombre>`, con uno de estos nombres.

| Área | Qué abarca |
| --- | --- |
| General | Documentación raíz (`README.md`, `CLAUDE.md`, `docs/`), configuración y todo lo transversal a los cuatro plugins. |
| Manifests | `.claude-plugin/marketplace.json` y los cuatro `plugin.json`. Vive aparte porque un bump de versión toca dos archivos a la vez: es una sola tarea aquí, nunca una fila duplicada por plugin. |
| brand-voice-pro | Los skills, agents, commands y el `.mcp.json` del plugin. Es el único con las cuatro piezas. |
| design-system | Los tres skills del plugin: `carousel-design`, `design-system` e `image-prompt`. |
| seo-suite | Los diez skills de la suite SEO y el flujo que los encadena (snapshots → análisis → tracking). |
| utils | Los skills del plugin: `agenda`, `balance`, `claude-activity-log`, `content-sync-check`, `documentar-proceso`, `plan-semanal`, `tarea` y `tarea-repo`. |

## Reglas

<!-- Opcional: lo propio de este repo en Toggl. -->

## Comentarios

<!-- Opcional. -->
