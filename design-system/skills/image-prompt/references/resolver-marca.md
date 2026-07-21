# Identidad visual y contexto externo — Resolución, creación e ingesta

Esta referencia cubre el paso 1 (resolver la marca, bloqueante) y el paso 3 (contexto externo) del flujo.

Regla de fondo: la verdad compartida vive una sola vez en el workspace del cliente y se lee por referencia. Este skill **no duplica** guías de marca ni sistemas de diseño existentes.

## 1. Resolver la raíz del cliente

Este skill opera en el **proyecto activo del cliente** (su vault o repo), no en el repo del plugin. Resolver la raíz del cliente subiendo desde el directorio activo hasta encontrar una carpeta `contexto/` — igual que el resto de la suite.

No usar una ruta relativa al directorio de trabajo del agente: en Cowork el agente corre desde una caché de plugin, no desde el proyecto del usuario.

Si no aparece ninguna carpeta `contexto/` al subir, no hay workspace de cliente. Ir directo al paso 3 de esta referencia (creación) con la pregunta de las cuatro salidas — con una diferencia: **sin workspace, la identidad construida vive solo en la sesión**. Se usa para el prompt y, al terminar, se ofrece guardarla si el usuario indica una carpeta. Nunca escribir en el directorio de trabajo del agente: es una caché de plugin, no el proyecto del usuario.

## 2. Las dos fuentes de marca

Viven ambas en `contexto/marca/` y tienen roles distintos. Ninguna sustituye a la otra.

| Archivo | Qué aporta | Si falta |
|---|---|---|
| `identidad-visual-imagenes.md` | paleta, estilo fotográfico, iconografía, restricciones sobre personas e IA, legales y médicas | **bloquea** — ver sección 3 |
| `brand-voice-guidelines.md` | arquetipo, valores, formalidad y energía, terminología prohibida | se anota y se sigue |

### Resolver la voz de marca por puntero

El archivo de voz de marca tiene un hogar canónico, pero el puntero puede apuntar a otro sitio. Resolver en este orden:

1. El campo `Archivo de guías:` en la sección **Voz de Marca** de `contexto/sitio.md`, si está declarado.
2. `contexto/marca/brand-voice-guidelines.md` — hogar canónico compartido, producido por brand-voice-pro.
3. La sección **Voz de Marca** de `contexto/sitio.md`, como fuente mínima.
4. Ubicaciones legacy toleradas: `.claude/brand-voice-pro-guidelines.md`, `.claude/brand-voice-guidelines.md`, `web/contenido/*/brand-voice/brand-voice-guidelines.md`.

Ignorar los archivos con fecha (`brand-voice-guidelines-YYYY-MM-DD.md`): son histórico archivado, no el vigente.

Si no se encuentra ninguno, seguir y anotar en la entrega que el prompt no aplicó restricciones de voz de marca.

### Traducir la voz de marca a decisiones visuales

El archivo de voz es verbal: no contiene un solo color. Lo aprovechable es semántico, y se traduce así:

| Insumo verbal | Decisión visual que informa |
|---|---|
| Arquetipo de marca | estilo dominante y registro de la escena (cercano vs. aspiracional, humano vs. abstracto) |
| `We Are / We Are Not` | pares visuales: cálido/frío, aireado/denso, orgánico/geométrico |
| Formalidad | simetría y orden compositivo; formal → composición centrada y estable |
| Energía | saturación y contraste; alta energía → color saturado, contraste marcado |
| Profundidad técnica | densidad de detalle y presencia de elementos explicativos |
| Terminología prohibida | palabras que no deben aparecer en texto dentro de la imagen |

Estas traducciones son inferencias, no datos. Cuando la identidad visual diga otra cosa, manda la identidad visual.

## 3. Crear `identidad-visual-imagenes.md` cuando falta

El bloqueo del paso 1 ofrece cuatro salidas. Tres construyen el archivo; la cuarta lo omite.

**Ruta A — el usuario entrega un documento guía.** Puede ser PPTX, PDF, imagen de referencia, manual de identidad o URL. Para PPTX existe `../../carousel-design/scripts/extract_pptx_guide.py`. Para URL, WebFetch. Extraer, volcar en la plantilla de la sección 4 y guardar en `contexto/marca/identidad-visual-imagenes.md` — solo si hay workspace; sin él, mantenerla en la sesión (ver sección 1).

**Ruta B — desde cero.** Preguntar los cuatro puntos **en un solo mensaje** — es la misma información y cuesta un turno en vez de cuatro:

> "Para armar la identidad visual necesito cuatro cosas:
> 1. ¿Qué colores usa la marca? Dame los hex si los tienes, o descríbelos y los aproximo.
> 2. ¿Cómo son sus imágenes? Por ejemplo: fotografía documental o de estudio, ilustración plana, 3D; con personas o sin ellas.
> 3. ¿Hay restricciones sobre imágenes generadas con IA, sobre mostrar personas, o claims legales o médicos que respetar?
> 4. ¿En qué formatos se publicará normalmente? Vertical de redes, horizontal web, cuadrado, impresión."

Si responde solo algunas, trabajar con lo respondido e inferir el resto declarándolo; no perseguir las que faltan. Si responde "no" a las restricciones, continuar sin insistir.

**Ruta C — mixta.** Combinar A y B según lo que falte.

**Ruta D — sin marca.** No crear archivo. Registrar la elección para no volver a preguntar en la sesión, generar con criterio de dirección de arte y declararlo en la entrega.

Si ya existe un sistema de diseño documentado del cliente en el proyecto, leerlo en lugar de preguntar lo que ya responde, y completar por entrevista solo los huecos.

Al cerrar cualquier ruta, resumir en máximo 6 bullets y avanzar.

## 4. Plantilla de `identidad-visual-imagenes.md`

Los nombres de campo replican los del sistema de diseño de cliente ya usado en este plugin, para que ambos sean interoperables. Omitir los campos sin dato en lugar de dejar marcadores vacíos.

```markdown
# Identidad Visual — Imágenes · [Cliente]

## Sistema Visual

- Paleta:
- Temperatura dominante:
- Tipografias:
- Logo y uso:
- Estilo de imagen:
- Estilo de iconografia:
- Nivel de realismo esperado:
- Tratamiento de datos/graficos:
- Area segura:

## Imagenes

- Fuentes permitidas: cliente, banco de imagenes, IA, ilustracion, iconografia
- Bancos autorizados:
- Estilo de fotografia/personajes:
- Restricciones sobre personas:
- Restricciones sobre IA:
- Criterios de seleccion:

## Restricciones

- Legales:
- Medicas:
- Politicas:
- Accesibilidad:
- Estilos prohibidos:
- Aprobacion interna:

## Formatos

- Formatos habituales:
- Espacio reservado para texto o logo:
```

Los campos que más pesan en un prompt de imagen son `Paleta`, `Estilo de imagen`, `Estilo de fotografia/personajes`, `Nivel de realismo esperado`, `Restricciones sobre personas`, `Restricciones sobre IA` y `Estilos prohibidos`. Si una ruta de creación se queda corta de tiempo o de datos, priorizar esos.

## 5. Restricciones que no se negocian

Cuando la identidad visual declare alguna de estas, se aplican aunque el usuario pida lo contrario en la conversación; el choque se declara y se pregunta, no se resuelve en silencio:

- **Restricciones sobre IA** — si la marca prohíbe imágenes generadas con IA para uso público, decirlo antes de entregar el prompt y confirmar que el uso es interno o exploratorio.
- **Restricciones sobre personas** — consentimiento, representación de pacientes, menores, grupos vulnerables.
- **Legales y médicas** — claims que la imagen no puede insinuar visualmente (resultados garantizados, antes/después, eficacia).
- **Estilos prohibidos** — si la marca excluye un estilo, no proponerlo ni siquiera como variante.

**Excepción única: infografía y texto sobre imágenes.** Si la identidad visual prohíbe texto sobre imágenes y el usuario pide una infografía, la restricción **no aplica**: una infografía exige texto por definición, y aplicar la regla haría la pieza imposible. En ese caso manda este skill sobre la regla del cliente. Anotar en la entrega que se aplicó la excepción. (La misma excepción está declarada en `tipos-de-imagen.md` (§ Infografía — cuándo proponerla); mantener ambas sincronizadas.)

## 6. Ingesta de contexto externo

Fuentes admitidas: URLs, documentación técnica, briefs creativos, PDFs, Word, presentaciones, archivos de texto, imágenes de referencia y diseños existentes.

Qué extraer de cada una:

- **Brief creativo** — objetivo de la pieza, audiencia, mensaje, tono, uso final y formato.
- **Documentación técnica o de producto** — qué es el objeto exactamente, materiales, acabados, proporciones. Es lo que evita inventar un producto que no existe.
- **URL de sitio o campaña** — lenguaje visual vigente, paleta en uso, tratamiento fotográfico.
- **Imagen de referencia** — describir sus rasgos observables (encuadre, luz, paleta, textura) y trasladarlos; no citar al autor ni pedir imitar a un artista vivo.

Reglas de ingesta:

- **Interpretar, no copiar.** El prompt final integra lo pertinente; no arrastra fragmentos literales ni información que no afecte a la imagen.
- **Solo lo que aporta.** Un brief de 20 páginas puede aportar tres decisiones; el resto no entra.
- **Declarar lo inferido.** Lo que se dedujo de una fuente, no lo que decía explícitamente, se menciona en las decisiones de la entrega.
