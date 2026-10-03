<!-- tarea: plan · repo {{repo}} · rama {{slug}} · área {{Área}} · coste ~{{estimación}} -->
<!-- Lo que el plan del modo plan lleva además de su propio texto. Hay un solo plan: el que guarda
     Claude Code en ~/.claude/plans/ (sin modo plan, Claude lo escribe ahí como <slug>.md). No se
     copia al repo. El marcador de la primera línea lo encuentra (mod avance-del-plan,
     pendientes.py); se completa al abrir la rama. -->

# {{Objetivo}}

## Estado

Van 0 de {{N}} pasos. Sigue: {{primer paso}}. Espera de ti: {{una decisión, o «nada por ahora»}}.

{{El texto del plan, como lo escribe el modo plan.}}

## Pasos

| # | Paso | Skill | Contexto | Hecho |
| --- | --- | --- | --- | --- |
| 1 | {{verbo + resultado revisable}} | {{plugin:skill, o «ninguna»}} | {{lo que se lee antes}} | |

## Esto te toca a ti

<!-- Solo lo que Claude no puede hacer y que te ocupa tiempo. Eliges qué va a Toggl («la 1 y la 3»);
     las decisiones no van aquí: se piden en el momento. Bórrala si no hay nada. -->

1. {{Validar el copy con la clínica}} (~{{30 min}}) — {{por qué no lo hace Claude}}

## Notas

<!-- Decisiones tomadas sobre la marcha y desvíos del plan, una línea cada uno. -->
