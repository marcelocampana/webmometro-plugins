# El informe

Ocho secciones, en este orden. **Una sección sin datos no sale**, y se nombra al pie en una línea
(«sin registro de presencia: faltan tu tiempo, salud y aplicaciones»).

## 1. Tiempo de proyecto

De Toggl: horas por cliente y por proyecto, y por sección (etiqueta) si aporta. Frente al período
anterior, solo si hay datos de los dos: «ODC 6h (+2h)». Los registros sin proyecto se cuentan aparte.

## 2. Tu tiempo

De `resumen`: total del período, promedio por día trabajado, y **a qué proyecto fue tu atención**
(`atencion`: cada minuto presente va al último proyecto al que le escribiste). Si el tiempo de
proyecto supera al tuyo, el paralelo se dice con su factor: «30h de proyecto con 18h tuyas: 1,7×».

## 3. Plan contra realidad

De `presencia.py plan comparar --semana AAAA-Www`: el plan **original** de la semana (el del lunes,
aunque después se replanificara) frente a lo medido.

- **Cumplimiento:** tareas cerradas a tiempo de las planificadas («6 de 9») y horas planificadas
  frente a horas reales en esas tareas.
- **Porcentaje planificado** (`porcentaje_planificado`): del tiempo medido en tareas, cuánto fue en
  tareas del plan. **Es el número del criterio de las 4 semanas**: se muestra junto al de las
  semanas anteriores, si las hay, para ver si sube.
- **Lo que desplazó el plan:** las tareas `fuera_de_plan` con más tiempo, dos o tres, por nombre.
- **Sin plan esa semana** (`hay_plan: false`): una línea, sin reproche. «Sin plan esta semana».

Solo cuenta tiempo medido en local; los imprevistos sueltos de Toggl entran en la sección 4.

## 4. Planificado contra imprevisto

Registros con la etiqueta de imprevistos (`toggl.md` de la configuración global) frente al total de
tiempo de proyecto, en porcentaje. Si pasa de un tercio, se dice qué proyecto concentra lo imprevisto.

## 5. Estimación

De los historiales: las filas cerradas en el período con `Coste` **y** `Duración` medida (sin `~`),
agrupadas por **familia** (verbo + objeto, igual que `tarea/references/estimacion.md`). Por familia,
la **mediana de las razones** Duración ÷ Coste:

- 0,8–1,25: «estimas bien las de X».
- Fuera de ese rango, el sesgo en palabras: «subestimas las de alinear con el diseño: tardan 2×».
- Con menos de 3 muestras en una familia, no se enuncia sesgo: se dice que la base es corta.

**Dos errores que no se corrigen con el mismo número**: esfuerzo (`Coste` → `Duración`, horas de
trabajo) y calendario (`Vence` → `Completada`, días de reloj, que en realidad mide capacidad). Si
hubo tareas con `Vence`, se dice aparte cuántas llegaron tarde; nunca se mezcla con el sesgo de
esfuerzo.

## 6. Qué optimizar

Las familias con más tiempo acumulado **y** al menos 3 apariciones: son las candidatas a automatizar,
a plantilla o a un skill. Una línea por candidata, con su tiempo y cuántas veces apareció. Si
`claude` muestra que Claude ya las hace solo casi enteras, se dice: ya están automatizadas en la
práctica.

Se ofrece llevarlas a `revisar.md` («¿las anoto en revisar.md de plugins?»); con el sí, se remite a
`tarea` en ese repo. Este skill no escribe.

## 7. Salud

De `resumen`: horas frente al computador por día (máximo y promedio), **sesión continua más larga**
(`sesion_max_min`), número de pausas y días trabajados. Trabajo fuera de horario: minutos antes de
las 8:00 o después de las 20:00, si los hay. Con un día de más de 9h o una sesión de más de 3h, una
línea sin sermones: «el miércoles: 4h 10m seguidas».

**Aplicaciones**: horas por aplicación (`apps`), las 5 primeras, y cuánto de eso cayó dentro de un
tramo con tarea abierta. «Slack 3h, casi todo fuera de tareas» dice más que el total.

## 8. Claude solo

De `claude`: horas que Claude trabajó sin el usuario presente, por proyecto (`solo`). Es trabajo que
no costó atención: sirve para ver qué ya delega bien. **No se suma a nada.**

## Plantilla

```text
Balance · 15 al 21 de septiembre

Proyecto    ODC 6h (+2h) · Webmómetro 4h 30m · Plugins 2h
Tu tiempo   9h 20m en 5 días · atención: Webmómetro 45%, ODC 40% · 1,3× en paralelo
Plan        6 de 9 a tiempo · 62% del tiempo en tareas del plan (semana anterior 48%)
Imprevisto  22% del tiempo de proyecto
Estimación  estimas bien las de «Corregir»; subestimas las de «Alinear con el diseño» (2×, 5 casos)
Optimizar   «Aplicar correcciones médicas»: 3h 10m en 6 veces → candidata a plantilla
Salud       máx. 6h 40m el jueves · sesión más larga 2h 50m · 3 pausas por día
Apps        Claude 5h · Chrome 2h · Slack 1h, casi todo fuera de tareas
Claude solo 4h 30m mientras no estabas (Webmómetro 3h)

⚠ sin datos de Toggl para ODC antes del miércoles
```
