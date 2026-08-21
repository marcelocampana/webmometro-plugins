# Skills disponibles

Resumen breve de para qué sirve cada skill, agrupado por plugin. Ver el
`SKILL.md` de cada carpeta para el detalle completo y los criterios exactos
de activación.

## brand-voice-pro

Gestión de voz de marca: descubrir materiales, generar guías y aplicarlas al
redactar contenido.

- **discover-brand** — Busca de forma autónoma materiales de marca ya
  existentes en plataformas conectadas (Notion, Confluence, Google Drive,
  Box, SharePoint, Figma, Gong, Granola, Slack) y entrega un reporte de
  descubrimiento.
- **guideline-generation** — Genera guías de voz de marca a partir de
  documentos, transcripciones de llamadas, grabaciones o un reporte de
  discover-brand, consolidando todo en una guía única.
- **brand-voice-enforcement** — Aplica las guías de marca ya existentes al
  crear contenido (emails, propuestas, posts, presentaciones, mensajes de
  Slack, etc.), asegurando que el resultado suene "on-brand".

## design-system

Sistema de diseño, piezas visuales para redes sociales y prompts de
generación de imágenes.

- **design-system** — Audita, documenta o extiende un sistema de diseño:
  detecta inconsistencias de nombres o valores hardcodeados en componentes,
  documenta variantes/estados/accesibilidad, o diseña un patrón nuevo
  coherente con el existente.
- **carousel-design** — Crea carruseles visuales (Facebook, Instagram,
  LinkedIn) a partir de texto ya redactado, respetando el sistema de diseño
  y la voz del cliente. No redacta el copy, solo diseña las piezas.
- **image-prompt** — Convierte una idea simple en un prompt de dirección de
  arte listo para pegar en ChatGPT Imágenes (u otras herramientas como
  Midjourney, Flux, SDXL), respetando la identidad visual del cliente e
  infiriendo el tipo de imagen y su destino.

## seo-suite

Suite completa de SEO/AEO: contexto estratégico, snapshots de datos,
auditorías, optimización de conversión, arquitectura de contenido y
seguimiento de cambios.

- **site-context** — Crea y mantiene el contexto estratégico de un sitio
  (posicionamiento, audiencia objetivo, ICP, diferenciación, voz de marca)
  en `contexto/sitio.md`, que otras skills de la suite usan como referencia.
- **site-snapshot** — Genera un snapshot factual de datos de todo un sitio o
  dominio (analytics, Search Console, performance, comportamiento). Solo
  extrae datos, no diagnostica ni recomienda.
- **page-snapshot** — Genera un snapshot factual de una página específica.
  Se activa únicamente con el comando `/page-snapshot`, nunca por contexto.
- **seo-audit** — Audita y diagnostica problemas de SEO técnico y on-page de
  un sitio (caídas de tráfico, pérdida de rankings, Core Web Vitals,
  indexación, etc.). Requiere `site-context` y `site-snapshot` previos.
- **ai-seo** — Audita y optimiza contenido para motores de búsqueda con IA
  (AEO/GEO/LLMO): visibilidad en AI Overviews, citas de LLMs como ChatGPT,
  Perplexity, Claude o Gemini. Funciona con páginas ya publicadas o
  contenido en borrador antes de publicar.
- **page-cro** — Optimiza la tasa de conversión de cualquier página de
  marketing (home, landing, pricing, blog). Requiere un `page-snapshot`
  previo de la página.
- **audience-demand-evaluation** — Evalúa si una audiencia objetivo es
  alcanzable vía búsqueda orgánica o si conviene un canal de adquisición
  alternativo. Usa MCPs para validar demanda, no es extracción de datos.
- **content-cluster-builder** — Construye un clúster de contenido (pilar +
  spokes) con autoridad temática a partir de un tema semilla.
- **landing-blueprint** — Decide qué secciones debe tener una landing page y
  en qué orden, con justificación y nivel de confianza por sección. No
  aplica cuando la landing ya existe y se quiere diagnosticar por qué no
  convierte (eso es `page-cro`).
- **seo-change-tracker** — Registra cambios SEO/AEO implementados (title,
  meta description, redirects, contenido publicado, schema, GBP, etc.) para
  poder medir su impacto después, y genera reportes ejecutivos agregados de
  lo ya registrado.

## utils

Utilidades transversales de organización del trabajo.

- **claude-activity-log** — Mantiene un registro persistente y cross-cuenta
  de las tareas realizadas en Claude, para no perder el rastro de en qué
  cuenta, proyecto y contexto se hizo cada cosa.
- **task-flow** — Gestiona las tareas de un proyecto en el directorio
  `tareas/`: cola de tareas con flujo "una tarea, una rama, un commit",
  bandeja de revisión y auditoría por áreas. Solo se activa si el proyecto
  ya tiene esa estructura o si el usuario pide montarla.
