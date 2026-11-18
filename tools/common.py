"""Shared pieces for the three profile README concepts."""
import base64, json, os, re
from pathlib import Path

DFK = Path(os.environ.get('DFK', '/home/claude/dfk'))
DAIFUKUS = Path(os.environ.get('DAIFUKUS', '/home/claude/daifukus/daifukus'))
FONTS = DFK / 'fonts/files'
UNIT_SRC = DFK / 'tools/unit/src'   # UNIT's rig, clips and flipbook.py
SYMS = json.load(open(Path(__file__).parent / 'syms.json'))   # real airgap tones for "dfklabs"

LINKS = {
    'site': 'https://dfklabs.com',
    'airgap': 'https://github.com/DFKlabs/airgap',
    'deploybudget': 'https://github.com/DFKlabs/deploybudget',
    'x': 'https://x.com/dfklabs',
    'instagram': 'https://instagram.com/dfklabs',
    'reddit': 'https://www.reddit.com/r/dfklabs',
    'repos': 'https://github.com/orgs/DFKlabs/repositories',
    'unit': 'https://dfklabs.com/unit',
}

# The README is one continuous black panel. GitHub can't colour the page behind it, so every image
# paints its own background and margins, and the README sets the images edge to edge, with no gaps.
PANEL = 1260   # panel width in SVG units; every row of images adds up to exactly this
PAD = 15       # outer margin and gutter between tiles; each tile also keeps half of it above and below
BG = '#07090c'
THIRD = '33.333%'   # README width of a tile in a row of three

APPS = [  # name, one line (from each landing page), icon
    ('Birdio', 'every round, remembered', 'birdio'),
    ('Nitnoi', 'a trip on your watch face', 'nitnoi'),
    ('Cue', 'your speech, one pinch away', 'cue'),
    ('Cooked', 'your feeds, in metres', 'cooked'),
]
TOOLS = [('Quakes', 'live earthquake map'), ('Studio', 'tools that run in your browser')]

REPOS = {
    'airgap': dict(title='airgap', line1='Text over sound. Two phones, flight', line2='mode on: one chirps, the other reads.',
                   chips=['JavaScript', 'MIT', '0 deps'], url='github.com/DFKlabs/airgap'),
    'deploybudget': dict(title='deploybudget', line1='Stop Vercel from building every', line2='branch you push.',
                         chips=['Node ≥ 18', 'Apache-2.0', '0 deps'], url='github.com/DFKlabs/deploybudget'),
}


def b64(path):
    return base64.b64encode(Path(path).read_bytes()).decode()


def font_css(*specs):
    """specs: ('Inter', 900) or ('JBM', 700) ... embedded as data URIs, so GitHub shows the real faces."""
    files = {'Inter': 'inter-latin-{w}-normal.woff2', 'JBM': 'jetbrains-mono-latin-{w}-normal.woff2',
             'Fredoka': 'fredoka-latin-{w}-normal.woff2'}
    out = []
    for fam, w in specs:
        f = FONTS / files[fam].format(w=w)
        out.append(f"@font-face{{font-family:{fam};font-weight:{w};src:url(data:font/woff2;base64,{b64(f)}) format('woff2')}}")
    return '\n'.join(out)


def icon_uri(name):
    return 'data:image/jpeg;base64,' + b64(DAIFUKUS / f'assets/logo-{name}.jpg')


def glyph(name):
    s = (DFK / f'admin/social/platforms/{name}.svg').read_text()
    return re.search(r' d="([^"]+)"', s).group(1)


# only the animated elements (they all carry a class): a bare * would also undo the transforms that place things
REDUCED = '@media (prefers-reduced-motion:reduce){[class]{animation:none!important;opacity:1!important;transform:none!important;clip-path:none!important}}'


def svg(w, h, body, css='', label=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{label}">'
            f'<title>{label}</title><style>text{{white-space:pre}}\n{css}\n{REDUCED}</style>{body}</svg>')


def slot(n, i):
    """Tile i in a row of n: (x, width) of its content, local to its own image (PANEL // n wide)."""
    w = (PANEL - (n + 1) * PAD) / n
    return PAD + i * (w + PAD) - i * PANEL / n, w


def tile(w, h, x, body, css='', label=''):
    """An image w × h on the panel background, its content moved to x and half a gutter down."""
    return svg(w, h, f'<rect width="{w}" height="{h}" fill="{BG}"/><g transform="translate({x:g} {PAD / 2:g})">{body}</g>', css, label)


def img(src, width, alt, href):
    """One README image. align="top" drops the gap a baseline leaves under inline images."""
    return f'<a href="{href}"><img src="assets/{src}" width="{width}" align="top" alt="{alt}"></a>'


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
