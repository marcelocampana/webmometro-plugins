# Redacción de tareas

Una tarea mal escrita se paga dos veces: al retomarla sin saber qué había que hacer, y al cerrarla sin
saber si se hizo.

## Anatomía

**Verbo + objeto concreto + ámbito.**

- *Verbo*: qué acción. `Corregir`, `Alinear`, `Convertir`, `Separar`, `Añadir`. No `revisar` ni
  `mejorar` a secas: no se puede declarar terminado.
- *Objeto concreto*: qué cosa, nombrada como se llama en el proyecto.
- *Ámbito*: dónde vive, entre paréntesis si hace falta. Es lo que decide el área y lo que evita
  abrir la tarea a ciegas.

## Antes y después

| Antes | Después |
| --- | --- |
| arreglar el menú | Corregir el desplegable del menú en móvil (`AppHeader.vue`) |
| revisar el registro | Alinear el diseño de `/registro` con la versión 2 del mockup |
| el tema está hardcodeado | Resolver el hardcodeo de `theme-mama` antes de añadir el segundo cluster |
| mejorar las tarjetas en móvil | Disponer verticalmente los componentes bajo «Contenido relacionado» en móvil |
| falta el índice | Convertir el índice móvil de los subtipos en un desplegable |
| separar estilos | Separar las reglas de prosa editorial de la clase de tema |

El patrón: el «después» dice **qué se verá distinto cuando esté hecho**. Ese es el test.

## La columna Tarea es una línea

El detalle —mockups, secciones afectadas, alcance, medidas— **va en el plan**, o en la descripción si es
una tarea del usuario en Toggl; de todos modos acaba en el historial al cerrarla. Una Tarea de tres líneas rompe la lectura de la tabla y duplica lo que el
cierre va a escribir igual.

Si el enunciado no cabe en una línea, casi siempre es porque:

- Lleva el **por qué** dentro. Va a la descripción.
- Lleva **dos tareas**. Se parte.

## Cuándo partir una tarea

**El plan ordena a Claude; Toggl, al usuario.** Un trabajo de Claude se parte solo si los trozos
tienen **distinta prioridad**, se harán en **momentos distintos**, o el usuario podría querer
**quedarse con uno** y dejar el otro. Lo que le toca al usuario va a «Esto te toca a ti» del plan,
no como trozo. Si no, es un solo trabajo y sus pasos viven en el plan (el del modo plan): siete
entradas para algo que Claude hace de corrido son siete cierres que nadie supervisa.

**Si el enunciado necesita una «y», probablemente son dos.** Propón partirla cuando:

- Los dos trozos se pueden cerrar por separado y en distinto momento.
- Tocan **áreas distintas** — entonces obligatoriamente son dos tareas.
- Uno está bloqueado y el otro no: mantenerlos juntos bloquea trabajo que podría avanzar.

**No la partas** si los trozos son inseparables en la práctica —un cambio que solo tiene sentido
completo— o si son pasos de la misma ejecución. El historial de tareas cerradas muestra que una tarea
puede cerrar trabajo en varias páginas a la vez y seguir siendo **una** tarea: lo que la define es
dónde vive el cambio, no cuántas cosas mejora.

## El ámbito decide el área

- El cambio vive en **una** área → esa área.
- El cambio vive en **código o contenido compartido** → el área de lo compartido, **una sola tarea**.
  Nunca una por consumidor: duplicarla cuenta su intervalo dos veces.
- El cambio es de configuración, despliegue o transversal → `General`.

Cuando dudes entre dos secciones, la pregunta útil es: **¿dónde lo buscaría dentro de un mes?**

## Observaciones que vale la pena hacer antes de crear

En una línea, y solo si aporta:

- «Ya está en la bandeja (`por-revisar.md`)» o «ya se delegó a Claude» — evita el duplicado.
- «Toca `AppHeader.vue`, afecta a todo el sitio → área General» — corrige el área.
- «Depende de la tarea 2, que está `Bloqueada`» — evita abrir algo que no avanzará.
- «El historial dice que se intentó y se descartó por X» — evita repetir.
- «Son dos: el estilo y el contenido. ¿Las separo?» — evita una tarea que no se puede cerrar.

Si no hay nada de esto, **no inventes una observación**. Propón la tarea y calla.

## Cuando el usuario rechaza tu redacción

**Se usa la suya, sin insistir.** Propones una vez. La lista es del usuario y un enunciado que él
reconoce vale más que uno técnicamente mejor que le resulta ajeno.
