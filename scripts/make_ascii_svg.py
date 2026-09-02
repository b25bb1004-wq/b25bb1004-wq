#!/usr/bin/env python3
from pathlib import Path
from PIL import Image

RAMP = " .`:-=+*cs#%@"

def main():
    src = Path("assets/source-prepped.png")
    out = Path("assets/arnav-ascii.svg")
    width = 100
    img = Image.open(src).convert("L")
    # Crop to the subject's own bounding box, not a fixed percentage of the
    # frame: prep_photo.py composites onto pure white, so anything below a
    # near-white threshold is background regardless of how much headroom or
    # framing the source photo happened to have. A hardcoded crop tuned for
    # one photo's composition silently mis-crops the next one — this is what
    # actually broke when the source photo changed.
    import numpy as np
    arr = np.array(img)
    subject_mask = arr < 245
    crop_aspect = img.width / img.height  # w/h fallback if the mask is empty
    if subject_mask.any():
        ys, xs = np.where(subject_mask)
        pad_x = int(img.width * 0.03)
        pad_y = int(img.height * 0.02)
        left = max(0, xs.min() - pad_x)
        right = min(img.width, xs.max() + pad_x)
        top_c = max(0, ys.min() - pad_y)
        bottom = min(img.height, ys.max() + pad_y)
        img = img.crop((left, top_c, right, bottom))
        # The full bounding box runs down to the shoulders, which on this
        # photo spread to the full frame width in a dark hoodie — that band
        # is wide and low-detail, so at ASCII resolution it renders as a
        # dense, cluttered slab rather than a readable collar/shoulder line.
        # Keeping only the top 60% (face + a little hair/neck) and then
        # re-tightening the x-bounds to THAT slice's own content (its own
        # subject is narrower than the full-width shoulders) is what
        # actually reads as a face instead of a blob.
        FACE_FRACTION = 0.54
        img = img.crop((0, 0, img.width, round(img.height * FACE_FRACTION)))
        sub_mask = np.array(img) < 245
        if sub_mask.any():
            ys2, xs2 = np.where(sub_mask)
            l2 = max(0, xs2.min() - pad_x)
            r2 = min(img.width, xs2.max() + pad_x)
            img = img.crop((l2, 0, r2, img.height))
        crop_aspect = img.width / img.height
    # A monospace glyph cell is noticeably taller than it is wide (~0.6 at
    # this font), so sampling into a fixed height regardless of the crop's
    # own aspect ratio silently stretches whatever doesn't match the ratio
    # that height was tuned for — a near-square crop like this one came out
    # visibly squashed sideways before this fix. Solve for the row count that
    # actually preserves the crop's proportions through the glyph grid.
    CELL_ASPECT = 0.6  # glyph advance width / line height, monospace
    height = max(1, round(width * CELL_ASPECT / crop_aspect))
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
