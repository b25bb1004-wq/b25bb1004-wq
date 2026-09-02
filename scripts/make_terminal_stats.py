from pathlib import Path

# Two ideas combined in one compact card, replacing the ASCII portrait:
# a terminal that types out a command, then a set of animated stat bars
# that fill in once the typing finishes. No photo involved, so none of the
# aspect-ratio/legibility problems a character-grid portrait had.

PROMPT = "~$ "
COMMAND = "./vibe_check.sh"
FONT_SIZE = 14
CHAR_W = FONT_SIZE * 0.6  # monospace advance width at this font

BARS = [
    ("COFFEE",    93, "#58a6ff"),
    ("DEBUGGING", 78, "#3fb950"),
    ("SLEEP",     22, "#f0883e"),
    ("CURIOSITY", 100, "#a371f7"),
]

TYPE_STEPS = len(PROMPT + COMMAND)
TYPE_DUR = 0.9  # seconds to "type" the command


def main():
    w, h = 370, 350
    text_x = 28
    cmd_y = 72
    track_x, track_w, track_h = 150, 150, 14
    row_y0, row_step = 132, 44

    cursor_x = text_x + len(PROMPT + COMMAND) * CHAR_W

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="Animated terminal stats for Arnav">',
        f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="10" fill="#0d1117" stroke="#30363d"/>',
        f'<rect x="1" y="1" width="{w-2}" height="34" rx="10" fill="#161b22"/>',
        '<circle cx="20" cy="18" r="5" fill="#ff5f56"/><circle cx="38" cy="18" r="5" fill="#ffbd2e"/><circle cx="56" cy="18" r="5" fill="#27c93f"/>',
        f'<text x="78" y="23" fill="#8b949e" font-family="ui-monospace,monospace" font-size="13">arnav@github — vibe_check</text>',
        '<style>',
        'text{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace}',
        # Typewriter reveal: a clip rect grows left-to-right in discrete
        # per-character jumps (steps()), rather than one continuous scaleX
        # sweep, so it actually reads as characters appearing one at a time.
        f'.type-clip{{transform-box:fill-box;transform-origin:0% 50%;animation:typeIn {TYPE_DUR:.2f}s steps({TYPE_STEPS},end) forwards}}',
        '@keyframes typeIn{from{transform:scaleX(0)}to{transform:scaleX(1)}}',
        f'.cursor{{animation:blink 0.9s step-end infinite;animation-delay:{TYPE_DUR:.2f}s;animation-fill-mode:backwards}}',
        '@keyframes blink{0%,100%{opacity:1}50%{opacity:0}}',
        '.bar-fill{transform-box:fill-box;transform-origin:0% 50%;transform:scaleX(0);animation:growBar .6s ease-out forwards}',
        '.row{opacity:0;transform-box:fill-box;animation:rowIn .5s ease-out forwards}',
        '@keyframes rowIn{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:translateX(0)}}',
        '@keyframes growBar{from{transform:scaleX(0)}to{transform:scaleX(1)}}',
        '</style>',
        f'<clipPath id="type-clip"><rect class="type-clip" x="{text_x-2}" y="{cmd_y-16}" width="{len(PROMPT+COMMAND)*CHAR_W+4}" height="20"/></clipPath>',
        f'<g clip-path="url(#type-clip)">',
        f'<text x="{text_x}" y="{cmd_y}" font-size="{FONT_SIZE}" fill="#7ee787">{PROMPT}</text>',
        f'<text x="{text_x+len(PROMPT)*CHAR_W}" y="{cmd_y}" font-size="{FONT_SIZE}" fill="#c9d1d9">{COMMAND}</text>',
        '</g>',
        f'<rect class="cursor" x="{cursor_x:.1f}" y="{cmd_y-12}" width="8" height="15" fill="#58a6ff"/>',
        f'<text x="{text_x}" y="{cmd_y+29}" font-size="11" fill="#8b949e">──────────────────────────────</text>',
    ]

    for i, (label, pct, color) in enumerate(BARS):
        y = row_y0 + i * row_step
        delay = TYPE_DUR + 0.15 + i * 0.18
        fill_w = track_w * pct / 100
        parts.append(f'<g class="row" style="animation-delay:{delay:.2f}s">')
        parts.append(f'<text x="{text_x}" y="{y}" font-size="12" fill="#7ee787">{label}</text>')
        parts.append(f'<rect x="{track_x}" y="{y-11}" width="{track_w}" height="{track_h}" rx="3" fill="#161b22" stroke="#30363d"/>')
        parts.append(
            f'<rect class="bar-fill" style="animation-delay:{delay+0.1:.2f}s" '
            f'x="{track_x}" y="{y-11}" width="{fill_w:.1f}" height="{track_h}" rx="3" fill="{color}"/>'
        )
        parts.append(f'<text x="{track_x+track_w+14}" y="{y}" font-size="12" fill="#c9d1d9">{pct}%</text>')
        parts.append('</g>')

    parts.append('</svg>')
    Path("assets/terminal-stats.svg").write_text("\n".join(parts), encoding="utf-8")
    print("Wrote assets/terminal-stats.svg")


if __name__ == "__main__":
    main()
