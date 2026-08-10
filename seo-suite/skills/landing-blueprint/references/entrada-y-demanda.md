# Entrada y demanda: qué busca quien necesita este servicio

Gobierna el **Paso 3**. Define de dónde salen las preguntas del visitante y, sobre todo, **qué
evidencia es admisible según cómo llegó a la página**.

El principio: el PAA, las queries y el volumen describen a alguien que *hizo una búsqueda*. Si el
visitante llegó por un anuncio de Instagram, un correo o una campaña PMax, nunca hizo esa búsqueda —
y tratar esos datos como si describieran sus preguntas es importar un supuesto y disfrazarlo de dato
con fuente y fecha.

El método de minería (herramientas, agrupación, doble destino, plantilla de respuesta FAQ) vive en
[../../content-cluster-builder/references/voz-del-buscador.md](../../content-cluster-builder/references/voz-del-buscador.md)
y es reutilizable por cualquier skill. **No lo dupliques aquí** — este reference define *qué es
admisible*, aquél define *cómo se obtiene*.

## Contenido

- [Tabla de admisibilidad por fuente de entrada](#tabla-de-admisibilidad-por-fuente-de-entrada)
- [Qué peso tiene el PAA según la entrada](#qué-peso-tiene-el-paa-según-la-entrada)
- [Message match: solo paid search](#message-match-solo-paid-search)
- [Conciencia derivada de la query, no supuesta](#conciencia-derivada-de-la-query-no-supuesta)
- [Tráfico mixto](#tráfico-mixto)
- [Tráfico sin query: cómo se construye el mapa](#tráfico-sin-query-cómo-se-construye-el-mapa)

---

## Tabla de admisibilidad por fuente de entrada

| Fuente de entrada | Qué se sabe del visitante | De dónde salen sus preguntas |
|---|---|---|
| **Orgánico** | La query exacta que tecleó | GSC (queries reales a la URL o al dominio) → **PAA de esas queries** → autocomplete/suggestions |
| **Google Ads — Search** | La keyword pujada y el anuncio que clicó | Keywords y términos de búsqueda de la campaña, copy del anuncio (**message match**), PAA/SERP de esas keywords |
| **Google Ads — PMax / Display / Demand Gen** | Nada de query: audiencia y creatividad | El anuncio y la audiencia; comportamiento del segmento en GA4/Clarity si la página existe. PAA solo como hipótesis de tema |
| **Meta / anuncio de WhatsApp** | La creatividad y el interés segmentado | Igual que PMax. Ojo: si es click-to-WhatsApp, **la conversión primaria puede ser abrir conversación**, no un formulario — eso reescribe la sección de fricción y la de "qué pasa después" |
| **Email a base propia** | La relación previa y el asunto que abrió | Objeciones de `sitio.md`, el mensaje que lo trajo, el segmento al que se envió |
| **Outbound / prospección** | Que no estaba buscando nada | Objeciones y el mensaje de origen. Máxima fricción de confianza |
| **RRSS orgánico** | El post que lo trajo | Igual que email: el mensaje de origen manda |

**Cómo se determina la fuente:** en auditoría sale de los canales GA4 del page-snapshot. En landing
nueva, si la página vive en una ruta real del sitio y hay presencia orgánica, el default es orgánico
y solo se confirma. **Nunca la preguntes de forma abierta cuando es inferible.**

---

## Qué peso tiene el PAA según la entrada

No es que no se pueda consultar. Es que **no puede clasificarse como evidencia de lo que pregunta
*este* visitante cuando este visitante nunca hizo una búsqueda.** Quien tecleó declaró su intención;
quien fue interrumpido por un anuncio, no.

Escala de peso:

1. **Como hipótesis de tema** — qué preocupaciones existen alrededor de este servicio en este
   mercado. **Admisible siempre**, con confianza **Media** como techo. Es útil justamente cuando no
   hay datos propios.
2. **Como evidencia de la pregunta del visitante** — solo con **orgánico** y **paid search**.
3. **Poder de promoción** — con tráfico sin query, el PAA **no dispara las reglas de promoción** de
   `sistema-de-decision.md`: no sube una sección a Esencial ni justifica la de orientación. Eso
   exige evidencia de query de entrada.

**Cómo queda etiquetado en la tabla de evidencia:**

```
Afirmación: "el visitante se pregunta cuánto dura la recuperación"
Fuente: PAA de "[servicio] recuperación" — Chile / es — 2026-08
Naturaleza: hipótesis de tema (el tráfico de esta landing es PMax, sin query)
Confianza: Media
Puede promover secciones: no
```

**Consecuencia práctica:** como el gate del Paso 3d solo autoriza una llamada que desbloquee una
decisión de sección, con tráfico sin query una consulta de PAA no pasa el gate por sí sola. La
restricción se aplica por diseño, sin necesidad de una prohibición aparte.

---

## Message match: solo paid search

Cuando el tráfico viene de búsqueda pagada, el visitante **ya aceptó una promesa** antes de llegar:
la del anuncio. El hero no parte de cero — tiene que continuar esa promesa.

**Qué pedir (opcional, nunca bloqueante):** el copy del anuncio (títulos y descripciones) y las
keywords del grupo de anuncios. No hay MCP de Google Ads configurado en la suite, así que lo aporta
el usuario o un brief. Si no llega, continúa y marca el message match como **no verificado** en los
metadatos del blueprint.

**Qué hacer con eso:**

- El **contrato de copy del hero** debe recoger la promesa del anuncio, no una distinta.
- Las objeciones que el anuncio ya neutralizó bajan de prioridad; las que despertó, suben.
- Si el anuncio promete algo que el sitio no sostiene —un precio, un plazo, un resultado sin
  respaldo— **regístralo como riesgo y exponlo al usuario**. No redactes encima del desajuste: la
  página cumpliría una promesa que el negocio no puede cumplir, y eso se paga después.

---

## Conciencia derivada de la query, no supuesta

El nivel de conciencia no se asume por el tipo de negocio: se lee de las queries de entrada. Reusa
las familias ya definidas en `audience-demand-evaluation` en vez de inventar una taxonomía nueva.

| Familia | Cómo se ve | Qué implica para la página |
|---|---|---|
| **problem-aware** | Describe el problema sin nombrar la solución ("se me cae el pelo") | No sabe qué servicio necesita → **orientación/triaje sube a Esencial** |
| **solution-aware** | Nombra la categoría de solución ("implante capilar FUE") | Ya decidió el qué, está eligiendo el quién → **orientación pasa a Excluida** |
| **category** | Busca la categoría de producto/servicio | Comparación y criterios de elección ganan peso |
| **brand** | Busca la marca por nombre | Ya te conoce: la página confirma y facilita, no convence desde cero |
| **local** | Incluye ciudad, barrio o "cerca de mí" | Prueba de proximidad y logística suben de prioridad |
| **comparison** | "X vs Y", "alternativa a X" | La sección de comparación deja de ser opcional |

Registra la **distribución** de las familias, no solo cuál aparece: una landing con 70%
problem-aware y 30% solution-aware se ordena distinto que la inversa. Esa distribución es la
evidencia que cita el Paso 5 al clasificar.

---

## Tráfico mixto

Si la landing recibirá tráfico de varias fuentes, **reconstruye la demanda por fuente** y no
promedies. Una sección puede ser Esencial para una fuente y Excluida para otra.

Cómo resolver:

1. Determina la **fuente dominante** por volumen esperado o real.
2. Clasifica según la dominante.
3. **Registra el conflicto** en el blueprint, nombrando qué fuente pierde y qué se hace con ella.
4. Si dos fuentes pesan parecido y piden arquitecturas incompatibles, la recomendación correcta
   suele ser **landings separadas**, no una que sirva mal a ambas. Dilo en vez de promediar.

---

## Tráfico sin query: cómo se construye el mapa

Cuando nadie buscó nada, el mapa de preguntas se construye desde tres fuentes, en este orden:

1. **La creatividad de origen** — el anuncio, el asunto del correo, el post. Define qué expectativa
   trae el visitante y qué ya le prometieron.
2. **Las objeciones de `contexto/sitio.md`** — §Objeciones y Anti-Personas, §Dinámicas de Cambio
   (push, pull, hábito, ansiedad). Es la mejor aproximación disponible a lo que duda esta audiencia.
3. **El comportamiento del segmento en GA4/Clarity**, si la página ya existe — lo más fuerte del
   grupo, porque describe a *este* tráfico y no a uno hipotético: dónde se detiene el scroll, qué
   se clickea, dónde abandona el formulario.

Declara la confianza resultante como **Media** o **Baja** según cuánto aportó el punto 3. Y deja
explícito en el blueprint que el mapa no se apoya en búsqueda: es la limitación que un lector futuro
necesita para juzgar las decisiones.
