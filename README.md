# webmometro-plugins

Marketplace personal de plugins de Claude Code para Webmometro. No es una
aplicación: no hay build, test ni lint — los "artefactos" son skills en
Markdown, agentes, comandos y manifiestos JSON que Claude Code carga
directamente.

Incluye cuatro plugins:

- **brand-voice-pro** — descubre materiales de marca, genera guías de voz y
  las aplica al contenido generado por IA.
- **design-system** — audita/documenta/extiende sistemas de diseño, produce
  carruseles para redes sociales y prompts de dirección de arte.
- **seo-suite** — suite de 10 skills de SEO/AEO: contexto estratégico,
  snapshots de datos, auditoría, CRO, clústeres de contenido, blueprints de
  landing y seguimiento de cambios.
- **utils** — utilidades personales: registro de actividad cross-cuenta y
  gestión de tareas por rama.

## Dónde ver qué hace cada skill

La lista completa de skills con una explicación breve de cada una, agrupada
por plugin, está en **[docs/skills.md](docs/skills.md)**. Para el detalle
exacto de activación y comportamiento de una skill puntual, revisa su
`SKILL.md` (p. ej. `seo-suite/skills/seo-audit/SKILL.md`).

## Estructura de manifiestos

```
.claude-plugin/marketplace.json     ← registro: una entrada por plugin (name, source, version, keywords)
<plugin>/.claude-plugin/plugin.json ← metadata del plugin (name, displayName, version, author, keywords)
<plugin>/skills/<skill>/SKILL.md    ← unidad central; el frontmatter dispara la auto-activación
```

## Versionado: cómo asegurar que Claude reconozca las actualizaciones

Claude Code detecta actualizaciones del marketplace comparando versiones en
los manifiestos, así que **cambiar código sin subir versión no es visible**
para el cliente. Dos invariantes se deben mantener siempre sincronizados:

1. El `name` de un plugin debe ser idéntico en `.claude-plugin/marketplace.json`
   y en el `plugin.json` de ese plugin.
2. Cada entrada de `marketplace.json` (`version`) debe coincidir con la
   `version` del `plugin.json` del plugin correspondiente.

Por lo tanto, al editar un plugin:

1. Sube el `version` (semver) en **ambos** archivos a la vez: el
   `plugin.json` del plugin y su entrada en `.claude-plugin/marketplace.json`.
2. Si además cambia algo a nivel de marketplace (se agrega/quita un plugin,
   cambia su descripción), sube también `metadata.version` en la raíz de
   `marketplace.json`.
3. Valida los JSON tocados antes de commitear:
   `python3 -m json.tool .claude-plugin/marketplace.json` y el `plugin.json`
   afectado.
4. Si el cambio es solo en una skill (`SKILL.md`), puedes además subir su
   `metadata.version` interno — es independiente del versionado del plugin,
   pero ayuda a rastrear cambios a nivel de skill.

Sin este paso, un usuario que ya tiene el plugin instalado puede no ver la
actualización disponible aunque el contenido en el repo ya haya cambiado.

Más contexto de convenciones (frontmatter, jerarquía cliente-workspace,
dependencias MCP) está en [CLAUDE.md](CLAUDE.md).
