"""Section header SVGs in the same visual language as the banner.

Run from the repo root:  python assets/scripts/make_headers.py
"""
import sys
from xml.sax.saxutils import escape

sys.path.insert(0, "assets/scripts")
from brand import BASE_CSS, GRADIENT_STOPS, MONO, SANS, finish, text_width  # noqa: E402

SECTIONS = [
    ("about", "01", "About Me", "who I am · what I do"),
    ("bring", "02", "What I Bring", "core strengths"),
    ("stack", "03", "Tech Stack", "languages · frameworks · AI · cloud"),
    ("experience", "04", "Experience", "professional journey"),
    ("projects", "05", "Featured Projects", "products & client work"),
    ("now", "06", "Currently", "building · leading · exploring"),
    ("stats", "07", "GitHub Activity", "streaks & contributions"),
    ("connect", "08", "Let's Connect", "open to collaboration"),
]

for slug, num, title, sub in SECTIONS:
    tw = text_width(title, 28, SANS, 800)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="70" viewBox="0 0 1000 70" role="img" aria-label="{escape(title)}">
<title>{escape(title)}</title>
<defs>
<linearGradient id="t" x1="0" x2="1">{GRADIENT_STOPS}</linearGradient>
<linearGradient id="ln" x1="0" x2="1"><stop offset="0" stop-color="#A78BFA" stop-opacity=".9"/><stop offset="1" stop-color="#A78BFA" stop-opacity="0"/></linearGradient>
</defs>
<style>/*FONTS*/{BASE_CSS}
.in{{animation:in .7s ease both}}@keyframes in{{from{{opacity:0;transform:translateX(-8px)}}to{{opacity:1;transform:none}}}}
.grow{{transform-origin:left;animation:g 1.1s .25s cubic-bezier(.2,.8,.2,1) both}}@keyframes g{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}</style>
<g class="in">
<rect x="1" y="14" width="54" height="40" rx="11" fill="#111827" stroke="#334155"/>
<text x="28" y="40" class="mono" font-size="16" font-weight="600" text-anchor="middle" fill="url(#t)">{num}</text>
<text x="72" y="44" font-size="28" font-weight="800" fill="url(#t)" letter-spacing="-.4">{escape(title)}</text>
<text x="{72 + tw + 13:.0f}" y="43" class="mono" font-size="13" fill="#8B95A7">// {escape(sub)}</text>
</g>
<rect class="grow" x="72" y="58" width="928" height="2" rx="1" fill="url(#ln)"/>
</svg>'''
    open(f"assets/headers/{slug}.svg", "w", encoding="utf-8").write(finish(svg, [(SANS, 800), (MONO, 400), (MONO, 600)]))
print("headers ok")
