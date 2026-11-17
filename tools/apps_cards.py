"""One card per app, each in its own landing page's palette, type and words.

Colours, fonts and headlines are read off the pages in daifukus/DFK:
birdio/index.html, nitnoi/nitnoi.css, cue/index.html, cooked/index.html,
quake/index.html and studio/index.html. Icons are the ones those pages use now.
"""
import base64, io
from pathlib import Path
from PIL import Image
from common import DFK, PAD, PANEL, THIRD, esc, font_css, img, slot, tile

W, H = 400, 440


def icon(path, size=192):
    im = Image.open(DFK / path).convert('RGBA')
    s = min(im.size); im = im.crop(((im.width - s) // 2, (im.height - s) // 2, (im.width + s) // 2, (im.height + s) // 2)).resize((size, size), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()


CARDS = {
    'birdio': dict(url='https://dfklabs.com/birdio', bg=('#0A140E', '#14241A'), ink='#ECE8DC', soft='rgba(236,232,220,.66)', acc='#E3C05A', on='#0A140E',
                   display='Fredoka', dw=700, text='Nunito', tw=600, mono=None, label='IPHONE · APPLE WATCH', name='Birdio', dot=True,
                   lines=['Your real handicap.', 'Every round remembered.'], hi=None, icon=('birdio/birdio-mascot.png', 30)),
    'nitnoi': dict(url='https://dfklabs.com/nitnoi', bg=('#f4eee4', '#ece3d4'), ink='#1c1814', soft='#7b7166', acc='#0e9f88', on='#ffffff',
                   display='Inter', dw=900, text='Inter', tw=500, mono='JBM', label='APPLE WATCH · IPHONE', name='Nitnoi', dot=True,
                   lines=['Sixteen words carry', 'a market stall.'], hi=None, icon=('nitnoi/icon.png', 30)),
    'cue': dict(url='https://dfklabs.com/cue', bg=('#FFFFFF', '#F5F5F7'), ink='#1D1D1F', soft='#6E6E73', acc='#F0A12B', on='#1A1100',
                display='Inter', dw=700, text='Inter', tw=500, mono=None, label='APPLE WATCH · IPHONE', name='Cue', dot=False,
                lines=['Your speech.', 'On your wrist.'], hi=None, icon=('cue/cue-icon.png', 30)),
    'cooked': dict(url='https://dfklabs.com/cooked', bg=('#FFF9F2', '#FBF0E4'), ink='#1F1A17', soft='#6F655D', acc='#E8562A', on='#FFFFFF',
                   display='Fredoka', dw=700, text='Nunito', tw=600, mono=None, label='IPHONE', name='Cooked', dot=False,
                   lines=['Your feeds, measured', 'in metres.'], hi=None, icon=('cooked/icon-180.png', 30), tape='#FFC93C'),
    'quakes': dict(url='https://dfklabs.com/quake', bg=('#0b0e14', '#141924'), ink='#f3f4f7', soft='#a9b0c0', acc='#e8a33d', on='#1a1408',
                   display='Plex', dw=700, text='Plex', tw=500, mono='PlexMono', label='WEB', name='Quakes', dot=False,
                   lines=['Every earthquake on Earth,', 'minutes after it happens.'], hi=1, icon=('quake/quake-icon.png', 24)),
    'studio': dict(url='https://studio.dfklabs.com', bg=('#08090A', '#101315'), ink='#E9EDEB', soft='#B4BDB9', acc='#3FE0C5', on='#062A24',
                   display='Plex', dw=700, text='Plex', tw=500, mono='PlexMono', label='WEB · 66 TOOLS', name='Studio', dot=False,
                   lines=['Small tools that', 'never see your files.'], hi=1, icon=None),
}

ROWS = [['birdio', 'cooked', 'nitnoi'], ['cue', 'quakes', 'studio']]

# what each app is, in a sentence; it goes in the README's alt text after the card's own words
DESC = {
    'birdio': 'The free golf app for iPhone and Apple Watch.',
    'cooked': 'For iPhone.',
    'nitnoi': 'The words and the money of your trip on your Apple Watch.',
    'cue': 'Discreet speaker notes for Apple Watch.',
    'quakes': 'A live earthquake tracker and map.',
    'studio': 'Free browser tools that never upload your files.',
}

FAMILY = {'Fredoka': "Fredoka,ui-rounded,system-ui,sans-serif", 'Nunito': "Nunito,ui-rounded,system-ui,sans-serif",
          'Inter': "Inter,-apple-system,'SF Pro Text',system-ui,sans-serif", 'JBM': "JBM,ui-monospace,monospace",
          'Plex': "Plex,-apple-system,'Segoe UI',system-ui,sans-serif", 'PlexMono': "PlexMono,ui-monospace,monospace"}


def plex_css(*ws, mono=False):
    from common import b64, FONTS
    out = []
    for w in ws:
        f = FONTS / (f'ibm-plex-{"mono" if mono else "sans"}-latin-{w}-normal.woff2')
        out.append(f"@font-face{{font-family:{'PlexMono' if mono else 'Plex'};font-weight:{w};src:url(data:font/woff2;base64,{b64(f)}) format('woff2')}}")
    return '\n'.join(out)


def card(key, i):
    c = CARDS[key]
    fonts = set()
    for fam, w in [(c['display'], c['dw']), (c['text'], c['tw']), (c['mono'] or 'JBM', 500)]:
        fonts.add((fam, w))
    css = []
    for fam, w in sorted(fonts):
        if fam == 'Plex':
            css.append(plex_css(w))
        elif fam == 'PlexMono':
            css.append(plex_css(400, mono=True))
        elif fam in ('Fredoka', 'Inter', 'JBM'):
            css.append(font_css((fam, w)))
        elif fam == 'Nunito':
            from common import b64, FONTS
            css.append(f"@font-face{{font-family:Nunito;font-weight:{w};src:url(data:font/woff2;base64,{b64(FONTS / f'nunito-latin-{w}-normal.woff2')}) format('woff2')}}")
    mono = FAMILY[c['mono'] or 'JBM']
    css.append(".pop{opacity:0;transform-box:fill-box;transform-origin:center;animation:pop .6s cubic-bezier(.34,1.56,.64,1) .1s forwards}"
               "@keyframes pop{from{opacity:0;transform:scale(.7)}to{opacity:1;transform:none}}")
    b = [f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["bg"][0]}"/><stop offset="1" stop-color="{c["bg"][1]}"/></linearGradient>'
         f'<radialGradient id="gl" cx="50%" cy="0%" r="80%"><stop offset="0" stop-color="{c["acc"]}" stop-opacity=".16"/><stop offset="1" stop-color="{c["acc"]}" stop-opacity="0"/></radialGradient>'
         f'<filter id="sh" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#000" flood-opacity=".28"/></filter></defs>',
         f'<rect width="{W}" height="{H}" rx="22" fill="url(#bg)"/><rect width="{W}" height="{H}" rx="22" fill="url(#gl)"/>']
    if c.get('tape'):  # Cooked's yellow measuring tape down the right edge
        b.append(f'<rect x="{W - 30}" y="0" width="30" height="{H}" fill="{c["tape"]}"/>' + ''.join(
            f'<line x1="{W - 30}" y1="{y}" x2="{W - (18 if (y // 18) % 2 else 8)}" y2="{y}" stroke="#1F1A17" stroke-opacity=".55" stroke-width="2"/>' for y in range(12, H, 18)))
        b[1] = f'<clipPath id="r"><rect width="{W}" height="{H}" rx="22"/></clipPath><g clip-path="url(#r)">' + b[1]
        b[-1] = b[-1] + '</g>'
    b.append(f'<text x="34" y="52" font-family="{mono}" font-size="12" letter-spacing="2.5" fill="{c["soft"]}">{c["label"]}</text>')
    # the icon, as the page shows it
    if c['icon']:
        path, r = c['icon']
        b.append(f'<g class="pop" filter="url(#sh)"><clipPath id="ic"><rect x="34" y="80" width="112" height="112" rx="{r}"/></clipPath>'
                 f'<image href="{icon(path)}" x="34" y="80" width="112" height="112" clip-path="url(#ic)"/></g>')
    else:  # Studio's own mark, from its favicon
        b.append(f'<g class="pop" filter="url(#sh)"><rect x="34" y="80" width="112" height="112" rx="27" fill="{c["acc"]}"/>'
                 f'<path d="M68 118h45M68 136h45M68 154h27" stroke="{c["on"]}" stroke-width="11" stroke-linecap="round"/></g>')
    name = esc(c['name'])
    dot = f'<tspan fill="{c["acc"]}">.</tspan>' if c['dot'] else ''
    b.append(f'<text x="32" y="262" font-family="{FAMILY[c["display"]]}" font-weight="{c["dw"]}" font-size="54" fill="{c["ink"]}" letter-spacing="-1.5">{name}{dot}</text>')
    y = 304
    for i, line in enumerate(c['lines']):
        col = c['acc'] if c['hi'] == i else c['ink'] if i == 0 else c['soft']
        if key == 'birdio' and i == 0:  # the page sets "real" in gold
            line_svg = f'Your <tspan fill="{c["acc"]}">real</tspan> handicap.'
            col = c['ink']
        else:
            line_svg = esc(line)
        b.append(f'<text x="34" y="{y}" font-family="{FAMILY[c["text"]]}" font-weight="{c["tw"]}" font-size="21" fill="{col}">{line_svg}</text>')
        y += 30
    slug = c['url'].split('//')[1]
    pw = 28 + len(slug) * 8.6 + 22
    b.append(f'<rect x="34" y="{H - 82}" width="{pw:.0f}" height="44" rx="22" fill="{c["acc"]}"/>'
             f'<text x="{34 + 22}" y="{H - 54}" font-family="{mono}" font-size="14" fill="{c["on"]}">{slug} →</text>')
    x, w = slot(3, i)
    assert w == W
    return tile(PANEL // 3, H + PAD, x, ''.join(b), '\n'.join(css), f'{c["name"]} — {" ".join(c["lines"])} {slug}')


def build(out):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    for row in ROWS:
        for i, k in enumerate(row):
            (out / f'app-{k}.svg').write_text(card(k, i))


def readme_block():
    """The two rows of cards, each row on one line with nothing between the images."""
    alt = {k: f'{CARDS[k]["name"]} — {" ".join(CARDS[k]["lines"])} {DESC[k]}' for k in CARDS}
    return '<br>\n'.join(''.join(img(f'app-{k}.svg', THIRD, alt[k], CARDS[k]['url']) for k in row) for row in ROWS)


if __name__ == '__main__':
    build('/tmp/cards'); print('ok')
