---
name: seo-change-tracker
description: >
  Registra cambios SEO para hacerles seguimiento de impacto, y de forma secundaria mide checkpoints
  y genera reportes ejecutivos. El trigger primario es que **ocurra un cambio real** que afecta o
  podría afectar el posicionamiento SEO/AEO — en el contenido, la estructura/arquitectura, el
  código/técnico, on-page, enlaces, schema, performance o el perfil local/GBP. Actívate en cuanto el
  usuario **describa o mencione haber implementado** uno de esos cambios (cambiar un title o meta
  description, un redirect o canonical, publicar/expandir contenido, link building, schema, un cambio
  en Google Business Profile), aunque no diga literalmente "regístralo" — y ofrécele registrarlo para
  poder medir su efecto después. También úsalo cuando pida explícitamente "registrar un cambio SEO",
  "documentar una optimización", "llevar un historial de lo que hemos hecho en SEO"; cuando (acción
  secundaria) quiera "medir el impacto de una acción SEO", "generar un reporte ejecutivo de SEO",
  "saber qué cambios han dado resultado"; o cuando pregunte "qué deberíamos medir" o "cómo llevamos el
  control de nuestros cambios SEO" — ahí propone el modelo de seguimiento. Generar un reporte NO es
  registrar: es una lectura agregada de lo ya registrado.
---

# Seguimiento estructurado de cambios SEO

Este skill resuelve un problema específico: cuando se hacen varios cambios SEO a lo largo del
tiempo, es difícil saber después **cuál de ellos generó qué resultado** — el impacto en SEO es
diferido y rara vez hay un solo cambio a la vez. Un log cronológico plano no alcanza, porque no
ofrece un "antes" comparable contra el "después" de cada cambio puntual.

La idea central: cada cambio es una **nota con su propio baseline** (las métricas en el momento en
que se implementó) y sus propios **checkpoints de seguimiento** (mediciones posteriores, típicamente
a 14 y 28 días). El reporte ejecutivo es solo una lectura agregada de esas notas — no hay una
recolección de datos separada del registro.

## Ubicación en el workspace del cliente

Este skill opera en el **proyecto activo del cliente** (su vault o repo), no en el repo del plugin.
Resuelve la raíz del cliente subiendo desde el directorio activo hasta encontrar una carpeta
`contexto/`. El seguimiento de cambios SEO es **verdad compartida cross-plugin** (lo leen los skills
analíticos de SEO y brand-voice-pro), así que vive en `contexto/`, continuo y **sin período** (a
diferencia de `web/seo/datos/{periodo}/` e `informes/{periodo}/`, que sí se versionan):

```
contexto/seo-tracking/
├── cambios/     # una nota por cambio: AAAA-MM-DD-slug.md
└── reportes/    # reportes ejecutivos generados
```

**Resolver flexible:** si el proyecto usa una ubicación antigua (un `seo-tracking/` en la raíz del
proyecto, un `reportes/…` legado, u otra), resuélvela por rol y **ofrece migrarla** a
`contexto/seo-tracking/` — no asumas un nombre fijo ni falles si no existe todavía.

## Configuración: se lee de `contexto/`, no se duplica

El dominio y los identificadores de propiedad (GSC, GA4, ubicación/idioma para SERP) son verdad
compartida y viven una sola vez en `contexto/configuracion.md` (IDs GA4/GSC/Clarity/DataForSEO +
URLs). Léelos **por puntero** desde ahí; nunca los copies a una config propia del tracker. Si el
proyecto guarda esos datos con nombres/ubicaciones antiguas, resuélvelos por rol y ofrece migrar. Si
`contexto/configuracion.md` no existe todavía, dilo y ofrece crearlo (vía `site-context` /
`site-snapshot`) antes de capturar baselines, en vez de inventar una config paralela.

Lo único propio del tracker es la cadencia de checkpoints (`checkpoint_dias`, default `[14, 28]`).
Ese default vive en este skill; si un cliente necesita otra cadencia por defecto, puede fijar
`checkpoint_dias_default` en `contexto/configuracion.md` — sin repetir jamás los IDs.

## Confirmación obligatoria

**Este skill nunca escribe nada sin confirmación explícita del usuario.** Toda acción que crea o
modifica archivos —crear una nota de cambio, agregar un checkpoint, generar un reporte, migrar un
layout legado, o crear/editar `contexto/configuracion.md`— se **propone primero** (mostrando qué se
va a escribir y dónde) y solo se ejecuta tras el OK del usuario. El skill aporta el dato y una
lectura inicial; el juicio final y la autorización son del usuario.

El esquema completo de una nota de cambio (campos, vocabularios, sub-objetos de métricas) está en
**`references/esquema-cambio.md`** — consúltalo siempre antes de escribir o editar una nota, para no
inventar campos ni vocabularios distintos a los ya establecidos.

## Modo 1: Registrar un cambio

Cuando el usuario describe algo que implementó o va a implementar (este es el uso primario del
skill):

1. **Identifica los campos básicos** a partir de lo que diga: `area`, `tipo`, `target_url`,
   `keywords`, `descripcion`. Si falta algo obvio, pregunta — pero no interrogues por cada campo si
   el contexto ya lo deja claro. Si el cambio **viene por hand-off de otro skill** (`seo-audit`,
   `page-cro`, `ai-seo`, `brand-voice-enforcement`), captura también el slug de la acción de origen
   en `accion_origen` — habilita el match determinista de la rutina de reconciliación.
2. **Pide la hipótesis** si el usuario no la dio espontáneamente ("¿qué esperas que pase con este
   cambio?"). Es el campo más importante del registro: sin una expectativa explícita, no hay forma
   de juzgar después si el cambio "funcionó" o no — cualquier resultado parecería un éxito a
   posteriori.
3. **Captura el baseline** consultando las herramientas MCP que correspondan al área del cambio,
   según el mapeo en **`references/areas-seguimiento.md`**. Usa la propiedad/dominio de
   `contexto/configuracion.md`. Límite de ejecución MCP: consulta **solo las fuentes del área del
   cambio**, no todas. Si una fuente no está disponible (servidor MCP no configurado, error de
   permisos, etc.), no bloquees el registro: deja ese campo en `null` y dilo explícitamente al
   usuario, ofreciendo que lo complete a mano si lo tiene.
4. **Propón y, tras confirmación, crea el archivo** `contexto/seo-tracking/cambios/AAAA-MM-DD-slug.md`
   a partir de `assets/cambio.template.md`, con `estado: implementado` si el cambio ya está hecho o
   `planificado` si todavía no. En cuanto el baseline quede capturado, pasa a `estado: midiendo`.
5. **Confirma al usuario** con un resumen corto: qué quedó registrado, qué baseline se capturó (o
   qué faltó) y cuándo corresponde el próximo checkpoint (`checkpoint_dias` desde la fecha del
   cambio, default `[14, 28]` salvo que `contexto/configuracion.md` diga otra cosa).

## Modo 2: Medir / actualizar seguimiento

Cuando el usuario pide revisar el resultado de un cambio, o tú detectas que conviene proponerlo
(por ejemplo, al abrir una nota en `estado: midiendo` cuyo checkpoint ya venció):

1. Localiza la nota correspondiente en `contexto/seo-tracking/cambios/`.
2. Vuelve a consultar **las mismas fuentes MCP, con la misma ventana de tiempo y los mismos
   filtros** que se usaron en el baseline — si no son comparables, el delta no significa nada.
3. Agrega un objeto a `checkpoints` con la fecha, los días transcurridos y las métricas nuevas.
4. Calcula el delta frente al baseline y **propón** un `resultado` (`positivo`, `neutral`,
   `negativo`, `inconcluso`) explicando el por qué en una frase, contrastándolo con la `hipotesis`
   original. No lo escribas como definitivo sin que el usuario lo confirme — el juicio de qué cuenta
   como "buen resultado" es del usuario, tú aportas el dato y una lectura inicial.
5. Si ya se cumplieron todos los `checkpoint_dias` y el usuario está conforme con el veredicto, pasa
   `estado: concluido`.

## Modo 3: Generar reporte ejecutivo

Usa **`scripts/generar_reporte.py`** — no redactes el reporte a mano, el script ya calcula deltas y
ordena por impacto de forma consistente:

```bash
python3 "<ruta-del-skill>/scripts/generar_reporte.py" contexto/seo-tracking/cambios \
  --desde 2026-06-01 --hasta 2026-06-30 \
  --cliente "Clínica Dra. Zaror" \
  --output contexto/seo-tracking/reportes/reporte-2026-06.md
```

- `--desde`/`--hasta` son opcionales: si el usuario dice "este mes" o "las últimas dos semanas",
  calcula tú las fechas concretas antes de llamar al script.
- Si el script no puede ejecutarse (entorno sin Python, etc.), la estructura a seguir manualmente
  está en `references/plantilla-reporte.md`.
- Después de generar el reporte, **léelo y preséntalo en la conversación** (no solo digas "listo,
  está guardado") — el usuario quiere la lectura ejecutiva ahí mismo, el archivo es para que quede
  guardado en el vault.
- Si hay reportes o datos crudos relacionados ya existentes en el proyecto (`web/seo/datos/{periodo}/`,
  `web/seo/informes/{periodo}/` — GSC, GA4, SERP), enlázalos desde el reporte con `[[wikilinks]]` si
  el formato del vault los usa.

## Rutina de reconciliación (recordatorio de ejecución)

Como red de seguridad para que ningún cambio recomendado se pierda sin registrar, existe una rutina
programable que cruza las acciones propuestas por los informes SEO contra los cambios registrados y
entrega un digest "estado de ejecución SEO" (hecho / pendiente / a medir). Su lógica y la plantilla
para crearla por cliente (con la skill `schedule`) están en **`references/rutina-reconciliacion.md`**.
Respalda —no reemplaza— la auto-activación y el hand-off entre skills, y también respeta la
confirmación obligatoria: propone, no escribe.

## Errores y casos límite

| Situación | Qué hacer |
|---|---|
| No existe `contexto/seo-tracking/` todavía | Proponer crearlo (previa confirmación) antes de registrar el primer cambio; la config se lee de `contexto/configuracion.md`, no se crea una config local |
| No existe `contexto/configuracion.md` | Decirlo y ofrecer generarlo vía `site-context`/`site-snapshot` antes de capturar baselines; no inventar una config paralela |
| Existe un `seo-tracking/` legado en la raíz del proyecto | Resolver por rol y ofrecer migrarlo a `contexto/seo-tracking/`; no fallar |
| Una fuente MCP no está disponible | Registrar el campo como `null`, decirlo explícitamente, ofrecer ingreso manual |
| El usuario pide un reporte sin haber registrado cambios | Decirlo claramente y ofrecer registrar el primero, en vez de generar un reporte vacío sin avisar |
| Cambio que afecta varias áreas a la vez | Clasificar por el área predominante en `area`, pero capturar métricas de todas las áreas afectadas en el baseline |
| El usuario pide cambiar el vocabulario o esquema | Es válido evolucionar el esquema, pero avisa que las notas anteriores no tendrán los campos nuevos — no reescribas notas viejas sin que el usuario lo pida |

## Idioma

Comunícate con el usuario en español neutro. El contenido de las notas (descripciones, hipótesis)
se escribe en el mismo idioma en que el usuario describe el cambio.
