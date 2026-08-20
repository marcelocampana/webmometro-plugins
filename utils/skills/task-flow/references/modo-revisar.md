# Modo 2 · Por revisar (`--revisar`)

La bandeja donde la IA propone libremente y el usuario aparca lo que aún no quiere en la cola. Tres
vías de entrada:

1. **La IA anota lo que detecta de paso** trabajando en otra tarea: un `TODO`, una deuda, un efecto
   colateral, algo que el diff deja a medias.
2. **La IA sugiere tareas derivadas** de lo ya ejecutado — el «esto quedó pendiente de lo anterior»,
   que sale del historial cerrado y del trabajo reciente.
3. **El usuario aparca una idea** para más adelante.

Columnas: `Tarea | Origen | Motivo | Notas`. **`Origen` es lo que hace útil la lista**: de qué tarea,
commit o archivo salió. Sin eso, en dos semanas una fila no dice por qué está ahí. Sin estados, sin
tiempos, sin ramas.

Operaciones: proponer, listar, **ascender a `tareas.md` con aprobación** y descartar. Al ascender, la
fila **se mueve** (desaparece de aquí), adopta las columnas de la principal en `Pendiente` y sin
Inicio, y su Motivo pasa a Comentarios. **Revisa el enunciado otra vez al ascender**: lo que basta en
una bandeja puede no bastar en la cola de trabajo (`redaccion-tareas.md`). Como en todas las listas,
**se propone y se espera**, y una sugerencia sin ancla verificable no se propone
(`contextualizacion.md`).
