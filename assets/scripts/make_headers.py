"""Section header SVGs in the same visual language as the banner."""
SECTIONS = [
    ("about", "01", "About Me", "who I am · what I do"),
    ("bring", "02", "What I Bring", "core strengths"),
    ("stack", "03", "Tech Stack", "languages · frameworks · AI · cloud"),
    ("experience", "04", "Experience", "1+ year of professional work"),
    ("projects", "05", "Featured Projects", "products & client work"),
    ("now", "06", "Currently", "building · leading · exploring"),
    ("stats", "07", "GitHub Analytics", "activity & contributions"),
    ("connect", "08", "Let's Connect", "open to collaboration"),
]
from xml.sax.saxutils import escape
for slug, num, title, sub in SECTIONS:
    sub = escape(sub)
    tw = 20 + len(title) * 14.6
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="70" viewBox="0 0 1000 70" role="img" aria-label="{title}">
<title>{title}</title>
<defs>
<linearGradient id="t" x1="0" x2="1"><stop offset="0" stop-color="#22D3EE"/><stop offset=".55" stop-color="#A78BFA"/><stop offset="1" stop-color="#F472B6"/></linearGradient>
<linearGradient id="ln" x1="0" x2="1"><stop offset="0" stop-color="#A78BFA" stop-opacity=".9"/><stop offset="1" stop-color="#A78BFA" stop-opacity="0"/></linearGradient>
</defs>
<style>text{{font-family:'Segoe UI',Ubuntu,'Helvetica Neue',Arial,sans-serif}}.m{{font-family:'JetBrains Mono',Consolas,Menlo,monospace}}
.in{{opacity:1;animation:in .7s ease forwards}}@keyframes in{{from{{opacity:0;transform:translateX(-8px)}}to{{opacity:1;transform:none}}}}
.grow{{transform-origin:left;transform:scaleX(1);animation:g 1.1s .25s cubic-bezier(.2,.8,.2,1) forwards}}@keyframes g{{to{{transform:scaleX(1)}}}}</style>
<g class="in">
<rect x="0" y="14" width="56" height="40" rx="10" fill="#111827" stroke="#334155"/>
<text x="28" y="40" class="m" font-size="16" font-weight="700" text-anchor="middle" fill="url(#t)">{num}</text>
<text x="72" y="44" font-size="28" font-weight="800" fill="url(#t)">{title}</text>
<text x="{72 + tw:.0f}" y="44" class="m" font-size="13" fill="#8B95A7">// {sub}</text>
</g>
<rect class="grow" x="72" y="58" width="928" height="2" rx="1" fill="url(#ln)"/>
</svg>'''
    open(f"assets/headers/{slug}.svg", "w").write(svg)
print("ok")
