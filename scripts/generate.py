"""Generate the System Signal profile README cards (dark + light SVGs).

Tokens follow the portfolio redesign (Handoff H1 token map): graphite surfaces,
one signal-red accent, mono for every piece of metadata, blueprint grid and
corner-tick frames as the only decoration.

Edit CONTENT below and run:  python scripts/generate.py
Output goes to assets/<name>-dark.svg and assets/<name>-light.svg.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"

THEMES = {
    "dark": {
        "bg": "#09090b", "surface": "#111115", "surface2": "#18181d",
        "fg": "#f2f2f4", "muted": "#a6a6b0", "subtle": "#80808b",
        "accent": "#ff2d55", "accent_soft": "#ff2d551f", "ok": "#34d399",
        "line": "#ffffff14", "line_strong": "#ffffff2e", "grid": "#ffffff12",
    },
    "light": {
        "bg": "#f6f5f2", "surface": "#ffffff", "surface2": "#f1efea",
        "fg": "#121216", "muted": "#4b4b55", "subtle": "#6a6a74",
        "accent": "#d1003f", "accent_soft": "#d1003f14", "ok": "#047857",
        "line": "#12121614", "line_strong": "#1212162e", "grid": "#12121612",
    },
}
SANS = "Outfit, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'Fira Code', 'Cascadia Code', Consolas, monospace"
W = 840
PAD = 32

# ---- content ---------------------------------------------------------------

HERO = {
    "role": "Software Engineer & Full Stack Developer",
    "headline": "I engineer high-performance web applications.",
    "tagline": "Specialized in building scalable microfrontends, high-throughput APIs, "
               "and optimized cloud architectures that drive business impact.",
    "facts": [("Based in", "Pune, India"), ("Currently", "Xogene"), ("Core stack", "React · Next.js · TypeScript")],
    "status": "Open to opportunities",
}

EXPERTISE = [
    ("Frontend", ["React", "Next.js", "TypeScript", "Microfrontends", "Module Federation", "Framer Motion", "Sass"]),
    ("Backend", ["Node.js", "Express", "Django", "Celery"]),
    ("Data", ["PostgreSQL", "MongoDB", "Redis"]),
    ("Cloud & delivery", ["AWS", "Docker"]),
    ("AI & desktop", ["Electron", "Local LLMs", "LM Studio", "RAG", "MCP"]),
]

# (dates · place, role, org, note, current)
JOURNEY = {
    "Work": [
        ("Nov 2024 – Present · Pune", "Jr. Software Developer", "Xogene",
         "React microfrontends, Django APIs, performance work, internal tooling.", True),
        ("May 2022 – Sep 2023 · Remote", "Associate Engineer", "Nagarro",
         "First industry role, alongside the MCA.", False),
    ],
    "Education": [
        ("Aug 2022 – May 2024 · Noida", "Master of Computer Applications", "Amity University",
         "Advanced software engineering, distributed systems, modern web architecture.", False),
        ("Aug 2019 – May 2022 · Mathura", "Bachelor of Computer Applications", "GLA University",
         "Object-oriented programming, database management, core algorithms.", False),
    ],
}

FEATURED = ("Orbie", "Living desktop AI assistant for Windows 11 — local-first, voice, memory.",
            "Electron · React · local LLMs", "github.com/legendajar/Orbie")

PROJECTS = [
    ("01", "ApniJob Job Portal", "Full-stack job portal: auth, real-time dashboards, applicant tracking.", "React · Node.js · MongoDB · Express"),
    ("02", "Logistics Delivery System", "Food-delivery management with real-time order tracking.", "React · Node.js · MongoDB · Express"),
    ("03", "CV Gesture Recognition", "Real-time hand-gesture recognition for touch-free control.", "Python · OpenCV · MediaPipe"),
    ("04", "GreatKart E-Commerce", "Django e-commerce platform tuned for fast page loads and search.", "Django · Python"),
]

LAB = [
    ("Local RAG pipeline", "Ingest, query and answer over your own files, fully offline."),
    ("Portfolio MCP server", "My projects, skills and résumé, exposed to any MCP client."),
    ("Job-search automation", "Scores and ranks openings against a profile."),
]

WRITING = [
    ("Jul 30, 2026", "An Agent Broke Into Production to Cheat a Benchmark. Read It as an Architecture Bug."),
    ("Jun 18, 2026", "Agentic AI: From Chatbots to Digital Coworkers"),
]

CONTACT = [
    ("Email", "harshsolanki9898@gmail.com"),
    ("Location", "Pune, Maharashtra, India"),
    ("Web", "theharshsolanki.in"),
]

# ---- helpers ---------------------------------------------------------------


def wrap(text, width):
    lines, cur = [], ""
    for word in text.split():
        if cur and len(cur) + 1 + len(word) > width:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    return lines + [cur] if cur else lines


def t(x, y, s, size, fill, weight=400, family=SANS, anchor="start", spacing=0):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" letter-spacing="{spacing}">{escape(s)}</text>')


def svg(width, height, c, body, title, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
            f'role="img"><title>{escape(title)}</title><defs>{defs}</defs>'
            f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="16" fill="{c["bg"]}" stroke="{c["line"]}"/>'
            f'{body}</svg>')


def grid(x, y, w, h, c, cell=24):
    """Blueprint grid masked to an ellipse — returns (defs, body)."""
    defs = (f'<pattern id="g" width="{cell}" height="{cell}" patternUnits="userSpaceOnUse">'
            f'<path d="M{cell} 0H0V{cell}" fill="none" stroke="{c["grid"]}"/></pattern>'
            f'<radialGradient id="gf"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
            f'<mask id="gm"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#gf)"/></mask>')
    return defs, f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#g)" mask="url(#gm)"/>'


def ticks(x, y, w, h, c, n=12):
    """Corner-tick viewport frame."""
    d = (f"M{x} {y + n}V{y}H{x + n} M{x + w - n} {y}H{x + w}V{y + n} "
         f"M{x + w} {y + h - n}V{y + h}H{x + w - n} M{x + n} {y + h}H{x}V{y + h - n}")
    return f'<path d="{d}" fill="none" stroke="{c["subtle"]}" stroke-width="1.5"/>'


def mark(x, y, size, c):
    """The “H” mark: text-coloured tile, bg glyph, accent full stop (dropped below 32px)."""
    b = f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{size * 0.22:.1f}" fill="{c["fg"]}"/>'
    b += t(x + size * 0.46, y + size * 0.71, "H", round(size * 0.6), c["bg"], 700, MONO, "middle")
    if size >= 32:
        b += f'<circle cx="{x + size * 0.79:.1f}" cy="{y + size * 0.74:.1f}" r="{size * 0.055:.1f}" fill="{c["accent"]}"/>'
    return b


def heading(c, num, label, title, y=36):
    """Mono section index (“01 — Expertise”) over the section title."""
    return t(PAD, y, f"{num} — {label}", 12, c["accent"], 500, MONO, spacing=0.5) + t(PAD, y + 34, title, 26, c["fg"], 700, spacing=-0.9)


def chip(x, y, label, c):
    w = int(len(label) * 7.2) + 22
    return w, (f'<rect x="{x}" y="{y}" width="{w}" height="28" rx="14" fill="{c["surface"]}" stroke="{c["line_strong"]}"/>'
               + t(x + w / 2, y + 18.5, label, 12, c["fg"], 400, MONO, "middle"))

# ---- cards -----------------------------------------------------------------


def hero(c):
    vx, vy, vs = 592, 32, 216
    defs, g = grid(vx - 40, vy - 20, vs + 80, vs + 40, c)
    b = g + ticks(vx, vy, vs, vs, c)
    b += mark(vx + vs / 2 - 48, vy + vs / 2 - 56, 96, c)
    b += t(vx + 14, vy + vs - 14, "PUNE · IN", 11, c["subtle"], 400, MONO, spacing=1)
    b += (f'<rect x="{vx}" y="{vy + vs + 16}" width="{vs}" height="32" rx="16" fill="{c["surface"]}" stroke="{c["line_strong"]}"/>'
          f'<circle cx="{vx + 20}" cy="{vy + vs + 32}" r="4" fill="{c["ok"]}"/>'
          + t(vx + 34, vy + vs + 36.5, HERO["status"], 12, c["fg"], 400, MONO))

    b += mark(PAD, 28, 28, c) + t(PAD + 38, 49, "Harsh", 20, c["fg"], 700) + t(PAD + 92, 49, ".", 20, c["accent"], 700)
    b += t(PAD, 104, HERO["role"].upper(), 12, c["accent"], 500, MONO, spacing=1.2)
    b += (f'<text x="{PAD}" y="152" font-family="{SANS}" font-size="44" font-weight="700" fill="{c["fg"]}" letter-spacing="-1.8">'
          f'Hi, I\'m Harsh Solanki<tspan fill="{c["accent"]}">.</tspan></text>')
    b += t(PAD, 188, HERO["headline"], 19, c["fg"], 500)
    for i, line in enumerate(wrap(HERO["tagline"], 66)):
        b += t(PAD, 218 + i * 22, line, 15, c["muted"])
    b += f'<line x1="{PAD}" y1="282" x2="552" y2="282" stroke="{c["line"]}"/>'
    for i, (label, value) in enumerate(HERO["facts"]):
        x = PAD + i * 150
        b += t(x, 306, label.upper(), 11, c["subtle"], 400, MONO, spacing=1) + t(x, 328, value, 14, c["fg"], 500)
    return svg(W, 358, c, b, "Harsh Solanki — Software Engineer & Full Stack Developer", defs)


def expertise(c):
    b, y = heading(c, "01", "Expertise", "Core expertise"), 100
    b += t(PAD, y - 4, "The tools I reach for, grouped by where they sit in the stack.", 15, c["muted"])
    y += 20
    for group, items in EXPERTISE:
        b += t(PAD, y + 19, group, 15, c["fg"], 600) + t(184, y + 19, f"{len(items):02d}", 12, c["subtle"], 400, MONO, "end")
        x = 204
        for item in items:
            w = int(len(item) * 7.2) + 22
            if x + w > W - PAD:
                x, y = 204, y + 36
            b += chip(x, y, item, c)[1]
            x += w + 8
        y += 44
    return svg(W, y + 12, c, b, "Core expertise")


def journey_column(c, x0, y, name, items):
    b = t(x0, y, name.upper(), 11, c["subtle"], 500, MONO, spacing=1.2)
    y += 28
    top = y
    for dates, role, org, note, current in items:
        b += f'<circle cx="{x0 + 6}" cy="{y - 4}" r="5" fill="{c["accent"] if current else c["bg"]}" stroke="{c["accent"] if current else c["subtle"]}" stroke-width="1.5"/>'
        b += t(x0 + 26, y, dates, 12, c["subtle"], 400, MONO)
        if current:
            b += (f'<rect x="{x0 + 324}" y="{y - 14}" width="58" height="20" rx="10" fill="{c["accent_soft"]}"/>'
                  + t(x0 + 353, y, "CURRENT", 10, c["accent"], 500, MONO, "middle", 0.8))
        b += t(x0 + 26, y + 26, role, 17, c["fg"], 600) + t(x0 + 26, y + 47, org, 13, c["accent"], 400, MONO)
        lines = wrap(note, 46)
        for i, line in enumerate(lines):
            b += t(x0 + 26, y + 70 + i * 20, line, 14, c["muted"])
        last = y
        y += 70 + 20 * len(lines) + 20
    b = f'<line x1="{x0 + 6}" y1="{top}" x2="{x0 + 6}" y2="{last - 4}" stroke="{c["line_strong"]}" stroke-width="1.5"/>' + b
    return b, y


def journey(c):
    b = heading(c, "02", "Journey", "Experience & education")
    heights = []
    for i, (name, items) in enumerate(JOURNEY.items()):
        col, y = journey_column(c, PAD + i * 404, 112, name, items)
        b += col
        heights.append(y)
    return svg(W, max(heights), c, b, "Experience & education")


def featured(c):
    name, desc, stack, repo = FEATURED
    b = heading(c, "03", "Work", "Selected projects")
    x, y, w, h = PAD, 96, W - 2 * PAD, 136
    defs, g = grid(x, y, w, h, c)
    b += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{c["surface"]}" stroke="{c["accent"]}"/>' + g
    b += t(x + 24, y + 32, "FEATURED BUILD", 11, c["accent"], 500, MONO, spacing=1.2)
    b += t(x + w - 24, y + 32, stack, 12, c["subtle"], 400, MONO, "end")
    b += t(x + 24, y + 72, name, 30, c["fg"], 700, spacing=-0.8) + t(x + 24, y + 100, desc, 15, c["muted"])
    b += t(x + w - 24, y + h - 20, f"{repo} ↗", 12, c["muted"], 400, MONO, "end")
    return svg(W, y + h + 24, c, b, f"Featured build: {name}", defs)


def project(c, num, name, desc, stack):
    w = 410
    b = t(24, 36, num, 12, c["accent"], 500, MONO) + t(50, 36, stack, 12, c["subtle"], 400, MONO)
    b += t(24, 70, name, 20, c["fg"], 600, spacing=-0.3)
    for i, line in enumerate(wrap(desc, 46)):
        b += t(24, 98 + i * 20, line, 14, c["muted"])
    b += f'<line x1="24" y1="140" x2="{w - 24}" y2="140" stroke="{c["line"]}"/>'
    b += t(24, 162, "theharshsolanki.in/#projects", 12, c["subtle"], 400, MONO) + t(w - 24, 162, "↗", 13, c["accent"], 500, MONO, "end")
    return svg(w, 184, c, b, f"Project {num}: {name}")


def lab(c):
    b = t(PAD, 40, "IN THE LAB", 11, c["accent"], 500, MONO, spacing=1.2) + t(W - PAD, 40, "in progress", 12, c["subtle"], 400, MONO, "end")
    y = 76
    for name, desc in LAB:
        b += f'<circle cx="{PAD + 6}" cy="{y - 5}" r="4" fill="none" stroke="{c["accent"]}" stroke-width="1.5"/>'
        b += t(PAD + 22, y, name, 15, c["fg"], 600) + t(260, y, desc, 14, c["muted"])
        y += 32
    return svg(W, y, c, b, "In the lab")


def post(c, date, title):
    b = t(24, 36, date, 12, c["accent"], 500, MONO)
    for i, line in enumerate(wrap(title, 40)):
        b += t(24, 70 + i * 24, line, 17, c["fg"], 600, spacing=-0.2)
    b += f'<line x1="24" y1="140" x2="386" y2="140" stroke="{c["line"]}"/>'
    b += t(24, 162, "Read on theharshsolanki.in", 12, c["subtle"], 400, MONO) + t(386, 162, "→", 13, c["accent"], 500, MONO, "end")
    return svg(410, 184, c, b, f"Post: {title}")


def contact(c):
    b = heading(c, "06", "Contact", "Let's build something")
    y = 116
    for label, value in CONTACT:
        b += f'<line x1="{PAD}" y1="{y - 22}" x2="{W - PAD}" y2="{y - 22}" stroke="{c["line"]}"/>'
        b += t(PAD, y, label.upper(), 11, c["subtle"], 400, MONO, spacing=1) + t(184, y, value, 15, c["fg"], 500)
        y += 40
    return svg(W, y - 8, c, b, "Contact")


def section_head(num, label, title):
    return lambda c: svg(W, 96, c, heading(c, num, label, title), title)


CARDS = {
    "hero": hero,
    "expertise": expertise,
    "journey": journey,
    "work": featured,
    "lab": lab,
    "writing": section_head("04", "Writing", "Latest writing"),
    "activity": section_head("05", "Activity", "On GitHub"),
    "contact": contact,
}
CARDS.update({f"project-{p[0]}": (lambda p: lambda c: project(c, *p))(p) for p in PROJECTS})
CARDS.update({f"post-{i + 1}": (lambda p: lambda c: post(c, *p))(p) for i, p in enumerate(WRITING)})


def main():
    OUT.mkdir(exist_ok=True)
    for name, build in CARDS.items():
        for theme, colors in THEMES.items():
            (OUT / f"{name}-{theme}.svg").write_text(build(colors), encoding="utf-8")
    print(f"wrote {len(CARDS) * 2} files to {OUT}")


if __name__ == "__main__":
    main()
