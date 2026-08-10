# Sistema de decisión de secciones

Gobierna el **Paso 5**. Define el catálogo de secciones, las reglas de clasificación, cómo la
demanda del Paso 3 promueve o descarta secciones, y los antipatrones.

**Regla base: ninguna sección entra por defecto.** Ni problema, ni comparación, ni precios, ni
urgencia, ni FAQ, ni testimonios. Cada sección incluida **y cada sección excluida** lleva su
justificación y su confianza.

## Contenido

- [Catálogo de secciones](#catálogo-de-secciones)
- [Las tres clasificaciones](#las-tres-clasificaciones)
- [Reglas que consumen la demanda](#reglas-que-consumen-la-demanda)
- [Modo plantilla: decisión por slot](#modo-plantilla-decisión-por-slot)
- [Antipatrones](#antipatrones)

---

## Catálogo de secciones

No es una lista de secciones obligatorias ni un orden sugerido: es el vocabulario con el que se
nombran las decisiones.

| Sección | Pregunta que suele resolver | Función de conversión |
|---|---|---|
| **Hero** | 1, 3 | Confirmar que está en el lugar correcto y hacer legible la oferta |
| **Prueba inmediata** | 5 | Bajar la guardia antes de pedir atención |
| **Barra de logos / respaldo** | 5 | Transferencia de confianza por asociación |
| **Orientación / triaje** | 2, previa | Ayudar a identificar qué necesita cuando no lo sabe |
| **Problema / agitación** | 2 | Reconocer la situación del visitante en su lenguaje |
| **Cómo funciona** | 4 | Hacer concreto el mecanismo y el entregable |
| **Resultados / beneficios** | 3 | Traducir características en outcome |
| **Características** | 4 | Detalle para quien ya compró el concepto |
| **Casos de uso** | 2, 4 | Reconocimiento: "este es mi caso" |
| **Prueba social** | 5 | Testimonios, casos, reseñas — atribuidos y verificables |
| **Datos cuantificados** | 5 | Cifras con fuente y fecha |
| **Comparación vs alternativas** | 6 | Diferenciar frente a competencia o frente a no hacer nada |
| **Precios** | 7 | El número, el rango o la mecánica |
| **Calculadora / ROI** | 7 | Hacer tangible el retorno o el costo real |
| **Objeciones / FAQ** | 7, residuales | Cerrar dudas que quedaron |
| **Garantía / reversión de riesgo** | 7 | Trasladar el riesgo del visitante al negocio |
| **Quién está detrás / credenciales** | 5 | Confianza en las personas, no en la marca |
| **Compliance / certificaciones** | 5 | Requisito en sectores regulados |
| **Logística transaccional** | 7, 8 | Envío, devolución, pago, plazos |
| **Urgencia / escasez** | 9 | Motivar la acción ahora — solo si es real |
| **Qué pasa después de convertir** | 8 | Eliminar la ansiedad del "y ahora qué" |
| **Formulario / checkout** | 9 | La conversión misma |
| **CTA final** | 9 | Recoger al que llegó abajo convencido |
| **Footer mínimo** | — | Legal y contacto, sin dispersar |

---

## Las tres clasificaciones

### Esencial

Entra porque resuelve **una pregunta decisiva**, **una exigencia transaccional** o **un requisito de
confianza o compliance**. Si se quita, el visitante no puede decidir o no puede completar la acción.

Justificación obligatoria: qué pregunta resuelve y con qué evidencia se sabe que esa pregunta pesa.

### Condicional

Entra **solo cuando el caso lo justifica**. La condición se escribe explícita, de modo que quien lea
el blueprint sepa qué tendría que cambiar para que entre o salga.

> Ejemplo: "Comparación vs alternativas — **Condicional**: entra si se documenta la diferenciación
> con prueba verificable. Hoy `sitio.md` la declara pero sin respaldo."

Una sección cuya evidencia quedó en confianza Baja por el gate de costo rechazado se clasifica
**Condicional con su condición escrita**, nunca Esencial por defecto.

### Excluida

No entra porque **duplica argumentos** de otra sección, **carece de evidencia** que la sostenga,
**distrae** de la conversión primaria, o **no corresponde al nivel de conciencia** del tráfico.

Las exclusiones también se justifican y aparecen en el blueprint. Una sección ausente sin explicación
se lee como olvido; una excluida con razón se lee como decisión.

---

## Reglas que consumen la demanda

El puente entre lo que la gente busca (Paso 3) y la clasificación de cada sección. Es donde el skill
gana su trazabilidad.

### Orientación / triaje

| Distribución de entradas | Clasificación | Razón |
|---|---|---|
| Dominantemente **problem-aware** | **Esencial** | El visitante no sabe qué servicio necesita; sin orientación rebota o elige mal |
| Dominantemente **solution-aware** | **Excluida** | Retrasa una decisión ya tomada |

Cita la distribución concreta y su fecha como justificación.

### Objeción con peso en las entradas

Una familia de query que expresa objeción (precio, duración, dolor, requisitos, riesgo) y supera el
umbral de participación hace **Esencial que la landing la resuelva** — citando el porcentaje y su
fecha.

**Ojo: *resolverla* no es *responderla literalmente ni ponerla arriba*.** La forma y la posición las
decide el Paso 4 según la economía de la conversión. Puede ser una sección de respuesta directa, o
una **secuencia** (diferenciador con prueba → mecanismo de evaluación → señal del dato) cuando
responder de frente destruye el caso.

> Esta es la corrección clave del sistema. Una regla que promoviera "sección de precio arriba" por
> peso de query sabotearía a un negocio que cotiza tras evaluación: produciría exactamente el
> filtrado por precio que ese negocio intenta evitar.

### Doble destino

Pregunta que **decide** la conversión → sección propia. Sub-pregunta que remueve una duda residual →
bloque FAQ. Ver [mapa-de-preguntas.md](mapa-de-preguntas.md).

### La objeción central nunca vive en un acordeón

Si lo que mata el negocio quedó enterrado en la FAQ al pie, la landing no lo resolvió. Es falla de
arquitectura, no detalle de contenido.

### Vocabulario

El lenguaje textual del buscador manda sobre el vocabulario interno en el contrato de copy del hero
y de la sección que resuelve cada objeción. Si la gente dice "se me cae el pelo", la página no abre
con "alopecia androgenética".

### Sin poder de promoción

Con tráfico que nunca hizo una búsqueda, el PAA **no dispara ninguna de estas reglas**. Ver la escala
de peso en [entrada-y-demanda.md](entrada-y-demanda.md).

---

## Modo plantilla: decisión por slot

Cuando existe un esqueleto (`contexto/plantilla-landing.md` o aprendido de landings hermanas), la
decisión cambia de forma:

| Decisión | Cuándo | Qué se registra |
|---|---|---|
| **Usar** | El slot resuelve una pregunta que este servicio tiene | Qué pregunta y con qué contenido |
| **Suprimir** | El slot no aplica a este servicio, o su contenido no existe | Por qué no aplica |
| **Adaptar** | El slot aplica pero con contenido o énfasis distinto | Qué cambia respecto del uso habitual |

**Lo que el esqueleto no contiene va aparte**, como *solicitud de cambio a la plantilla*: implica
desarrollo que afecta a todas las landings del patrón, así que la barra de justificación es más alta
y es una decisión de lote, no de este servicio. **Nunca inventes un slot dentro de la tabla normal
como si fuera gratis.**

Criterio para elevar una solicitud de cambio:

- El servicio **no puede convertir** sin ese slot (no basta con que "mejoraría").
- Hay al menos **otro servicio del mismo patrón** que se beneficiaría, o se argumenta por qué este
  es una excepción legítima.
- Existe la evidencia y el contenido para llenarlo — no se pide un slot vacío.

---

## Antipatrones

| Antipatrón | Síntoma | Qué hacer |
|---|---|---|
| **Sección de problema ante tráfico caliente** | Se explica el dolor a quien ya buscó la solución por nombre | Excluir; ir directo al mecanismo y la prueba |
| **Comparativa sin diferenciación documentada** | Tabla comparativa donde la propia columna gana en todo | Excluir hasta tener prueba; o reformular como criterios de elección |
| **Precios cuando la conversión es cotización** | Un número inventado o un "desde" que nadie paga | Aplicar la mecánica real y la señal mínima |
| **Urgencia inventada** | Contador o "últimos cupos" sin escasez real | Excluir. Es la vía más rápida a perder confianza |
| **FAQ como vertedero** | Todo lo que no cupo termina en el acordeón | Reclasificar: lo decisivo sube a sección |
| **Testimonios genéricos sin atribución** | "Excelente servicio — María G." | Excluir hasta tener testimonios atribuidos y específicos |
| **PAA como evidencia del visitante sin búsqueda** | Preguntas de PAA sustentando secciones en una landing de PMax | Admitir solo como hipótesis de tema, sin poder de promoción |
| **Múltiples conversiones primarias** | Tres CTAs que compiten con igual jerarquía | Una sola primaria; el resto reduce riesgo o apoya |
| **Sección sin prueba disponible** | Se propone prueba social donde no hay casos | Marcar el hueco; no redactar sobre evidencia inexistente |
