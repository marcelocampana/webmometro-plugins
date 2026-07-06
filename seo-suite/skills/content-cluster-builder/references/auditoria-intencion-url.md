# Auditoría de contenido e intención de URL

Reference compartido. Describe cómo clasificar **qué tipo de página es una URL y qué intención
satisface**, y **qué intención premia Google en una SERP**. Lo usa `content-cluster-builder` en los
Pasos 3–5, pero es deliberadamente independiente del clúster: cualquier skill que necesite decidir
si una página calza con la intención de una búsqueda (tracker de cambios, detector de
canibalización, auditoría on-page) puede apoyarse aquí sin duplicar la lógica.

**El principio de fondo:** una URL no se define por la keyword que rankea, sino por *lo que la
página hace cuando alguien llega*. Dos páginas pueden rankear el mismo término y servir
intenciones opuestas — una vende, la otra informa. Asignar roles (pilar, spoke, money page) sin
mirar el contenido real produce recomendaciones que destruyen conversión o canibalizan.

## Contenido

- [Taxonomía de tipo de página](#taxonomía-de-tipo-de-página)
- [Intención dominante de la SERP](#intención-dominante-de-la-serp)
- [Procedimiento: auditar una URL propia](#procedimiento-auditar-una-url-propia)
- [Salida esperada](#salida-esperada)

---

## Taxonomía de tipo de página

Clasificar cada página en uno de estos tipos según **señales observables en el contenido**, no
según la keyword:

| `tipo_pagina` | Señales observables | Intención que satisface |
|---|---|---|
| **transaccional** | CTAs repetidos ("agenda", "reserva", "pide tu hora"), formulario de contacto/agendamiento, precios o "consulta el precio", teléfono/WhatsApp prominente, foco en *este* servicio/producto | El usuario quiere actuar ahora (contratar, comprar, agendar) |
| **comercial** | Comparativas, tablas de opciones, "mejor/tipos de", beneficios frente a alternativas, reviews — orientado a decidir antes de actuar | El usuario evalúa opciones antes de decidir |
| **informacional** | Guía, FAQ, "qué es / cómo / por qué", contenido educativo extenso, sin presión de conversión | El usuario quiere entender o aprender |
| **mixta** | Combina explicación educativa con CTAs y/o precios en proporciones parecidas | Sirve a más de una intención; anotar cuál predomina |

Una página puede tener algo de todo (casi todas tienen un CTA). Lo que define el tipo es **qué
predomina y cuál es el objetivo principal de la página**, no la presencia aislada de una señal.

---

## Intención dominante de la SERP

La intención de la SERP es **qué tipo de páginas premia Google en el top-10** para un término. Es
la señal más fiable de qué quiere el buscador, por encima de la intención que uno le supone a la
keyword leyéndola.

Para clasificarla, mirar el top-10 orgánico (`serp_google_organic_live`) y contar qué tipo de
resultado domina:

| Si domina en el top-10… | Intención dominante de la SERP |
|---|---|
| Páginas de servicio / landing de clínicas, e-commerce de producto | **transaccional** |
| Categorías, comparativas, "mejores X", agregadores | **comercial** |
| Guías, blogs, artículos educativos, FAQ, Wikipedia | **informacional** |
| Pack local / mapa / fichas de negocio prominentes | **local** (suele coexistir con transaccional) |

Pistas rápidas sin abrir cada resultado: el **tipo de dominio** (clínica/tienda vs. medio/blog), el
**patrón de la URL** (`/servicios/…`, `/producto/…` vs. `/blog/…`, `/guia/…`) y el **título** del
resultado. Los `item_types` que devuelve la SERP (organic, paid, local_pack, people_also_ask,
featured_snippet) también informan: un featured snippet o PAA empuja hacia informacional; un local
pack, hacia transaccional/local.

**Regla de oro:** el tipo de contenido de la página que quieres posicionar debe coincidir con la
intención dominante de su SERP. Si la SERP es transaccional, una guía informativa rara vez rankea
ahí — y viceversa.

---

## Procedimiento: auditar una URL propia

Cuando el sitio ya tiene una URL que rankea un término del análisis (vía GSC o porque aparece en
la SERP del propio dominio), **auditarla antes de asignarle cualquier rol**:

1. **Abrir la página y leer su contenido real.** Opción simple: `WebFetch` sobre la URL.
   Alternativas si se necesita más fidelidad: `chrome-devtools` (render real), o las herramientas
   `onpage_*` / `content_analysis` de DataForSEO. Nunca clasificar por el slug ni por la keyword:
   abrir y leer.
2. **Clasificar `tipo_pagina_actual`** con la taxonomía de arriba, anotando las señales que lo
   justifican (p. ej. "5 CTAs de agenda + formulario → transaccional").
3. **Anotar `intencion_satisfecha`**: qué resuelve hoy la página para quien llega.
4. **Comparar con la intención de la SERP** del término objetivo (`coincide_con_serp`):
   - **alineado** — el tipo de página coincide con lo que premia la SERP. No forzar cambios de
     intención.
   - **desalineado** — la página sirve una intención distinta a la de la SERP. Es una señal, no
     una orden: puede convenir crear una página nueva del tipo correcto en vez de reconvertir la
     existente, sobre todo si la existente ya convierte.
5. **Si la página ya convierte** (datos de GA4/GSC: conversiones, buen CTR, leads), tratar su
   intención como **un activo a preservar**. Reconvertir una página transaccional que convierte en
   contenido informativo se hace solo con decisión explícita del responsable, nunca por defecto.

---

## Salida esperada

Por cada URL auditada, dejar registrado:

```
url: https://…
tipo_pagina_actual: transaccional | comercial | informacional | mixta
intencion_satisfecha: <qué resuelve hoy>
intencion_serp_dominante: transaccional | comercial | informacional | local
coincide_con_serp: alineado | desalineado
convierte: sí | no | desconocido   (de GA4/GSC si está disponible)
señales: <evidencia observada que justifica la clasificación>
```

Estos campos alimentan el coverage scoring (Paso 4) y la matriz de asignación de rol (Paso 5) de
`content-cluster-builder`, y son reutilizables por cualquier otro skill que razone sobre intención
de página.
