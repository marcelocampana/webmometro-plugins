# Historial · {{AAAA-MM}}

Lo cerrado y lo descartado este mes, con el texto íntegro de sus comentarios: la memoria del repo.
Lo pendiente vive en `tareas/pendientes.md`; aquí queda lo hecho, lo descartado y por qué.

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

## Descartadas

<!-- Una línea por entrada descartada de pendientes.md o de la bandeja:
     - **Título** · Área · AAAA-MM-DD · de pendientes|bandeja — por qué se descarta -->

## Tareas archivadas

<!-- Un ### por área (la del plan, tal cual está en tareas/config.md) — solo las que tengan alguna fila este mes, de la más reciente en cerrar algo
     a la más antigua. Una tarea es una sola fila, aunque tenga subtareas. -->

### {{Área A}}

| Estado | Tarea | Vence | Coste | Inicio | Completada | Duración | Claude | Comentarios |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

### {{Área B}}

| Estado | Tarea | Vence | Coste | Inicio | Completada | Duración | Claude | Comentarios |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

**Total del mes: {{Xh Ym}}**
