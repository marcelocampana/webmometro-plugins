<!-- tarea: plan · toggl:16667649 · rama bandeja-y-tiempo-claude-locales -->
<!-- El plan es el registro de Claude: sus pasos no van a Toggl. Se acuerda con el usuario antes de
     empezar, Claude lo lee al retomar y lo completa al cerrar. El usuario solo lee «Estado». -->

# Pasar bandeja y tiempo de Claude a archivos locales

## Estado

Van 6 de 7 pasos. Sigue: el cierre, con tu aprobación del merge tras ver el resultado. Te toca:
aprobar el merge y decidir sobre la rutina `enviar-claude-sin-tarea`.

## Pasos

| # | Paso | Skill | Contexto | Hecho |
| --- | --- | --- | --- | --- |
| 1 | `presencia.py asentar` escribe el tiempo de Claude en `~/Obsidian/global/claude/registro-tiempo/<proyecto>-AAAA-MM.md`; fuera el envío a Toggl; tests | ninguna | `tarea/scripts/presencia.py`, `test_presencia.py` | Hecho: 47 pruebas en verde; `asentar` regeneró 264 tramos en 11 archivos; totales de la semana 22–28 iguales al cálculo anterior (±4 s) |
| 2 | `tarea`: nada de Claude va a Toggl (SKILL, ciclo, assets, `cola.py`) | ninguna | `tarea/references/ciclo.md` | Hecho: cierre = tramos → asentar → Done; `etiqueta_claude` fuera del esqueleto |
| 3 | `tarea-repo`: `por-revisar.md`, `para-claude.md`, `modo-revisar`, `modo-claude`, migración y referencias | ninguna | `tarea-repo/references/` | Hecho: `modo-revisar` reescrito, `modo-claude` nuevo, esqueletos; migrador con 15 pruebas en verde |
| 4 | `balance`, `agenda`, `plan-semanal` leen las fuentes nuevas | ninguna | `balance/references/informe.md` | Hecho: balance, agenda (aviso «Claude tiene N pendientes») y plan-semanal |
| 5 | Datos reales: `~/Obsidian/global/`, primer `asentar`, bandeja de Toggl a archivos (con tu sí) | ninguna | `cola.py` | Hecho: `~/Obsidian/global/` creado; ninguna tarea con `por-revisar` en Toggl (33 revisadas): nada que migrar |
| 6 | `CLAUDE.md`, manifests 5.0.0, versiones de skills y evals | ninguna | `CLAUDE.md` § versiones | Hecho: 5.0.0 en ambos manifests; tarea 5.0.0, tarea-repo 5.0.0, balance 1.6.0, agenda 2.1.0, plan-semanal 2.0.4; 2 evals nuevas |
| 7 | Cierre con tu aprobación: historial, commit, merge y push | utils:tarea-repo | `modo-gestion.md` | |

## Lo que te toca (subtareas en Toggl, las cronometras tú)

- Nada.

## Notas

- Plan aprobado el 2026-09-29 (`~/.claude/plans/haz-el-plan-de-functional-spindle.md`). Git de la
  bandeja: commit directo y acotado sobre la destino, solo `por-revisar.md` y `para-claude.md`.
- El asignado en Toggl es el `user_account_id` (1156150), no el `id` de `users list` (9360555).
- En Toggl el proyecto se llama «Plugins IA», con cliente «Interno» (762706); el marcador de
  `toggl.md` decía «Plugins de IA» · «Webmómetro». Se corrige, porque el nombre del archivo de tiempo
  sale del marcador.
- «Solo» queda en `—` los días sin registro de presencia (antes del 26-09): no se puede afirmar.
- Los trocitos que deja cortar un tramo por una tarea se cuentan (antes se perdían 4½ min en la semana).
- El agente de launchd ya corre el código nuevo (apunta al repo): hizo el primer asiento solo, a las 21:18.
