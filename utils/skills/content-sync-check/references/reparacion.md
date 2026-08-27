# Modo 2 · Reparar

Aplica las diferencias encontradas. **Se entra solo si el usuario lo pide** (`--reparar`, «pásalo a
Design», «actualiza el sitio»), y siempre **después** de haber verificado: no se repara lo que no
se mostró antes.

**Si más de un lado cambió sobre el mismo bloque, esto no aplica**: ve a `reconciliacion.md`. Aquí
se repara cuando está claro qué versión gobierna; cuando no lo está, decidirlo es el trabajo previo.

**Nada se escribe sin visto bueno, y el visto bueno es por pieza.** Aprobar la corrección de una
página no autoriza las demás. Es deliberado: cada destino que se toca es contenido que alguien va a
leer, y en el canvas es lo que el cliente ve.

## Antes de reparar una ausencia: comprueba que falta de verdad

**Un texto que se movió de bloque no se repara: se duplica.** Si el hallazgo dice «falta en X»,
busca ese texto en el resto del destino antes de escribirlo. Si aparece en otro bloque, no era una
ausencia — era una reubicación (`comparacion.md`), y añadirlo lo deja dos veces en la página.

Vale también al revés: si vas a añadir un bloque entero, comprueba que su contenido no esté ya
repartido en otros. Reparar sin esa comprobación es el modo más fácil de empeorar una página.

## El protocolo, para cada corrección

1. **Muestra antes de escribir**: qué destino, qué archivo, qué campo o sección, **texto actual** y
   **texto propuesto**. Literales, sin parafrasear.
2. **Espera el visto bueno** de esa pieza.
3. **Escribe.**
4. **Relee y verifica** que quedó como debía. Sin este paso la reparación es una suposición.
5. **Dilo en una línea**: qué quedó aplicado y dónde.

Si una corrección afecta varias piezas, muéstralas agrupadas para que el usuario vea el alcance,
pero **pide confirmación pieza por pieza** al aplicar.

## Las tres direcciones que se propagan

### Fuente → sitio

La más simple: el archivo del sitio es del mismo formato que la fuente. Añade los campos que
faltan o corrige los que difieren, **respetando el esquema de la colección** (`content.config.ts`):
un campo que el esquema no declara hará fallar la validación del sitio.

Conserva lo que el destino tenga y la fuente no cuando sea propio del sitio (rutas de imagen ya
resueltas, por ejemplo). Si no está claro si un campo es propio del destino o quedó huérfano,
**pregunta**: no lo borres.

### Fuente → Claude Design

Se repara **la página** (el `.dc.html` de la raíz del proyecto) y nada más. **El material de
`uploads/` no se toca**: es contexto temporal que el usuario le pasó al chat, no contenido
publicado — reescribirlo no arregla nada y ensucia su espacio de trabajo.

Aquí está el cuidado: **se reescribe el archivo completo** —la API no acepta parches— así que hay
que leerlo, cambiar **solo el texto que corresponde** y devolver todo lo demás **byte a byte**:
estructura, clases, estilos inline, tokens del design system, scripts, comentarios de sección.

Si el texto vive en constantes del script (`const faqs = [...]`) y no en el marcado, se edita ahí,
respetando el escapado de comillas del original.

**Al reparar una página con variantes, aplica el cambio en las dos** —escritorio y móvil— salvo que
el bloque esté declarado como omitido a propósito en una de ellas (`dispositivos.md`). Corregir solo
escritorio deja móvil con la versión vieja, y móvil suele ser donde está la mayoría del tráfico.

**Nunca reescribas un `.dc.html` desde cero a partir de la fuente.** El diseño no está en la
fuente: está en ese HTML, y regenerarlo lo destruye. Si el cambio de texto obliga a tocar el
marcado (un bloque nuevo que no existe en el diseño), **detente y dilo**: eso es trabajo de diseño,
no de sincronización, y lo decide el usuario en el canvas.

Mecánica de escritura con `DesignSync`:

1. `get_file` para leer el archivo actual.
2. Prepara el contenido corregido en un archivo local (el scratchpad de la sesión).
3. `finalize_plan` con `writes` (las rutas exactas), `deletes` (obligatorio, aunque sea `[]`) y
   `localDir` (la carpeta desde donde se sube).
4. `write_files` con el `planId` devuelto.
5. `get_file` otra vez para verificar.

Solo se escriben las rutas declaradas en el plan: cualquier otra se rechaza. Es una salvaguarda,
no un obstáculo — declara exactamente lo que vas a tocar.

### Claude Design → fuente

Cuando el cambio se acordó sobre el diseño —una reunión con el cliente, una corrección aplicada
directamente en el canvas— y no volvió a la fuente. Se trae el texto al archivo fuente
respetando su formato: el frontmatter con las claves del esquema, la prosa en el cuerpo.

**Extraer texto de HTML pierde matices**: cursivas, enlaces, saltos deliberados. Muestra lo que vas
a escribir y **advierte de lo que se pudo perder** en la extracción. Si el bloque es largo o tiene
formato rico, di que conviene revisarlo a mano.

Tras aplicar, la fuente cambió: **ofrece actualizar `fecha_aprobacion`** — pero solo si el usuario
confirma que ese cambio está aprobado, no por el hecho de haberlo copiado.

## La dirección que no se propaga: sitio → fuente

Si el sitio tiene contenido que la fuente no, **no lo traigas automáticamente**. Repórtalo,
explica lo que implica —se editó el sitio saltándose la fuente, y el próximo despliegue desde la
fuente lo perdería— y ofrece dos salidas explícitas:

- **Traerlo a la fuente**, si el cambio es válido y debe conservarse (es una decisión del usuario,
  se aplica como cualquier otra reparación).
- **Revertirlo en el sitio**, si fue un cambio indebido.

Que la elección sea del usuario es el punto: propagar en silencio consagraría al sitio como fuente
de verdad, que es la práctica que este skill existe para corregir.

## Después de reparar

Vuelve a verificar lo reparado — no todo el mapeo, solo las piezas tocadas — y confirma que quedaron
al día. Si algo sigue divergiendo, dilo; no des por bueno un resultado que no comprobaste.

Si tras reparar el canvas el espejo local (`htmls/`) quedó desfasado respecto de lo que acabas de
escribir, **menciónalo**: el usuario querrá reexportar.

## Errores

| Situación | Qué hacer |
| --- | --- |
| `finalize_plan` rechaza una ruta | Revisa que esté declarada exactamente igual, incluidas tildes y mayúsculas del nombre. |
| `write_files` falla | No reintentes en bucle: di qué falló y con qué ruta. |
| Al releer, el archivo no quedó como se propuso | Dilo de inmediato, muestra la diferencia y **no vuelvas a escribir** sin instrucción. |
| El cambio exige tocar el marcado del diseño | Detente: es trabajo de diseño. Explica qué haría falta y devuélvelo al canvas. |
| El campo a añadir no existe en el esquema del sitio | No lo escribas: rompería la validación. Dilo y ofrece añadirlo al esquema como tarea aparte. |
| El usuario aprueba «todo» de una vez | Confirma el alcance en una línea (cuántas piezas, qué destinos) y ve pieza por pieza igualmente. |
| Tras escribir, el texto aparece dos veces en la página | Era una reubicación, no una ausencia. Dilo, revierte lo añadido y repórtalo como reubicación. |
