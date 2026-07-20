# Tipos de imagen — Taxonomía y perfil de bloques

Esta referencia gobierna el paso 2 del flujo. El tipo determina qué bloques del paso 7 aplican, qué vocabulario usar y cuánto detalle es útil.

Regla general: **los bloques que no aplican no se escriben en versión suave — se omiten.** Poner "sin profundidad de campo" en un vector plano introduce un concepto óptico donde no lo había.

## Cómo clasificar

Clasificar por lo que el usuario necesita, no por la palabra que usó. Señales útiles:

- Menciona un uso comercial concreto (web, catálogo, ficha) → probablemente producto, no "foto" genérica.
- Menciona una marca, logo o pieza gráfica → iconografía, vector o diseño gráfico.
- Menciona un espacio que aún no existe → render arquitectónico, no fotografía.
- Menciona un personaje inventado → personaje o concept art, no retrato.
- Describe un proceso o una relación entre partes → infografía o diagrama.

Cuando dos tipos plausibles den resultados muy distintos, preguntar. Cuando den resultados parecidos, elegir el más probable y declararlo.

## Familia fotográfica

Todos admiten el bloque **f (parámetros fotográficos)**. Ninguno admite vocabulario de ilustración o render.

| Tipo | Bloques que pesan | Qué omitir | Vocabulario propio | Error típico |
|---|---|---|---|---|
| Retrato | luz, expresión, lente larga, piel | efectos, materiales ajenos al sujeto | 85–135 mm, luz suave, catchlight, rim light | gran angular, que deforma el rostro |
| Producto / packshot | luz de estudio, fondo, materiales, reflejos | ambiente narrativo, efectos | mesa de bodegón, luz difusa, degradado sin costura, f/8–f/11 | poca profundidad de campo, que desenfoca el producto |
| Comida | textura, frescura, luz lateral, atrezo | efectos, saturación exagerada | luz de ventana, vapor sutil, superficie mate, cenital o 45° | luz frontal dura, que aplana la comida |
| Moda | pose, vestuario, tejido, luz de estudio | detalle del fondo | editorial, tejido con caída, plano entero, luz de recorte | describir la ropa sin describir el tejido |
| Paisaje | hora del día, capas de profundidad, clima | parámetros de estudio | hora dorada, hora azul, gran angular, f/11, hiperfocal | apertura amplia, que anula la nitidez del fondo |
| Arquitectura | perspectiva, líneas, luz natural, materiales | efectos, bokeh | líneas verticales corregidas, tilt-shift, 16–24 mm | plano holandés, que tuerce lo que debe estar recto |
| Mascotas | expresión, pelaje, altura de cámara | efectos | a la altura del animal, velocidad rápida, pelaje definido | velocidad lenta con animal en movimiento |
| Vehículos | reflejos, carrocería, entorno, hora | detalle interior si es exterior | luz envolvente, panning, superficie especular | luz dura, que rompe las curvas |
| Editorial / reportaje | contexto, momento, luz disponible | luz de estudio, retoque | luz natural disponible, documental, grano leve | esterilizar la escena hasta que parece publicidad |

## Familia ilustración y pintura

Ninguno admite el bloque **f**. Sí admiten materiales entendidos como medio (papel, grano, pincelada).

| Tipo | Bloques que pesan | Qué omitir | Vocabulario propio |
|---|---|---|---|
| Ilustración editorial | concepto, composición, paleta limitada | óptica, ISO | trazo, planos de color, síntesis, metáfora visual |
| Acuarela | soporte, sangrado, transparencias | nitidez, realismo | pigmento diluido, bordes húmedos, papel con grano, blancos reservados |
| Óleo | pincelada, empaste, luz | nitidez fotográfica | empaste, veladuras, claroscuro, lienzo |
| Pintura digital | luz, volumen, acabado | ISO, apertura | pinceles digitales, valores, luz ambiental |
| Lápiz / carboncillo | trazo, valor, soporte | color salvo que sea puntual | grafito, difuminado, línea de contorno, papel texturado |
| Concept art | diseño, función, escala, iteración | perfección de acabado | hoja de diseño, escala humana de referencia, silueta legible |

## Familia gráfica y geométrica

Ninguno admite **f**, ni bokeh, ni texturas fotorrealistas. La legibilidad manda sobre el detalle.

| Tipo | Bloques que pesan | Qué omitir | Vocabulario propio |
|---|---|---|---|
| Vector / flat | formas planas, paleta cerrada, legibilidad | luz, sombra realista, textura | color plano, contornos limpios, sin degradados, geometría simple |
| Low poly | facetas, paleta, silueta | textura fina, realismo | polígonos visibles, facetado, sombreado por cara |
| Isométrico | ángulo, modularidad, profundidad falsa | perspectiva cónica, punto de fuga | proyección isométrica, 30°, sin escorzo |
| Pixel art | rejilla, paleta limitada, resolución baja | `8k`, `ultra detailed`, antialiasing | rejilla visible, paleta de N colores, dithering, sprite |
| Iconografía | claridad a tamaño mínimo, grosor de trazo | escena, fondo, ambiente | trazo uniforme, esquinas redondeadas, rejilla, monocromo |
| Infografía / diagrama | jerarquía, orden de lectura, etiquetas | efectos, realismo | flujo, leyenda, agrupación, espacio para texto |

Para infografía e iconografía, el bloque **j (formato)** es tan importante como la escena: área segura, espacio para texto y tamaño mínimo de lectura.

## Infografía — cuándo proponerla

La infografía es el único tipo que conviene **ofrecer de oficio**. Cuando el paso 3 lee un artículo, un brief o un informe, evaluar si el contenido pide una infografía en lugar de una imagen ilustrativa, y proponerlo aunque el usuario no lo haya pedido. Si el usuario ya dijo qué tipo quiere, respetarlo y no insistir.

**Señales que la justifican** — el contenido tiene estructura que una imagen ilustrativa desperdiciaría:

| Señal en el contenido | Subtipo que pide |
|---|---|
| Pasos ordenados, un procedimiento, un antes y un después | diagrama de proceso o flujo |
| Dos o más opciones con atributos comparables | tabla o cuadro comparativo |
| Fechas, hitos, evolución en el tiempo | cronología |
| Cifras, porcentajes, proporciones, series | visualización de datos |
| Categorías que contienen subcategorías | jerarquía o taxonomía |
| Causa y efecto, dependencias entre partes | diagrama de relaciones |
| Distribución territorial | mapa temático |
| Partes de un objeto o sistema | despiece o diagrama anotado |

**Señales que no la justifican** — proponerla aquí solo produce una pieza vacía:

- Texto narrativo, opinión o testimonio sin estructura interna.
- Un dato suelto: no necesita infografía, necesita un número grande y bien compuesto.
- Contenido emocional o de marca, donde la fuerza está en la imagen y no en el orden.
- Menos de tres elementos que ordenar: una lista de dos cosas no es una infografía.

### La advertencia que hay que dar al proponerla

Una infografía vive de sus etiquetas, y **los modelos de imagen generan texto ilegible** en cuanto pasa de unas pocas palabras. Prometer una infografía completa generada de una sola pasada es prometer algo que no va a salir.

Al ofrecerla, decir cómo se va a producir realmente. Dos vías, en orden de fiabilidad:

1. **Componer, no generar.** Producir la infografía como pieza compuesta —HTML o vector— donde la tipografía es real, legible y respeta las fuentes de la marca. Un modelo de imagen puede aportar los iconos o una ilustración de apoyo, no la estructura.
2. **Base visual sin texto.** Generar con el modelo solo el fondo, la escena o los elementos gráficos, reservando el espacio de las etiquetas, y componer el texto encima después.

Nunca pedir al modelo una infografía con sus rótulos y esperar que sean legibles. Si el usuario insiste en generarla de una pasada, hacerlo con el mínimo texto posible y advertir que los rótulos habrá que rehacerlos.

### Al construir el prompt

Lo que importa en una infografía es el **orden de lectura**, no el detalle: por dónde entra el ojo, cómo avanza, dónde termina. Declarar la estructura (columnas, franjas, radial, línea temporal), la jerarquía entre niveles, la separación entre grupos y el espacio reservado para cada etiqueta. Paleta corta y funcional: el color debe distinguir categorías, no decorar.

## Familia 3D

| Tipo | Bloques que pesan | Qué omitir | Vocabulario propio |
|---|---|---|---|
| 3D realista | materiales, luz, oclusión | ISO, grano de película | PBR, oclusión ambiental, HDRI, subsurface scattering |
| Clay render | forma, luz suave, material único | color variado, realismo de materiales | arcilla mate, monocromo, luz de estudio suave, sin textura |
| Render arquitectónico | espacio, luz natural, materiales, escala | grano, efectos | luz de mediodía difusa, escala humana, materiales reales, exterior o interior |

El render arquitectónico admite vocabulario de lente (focal, corrección de verticales) aunque no sea fotografía: los motores lo replican.

## Familia estilizada

| Tipo | Bloques que pesan | Qué omitir | Vocabulario propio |
|---|---|---|---|
| Anime / manga | diseño de personaje, línea, cel shading | fotorrealismo, óptica | línea limpia, sombreado en dos tonos, ojos expresivos |
| Cómic | viñeta, entintado, contraste | realismo | entintado, tramas, alto contraste, dinamismo |
| Personaje | silueta, vestuario, pose, expresión | fondo complejo | hoja de personaje, pose neutra o de acción, fondo liso |

## Casos especiales

- **Imagen científica** — prioriza exactitud sobre belleza. Nombrar la estructura con precisión, evitar dramatismo lumínico, no añadir efectos. Advertir al usuario que el modelo puede inventar detalle anatómico o técnico plausible pero falso, y que no sirve como fuente.
- **Abstracto** — no hay sujeto. El peso cae en color, forma, ritmo, textura y composición. Los bloques de escena y parámetros no aplican.
- **Paisaje y naturaleza** — decidir si es fotográfico o ilustrado antes de nada; el vocabulario no se comparte.
