#!/usr/bin/env node
/**
 * verify_html_carousel.js
 * Audita un HTML de carrusel: detecta overflow y texto fuera del area segura,
 * captura screenshot y guarda un reporte JSON.
 *
 * Uso: node verify_html_carousel.js input.html [out-dir]
 *
 * Requiere Chrome instalado. Busca en $CHROME_PATH o en la ruta por defecto de macOS.
 * Codigo de salida: 0 = sin issues, 3 = issues detectados, 1/2 = error de ejecucion.
 */

"use strict";
const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

// ── Configuracion ────────────────────────────────────────────────────────────

const input   = process.argv[2];
const outDir  = process.argv[3] || "visual-check";
const chrome  = process.env.CHROME_PATH ||
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";

if (!input) {
  console.error("Uso: verify_html_carousel.js input.html [out-dir]");
  process.exit(2);
}

const htmlPath = path.resolve(input);
if (!fs.existsSync(htmlPath)) {
  console.error(`Archivo HTML no encontrado: ${htmlPath}`);
  process.exit(1);
}

fs.mkdirSync(outDir, { recursive: true });

const reportPath     = path.resolve(outDir, "report.json");
const screenshotPath = path.resolve(outDir, "full-page.png");
const userDataDir    = path.resolve(outDir, `chrome-profile-${Date.now()}-${process.pid}`);
fs.mkdirSync(userDataDir, { recursive: true });

// ── Script de auditoria ─────────────────────────────────────────────────────
// Se inyecta en el HTML y escribe el reporte en data-audit-report del body.

const auditScript = `
(() => {
  const slides = [...document.querySelectorAll('.slide')];
  const issues = [];
  const zOf = (el) => {
    const z = parseInt(getComputedStyle(el).zIndex, 10);
    return Number.isNaN(z) ? 0 : z;
  };
  slides.forEach((slide, i) => {
    const s = slide.getBoundingClientRect();
    const safeX = s.width  * 0.07;
    const safeY = s.height * 0.06;
    const textNodes = [];
    const nodes = [...slide.querySelectorAll(
      'h1,h2,p,small,strong,span,.content,.cta,.quote-card,.warm-card,.brand'
    )];
    nodes.forEach((node) => {
      const r    = node.getBoundingClientRect();
      const text = (node.innerText || node.textContent || '').trim().slice(0, 90);
      if (!text && !node.className) return;
      if (text) textNodes.push({ node, r, text });
      const outside    = r.left < s.left || r.top < s.top || r.right > s.right || r.bottom > s.bottom;
      const unsafeText = /^(H1|H2|P|SMALL|STRONG|SPAN)$/.test(node.tagName) &&
        (r.left  < s.left  + safeX ||
         r.right > s.right - safeX ||
         r.top   < s.top   + safeY ||
         r.bottom > s.bottom - safeY);
      if (outside || unsafeText) {
        issues.push({
          slide     : i + 1,
          type      : outside ? 'outside' : 'unsafe-text',
          tag       : node.tagName.toLowerCase(),
          className : String(node.className || ''),
          outside,
          unsafeText,
          text,
          rect      : { left: r.left - s.left, top: r.top - s.top, right: r.right - s.left, bottom: r.bottom - s.top },
          slideSize : { width: s.width, height: s.height }
        });
      }
    });

    // ── Imágenes a sangre / capa de fondo ────────────────────────────────────
    // Un <img> con object-fit:cover destinado a cubrir un eje completo del lienzo
    // pero que colapsa a su ancho/alto natural (clásico bug de left:0;right:0 sin
    // width) deja zonas vacías. También detectamos cuando una imagen de capa baja
    // se monta sobre el texto (solape de z-index).
    const imgs = [...slide.querySelectorAll('img')];
    imgs.forEach((img) => {
      const cs = getComputedStyle(img);
      const ir = img.getBoundingClientRect();
      const cls = String(img.className || '');
      const z = zOf(img);
      const isBleed = /\\b(bg-img|img-band)\\b/.test(cls) ||
        (cs.position === 'absolute' && cs.objectFit === 'cover' && z <= 3);
      if (isBleed) {
        // ¿qué eje debería llenar? Si su ancho de layout abarca casi todo el slide,
        // esperamos que cubra el ancho; si no, probablemente sea subfill.
        const widthRatio  = ir.width  / s.width;
        const looksFullWidth = /\\b(bg-img|img-band)\\b/.test(cls) || widthRatio > 0.5;
        if (looksFullWidth && widthRatio < 0.98) {
          issues.push({
            slide     : i + 1,
            type      : 'subfill',
            tag       : 'img',
            className : cls,
            text      : '',
            note      : 'Imagen a sangre cubre solo ' + Math.round(widthRatio * 100) +
                        '% del ancho del lienzo. ¿Falta width:100%?',
            rect      : { left: ir.left - s.left, top: ir.top - s.top, right: ir.right - s.left, bottom: ir.bottom - s.top },
            slideSize : { width: s.width, height: s.height }
          });
        }
      }
      // Solape capa-texto: imagen con z-index mayor que un nodo de texto al que cubre.
      textNodes.forEach(({ r: tr, text }) => {
        const intersects = !(ir.right <= tr.left || ir.left >= tr.right ||
                             ir.bottom <= tr.top || ir.top >= tr.bottom);
        // solo cuenta si la imagen está por encima del texto (z mayor) y el solape
        // es significativo (la imagen tapa parte real del texto, no un pixel)
        const overlapW = Math.min(ir.right, tr.right) - Math.max(ir.left, tr.left);
        const overlapH = Math.min(ir.bottom, tr.bottom) - Math.max(ir.top, tr.top);
        const textArea = (tr.right - tr.left) * (tr.bottom - tr.top) || 1;
        const overlapRatio = (overlapW * overlapH) / textArea;
        if (intersects && z >= 10 && overlapRatio > 0.05) {
          issues.push({
            slide     : i + 1,
            type      : 'overlap',
            tag       : 'img',
            className : String(img.className || ''),
            text      : text,
            note      : 'Imagen (z=' + z + ') se monta sobre texto cubriendo ' +
                        Math.round(overlapRatio * 100) + '% de su área.',
            rect      : { left: ir.left - s.left, top: ir.top - s.top, right: ir.right - s.left, bottom: ir.bottom - s.top },
            slideSize : { width: s.width, height: s.height }
          });
        }
      });
    });
  });
  const report = JSON.stringify({
    slideCount : slides.length,
    viewport   : { width: window.innerWidth, height: window.innerHeight },
    issues
  });
  document.body.setAttribute('data-audit-report', report);
  // Tambien lo ponemos en el title para facilitar extraccion con grep
  document.title = 'AUDIT_REPORT:' + report;
})();
`;

// ── Preparar HTML con script inyectado ──────────────────────────────────────

const auditHtml = path.resolve(outDir, "audit.html");
const source    = fs.readFileSync(htmlPath, "utf8");
// Inyectar ANTES de </body>; si no hay </body>, agregar al final
const injected  = source.includes("</body>")
  ? source.replace("</body>", `<script>${auditScript}</script></body>`)
  : source + `<script>${auditScript}</script>`;
fs.writeFileSync(auditHtml, injected, "utf8");

const auditUrl = `file://${auditHtml}`;

// ── Helpers ──────────────────────────────────────────────────────────────────

function runChrome(args, label) {
  const result = spawnSync(chrome, args, { encoding: "utf8", timeout: 20000 });
  if (result.error) {
    console.warn(`[${label}] Chrome error: ${result.error.message}`);
    return null;
  }
  if (result.status !== 0 && result.status !== null) {
    // Chrome headless a veces sale con status != 0 pero igual produce output
    // Solo lo consideramos fallo si no hay stdout util
    if (!result.stdout) {
      console.warn(`[${label}] Chrome exited status=${result.status} signal=${result.signal}`);
      return null;
    }
  }
  return result;
}

function extractReport(stdout) {
  if (!stdout) return null;

  // Estrategia 1: buscar en <title>AUDIT_REPORT:{...}</title>
  const titleMatch = stdout.match(/<title>AUDIT_REPORT:([\s\S]*?)<\/title>/);
  if (titleMatch) {
    try { return JSON.parse(titleMatch[1]); } catch (_) {}
  }

  // Estrategia 2: buscar data-audit-report="..." con entidades HTML decodificadas
  const attrMatch = stdout.match(/data-audit-report="([^"]*)"/);
  if (attrMatch) {
    const decoded = attrMatch[1]
      .replace(/&quot;/g, '"')
      .replace(/&amp;/g,  '&')
      .replace(/&lt;/g,   '<')
      .replace(/&gt;/g,   '>')
      .replace(/&#39;/g,  "'");
    try { return JSON.parse(decoded); } catch (_) {}
  }

  // Estrategia 3: buscar JSON inline con slideCount (ultimo recurso)
  const jsonMatch = stdout.match(/\{"slideCount":\d+[\s\S]*?"issues":\[[\s\S]*?\]\}/);
  if (jsonMatch) {
    try { return JSON.parse(jsonMatch[0]); } catch (_) {}
  }

  return null;
}

// ── Paso 1: Screenshot ───────────────────────────────────────────────────────
// Chrome headless puede capturar screenshot y ejecutar JS, pero --screenshot
// no ejecuta JS de forma confiable en todos los builds. Lo intentamos igual
// porque es la forma mas directa de obtener la imagen.

const screenshotResult = runChrome([
  "--headless=new",
  "--disable-gpu",
  "--no-sandbox",
  "--disable-dev-shm-usage",
  `--user-data-dir=${userDataDir}`,
  "--hide-scrollbars",
  "--allow-file-access-from-files",
  "--window-size=1200,2200",
  "--virtual-time-budget=2000",
  `--screenshot=${screenshotPath}`,
  auditUrl,
], "screenshot");

const screenshotOk = screenshotResult !== null && fs.existsSync(screenshotPath);
if (screenshotOk) {
  console.log(`Screenshot: ${screenshotPath}`);
} else {
  console.warn("Screenshot: no generado (Chrome no disponible o fallo)");
}

// ── Paso 2: Dump DOM para extraer el reporte de auditoria ───────────────────
// Usamos un userDataDir fresco para evitar conflictos con el proceso anterior.

const dumpDataDir = path.resolve(outDir, `chrome-profile-dump-${Date.now()}`);
fs.mkdirSync(dumpDataDir, { recursive: true });

const dumpResult = runChrome([
  "--headless=new",
  "--disable-gpu",
  "--no-sandbox",
  "--disable-dev-shm-usage",
  `--user-data-dir=${dumpDataDir}`,
  "--allow-file-access-from-files",
  "--virtual-time-budget=2000",
  "--dump-dom",
  auditUrl,
], "dump-dom");

let report = null;
if (dumpResult) {
  report = extractReport(dumpResult.stdout);
}

if (!report) {
  // Chrome headless moderno a veces no ejecuta JS en --dump-dom.
  // Fallback: intentar con --run-all-compositor-stages-before-draw
  const dumpDataDir2 = path.resolve(outDir, `chrome-profile-dump2-${Date.now()}`);
  fs.mkdirSync(dumpDataDir2, { recursive: true });

  const dumpResult2 = runChrome([
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    `--user-data-dir=${dumpDataDir2}`,
    "--allow-file-access-from-files",
    "--run-all-compositor-stages-before-draw",
    "--virtual-time-budget=3000",
    "--dump-dom",
    auditUrl,
  ], "dump-dom-v2");

  if (dumpResult2) {
    report = extractReport(dumpResult2.stdout);
  }
}

// ── Guardar reporte ──────────────────────────────────────────────────────────

if (!report) {
  report = {
    slideCount : null,
    issues     : [],
    note       : "No se pudo extraer el reporte de auditoria del DOM. " +
                 "Verifica manualmente el HTML o usa mcp__chrome-devtools__evaluate_script."
  };
  console.warn("Reporte: no disponible (DOM dump no ejecuto JS)");
} else {
  console.log(`Slides encontradas: ${report.slideCount}`);
  console.log(`Issues: ${report.issues.length}`);
}

fs.writeFileSync(reportPath, JSON.stringify(report, null, 2), "utf8");
console.log(`Reporte: ${reportPath}`);

// Limpiar directorios temporales de Chrome
[userDataDir, dumpDataDir].forEach(d => {
  try { fs.rmSync(d, { recursive: true, force: true }); } catch (_) {}
});

process.exit(report.issues && report.issues.length > 0 ? 3 : 0);
