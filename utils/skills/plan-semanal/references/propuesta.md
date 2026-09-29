# La propuesta de la semana

El usuario tiene que poder aprobarla en un minuto. **Claude hace el cálculo; el usuario solo ve el
resultado y corrige lo que no le cuadra.**

## Cómo se llena cada día

Se recorren los días de la semana con la jornada que da `capacities` (o la de la configuración de
`agenda` si la trae). Cada día se llena hasta su capacidad, en este orden:

1. **Lo ya fechado por el usuario** en Toggl para ese día: se respeta, aunque desborde.
2. **El arrastre** de la semana pasada, primero lo más antiguo.
3. **Lo que tiene `Vence`** esta semana o la siguiente: va el día que permita llegar, contando
   hacia atrás desde el vencimiento.
4. **Las pendientes sin día**, por prioridad, después por el orden de los proyectos en la
   configuración y, dentro de cada uno, por su posición en Toggl. **Se reparten los proyectos entre
   los días**: no se llena el lunes entero con uno solo si hay otros esperando, salvo que el usuario
   lo pida. Una tarea que no cabe entera en lo que queda de un día pasa al siguiente; no se parte.
   Una subtarea del usuario va antes que la parte de su tarea que la necesita.

**Se deja un 20% libre cada día** para imprevistos. Un plan al 100% se rompe el lunes a las diez;
`balance` dirá después si el 20% alcanzó y se ajusta.

## Lo que no tiene estimación

Se juntan todas en **una sola pregunta**, dentro de la propuesta, con la sugerencia de `tarea` si el
historial de ese repo la tiene (`tarea-repo/references/estimacion.md`), o sin ella:

```text
Sin estimación (dime un número o déjalas fuera):
  · Documentar agenda en el README (plugins) — historial: ~20m
  · Revisar el copy de la home (webmometro) — sin base
```

La estimación que da el usuario va a Toggl **sin `~`**: es suya. Las que se dejan fuera salen al pie
como «sin estimar» y no se planifican.

## Los avisos

Van al pie, una línea cada uno y solo si se cumplen:

- **Un día pasa del umbral de sesión continua** (`sesion_min` de `toggl.md`) sin pausa posible:
  «el martes suma 3h 40m: te propondré una pausa hacia las 2h».
- **La semana no alcanza:** «quedan fuera 3 tareas (~4h); ¿alguna es más urgente que lo planificado?».
- **Un `Vence` no se cumple** ni poniéndolo primero: se dice cuál y cuándo cae.
- **El plan contradice una dependencia** escrita en la descripción o las notas («necesita X» y X va
  después): se dice; no se reordena.
- **Repos sin migrar** (sin `tareas/toggl.md`): se nombran al pie; sus tareas no se ven.

## Plantilla

```text
Semana del lunes 28 de septiembre · capacidad 20h (16h planificables, 20% libre)

Lunes 28    ~3h 10m   Planificar la semana en Toggl (plugins) · Revisar el copy de la home (web)
Martes 29   ~3h       Corregir el menú móvil (odc) · Documentar agenda (plugins)
Miércoles   ~2h 40m   Arrastre: Aplicar correcciones médicas (odc-clusters)
Jueves      ~3h 20m   …
Viernes     ~1h       Balance de la semana · margen

9 tareas · ~13h 10m de 16h · 2 sin estimar · 1 repo sin migrar (cdz)

¿La guardo así, o mueves algo?
```

- **El nombre, tal cual está en Toggl**, recortado por la derecha si no cabe (por caracteres, no
  bytes). Un paso lleva el nombre de su principal si cabe.
- **El proyecto entre paréntesis**, o la etiqueta del registro si es un repo.
- **Una sola pregunta.** Las correcciones del usuario («el copy al jueves», «saca la de ODC») se
  aplican y se muestra solo lo que cambió, no la semana entera otra vez.
