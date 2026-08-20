# Archivado del historial

El comentario de una fila cerrada pesa ~10× más que el resto de la fila (30% del archivo frente a 3%) y
se paga en cada sesión para consultar lo que menos se consulta.

Dos etapas, y **un solo archivo mensual sirve a las dos**: nunca hay más de un archivo por mes.

```text
tareas/historial/
├── 2026-08.md   ← comentarios del mes en curso; + las filas al cumplir el mes
└── 2026-07.md
```

## Etapa 1 · El comentario, al cerrar la tarea

**Todo comentario de una tarea cerrada vive en el historial**, y se mueve en el cierre, siempre — no
cuando salta un umbral. Así el archivo nunca acumula ese peso, ni siquiera en una sesión que cierra
varias tareas el mismo día.

En la celda queda **siempre** un resumen **≤240 chars** más el enlace — nunca vacía, nunca solo el
enlace:

Así queda la celda (148 chars, y ya evita repetir el error):

> Auditoría de diferencias, no implementación. Trampa: `UPageBody` suma `space-y-12` y `pb-24`; se
> anula con `space-y-0 pb-0`. `[detalle](historial/2026-08.md#alinear-la-vista-movil...)`

**Cómo se escribe el resumen** — por este orden: (1) **la trampa que costó encontrar**, que es lo que
evita repetir el error; (2) la **decisión no evidente** y su motivo; (3) el **efecto colateral**. Se
suelta la narración del proceso, las medidas exactas y el detalle de implementación.

**El comentario archivado también tiene tope: ≤900 caracteres** — sin techo en el destino, cada apertura
costaría más y el ahorro sería imprevisible. Conserva trampa, alternativa descartada, efecto colateral y
medidas no recuperables del repo; suelta el relato, que ya está en el mensaje del commit.

**Nunca se toca el comentario de una tarea abierta**: ahí es contexto de trabajo en curso.

**Confirmación:** va dentro del cierre, que el usuario ya confirma, así que no añade una pregunta. Di en
una línea que el comentario quedó en el mensual y **muestra el resumen** para que lo corrija.

## Etapa 2 · La fila completa, al cumplir el mes

**Disparador:** cerró hace más de un mes (contra su Completada); se comprueba al abrir o cerrar, no en
cada consulta. La fila se muda al mensual **junto a su comentario, que ya está ahí**. **Siempre con
confirmación**: mover filas nunca ocurre en silencio.

Al mover la fila, **su enlace pasa a ancla del mismo archivo** (`[detalle](#el-ancla)`): la ruta
`historial/AAAA-MM.md` era relativa a `tareas.md` y desde dentro de `historial/` ya no resuelve.

La sección conserva su **total acumulado** más un puntero, para que siga sirviendo para estimar:

```markdown
**Cerradas en esta sección: 10h 21m** · 3 archivadas en [historial](historial/2026-07.md)
```

**Para leer un detalle**: se lee la sección del ancla, nunca el archivo, y solo en cuatro casos tasados
— reglas en `historial-lectura.md`, que se consulta al abrir un detalle, no al archivar.

## El umbral

Red de seguridad, no mecanismo principal —de eso se encarga la etapa 1—. Se anota al inicio de
`tareas.md`:

```markdown
<!-- task-flow: umbral 40000 chars · holgura 70% · última revisión 2026-08-20 -->
```

Por defecto ~40.000 chars (~10k tokens). Al vivir en el archivo es visible y editable; el skill lo
respeta y no lo reescribe sin permiso. **Se mide con `wc -c`**: exacto y sin depender de un tokenizador
(4 chars ≈ 1 token, solo para explicárselo al usuario).

Si el archivo supera el umbral con todos los comentarios ya archivados, el peso está en las filas
(etapa 2) o en lo abierto — y si es lo abierto, **dilo y no archives nada**.

## El formato del mensual

Desde `assets/historial.esqueleto.md`: zona `## Comentarios` (un `### <título>` en kebab-case sin
tildes por comentario — es el ancla del enlace) y zona `## Tareas archivadas` (las mismas columnas que
las secciones, por sección de origen, de la menos a la más antigua, con el total al pie). Columnas
idénticas = mover una fila es cortar y pegar, sin reformatear.

## Reversión

Recuperar una tarea archivada la devuelve a su sección **con el comentario íntegro**, no con el resumen
recortado, y la quita del mensual. El historial no es un destino de solo ida.

## Errores

- **Enlace a un mensual o ancla que no existe** → dilo y ofrece reconstruirlo; no inventes el comentario.
- **Fila en el mensual sin su comentario, o al revés** → avisa y ofrece reunirlos.
- **Umbral editado a un valor absurdo** → dilo y propón uno razonable; no lo cambies solo.
- **Un comentario no baja de 900 sin perder lo accionable** → deja lo que quepa y dilo. Antes perder
  relato que perder la trampa.
- **Piden archivar una tarea abierta** → no se hace: solo `✅ Completada`.
- **Piden reabrir una archivada** → se revierte primero, y luego es una tarea normal.
