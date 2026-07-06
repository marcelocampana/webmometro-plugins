#!/usr/bin/env python3
"""
Extrae datos de PageSpeed Insights (PSI v5) + Core Web Vitals de campo (CrUX) para una URL.

Es un extractor SOLO DE DATOS, pensado para ser invocado por las skills de snapshot
(site-snapshot, page-snapshot). Devuelve números crudos, sin ratings ni interpretación: la
lectura "bueno/malo" vive en la capa analítica (seo-audit/references/rendimiento-web.md), no aquí.

No depende de paquetes externos (solo stdlib: urllib) para no requerir `pip install` en la
máquina del usuario, siguiendo el mismo criterio que scripts/generar_reporte.py del tracker.

Credencial (Google API key para PSI/CrUX), en este orden:
  1. Variable de entorno GOOGLE_API_KEY (la key en crudo)
  2. Variable de entorno CLAUDE_SEO_GOOGLE_API (ruta a un archivo JSON, o a un directorio que
     contenga google-api.json) — para credenciales guardadas fuera de la ubicación por defecto
  3. Campo "api_key" en ~/.config/claude-seo/google-api.json (ubicación por defecto)
La key NUNCA vive en el plugin ni en el repo; se resuelve por convención desde fuera.

Uso:
    python3 pagespeed_field.py <url> [--strategy mobile|desktop|both] [--json]

Salida (--json): un objeto con una entrada por estrategia. Si no hay API key, sale con código 3
y un objeto {"error": "no_api_key", ...} para que la skill degrade explícitamente al fallback
de DataForSEO Lighthouse (lab-only) sin abortar el snapshot.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

PSI_ENDPOINT = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
CONFIG_FILENAME = "google-api.json"

# Ubicación por defecto, genérica (sin rutas personales para que el plugin sea compartible).
# Cada usuario apunta a SU credencial vía la env var CLAUDE_SEO_GOOGLE_API o GOOGLE_API_KEY
# (ver README de seo-suite). La key vive siempre fuera del repo.
DEFAULT_CONFIG_PATH = Path.home() / ".config" / "claude-seo" / CONFIG_FILENAME

# Métricas de campo (CrUX) que reportamos, con su clave en la respuesta PSI.
FIELD_METRICS = {
    "LARGEST_CONTENTFUL_PAINT_MS": "lcp_ms",
    "INTERACTION_TO_NEXT_PAINT": "inp_ms",
    "CUMULATIVE_LAYOUT_SHIFT_SCORE": "cls",
    "FIRST_CONTENTFUL_PAINT_MS": "fcp_ms",
    "EXPERIMENTAL_TIME_TO_FIRST_BYTE": "ttfb_ms",
}

# Auditorías de laboratorio (Lighthouse) que reportamos.
LAB_AUDITS = {
    "largest-contentful-paint": "lcp",
    "first-contentful-paint": "fcp",
    "cumulative-layout-shift": "cls",
    "total-blocking-time": "tbt",
    "speed-index": "speed_index",
    "interactive": "tti",
    "server-response-time": "ttfb",
}


def _read_key_from_file(path):
    """Lee el campo api_key de un JSON. Devuelve la key o None si no existe/está malformado."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        key = data.get("api_key")
        return key.strip() if key else None
    except (json.JSONDecodeError, OSError):
        return None


def resolve_api_key():
    """
    Devuelve la Google API key resolviéndola por convención, o None si no está configurada.
    Orden: GOOGLE_API_KEY (crudo) → CLAUDE_SEO_GOOGLE_API (ruta) → ubicación por defecto.
    """
    key = os.environ.get("GOOGLE_API_KEY")
    if key:
        return key.strip()

    override = os.environ.get("CLAUDE_SEO_GOOGLE_API")
    if override:
        path = Path(override).expanduser()
        if path.is_dir():
            path = path / CONFIG_FILENAME
        if path.exists():
            return _read_key_from_file(path)

    if DEFAULT_CONFIG_PATH.exists():
        return _read_key_from_file(DEFAULT_CONFIG_PATH)

    return None


def fetch(url, strategy, api_key):
    """Llama a PSI para una estrategia y devuelve la respuesta JSON cruda."""
    params = {
        "url": url,
        "strategy": strategy,
        "key": api_key,
        "category": "PERFORMANCE",
    }
    query = urllib.parse.urlencode(params)
    req = urllib.request.Request(f"{PSI_ENDPOINT}?{query}", headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def parse_field(payload):
    """Extrae Core Web Vitals de campo (CrUX) del payload PSI. None si no hay datos de campo."""
    crux = payload.get("loadingExperience", {})
    metrics = crux.get("metrics")
    if not metrics:
        return None
    out = {"overall_category": crux.get("overall_category")}
    for psi_key, our_key in FIELD_METRICS.items():
        m = metrics.get(psi_key)
        if m:
            out[our_key] = {
                "p75": m.get("percentile"),
                "category": m.get("category"),
            }
    return out


def parse_lab(payload):
    """Extrae score de performance y métricas de laboratorio (Lighthouse) del payload PSI."""
    lh = payload.get("lighthouseResult", {})
    audits = lh.get("audits", {})
    perf = lh.get("categories", {}).get("performance", {}).get("score")
    out = {"performance_score": round(perf * 100) if isinstance(perf, (int, float)) else None}
    for audit_key, our_key in LAB_AUDITS.items():
        a = audits.get(audit_key, {})
        if "numericValue" in a:
            out[our_key] = {
                "value": a.get("numericValue"),
                "display": a.get("displayValue"),
            }
    return out


def analyze(url, strategy, api_key):
    payload = fetch(url, strategy, api_key)
    return {
        "strategy": strategy,
        "final_url": payload.get("lighthouseResult", {}).get("finalUrl", url),
        "field": parse_field(payload),      # None => sin datos de campo CrUX para esta URL
        "lab": parse_lab(payload),
    }


def main():
    parser = argparse.ArgumentParser(description="Extrae PSI v5 + CrUX (solo datos) para una URL.")
    parser.add_argument("url", help="URL a analizar")
    parser.add_argument("--strategy", choices=["mobile", "desktop", "both"], default="both")
    parser.add_argument("--json", action="store_true", help="Salida JSON (recomendado para skills)")
    args = parser.parse_args()

    api_key = resolve_api_key()
    if not api_key:
        result = {
            "error": "no_api_key",
            "message": (
                "No hay Google API key configurada (env GOOGLE_API_KEY ni "
                "~/.config/claude-seo/google-api.json). La skill debe degradar al fallback "
                "DataForSEO Lighthouse (lab-only, sin datos de campo CrUX)."
            ),
            "url": args.url,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 3

    strategies = ["mobile", "desktop"] if args.strategy == "both" else [args.strategy]
    results, errors = {}, {}
    for strat in strategies:
        try:
            results[strat] = analyze(args.url, strat, api_key)
        except urllib.error.HTTPError as exc:
            errors[strat] = f"HTTP {exc.code}: {exc.reason}"
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            errors[strat] = str(exc)

    output = {"url": args.url, "results": results}
    if errors:
        output["errors"] = errors

    print(json.dumps(output, ensure_ascii=False, indent=2))
    # Código 4: la key existe pero fallaron todas las estrategias (p. ej. cuota/HTTP 429).
    return 0 if results else 4


if __name__ == "__main__":
    sys.exit(main())
