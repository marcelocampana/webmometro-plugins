# Escritorio y móvil: qué diferencia importa

Un mismo contenido en dos variantes **no tiene por qué decir exactamente lo mismo**: en móvil se
condensa, se pliega tras un acordeón o se omite lo accesorio. Son decisiones de diseño, no fallos
de sincronización — así que «si difieren, hallazgo» produce **varios falsos por página y por
corrida**, y un reporte con ruido constante se deja de leer.

Medido en páginas reales: entre escritorio y móvil **~90% del texto es común**, y casi toda la
diferencia restante es de **segmentación** (la misma frase partida en otro punto), no contenido
ausente.

## Antes de comparar: descarta lo estructural

Las secciones presentes en una variante y no en la otra suelen ser **andamiaje**: un índice lateral
que no cabe en móvil, un encabezado fijo, un bloque que en escritorio va anidado y en móvil suelto.

**Compara texto, no secciones.** Un bloque ausente solo importa si su texto desaparece; si está en
otro lugar de la misma variante, no falta.

## El método

1. **Extrae el texto de las dos variantes** (`extraccion.md`) y normaliza: sin tildes, sin
   mayúsculas, sin puntuación.
2. **Descarta la segmentación**: no compares frases completas, sino tiradas de ~8-10 palabras. Una
   frase partida en dos en móvil no es texto ausente.
3. **Quédate con lo que solo está en una variante** — y clasifícalo antes de reportar.

## Qué es hallazgo y qué no

**El criterio por defecto es reportar.** Solo se descarta lo que se puede clasificar con seguridad
como andamiaje o refuerzo; **ante la duda, se reporta**. El coste está desequilibrado: un aviso de
más cuesta una línea de lectura; uno de menos puede dejar a alguien sin un dato clínico. Nunca
descartes por parecerte poco importante — descarta solo por saber lo que es.

### Se descarta (sin reportar)

Únicamente esto, y solo cuando el texto no lleva dentro nada de la lista siguiente:

- **Andamiaje**: índice, navegación, encabezado fijo, migas, pies de página, etiquetas de interfaz
  («Ver más», «Cerrar»).
- **Segmentación**: la misma frase partida en distinto punto — no es texto ausente.
- **Notas de trabajo y marcadores de pendiente** — se cuentan aparte, en la línea de resumen.

### Se reporta siempre

Aunque la omisión parezca deliberada y aunque el bloque sea «de refuerzo»:

- **Datos**: cifras, porcentajes, fechas, edades, plazos, dosis.
- **Nombres propios que anclan una afirmación**: fármacos, leyes, programas, instituciones,
  exámenes, la fuente citada.
- **Advertencias y límites**: contraindicaciones, efectos adversos, «no reemplaza», «consulte
  antes de», signos de alarma, cuándo acudir a urgencias.
- **Acceso y elegibilidad**: coberturas, requisitos, quién califica, cómo se pide, dónde se
  consulta, plazos de garantía.
- **Negaciones y matices que cambian el sentido**: «no», «solo si», «salvo», «puede» frente a
  «debe». Una negación perdida invierte la frase.
- **Síntomas, efectos y experiencias clínicas** — estén donde estén, incluido dentro de un
  testimonio o un video.
- **Cualquier texto que no puedas clasificar con confianza.**

### El caso inverso: texto que solo está en una variante nueva

Si una variante **tiene texto que la otra no y que tampoco está en la fuente**, no es una omisión:
es **contenido sin aprobar** que entró por el diseño. Repórtalo siempre, en cualquier categoría —
incluido lo que aquí se descartaría—, porque nadie lo revisó.

### La prueba, cuando la tabla no alcanza

Pregúntate: **¿alguien que lea solo esta variante tomaría una decisión distinta, o se quedaría sin
saber algo que la otra sí le dice?** Si la respuesta es sí, o no lo tienes claro, es hallazgo.

Un bloque «de refuerzo» no es inocuo por serlo: un testimonio puede contener la única mención de un
efecto adverso, y una sección «accesoria» la única indicación de cuándo consultar. **Clasifica por
lo que dice el texto, no por el bloque donde vive.**

## Cómo reportarlo

Nunca como una lista de diferencias. **Una línea de resumen** y, debajo, lo que se reporta:

```
HER2 positivo — escritorio vs móvil
  90% del texto coincide. 6 diferencias: 4 de segmentación, 1 de andamiaje (índice).
  ⚠ móvil omite: «cobertura GES para el trastuzumab desde 2024»
    Vía de acceso: quien lea en móvil no la verá.
  ? móvil omite: «…y puede provocar cardiotoxicidad» (dentro del testimonio de M. Cortés)
    Efecto adverso dentro de un bloque de refuerzo — se reporta por lo que dice, no por dónde está.
```

Lo descartado se cuenta en la línea de resumen —«4 de segmentación, 1 de andamiaje»— para que se
vea que se miró. **Nómbralo por lo que era**: «5 diferencias menores» no permite comprobar que el
descarte fue correcto; «4 de segmentación, 1 índice» sí.

Marca con `?` lo que reportas por duda, no por certeza. Es información útil: distingue lo que exige
decisión de lo que solo pide una mirada.

## Qué proponer

**Para lo que no cruzó la línea, nada.** No propongas igualar variantes: obligar a móvil a mostrar
todo lo de escritorio deshace una decisión de diseño que probablemente era correcta.

**Para lo que sí cruzó**, propón añadirlo a la variante que lo omite — señalando que puede requerir
trabajo de diseño (un acordeón, una nota plegable) y no solo pegar texto. Si el bloque no cabe,
**es una decisión de diseño y del equipo editorial**, no del chequeo: se señala y se devuelve.

## No basta con mirar lo que falta

El método hasta aquí compara **qué texto está en una variante y no en la otra**. Eso no detecta un
cambio **dentro** de una frase presente en las dos: una cifra distinta, un «no» que desapareció, un
«puede» que se volvió «debe», una edad que cambió de 40 a 50.

Por eso, sobre el **texto común**, revisa además que coincidan cifras, negaciones, condicionales y
nombres propios. Una diferencia ahí es hallazgo siempre, y de las graves: las dos variantes parecen
decir lo mismo y no lo dicen.

## Registrar lo intencional

Cuando el usuario confirme que una omisión en móvil es deliberada, **anótala en la fuente** junto al
bloque. Sin eso, cada corrida la vuelve a levantar y el reporte pierde credibilidad.

Formato sugerido en el frontmatter de la pieza:

```yaml
variaciones_dispositivo:
  - bloque: videos
    omitido_en: movil
    motivo: "Cuatro testimonios en móvil alargan demasiado la página."
```

## Errores

| Situación | Qué hacer |
| --- | --- |
| Las dos variantes difieren en casi todo | Sospecha de mapeo: probablemente no son la misma página. Dilo así. |
| Móvil tiene texto que escritorio no | Mismo criterio, en espejo. No asumas que móvil siempre resta. |
| No se puede saber si un texto está plegado o ausente | Dilo: plegado no es omitido. No lo reportes como ausencia sin comprobarlo. |
| La fuente no distingue variantes | Es lo normal: la fuente es una sola. Las variaciones se anotan en ella, no se duplica el archivo. |
