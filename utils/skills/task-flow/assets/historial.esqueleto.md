# Historial · {{AAAA-MM}}

Tareas cerradas de este mes y el texto íntegro de sus comentarios. Se llega aquí desde el enlace
`[detalle](...)` de cada fila en `tareas/tareas.md`.

**Se lee la sección concreta, no el archivo entero.** Con veinte comentarios acumulados, leerlo
completo cuesta más que el `tareas.md` que se quiso aligerar:

```bash
awk -v a='### el-ancla-de-la-tarea' 'index($0,a)==1{f=1;print;next} f&&/^#/{exit} f' \
  tareas/historial/{{AAAA-MM}}.md
```

Con un rango `sed` hasta el siguiente `###` el último comentario se desborda a la zona de filas.

## Comentarios

<!-- Un ### por tarea, en kebab-case sin tildes: es el ancla del enlace.
     Debajo, el comentario condensado a un máximo de 900 caracteres. -->

## Tareas archivadas

<!-- Agrupadas por sección de origen, de la menos a la más antigua. -->

### {{Sección de origen}}

| Estado | Tarea | Inicio | Completada | Duración | Comentarios |
| --- | --- | --- | --- | --- | --- |

**Total del mes: {{Xh Ym}}**
