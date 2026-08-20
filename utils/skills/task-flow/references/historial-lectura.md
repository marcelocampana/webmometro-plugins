# Leer el historial sin perder el ahorro

Un puntero sin criterio de apertura devuelve el coste por otra vía: si se abre el historial «por si
acaso», se lee lo mismo repartido en más archivos y con más llamadas.

**Regla 1 · Se lee la sección, nunca el archivo.** Con comentarios de ~1.000 caracteres de media:

| Qué se lee | Coste | |
| --- | --- | --- |
| Solo la sección del ancla | **~1.000 chars (~250 tok)** | constante |
| El mensual entero, 10 comentarios | ~10.000 | 10× |
| El mensual entero, 20 comentarios | ~20.000 | **20× — más que el `tareas.md` completo** |

Con veinte comentarios acumulados, leer el mensual entero cuesta más que no haber archivado nunca. La
lectura va acotada:

```bash
ANCLA=alinear-la-vista-movil-con-los-mockups
awk -v a="### $ANCLA" 'index($0,a)==1{f=1;print;next} f&&/^#/{exit} f' tareas/historial/2026-08.md
```

**No uses un rango `sed` del ancla al siguiente `###`**: el último comentario de la zona no tiene otro
`###` detrás, así que el rango se desborda a `## Tareas archivadas` y arrastra todas las filas
archivadas — justo el coste que esta regla evita, y peor en la tarea cerrada más reciente, que es la
que más se abre. El `awk` corta en **cualquier** cabecera (`#`).

**Nunca** `cat` ni lectura completa del mensual, salvo que el usuario pida ver el historial de un mes.

**Regla 2 · Lista blanca cerrada.** El resumen de la celda es **la respuesta por defecto**. El detalle
se abre solo en cuatro casos:

| Se abre | |
| --- | --- |
| 1 | El usuario lo pide («¿qué decía de esa tarea?») |
| 2 | Se va a **tocar el mismo archivo o componente** que el resumen nombra — ahí el detalle previene repetir una trampa documentada |
| 3 | El resumen **no alcanza para decidir** algo concreto. Hay que **decirlo antes de abrir**: «el resumen no dice si X; abro el detalle» |
| 4 | **Reversión** de esa tarea |

**No se abre nunca** en: la contextualización de sesión (se leen los resúmenes), la auditoría (contrasta
contra títulos y resúmenes, que basta para deduplicar), «qué sigue» y cualquier consulta, ni al crear o
afinar una tarea salvo que caiga en el caso 2.

El caso 3 lleva su propio freno: **declararlo en voz alta antes de abrir** convierte una apertura
silenciosa en una decisión visible, y es lo que impide usarlo como comodín. Si se declara dos veces en
la misma sesión por la misma tarea, el resumen estaba mal escrito: el arreglo es **mejorar el resumen**,
no seguir abriendo.
