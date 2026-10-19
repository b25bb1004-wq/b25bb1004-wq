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
CYCLE = 22.0  # seconds; the whole scene loops
START = 10.4  # the clock starts here: the first frame shows scene 1 finished


def window_css(name, t_on, t_off):
    """Keyframes: invisible until t_on, visible until t_off, fades out at the end of the cycle."""
    a, b = 100 * t_on / CYCLE, 100 * t_off / CYCLE
    return (f"@keyframes {name}{{0%,{a:.2f}%{{opacity:0}}{a+0.6:.2f}%,{b:.2f}%{{opacity:1}}{b+1.2:.2f}%,100%{{opacity:0}}}}"
            f".{name}{{animation:{name} {CYCLE}s linear infinite;animation-delay:-{START}s}}")


def type_css(name, t_on, dur, t_off):
    """Typewriter reveal: a clip rectangle that grows in `steps`, then holds, then resets."""
    a, d, b = 100 * t_on / CYCLE, 100 * dur / CYCLE, 100 * t_off / CYCLE
    return (f"@keyframes {name}{{0%,{a:.2f}%{{width:0}}{a+d:.2f}%,{b:.2f}%{{width:var(--w)}}{b+0.1:.2f}%,100%{{width:0}}}}"
            f".{name}{{animation:{name} {CYCLE}s steps(36,end) infinite;animation-delay:-{START}s}}")


def hero():
    w, h = 868, 292
    css, body, n = [], [], 0
    body += [f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{BLUE}"/>'
             f'<stop offset="1" stop-color="{GREEN}"/></linearGradient></defs>',
             f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="{BG}" stroke="{EDGE}"/>',
             chrome(w, "arnav@iitj: ~/hello")]

    # ---- left: identity (static) + what I am doing now (typed, looping)
    body += [f'<text x="40" y="92" font-size="15"><tspan fill="{GREEN}">$</tspan><tspan fill="{TEXT}"> whoami</tspan></text>',
             f'<text x="38" y="154" font-size="56" font-weight="700" fill="url(#g)">Arnav Yadav</text>',
             f'<text x="40" y="190" font-size="16" fill="{TEXT}">ML systems <tspan fill="{AMBER}">&#183;</tspan> '
             f'LLM training, evaluation &amp; serving</text>']
    typed = [(226, 15, [("$", GREEN), (" cat now.txt", TEXT)], 0.6, 1.0),
             (250, 13.5, [("&gt; ", AMBER), ("teaching a small model to prove its citations", MUTED)], 1.9, 2.2),
             (272, 13.5, [("&gt; ", AMBER), ("serving open LLMs on one 12 GB GPU", MUTED)], 4.4, 1.8)]
    last_x = 40
    for y, size, parts, t_on, dur in typed:
        n += 1
        text_w = sum(len(t.replace("&gt;", ">")) for t, _ in parts) * size * CW
        spans = "".join(f'<tspan fill="{c}" xml:space="preserve">{t}</tspan>' for t, c in parts)
        cid = f"tw{n}"
        css.append(type_css(cid, t_on, dur, 19.5).replace("var(--w)", f"{text_w + 6:.0f}px"))
        body.append(f'<clipPath id="c{cid}"><rect class="{cid}" x="40" y="{y-size}" width="{text_w + 6:.0f}" height="{size+6}"/></clipPath>'
                    f'<text x="40" y="{y}" font-size="{size}" clip-path="url(#c{cid})">{spans}</text>')
        last_x = 40 + text_w
    body.append(f'<rect class="cur" x="{last_x + 6:.0f}" y="{272-13}" width="8" height="15" fill="{BLUE}"/>')

    # ---- right: the answer-or-abstain loop on two demo claims
    px, py, pw, ph = 508, 56, 328, 216
    body.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="8" fill="#0b0f14" stroke="#21262d"/>'
                f'<text x="{px+pw-14}" y="{py+18}" font-size="10.5" fill="#484f58" text-anchor="end">demo</text>')
    scenes = [  # (t_on, t_off, [(text-parts...)])
        [(0.8, [("$ ", GREEN), ('answer "does X reduce Y?"', TEXT)]),
         (2.0, [("retrieved 10 candidate papers", MUTED)]),
         (3.0, [("#1 paper B  ", TEXT), ("&#10007; quote not found", RED)]),
         (3.9, [("#2 paper A  ", TEXT), ("&#10003; verified", GREEN)]),
         (4.8, [("#3 paper A  ", TEXT), ("&#10003; verified", GREEN)]),
         (5.7, [("#4 paper C  ", TEXT), ("&#10007; not entailed", RED)]),
         (6.6, [("#5 paper A  ", TEXT), ("&#10003; verified", GREEN)]),
         (8.0, [("vote: ", MUTED), ("paper A", BLUE), (" (3 of 3 verified)", MUTED)]),
         (9.3, [("&#8594; answered, ", GREEN), ("citation checked", GREEN)])],
        [(12.2, [("$ ", GREEN), ('answer "does Z improve W?"', TEXT)]),
         (13.2, [("retrieved 10 candidate papers", MUTED)]),
         (14.1, [("#1 paper D  ", TEXT), ("&#10007; not entailed", RED)]),
         (15.0, [("#2 paper E  ", TEXT), ("&#10007; quote not found", RED)]),
         (15.9, [("#3 paper D  ", TEXT), ("&#10007; not entailed", RED)]),
         (16.8, [("... 5 more, none verified", MUTED)]),
         (18.0, [("vote: ", MUTED), ("none", RED)]),
         (19.2, [("&#8594; abstained, ", AMBER), ("can't prove it", AMBER)])]]
    scene_off = [11.4, 21.0]
    y0, dy = py + 40, 20
    for si, scene in enumerate(scenes):
        for li, (t_on, parts) in enumerate(scene):
            n += 1
            name = f"l{n}"
            t_start = t_on
            css.append(window_css(name, t_start, scene_off[si]))
            spans = "".join(f'<tspan fill="{c}" xml:space="preserve">{t}</tspan>' for t, c in parts)
            body.append(f'<text class="{name}" x="{px+16}" y="{y0 + li*dy + (6 if li else 0)}" font-size="12.5">{spans}</text>')
    style_extra = "".join(css)
    out = svg(w, h, "".join(body), "Arnav Yadav, ML systems student at IIT Jodhpur")
    out = out.replace("</style>", style_extra + "</style>", 1)
    (OUT / "hero.svg").write_text(out, encoding="utf-8")


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
    ("bench", "local-llm-bench", "5 open LLMs, 1 GPU", "#ff7b72",
     "MMLU and HumanEval runners plus a llama.cpp router that loads each model on demand, with the raw results.",
     "35B MoE: 83.7% MMLU, 75.6% HumanEval", ["llama.cpp", "MMLU", "HumanEval"]),
    ("llm", "llm-from-scratch", "Karpathy: Zero to Hero", GREEN,
     "A GPT built from the ground up, one lecture per folder, each run top to bottom. The autograd engine has tests.",
     "micrograd done, makemore in progress", ["Python", "PyTorch", "pytest"]),
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
