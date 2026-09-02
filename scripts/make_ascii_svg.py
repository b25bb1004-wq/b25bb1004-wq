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
    reveal_h = svg_h - top + 12  # covers from just above the first row to past the last
    dur = max(1.4, len(rows) * 0.045)  # slow enough to actually watch, not instant

    # A single reveal, not per-row wipes: one clip-rect grows downward from
    # the top of the block (transform-box:fill-box + scaleY, same trick as
    # the heatmap/info-card fix — CSS @keyframes, never SMIL <animate>, which
    # GitHub's README image pipeline strips outright), so nothing below the
    # current line exists yet rather than the whole portrait being present
    # from frame one. A bright bar rides the leading edge and fades out once
    # the reveal completes, standing in for the "cursor" the clip alone can't
    # show since a mask has no visible edge of its own.
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" role="img" aria-label="Animated ASCII portrait">',
        '<rect width="100%" height="100%" fill="#0d1117"/>',
        '<style>'
        'text{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;font-size:12px;fill:#c9d1d9}'
        f'.reveal{{transform-box:fill-box;transform-origin:0% 0%;animation:growDown {dur:.2f}s linear forwards}}'
        '@keyframes growDown{from{transform:scaleY(0)}to{transform:scaleY(1)}}'
        f'.scanline{{animation:scanDown {dur:.2f}s linear forwards}}'
        f'@keyframes scanDown{{0%{{transform:translateY(0);opacity:1}}96%{{opacity:1}}100%{{transform:translateY({reveal_h}px);opacity:0}}}}'
        '</style>',
        f'<clipPath id="reveal"><rect class="reveal" x="0" y="{top-12}" width="{svg_w}" height="{reveal_h}"/></clipPath>',
        '<g clip-path="url(#reveal)">'
    ]
    for i, row in enumerate(rows):
        safe = row.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
        y = top + (i+1)*line_h
        parts.append(f'<text x="10" y="{y}">{safe}</text>')
    parts.append('</g>')
    parts.append(
        f'<rect class="scanline" x="0" y="{top-12}" width="{svg_w}" height="2" fill="#58a6ff"/>'
    )
    parts.append("</svg>")
    out.write_text("\n".join(parts), encoding="utf-8")
    print(f"Wrote {out}")

if __name__ == "__main__":
    main()
