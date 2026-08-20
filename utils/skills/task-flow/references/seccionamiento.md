# Seccionamiento: derivar y ordenar las secciones

Una sección es **una unidad de trabajo estable**: un ámbito que se mantiene en el tiempo y donde uno
busca por reflejo. No es una etiqueta temática, ni un sprint, ni un estado.

Es la decisión más difícil de deshacer del sistema —**las secciones no se reordenan**, para que una
página se busque siempre en el mismo sitio—, así que se propone con cuidado y se confirma.

## Las tres fuentes, a la vez

Ninguna basta sola:

1. **Las tareas que el usuario ya nombró.** Si pidió el sistema mencionando tres cosas concretas, esas
   tres dicen dónde está el trabajo real hoy.
2. **La estructura y el contexto del proyecto.** Sus rutas, sus módulos, sus áreas declaradas en
   `CLAUDE.md`. Es lo que hace que la lista siga sirviendo cuando aparezca trabajo que hoy nadie
   mencionó.
3. **Las tareas que la IA sugiera** en esa primera pasada. Un hueco evidente —no hay nada de
   despliegue, no hay nada de pruebas— sugiere una sección que las otras dos fuentes no habrían dado.

Cruzarlas evita los dos fracasos típicos: un seccionamiento calcado del árbol de directorios (que no
refleja dónde se trabaja) y uno calcado de lo que el usuario dijo en una frase (que se queda corto a
la semana).

## Tabla de derivación

| Tipo de proyecto | Secciones típicas |
| --- | --- |
| Sitio web / app | Una por página o ruta, + `General`, + una por el código compartido |
| Vault de contenido | Una por publicación, cliente o colección |
| Repo de plugins | Una por plugin, + `General` / `Manifests` |
| Librería / CLI | Una por módulo o comando, + `General` |
| Infra / configuración | Una por entorno o servicio, + `General` |

`General` **siempre existe**: es donde va lo transversal y lo que no llena una sección propia.

## Dos criterios al proponer

**Una sección se gana su sitio.** Si solo va a tener una fila, va en `General`. Un archivo con diez
secciones de una tarea cada una no se lee de un vistazo, que es justo lo que la lista debía dar. Como
guía: **dos o tres tareas previsibles** justifican una sección propia.

**El orden es lógico y estable.** Lo transversal primero, lo concreto después:

1. `General` — config, despliegue, lo que no es de un área.
2. El **código o contenido compartido** — lo que alcanza a varias áreas a la vez.
3. Las **áreas concretas**, en un orden que tenga sentido para el proyecto: el del recorrido del
   usuario, el del flujo de datos, o alfabético si no hay uno mejor.

Lo compartido va arriba a propósito: es donde más se trabaja y donde un cambio cierra varias tareas.

## La regla del código compartido

**Un cambio en código o contenido compartido por varios consumidores es UNA tarea, en la sección de lo
compartido — nunca una fila duplicada por consumidor.**

El motivo, que es lo que hace que se respete: duplicarla **cuenta su intervalo dos veces** y obliga a
escribir «no suma al total» en cada copia. Además miente sobre el trabajo: se arregló una vez, no
tres.

De ahí que casi todo proyecto necesite una sección para lo compartido —`Componentes`, `Layout`,
`Utilidades`, `Manifests`—, incluso si al principio está vacía. Sin ella, el primer cambio compartido
no tiene dónde ir y acaba duplicado.

Corolario para los consumidores: una sección puede existir **sin tabla**, con una línea de prosa que
diga dónde se sigue su trabajo. Es información, no un hueco:

> Sin tareas propias. Lo compartido se sigue en «Componentes», porque el cambio vive ahí.

## Qué proponer al usuario

Una tabla corta y una pregunta. Nada más:

| Sección | Abarca | Semillas |
| --- | --- | --- |
| General | Config, despliegue, transversal | 2 |
| Componentes | Código compartido entre páginas | 3 |
| Página de registro | `/registro` | 1 |

El usuario añade, quita o renombra. Si duda, recuerda que **añadir una sección después es fácil** y
reordenarlas no: ante la duda, menos secciones.
