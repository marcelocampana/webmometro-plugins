# Destino de la pieza — Inferencia y variables que fija

Aplicar en el paso 4 del flujo. El destino condiciona el formato, el fondo, los márgenes y el espacio para texto; determinarlo antes de proponer composiciones evita rehacer la dirección creativa.

La regla de fondo: **inferir primero, preguntar solo si la inferencia falla**. Una pregunta que el workspace ya responde es una pregunta perdida.

## 1. Leer la ruta

Resolver la raíz del cliente subiendo desde el directorio activo hasta encontrar `contexto/`, y **recorrer todos los segmentos de la ruta**, no solo el primero. Un segmento reconocible resuelve aunque cuelgue de otras carpetas: `web/rrss/carruseles/pieza-x/` se lee igual que `carruseles/pieza-x/`.

Comparar por **segmento completo normalizado** — sin acentos, sin distinguir mayúsculas, admitiendo singular y plural. Comparar por segmento y no por subcadena evita falsos positivos como `mis-carruseles-viejos`.

| Segmento | Naturaleza | Qué aporta |
|---|---|---|
| `carrusel`, `carruseles` | dominio | pieza de carrusel para redes |
| `rrss`, `redes`, `social` | dominio | pieza de redes |
| `story`, `stories` | dominio | vertical completo 9:16 |
| `web` | dominio | web; afinar con `contenido` (artículo) o `seo` (analítico, improbable como destino) |
| `blog`, `articulos`, `posts` | dominio | artículo |
| `fondos` | rol | fondo — a sangre, con zona tranquila para el texto que irá encima |
| `logos`, `iconos` | rol | marca o icono — legible en tamaño mínimo, recortable |
| `portadas` | rol | portada o cabecera |
| `imagenes`, `fotos` | rol | imagen suelta, sin rol declarado |
| `productos` | rol | ficha de producto — fondo neutro, producto completo |
| `recursos`, `assets`, `_recursos-cliente` | contenedor | no resuelve por sí solo; seguir escaneando |
| `contexto`, `conocimiento` | — | no son destinos de pieza; seguir buscando señal |

### Componer dominio y rol

Los dos tipos de segmento informan cosas distintas y **se suman**:

- **Dominio** — fija formato, canal y contexto de publicación.
- **Rol** — fija qué es la pieza y cómo se trata.

`carruseles/pieza-x/recursos/fondos/` da las dos: un **fondo** (rol) para un **carrusel** (dominio), luego 1080×1350 a sangre, sin punto de interés en el centro y con una franja tranquila para el texto. Ninguna señal por separado llega ahí.

Cuando compitan dos segmentos de la **misma** naturaleza, gana el más profundo: está más cerca del directorio activo y es más específico sobre lo que se está haciendo.

## 2. Señales fuera de la ruta

Cuando la ruta no resuelve:

- **Archivos vecinos** — un `Brief.md` o un HTML con clases `.slide` en el directorio señalan carrusel; un `.md` con estructura de artículo señala contenido web; un `sistema-de-diseno/` cerca indica que hay identidad visual que consultar.
- **Delegación** — si otro skill invocó a este, su dominio es el destino sin más averiguación.
- **El uso que el usuario describe** aunque no nombre el canal: "va arriba del todo en la página" es un hero; "para acompañar el texto" es imagen de artículo.

## 3. Preguntar, si no queda otra

Una sola pregunta, con opciones cerradas y una salida por defecto:

> "¿Dónde se va a usar esta imagen?
> - Carrusel o post de redes
> - Cabecera o hero de una página web
> - Artículo de blog
> - Fondo, con texto encima
> - Otro (dime cuál)"

No preguntar el formato por separado: el destino ya lo determina.

## 4. Variables que fija cada destino

La relación de aspecto sale de la tabla de `modelos-destino.md`; aquí se fija todo lo demás.

| Destino | Fondo | Texto encima | Encuadre y márgenes |
|---|---|---|---|
| Carrusel de redes | a sangre, cubre el lienzo | sí, casi siempre | 1080×1350 por defecto; área segura ~7% horizontal y ~6% vertical; punto de interés fuera de esa franja |
| Story vertical | a sangre | sí | 9:16; los extremos superior e inferior los tapa la interfaz — nada importante ahí |
| Hero web | a sangre, ancho | sí, y suele ir a un lado | horizontal amplio; sujeto descentrado dejando un lado despejado; el recorte cambia mucho entre móvil y escritorio, así que nada crítico en los bordes |
| Artículo de blog | con fondo propio | no | horizontal; puede ser más narrativa y menos limpia, porque no compite con tipografía |
| Fondo | a sangre | sí, y es lo que manda | zona tranquila y de bajo contraste donde irá el texto; sin detalle fino que compita; nunca el punto de interés bajo la mancha de texto |
| Icono o avatar | recortable o plano | no | cuadrado; silueta legible a tamaño mínimo; sin detalle que desaparezca al reducir |
| Producto para ficha | neutro y uniforme | no | producto completo y centrado, sin recortes de encuadre; luz de estudio |
| Miniatura | con fondo | a veces | legibilidad a tamaño muy reducido; un solo foco, contraste alto |
| Banner | a sangre | sí | muy apaisado; el sujeto sobrevive a recortes laterales agresivos |

Si la identidad visual del cliente declara `Formatos habituales` o `Area segura`, esos valores mandan sobre esta tabla.

## 5. Tratamiento del fondo

Tres tratamientos posibles, y el destino elige:

- **A sangre** — la imagen cubre el lienzo entero. Carrusel, story, hero, fondo, banner.
- **Con fondo propio** — la imagen es un rectángulo con su propia escena. Artículo, miniatura.
- **Recortable** — el sujeto debe poder aislarse del fondo. Icono, logo, figura recortada de carrusel, producto que se compondrá sobre otro color.

### Cuando la pieza debe ser recortable

`carousel-design` distingue "figura recortada" (PNG con alfa) de "foto con fondo", y son modos compositivos incompatibles. Si el destino es una figura recortada, el prompt debe pedirlo — pero **nunca en negativo**: "sin fondo" es exactamente la formulación que la regla del skill prohíbe, y tiende a producir el fondo que niega.

Dos vías, según el modelo destino:

- **Si el modelo expone control de fondo o canal alfa**, pedirlo explícitamente. Después, verificar que el resultado sea transparencia real y no un damero gris dibujado dentro de la imagen, que es el fallo típico.
- **Si no lo expone**, redactar en positivo: *"el sujeto completo y aislado, sobre un fondo liso de color uniforme claramente contrastado con él"*. Y advertir al usuario de que el recorte se hace después con otra herramienta.

Elegir el color del fondo plano en función del sujeto, no por costumbre: un fondo blanco contra un producto blanco no se puede recortar limpiamente.
