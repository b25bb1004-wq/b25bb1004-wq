#!/usr/bin/env python3
"""Fetch the public GitHub contribution calendar without a token."""
import json, re
from datetime import date, timedelta
from pathlib import Path
import requests
from bs4 import BeautifulSoup

USERNAME = "hades-3008"
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT = Path("data/contributions.json")

def parse():
    r = requests.get(URL, timeout=30, headers={"User-Agent": "hades-3008-profile/1.0"})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    days = []
    for cell in soup.select("td.ContributionCalendar-day"):
        d = cell.get("data-date")
        if not d:
            continue
        text = cell.get("aria-label", "")
        m = re.search(r"(\d[\d,]*)\s+contribution", text)
        count = int(m.group(1).replace(",", "")) if m else 0
        level = int(cell.get("data-level", "0"))
        days.append({"date": d, "count": count, "level": level})

    if not days:
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

    if not days:
        raise RuntimeError("Could not find contribution cells; inspect GitHub markup.")

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

    today = date.today()
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
