# El mapa de preguntas del visitante

Gobierna el **Paso 4**. Define las preguntas que un visitante debe resolver para convertir, cómo se
reordenan según el caso, y qué hacer cuando el orden del visitante choca con el del negocio.

**No es una secuencia rígida.** Es un inventario de lo que hay que resolver; el orden lo determinan
el arquetipo, el nivel de conciencia, la temperatura del tráfico y la economía de la conversión. Una
landing para tráfico de marca puede resolver tres de estas preguntas en el hero y saltarse dos.

## Contenido

- [Las nueve preguntas](#las-nueve-preguntas)
- [Cómo se reordena el mapa](#cómo-se-reordena-el-mapa)
- [Los dos atributos de cada pregunta](#los-dos-atributos-de-cada-pregunta)
- [Destino: sección propia o bloque FAQ](#destino-sección-propia-o-bloque-faq)
- [Formato de registro](#formato-de-registro)

---

## Las nueve preguntas

| # | Pregunta | Qué la responde | Evidencia que la respalda |
|---|---|---|---|
| 1 | **¿Estoy en el lugar correcto?** | Coincidencia entre lo que buscaba/le prometieron y lo primero que ve | Queries de entrada, copy del anuncio, canal |
| 2 | **¿Esto es para alguien como yo?** | Señales de audiencia: contexto, casos, lenguaje, ejemplos reconocibles | Audiencia de `sitio.md`, familias de query, segmento del anuncio |
| 3 | **¿Qué resultado ofrece?** | El outcome concreto, no la lista de características | §Diferenciación y §Pruebas de `sitio.md` |
| 4 | **¿Cómo funciona y qué recibo exactamente?** | El mecanismo y el entregable; qué pasa paso a paso | Mecánica de venta (Paso 2), material del cliente |
| 5 | **¿Por qué debería creerlo?** | Prueba: datos, casos, credenciales, respaldo verificable | §Pruebas y Evidencia; nunca inventada |
| 6 | **¿Por qué esto y no la alternativa — o no hacer nada?** | Diferenciación real frente a competencia y frente a la inercia | §Panorama Competitivo, §Dinámicas de Cambio |
| 7 | **¿Qué esfuerzo, costo o riesgo implica?** | Precio o su mecánica, tiempo, compromiso, qué puede salir mal | Economía de la conversión (Paso 2) |
| 8 | **¿Qué pasa después de convertir?** | El siguiente paso concreto: quién contacta, cuándo, qué sigue | Mecánica de venta |
| 9 | **¿Puedo avanzar ahora sin fricción?** | Formulario, CTA, requisitos, alternativas de contacto | Snapshot (auditoría), diseño del formulario |

**La 6 y la 7 son las que más se subestiman.** "No hacer nada" es el competidor más frecuente, y el
costo percibido rara vez es solo el precio: incluye tiempo, riesgo de equivocarse y esfuerzo de
cambio.

**La 8 casi siempre falta.** Un visitante que no sabe qué va a pasar después de dar sus datos asume
lo peor: una llamada de venta insistente. Responderla baja la fricción del formulario sin tocar el
formulario.

---

## Cómo se reordena el mapa

### Por nivel de conciencia

| Conciencia | Preguntas que suben | Preguntas que bajan o se colapsan |
|---|---|---|
| **problem-aware** | 2, 3 y una previa de orientación ("¿cuál de estos necesito?") | 6 pierde sentido: aún no compara proveedores |
| **solution-aware** | 5, 6, 7 — está eligiendo entre opciones | 3 se resuelve en una línea; la orientación estorba |
| **brand-aware** | 9 y 7 — vino a avanzar | 1, 2 y 3 se colapsan en el hero |

### Por temperatura del tráfico

- **Frío** (display, outbound, prospección): la 1 y la 2 son críticas y caras de responder. Sin
  ellas el resto no se lee.
- **Templado** (orgánico informacional, RRSS): la 3 y la 5 cargan el peso.
- **Caliente** (marca, remarketing, referido): la 9 manda; el resto se resume.

### Por arquetipo

Ver [arquetipos.md](arquetipos.md) para qué preguntas suben en cada uno. Como referencia rápida: en
**donación** la 5 y la 8 dominan (a dónde va mi plata); en **compra** la 7 y la 9; en **cotización**
la 4 y la 7; en **evento** la 7 y la 8 (fecha, cupo, qué incluye).

---

## Los dos atributos de cada pregunta

Cada pregunta del mapa lleva **dos atributos, no uno**:

| Atributo | De dónde sale | Qué significa |
|---|---|---|
| **Cuándo la pregunta el visitante** | Paso 3 (demanda) | El orden natural en que surge la duda |
| **Cuándo conviene responderla** | Paso 2 (economía de la conversión) | El orden en que el negocio puede responderla sin perder la venta |

Cuando coinciden, la página se ordena sola. Cuando divergen, aplica una de las tres movidas
—responder donde se pregunta, diferir con acuse, reformular— según
[economia-de-conversion.md](economia-de-conversion.md). **Ignorar la pregunta nunca es una opción.**

La movida elegida y su razón se registran en el blueprint. Es lo que explica *por qué el orden de la
página es ese* y no el orden en que el visitante pregunta.

---

## Destino: sección propia o bloque FAQ

Traducción del "doble destino" de
[../../content-cluster-builder/references/voz-del-buscador.md](../../content-cluster-builder/references/voz-del-buscador.md):

| Destino | Criterio | Ejemplo |
|---|---|---|
| **Sección propia** | La pregunta **decide** la conversión: si no se resuelve, no convierte | "¿Por qué cuesta más que la alternativa?" |
| **Bloque FAQ** | Sub-pregunta que remueve una duda residual una vez tomada la decisión | "¿Puedo reagendar la evaluación?" |

**Regla dura: la objeción central nunca vive en un acordeón.** Si lo que mata el negocio quedó
enterrado en la FAQ al pie, la landing no lo resolvió — eso es una falla de arquitectura, no un
detalle de contenido.

**Las FAQ no son un mecanismo aparte:** son la salida de este mismo mapa. Sus fuentes, por fuerza
descendente:

1. **Lo que realmente le preguntan a la empresa** — WhatsApp, formularios, correos, llamadas.
   Evidencia de primera mano; pesa más que todo lo demás.
2. **Queries de entrada con forma de pregunta** — GSC, términos de búsqueda de campaña.
3. **PAA**, con la escala de peso de [entrada-y-demanda.md](entrada-y-demanda.md).
4. **Objeciones** de `contexto/sitio.md` y de `contexto/antecedentes/`.
5. **Comportamiento** — rage/dead clicks cerca de un bloque, scroll que se detiene.

La forma de responder cada FAQ (respuesta directa primero, 40–80 palabras) la aplica
`brand-voice-enforcement` al redactar; aquí solo defines qué preguntas entran y qué debe contener
cada respuesta.

---

## Formato de registro

Por cada pregunta del mapa, deja registrado:

```
pregunta: <la pregunta, en el lenguaje del visitante cuando se conozca>
prioridad: <alta | media | baja>   ← según conciencia, temperatura y arquetipo
cuando_pregunta: <momento natural en el recorrido>
cuando_conviene_responder: <momento según la economía de la conversión>
movida: <responder donde se pregunta | diferir con acuse | reformular>
razon_movida: <una línea; obligatoria si no es "responder donde se pregunta">
destino: <sección propia | bloque FAQ>
evidencia: <fuente + fecha>
confianza: <Alta | Media | Baja>
```

Este registro va en el bloque plegado *Sustento y evidencia* del blueprint. La tabla visible de
arquitectura solo muestra la sección, la pregunta que resuelve y la confianza — el detalle queda
disponible para auditar la decisión, no al frente.
