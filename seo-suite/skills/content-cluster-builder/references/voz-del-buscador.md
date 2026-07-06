# Voz del buscador: cómo busca y pregunta la gente

Reference compartido. Define cómo capturar **el lenguaje, las preguntas y las objeciones reales**
con que la gente busca un tema, y cómo convertirlas en estructura de contenido (subtemas, H2 y
FAQ). Lo usa `content-cluster-builder` en los Pasos 1–2 (captura) y Paso 5 (aplicación), pero es
independiente del clúster: cualquier skill que redacte contenido orientado a búsqueda puede
apoyarse aquí.

**El principio de fondo:** el volumen de una keyword dice *cuánta* gente busca; no dice *qué*
quiere saber ni *cómo* lo pregunta. Una pieza construida solo desde el volumen responde a una
keyword; una pieza construida desde la voz del buscador responde a una persona. El contenido que
rankea y convierte usa el lenguaje real del usuario, no uno inventado por quien escribe.

## Contenido

- [Fuentes y prioridad](#fuentes-y-prioridad)
- [Síntesis: de señales a preguntas](#síntesis-de-señales-a-preguntas)
- [Doble destino: spoke vs FAQ](#doble-destino-spoke-vs-faq)
- [Plantilla de respuesta FAQ](#plantilla-de-respuesta-faq)
- [Salida esperada](#salida-esperada)

---

## Fuentes y prioridad

Combinar varias fuentes; ninguna por sí sola da la imagen completa. Orden de fiabilidad para
*cómo* pregunta la gente (no para volumen):

| Prioridad | Fuente | Qué aporta | Herramienta |
|---|---|---|---|
| 1 | Queries reales del propio sitio | Lenguaje de 1ª mano: lo que la gente tecleó y *llegó al sitio* | `mcp__gsc__search_analytics` (dimensión `query`) |
| 2 | People Also Ask | Sub-preguntas y sub-intenciones que Google asocia al tema | `mcp__dataforseo__labs_google_keyword_ideas` con `include_serp_info=true`; o el bloque `people_also_ask` de `serp_google_organic_live` |
| 3 | Sugerencias / autocomplete | Variantes y modificadores (precio, duele, opiniones, cerca de mí…) | `mcp__dataforseo__labs_google_keyword_suggestions` |
| 4 | Comunidades y foros (opcional) | Lenguaje natural, dolores y objeciones que ninguna herramienta de pago genera sola | `mcp__dataforseo__business_data_reddit_search`; `content_analysis_*` para sentimiento |

Default gratis y suficiente: GSC + PAA + suggestions. Reddit/foros es profundización opcional —
ofrecerlo, no imponerlo (consume créditos y tiempo). Si una fuente no responde, continuar con las
demás; no bloquear.

---

## Síntesis: de señales a preguntas

No basta con listar queries. Convertirlas en estructura:

1. **Agrupar por subtema.** Mapear cada query/pregunta al subtema del clúster al que pertenece
   (precio, recuperación, antes/después, riesgos, etc.).
2. **Frecuencia.** Dentro de cada subtema, ordenar por cuántas veces aparece la misma pregunta o
   intención fraseada de distintas formas — la repetición señala qué importa de verdad.
3. **Detectar objeciones y dudas.** Buscar el subtexto: "¿duele?", "¿es seguro?", "¿cuánto tarda
   en sanar?", "¿vale la pena el precio?" son objeciones de compra disfrazadas de preguntas.
   Estas deciden conversiones, no solo tráfico.
4. **Anotar el lenguaje exacto.** Conservar las palabras del usuario (p. ej. "se me cae la piel"
   en vez de "flacidez cutánea") para usarlas en el contenido donde suene natural.

---

## Doble destino: spoke vs FAQ

Cada pregunta detectada va a uno de dos lugares — no confundirlos:

- **Spoke** — si la pregunta tiene volumen propio y SERP diferenciada, merece su propia página
  (ver criterios de solapamiento en `metodologia-cluster.md`). Ej.: "laser co2 recuperación".
- **Bloque FAQ** — si es una sub-pregunta sin volumen suficiente para página propia pero que la
  gente igual hace, va al FAQ del pilar o del spoke más cercano. Ej.: "¿puedo maquillarme después
  del láser?".

Regla práctica: una pregunta que aparece en PAA pero no como keyword con volumen es casi siempre
material de FAQ, no de spoke.

---

## Plantilla de respuesta FAQ

Para cada pregunta del bloque FAQ, responder en este orden (estructura que favorece featured
snippets y respuestas en buscadores con IA):

1. **Definición o respuesta directa** en la primera frase — sin rodeos.
2. **Pasos o criterios** si la pregunta los requiere (lista corta).
3. **Un ejemplo concreto** cuando aplique.
4. **Mini-FAQ** con las sub-preguntas adyacentes del PAA, si las hay.

Mantener cada respuesta concisa; el FAQ no es el cuerpo del artículo, es el cierre de dudas.

---

## Salida esperada

Por subtema del clúster, dejar registrado:

```
subtema: <nombre>
preguntas_con_volumen: [<query>, …]      → candidatas a spoke
preguntas_sin_volumen: [<pregunta PAA>, …] → bloque FAQ
objeciones_detectadas: [<duda/temor recurrente>, …]
lenguaje_real: [<frases textuales del usuario a reutilizar>]
fuentes: [gsc | paa | suggestions | reddit]
```

Esto alimenta la nominación de spokes (Paso 5), el diseño de H2 y los bloques FAQ de cada pieza, y
es reutilizable por cualquier skill de redacción orientada a búsqueda.
