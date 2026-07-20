# Consistencia — Tabla de incompatibilidades y checklist de cierre

Aplicar en el paso 8, siempre, antes de entregar. Este pase es silencioso: no se reporta al usuario salvo que obligue a preguntar.

## 1. Incompatibilidades duras

Cada fila es una combinación que el modelo no puede satisfacer. Si aparecen las dos, elegir una y eliminar la otra.

| Instrucción | Incompatible con | Por qué |
|---|---|---|
| `f/1.4`, `f/1.8`, bokeh marcado | `todo en foco`, `nitidez de extremo a extremo` | la apertura determina la profundidad de campo |
| ISO alto, `ISO 3200` | `sin ruido`, `imagen limpia` | el ruido es consecuencia física de la sensibilidad |
| `1/1000 s`, `congela el movimiento` | `motion blur`, `barrido`, `estela` | la velocidad alta elimina la estela |
| `larga exposición`, `agua sedosa` | `gotas congeladas`, `instante detenido` | son tratamientos opuestos del tiempo |
| Gran angular `16 mm`, `24 mm` | `compresión del fondo`, `fondo aplastado` | la compresión es propiedad de la focal larga |
| Teleobjetivo `200 mm` | `perspectiva envolvente`, `mucho contexto` | la focal larga recorta y aísla |
| `contraluz`, `silueta` | `rostro plenamente iluminado con detalle` | la luz viene de detrás; requiere relleno explícito |
| `hora dorada`, `luz cálida rasante` | `mediodía`, `sombras cenitales duras` | son momentos lumínicos excluyentes |
| `cenital`, `vista desde arriba` | `horizonte visible`, `línea de cielo` | geometría imposible |
| `contrapicado` | `vista de pájaro`, `plano cenital` | direcciones opuestas de cámara |
| `vector plano`, `flat design` | `bokeh`, `profundidad de campo`, `textura de piel realista`, `oclusión ambiental` | el medio no tiene óptica ni simulación física |
| `pixel art` | `ultra detailed`, `8k`, `hiperrealista`, `antialiasing` | el medio se define por su límite de resolución |
| `clay render`, `arcilla mate` | `materiales fotorrealistas`, `reflejos especulares`, `color variado` | el material es único y mate por definición |
| `minimalista`, `espacio negativo amplio` | inventario largo de objetos, `escena abarrotada` | densidades opuestas |
| `blanco y negro`, `monocromo` | paleta cromática, `colores cálidos`, acento de color | excluyentes salvo que se pida color selectivo explícito |
| `simetría perfecta`, `composición centrada` | `regla de tercios`, `sujeto descentrado` | dos reglas compositivas opuestas |
| `isométrico`, `sin punto de fuga` | `perspectiva cónica`, `punto de fuga` | proyecciones incompatibles |
| `fotorrealista` | `ilustración`, `pintura`, `cel shading` | medios opuestos |
| Fondo `desenfocado` | fondo descrito con detalle fino | lo que se desenfoca no se lee |
| `luz suave difusa` | `sombras duras y marcadas` | la calidad de la luz define la sombra |
| `nublado`, `luz plana` | `sombras largas`, `contraste alto` | la difusión elimina la sombra direccional |

## 2. Redundancias que restan

No son contradicciones, pero diluyen. Dejar una sola formulación:

- `ultra detailed` + `extremely detailed` + `fine details` + `intricate` → uno.
- `high resolution` + `8k` + `high quality` + `professional quality` → uno, y solo si el tipo lo justifica.
- `beautiful` + `stunning` + `gorgeous` + `masterpiece` → ninguno: no dirigen nada.
- `sharp focus` cuando ya se declaró el punto de enfoque y la apertura → sobra.
- Repetir la paleta en el bloque de color y otra vez en el de ambiente → una vez.
- `realistic lighting` cuando ya se describió hora, dirección y calidad de la luz → sobra.

## 3. Vaguedad a resolver

Si alguno de estos términos sobrevive al borrador, sustituirlo por su versión concreta:

| Vago | Resolver como |
|---|---|
| moderno | rasgos concretos: paleta, geometría, materiales de época |
| bonito, impactante, increíble | eliminar; no dirigen |
| profesional | el atributo real: luz controlada, encuadre limpio, color corregido |
| buena iluminación | dirección + calidad + hora |
| colores agradables | la paleta nombrada |
| alta calidad | el atributo del tipo, o nada |
| gente, personas | quiénes: edad aproximada, número, actitud |
| algo de naturaleza | qué vegetación, en qué estado, en qué plano |

## 4. Checklist de cierre

Verificar antes de entregar:

- [ ] El sujeto y la acción están en la primera frase del prompt.
- [ ] Ninguna fila de la tabla de incompatibilidades aplica.
- [ ] Ningún concepto aparece dos veces con distintas palabras.
- [ ] Ningún atributo genérico que el tipo de imagen no justifique.
- [ ] Ningún término de la tabla de vaguedad sin resolver.
- [ ] Los bloques que no aplican al tipo están **ausentes**, no negados.
- [ ] El prompt corresponde a la dirección creativa que el usuario eligió en el paso 6.
- [ ] Cada elemento de contexto se puede justificar en una frase, y no hay más de dos.
- [ ] Si hay parámetros fotográficos, son coherentes entre sí (apertura, ISO, velocidad, focal).
- [ ] La paleta respeta la identidad visual, o se declara que se generó sin marca.
- [ ] Se cumplen las restricciones sobre personas, IA, legales y médicas.
- [ ] Ningún estilo prohibido por la marca aparece, ni en el prompt ni en las variantes.
- [ ] No se pide imitar a un artista vivo ni a un estudio en activo.
- [ ] El formato y la relación de aspecto corresponden al destino determinado en el paso 4.
- [ ] El tratamiento del fondo corresponde al destino: a sangre, con fondo propio o recortable.
- [ ] Si la pieza debe ser recortable, se pidió en positivo — fondo liso y contrastado — nunca "sin fondo".
- [ ] Si la pieza lleva texto encima, hay espacio negativo reservado para él.
- [ ] Si el contexto justificaba una infografía, se ofreció; y si es infografía, se declaró cómo se produce el texto.

## 5. Texto dentro de la imagen

Cuando el usuario pida un rótulo, titular o palabra legible dentro de la imagen:

- Declararlo **entre comillas** y en la cantidad mínima: una línea corta, no un párrafo.
- Ponerlo pronto en el prompt, no al final.
- Advertir al usuario que la fidelidad tipográfica varía mucho entre modelos y que el texto largo se degrada en caracteres inventados.
- Recomendar la alternativa fiable: generar la imagen **sin** texto, reservando espacio negativo, y componer la tipografía después con la fuente de la marca. Es además la única forma de respetar los roles tipográficos de la identidad visual.

## 6. Cuándo la verificación obliga a preguntar

El pase es silencioso salvo en dos casos, donde hay que detenerse y consultar:

1. **La contradicción viene del usuario**, no del borrador — pidió explícitamente las dos cosas incompatibles. Presentar las dos opciones y dejar que elija.
2. **La instrucción del usuario choca con una restricción de marca** — de personas, IA, legal o médica. Declarar el choque y preguntar cuál prevalece. Nunca resolverlo en silencio a favor de ninguna de las dos.
