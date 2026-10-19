"""
Static, aligned art for the profile README: hero window, stat strip, six project cards, toolbox, link buttons.

Everything is monospace so text widths are predictable (0.62 x font size per character), every element is drawn from
one grid, and nothing depends on animation to be visible (the little cursor blink is decoration only).

  python scripts/make_profile_art.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path("assets")
OUT.mkdir(exist_ok=True)

BG, PANEL, EDGE, TEXT, MUTED = "#0d1117", "#161b22", "#30363d", "#e6edf3", "#8b949e"
BLUE, GREEN, AMBER, PURPLE, RED = "#58a6ff", "#7ee787", "#e8a04a", "#d2a8ff", "#ff7b72"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
CW = 0.62  # monospace character width / font size


def width(text, size):
    return len(text) * size * CW


def wrap(text, size, max_px):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if width(trial, size) <= max_px:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    return lines + [cur] if cur else lines


def svg(w, h, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
            f'aria-label="{escape(label)}"><style>text{{font-family:{MONO}}}'
            f'@keyframes blink{{50%{{opacity:0}}}}.cur{{animation:blink 1.1s steps(1) infinite}}</style>{body}</svg>')


def write(name, w, h, body, label):
    (OUT / name).write_text(svg(w, h, body, label), encoding="utf-8")


def chrome(w, title):
    return (f'<rect x="1" y="1" width="{w-2}" height="36" rx="11" fill="{PANEL}"/>'
            f'<rect x="1" y="26" width="{w-2}" height="11" fill="{PANEL}"/>'
            f'<circle cx="22" cy="19" r="5.5" fill="#ff5f56"/><circle cx="42" cy="19" r="5.5" fill="#ffbd2e"/>'
            f'<circle cx="62" cy="19" r="5.5" fill="#27c93f"/>'
            f'<text x="86" y="24" fill="{MUTED}" font-size="13">{escape(title)}</text>')


# ---------------------------------------------------------------- hero
def hero():
    w, h = 868, 268
    body = [f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{BLUE}"/>'
            f'<stop offset="1" stop-color="{GREEN}"/></linearGradient></defs>',
            f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="{BG}" stroke="{EDGE}"/>',
            chrome(w, "arnav@iitj: ~/hello"),
            f'<text x="40" y="92" font-size="15"><tspan fill="{GREEN}">$</tspan><tspan fill="{TEXT}"> whoami</tspan></text>',
            f'<text x="38" y="156" font-size="56" font-weight="700" fill="url(#g)">Arnav Yadav</text>',
            f'<text x="40" y="196" font-size="17" fill="{TEXT}">ML systems <tspan fill="{AMBER}">·</tspan> '
            f'LLM training, evaluation &amp; serving</text>']
    chip = "open to research & engineering internships"
    cw_ = width(chip, 13) + 44
    body += [f'<rect x="40" y="218" width="{cw_:.0f}" height="30" rx="15" fill="#0f2a1a" stroke="#238636"/>',
             f'<circle cx="58" cy="233" r="4.5" fill="{GREEN}"/>',
             f'<text x="72" y="238" font-size="13" fill="{GREEN}">{escape(chip)}</text>']
    # the idea in six lines
    px, py, pw, ph = 566, 60, 270, 190
    body.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="8" fill="#0b0f14" stroke="#21262d"/>')
    lines = [[("def ", RED), ("answer", PURPLE), ("(claim):", TEXT)],
             [("  for ", RED), ("a ", TEXT), ("in ", RED), ("sample(8):", TEXT)],
             [("    if ", RED), ("verified(a):", TEXT)],
             [("      vote(a)", TEXT)],
             [("  return ", RED), ("majority()", TEXT)],
             [("    or ", RED), ('"can\'t prove it"', GREEN)]]
    y = py + 34
    for ln in lines:
        spans = "".join(f'<tspan fill="{c}">{escape(t).replace(" ", "&#160;")}</tspan>' for t, c in ln)
        body.append(f'<text x="{px+18}" y="{y}" font-size="13.5" xml:space="preserve">{spans}</text>')
        y += 25
    body.append(f'<rect class="cur" x="{px+18+width("    or " + chr(34) + "can't prove it" + chr(34), 13.5)+4:.0f}" '
                f'y="{y-25-12}" width="8" height="16" fill="{BLUE}"/>')
    write("hero.svg", w, h, "".join(body), "Arnav Yadav, ML systems student at IIT Jodhpur")


# ---------------------------------------------------------------- stats
def stats():
    w, h = 868, 118
    cells = [("26/31", GREEN, "real repos verified by HUMBLE, 36 breaks fixed"),
             ("0.62 s", BLUE, "Pitwall error vs 1.11 s baseline, held out"),
             ("2nd", AMBER, "in Product, Murf AI x IIT Bombay Techfest"),
             ("5 LLMs", PURPLE, "benchmarked and served on one 12 GB GPU")]
    body = [f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="{BG}" stroke="{EDGE}"/>']
    cell = (w - 2) / 4
    for i, (num, col, label) in enumerate(cells):
        x = 1 + i * cell + 28
        if i:
            body.append(f'<rect x="{1 + i*cell:.0f}" y="22" width="1" height="{h-44}" fill="{EDGE}"/>')
        body.append(f'<text x="{x:.0f}" y="55" font-size="32" font-weight="700" fill="{col}">{escape(num)}</text>')
        for j, ln in enumerate(wrap(label, 11.5, cell - 48)):
            body.append(f'<text x="{x:.0f}" y="{78 + j*16}" font-size="11.5" fill="{MUTED}">{escape(ln)}</text>')
    write("stats.svg", w, h, "".join(body), "Four numbers from recent projects")


# ---------------------------------------------------------------- cards
CARDS = [
    ("humble", "HUMBLE", "IBM Bob 2.0 Hackathon", GREEN,
     "Follows a repo's setup docs on a clean machine, repairs what breaks with evidence, replays from zero, opens a PR.",
     "26 of 31 real repos verified, 36 breaks fixed", ["agents", "Docker", "TypeScript"]),
    ("pitwall", "Pitwall", "F1 strategy engine", BLUE,
     "Lap-time model, tyre degradation and a pit-stop decision engine on 2021-2025 races, with a live 3D replay app.",
     "0.62 s error vs 1.11 s, tested once on 2025", ["Python", "dynamic programming", "WebGL"]),
    ("vox", "VOX", "Murf AI x IIT Bombay", AMBER,
     "Real-time voice research agent: live transcription, streaming speech, RAG over PDFs, arXiv, web and patent tools.",
     "2nd in Product, 4th overall in Presentation", ["FastAPI", "React", "RAG"]),
    ("faith", "Faith", "private research", PURPLE,
     "A small open model trained to cite only what a checker can verify: benchmark, verifier and training loop.",
     "every claim measured on held-out data", ["PyTorch", "LoRA", "vLLM"]),
    ("llm", "llm-from-scratch", "Karpathy: Zero to Hero", GREEN,
     "A GPT built from the ground up, one lecture per folder, each run top to bottom. The autograd engine has tests.",
     "micrograd done, makemore in progress", ["Python", "PyTorch", "pytest"]),
    ("desmos", "DESMOS Engine", "C++17", BLUE,
     "Expression parser and function plotter: tokenizer, Shunting-Yard to RPN, stack evaluator, ASCII and Matplotlib plots.",
     "infix to postfix to plot, from scratch", ["C++17", "parsing", "Matplotlib"]),
]


def card(slug, title, sub, col, desc, receipt, tags):
    w, h = 432, 184
    body = [f'<defs><clipPath id="c"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="10"/></clipPath></defs>',
            f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="10" fill="{BG}"/>',
            f'<g clip-path="url(#c)"><rect x="0" y="0" width="6" height="{h}" fill="{col}"/></g>',
            f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="10" fill="none" stroke="{EDGE}"/>',
            f'<text x="28" y="42" font-size="19" font-weight="700" fill="{TEXT}">{escape(title)}</text>',
            f'<text x="{w-24}" y="40" font-size="11" fill="{MUTED}" text-anchor="end">{escape(sub)}</text>']
    y = 70
    for ln in wrap(desc, 12.5, w - 28 - 28)[:3]:
        body.append(f'<text x="28" y="{y}" font-size="12.5" fill="{MUTED}">{escape(ln)}</text>')
        y += 19
    body.append(f'<text x="28" y="136" font-size="12.5" font-weight="700" fill="{col}">&#9656; {escape(receipt)}</text>')
    x = 28
    for t in tags:
        cwid = width(t, 11) + 18
        body.append(f'<rect x="{x:.0f}" y="150" width="{cwid:.0f}" height="22" rx="11" fill="{PANEL}" stroke="{EDGE}"/>'
                    f'<text x="{x + cwid/2:.0f}" y="165" font-size="11" fill="{TEXT}" text-anchor="middle">{escape(t)}</text>')
        x += cwid + 8
    write(f"card-{slug}.svg", w, h, "".join(body), f"{title}: {desc}")


# ---------------------------------------------------------------- toolbox
def toolbox():
    w = 868
    groups = [("languages", ["Python", "C++", "TypeScript", "SQL"]),
              ("ml", ["PyTorch", "Hugging Face", "LoRA / PEFT", "vLLM", "llama.cpp", "scikit-learn"]),
              ("systems", ["FastAPI", "Next.js", "Postgres", "Docker", "Linux", "ROS 2"]),
              ("practice", ["held-out evals", "ablations", "paired bootstrap", "reproducible runs"])]
    body, y = [], 60
    size, gap, x0 = 12, 8, 150
    for label, items in groups:
        body.append(f'<text x="32" y="{y+16}" font-size="12" fill="{GREEN}">{label}</text>')
        x = x0
        for it in items:
            cw_ = width(it, size) + 24
            if x + cw_ > w - 28:
                x, y = x0, y + 32
            body.append(f'<rect x="{x:.0f}" y="{y}" width="{cw_:.0f}" height="24" rx="12" fill="{PANEL}" stroke="{EDGE}"/>'
                        f'<text x="{x + cw_/2:.0f}" y="{y+16}" font-size="{size}" fill="{TEXT}" text-anchor="middle">{escape(it)}</text>')
            x += cw_ + gap
        y += 40
    h = y + 14
    head = (f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="{BG}" stroke="{EDGE}"/>'
            + chrome(w, "arnav@iitj: ~/toolbox"))
    write("toolbox.svg", w, h, head + "".join(body), "Toolbox: languages, ML, systems and practice")


# ---------------------------------------------------------------- buttons
def button(slug, label, col):
    w, h = 286, 46
    body = (f'<defs><clipPath id="c"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="10"/></clipPath></defs>'
            f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="10" fill="{PANEL}"/>'
            f'<g clip-path="url(#c)"><rect x="0" y="0" width="6" height="{h}" fill="{col}"/></g>'
            f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="10" fill="none" stroke="{EDGE}"/>'
            f'<text x="{w/2+3:.0f}" y="28" font-size="15" font-weight="700" fill="{TEXT}" text-anchor="middle">{escape(label)}'
            f' <tspan fill="{col}">&#8599;</tspan></text>')
    write(f"btn-{slug}.svg", w, h, body, label)


if __name__ == "__main__":
    hero()
    stats()
    for c in CARDS:
        card(*c)
    toolbox()
    button("linkedin", "LinkedIn", BLUE)
    button("site", "Portfolio", GREEN)
    button("mail", "Email", AMBER)
    print("wrote", len(list(OUT.glob("*.svg"))), "svg files")
