"""Custom SVG cards for the profile README (same design language as banner.svg)."""
import os
from xml.sax.saxutils import escape as esc

os.makedirs("assets/cards", exist_ok=True)

FONT = "'Segoe UI',Ubuntu,'Helvetica Neue',Arial,sans-serif"
MONO = "'JetBrains Mono',Consolas,'SFMono-Regular',Menlo,monospace"

DEFS = """
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0B1020"/><stop offset="1" stop-color="#111827"/></linearGradient>
<linearGradient id="acc" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#22D3EE"/><stop offset=".55" stop-color="#A78BFA"/><stop offset="1" stop-color="#F472B6"/></linearGradient>
<linearGradient id="accv" gradientUnits="userSpaceOnUse" x1="0" y1="30" x2="0" y2="680"><stop offset="0" stop-color="#22D3EE"/><stop offset=".5" stop-color="#A78BFA"/><stop offset="1" stop-color="#F472B6"/></linearGradient>
<linearGradient id="card" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#131C33"/><stop offset="1" stop-color="#0E1529"/></linearGradient>
<pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#1A2440"/></pattern>
<radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#7C3AED" stop-opacity=".22"/><stop offset="1" stop-color="#7C3AED" stop-opacity="0"/></radialGradient>
"""

STYLE = f"""
text{{font-family:{FONT}}} .m{{font-family:{MONO}}}
.up{{opacity:0;animation:up .7s cubic-bezier(.2,.8,.2,1) forwards}}
@keyframes up{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
.pulse{{animation:pulse 1.8s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}
@keyframes pulse{{0%,100%{{opacity:.9;transform:scale(1)}}50%{{opacity:.25;transform:scale(1.9)}}}}
.draw{{stroke-dasharray:1200;stroke-dashoffset:1200;animation:draw 2.2s .2s ease forwards}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
.blink{{animation:blink 1s steps(1) infinite}} @keyframes blink{{50%{{opacity:0}}}}
.type{{opacity:0;animation:type .01s forwards}} @keyframes type{{to{{opacity:1}}}}
"""


def wrap(text, width_px, size, factor=0.53):
    max_chars = int(width_px / (size * factor))
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) > max_chars:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    if cur:
        lines.append(cur)
    return lines


def tags(x, y, items, max_x, size=11.5, h=22, gap=6):
    out, cx, cy = [], x, y
    for t in items:
        w = 16 + len(t) * size * 0.58
        if cx + w > max_x:
            cx, cy = x, cy + h + 6
        out.append(f'<rect x="{cx:.0f}" y="{cy}" width="{w:.0f}" height="{h}" rx="{h/2}" fill="#18213D" stroke="#2D3B63"/>'
                   f'<text x="{cx + w/2:.0f}" y="{cy + h*0.69:.0f}" font-size="{size}" text-anchor="middle" fill="#C7D2FE">{esc(t)}</text>')
        cx += w + gap
    return "".join(out), cy + h


def svg(w, h, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">'
            f'<title>{esc(label)}</title><defs>{DEFS}</defs><style>{STYLE}</style>'
            f'<clipPath id="r"><rect width="{w}" height="{h}" rx="20"/></clipPath>'
            f'<g clip-path="url(#r)"><rect width="{w}" height="{h}" fill="url(#bg)"/><rect width="{w}" height="{h}" fill="url(#grid)"/>{body}</g>'
            f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="20" fill="none" stroke="#1E293B"/></svg>')


# ───────────────────────── 1. What I Bring (3 × 2 grid) ─────────────────────────
BRING = [
    ("🤖", "Agentic & Generative AI", "Multi-agent workflows with LangGraph, tool-using agents with LangChain, RAG over private data and fully offline LLMs with Ollama.", ["LangGraph", "LangChain", "RAG", "Ollama"]),
    ("🌐", "Full Stack Engineering", "Production web platforms end to end: REST APIs, auth, data modelling and fast, responsive, animated interfaces.", ["MERN", "Spring Boot", "Laravel", "FastAPI"]),
    ("📱", "Cross-Platform Mobile", "One codebase for Android & iOS with clean state management, smooth UI and solid API integration.", ["React Native", "Flutter", "Dart"]),
    ("📊", "ML · DL · Data Science", "From data wrangling and visualisation to training and evaluating classical ML and deep-learning models.", ["PyTorch", "scikit-learn", "Pandas"]),
    ("👥", "Leadership & Delivery", "Leading a remote team: sprint planning, code reviews, mentoring and owning client delivery start to finish.", ["Team Lead", "Agile", "Code Review"]),
    ("🔐", "Networking & Security", "Secure-by-default backends with role-based access, validation and strong networking fundamentals.", ["RBAC", "Auth", "Networking"]),
]
W, H = 1000, 470
cw, ch, gx, gy, ox, oy = 312, 205, 18, 20, 24, 22
body = ['<circle cx="500" cy="235" r="380" fill="url(#glow)"/>']
for i, (ico, title, desc, tg) in enumerate(BRING):
    c, r = i % 3, i // 3
    x, y = ox + c * (cw + gx), oy + r * (ch + gy)
    d = 0.1 + i * 0.12
    lines = wrap(desc, cw - 40, 13)
    desc_svg = "".join(f'<text x="{x+20}" y="{y+92+k*19}" font-size="13" fill="#A3AEC2">{esc(l)}</text>' for k, l in enumerate(lines[:4]))
    tg_svg, _ = tags(x + 20, y + ch - 40, tg, x + cw - 14)
    body.append(
        f'<g class="up" style="animation-delay:{d:.2f}s">'
        f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="16" fill="url(#card)" stroke="#24304F"/>'
        f'<rect x="{x}" y="{y}" width="{cw}" height="3" rx="1.5" fill="url(#acc)"/>'
        f'<rect x="{x+20}" y="{y+22}" width="38" height="38" rx="10" fill="#1A2342" stroke="#2D3B63"/>'
        f'<text x="{x+39}" y="{y+48}" font-size="19" text-anchor="middle">{ico}</text>'
        f'<text x="{x+72}" y="{y+47}" font-size="17" font-weight="700" fill="#F1F5F9">{esc(title)}</text>'
        f'{desc_svg}{tg_svg}</g>')
open("assets/cards/bring.svg", "w").write(svg(W, H, "".join(body), "What I bring"))

# ───────────────────────── 2. Experience timeline ─────────────────────────
EXP = [
    ("Aug 2026 — Present", "Kolkata · On-site", True, "AI Engineer", "Sibiri Innovation (OPC) Pvt Ltd",
     ["Designing agentic AI products: SIBIRI Educational Content OS & EngiMate",
      "LangGraph multi-agent pipelines, RAG and on-device LLMs with Ollama",
      "Delivering client platforms in Laravel · PHP · MySQL"]),
    ("Apr 2026 — Present", "Remote", True, "Senior Software Engineer · Team Lead", "Bengal IT Hub",
     ["Leading a remote engineering team: planning, architecture, code review",
      "Owning client projects end to end, requirements through deployment",
      "Promoted from Junior Software Engineer (Biswa Bangla Hub)"]),
    ("Dec 2025 — Apr 2026", "Kolkata · On-site", False, "Junior Software Engineer", "Biswa Bangla Hub",
     ["Software design and feature delivery across client projects"]),
    ("Apr 2025 — Nov 2025", "Kolkata · On-site", False, "Agentic AI Intern", "Sibiri Innovation",
     ["Built AI agents and data workflows in Python, NumPy and LLM frameworks"]),
    ("Dec 2023 — Sep 2024", "Kolkata", False, "Full Stack · JavaScript · PHP Trainee", "Euphoria GenX · Nikhil Bharat Shiksha Parishad",
     ["MERN, modern JavaScript, PHP & MySQL: CRUD, auth, APIs, database design"]),
]
W = 1000
LX = 230  # timeline x
y = 40
parts = []
for i, (when, where, now, role, org, pts) in enumerate(EXP):
    h = 70 + len(pts) * 22
    d = 0.3 + i * 0.25
    node = (f'<circle cx="{LX}" cy="{y+26}" r="11" fill="#22D3EE" class="pulse"/>' if now else "") + \
           f'<circle cx="{LX}" cy="{y+26}" r="7" fill="{"#22D3EE" if now else "#0B1020"}" stroke="{"#7DF9FF" if now else "#A78BFA"}" stroke-width="2.5"/>'
    badge = (f'<rect x="{W-24-90}" y="{y+14}" width="80" height="22" rx="11" fill="#064E3B" stroke="#10B981"/>'
             f'<circle cx="{W-24-80}" cy="{y+25}" r="3.5" fill="#34D399" class="pulse"/>'
             f'<text x="{W-24-43}" y="{y+29.5}" font-size="10" font-weight="700" text-anchor="middle" fill="#6EE7B7" letter-spacing=".5">CURRENT</text>') if now else ""
    pts_svg = "".join(f'<circle cx="{LX+44}" cy="{y+73+k*22}" r="2.6" fill="#A78BFA"/>'
                      f'<text x="{LX+56}" y="{y+78+k*22}" font-size="13.5" fill="#A3AEC2">{esc(p)}</text>' for k, p in enumerate(pts))
    parts.append(
        f'<g class="up" style="animation-delay:{d:.2f}s">'
        f'<text x="{LX-26}" y="{y+24}" font-size="14" font-weight="700" text-anchor="end" fill="{"#E2E8F0" if now else "#CBD5E1"}">{when}</text>'
        f'<text x="{LX-26}" y="{y+44}" font-size="12" text-anchor="end" fill="#64748B">{where}</text>'
        f'{node}'
        f'<rect x="{LX+26}" y="{y}" width="{W-LX-50}" height="{h}" rx="14" fill="url(#card)" stroke="{"#3B3A7A" if now else "#24304F"}"/>'
        f'<text x="{LX+44}" y="{y+28}" font-size="17" font-weight="700" fill="#F1F5F9">{esc(role)}</text>{badge}'
        f'<text x="{LX+44}" y="{y+50}" font-size="13.5" font-weight="600" fill="url(#acc)">{esc(org)}</text>'
        f'{pts_svg}</g>')
    y += h + 18
H = y + 22
line = f'<line x1="{LX}" y1="30" x2="{LX}" y2="{H-30}" stroke="url(#accv)" stroke-width="2.5" class="draw" stroke-linecap="round"/>'
open("assets/cards/experience.svg", "w").write(svg(W, H, line + "".join(parts), "Professional experience timeline"))

# ───────────────────────── 3. Project cards ─────────────────────────
PROJ = [
    ("sibiri", "🎓", "SIBIRI", "Educational Content OS", "AGENTIC AI · EDTECH",
     "An agentic AI operating system for teachers. Upload notes; agents analyse the lesson, plan content and generate quizzes, videos, labs and mind maps, then publish to Moodle.",
     ["LangGraph", "LangChain", "FastAPI", "ChromaDB", "Celery", "PostgreSQL", "Moodle API"], "In development", "#A78BFA"),
    ("engimate", "🛠️", "EngiMate", "Offline AI Agent for Engineers", "LOCAL LLM · DESKTOP",
     "A fully offline AI assistant for engineering students on Windows, macOS and Linux. v2 adds voice-to-text note-making and spoken-English practice. Licensed per machine.",
     ["Python", "Ollama", "Local LLM", "Speech-to-Text", "Nuitka"], "sibiri.in", "#22D3EE"),
    ("fastgate", "🔐", "FastGate", "AI Gate-Pass Platform", "UI/UX · WEB",
     "Complete product website for an AI-enabled gate-pass and campus-security system: multi-page, dark/light theming, premium UI with 3D visuals and motion.",
     ["UI/UX", "HTML5", "CSS3", "JavaScript", "Animations"], "fastgate.in", "#F472B6"),
    ("dhanantari", "✈️", "Dhanantari Suite", "Travel & Education Platforms", "CLIENT · ERP / SAAS",
     "Platforms for Dhanantari Tourism Pvt Ltd (Swapnokamal, Anukul & Rajeet Travels) and Kamal Dutta Education, built to grow into a full ERP / SaaS product.",
     ["Laravel", "PHP", "MySQL", "ERP", "SaaS"], "Client project", "#34D399"),
]
W, H = 490, 310
for slug, ico, name, sub, kind, desc, tg, foot, col in PROJ:
    lines = wrap(desc, W - 56, 13.5)
    desc_svg = "".join(f'<text x="28" y="{124+k*20}" font-size="13.5" fill="#A3AEC2">{esc(l)}</text>' for k, l in enumerate(lines[:4]))
    tg_svg, ty = tags(28, 210, tg, W - 24)
    body = (f'<circle cx="{W-40}" cy="30" r="150" fill="{col}" opacity=".07"/>'
            f'<rect width="{W}" height="4" fill="{col}"/>'
            f'<g class="up" style="animation-delay:.1s">'
            f'<rect x="28" y="28" width="52" height="52" rx="14" fill="#1A2342" stroke="#2D3B63"/>'
            f'<text x="54" y="63" font-size="26" text-anchor="middle">{ico}</text>'
            f'<text x="96" y="52" font-size="23" font-weight="800" fill="#F8FAFC">{esc(name)}</text>'
            f'<text x="96" y="74" font-size="14" fill="{col}" font-weight="600">{esc(sub)}</text>'
            f'<text x="{W-28}" y="44" class="m" font-size="10.5" text-anchor="end" fill="#64748B" letter-spacing="1">{esc(kind)}</text></g>'
            f'<g class="up" style="animation-delay:.3s">{desc_svg}</g>'
            f'<g class="up" style="animation-delay:.5s">{tg_svg}</g>'
            f'<g class="up" style="animation-delay:.7s"><line x1="28" y1="{H-46}" x2="{W-28}" y2="{H-46}" stroke="#1E293B"/>'
            f'<circle cx="34" cy="{H-24}" r="4" fill="{col}"/>'
            f'<text x="46" y="{H-19}" class="m" font-size="12.5" fill="#CBD5E1">{esc(foot)}</text>'
            f'<text x="{W-28}" y="{H-19}" font-size="12.5" text-anchor="end" fill="#94A3B8">View →</text></g>')
    open(f"assets/cards/project-{slug}.svg", "w").write(svg(W, H, body, f"{name} — {sub}"))

# ───────────────────────── 4. "Currently" terminal ─────────────────────────
TERM = [
    ("$", "cat ~/now.yaml", "#E2E8F0"),
    ("", "building:", "#F472B6"),
    ("", "  - SIBIRI v1 → agentic content pipeline (LangGraph + RAG)", "#CBD5E1"),
    ("", "  - EngiMate v2 → voice notes & spoken-English practice", "#CBD5E1"),
    ("", "leading:    remote engineering team @ Bengal IT Hub", "#CBD5E1"),
    ("", "exploring:  multi-agent evals · on-device LLMs · production RAG", "#CBD5E1"),
    ("", "open_to:    AI product collabs · freelance full-stack & mobile", "#CBD5E1"),
    ("$", "echo $MOTTO", "#E2E8F0"),
    ("", "Build it right. Ship it fast. Then make it better.", "#7DF9FF"),
]
W = 1000
H = 70 + len(TERM) * 27 + 40
rows = []
for i, (p, t, col) in enumerate(TERM):
    yy = 92 + i * 27
    d = 0.4 + i * 0.32
    key, rest = (t.split(":", 1) + [""])[:2] if (":" in t and not t.startswith("  ") and p == "") else (None, None)
    if key is not None and rest is not None and key.strip() in ("building", "leading", "exploring", "open_to"):
        content = f'<tspan fill="#A78BFA">{esc(key)}:</tspan><tspan fill="{col}">{esc(rest)}</tspan>'
    else:
        content = f'<tspan fill="{col}">{esc(t)}</tspan>'
    prompt = '<tspan fill="#34D399">debanjan@sibiri</tspan><tspan fill="#64748B">:</tspan><tspan fill="#22D3EE">~</tspan><tspan fill="#64748B"> $ </tspan>' if p else ""
    rows.append(f'<text xml:space="preserve" x="34" y="{yy}" class="m type" font-size="14.5" style="animation-delay:{d:.2f}s">{prompt}{content}</text>')
last = 92 + len(TERM) * 27
rows.append(f'<text xml:space="preserve" x="34" y="{last}" class="m type" font-size="14.5" style="animation-delay:{0.4+len(TERM)*0.32:.2f}s">'
            f'<tspan fill="#34D399">debanjan@sibiri</tspan><tspan fill="#64748B">:</tspan><tspan fill="#22D3EE">~</tspan><tspan fill="#64748B"> $ </tspan>'
            f'<tspan class="blink" fill="#7DF9FF">▍</tspan></text>')
chrome = ('<rect width="1000" height="44" fill="#0F172A"/><line x1="0" y1="44" x2="1000" y2="44" stroke="#1E293B"/>'
          '<circle cx="26" cy="22" r="6.5" fill="#FF5F57"/><circle cx="48" cy="22" r="6.5" fill="#FEBC2E"/><circle cx="70" cy="22" r="6.5" fill="#28C840"/>'
          '<text x="500" y="27" class="m" font-size="12.5" text-anchor="middle" fill="#64748B">debanjan@sibiri — zsh — now.yaml</text>')
open("assets/cards/now.svg", "w").write(svg(W, H, chrome + "".join(rows), "What I'm working on now"))
print("cards ok")
