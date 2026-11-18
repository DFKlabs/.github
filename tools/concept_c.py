"""Concept C, "Terminal": the profile as a shell session that types itself, neofetch-style, with keycaps for the socials."""
from pathlib import Path
from common import *
import apps_cards

OUT = Path(__file__).parent / 'c'
WIN, BAR, LINE, INK, DIM, MUTE = '#0b0f14', '#141a22', 'rgba(255,255,255,.08)', '#e6edf3', '#8b949e', '#4b5563'
GREEN, BLUE2, AMBER, PINK, BLUE = '#34d399', '#60a5fa', '#fbbf24', '#f472b6', '#2563eb'
MONO = "JBM,ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS = "Inter,system-ui,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
CSS = f"""
.m{{font-family:{MONO}}} .s{{font-family:{SANS}}}
.type{{clip-path:inset(0 100% 0 0);animation:type .55s steps(28,end) forwards}}
.show{{opacity:0;animation:show .01s linear forwards}}
.blink{{animation:blink 1.1s steps(1) infinite}}
.scan{{animation:scan 6s linear infinite}}
@keyframes type{{to{{clip-path:inset(0 0 0 0)}}}}
@keyframes show{{to{{opacity:1}}}}
@keyframes blink{{50%{{opacity:0}}}}
@keyframes scan{{from{{transform:translateY(-120px)}}to{{transform:translateY(760px)}}}}
"""
FONTS = (('JBM', 500), ('JBM', 700), ('JBM', 800), ('Inter', 900))
UNIT_X, UNIT_Y, UNIT_S = 830, 350, .38   # where UNIT stands in the header window (his rig is a 1000-unit square)

# a 5-row block font for the banner, drawn with full blocks
GLYPHS = {
    'D': ['████ ', '█   █', '█   █', '█   █', '████ '], 'F': ['█████', '█    ', '████ ', '█    ', '█    '],
    'K': ['█   █', '█  █ ', '███  ', '█  █ ', '█   █'], 'L': ['█    ', '█    ', '█    ', '█    ', '█████'],
    'A': [' ███ ', '█   █', '█████', '█   █', '█   █'], 'B': ['████ ', '█   █', '████ ', '█   █', '████ '],
    'S': [' ████', '█    ', ' ███ ', '    █', '████ '], ' ': ['  ', '  ', '  ', '  ', '  '],
}


def banner(text, x, y, cell, color, delay):
    out = []
    cx = x
    for ch in text:
        g = GLYPHS[ch]
        for r, row in enumerate(g):
            for c, px in enumerate(row):
                if px == '█':
                    out.append(f'<rect x="{cx + c * cell}" y="{y + r * cell}" width="{cell - 1.5}" height="{cell - 1.5}" fill="{color}"/>')
        cx += (len(g[0]) + 1) * cell
    return f'<g class="show" style="animation-delay:{delay}s">' + ''.join(out) + '</g>'


def window(w, h, title):
    return (f'<rect width="{w}" height="{h}" fill="{BG}"/><rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="{WIN}" stroke="{LINE}" stroke-width="2"/>'
            f'<path d="M1 15a14 14 0 0 1 14-14h{w - 30}a14 14 0 0 1 14 14v31H1z" fill="{BAR}"/>'
            f'<circle cx="30" cy="24" r="7" fill="#ff5f57"/><circle cx="54" cy="24" r="7" fill="#febc2e"/><circle cx="78" cy="24" r="7" fill="#28c840"/>'
            f'<text x="{w / 2}" y="29" class="m" font-size="13" fill="{DIM}" text-anchor="middle">{title}</text>'
            # scanline sheen that drifts down the screen
            f'<defs><linearGradient id="sh" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".035"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<pattern id="lines" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" fill-opacity=".22"/></pattern>'
            f'<clipPath id="scr"><rect x="2" y="46" width="{w - 4}" height="{h - 48}" rx="12"/></clipPath></defs>'
            f'<g clip-path="url(#scr)"><rect class="scan" x="0" y="0" width="{w}" height="120" fill="url(#sh)"/><rect x="0" y="46" width="{w}" height="{h}" fill="url(#lines)"/></g>')


def prompt(x, y, cmd, delay, size=19):
    return (f'<text x="{x}" y="{y}" class="m show" font-size="{size}" style="animation-delay:{delay}s"><tspan fill="{GREEN}">dfk</tspan><tspan fill="{MUTE}">@</tspan><tspan fill="{BLUE2}">labs</tspan><tspan fill="{DIM}"> ~ $ </tspan></text>'
            f'<text x="{x + size * 8.4}" y="{y}" class="m type" font-size="{size}" fill="{INK}" style="animation-delay:{delay + .15}s">{esc(cmd)}</text>')


def unit_hello(start):
    """UNIT's "hi, i'm unit" clip as a flipbook, drawn by his own rig from the DFK checkout."""
    import sys
    sys.path.insert(0, str(UNIT_SRC))
    from anim import CLIPS
    from flipbook import flipbook
    clip = next(c for c in CLIPS if c.name == '01-hi-im-unit')
    return flipbook(clip, fps=30, ns='u', start=start, parts=True)


def header():
    W, H = PANEL - 2 * PAD, 700
    b = [window(W, H, 'dfklabs — zsh — 120×32')]
    b.append(prompt(40, 94, 'whoami --pretty', .2))
    b.append(banner('DFK', 46, 130, 15, GREEN, 1.0) + banner('LABS', 46, 230, 15, BLUE2, 1.15))
    info = [('org', 'DFK Labs', INK), ('builds', 'iPhone · Apple Watch · web', INK), ('apps', 'Birdio · Cooked · Nitnoi · Cue', INK),
            ('web', 'Quakes · Studio', INK), ('rules', 'no servers · no accounts · no tracking', AMBER),
            ('site', 'dfklabs.com', BLUE2), ('unit', 'online · dfklabs.com/unit', GREEN)]
    y = 138
    for k, (key, val, col) in enumerate(info):
        d = 1.4 + k * .16
        b.append(f'<text x="600" y="{y}" class="m show" font-size="19" style="animation-delay:{d:.2f}s"><tspan fill="{GREEN}" font-weight="700">{key:<7}</tspan><tspan fill="{col}"> {esc(val)}</tspan></text>')
        y += 36
    b.append(f'<line x1="600" y1="{y - 18}" x2="1190" y2="{y - 18}" stroke="{LINE}" class="show" style="animation-delay:2.5s"/>')
    for i, c in enumerate(['#0f1115', '#f87171', GREEN, AMBER, BLUE, PINK, '#22d3ee', INK]):
        b.append(f'<rect x="{600 + i * 40}" y="{y}" width="34" height="22" rx="3" fill="{c}" class="show" style="animation-delay:{2.6 + i * .04:.2f}s"/>')
    for k, line in enumerate(['# small software that works offline,', '# on-device, without an account.']):
        b.append(f'<text x="40" y="{420 + k * 26}" class="m show" font-size="18" fill="{DIM}" style="animation-delay:2.4s">{line}</text>')
    # unitsay: like cowsay, with UNIT, the studio's mascot, as the one talking
    b.append(prompt(40, 516, 'unitsay "hi, i\'m unit."', 2.9))
    said = 3.6
    bubble = [' ________________', "< hi, i'm unit. >", ' ----------------', '                \\', '                 \\']
    b.append(f'<g class="show" style="animation-delay:{said}s">' + ''.join(
        f'<text x="668" y="{482 + k * 23}" class="m" font-size="17" fill="{INK if k == 1 else DIM}">{esc(t)}</text>' for k, t in enumerate(bubble)) + '</g>')
    defs, unit, unit_css = unit_hello(said)
    b.append(f'{defs}<g transform="translate({UNIT_X} {UNIT_Y}) scale({UNIT_S})">{unit}</g>')
    b.append(f'<g class="show" style="animation-delay:{said + .3:.1f}s">{prompt(40, 568, "", 0)}'
             f'<rect x="{40 + 19 * 8.4}" y="551" width="11" height="22" fill="{GREEN}" class="blink"/></g>')
    # the prompt that opens the app cards sits under the window, in the same image
    IH = PAD + H + 65
    b = [f'<rect width="{PANEL}" height="{IH}" fill="{BG}"/><g transform="translate({PAD} {PAD})">'] + b + ['</g>',
         f'<text x="{PAD + 15}" y="{PAD + H + 40}" class="m" font-size="17"><tspan fill="{GREEN}">dfk</tspan><tspan fill="{MUTE}">@</tspan><tspan fill="{BLUE2}">labs</tspan><tspan fill="{DIM}"> ~ $ </tspan><tspan fill="{INK}">open ~/apps ~/web</tspan><tspan fill="{MUTE}">   # each in its own colours</tspan></text>']
    return svg(PANEL, IH, ''.join(b), font_css(*FONTS) + CSS + unit_css,
               'DFK Labs — a terminal session: apps for iPhone, Apple Watch and the web; no servers, no accounts, no tracking. UNIT, the mascot, says hi.')


def repo(key, i):
    x0, W = slot(2, i)
    H = 450
    r = REPOS[key]
    b = [window(W, H, f'~/open-source/{key}')]
    b.append(prompt(30, 88, f'cat {key}/README.md | head', .2, 16))
    b.append(f'<text x="30" y="150" class="s show" font-size="50" font-weight="900" fill="{INK}" letter-spacing="-2" style="animation-delay:.9s">{r["title"]}</text>'
             f'<text x="30" y="188" class="m show" font-size="16" fill="{DIM}" style="animation-delay:1s"># {esc(r["line1"])}</text>'
             f'<text x="30" y="212" class="m show" font-size="16" fill="{DIM}" style="animation-delay:1s">#   {esc(r["line2"])}</text>')
    if key == 'airgap':
        lines = [('const', BLUE2, ' TONES = ', INK, '16', AMBER, ';  // 1.0–3.4 kHz', MUTE),
                 ('const', BLUE2, ' PREAMBLE = ', INK, '[0,15,0,15,0,15]', AMBER, ';', MUTE),
                 ('const', BLUE2, ' SYM = ', INK, '0.07', AMBER, ', GAP = 0.02;', MUTE)]
    else:
        lines = [('"git"', GREEN, ': { ', INK, '"deploymentEnabled"', GREEN, ': {', INK),
                 ('  "*"', GREEN, ': ', INK, 'false', PINK, ',   // every branch', MUTE),
                 ('  "main"', GREEN, ': ', INK, 'true', AMBER, '  // production only', MUTE)]
    y = 254
    for k, parts in enumerate(lines):
        spans = ''.join(f'<tspan fill="{parts[i + 1]}">{esc(parts[i])}</tspan>' for i in range(0, len(parts), 2))
        b.append(f'<rect x="20" y="{y - 20}" width="{W - 40}" height="30" fill="{BG}" fill-opacity=".6"/>'
                 f'<text x="30" y="{y}" class="m show" font-size="15.5" style="animation-delay:{1.2 + k * .15:.2f}s"><tspan fill="{MUTE}">{k + 1}  </tspan>{spans}</text>')
        y += 30
    x = 30
    for c in r['chips']:
        w = 20 + len(c) * 9.6
        b.append(f'<rect x="{x}" y="{y + 10}" width="{w:.0f}" height="30" rx="6" fill="none" stroke="{GREEN}" stroke-opacity=".5"/>'
                 f'<text x="{x + w / 2:.0f}" y="{y + 30}" class="m" font-size="14" fill="{GREEN}" text-anchor="middle">{esc(c)}</text>')
        x += w + 10
    b.append(f'<text x="{W - 30}" y="{H - 24}" class="m" font-size="13" fill="{BLUE2}" text-anchor="end">open {r["url"]} ↗</text>')
    return tile(PANEL // 2, H + PAD, x0, ''.join(b), font_css(*FONTS) + CSS, f'{r["title"]} — {r["line1"]} {r["line2"]}')


def apps():
    W, H = 1240, 300
    b = [window(W, H, 'ls ~/apps ~/web')]
    b.append(prompt(30, 88, 'ls -1 ~/apps ~/web', .2, 16))
    items = [(n, l, icon_uri(i)) for n, l, i in APPS] + [(n, l, None) for n, l in TOOLS]
    cw = (W - 60) / 3
    for k, (name, line, uri) in enumerate(items):
        x = 30 + (k % 3) * cw; y = 120 + (k // 3) * 80
        d = .9 + k * .12
        if uri:
            b.append(f'<g class="show" style="animation-delay:{d:.2f}s"><clipPath id="c{k}"><rect x="{x}" y="{y}" width="56" height="56" rx="14"/></clipPath><image href="{uri}" x="{x}" y="{y}" width="56" height="56" clip-path="url(#c{k})"/></g>')
        else:
            b.append(f'<g class="show" style="animation-delay:{d:.2f}s"><rect x="{x}" y="{y}" width="56" height="56" rx="14" fill="none" stroke="{AMBER if name == "Quakes" else BLUE2}" stroke-width="2"/>'
                     f'<text x="{x + 28}" y="{y + 36}" class="m" font-size="20" font-weight="800" fill="{AMBER if name == "Quakes" else BLUE2}" text-anchor="middle">{"~" if name == "Quakes" else "▦"}</text></g>')
        b.append(f'<text x="{x + 74}" y="{y + 24}" class="m show" font-size="19" font-weight="800" fill="{INK}" style="animation-delay:{d:.2f}s">{name}{"" if uri else ".web"}</text>'
                 f'<text x="{x + 74}" y="{y + 48}" class="m show" font-size="14" fill="{DIM}" style="animation-delay:{d:.2f}s">{esc(line)}</text>')
    return svg(W, H, ''.join(b), font_css(*FONTS) + CSS, 'Also from DFK Labs: Birdio, Nitnoi, Cue, Cooked, Quakes and Studio.')


def label_repos():
    W, H = PANEL, 130   # at least 24px tall on a phone, or the line box shows under it
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         f'<text x="30" y="50" class="m" font-size="17"><tspan fill="{GREEN}">dfk</tspan><tspan fill="{MUTE}">@</tspan><tspan fill="{BLUE2}">labs</tspan><tspan fill="{DIM}"> ~ $ </tspan><tspan fill="{INK}">ls ~/open-source</tspan></text>',
         f'<text x="30" y="86" class="m" font-size="17"><tspan fill="{BLUE2}" font-weight="700">airgap/</tspan><tspan fill="{DIM}">        text over sound            </tspan><tspan fill="{BLUE2}" font-weight="700">deploybudget/</tspan><tspan fill="{DIM}">   vercel builds, on a budget</tspan></text>']
    return svg(W, H, ''.join(b), font_css(('JBM', 500), ('JBM', 700)) + CSS, 'ls ~/open-source: airgap, text over sound; deploybudget, Vercel builds on a budget')


def key(name, label, handle, i):
    x0, W = slot(3, i)   # a keycap as wide as an app card
    b = [f'<rect x="0" y="6" width="{W:g}" height="120" rx="16" fill="#05070a"/>',
         f'<rect x="1" y="1" width="{W - 2:g}" height="114" rx="16" fill="{BAR}" stroke="{LINE}" stroke-width="2"/>',
         f'<rect x="10" y="8" width="{W - 20:g}" height="96" rx="11" fill="{WIN}"/>',
         f'<g transform="translate(32 34) scale(1.75)"><path d="{glyph(name)}" fill="{INK}"/></g>',
         f'<text x="98" y="62" class="m" font-size="26" font-weight="800" fill="{INK}">{handle}</text>',
         f'<text x="98" y="86" class="m" font-size="12" fill="{GREEN}" letter-spacing="2">open {label}</text>']
    return tile(PANEL // 3, 126 + PAD, x0, ''.join(b), font_css(('JBM', 500), ('JBM', 800)) + CSS, f'DFK Labs on {label}: {handle}')


def footer():
    W, H = PANEL, 130   # at least 24px tall on a phone, like label_repos
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         f'<text x="30" y="50" class="m" font-size="16"><tspan fill="{GREEN}">dfk</tspan><tspan fill="{MUTE}">@</tspan><tspan fill="{BLUE2}">labs</tspan><tspan fill="{DIM}"> ~ $ </tspan><tspan fill="{INK}">exit</tspan></text>',
         f'<text x="30" y="80" class="m" font-size="16"><tspan fill="{DIM}">logout</tspan><tspan fill="{MUTE}">   # © 2026 DFK Labs · dfklabs.com</tspan></text>']
    return svg(W, H, ''.join(b), font_css(('JBM', 500)) + CSS, 'exit. © 2026 DFK Labs.')


def readme():
    """The panel, then the same story in real text. The panel is one paragraph of images, row by row,
    with no whitespace between images and align="top" on each, so it has no seams."""
    L = LINKS
    rows = [
        img('terminal.svg', '100%', 'DFK Labs — apps for iPhone, Apple Watch and the web; no servers, no accounts, no tracking. '
            'UNIT, the studio\'s mascot, waves hello from the terminal.', L['site']),
        apps_cards.readme_block(),
        img('label-repos.svg', '100%', 'ls ~/open-source: airgap and deploybudget', L['repos']),
        img('repo-airgap.svg', '50%', 'airgap — text over sound. Two phones, flight mode on: one chirps, the other reads. '
            'Send text between two phones with sound, no internet, no server.', L['airgap'])
        + img('repo-deploybudget.svg', '50%', 'deploybudget — stop Vercel from building every branch you push.', L['deploybudget']),
        img('x.svg', THIRD, 'X: @dfklabs', L['x']) + img('instagram.svg', THIRD, 'Instagram: @dfklabs', L['instagram'])
        + img('reddit.svg', THIRD, 'Reddit: r/dfklabs', L['reddit']),
        img('footer.svg', '100%', 'exit. © 2026 DFK Labs — dfklabs.com', L['site']),
    ]
    return '<p align="center">' + '<br>\n'.join(rows) + '</p>\n\n' + text()


def text():
    """Real text under the panel, for search engines and AI readers: who we are, every app, every link."""
    L, U = LINKS, {k: c['url'] for k, c in apps_cards.CARDS.items()}
    return f'''## About DFK Labs

DFK Labs builds small software for iPhone, Apple Watch and the web that works offline, on-device and
without an account: no servers, no accounts, no tracking. Everything is at [dfklabs.com]({L['site']}).

### UNIT

UNIT is the studio's character: the DFK mark with a screen for a face, a status light set into his rim
and eyes that are glowing screen pills. He is the one waving from the terminal at the top of this page.
Meet him at [dfklabs.com/unit]({L['unit']}).

### Apps

- **[Birdio]({U['birdio']})**, for iPhone and Apple Watch: the free golf app. Your real handicap, every round remembered.
- **[Cooked]({U['cooked']})**, for iPhone: your feeds, measured in metres.
- **[Nitnoi]({U['nitnoi']})**, for Apple Watch and iPhone: the words and the money of your trip on your Apple Watch.
  Sixteen words carry a market stall.
- **[Cue]({U['cue']})**, for Apple Watch and iPhone: discreet speaker notes for Apple Watch. Your speech, on your wrist.
- **[Quakes]({U['quakes']})**, on the web: a live earthquake tracker and map. Every earthquake on Earth, minutes after it happens.
- **[Studio]({U['studio']})**, on the web: 66 free browser tools that never upload your files.

### Open source

- **[airgap]({L['airgap']})**: text over sound. Open [dfklabs.com/labs/airgap](https://dfklabs.com/labs/airgap)
  on two phones with flight mode on: one chirps a message and the other reads it, with no internet, no server and
  no account. It is a modem in about 330 lines of JavaScript with no dependencies: 16 tones from 1.0 to 3.4 kHz
  carry 4 bits each, messages travel in packets of up to 20 bytes with a CRC-16 checksum, and the receiver decodes
  them with the Goertzel algorithm. MIT License.
- **[deploybudget]({L['deploybudget']})**: stop Vercel from building every branch you push. A drop-in
  `vercel.json` keeps automatic deployments for your production branch only, which fixes "Deployment rate
  limited — retry in 24 hours" on the Hobby plan and stops paying for builds nobody opens on Pro, where build
  minutes are metered.
  `apply.mjs` (Node 18 or newer, zero dependencies) applies it to every project in a folder at once, and it also
  installs as a Claude Code plugin. Apache-2.0; the templates are CC0.

### Follow DFK Labs

[dfklabs.com]({L['site']}) · [X: @dfklabs]({L['x']}) · [Instagram: @dfklabs]({L['instagram']}) ·
[Reddit: r/dfklabs]({L['reddit']}) · [all repositories]({L['repos']})
'''


def build(out=OUT):
    out = Path(out); a = out / 'assets'; a.mkdir(parents=True, exist_ok=True)
    (a / 'terminal.svg').write_text(header())
    (a / 'repo-airgap.svg').write_text(repo('airgap', 0))
    (a / 'repo-deploybudget.svg').write_text(repo('deploybudget', 1))
    (a / 'label-repos.svg').write_text(label_repos())
    apps_cards.build(a)
    (a / 'x.svg').write_text(key('x', 'x.com', '@dfklabs', 0))
    (a / 'instagram.svg').write_text(key('instagram', 'instagram', '@dfklabs', 1))
    (a / 'reddit.svg').write_text(key('reddit', 'reddit', 'r/dfklabs', 2))
    (a / 'footer.svg').write_text(footer())
    (out / 'README.md').write_text(readme())


if __name__ == '__main__':
    import sys
    build(*sys.argv[1:2])   # optional output folder, e.g. profile
