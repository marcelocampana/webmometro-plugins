---
tipo: blueprint-landing
cliente: "{cliente}"
landing: "{nombre de la landing}"
slug: "{slug}"
url: "{URL si existe, o null}"
modalidad: "{nueva|auditoria}"
grado_libertad: "{plantilla|libre}"
arquetipo: "{compra|demo|cotizacion|lead|registro|prueba|descarga|evento|donacion|aplicacion}"
conversion_primaria: "{la única acción}"
fuente_trafico: "{organico|paid-search|pmax|meta|email|outbound|rrss|mixto}"
mercado: "{país}"
idioma: "{código}"
periodo: "{AAAA-MM}"
fecha: "{AAAA-MM-DD}"
corte_evidencia: "{AAAA-MM-DD — fecha del dato más reciente usado}"
fuentes_usadas: []
fuentes_ausentes: []
llamadas_mcp: 0
message_match: "{verificado|no verificado|no aplica}"
version_skill: "1.0.0"
estado: "{borrador|revisado|aprobado}"
---

# Blueprint: {nombre de la landing}

- **Conversión primaria:** {la acción}
- **Arquetipo:** {arquetipo} · **Entrada:** {fuente de tráfico} · **Mercado:** {país} / {idioma}
- **Modalidad:** {nueva | auditoría estructural} · **Estructura:** {plantilla fija | libre}

<!--
ORDEN DEL INFORME: primero lo accionable, el sustento metodológico plegado al final.
Quien lo lee necesita ejecutar la landing, no re-derivarla.
-->

---

## 1. Resumen ejecutivo y decisión estratégica

{3–5 líneas: qué tiene que lograr esta página, cuál es la tensión principal entre lo que el
visitante pregunta y lo que al negocio le conviene responder, y cómo se resuelve.}

| Secciones | Esenciales | Condicionales | Excluidas |
|---|---|---|---|
| {n} | {n} | {n} | {n} |

> [!warning] Decisiones clave y alertas
> - {decisión estructural principal y su razón}
> - {riesgo o supuesto abierto que más pesa}
> - {información pendiente que cambiaría el blueprint}

---

## 2. El caso

| Dimensión | Valor | Evidencia |
|---|---|---|
| Arquetipo | {arquetipo} | {fuente} |
| Conversión primaria | {acción} | {fuente} |
| Fuente y temperatura | {fuente} · {frío/templado/caliente} | {fuente + fecha} |
| Nivel de conciencia | {distribución de familias de query} | {fuente + fecha} |
| Complejidad de decisión | {baja/media/alta} | {fuente} |
| Actores involucrados | {quién decide, quién influye} | {fuente} |
| Riesgos percibidos | {los dominantes} | {fuente} |

---

## 3. Economía de la conversión

**Esta sección explica por qué el orden de la página es el que es** — y no el orden en que el
visitante pregunta.

- **Mecánica de la venta:** {precio fijo | rango | cotización tras evaluación | …}
- **Paso intermedio obligatorio:** {cuál, o "ninguno"}
- **Dónde muere el negocio hoy:** {la objeción o fricción que mata la conversión}
- **Qué tiene que creer el visitante:** {la creencia que desactiva esa objeción}
- **Con qué prueba se sostiene:** {la evidencia disponible, o el hueco declarado}

### Asimetrías detectadas

| Pregunta del visitante | Cuándo la hace | Cuándo conviene responderla | Movida | Razón |
|---|---|---|---|---|
| {pregunta} | {momento} | {momento} | {responder aquí / diferir con acuse / reformular} | {una línea} |

{Si hay diferimiento: declarar cuál es la señal mínima que igual se entrega, para que diferir no se
lea como esconder.}

---

## 4. Arquitectura de secciones

<!-- VARIANTE LIBRE — usar esta tabla cuando grado_libertad = libre -->

| # | Clasificación | Sección | Pregunta que resuelve | CTA | Confianza |
|---|---|---|---|---|---|
| 1 | Esencial | {sección} | {pregunta} | {primario/ninguno} | {Alta/Media/Baja} |

<!-- VARIANTE PLANTILLA — usar esta tabla cuando grado_libertad = plantilla
| # | Slot | Decisión | Pregunta que resuelve | CTA | Confianza |
|---|---|---|---|---|---|
| 1 | {slot del esqueleto} | {usar/suprimir/adaptar} | {pregunta} | {primario/ninguno} | {Alta/Media/Baja} |
-->

---

## 5. Solicitudes de cambio a la plantilla

*(Solo en modo plantilla. Eliminar la sección si no aplica.)*

> Estas piden desarrollo que afecta a **todas** las landings del patrón: son decisión de lote, no de
> este servicio.

| Slot propuesto | Por qué este servicio no convierte sin él | A qué otros servicios serviría | Contenido disponible |
|---|---|---|---|
| {slot} | {justificación reforzada} | {cuáles} | {sí/no + qué falta} |

---

## 6. Desarrollo de cada sección

{Un bloque por sección incluida, en el orden de la tabla. Es la parte que se ejecuta.}

### {N}. {Nombre de la sección} — {Esencial | Condicional}

- **Pregunta que resuelve:** {cuál}
- **Función de conversión:** {qué hace por la conversión, en una línea}
- **Contenido requerido:** {qué tiene que haber}
- **Prueba requerida:** {qué evidencia debe citar — o "hueco: falta X"}
- **Componente / restricción de diseño:** {del sistema de diseño, o "sin restricción documentada"}
- **Métrica / evento:** {qué se mide aquí}
- **Razón de la clasificación:** {por qué Esencial o cuál es su condición}

**Contrato de copy** *(lo consume `brand-voice-enforcement`)*
- **Mensaje que debe transmitir:** {el mensaje, no el texto}
- **Prueba obligatoria a citar:** {cuál}
- **Extensión aproximada:** {palabras o líneas}
- **CTA:** {función + texto tentativo, o "sin CTA"}

---

## 7. Secciones excluidas y por qué

| Sección | Razón de la exclusión | Qué la haría entrar |
|---|---|---|
| {sección} | {duplica / sin evidencia / distrae / no corresponde a la conciencia} | {condición} |

---

## 8. Diff estructural

*(Solo en modo auditoría. Eliminar la sección si no aplica.)*

Checklist parseable para la reconciliación de `seo-change-tracker`.

| Slug | Acción | Sección | Qué cambia | area | target_url | prioridad |
|---|---|---|---|---|---|---|
| `{slug-corto}` | {mantener/modificar/mover/eliminar} | {sección} | {qué} | {contenido/estructura/on-page} | `{url}` | {alta/media/baja} |

> Cuando implementes una de estas, ofrece registrarla en `seo-change-tracker` pasando el slug para
> que quede como `accion_origen`.

---

## 9. Handoff estructural

- **Componentes funcionales:** {lista de componentes necesarios, sin estilos}
- **Contenido a producir:** {qué falta escribir, fotografiar o conseguir}
- **Prioridad móvil:** {qué se ve primero en móvil y qué se colapsa}
- **Restricciones del sistema de diseño:** {las declaradas, o la ausencia}

**Siguientes pasos por skill:** copy → `brand-voice-enforcement` (sub-modo landing, consumiendo los
contratos de la sección 6) · imágenes → `image-prompt` · componentes → `design-system`.

---

## 10. Plan de medición y experimentos

- **KPI primario:** {métrica de la conversión primaria}
- **Microconversiones:** {las intermedias}
- **Eventos a instrumentar:** {nombre y disparador}
- **Segmentos a separar:** {por fuente, dispositivo, etc.}

| Hipótesis | Qué la validaría | Prioridad |
|---|---|---|
| {hipótesis} | {experimento o medición} | {alta/media/baja} |

---

## 11. Riesgos, supuestos y próximos pasos

### Supuestos abiertos

| Supuesto | Secciones que dependen de él | Qué lo resolvería |
|---|---|---|
| {supuesto} | {secciones, por nombre} | {dato, respuesta o medición} |

### Riesgos

- {riesgo y su consecuencia}

### Próximos pasos

1. {acción concreta}

---

<details>
<summary><strong>Sustento y evidencia</strong> — mapa de preguntas, fuentes, contradicciones y gate MCP</summary>

### Mapa de preguntas completo

```
pregunta: <la pregunta, en el lenguaje del visitante>
prioridad: <alta|media|baja>
cuando_pregunta: <momento natural>
cuando_conviene_responder: <momento según la economía de la conversión>
movida: <responder donde se pregunta|diferir con acuse|reformular>
razon_movida: <obligatoria si no es la primera>
destino: <sección propia|bloque FAQ>
evidencia: <fuente + fecha>
confianza: <Alta|Media|Baja>
```

### Tabla de evidencia

| Afirmación | Fuente | Fecha | Mercado | Segmento | Período | Confianza |
|---|---|---|---|---|---|---|
| {afirmación} | {fuente} | {fecha} | {país} | {segmento} | {ventana} | {nivel} |

### Contradicciones detectadas

| Fuente A (fecha) | Fuente B (fecha) | En qué difieren | Cómo se resolvió |
|---|---|---|---|

### Vacíos de evidencia

| Qué falta | Qué decisión afecta | Cómo conseguirlo |
|---|---|---|

### Cuadro de las cinco

| # | Pregunta | Respuesta | Estado |
|---|---|---|---|
| 1 | ¿Dónde se caen los que no cierran y qué dicen? | {respuesta} | {Respondida/Inferida/Parcial/Sin información} |
| 2 | ¿Qué preguntan siempre que incomoda responder? | {respuesta} | {estado} |
| 3 | ¿Qué tienen en común los que sí cierran? | {respuesta} | {estado} |
| 4 | ¿Qué entiende mal la gente de lo que se vende? | {respuesta} | {estado} |
| 5 | ¿Qué diferencia no se nota hasta después de contratar? | {respuesta} | {estado} |

### Registro del gate MCP

- **Consultas propuestas:** {cuáles y para qué decisión}
- **Aprobación:** {concedida | rechazada | no fue necesaria}
- **Llamadas realizadas:** {n} de un techo de 10
- **Early stopping:** {sí/no + por qué}

</details>
