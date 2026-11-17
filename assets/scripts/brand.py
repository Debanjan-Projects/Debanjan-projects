"""Shared design tokens for every generated SVG: palette, embedded fonts, brand icons.

Fonts are subset to the characters an SVG actually uses and embedded as base64 WOFF2,
so they render the same everywhere (GitHub serves SVGs as <img>, which cannot load web fonts).
"""
import base64
import io
import json
import os
import re

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = os.path.join(os.path.dirname(__file__), "..")
FONT_DIR = os.path.join(ROOT, "src", "fonts")
ICON_DIR = os.path.join(ROOT, "src", "icons")

SANS = "Sora"
MONO = "JBMono"
FONT_FILES = {
    (SANS, 400): "sora-400.woff2",
    (SANS, 600): "sora-600.woff2",
    (SANS, 700): "sora-700.woff2",
    (SANS, 800): "sora-800.woff2",
    (MONO, 400): "jbmono-400.woff2",
    (MONO, 600): "jbmono-600.woff2",
}

BASE_CSS = f"""
  text{{font-family:'{SANS}','Segoe UI',Ubuntu,'Helvetica Neue',Arial,sans-serif}}
  .mono{{font-family:'{MONO}','JetBrains Mono',Consolas,Menlo,monospace}}
"""

GRADIENT_STOPS = '<stop offset="0" stop-color="#22D3EE"/><stop offset=".55" stop-color="#A78BFA"/><stop offset="1" stop-color="#F472B6"/>'


def _subset_b64(path, chars):
    font = TTFont(path)
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga", "calt"]
    opts.name_IDs = []
    s = subset.Subsetter(opts)
    s.populate(text=chars + " ")
    s.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff2"
    font.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


def font_css(svg_body, weights=((SANS, 400), (SANS, 600), (SANS, 700), (SANS, 800), (MONO, 400), (MONO, 600))):
    """@font-face rules for the given (family, weight) pairs, subset to the text inside svg_body."""
    import html

    texts = re.findall(r">([^<>]+)<", svg_body)
    chars = "".join(sorted(set(html.unescape("".join(texts)))))
    rules = []
    for fam, w in weights:
        b64 = _subset_b64(os.path.join(FONT_DIR, FONT_FILES[(fam, w)]), chars)
        rules.append(f"@font-face{{font-family:'{fam}';font-weight:{w};src:url(data:font/woff2;base64,{b64}) format('woff2')}}")
    return "\n".join(rules)


def finish(svg_template, weights=None):
    """Replace the /*FONTS*/ marker in an SVG string with embedded, subset fonts."""
    css = font_css(svg_template) if weights is None else font_css(svg_template, weights)
    return svg_template.replace("/*FONTS*/", css)


_METRICS = {}


def text_width(text, size, family=SANS, weight=400):
    """Exact advance width of `text` in px, from the embedded font's metrics."""
    key = (family, weight)
    if key not in _METRICS:
        f = TTFont(os.path.join(FONT_DIR, FONT_FILES[key]))
        _METRICS[key] = (f.getBestCmap(), f["hmtx"].metrics, f["head"].unitsPerEm)
    cmap, hmtx, upm = _METRICS[key]
    return sum(hmtx[cmap[ord(c)]][0] for c in text if ord(c) in cmap) * size / upm


# ------------------------------------------------------------------ brand icons
_COLORS = json.load(open(os.path.join(ICON_DIR, "colors.json")))


def _lum(hexc):
    r, g, b = (int(hexc[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _readable(hexc):
    """Keep the brand hue but lift very dark colours toward white so they read on navy."""
    lum = _lum(hexc)
    if lum >= 0.3:
        return f"#{hexc}"
    t = 0.75 if lum < 0.08 else 0.5
    rgb = [int(hexc[i:i + 2], 16) for i in (0, 2, 4)]
    return "#" + "".join(f"{round(c + (255 - c) * t):02X}" for c in rgb)


def icon(slug, x, y, size, color=None):
    """Brand icon as a nested <svg>; dark brand colours are lifted so they read on navy."""
    raw = open(os.path.join(ICON_DIR, f"{slug}.svg"), encoding="utf-8").read()
    vb = re.search(r'viewBox="([^"]+)"', raw).group(1)
    inner = re.sub(r"^.*?<svg[^>]*>|</svg>\s*$", "", raw, flags=re.S)
    inner = re.sub(r"<title>.*?</title>", "", inner, flags=re.S)
    hexc = _COLORS.get(slug)
    if hexc is None:  # multi-colour icon (devicon), keep its own fills
        return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="{vb}">{inner}</svg>'
    fill = color or _readable(hexc)
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="{vb}" fill="{fill}">{inner}</svg>'
