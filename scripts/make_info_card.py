from pathlib import Path
import os

STATIC = os.getenv("STATIC") == "1"
anim = "" if STATIC else """
<style>
.item{opacity:0;animation:fade .5s ease forwards}
@keyframes fade{to{opacity:1}}
</style>
"""
rows = [
    ("Role", "CS / AI / ML Builder"),
    ("Study", "IIT Jodhpur"),
    ("Degree", "Bioengineering"),
    ("Focus", "software · AI · ML · systems"),
    ("Stack", "C++ · Python · SQL"),
    ("ML", "PyTorch · TensorFlow · scikit-learn"),
    ("Tools", "Hugging Face · Node.js · Linux · Git"),
]
svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 420" role="img" aria-label="Arnav profile card">',
'<rect x="1" y="1" width="538" height="418" rx="12" fill="#0d1117" stroke="#30363d"/>',
'<rect x="1" y="1" width="538" height="34" rx="12" fill="#161b22"/>',
'<circle cx="20" cy="18" r="5" fill="#ff5f56"/><circle cx="38" cy="18" r="5" fill="#ffbd2e"/><circle cx="56" cy="18" r="5" fill="#27c93f"/>',
'<text x="78" y="23" fill="#8b949e" font-family="ui-monospace,monospace" font-size="13">arnav@github — neofetch</text>',
'<g font-family="ui-monospace,monospace" font-size="15">',
'<text x="28" y="72" fill="#58a6ff">arnav</text><text x="94" y="72" fill="#8b949e">@</text><text x="108" y="72" fill="#79c0ff">github</text>',
'<text x="28" y="101" fill="#8b949e">────────────────────────────────────────</text>']
y = 137
for i, (k,v) in enumerate(rows):
    cls = "" if STATIC else ' class="item"'
    extra = "" if STATIC else f' style="animation-delay:{i*0.12:.2f}s"'
    svg.append(f'<text x="28" y="{y}" fill="#c9d1d9"{cls}{extra}>{k}</text><text x="154" y="{y}" fill="#8b949e"{cls}{extra}>{v}</text>')
    y += 36
svg += ['</g>', anim, '</svg>']
Path("assets/info-card.svg").write_text("\n".join(svg), encoding="utf-8")
print("Wrote assets/info-card.svg")
