---
name: page-snapshot
description: "Activar solo con el comando /page-snapshot. No invocar automáticamente por contexto de conversación."
metadata:
  version: 1.2.0
---

# Snapshot de Página

Construyes un snapshot de datos factuales para una URL específica, consolidando métricas a nivel de página provenientes de GA4, GSC, PageSpeed, Clarity y DataForSEO, más los elementos de la página, en un único documento de referencia en Markdown.

El archivo de salida es `context/pages/page-snapshot-{slug}.md` — un archivo neutral, solo de datos, diseñado para lectura humana y consumo posterior por habilidades como page-cro y seo-audit (modo URL específica).

## Principios Editoriales

El snapshot es estrictamente factual. Incluye únicamente: datos de la página, metadatos de la página, métricas por período, tablas por fuente, elementos de página verificables y definiciones de campos.

No incluyas: diagnósticos, recomendaciones, prioridades de optimización, hipótesis causales ni juicios de calidad.

Esto importa porque page-cro y seo-audit dependen de datos de página limpios y sin sesgos. Si el snapshot carga opiniones implícitas, el análisis posterior hereda esos sesgos.

## Idioma

**El documento de salida completo debe estar escrito en español neutro** — incluyendo todos los encabezados de sección, encabezados de tabla, nombres de columna, etiquetas de campo, nombres de período y términos técnicos. No usar encabezados ni etiquetas en inglés en el archivo de salida.

Ejemplos de traducción correcta:
- "Extraction date" → "Fecha de extracción"
- "Reference date" → "Fecha de referencia"
- "Last 28 days" → "Últimos 28 días"
- "Last 90 days" → "Últimos 90 días"
- "Last 6 months" → "Últimos 6 meses"
- "Last 12 months" → "Últimos 12 meses"
- "Current state" → "Estado actual"
- "Latest snapshot" → "Snapshot más reciente"
- "Page Identity" → "Identidad de la Página"
- "Source Inventory" → "Inventario de Fuentes"
- "Heading Structure" → "Estructura de Encabezados"
- "Conversion Actions" → "Acciones de Conversión"
- "Image Inventory" → "Inventario de Imágenes"
- "Metric Definitions" → "Definiciones de Métricas"

El contenido dentro de las tablas permanece en el idioma original de la fuente. Si GA4 reporta un evento como `book_demo`, se registra tal cual. Si el título de una página está en inglés, se registra en inglés. Solo las etiquetas, encabezados y elementos estructurales del documento se traducen — nunca los valores de datos en crudo.

Escribe toda la comunicación con el usuario (explicaciones, preguntas, advertencias, errores) en español neutro.

## Fecha de Referencia

Todas las ventanas de tiempo relativas se calculan hacia atrás desde una **fecha de referencia** proporcionada por el usuario — no desde la fecha del sistema.

Solicita la fecha de referencia al usuario antes de iniciar cualquier extracción de datos. Si el usuario no especifica una, pregunta explícitamente:

> "¿Desde qué fecha quieres que se calculen los períodos del snapshot de esta página? Por ejemplo: si indicas el 31 de marzo de 2025, 'últimos 28 días' irá del 2 al 31 de marzo."

Acepta cualquier formato no ambiguo (ISO, fecha escrita, "fin del mes pasado", etc.) y confirma la fecha resuelta antes de continuar.

Si ya existe un `Fecha de referencia` en `context/snapshot-config.md`, confirma con el usuario si se reutiliza o si desea actualizarla para este snapshot.

Registra la fecha de referencia confirmada en los **Metadatos** del archivo de salida.

## Convención de Slug

El slug se deriva de las dos últimas partes de la ruta de la URL. Si la URL tiene solo un nivel de ruta, se usa únicamente esa parte.

| URL | Slug | Archivo |
|---|---|---|
| `/pricing` | `pricing` | `page-snapshot-pricing.md` |
| `/blog/seo-audit-template` | `blog-seo-audit-template` | `page-snapshot-blog-seo-audit-template.md` |
| `/features/analytics` | `features-analytics` | `page-snapshot-features-analytics.md` |
| `/` | `home` | `page-snapshot-home.md` |

Reglas:
- Usar guion `-` como separador entre niveles de ruta
- Convertir a minúsculas
- La ruta `/` siempre se traduce como `home`
- Si la ruta tiene más de dos niveles, usar solo los últimos dos
- No incluir barra final, parámetros de consulta ni fragmentos

## Arquitectura de Archivos

```text
{dominio-o-proyecto}/
  context/
    snapshot-config.md
    pages/
      page-snapshot-{slug}.md
```

## Alcance

El snapshot de página responde:
- Identidad técnica y editorial de la URL
- Rendimiento de tráfico y conversión
- Consultas orgánicas que aterrizan en la URL
- Rendimiento técnico
- Señales de comportamiento
- Elementos de interfaz con interacciones
- Resumen orgánico y de backlinks

## Fuentes y Ventanas de Tiempo

Todas las ventanas se calculan hacia atrás desde la fecha de referencia proporcionada por el usuario.

| Fuente | Ventanas |
|---|---|
| GA4 | Últimos 28 días, Últimos 90 días, Últimos 6 meses, Últimos 12 meses |
| GSC | Últimos 28 días, Últimos 90 días, Últimos 6 meses, Últimos 12 meses |
| PageSpeed | Estado actual |
| Clarity | Últimos 28 días, Últimos 90 días |
| DataForSEO | Snapshot más reciente |

## Conjuntos de Datos Mínimos por Fuente

**GA4:** resumen de página por período, desglose por dispositivo, desglose por canal, eventos de página, tendencia mensual (12 meses).

**GSC:** resumen de URL por período, consultas para la URL.

**PageSpeed:** snapshots móvil y escritorio, datos de campo cuando estén disponibles.

**Clarity:** resumen de URL por período, desglose por dispositivo, interacciones con elementos.

**DataForSEO:** resumen orgánico de URL, palabras clave posicionadas de la URL, backlinks de la URL.

## Elementos de Página a Registrar

Registra estos elementos de forma factual, sin evaluar si son buenos o malos:

- **Título, meta descripción, H1**
- **Estructura de encabezados:** H1, H2, H3 con conteos, listados y árbol jerárquico
- **Inventario de imágenes:** src, existencia de alt, valor del alt
- **Acciones de conversión:** nombre, tipo, elemento disparador, ubicación en la página, destino/resultado, evento de GA4
- **Señales técnicas:** canónica, meta robots, código de estado, indexabilidad, tipos de schema detectados
- **Métricas de contenido:** conteo de palabras, enlaces internos que apuntan a la página, enlaces salientes
- **Jerarquía de CTA:** CTA principal, CTA secundario
- **Presencia de módulos:** formulario, tabla de precios, FAQ, testimonios

## Estructura del Archivo de Salida

1. **Metadatos** — debe incluir `Fecha de extracción` y `Fecha de referencia` como campos obligatorios, más: nombre del reporte, versión, sitio/propiedad, etiqueta de página, URL de página, ruta de página, tipo de página, mercado, idioma, períodos incluidos con sus fechas exactas calculadas, fuentes de datos, y declaraciones explícitas de que no se incluyen interpretaciones ni recomendaciones
2. **Identidad de la Página** — URL, canónica, URL indexable final, plantilla, intención principal, estado HTTP, indexabilidad, meta robots, estado de la canónica, idioma, última modificación, tipos de schema
3. **Elementos de la Página** — tabla resumen + subsecciones detalladas:
   - Acciones de Conversión (tabla de inventario + resumen)
   - Inventario de Imágenes (resumen + tabla de detalle)
   - Estructura de Encabezados (conteos + listados de H1/H2/H3 + árbol de encabezados)
4. **Inventario de Fuentes** — misma función de trazabilidad que site-snapshot: lista cada fuente consultada, datasets extraídos, ventanas de tiempo con fechas exactas, granularidad, cantidad de filas, y fuentes no disponibles con su estado
5. **Google Analytics 4** — resumen de página por período, desglose por dispositivo (28d + 90d), desglose por canal (28d + 90d), eventos de página (28d + 90d), tendencia mensual (12 meses)
6. **Google Search Console** — resumen de URL por período, consultas para la URL (28d + 90d)
7. **Google PageSpeed / Core Web Vitals** — snapshots de URL (móvil + escritorio), snapshot de datos de campo cuando estén disponibles
8. **Microsoft Clarity** — resumen de URL por período, desglose por dispositivo (28d + 90d), interacciones con elementos (28d + 90d)
9. **DataForSEO** — resumen orgánico de URL, palabras clave posicionadas de la URL, backlinks de la URL
10. **Definiciones de Métricas** — definiciones breves para cada métrica utilizada, escritas en español neutro

## Nombres de Período

Usar siempre estos nombres en español en encabezados, etiquetas de tabla y metadatos:

- `Últimos 28 días`
- `Últimos 90 días`
- `Últimos 6 meses`
- `Últimos 12 meses`
- `Estado actual`
- `Snapshot más reciente`

En los Metadatos, incluir las fechas exactas calculadas para cada período. Por ejemplo:
- Últimos 28 días: 2025-03-04 al 2025-03-31
- Últimos 90 días: 2024-12-31 al 2025-03-31

## Límites de Tablas

- Consultas: hasta 20 filas, ordenadas por clics
- Interacciones con elementos: hasta 10 filas, ordenadas por interacciones
- Períodos: todos los períodos definidos
- Dispositivos y canales: todas las categorías disponibles

Al truncar, ordenar primero por la métrica principal y anotar el corte.

## Disponibilidad de Fuentes

Mismas reglas que site-snapshot: ejecutar una verificación previa, notificar al usuario sobre fuentes no disponibles especificando qué plataforma falló y qué identificador falta, solicitar una decisión explícita (continuar o corregir), registrar las ausencias de forma factual en el Inventario de Fuentes.

## Flujo de Construcción

### Paso 1: Definir la URL objetivo y la fecha de referencia

Verificar si existe `context/snapshot-config.md`. Si existe, leerlo.

Si no existe, seguir el mismo flujo de detección automática y consulta al usuario que site-snapshot.

**Solicitar la fecha de referencia al usuario** — la fecha desde la cual se calcularán todas las ventanas de tiempo relativas. Hacerlo antes de cualquier extracción de datos. Si el config ya tiene una `Fecha de referencia`, confirmar con el usuario si se reutiliza o actualiza.

Calcular y confirmar con el usuario las fechas exactas de cada período antes de continuar:

| Período | Desde | Hasta |
|---|---|---|
| Últimos 28 días | [fecha_ref - 27 días] | [fecha_ref] |
| Últimos 90 días | [fecha_ref - 89 días] | [fecha_ref] |
| Últimos 6 meses | [fecha_ref - 6 meses] | [fecha_ref] |
| Últimos 12 meses | [fecha_ref - 12 meses] | [fecha_ref] |

Definir además: URL exacta, tipo de página, etiquetas internas si existen.

Si existe una lista curada de URLs estratégicas, usarla como primera fuente de selección. De lo contrario, elegir entre las páginas más visitadas, principales páginas de destino o páginas clave del negocio.

### Paso 2: Verificación previa de disponibilidad de fuentes

Igual que site-snapshot: probar cada fuente, clasificar el estado (disponible, no configurada, fallo de acceso, configurada sin datos, no compatible), notificar al usuario sobre problemas, solicitar decisión explícita.

Si el usuario decide continuar sin alguna fuente, registrar la ausencia de forma factual en el Inventario de Fuentes.

### Paso 3: Extraer identidad y elementos de la página

Obtener o derivar: canónica, meta robots, título, meta descripción, H1, estructura de encabezados (H1/H2/H3), inventario de imágenes con atributos alt, acciones de conversión visibles, tipos de schema, código de estado, conteos estructurales.

### Paso 4: Extraer datos de GA4 para la URL

Consultar conjuntos de datos a nivel de página usando las fechas exactas calculadas en el Paso 1 para: períodos, dispositivos, canales, eventos, tendencia mensual.

### Paso 5: Extraer datos de GSC para la URL

Consultar usando las fechas exactas calculadas: resumen de URL por período, consultas asociadas a la URL.

### Paso 6: Extraer PageSpeed para la URL

Ejecutar: móvil y escritorio. Registrar: métricas de laboratorio, datos de campo cuando estén disponibles.

### Paso 7: Extraer datos de Clarity para la URL

Consultar usando las fechas exactas calculadas: resumen de URL, distribución de sesiones por dispositivo, interacciones con elementos.

### Paso 8: Extraer datos de DataForSEO para la URL

Consultar: tráfico orgánico estimado, palabras clave posicionadas, backlinks y dominios de referencia.

### Paso 9: Normalizar y renderizar

Aplicar únicamente transformaciones editoriales: estandarizar nombres de período en español, ordenar filas, redondear visualmente, truncar tablas largas.

No añadir interpretaciones.

### Paso 10: Verificación editorial

Confirmar:
- No hay recomendaciones presentes
- No hay lenguaje evaluativo ni adjetivos de calidad
- Las tablas tienen períodos y fuente claros
- La URL aparece de forma consistente en todas las secciones relevantes
- Las fuentes no disponibles están listadas con estado y nota factual
- `Fecha de extracción` y `Fecha de referencia` están presentes en los Metadatos
- Los Metadatos incluyen las fechas exactas calculadas para cada período
- Todos los encabezados de sección, encabezados de tabla y etiquetas de campo están en español neutro

## Ejemplo de Referencia

El archivo `page-snapshot-pricing-example.md` (provisto como referencia durante la creación del skill) define la estructura esperada y el nivel de detalle. Al construir un snapshot de página, seguir esa estructura, orden de secciones y formato de tablas.

## Habilidades Relacionadas

- **site-snapshot** — snapshot factual para todo el sitio
- **site-context** — contexto estratégico del sitio
- **seo-audit** — diagnóstico SEO (el modo URL específica requiere este snapshot)
- **page-cro** — análisis de conversión (requiere este snapshot)
