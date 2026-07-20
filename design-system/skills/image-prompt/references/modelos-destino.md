# Modelos destino y formato

Aplicar en el bloque **j** del paso 5 y al entregar (paso 7).

Este archivo describe **comportamientos**, no versiones. Los modelos cambian de número cada pocos meses; lo que se mantiene es la familia de comportamiento. Si el usuario nombra un modelo que no aparece aquí, ubicarlo por comportamiento preguntando o probando, no asumir.

## Destino por defecto: conversacional (ChatGPT imágenes)

Es el destino habitual de este usuario. **Asumirlo salvo mención explícita de otro modelo**, y no preguntar por el modelo si no hay señal de que sea otro.

Consecuencias prácticas al redactar:

- **Una sola instrucción, en prosa.** Ni etiquetas separadas por comas ni banderas. La familia interpreta lenguaje natural y responde mejor a una descripción bien construida que a una lista de atributos.
- **No hay campo negativo.** Todo lo que no debe aparecer se expresa afirmando lo que sí hay. Ver la tabla de conversión más abajo.
- **El formato va en palabras.** "En formato vertical 9:16, con espacio libre en el tercio superior para un titular", no `--ar 9:16`.
- **Reescribe el prompt internamente** antes de generar. Por eso conviene ser explícito y concreto: lo ambiguo lo resuelve por su cuenta, y no siempre como conviene.
- **Es de las mejores familias con texto dentro de la imagen**, pero sigue degradándose con frases largas. Una línea corta entre comillas, y el resto compuesto después.
- **Admite conversación.** Si el resultado no convence, se puede pedir un ajuste sobre la imagen ya generada en vez de reescribir el prompt entero — que es justo lo que pide el paso 8 del flujo.

## Otras familias

Solo aplican cuando el usuario nombra el modelo explícitamente.

| Familia | Cómo prefiere el prompt | Prompt negativo | Notas |
|---|---|---|---|
| Tipo Midjourney | frase descriptiva compacta, buen rendimiento con estilo declarado; los parámetros van al final con `--` | sí, inline con `--no` en el mismo texto | fuerte carácter estético propio; conviene contrarrestarlo con instrucciones concretas si se busca neutralidad |
| Tipo difusión abierta (SD, SDXL y derivados) | etiquetas separadas por comas, orden por importancia; admite pesos | sí, muy efectivo; se integra con la línea `Negative prompt:` | el más sensible al orden y a la sintaxis de peso |
| Tipo Flux | prosa natural y larga, entiende relaciones espaciales descritas en lenguaje corriente | poco o nulo efecto; redactar en positivo | responde mal a listas de etiquetas sueltas; premia la frase bien construida |

## Negativos: siempre dentro de la misma salida

El negativo **nunca se entrega en un bloque aparte**. El usuario debe poder copiar una sola vez.

En el destino por defecto no hay nada que integrar: no existe campo negativo, así que las exclusiones se redactan en positivo dentro de la propia instrucción y la salida es naturalmente una sola. Ejemplo:

```
Un retrato de estudio de una mujer de unos 60 años, de tres cuartos, mirando a cámara con
expresión serena. Luz de ventana lateral suave que modela el rostro y deja el fondo en
penumbra. Fondo liso de color arena, sin objetos ni texto. Aspecto de fotografía tomada con
teleobjetivo corto y diafragma abierto: el rostro nítido y el fondo suavemente desenfocado.
Piel con textura natural, sin retoque. Formato vertical 4:5.
```

Nótese que "sin objetos ni texto" y "sin retoque" funcionan porque niegan una *categoría ausente*, no un objeto concreto: no introducen nada que dibujar. Negar un sustantivo visual —"sin perros", "sin coches"— sí tiende a introducirlo, y debe reescribirse describiendo la escena vacía.

Cuando el usuario nombre explícitamente un modelo de otra familia:

| Familia | Cómo integrarlo en el mismo texto |
|---|---|
| Tipo Midjourney | al final de la misma línea, con `--no elemento, elemento`, junto al resto de parámetros (`--ar 3:2 --no texto, marca de agua`) |
| Tipo difusión abierta | en una segunda línea del mismo bloque, con la etiqueta literal `Negative prompt:`. Es el formato de metadatos que estas interfaces reconocen al pegar el bloque completo, de modo que reparten cada parte en su campo |
| Tipo Flux | no hay campo negativo: las exclusiones se redactan en positivo dentro de la prosa |

Tabla de conversión de negaciones a afirmaciones:

| En vez de | Escribir |
|---|---|
| sin fondo desordenado | fondo liso y despejado |
| sin gente | espacio vacío, sin presencia humana → mejor: describir el lugar deshabitado |
| sin texto | superficie limpia, sin rótulos |
| sin deformidad en las manos | manos visibles en pose simple y relajada |

Cuando el modelo **sí** admite negativo, el bloque útil es corto y específico del fallo esperado del tipo de imagen: manos y dedos en escenas con personas, texto ilegible en piezas gráficas, marcas de agua y firmas en cualquier caso, distorsión de líneas rectas en arquitectura.

## Relación de aspecto por uso final

| Uso | Relación | Orientación |
|---|---|---|
| Feed cuadrado | 1:1 | cuadrada |
| Feed vertical de redes | 4:5 | vertical |
| Stories, reels, vertical completo | 9:16 | vertical |
| Hero web, cabecera | 16:9 | horizontal |
| Fotografía estándar | 3:2 | ambas |
| Póster, portada editorial | 2:3 | vertical |
| Panorámica cinemática | 21:9 | horizontal |
| Banner ancho | 3:1 | horizontal |
| Icono, avatar | 1:1 | cuadrada |

Si la identidad visual declara `Formatos habituales`, esos mandan sobre esta tabla.

## Margen de seguridad y espacio para texto

Cuando la pieza vaya a llevar texto, logo o interfaz encima, reservarlo **en la composición**, no recortarlo después:

- Declarar explícitamente dónde va el espacio libre: "espacio negativo amplio en el tercio superior", "zona lisa a la izquierda para titular".
- En vertical de redes, los extremos superior e inferior quedan tapados por la interfaz: no poner ahí el punto de interés.
- Si lleva logo, reservar una esquina con fondo de bajo contraste para que el logo sea legible.
- Pedir el sujeto ligeramente descentrado cuando el texto ocupará un lado.

## Resolución

Pedir la resolución nativa del modelo y escalar después si hace falta; forzar dimensiones muy fuera de lo habitual degrada la composición y suele duplicar elementos. Para impresión, generar en la relación correcta y escalar con una herramienta dedicada, no pidiendo un número de píxeles mayor en el prompt.

## Iterar sobre un resultado

En el destino por defecto no hay semilla que fijar. La vía de iteración es conversacional: pedir el ajuste sobre la imagen ya generada —"la misma imagen pero con la luz entrando desde la izquierda"— en lugar de reescribir y reenviar el prompt completo. Mantiene el resto de la composición y aísla el cambio, que es lo que pide el paso 8 del flujo.

En las familias que exponen la semilla, fijarla cumple la misma función y conviene recordarlo cuando el usuario nombre una de ellas.
