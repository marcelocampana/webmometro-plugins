# Los estados

Cinco, y no hay más: si una situación no cabe en uno de estos, va en la Nota o en Comentarios, **no en
un estado nuevo**. Cuatro son **abiertos** —la tarea sigue viva y va arriba en su sección— y uno es
cerrado.

| Estado | Qué significa | Se entra cuando | Se sale cuando | En `## Ahora` |
| --- | --- | --- | --- | --- |
| `Pendiente` | Anotada y sin empezar. No tiene rama ni Inicio. | Se anota la tarea en la sección de su área. | Se crea su rama → `🔵 En curso`. | Solo si el usuario la priorizó; puede estar priorizada sin haber empezado. |
| `🔵 En curso` | Es la tarea que se está trabajando. **Lleva punto azul**: es la única fila activa, y el punto la encuentra sin leer. | Se crea la rama y se anota el Inicio. | Se cierra → `✅ Completada`, o se interrumpe → `Pausada` / `Bloqueada`. | Sí, y **es la única que puede estarlo**: una tarea a la vez. |
| `Pausada` | Empezada y detenida **por tiempo**. Se puede retomar cuando haya rato. | El usuario para sin cerrarla. | Se retoma → `🔵 En curso`, o se cierra → `✅ Completada`. | Sí; conviene una Nota de dónde quedó el trabajo, pero no es obligatoria. |
| `Bloqueada` | Detenida **por una dependencia**: falta una validación, un dato, una decisión u otra tarea. No avanza aunque haya tiempo. | Se descubre lo que falta. | Se resuelve la dependencia → `🔵 En curso` o `Pendiente`. | Sí, con Nota de **qué falta para desbloquear** — sin eso la fila no informa. |
| `✅ Completada` | Cerrada: commit hecho y fila rellena. **Es el único estado con tick**, para que el historial se distinga de lo abierto de un vistazo. | Las tres confirmaciones de cierre. | Nunca. Es terminal. | No: su fila se borra de `## Ahora` al cerrar. |

## Lo que hay que saber, aparte de la tabla

- **`Pendiente` y `En curso` se distinguen por el Inicio, no solo por la etiqueta.** Una `En curso`
  sin Inicio, o una `Pendiente` con Inicio, es un error de registro: el Inicio es la creación de la
  rama, y las dos cosas se anotan en el mismo momento.
- **`Pausada` y `Bloqueada` no son lo mismo y no se usan indistintamente.** La diferencia decide qué
  se trabaja: una pausada se retoma en cuanto haya rato; una bloqueada **no se toma aunque sea la
  primera fila de `## Ahora`** — se avisa y se propone la siguiente no bloqueada, y saltarla o bajarla
  lo decide el usuario.
- **Un tramo `Bloqueada` que dure días se descuenta de la Duración**, igual que una noche. Si no, una
  tarea de dos horas que esperó una semana registra ~170h y ese número no informa de nada.
- **`Bloqueada` sin Nota no vale.** Es el único estado con Nota **obligatoria**: una fila bloqueada
  que no dice qué falta obliga a reconstruirlo, que es justo lo que el registro debía evitar. En
  `Pausada` la Nota es recomendable —dónde quedó el trabajo— pero no impide dejar la tarea así.
- **La Nota solo existe en `## Ahora`.** Si la tarea se bloquea o se pausa sin estar priorizada, ese
  texto va en **Comentarios**, en su fila de la sección: es el único sitio donde puede vivir.
- **El estado se cambia en los dos sitios**, en la fila de `## Ahora` y en la de la sección de su
  área. La tarea existe duplicada mientras está priorizada, y actualizar solo una deja el archivo
  mintiendo.
- **Solo `Completada` mueve la fila de sitio** (baja al final de su sección). Los cuatro estados
  abiertos la dejan donde está, arriba.
- **Dos estados llevan icono, y solo dos: `🔵 En curso` y `✅ Completada`.** Son los dos extremos que
  se buscan de un vistazo — qué se está trabajando ahora, y qué ya es historial. `Pendiente`,
  `Pausada` y `Bloqueada` van sin icono a propósito: si todas las filas lo llevaran, el icono dejaría
  de señalar nada.
- **El icono va pegado al texto, nunca a secas.** Es la marca visual; el texto es lo que se busca.
  `grep "En curso"` y `grep Completada` tienen que seguir funcionando, y la columna debe leerse igual
  en un visor que no renderice el emoji.

## Por qué el estado es una columna de texto

En una celda de tabla, un `- [x]` de Markdown **no** se renderiza como casilla —GitHub solo convierte
en casillas los ítems de lista—, así que una tabla de tareas no puede usar checkboxes. Y un icono a
secas depende de cómo renderice cada visor y no se encuentra con `grep`. De ahí que el estado sea
texto, en su propia columna, con icono solo en los dos extremos.
