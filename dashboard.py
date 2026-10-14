#!/usr/bin/env python3
"""Live dashboard, rendered from the experiment record on every request.

    uv run --with markdown python dashboard.py          # serves http://127.0.0.1:8765
    uv run --with markdown python dashboard.py --build  # writes static html to dashboard/

Nothing here is written by hand after the fact: every page is a view of
experiments/*/result.json, experiments/*/experiment.md, results.tsv,
champion.json and families.md.
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
except ImportError:  # fall back to preformatted text
    def md(text):
        return f"<pre>{html.escape(text)}</pre>"

ROOT = Path(__file__).resolve().parent
EXPERIMENTS = ROOT / "experiments"
STATIC = ROOT / "dashboard"

CSS = """
:root{--bg:#fafaf7;--fg:#1b1b1b;--muted:#6b6b6b;--line:#e3e1da;--kept:#1f7a4d;--rev:#9a3b3b;--acc:#2b5aa6;--card:#fff}
@media(prefers-color-scheme:dark){:root{--bg:#141414;--fg:#e8e6e1;--muted:#9a9a9a;--line:#2b2b2b;--kept:#5ec48f;--rev:#e07b7b;--acc:#7fa6e6;--card:#1c1c1c}}
*{box-sizing:border-box}body{margin:0;font:15px/1.5 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--fg)}
header{padding:14px 24px;border-bottom:1px solid var(--line);display:flex;gap:18px;align-items:baseline}
header a{color:var(--acc);text-decoration:none}header .t{font-weight:600;font-size:17px}header .m{color:var(--muted);font-size:13px;margin-left:auto}
main{max-width:1180px;margin:0 auto;padding:20px 24px}
h1{font-size:22px;margin:0 0 6px}h2{font-size:17px;margin:26px 0 8px}h3{font-size:15px;margin:18px 0 6px}
table{border-collapse:collapse;width:100%;font-size:14px}th,td{padding:6px 8px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
th{color:var(--muted);font-weight:500}td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
.kept{color:var(--kept);font-weight:600}.reverted{color:var(--rev)}.timeout,.error{color:var(--muted)}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin:12px 0 4px}
.card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px 14px}.card .k{color:var(--muted);font-size:12px}.card .v{font-size:22px;font-weight:600}
code,pre{font:13px/1.45 ui-monospace,SFMono-Regular,Menlo,monospace}pre{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:10px 12px;overflow:auto}
.ct{letter-spacing:.08em;word-break:break-all}.ct b{color:var(--kept)}.ct i{color:var(--rev);font-style:normal}
.lineage li{margin:2px 0}.muted{color:var(--muted)}
article h2{border-top:1px solid var(--line);padding-top:14px}
"""

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


def k4_marked(pt, known):
    """Plaintext with crib positions marked: green if right, red if wrong."""
    out = []
    for i, ch in enumerate(pt, start=1):
        if i in known:
            out.append(f"<b>{ch}</b>" if ch == known[i] else f"<i>{ch}</i>")
        else:
            out.append(ch)
    return f'<span class="ct">{"".join(out)}</span>'


def page(title, body, refresh=True):
    meta = '<meta http-equiv="refresh" content="20">' if refresh else ""
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{esc(title)}</title>{meta}
<meta name="viewport" content="width=device-width,initial-scale=1"><style>{CSS}</style></head><body>
<header><span class="t">Kryptos K4 autoresearch</span><a href="/">overview</a><a href="/families">families</a><a href="/program">program</a>
<span class="m">rendered from the record, refreshes every 20 s</span></header><main>{body}</main></body></html>"""


def overview():
    rows = load_results()
    ch = champion()
    n = len(rows)
    kept = sum(1 for r in rows if r["decision"] == "kept")
    best_hits = max((r["best_crib_hits"] for r in rows), default=0)
    fams = len({r["family"] for r in rows})
    secs = sum(r["seconds"] for r in rows)
    cards = f"""<div class="cards">
<div class="card"><div class="k">experiments</div><div class="v">{n}</div></div>
<div class="card"><div class="k">kept</div><div class="v">{kept}</div></div>
<div class="card"><div class="k">best crib hits</div><div class="v">{best_hits}<span class="muted" style="font-size:14px"> / 24</span></div></div>
<div class="card"><div class="k">families touched</div><div class="v">{fams}</div></div>
<div class="card"><div class="k">compute</div><div class="v">{secs/60:.0f}<span class="muted" style="font-size:14px"> min</span></div></div>
</div>"""
    if ch:
        champ = f"""<h2>Champion</h2><div class="card"><div class="k">{esc(ch['experiment'])}, fitness {ch['fitness']:.3f}</div>
<div><code>{esc(ch['plaintext'])}</code></div><div class="muted">{esc(ch['key_description'])}</div></div>"""
    else:
        champ = '<h2>Champion</h2><p class="muted">None yet. No candidate has passed all four gates.</p>'
    trs = "".join(
        f"""<tr><td><a href="/exp/{esc(r['tag'])}">{esc(r['tag'])}</a></td><td>{esc(r['title'])}</td><td>{esc(r['family'])}</td>
<td>{esc(r['parent'] or '-')}</td><td class="{esc(r['decision'])}">{esc(r['decision'])}</td>
<td class="num">{r['n_candidates']}</td><td class="num">{r['n_passed']}</td><td class="num">{r['best_crib_hits']}/24</td>
<td class="num">{'' if r['best_fitness'] is None else f"{r['best_fitness']:.3f}"}</td><td class="num">{r['seconds']:.0f}</td></tr>"""
        for r in reversed(rows)
    )
    table = f"""<h2>Experiments (newest first)</h2><table><thead><tr><th>id</th><th>title</th><th>family</th><th>parent</th><th>decision</th>
<th class="num">cands</th><th class="num">passed</th><th class="num">cribs</th><th class="num">fitness</th><th class="num">s</th></tr></thead><tbody>{trs}</tbody></table>"""
    # lineage as a tree
    by_parent = {}
    for r in rows:
        by_parent.setdefault(r["parent"], []).append(r)

    def tree(parent):
        kids = by_parent.get(parent, [])
        if not kids:
            return ""
        return "<ul class='lineage'>" + "".join(
            f"<li><a href='/exp/{esc(k['tag'])}'>{esc(k['tag'])}</a> <span class='{esc(k['decision'])}'>{esc(k['decision'])}</span> "
            f"<span class='muted'>{esc(k['family'])}, cribs {k['best_crib_hits']}/24</span>{tree(k['tag'])}</li>" for k in kids) + "</ul>"

    lineage = "<h2>Lineage</h2>" + (tree(None) or "<p class='muted'>empty</p>")
    return page("Kryptos K4 autoresearch", "<h1>Overview</h1>" + cards + champ + table + lineage)


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
        marked = f"""<h2>Best candidate against the cribs</h2>
<p class="muted">Green letters are crib positions that match; red are crib positions that miss. Ciphertext shown above for reference.</p>
<pre><span class="ct muted">{esc(K4)}</span>
{k4_marked(best['plaintext'], KNOWN)}</pre>"""
    body = f"<p class='muted'><a href='/'>overview</a> / {esc(tag)}</p>" + marked + "<article>" + md(r["_md"]) + "</article>"
    return page(tag, body)


def families_page():
    return page("families", "<article>" + md((ROOT / "families.md").read_text()) + "</article>")


def program_page():
    return page("program", "<article>" + md((ROOT / "program.md").read_text()) + "</article>", refresh=False)


def route(path):
    if path in ("/", "/index.html"):
        return overview()
    if path.startswith("/exp/"):
        return experiment_page(path[5:].strip("/"))
    if path == "/families":
        return families_page()
    if path == "/program":
        return program_page()
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

    def log_message(self, *a):  # quiet
        pass


def build():
    STATIC.mkdir(exist_ok=True)
    (STATIC / "index.html").write_text(overview().replace('href="/', 'href="'))
    (STATIC / "families.html").write_text(families_page())
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
