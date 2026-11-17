"""Tech-stack board: one SVG, brand icons on uniform tiles, grouped by category.

Run from the repo root:  python assets/scripts/make_stack.py
"""
import sys

sys.path.insert(0, "assets/scripts")
from brand import BASE_CSS, GRADIENT_STOPS, MONO, SANS, finish, icon  # noqa: E402

ROWS = [
    ("Languages", "core", [("openjdk", "Java"), ("python", "Python"), ("javascript", "JavaScript"), ("php", "PHP"),
                           ("c", "C"), ("dart", "Dart"), ("html5", "HTML5"), ("css3", "CSS3")]),
    ("Frontend", "web ui", [("react", "React"), ("redux", "Redux"), ("tailwindcss", "Tailwind"), ("bootstrap", "Bootstrap"),
                            ("mui", "Material UI"), ("jquery", "jQuery"), ("figma", "Figma")]),
    ("Mobile", "cross-platform", [("react", "React Native"), ("flutter", "Flutter"), ("dart", "Dart"),
                                  ("androidstudio", "Android Studio")]),
    ("Backend", "apis &amp; services", [("nodedotjs", "Node.js"), ("express", "Express"), ("springboot", "Spring Boot"),
                                    ("laravel", "Laravel"), ("fastapi", "FastAPI"), ("php", "PHP"), ("celery", "Celery")]),
    ("Databases", "data layer", [("mongodb", "MongoDB"), ("mysql", "MySQL"), ("postgresql", "PostgreSQL"),
                                 ("sqlite", "SQLite"), ("firebase", "Firebase")]),
    ("Generative AI", "agents · llms · rag", [("langchain", "LangChain"), ("langchain", "LangGraph"), ("openai", "OpenAI"),
                                              ("googlegemini", "Gemini"), ("ollama", "Ollama"), ("huggingface", "Hugging Face")]),
    ("ML &amp; Data", "models · analysis", [("pytorch", "PyTorch"), ("tensorflow", "TensorFlow"), ("scikitlearn", "scikit-learn"),
                                        ("opencv", "OpenCV"), ("numpy", "NumPy"), ("pandas", "Pandas"),
                                        ("matplotlib", "Matplotlib"), ("jupyter", "Jupyter")]),
    ("Cloud &amp; DevOps", "ship &amp; run", [("amazonaws", "AWS"), ("googlecloud", "Google Cloud"), ("vercel", "Vercel"),
                                      ("linux", "Linux"), ("ubuntu", "Ubuntu"), ("githubactions", "GH Actions")]),
    ("Tools", "daily drivers", [("git", "Git"), ("github", "GitHub"), ("visualstudiocode", "VS Code"),
                                ("intellijidea", "IntelliJ"), ("postman", "Postman"), ("npm", "npm")]),
]

W = 1000
TOP = 24
ROW_H = 98
TILE = 54
PITCH = 92
X0 = 248
H = TOP * 2 + ROW_H * len(ROWS) - 14

body = []
for r, (title, sub, items) in enumerate(ROWS):
    y = TOP + r * ROW_H
    d = 0.08 * r
    body.append(f'<g class="row" style="animation-delay:{d:.2f}s">')
    if r:
        body.append(f'<line x1="28" y1="{y - 10}" x2="{W - 28}" y2="{y - 10}" stroke="#1B2540"/>')
    body.append(f'<rect x="28" y="{y + 14}" width="3" height="28" rx="1.5" fill="url(#acc)"/>')
    body.append(f'<text x="44" y="{y + 32}" font-size="17" font-weight="700" fill="#F1F5F9">{title}</text>')
    body.append(f'<text x="44" y="{y + 52}" class="mono" font-size="11.5" fill="#64748B">{sub} · {len(items)}</text>')
    for i, (slug, label) in enumerate(items):
        cx = X0 + i * PITCH + PITCH / 2
        tx = cx - TILE / 2
        body.append(
            f'<g class="tile"><rect x="{tx:.0f}" y="{y}" width="{TILE}" height="{TILE}" rx="14" fill="url(#tile)" stroke="#26324F"/>'
            + icon(slug, f"{cx - 15:.0f}", y + 12, 30)
            + f'<text x="{cx:.0f}" y="{y + TILE + 18}" text-anchor="middle" font-size="11" font-weight="600" fill="#94A3B8">{label}</text></g>')
    body.append("</g>")

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Tech stack">
<title>Tech stack</title>
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0B1020"/><stop offset="1" stop-color="#111827"/></linearGradient>
<linearGradient id="tile" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#172036"/><stop offset="1" stop-color="#10172A"/></linearGradient>
<linearGradient id="acc" x1="0" y1="0" x2="0" y2="1">{GRADIENT_STOPS}</linearGradient>
<pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#172038"/></pattern>
</defs>
<style>/*FONTS*/{BASE_CSS}
  .row{{animation:up .6s cubic-bezier(.2,.8,.2,1) both}}
  @keyframes up{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
</style>
<rect width="{W}" height="{H}" rx="20" fill="url(#bg)"/>
<rect width="{W}" height="{H}" rx="20" fill="url(#grid)"/>
{"".join(body)}
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="20" fill="none" stroke="#1E293B"/>
</svg>'''

open("assets/stack.svg", "w", encoding="utf-8").write(finish(svg, [(SANS, 600), (SANS, 700), (MONO, 400)]))
print("stack.svg", H)
