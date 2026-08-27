# Qué se compara, y qué no cuenta como diferencia

Un chequeo que reporta ruido deja de leerse. Estas son las reglas para que un hallazgo signifique
siempre «alguien tiene que hacer algo».

## Lo que nunca es un hallazgo

Esta lista es **cerrada y objetiva**: se descarta por saber lo que es —un campo de proceso con
nombre conocido, una diferencia tipográfica— nunca por parecer poco importante. **Lo que no esté
aquí, se reporta**, aunque parezca menor; ante la duda, reportar. Un aviso de más cuesta una línea
de lectura; uno de menos puede dejar sin ver un dato clínico.

**Metadata de proceso editorial.** Vive en la fuente porque el equipo la necesita, y no viaja al
sitio por diseño: `origen_spoke`, `pilar`, `keyword_objetivo`, `keywords_secundarias`,
`volumen_mensual`, `intencion`, `audiencia`, `voz`, `estado`, `fecha_aprobacion`,
`fecha_redaccion`, `schema_sugerido`, `spokes_relacionados`, `url_existente`. Su ausencia en el
destino es lo esperado.

**Notas internas.** Comentarios HTML en la fuente (`<!-- NOTAS PARA EL EQUIPO … -->`) y todo lo que
marquen como no publicable. Nunca deben aparecer en un destino: si aparecen, **eso sí es un
hallazgo** — se filtró contenido interno.

**Marcadores de pendiente.** `[PENDIENTE-enlace-…]` y similares son parte del texto mientras
existan: si están en los dos lados, coinciden. Pero **cuéntalos en el reporte**: una pieza aprobada
con marcadores de pendiente es algo que el usuario querrá saber antes de publicar.

**Diferencias de forma sin efecto en el texto**: espacios, saltos de línea, comillas rectas frente
a tipográficas, entidades HTML (`&aacute;` vs `á`), y el orden de las claves del frontmatter.

**Capitalización de nombres de archivo** — en macOS son el mismo archivo; empareja ignorándola.

**Ausencia de una variante de dispositivo** que el mapeo no declara.

**Rutas de imagen distintas** que apuntan al mismo recurso (`/images/x.png` vs `assets/x.png`):
compara el nombre del archivo, no la ruta. Si el nombre difiere, sí es hallazgo.

## Lo que siempre es un hallazgo

- **Un campo del esquema presente en la fuente y ausente en el destino.** El caso más silencioso y
  el más grave.
- **Un texto que difiere**: una cifra, una fecha, una frase, un nombre propio.
- **Un bloque de prosa presente en un lado y no en el otro.**
- **Dos variantes de dispositivo que dicen cosas distintas** sobre el mismo contenido.
- **Un destino modificado después de la `fecha_aprobacion`** de la fuente: alguien tocó el destino
  saltándose el flujo.
- **Contenido interno filtrado a un destino** (notas del equipo, comentarios de trabajo).
- **Una negación, un condicional o un matiz que cambia**: «no», «solo si», «salvo», «puede» frente
  a «debe». Basta una palabra para invertir una indicación clínica, y es la diferencia más fácil de
  pasar por alto porque el resto del párrafo coincide.
- **Contenido en un destino que no está en la fuente**: nadie lo aprobó. Repórtalo siempre, aunque
  encaje en alguna categoría de las descartables.

## Cifras y datos: el caso que más importa

En contenido médico o regulado, **una cifra distinta no es una diferencia de estilo**: es hallazgo
siempre, aunque el resto del párrafo coincida, y va **literal en el reporte** —las dos versiones,
sin redondear ni parafrasear—.

Atención especial a porcentajes, años, edades, plazos, dosis, cantidades, leyes, fármacos, y el año
o la institución de la fuente citada. Una cifra igual en valor pero con otra fuente o año **también**
es hallazgo.

## Comparar frontmatter

Clave por clave, por **nombre de clave**, no por posición. Para valores anidados (objetos, listas),
compara elemento a elemento y reporta la ruta completa del que difiere: `stats.items[2].label`, no
«algo en stats».

En listas, distingue tres casos y nómbralos distinto: **falta un elemento**, **sobra un elemento**,
**un elemento difiere**. Un reordenamiento sin cambio de contenido no es un hallazgo, pero
menciónalo si cambia el orden visible en la página.

## Comparar prosa

Por bloques: encabezados, párrafos, elementos de lista. Empareja los bloques por su encabezado más
cercano, no por posición, para que un bloque insertado no desplace todo lo demás y genere un
reporte de diferencias falso.

Dentro de un bloque, compara el texto plano: el énfasis (`**negrita**`, `*cursiva*`) y los enlaces
se comparan por su texto visible. Que un enlace cambie de destino **sí** es un hallazgo.

## Comparar HTML renderizado

Extrae el texto visible: descarta etiquetas, atributos, estilos y scripts. Conserva el orden y los
límites de bloque.

Los `.dc.html` suelen traer comentarios de sección (`<!-- HERO -->`, `<!-- CIFRAS -->`,
`<!-- ACCESO -->`) que delimitan bloques y **suelen corresponder a los campos del esquema**. Úsalos
para ubicar dónde cae cada diferencia y para nombrarla en términos que el usuario reconozca.

**No vuelques el HTML completo al contexto.** Un `.dc.html` de página real pesa decenas de miles de
caracteres: extrae el texto y trabaja con eso.

## Umbral de ruido

Si una pieza acumula muchas diferencias menores de forma, **no las listes una por una**: dilo en
una línea agregada («difieren en espaciado en 14 lugares, sin cambio de texto») y sigue. El detalle
solo si el usuario lo pide.

Si una pieza difiere en todo, probablemente el mapeo está mal —dos páginas distintas emparejadas—:
**dilo como sospecha de mapeo**, no como 40 hallazgos de contenido.

## Contenido que se movió, no que falta

**El falso hallazgo más frecuente y más caro.** El diseño reubica texto: un párrafo del `hero` que
resultó largo baja a la sección siguiente, un dato salta de bloque, dos bloques se fusionan. El
contenido está completo y aprobado — cambió de sitio.

Leído campo a campo produce **dos hallazgos falsos**: «falta en `hero`» y «sobra en `intro`». Y si
se repara el primero sin ver el segundo, **el párrafo queda duplicado**.

**Antes de declarar que un texto falta, búscalo en toda la página, no solo en su bloque.** Compara
normalizado (sin tildes, mayúsculas ni puntuación); basta que coincida una tirada de ~8-10
palabras, porque el reencuadre suele reescribir el principio o el final, no el medio.

| Lo que encuentras | Qué es | Cómo reportarlo |
| --- | --- | --- |
| El texto está, en otro bloque | Se movió | **Un** hallazgo de reubicación, no dos |
| Está partido entre dos bloques | Se dividió por longitud | Uno, diciendo dónde quedó cada parte |
| No está en ninguna parte | Falta de verdad | Hallazgo de contenido ausente |

Repórtalo en una línea que nombre origen y destino, y **sepáralo del resto**: una reubicación sin
cambio de texto no es un problema de contenido, y mezclarla con cifras divergentes hace que todo se
lea con la misma alarma.

**Por defecto no propongas nada**: la decisión de diseño es legítima y no se revierte desde un
chequeo de sincronización. Ofrece anotarla en la fuente para no volver a levantarla, y sigue.
**Nunca la propagues al sitio**: que el diseño reordene no obliga al sitio a reordenar.

Solo hay algo que decidir si la reubicación **cambia el sentido** — un dato separado de la fuente
que lo respalda, una advertencia clínica lejos de aquello a lo que advierte. Eso se señala como
problema editorial, no como desincronización.
