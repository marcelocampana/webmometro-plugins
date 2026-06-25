# Conectores

Este archivo traduce los marcadores genéricos (`~~...`) que usan los skills de este plugin a las herramientas reales que tienes conectadas en Claude (Claude Code / Claude Desktop).

Cuando un skill diga, por ejemplo, *"si **~~design tool** está conectado"*, busca aquí a qué corresponde y si está disponible.

## Marcadores usados en este plugin

| Marcador           | Qué representa                                          | Tu herramienta | Estado          |
| ------------------ | ------------------------------------------------------- | -------------- | --------------- |
| `~~design tool`    | Herramienta de diseño (componentes, variantes, tokens)  | _por definir_  | ⬜ no conectado |
| `~~knowledge base` | Base de conocimiento / wiki (documentación, guías)      | _por definir_  | ⬜ no conectado |

## Cómo completarlo

1. **`~~design tool`** — la app donde viven tus componentes y tokens. Ejemplos: Figma, Penpot, Sketch.
   - Sustituye `_por definir_` por el nombre real (p. ej. `Figma`).
   - Cambia el estado a ✅ cuando el conector/MCP esté activo.

2. **`~~knowledge base`** — donde documentas y publicas guías de componentes. Ejemplos: Notion, Confluence, una wiki interna.
   - Sustituye `_por definir_` por el nombre real (p. ej. `Notion`).
   - Cambia el estado a ✅ cuando esté conectado.

## Notas

- Si un marcador aparece como ⬜ **no conectado**, el skill simplemente omite los pasos que dependen de esa herramienta y trabaja con lo que tenga en el contexto.
- Mantén esta tabla actualizada cuando conectes o desconectes herramientas, para que los skills sepan de qué pueden disponer.
