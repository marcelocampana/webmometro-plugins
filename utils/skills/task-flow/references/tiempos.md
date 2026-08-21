# Tiempos: medición, descuentos y totales

El registro de tiempos sirve para **estimar la próxima área**, no para llevar la cuenta de las horas.
De ahí las dos reglas que gobiernan todo: se mide contra git, y se descuenta lo que no fue trabajo.

## Las dos marcas

- **Inicio = creación de la rama de la tarea.**
- **Fin = commit de cierre.**

Ambas verificables, y de ahí sale el valor del registro: no depende de que alguien se acordara de
anotar.

```bash
# Cuándo se creó la rama de la tarea
git reflog --date=iso | grep 'moving from main to <rama>'

# El commit de cierre y su fecha
git log -1 --format='%ad  %s' --date=iso <rama>

# Todos los commits de la rama, para ver la actividad real
git log --format='%ad  %s' --date=iso main..<rama>
```

**Fecha *y* hora, siempre.** Estas tareas duran horas, no días: sin hora, casi todas registrarían
`0d`. La hora del momento actual sale de `date '+%Y-%m-%d %H:%M'` — **nunca se inventa**.

## La Duración es tiempo de trabajo

**Si el intervalo rama→commit contiene una pausa larga, se descuenta y se explica en Comentarios.**

Qué se descuenta:

- **Una noche.** Rama a las 17:55, commit a las 09:55 del día siguiente: no son 16 horas.
- **Un salto de horas sin actividad**, visible porque no hay commits intermedios.
- **Un tramo `Bloqueada` de días**, por el mismo motivo.

Qué **no** se descuenta: un intervalo continuo dentro del mismo día se anota tal cual. Git no ve un
almuerzo y no conviene inventarlo.

El caso que justifica la regla: la tarea del enlace del logo ocupó **algo más de una hora** de trabajo
real, pero su intervalo rama→commit cruzaba una noche. Sin descontar, la fila decía **«15h 19m»** — un
número que no informa de nada y que además envenena cualquier estimación futura.

## Cifras estimadas

**Una cifra estimada se marca con `~` y se dice que lo es.** Las tareas sin rama propia no tienen marca
de inicio en el reflog: lo más que se puede acotar es la ventana entre la marca anterior y el commit.
Cuando esa ventana contiene una noche, el inicio es **inferencia, no medición**, y la fila debe
decirlo.

Los totales que incluyen una cifra estimada llevan `~` también.

**Al sembrar historial desde `git log`** (Modo 0), el `~` va **solo en la Duración**: la fecha de
Completada es el commit y es exacta, mientras el Inicio es lo inferido —lo más que se puede acotar es
la ventana entre la marca anterior y ese commit—. Si esa ventana contiene una noche, el Inicio también
va con `~`. En Comentarios se resume el mensaje del commit, y se añade que la fila se reconstruyó del
historial: quien la lea tiene que saber que no se midió en su momento.

## El total vive en `secciones.md`

**No al pie de `tareas.md`, y no solo ahí.** «La página de registro costó 6h 42m» sirve para estimar
la siguiente página; un total global de horas no sirve para nada.

Con el archivado inmediato al cerrar, el total vive **siempre** en `tareas/secciones.md`, en la
entrada de esa sección (`secciones-catalogo.md`), y **se refleja también** bajo la tabla de
`tareas.md` mientras la sección tenga alguna fila activa ahí:

```markdown
**Cerradas en esta sección: 10h 21m** · 3 archivadas
```

Una sección sin tareas cerradas todavía no lleva esa línea. Cuando la sección se vacía y su header
sale de `tareas.md`, el total **no se pierde**: sigue en `secciones.md`, que es la única de las dos
copias garantizada a persistir.

**El total incluye siempre lo archivado.** Nunca se recalcula a la baja: archivar una fila no resta
del total acumulado, solo la mueve de `tareas.md` al historial. Si se recalculara sin las archivadas,
se perdería justo lo que sirve para estimar la siguiente área.

**El archivo no se recalcula solo.** La duración se calcula al cerrar; si después se corrige una fecha
a mano, esa duración y el total en `secciones.md` quedan desincronizados hasta que se pida rehacerlos.

## Comentarios es para el trabajo, no para la medición

Qué se hizo y qué conviene recordar: la decisión no evidente, la trampa que costó encontrar, el efecto
colateral en otras partes del proyecto. **Nada de cómo se calculó el tiempo** — eso se explica una vez,
aquí, y no en cada fila.

La nota que vale es **la que ahorraría un rato a quien vuelva**. «Arrastró cambios de design system a
todo el sitio» o «`.odc-card` gana por cascada a `@layer utilities`» sirven; «se ajustaron paddings» no
dice nada que el diff no diga mejor.

El mensaje del commit de cierre suele traer ya el material: se resume, no se reescribe.
