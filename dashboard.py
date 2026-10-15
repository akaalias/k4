#!/usr/bin/env python3
"""Live dashboard, rendered from the experiment record on every request.

    uv run --with markdown python dashboard.py          # serves http://127.0.0.1:8765
    uv run --with markdown python dashboard.py --build  # writes static html to dashboard/

Nothing here is written by hand after the fact: every page is a view of
experiments/*/result.json, experiments/*/experiment.md, results.tsv,
champion.json, families.md and the clue register. Style follows STYLE.md.
"""
import argparse
import html
import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

try:
    import markdown as _md

    def md(text):
        return _md.markdown(text, extensions=["tables", "fenced_code"])
except ImportError:
    def md(text):
        return f"<pre>{html.escape(text)}</pre>"

ROOT = Path(__file__).resolve().parent
EXPERIMENTS = ROOT / "experiments"
STATIC = ROOT / "dashboard"

CSS = """
:root{--paper:#fffff8;--ink:#111111;--muted:#6b6a60;--faint:#9b998c;--rule:#d9d5c3;--rule-soft:#ece9da;
--accent:#8c2f1f;--kept:#111111;--disc:#b9b6a6;--ochre:#8a6a1e;--wash:#fbf8ea;--hl:#f4ecd2;
--serif:"Palatino","Palatino Linotype","Book Antiqua","URW Palladio L",Georgia,serif;--mono:ui-monospace,"SF Mono",Menlo,monospace}
@media(prefers-color-scheme:dark){:root{--paper:#161614;--ink:#ece9da;--muted:#a39f90;--faint:#7c7a6e;--rule:#3a382f;--rule-soft:#2a2924;
--accent:#d9775f;--kept:#ece9da;--disc:#5a584e;--ochre:#c9a227;--wash:#1f1e1a;--hl:#3a3320}}
*{box-sizing:border-box}html{background:var(--paper)}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 var(--serif);font-feature-settings:"onum" 1,"liga" 1;-webkit-font-smoothing:antialiased;padding-bottom:60px}
a{color:var(--accent);text-decoration:none;border-bottom:1px solid transparent}a:hover{border-bottom-color:var(--accent)}
.smcp{font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.08em}
.num{font-variant-numeric:lining-nums tabular-nums}
.topnav{display:flex;gap:28px;justify-content:center;align-items:baseline;flex-wrap:wrap;border-bottom:1px solid var(--rule);padding:18px 0 12px;margin:0}
.topnav .brand{font:italic 14px var(--serif);color:var(--faint)}
.topnav a{font:600 12px var(--serif);font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.09em;color:var(--muted);border-bottom:2px solid transparent;padding-bottom:3px}
.topnav a.on,.topnav a:hover{color:var(--ink);border-bottom-color:var(--ink)}
.wrap{max-width:980px;margin:0 auto;padding:14px 28px 40px}
h1.home{font:italic 400 40px/1.15 var(--serif);text-align:center;margin:28px 0 10px;letter-spacing:-.01em}
p.psub{text-align:center;font-style:italic;color:var(--muted);font-size:15.5px;line-height:1.7;margin:0 auto 8px;max-width:760px}
.stat-hero{max-width:560px;margin:30px auto 4px;text-align:center}
.stat-hero>b{display:block;font-size:56px;line-height:1.05;font-weight:600;color:var(--ink)}
.stat-hero>span{display:block;font:600 11px var(--serif);font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin-top:6px}
.hero-sub{max-width:560px;margin:12px auto 0;font-size:13px;line-height:1.6;color:var(--muted);text-align:center}
.stats{display:flex;flex-wrap:wrap;gap:18px 30px;justify-content:center;margin:22px auto 10px;text-align:center}
.stat{flex:0 1 150px}.stat>b{display:block;font-size:30px;line-height:1.1;font-weight:600}
.stat>span{display:block;font:600 10.5px var(--serif);font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin-top:5px}
.rsec{max-width:980px;margin:52px auto 0;display:flex;align-items:baseline;gap:14px}
.rsec-n{font:italic 26px var(--serif);color:var(--rule);flex:none}.rsec-t{margin:0;font:400 26px/1.2 var(--serif)}
.rsec-sub{margin:6px auto 16px;font:italic 15px/1.55 var(--serif);color:var(--muted)}
table{border-collapse:collapse;width:100%;font-size:14px}th,td{padding:7px 9px;border-bottom:1px solid var(--rule-soft);text-align:left;vertical-align:top}
th{white-space:nowrap;font:600 10.5px var(--serif);font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
td.num,th.num{text-align:right}
.kept{color:var(--ink);font-weight:600}.reverted{color:var(--muted)}.timeout,.error{color:var(--ochre)}
.live-row{background:rgba(140,47,31,.045);box-shadow:inset 0 0 0 1.5px var(--accent)}
.callout{max-width:980px;margin:18px auto 0;padding:14px 20px 12px;border:1px solid var(--rule);border-left:3px solid var(--accent);border-radius:0 2px 2px 0;background:var(--wash)}
.callout-h{font:600 11px var(--serif);font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.08em;color:var(--accent);margin:0 0 6px}
.callout p{margin:0;font-size:15px;line-height:1.6}
code,pre{font:12.5px/1.5 var(--mono)}pre{background:var(--wash);border:1px solid var(--rule-soft);border-radius:2px;padding:12px 14px;overflow:auto}
.ct{letter-spacing:.1em;word-break:break-all}.ct b{color:var(--ink);background:var(--hl)}.ct i{color:var(--accent);font-style:normal}
.lineage li{margin:3px 0}.lineage ul{padding-left:22px}
.muted{color:var(--muted)}.faint{color:var(--faint)}
article{max-width:980px}article h1{font:400 30px/1.2 var(--serif);margin:10px 0 6px}
article h2{font:400 22px/1.25 var(--serif);margin:34px 0 6px;padding-top:12px;border-top:1px solid var(--rule)}
article h3{font:600 12px var(--serif);font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin:22px 0 6px}
article p,article li{max-width:720px}article table{table-layout:fixed;width:100%}article td{vertical-align:top;overflow-wrap:anywhere}article td code{white-space:normal;word-break:break-all;letter-spacing:.04em}article ol{padding-left:26px}article ol li{margin:0 0 8px}
.crumb{max-width:980px;margin:10px auto 0;color:var(--muted);font-size:14px}
.rec-head{max-width:980px;margin:18px auto 0}.eyebrow{font:600 11px var(--serif);font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);margin:0 0 10px}.eyebrow .kept{color:var(--accent)}
h1.rec-title{font:400 34px/1.18 var(--serif);margin:0 0 10px;letter-spacing:-.005em;max-width:900px}
.standfirst{font:italic 16.5px/1.6 var(--serif);color:var(--muted);margin:0 0 18px;max-width:820px}
.meta-row{display:grid;grid-template-columns:repeat(5,1fr);gap:0 24px;padding:14px 0 12px;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule-soft)}.meta-row>div{display:flex;flex-direction:column}.meta-bar{margin-top:7px}.meta-bar svg rect{cursor:help}.meta-bar .faint{display:block;margin-top:3px}.meta-row b{font-weight:600;font-size:14.5px;line-height:1.3}.meta-row span{font:600 10px var(--serif);font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin-top:2px}
.plain p{font-size:17px;line-height:1.7;margin:0 0 12px;max-width:640px}
.gl{border-bottom:1px dotted var(--accent);cursor:help;transition:background .15s}.gl.on,.gl:hover{background:var(--hl)}.gl-entry{border-left:2px solid transparent;padding-left:6px;margin-left:-8px;transition:background .15s}.gl-entry.on,.gl-entry:hover{background:var(--hl);border-left-color:var(--accent)}.aside p{margin:0 0 9px;font-size:13px;line-height:1.5}.aside p b{color:var(--ink);font-weight:600}.aside h4{margin-bottom:8px}.aside .faint{font-size:12px}
.rec-body{max-width:980px}.rec-body h3{font:600 12px var(--serif);font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin:22px 0 6px}.rec-body p,.rec-body li{max-width:720px;font-size:15.5px;line-height:1.6}
.sculpture-wrap{max-width:980px;margin:14px auto 22px}#sculpture{width:100%;border:1px solid var(--rule-soft);border-radius:2px;overflow:hidden;cursor:grab}#sculpture canvas{display:block}.sculpture-foot{display:flex;gap:22px;align-items:baseline;margin-top:8px}.sculpture-key span{font:600 11px var(--serif);font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);margin-right:14px;cursor:pointer;border-bottom:2px solid transparent}.sculpture-key span.on{color:var(--accent);border-bottom-color:var(--accent)}#sculpture-label{margin:0;font-size:13.5px;flex:1}
.explain-row{display:grid;grid-template-columns:1fr 1fr 1fr;gap:34px;max-width:980px;margin:22px auto 0}.explain-col h4{font:600 11px var(--serif);font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.1em;color:var(--accent);margin:0 0 8px}.explain-col p{font-size:15.5px;line-height:1.65;margin:0;color:var(--ink)}
@media(max-width:860px){.explain-row{grid-template-columns:1fr}}
.panel-wrap{display:flex;gap:36px;justify-content:center;flex-wrap:wrap;margin:14px 0 6px}.panel{padding:0}.panel-h{font:600 10.5px var(--serif);font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin:0 0 4px}.panel pre{margin:0;padding:12px 16px;font:15px/1.75 var(--mono);letter-spacing:.14em;background:var(--wash);border:1px solid var(--rule-soft);border-radius:2px}.panel u{text-decoration:none;border-bottom:2px solid var(--rule)}.panel b{color:var(--ink);background:var(--hl);font-weight:700}.panel i{color:var(--accent);font-style:normal;background:var(--hl)}.k3tail{color:var(--rule)}
.gloss{margin:6px 0 28px;padding:10px 0 0;border-top:1px solid var(--rule-soft)}.gloss .callout-h{color:var(--muted)}.gloss dl{margin:0;columns:2;column-gap:32px}.gloss .entry{break-inside:avoid;-webkit-column-break-inside:avoid;page-break-inside:avoid;display:inline-block;width:100%;margin:0 0 8px}.gloss dt{font-weight:600;font-size:13.5px}.gloss dd{margin:1px 0 0 0;color:var(--muted);font-size:13px;line-height:1.5}.gloss p{margin:8px 0 0}
figure.chart{margin:16px 0 0}figure.chart svg{width:100%;height:auto;display:block}
.chart-row{display:grid;grid-template-columns:minmax(0,1fr) 250px;gap:28px;align-items:start;margin-top:8px}
.aside{font-size:13.5px;line-height:1.5;color:var(--muted);border-left:1px solid var(--rule);padding-left:16px;margin-top:16px}
.aside h4{font:600 10.5px var(--serif);font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin:0 0 6px}
.aside p{margin:0 0 10px}.aside svg{display:block;width:100%;height:auto;margin:4px 0 10px}
@media(max-width:860px){.chart-row{grid-template-columns:1fr}.aside{border-left:0;padding-left:0}}
svg text{paint-order:stroke;stroke:var(--paper);stroke-width:2.8px;stroke-linejoin:round;font-family:var(--serif)}
.tip{position:fixed;pointer-events:none;background:var(--paper);border:1px solid var(--rule);padding:6px 9px;font-size:12.5px;line-height:1.45;display:none;max-width:320px;z-index:9}
.foot{position:fixed;left:0;right:0;bottom:0;padding:7px 18px;text-align:center;font:12.5px var(--serif);color:var(--muted);background:var(--paper);border-top:1px solid var(--rule-soft)}
.foot .dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--accent);margin-right:8px;animation:p 1.8s ease-out infinite}
@keyframes p{0%{box-shadow:0 0 0 0 rgba(140,47,31,.45)}70%{box-shadow:0 0 0 7px rgba(140,47,31,0)}100%{box-shadow:0 0 0 0 rgba(140,47,31,0)}}
@media(max-width:640px){.wrap{padding:10px 14px 60px}h1.home{font-size:28px}.stat-hero>b{font-size:40px}.rsec-t{font-size:21px}}
"""

JS = """
<script>
const tip=document.createElement('div');tip.className='tip';document.body.appendChild(tip);
document.querySelectorAll('[data-tip]').forEach(el=>{
 el.addEventListener('mousemove',e=>{tip.innerHTML=el.dataset.tip;tip.style.display='block';
  tip.style.left=(e.clientX+14)+'px';tip.style.top=(e.clientY+14)+'px';});
 el.addEventListener('mouseleave',()=>tip.style.display='none');});
</script>"""


def esc(s):
    return html.escape(str(s))


def load_results():
    rows = []
    if not EXPERIMENTS.exists():
        return rows
    for d in sorted(EXPERIMENTS.iterdir()):
        rj = d / "result.json"
        if d.is_dir() and rj.exists():
            r = json.loads(rj.read_text())
            r["_dir"] = d
            r["_md"] = (d / "experiment.md").read_text() if (d / "experiment.md").exists() else ""
            m = re.search(r"\*\*Family:\*\* (.+?)  ", r["_md"])
            r["family"] = m.group(1).strip() if m else "?"
            m = re.search(r"\*\*Parent:\*\* (.+?)  ", r["_md"])
            p = m.group(1).strip() if m else "none"
            r["parent"] = None if p.startswith("none") else p
            m = re.search(r"^# \S+: (.+)$", r["_md"], re.M)
            r["title"] = m.group(1).strip() if m else r["tag"]
            m = re.search(r"## In plain words\n\n(.+?)\n\n## ", r["_md"], re.S)
            r["eli5"] = m.group(1).strip() if m else ""
            rows.append(r)
    return rows


def champion():
    p = ROOT / "champion.json"
    return json.loads(p.read_text()) if p.exists() else None


PHASE_ORDER = ("design", "implement", "test", "run", "record", "unattributed")
PHASE_FILL = {"design": "var(--ochre)", "implement": "var(--accent)", "test": "var(--muted)",
              "run": "var(--ink)", "record": "var(--disc)", "unattributed": "var(--rule)"}


def fmt_dur(sec):
    if sec is None:
        return ""
    if sec < 90:
        return f"{sec:.0f} s"
    if sec < 5400:
        return f"{sec/60:.0f} min"
    return f"{sec/3600:.1f} h"


def phase_bar(ph, scale_max, width=160, height=10):
    """Length is the experiment's total time against the longest experiment on the page;
    segments are the phases in order. A one-second run is a sliver, by design."""
    total = sum(ph.values())
    if total <= 0 or scale_max <= 0:
        return '<span class="faint">none</span>'
    full = max(2.0, width * total / scale_max)
    x = 0.0
    parts = []
    for k in PHASE_ORDER:
        v = ph.get(k, 0.0)
        if v <= 0:
            continue
        w = full * v / total
        share = 100.0 * v / total
        parts.append(f'<rect x="{x:.1f}" y="0" width="{max(w-0.5,0.5):.1f}" height="{height}" fill="{PHASE_FILL[k]}" data-tip="<b>{k}</b> {fmt_dur(v)}, {share:.0f}% of {fmt_dur(total)}"/>')
        x += w
    pre = sum(ph.get(k, 0.0) for k in ("design", "implement", "test"))
    note = '' if pre >= 10 else ' <span class="faint" style="font-size:11.5px;white-space:nowrap" title="design, implement and test were not clocked; the bar is run time only">unclocked</span>'
    return f'<svg width="{width}" height="{height}" style="vertical-align:middle;overflow:visible">{"".join(parts)}</svg>' + note


def phase_legend():
    return " ".join(f'<span style="display:inline-block;width:9px;height:9px;background:{PHASE_FILL[k]};margin:0 3px 0 10px"></span>{k}' for k in PHASE_ORDER[:5])


def words_str(r):
    w = r.get("best_crib_words") or {}
    return ", ".join(f"{k} {h}/{n}" for k, (h, n) in w.items())


def words_short(r):
    w = r.get("best_crib_words") or {}
    out = []
    for k in ("EAST", "NORTHEAST", "BERLIN", "CLOCK"):
        h, n = w.get(k, (0, 1))
        out.append(k[0] if h == n else (k[0].lower() if h else "."))
    return "".join(out)


K3_TAIL = "ECDMRIPFEIMEHNLSSTTRTVDOHW?"
PANEL_CUTS = (4, 35, 66, 97)   # K4 on the copper: OBKR ends the K3 line, then three lines of 31


def panel_lines(text):
    out, start = [], 0
    for cut in PANEL_CUTS:
        out.append(text[start:cut]); start = cut
    return out


def panel_block(ct, pt, known):
    """Two blocks side by side, laid out as the copper carries K4: the K3 tail and OBKR on the
    first line, then three lines of 31. Left: as carved, known positions underlined. Right: the
    candidate, matches bold on a wash, misses in the accent."""
    def block(text, label, carved):
        lines = []
        offset = 0
        for k, chunk in enumerate(panel_lines(text)):
            cells = []
            for j, ch in enumerate(chunk):
                i = offset + j + 1
                if carved:
                    cells.append(f'<u>{esc(ch)}</u>' if i in known else esc(ch))
                elif i in known:
                    cells.append(f'<b>{esc(ch)}</b>' if ch == known[i] else f'<i>{esc(ch)}</i>')
                else:
                    cells.append(esc(ch))
            lead = f'<span class="k3tail">{esc(K3_TAIL) if carved else "&nbsp;" * len(K3_TAIL)}</span>' if k == 0 else ""
            lines.append(lead + "".join(cells))
            offset += len(chunk)
        return f'<div class="panel"><div class="panel-h">{label}</div><pre>{chr(10).join(lines)}</pre></div>'
    right = block(pt, "candidate", False) if pt else ""
    return f'<div class="panel-wrap">{block(ct, "as carved", True)}{right}</div>'


def best_candidate(r):
    """The candidate the harness ranked best: top fitness among gate passers, else most crib hits."""
    cands = r.get("candidates", [])
    if not cands:
        return None
    passed = [c for c in cands if c.get("gate_passed")]
    if passed:
        return max(passed, key=lambda c: c.get("fitness") if c.get("fitness") is not None else -99)
    return max(cands, key=lambda c: c.get("crib_hits", 0))


def load_glossary():
    import re as _re
    entries = []
    for line in (ROOT / "GLOSSARY.md").read_text().splitlines():
        m = _re.match(r"\*\*(.+?)\*\*\s*(?:\((?:also:)?\s*(.*?)\))?\s*:\s*(.+)", line)
        if m:
            term, aliases, definition = m.group(1), m.group(2) or "", m.group(3)
            names = [term] + [a.strip() for a in aliases.split(",") if a.strip()]
            entries.append((term, names, definition))
    return entries


def glossary_for(text):
    low = text.lower()
    hits = []
    for term, names, definition in load_glossary():
        if any(n.lower() in low for n in names):
            hits.append((term, definition))
    if not hits:
        return ""
    items = "".join(f"<div class='entry'><dt>{esc(t)}</dt><dd>{esc(d)}</dd></div>" for t, d in hits)
    return f'<div class="gloss"><div class="callout-h">Words used above</div><dl>{items}</dl><p class="muted" style="font-size:13px">The full list is on the <a href="/glossary">glossary</a> page.</p></div>'


def link_experiments(html_text, tags):
    """Turn bare experiment numbers like 0012 into links where such a record exists."""
    import re as _re
    by_id = {t[:4]: t for t in tags}
    return _re.sub(r"(?<![\w/-])(\d{4})(?![\w-])", lambda m: f'<a href="/exp/{by_id[m.group(1)]}">{m.group(1)}</a>' if m.group(1) in by_id else m.group(1), html_text)


def k4_marked(pt, known):
    out = []
    for i, ch in enumerate(pt, start=1):
        if i in known:
            out.append(f"<b>{ch}</b>" if ch == known[i] else f"<i>{ch}</i>")
        else:
            out.append(ch)
    return f'<span class="ct">{"".join(out)}</span>'


def loss_chart(rows):
    """Loss per experiment, 0 at the bottom. The axis breaks at 10, the crib gate: the band
    0-10 gets 40% of the height, 10-240 the rest. Kept: ink dot, champion line in accent.
    Reverted: recessive grey dot. No valid candidate: hollow dot at the top."""
    if not rows:
        return "<p class='muted'>No experiments yet.</p>"
    W, H = 980, 360
    L, R, T, B = 130, 150, 24, 40
    n = len(rows)
    gate, ymax = 10.0, 240.0
    plot_h = H - T - B
    low_h = plot_h * 0.40
    y_gate = T + plot_h - low_h
    xs = [L + (i + 0.5) * (W - L - R) / max(n, 1) for i in range(n)]

    def y(v):
        v = min(v, ymax)
        if v <= gate:
            return T + plot_h - low_h * (v / gate)
        return y_gate - (plot_h - low_h) * ((v - gate) / (ymax - gate))

    g = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Loss per experiment; zero is solved">']
    for v in (0, 5, 10, 60, 120, 180, 240):
        yy = y(v)
        if v == gate:
            g.append(f'<line x1="{L}" x2="{W-R}" y1="{yy:.1f}" y2="{yy:.1f}" stroke="var(--accent)" stroke-width="1.5"/>')
        else:
            g.append(f'<line x1="{L}" x2="{W-R}" y1="{yy:.1f}" y2="{yy:.1f}" stroke="var(--rule-soft)" stroke-width="1"/>')
        lab = f"{v}" if v < 60 else f"{v} = {v // 10} wrong"
        g.append(f'<text x="{L-8}" y="{yy+4:.1f}" text-anchor="end" font-size="14" fill="var(--muted)">{lab}</text>')
    # axis break marks just above the gate line
    bx = L - 2
    g.append(f'<path d="M{bx-5},{y_gate-10:.1f} l10,-5 M{bx-5},{y_gate-6:.1f} l10,-5" stroke="var(--muted)" stroke-width="1" fill="none"/>')
    # annotations at right, clear of the plot
    ax = W - R + 10
    g.append(f'<text x="{ax}" y="{y(gate)+4:.1f}" font-size="14" font-style="italic" fill="var(--accent)">all 24 known right</text>')
    g.append(f'<text x="{ax}" y="{y(0)+4:.1f}" font-size="14" font-style="italic" fill="var(--muted)">solved</text>')
    g.append(f'<text x="{ax}" y="{y(ymax)+4:.1f}" font-size="14" font-style="italic" fill="var(--muted)">none right</text>')
    # best-so-far step line in ink: starts at the first experiment with a candidate, steps down
    # when a later candidate beats it, runs flat otherwise; hollow dots never move it
    best = None
    path = []
    for i, r in enumerate(rows):
        v = r.get("best_loss")
        if v is None:
            continue
        if best is None:
            best = v; path.append((xs[i], y(best)))
        elif v < best:
            path.append((xs[i], y(best))); best = v; path.append((xs[i], y(best)))
    if path:
        path.append((xs[-1] + 12, y(best)))
        d = "M" + " L".join(f"{x:.1f},{yy:.1f}" for x, yy in path)
        g.append(f'<path d="{d}" fill="none" stroke="var(--ink)" stroke-width="1.6" stroke-linejoin="miter"/>')
    for i, r in enumerate(rows):
        v = r.get("best_loss")
        tip = f"{esc(r['tag'])}<br>{esc(r['title'])}<br>loss {'' if v is None else f'{v:.2f}'}; cribs {r['best_crib_hits']}/24 ({esc(words_str(r))})<br>{esc(r['decision'])}, {r['n_candidates']} candidates"
        href = f"/exp/{esc(r['tag'])}"
        if v is None:
            g.append(f'<a href="{href}"><circle cx="{xs[i]:.1f}" cy="{y(ymax):.1f}" r="5" fill="var(--paper)" stroke="var(--disc)" stroke-width="2" data-tip="{tip}"/></a>')
        else:
            fill = "var(--kept)" if r["decision"] == "kept" else "var(--disc)"
            g.append(f'<a href="{href}"><circle cx="{xs[i]:.1f}" cy="{y(v):.1f}" r="5" fill="{fill}" stroke="var(--paper)" stroke-width="2" data-tip="{tip}"/></a>')
    if best is not None:
        g.append(f'<text x="{xs[-1]+16:.1f}" y="{y(best)+5:.1f}" font-size="14" fill="var(--ink)">{best:.1f} best so far</text>')
    g.append(f'<text transform="translate(18,{T + plot_h/2:.1f}) rotate(-90)" text-anchor="middle" font-size="14" fill="var(--muted)">loss, points</text>')
    for i in range(n):
        if i == 0 or (i + 1) % 3 == 0 or i == n - 1:
            g.append(f'<text x="{xs[i]:.1f}" y="{H-8}" font-size="13" fill="var(--faint)" text-anchor="middle">{i + 1}</text>')
    g.append(f'<text x="{L-8}" y="{H-8}" font-size="13" fill="var(--faint)" text-anchor="end">experiment</text>')
    g.append("</svg>")
    return "<figure class='chart'>" + "".join(g) + "</figure>"


GL_JS = """<script>
(function(){
  var all=document.querySelectorAll('[data-gl]');
  all.forEach(function(el){
    el.addEventListener('mouseenter',function(){var id=el.getAttribute('data-gl');document.querySelectorAll('[data-gl="'+id+'"]').forEach(function(x){x.classList.add('on');});});
    el.addEventListener('mouseleave',function(){var id=el.getAttribute('data-gl');document.querySelectorAll('[data-gl="'+id+'"]').forEach(function(x){x.classList.remove('on');});});
  });
})();
</script>"""


def page(title, body, active="", refresh=True):
    meta = '<meta http-equiv="refresh" content="20">' if refresh else ""
    nav = "".join(f'<a href="{h}" class="{"on" if active == h else ""}">{t}</a>' for h, t in
                  (("/", "Overview"), ("/notebook", "Notebook"), ("/glossary", "Glossary"), ("/families", "Families"), ("/clues", "Clues"), ("/program", "Program")))
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{esc(title)}</title>{meta}
<meta name="viewport" content="width=device-width,initial-scale=1"><style>{CSS}</style></head><body>
<nav class="topnav"><span class="brand">Kryptos K4</span>{nav}</nav><div class="wrap">{body}</div>
<div class="foot"><span class="dot"></span>Rendered from the record. Refreshes every 20 seconds.</div>{JS}{GL_JS}</body></html>"""


def crib_strip():
    """97 cells; the 24 known positions in accent."""
    from kryptos.facts import KNOWN
    known = set(KNOWN)
    cw, gap = 9, 1.4
    W = 97 * (cw + gap)
    cells = "".join(
        f'<rect x="{(i-1)*(cw+gap):.1f}" y="0" width="{cw}" height="14" rx="1" fill="{'var(--accent)' if i in known else 'var(--rule-soft)'}"><title>position {i}{': ' + KNOWN[i] if i in known else ''}</title></rect>'
        for i in range(1, 98))
    return f'<svg viewBox="0 0 {W:.0f} 14" aria-label="the 24 known letters among the 97">{cells}</svg>'



# ---- the sculpture's four plates, line by line as carved --------------------------------------
UL_STARTS = ["EMUFPHZ", "YQTQUXQ", "VFPJUDE", "GGWHKK?", "TIMVMZJ", "QZGZLEC", "YIZETKZ", "HHDDDUV", "EVLDKFE", "FLGGTEZ", "FHQNTGP", "ELZZVRR", "DNQFMPN", "DQUMEBE"]
LL_STARTS = ["ENDYAHR", "CHTNREY", "TPRNGAT", "WMTWNDI", "TFOLSED", "EIFTBRS", "TEEFOAS", "BSEDDNI", "AECTDDH", "RKLMLEH", "ECDMRIP", "UOXOGHU", "TWTQSJQ", "VTTMZFP"]


def split_by_starts(text, starts):
    cuts = []
    pos = 0
    for st in starts:
        i = text.index(st, pos)
        cuts.append(i); pos = i + 1
    cuts.append(len(text))
    return [text[cuts[k]:cuts[k + 1]] for k in range(len(starts))]


def sculpture_panels():
    from kryptos.facts import load_k1, load_k2, load_k3, KRYPTOS_ALPHABET as KRY, STANDARD_ALPHABET as STD
    k4 = (ROOT / "data" / "k4.txt").read_text().strip()
    ul = split_by_starts(load_k1()["ciphertext"] + load_k2()["ciphertext_as_carved"], UL_STARTS)
    ll = split_by_starts(load_k3()["ciphertext"] + k4, LL_STARTS)
    rows = []
    for i in range(26):
        sh = KRY[i:] + KRY[:i]
        row = STD[i] + sh + sh[:4] + ("L" if STD[i] == "N" else "")
        rows.append(row)
    top = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCD"
    ur = [top] + rows[:13]
    lr = rows[13:] + [top]
    obkr = ll[10].index("OBKR")
    regions = [
        {"name": "K1", "quad": "ul", "spans": [[0, 0, 99], [1, 0, 99]], "caption": "K1, the first message: 63 letters, two lines. Solved: a keyed table with the word PALIMPSEST. Its text has the misspelling IQLUSION."},
        {"name": "K2", "quad": "ul", "spans": [[r, 0, 99] for r in range(2, 14)], "caption": "K2, the second message: 372 letters with three question marks. Solved: the same table with the word ABSCISSA. It ends with map coordinates and the words LAYER TWO."},
        {"name": "K3", "quad": "ll", "spans": [[r, 0, 99] for r in range(10)] + [[10, 0, obkr]], "caption": "K3, the third message: 337 letters. Solved: a grid scramble, no table. It retells Howard Carter opening Tutankhamun's tomb, down to the question mark after CAN YOU SEE ANYTHING."},
        {"name": "K4", "quad": "ll", "spans": [[10, obkr, 99], [11, 0, 99], [12, 0, 99], [13, 0, 99]], "caption": "K4, the fourth message: 97 letters from OBKR to the end, unsolved since 1990. The 24 known letters sit on the last three lines."},
        {"name": "the table", "quad": "ur", "spans": [[r, 0, 99] for r in range(14)], "caption": "The table: 26 rows of the alphabet, each starting one letter further along KRYPTOSABCDEFGHIJLMNQUVWXZ, with the plain alphabet down the left edge. K1 and K2 were enciphered on it."},
        {"name": "the table", "quad": "lr", "spans": [[r, 0, 99] for r in range(14)], "caption": "The table, lower half. Row N carries an extra L at its end, which makes the right-hand column read HILL over four rows."},
    ]
    return {"ul": ul, "ll": ll, "ur": ur, "lr": lr, "regions": regions}


def sculpture_block():
    data = json.dumps(sculpture_panels())
    keys = "".join(f'<span data-region="{esc(n)}">{esc(n)}</span>' for n in ("K1", "K2", "K3", "K4", "the table"))
    return (f'<div class="sculpture-wrap"><div id="sculpture"></div>'
            f'<div class="sculpture-foot"><div class="sculpture-key">{keys}</div><p id="sculpture-label" class="muted">Hover a plate to see which part of the puzzle it carries. Drag to turn.</p></div></div>'
            f'<script>window.KRYPTOS_PANELS = {data};</script>'
            '<script type="importmap">{"imports": {"three": "https://unpkg.com/three@0.160.0/build/three.module.js", "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"}}</script>'
            '<script type="module" src="/assets/sculpture.js"></script>')

def what_we_look_for():
    from kryptos.facts import KNOWN as _KNOWN, K4 as _K4
    panel = panel_block(_K4, None, _KNOWN)
    cols = [
        ("The 24 known letters", "Jim Sanborn has confirmed two stretches of the hidden message: EASTNORTHEAST at positions 22 to 34 and BERLINCLOCK at 64 to 74, underlined in the panel. They are the only hard facts about the message, and every experiment leans on them."),
        ("What the loss counts", "A candidate is a full 97-letter reading of the panel. It pays ten points for each known letter it gets wrong, then a little for how far the other 73 letters sit from English, then a charge for a secret word too long to remember. Zero would be solved."),
        ("The line at ten", "Above it, at least one known letter is wrong. Below it, all 24 are right and only the English of the rest and the length of the key remain. A dot below the line is not a solution until the text reads as English and the key is one a person could remember."),
    ]
    html = "".join(f'<div class="explain-col"><h4>{esc(h)}</h4><p>{esc(t)}</p></div>' for h, t in cols)
    return sculpture_block() + panel + f'<div class="explain-row">{html}</div>'


def sec(n, title, sub=""):
    return f'<div class="rsec"><span class="rsec-n">{n}</span><h2 class="rsec-t">{esc(title)}</h2></div>' + (f'<p class="rsec-sub">{esc(sub)}</p>' if sub else "")


def overview():
    rows = load_results()
    ch = champion()
    n = len(rows)
    kept = sum(1 for r in rows if r["decision"] == "kept")
    best_hits = max((r["best_crib_hits"] for r in rows), default=0)
    losses = [r["best_loss"] for r in rows if r.get("best_loss") is not None]
    best_loss = min(losses) if losses else None
    fams = len({r["family"] for r in rows})
    secs = sum(sum((r.get("phases") or {}).values()) or r["seconds"] for r in rows)
    by_phase = {}
    for r in rows:
        for k, v in (r.get("phases") or {"run": r["seconds"]}).items():
            by_phase[k] = by_phase.get(k, 0.0) + v
    hero = f"""<div class="stat-hero"><b class="num">{'' if best_loss is None else f'{best_loss:.1f}'}</b><span>best loss so far. zero is solved</span></div>
<p class="hero-sub">Ten per missed known letter (24 cribs: EASTNORTHEAST, BERLINCLOCK), plus how far the other 73 letters are from English, plus the cost of a key too long to remember. Below ten means every known letter is in place.</p>
<div class="stats">
<div class="stat"><b class="num">{n}</b><span>experiments</span></div>
<div class="stat"><b class="num">{kept}</b><span>kept</span></div>
<div class="stat"><b class="num">{best_hits}<span style="font-size:14px;font-weight:400;display:inline">/24</span></b><span>best crib hits</span></div>
<div class="stat"><b class="num">{fams}</b><span>families touched</span></div>
<div class="stat"><b class="num">{secs/3600:.1f}</b><span>hours, all phases</span></div>
</div>
<p class="hero-sub">Time by phase across the run: {', '.join(f"{k} {fmt_dur(v)}" for k, v in sorted(by_phase.items(), key=lambda kv: PHASE_ORDER.index(kv[0]) if kv[0] in PHASE_ORDER else 9) if v >= 1) or 'none yet'}.</p>"""
    if ch:
        from kryptos.facts import KNOWN as _KNOWN, K4 as _K4
        champ = f"""<div class="callout"><div class="callout-h">Champion: <a href="/exp/{esc(ch['experiment'])}">{esc(ch['experiment'])}</a></div>{panel_block(_K4, ch['plaintext'], _KNOWN)}<p class="muted" style="font-size:13px">{esc(ch['key_description'])}, fitness {ch['fitness']:.3f}. A champion is the best candidate that passed every gate; it is not a solution until its text reads as English and its key is memorable.</p></div>"""
    else:
        champ = '<div class="callout"><div class="callout-h">Champion</div><p>None yet. No candidate has passed all four gates.</p></div>'
    scale_max = max((sum((r.get("phases") or {"run": r["seconds"]}).values()) for r in rows), default=0)
    trs = "".join(
        f"""<tr><td class="num">{int(r['tag'][:4])}</td><td><a href="/exp/{esc(r['tag'])}">{esc(r['title'])}</a></td><td class="muted">{esc(r['family'])}</td>
<td class="{esc(r['decision'])}">{esc(r['decision'])}</td>
<td class="num">{'' if r.get('best_loss') is None else f"{r['best_loss']:.1f}"}</td>
<td class="num" title="{esc(words_str(r))}">{r['best_crib_hits']}/24</td>
<td class="num">{r['n_candidates']}</td><td class="num" title="{esc(', '.join(f'{k} {fmt_dur(v)}' for k, v in (r.get('phases') or {}).items()))}">{fmt_dur(sum((r.get('phases') or {}).values()) or r['seconds'])}</td><td>{phase_bar(r.get('phases') or {'run': r['seconds']}, scale_max)}</td></tr>"""
        for r in reversed(rows)
    )
    table = f"""<table><thead><tr><th class="num">id</th><th>title</th><th>family</th><th>decision</th><th class="num">loss</th><th class="num" title="known letters the best candidate got right, out of 24">crib letters</th><th class="num" title="full 97-letter decryptions the experiment handed to the gates">candidates</th><th class="num">time</th><th>by phase, scaled to the longest</th></tr></thead><tbody>{trs}</tbody></table>"""
    by_parent = {}
    for r in rows:
        by_parent.setdefault(r["parent"], []).append(r)

    def tree(parent):
        kids = by_parent.get(parent, [])
        if not kids:
            return ""
        return "<ul class='lineage'>" + "".join(
            f"<li><a href='/exp/{esc(k['tag'])}'>{esc(k['tag'])}</a> <span class='{esc(k['decision'])}'>{esc(k['decision'])}</span> "
            f"<span class='muted'>{esc(k['family'])}, loss {'' if k.get('best_loss') is None else f'{k['best_loss']:.1f}'}</span>{tree(k['tag'])}</li>" for k in kids) + "</ul>"

    body = ('<h1 class="home">Can a research loop find the method behind K4?</h1>'
            '<p class="psub">Ninety-seven letters on a copper screen at Langley, four clue words, and a definition of done that demands the method, not just the words.</p>'
            + hero + champ
            + sec(1, "What the loop is looking for", "The fourth message as the copper carries it, and the three things every experiment is measured against.")
            + what_we_look_for()
            + sec(2, "Loss over the run", "Each dot is one experiment's best candidate; a hollow dot means the search ruled everything out before producing one. The axis breaks at the line so the band where a solution would appear has room.")
            + loss_chart(rows)
            + sec(3, "Experiments", "Newest first. Crib letters: how many of the 24 known letters the best candidate got right. Candidates: full 97-letter decryptions the experiment handed to the gates; zero means the search ruled everything out before producing one. A bar marked unclocked shows run time only; its design and coding phases were not timed.")
            + table + f'<p class="hero-sub" style="text-align:left;max-width:none">Phase bar: {phase_legend()}</p>' 
            + sec(4, "Lineage", "What each experiment inherits from.")
            + (tree(None) or "<p class='muted'>empty</p>"))
    return page("Kryptos K4 autoresearch", body, "/")


def experiment_page(tag):
    import re as _re
    rows = {r["tag"]: r for r in load_results()}
    r = rows.get(tag)
    if not r:
        return page("not found", f"<p>No experiment {esc(tag)}</p>")
    from kryptos.facts import KNOWN, K4
    tags = list(rows)
    num = int(tag[:4])
    fam = r["family"]
    fam_label = fam.split("-", 1)[1].replace("-", " ") if "-" in fam else fam
    fam_num = fam.split("-", 1)[0]
    ph = r.get("phases") or {}
    total = sum(ph.values()) or r.get("seconds", 0)
    started = (r.get("started") or "")[:16].replace("T", " ")
    # pull the prose fields out of the record markdown
    def section(name):
        m = _re.search(r"## " + _re.escape(name) + r"\n\n(.+?)(?=\n\n## |\Z)", r["_md"], _re.S)
        return m.group(1).strip() if m else ""
    changed = ""
    m = _re.search(r"What changed: (.+?)(?=\n\n## )", r["_md"], _re.S)
    if m:
        changed = m.group(1).strip()
    parent = r.get("parent")
    parent_html = f'<a href="/exp/{esc(parent)}">experiment {int(parent[:4])}</a>' if parent and parent in rows else "a new root"
    decision = r["decision"]
    best = best_candidate(r)
    # header
    head = f"""<p class="crumb"><a href="/">Overview</a> / experiment {num}</p>
<div class="rec-head">
<p class="eyebrow">Experiment {num} &middot; family {esc(fam_num)}, {esc(fam_label)} &middot; <span class="{esc(decision)}">{esc(decision)}</span></p>
<h1 class="rec-title">{esc(r['title'])}</h1>
<p class="standfirst">{esc(changed)}</p>
<div class="meta-row">
<div><b>{parent_html}</b><span>builds on</span></div>
<div><b>{fmt_dur(total)}</b><span>time, all phases</span><div class="meta-bar">{phase_bar(ph if ph else {'run': r.get('seconds', 0)}, total or 1, width=190, height=8)}</div></div>
<div><b>{r['n_candidates']}</b><span>candidates</span></div>
<div><b>{r['best_crib_hits']}/24</b><span>known letters right</span></div>
<div><b>{'' if r.get('best_loss') is None else f"{r['best_loss']:.1f}"}</b><span>best loss</span></div>
</div></div>"""
    # section 1: plain words with the glossary rail
    eli5 = r.get("eli5") or ""
    low = eli5.lower()
    found = []   # (start, end, term_id, term, definition)
    for k, (term, names, definition) in enumerate(load_glossary()):
        best = None
        for n in names:
            m = _re.search(r"(?<![a-z])" + _re.escape(n.lower()) + r"(?![a-z])", low)
            if m and (best is None or m.start() < best[0]):
                best = (m.start(), m.end())
        if best:
            found.append((best[0], best[1], f"g{k}", term, definition))
    found.sort()
    kept, last_end = [], -1
    for f in found:
        if f[0] >= last_end:
            kept.append(f); last_end = f[1]
    kept = kept[:7]

    def first_sentence(d):
        m = _re.match(r"(.+?[.!?])(\s|$)", d)
        return m.group(1) if m else d
    # wrap the terms in the text
    out, pos = [], 0
    for st, en, gid, term, definition in kept:
        out.append(esc(eli5[pos:st]))
        out.append(f'<span class="gl" data-gl="{gid}" title="{esc(first_sentence(definition))}">{esc(eli5[st:en])}</span>')
        pos = en
    out.append(esc(eli5[pos:]))
    eli5_html = "<p>" + "".join(out).replace("\n\n", "</p><p>") + "</p>"
    rail = ""
    if kept:
        rail = '<aside class="aside"><h4>Words used here</h4>' + "".join(f'<p class="gl-entry" data-gl="{gid}"><b>{esc(term)}</b> {esc(first_sentence(definition))}</p>' for _, _, gid, term, definition in kept) + '<p class="faint">Full list on the <a href="/glossary">glossary</a> page.</p></aside>'
    plain = sec(1, "In plain words", "") + f'<div class="chart-row"><div class="plain">{eli5_html}</div>{rail}</div>'
    # section 2: best candidate
    cand = ""
    if best:
        how = "the harness's best by fitness among gate passers" if best.get("gate_passed") else "the candidate with most known letters right; none passed every gate"
        cand = sec(2, "Best candidate against the known letters", f"Laid out as the copper carries K4: OBKR ends the line that finishes K3, then three lines of 31. Left, as carved, with the 24 known positions underlined. Right, the candidate: a letter on a wash sits at a known position and matches, a red one sits there and misses. This is {how}.") + panel_block(K4, best["plaintext"], KNOWN)
    else:
        cand = sec(2, "Best candidate against the known letters", "This experiment produced no candidate: the search ruled everything out before a full text was built. Its product is the bounded negative in section 7.")
    # remaining sections from the record, numbered
    order = [("Walkthrough, by hand", "Walkthrough, by hand", "Redo the method on a few letters with pencil and paper."),
             ("Worked example (generated)", "Worked example, generated", "The same steps run by the code on the real letters."),
             ("Hypothesis (domain expert)", "Hypothesis, for a cryptanalyst", "Family, key space, the constraint under test, and the clues it reads."),
             ("Prediction", "Prediction", "Written before the run; the result decides it."),
             ("Method", "Method", ""),
             ("Result", "Result and bounds", "The harness's record: candidates, gates, loss, and the negative result this experiment leaves behind.")]
    body = [head, plain, cand]
    n = 3
    for key, title, sub in order:
        content = section(key)
        if not content:
            continue
        html_c = md(content)
        html_c = link_experiments(html_c, tags)
        body.append(sec(n, title, sub) + f'<article class="rec-body">{html_c}</article>')
        n += 1
    return page(f"experiment {num}", "".join(body))


def md_page(title, path, active, refresh=True):
    return page(title, "<article>" + md((ROOT / path).read_text()) + "</article>", active, refresh)


def route(path):
    if path in ("/", "/index.html"):
        return overview()
    if path.startswith("/exp/"):
        return experiment_page(path[5:].strip("/"))
    if path.startswith("/assets/"):
        f = ROOT / "assets" / path[len("/assets/"):]
        if f.exists() and f.suffix == ".js":
            return ("application/javascript", f.read_text())
    if path == "/glossary":
        return md_page("glossary", "GLOSSARY.md", "/glossary", refresh=False)
    if path == "/notebook":
        return md_page("lab notebook", "NOTEBOOK.md", "/notebook")
    if path == "/families":
        return md_page("families", "families.md", "/families")
    if path == "/clues":
        return md_page("clue register", "knowledge/11-clue-register.md", "/clues")
    if path == "/program":
        return md_page("program", "program.md", "/program", refresh=False)
    return None


class H(BaseHTTPRequestHandler):
    def do_GET(self):
        out = route(self.path.split("?")[0])
        if out is None:
            self.send_response(404); self.end_headers(); return
        ctype = "text/html; charset=utf-8"
        if isinstance(out, tuple):
            ctype, out = out
        data = out.encode()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *a):
        pass


def build():
    STATIC.mkdir(exist_ok=True)
    (STATIC / "index.html").write_text(overview())
    for r in load_results():
        (STATIC / f"{r['tag']}.html").write_text(experiment_page(r["tag"]))
    print(f"wrote {STATIC}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--port", type=int, default=8765)
    a = ap.parse_args()
    if a.build:
        build()
    else:
        print(f"dashboard at http://127.0.0.1:{a.port}")
        ThreadingHTTPServer(("127.0.0.1", a.port), H).serve_forever()
