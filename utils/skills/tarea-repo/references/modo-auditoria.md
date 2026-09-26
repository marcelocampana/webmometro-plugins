# Modo 3 · Revisión completa (`--auditoria`)

Solo bajo petición explícita. Recorre el proyecto **por áreas** y propone para `auditoria.md` lo que
sea recomendable para completarlo, con la condición que define el modo: **solo tareas que no estén ya
en ninguna de las otras dos listas**. Antes de escribir, contrasta contra `tareas.md` —abiertas **y
cerradas**, que el historial cuenta— y contra `revisar.md`.

**Áreas: el checklist base + las propias del proyecto** (en un sitio, SEO y OG; en un repo de plugins,
sincronía de manifests). El checklist completo, con la evidencia que hace válida cada fila, está más
abajo en este archivo.

Columnas: `Tarea | Área | Severidad | Motivo`, severidad `alta | media | baja`. El **Motivo cita
evidencia concreta** —archivo y línea, o el comando que lo delata—. Una fila sin evidencia no se puede
evaluar: **no la escribas**.

Al terminar: tabla, resumen de una línea por área y cuántas filas nuevas. **No asciendas nada**: el
ascenso lo decide el usuario, fila por fila o en bloque.

**Los marcadores de pendiente intencionales no son hallazgos.** Si el proyecto siembra
`[PENDIENTE-validación]`, `TODO(nombre)` o equivalentes a propósito, **no los conviertas en tareas**
salvo que el usuario lo pida: están ahí señalando algo que espera una decisión ajena al código.

---

## Áreas de la revisión completa

El checklist base da **cobertura predecible y comparable**: dos revisiones del mismo proyecto miran lo
mismo, así que la diferencia entre ellas significa algo.

## Antes de escribir una fila

Tres filtros; una fila que no los pase **no se escribe**: (1) no está ya en `tareas.md` —abiertas *o*
cerradas— ni en `revisar.md`; (2) tiene evidencia concreta; (3) no es un marcador intencional del
proyecto.

## El checklist base

| Área | Qué se mira | Evidencia típica |
| --- | --- | --- |
| **Seguridad** | Secretos versionados, dependencias con vulnerabilidades conocidas, validación de entrada, permisos y alcance de tokens, datos sensibles en logs | El archivo con la clave; la salida del auditor de dependencias |
| **Funcionalidad** | Flujos incompletos, casos límite sin cubrir, manejo de errores ausente, `TODO`/`FIXME` vivos, estados vacíos y de carga | La rama del código que no maneja el caso |
| **Accesibilidad** | Semántica del marcado, contraste, foco visible, navegación por teclado, alternativas textuales, orden de lectura | El elemento sin rol o sin alternativa; el contraste medido |
| **Rendimiento** | Peso de assets, imágenes sin optimizar, consultas repetidas, tamaño del bundle, métricas de carga | El archivo y su peso; la medición |
| **Contenido** | Marcadores de pendiente reales, texto de relleno, enlaces rotos, copia desactualizada, metadatos ausentes — del contenido del proyecto, no de su documentación (esa es **Documentación**) | La ruta y el fragmento |
| **Documentación** | README y los archivos que enlaza, `CLAUDE.md` y `docs/`: instrucciones que ya no funcionan, rutas o comandos que no existen, inventarios incompletos, convenciones descritas que el repo dejó de seguir, enlaces internos rotos | El comando del README que falla; la ruta citada que no existe; el recuento que no cuadra |
| **Mantenibilidad** | Duplicación, valores hardcodeados, deuda declarada en los docs | La deuda citada en `CLAUDE.md`; los dos sitios duplicados |
| **Despliegue** | Configuración incompleta, variables de entorno sin documentar, reglas de proxy o enrutado que faltan, build que depende de algo local | La regla ausente; el prefijo no enrutado |
| **Pruebas** | Cobertura de lo crítico, verificaciones que solo se hacen a mano, ausencia de comprobación en el camino de mayor riesgo | El flujo crítico sin prueba |

**Documentación se verifica, no se intuye**: una fila se escribe cuando la afirmación del documento y
el estado del repo se contradicen de forma comprobable —el comando se ejecutó y falló, la ruta no
existe, el inventario no cuadra—. «Podría ampliarse» o «está algo escueto» no son hallazgos. Y a
diferencia del chequeo del cierre, aquí **sí se recorre el conjunto**: es el barrido completo que
aquel deliberadamente no hace.

No todas aplican a todo proyecto. **Declara qué áreas cubriste** y omite las que no apliquen, en vez
de rellenarlas con hallazgos forzados.

## Áreas propias del proyecto

Se derivan del contexto. Ejemplos:

| Proyecto | Áreas propias |
| --- | --- |
| Sitio web público | SEO, metadatos sociales / OG, analítica |
| Repo de plugins o paquetes | Sincronía de manifests, versionado, compatibilidad |
| Vault de contenido | Consistencia editorial, taxonomía, fuentes citadas |
| App con datos de usuario | Privacidad, retención, trazabilidad |
| Proyecto con diseño de referencia | Fidelidad al mockup, tokens del design system |

## Severidad

| Nivel | Criterio |
| --- | --- |
| `alta` | Rompe algo, expone datos, o bloquea el uso. Hay que hacerlo. |
| `media` | Degrada la calidad o acumula deuda que encarece lo siguiente. Conviene hacerlo. |
| `baja` | Mejora acotada, sin consecuencia si se posterga. |

La severidad es del **hallazgo**, no del esfuerzo: algo grave y fácil sigue siendo `alta`.

## Qué entregar al terminar

La tabla y un resumen de **una línea por área**. Nada más: sin informe ni plan de acción. **No
asciendas ninguna fila.** Si un área sale limpia, dilo — hace comparable la revisión siguiente.
