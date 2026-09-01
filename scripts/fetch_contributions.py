#!/usr/bin/env python3
"""Fetch the public GitHub contribution calendar without a token."""
import json, re
from datetime import date, timedelta
from pathlib import Path
import requests
from bs4 import BeautifulSoup

USERNAME = "b25bb1004-wq"
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT = Path("data/contributions.json")

def parse():
    r = requests.get(URL, timeout=30, headers={"User-Agent": "b25bb1004-wq-profile-art/1.0"})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    days = []
    # GitHub has used both td.ContributionCalendar-day and generic data-date cells.
    for cell in soup.select("td.ContributionCalendar-day[data-date], [data-date][data-level]"):
        d = cell.get("data-date")
        if not d:
            continue
        # Current GitHub markup stores the human-readable count in a sibling
        # <tool-tip for="contribution-day-component-…"> element; older markup
        # exposed it directly as aria-label.
        tooltip = soup.find("tool-tip", attrs={"for": cell.get("id")}) if cell.get("id") else None
        text = cell.get("aria-label", "") or (tooltip.get_text(" ", strip=True) if tooltip else "")
        m = re.search(r"(\d[\d,]*)\s+contribution", text)
        count = int(m.group(1).replace(",", "")) if m else 0
        level = int(cell.get("data-level", "0"))
        days.append({"date": d, "count": count, "level": level})

    if len(days) < 300:
        # Fallback for markup changes: use data-date anywhere inside calendar.
        for cell in soup.select("[data-date]"):
            d = cell.get("data-date")
            if not d:
                continue
            level = int(cell.get("data-level", "0"))
            label = cell.get("aria-label", "")
            m = re.search(r"(\d[\d,]*)\s+contribution", label)
            count = int(m.group(1).replace(",", "")) if m else 0
            days.append({"date": d, "count": count, "level": level})

    if len(days) < 300:
        raise RuntimeError("Could not find a complete contribution calendar; inspect GitHub markup.")

    days = sorted({x["date"]: x for x in days}.values(), key=lambda x: x["date"])
    counts = [x["count"] for x in days]
    total = sum(counts)

    best_day = max(days, key=lambda x: x["count"])
    longest = current = 0
    prev = None
    for x in days:
        d = date.fromisoformat(x["date"])
        if x["count"] > 0 and prev is not None and d == prev + timedelta(days=1):
            current += 1
        elif x["count"] > 0:
            current = 1
        else:
            current = 0
        longest = max(longest, current)
        prev = d

    today = date.fromisoformat(days[-1]["date"])
    streak = 0
    by_date = {date.fromisoformat(x["date"]): x["count"] for x in days}
    d = today
    while d in by_date and by_date[d] > 0:
        streak += 1
        d -= timedelta(days=1)

    payload = {
        "username": USERNAME,
        "fetched_at": date.today().isoformat(),
        "total": total,
        "current_streak": streak,
        "longest_streak": longest,
        "best_day": best_day,
        "days": days,
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}: {len(days)} days, {total} contributions")

if __name__ == "__main__":
    parse()
