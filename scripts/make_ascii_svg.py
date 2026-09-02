#!/usr/bin/env python3
from pathlib import Path
from PIL import Image

RAMP = " .`:-=+*cs#%@"

def main():
    src = Path("assets/source-prepped.png")
    out = Path("assets/arnav-ascii.svg")
    width, height = 100, 53
    img = Image.open(src).convert("L")
    # Portrait-oriented crop: retain face and shoulders while removing blank wall.
    crop_w = int(img.width * 0.82)
    crop_h = int(img.height * 0.70)
    left = (img.width - crop_w) // 2
    top = int(img.height * 0.16)
    img = img.crop((left, top, left + crop_w, min(img.height, top + crop_h)))
    img = img.resize((width, height), Image.Resampling.LANCZOS)

    rows = []
    for y in range(height):
        row = []
        for x in range(width):
            value = img.getpixel((x, y))
            idx = max(0, min(len(RAMP)-1, int((255-value)/256*len(RAMP))))
            row.append(RAMP[idx])
        rows.append("".join(row).rstrip())

    while rows and not rows[0].strip(): rows.pop(0)
    while rows and not rows[-1].strip(): rows.pop()
    left = min((len(r)-len(r.lstrip()) for r in rows if r.strip()), default=0)
    rows = [r[left:].rstrip() for r in rows]

    line_h, top, svg_w = 10, 14, 640
    svg_h = top + len(rows)*line_h + 20
    # CSS @keyframes, not SMIL <animate>: GitHub's README image pipeline
    # strips <animate> elements outright, which left every clip-rect frozen
    # at its `from` state (width 0) — a permanently blank portrait rather
    # than a typing one. transform-box:fill-box makes scaleX(0->1) expand
    # from each rect's own left edge regardless of its y position, so one
    # shared class + a per-row animation-delay is enough for the stagger.
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" role="img" aria-label="Animated ASCII portrait">',
        '<rect width="100%" height="100%" fill="#0d1117"/>',
        '<style>'
        'text{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;font-size:12px;fill:#c9d1d9}'
        '.row{transform-box:fill-box;transform-origin:0% 50%;animation:wipeIn .42s ease-out both}'
        '@keyframes wipeIn{from{transform:scaleX(0)}to{transform:scaleX(1)}}'
        '</style>'
    ]
    for i, row in enumerate(rows):
        safe = row.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
        y = top + (i+1)*line_h
        parts.append(
            f'<clipPath id="r{i}"><rect class="row" style="animation-delay:{i*0.040:.3f}s" '
            f'x="0" y="{y-line_h+1}" width="{svg_w}" height="{line_h+2}"/></clipPath>'
        )
        parts.append(f'<text x="10" y="{y}" clip-path="url(#r{i})">{safe}</text>')
    parts.append("</svg>")
    out.write_text("\n".join(parts), encoding="utf-8")
    print(f"Wrote {out}")

if __name__ == "__main__":
    main()
