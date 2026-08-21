# Formato de las tablas

Columnas verbatim de las cuatro tablas — **preservarlas exactamente**:

```text
| # | Tarea | Sección | Estado | Inicio | Nota |                    ← tareas.md · ## Ahora
| Estado | Tarea | Inicio | Completada | Duración | Comentarios |   ← tareas.md · secciones
| Tarea | Origen | Motivo | Notas |                                 ← revisar.md
| Tarea | Área | Severidad | Motivo |                               ← auditoria.md
```

- **El `#` de `## Ahora` es el orden de ejecución**, empezando en 1: la fila 1 es la siguiente tarea
  a tomar. **Se renumera** cuando se inserta una fila o se borra al cerrar, para que no queden huecos
  ni números repetidos. Renumerar no es reordenar: el orden relativo de las demás filas no cambia.
- **Sin saltos de línea dentro de una celda**: rompen la tabla. Si hay que separar ideas, van en la
  misma línea o con `<br>`.
- **Un `|` en el texto hay que escaparlo** (`\|`) o parte la fila en dos columnas.
- **Comentarios es para el trabajo, no para la medición.** Qué se hizo y qué conviene recordar: la
  decisión no evidente, la trampa que costó encontrar, el efecto colateral. Nada de cómo se calculó el
  tiempo. La nota que vale es la que ahorraría un rato a quien vuelva.
- **Una tarea abierta lleva `—`** en Completada y Duración.
- **El archivo no se recalcula solo.** Si se corrige una fecha a mano, la duración y el total de la
  sección quedan desincronizados hasta que se pida rehacerlos.
- **`secciones.md` no lleva tabla**: es prosa corta por sección — nombre, ámbito y total. Su formato
  vive en `secciones-catalogo.md`, no aquí.
