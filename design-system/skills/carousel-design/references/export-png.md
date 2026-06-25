# Exportación PNG retina — Opción Playwright

Usar solo si las herramientas MCP `mcp__chrome-devtools` no están disponibles.

## Verificar disponibilidad

```bash
npx playwright --version
```

Si no está instalado:
```bash
npm install -g playwright && npx playwright install chromium
```

## Script de exportación por slide

```javascript
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const htmlPath = process.argv[2];
  const outDir = process.argv[3] || path.dirname(htmlPath);

  const browser = await chromium.launch();
  const page = await browser.newPage({
    deviceScaleFactor: 2  // retina 2x
  });

  await page.goto(`file://${path.resolve(htmlPath)}`);
  await page.waitForLoadState('networkidle');

  const slides = await page.$$('.slide');
  for (let i = 0; i < slides.length; i++) {
    const n = String(i + 1).padStart(2, '0');
    const box = await slides[i].boundingBox();
    await page.screenshot({
      path: `${outDir}/slide-${n}.png`,
      clip: box
    });
  }

  await browser.close();
  console.log(`${slides.length} PNGs exportados en ${outDir}`);
})();
```

## Uso

```bash
node export-slides.js ruta/al/carrusel.html ruta/de/salida/
```

## Fallback manual

Si ninguna opción automática funciona, indicar al usuario:
1. Abrir el HTML en Chrome
2. Zoom al 200% para resolución retina equivalente
3. Capturar cada slide individualmente con una extensión de captura (ej. "Full Page Screen Capture")
4. Guardar con el patrón `slide-01.png`, `slide-02.png`, etc.
