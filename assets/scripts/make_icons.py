"""Consistent line icons (gradient stroke on a navy tile) used in place of emojis.

Run from the repo root:  python assets/scripts/make_icons.py
"""
import os

ICONS = {
    "ai": '<rect x="4" y="8" width="16" height="12" rx="3"/><path d="M12 4.5V8"/><circle cx="12" cy="3.5" r="1"/>'
          '<circle cx="9" cy="13.5" r="1.2"/><circle cx="15" cy="13.5" r="1.2"/><path d="M10 17h4M2 13v3M22 13v3"/>',
    "web": '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/>',
    "mobile": '<rect x="6.5" y="2.5" width="11" height="19" rx="2.5"/><path d="M10.5 18.5h3"/>',
    "ml": '<circle cx="5" cy="6" r="2"/><circle cx="5" cy="18" r="2"/><circle cx="12" cy="12" r="2.2"/>'
          '<circle cx="19" cy="6" r="2"/><circle cx="19" cy="18" r="2"/>'
          '<path d="M6.6 7.3l3.7 3.2M6.6 16.7l3.7-3.2M13.7 10.5l3.7-3.2M13.7 13.5l3.7 3.2"/>',
    "team": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c0-3.6 2.9-6 6.5-6s6.5 2.4 6.5 6"/>'
            '<circle cx="17" cy="9" r="2.6"/><path d="M17 14c2.6 0 4.5 1.8 4.5 4.5"/>',
    "shield": '<path d="M12 2.8l7.5 3V11.5c0 4.5-3.2 8.1-7.5 9.7-4.3-1.6-7.5-5.2-7.5-9.7V5.8z"/><path d="M8.8 12l2.2 2.2 4.2-4.4"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "briefcase": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5.5A1.5 1.5 0 0 1 10.5 4h3A1.5 1.5 0 0 1 15 5.5V7M3 12.5h18"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.3"/>',
    "chat": '<path d="M4 5h16v11H10l-5 4v-4H4z"/><path d="M8 9.5h8M8 12.5h5"/>',
    "edu": '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c0 1.5 2.7 3 6 3s6-1.5 6-3v-5M22 9v5"/>',
    "cpu": '<rect x="6" y="6" width="12" height="12" rx="2"/><rect x="9.5" y="9.5" width="5" height="5" rx="1"/>'
           '<path d="M9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3"/>',
    "lock": '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/><circle cx="12" cy="16" r="1.3"/>',
    "map": '<path d="M3 6l6-2 6 2 6-2v14l-6 2-6-2-6 2z"/><path d="M9 4v14M15 6v14"/>',
}

os.makedirs("assets/icons", exist_ok=True)
for name, body in ICONS.items():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 48 48" role="img" aria-label="{name}">
<defs>
<linearGradient id="g" gradientUnits="userSpaceOnUse" x1="2" y1="2" x2="22" y2="22"><stop offset="0" stop-color="#22D3EE"/><stop offset=".55" stop-color="#A78BFA"/><stop offset="1" stop-color="#F472B6"/></linearGradient>
<linearGradient id="t" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#172036"/><stop offset="1" stop-color="#0E1529"/></linearGradient>
</defs>
<rect x=".5" y=".5" width="47" height="47" rx="13" fill="url(#t)" stroke="#2B3A5E"/>
<g transform="translate(11 11) scale(1.0833)" fill="none" stroke="url(#g)" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{body}</g>
</svg>'''
    open(f"assets/icons/{name}.svg", "w", encoding="utf-8").write(svg)
print(len(ICONS), "icons")
