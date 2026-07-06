---
tipo: mapa-cluster
cluster: "{nombre-del-cluster}"
semilla: "{keyword semilla de origen}"
fecha_creacion: "{AAAA-MM-DD}"
estado: "{borrador|en-produccion|completo|necesita-revision}"
pilar: "[[{nombre-del-pilar}]]"
keywords_analizadas: null
clusters_formados: null
volumen_total_mensual: null
scorecard:
  cobertura: null
  link_health: null
  content_quality: null
  gates_ok: null
---

# Mapa de clúster: {nombre del clúster}

- **Semilla:** {keyword semilla}
- **Fecha:** {AAAA-MM-DD}
- **Estado:** {estado}

<!--
ORDEN DEL INFORME (ejecutivo, no por pasos del proceso):
lo primero que se lee es el clúster y CÓMO se desarrolla cada tema; el sustento
metodológico va plegado al final. Ver "Forma del informe" en SKILL.md.
-->

---

## Resumen ejecutivo

{2–4 líneas: tracción actual del pilar (posición, conversión), cuántas piezas faltan, apuesta estratégica principal y alerta clave — el "por qué" que da paso a los números de abajo.}

| Pilar | URL | Intención | Posición | Vol./mes | KD |
|---|---|---|---|---|---|
| [[{nombre-del-pilar}]] | `{url}` | {tipo} | {posición actual / "GAP"} | {vol} | {kd} |

| Spokes | GAP | Parcial | Cubierto | Vol. clúster | KW analizadas |
|---|---|---|---|---|---|
| {n} | {n} | {n} | {n} | ~{n}/mes | {n} |

> [!warning] Decisiones clave y alertas
> - {acción / alerta 1}
> - {acción / alerta 2 — p.ej. "spoke X a vigilar por canibalización ~N%"}
> - {acción / alerta 3 si aplica — gates que fallan o están en vigilancia; tablas completas en el Sustento}

---

## El clúster

| Rol | Página | Keyword objetivo | Vol./mes | KD | Intención | Estado |
|---|---|---|---|---|---|---|
| **Pilar** | [[{nombre-del-pilar}]] | {keyword} | {vol} | {kd} | {tipo} | {posición / GAP} |
| Spoke | [[{nombre-spoke-1}]] | {keyword} | {vol} | {kd} | {tipo} | GAP |
| Spoke | [[{nombre-spoke-2}]] | {keyword} | {vol} | {kd} | {tipo} | Parcial |
| Spoke | [[{nombre-spoke-3}]] | {keyword} | {vol} | {kd} | {tipo} | Cubierto |

<!-- Repetir filas Spoke para cada pieza (3–7 total). Notas en columna Estado: "GAP ⚠️ canibalización", "↳ sección del pilar", etc. -->

---

## Desarrollo de cada tema

> El corazón del informe: qué es cada pieza y cómo se desarrolla. H1 + H2 derivados de la voz real
> del buscador y redactados en la voz de marca. Cada bloque es la base de la nota que se materializa
> en el Modo 2.

### Pilar — [[{nombre-del-pilar}]]
- **Keyword objetivo:** {keyword} · **Intención:** {tipo} · **Estado:** {parcial/optimizar | gap/crear}
- **H1:** {título on-brand del pilar}
- **H2:**
  1. {H2 — mecanismo/qué es} → enlaza a [[{spoke relacionado}]]
  2. {H2 — qué tratamos/beneficios} → enlaza a [[{spoke}]]
  3. {H2 — resultados / prueba}
  4. {H2 — recuperación / proceso} → enlaza a [[{spoke}]]
  5. {H2 — precio/plan o CTA según tipo}
- **Ángulo de marca:** {1–2 líneas: cómo suena, qué marco usa, qué evita}
- **FAQ (de preguntas PAA sin volumen propio):** {pregunta 1 · pregunta 2 · pregunta 3 …}
- **Ajustes vs. la página actual (si ya existe):** {diff concreto — secciones a añadir, enlaces, extensión}

### Spoke 1 — [[{nombre-spoke-1}]]
- **Keyword objetivo:** {keyword} · **Intención:** {tipo} · **Estado:** {gap/parcial/cubierto}
- **H1:** {título on-brand del spoke}
- **H2:** {H2-1} · {H2-2} · {H2-3} · {H2-4 opcional}
- **Ángulo de marca:** {1 línea}
- **Enlaces salientes:** → [[{pilar}]] · → [[{spoke hermano}]]

<!-- Repetir el bloque "Spoke N" para cada spoke (3–7 en total). -->

---

## Roadmap de producción

Orden por score de oportunidad (volumen 40% + KD inverso 30% + intención 30%):

1. **[[{pieza-1}]]** — score {n} · {gap/parcial} · intención {tipo} · {por qué primero}
2. **[[{pieza-2}]]** — score {n} · {estado} · intención {tipo}
3. **[[{pieza-3}]]** — score {n} · {estado} · intención {tipo}

---

## Mapa de enlazado interno

| Desde | Hacia | Anchor sugerido |
|---|---|---|
| [[{pilar}]] | [[{spoke-1}]] | "{texto de anchor}" |
| [[{spoke-1}]] | [[{pilar}]] | "{texto de anchor}" |
| [[{spoke-1}]] | [[{spoke-2}]] | "{texto de anchor}" |

---

## Sustento y análisis

> Evidencia y metodología, plegadas. Están para auditar/defender cada decisión, no para leerse de
> corrido. Abrir solo lo que haga falta.

<details>
<summary><strong>Expansión de semilla + keywords</strong> — volúmenes, KD, fuentes</summary>

- Fuentes que respondieron: {…} · Fuentes que fallaron (campo `null`): {…}
- Nota de fiabilidad de volumen (Chile vs global, GSC vs estimado): {…}

| Keyword | Vol./mes | KD/competencia | Señal GSC | Intención |
|---|---|---|---|---|
| {keyword} | {n} | {n} | {pos · clics} | {tipo} |

</details>

<details>
<summary><strong>Inventario del sitio + auditoría de intención de URLs propias</strong></summary>

| URL | Tipo de página actual | Intención satisfecha | Intención SERP | Alineado |
|---|---|---|---|---|
| {url} | transaccional / comercial / informacional / mixta | {qué resuelve hoy} | {tipo} | alineado / desalineado |

</details>

<details>
<summary><strong>Clustering por solape de SERP + canibalización</strong> — overlaps medidos</summary>

| Par de keywords | URLs/dominios compartidos top-10 | Overlap | Acción |
|---|---|---|---|
| {kw A} ↔ {kw B} | {dominios} | ~{n}% | {mismo clúster / interlinkar / fundir / vigilar} |

</details>

<details>
<summary><strong>Cobertura (coverage scoring)</strong></summary>

| Subtema | Página/nota existente | Calidad (1–5) | Estado |
|---|---|---|---|
| {subtema} | [[{nota}]] o — | {n} | cubierto / parcial / gap |

**Cobertura actual:** {n}% ({n} de {n} subtemas cubiertos o parciales)

</details>

<details>
<summary><strong>Scorecard de salud + gates de tolerancia-cero</strong></summary>

```
Cobertura    = {n}%
Link Health  = {n}%
Content Quality = {n}%
```

| Gate | Estado | Detalle |
|---|---|---|
| Canibalización | — | {ningún par >40% overlap / revisar: par X–Y} |
| Huérfanos | — | {0 huérfanos / revisar: spoke Z sin enlace desde pilar} |
| Cobertura | — | {cobertura}% ({≥70% ok / por debajo del umbral}) |
| Anchor diversity | — | {ok / anchor "{texto}" en {n}% de los enlaces} |
| Coherencia de intención | — | {ok / desajuste: "{pieza}" propuesta como {tipo} pero SERP es {tipo_serp}} |

</details>

<details>
<summary><strong>Notas, keywords descartadas, decisiones de diseño y fuentes</strong></summary>

- Keywords descartadas (clústeres aparte): {…}
- Decisiones de diseño / pendientes de confirmación: {…}
- Estado de fuentes MCP: {…}

</details>
