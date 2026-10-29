"""Generate the profile README SVGs (dark + light) into ./assets.

Run: python3 build.py   (no dependencies). Edit the CONTENT section, re-run, commit.
"""

import math
from html import escape
from pathlib import Path

# ---------------------------------------------------------------- CONTENT
HANDLE = "rteeen"
NAME = "RTeeen"  # shown in the title; swap for your real name if you like
EYEBROW = "// hello, world"
HEADLINE = f"Hi, I'm {NAME}"
SUBTITLE = "I build data pipelines that don't wake anyone up at 3am."
ROLE = "data engineer"
TAGLINE = "pipelines · identity · warehouses"
SOURCES = ["api", "files", "events", "crm", "stream"]

# (kind, text): "cmd" lines are typed after a prompt, "out" lines fade in.
TERMINAL = [
    ("cmd", "whoami"),
    ("out", f"{HANDLE} — {ROLE}"),
    ("cmd", "cat about.txt"),
    ("out", "I build the plumbing that turns messy sources into clean,"),
    ("out", "trustworthy data — ingestion, identity resolution, warehouses."),
    ("cmd", "cat stack.yml"),
    ("out", "lang:   [python, sql, typescript]"),
    ("out", "data:   [snowflake, databricks, dbt, spark]"),
    ("out", "cloud:  [azure, aws]"),
    ("cmd", "ls ./into"),
    ("out", "data-platforms/  dev-tooling/  ai-agents/  automation/"),
]

# ---------------------------------------------------------------- THEMES
THEMES = {
    "dark": dict(
        bg="#0d1117", panel="#0b0f17", border="#30363d", text="#e6edf3",
        muted="#7d8590", faint="#21262d", a1="#22d3ee", a2="#a78bfa", a3="#34d399",
        grid=["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"],
    ),
    "light": dict(
        bg="#ffffff", panel="#f6f8fa", border="#d0d7de", text="#1f2328",
        muted="#59636e", faint="#e4e8ec", a1="#0891b2", a2="#7c3aed", a3="#059669",
        grid=["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"],
    ),
}

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'DejaVu Sans Mono', monospace"
W = 840
CHAR_W = 8.45  # ~0.6em advance of common monospace fonts at 14px

REDUCED = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } .motion { display: none; } }"


def svg(height: int, title: str, css: str, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" '
        f'viewBox="0 0 {W} {height}" xml:space="preserve" role="img" aria-label="{escape(title)}">\n'
        f"<title>{escape(title)}</title>\n<style>\n{css}\n{REDUCED}\n</style>\n{body}\n</svg>\n"
    )


# ---------------------------------------------------------------- TITLE
def title(t: dict) -> str:
    h, cx = 190, W / 2
    css = f"""
    .eyebrow {{ font-family: {MONO}; font-size: 14px; fill: {t['a3']}; letter-spacing: .12em;
                animation: rise .6s ease-out .1s both; }}
    .head {{ font-family: {SANS}; font-size: 64px; font-weight: 800; letter-spacing: -.03em; }}
    .sweep {{ animation: sweep 6s linear infinite; }}
    .sub {{ font-family: {SANS}; font-size: 18px; fill: {t['muted']}; animation: rise .6s ease-out .5s both; }}
    .rule {{ fill: none; stroke: url(#g); stroke-width: 3; stroke-linecap: round; stroke-dasharray: 100;
             animation: draw 1s cubic-bezier(.6,0,.2,1) .3s both; }}
    @keyframes sweep {{ to {{ transform: translateX(-{W}px); }} }}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(8px); }} }}
    @keyframes draw {{ from {{ stroke-dashoffset: 100; }} }}
    """
    stops = [t["a1"], t["a2"], t["a3"], t["a1"], t["a2"], t["a3"], t["a1"]]
    grad = "".join(f'<stop offset="{i / (len(stops) - 1):.3f}" stop-color="{c}"/>' for i, c in enumerate(stops))
    body = f"""<defs>
<linearGradient id="g" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W * 2}" y2="0">{grad}</linearGradient>
<clipPath id="txt"><text class="head" x="{cx}" y="112" text-anchor="middle">{escape(HEADLINE)}</text></clipPath>
</defs>
<text class="eyebrow" x="{cx}" y="36" text-anchor="middle">{escape(EYEBROW)}</text>
<g clip-path="url(#txt)"><rect class="sweep" x="0" y="40" width="{W * 2}" height="90" fill="url(#g)"/></g>
<path class="rule" pathLength="100" d="M{cx - 60},136 H{cx + 60}"/>
<text class="sub" x="{cx}" y="172" text-anchor="middle">{escape(SUBTITLE)}</text>"""
    return svg(h, HEADLINE, css, body)


# ---------------------------------------------------------------- HERO
def hero(t: dict) -> str:
    h = 300
    core_x, core_y = 350, 150
    ys = [50 + i * (200 / (len(SOURCES) - 1)) for i in range(len(SOURCES))]
    css = f"""
    text {{ font-family: {MONO}; }}
    .src rect {{ fill: {t['panel']}; stroke: {t['border']}; }}
    .src text {{ fill: {t['muted']}; font-size: 13px; }}
    .wire {{ fill: none; stroke: {t['faint']}; stroke-width: 2; }}
    .flow {{ fill: none; stroke: {t['border']}; stroke-width: 2; stroke-dasharray: 2 6;
             animation: dash 1.2s linear infinite; }}
    .pkt {{ fill: none; stroke-width: 6; stroke-linecap: round; stroke-dasharray: 0 100;
            animation: pkt 2.4s cubic-bezier(.5,0,.5,1) infinite both; }}
    .ring {{ fill: none; stroke: {t['a2']}; stroke-width: 1.5; stroke-dasharray: 4 7;
             transform-origin: {core_x}px {core_y}px; animation: spin 14s linear infinite; }}
    .core {{ fill: {t['panel']}; stroke: {t['a2']}; stroke-width: 2;
             transform-origin: {core_x}px {core_y}px; animation: pulse 2.4s ease-in-out infinite; }}
    .wh {{ fill: {t['panel']}; stroke: {t['a1']}; stroke-width: 2; }}
    .lbl {{ fill: {t['muted']}; font-size: 11px; letter-spacing: .08em; }}
    .name {{ fill: {t['text']}; font-size: 40px; font-weight: 700; letter-spacing: -.02em; }}
    .role {{ fill: {t['a1']}; font-size: 15px; }}
    .tag {{ fill: {t['muted']}; font-size: 12px; }}
    .caret {{ fill: {t['a3']}; animation: blink 1s steps(1) infinite; }}
    @keyframes dash {{ to {{ stroke-dashoffset: -8; }} }}
    @keyframes pkt {{ from {{ stroke-dashoffset: 100; }} to {{ stroke-dashoffset: 0; }} }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    @keyframes pulse {{ 50% {{ transform: scale(1.06); }} }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    """
    colors = [t["a1"], t["a2"], t["a3"], t["a1"], t["a2"]]
    parts = [f'<rect x="1" y="1" width="{W-2}" height="{h-2}" rx="14" fill="{t["bg"]}" stroke="{t["border"]}"/>']
    for i, (name, y) in enumerate(zip(SOURCES, ys)):
        d = f"M150,{y} C245,{y} 245,{core_y} 300,{core_y}"
        parts.append(f'<g class="src"><rect x="40" y="{y-14}" width="110" height="28" rx="8"/>'
                     f'<text x="95" y="{y+4.5}" text-anchor="middle">{name}</text></g>')
        parts.append(f'<path class="flow" d="{d}"/>')
        parts.append(f'<path class="pkt motion" pathLength="100" stroke="{colors[i]}" d="{d}" '
                     f'style="animation-delay:{i * 0.37:.2f}s"/>')
    # transform core: hexagon
    hexpts = " ".join(f"{core_x + 44*math.cos(math.radians(a)):.1f},{core_y + 44*math.sin(math.radians(a)):.1f}"
                      for a in range(30, 390, 60))
    parts += [
        f'<circle class="ring" cx="{core_x}" cy="{core_y}" r="60"/>',
        f'<polygon class="core" points="{hexpts}"/>',
        f'<text class="lbl" x="{core_x}" y="{core_y + 4}" text-anchor="middle">transform</text>',
        f'<path class="flow" d="M394,{core_y} L466,{core_y}"/>',
        f'<path class="pkt motion" pathLength="100" stroke="{t["a2"]}" d="M394,{core_y} L466,{core_y}" style="animation-delay:1.2s"/>',
        # warehouse cylinder
        f'<path class="wh" d="M470,124 v52 a35,10 0 0 0 70,0 v-52"/>',
        f'<ellipse class="wh" cx="505" cy="124" rx="35" ry="10"/>',
        f'<path class="wh" d="M470,141 a35,10 0 0 0 70,0 M470,158 a35,10 0 0 0 70,0" fill="none"/>',
        f'<text class="lbl" x="505" y="208" text-anchor="middle">warehouse</text>',
        f'<path class="flow" d="M544,{core_y} L572,{core_y}"/>',
        # output: the name
        f'<text class="name" x="582" y="146">{escape(HANDLE)}</text>',
        f'<rect class="caret" x="{582 + len(HANDLE) * 24.3:.0f}" y="116" width="14" height="34" rx="2"/>',
        f'<text class="role" x="584" y="174">&gt; {escape(ROLE)}</text>',
        f'<text class="tag" x="584" y="196">{escape(TAGLINE)}</text>',
    ]
    return svg(h, f"{HANDLE}: {ROLE}", css, "\n".join(parts))


# ---------------------------------------------------------------- TERMINAL
def terminal(t: dict) -> str:
    top, lh, left = 64, 22, 30
    h = top + lh * len(TERMINAL) + lh + 22
    css_rules, parts = [], []
    clock, line_y = 0.6, top
    for i, (kind, txt) in enumerate(TERMINAL):
        if kind == "cmd":
            clock += 0.35
            width = len(txt) * CHAR_W + 4
            dur = max(0.25, len(txt) * 0.055)
            parts.append(f'<text x="{left}" y="{line_y}"><tspan class="ps">$</tspan> <tspan class="cmd">{escape(txt)}</tspan></text>')
            parts.append(f'<rect class="cover c{i}" x="{left + 2*CHAR_W:.1f}" y="{line_y-15}" width="{width:.1f}" height="20"/>')
            css_rules.append(
                f".c{i} {{ transform: translateX({width:.1f}px); animation: type{i} {dur:.2f}s steps({len(txt)}) {clock:.2f}s both; }}"
                f" @keyframes type{i} {{ from {{ transform: translateX(0); }} }}")
            clock += dur + 0.25
        else:
            parts.append(f'<text class="out o{i}" x="{left}" y="{line_y}">{escape(txt)}</text>')
            css_rules.append(f".o{i} {{ animation: fade .3s ease-out {clock:.2f}s both; }}")
            clock += 0.12
        line_y += lh
    clock += 0.3
    parts.append(f'<text x="{left}" y="{line_y}"><tspan class="ps">$</tspan></text>')
    parts.append(f'<rect class="cursor" x="{left + 2*CHAR_W:.1f}" y="{line_y-14}" width="9" height="18"/>')
    css = f"""
    text {{ font-family: {MONO}; font-size: 14px; white-space: pre; }}
    .ps {{ fill: {t['a3']}; font-weight: 700; }}
    .cmd {{ fill: {t['text']}; }}
    .out {{ fill: {t['muted']}; }}
    .cover {{ fill: {t['panel']}; }}
    .cursor {{ fill: {t['a1']}; animation: fade 0s {clock:.2f}s both, blink 1s steps(1) {clock:.2f}s infinite; }}
    .title {{ fill: {t['muted']}; font-size: 12px; }}
    @keyframes fade {{ from {{ opacity: 0; }} }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    {chr(10).join(css_rules)}
    """
    chrome = [
        f'<clipPath id="win"><rect x="1" y="1" width="{W-2}" height="{h-2}" rx="12"/></clipPath>',
        f'<rect x="1" y="1" width="{W-2}" height="{h-2}" rx="12" fill="{t["panel"]}" stroke="{t["border"]}"/>',
        f'<path d="M1,36 H{W-1}" stroke="{t["border"]}"/>',
        *(f'<circle cx="{22 + k*20}" cy="18.5" r="6" fill="{c}"/>' for k, c in enumerate(["#ff5f57", "#febc2e", "#28c840"])),
        f'<text class="title" x="{W/2}" y="23" text-anchor="middle">{escape(HANDLE)}@github: ~</text>',
    ]
    body = "\n".join(chrome) + '\n<g clip-path="url(#win)">\n' + "\n".join(parts) + "\n</g>"
    return svg(h, f"Terminal: about {HANDLE}", css, body)


# ---------------------------------------------------------------- FOOTER
def footer(t: dict) -> str:
    cols, rows, cell, gap = 53, 7, 11, 3
    step = cell + gap
    gx = (W - (cols * step - gap)) / 2
    h = rows * step - gap + 20
    period = 4.0
    rects = []
    for c in range(cols):
        for r in range(rows):
            delay = ((c + r * 1.5) / (cols + rows * 1.5)) * period - period
            rects.append(f'<rect x="{gx + c*step:.1f}" y="{10 + r*step}" width="{cell}" height="{cell}" rx="2.5" '
                         f'style="animation-delay:{delay:.2f}s"/>')
    g = t["grid"]
    css = f"""
    rect {{ fill: {g[0]}; animation: wave {period}s ease-in-out infinite; }}
    @keyframes wave {{
      0%, 55%, 100% {{ fill: {g[0]}; }}
      10% {{ fill: {g[1]}; }} 18% {{ fill: {g[2]}; }} 24% {{ fill: {g[4]}; }} 32% {{ fill: {g[3]}; }} 42% {{ fill: {g[1]}; }}
    }}
    """
    return svg(h, "Animated contribution-style grid", css, "\n".join(rects))


def main() -> None:
    out = Path(__file__).parent / "assets"
    out.mkdir(exist_ok=True)
    for name, fn in [("title", title), ("hero", hero), ("terminal", terminal), ("footer", footer)]:
        for theme, t in THEMES.items():
            (out / f"{name}-{theme}.svg").write_text(fn(t), encoding="utf-8")
    print("wrote", sorted(p.name for p in out.glob("*.svg")))


if __name__ == "__main__":
    main()
