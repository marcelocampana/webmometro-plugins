# Formato de las tablas

Columnas verbatim de las cuatro tablas — **preservarlas exactamente**:

```text
| # | Tarea | Sección | Estado | Vence | Coste | Nota |                                  ← tareas.md · ## Ahora
| Estado | Tarea | Vence | Coste | Inicio | Completada | Duración | Comentarios |        ← tareas.md · secciones
| Tarea | Origen | Motivo | Notas |                                                      ← revisar.md
| Tarea | Área | Severidad | Motivo |                                                    ← auditoria.md
```

Las tablas del mensual (`historial/AAAA-MM.md`) llevan **las mismas columnas que las secciones**:
archivar es cortar y pegar, no reformatear (`archivado.md`).

**Variante conectada a Toggl** (marcador `<!-- tarea: toggl … -->`, `toggl-conexion.md`): todo lo que
es tiempo vive en Toggl y en el registro local, y `tareas.md` queda sin esas columnas.

```text
| # | Tarea | Sección | Estado | Nota |                                           ← ## Ahora
| Estado | Tarea | Comentarios |                                                 ← secciones
| Estado | Tarea | Vence | Coste | Inicio | Completada | Duración | Comentarios |  ← historial (igual)
```

La celda `Tarea` lleva el id de Toggl pegado al texto: `Corregir el menú <!-- toggl:16504199 -->`. Se
lee igual y no añade columna; quien muestre la tarea quita el comentario. **El historial conserva las
ocho columnas**: al cerrar, la fila se arma con los números de `presencia.py tramos` (`toggl.md`).
Una fila cerrada ya no cambia, así que no se desincroniza, y la estimación sigue leyendo archivos.

- **El `#` de `## Ahora` es el orden de ejecución**, empezando en 1: la fila 1 es la siguiente tarea
  a tomar. **Se renumera** cuando se inserta una fila o se borra al cerrar, para que no queden huecos
  ni números repetidos. Renumerar no es reordenar: el orden relativo de las demás filas no cambia.
- **Sin saltos de línea dentro de una celda**: rompen la tabla. Si hay que separar ideas, van en la
  misma línea o con `<br>`.
- **Un `|` en el texto hay que escaparlo** (`\|`) o parte la fila en dos columnas.
- **Comentarios es para el trabajo, no para la medición.** Qué se hizo y qué conviene recordar: la
  decisión no evidente, la trampa que costó encontrar, el efecto colateral. Nada de cómo se calculó el
  tiempo. La nota que vale es la que ahorraría un rato a quien vuelva.
- **Una tarea abierta lleva `—`** en Completada y Duración.
- **El archivo no se recalcula solo.** Si se corrige una fecha a mano, la duración y el total de la
  sección quedan desincronizados hasta que se pida rehacerlos.
- **`secciones.md` no lleva tabla**: es prosa corta por sección — nombre, ámbito y total. Su formato
  vive en `secciones-catalogo.md`, no aquí.

## `Vence` y `Coste`

Los dos campos de planificación. Van juntos, delante de la zona de medición, porque se leen juntos:
**para cuándo** y **cuánto**. Ambos son opcionales y llevan `—` cuando no hay dato.

| | Formato | Qué es | Quién lo pone |
| --- | --- | --- | --- |
| `Vence` | `2026-09-30` | **Compromiso externo real**: una entrega, una validación ajena. | El usuario. Es raro |
| `Coste` | `45m`, `2h 30m`, `~25m` | Estimación de **horas de trabajo** para hacerla. | Lo propone el skill; lo confirma o corrige el usuario |

- **`Vence` no planifica: audita.** No sirve para decidir qué se hace hoy —de eso se encarga el orden
  de `## Ahora`— sino para avisar de que el orden que puso el usuario hace caer una tarea después de
  su límite. Si una tarea no tiene un compromiso externo, **no lleva fecha**, y eso es lo normal.
- **`Coste` está en la misma unidad que `Duración`**: horas de trabajo, con las pausas ya descontadas
  (`tiempos.md`). Estimar «2h» y que el intervalo rama→commit cruce una noche no es un fallo de
  estimación. Comparar `Coste` con un tiempo de calendario es el error que invalida la calibración.
- **El `~` de `Coste` significa «lo estimó el skill»**; sin `~`, lo dijo el usuario. La distinción
  importa: solo lo que el skill estimó mide si el skill estima bien.
- **Una fecha nunca se inventa**: sale de `date '+%Y-%m-%d'`. Si el usuario dice «para el viernes», se
  convierte a fecha absoluta y se confirma en la misma línea.
- **Sin muestras suficientes, `Coste` va `—` y se dice.** No se rellena con un número plausible:
  un coste inventado contamina la estimación de todas las tareas que vengan después (`estimacion.md`).
- **Estas columnas también las lee el skill `agenda`**, que compone la vista diaria cruzando repos.
  Las localiza por su nombre en la cabecera, así que añadir una no lo rompe; **renombrar `Vence`,
  `Coste` o `Estado`, sí**. Si cambian aquí, cambia también `agenda/references/contrato-formato.md`.
- **Al archivar, los dos campos viajan con la fila.** `Coste` queda al lado de `Duración` en el
  mensual, que es lo que permite calibrar sin llevar ningún registro aparte.
