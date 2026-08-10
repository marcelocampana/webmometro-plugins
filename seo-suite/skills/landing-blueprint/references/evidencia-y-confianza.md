# Evidencia y confianza

Define cómo se sostiene cada afirmación del blueprint. Aplica a todo el flujo, no a un paso
concreto.

**El principio:** un blueprint sin trazabilidad es una opinión con formato de informe. Quien lo lea
dentro de seis meses —o quien tenga que defender una decisión ante el cliente— necesita saber de
dónde salió cada cosa y cuánto pesa.

## Contenido

- [Jerarquía de fuentes](#jerarquía-de-fuentes)
- [Registro obligatorio por afirmación](#registro-obligatorio-por-afirmación)
- [Niveles de confianza](#niveles-de-confianza)
- [Qué nunca se inventa](#qué-nunca-se-inventa)
- [Contradicciones entre fuentes](#contradicciones-entre-fuentes)
- [Cómo se marcan las inferencias](#cómo-se-marcan-las-inferencias)
- [Supuestos que quedan abiertos](#supuestos-que-quedan-abiertos)

---

## Jerarquía de fuentes

De mayor a menor peso:

| # | Fuente | Ejemplos |
|---|---|---|
| 1 | **Datos propios y voz textual del cliente** | GA4, GSC, Clarity del propio sitio; consultas reales de WhatsApp o formulario; lo que el dueño del negocio afirma de su venta |
| 2 | **Fuentes confirmadas por el cliente** | `contexto/sitio.md` revisado, `antecedentes/`, briefs, exports que el cliente entrega |
| 3 | **Observación de mercado y competencia** | SERP, PAA, volumen, páginas de competidores |
| 4 | **Inferencia** | Deducciones del skill a partir de lo anterior |

**Una fuente de nivel superior gana sobre una inferior cuando se contradicen** — pero la
contradicción se expone, no se resuelve en silencio (ver más abajo).

Caso especial: el **PAA y el volumen** son nivel 3, y con tráfico que nunca hizo una búsqueda bajan
a hipótesis de tema sin poder de promoción. Ver
[entrada-y-demanda.md](entrada-y-demanda.md).

---

## Registro obligatorio por afirmación

Toda afirmación que sostenga una decisión de sección lleva:

```
afirmacion: <qué se afirma>
fuente: <archivo, herramienta o persona>
fecha: <AAAA-MM o AAAA-MM-DD>
mercado: <país / región>          ← cuando aplique
segmento: <audiencia o canal>     ← cuando aplique
periodo_analizado: <ventana de tiempo de los datos>
confianza: <Alta | Media | Baja>
```

Esto vive en la tabla de evidencia del bloque plegado *Sustento y evidencia*. La tabla visible de
arquitectura solo muestra la confianza; el detalle queda para auditar.

**Mercado e idioma son obligatorios en cualquier consulta externa.** Nunca aceptes un default de
Estados Unidos en silencio: derívalos del mercado declarado en `contexto/sitio.md` o
`contexto/configuracion.md`.

---

## Niveles de confianza

| Nivel | Cuándo | Qué habilita |
|---|---|---|
| **Alta** | Datos propios del cliente, vigentes (≤30 días para métricas), o afirmación confirmada por él | Puede sostener una sección **Esencial** |
| **Media** | Fuentes confirmadas pero dadas (>30 días), observación de mercado, hipótesis de tema | Sostiene **Condicional**; para Esencial necesita respaldo adicional |
| **Baja** | Inferencia sin respaldo, gate de costo rechazado, modo sin workspace | **Nunca** sostiene una Esencial por sí sola |

**Regla dura:** una sección cuya única evidencia es de confianza Baja se clasifica **Condicional con
su condición escrita**, nunca Esencial por defecto. La condición dice qué haría falta para
promoverla.

---

## Qué nunca se inventa

- **Volúmenes de búsqueda, CTR, tasas de conversión o benchmarks.** Si no hay dato, se dice que no
  hay dato.
- **Testimonios, casos, cifras de resultados, logos de clientes.** Si el contrato de copy de una
  sección requiere prueba y la prueba no existe, se marca el hueco y se propone conseguirla — no se
  redacta un placeholder que parezca evidencia.
- **Componentes del sistema de diseño.** Solo se nombran los que el sistema declara. Si no hay
  sistema documentado, el handoff va sin restricciones de componente y se dice.
- **Benchmarks de industria** presentados como hechos actuales. Si se citan estudios, van con su
  fecha y como heurística datada.
- **Precios, plazos o promesas** que el negocio no haya confirmado.

---

## Contradicciones entre fuentes

Cuando dos fuentes se contradicen —típicamente `contexto/sitio.md` contra los datos frescos, o un
antecedente contra el snapshot actual—:

1. **Exponla con las fechas de ambas.** No elijas bando en silencio.
2. **Pregunta.** Una de las dos está desactualizada, o hay un tercer factor que ninguna captura — y
   ese tercer factor suele ser el hallazgo valioso (ver los mecanismos de descubrimiento en
   [economia-de-conversion.md](economia-de-conversion.md)).
3. **Regístrala** en la sección de contradicciones del blueprint, aunque se resuelva. Deja rastro de
   que se detectó y cómo se resolvió.

Nunca trates un documento más viejo como verdad por encima de datos frescos sin decirlo, ni al
revés: un dato fresco puede reflejar un cambio reciente que el documento aún no recoge.

---

## Cómo se marcan las inferencias

Reusa la convención ya establecida por `site-context`: **`[inferido — requiere revisión]`**.

Aplica a:
- Cualquier campo del cuadro de las cinco con estado *Inferida*.
- Secciones de `contexto/sitio.md` que el skill proponga completar.
- Interpretaciones de material aportado por el usuario.

**En una inferencia se confirma la interpretación, no el dato.** La diferencia importa: preguntar
"¿cuánta gente abandona el formulario?" cuando el dato ya está en el snapshot es hacerle trabajo al
usuario; preguntar "interpreto que abandonan porque pides el RUT antes de mostrar el precio, ¿lo lees
igual?" es pedirle lo único que él tiene y tú no.

---

## Supuestos que quedan abiertos

Si tras agotar los mecanismos queda una duda **que cambiaría la arquitectura**, no la resuelvas en
silencio:

1. Escríbela como **supuesto explícito** en la sección de riesgos y supuestos.
2. **Marca qué secciones dependen de él** — con nombre, no genéricamente.
3. Indica **qué la resolvería**: un dato, una respuesta del cliente, una medición.

Así, si el supuesto resulta falso, se ve exactamente qué decisiones hay que rehacer. Un desafío no
detectado deja entonces un rastro recuperable, en vez de aparecer meses después como una landing que
no convierte sin explicación.
