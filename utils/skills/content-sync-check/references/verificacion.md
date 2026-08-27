# Modo 1 · Verificar (por defecto)

Compara cada pieza aprobada de la fuente contra sus destinos y reporta. **Este modo no escribe
nada** — ni en la fuente, ni en el sitio, ni en el canvas. Reparar es el otro modo, y solo se entra
si el usuario lo pide.

## Qué entra al chequeo

Las piezas cuyo frontmatter diga `estado: aprobado` o `estado: publicado`. Un borrador que no
coincide con el sitio **no es un hallazgo**. Si el usuario nombra una página concreta, verifícala
aunque esté en borrador — diciéndolo.

Si ninguna pieza tiene `estado:`, no falles: dilo en una línea y ofrece verificar el mapeo
completo igualmente (`task-flow` mantiene ese campo al cerrar la tarea que aprueba).

## Los cuatro cotejos

### 1 · Fuente contra el sitio

Campo a campo, según las claves del frontmatter de la fuente (el esquema de la colección manda:
`content.config.ts`). Tres resultados por campo: coincide, difiere, o **falta en el sitio**.

El caso más grave y más silencioso es el tercero: un bloque entero de la fuente —cifras, cobertura,
preguntas frecuentes— que nunca llegó al archivo publicado. **Repórtalo por nombre de campo**, no
como «faltan cosas»: quien lo lee tiene que saber qué sección falta sin abrir los dos archivos.

**Antes de declarar que algo falta, búscalo en el resto del destino.** Un texto puede haberse
movido de bloque por una decisión de diseño o de maquetación: entonces no falta, está en otro
sitio, y reportarlo como ausente genera dos hallazgos falsos y arriesga duplicarlo al reparar.
Cómo distinguirlo: `comparacion.md`, § *Contenido que se movió*.

El cuerpo en prosa (bajo el frontmatter) se compara por bloques: encabezados y párrafos. Un
reordenamiento no es una diferencia de contenido, pero **dilo** si lo detectas.

### 2 · Fuente contra Claude Design

**Se compara contra la página, y solo contra la página**: el `.dc.html` que vive en la raíz del
proyecto. Extrae su texto visible y compáralo con el de la fuente.

**Nunca compares contra `uploads/`**: es material temporal que el usuario le pasa al chat
—borradores, referencias, descartes—. Un mismo documento aparece ahí varias veces con sufijos de
hash porque son subidas distintas, no versiones, y ninguna representa lo publicado.

**El texto casi nunca está en el marcado**: las páginas usan plantillas (`sc-for`, `{{ item.q }}`)
y guardan el contenido en constantes del script. Buscarlo en el HTML visible da por ausente lo que
sí está. El método completo, en `extraccion.md` — léelo antes de comparar contra el diseño.

Compara **texto**, no marcado: espacios, saltos de línea y entidades HTML no son diferencias de
contenido. Una cifra distinta, una frase que cambió o un párrafo ausente, sí.

### 3 · Variantes de dispositivo entre sí

Cada variante se compara **contra la fuente**, no una contra otra. Pero **que difieran entre sí no
es, por sí solo, un hallazgo**: escritorio y móvil son medios distintos y es normal que móvil
condense o esconda lo accesorio. Detalle en `dispositivos.md` — léelo antes de reportar una
diferencia entre variantes.

**Que no exista variante móvil no es un hallazgo.** Muchas páginas se diseñan solo en escritorio. La
ausencia solo se reporta si el mapeo declara que debería existir.

### 4 · Espejo local

Compara los `.dc.html` del espejo (`htmls/`) con los del canvas: se actualiza a mano, así que se
desfasa solo. Reporta lo que el canvas tiene y el espejo no, y lo que difiere. No bloquea nada —el
chequeo real va contra el canvas— pero avisa de que la copia local dejó de representarlo.

## Huérfanos

Páginas en el canvas sin fuente ni contraparte en el sitio. **Repórtalas, no las trates como
error**: pueden ser pruebas, exploraciones o páginas cuya fuente está por localizar. Una línea por
cada una, agrupadas al final del reporte.

Los excluidos declarados en la configuración (wireframes, canvas de trabajo) no se reportan aquí:
ya se decidió que no entran.

> **A partir de tres piezas, delega la extracción a subagentes** —uno por pieza— y quédate con la
> síntesis. Cómo hacerlo y qué deben devolver: `extraccion.md`, § *Delegar*.

## El reporte

**Agrupa por pieza, no por destino**: al usuario le importa «cómo está esta página», no «qué pasa
en el sitio». Una línea de veredicto por pieza y, debajo, solo lo que difiere. Estructura:

1. **Resumen en una línea**: cuántas piezas al día, cuántas con diferencias, cuántos destinos no se
   pudieron verificar.
2. **Una sección por pieza con hallazgos**: qué destino, qué campo, y qué dice cada lado. Las
   piezas que coinciden se mencionan en una sola línea agrupada — no ocupan espacio.
3. **Reubicaciones** —texto que cambió de bloque sin cambiar— en su propio grupo, aparte de las
   diferencias de contenido: no son un problema, y mezclarlas sube el ruido del reporte.
4. **Huérfanos y pendientes**, al final.
5. **Lo que no se pudo verificar**, siempre explícito: destino inaccesible, pieza sin `estado:`,
   página sin mapear.

Sé literal citando: **el texto de las piezas se cita, no se parafrasea**. En contenido médico, un
resumen aproximado de la diferencia no sirve para decidir.

## Al cerrar

Si **varios lados divergen a la vez** sobre el mismo bloque, no lo trates como una reparación
simple: es una reconciliación y tiene su propio método (`reconciliacion.md`).

Si hay hallazgos, ofrece en una línea: **repararlos** (`reparacion.md`) o **registrarlos** como
tarea vía `task-flow`. Si el usuario elige registrar y el texto corregido es largo, escríbelo en un
archivo del reporte y que la tarea lleve el puntero: los comentarios de `task-flow` se recortan a
900 caracteres y el texto se perdería.

Si no hay hallazgos, dilo en una línea y para. No hace falta un informe para decir que todo
coincide.

## Cuando fuente y destino no comparten esquema

Pasa en artículos de blog: el archivo de trabajo lleva metadata editorial (origen, keyword, voz),
wikilinks `[[…]]` y notas internas, mientras el destino espera el frontmatter del motor del sitio
y prosa limpia. **No lo reportes como «faltan todos los campos»** — es ruido. Dilo en una línea y
compara lo que sí es comparable: el texto del cuerpo, bloque a bloque.

**Convertir un formato en el otro no es trabajo de este skill**: traducir wikilinks a rutas,
decidir autor y categoría o volver un bloque componente del motor son decisiones editoriales que se
resuelven al publicar, con el artículo delante.

## Errores

| Situación | Qué hacer |
| --- | --- |
| Una página del mapeo no existe en un destino | Repórtalo como «falta en destino»; no es un error del chequeo. |
| Fuente y destino no comparten ninguna clave de frontmatter | Dilo en una línea y compara solo el cuerpo; no listes cada clave como ausente. |
| El `.dc.html` es demasiado grande para leer entero | Extrae solo el texto visible; no vuelques el HTML al contexto. |
| El frontmatter de la fuente no parsea | Dilo con la línea del problema y sáltala; no adivines el contenido. |
| La fuente y el destino difieren solo en espacios o comillas tipográficas | No es hallazgo. Menciónalo solo si el usuario pregunta. |
| Un campo existe en el destino y no en la fuente | Es un hallazgo en dirección contraria: repórtalo, y recuerda que sitio → fuente no se propaga solo. |
