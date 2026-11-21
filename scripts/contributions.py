"""Draw the full-year GitHub contribution calendar as dark + light SVG cards.

Fetches the calendar for USER from the GitHub GraphQL API and writes
assets/contributions-dark.svg and assets/contributions-light.svg in the same
style as the other cards. Run by .github/workflows/contributions.yml every day.

Token: GITHUB_TOKEN env var, or the local `gh` login when run by hand:
    python scripts/contributions.py
"""
import json
import os
import subprocess
import sys
import urllib.request
from datetime import date

sys.path.insert(0, os.path.dirname(__file__))
from generate import MONO, OUT, PAD, THEMES, W, svg, t  # noqa: E402

USER = "legendajar"
QUERY = """query($login: String!) { user(login: $login) { contributionsCollection {
  contributionCalendar { totalContributions weeks { contributionDays {
    date contributionCount contributionLevel } } } } } }"""
LEVELS = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}
ALPHA = {1: "47", 2: "80", 3: "b8", 4: "ff"}  # accent opacity per level

CELL, GAP = 11, 3
STEP = CELL + GAP
LEFT = PAD + 30          # room for the weekday labels
TOP = 80                 # first row of cells


def token():
    if os.environ.get("GITHUB_TOKEN"):
        return os.environ["GITHUB_TOKEN"]
    return subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True).stdout.strip()


def fetch():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {token()}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        data = json.load(r)
    if "errors" in data:
        sys.exit(f"GitHub API error: {data['errors']}")
    return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def fill(c, level):
    return c["line"] if level == 0 else c["accent"] + ALPHA[level]


def card(c, cal):
    weeks = cal["weeks"]
    total = cal["totalContributions"]
    b = t(PAD, 40, "CONTRIBUTIONS · LAST 12 MONTHS", 11, c["accent"], 500, MONO, spacing=1.2)
    b += t(W - PAD, 40, f"{total:,} contribution{'s' if total != 1 else ''}", 12, c["subtle"], 400, MONO, "end")

    for row, label in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        b += t(PAD, TOP + row * STEP + CELL - 2, label, 10, c["subtle"], 400, MONO)

    last_month = None
    for col, week in enumerate(weeks):
        x = LEFT + col * STEP
        first = date.fromisoformat(week["contributionDays"][0]["date"])
        if first.month != last_month and first.day <= 7 and col < len(weeks) - 2:
            b += t(x, TOP - 10, first.strftime("%b"), 10, c["subtle"], 400, MONO)
        last_month = first.month
        for day in week["contributionDays"]:
            d = date.fromisoformat(day["date"])
            row = (d.weekday() + 1) % 7  # Sunday first, like GitHub
            n = day["contributionCount"]
            b += (f'<rect x="{x}" y="{TOP + row * STEP}" width="{CELL}" height="{CELL}" rx="2.5" '
                  f'fill="{fill(c, LEVELS[day["contributionLevel"]])}">'
                  f'<title>{n} contribution{"s" if n != 1 else ""} on {d:%b} {d.day}, {d.year}</title></rect>')

    y = TOP + 7 * STEP + 22
    lx = W - PAD - 5 * STEP - 34
    b += t(lx - 8, y + CELL - 1, "Less", 10, c["subtle"], 400, MONO, "end")
    for i in range(5):
        b += f'<rect x="{lx + i * STEP}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{fill(c, i)}"/>'
    b += t(lx + 5 * STEP + 4, y + CELL - 1, "More", 10, c["subtle"], 400, MONO)
    return svg(W, y + CELL + 26, c, b, f"{total} GitHub contributions in the last year")


def main():
    cal = fetch()
    for theme, colors in THEMES.items():
        (OUT / f"contributions-{theme}.svg").write_text(card(colors, cal), encoding="utf-8")
    print(f"{cal['totalContributions']} contributions; wrote contributions-dark/light.svg")


if __name__ == "__main__":
    main()
