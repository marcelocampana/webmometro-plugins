# La bandeja: `por-revisar` (`--revisar`)

La bandeja son las tareas del proyecto en Toggl con la etiqueta **`por-revisar`**, sin fecha y sin
asignar: no entran en la capacidad ni en el plan de la semana. Es donde la IA propone libremente y el
usuario aparca lo que aún no quiere en la cola.

Tres vías de entrada:

1. **La IA anota lo que detecta de paso** trabajando en otra tarea: un `TODO`, una deuda, un efecto
   colateral, algo que el diff deja a medias. Se propone **en una línea y se sigue**.
2. **La IA sugiere tareas derivadas** de lo ya ejecutado: lo que quedó pendiente según el historial.
3. **El usuario aparca una idea** para más adelante.

**La descripción dice de dónde salió** —la tarea, el commit o el archivo— y por qué: sin eso, en dos
semanas no se sabe por qué está ahí. Primera línea, el área, como en toda tarea.

Operaciones:

- **Listar:** `cola.py leer --vista pendientes --proyecto <ID>` y quedarse con las que llevan
  `#por-revisar`.
- **Ascender, con aprobación:** quitar la etiqueta, asignarla al usuario y poner la estimación.
  **Revisa el enunciado otra vez al ascender**: lo que basta en una bandeja puede no bastar en la cola
  (`redaccion-tareas.md`).
- **Descartar:** archivarla en Toggl, con visto bueno.

Como siempre, **se propone y se espera**, y una sugerencia sin ancla verificable no se propone.
