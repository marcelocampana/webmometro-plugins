# Cuando divergen tres lados a la vez

«La fuente manda» resuelve el caso simple: la fuente cambió y un destino se quedó atrás. No resuelve
el caso real: **cada lado tiene algo que los otros no**, y todo parece legítimo. Esta referencia es
para ese caso.

**El principio: no elijas tú.** Con contenido médico o regulado, decidir qué versión gobierna no es
una operación técnica — es una decisión editorial con consecuencias clínicas. El trabajo del skill
es **reconstruir qué pasó y presentarlo de forma decidible**, no resolverlo.

## 1 · Reconstruir la historia antes de proponer nada

Una divergencia sin explicación no se puede decidir. Reúne, para cada lado:

- **Fecha de modificación** del archivo (en el repo, `git log -1 --format=%ci -- <archivo>`; en el
  workspace, el filesystem).
- **`fecha_aprobacion`** de la fuente, si la tiene.
- **Qué commit tocó el destino por última vez** y qué decía su mensaje: a menudo explica el cambio
  mejor que el diff.
- **Si el bloque divergente existía antes** en algún lado (`git log -S '<frase>'` encuentra cuándo
  entró o salió una frase).

Con eso, casi siempre se distingue **contenido añadido** de **contenido revertido**, que es la
distinción que cambia la decisión.

## 2 · Clasificar cada diferencia por separado

**Una página no diverge: divergen sus bloques.** Trata cada campo por separado — es normal que
`faq` esté al día y `stats` no. Clasifica cada uno:

| Patrón | Lectura probable | Qué proponer |
| --- | --- | --- |
| Está en la fuente, falta en los demás | Nunca se propagó | Propagar desde la fuente |
| Está en un destino, falta en fuente y en el otro | Se añadió en el destino | Traerlo a la fuente y luego propagar |
| Está en los dos destinos, no en la fuente | Se añadió antes de una copia y la fuente quedó atrás | Traerlo a la fuente |
| Difiere en los tres, mismo tema | Ediciones paralelas | **No proponer merge**: mostrar las tres y preguntar |
| Está en la fuente, falta en los destinos, y la fuente es más antigua | Puede ser contenido **retirado a propósito** | Preguntar antes de reponer |

La última fila es la trampa: reponer contenido que alguien retiró deliberadamente —una cifra sin
fuente, una afirmación sin validar— es peor que dejarlo faltando. **Si la fuente es más antigua que
el destino, la ausencia no es un olvido hasta que se confirme.**

## 3 · Presentar para decidir, no para leer

Por cada bloque divergente, muestra **las tres versiones literales**, con su fecha, y una lectura de
qué pasó en una línea. Nada de resúmenes: en contenido médico la diferencia está en la palabra
exacta.

```
stats.items[3] — difiere en los tres
  fuente (2026-08-20):  «12% había accedido a terapias avanzadas»
  sitio   (2026-07-14):  ausente
  diseño  (2026-08-22):  «12% había accedido… al 30 de septiembre de 2024»
  Lectura: el diseño precisa la fecha de corte; el sitio nunca recibió el bloque.
```

Y ofrece opciones **concretas**, no genéricas: cuál versión adoptar, o mantener la divergencia si es
intencional. «¿Qué hacemos?» no es una opción.

## 4 · Aplicar en el orden correcto

Cuando el usuario decide, **la fuente se actualiza primero, siempre** — aunque el contenido venga de
un destino. Solo después se propaga desde la fuente a los demás.

Saltarse ese orden —copiar del diseño directo al sitio— deja la fuente mintiendo y reproduce el
problema que se estaba arreglando. Es el orden lo que sostiene que la fuente sea la fuente.

Tras aplicar, **verifica de nuevo solo lo tocado** y confirma que los tres lados coinciden.

> Antes de tratar una ausencia como divergencia, descarta que el texto solo se haya **movido de
> bloque** por una decisión de diseño: `comparacion.md`, § *Contenido que se movió*.

## Cuando hay varios candidatos a ser «la» página

Distinto del caso anterior: aquí no divergen tres lados, sino que **un mismo lado ofrece varias
páginas** que podrían ser la buena — `Página.dc.html` y `Página v2.dc.html`, o una variante con
sufijo. Antes de comparar contra ninguna, hay que saber cuál cuenta.

**No lo decidas por el nombre.** «v2» no siempre es la vigente: puede ser una exploración que se
descartó, o la anterior que quedó por si acaso.

1. **Mira el mapeo**: si la configuración declara cuál es la página de esa pieza, esa manda y las
   demás ni se miran.
2. **Si no está declarado**, presenta los candidatos con su fecha de modificación y en qué se
   diferencian —una línea cada uno— y **pregunta cuál es la vigente**.
3. **Registra la respuesta en el mapeo** para no volver a preguntar. Las demás pasan a la lista de
   excluidos, con su motivo.

Lo mismo vale al revés: si una fuente empareja con dos destinos posibles, no elijas — muestra ambos.

## Divergencias intencionales

No todo lo que difiere está mal. Un destino puede omitir algo a propósito: un bloque que no aplica
a móvil, una sección que el sitio resuelve con un componente propio.

Cuando el usuario decida que una divergencia es intencional, **regístrala en la fuente** —una nota
en el frontmatter o junto al bloque— para que la próxima corrida no la vuelva a levantar. Un
hallazgo que reaparece cada vez y siempre se descarta enseña a ignorar el reporte entero.

## Errores

| Situación | Qué hacer |
| --- | --- |
| No hay fechas fiables en ningún lado | Dilo: sin cronología no hay lectura de qué pasó, solo diferencias. Presenta las versiones y no interpretes. |
| El usuario pide «usa la más completa» | Confírmalo bloque a bloque: más largo no es más correcto, y puede reponer algo retirado a propósito. |
| Dos destinos coinciden entre sí y difieren de la fuente | Es señal de que la fuente quedó atrás, no de que los destinos estén mal. Dilo así. |
| La divergencia es una cifra, una fecha o un fármaco | Marca prioridad alta: no lo mezcles con diferencias de redacción en el mismo listado. |
| El usuario no decide ahora | Regístralo como tarea con las versiones literales; no dejes la decisión solo en el chat. |
