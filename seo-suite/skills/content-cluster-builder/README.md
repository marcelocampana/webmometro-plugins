# Content Cluster Builder

Skill para construir clústeres de contenido (pilar + spokes) con autoridad temática. Investiga
keywords, analiza la competencia en Google y genera el plan más las notas de Obsidian listas para
redactar.

---

## Cómo invocarlo

Di cualquiera de estas frases y el skill se activa automáticamente:

- "quiero crear un clúster de contenido sobre [tema]"
- "qué artículos debería escribir alrededor de [tema]"
- "construye autoridad temática sobre [tema]"
- "necesito una arquitectura pilar y spokes para [tema]"
- "organiza el contenido sobre [tema] en un clúster SEO"

---

## Qué necesitas tener listo

**Solo el tema semilla.** Una palabra o frase es suficiente para arrancar.

El skill lee el contexto del negocio (dominio, ubicación, keywords principales) desde
`seo-tracking/config.md` si existe. Si no existe o es un proyecto nuevo, te preguntará esos datos
una sola vez y los guardará para las próximas sesiones.

No necesitas traer keyword research previo ni listados — el skill los construye solo.

---

## Qué hace el skill (flujo en dos fases)

### Fase 1 — Investiga y planifica

El skill investiga con estas fuentes:

1. **DataForSEO Labs** — expande la semilla en 50–150 keywords con volumen, dificultad y CPC
2. **Google Search Console** — suma las keywords reales por las que tu sitio ya aparece en Google
3. **Inventario del sitio** — parsea el sitemap y revisa qué páginas ya existen (aunque no tengan
   tráfico) antes de declarar algo como faltante, para no proponerte temas duplicados
4. **SERP en vivo geolocalizada** — agrupa keywords por solapamiento de resultados (no por texto
   similar) y detecta qué tipo de contenido premia Google para cada término (su intención)
5. **Voz del buscador** — analiza *cómo* pregunta la gente (queries reales, People Also Ask,
   sugerencias y, opcionalmente, foros) para que los H2 y las FAQ respondan el lenguaje real
6. **Tu vault de Obsidian** — detecta qué contenido ya tienes y qué está faltando
7. **Guía de brand voice** — si existe en el proyecto, la usa para que los títulos suenen al negocio

**Hay un punto de decisión contigo temprano:** apenas detecta las páginas que ya cubren el tema, el
skill te muestra los candidatos a página pilar y te pide confirmar cuál es (o, si no existe, qué
tipo de contenido quieres). Si la página ya existe, la revisa y te confirma su tipo (transaccional,
informativa, etc.) — nunca convierte por su cuenta una página que ya vende en una guía informativa.

Con eso arma la arquitectura: un pilar + 3–7 spokes, ordenados por oportunidad, con el mapa de
enlazado interno, una lista de ajustes para la página pilar existente y un scorecard de salud.

**El skill te presenta el plan completo para que lo revises antes de crear nada.** Puedes ajustar,
descartar spokes o cambiar prioridades en ese punto.

### Fase 2 — Materializa en Obsidian

Solo después de que apruebes el plan, crea los archivos:

- Una **nota pilar** con frontmatter, estructura H1/H2 y enlaces `[[wikilink]]` a los spokes
- Una **nota spoke** por cada artículo del clúster, con enlace al pilar y a sus hermanos
- Un **mapa maestro** con el resumen, arquitectura, roadmap y scorecard del clúster

---

## Después de crear el clúster

### Revisar la salud del clúster con el script

Una vez que las notas están en el vault, puedes verificar la salud del clúster en cualquier momento:

```bash
python3 .claude/skills/content-cluster-builder/scripts/salud_cluster.py \
  --cluster "nombre-del-cluster" \
  --vault "/ruta/al/vault"
```

O pasando las notas directamente:

```bash
python3 .claude/skills/content-cluster-builder/scripts/salud_cluster.py \
  nota-pilar.md spoke-1.md spoke-2.md
```

El script calcula:
- **Cobertura** — qué porcentaje de subtemas tiene contenido
- **Link Health** — qué porcentaje de spokes tiene enlazado bidireccional con el pilar
- **Gates de tolerancia-cero** — canibalización, huérfanos, anchor diversity, coherencia de intención

### Medir el impacto en SEO

Cuando publiques los artículos del clúster, el skill te ofrecerá registrarlos en `seo-change-tracker`
para medir el impacto a 14 y 28 días. Puedes aceptar o saltar eso.

---

## Qué NO necesitas hacer

- Traer keyword research propio — el skill lo hace
- Elegir qué herramientas usar — lee las fuentes disponibles y avisa si alguna falla
- Crear las notas a mano — las genera desde las plantillas con los wikilinks ya conectados
- Repetir el contexto del negocio en cada sesión — lo lee de `seo-tracking/config.md`
