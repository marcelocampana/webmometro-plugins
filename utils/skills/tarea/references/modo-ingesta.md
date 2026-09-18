# Modo 4 · Ingesta (`--ingerir`)

Convertir en tareas lo que **ya existe**: una conversación donde se diagnosticó algo, o un archivo
producido por otro skill (una auditoría SEO, un análisis UX).

Cada tarea propuesta se afina con `redaccion-tareas.md` y se ancla en la fuente; el contexto del
proyecto sale de `contextualizacion.md`.

**Regla única de destino: todo entra por `revisar.md`.** Nada de una fuente externa aterriza en la cola
de prioridad sin pasar por la bandeja y un ascenso explícito del usuario. Y como siempre: **se propone
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

`Origen` se rellena con el tema y la fecha de la conversación, no con «conversación» a secas.

## Fuente B · Un archivo

`--ingerir <ruta>`, o cuando el usuario pasa un archivo pidiendo que se añadan sus tareas. Cinco pasos:

1. **Leer el archivo entero** antes de proponer nada. Nunca ingerir lo que no se ha leído.
2. **Detectar su forma** y mapearla (tabla de abajo).
3. **Extraer solo lo accionable.** Es el paso que decide la calidad: un informe trae diagnóstico, datos
   y recomendaciones, y **solo las recomendaciones son tareas**. «El LCP es de 4,2 s» es un dato;
   «comprimir las imágenes del hero» es una tarea.
4. **Afinar y deduplicar** (abajo).
5. **Proponer en una tabla compacta** y esperar. `Origen` = ruta del archivo y su fecha, para poder
   rastrear de qué informe salió cada fila.

### Mapeo por forma del archivo

| Forma | Cómo se lee |
| --- | --- |
| **Tabla Markdown** | Una fila por tarea. La columna que describe la acción → `Tarea`; severidad, prioridad o impacto → `Motivo` |
| **Lista de viñetas** | Un ítem por tarea; si un ítem tiene subítems, suelen ser el detalle → `Motivo` |
| **Encabezados por hallazgo** (`### …`) | El encabezado → `Tarea`; su primer párrafo, condensado → `Motivo` |
| **Prosa corrida** | Extrae solo las frases imperativas o recomendatorias. Si no hay ninguna clara, **dilo** en vez de inventar tareas |

**Las severidades y prioridades ajenas se conservan como texto en `Motivo`** («severidad alta según el
informe»). No se traducen a los cinco estados ni a la cola `## Ahora`: son criterios de otro sistema y
mezclarlos falsearía la prioridad, que la decide el usuario.

### Deduplicar contra cuatro fuentes

Antes de proponer, descarta lo que ya esté en: `tareas.md` **abiertas**, `tareas.md`
**`✅ Completada`** (el historial cuenta: algo ya resuelto no vuelve), `revisar.md` y `auditoria.md`.
Si un ítem es una variante de algo existente, dilo en una línea en vez de crear un duplicado.

## Qué NO hace la ingesta

- **No ejecuta** ninguna tarea.
- **No prioriza** ni sube nada a `## Ahora`.
- **No reinterpreta** el informe de origen: si una recomendación es ambigua, la propone marcada como
  tal en vez de inventarle alcance.
- **No copia el informe.** Solo sus tareas; el archivo sigue siendo la fuente y se referencia por ruta.

## Disponible en cualquier modo

No hace falta la flag: si el usuario pasa un archivo de tareas mientras hace otra cosa, **ofrece
ingerirlo** en una línea. El destino sigue siendo `revisar.md`.

## Errores

| Situación | Qué hacer |
| --- | --- |
| El archivo no existe o no se puede leer | Dilo y para. No adivines su contenido. |
| No contiene nada accionable | Dilo en una línea: «son datos, no recomendaciones». No fuerces tareas. |
| Trae decenas de ítems | Propón los que pasen el filtro y di cuántos descartaste y por qué. No los escribas todos por volumen. |
| El usuario pide que vayan directo a `tareas.md` | Es su lista: se acepta, pero se dice que lo normal es ascender desde la bandeja. |
| La conversación no tiene material | Dilo. Una ingesta vacía es un resultado válido. |
