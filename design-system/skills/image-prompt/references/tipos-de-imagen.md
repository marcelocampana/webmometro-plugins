# Tipos de imagen — Taxonomía y perfil de bloques

Esta referencia gobierna el paso 2 del flujo. El tipo determina qué bloques del paso 6 aplican, qué vocabulario usar y cuánto detalle es útil.

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
