# Contextualización: qué leer, en qué orden, qué retener

## El principio

**Ninguna tarea se crea, modifica o describe sin contexto del proyecto** —venga de la IA o dictada
por el usuario—. **Se contextualiza una vez por sesión y se reutiliza**; después, solo se relee lo
que se va a tocar.

## Qué leer, en orden

1. **`CLAUDE.md` y los docs que señale.** Qué es el proyecto, sus convenciones, su deuda declarada y
   sus trampas conocidas.
2. **`tareas/toggl.md`**: el proyecto de Toggl, las áreas y las reglas propias del repo.
3. **Lo pendiente del proyecto:** `cola.py leer --vista pendientes --proyecto <ID>` (nombre, área y
   primera línea de cada tarea; la bandeja va marcada `#por-revisar`). Nunca `tasks list` crudo.
4. **El historial reciente:** la zona `## Tareas archivadas` del mensual en curso y del anterior, y
   de ahí **solo el comentario** (por su ancla, `historial-lectura.md`) de lo que toque el mismo
   ámbito que la tarea nueva.
5. **La tarea en curso** y su rama (`git branch --show-current`), y **`git log` reciente** (10–20).
6. **La conversación en marcha**: lo que se acaba de descubrir depurando es materia prima de tareas
   y no está escrito en ningún sitio todavía.

## El historial es la parte que más rinde

Sus comentarios guardan la trampa que costó dos horas, el efecto colateral que no era obvio y la
decisión que alguien ya tomó. Usarlos evita **proponer algo ya resuelto**, **proponer algo que ya se
intentó y se descartó** y **repetir una trampa conocida**. También sirve para estimar
(`estimacion.md`).

## Anclar: la regla que separa una sugerencia de una ocurrencia

**Toda tarea propuesta se ancla en algo verificable.** Sin ancla, no se propone.

| Ancla | Ejemplo |
| --- | --- |
| Un archivo o línea | `AppHeader.vue:42` no maneja el caso de menú vacío |
| Deuda declarada en los docs | `CLAUDE.md` lista tres hardcodeos a resolver antes de escalar |
| Un hallazgo de la conversación | «esto reventó al probar en móvil» dicho hace dos mensajes |
| Un patrón del historial | dos tareas cerradas tocaron el mismo componente por el mismo motivo |
| Salida de un comando | un `grep` que encuentra el marcador, un build que avisa |

No son ancla: «suele ser buena práctica», «convendría revisar» sin decir qué.

**El protocolo: propone y espera**, también para lo que dicta el usuario: si el enunciado se puede
afinar, propónlo afinado y di qué cambió. Excepción de forma: un hallazgo lateral detectado
**mientras trabajas en otra tarea** se propone para la bandeja **en una línea y sigues**.

## Cuándo se relee

Si el usuario dice que editó tareas a mano en Toggl (`cola.py leer --refrescar`), si se cambió de
rama o se hizo un merge, o antes de una auditoría.

## Qué retener

Qué es el proyecto y qué **no** hay que hacer en él; sus áreas; qué hay en curso o bloqueado y por
qué; qué se cerró hace poco y qué dejó pendiente. **Lo que se retiene se usa, no se narra.**
