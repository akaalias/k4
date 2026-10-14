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
article p,article li{max-width:720px}
figure.chart{margin:16px 0 0}figure.chart svg{width:100%;height:auto;display:block}
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


def phase_bar(ph, scale_max, width=160):
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
        parts.append(f'<rect x="{x:.1f}" y="0" width="{max(w-0.5,0.5):.1f}" height="10" fill="{PHASE_FILL[k]}"><title>{k}: {fmt_dur(v)}</title></rect>')
        x += w
    return f'<svg width="{width}" height="10" style="vertical-align:middle">{"".join(parts)}</svg>'


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
    W, H = 960, 320
    L, R, T, B = 56, 80, 20, 34
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
        g.append(f'<text x="{L-8}" y="{yy+4:.1f}" text-anchor="end" font-size="11.5" fill="var(--muted)">{v}</text>')
    # axis break marks just above the gate line
    bx = L - 2
    g.append(f'<path d="M{bx-5},{y_gate-10:.1f} l10,-5 M{bx-5},{y_gate-6:.1f} l10,-5" stroke="var(--muted)" stroke-width="1" fill="none"/>')
    # annotations at right, clear of the plot
    ax = W - R + 10
    g.append(f'<text x="{ax}" y="{y(gate)+4:.1f}" font-size="11.5" font-style="italic" fill="var(--accent)">crib gate</text>')
    g.append(f'<text x="{ax}" y="{y(0)+4:.1f}" font-size="11.5" font-style="italic" fill="var(--muted)">solved</text>')
    g.append(f'<text x="{ax}" y="{y(ymax)+4:.1f}" font-size="11.5" font-style="italic" fill="var(--muted)">no cribs</text>')
    pts, best = [], None
    for i, r in enumerate(rows):
        if r.get("decision") == "kept" and r.get("best_loss") is not None:
            best = r["best_loss"] if best is None else min(best, r["best_loss"])
        if best is not None:
            pts.append(f"{xs[i]:.1f},{y(best):.1f}")
    if len(pts) >= 2:
        g.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
    for i, r in enumerate(rows):
        v = r.get("best_loss")
        tip = f"{esc(r['tag'])}<br>{esc(r['title'])}<br>loss {'' if v is None else f'{v:.2f}'}; cribs {r['best_crib_hits']}/24 ({esc(words_str(r))})<br>{esc(r['decision'])}, {r['n_candidates']} candidates"
        href = f"/exp/{esc(r['tag'])}"
        if v is None:
            g.append(f'<a href="{href}"><circle cx="{xs[i]:.1f}" cy="{y(ymax):.1f}" r="5" fill="var(--paper)" stroke="var(--disc)" stroke-width="2" data-tip="{tip}"/></a>')
        else:
            fill = "var(--kept)" if r["decision"] == "kept" else "var(--disc)"
            g.append(f'<a href="{href}"><circle cx="{xs[i]:.1f}" cy="{y(v):.1f}" r="5" fill="{fill}" stroke="var(--paper)" stroke-width="2" data-tip="{tip}"/></a>')
    last = rows[-1]
    if last.get("best_loss") is not None:
        g.append(f'<text x="{xs[-1]+9:.1f}" y="{y(last["best_loss"])+4:.1f}" font-size="11.5" fill="var(--ink)">{last["best_loss"]:.1f}</text>')
    g.append(f'<text x="{L}" y="{H-8}" font-size="11.5" fill="var(--faint)">experiment 1</text>')
    g.append(f'<text x="{W-R}" y="{H-8}" font-size="11.5" fill="var(--faint)" text-anchor="end">experiment {n}</text>')
    g.append("</svg>")
    return "<figure class='chart'>" + "".join(g) + "</figure>"


def page(title, body, active="", refresh=True):
    meta = '<meta http-equiv="refresh" content="20">' if refresh else ""
    nav = "".join(f'<a href="{h}" class="{"on" if active == h else ""}">{t}</a>' for h, t in
                  (("/", "Overview"), ("/families", "Families"), ("/clues", "Clues"), ("/program", "Program")))
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{esc(title)}</title>{meta}
<meta name="viewport" content="width=device-width,initial-scale=1"><style>{CSS}</style></head><body>
<nav class="topnav"><span class="brand">Kryptos K4</span>{nav}</nav><div class="wrap">{body}</div>
<div class="foot"><span class="dot"></span>Rendered from the record. Refreshes every 20 seconds.</div>{JS}</body></html>"""


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
<p class="hero-sub">Ten per missed crib letter, plus how far the other 73 letters are from English, plus the cost of a key too long to remember. Below ten means every known letter is in place.</p>
<div class="stats">
<div class="stat"><b class="num">{n}</b><span>experiments</span></div>
<div class="stat"><b class="num">{kept}</b><span>kept</span></div>
<div class="stat"><b class="num">{best_hits}<span style="font-size:14px;font-weight:400;display:inline">/24</span></b><span>best crib hits</span></div>
<div class="stat"><b class="num">{fams}</b><span>families touched</span></div>
<div class="stat"><b class="num">{secs/3600:.1f}</b><span>hours, all phases</span></div>
</div>
<p class="hero-sub">Time by phase across the run: {', '.join(f"{k} {fmt_dur(v)}" for k, v in sorted(by_phase.items(), key=lambda kv: PHASE_ORDER.index(kv[0]) if kv[0] in PHASE_ORDER else 9)) or 'none yet'}.</p>"""
    if ch:
        champ = f"""<div class="callout"><div class="callout-h">Champion: {esc(ch['experiment'])}</div><p><code class="ct">{esc(ch['plaintext'])}</code></p><p class="muted" style="font-size:13px">{esc(ch['key_description'])}, fitness {ch['fitness']:.3f}</p></div>"""
    else:
        champ = '<div class="callout"><div class="callout-h">Champion</div><p>None yet. No candidate has passed all four gates.</p></div>'
    scale_max = max((sum((r.get("phases") or {"run": r["seconds"]}).values()) for r in rows), default=0)
    trs = "".join(
        f"""<tr><td><a href="/exp/{esc(r['tag'])}">{esc(r['tag'])}</a></td><td>{esc(r['title'])}</td><td class="muted">{esc(r['family'])}</td>
<td class="{esc(r['decision'])}">{esc(r['decision'])}</td>
<td class="num">{'' if r.get('best_loss') is None else f"{r['best_loss']:.1f}"}</td>
<td class="num" title="{esc(words_str(r))}">{r['best_crib_hits']}/24 <span class="faint">{esc(words_short(r))}</span></td>
<td class="num">{r['n_candidates']}</td><td class="num" title="{esc(', '.join(f'{k} {fmt_dur(v)}' for k, v in (r.get('phases') or {}).items()))}">{fmt_dur(sum((r.get('phases') or {}).values()) or r['seconds'])}</td><td>{phase_bar(r.get('phases') or {'run': r['seconds']}, scale_max)}</td></tr>"""
        for r in reversed(rows)
    )
    table = f"""<table><thead><tr><th>experiment</th><th>title</th><th>family</th><th>decision</th><th class="num">loss</th><th class="num" title="hits out of 24, then E N B C: capital = whole word in place, lower = partial">crib letters</th><th class="num">candidates</th><th class="num">time</th><th>by phase, scaled to the longest</th></tr></thead><tbody>{trs}</tbody></table>"""
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
            + sec(1, "Loss over the run", "Each dot is one experiment's best candidate; hollow dots returned no candidate. The axis breaks at the crib gate so the band below it, where a solution would appear, has room.")
            + loss_chart(rows)
            + sec(2, "Experiments", "Newest first. Crib letters: E N B C flags, a capital when a whole clue word is in place.")
            + table + f'<p class="hero-sub" style="text-align:left;max-width:none">Phase bar: {phase_legend()}</p>' 
            + sec(3, "Lineage", "What each experiment inherits from.")
            + (tree(None) or "<p class='muted'>empty</p>"))
    return page("Kryptos K4 autoresearch", body, "/")


def experiment_page(tag):
    rows = {r["tag"]: r for r in load_results()}
    r = rows.get(tag)
    if not r:
        return page("not found", f"<p>No experiment {esc(tag)}</p>")
    from kryptos.facts import KNOWN, K4
    cands = r.get("candidates", [])
    best = cands[0] if cands else None
    marked = ""
    if best:
        marked = f"""{sec("", "Best candidate against the cribs", "Highlighted letters sit at crib positions and match. Red letters sit at crib positions and miss. Ciphertext above for reference.")}
<pre><span class="ct faint">{esc(K4)}</span>
{k4_marked(best['plaintext'], KNOWN)}</pre>"""
    body = f"<p class='muted'><a href='/'>Overview</a> / {esc(tag)}</p>" + marked + "<article>" + md(r["_md"]) + "</article>"
    return page(tag, body)


def md_page(title, path, active, refresh=True):
    return page(title, "<article>" + md((ROOT / path).read_text()) + "</article>", active, refresh)


def route(path):
    if path in ("/", "/index.html"):
        return overview()
    if path.startswith("/exp/"):
        return experiment_page(path[5:].strip("/"))
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
        data = out.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
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
