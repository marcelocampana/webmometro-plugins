---
name: content-cluster-builder
description: >
  Construye un clúster de contenido (pilar + spokes) con autoridad temática a partir de un tema
  semilla. Usa cuando el usuario quiera "crear un clúster de contenido", "planificar artículos
  alrededor de un tema", "construir autoridad temática", "arquitectura pilar y spokes", "qué
  artículos escribir sobre [tema]", "organizar el contenido por tema", "estructura hub-and-spoke",
  "topic cluster" o "clúster SEO". Para registrar el impacto posterior de los artículos creados,
  ver seo-change-tracker.
metadata:
  version: 1.2.0
---

# Content Cluster Builder

Construye una arquitectura de contenido pilar-spoke con autoridad temática, a partir de un único
tema semilla. El skill investiga de forma autónoma (keywords, SERP, GSC, vault, brand voice) y
entrega un plan auditable más las notas reales de Obsidian listas para redactar.

**El contexto del negocio siempre se lee del proyecto, nunca se asume.** Este skill funciona igual
para una clínica estética que para un observatorio científico — la vertical, la ubicación y las
keywords semilla vienen del `config.md` o de lo que el usuario responda al inicio.

---

## Antes de empezar: contexto de negocio

Leer **`seo-tracking/config.md`** si existe — es la fuente de verdad compartida del proyecto
(dominio, GSC, GA4, ubicación SERP, keywords principales). Si no existe o le faltan campos, seguir
la guía en **`references/contexto-negocio.md`**: preguntar el mínimo al usuario y persistirlo.

Si el usuario no proporcionó la semilla, pedirla. Con eso es suficiente para arrancar el Paso 1.

---

## Modo 1 — Planificar el clúster

Ejecutar los pasos en orden. La metodología completa, los criterios de agrupación y las tablas de
salud están en **`references/metodologia-cluster.md`**. El mapeo de herramientas MCP está en
**`references/fuentes-datos-mcp.md`**.

### Forma del informe (importante: el orden de los pasos ≠ el orden del entregable)

Los 7 pasos de abajo son el orden de la **investigación**. El **informe que presentas NO se ordena
por número de paso.** Quien lo lee necesita accionar el clúster, no re-derivarlo: primero quiere ver
*qué temas son* y *cómo se desarrolla cada uno*; la justificación metodológica solo la abre si
quiere auditar o defender una decisión. Si pones la expansión de keywords, el inventario y los
cálculos al frente, el lector tiene que scrollear medio documento para llegar a lo que vino a buscar.

Por eso el informe sigue el orden ejecutivo de **`assets/mapa-cluster.template.md`**:

1. **Resumen ejecutivo** — pilar, nº de spokes, volumen y una línea de **"Decisiones clave y alertas"**.
2. **El clúster** — el árbol pilar→spokes de un vistazo.
3. **Desarrollo de cada tema** — el corazón: H1/H2 + ángulo de marca por pieza.
4. **Roadmap de producción**.
5. **Mapa de enlazado interno**.
6. **Sustento y análisis** — todo lo metodológico (expansión, inventario, solape de SERP,
   canibalización, cobertura, scorecard+gates, notas), **plegado en bloques `<details>`**. Presente
   para auditabilidad, nunca al frente.

Genera la evidencia en cada paso, pero al redactar el informe colócala donde corresponde según esta
forma, no en el orden en que la fuiste produciendo.

### Paso 1: Expandir la semilla

Usar DataForSEO Labs para obtener keywords relacionadas, variantes long-tail y preguntas PAA.
Complementar con las keywords reales por las que el sitio ya aparece en Google, via GSC.

Objetivo: 50–150 keywords candidatas con volumen, KD y CPC.

Si una fuente MCP no responde: dejar el campo en `null`, informarlo al usuario y continuar con las
fuentes disponibles — no bloquear el flujo por una fuente caída.

### Paso 1a: Inventario de contenido existente en el sitio

Antes de proponer cualquier tema, **verificar qué ya existe en el sitio web** — no solo lo que
GSC reporta con tráfico. Una página puede existir sin recibir clics (mal posicionada, recién
publicada, o nunca descubierta por GSC) y aun así no ser un GAP: sería un `parcial` a optimizar,
no contenido a crear desde cero. Proponer crear algo que ya existe es trabajo duplicado.

**Mapear las URLs del sitio:** parsear el sitemap del dominio (`list_sitemaps` + `get_sitemap` de
GSC). Filtrar las URLs cuyo slug o ruta se relacione semánticamente con la semilla y sus variantes
— no auditar el sitio entero, solo el subconjunto temáticamente relevante.

**Auditar las URLs relevantes:** abrir cada una con WebFetch y clasificar de qué trata y su tipo
(siguiendo `references/auditoria-intencion-url.md`). Esto produce un inventario real:
- qué subtemas del clúster **ya tienen página** (aunque no rankeen)
- qué páginas están desalineadas o son débiles (candidatas a optimizar)
- qué subtemas son GAP genuino (no existe nada)

Este inventario alimenta directamente el coverage del Paso 4 y evita proponer temas duplicados.

Si el dominio no tiene sitemap accesible, informarlo y caer en GSC + SERP como mejor aproximación
disponible — no bloquear el flujo. Para un inventario exhaustivo de sitios grandes, ofrecer el
crawl con `onpage_*` de DataForSEO (consume créditos; ver `references/fuentes-datos-mcp.md`).

### Paso 1b: Identificar y confirmar la URL pilar con el usuario

Este paso ocurre justo después del inventario (antes de filtrar o clusterizar) porque ya tiene
los candidatos reales del sitio. Es el único punto donde el usuario toma una decisión activa
sobre la arquitectura antes de ver el plan completo.

**Descubrir candidatos:** cruzar el inventario del Paso 1a con los datos de GSC para identificar
qué URLs del propio dominio ya cubren la semilla o sus variantes principales. Presentar al usuario
una tabla concisa:

| URL | Posición media | Clics/mes | Tipo inferido (preliminar) |
|---|---|---|---|
| /ruta/al-servicio | 6.6 | 42 | transaccional (inferido) |

Si el usuario ya mencionó una URL en su mensaje inicial, usarla como candidata sin preguntar de
nuevo — solo confirmar.

**Preguntar al usuario:**
- Si hay candidatos: "¿Es esta la página pilar del clúster, o prefieres otra URL?"
- Si no hay candidatos: "¿Ya existe una página sobre este tema en el sitio? Si es así, comparte la
  URL. Si no existe aún, ¿qué tipo de contenido quieres crear para el pilar: transaccional
  (página de servicio/venta), informativo (guía/hub educativo), o comercial (comparativa/decisión)?"

**Con la URL confirmada → auditar de inmediato:**
Seguir el procedimiento de `references/auditoria-intencion-url.md`: abrir la página con WebFetch,
clasificar `tipo_pagina_actual` e `intencion_satisfecha`. Luego presentar el hallazgo al usuario:

> "Revisé la página. Es de tipo **[transaccional / informacional / comercial / mixta]**: [señales
> observadas en 1-2 líneas]. ¿Confirmas que este es el enfoque correcto, o la página debería
> tener un tipo distinto?"

Esperar confirmación antes de continuar. El tipo confirmado es el contrato del Paso 5.

**Si no existe URL (GAP):** el tipo declarado por el usuario define directamente el tipo del pilar
— no se necesita auditoría de página. Continuar al Paso 2.

### Paso 2: Filtrar, etiquetar intención y capturar la voz del buscador

Eliminar keywords de marca, duplicados y las que caigan fuera de los umbrales de volumen/KD del
`config.md` (o los defaults de `metodologia-cluster.md`). Etiquetar cada keyword con su intención:
informacional, comercial, transaccional o local.

**Capturar la voz del buscador:** además del volumen, analizar *cómo* pregunta la gente —
queries reales de GSC, People Also Ask, sugerencias/autocomplete y, opcionalmente, comunidades.
Seguir `references/voz-del-buscador.md`: agrupar por subtema, detectar preguntas y objeciones
recurrentes, y conservar el lenguaje textual del usuario. Este material define los H2 y los
bloques FAQ en el Paso 5 — el contenido debe responder el lenguaje real, no uno inventado.

### Paso 3: Clusterizar por solapamiento de SERP + intención dominante

Consultar el top-10 orgánico de Google en vivo para las keywords candidatas más prometedoras,
geolocalizado según `config.md`. Agrupar por URLs compartidas en los resultados — no por similitud
de texto. Ver criterios exactos en `references/metodologia-cluster.md`.

Esta es la diferencia clave frente a enfoques semánticos: si Google muestra los mismos resultados,
trata los términos como el mismo tema.

**Además de agrupar, clasificar la intención dominante de la SERP** para cada keyword cabeza del
clúster (transaccional / comercial / informacional / local), según la heurística de
`references/auditoria-intencion-url.md`. Registrar `intencion_serp_dominante` por keyword: es la
señal de qué tipo de contenido premia Google y debe guiar la asignación de roles en el Paso 5.

### Paso 4: Cobertura + auditoría de contenido e intención

Dos sub-tareas que deben hacerse juntas:

**4a. Coverage en sitio + vault:** combinar dos fuentes para clasificar cada subtema como
cubierto / parcial / gap:
- **Sitio web:** el inventario del Paso 1a — qué páginas ya existen y su estado (sólida, débil,
  desalineada, inexistente).
- **Vault:** buscar con Grep/Glob si ya existen notas de Obsidian sobre el subtema.

Un subtema con página existente pero débil es `parcial` (optimizar), no `gap` (crear). No declarar
GAP sin haber revisado el inventario del sitio.

**4b. Auditoría de URLs propias (spokes y páginas no-pilar):** para cada URL del propio dominio
que rankea keywords del clúster y que **no es la URL pilar** (ya auditada en el Paso 1b), abrir
la página y auditar su contenido siguiendo `references/auditoria-intencion-url.md`. Clasificar
`tipo_pagina_actual`, `intencion_satisfecha` y `coincide_con_serp`.

La cobertura es bidimensional: *existe* (cubierto/parcial/gap) × *alineada* (alineado/desalineado).
Una página alineada con su SERP no se toca en su intención — solo se puede enriquecer o reenlazar.

**4c. Chequeo de canibalización contra URLs propias:** para cada pieza nueva que se vaya a crear
(gap), comparar la SERP en vivo de su keyword objetivo contra las SERPs de las URLs propias que ya
rankean en el clúster. Si comparten **más del 40% de URLs en el top-10**, hay riesgo de
canibalización: Google trata ambos términos como la misma intención y la pieza nueva competiría
contra una página existente. En ese caso, no crear la pieza nueva: fundir el subtema en la página
existente (expandirla) o reorientar la keyword objetivo a un ángulo long-tail con SERP distinta.
Registrar el overlap medido por par para el gate del Paso 7. Ver la tabla de umbrales en
`references/metodologia-cluster.md` y la herramienta en `references/fuentes-datos-mcp.md`.

### Paso 5: Arquitectura pilar + spokes + auditoría de ajustes

Usar el tipo de pilar **ya confirmado por el usuario en el Paso 1b** — no renegociar aquí.
Aplicar la **matriz de asignación de rol** de `references/metodologia-cluster.md` para validar
que el tipo confirmado es coherente con la intención dominante de la SERP. Nominar 3–7 spokes.
Proponer H1 y 3–5 H2 para el pilar; H1 y 3–4 H2 para cada spoke.

La salida de este paso es la pieza principal del informe: el árbol pilar→spokes va en la sección
**"El clúster"** y el detalle por pieza (H1, H2, ángulo de marca, intención, estado, enlaces) va en
**"Desarrollo de cada tema"** del template — esa sección es lo primero que el usuario quiere leer,
así que debe quedar completa y autosuficiente sin obligar a bajar al sustento.

**Derivar H2 y FAQ de la voz del buscador (Paso 2):** los H2 y los bloques FAQ de cada pieza deben
salir de las preguntas y el lenguaje real capturados, no de suposiciones. Usar el doble destino de
`references/voz-del-buscador.md`: preguntas con volumen → spoke propio; sub-preguntas sin volumen →
bloque FAQ del pilar o del spoke más cercano. Aplicar la plantilla de respuesta FAQ de ese
reference.

**Auditoría de ajustes del pilar:** con el tipo confirmado y el análisis del clúster en mano,
evaluar qué le falta a la página actual para cumplir su rol de hub. Presentar al usuario una lista
concreta de ajustes recomendados, por ejemplo:

- Añadir sección "Precio del tratamiento" con enlace al spoke de precio
- Añadir sección "Tiempo de recuperación" con enlace al spoke de recuperación
- Incluir galería de antes/después más amplia (ya rankea en pos 2 sin página dedicada)
- Añadir enlazado interno a los 5 spokes desde las secciones relevantes

Esta auditoría no es un rediseño de la página — es un diff entre lo que tiene hoy y lo que
necesita para ser el hub del clúster, respetando su tipo e intención.

**Si el tipo confirmado no coincide con la intención dominante de la SERP** (desajuste detectado
en Paso 3 pero no resuelto en Paso 1b): exponer el desajuste con evidencia (qué tipo de páginas
rankean vs qué tipo es el pilar) y esperar nueva decisión del usuario antes de continuar.

Si el proyecto tiene una guía de brand voice, descubrirla buscando por nombre (archivos con "brand",
"voice", "tono" o "voz" en la ruta; ver `references/fuentes-datos-mcp.md`) y usarla para que los
títulos suenen al negocio, no genéricos. Si no existe, continuar sin ella.

Mapear el enlazado interno: pilar ↔ todos los spokes; spokes ↔ 2–4 hermanos donde sea natural.

### Paso 6: Priorizar el orden de producción

Calcular el score de oportunidad de cada pieza: volumen (40%) + KD inverso (30%) + intención
comercial/local (30%). Ordenar la producción: primero los gaps de mayor score.

### Paso 7: Scorecard de salud

Antes de presentar el plan, correr `scripts/salud_cluster.py` (si el clúster ya tiene notas en el
vault) o calcularlo manualmente con las tablas de `metodologia-cluster.md`. Incluir el gate
"Coherencia de intención" (ver `metodologia-cluster.md`). Si algún gate de tolerancia-cero falla,
marcar el mapa como "necesita revisión" y explicar qué falla y por qué.

El gate "Canibalización" **no lo computa el script** (necesita SERP en vivo, no archivos locales):
poblarlo con el overlap medido en el Paso 4c. Si algún par supera el 40%, el gate falla aunque el
script lo marque como ⚠️ no calculable.

**Presentar el plan al usuario para revisión antes de materializar.** Estructurar el informe en el
**orden ejecutivo** de `assets/mapa-cluster.template.md` (ver "Forma del informe" arriba): primero
el clúster y el desarrollo de cada tema, luego el roadmap y el enlazado, y al final el bloque
**"Sustento y análisis"** con toda la evidencia plegada en `<details>` (expansión, inventario,
solape de SERP, canibalización, cobertura, scorecard+gates, notas). Las mediciones están ahí para
auditar, no al frente. Los gates que fallan o están en vigilancia se condensan en la línea
**"Decisiones clave y alertas"** del resumen ejecutivo, con la tabla completa de gates plegada en el
sustento. Esa plantilla es la fuente de verdad canónica del informe, tanto para el plan que se
muestra aquí como para la nota que se materializa en el Modo 2. El usuario puede ajustar la
arquitectura, cambiar prioridades o descartar spokes antes de que se creen las notas.

---

## Modo 2 — Materializar en Obsidian

Solo después de que el usuario apruebe el plan del Modo 1.

Generar las notas usando las plantillas de `assets/`:
- `assets/pilar.template.md` → nota pilar con frontmatter y `[[wikilinks]]` a los spokes
- `assets/spoke.template.md` → una nota por spoke con link al pilar y a sus hermanos
- `assets/mapa-cluster.template.md` → nota maestra del clúster con resumen, mapa y roadmap

**Ubicación de las notas:** preguntar al usuario si no está claro, o inferir de la estructura del
vault. Nunca crear notas en el directorio `.claude/`.

Los `[[wikilinks]]` deben usar el nombre exacto de la nota de destino. Verificar que ningún spoke
quede huérfano (sin enlace desde el pilar) antes de dar la tarea por terminada.

---

## Integración opcional con seo-change-tracker

Al terminar el Modo 2, ofrecer registrar el clúster como un cambio de área `contenido` en
`seo-change-tracker` para medir el impacto a 14 y 28 días. Si el usuario no quiere, no insistir.

---

## Manejo de errores

| Situación | Qué hacer |
|---|---|
| No hay `seo-tracking/config.md` | Seguir guía en `references/contexto-negocio.md` y crear contexto mínimo |
| Un MCP no responde | Dejar campo `null`, informar, continuar con fuentes disponibles |
| La semilla devuelve <20 keywords | Avisar y preguntar si el usuario quiere ampliar o trabajar con lo disponible |
| El clúster falla un gate de salud | Presentar el fallo con su causa y proponer cómo resolverlo |
| La intención de una pieza no coincide con su SERP | Exponer el desajuste con evidencia, esperar decisión del usuario antes de continuar |
| Una URL pilar ya convierte y se querría cambiar su intención | No hacerlo por defecto — el Paso 1b confirma el tipo con el usuario antes de planificar; si hay desajuste con la SERP, señalarlo ahí |
| El usuario no aprueba el plan | Ajustar según feedback y volver a presentar antes de crear notas |

---

## Idioma

Comunicarse con el usuario en español neutro. Los H1/H2 y el contenido de las notas se generan en
el idioma configurado en `config.md` (o español por defecto).
