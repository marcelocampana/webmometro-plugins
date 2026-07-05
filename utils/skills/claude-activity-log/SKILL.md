---
name: claude-activity-log
description: >
  Mantiene un registro (log) persistente y cross-cuenta de las tareas realizadas en Claude, para
  no perder el rastro de en qué cuenta, proyecto y contexto se hizo cada cosa. Úsalo cuando el
  usuario quiera "registrar lo que hice", "anotar esta tarea en el log", "actualizar el registro
  de trabajo", "llevar un historial de actividades", "qué hice en X proyecto", "en qué cuenta hice
  esto", "qué he trabajado últimamente" o "muéstrame el log". También aplica de forma proactiva al
  finalizar un plan de trabajo, completar una tarea significativa, cerrar una sesión, concluir un
  hito, o antes de cambiar de proyecto o de cuenta: en esos momentos ofrece registrar la actividad.
metadata:
  version: 1.1.0
---

# Registro de actividad cross-cuenta (claude-activity-log)

Este skill resuelve un problema concreto: el usuario trabaja con **dos cuentas distintas de
Claude** (p. ej. Observatorio del Cáncer y personal) y proyectos que se solapan entre ellas.
Después de unos días pierde el rastro de **en qué cuenta, proyecto y contexto** hizo cada tarea.
Un log único y compartido —que sobreviva al cambio de cuenta y de proyecto— resuelve esto.

La idea central: **un solo par de archivos compartidos** que todas las cuentas leen y escriben.
La cuenta nunca se adivina: se lee de un pequeño config por-cuenta.

## Ubicación del log (fija, no la cambies)

Todo el historial vive en una carpeta local compartida por las cuentas de este equipo:

```
/Users/marcelocampana/Documents/logs/claude-work-logs/
├── resumen.md    # Nivel 1: tabla consolidada. Una fila por tarea. Entradas nuevas ARRIBA.
├── detalle.md    # Nivel 2: un bloque por tarea, con algo más de contexto. Mismo id que la fila.
└── _README.md    # explica el sistema (créalo en el primer uso)
```

Esta ruta es **absoluta y hardcoded**: aunque el skill se copie a otro proyecto u otra cuenta,
siempre escribe aquí. Nunca crees una carpeta de logs dentro del proyecto de trabajo.

Define una variable mental al inicio de cada operación:

```
LOG_DIR="/Users/marcelocampana/Documents/logs/claude-work-logs"
```

Todas las cuentas de Claude de este Mac comparten esta carpeta, así el registro sobrevive al
cambio de cuenta y de proyecto.

## Identidad de cuenta

El nombre de la cuenta se lee de `~/.claude/ia-log-cuenta.md` (uno por cada cuenta/`~/.claude`):

```yaml
---
cuenta: Personal
---
```

- **Si el archivo existe**: usa el valor de `cuenta:`.
- **Si NO existe**: ve al **Modo 3** (inicializar config) antes de registrar. No inventes el nombre
  de la cuenta ni dejes el campo vacío.

## Marca de tiempo

Obtén siempre la fecha y hora **reales** con Bash, nunca las inventes:

```bash
date '+%Y-%m-%d %H:%M'
```

A partir de esa marca arma también el `id` de la entrada: `AAAA-MM-DD-HHMM-slug`, donde `slug` es
un kebab-case corto de la tarea (p. ej. `2026-06-22-1430-plan-logging`).

---

## Modo 1 · Registrar una actividad (por defecto)

Es la operación más común. Pasos:

1. **Resolver la cuenta**: lee `~/.claude/ia-log-cuenta.md`. Si falta → Modo 3 primero.
2. **Marca de tiempo + id**: corre `date '+%Y-%m-%d %H:%M'` y construye el `id`.
3. **Reunir los campos** (pregunta al usuario solo lo que no puedas inferir del contexto):
   - **Fecha y hora** — de `date`.
   - **Cuenta** — del config.
   - **Proyecto** — nombre de la carpeta de trabajo (p. ej. `cdz-content`) o el que indique el usuario.
   - **Tarea** — título corto.
   - **Descripción breve** — una frase para la tabla.
   - **Etiquetas** — 1 a 3 tags temáticos en kebab-case, separados por coma (p. ej. `seo, contenido`).
     Sirven para filtrar el historial por tema. Si no aplica, usa `—`.
   - **Enlaces/archivos** — archivos o URLs relevantes tocados en la tarea. Si no aplica, usa `—`.
   - **Estado** — uno de: `completado` · `en-progreso` · `bloqueado` · `pausado`.
   - **Siguiente paso** — qué queda pendiente para retomar. Si no aplica, usa `—`.
4. **Asegurar que el log existe**: si `resumen.md` o `detalle.md` no existen en `LOG_DIR`, créalos
   a partir de `assets/resumen.header.md` y `assets/detalle.header.md` respectivamente, y crea
   `_README.md` con una explicación breve del sistema.
5. **Escribir el resumen (Nivel 1)**: inserta una fila **justo debajo de la fila separadora de la
   tabla** (entradas nuevas arriba), con este orden de columnas:

   ```
   | Fecha y hora | Cuenta | Proyecto | Tarea | Descripción | Etiquetas | Estado | ID |
   ```

6. **Escribir el detalle (Nivel 2)**: añade al **inicio** de la sección de entradas de `detalle.md`
   un bloque con el formato de `assets/detalle.template.md` (mismo `id` como ancla `## `), con los
   campos **Etiquetas**, **Enlaces/archivos** y **Siguiente paso**, más 2–4 frases de qué se hizo y
   decisiones tomadas.
7. **Confirmar**: dile al usuario en una línea qué registraste y dónde (`claude-work-logs/`).

Mantén la consistencia: cada fila de `resumen.md` debe tener su bloque homónimo en `detalle.md`.

## Modo 2 · Consultar el historial

Cuando el usuario pregunte "qué hice", "en qué cuenta", "muéstrame el log", etc.:

1. Lee `resumen.md` de `LOG_DIR`.
2. Filtra por lo que pida: cuenta, proyecto, **etiqueta**, rango de fechas, o texto libre (busca en
   Tarea/Descripción/Etiquetas).
3. Devuelve una tabla compacta con las filas que coinciden.
4. Si pide el detalle de una entrada concreta, abre su bloque por `id` en `detalle.md` y muéstralo.

No reescribas los archivos en este modo: es solo lectura.

## Modo 3 · Inicializar el config de cuenta

Cuando `~/.claude/ia-log-cuenta.md` no existe:

1. Pregunta al usuario **una sola vez**: "¿Cómo quieres etiquetar esta cuenta en el log? (p. ej.
   `Personal`, `ODC`, `CDZ`)".
2. Tras su confirmación, crea `~/.claude/ia-log-cuenta.md` con el frontmatter `cuenta: <valor>`.
3. Continúa con el registro que estuviera en curso.

Usa etiquetas cortas y estables; deben ser las mismas cada vez para que el filtrado por cuenta
funcione.

---

## Cuándo registrar (disparadores)

Ofrece registrar —en una línea, para que el usuario confirme— en estos momentos. No escribas
silenciosamente; el log vive fuera del repo de trabajo, así que confirma primero.

1. Al **finalizar un plan de trabajo**.
2. Al **completar una tarea significativa**.
3. Al **cerrar una sesión** de trabajo.
4. **Antes de cambiar de proyecto o de cuenta**.
5. Al **concluir una etapa o hito** importante.

Detalle y matices en `references/momentos-registro.md`.

## Idioma

Comunícate con el usuario en **español neutro**. Los nombres de archivo, claves de frontmatter
(`cuenta`, `id`), el `slug` del id y las `etiquetas` van en minúsculas/kebab-case. Respeta tildes y
caracteres especiales en todo el texto.
