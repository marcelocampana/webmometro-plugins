# La vista diaria

Una pantalla que responde **qué toca hoy y si cabe**. Todo lo que no sirva a esa pregunta sobra, por
interesante que sea.

## Qué entra, en tres tramos

**Tramo 1 · Lo que ya está abierto.** Toda fila `🔵 En curso`, en cualquier repo. Siempre aparece,
aunque no quepa en la capacidad: ya está consumiendo el día.

**Tramo 2 · Lo que tiene la fecha encima.** `Vence` anterior a hoy (vencida) o igual a hoy. También
aparece siempre, marcada. Son las únicas dos cosas que pueden saltarse el orden del usuario, y solo
para mostrarse: nunca se reordena el archivo.

**Tramo 3 · El relleno, por orden.** Se recorre el **registro de repos en el orden de la
configuración** y, dentro de cada uno, `## Ahora` **desde arriba**, saltando `Bloqueada` y lo ya
listado. Se para al llegar al primero de estos tres límites:

| Límite | Valor |
| --- | --- |
| La capacidad declarada se llena | Suma de `Coste` de lo listado |
| Se alcanza el tope de filas | **5** en el tramo 3 |
| Se acaban las colas | — |

El tope de filas no es decoración: **el día uno casi nada tiene `Coste`**, y sin él la capacidad no se
llena nunca. Sin tope, la agenda se convierte en el backlog completo justo cuando menos informa.

## Las dos cuentas corren en paralelo

- **Horas** — suma de los `Coste` presentes. Una fila sin `Coste` **no suma cero: no suma**, y se
  cuenta aparte. Decir «1h 20m de 4h» ocultando que hay tres filas sin estimar es mentir con datos
  ciertos.
- **Filas** — cuántas se listan de cuántas hay disponibles.

```text
3 tareas · ~1h 20m de 4h · entra con holgura
3 tareas · 2 sin coste, así que la cuenta de horas va incompleta
5 tareas · ~4h 10m de 4h · se pasa; la última no cabe
```

## Los avisos

Van al pie, **una línea cada uno**, y solo si se cumplen:

- **Dos o más `🔵 En curso`.** Rompe «una tarea a la vez» de hecho, aunque cada repo cumpla la regla
  por separado. Se nombra: «dos ramas abiertas a la vez: X en *a*, Y en *b*».
- **Un `Vence` que el orden no alcanza.** Solo se enuncia **si todas las filas que van por delante
  tienen `Coste`**: la proyección se calcula acumulando costes y dividiendo por la capacidad diaria.
  Si falta un coste por el camino, se dice que no se puede proyectar, en vez de inventar el día.
- **El día se lo lleva un solo repo.** Cuando el tramo 3 sale entero de un repo, se dice en una línea
  para que el usuario decida; no se reparte por cuenta propia.
- **El empujón a planificar**, y **por umbral, nunca por calendario**: ≥5 filas sin `Coste` o ≥2
  vencidas, sumando repos. Una línea, y no se repite dentro de la misma respuesta.

```text
⚠ «Cerrar la validación médica» vence el jueves (~50m) y va en la 6: por orden cae el viernes.
⚠ «Cerrar la validación médica» vence el jueves y va en la 6: no se puede proyectar el día,
  faltan costes en dos filas por delante.
```

## La plantilla

```text
Hoy · martes 15 · capacidad 4h · llevas 1h 10m trabajadas

  En curso   Crear el skill agenda con la vista diaria     plugins        —
  1          Aislar por qué el dev pierde la base          odc-clusters   ~25m
  2          Aplicar las correcciones médicas de HER2      odc-clusters   ~15m
  ─────────────────────────────────────────────────────────────────────────
  3 tareas · ~40m de 4h · 1 sin coste, la cuenta va incompleta

  ⚠ odc-clusters no tiene Coste en ninguna fila: `tarea` allí los estima al abrirlas.
```

- **El enunciado de la tarea, tal cual está en el archivo**, recortado por la derecha si no cabe.
  Nunca reescrito: el usuario tiene que reconocerlo de un vistazo.
- **El recorte cuenta caracteres, no bytes.** El `substr` de `awk` corta bytes y parte un acento por
  la mitad —`calibraci` seguido de basura—, justo en un idioma donde casi toda línea larga lleva uno.
  Se recorta al componer la salida, no dentro del `awk`.
- **La etiqueta del repo es la del registro**, no la ruta.
- **`—` donde no hay coste.** No se rellena con un guion largo que parezca un número.

## Qué NO entra

- **`revisar.md`, `auditoria.md` y el historial.** La bandeja es material de la revisión semanal
  —skill `balance`—, no de la mañana; abrirla a diario convierte la agenda en un volcado.
- **Las secciones de `tareas.md`.** La fila de `## Ahora` ya trae lo necesario; el detalle es para
  cuando se abre la tarea, dentro de su repo.
- **Nada calculado sobre el historial.** Calibrar es de `balance`, y leer el mensual de cada repo
  cada mañana cuesta más que toda la vista.
- **Lo que no cabe en la capacidad.** No se lista «por si acaso»: se cuenta y se calla.
