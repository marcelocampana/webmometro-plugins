# Historial · {{AAAA-MM}}

Tareas cerradas de este mes y el texto íntegro de sus comentarios: la memoria del repo. Los
pendientes viven en Toggl; aquí queda lo hecho y por qué.

**Se lee la sección concreta, no el archivo entero.** Con veinte comentarios acumulados, leerlo
completo cuesta mucho más que lo que se buscaba:

```bash
awk -v a='### el-ancla-de-la-tarea' 'index($0,a)==1{f=1;print;next} f&&/^#/{exit} f' \
  tareas/historial/{{AAAA-MM}}.md
```

Con un rango `sed` hasta el siguiente `###` el último comentario se desborda a la zona de filas.

## Comentarios

<!-- Un ### por tarea, en kebab-case sin tildes: es el ancla del enlace.
     Debajo, el comentario condensado a un máximo de 900 caracteres. -->

## Tareas archivadas

<!-- Un ### por área (la de la primera línea de la descripción en Toggl, tal cual está en
     tareas/toggl.md) — solo las que tengan alguna fila este mes, de la más reciente en cerrar algo
     a la más antigua. Una tarea es una sola fila, aunque tenga subtareas. -->

### {{Área A}}

| Estado | Tarea | Vence | Coste | Inicio | Completada | Duración | Claude | Comentarios |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

### {{Área B}}

| Estado | Tarea | Vence | Coste | Inicio | Completada | Duración | Claude | Comentarios |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

**Total del mes: {{Xh Ym}}**
