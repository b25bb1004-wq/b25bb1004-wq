#!/usr/bin/env python3
import json
from pathlib import Path

DATA = Path("data/contributions.json")
OUT = Path("assets/contrib-heatmap.svg")
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    days = data["days"]
    by_date = {x["date"]: x for x in days}
    if not days:
        raise RuntimeError("No contribution data.")

    if data.get("username") != "b25bb1004-wq":
        raise RuntimeError("Contribution data must belong to b25bb1004-wq.")
    # GitHub's contribution calendar is laid out Sunday -> Saturday.
    from datetime import date, timedelta
    first = date.fromisoformat(days[0]["date"])
    start = first - timedelta(days=(first.weekday()+1)%7)
    cells = []
    for i in range(53*7):
        d = start + timedelta(days=i)
        x = by_date.get(d.isoformat(), {"count":0, "level":0})
        cells.append((d, x["count"], x["level"]))

    cell = 11
    gap = 3
    left = 30
    top = 54
    width = 860
    height = 186
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-label="Animated GitHub contribution calendar for b25bb1004-wq">',
        f'<rect width="{width}" height="{height}" rx="10" fill="#0d1117" stroke="#30363d"/>',
        # CSS @keyframes, not SMIL <animate>: GitHub's README image pipeline
        # strips <animate> elements outright, which left every cell frozen at
        # its `from` state (opacity 0) — an empty grid instead of one that
        # reveals itself. A diagonal slide-down: fades in while easing up
        # from a few px below, staggered by the same per-cell delay as before.
        '<style>'
        '.label{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace}'
        '.cell{opacity:0;animation:cellIn .32s ease-out both}'
        '@keyframes cellIn{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:translateY(0)}}'
        '</style>',
        f'<text class="label" x="30" y="27" fill="#c9d1d9" font-size="14">{data["total"]:,} contributions in the last year</text>',
        f'<text class="label" x="30" y="44" fill="#8b949e" font-size="10">{data["longest_streak"]}-day longest streak · public activity</text>',
        '<text class="label" x="4" y="82" fill="#8b949e" font-size="9">Mon</text>',
        '<text class="label" x="4" y="110" fill="#8b949e" font-size="9">Wed</text>',
        '<text class="label" x="4" y="138" fill="#8b949e" font-size="9">Fri</text>'
    ]
    for i, (d, count, level) in enumerate(cells):
        col = i // 7
        row = i % 7
        x = left + col*(cell+gap)
        y = top + row*(cell+gap)
        delay = (col*0.022 + row*0.012)
        title = f"{count} contribution{'s' if count != 1 else ''} on {d.isoformat()}"
        parts.append(
            f'<rect class="cell" style="animation-delay:{delay:.3f}s" x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{PALETTE[min(level,4)]}">'
            f'<title>{title}</title></rect>'
        )
    parts += [
        '<text class="label" x="665" y="171" fill="#8b949e" font-size="10">Less</text>'
    ]
    for i, color in enumerate(PALETTE):
        parts.append(f'<rect x="{700+i*16}" y="161" width="11" height="11" rx="2" fill="{color}"/>')
    parts.append('<text class="label" x="784" y="171" fill="#8b949e" font-size="10">More</text>')
    parts.append('</svg>')
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
