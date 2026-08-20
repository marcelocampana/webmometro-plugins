# Contextualización: qué leer, en qué orden, qué retener

## El principio

**Ninguna tarea se crea, modifica o describe sin contexto del proyecto** — venga de la IA o dictada
por el usuario. Es la regla que ordena todo lo demás.

**Se contextualiza una vez por sesión y se reutiliza.** En la primera operación, lee y retén:

1. `CLAUDE.md` y los docs que este señale — qué es el proyecto, sus convenciones, su deuda declarada.
2. **Las tres listas completas**, incluido el historial `✅ Completada` de `tareas.md`: es el mapa de
   lo ya resuelto y de las trampas que costaron tiempo.
3. La tarea **en curso** y su rama, si hay una (`git branch --show-current`).
4. `git log` reciente — qué se ha movido últimamente.
5. **La conversación en marcha**: lo que se acaba de descubrir depurando es materia prima de tareas,
   y a menudo la mejor.

Después, reutiliza esa lectura y solo relee el archivo que vas a tocar.

**El protocolo: propone y espera.** Muestra el enunciado y las observaciones, y **espera el visto
bueno antes de escribir la fila** — en las tres listas. Vale igual para lo que sugiere la IA y para
lo que dicta el usuario: si el enunciado dictado se puede afinar, propónlo afinado y di qué cambió.

Excepción única, y es de forma: un hallazgo lateral detectado **mientras trabajas en otra tarea** se
propone para `revisar.md` **en una línea y sigues** — sin abrir una deliberación que descarrile la
tarea en curso.

Una tarea escrita sin contexto es una que habrá que reescribir, y a menudo una que duplica algo ya
resuelto.

## Cuándo se relee

Antes de tiempo, solo si:

- El usuario dice que editó las listas a mano.
- Se cambió de rama o se hizo un merge desde la última lectura.
- Se va a auditar (Modo 3): ahí la lectura de las tres listas tiene que estar fresca, porque la
  condición del modo es no duplicar lo que ya existe.

## Qué leer, en orden

1. **`CLAUDE.md` y los docs que señale.** Qué es el proyecto, sus convenciones, su deuda declarada y
   sus trampas conocidas. Un proyecto que documenta «no añadir `dark:`» o «los assets no van en la
   raíz de `public/`» ya te está diciendo qué tareas tienen sentido y cuáles serían un error.
2. **Las tres listas, completas.** Incluido el historial `✅ Completada` — ver abajo.
3. **La tarea en curso**, si hay una: `git branch --show-current` y la fila `🔵 En curso`. Todo lo que
   propongas se lee en relación con ella.
4. **`git log` reciente** (10–20 commits). Qué se ha movido, y si `main` está al día.
5. **La conversación en marcha.** A menudo la mejor fuente: lo que se acaba de descubrir depurando es
   materia prima de tareas y no está escrito en ningún sitio todavía.

## El historial cerrado es la parte que más rinde

Las filas `✅ Completada` no son archivo muerto. Sus Comentarios son el único sitio donde vive la
trampa que costó dos horas, el efecto colateral que no era obvio y la decisión que alguien ya tomó.
Usarlas evita los tres errores más caros:

- **Proponer algo ya resuelto.** Aparece cerrado, con su motivo.
- **Proponer algo que ya se intentó y se descartó.** El comentario suele decir por qué.
- **Repetir una trampa conocida.** Si el historial dice que un componente compartido cambia de forma
  en móvil, una tarea nueva sobre ese componente tiene que tenerlo en cuenta.

También sirve para **estimar**: el total por sección dice lo que costó un área comparable.

## Anclar: la regla que separa una sugerencia de una ocurrencia

**Toda tarea propuesta se ancla en algo verificable.** Sin ancla, no se propone. Ancla válida:

| Ancla | Ejemplo |
| --- | --- |
| Un archivo o línea | `AppHeader.vue:42` no maneja el caso de menú vacío |
| Deuda declarada en los docs | `CLAUDE.md` lista tres hardcodeos a resolver antes de escalar |
| Un hallazgo de la conversación | «esto reventó al probar en móvil» dicho hace dos mensajes |
| Un patrón del historial | dos tareas cerradas tocaron el mismo componente por el mismo motivo |
| Salida de un comando | un `grep` que encuentra el marcador, un build que avisa |

No son ancla: «suele ser buena práctica», «los proyectos así normalmente necesitan», «convendría
revisar» sin decir qué. Eso es lo que produce listas que nadie ejecuta.

## Qué retener

Poco y útil. Después de la lectura deberías poder responder sin volver a los archivos:

- Qué es el proyecto y qué **no** hay que hacer en él (sus prohibiciones explícitas).
- Las secciones que existen y qué abarca cada una.
- Qué hay en curso, qué está bloqueado y por qué.
- Qué se cerró recientemente y qué dejó pendiente.

**Lo que se retiene se usa, no se narra.** No abras una respuesta recapitulando lo leído: el usuario
escribió esos archivos.
