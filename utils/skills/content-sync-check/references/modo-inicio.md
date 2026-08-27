# Modo 0 · Inicio: configurar los destinos

Se invoca con `--init`, o cuando el Paso 0 no encuentra `## Destinos de publicación` en
`contexto/configuracion.md` y el usuario pidió algo de sincronización. **Solo ante esa petición** —
nunca en medio de otro trabajo.

**El trabajo real es proponer, no interrogar.** Casi todo se deriva leyendo lo que ya existe; pedir
al usuario dato por dato lo que se puede descubrir es hacerle escribir un inventario que el skill
tiene delante. Un solo dato es genuinamente impreguntable.

## 1 · Derivar en silencio

Antes de preguntar nada:

- **Repo del sitio** — busca `content.config.ts` o `nuxt.config.ts` en los directorios de trabajo
  de la sesión. Si hay uno solo, propónlo; si hay varios, muéstralos y que el usuario elija.
- **Colecciones y sus rutas** — de `content.config.ts`: el `source.include` y el `prefix` de cada
  colección dicen qué carpeta sirve cada cosa.
- **Fuentes del workspace** — las carpetas bajo `web/contenido/` que contengan `.md` con
  frontmatter del mismo esquema que las colecciones.
- **Espejo local** — una carpeta de `.dc.html` en el repo del sitio (típicamente `htmls/`).

## 2 · Pedir solo lo impreguntable

**El identificador del proyecto de diseño no se puede descubrir**: `list_projects` solo devuelve
proyectos de tipo design-system, y los de páginas no aparecen ahí — ni con el consentimiento de
acceso concedido. Pídelo **una vez**, y hazlo fácil:

- Acepta la **URL completa** del canvas (`https://claude.ai/design/p/<uuid>?file=…`) y extrae el
  uuid tú: es lo que el usuario tiene a mano, no el id pelado.
- Di **dónde encontrarla**: la barra de direcciones al abrir el canvas.
- **Si no la tiene a mano, no bloquees.** Sigue con los destinos que sí resuelven y anota Claude
  Design como pendiente en la configuración. Un onboarding que exige todo por adelantado es un
  onboarding que se abandona a medias.

Con el id, confirma el acceso (`get_project`) y usa el `name` que devuelve — no pidas que lo
escriba.

## 3 · Proponer el mapeo ya cruzado

Cruza las tres listas (fuentes, colecciones del sitio, archivos del canvas) y **propón la tabla ya
resuelta**, en una tabla corta. Empareja por slug normalizado: sin tildes, sin prefijos numéricos
(`4.triple-negativo` → `triple-negativo`), sin sufijos de rol (`-copy`), **ignorando
mayúsculas**. Las variantes de dispositivo se detectan por sufijo (`- Móvil`, `- Movil`,
`- Mobile`) sobre un nombre base que ya emparejó.

Cuatro desenlaces, y cada uno se muestra distinto:

| Caso | Qué significa | Qué proponer |
| --- | --- | --- |
| fuente + sitio + canvas | Mapeo completo | Fila lista, sin marcas |
| fuente sin destinos | Aprobada pero no publicada | Fila con destinos vacíos |
| canvas sin fuente | Huérfana, o su fuente está por localizar | Fila marcada `sin fuente` |
| wireframes, `Canvas*.dc.html`, borradores del canvas | No son páginas de contenido | **Excluir por defecto**, listándolos aparte en una línea |

Los excluidos se nombran, no se ocultan: el usuario tiene que poder decir «ese sí entra».

**Propón y espera.** El usuario corrige, añade o descarta filas. No escribas la configuración antes
de su visto bueno.

## 4 · Escribir la configuración

Con la aprobación, escribe la sección `## Destinos de publicación` en `contexto/configuracion.md` —
**añadiéndola al archivo existente**, sin tocar lo que ya tenga. Formato:

```markdown
## Destinos de publicación

### Repo del sitio
ruta: /ruta/absoluta/al/repo
motor: nuxt-content
config_esquema: content.config.ts
espejo_disenos: htmls/

### Claude Design
project_id: <uuid>
nombre: <el que devolvió get_project>

### Mapeo de páginas
| Fuente | Sitio | Canvas desktop | Canvas móvil |
| --- | --- | --- | --- |
| clusters/ejemplo-copy.md | content/2.seccion/1.ejemplo.md | Ejemplo.dc.html | Ejemplo - Móvil.dc.html |

### Excluidos del chequeo
Wireframes, `Canvas.dc.html` — no son páginas de contenido.
```

**Lo pendiente se escribe como pendiente**, nunca se omite: una página sin fuente localizada va en
la tabla con la celda vacía y una nota, para que la próxima corrida la vuelva a plantear. Una
configuración que calla lo que no se resolvió es peor que una incompleta que lo dice.

## 5 · Continuar

Retoma el chequeo que estaba en curso cuando se disparó el onboarding. Configurar no es el
objetivo: era el trámite para responder lo que el usuario preguntó.

## Onboarding incremental

**No hace falta mapearlo todo para empezar a servir.** Si en una corrida posterior aparece una
página sin mapear —nueva en el canvas, nueva en el sitio—, repórtala y **ofrece añadirla** al
mapeo en una línea. Se acepta o se descarta ahí mismo, sin volver al modo completo.

Si lo que cambió es la estructura (una colección nueva en `content.config.ts`, una página del
canvas renombrada), dilo en una línea y ofrece poner al día la sección. **No la corrijas por tu
cuenta**: un renombre puede ser una página distinta, y solo el usuario sabe cuál.

## Errores

| Situación | Qué hacer |
| --- | --- |
| No se encuentra ningún `content.config.ts` | Pregunta la ruta del repo del sitio; no la adivines. |
| Hay varios repos candidatos | Muéstralos y que elija; no tomes el primero. |
| La URL de Claude Design no trae un uuid reconocible | Dilo y pide el enlace del canvas; no inventes el id. |
| `get_project` responde que no hay acceso | Dilo con el id probado, y menciona que el acceso de agentes a los proyectos de diseño puede requerir concederse una vez en el cliente (en Claude Code, `/design-consent`; se revoca con `/design revoke`). No lo ejecutes tú: es del usuario. |
| `configuracion.md` no existe | Créalo con la sección; si existe con otro nombre por convención antigua, resuélvelo por rol y ofrece migrar. |
| Una fuente empareja con dos destinos posibles | No elijas: muestra ambos y pregunta. |
