<!-- tarea: toggl · proyecto {{ID}} «{{Proyecto}}» · cliente {{ID}} «{{Cliente}}» -->

# Configuración · {{Proyecto}}

Configuración del sistema de tareas en este repo: la rama destino (la lee también la guardia de
git), las áreas, el proyecto de Toggl donde van las tareas que el usuario elige y las reglas propias.
Lo común a todos los repos (espacio de trabajo, umbrales) está en la configuración global de Toggl.

## Rama destino

`main`

La rama desde la que sale cada tarea y a la que vuelve al cerrarse, siempre con la aprobación del
usuario después de ver el resultado. `main` por defecto; en un repo con rama de pruebas (por ejemplo
`preview`), esa. Si no es `main`, pasar de ella a `main` es un acto aparte, con su propia aprobación.

## Áreas

Cada plan, pendiente y fila del historial lleva una de estas áreas; las tareas que van a Toggl la
llevan como etiqueta y en la primera línea de la descripción (`Área: <nombre>`). Un área se gana su
sitio: si solo tendría una tarea, va en `General`.

| Área | Qué abarca |
| --- | --- |
| General | {{Lo transversal: documentación raíz, configuración, lo que toca a todo}} |

## Reglas

<!-- Opcional. Lo propio de este repo, por ejemplo:
     - Lo del SII va al proyecto «Administración», no a este.
     - Las tareas del área Pagos son facturables.
     - Estimación por defecto de una tarea de contenido: 45m. -->

## Comentarios

<!-- Opcional. Notas libres sobre cómo se trabaja este proyecto. -->
