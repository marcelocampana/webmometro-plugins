# Modo 4 · Ingesta (`--ingerir`)

Convertir en tareas lo que **ya existe**: una conversación donde se diagnosticó algo, o un archivo
producido por otro skill (una auditoría SEO, un análisis UX).

Cada tarea propuesta se afina con `redaccion-tareas.md` y se ancla en la fuente; el contexto del
proyecto sale de `contextualizacion.md`.

**Regla única de destino: todo entra por la bandeja** (`tareas/por-revisar.md`, formato en
`modo-revisar.md`). Nada de una fuente externa aterriza en Toggl ni en `para-claude.md` sin pasar por
la bandeja y una revisión del usuario. Y como siempre: **se propone
y se espera**, nunca se escribe directo.

## Fuente A · La conversación

`--ingerir` sin argumento: recorre **la conversación previa a la invocación**. Hay que buscar tres
cosas distintas, porque no se parecen entre sí:

| Fuente | Qué buscar |
| --- | --- |
| Lo que el usuario pidió y no se hizo | «habría que…», «esto hay que arreglarlo», algo aplazado |
| **Lo que la IA propuso antes** | recomendaciones, alternativas descartadas por tiempo, «convendría también…» |
| Lo que el trabajo destapó | un fallo encontrado depurando, una deuda que salió al leer código, un efecto colateral |

La tercera es la que más rinde **y la que siempre se pierde**: el hallazgo de una sesión de depuración
no está escrito en ningún sitio cuando la sesión termina. La segunda se olvida por otro motivo: la IA
tiende a mirar solo lo que el usuario dijo.

El origen —que va en la descripción, después del área— se rellena con el tema y la fecha de la conversación, no con «conversación» a secas.

## Fuente B · Un archivo

`--ingerir <ruta>`, o cuando el usuario pasa un archivo pidiendo que se añadan sus tareas. Cinco pasos:

1. **Leer el archivo entero** antes de proponer nada. Nunca ingerir lo que no se ha leído.
2. **Detectar su forma** y mapearla (tabla de abajo).
3. **Extraer solo lo accionable.** Es el paso que decide la calidad: un informe trae diagnóstico, datos
   y recomendaciones, y **solo las recomendaciones son tareas**. «El LCP es de 4,2 s» es un dato;
   «comprimir las imágenes del hero» es una tarea.
4. **Afinar y deduplicar** (abajo).
5. **Proponer en una tabla compacta** y esperar. El origen = ruta del archivo y su fecha, para poder
   rastrear de qué informe salió cada fila.

### Mapeo por forma del archivo

| Forma | Cómo se lee |
| --- | --- |
| **Tabla Markdown** | Una fila por tarea. La columna que describe la acción → `Tarea`; severidad, prioridad o impacto → el motivo, en la descripción |
| **Lista de viñetas** | Un ítem por tarea; si un ítem tiene subítems, suelen ser el detalle → la descripción |
| **Encabezados por hallazgo** (`### …`) | El encabezado → `Tarea`; su primer párrafo, condensado → la descripción |
| **Prosa corrida** | Extrae solo las frases imperativas o recomendatorias. Si no hay ninguna clara, **dilo** en vez de inventar tareas |

**Las severidades y prioridades ajenas se conservan como texto en la descripción** («severidad alta según el
informe»). No se traducen a estados ni a la prioridad de Toggl: son criterios de otro sistema y
mezclarlos falsearía la prioridad, que la decide el usuario.

### Deduplicar contra cinco fuentes

Antes de proponer, descarta lo que ya esté en: lo **pendiente** del proyecto en Toggl
(`cola.py leer --vista pendientes --proyecto <ID>`), `por-revisar.md` y `para-claude.md`, **el
historial** (algo ya resuelto no vuelve) y `auditoria.md`.
Si un ítem es una variante de algo existente, dilo en una línea en vez de crear un duplicado.

## Qué NO hace la ingesta

- **No ejecuta** ninguna tarea.
- **No prioriza** ni saca nada de la bandeja.
- **No reinterpreta** el informe de origen: si una recomendación es ambigua, la propone marcada como
  tal en vez de inventarle alcance.
- **No copia el informe.** Solo sus tareas; el archivo sigue siendo la fuente y se referencia por ruta.

## Disponible en cualquier modo

No hace falta la flag: si el usuario pasa un archivo de tareas mientras hace otra cosa, **ofrece
ingerirlo** en una línea. El destino sigue siendo la bandeja.

## Errores

| Situación | Qué hacer |
| --- | --- |
| El archivo no existe o no se puede leer | Dilo y para. No adivines su contenido. |
| No contiene nada accionable | Dilo en una línea: «son datos, no recomendaciones». No fuerces tareas. |
| Trae decenas de ítems | Propón los que pasen el filtro y di cuántos descartaste y por qué. No los escribas todos por volumen. |
| El usuario pide que vayan directo a la cola | Es su lista: se acepta y se crean en Toggl (`tarea`), pero se dice que lo normal es revisarlas desde la bandeja. |
| La conversación no tiene material | Dilo. Una ingesta vacía es un resultado válido. |
