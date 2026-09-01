from pathlib import Path
rows = [
    ("USER", "Arnav"),
    ("EDUCATION", "IIT Jodhpur"),
    ("FOCUS", "CS / AI / ML"),
    ("LANGUAGES", "C++ / Python"),
    ("STACK", "PyTorch / TensorFlow / HF"),
    ("TOOLS", "Git / Linux / SQL"),
    ("BUILDING", "ML systems + developer tools"),
]
svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 490 350" role="img" aria-label="Animated terminal profile card for Arnav">',
'<rect x="1" y="1" width="488" height="348" rx="10" fill="#0d1117" stroke="#30363d"/>',
'<rect x="1" y="1" width="488" height="34" rx="10" fill="#161b22"/>',
'<circle cx="20" cy="18" r="5" fill="#ff5f56"/><circle cx="38" cy="18" r="5" fill="#ffbd2e"/><circle cx="56" cy="18" r="5" fill="#27c93f"/>',
'<text x="78" y="23" fill="#8b949e" font-family="ui-monospace,monospace" font-size="13">arnav@github — neofetch</text>',
'<g font-family="ui-monospace,monospace" font-size="15">',
'<text x="28" y="72" fill="#58a6ff">arnav</text><text x="94" y="72" fill="#8b949e">@</text><text x="108" y="72" fill="#79c0ff">github</text>',
'<text x="28" y="101" fill="#8b949e">──────────────────────────────────────</text>']
y = 130
for i, (k,v) in enumerate(rows):
    delay = i * 0.13
    svg.append(
        f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.38s" begin="{delay:.2f}s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" from="-8 0" to="0 0" dur="0.38s" begin="{delay:.2f}s" fill="freeze"/>'
        f'<text x="28" y="{y}" fill="#7ee787">{k}</text><text x="154" y="{y}" fill="#c9d1d9">{v}</text></g>'
    )
    y += 30
svg += ['</g>', '</svg>']
Path("assets/info-card.svg").write_text("\n".join(svg), encoding="utf-8")
print("Wrote assets/info-card.svg")
