# Cuándo registrar — los cinco disparadores

El valor del log depende de la **consistencia**: si solo se registra "a veces", se vuelve a perder
el rastro. Estos cinco momentos son los puntos donde Claude debe **ofrecer registrar** (en una
línea, para que el usuario confirme). No se escribe silenciosamente porque el log vive fuera del
repo de trabajo.

## 1. Al finalizar un plan de trabajo

Cuando se aprueba/termina un plan o se completa la última de sus tareas. Registra el plan como una
entrada: qué se planificó y qué quedó hecho. Estado típico: `completado` o `en-progreso` si el plan
continúa en otra sesión.

## 2. Al completar una tarea significativa

No toda microacción merece entrada — solo lo "significativo": un artículo publicado, un análisis
entregado, un skill creado, un bug resuelto, un reporte generado. Regla práctica: si dentro de una
semana querrías poder recordar que lo hiciste, regístralo.

## 3. Al cerrar una sesión de trabajo

Si la sesión produjo trabajo relevante y aún no se registró, ofrece un cierre: una entrada que
resuma lo principal de la sesión. Útil cuando se hicieron varias cosas pequeñas que en conjunto sí
importan.

## 4. Antes de cambiar de proyecto o de cuenta

Este es el disparador **más importante** para el problema original: el cambio de cuenta/proyecto es
exactamente cuando se pierde el contexto. Antes de saltar, deja registrado dónde quedó el trabajo
actual (estado `en-progreso` o `pausado` si no terminó).

## 5. Al concluir una etapa o hito importante

Hitos de proyecto más grandes que una sola tarea: cerrar un clúster de contenido, terminar una
auditoría completa, lanzar una sección del sitio. Estado típico: `completado`.

---

## Qué NO registrar

- Conversaciones exploratorias sin entregable.
- Lecturas o búsquedas que no derivaron en una acción concreta.
- Pasos intermedios de una tarea que se registrará completa al final.

## Cómo ofrecerlo

Una sola línea, sin fricción. Ejemplo:

> "¿Registro esto en el log de actividad (cuenta Personal · proyecto cdz-content)?"

Si el usuario acepta, ejecuta el **Modo 1** del skill. Si no, sigue sin escribir.
