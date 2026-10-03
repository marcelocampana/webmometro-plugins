# La vista diaria

Una pantalla que responde **qué toca hoy y si cabe**. Todo lo que no sirva a esa pregunta sobra.

## Qué entra, en tres tramos

**Tramo 1 · Lo que ya está abierto.** Toda tarea en In Progress. Siempre aparece, aunque no quepa:
ya está consumiendo el día. Una tarea y sus subtareas (lo que le toca al usuario) se listan las dos.

**Tramo 2 · Lo que tiene la fecha encima.** Lo vencido (fin anterior a hoy, sin hacer) y lo que es
de hoy (su día o su vence es hoy): es lo que `plan-semanal` o el usuario ya pusieron en este día.
Siempre aparece, marcado. Lo planificado para días anteriores y no hecho se marca `arrastre`, y si
son varias, un aviso: «3 del plan de ayer quedaron pendientes: `plan-semanal --replanificar`».

**Tramo 3 · El relleno, por orden.** Solo si queda capacidad. De las pendientes **sin día** y no
bloqueadas (ni las antiguas con la etiqueta `por-revisar`): por prioridad, después por el orden de los proyectos en la
configuración, y dentro de cada proyecto por su posición en Toggl. Se para al llegar a:

| Límite | Valor |
| --- | --- |
| La capacidad del día se llena | La suma de estimaciones de lo listado |
| Se alcanza el tope de filas | **5** en el tramo 3 |
| Se acaban las pendientes | — |

## Las dos cuentas corren en paralelo

- **Horas** — suma de las estimaciones presentes contra la jornada de Toggl (`working_minutes`). Una
  tarea sin estimación **no suma cero: no suma**, y se cuenta aparte.
- **Filas** — cuántas se listan de cuántas hay disponibles.

```text
3 tareas · ~1h 20m de 8h · entra con holgura
3 tareas · 2 sin estimación, así que la cuenta de horas va incompleta
```

## Los avisos

Al pie, **una línea cada uno**, y solo si se cumplen:

- **Dos o más tareas en In Progress** de proyectos distintos: «dos abiertas a la vez: X y Y».
- **Un vence que no se alcanza** con lo que va por delante, solo si todo lo de delante tiene
  estimación; si falta alguna, se dice que no se puede proyectar.
- **Atención sin tarea abierta**: si `presencia.py resumen` muestra más de 15 min en un repo sin
  ninguna tarea abierta de su proyecto: «40 min en odc-clusters sin tarea abierta».
- **La jornada es la de por defecto**: si `working-hours` del usuario está vacío, una vez: «la
  jornada de Toggl no está configurada: uso sus 8h por defecto».
- **El empujón a planificar**, por umbral: ≥5 pendientes sin estimación o ≥2 vencidas.
- **Lo de Claude**, si hay: las entradas de `tareas/pendientes.md` de los repos de la configuración
  (y del global, `~/Obsidian/Global/pendientes.md`), contadas: «Claude tiene 3 pendientes en 2
  repos». No se listan ni suman a tu capacidad: no están en Toggl y las hace Claude cuando lo pidas.

## La plantilla

```text
Hoy · martes 29 · jornada 8h · llevas 1h 10m trabajadas · copia de hace 3 min

  En curso   Crear el script de migración              Plugins de IA   ~30m
  Hoy        Aplicar las correcciones médicas de HER2  Contenidos ODC  ~15m
  1          Aislar por qué el dev pierde la base      Clusters ODC    ~25m
  ─────────────────────────────────────────────────────────────────────────
  3 tareas · ~1h 10m de 8h · 1 sin estimación, la cuenta va incompleta
```

- **El nombre, tal cual está en Toggl**, recortado por la derecha si no cabe, **contando caracteres
  y no bytes** (un acento no se parte).
- **El proyecto de Toggl**, no la ruta del repo. Un paso lleva el nombre de su principal si cabe.
- **`—` donde no hay estimación.**

## Qué NO entra

- **La bandeja (`por-revisar.md`), la auditoría y el historial.** Son de la revisión semanal
  (`balance`), no de la mañana.
- **Nada calculado sobre el historial.** Calibrar es de `balance`.
- **Lo que no cabe en la capacidad.** No se lista «por si acaso»: se cuenta y se calla.
