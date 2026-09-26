# Contrato de formato con `tarea`

La agenda **no define ningún formato**: consume el de `tarea`, cuyo dueño es
`utils/skills/tarea-repo/references/formato-tablas.md`. Si allí cambia una columna, este archivo
cambia con ella. Es el mismo acoplamiento declarado que hay entre `landing-blueprint` y
`brand-voice-enforcement`, y se sostiene igual: escrito en los dos lados.

## Lo único que se lee

El bloque `## Ahora` de `<repo>/tareas/tareas.md`, y de él estas columnas:

| Columna | Para qué | Si falta |
| --- | --- | --- |
| `#` | Posición, para nombrarla en un aviso | Se usa el orden de aparición |
| `Tarea` | El enunciado, **verbatim** | La fila es inservible: se reporta |
| `Sección` | No se muestra; el repo ya sitúa | — |
| `Estado` | `Bloqueada` se salta; `🔵 En curso` va al tramo 1 | Se trata como `Pendiente` |
| `Vence` | Vencidas y de hoy, y la proyección | `—`: la fila no genera avisos de fecha |
| `Coste` | La cuenta de horas | `—`: cuenta como fila, no como tiempo |
| `Nota` | No se muestra | — |

## Variante conectada a Toggl

Con el marcador `<!-- tarea: toggl … -->`, `## Ahora` es `| # | Tarea | Sección | Estado | Nota |`:
**sin `Vence` ni `Coste`**, que se toman de Toggl (`references/toggl.md`). La celda `Tarea` lleva
`<!-- toggl:id -->` pegado al texto: se extrae el id para cruzar y **se quita al mostrar**. Leer por
nombre de columna es lo que permite que las dos variantes convivan sin romper nada.

## Las columnas se localizan por nombre, nunca por posición

**No es una precaución teórica: hay repos en producción con el formato anterior**, de seis columnas y
sin `Vence` ni `Coste`. Leer por posición ahí devuelve el `Inicio` donde debería ir el `Vence`.

```bash
sed -n '/^## Ahora/,/^---$/p' "$REPO/tareas/tareas.md" | awk '
BEGIN { FS="|"; OFS="\t" }
/^\| *:?-+:? *\|/ { next }                                   # separador
/^\|/ && !h { for (i=2; i<NF; i++) { gsub(/^ +| +$/,"",$i); col[$i]=i } n=NF; h=1; next }
/^\|/ && NF != n { print "FILA-RARA", $0; next }              # celda con | sin escapar
/^\|/ {
  for (i=2; i<NF; i++) gsub(/^ +| +$/,"",$i)
  print $(col["#"]), $(col["Estado"]), ("Coste" in col ? $(col["Coste"]) : "—"),
        ("Vence" in col ? $(col["Vence"]) : "—"), $(col["Tarea"])
}'
```

**Una fila que no encaja se reporta, nunca se descarta en silencio.** Una fila perdida es una tarea
que desaparece del día sin que nadie se entere — el único fallo de esta vista que el usuario no puede
detectar por sí mismo. Un `\|` escapado dentro de una celda parte la fila y es la causa habitual.

**Un repo sin `Coste` en ninguna fila se dice una vez, al pie**, con el remedio: `tarea` los
estima dentro de ese repo, al abrir cada tarea. La agenda no los pone: no puede, y no debe.

## Los valores que se dan por ciertos

- **Los estados, literales**: `Pendiente`, `🔵 En curso`, `Pausada`, `Bloqueada`, `✅ Completada`. Se
  comparan **por el texto**, no por el icono; un `grep` de `En curso` tiene que seguir bastando.
  Una `✅ Completada` en `## Ahora` no debería existir —se archiva al cerrar— y si aparece, se ignora
  y se menciona.
- **`—` es el vacío** en las cuatro tablas. No `N/A`, no celda en blanco.
- **`Coste`**: `45m`, `2h 30m`, `~25m`. El `~` significa «lo estimó el skill» y **para la suma da
  igual**; se conserva en la salida porque el usuario lee distinto un número suyo que uno propuesto.
- **`Vence`**: `AAAA-MM-DD` absoluta. Hoy sale de `date '+%Y-%m-%d'`, **nunca de la memoria**.
- **`Coste` es tiempo de trabajo**, con las pausas descontadas, igual que `Duración`
  (`tarea-repo/references/tiempos.md`). Compararlo con horas de calendario invalida la cuenta del día:
  la capacidad declarada también son horas de trabajo, no horas del reloj.

## Lo que no se toca

`revisar.md`, `auditoria.md`, `secciones.md` y `historial/` **no se abren en la vista diaria**. El
mensual, además, nunca se lee entero ni aunque haga falta (invariante 9 de `tarea`): se lee la
sección de un ancla. La agenda no tiene ningún motivo para llegar ahí.
