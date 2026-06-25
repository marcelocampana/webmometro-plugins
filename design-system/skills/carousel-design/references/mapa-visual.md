# Mapas visuales para carruseles

Usa esta referencia cuando el carrusel requiera un mapa como recurso visual. El mapa puede ser:

- **Con datos estadísticos**: tasas, coberturas, prevalencias, comparaciones por país o región (gradiente de color por valor).
- **Geográfico contextual**: destacar un país, zona o región sin datos numéricos (colores planos, zona resaltada).
- **Con capas adicionales**: puntos de interés, flechas de flujo, zonas sombreadas, íconos sobre países, texto anotado.
- **Ilustrativo/de marca**: mapa estilizado con la paleta del cliente como fondo o elemento editorial.

El resultado es un PNG de 1080×1080 px (o 1080×1350 px en formato vertical) listo para incrustar en el HTML del carrusel.

---

## Cuándo leer esta referencia

Lee este archivo cuando el diagnóstico del texto (paso 4) o el usuario indiquen que una lámina necesita un mapa. No cargues este flujo si el mapa no es necesario — es un paso opcional que solo se activa cuando hay una razón visual o comunicacional clara para usarlo.

Señales típicas:
- El texto menciona países, regiones o zonas geográficas de forma comparativa o contextual.
- El usuario pide explícitamente un mapa.
- Una lámina de datos se comunicaría mejor con un mapa que con una tabla o gráfico de barras.
- El carrusel necesita anclar visualmente el alcance geográfico de un tema.

---

## Librerías requeridas

```bash
pip install geopandas matplotlib pillow --break-system-packages
```

GeoPandas instala automáticamente `fiona` y `shapely` como dependencias.

Verifica disponibilidad antes de continuar:

```python
import geopandas, matplotlib, PIL
print("OK")
```

Si la instalación falla por restricciones del entorno, informa al usuario y propón alternativa: mapa SVG inline en HTML, o composición con flags emoji sobre fondo del cliente.

---

## Datos geográficos base

Los shapes de países provienen de **Natural Earth**, dataset de dominio público. Se cargan directamente desde GitHub sin necesidad de archivo local:

```python
import geopandas as gpd

world = gpd.read_file(
    "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/"
    "master/geojson/ne_110m_admin_0_countries.geojson"
)
```

**Recortes frecuentes:**

```python
# América Latina
latam = world[world["SUBREGION"].isin([
    "South America", "Central America", "Caribbean"
]) | world["NAME"].isin(["Mexico"])]

# Sudamérica
sudamerica = world[world["SUBREGION"] == "South America"]

# Global (sin filtro)
global_map = world.copy()

# Europa
europa = world[world["CONTINENT"] == "Europe"]

# Un solo país resaltado
chile = world[world["NAME"] == "Chile"]
```

Para mapas de Chile a nivel de regiones, Natural Earth no tiene la granularidad necesaria. Solicitar al usuario el shapefile de regiones del BCN (Biblioteca del Congreso Nacional) en formato GeoJSON o Shapefile.

---

## Flujo de producción

### 1. Definir el tipo de mapa

Antes de escribir código, decide qué tipo de mapa corresponde:

| Tipo | Cuándo usarlo | Técnica principal |
|---|---|---|
| Estadístico (coroplético) | Datos numéricos por país/región | `column=` + `cmap=` en GeoPandas |
| Contextual / resaltado | Destacar zona sin datos | Colores planos, país resaltado en color de acento |
| Con anotaciones | Puntos, flechas, íconos, texto sobre el mapa | `ax.annotate()`, `ax.scatter()`, `ax.plot()` |
| Ilustrativo de marca | Mapa como elemento visual/fondo | Paleta del cliente, sin etiquetas de datos |

### 2. Recopilar datos (si aplica)

Si el mapa lleva datos numéricos, extráelos del texto del carrusel e ingrésalos como diccionario Python:

```python
datos = {
    "Chile":     12.3,
    "Argentina": 14.7,
    "Peru":       9.1,
    "Colombia":  11.5,
    "Brazil":    15.2,
}
```

Usa los nombres de país tal como aparecen en la columna `NAME` del GeoDataFrame (en inglés). Traduce los nombres en español al mapear: `"Brasil"` → `"Brazil"`, `"México"` → `"Mexico"`, `"Perú"` → `"Peru"`.

Si el mapa no lleva datos, omite este paso.

### 3. Construir la paleta de colores

#### Observatorio del Cáncer

```python
from matplotlib.colors import LinearSegmentedColormap

cmap_cliente = LinearSegmentedColormap.from_list("odc", ["#221B4A", "#FFC391"])
color_fondo  = "#221B4A"
color_acento = "#FFC391"
color_neutro = "#3A3A4A"   # países sin dato o sin relevancia
```

#### Otros clientes

Usa la paleta registrada en el sistema de diseño del cliente. Si no hay paleta definida, usa como fallback:

```python
cmap_cliente = LinearSegmentedColormap.from_list("default", ["#1a1a2e", "#e94560"])
color_fondo  = "#1a1a2e"
color_acento = "#e94560"
color_neutro = "#2e2e3e"
```

### 4. Renderizar el mapa

```python
import matplotlib.pyplot as plt

ANCHO_PX = 1080
ALTO_PX  = 1080   # cambiar a 1350 para formato vertical
DPI      = 96

fig, ax = plt.subplots(figsize=(ANCHO_PX / DPI, ALTO_PX / DPI), dpi=DPI)
fig.patch.set_facecolor(color_fondo)
ax.set_facecolor(color_fondo)
ax.axis("off")
```

**Mapa coroplético (con datos):**

```python
import pandas as pd

df_datos = pd.DataFrame(list(datos.items()), columns=["NAME", "valor"])
gdf = latam.merge(df_datos, on="NAME", how="left")

vmin = gdf["valor"].min()
vmax = gdf["valor"].max()

# Países sin dato
gdf[gdf["valor"].isna()].plot(ax=ax, color=color_neutro, edgecolor="#FFFFFF", linewidth=0.4)

# Países con dato
gdf[gdf["valor"].notna()].plot(
    ax=ax, column="valor", cmap=cmap_cliente,
    vmin=vmin, vmax=vmax,
    edgecolor="#FFFFFF", linewidth=0.4
)

# Barra de leyenda
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

sm = ScalarMappable(cmap=cmap_cliente, norm=Normalize(vmin=vmin, vmax=vmax))
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, orientation="horizontal",
                    fraction=0.03, pad=0.02, shrink=0.6)
cbar.ax.tick_params(labelcolor="#FFFFFF", labelsize=7)
cbar.outline.set_edgecolor("#FFFFFF")
```

**Mapa contextual (zona resaltada, sin datos):**

```python
# Todos los países en color neutro
latam.plot(ax=ax, color=color_neutro, edgecolor="#FFFFFF", linewidth=0.4)

# País o zona a destacar
pais_destacado = latam[latam["NAME"] == "Chile"]
pais_destacado.plot(ax=ax, color=color_acento, edgecolor="#FFFFFF", linewidth=0.6)
```

**Capas adicionales (anotaciones, puntos, texto):**

```python
# Punto sobre una ubicación
ax.scatter(lon, lat, color=color_acento, s=40, zorder=5)

# Etiqueta de texto
ax.annotate("Texto", xy=(lon, lat), ha="center", va="center",
            fontsize=7, color="#FFFFFF", fontweight="bold")

# Etiquetas de valor por país (mapa coroplético)
for _, row in gdf[gdf["valor"].notna()].iterrows():
    centroid = row.geometry.centroid
    ax.annotate(
        f"{row['NAME']}\n{row['valor']}",
        xy=(centroid.x, centroid.y),
        ha="center", va="center",
        fontsize=6.5, color="#FFFFFF", fontweight="bold"
    )
```

### 5. Exportar PNG

```python
from pathlib import Path
from PIL import Image

RUTA = Path("[cliente]/carruseles/[nombre-carrusel]/recursos/mapa.png")
RUTA.parent.mkdir(parents=True, exist_ok=True)

plt.tight_layout(pad=0.5)
fig.savefig(RUTA, dpi=DPI, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close(fig)

# Verificar y ajustar dimensiones si es necesario
img = Image.open(RUTA)
print(f"Dimensiones: {img.size}")
if img.size != (ANCHO_PX, ALTO_PX):
    img.resize((ANCHO_PX, ALTO_PX), Image.LANCZOS).save(RUTA)
    print("Redimensionado OK")
```

---

## Incrustar el PNG en el HTML del carrusel

```html
<div class="slide-visual">
  <img src="assets/mapa.png"
       alt="Mapa de [descripción]"
       style="width:100%; height:100%; object-fit:cover;" />
</div>
```

El texto superpuesto (título, fuente, CTA) siempre va como HTML por encima del mapa — nunca embebido en el PNG — para mantener la capa editorial editable.

---

## QA del mapa antes de entregar

- Los países con dato o zona destacada tienen color visible y contrastan con el fondo.
- Los países sin relevancia se distinguen del fondo sin confundirse con los destacados.
- Las etiquetas (si las hay) son legibles y no se superponen entre sí.
- La barra de leyenda (si la hay) tiene escala correcta y contraste suficiente.
- El PNG tiene las dimensiones exactas del formato acordado.
- La fuente de los datos está citada en el HTML, no dentro del PNG.
- El archivo `mapa.png` está guardado en `assets/` del directorio del carrusel.
