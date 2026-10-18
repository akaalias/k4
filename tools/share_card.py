"""Draw the public site's social preview card, assets/share.png (1200 x 630), issue #69.

The carved text of the sculpture, K1 to K4 in order, as the site's letter cells, with K4 darker and
its 24 known places in accent, under a paper band with the project's question. Rendered by headless
Chrome so the house fonts (Palatino) are used. It carries no counts, so it does not go stale; the
count of ways that don't work is in the page's description instead.

    uv run python tools/share_card.py
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from kryptos.facts import K4, KNOWN  # noqa: E402

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = ROOT / "assets" / "share.png"
W, H, COLS, CW, CH, GAP = 1200, 630, 46, 23, 29, 3


def cells():
    k = [json.loads((ROOT / "data" / f"k{i}.json").read_text()) for i in (1, 2, 3)]
    before = k[0]["ciphertext"] + k[1]["ciphertext_as_carved"] + k[2]["ciphertext"]
    rows = -(-(len(before) + len(K4)) // COLS)
    pad = rows * COLS - len(before) - len(K4)
    out = ['<span class="c t"></span>'] * pad
    out += [f'<span class="c">{ch}</span>' for ch in before]
    out += [f'<span class="c k{" n" if i + 1 in KNOWN else ""}">{ch}</span>' for i, ch in enumerate(K4)]
    return rows, "".join(out)


def html():
    rows, grid = cells()
    gw, gh = COLS * (CW + GAP) - GAP, rows * (CH + GAP) - GAP
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
:root{{--paper:#fffff8;--ink:#111111;--muted:#6b6a60;--accent:#8c2f1f;
--serif:"Palatino","Palatino Linotype","Book Antiqua",Georgia,serif;--mono:ui-monospace,"SF Mono",Menlo,monospace}}
html,body{{margin:0;width:{W}px;height:{H}px;overflow:hidden;background:var(--paper)}}
.g{{position:absolute;left:{(W - gw) // 2}px;top:{H - gh - 6}px;width:{gw}px;display:flex;flex-wrap:wrap;gap:{GAP}px}}
.c{{width:{CW}px;height:{CH}px;border-radius:3px;background:#ebe7d8;color:#a9a594;font:15px/{CH}px var(--mono);text-align:center}}
.c.t{{background:#f1eee3}}
.c.k{{color:var(--ink);background:#e3decb}}
.c.n{{background:var(--accent);color:var(--paper);font-weight:700}}
.band{{position:absolute;left:0;right:0;top:178px;height:250px;background:var(--paper);border-top:2px solid var(--accent);
border-bottom:2px solid var(--accent);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}}
h1{{margin:0 40px;font:italic 400 47px/1.15 var(--serif);color:var(--ink)}}
.s{{margin-top:16px;font:400 25px var(--serif);color:var(--muted)}}
.a{{margin-top:8px;font:italic 400 25px var(--serif);color:var(--accent)}}
</style></head><body><div class="g">{grid}</div><div class="band">
<h1>&ldquo;Can an autonomous research loop<br>find the secret of Kryptos K4?&rdquo;</h1>
<div class="s">an AI agent &middot; one cipher experiment at a time &middot; every result on the record</div>
<div class="a">not solved yet &mdash; alexisrondeau.me/k4</div>
</div></body></html>"""


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
