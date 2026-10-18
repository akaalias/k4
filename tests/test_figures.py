"""Crib maps must be drawn, not written (issues #67, #68).

Every experiment with a record has figures/NNNN-cribmap.svg, and the method panel of each crib
map holds a drawing: cells, dots, leaders, bars. Sentences alone don't count.
"""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
EXP = ROOT / "experiments"

PANEL = re.compile(r'<rect x="[\d.]+" y="([\d.]+)" width="[\d.]+" height="([\d.]+)" rx="6" fill="#f5f2e6"')
MIN_MARKS = 3   # a lone legend swatch is not a drawing


def marks_in_panel(svg):
    """Rects, circles, paths, lines and polygons whose top sits inside the wash panel."""
    m = PANEL.search(svg)
    if not m:
        return None
    top, bottom = float(m.group(1)), float(m.group(1)) + float(m.group(2))
    ys = [float(y) for y in re.findall(r'<rect [^>]*?\by="([\d.]+)"', svg[m.end():])]
    ys += [float(y) for y in re.findall(r'<circle [^>]*?\bcy="([\d.]+)"', svg)]
    ys += [float(y) for y in re.findall(r'<path d="M\s*[\d.]+[ ,]([\d.]+)', svg)]
    ys += [float(y) for y in re.findall(r'<(?:line|polyline|polygon|ellipse) [^>]*?\b(?:y1|cy|points="[\d.]+,)="?([\d.]+)', svg)]
    return sum(top < y < bottom for y in ys)


def experiments():
    return sorted(p.name for p in EXP.iterdir() if p.is_dir() and re.match(r"\d{4}-", p.name) and (p / "result.json").exists())


@pytest.mark.parametrize("name", experiments())
def test_crib_map_exists(name):
    assert (FIG / f"{name[:4]}-cribmap.svg").exists(), f"{name}: no crib map (program.md step 10)"


@pytest.mark.parametrize("path", sorted(FIG.glob("[0-9][0-9][0-9][0-9]-cribmap.svg")), ids=lambda p: p.name[:4])
def test_crib_map_is_drawn(path):
    n = marks_in_panel(path.read_text())
    assert n is not None, "no method panel found"
    assert n >= MIN_MARKS, f"method panel holds {n} graphic marks: text only, draw the method (issue #68)"
