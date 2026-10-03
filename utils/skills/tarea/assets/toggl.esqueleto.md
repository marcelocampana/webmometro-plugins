<!-- tarea: config toggl · la leen `tarea`, `agenda`, `balance` y `presencia.py` · vive fuera de todo repo -->

# Toggl

Configuración global de la integración con Toggl 2.0. **Se edita a mano**; los skills solo la leen.
Vive en `~/Github/AI-kit/config/context/toggl.md` (o donde diga `TOGGL_CONFIG`).

## Espacio de trabajo

| Clave | Valor |
| --- | --- |
| `workspace_id` | {{id del espacio de Toggl}} |
| `etiqueta_imprevisto` | imprevisto |

## Umbrales (minutos)

`presencia.py` lee esta tabla por nombre de clave; un valor que falte usa el de por defecto.

| Clave | Valor | Qué es |
| --- | --- | --- |
| `ausencia_min` | 10 | Sin teclado, mouse ni mensajes durante esto → ausente desde la última actividad |
| `sesion_min` | 90 | Sesión continua a partir de la cual se avisa de una pausa |
| `pausa_min` | 10 | Hueco que cuenta como pausa y corta la sesión |
| `repetir_aviso_min` | 30 | El aviso no se repite antes de esto |
| `notificar_mac` | 1 | 1: el aviso también sale como notificación de macOS, aunque no le escribas a Claude; 0: solo en la conversación |
| `proyecto_mi_tiempo` | 0 | Id del proyecto de Toggl donde iba tu tiempo frente al computador; ya no se envía (lo cronometras tú) |
| `imprevisto_min` | 30 | Claude trabajando más que esto en un repo sin tarea abierta: `balance` lo señala (ya no se ofrece crear nada en Toggl) |

## Registro de presencia

Carpeta: `~/.local/share/tarea/presencia/` (o `TAREA_PRESENCIA_DIR`). Un archivo por día; no se
versiona y no sale del Mac.
