# Modelos destino y formato

Aplicar en el bloque **j** del paso 5 y al entregar (paso 7).

Este archivo describe **comportamientos**, no versiones. Los modelos cambian de número cada pocos meses; lo que se mantiene es la familia de comportamiento. Si el usuario nombra un modelo que no aparece aquí, ubicarlo por comportamiento preguntando o probando, no asumir.

## Familias por comportamiento

| Familia | Cómo prefiere el prompt | Prompt negativo | Notas |
|---|---|---|---|
| Tipo Midjourney | frase descriptiva compacta, buen rendimiento con estilo declarado; los parámetros van al final con `--` | sí, inline con `--no` en el mismo texto | fuerte carácter estético propio; conviene contrarrestarlo con instrucciones concretas si se busca neutralidad |
| Tipo difusión abierta (SD, SDXL y derivados) | etiquetas separadas por comas, orden por importancia; admite pesos | sí, muy efectivo; se integra con la línea `Negative prompt:` | el más sensible al orden y a la sintaxis de peso |
| Tipo Flux | prosa natural y larga, entiende relaciones espaciales descritas en lenguaje corriente | poco o nulo efecto; redactar en positivo | responde mal a listas de etiquetas sueltas; premia la frase bien construida |
| Tipo conversacional (DALL·E, Imagen, Nano Banana y similares) | instrucción en lenguaje natural, como se le explicaría a una persona | no admite; se expresa como instrucción positiva | suele reescribir el prompt internamente; conviene ser explícito con lo que **no** debe aparecer, en positivo |

**Cuando el usuario no dice a qué modelo apunta:** entregar en prosa descriptiva. Es lo que funciona razonablemente en las cuatro familias, y ofrecer la adaptación a una concreta.

## Negativos: siempre dentro de la misma salida

El negativo **nunca se entrega en un bloque aparte**. El usuario debe poder copiar una sola vez. Cómo se integra depende de la familia:

| Familia | Cómo integrarlo en el mismo texto |
|---|---|
| Tipo Midjourney | al final de la misma línea, con `--no elemento, elemento`, junto al resto de parámetros (`--ar 3:2 --no texto, marca de agua`) |
| Tipo difusión abierta | en una segunda línea del mismo bloque, con la etiqueta literal `Negative prompt:`. Es el formato de metadatos que estas interfaces reconocen al pegar el bloque completo, de modo que reparten cada parte en su campo |
| Tipo Flux | no hay campo negativo: las exclusiones se redactan en positivo dentro de la prosa |
| Tipo conversacional | no hay campo negativo: las exclusiones se redactan en positivo dentro de la instrucción |

Ejemplo de salida única para difusión abierta — un solo bloque, un solo copiado:

```
retrato de una mujer de unos 60 años, 85 mm, f/2, luz de ventana lateral suave, fondo disuelto
Negative prompt: manos deformes, texto, marca de agua, firma
Steps: 30, CFG scale: 6, Size: 832x1216
```

En las familias sin campo negativo, no escribir "sin X" y esperar que funcione: en varias arquitecturas mencionar un concepto lo introduce. Convertir la negación en afirmación:

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

## Semilla y reproducibilidad

Si el usuario quiere iterar sobre un resultado concreto, recordarle fijar la semilla en los modelos que la exponen: permite cambiar un bloque del prompt y ver el efecto aislado, que es exactamente lo que pide el paso 8 del flujo.
