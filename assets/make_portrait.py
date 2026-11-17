"""Builds a dot-matrix (halftone) portrait + profile banner SVG from avatar.png."""
import math
from PIL import Image, ImageFilter
import numpy as np

SRC = "avatar.png"
img = Image.open(SRC).convert("RGB")
W0, H0 = img.size
cx0, cy0, R0 = W0 / 2, H0 / 2, 176

hsv = np.asarray(img.convert("HSV")).astype(float)
H, S, V = hsv[..., 0], hsv[..., 1], hsv[..., 2]
lum = np.asarray(img.convert("L").filter(ImageFilter.UnsharpMask(4, 160, 2)).filter(ImageFilter.GaussianBlur(0.8))).astype(float) / 255

# subject mask: drop the yellow backdrop, the white ring, and the GitHub badge
bg = (V > 222) & (H >= 24) & (H <= 52) & (S > 30)
yy, xx = np.mgrid[0:H0, 0:W0]
outside = (xx - cx0) ** 2 + (yy - cy0) ** 2 > R0 ** 2
badge = (xx - 340) ** 2 + (yy - 304) ** 2 < 34 ** 2
mask_img = Image.fromarray(((~(bg | outside | badge)) * 255).astype(np.uint8))
mask_img = mask_img.filter(ImageFilter.MedianFilter(7)).filter(ImageFilter.GaussianBlur(2))
mask = np.asarray(mask_img).astype(float) / 255

# contrast curve on luminance
lo, hi = np.percentile(lum[mask > 0.5], [3, 99])
l = np.clip((lum - lo) / (hi - lo), 0, 1) ** 1.35


def dots(size, step, ox, oy, groups=24):
    """Return list of (x, y, r, t, g) for a portrait of `size` px placed at (ox, oy)."""
    n = int(size / step)
    out = []
    for j in range(n):
        for i in range(n):
            # hex-offset grid looks more organic
            fx = (i + 0.5 + (0.5 if j % 2 else 0)) / n
            fy = (j + 0.5) / n
            if fx >= 1:
                continue
            sx, sy = int(fx * W0), int(fy * H0)
            m = mask[sy, sx]
            if m < 0.35:
                continue
            b = l[sy, sx]
            r = step * 0.56 * (0.12 + 0.88 * b) * min(1, m * 1.3)
            if r < 0.35:
                continue
            x, y = ox + fx * size, oy + fy * size
            # diagonal sweep index for the reveal animation
            t = (fx * 0.55 + fy * 0.45)
            out.append((x, y, r, t, int(t * (groups - 1))))
    return out


def portrait_group(size, step, ox, oy, groups=24, idp="p"):
    pts = dots(size, step, ox, oy, groups)
    by_g = {}
    for x, y, r, t, g in pts:
        by_g.setdefault(g, []).append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}"/>')
    parts = []
    for g in sorted(by_g):
        parts.append(f'<g class="{idp}g" style="animation-delay:{g * 0.06:.2f}s">' + "".join(by_g[g]) + "</g>")
    return "\n".join(parts), len(pts)


STYLE = """
  .pg{opacity:1;animation:pop .9s cubic-bezier(.2,.8,.2,1) forwards}
  @keyframes pop{0%{opacity:0;transform:translateY(6px)}100%{opacity:1;transform:none}}
  .scan{animation:scan 5.5s ease-in-out 1.8s infinite}
  @keyframes scan{0%{transform:translateY(-10px);opacity:0}10%{opacity:.55}90%{opacity:.55}100%{transform:translateY(360px);opacity:0}}
  .blink{animation:blink 1.1s steps(1) infinite}
  @keyframes blink{50%{opacity:0}}
  .fade{opacity:1;animation:fadein .8s ease forwards}
  @keyframes fadein{to{opacity:1}}
  text{font-family:'Segoe UI',Ubuntu,'Helvetica Neue',Arial,sans-serif}
  .mono{font-family:'JetBrains Mono',Consolas,'SFMono-Regular',Menlo,monospace}
"""

GRAD = """
  <linearGradient id="dotgrad" gradientUnits="userSpaceOnUse" x1="20" y1="20" x2="400" y2="400">
    <stop offset="0" stop-color="#22D3EE"/>
    <stop offset=".5" stop-color="#818CF8"/>
    <stop offset="1" stop-color="#E879F9"/>
  </linearGradient>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0B1020"/>
    <stop offset="1" stop-color="#111827"/>
  </linearGradient>
  <linearGradient id="txt" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#22D3EE"/>
    <stop offset=".55" stop-color="#A78BFA"/>
    <stop offset="1" stop-color="#F472B6"/>
  </linearGradient>
  <radialGradient id="glow" cx=".5" cy=".5" r=".5">
    <stop offset="0" stop-color="#6366F1" stop-opacity=".16"/>
    <stop offset="1" stop-color="#6366F1" stop-opacity="0"/>
  </radialGradient>
  <pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse">
    <circle cx="1" cy="1" r="1" fill="#1F2A44"/>
  </pattern>
"""

# ---------- 1. standalone square portrait ----------
SZ = 420
body, n1 = portrait_group(380, 3.7, 20, 20)
square = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{SZ}" height="{SZ}" viewBox="0 0 {SZ} {SZ}" role="img" aria-label="Dot-matrix portrait of Debanjan Roy">
<title>Debanjan Roy — dot portrait</title>
<defs>{GRAD}<clipPath id="cc"><rect width="{SZ}" height="{SZ}" rx="28"/></clipPath></defs>
<style>{STYLE}</style>
<g clip-path="url(#cc)">
<rect width="{SZ}" height="{SZ}" fill="url(#bg)"/>
<rect width="{SZ}" height="{SZ}" fill="url(#grid)"/>
<circle cx="210" cy="200" r="190" fill="url(#glow)"/>
<g fill="url(#dotgrad)">
{body}
</g>
<rect class="scan" x="0" y="20" width="{SZ}" height="2" fill="#22D3EE" opacity="0"/>
</g>
<rect x=".5" y=".5" width="{SZ-1}" height="{SZ-1}" rx="28" fill="none" stroke="#1E293B"/>
</svg>'''
open("assets/dot-portrait.svg", "w").write(square)

# ---------- 2. wide banner: portrait + identity ----------
BW, BH = 1000, 400
pbody, n2 = portrait_group(352, 3.7, 30, 24)

roles = [
    ("Senior Software Engineer · Team Lead", "@ Bengal IT Hub"),
    ("AI Engineer", "@ Sibiri Innovation (OPC) Pvt Ltd"),
]
chips = ["Full Stack", "Generative AI", "Agentic AI", "LangChain", "LangGraph",
         "ML / DL", "React Native", "Flutter", "Spring Boot", "Laravel"]

chip_svg = []
x, y = 430, 262
for i, c in enumerate(chips):
    w = 14 + len(c) * 7.4
    if x + w > BW - 30:
        x, y = 430, y + 34
    d = 1.6 + i * 0.08
    chip_svg.append(
        f'<g class="fade" style="animation-delay:{d:.2f}s"><rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="25" rx="12.5" '
        f'fill="#111C34" stroke="#2B3A5E"/><text x="{x + w/2:.0f}" y="{y+17}" text-anchor="middle" '
        f'font-size="12.5" fill="#C7D2FE">{c}</text></g>')
    x += w + 8

banner = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{BW}" height="{BH}" viewBox="0 0 {BW} {BH}" role="img" aria-label="Debanjan Roy — Senior Full Stack and AI Engineer, Kolkata">
<title>Debanjan Roy — Senior Full Stack &amp; AI Engineer</title>
<defs>{GRAD}<clipPath id="cb"><rect width="{BW}" height="{BH}" rx="24"/></clipPath></defs>
<style>{STYLE}</style>
<g clip-path="url(#cb)">
<rect width="{BW}" height="{BH}" fill="url(#bg)"/>
<rect width="{BW}" height="{BH}" fill="url(#grid)"/>
<circle cx="206" cy="200" r="200" fill="url(#glow)"/>
<g fill="url(#dotgrad)">
{pbody}
</g>
<rect class="scan" x="20" y="20" width="370" height="2" fill="#22D3EE" opacity="0"/>
<line x1="405" y1="40" x2="405" y2="360" stroke="#1E293B"/>

<g class="fade" style="animation-delay:.6s">
<text x="430" y="70" class="mono" font-size="14" fill="#64748B">~/debanjan-roy $ whoami<tspan class="blink" fill="#22D3EE"> ▍</tspan></text>
</g>
<g class="fade" style="animation-delay:.85s">
<text x="428" y="122" font-size="44" font-weight="800" fill="url(#txt)">Debanjan Roy</text>
<text x="432" y="150" font-size="15" fill="#94A3B8">a.k.a. Babai · Kolkata, West Bengal, India</text>
</g>
<g class="fade" style="animation-delay:1.1s">
<text x="430" y="190" font-size="17" fill="#E2E8F0" font-weight="600">{roles[0][0]} <tspan fill="#818CF8" font-weight="500">{roles[0][1]}</tspan></text>
<text x="430" y="220" font-size="17" fill="#E2E8F0" font-weight="600">{roles[1][0]} <tspan fill="#E879F9" font-weight="500">{roles[1][1]}</tspan></text>
</g>
{"".join(chip_svg)}
<g class="fade" style="animation-delay:2.6s">
<text x="430" y="368" class="mono" font-size="12.5" fill="#475569">// building agentic AI products &amp; full-stack platforms that ship</text>
</g>
</g>
<rect x=".5" y=".5" width="{BW-1}" height="{BH-1}" rx="24" fill="none" stroke="#1E293B"/>
</svg>'''
open("assets/banner.svg", "w").write(banner)
print("dots:", n1, n2)
