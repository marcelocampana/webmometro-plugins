# Contexto de negocio: cómo leerlo y derivarlo

El skill `content-cluster-builder` es agnóstico al negocio. Esta guía describe cómo obtener el
contexto necesario sin hardcodear nada, de forma que el skill funcione igual para cualquier proyecto.

---

Primero, resolver la raíz del cliente subiendo desde el directorio activo hasta encontrar una
carpeta `contexto/`. Toda la resolución de config parte de ahí.

## Prioridad de fuentes (resolver en orden)

1. **`contexto/configuracion.md`** — fuente de verdad compartida de toda la suite (IDs GA4/GSC/
   Clarity/DataForSEO + URLs). Leer con Read **por puntero**; nunca copiar sus datos a una config
   propia del cluster-builder. Extraer: `dominio`, `gsc_property`, `ga4_property_id`,
   `ubicacion_serp` (país, ciudad, idioma) y `keywords_principales`.

2. **`contexto/sitio.md`** (si existe) — contexto estratégico: vertical, audiencia, posicionamiento,
   objetivos. De aquí sale el rubro del negocio para anclar la expansión de keywords y los títulos.

3. **Ubicaciones legadas** — si el proyecto guarda esos datos con nombres/rutas antiguas (p. ej. un
   `seo-tracking/config.md` en la raíz del proyecto, o un `context/…` legado), resolverlos por rol y
   **ofrecer migrarlos** a `contexto/configuracion.md`. No asumir un nombre alterno fijo.

4. **Skill `site-context` / `site-snapshot`** — si falta `contexto/configuracion.md` o `contexto/sitio.md`,
   ofrecer generarlos con estos skills antes de continuar, en vez de inventar una config paralela.

5. **Preguntar al usuario** — solo si ninguna fuente anterior da el dato. Pedir el mínimo:
   - Dominio del sitio (para GSC y como referencia)
   - Ubicación/ciudad objetivo para SERP (si es local)
   - Idioma del contenido

   Persistir lo que el usuario responda en `contexto/configuracion.md` (previa confirmación), no en
   una config propia del skill (ver formato más abajo).

---

## Campos mínimos necesarios para el skill

| Campo | Fuente preferida | Para qué se usa |
|---|---|---|
| `dominio` | `contexto/configuracion.md` o usuario | Consultas GSC, referencia de cobertura |
| `gsc_property` | `contexto/configuracion.md` | Leer keywords reales del sitio |
| `ubicacion_serp.ciudad` | `contexto/configuracion.md` o usuario | Geolocalizar SERP en vivo |
| `ubicacion_serp.idioma` | `contexto/configuracion.md` o usuario | Parámetro de SERP y de intención |
| `keywords_principales` | `contexto/configuracion.md` o usuario | Anclar la expansión al negocio real |

Los campos `ga4_property_id` y `checkpoint_dias_default` son opcionales para este skill (los usa
el tracker, no el cluster-builder).

---

## Formato para crear contexto mínimo (si no existe `contexto/configuracion.md`)

Si el proyecto no tiene `contexto/configuracion.md`, la vía preferida es generarlo con `site-context`
/ `site-snapshot`. Si el usuario prefiere un mínimo rápido, crear (previa confirmación)
`contexto/configuracion.md` con el siguiente formato — la misma config compartida que lee toda la
suite, no una config paralela del skill:

```yaml
---
cliente: "{Nombre del negocio}"
dominio: "https://www.ejemplo.com"
gsc_property: "https://www.ejemplo.com/"
ga4_property_id: null
checkpoint_dias_default: [14, 28]
ubicacion_serp:
  pais: "{País}"
  ciudad: "{Ciudad principal}"
  idioma: "{es|en|...}"
keywords_principales:
  - "{keyword 1}"
  - "{keyword 2}"
---
```

Dejar `null` los campos que el usuario no proporcionó. No inventar valores.

---

## Cómo inferir el rubro sin preguntar

La fuente preferida es `contexto/sitio.md` (producida por `site-context`): describe la vertical, la
audiencia objetivo, el posicionamiento y las páginas estratégicas. Con eso es suficiente para
contextualizar la expansión de keywords y los títulos H1/H2. Si no existe, caer en archivos de brand
voice o propuesta de posicionamiento del proyecto y leer el primer párrafo como aproximación.

No asumir vertical, ubicación ni idioma si ninguna fuente los confirma. Ante la duda, preguntar.

---

## Intención local

La intención local es relevante cuando el negocio presta servicios o vende productos en una
ubicación geográfica específica (clínicas, restaurantes, estudios, consultoras, etc.).

Señales de que aplica: `ubicacion_serp.ciudad` está definida, el dominio termina en un TLD local
(.cl, .com.ar, etc.), o las `keywords_principales` incluyen nombres de ciudades o comunas.

Cuando aplica, añadir variantes locales a la expansión de keywords: `[servicio] + [ciudad]`,
`[servicio] + [comuna]`, `[servicio] cerca de mí`.

Cuando no aplica (negocio digital, audiencia nacional o global), ignorar el filtro local en la
priorización de intención.
