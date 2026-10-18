"""Draw the public site's social preview card, assets/share.png (1200 x 630), issues #69 and #70.

The crib map of experiment 6, drawn wide: the 97 carved letters of K4 along the top with the 24
known places in accent, the same 97 places along the bottom, and a curve carrying each known letter
to where one route puts it (write the message in rows of 7, read down the columns). One of the ways
that don't work. No title in the image: previews print the page's title under it. Rendered by
headless Chrome so the house fonts are used.

    uv run python tools/share_card.py
"""

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from kryptos.facts import K4, KNOWN  # noqa: E402

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = ROOT / "assets" / "share.png"
W, H = 1200, 630
X0, STEP, CW, CH = 30, 11.75, 10.4, 16          # 97 cells across the card
TOP, BOT = 100, 505                              # the copper row and the reading row
ACC, MUTED, CELL, PAPER = "#8c2f1f", "#6b6a60", "#ebe7d8", "#fffff8"


def land(p):
    """Place p (1-based) after writing 97 letters in rows of 7 and reading the columns down."""
    r, c = divmod(p - 1, 7)
    return c * 14 + r + 1


def cell(i, y, ch, known):
    x = X0 + (i - 1) * STEP
    fill, ink, weight = (ACC, PAPER, 700) if known else (CELL, MUTED, 400)
    out = f'<rect x="{x:.1f}" y="{y}" width="{CW}" height="{CH}" rx="1.5" fill="{fill}"/>'
    if ch:
        out += (f'<text x="{x + CW / 2:.1f}" y="{y + 11.6}" font-family="SF Mono, Menlo, monospace" font-size="9" '
                f'font-weight="{weight}" fill="{ink}" text-anchor="middle">{ch}</text>')
    else:
        out += f'<circle cx="{x + CW / 2:.1f}" cy="{y + CH / 2}" r="1.1" fill="#b9b6a6"/>'
    return out


def svg():
    landed = {land(p): ch for p, ch in KNOWN.items()}
    g = [f'<rect x="14" y="{BOT - 120}" width="{W - 28}" height="{H - BOT + 106}" rx="10" fill="#f3efe2"/>']
    for p in sorted(KNOWN):                                        # curves first, under the cells
        x1, x2 = X0 + (p - 1) * STEP + CW / 2, X0 + (land(p) - 1) * STEP + CW / 2
        y1, y2, m = TOP + CH, BOT, (TOP + CH + BOT) / 2
        bold = p == 22
        g.append(f'<path d="M{x1:.1f},{y1} C{x1:.1f},{m:.1f} {x2:.1f},{m:.1f} {x2:.1f},{y2}" fill="none" stroke="{ACC}" '
                 f'stroke-width="{2.6 if bold else 1.3}" stroke-opacity="{1 if bold else .38}"/>')
    g += [cell(i, TOP, KNOWN.get(i, K4[i - 1]), i in KNOWN) for i in range(1, 98)]
    g += [cell(i, BOT, landed.get(i, ""), i in landed) for i in range(1, 98)]
    g.append(f'<text x="{W / 2}" y="{H - 40}" font-family="Palatino, Palatino Linotype, Book Antiqua, Georgia, serif" '
             f'font-size="22" font-style="italic" fill="{MUTED}" text-anchor="middle">Kryptos K4: the known letters, carried '
             f'by one route that doesn\'t work &#183; alexisrondeau.me/k4</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{"".join(g)}</svg>'


def html():
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;width:{W}px;height:{H}px;'
            f'overflow:hidden;background:{PAPER}}}svg{{display:block}}</style></head><body>{svg()}</body></html>')


def main():
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "card.html"
        page.write_text(html())
        # headless Chrome counts its own frame in the window size, so draw taller and crop the top
        subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", "--force-device-scale-factor=1",
                        f"--window-size={W},{H + 200}", f"--screenshot={OUT}", page.as_uri()],
                       check=True, capture_output=True)
        subprocess.run(["uv", "run", "--quiet", "--with", "pillow", "python", "-c",
                        f"from PIL import Image; Image.open({str(OUT)!r}).crop((0, 0, {W}, {H})).save({str(OUT)!r})"],
                       check=True)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
