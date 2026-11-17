"""Builds the full-colour portrait card + profile banner SVGs from assets/src/photo.jpg.

Run from the repo root:  python assets/scripts/make_portrait.py
Needs: pillow (with WebP), numpy.
"""
import base64
import io

import sys

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

sys.path.insert(0, "assets/scripts")
from brand import BASE_CSS, MONO, SANS, finish, text_width  # noqa: E402

SRC = "assets/src/photo.jpg"


# ---------------------------------------------------------------- cut-out
def cutout(path):
    """Remove the flat yellow studio backdrop and return an RGBA head-and-shoulders crop."""
    im = Image.open(path).convert("RGB")
    arr = np.asarray(im)
    top = 0
    while arr[top].mean() < 60:  # thin black strip on top of the source photo
        top += 1
    im = im.crop((0, top, im.width, im.height))
    W, H = im.size
    hsv = np.asarray(im.convert("HSV")).astype(float)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]

    # backdrop candidates, kept only where connected to the image border
    cand = (h >= 26) & (h <= 52) & (v >= 205) & (s >= 25)
    m = Image.fromarray((cand * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5))
    seed = Image.new("L", (W + 2, H + 2), 255)
    seed.paste(m, (1, 1))
    seed = seed.point(lambda p: 128 if p > 127 else 0)
    seed.paste(128, (0, 0, W + 2, 1))
    seed.paste(128, (0, 0, 1, H + 2))
    seed.paste(128, (W + 1, 0, W + 2, H + 2))
    ImageDraw.floodfill(seed, (0, 0), 255, thresh=0)
    bg = np.asarray(seed)[1:-1, 1:-1] == 255

    fg = Image.fromarray((~bg * 255).astype(np.uint8))
    fg = fg.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.MaxFilter(3))
    fg = fg.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.3))
    a = np.asarray(fg).astype(float) / 255

    # neutralise the yellow spill on soft edge pixels
    rgb = np.asarray(im).astype(float)
    lum = rgb @ np.array([0.299, 0.587, 0.114])
    k = np.clip((1 - a) * 1.6, 0, 1)[..., None] * ((a > 0.01) & (a < 0.99))[..., None]
    neutral = np.stack([np.minimum(lum, 90) * 0.5] * 3, -1)
    rgb = rgb * (1 - k) + neutral * k
    yellowish = (h >= 22) & (h <= 55) & (s > 20) & (v > 150)
    a[(a < 0.7) & yellowish] *= 0.4

    out = Image.fromarray(np.dstack([np.clip(rgb, 0, 255), a * 255]).astype(np.uint8), "RGBA")
    # gentle polish: a touch more contrast and warmth, keep natural colour
    rgb_img = ImageEnhance.Contrast(out.convert("RGB")).enhance(1.06)
    rgb_img = ImageEnhance.Color(rgb_img).enhance(1.05)
    out = Image.merge("RGBA", (*rgb_img.split(), out.getchannel("A")))
    # square crop: full head + shoulders
    return out.crop((0, 0, W, W))


def data_uri(img, px):
    buf = io.BytesIO()
    img.resize((px, px), Image.LANCZOS).save(buf, "WEBP", quality=88, method=6)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()


PHOTO = data_uri(cutout(SRC), 640)

# ---------------------------------------------------------------- shared defs
STYLE = """
  .photo{opacity:1;animation:rise 1.1s cubic-bezier(.2,.8,.2,1) both}
  @keyframes rise{0%{opacity:0;transform:translateY(14px)}100%{opacity:1;transform:none}}
  .pulse{animation:pulse 2.2s ease-in-out infinite}
  @keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}
  .blink{animation:blink 1.1s steps(1) infinite}
  @keyframes blink{50%{opacity:0}}
  .fade{opacity:1;animation:fadein .8s ease both}
  @keyframes fadein{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
"""
STYLE = "/*FONTS*/" + BASE_CSS + STYLE

GRAD = """
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0B1020"/>
    <stop offset="1" stop-color="#111827"/>
  </linearGradient>
  <linearGradient id="txt" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#22D3EE"/>
    <stop offset=".55" stop-color="#A78BFA"/>
    <stop offset="1" stop-color="#F472B6"/>
  </linearGradient>
  <linearGradient id="ringg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#22D3EE"/>
    <stop offset=".5" stop-color="#A78BFA"/>
    <stop offset="1" stop-color="#F472B6"/>
  </linearGradient>
  <radialGradient id="disc" cx=".5" cy=".38" r=".7">
    <stop offset="0" stop-color="#4338CA"/>
    <stop offset=".55" stop-color="#312E81"/>
    <stop offset="1" stop-color="#1E1B4B"/>
  </radialGradient>
  <radialGradient id="glow" cx=".5" cy=".5" r=".5">
    <stop offset="0" stop-color="#818CF8" stop-opacity=".38"/>
    <stop offset="1" stop-color="#6366F1" stop-opacity="0"/>
  </radialGradient>
  <filter id="rim" x="-10%" y="-10%" width="120%" height="120%">
    <feDropShadow dx="0" dy="0" stdDeviation="5" flood-color="#A78BFA" flood-opacity=".55"/>
  </filter>
  <pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse">
    <circle cx="1" cy="1" r="1" fill="#1F2A44"/>
  </pattern>
"""


def portrait(cx, cy, size, uid):
    """Colour photo on a gradient disc with a spinning ring; head pops out above the disc.

    (cx, cy) is the disc centre, `size` the photo edge length.
    """
    r = size * 0.40
    px, py = cx - size / 2, cy - size * 0.56
    return f'''
<circle cx="{cx}" cy="{cy}" r="{r * 1.55:.0f}" fill="url(#glow)"/>
<circle cx="{cx}" cy="{cy}" r="{r + 12:.1f}" fill="none" stroke="url(#ringg)" stroke-width="1.6" stroke-dasharray="3 7" opacity=".6"/>
<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="url(#disc)"/>
<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="none" stroke="url(#ringg)" stroke-width="3"/>
<clipPath id="pc{uid}">
  <circle cx="{cx}" cy="{cy}" r="{r - 1.5:.1f}"/>
  <rect x="{px:.0f}" y="{py - 20:.0f}" width="{size}" height="{cy - py + 20:.0f}"/>
</clipPath>
<g clip-path="url(#pc{uid})"><image class="photo" href="{PHOTO}" x="{px:.1f}" y="{py:.1f}" width="{size}" height="{size}" filter="url(#rim)" preserveAspectRatio="xMidYMid meet"/></g>
'''


# ---------------------------------------------------------------- 1. square portrait card
SZ = 420
card = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{SZ}" height="{SZ}" viewBox="0 0 {SZ} {SZ}" role="img" aria-label="Portrait of Debanjan Roy">
<title>Debanjan Roy</title>
<defs>{GRAD}<clipPath id="cc"><rect width="{SZ}" height="{SZ}" rx="28"/></clipPath></defs>
<style>{STYLE}</style>
<g clip-path="url(#cc)">
<rect width="{SZ}" height="{SZ}" fill="url(#bg)"/>
<rect width="{SZ}" height="{SZ}" fill="url(#grid)"/>
{portrait(210, 222, 330, "a")}
<g class="fade" style="animation-delay:1.2s">
  <rect x="110" y="368" width="200" height="30" rx="15" fill="#0F172A" fill-opacity=".92" stroke="#2B3A5E"/>
  <circle class="pulse" cx="130" cy="383" r="4.5" fill="#34D399"/>
  <text x="142" y="388" font-size="12.5" font-weight="600" fill="#E2E8F0">Open to collaboration</text>
</g>
</g>
<rect x=".5" y=".5" width="{SZ - 1}" height="{SZ - 1}" rx="28" fill="none" stroke="#1E293B"/>
</svg>'''
W8 = [(SANS, 400), (SANS, 600), (SANS, 800), (MONO, 400)]
open("assets/dot-portrait.svg", "w", encoding="utf-8").write(finish(card, W8))

# ---------------------------------------------------------------- 2. wide banner
BW, BH = 1000, 400
roles = [
    ("Senior Software Engineer · Team Lead", "@ Bengal IT Hub"),
    ("AI Engineer", "@ Sibiri Innovation (OPC) Pvt Ltd"),
]
chips = ["Agentic AI", "LangGraph", "Full Stack", "React Native", "Flutter", "ML / DL"]
stats = [("1+ Year", "Experience"), ("2", "Current roles"), ("AI · Web · App", "End-to-end delivery")]

parts = []
sx = 430
for i, (big, small) in enumerate(stats):
    w = 124 if i < 2 else 176
    d = 1.35 + i * 0.12
    parts.append(
        f'<g class="fade" style="animation-delay:{d:.2f}s"><rect x="{sx}" y="242" width="{w}" height="54" rx="10" fill="#0F172A" stroke="#26324F"/>'
        f'<text x="{sx + 12}" y="267" font-size="17" font-weight="800" fill="url(#txt)">{big}</text>'
        f'<text x="{sx + 12}" y="285" font-size="11" fill="#94A3B8" letter-spacing=".3">{small.upper()}</text></g>')
    sx += w + 10
x, y = 430, 312
for i, c in enumerate(chips):
    w = 24 + text_width(c, 12, SANS, 600)
    d = 1.8 + i * 0.08
    parts.append(
        f'<g class="fade" style="animation-delay:{d:.2f}s"><rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="24" rx="12" '
        f'fill="#111C34" stroke="#2B3A5E"/><text x="{x + w / 2:.0f}" y="{y + 16}" text-anchor="middle" '
        f'font-size="12" font-weight="600" fill="#C7D2FE">{c}</text></g>')
    x += w + 7

banner = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{BW}" height="{BH}" viewBox="0 0 {BW} {BH}" role="img" aria-label="Debanjan Roy — Senior Full Stack and AI Engineer, Kolkata">
<title>Debanjan Roy — Senior Full Stack &amp; AI Engineer</title>
<defs>{GRAD}<clipPath id="cb"><rect width="{BW}" height="{BH}" rx="24"/></clipPath></defs>
<style>{STYLE}</style>
<g clip-path="url(#cb)">
<rect width="{BW}" height="{BH}" fill="url(#bg)"/>
<rect width="{BW}" height="{BH}" fill="url(#grid)"/>
{portrait(206, 214, 318, "b")}
<line x1="405" y1="40" x2="405" y2="360" stroke="#1E293B"/>

<g class="fade" style="animation-delay:.6s">
<text x="430" y="70" class="mono" font-size="14" fill="#64748B">~/debanjan-roy $ whoami<tspan class="blink" fill="#22D3EE"> ▍</tspan></text>
</g>
<g class="fade" style="animation-delay:.85s">
<text x="428" y="122" font-size="42" font-weight="800" letter-spacing="-1" fill="url(#txt)">Debanjan Roy</text>
<text x="432" y="150" font-size="15" fill="#94A3B8">a.k.a. Babai · Kolkata, West Bengal, India</text>
</g>
<g class="fade" style="animation-delay:1.1s">
<text x="430" y="190" font-size="16" fill="#E2E8F0" font-weight="600">{roles[0][0]} <tspan fill="#818CF8" font-weight="400">{roles[0][1]}</tspan></text>
<text x="430" y="220" font-size="16" fill="#E2E8F0" font-weight="600">{roles[1][0]} <tspan fill="#E879F9" font-weight="400">{roles[1][1]}</tspan></text>
</g>
{"".join(parts)}
<g class="fade" style="animation-delay:2.6s">
<text x="430" y="370" class="mono" font-size="12.5" fill="#475569">// building agentic AI products &amp; full-stack platforms that ship</text>
</g>
</g>
<rect x=".5" y=".5" width="{BW - 1}" height="{BH - 1}" rx="24" fill="none" stroke="#1E293B"/>
</svg>'''
open("assets/banner.svg", "w", encoding="utf-8").write(finish(banner, W8))
print("photo bytes:", len(PHOTO))
