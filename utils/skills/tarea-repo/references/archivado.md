# El historial: qué se escribe al cerrar

El historial es la memoria del repo: lo que se hizo, cuánto costó, lo que se descartó y **por qué**. Es lo que Claude lee
para saber qué se ha venido haciendo, y lo que calibra las estimaciones. **Se escribe en el mismo
cierre**, dentro de la cadena, nunca como paso aparte.

```text
tareas/historial/
├── 2026-09.md   ← comentarios y filas de todo lo cerrado este mes
└── 2026-08.md
```

## Qué se escribe

**El comentario** (≤900 caracteres: la trampa, la decisión no evidente, el efecto colateral, las
medidas que no se recuperan del repo; lo relevante de las notas del plan) va bajo
`## Comentarios` del mensual, como `### <ancla>` en kebab-case sin tildes. Nada de cómo se calculó
el tiempo: la nota que vale es la que ahorraría un rato a quien vuelva.

**La fila** va bajo `## Tareas archivadas`, en el `### <Área>` del área del trabajo (la de la
cabecera del plan), con nueve columnas:

```text
| Estado | Tarea | Vence | Coste | Inicio | Completada | Duración | Claude | Comentarios |
```

- Los números salen de `presencia.py tramos` (`inicio`, `fin`, `duracion`, `coste`, `vence`,
  `claude`).
- **Duración** es el tiempo del usuario; **Claude**, el de Claude en la tarea, como
  `<claude> · <solo> solo` (`1h 10m · 40m solo`), o `—` sin respuestas suyas. Nunca se suman: un
  minuto con los dos cuenta en ambas. No va a Toggl: el detalle tramo a tramo está en el registro
  local de Claude (`presencia.py asentar`), y aquí queda el total de la tarea. Sin registro de presencia (se trabajó fuera del Mac), la Duración sale del intervalo de la
  rama y lleva `~`, y se dice.
- La celda Tarea lleva `<!-- plan:<slug> -->` (las filas antiguas, `<!-- toggl:id -->`); la de
  Comentarios termina en `[detalle](#el-ancla)`, ancla del mismo archivo.
- **Un trabajo es una sola fila**, aunque se haya retomado varias veces: Duración, lo medido en
  local; Claude, el `claude` de sus `tramos`. El comentario enlaza el plan
  (`tareas/planes/<slug>.md`), donde queda el paso a paso.
- Una fila cerrada ya no cambia.

## Lo descartado

Lo que sale de `pendientes.md` o de la bandeja sin hacerse va bajo `## Descartadas` del mensual (antes
de `## Tareas archivadas`), una línea por entrada, para que no se pierda ni se vuelva a proponer:

```text
- **Título** · Área · AAAA-MM-DD · de pendientes|bandeja — por qué se descarta
```

## El formato del mensual

Desde `assets/historial.esqueleto.md`: zona `## Comentarios`, zona `## Descartadas` (si hubo) y zona
`## Tareas archivadas`, con un
`### <Área>` por cada área que tenga alguna fila ese mes (el nombre tal cual está en `config.md`). El
orden de los `###` es **del área más reciente en cerrar algo a la más antigua**: lo que se consulta
primero es lo que se acaba de cerrar. El total del mes va al pie, una sola cifra.

Una tabla de ocho columnas (sin **Claude**) es de antes de medir a Claude: al añadirle la primera
fila de nueve, se le agrega la columna con `—` en las filas que ya estaban. Solo cambia el formato.

Los mensuales anteriores a la migración usan el nombre de la **sección** en el `###`: es el mismo
dato con el nombre de antes y se lee igual.

## Reabrir algo archivado

Se devuelve a `pendientes.md` (`Por hacer`, con el comentario íntegro como «qué falta») y se quitan
del mensual su `###` de Comentarios y su fila. Si era la única fila de esa área ese mes, se
quita también su `### <Área>`.

## Errores

- **Enlace a un ancla que no existe** → dilo y ofrece reconstruirlo; no inventes el comentario.
- **Fila sin su comentario, o al revés** → avisa y ofrece reunirlos.
- **Un comentario no baja de 900 sin perder lo accionable** → deja lo que quepa y dilo. Antes perder
  relato que perder la trampa.
