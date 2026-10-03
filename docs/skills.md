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

- **tarea** — El sistema de tareas. **Toggl 2.0 es tuyo y lo llevas tú, a
  mano**: creas, planificas, cronometras y cierras. Claude solo crea en Toggl
  las tareas que eliges de la sección **«Esto te toca a ti»** con que termina
  su plan (lo que no puede hacer él y te ocupa tiempo; las decisiones no van),
  y lee tus registros para verificarlos contra tu actividad en el Mac. Su
  tiempo se asienta en un registro local por repo y mes
  (`~/Obsidian/Global/claude/registro-tiempo/`), nunca en Toggl. **Tu tiempo**
  frente al computador se mide aparte (`presencia.py`), con avisos de pausa.
  Lee Toggl por una copia local reducida (`cola.py`).
- **tarea-repo** — El trabajo de Claude en un repo con `tareas/`: plan
  (`tareas/planes/<slug>.md`) y rama desde la rama destino de
  `tareas/config.md` (`main` por defecto, o una de pruebas como `preview`),
  pasos encadenados sin preguntar y cierre en cadena —historial, commit,
  merge y push— con tu «apruebo el merge». **Nada de lo decidido se pierde**:
  lo que no se termina va a `tareas/pendientes.md` con su motivo, lo anotado
  sin decidir a `tareas/por-revisar.md`, y todo sale al historial, hecho o
  descartado con su porqué. Estima el coste desde el historial, audita el
  proyecto por áreas, ingiere tareas de una conversación o un archivo y migra
  los repos con formatos anteriores (`--migrar`).
- **Ganchos de utils** — La **guardia de git** bloquea, en todo repo y en
  cualquier modo de permisos, los commits sobre `main` y la rama destino, y el
  merge o push hacia ellas salvo que escribas «apruebo el merge» en esa
  sesión; falla cerrada. Al cerrar la sesión (y una vez al día) se anotan en
  `pendientes.md` las ramas que quedaron a medias.
- **agenda** — Compone la vista diaria con todos los proyectos: lee la cola
  de Toggl por la copia local y la jornada de Toggl, y responde qué toca hoy
  y si cabe. Avisa de lo vencido, de varias tareas abiertas a la vez y de las
  que no tienen estimación. **Solo lee**: nunca escribe en Toggl ni en un
  repo, que es lo que le permite correr desatendida desde una rutina.
- **plan-semanal** — Planifica la semana por día con todos los proyectos:
  propone qué tarea va cada día según la jornada y las estimaciones (dejando
  un 20% para imprevistos), y con visto bueno escribe el día y la estimación
  en Toggl y guarda la versión original para medir después plan contra
  realidad. Solo escribe días y estimaciones. Todo sigue funcionando si un
  lunes no se planifica (hoy está en reposo: planificas a mano).
- **balance** — Revisión para mejorar: **lo abierto** (lo cerrado en la
  semana, los pendientes por antigüedad, lo que espera tu decisión, la bandeja
  y las ramas sin mergear), tiempo de proyecto por cliente
  (Toggl) separado del tiempo real del usuario (registro de presencia),
  plan contra realidad, imprevistos, sesgo de estimación por familia de tarea, candidatas a
  automatizar, salud (sesiones sin pausa, horas frente al computador),
  uso de aplicaciones y tiempo que Claude trabajó solo. **Solo lee.**
