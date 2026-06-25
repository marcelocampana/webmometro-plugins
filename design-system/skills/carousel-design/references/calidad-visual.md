# Framework de Calidad Visual Compositiva

10 principios organizados en 3 grupos funcionales. Aplicar internamente — nunca reportar el framework al usuario; solo reportar los problemas encontrados y las correcciones aplicadas.

---

## Grupo 1 — Espacio y respiración

### 1. Respiración visual
**Pregunta:** ¿Hay aire suficiente entre elementos y entre el contenido y los bordes?
**Síntoma de fallo:** Texto o íconos que "tocan" otros elementos o quedan demasiado cerca del borde del lienzo.
**Corrección:** Aumentar `padding`, `margin` o `gap` entre bloques. Asegurarse que el área segura mínima (76–110px) esté respetada en los cuatro lados.

### 2. Márgenes consistentes
**Pregunta:** ¿Los márgenes internos son coherentes con el área segura del sistema?
**Síntoma de fallo:** Márgenes distintos en láminas similares del mismo carrusel; contenido que se recorta al 1080×1350px.
**Corrección:** Unificar el valor de `padding` o `left`/`right` de la safe-area a lo largo de todas las láminas. Valor mínimo: 76px; valor confortable: 96–110px.

### 3. Espacio negativo
**Pregunta:** ¿El vacío trabaja a favor de la composición, o hay zonas de lienzo desperdiciadas?
**Síntoma de fallo:** Todo el espacio está ocupado sin ritmo, o hay una zona vacía grande que rompe el balance sin intención.
**Corrección:** Redistribuir elementos para que el espacio en blanco guíe la mirada hacia el punto focal. En portadas, el espacio negativo debe favorecer el titular.

---

## Grupo 2 — Organización y jerarquía

### 4. Agrupación
**Pregunta:** ¿Los elementos relacionados están visualmente próximos entre sí?
**Síntoma de fallo:** Eyebrow, titular y subtítulo con gaps inconsistentes; dato y fuente separados por demasiado espacio.
**Corrección:** Reducir `margin-bottom` entre elementos del mismo bloque semántico. Usar `gap` unificado dentro del bloque de contenido.

### 5. Separación
**Pregunta:** ¿Los elementos no relacionados tienen distancia suficiente para leerse como grupos distintos?
**Síntoma de fallo:** El bloque de texto se confunde visualmente con el logo, los íconos o la figura.
**Corrección:** Aumentar la distancia entre bloques de contenido distintos. Si la figura y el texto compiten por el mismo espacio visual, ajustar `max-width` del texto o reposicionar la figura.

### 6. Jerarquía visual
**Pregunta:** ¿El ojo recorre la lámina en el orden correcto — eyebrow → titular → cuerpo → CTA?
**Síntoma de fallo:** El cuerpo de texto tiene peso similar al titular; el eyebrow no se lee como etiqueta secundaria.
**Corrección:** Verificar contraste de tamaños entre niveles (titular al menos 1.5× el cuerpo). Si el peso visual del cuerpo compite con el titular, reducir `font-size` o `font-weight` del cuerpo.

### 7. Distribución y balance
**Pregunta:** ¿Los elementos están equilibrados en el espacio de la lámina — ni todo arriba, ni todo a un lado sin contrapeso?
**Síntoma de fallo:** Lámina cargada en la mitad superior con la zona inferior vacía; o figura derecha sin contrapeso visual a la izquierda.
**Corrección:** Distribuir el contenido para que el peso visual esté repartido. En Modo B2, el bloque de texto actúa como contrapeso a la figura — asegurarse de que tienen masa visual comparable.

---

## Grupo 3 — Legibilidad

### 8. Densidad de texto
**Pregunta:** ¿El bloque de texto se siente equilibrado, o la lámina está saturada de palabras?
**Síntoma de fallo:** Más de 55–65 palabras visibles en la lámina; párrafos apretados sin `line-height` suficiente.
**Corrección:** Reducir el copy (si el contenido lo permite) o dividir en dos láminas. Asegurarse de `line-height` ≥ 1.4 en cuerpos de texto.

### 9. Contraste
**Pregunta:** ¿El texto es legible sobre su fondo? ¿Hay suficiente diferencia de valor cromático?
**Síntoma de fallo:** Texto sobre imagen sin overlay; texto claro sobre fondo claro; texto oscuro sobre fondo oscuro saturado.
**Corrección:** Agregar overlay semitransparente bajo el texto si hay imagen de fondo. Usar el color de texto del sistema para garantizar contraste mínimo 4.5:1 (WCAG AA).

### 10. Legibilidad general
**Pregunta:** ¿La lámina se puede leer y entender en 3 segundos sin esfuerzo?
**Síntoma de fallo:** La lámina requiere más de un vistazo para captar el mensaje principal; el orden de lectura no es evidente.
**Corrección:** Si la respuesta es no, identificar cuál de los 9 principios anteriores falla y aplicar la corrección correspondiente. Este criterio es el diagnóstico integrador de los demás.

---

## Protocolo de aplicación

**Durante producción (paso 9):** aplicar los 10 principios inmediatamente después de escribir el HTML de cada lámina, antes de pasar a la siguiente. Corregir en el momento. Silencioso — solo reportar al usuario si el problema requiere una decisión editorial (ej. reducir copy).

**Después de renderizado (paso 11):** aplicar los 10 principios sobre lo que se ve en pantalla — no sobre el código. Este pase detecta problemas de proporciones, densidad percibida y overflow sutil que el código no revela. Corregir antes de entregar y registrar observaciones en `qa/`.
