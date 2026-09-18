# El catálogo de secciones (`tareas/secciones.md`)

Persiste lo que `seccionamiento.md` solo describe como criterio: el nombre y el ámbito de cada
sección **exista o no, ahora mismo, una fila activa suya en `tareas.md`**. Sin este catálogo, una
sección que se vació al archivarse su última tarea no tendría dónde reaparecer si el trabajo vuelve
— y se acabaría re-derivando de cero, justo lo que el seccionamiento estable evita.

## Por qué existe aparte de `tareas.md`

`tareas.md` solo muestra secciones **con al menos una fila no completada**. Si el catálogo viviera
solo ahí, una sección sin trabajo activo se perdería. `secciones.md` es la memoria que sobrevive a
ese vaciado: nace con la sección y no se borra cuando esta se queda temporalmente sin tareas.

## Qué contiene, y qué NO

Una entrada por sección: nombre, ámbito (una o dos líneas) y, si ya cerró algo, el total acumulado
de tiempo y el contador de archivadas. **Nunca una tabla de tareas** — eso vive en `tareas.md`
mientras hay trabajo activo, y en el historial mensual una vez cerrado.

```markdown
## Componentes

Código compartido entre páginas: cambios aquí alcanzan a varios consumidores a la vez.

**Cerradas: 2h 25m** · 4 archivadas

## Página de registro

`/registro` y su formulario. Sin tareas activas — lo compartido se sigue en «Componentes».

**Cerradas: 40m** · 1 archivada
```

Una sección recién creada, sin nada cerrado todavía, no lleva la línea `**Cerradas: …**` — se añade
la primera vez que se archiva una tarea suya.

## El catálogo está abierto, no cerrado

`secciones.md` registra lo que se derivó o se propuso al montar el sistema (`--init`) y lo que se ha
usado desde entonces. **No es la lista exhaustiva de secciones posibles**, ni una restricción sobre
lo que puede existir: es memoria de lo ya decidido, no un techo.

Proponer una sección **completamente nueva** —que no salió del `--init` original— sigue siendo
válido en cualquier momento, con el mismo criterio de siempre (`seccionamiento.md`): se gana su sitio
con **dos o tres tareas previsibles**, o va a `General`. No hace falta agotar ni revisar el catálogo
existente antes de proponer una sección nueva — no es una puerta que haya que abrir primero.

Cuando esto pasa, **el catálogo se amplía**: se añade la entrada nueva con su ámbito, igual que
cualquier otra. El catálogo crece con el proyecto; nunca al revés.

## Cuándo se añade o actualiza una entrada

| Situación | Qué hacer en `secciones.md` |
| --- | --- |
| Se propone y confirma una sección en `--init` | Se crea su entrada con nombre + ámbito, sin total todavía |
| Se propone y confirma una sección nueva, no anticipada, en cualquier otro momento | Se **añade** una entrada al final del catálogo — no reemplaza ni «usa un cupo» de las existentes |
| Se cierra una tarea de una sección | Su total acumulado sube, junto con el de `tareas.md` (movimiento del cierre: `modo-gestion.md`, `archivado.md`) |
| Una sección se vacía de tareas activas en `tareas.md` | Su entrada **permanece**, con su total y su contador de archivadas — no se borra ni se marca especial |
| Reversión de una tarea archivada, y su sección ya no tiene header en `tareas.md` | Se recrea el header en su posición de orden estable, y se resta 1 del contador de archivadas aquí |

## Orden

**El mismo orden estable de `seccionamiento.md`**: `General` primero, lo compartido después, las
áreas concretas al final. El catálogo y `tareas.md` nunca se desincronizan en el orden relativo
aunque `tareas.md` muestre solo un subconjunto: si el catálogo tiene General → Componentes →
Contacto, y Contacto se vacía, el catálogo sigue listando General → Componentes → Contacto → lo que
venga después.

## Relación con `seccionamiento.md`

`seccionamiento.md` sigue siendo el criterio para **derivar y proponer** secciones nuevas (las tres
fuentes, «se gana su sitio», la regla del código compartido). Este archivo gobierna **la
persistencia** de lo ya decidido. Se leen juntos solo al proponer una sección nueva; para el resto de
operaciones sobre secciones existentes basta este archivo.

## Errores

- **Una sección tiene fila activa en `tareas.md` pero no está en el catálogo** → inconsistencia:
  dilo y ofrece añadirla con el ámbito que se infiera del uso ya hecho.
- **Se propone una sección que ya existe en el catálogo pero sin fila activa** → no es una sección
  nueva, es reactivarla: créale el header en `tareas.md` y no dupliques la entrada.
- **La sección de una fila reactivada no está en ninguno de los dos archivos** → no debería pasar (el
  catálogo es persistente); si ocurre, dilo y ofrece reconstruir la entrada antes de devolver la fila.
