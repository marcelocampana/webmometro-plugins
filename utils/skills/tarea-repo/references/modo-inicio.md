# Modo 0 · Inicio: montar el sistema y seccionarlo

Se invoca con `--init`, o cuando el Paso 0 no
encuentra `tareas/` y el usuario pidió algo de tareas.

Dos vías de entrada, mismo flujo:

- **Explícita**: `--init`, «monta el sistema de tareas», «crea la lista de tareas».
- **Detectada**: el usuario pide una operación de tareas y no existe `tareas/`. Dilo en una línea y
  ofrece montarlo. **Solo ante una petición de tareas** — nunca en medio de otro trabajo.

El trabajo real es **proponer el seccionamiento**, no crear archivos vacíos:

1. **Contextualizar** (ver `contextualizacion.md`): qué es el proyecto, su estructura, su deuda
   declarada, `git log`, y lo que el usuario acabe de pedir.
2. **Derivar las secciones** de tres fuentes a la vez: las **tareas que el usuario ya nombró**, la
   **estructura y el contexto del proyecto**, y las **tareas que tú sugieras** en esa primera pasada.
   Dos criterios: **una sección se gana su sitio** (si solo va a tener una fila, va en `General`), y
   el **orden es lógico y estable** —lo transversal primero (`General`, código compartido), luego las
   áreas concretas—, porque después **las secciones no se reordenan**. Detalle y tabla de derivación
   por tipo de proyecto en `references/seccionamiento.md`.
3. **Proponer en una tabla corta** —sección, qué abarca, cuántas semillas— y esperar. El usuario
   añade, quita o renombra.
4. **Crear** `tareas/` con los cuatro archivos desde `assets/tareas.esqueleto.md`,
   `assets/revisar.esqueleto.md`, `assets/auditoria.esqueleto.md` y `assets/secciones.esqueleto.md`,
   sembrar las tareas acordadas con su enunciado ya afinado **y una entrada por cada sección
   acordada en el catálogo** (con su ámbito, aunque no tenga semillas todavía), y ofrecer dos extras
   **en una línea cada uno**: el bloque para `CLAUDE.md` (`assets/claude-md-puntero.md`) y sembrar el
   historial de tareas ya cerradas desde `git log`, marcado con `~`.

Las cuatro piezas se crean juntas aunque alguna nazca vacía: existir es lo que las hace usables desde
la primera sesión. Se crea también `tareas/historial/` (vacío) y se **anota el umbral** en la
cabecera de `tareas.md` — el esqueleto ya trae la línea; ajústala al tamaño del proyecto
(`archivado.md`).

**Variante: migrar un `tareas.md` plano.** Si el Paso 0 encontró el formato antiguo, el trabajo no es
proponer secciones —ya las tiene— sino mover el archivo y completar el resto. Con el visto bueno:
`git mv tareas.md tareas/tareas.md` (con `git mv`, para no perder el historial del archivo), crear
`revisar.md` y `auditoria.md` desde sus esqueletos, y **`secciones.md`** poblado leyendo los headers
`##` ya existentes en el `tareas.md` migrado (con ámbito inferido de su contenido si no hay uno
explícito) — y **no tocar el contenido existente**: ni las secciones, ni los totales, ni el
historial. Si el archivo trae las convenciones antiguas al pie —la tabla larga de estados y el «cómo
se llena esta lista»—, **ofrece** sustituirlas por la leyenda breve del esqueleto, porque ahora viven
en el skill; pero solo si el usuario acepta.

Si el archivo migrado trae comentarios largos en sus filas cerradas, **ofrece archivarlos** en el
mismo paso (`archivado.md`): es donde está casi todo el peso de un `tareas.md` heredado. Si además
trae filas ya `✅ Completada` conviviendo en sus secciones, **ofrece archivarlas de inmediato** con
el mecanismo nuevo, en el mismo paso — es la oportunidad de dejar el `tareas.md` migrado ya limpio
desde el primer día.

**Si en cambio el proyecto ya tiene `tareas/` pero alguna convención de formato quedó antigua** (sin
`secciones.md`, leyenda de estados en una línea, archivado por antigüedad en vez de inmediato), no es
esta variante: es `modo-actualizacion.md` (`--actualizar`).
