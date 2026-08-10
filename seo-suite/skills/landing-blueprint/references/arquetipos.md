# Arquetipos de landing

Gobierna la clasificación del caso en el **Paso 2**. El arquetipo se determina por **la conversión
primaria**, no por el rubro: una clínica y una consultora que ambas cotizan tras evaluación
comparten arquetipo aunque no compartan nada más.

**El arquetipo nunca se pregunta.** Se infiere de la conversión primaria más la oferta y se confirma
en una línea junto al resto del acuse de contexto.

Lo que sigue son **tendencias, no reglas**. La evidencia del caso concreto siempre manda sobre la
tendencia del arquetipo: si el arquetipo dice que una sección suele ser Esencial pero los datos de
este cliente dicen lo contrario, ganan los datos.

---

## Tabla comparativa

| Arquetipo | Conversión primaria | Riesgo percibido dominante | Preguntas que suben |
|---|---|---|---|
| **Compra** | Pago completado | Perder el dinero; que no sea lo esperado | 7, 9 |
| **Demo** | Demo agendada | Perder el tiempo; recibir presión de venta | 4, 8 |
| **Cotización** | Solicitud de presupuesto | Que el precio sea inabordable; quedar comprometido | 4, 7 |
| **Lead** | Datos entregados | Spam; que no valga lo que pide a cambio | 5, 8 |
| **Registro** | Cuenta creada | Esfuerzo de configuración; abandono posterior | 4, 9 |
| **Prueba** | Trial iniciado | Cobro automático; migrar después | 7, 8 |
| **Descarga** | Recurso descargado | Que el contenido no valga el correo | 3, 5 |
| **Evento** | Inscripción | Fecha, cupo, que no aplique a su nivel | 7, 8 |
| **Donación** | Donación completada | Que la plata no llegue a destino | 5, 8 |
| **Aplicación** | Postulación enviada | Rechazo; esfuerzo de postular en vano | 2, 4 |

Numeración de preguntas según [mapa-de-preguntas.md](mapa-de-preguntas.md).

---

## Detalle por arquetipo

### Compra

Transacción directa, precio publicado. **Actores:** decisor único, salvo compras familiares o
corporativas. **Suelen ser Esenciales:** precios, logística transaccional (envío, devolución,
plazos), garantía, prueba social, checkout. **Suelen sobrar:** orientación si el tráfico es
solution-aware; comparación si no hay diferenciación documentada.

### Demo

El visitante entrega tiempo, no dinero. **Actores:** frecuentemente múltiples (usuario evalúa,
gerencia aprueba). **Suelen ser Esenciales:** cómo funciona, qué pasa después de agendar (quién
llama, cuánto dura, si es comercial o técnica), prueba social con logos reconocibles. **Suelen
sobrar:** precios detallados; urgencia.

### Cotización

No hay precio hasta que hay evaluación. **Es el arquetipo donde la asimetría del Paso 4 pesa más.**
**Suelen ser Esenciales:** cómo funciona la evaluación (duración, costo, entregable, compromiso),
diferenciador con prueba, señal mínima de precio, qué pasa después. **Suelen sobrar:** tabla de
precios; comparativa de planes.

### Lead

Se cambian datos por algo de valor. **Suelen ser Esenciales:** qué recibe exactamente, quién lo
envía, qué pasa con sus datos, formulario mínimo. **Suelen sobrar:** características extensas;
comparación. **Regla:** cada campo del formulario tiene que justificar su costo de fricción.

### Registro

Cuenta gratuita o freemium. **Suelen ser Esenciales:** qué puede hacer sin pagar, cuánto demora
partir, si pide tarjeta. **Suelen sobrar:** prueba social de enterprise si el registro es
self-service.

### Prueba

Trial con o sin tarjeta. **Suelen ser Esenciales:** qué incluye, qué pasa al terminar, si hay cobro
automático, cómo cancelar. **Suelen sobrar:** agitación del problema. **Regla:** la ansiedad
dominante es el cobro sorpresa; resolverla explícitamente sube la conversión más que cualquier
argumento de valor.

### Descarga

Contenido a cambio de contacto. **Suelen ser Esenciales:** qué contiene (índice o vistazo), quién lo
escribió, formato y extensión. **Suelen sobrar:** casi todo lo demás — es el arquetipo más corto.

### Evento

Inscripción con fecha. **Suelen ser Esenciales:** fecha, hora, formato, qué incluye, quién expone,
cupo si es real. **Urgencia y escasez son legítimas aquí** porque la restricción existe — pero solo
con el cupo o el plazo reales, nunca inventados. **Suelen sobrar:** comparación con alternativas.

### Donación

Aporte sin contraprestación material. **Suelen ser Esenciales:** a dónde va el dinero con detalle,
transparencia y rendición, impacto verificable, qué pasa después del aporte, opciones de monto.
**Suelen sobrar:** comparación; características. **Regla:** el riesgo percibido es que el aporte no
llegue; toda la arquitectura debe atacar eso.

### Aplicación

Postulación a un programa, beca, empleo o membresía con filtro. **Suelen ser Esenciales:**
requisitos y criterios explícitos, qué implica postular (tiempo, documentos), plazos, qué pasa
después y cuándo. **Suelen sobrar:** persuasión de venta. **Regla:** la anti-persona importa tanto
como la persona — decir claramente para quién *no* es ahorra postulaciones inútiles a ambos lados.

---

## Combinaciones y casos límite

**Un arquetipo por landing.** Si la página persigue dos conversiones de arquetipos distintos
(comprar *o* cotizar), eso no es un caso híbrido: es una landing sin conversión primaria definida.
Elige una y trata la otra como acción secundaria, o recomienda separar en dos páginas.

**Arquetipo secundario legítimo:** una acción de menor compromiso que **reduce riesgo** hacia la
conversión primaria — descargar la ficha técnica antes de cotizar, ver una demo grabada antes de
agendar. Es válido siempre que no compita en jerarquía visual con la primaria.

**Click-to-WhatsApp:** si el anuncio abre conversación en vez de llevar a un formulario, la
conversión primaria es *iniciar conversación*. Eso reescribe la sección de fricción (no hay
formulario) y la de "qué pasa después" (quién responde, en cuánto tiempo, en qué horario).
