# Contexto de negocio: cómo leerlo y derivarlo

El skill `content-cluster-builder` es agnóstico al negocio. Esta guía describe cómo obtener el
contexto necesario sin hardcodear nada, de forma que el skill funcione igual para cualquier proyecto.

---

## Prioridad de fuentes (resolver en orden)

1. **`seo-tracking/config.md`** (si existe en el proyecto) — fuente de verdad compartida.
   Leer con Read. Extraer: `cliente`, `dominio`, `gsc_property`, `ga4_property_id`,
   `ubicacion_serp` (país, ciudad, idioma) y `keywords_principales`.

2. **Archivos de contexto del proyecto** — si no hay `seo-tracking/config.md`, buscar otros
   indicadores: archivos de brand voice, propuesta de posicionamiento, README del vault, o cualquier
   nota que mencione el dominio o el rubro del negocio.

3. **Skill `site-context`** (si está disponible en el proyecto) — puede inferir el rubro, la
   audiencia y los temas principales directamente desde el sitio web.

4. **Preguntar al usuario** — solo si ninguna fuente anterior da el dato. Pedir el mínimo:
   - Dominio del sitio (para GSC y como referencia)
   - Ubicación/ciudad objetivo para SERP (si es local)
   - Idioma del contenido

   Persistir lo que el usuario responda en un archivo de contexto del proyecto para no volver a
   preguntar (ver formato más abajo).

---

## Campos mínimos necesarios para el skill

| Campo | Fuente preferida | Para qué se usa |
|---|---|---|
| `dominio` | `config.md` o usuario | Consultas GSC, referencia de cobertura |
| `gsc_property` | `config.md` | Leer keywords reales del sitio |
| `ubicacion_serp.ciudad` | `config.md` o usuario | Geolocalizar SERP en vivo |
| `ubicacion_serp.idioma` | `config.md` o usuario | Parámetro de SERP y de intención |
| `keywords_principales` | `config.md` o usuario | Anclar la expansión al negocio real |

Los campos `ga4_property_id` y `checkpoint_dias_default` son opcionales para este skill (los usa
el tracker, no el cluster-builder).

---

## Formato para crear contexto mínimo (si no existe config.md)

Si el proyecto no tiene `seo-tracking/config.md`, crear un archivo mínimo de contexto para este
skill en `seo-tracking/config.md` con el siguiente formato (mismo que el tracker usa, para que sean
compatibles):

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

Si hay archivos de brand voice o propuesta de posicionamiento en el vault, leer el primer párrafo
— suele describir la vertical, el público objetivo y los servicios principales. Con eso es suficiente
para contextualizar la expansión de keywords y los títulos H1/H2.

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
