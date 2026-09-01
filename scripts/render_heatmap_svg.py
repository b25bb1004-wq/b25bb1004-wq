#!/usr/bin/env python3
import json, math
from pathlib import Path

DATA = Path("data/contributions.json")
OUT = Path("assets/contrib-heatmap.svg")
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    days = data["days"]
    by_date = {x["date"]: x for x in days}
    if not days:
        raise RuntimeError("No contribution data.")

    # GitHub's contribution calendar is laid out Sunday -> Saturday.
    from datetime import date, timedelta
    first = date.fromisoformat(days[0]["date"])
    start = first - timedelta(days=(first.weekday()+1)%7)
    cells = []
    for i in range(53*7):
        d = start + timedelta(days=i)
        x = by_date.get(d.isoformat(), {"count":0, "level":0})
        cells.append((d, x["count"], x["level"]))

    cell = 12
    gap = 3
    left = 28
    top = 50
    width = 920
    height = 155
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-label="GitHub contribution heatmap for hades-3008">',
        f'<rect width="{width}" height="{height}" rx="10" fill="#0d1117" stroke="#30363d"/>',
        '<style>.day{opacity:0;animation:show .35s ease forwards}@keyframes show{to{opacity:1}}</style>',
        f'<text x="28" y="27" fill="#c9d1d9" font-family="ui-monospace,monospace" font-size="15">{data["total"]:,} contributions in the last year</text>'
    ]
    for i, (d, count, level) in enumerate(cells):
        col = i // 7
        row = i % 7
        x = left + col*(cell+gap)
        y = top + row*(cell+gap)
        delay = (col*0.025 + row*0.01)
        title = f"{count} contribution{'s' if count != 1 else ''} on {d.isoformat()}"
        parts.append(
            f'<rect class="day" x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{PALETTE[min(level,5)]}" '
            f'style="animation-delay:{delay:.3f}s"><title>{title}</title></rect>'
        )
    parts += [
        '<text x="28" y="147" fill="#8b949e" font-family="ui-monospace,monospace" font-size="11">Less</text>'
    ]
    for i, color in enumerate(PALETTE):
        parts.append(f'<rect x="{70+i*16}" y="138" width="11" height="11" rx="2" fill="{color}"/>')
    parts.append('<text x="168" y="147" fill="#8b949e" font-family="ui-monospace,monospace" font-size="11">More</text>')
    parts.append('</svg>')
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
