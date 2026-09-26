---
name: tarea
description: >
  Entrada del sistema de tareas del usuario: entiende qué va a hacer, decide el carril y delega en el
  skill específico. Úsalo cada vez que el usuario hable de una tarea o de su trabajo pendiente: "qué
  sigue", "empiezo X", "anota esto", "haz lo siguiente", "listo, ya está", "pausa", "qué tengo
  abierto", "crea una tarea", "tengo que facturar", "estuve en una reunión", o cuando pase un archivo
  o una conversación de la que extraer tareas. **Carril repositorio** (`tarea-repo`): trabajo que
  cambia archivos de un repo con `tareas/` y termina en commit. **Carril suelto** (`tarea-suelta`):
  tareas que no viven en ningún repo —facturar, reuniones, llamadas, trámites—, registradas solo en
  Toggl, sin git. Si no está claro, hace una sola pregunta. NO lo uses para la vista de hoy (eso es
  `agenda`), para planificar la semana (`plan-semanal`) ni para revisarla (`balance`), ni para TODOs
  efímeros de la sesión.
argument-hint: "[lo que el usuario quiere hacer]"
metadata:
  version: 3.0.0
---

# Tareas: la entrada (tarea)

El usuario no debería tener que saber qué skill se encarga de qué. Dice lo que va a hacer; este
skill decide **por dónde va** y pasa el control. **No gestiona tareas él mismo**: es un desvío corto.

## Los dos carriles

| | `tarea-repo` | `tarea-suelta` |
| --- | --- | --- |
| **Qué** | Trabajo que cambia archivos de un repo y termina en commit | Todo lo demás que requiere tiempo: facturar, reuniones, llamadas, trámites, revisar algo fuera de un repo |
| **Dónde vive** | `tareas/` del repo (y en Toggl si el repo está conectado) | Solo en Toggl |
| **Ceremonia** | Rama, commit, merge, historial | Empezar y terminar; sin git |
| **Quién la hace** | Casi siempre Claude | El usuario, o Claude si se lo delega |

Los dos miden igual: marcas locales en `presencia.py`, tramos recortados por la presencia real y
envío a Toggl en bloque al terminar. Lo que cambia es solo si hay git.

## Cómo decidir

En este orden; la primera que responda, manda:

1. **El usuario lo dice** («es de repo», «no va en ningún repo») → ese carril.
2. **Es una tarea que ya existe**: si está en el `tareas.md` del repo actual → `tarea-repo`; si
   aparece en `presencia.py abiertas --repo suelta` o es una tarea de Toggl con la etiqueta `suelta`
   → `tarea-suelta`.
3. **El trabajo va a cambiar archivos de un repo que tiene `tareas/`** y es para commitear
   (código, contenido, configuración, documentación) → `tarea-repo`.
4. **No toca ningún repo**: una reunión, una llamada, facturar, responder correos, un trámite,
   algo que el usuario hace fuera de Claude → `tarea-suelta`.
5. **No está claro** → **una sola pregunta**, corta: «¿Esto termina en un commit en algún repo, o
   es trabajo suelto?». No se adivina.

**Consultas generales** («qué tengo abierto», «qué sigue»): se miran los dos carriles —`tareas.md`
del repo actual, si lo hay, y `presencia.py abiertas --repo suelta`— y se responde en una sola
lista. Para la vista de todos los proyectos, se remite a `agenda`.

## Cuando una tarea cambia de carril

- **Una suelta que empieza a producir commits** (Claude va a automatizar la facturación con un script
  en un repo): se cierra la suelta con lo medido y se crea la de repo, con visto bueno. No se mezclan.
- **Una de repo que resulta no necesitar commit** (era solo investigar): se cierra en su repo como
  siempre; `tarea-repo` sabe cerrar sin cambios de código.

## Después de decidir

Se invoca el skill del carril con lo que dijo el usuario, sin repetirle nada ni anunciar el desvío
con más de media línea («Va por el carril suelto»). Las reglas, los estados y los tiempos son de
cada carril: este archivo no los duplica.

La infraestructura común vive aquí: `scripts/presencia.py` (presencia, marcas, tramos, plan) y
`assets/` (instalación del registro y del gancho, y la configuración global de Toggl).

## Idioma

Español neutro. Los nombres de las tareas, tal cual.
