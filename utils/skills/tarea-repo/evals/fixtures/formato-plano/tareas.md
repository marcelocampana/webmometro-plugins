# Tareas

## Ahora

| Tarea | Sección | Estado | Inicio | Nota |
| --- | --- | --- | --- | --- |
| Alinear el contenido bajo «Sigue leyendo» con el diseño original | Componentes | Pendiente | — | — |

---

## General

| Estado | Tarea | Inicio | Completada | Duración | Comentarios |
| --- | --- | --- | --- | --- | --- |
| ✅ Completada | Corregir el enlace del logo a la página de inicio | 2026-07-17 17:55 | 2026-07-18 09:55 | ~1h 50m | El logo se movió a `public/images/` y `AppLogo.vue` pasó a `NuxtImg`; el home quedó en `site.url` como URL absoluta con `www`. **Esta app no sirve `/`** — el home vive en Wix, tras el proxy de Cloudflare —, así que un `to="/"` daba 404 tanto en el dominio como en local; por eso la URL absoluta y no una ruta relativa. Ningún asset debe quedar en la raíz de `public/`: no cae bajo ningún prefijo del proxy y no se sirve en el dominio. Se comprobó en producción mirando la cabecera `x-vercel-*`, porque `/favicon.ico` y `/blog` devuelven 200 desde Wix y un 200 no prueba que el prefijo esté enrutado. |

**Cerradas en esta sección: ~1h 50m**

---

## Componentes

| Estado | Tarea | Inicio | Completada | Duración | Comentarios |
| --- | --- | --- | --- | --- | --- |
| Pendiente | Alinear el contenido bajo «Sigue leyendo» con el diseño original | — | — | — | Afecta a dos páginas a la vez: el bloque vive en `RelatedCard`. |

---

## Los estados

Cinco, y no hay más: si una situación no cabe en uno de estos, va en la Nota o en Comentarios.

| Estado | Qué significa | Se entra cuando | Se sale cuando |
| --- | --- | --- | --- |
| `Pendiente` | Anotada y sin empezar. | Se anota la tarea. | Se crea su rama. |
| `🔵 En curso` | La que se está trabajando. | Se crea la rama y se anota el Inicio. | Se cierra o se interrumpe. |
| `Pausada` | Detenida por tiempo. | El usuario para sin cerrarla. | Se retoma o se cierra. |
| `Bloqueada` | Detenida por una dependencia. | Se descubre lo que falta. | Se resuelve la dependencia. |
| `✅ Completada` | Cerrada: commit hecho y fila rellena. | Las tres confirmaciones. | Nunca. Es terminal. |

---

## Cómo se llena esta lista

- **`## Ahora` es la prioridad, y la determina el usuario.** Sus filas son punteros.
- **Las secciones no se reordenan.** Dentro de cada una, lo abierto va arriba.
- **La columna Tarea es una línea.** El detalle va en Comentarios.
- **Inicio** es la creación de la rama y **Completada** su commit de cierre.
- **El total va por sección, no al pie del archivo.**
