#!/usr/bin/env python3
"""Generate the animated SVGs for the GitHub profile README.

GitHub renders README images through <img>, so these use only inline CSS and SMIL
(no scripts, no web fonts). Run: python3 tools/gen_assets.py
"""
import random
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)
random.seed(1803)

MONO = "'JetBrains Mono','Fira Code','SF Mono',Menlo,Consolas,'Courier New',monospace"
GLYPHS = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾗﾘﾙﾚﾛﾜﾝ0123456789<>/{}=+*#$"
GREEN, CYAN, MAGENTA = "#00ff41", "#00e5ff", "#ff2e88"


def rain(width, height, step=24, size=16, opacity=0.38):
    cols = []
    for x in range(8, width, step):
        n = random.randint(10, 22)
        dur = random.uniform(4.5, 10.0)
        delay = -random.uniform(0, dur)
        spans = "".join(
            f'<tspan x="{x}" dy="{size + 2}">{escape(random.choice(GLYPHS))}</tspan>' for _ in range(n)
        )
        cols.append(
            f'<text class="col" style="animation-duration:{dur:.2f}s;animation-delay:{delay:.2f}s" '
            f'y="0">{spans}</text>'
        )
    return (
        f'<g font-family="{MONO}" font-size="{size}" fill="url(#rain)" opacity="{opacity}">'
        + "".join(cols)
        + "</g>"
    )


def header():
    W, H = 1200, 340
    name = "NIKHIL SAHU"
    sub = "founder @ netsphere tech  //  apps · agents · infra"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Nikhil Sahu, founder of Netsphere Tech">
<defs>
  <linearGradient id="rain" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{GREEN}" stop-opacity="0"/>
    <stop offset="0.75" stop-color="{GREEN}" stop-opacity="0.7"/>
    <stop offset="1" stop-color="#d9ffe1"/>
  </linearGradient>
  <radialGradient id="vignette" cx="50%" cy="50%" r="70%">
    <stop offset="0.55" stop-color="#000" stop-opacity="0"/>
    <stop offset="1" stop-color="#000" stop-opacity="0.85"/>
  </radialGradient>
  <linearGradient id="band" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#000" stop-opacity="0"/>
    <stop offset="0.2" stop-color="#000" stop-opacity="0.78"/>
    <stop offset="0.8" stop-color="#000" stop-opacity="0.78"/>
    <stop offset="1" stop-color="#000" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{GREEN}" stop-opacity="0"/>
    <stop offset="0.5" stop-color="{GREEN}" stop-opacity="0.18"/>
    <stop offset="1" stop-color="{GREEN}" stop-opacity="0"/>
  </linearGradient>
  <pattern id="lines" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="{GREEN}" fill-opacity="0.05"/>
  </pattern>
  <filter id="glow" x="-20%" y="-50%" width="140%" height="200%">
    <feGaussianBlur stdDeviation="4" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <clipPath id="typeclip"><rect x="0" y="200" width="0" height="40">
    <animate attributeName="width" from="0" to="{W}" dur="2.6s" begin="0.8s" fill="freeze"/>
  </rect></clipPath>
  <style>
    .col {{ animation-name: fall; animation-timing-function: linear; animation-iteration-count: infinite; }}
    @keyframes fall {{ from {{ transform: translateY(-440px); }} to {{ transform: translateY({H + 40}px); }} }}
    .scanbar {{ animation: sweep 6s linear infinite; }}
    @keyframes sweep {{ from {{ transform: translateY(-60px); }} to {{ transform: translateY({H}px); }} }}
    .g1 {{ animation: g1 3.2s steps(1) infinite; }}
    .g2 {{ animation: g2 3.2s steps(1) infinite; }}
    @keyframes g1 {{ 0%,86%,100% {{ opacity:0; transform:translate(0,0); }} 88% {{ opacity:.85; transform:translate(-4px,1px); }} 91% {{ opacity:.85; transform:translate(3px,-2px); }} 94% {{ opacity:0; }} }}
    @keyframes g2 {{ 0%,86%,100% {{ opacity:0; transform:translate(0,0); }} 88% {{ opacity:.85; transform:translate(4px,-1px); }} 91% {{ opacity:.85; transform:translate(-3px,2px); }} 94% {{ opacity:0; }} }}
    .main {{ animation: flick 3.2s steps(1) infinite; }}
    @keyframes flick {{ 0%,87%,93%,100% {{ opacity:1; }} 89% {{ opacity:.55; }} 91% {{ opacity:.9; }} }}
    .blink {{ animation: blink 1s steps(1) infinite; }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
  </style>
</defs>
<rect width="{W}" height="{H}" fill="#010a04"/>
{rain(W, H)}
<rect width="{W}" height="{H}" fill="url(#vignette)"/>
<rect x="0" y="96" width="{W}" height="160" fill="url(#band)"/>
<g font-family="{MONO}" font-weight="800" font-size="76" letter-spacing="12" text-anchor="middle">
  <text class="g1" x="{W // 2}" y="182" fill="{MAGENTA}">{name}</text>
  <text class="g2" x="{W // 2}" y="182" fill="{CYAN}">{name}</text>
  <text class="main" x="{W // 2}" y="182" fill="#eafff0" filter="url(#glow)">{name}</text>
</g>
<g clip-path="url(#typeclip)">
  <text x="{W // 2}" y="226" font-family="{MONO}" font-size="21" fill="{GREEN}" text-anchor="middle" letter-spacing="1">&gt; {escape(sub)}<tspan class="blink">█</tspan></text>
</g>
<g font-family="{MONO}" font-size="13" fill="{GREEN}" opacity="0.8" letter-spacing="2">
  <text x="34" y="38">NETSPHERE//SYS  v26.10</text>
  <text x="{W - 34}" y="38" text-anchor="end">ONLINE <tspan class="blink">●</tspan></text>
  <text x="34" y="{H - 26}">&gt; uplink established</text>
  <text x="{W - 34}" y="{H - 26}" text-anchor="end">mode: shipping</text>
</g>
<g stroke="{GREEN}" stroke-width="2" fill="none" opacity="0.7">
  <path d="M16 56 V16 H56"/><path d="M{W - 56} 16 H{W - 16} V56"/>
  <path d="M16 {H - 56} V{H - 16} H56"/><path d="M{W - 56} {H - 16} H{W - 16} V{H - 56}"/>
</g>
<rect width="{W}" height="{H}" fill="url(#lines)"/>
<rect class="scanbar" width="{W}" height="60" fill="url(#scan)"/>
</svg>
'''


def terminal():
    W = 1200
    P, D, C, T, O = GREEN, "#3fae5a", CYAN, "#eaffea", "#8dffad"
    prompt = f'<tspan fill="{P}">nikhil@netsphere</tspan><tspan fill="{D}">:</tspan><tspan fill="{C}">~</tspan><tspan fill="{D}">$ </tspan>'
    # (kind, svg-content, plain-length) — kind "cmd" types out, "out" appears at once
    lines = [
        ("cmd", prompt + f'<tspan fill="{T}">whoami</tspan>', 24),
        ("out", f'<tspan fill="{O}">Nikhil Sahu. Founder of Netsphere Tech. I design, build and ship apps end to end.</tspan>', 0),
        ("gap", "", 0),
        ("cmd", prompt + f'<tspan fill="{T}">cat stack.txt</tspan>', 31),
        ("out", f'<tspan fill="{C}">mobile   </tspan><tspan fill="{O}">flutter · dart · swiftui · ios · android · wear os</tspan>', 0),
        ("out", f'<tspan fill="{C}">backend  </tspan><tspan fill="{O}">go · fastapi · node · firebase · postgres</tspan>', 0),
        ("out", f'<tspan fill="{C}">web      </tspan><tspan fill="{O}">next.js · astro · react · tailwind</tspan>', 0),
        ("out", f'<tspan fill="{C}">infra    </tspan><tspan fill="{O}">hetzner · cloudflare r2 · caddy · github actions</tspan>', 0),
        ("gap", "", 0),
        ("cmd", prompt + f'<tspan fill="{T}">ls ~/shipping</tspan>', 31),
        ("out", f'<tspan fill="{O}">stepzsync/  unfyltered/  bytebox/  shubhly/  orbit/  tether/  netblock/  docverify/</tspan>', 0),
        ("gap", "", 0),
        ("cmd", prompt + f'<tspan fill="{T}">./status --now</tspan>', 32),
        ("out", f'<tspan fill="{P}">[██████████]</tspan><tspan fill="{O}"> ai agents · solution architecture · store releases</tspan>', 0),
        ("gap", "", 0),
        ("cursor", prompt + '<tspan class="blink" fill="#eafff0">█</tspan>', 0),
    ]
    LH, top = 30, 92
    H = top + LH * len(lines) + 30
    clips, body, t = [], [], 0.5
    for i, (kind, content, n) in enumerate(lines):
        y = top + i * LH
        if kind == "gap":
            continue
        if kind == "cmd":
            dur = max(0.6, n * 0.045)
            clips.append(
                f'<clipPath id="c{i}"><rect x="40" y="{y - 22}" width="0" height="30">'
                f'<animate attributeName="width" from="0" to="{W - 80}" dur="{dur:.2f}s" begin="{t:.2f}s" fill="freeze"/></rect></clipPath>'
            )
            t += dur + 0.25
        else:
            clips.append(
                f'<clipPath id="c{i}"><rect x="40" y="{y - 22}" width="0" height="30">'
                f'<set attributeName="width" to="{W - 80}" begin="{t:.2f}s" fill="freeze"/></rect></clipPath>'
            )
            t += 0.18
        body.append(f'<text x="48" y="{y}" clip-path="url(#c{i})" xml:space="preserve">{content}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Terminal: whoami, stack, what I am shipping">
<defs>
  {"".join(clips)}
  <pattern id="lines" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="{GREEN}" fill-opacity="0.035"/></pattern>
  <style>.blink {{ animation: blink 1s steps(1) infinite; }} @keyframes blink {{ 50% {{ opacity: 0; }} }}</style>
</defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="#030c06" stroke="{GREEN}" stroke-opacity="0.35" stroke-width="2"/>
<rect x="1" y="1" width="{W - 2}" height="46" rx="14" fill="#06180c"/>
<rect x="1" y="34" width="{W - 2}" height="13" fill="#06180c"/>
<line x1="1" y1="47" x2="{W - 1}" y2="47" stroke="{GREEN}" stroke-opacity="0.25"/>
<circle cx="30" cy="24" r="7" fill="#ff5f56"/><circle cx="54" cy="24" r="7" fill="#ffbd2e"/><circle cx="78" cy="24" r="7" fill="#27c93f"/>
<text x="{W // 2}" y="29" font-family="{MONO}" font-size="14" fill="{D}" text-anchor="middle">nikhil@netsphere: ~  (zsh)</text>
<g font-family="{MONO}" font-size="19">{"".join(body)}</g>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="url(#lines)"/>
</svg>
'''


def footer():
    W, H = 1200, 70
    strip = "".join(random.choice("01ｱｳｶｻﾀﾅﾊﾏﾔﾗﾜ") for _ in range(120))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="connection closed, keep shipping">
<defs><style>
  .run {{ animation: run 30s linear infinite; }} @keyframes run {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-{W}px); }} }}
  .blink {{ animation: blink 1s steps(1) infinite; }} @keyframes blink {{ 50% {{ opacity: 0; }} }}
</style>
<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="#010a04"/><stop offset=".15" stop-color="#010a04" stop-opacity="0"/><stop offset=".85" stop-color="#010a04" stop-opacity="0"/><stop offset="1" stop-color="#010a04"/></linearGradient></defs>
<rect width="{W}" height="{H}" rx="10" fill="#010a04"/>
<g class="run" font-family="{MONO}" font-size="14" fill="{GREEN}" opacity="0.22" letter-spacing="3">
  <text x="0" y="22">{strip}</text><text x="{W}" y="22">{strip}</text>
  <text x="-300" y="62">{strip}</text><text x="{W - 300}" y="62">{strip}</text>
</g>
<rect width="{W}" height="{H}" fill="url(#fade)"/>
<text x="{W // 2}" y="42" font-family="{MONO}" font-size="16" fill="{GREEN}" text-anchor="middle" letter-spacing="2">&gt; connection closed. keep shipping<tspan class="blink">_</tspan></text>
</svg>
'''


for fname, svg in (("header.svg", header()), ("terminal.svg", terminal()), ("footer.svg", footer())):
    (OUT / fname).write_text(svg, encoding="utf-8")
    print(f"{fname}: {len(svg.encode()) / 1024:.1f} KB")
