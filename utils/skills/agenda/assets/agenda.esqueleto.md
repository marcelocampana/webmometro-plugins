<!-- agenda: config · la lee el skill `agenda` (plugin utils) · vive fuera de todo repo -->

# Agenda

Registro de repos y capacidad diaria. **Este archivo se edita a mano**; la agenda solo lo lee, salvo
cuando el usuario le pide crearlo o cambiarlo.

Ubicación esperada: `~/Documents/config/claude/agenda.md`, o `~/.claude/agenda.md`. La variable
`AGENDA_CONFIG` tiene prioridad sobre las dos.

## Capacidad

Horas de **trabajo** al día —las mismas unidades que `Coste` y `Duración` en `task-flow`, con las
pausas fuera—, no horas de calendario. Es **una sola cifra para el día**, no una por repo: el día no
se multiplica por tener tres proyectos.

| Día | Capacidad |
| --- | --- |
| Por defecto | 4h |
| Sábado | 1h |
| Domingo | 0 |

Vale más ponerla baja y que sobre. Una capacidad optimista produce agendas que no se cumplen, y a las
dos semanas la vista deja de leerse.

## Repos

**El orden de esta tabla es la prioridad entre repos**, y es lo único que la agenda sabe del reparto
del día: recorre los repos de arriba abajo y toma cada cola desde su primera fila. No hay más señal
que esta, así que el primero de la lista debería ser el que más pesa hoy.

| Etiqueta | Ruta |
| --- | --- |
| clientes | ~/Projects/cliente-principal |
| plugins | ~/Documents/config/claude/webmometro-plugins |

- **La etiqueta es lo que se ve en la agenda**: corta, reconocible, sin ruta.
- **La ruta apunta al repo**, no a su `tareas/`. Si falta ese directorio, la agenda lo dice y sigue.
- **Un repo archivado se borra de aquí.** Mientras esté, sus pendientes compiten por el día todas las
  mañanas, y esa es la vía rápida a que la agenda deje de ser creíble.
- `~` se expande, y una **ruta relativa se resuelve respecto a este archivo** —no respecto al
  directorio desde el que se invoque la agenda, que puede ser cualquiera.

## Lo que no va aquí

- **Conectores y fuentes externas.** La agenda lee archivos y nada más; lo que venga de fuera lo pide
  la rutina que la dispara, por su cuenta.
- **Estados, costes o fechas de ninguna tarea.** Esos viven en el `tareas.md` de su repo, una sola
  vez. Duplicarlos aquí garantiza que un día discrepen.
