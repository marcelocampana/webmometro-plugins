# Plantilla del reporte ejecutivo

El reporte lo genera `scripts/generar_reporte.py` (no lo escribas a mano salvo que el script no esté
disponible). Esta referencia documenta la estructura para que puedas revisar o ajustar el output del
script, o redactar el reporte manualmente si es necesario.

El criterio rector: alguien que no vio ninguno de los cambios debe poder leer el reporte en menos de
2 minutos y entender **qué se hizo, qué funcionó y qué se sigue midiendo** — no es un dump de datos,
es una herramienta de decisión.

```markdown
# Reporte SEO — {cliente} — {fecha_desde} a {fecha_hasta}

**Generado:** {fecha de generación}
**Cambios en el período:** {n_total} ({n_concluidos} concluidos, {n_midiendo} en medición)

## Resumen ejecutivo

- {n_positivos} de {n_concluidos} cambios concluidos dieron resultado positivo.
- Estimado de impacto combinado: {suma de deltas relevantes, p.ej. "+120 clics/mes, +6 leads/mes"}.
- {Una frase sobre el patrón más notable: qué tipo de cambio está rindiendo mejor, o qué área
  necesita atención}.

## Qué funcionó

| Estado | Cambio | Área | Implementado | Resultado | Delta clave |
|---|---|---|---|---|---|
| ✅ | {descripcion} | {area} | {fecha} | Positivo | {métrica}: {baseline} → {último checkpoint} ({+/-X%}) |
| ➖ | {descripcion} | {area} | {fecha} | Neutral | ... |
| ❌ | {descripcion} | {area} | {fecha} | Negativo | ... |

Ordenada por impacto absoluto (mayor delta primero), no por fecha.

## En medición

| Cambio | Área | Implementado | Próximo checkpoint | Hipótesis |
|---|---|---|---|---|
| {descripcion} | {area} | {fecha} | {fecha checkpoint pendiente} | {hipotesis} |

## Por área

| Área | Cambios | Positivos | Negativos | En medición |
|---|---|---|---|---|
| on-page | n | n | n | n |
| tecnico | n | n | n | n |
| ... | | | | |

## Notas metodológicas

- Los deltas comparan el baseline (al momento del cambio) contra el checkpoint más reciente
  disponible, no contra el período anterior al cambio — esto aísla el efecto del cambio específico.
- "Inconcluso" significa que los datos disponibles no permiten un veredicto claro (señales mixtas,
  volumen insuficiente, o un factor externo conocido como estacionalidad o un cambio de algoritmo).
```

## Convenciones de los íconos de estado

| Ícono | Significado |
|---|---|
| ✅ | `resultado: positivo` |
| ➖ | `resultado: neutral` |
| ❌ | `resultado: negativo` |
| ⏳ | `estado: midiendo` (sin veredicto aún, no aparece en "Qué funcionó") |
| ❓ | `resultado: inconcluso` |

## Cálculo de "delta clave"

Para cada cambio, el script elige automáticamente la métrica más relevante según el `area`:
- `on-page` → CTR de GSC (es lo que un cambio de copy más directamente mueve)
- `tecnico` → posición/indexación o Core Web Vitals, lo que esté presente
- `contenido` → clics de GSC o sesiones de GA4
- `backlinks` → dominios de referencia
- `local` → rating o cantidad de reseñas

Si el usuario pide un reporte centrado en otra métrica (p.ej. "quiero ver todo en términos de
leads"), recalcula manualmente usando `ga4.conversions` como columna principal en vez de la default
del script.
