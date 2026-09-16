# Estimar el `Coste` de una tarea

El `Coste` que se propone al crear una tarea sale del **historial de tareas ya cerradas**, no del
criterio. Es lo que convierte la planificación en algo que ocurre al vuelo: el usuario no estima, solo
confirma o corrige un número.

## La regla que decide todo: se empareja por forma, no por sección

Las duraciones **no se agrupan por sección**. Se agrupan por **verbo + objeto**, y esas familias
cruzan secciones. Medido sobre un proyecto real con 29 filas archivadas (17 medidas, 11 estimadas):

| Familia | Medidas | Duraciones | Mediana |
| --- | --- | --- | --- |
| «Alinear *X* con su diseño» | 5 | 3m · 16m · 32m · 6h 33m · 6h 42m | **32m** |
| «Aplicar las N correcciones» | 2 | 10m · 14m | sin base |

En ese mismo proyecto la sección `General` contiene desde 5m hasta 4h 33m: **su media no informa de
nada**. La media por sección es la trampa obvia y hay que evitarla.

Para emparejar, se compara el enunciado nuevo con los de las filas archivadas: mismo verbo y mismo
tipo de objeto. «Alinear la página de HER2 con su diseño» y «Alinear el hero de reconstrucción
mamaria» son la misma familia; «Alinear la página» y «Renovar las imágenes de la página» no lo son,
aunque compartan sección y objeto.

**La primera fila también explica por qué mediana y no media**: con esas cinco muestras la media sale
**2h 49m** y la mediana **32m**. La media describe una tarea que no existe.

## Cuando la familia se dispara, se dice

Esas dos muestras de 6h+ son alineaciones de **una página entera**; las de minutos, de **una sección**.
Misma familia por verbo y objeto, dos órdenes de magnitud de diferencia. La mediana aguanta, pero
proponerla a secas engaña.

**Si el rango de la familia abarca más de un orden de magnitud, se enuncia junto al número.** El
usuario es quien sabe si lo que va a hacer se parece a las de 3m o a las de 6h, y con el rango delante
puede corregir; con la mediana sola, no.

```text
Coste ~32m — mediana de 5 medidas, pero la familia va de 3m a 6h 42m:
las largas son páginas enteras, las cortas secciones sueltas. ¿Cuál se parece a esta?
```

## De dónde se leen las muestras

```bash
# Filas archivadas de la sección candidata, en el mes en curso y el anterior
awk '/^## Tareas archivadas/,0' tareas/historial/2026-09.md | grep '^| ✅'
```

**No se abre el mensual entero** (invariante 11): se lee la zona `## Tareas archivadas`, que son filas
de una línea, nunca la zona `## Comentarios`. Si `tareas/calibracion.md` existe y está al día, se lee
**solo ese archivo** y no se toca el historial.

**La ventana se abre hacia atrás hasta tener base, no hasta un número fijo de meses.** Arranca en el
mes en curso y el anterior; si de ahí no salen las 3 muestras medidas de la familia, se lee el mensual
anterior, y así mes a mes **hasta reunirlas o hasta que se acabe el historial** — y entonces `Coste`
va `—`. Dos meses es el punto de partida porque en un proyecto vivo suele bastar, no porque el dato
de marzo estorbe: lo que no sirve es parar en seco con dos muestras teniendo la tercera un mes más
atrás.

Retroceder **no relaja ninguna otra regla**: de cada mensual se sigue leyendo solo su zona
`## Tareas archivadas`, se siguen descartando las `Duración` con `~`, y la mediana se calcula sobre
todas las muestras reunidas, sin ponderar por antigüedad. **Se dice de cuántos meses salieron**: una
mediana de tres muestras repartidas en cinco meses describe una familia rara, y el usuario lee distinto
ese número que uno de la semana pasada.

## Qué muestra vale y cuál no

- **Solo duraciones medidas.** Una `Duración` con `~` es una estimación; calibrar contra ella es
  morderse la cola. En el proyecto de referencia, 9 de 21 llevaban `~`: **se descartan**.
- **Mediana, nunca media.** Una tarea que se fue a 6× destroza una media. Con pocas muestras la
  mediana es lo único robusto.
- **Mínimo 3 muestras medidas** en la familia para proponer un número. Entre 3 y 4, se propone pero se
  dice que la base es corta. Con menos de 3, se usa el factor global de `calibracion.md` si existe.
- **Sin base, `Coste` va `—` y se dice en la misma línea.** No se inventa un número plausible: un coste
  inventado entra al historial y contamina todas las estimaciones posteriores. «Sin base» es una
  respuesta correcta y frecuente en un proyecto joven.

## Cómo se presenta

Una línea, dentro de la propuesta de la tarea, **con las muestras a la vista** para que el usuario
pueda corregir con criterio:

```text
Coste ~32m — mediana de 5 similares medidas («Alinear X con su diseño»: 3m, 16m, 32m, 6h 33m, 6h 42m).
```

Y cuando no la hay:

```text
Coste — · sin base: 1 cierre en este proyecto y su duración es estimada.
```

**El número propuesto lleva `~`; si el usuario lo corrige, el `~` desaparece.** Esa marca es la que
después permite medir si el skill estima bien (`tiempos.md`).

## Qué NO hace este archivo

- **No corrige el sesgo.** Aplicar un factor de corrección a la mediana es trabajo de
  `calibracion.md`, que se recalcula por tandas y no en cada tarea. Aquí solo se lee el factor
  vigente si está escrito; no se calcula sobre la marcha.
- **No estima retrasos.** Llegar tarde es un problema de capacidad, no de estimación, y se mide en
  días de calendario, no en horas de trabajo. Son dos errores distintos y no se corrigen con el mismo
  número (`tiempos.md`).
