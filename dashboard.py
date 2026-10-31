#!/usr/bin/env python3
"""The project's dashboard, rendered from the experiment record on every request.

    uv run --with markdown python dashboard.py          # serves http://127.0.0.1:8765
    uv run --with markdown python dashboard.py --build  # writes static html to dashboard/

Nothing here is written by hand after the fact: every page is a view of
experiments/*/result.json, experiments/*/experiment.md, results.tsv,
champion.json, families.md and the clue register. Style follows STYLE.md.
"""
import argparse
import hashlib
import html
import json
import re
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

STARTED = int(time.time())

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
MODEL = ROOT / "assets" / "kryptos.glb"     # Bret L Bowen's model; local only, see .gitignore
EXPORT = {}                                  # set by export(): {"base": "/k4", "date": "..."} for the public site

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
.topnav{display:flex;gap:22px;align-items:baseline;flex-wrap:wrap;border-bottom:1px solid var(--rule);padding:18px 28px 12px;margin:0}
.topnav .spacer{flex:1 1 24px}
.topnav .sec{display:flex;gap:16px;align-items:baseline;flex-wrap:wrap}
.topnav .sec a{font-size:10.5px;letter-spacing:.08em;color:var(--faint)}
@media(max-width:640px){.topnav{gap:14px 18px;padding:14px 16px 10px}.topnav .spacer{flex-basis:100%;height:0}.topnav .sec{gap:14px}}
.topnav .brand{font:italic 14px var(--serif);color:var(--faint)}
.topnav a{font:600 12px var(--serif);font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.09em;color:var(--muted);border-bottom:2px solid transparent;padding-bottom:3px}
.topnav a.on,.topnav a:hover{color:var(--ink);border-bottom-color:var(--ink)}
.wrap{max-width:980px;margin:0 auto;padding:14px 28px 40px}
h1.home{font:italic 400 40px/1.15 var(--serif);text-align:center;margin:72px 0 10px;letter-spacing:-.01em}
@media(min-width:761px){h1.home{white-space:nowrap;font-size:clamp(26px,3.9vw,40px);width:96vw;position:relative;left:50%;transform:translateX(-50%)}}
.sec-lead{max-width:760px;font-size:17px;line-height:1.65;margin:4px 0 12px}
#sculpture .sc-credit{position:absolute;right:12px;bottom:10px;z-index:2;font:italic 12.5px var(--serif);color:var(--muted);background:color-mix(in srgb,var(--paper) 78%,transparent);padding:3px 8px;border-radius:3px;text-decoration:none}
#sculpture .sc-credit:hover{color:var(--accent)}
.learn-hero h1.home{white-space:normal!important;width:auto!important;position:static!important;left:auto!important;transform:none!important;max-width:980px;margin:96px auto 18px;font-size:40px;line-height:1.25}
.learn-hero p.psub{max-width:900px}
.learn-arrow{text-align:center;margin:34px 0 18px}
.hf-method.learn-soon{width:min(560px,100%);margin:0 auto 60px}
p.psub{text-align:center;font-style:italic;color:var(--muted);font-size:15.5px;line-height:1.7;margin:0 auto 8px;max-width:760px}p.psub.answer{font-size:32px;line-height:1.3;color:var(--ink);margin:44px auto 34px;max-width:none}@media(max-width:760px){p.psub.answer{font-size:22px;margin-top:28px}}
.hero-flow{width:96vw;position:relative;left:50%;transform:translateX(-50%);display:flex;align-items:center;justify-content:center;gap:12px;margin:22px 0 26px}
.hero-flow .lp-col{zoom:.74}
.hf-arrow{color:var(--muted);flex:none;padding-top:22px}
.hf-method{flex:none;width:250px;box-sizing:border-box;margin-top:22px;padding:30px 20px;border:2px dashed var(--accent);border-radius:8px;text-align:center}
.hf-method b{display:block;font:700 18px/1.3 var(--serif);color:var(--ink)}
.hf-method span{display:block;margin-top:8px;font:italic 14px/1.45 var(--serif);color:var(--muted)}
@media(max-width:1180px){.hero-flow{flex-direction:column;gap:6px}.hf-arrow{transform:rotate(90deg);padding:0}.hf-method{margin-top:0}.hero-flow .lp-col{zoom:.62}}
.stat-hero{max-width:560px;margin:30px auto 4px;text-align:center}
.stat-hero>b{display:block;font-size:56px;line-height:1.05;font-weight:600;color:var(--ink)}
.stat-hero>span{display:block;font:600 11px var(--serif);font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin-top:6px}
.hero-sub{max-width:560px;margin:12px auto 0;font-size:13px;line-height:1.6;color:var(--muted);text-align:center}
.stats{display:flex;flex-wrap:wrap;gap:18px 30px;justify-content:center;margin:22px auto 88px;text-align:center}
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
article blockquote{margin:14px 0 16px;padding:2px 0 2px 18px;border-left:3px solid var(--accent);max-width:700px}article blockquote p{font:italic 17px/1.55 var(--serif);color:var(--ink);margin:0}
article ol li strong,article ul li strong{font-weight:600}article li>ul,article li>ol{margin:6px 0 4px}
article p,article li{max-width:720px}article table{width:100%}article td{vertical-align:top;overflow-wrap:anywhere}article td code{white-space:normal;word-break:break-all;letter-spacing:.04em}article ol{padding-left:26px}article ol li{margin:0 0 8px}
.crumb{max-width:980px;margin:10px auto 0;color:var(--muted);font-size:14px}
.rec-head{max-width:980px;margin:18px auto 0}.eyebrow{font:600 11px var(--serif);font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);margin:0 0 10px}.eyebrow .kept{color:var(--accent)}
h1.rec-title{font:400 34px/1.18 var(--serif);margin:0 0 10px;letter-spacing:-.005em;max-width:900px}
.standfirst{font:italic 16.5px/1.6 var(--serif);color:var(--muted);margin:0 0 18px;max-width:820px}
.fc-1{--fc:#3d6b8c}.fc-2{--fc:#8a6a1e}.fc-3{--fc:#5b7f4a}.fc-4{--fc:#7a4f86}.fc-5{--fc:#b0603a}.fc-6{--fc:#2f7f7a}.fc-7{--fc:#9a5470}.fc-8{--fc:#5c5a8f}.fc-9{--fc:#7d7a3a}.fc-10{--fc:#6b6a60}.fc-11{--fc:#6b6a60}.fc-12{--fc:#6b6a60}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]) .fc-1{--fc:#7fa8c9}:root:not([data-theme=light]) .fc-2{--fc:#c9a227}:root:not([data-theme=light]) .fc-3{--fc:#8fb87a}:root:not([data-theme=light]) .fc-4{--fc:#b48cc0}:root:not([data-theme=light]) .fc-5{--fc:#e0936b}:root:not([data-theme=light]) .fc-6{--fc:#6cbfb8}:root:not([data-theme=light]) .fc-7{--fc:#d08aa6}:root:not([data-theme=light]) .fc-8{--fc:#9a98d0}:root:not([data-theme=light]) .fc-9{--fc:#bdb86a}:root:not([data-theme=light]) .fc-10{--fc:#a39f90}:root:not([data-theme=light]) .fc-11{--fc:#a39f90}:root:not([data-theme=light]) .fc-12{--fc:#a39f90}}
.famhead{font:600 11px/1.3 var(--serif);font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.06em;color:var(--fc)}
.famhead .sw{display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--fc);margin-right:6px;vertical-align:0}
.famhead .cnt{display:block;color:var(--faint);font-weight:400;margin-top:2px}
.xchip{display:inline-block;font:12px/1.2 var(--serif);font-variant-numeric:lining-nums tabular-nums;color:var(--fc,var(--muted));border:1px solid color-mix(in srgb,var(--fc,var(--muted)) 40%,transparent);border-radius:3px;padding:1px 4px;margin:0 3px 3px 0;text-decoration:none}
.xchip:hover{background:var(--fc,var(--muted));color:var(--paper)}
.lin-legend{display:flex;flex-wrap:wrap;gap:8px 22px;font-size:13px;color:var(--muted);margin:6px 0 4px}
.lin-legend .k{display:inline-flex;align-items:center;gap:7px;white-space:nowrap}
.lin-legend .ldot{width:9px;height:9px;border-radius:50%;display:inline-block;background:currentColor}
.lin-legend .lkept{width:11px;height:11px;background:var(--ink)}
.lin-legend .lwas{width:13px;height:13px;border-radius:50%;border:1.3px dashed var(--ink);display:inline-block}
.lin-legend .lerr{color:var(--accent);font:700 14px/1 var(--serif)}
.lin-legend .larc{width:8px;height:16px;border-right:1.2px solid var(--muted);border-radius:0 9px 9px 0;display:inline-block}
.lin-legend .lx{width:0;height:16px;border-left:1.2px dashed var(--muted);display:inline-block;margin:0 4px}
.ph{max-width:980px;margin:0 auto 40px}.ph h1{font:400 34px/1.18 var(--serif);margin:18px 0 10px;letter-spacing:-.005em}.ph .standfirst{max-width:760px}
.ph .standfirst{margin-bottom:0}.ph-meta{margin-top:56px}
.ph h1 .exp-q{font-style:italic}
.ph .facts{font-size:14.5px;color:var(--muted);margin:0 0 12px;max-width:820px}
.ph-legend{display:flex;flex-wrap:wrap;gap:8px 22px;font-size:13px;color:var(--muted);margin:6px 0 14px}.ph-legend>span{display:inline-flex;align-items:center;gap:7px}
.pf{max-width:980px;margin:34px auto 0;padding-top:10px;border-top:1px solid var(--rule-soft);font-size:13.5px;color:var(--muted)}
@media(max-width:640px){.ph h1{font-size:26px}}
.meta-time{line-height:0;margin:2px 0 22px}.meta-time svg{width:100%;height:8px}.meta-time .faint{display:block;line-height:1.4;margin-top:6px}
.meta-row{display:grid;grid-template-columns:repeat(5,1fr);gap:0 24px;padding:14px 0 12px;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule-soft)}.meta-row>div{display:flex;flex-direction:column}.meta-bar{margin-top:7px}.meta-bar svg rect{cursor:help}.meta-bar .faint{display:block;margin-top:3px}.meta-row b{font-weight:600;font-size:14.5px;line-height:1.3}.meta-row span{font:600 10px var(--serif);font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin-top:2px}
.plain p{font-size:17px;line-height:1.7;margin:0 0 12px;max-width:640px}
.gl{border-bottom:1px dotted var(--accent);cursor:help;transition:background .15s}.gl.on,.gl:hover{background:var(--hl)}.gl-entry{border-left:2px solid transparent;padding-left:6px;margin-left:-8px;transition:background .15s}.gl-entry.on,.gl-entry:hover{background:var(--hl);border-left-color:var(--accent)}.aside p{margin:0 0 9px;font-size:13px;line-height:1.5}.aside p b{color:var(--ink);font-weight:600}.aside h4{margin-bottom:8px}.aside .faint{font-size:12px}
.rec-body{max-width:980px}.rec-body h3{font:600 12px var(--serif);font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin:22px 0 6px}.rec-body p,.rec-body li{max-width:720px;font-size:15.5px;line-height:1.6}
.sculpture-wrap{max-width:980px;margin:14px auto 22px}#sculpture{width:90vw;position:relative;left:50%;transform:translateX(-50%);border:1px solid var(--rule-soft);border-radius:2px;overflow:hidden;cursor:grab}#sculpture canvas{display:block}.sculpture-foot{display:flex;gap:22px;align-items:baseline;margin-top:8px}.sculpture-key span{font:600 11px var(--serif);font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);margin-right:14px;cursor:pointer;border-bottom:2px solid transparent}.sculpture-key span.on{color:var(--accent);border-bottom-color:var(--accent)}#sculpture-label{margin:0;font-size:13.5px;flex:1}
.explain-row{display:grid;grid-template-columns:1fr 1fr 1fr;gap:34px;max-width:980px;margin:22px auto 0}.explain-row.cols-2{grid-template-columns:1fr 1fr}.explain-row.cols-4{grid-template-columns:repeat(4,1fr);gap:28px;margin-top:40px}.explain-col h4 a{color:inherit;text-decoration:none}.explain-col h4 a:hover{text-decoration:underline}.explain-col h4{font:600 11px var(--serif);font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.1em;color:var(--accent);margin:0 0 8px}.explain-col p{font-size:15.5px;line-height:1.65;margin:0;color:var(--ink)}
@media(max-width:860px){.explain-row,.explain-row.cols-2,.explain-row.cols-4{grid-template-columns:1fr}}
dl.bd{display:grid;grid-template-columns:minmax(150px,max-content) 1fr;gap:6px 18px;margin:6px 0 10px;font-size:14.5px}dl.bd dt{color:var(--muted)}dl.bd dd{margin:0;min-width:0;overflow-wrap:anywhere}dl.bd dl.bd{grid-template-columns:minmax(70px,max-content) 1fr;margin:0;padding-left:12px;border-left:2px solid var(--rule-soft);font-size:13.5px}.bd-text{font:12.5px var(--mono);letter-spacing:.06em;overflow-wrap:anywhere}ol.bd-list{margin:0;padding-left:20px}
.ktabs{display:flex;gap:6px;margin:4px 0 2px}.ktab{font:600 12px var(--serif);letter-spacing:.1em;padding:5px 14px;border:1px solid var(--rule);background:var(--paper);color:var(--muted);border-radius:3px;cursor:pointer}.ktab.on{background:var(--accent);border-color:var(--accent);color:var(--paper)}.kpane-notes{display:grid;grid-template-columns:1fr 1fr;gap:28px;max-width:980px;margin:4px auto 0;font-size:15px;color:var(--ink)}.kpane-notes p{margin:0}.lrow.start{justify-content:flex-start}.inl{display:inline-flex;align-items:flex-end;gap:1px;white-space:nowrap;height:.78em;line-height:1;vertical-align:-0.06em}.inl .lc{width:1.22em;height:1.42em;font-size:.56em;border-radius:2px}.lp-note{width:573px;box-sizing:border-box;font-size:15px;line-height:1.5;margin:10px 0 0;padding:0 2px}.lc.q,.lc.ink.q{color:var(--accent);font-weight:700}
.fig-row{clear:both;width:min(1640px,98vw);margin-top:30px!important;position:relative;left:50%;transform:translateX(-50%);margin:26px 0 8px}.fig-main{margin:0}.fig-scroll{overflow-x:auto;padding-bottom:6px}.fig-main svg{display:block;margin:0 auto;max-width:none}.fig-eyebrow{font:600 11px var(--serif);font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);margin:0 0 6px}.fig-notes{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:24px;max-width:980px;margin:14px auto 0}.fig-note{margin:0}.fig-note b{display:block;font:600 11px var(--serif);font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.08em;color:var(--accent);margin:0 0 3px}.fig-note p{margin:0;font-size:14px;line-height:1.5;color:var(--muted)}
.plain.tufte{position:relative;display:flow-root}.plain.tufte p{max-width:620px}.sidenote{float:right;clear:right;margin-right:-300px;width:270px;margin-top:.35em;margin-bottom:.9em;font-size:13.5px;line-height:1.45;color:var(--muted);padding-left:12px;border-left:1px solid var(--rule)}.sidenote b{color:var(--ink);font-weight:600}.sidenote-more{max-width:620px;font-size:13px;color:var(--faint);margin:4px 0 0}@media(max-width:980px){.sidenote{float:none;display:block;margin:6px 0 10px;width:auto;max-width:620px}}
.word{display:flex;gap:1.5px;border-radius:3px;box-shadow:0 0 0 1px #cfc8ae}
.verdict-note{max-width:760px;margin:10px 0 0;padding:8px 12px;border-left:3px solid var(--accent);background:var(--wash);font-size:14.5px}
.how{width:min(1200px,94vw);position:relative;left:50%;transform:translateX(-50%);margin:22px 0 6px;padding-top:14px;border-top:1px solid var(--rule-soft)}.how-grid{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:40px;align-items:start}.how-steps{margin:0;padding-left:20px;font-size:15.5px;line-height:1.55;max-width:560px}.how-steps li{margin:0 0 8px}.how-figure{background:var(--wash);border:1px solid var(--rule);border-radius:7px;padding:12px 14px}.how-row{display:flex;align-items:center;gap:10px;margin:0 0 4px}.how-label{width:150px;text-align:right;font:italic 12.5px var(--serif);color:var(--muted)}.lc.keyc{background:#8a6d1f;color:var(--paper);font-weight:700}.lc.num{font-size:10px;background:transparent;color:var(--muted)}.how-figure.k3 .lc{width:26px}.how-worked{font-size:14px;color:var(--muted);margin:8px 0 0;max-width:520px}
.res-notes{font-size:16px;margin:16px 0 6px;max-width:760px}.res-notes.err{color:var(--accent)}.res-stats{display:flex;gap:44px;flex-wrap:wrap;margin:6px 0 18px;padding:14px 0;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)}.res-stats div{display:flex;flex-direction:column}.res-stats b{font:400 24px var(--serif)}.res-stats span{font:600 11px var(--serif);font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.1em;color:var(--muted)}.res-card{display:flex;gap:26px;align-items:flex-start;padding:16px 0;border-bottom:1px solid var(--rule-soft)}.res-side{display:flex;flex-direction:column;gap:3px;min-width:150px;font-size:14px;color:var(--muted)}.res-rank{font:400 26px var(--serif);color:var(--ink)}.res-loss{color:var(--accent);font-weight:600}.res-main{flex:1;min-width:0}.res-main .lp-box{display:inline-block}.res-key{font-size:13.5px;color:var(--muted);margin:8px 0 0;overflow-wrap:anywhere;max-width:620px}
table.score{width:100%;max-width:760px;margin:10px 0 6px;border-collapse:collapse}table.score td,table.score th{padding:7px 10px;border-bottom:1px solid var(--rule-soft);font-size:15px}table.score td:first-child{font-weight:600}table.score tr.total td{border-top:1.5px solid var(--ink);border-bottom:none;font-weight:700}table.score .pct{color:var(--accent);margin-left:8px}table.score.ranks td:first-child{font-weight:400}table.score.ranks tr.kept td{font-weight:700;color:var(--accent)}table.score.ranks tr.gap td{color:var(--faint);border-bottom:none}.score-sub{font-size:14px;color:var(--muted);margin:16px 0 4px;max-width:760px}
.panel-wrap{display:flex;gap:18px;justify-content:center;align-items:flex-start;flex-wrap:nowrap;margin:16px 0 8px}.panel-wrap.wide{width:min(1360px,96vw);max-width:none;position:relative;left:50%;transform:translateX(-50%)}.callout.wide{width:min(1400px,96vw);max-width:none;position:relative;left:50%;transform:translateX(-50%);box-sizing:border-box}.callout .panel-wrap.wide{width:auto;left:0;transform:none}#sculpture-label{min-height:3.2em}.subsec{display:flex;align-items:baseline;gap:12px;margin:34px 0 10px;padding-top:12px;border-top:1px solid var(--rule-soft)}.subsec b{font:400 15px var(--serif);color:var(--faint)}.subsec h3{font:400 21px var(--serif);margin:0}.subsec-sub{font-style:italic;color:var(--muted);font-size:15px;margin:0 0 6px}.lp-col{display:flex;flex-direction:column}.lp-eyebrow{font:600 11px/1.2 var(--serif)!important;font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);margin:0 0 6px}.lp-box{background:var(--wash);border:1px solid var(--rule);border-radius:7px;padding:10px 14px 12px;width:573px;box-sizing:border-box}.lp.mini .lp-box{width:auto}.lp-title{font:600 13px var(--serif);color:var(--muted);text-align:center;margin:0 0 8px}.lrow{display:flex;gap:1.5px;margin:0 0 2.5px;justify-content:flex-start}.lc{display:inline-flex;align-items:center;justify-content:center;width:15px;height:19px;border-radius:2.5px;background:#ebe7d8;color:var(--muted);font:normal 11.5px/1 var(--mono)}.lc.tail{background:#f1eee3;color:#cfcab8}.lc.known{background:var(--accent);color:var(--paper);font-weight:700}.lc.miss{background:var(--paper);color:var(--accent);box-shadow:inset 0 0 0 1.3px var(--accent);font-weight:700}.lc.ink{color:var(--ink)}.lc.dot:after{content:"";width:2px;height:2px;border-radius:50%;background:var(--faint,#9b998c)}.lp-cap{font:italic 13px/1.4 var(--serif);color:var(--muted);text-align:center;margin:6px 0 0}.lp-cap.acc{color:var(--accent);margin-top:2px}.lp-arrow{color:var(--muted);padding-top:72px}.lp.mini .lp-box{padding:5px 6px;border-radius:4px;background:transparent;border-color:var(--rule-soft)}.lp.mini .lp-title{display:none}.lp.mini .lc{width:6.5px;height:9px;font-size:6px;border-radius:1px}.lp.mini .lrow{gap:1px;margin-bottom:1px}
.gloss{margin:6px 0 28px;padding:10px 0 0;border-top:1px solid var(--rule-soft)}.gloss .callout-h{color:var(--muted)}.gloss dl{margin:0;columns:2;column-gap:32px}.gloss .entry{break-inside:avoid;-webkit-column-break-inside:avoid;page-break-inside:avoid;display:inline-block;width:100%;margin:0 0 8px}.gloss dt{font-weight:600;font-size:13.5px}.gloss dd{margin:1px 0 0 0;color:var(--muted);font-size:13px;line-height:1.5}.gloss p{margin:8px 0 0}
.cta{display:block;max-width:640px;margin:34px auto 10px;padding:18px 22px;border:1px solid var(--rule);border-left:3px solid var(--accent);background:var(--wash);text-decoration:none;color:var(--ink)}.cta:hover{background:var(--hl)}.xtable{width:90vw;position:relative;left:50%;transform:translateX(-50%);margin-top:22px}.xtable td.num,.xtable td:nth-child(3){white-space:nowrap}.xtable table{border-collapse:separate;border-spacing:0}.xtable tr.pivot-row td{border-top:1.2px dotted color-mix(in srgb,var(--accent) 55%,transparent);border-bottom:1.2px dotted color-mix(in srgb,var(--accent) 55%,transparent);text-align:right;padding:5px 9px}.xtable tr.pivot-row a{color:var(--accent);font:italic 400 14px var(--serif);text-decoration:none}.xtable tr.pivot-row svg{margin-left:8px;vertical-align:1px}@media(max-width:760px){.xtable{width:calc(100vw - 32px);overflow-x:auto}}.cta-k{display:block;font:600 11px var(--serif);text-transform:uppercase;letter-spacing:.1em;color:var(--muted)}.cta-h{display:block;font-size:22px;margin:4px 0 4px;color:var(--accent)}.cta-s{display:block;font-size:15px;color:var(--muted)}
.chart-wide{width:90vw;position:relative;left:50%;transform:translateX(-50%);margin:10px 0 6px}.chart-eyebrow{font:600 11px var(--serif);font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);margin:0 0 6px;padding-top:10px;border-top:1px solid var(--rule)}.chart-legend{display:flex;flex-wrap:wrap;gap:8px 26px;font-size:13px;color:var(--muted);margin:6px 0 0}.chart-legend span{white-space:nowrap}.mk{display:inline-block;width:11px;height:11px;border-radius:50%;vertical-align:-1px;margin-right:6px}.mk-kept{background:var(--ink)}.mk-disc{background:var(--disc)}.mk-none{background:var(--paper);border:2px solid var(--disc);width:8px;height:8px}.mk-err{background:none;border-radius:0;position:relative;width:11px;height:11px}.mk-err:before,.mk-err:after{content:'';position:absolute;left:5px;top:-1px;width:2px;height:13px;background:var(--accent)}.mk-err:before{transform:rotate(45deg)}.mk-err:after{transform:rotate(-45deg)}.mk-line{border-radius:0;height:2px;width:18px;background:var(--ink);vertical-align:3px}
figure.chart{margin:16px 0 0}figure.chart svg{width:100%;height:auto;display:block}
.chart-row{display:grid;grid-template-columns:minmax(0,1fr) 250px;gap:28px;align-items:start;margin-top:8px}
.aside{font-size:13.5px;line-height:1.5;color:var(--muted);border-left:1px solid var(--rule);padding-left:16px;margin-top:16px}
.aside h4{font:600 10.5px var(--serif);font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin:0 0 6px}
.aside p{margin:0 0 10px}.aside svg{display:block;width:100%;height:auto;margin:4px 0 10px}
@media(max-width:860px){.chart-row{grid-template-columns:1fr}.aside{border-left:0;padding-left:0}}
figure.chart svg text{paint-order:stroke;stroke:var(--paper);stroke-width:2.8px;stroke-linejoin:round;font-family:var(--serif)}
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


# records cannot be edited after their run, so spelling variants of a family slug are merged here
FAMILY_ALIASES = {"8-hill-and-polygraphic": "8-hill-polygraphic", "2-masked-then-keyed": "2-masked-plaintext", "5-gromark": "5-gromark-lfsr", "4-visual-systems": "4-visual-spatial", "6-matrix-transposition-then-tableau": "6-transposition-then-tableau"}


def rescore(r):
    """Recompute every candidate's loss under the current rules (key charged by the length of its
    description, counted by the harness), so every page shows one number. The record's own figure
    is kept as loss_recorded."""
    from kryptos.scorer import loss as _loss, key_bits_of
    best = None
    for c in r.get("candidates", []):
        if c.get("loss") is None or not c.get("plaintext"):
            continue
        c.setdefault("loss_recorded", c["loss"])
        bits = key_bits_of(c.get("key"))
        c["key_bits"] = bits
        c["loss"] = _loss(c["plaintext"], bits, c.get("crib_hits", 0))
        best = c["loss"] if best is None else min(best, c["loss"])
    if best is not None:
        r["best_loss_recorded"] = r.get("best_loss")
        r["best_loss"] = best


def confirmed():
    """Experiments Alexis and Claude have checked together (data/confirmed.json, issue #95). On the public
    site a kept result or a champion shows only once it is listed here."""
    p = ROOT / "data" / "confirmed.json"
    return {c["experiment"] for c in json.loads(p.read_text()).get("confirmed", [])} if p.exists() else set()


HELD = "Held back on the public site until it has been checked together (issue #95)."


def replay():
    """Current verdicts from tools/replay_rules.py: {tag: {...}} (records keep their own decision)."""
    p = ROOT / "data" / "replay.json"
    return json.loads(p.read_text()).get("experiments", {}) if p.exists() else {}


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
            r["family"] = FAMILY_ALIASES.get(m.group(1).strip(), m.group(1).strip()) if m else "?"
            m = re.search(r"\*\*Parent:\*\* (.+?)  ", r["_md"])
            p = m.group(1).strip() if m else "none"
            r["parent"] = None if p.startswith("none") else p
            m = re.search(r"^# \S+: (.+)$", r["_md"], re.M)
            r["title"] = m.group(1).strip() if m else r["tag"]
            m = re.search(r"## In plain words\n\n(.+?)\n\n## ", r["_md"], re.S)
            r["eli5"] = m.group(1).strip() if m else ""
            rescore(r)
            v = replay().get(r["tag"])
            r["decision_recorded"] = r.get("decision")
            if v and v["verdict_now"] != r.get("decision") and r.get("decision") in ("kept", "reverted"):
                r["decision"] = v["verdict_now"]
                r["verdict_note"] = v["reason"]
            if EXPORT and r.get("decision") == "kept" and r["tag"] not in confirmed():
                r["decision"], r["verdict_note"] = "awaiting review", HELD
            rows.append(r)
    return rows


def champion():
    p = ROOT / "champion.json"
    ch = json.loads(p.read_text()) if p.exists() else None
    if ch and EXPORT and ch.get("experiment") not in confirmed():
        return None          # the public site announces a champion only once confirmed (issue #95)
    return ch


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


_READABLE = {"mtime": None, "data": {}}


def readable_words(text):
    """Readable-word spans [[start, end, word], ...] (0-based) for a 97-letter reading, from
    data/readable_words.json, which the harness fills after every run (tools/readable_words.py)."""
    p = ROOT / "data" / "readable_words.json"
    if not p.exists():
        return []
    m = p.stat().st_mtime
    if _READABLE["mtime"] != m:
        _READABLE["data"] = json.loads(p.read_text()); _READABLE["mtime"] = m
    return (_READABLE["data"].get(text) or {}).get("words", [])


def letter_panel(text, known, mode, title, captions=()):
    """Every panel box is 33 cells wide, the longest line on the copper (K3's ninth), so all panels match.
    One panel in the house letter-cell style, laid out as the copper carries K4: the K3 tail
    (faint) and OBKR on the first line, then three lines of 31.
    mode 'carved': every carved letter in a wash cell, the 24 known places in accent cells.
    mode 'reading': unknown places as dots, the 24 known letters in accent cells.
    mode 'candidate': every letter in a cell; a known place that matches is an accent cell, one
    that misses is outlined in accent."""
    rows = []
    offset = 0
    word_of = {}
    if mode == "candidate" and text:
        for n, (a, b, _w) in enumerate(readable_words(text)):
            for q in range(a, b):
                word_of[q + 1] = n            # 1-based place -> word number
    for k, chunk in enumerate(panel_lines(text if text else "?" * 97)):
        cells = []
        if k == 0:
            cells += [f'<i class="lc tail">{esc(c)}</i>' for c in K3_TAIL]
        for j, ch in enumerate(chunk):
            i = offset + j + 1
            if mode == "carved":
                cells.append(f'<i class="lc known">{esc(ch)}</i>' if i in known else f'<i class="lc">{esc(ch)}</i>')
            elif mode == "reading":
                cells.append(f'<i class="lc known">{esc(known[i])}</i>' if i in known else '<i class="lc dot"></i>')
            else:
                if i in known:
                    cells.append(f'<i class="lc known">{esc(ch)}</i>' if ch == known[i] else f'<i class="lc miss" title="should be {esc(known[i])}">{esc(ch)}</i>')
                else:
                    cells.append(f'<i class="lc ink">{esc(ch)}</i>')
        if word_of:
            # box the readable words: group this line's cells by word, as in the K1-K3 panels
            tail_n = len(K3_TAIL) if k == 0 else 0
            grouped, run, cur = cells[:tail_n], [], None
            for j, cell in enumerate(cells[tail_n:]):
                w = word_of.get(offset + j + 1)
                if run and w != cur:
                    grouped.append(f'<span class="word">{"".join(run)}</span>' if cur is not None else "".join(run)); run = []
                run.append(cell); cur = w
            if run:
                grouped.append(f'<span class="word">{"".join(run)}</span>' if cur is not None else "".join(run))
            cells = grouped
        rows.append(f'<div class="lrow">{"".join(cells)}</div>')
        offset += len(chunk)
    caps = "".join(f'<p class="lp-cap{" acc" if c.startswith("scored") else ""}">{esc(c)}</p>' for c in captions)
    return f'<div class="lp"><div class="lp-box"><div class="lp-title">{esc(title)}</div>{"".join(rows)}</div>{caps}</div>'


def panel_block(ct, pt, known, in_caption=True):
    """IN: the copper as carved; OUT: a reading of the same 97 places, either the empty reading
    (the known letters where they must land) or a candidate."""
    left = ('<div class="lp-col"><p class="lp-eyebrow">in: the copper, always the same</p>'
            + letter_panel(ct, known, "carved", "as carved, 97 letters; the 24 known places in accent",
                           ("OBKR ends the line that finishes K3, then three lines of 31",) if in_caption else ()) + '</div>')
    if pt:
        right = ('<div class="lp-col"><p class="lp-eyebrow">out: the candidate</p>'
                 + letter_panel(pt, known, "candidate", "every place read; known places in accent, misses outlined",
                                ("checked: the known letters in place, and the reading turns back into the copper",)) + '</div>')
    else:
        right = ('<div class="lp-col"><p class="lp-eyebrow">out: a reading of the same 97 places</p>'
                 + letter_panel(None, known, "reading", "the 24 known letters must land here; the rest is read",
                                ("checked: the known letters in place, and the reading turns back into the copper", "scored: the loss, zero is solved")) + '</div>')
    arrow = '<div class="lp-arrow"><svg width="34" height="14" viewBox="0 0 34 14"><path d="M1,7 L28,7" stroke="currentColor" stroke-width="1.4"/><path d="M26,2 L33,7 L26,12 z" fill="currentColor"/></svg></div>'
    return f'<div class="panel-wrap wide">{left}{arrow}{right}</div>'


def hero_flow():
    """Above the overview's question: the carved K4, the method still to be found, the cleartext
    it must give. The panels are panel_block's; the placeholder is the illustrations' dashed box."""
    from kryptos.facts import KNOWN as _KNOWN, K4 as _K4
    left = ('<div class="lp-col"><p class="lp-eyebrow">The Kryptos K4 ciphertext message</p>'
            + letter_panel(_K4, _KNOWN, "carved", "as carved, 97 letters; the 24 known places in accent") + "</div>")
    right = ('<div class="lp-col"><p class="lp-eyebrow">The fully decrypted cleartext message</p>'
             + letter_panel(None, _KNOWN, "reading", "the 24 known letters must land here; the rest is read") + "</div>")
    arrow = '<div class="hf-arrow"><svg width="34" height="14" viewBox="0 0 34 14"><path d="M1,7 L28,7" stroke="currentColor" stroke-width="1.4"/><path d="M26,2 L33,7 L26,12 z" fill="currentColor"/></svg></div>'
    method = ('<div class="hf-method"><b>the method goes here</b>'
              '<span>one experiment, one way of turning the left into the right</span></div>')
    return f'<div class="hero-flow">{left}{arrow}{method}{arrow}{right}</div>'


def mini_panel(pt, known):
    """A small candidate panel for tables: the three lines of 31 plus OBKR's line, letters in cells."""
    return letter_panel(pt, known, "candidate", "").replace('<div class="lp">', '<div class="lp mini">', 1)


WORST = 240.0   # the loss with all 24 known letters wrong


def pct(v):
    return "" if v is None else f"{100.0 * v / WORST:.1f}%"


def best_candidate(r):
    """The candidate the harness ranked best among gate passers: lowest loss since the rule changed
    at experiment 0050, highest fitness before (experiments 0001-0049). Else most crib hits."""
    cands = r.get("candidates", [])
    if not cands:
        return None
    passed = [c for c in cands if c.get("gate_passed")]
    if passed:
        # the current rule everywhere: lowest loss (records before experiment 50 were kept by
        # fitness; their own decision is shown as history, not used to pick the candidate here)
        return min(passed, key=lambda c: c.get("loss") if c.get("loss") is not None else 1e9)
    return max(cands, key=lambda c: c.get("crib_hits", 0))


def row_loss(r):
    """What a row is marked at: the kept candidate's loss for a kept experiment, else its best."""
    kl = kept_loss(r)
    return kl if kl is not None else r.get("best_loss")


def kept_loss(r):
    """The loss of the candidate that became champion, for a kept experiment."""
    b = best_candidate(r) if r.get("decision") == "kept" else None
    return b.get("loss") if b else None


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
    by_num = {str(int(k)): v for k, v in by_id.items()}

    def link(num):
        tag = by_num.get(str(int(num)))
        return f'<a href="/exp/{tag}">{num}</a>' if tag else num

    out = _re.sub(r"(?<![\w/-])(\d{4})(?![\w-])", lambda m: link(m.group(1)) if m.group(1) in by_id else m.group(1), html_text)
    # "experiment 34", "Experiments 34 and 35", "experiments 6, 12 and 15": link every number in the phrase
    phrase = _re.compile(r"(?i)(?<![\w/-])(experiments?\s+)(\d{1,3}(?:\s*,\s*\d{1,3})*(?:\s+(?:and|to)\s+\d{1,3})?)(?![\w-])")
    return phrase.sub(lambda m: m.group(1) + _re.sub(r"\d{1,3}", lambda n: link(n.group(0)) if "<a" not in n.group(0) else n.group(0), m.group(2)), out)


def k4_marked(pt, known):
    out = []
    for i, ch in enumerate(pt, start=1):
        if i in known:
            out.append(f"<b>{ch}</b>" if ch == known[i] else f"<i>{ch}</i>")
        else:
            out.append(ch)
    return f'<span class="ct">{"".join(out)}</span>'


def loss_chart(rows, bare=False):
    """Loss per experiment, 0 at the bottom. The axis breaks at 10, the crib gate: the band
    0-10 gets 40% of the height, 10-240 the rest. Kept: ink dot, champion line in accent.
    Reverted: recessive grey dot. No valid candidate: hollow dot at the top."""
    if not rows:
        return "<p class='muted'>No experiments yet.</p>"
    W, H = 1400, 440
    L, R, T, B = 110, 150, 58, 44
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
    # bands: one per working day, from the run start stamps
    days = []
    for i, r in enumerate(rows):
        d = (r.get("started") or "")[:10]
        if not days or days[-1][0] != d:
            days.append([d, i, i])
        else:
            days[-1][2] = i
    half = (xs[1] - xs[0]) / 2 if n > 1 else 10
    for k, (d, i0, i1) in enumerate(days):
        x0, x1 = xs[i0] - half, xs[i1] + half
        g.append(f'<rect x="{x0:.1f}" y="{T}" width="{x1 - x0:.1f}" height="{plot_h}" fill="{"var(--wash)" if k % 2 == 0 else "var(--paper)"}"/>')
        if k > 0:
            g.append(f'<line x1="{x0:.1f}" x2="{x0:.1f}" y1="{T}" y2="{T + plot_h}" stroke="var(--rule)" stroke-width="1"/>')
        g.append(f'<text x="{x0 + 6:.1f}" y="{T - 10}" font-size="14" font-weight="600" fill="var(--muted)">day {k + 1} &middot; {i1 - i0 + 1} experiments</text>')
    for v in (0, 5, 10, 60, 120, 180, 240):
        yy = y(v)
        if v == gate:
            g.append(f'<line x1="{L}" x2="{W-R}" y1="{yy:.1f}" y2="{yy:.1f}" stroke="var(--accent)" stroke-width="1.5"/>')
        else:
            g.append(f'<line x1="{L}" x2="{W-R}" y1="{yy:.1f}" y2="{yy:.1f}" stroke="var(--rule-soft)" stroke-width="1"/>')
        lab = f"{100.0 * v / ymax:.0f}%" if v >= 10 else f"{100.0 * v / ymax:.0f}%"
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
        v = kept_loss(r)
        if v is None:
            continue
        if best is None:
            best = v; path.append((xs[i], y(best)))
        else:
            path.append((xs[i], y(best))); best = v; path.append((xs[i], y(best)))
    if path:
        path.append((xs[-1] + 12, y(best)))
        r_ = 6.0
        d = f"M{path[0][0]:.1f},{path[0][1]:.1f}"
        for k in range(1, len(path)):
            x0, y0 = path[k - 1]; x1, y1 = path[k]
            if k < len(path) - 1:
                x2, y2 = path[k + 1]
                # approach the corner, stop r_ short, bend with a quadratic through the corner
                if x1 != x0:
                    d += f" L{x1 - min(r_, abs(x1 - x0)) * (1 if x1 > x0 else -1):.1f},{y1:.1f}"
                    d += f" Q{x1:.1f},{y1:.1f} {x1:.1f},{y1 + min(r_, abs(y2 - y1)) * (1 if y2 > y1 else -1):.1f}"
                else:
                    d += f" L{x1:.1f},{y1 - min(r_, abs(y1 - y0)) * (1 if y1 > y0 else -1):.1f}"
                    d += f" Q{x1:.1f},{y1:.1f} {x1 + min(r_, abs(x2 - x1)) * (1 if x2 > x1 else -1):.1f},{y1:.1f}"
            else:
                d += f" L{x1:.1f},{y1:.1f}"
        g.append(f'<path d="{d}" fill="none" stroke="var(--ink)" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"/>')
    for i, r in enumerate(rows):
        v = r.get("best_loss")
        kl = kept_loss(r)
        if kl is not None:
            v = kl                      # a kept experiment is marked at the loss of the candidate it kept
        tip = f"{esc(r['tag'])}<br>{esc(r['title'])}<br>loss {pct(v)} of the worst possible ({'' if v is None else f'{v:.2f}'}); cribs {r['best_crib_hits']}/24 ({esc(words_str(r))})<br>{esc(r['decision'])}, {r['n_candidates']} candidates"
        href = f"/exp/{esc(r['tag'])}"
        dec = r.get("decision")
        if dec in ("error", "timeout"):
            cx, cy = xs[i], y(ymax)
            g.append(f'<a href="{href}"><path d="M{cx-4:.1f},{cy-4:.1f} L{cx+4:.1f},{cy+4:.1f} M{cx-4:.1f},{cy+4:.1f} L{cx+4:.1f},{cy-4:.1f}" stroke="var(--accent)" stroke-width="2" fill="none" data-tip="{tip}"/></a>')
        elif v is None:
            g.append(f'<a href="{href}" class="fc-{esc(fam_num(r))}"><circle cx="{xs[i]:.1f}" cy="{y(ymax):.1f}" r="5" fill="var(--paper)" stroke="var(--disc)" stroke-width="2" data-tip="{tip}"/></a>')
        else:
            fill = "var(--ink)" if dec == "kept" else "var(--disc)"
            g.append(f'<a href="{href}" class="fc-{esc(fam_num(r))}"><circle cx="{xs[i]:.1f}" cy="{y(v):.1f}" r="5.5" fill="{fill}" stroke="var(--paper)" stroke-width="2" data-tip="{tip}"/></a>')
    if best is not None:
        g.append(f'<text x="{xs[-1]+16:.1f}" y="{y(best)+5:.1f}" font-size="14" fill="var(--ink)">{100.0 * best / ymax:.1f}% the champion</text>')
    g.append(f'<text transform="translate(18,{T + plot_h/2:.1f}) rotate(-90)" text-anchor="middle" font-size="14" fill="var(--muted)">loss, as % of the worst possible</text>')
    for i in range(n):
        if i == 0 or (i + 1) % 3 == 0 or i == n - 1:
            g.append(f'<text x="{xs[i]:.1f}" y="{H-8}" font-size="13" fill="var(--faint)" text-anchor="middle">{i + 1}</text>')
    g.append(f'<text x="{L-8}" y="{H-8}" font-size="13" fill="var(--faint)" text-anchor="end">experiment</text>')
    g.append("</svg>")
    legend = ('<div class="chart-legend">'
              '<span><i class="mk mk-kept"></i>kept: passed every gate and beat the champion; marked at the loss of the candidate it kept</span>'
              '<span><i class="mk mk-disc"></i>reverted, with a candidate</span>'
              '<span><i class="mk mk-none"></i>reverted, no candidate: ruled out before one was built</span>'
              '<span><i class="mk mk-err"></i>errored</span>'
              '<span><i class="mk mk-line"></i>the champion\'s loss; it moves only when an experiment is kept</span></div>')
    eyebrow = f'<p class="chart-eyebrow">Loss per experiment, all {n} of them &middot; share of the worst possible, 24 known letters wrong &middot; lower is better</p>'
    if bare:
        return "<div class='chart-wide' style='padding-top:14px'><figure class='chart'>" + "".join(g) + "</figure></div>"
    return "<div class='chart-wide'>" + eyebrow + "<figure class='chart'>" + "".join(g) + "</figure>" + legend + "</div>"


def load_grades():
    """{id: grade row} from grades.tsv: outcome, strength, cribs_forced, space, note (issue #29)."""
    p = ROOT / "grades.tsv"
    out = {}
    if p.exists():
        lines = p.read_text().splitlines()
        head = lines[0].split("\t")
        for ln in lines[1:]:
            f = ln.split("\t")
            if len(f) == len(head):
                out[f[0]] = dict(zip(head, f))
    return out


FINDING_ROWS = [
    ("beat-chance", "beat the scrambled copies"),
    ("chance", "at chance"),
    ("ruled-out", "ruled out"),
    ("other", "no comparison run"),
]
FAMILY_PALETTE = ["#3d6b8c", "#8a6a1e", "#5b7f4a", "#7a4f86", "#b0603a", "#2f7f7a", "#9a5470", "#5c5a8f", "#7d7a3a", "#6b6a60"]
FAMILY_PALETTE_DARK = ["#7fa8c9", "#c9a227", "#8fb87a", "#b48cc0", "#e0936b", "#6cbfb8", "#d08aa6", "#9a98d0", "#bdb86a", "#a39f90"]


def findings_chart(rows):
    """What each experiment found, against chance: one dot per experiment in run order, in the row
    of its outcome (grades.tsv). Colour is the family, shape the strength of the test, a ring marks
    readings whose known letters were fitted by the method itself."""
    if not rows:
        return "<p class='muted'>No experiments yet.</p>"
    grades = load_grades()
    W, L, R, T, B, band = 1400, 40, 250, 26, 40, 62
    H = T + band * len(FINDING_ROWS) + B
    n = len(rows)
    xs = [L + (i + 0.5) * (W - L - R) / n for i in range(n)]
    row_of = {k: j for j, (k, _) in enumerate(FINDING_ROWS)}
    keys = sorted({r["family"].split("-", 1)[0] for r in rows}, key=lambda k: (not k.isdigit(), int(k) if k.isdigit() else 0, k))
    # a family's colour follows its number, as .fc-N does; families past the ninth share the neutral last slot
    fam_ix = {k: min(int(k) - 1, len(FAMILY_PALETTE) - 1) if k.isdigit() else len(FAMILY_PALETTE) - 1 for k in keys}
    short = {}
    for r in rows:
        num, _, rest = r["family"].partition("-")
        short.setdefault(num, f"{num} {rest.replace('-', ' ')}" if rest else num)
    style = "<style>.fc{" + ";".join(f"--fc{i}:{c}" for i, c in enumerate(FAMILY_PALETTE)) + "}" \
            "@media(prefers-color-scheme:dark){:root:not([data-theme=light]) .fc{" + ";".join(f"--fc{i}:{c}" for i, c in enumerate(FAMILY_PALETTE_DARK)) + "}}" \
            ":root[data-theme=dark] .fc{" + ";".join(f"--fc{i}:{c}" for i, c in enumerate(FAMILY_PALETTE_DARK)) + "}" \
            ".fc .chart-legend span{white-space:normal}.fc .mk-fam{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:-1px}</style>"
    g = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="What each experiment found, against scrambled copies of K4">']
    counts = {k: 0 for k, _ in FINDING_ROWS}
    for j, (k, label) in enumerate(FINDING_ROWS):
        y0 = T + j * band
        if j % 2 == 0:
            g.append(f'<rect x="{L}" y="{y0}" width="{W - L - R}" height="{band}" fill="var(--wash)"/>')
        g.append(f'<line x1="{L}" x2="{W - R}" y1="{y0 + band / 2:.1f}" y2="{y0 + band / 2:.1f}" stroke="var(--rule-soft)" stroke-width="1"/>')
    placed = []
    for i, r in enumerate(rows):
        gr = grades.get(r["tag"][:4], {})
        oc = gr.get("outcome", "")
        k = oc if oc in row_of else "other"
        counts[k] += 1
        cy = T + row_of[k] * band + band / 2
        c = f"var(--fc{fam_ix[r['family'].split('-', 1)[0]] % 10})"
        st = gr.get("strength", "")
        tip = (f"{esc(r['tag'])}<br>{esc(r['title'])}<br><b>{esc(oc or 'not graded')}</b>, {esc(st or '-')} test"
               f"{'; known letters fitted by the method' if gr.get('cribs_forced') == 'yes' else ''}<br>{esc(gr.get('note', ''))}")
        href = f"/exp/{esc(r['tag'])}"
        if st == "exact":
            shape = f'<circle cx="{xs[i]:.1f}" cy="{cy:.1f}" r="5" fill="{c}" stroke="var(--paper)" stroke-width="1.5"/>'
        elif st == "sampled":
            shape = f'<circle cx="{xs[i]:.1f}" cy="{cy:.1f}" r="4.2" fill="var(--paper)" stroke="{c}" stroke-width="2.2"/>'
        else:
            shape = f'<circle cx="{xs[i]:.1f}" cy="{cy:.1f}" r="4.2" fill="var(--paper)" stroke="{c}" stroke-width="1.4" stroke-dasharray="2 2"/>'
        ring = (f'<circle cx="{xs[i]:.1f}" cy="{cy:.1f}" r="8.5" fill="none" stroke="var(--ink)" stroke-width="1"/>'
                if gr.get("cribs_forced") == "yes" else "")
        placed.append(f'<a href="{href}"><g data-tip="{tip}">{ring}{shape}<rect x="{xs[i] - 6:.1f}" y="{cy - 10:.1f}" width="12" height="20" fill="transparent"/></g></a>')
    g += placed
    for j, (k, label) in enumerate(FINDING_ROWS):
        cy = T + j * band + band / 2
        col = "var(--accent)" if k == "beat-chance" else "var(--ink)"
        g.append(f'<text x="{W - R + 14}" y="{cy - 2:.1f}" font-size="15" fill="{col}">{label}</text>')
        g.append(f'<text x="{W - R + 14}" y="{cy + 16:.1f}" font-size="13" fill="var(--muted)">{counts[k]} experiment{"" if counts[k] == 1 else "s"}</text>')
    for i in range(n):
        if i == 0 or (i + 1) % 5 == 0 or i == n - 1:
            g.append(f'<text x="{xs[i]:.1f}" y="{H - 14}" font-size="13" fill="var(--faint)" text-anchor="middle">{i + 1}</text>')
    g.append("</svg>")
    fam_legend = "".join(
        f'<span><i class="mk-fam" style="background:var(--fc{i % 10})"></i>{esc(short[k])}</span>'
        for k, i in fam_ix.items())
    legend = ('<div class="chart-legend">'
              '<span><svg width="14" height="14" style="vertical-align:-2px;margin-right:6px"><circle cx="7" cy="7" r="5" fill="var(--muted)"/></svg>exact: the whole space was enumerated or solved</span>'
              '<span><svg width="14" height="14" style="vertical-align:-2px;margin-right:6px"><circle cx="7" cy="7" r="4.2" fill="var(--paper)" stroke="var(--muted)" stroke-width="2.2"/></svg>sampled: a sample or a heuristic search</span>'
              '<span><svg width="14" height="14" style="vertical-align:-2px;margin-right:6px"><circle cx="7" cy="7" r="4.2" fill="var(--paper)" stroke="var(--muted)" stroke-width="1.4" stroke-dasharray="2 2"/></svg>weak: too little power to decide</span>'
              '<span><svg width="20" height="20" style="vertical-align:-5px;margin-right:6px"><circle cx="10" cy="10" r="8.5" fill="none" stroke="var(--ink)"/><circle cx="10" cy="10" r="4" fill="var(--muted)"/></svg>ring: the method fitted its key to the known letters, so hitting them proves nothing</span>'
              '</div><div class="chart-legend">' + fam_legend + '</div>')
    eyebrow = (f'<p class="chart-eyebrow">What each of the {n} experiments found, judged against scrambled copies of K4 &middot; '
               'in run order &middot; graded in grades.tsv</p>')
    expl = ('<p class="hero-sub">Every experiment runs the same search on scrambled copies of the carved text. A result counts only if K4 '
            'does better than all of them. <b>Ruled out</b>: no setting in the searched space fits the 24 known letters. '
            '<b>At chance</b>: settings or readings exist, but scrambled copies produce them just as well. '
            '<b>Beat the scrambled copies</b>: the one entry, 0056, is a property of the carved text (doubled letters lining up in '
            'columns of 7, repeats 21 apart), not a reading of it. No decryption has beaten chance.</p>')
    return style + "<div class='chart-wide fc'>" + eyebrow + "<figure class='chart'>" + "".join(g) + "</figure>" + legend + expl + "</div>"


GL_JS = """<script>
(function(){
  var all=document.querySelectorAll('[data-gl]');
  all.forEach(function(el){
    el.addEventListener('mouseenter',function(){var id=el.getAttribute('data-gl');document.querySelectorAll('[data-gl="'+id+'"]').forEach(function(x){x.classList.add('on');});});
    el.addEventListener('mouseleave',function(){var id=el.getAttribute('data-gl');document.querySelectorAll('[data-gl="'+id+'"]').forEach(function(x){x.classList.remove('on');});});
  });
})();
</script>"""


def page_head(eyebrow, title, standfirst, facts="", extra=""):
    """The header every page but the overview shares, after the lineage page: eyebrow, title,
    italic standfirst, a line of facts from the record, and an optional key."""
    meta = (f'<p class="facts">{facts}</p>' if facts else "") + extra
    return (f'<header class="ph"><p class="eyebrow">{eyebrow}</p><h1>{title}</h1>'
            f'<p class="standfirst">{standfirst}</p>' + (f'<div class="ph-meta">{meta}</div>' if meta else "") + "</header>")


def page_foot(html_text):
    return f'<p class="pf">{html_text}</p>'


SITE = "https://alexisrondeau.me/k4"
REPO = "https://github.com/akaalias/k4"
# the corner ribbon every autoresearch site at alexisrondeau.me carries, as airloom has it
GH_RIBBON = ('<style>#gh-ribbon{position:fixed;right:-56px;bottom:36px;z-index:80;transform:rotate(-45deg);background:#111111;color:#fffff8;font:600 11px "Palatino","Palatino Linotype","Book Antiqua",Georgia,serif;font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.12em;white-space:nowrap;padding:7px 64px;text-decoration:none;border:none;outline:1px solid rgba(255,255,248,.4);outline-offset:-4px;box-shadow:0 1px 8px rgba(0,0,0,.3)}#gh-ribbon:hover{background:#8c2f1f;color:#fffff8}@media(max-width:600px){#gh-ribbon{right:-50px;bottom:24px;font-size:9px;letter-spacing:.09em;padding:5px 44px}}</style>'
             f'<a id="gh-ribbon" href="{REPO}" target="_blank" rel="noopener">view on GitHub</a>')


def ways_that_dont_work():
    """Experiments graded ruled-out (no setting gives the known letters) or chance (no better than
    the scrambled copies); tools/publish.py counts the same for the repository's description."""
    return sum(1 for g in load_grades().values() if g.get("outcome") in ("ruled-out", "chance"))


def social_tags():
    """Open Graph and Twitter card tags for the public site, as the other autoresearch sites have them; the
    title stays under 60 characters and the description under 125, so previews do not cut them."""
    title = "Can an AI research loop find the secret of Kryptos K4?"
    desc = f"Not solved yet, but {ways_that_dont_work()} ways that don't work, each on the record: an AI agent's cipher experiments on K4."
    # the version stamp changes with the card, so previews that cache by URL fetch a redrawn one
    v = hashlib.md5((ROOT / "assets" / "share.png").read_bytes()).hexdigest()[:8]
    img, alt = f"{SITE}/share.png?v={v}","K4's 97 carved letters, the 24 known places in red, each carried by a curve to where one ruled-out route puts it."
    t = lambda k, v, a="property": f'<meta {a}="{k}" content="{esc(v)}">'
    return "".join([t("description", desc, "name"), t("og:type", "website"), t("og:site_name", "Kryptos K4 autoresearch"),
                    t("og:title", title), t("og:description", desc), t("og:url", f"{SITE}/"), t("og:image", img),
                    t("og:image:width", "1200"), t("og:image:height", "630"), t("og:image:alt", alt),
                    t("twitter:card", "summary_large_image", "name"), t("twitter:title", title, "name"),
                    t("twitter:description", desc, "name"), t("twitter:image", img, "name")])


# the reference pages behind the nav's one Reference link (issue #71): path, name, what it holds
REFERENCE = {
    "/record": ("Full record", "What each family has covered: every bound the search has set, with the experiments behind it."),
    "/notebook": ("Notebook", "What was decided, run, found and left open, day by day, newest first."),
    "/clues": ("Clues", "Every hint about K4 and its readings; experiments cite them by number."),
    "/assumptions": ("Assumptions", "What the project takes for granted, and what each assumption rests on."),
    "/glossary": ("Glossary", "The words the pages use, each in one plain sentence."),
    "/program": ("Program", "The instructions the loop agent follows on every experiment."),
    "/controls": ("Controls", "Each closed item rerun on a planted message: did its own search find the plant? Live as the loop runs."),
}


def reference_page():
    cols = "".join(f'<div class="explain-col"><h4><a href="{h}">{esc(n)}</a></h4><p>{esc(d)}</p></div>' for h, (n, d) in REFERENCE.items())
    head = page_head("Reference", "The record behind the pages", "The full record, the notebook, the hints and assumptions the search starts from, the glossary and the loop's instructions.")
    return page("reference", head + f'<div class="explain-row" style="row-gap:34px;margin:28px 0 0">{cols}</div>', "/reference", False)


def controls_page():
    """Stage 2's positive controls (assumption A3, issue #73), straight from controls.tsv as each one lands."""
    import csv
    f = ROOT / "controls.tsv"
    rows = list(csv.DictReader(f.open(), delimiter="\t")) if f.exists() else []
    planned = len(re.findall(r"^\| C-", (ROOT / "order-of-work.md").read_text(), re.M))
    tags = {r["tag"][:4]: r["tag"] for r in load_results()}
    npass = sum(r["passed"] == "yes" for r in rows)
    nfail = len(rows) - npass
    trs = "".join(
        f'<tr><td>{esc(r["id"])}</td><td>{esc(r["item"])}</td>'
        f'<td class="num"><a href="/exp/{esc(tags.get(r["experiment"], r["experiment"]))}">{int(r["experiment"]) if r["experiment"].isdigit() else esc(r["experiment"])}</a></td>'
        f'<td style="color:var({"--ink" if r["passed"] == "yes" else "--accent"});font-weight:600">{"passed" if r["passed"] == "yes" else "FAILED"}</td>'
        f'<td class="num">{esc(r["seconds"])} s</td><td>{esc(r["what"])}</td><td class="muted">{esc(r["why"])}</td></tr>'
        for r in rows)
    head = page_head("Controls", "Does each search find a planted answer?",
                     "A closed item rests on a search that found nothing on K4. Each control plants a message made with the item's own "
                     "method and a key inside its space, reruns the closing experiment unchanged on it, and requires the plant to be found. "
                     "A failure reopens the item.",
                     f"{len(rows)} of {planned} controls run: {npass} passed, {nfail} failed. The page reloads as each one lands.")
    table = ('<div class="xtable"><table><thead><tr><th>control</th><th>item</th><th class="num">experiment</th><th>result</th>'
             f'<th class="num">time</th><th>what was planted</th><th>what the search returned</th></tr></thead><tbody>{trs}</tbody></table></div>')
    foot = page_foot('The queue and its rules are on the <a href="/priorities">priorities</a> page; the reason for stage 2 is assumption A3 on the <a href="/assumptions">assumptions</a> page.')
    return page("controls", head + table + foot, "/controls", True)


def page(title, body, active="", refresh=True):
    # reload only when the record changes: poll a version stamp so the 3D model and a reader's
    # place on the page survive quiet periods
    refresh = refresh and not EXPORT
    meta = '<script>(function(){var v=null;setInterval(function(){fetch("/version").then(function(r){return r.text()}).then(function(t){if(v===null)v=t;else if(t!==v)location.reload();});},10000);})();</script>' if refresh else ""
    link = lambda h, t: f'<a href="{h}" class="{"on" if active == h else ""}">{t}</a>'
    nav = ("".join(link(h, t) for h, t in (("/", "Project Overview"), ("/experiments", "Experiments"), ("/lineage", "Lineage"), ("/learnings", "Learnings")))
           + '<span class="spacer"></span><span class="sec">'
           + "".join(link(h, t) for h, t in (("/families", "Families"), ("/priorities", "Priorities"), ("/keys", "Keys"), ("/dead-ends", "Dead Ends"), ("/pivots", "Pivots")))
           + f'<a href="/reference" class="{"on" if active == "/reference" or active in REFERENCE else ""}">Reference</a>'
           + "</span>")
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{esc(title)}</title>{meta}{social_tags() if EXPORT else ""}
<meta name="viewport" content="width=device-width,initial-scale=1"><style>{CSS}</style></head><body>
<nav class="topnav"><span class="brand">Kryptos K4</span>{nav}</nav><div class="wrap">{body}</div>
<div class="foot"><span class="dot"></span>{f"Rendered from the record on {EXPORT['date']}; updated after every experiment." if EXPORT else "Rendered from the record. Reloads when a new experiment lands."}</div>{JS}{GL_JS}{GH_RIBBON if EXPORT else ""}</body></html>"""


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
    return (f'<div class="sculpture-wrap"><div id="sculpture"><a class="sc-credit" href="https://www.youtube.com/@K4HasGotMe" target="_blank" rel="noopener">Model: Bret L Bowen (K4HasGotMe on YouTube)</a></div>'
            f'<div class="sculpture-foot"><div class="sculpture-key">{keys}</div><p id="sculpture-label" class="muted">Hover a plate to see which part of the puzzle it carries. Drag to turn; right-drag or shift-drag to move the view.</p></div></div>'
            f'<script>window.KRYPTOS_PANELS = {data};</script>'
            '<script type="importmap">{"imports": {"three": "https://unpkg.com/three@0.160.0/build/three.module.js", "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"}}</script>'
            '<script type="module" src="/assets/sculpture.js"></script>')

# K1-K3 solutions with word breaks, for the word boxes; each joins back to the record's text exactly
SPACED = {
    "K1": "BETWEEN SUBTLE SHADING AND THE ABSENCE OF LIGHT LIES THE NUANCE OF IQLUSION",
    "K2": "IT WAS TOTALLY INVISIBLE HOWS THAT POSSIBLE ? THEY USED THE EARTHS MAGNETIC FIELD X THE INFORMATION WAS GATHERED AND TRANSMITTED UNDERGRUUND TO AN UNKNOWN LOCATION X DOES LANGLEY KNOW ABOUT THIS ? THEY SHOULD ITS BURIED OUT THERE SOMEWHERE X WHO KNOWS THE EXACT LOCATION ? ONLY WW THIS WAS HIS LAST MESSAGE X THIRTY EIGHT DEGREES FIFTY SEVEN MINUTES SIX POINT FIVE SECONDS NORTH SEVENTY SEVEN DEGREES EIGHT MINUTES FORTY FOUR SECONDS WEST ID BY ROWS",
    "K3": "SLOWLY DESPARATLY SLOWLY THE REMAINS OF PASSAGE DEBRIS THAT ENCUMBERED THE LOWER PART OF THE DOORWAY WAS REMOVED WITH TREMBLING HANDS I MADE A TINY BREACH IN THE UPPER LEFT HAND CORNER AND THEN WIDENING THE HOLE A LITTLE I INSERTED THE CANDLE AND PEERED IN THE HOT AIR ESCAPING FROM THE CHAMBER CAUSED THE FLAME TO FLICKER BUT PRESENTLY DETAILS OF THE ROOM WITHIN EMERGED FROM THE MIST X CAN YOU SEE ANYTHING Q ?",
}


def how_solved_html(name):
    """How K1, K2 or K3 was solved: short steps, and the first letters worked by hand."""
    from kryptos.facts import load_k1, load_k2, load_k3, KRYPTOS_ALPHABET as KRY
    from kryptos.ciphers import keyed_vigenere_decrypt

    def row(label, letters, cls):
        cells = "".join(f'<i class="lc {cls}">{esc(ch)}</i>' for ch in letters)
        return f'<div class="how-row"><span class="how-label">{esc(label)}</span><div class="lrow start">{cells}</div></div>'

    if name in ("K1", "K2"):
        d = load_k1() if name == "K1" else load_k2()
        ct = d["ciphertext"] if name == "K1" else d["ciphertext_as_carved"]
        key = d["key"]
        n = 14
        carved = ct[:n]
        keyrow = (key * 3)[:n]
        plain = keyed_vigenere_decrypt(carved, key, KRY)
        c0, k0, p0 = carved[0], key[0], plain[0]
        ci, ki = KRY.index(c0), KRY.index(k0)
        steps = [
            "The table carved on the sculpture's right half gives the alphabet: KRYPTOSABCDEFGHIJLMNQUVWXZ, each row shifted one place further.",
            "Letter counts in the carved text rise and fall with a short period, the mark of a repeating key word. Its length came from the statistics; K2's 372 letters made that easy, and the same table opened K1.",
            f"Each letter is then undone by hand: find the carved letter's place in the KRYPTOS alphabet, take away the key letter's place, and read the letter at the difference.",
        ]
        worked = (row("carved", carved, "") + row(f"key: {key}, repeated", keyrow, "keyc") + row("message", plain, "ink")
                  + f'<p class="how-worked">First letter: {c0} is {ci} in the KRYPTOS alphabet, key {k0} is {ki}; {ci} take away {ki} is {(ci - ki) % 26}, which is {p0}.</p>')
        if name == "K2":
            steps[1] = "The same table and the same kind of key as K1, with a different key word; the longer text makes the key word's length plain from the letter statistics."
            steps.append("The question marks are carved and left alone; X marks the end of a sentence. In 2006 Sanborn said a letter was left out of the carving near the end, which turns ID BY ROWS into LAYER TWO.")
    else:
        d = load_k3()
        ct, pt = d["ciphertext"], d["plaintext"]
        a, b, n_ = d["formula"]["a"], d["formula"]["b"], d["formula"]["n"]
        places = [(a + b * i) % n_ + 1 for i in range(10)]
        steps = [
            "The letter counts are those of ordinary English, so no letter was changed: they were only moved. That makes K3 a transposition.",
            "Sanborn wrote the message into a grid, turned it a quarter turn, wrote it into a grid of another width, and turned it again, then carved the result.",
            f"The two turns come to a simple rule: each letter of the message is the carved letter {b} places on from the last, counting round the {n_} letters and starting at place {a + 1}.",
        ]
        cells_pl = "".join(f'<i class="lc ink">{esc(pt[i])}</i>' for i in range(10))
        cells_ct = "".join(f'<i class="lc">{esc(ct[p_ - 1])}</i>' for p_ in places)
        nums = "".join(f'<i class="lc num">{p_}</i>' for p_ in places)
        worked = (f'<div class="how-row"><span class="how-label">carved place</span><div class="lrow start">{nums}</div></div>'
                  f'<div class="how-row"><span class="how-label">carved letter</span><div class="lrow start">{cells_ct}</div></div>'
                  f'<div class="how-row"><span class="how-label">message</span><div class="lrow start">{cells_pl}</div></div>'
                  f'<p class="how-worked">Start at place {places[0]}, then count {b} on each time: {places[0]}, {places[1]}, {places[2]}, ... wrapping past {n_}. The letters read {pt[:10]}.</p>')
    steps_html = "".join(f"<li>{esc(st_) if 'Sanborn said' not in st_ else esc(st_)}</li>" for st_ in steps)
    return (f'<div class="how"><p class="lp-eyebrow">how it was solved</p><div class="how-grid"><ol class="how-steps">{steps_html}</ol>'
            f'<div class="how-figure{" k3" if name == "K3" else ""}">{worked}</div></div></div>')


def solved_messages_block():
    """K1, K2, K3 as IN (the carved lines, as on the copper) and OUT (the solution laid out in the
    same lines), one block each, so a reader sees what a solved message looks like."""
    from kryptos.facts import load_k1, load_k2, load_k3
    k1, k2, k3 = load_k1(), load_k2(), load_k3()
    ul = split_by_starts(k1["ciphertext"] + k2["ciphertext_as_carved"], UL_STARTS)
    ll = split_by_starts(k3["ciphertext"] + (ROOT / "data" / "k4.txt").read_text().strip(), LL_STARTS)
    obkr = ll[10].index("OBKR")
    msgs = [
        ("K1", ul[0:2], k1["plaintext"],
         f"Keyed Vigen&egrave;re on the sculpture's own table, key word {k1['key']}. Each letter stays in its place; the table changes it.",
         f"Solved by David Stein (1998) and Jim Gillogly (1999), and by the NSA in 1992. The misspelling {k1['misspelling']} is Sanborn's own."),
        ("K2", ul[2:14], k2["plaintext_as_carved"],
         f"The same table, key word {k2['key']}. The question marks are carved and stay where they are.",
         f"Same solvers. {k2['misspelling']} is carved that way; in 2006 Sanborn said one letter was left out, which changes the last words to LAYER TWO."),
        ("K3", ll[0:10] + [ll[10][:obkr]], k3["plaintext"],
         "No table: the letters are moved, not changed. Written in a grid, turned, and read off in columns; the solution is laid out here in the copper's line shape, not letter for letter.",
         f"Same solvers. It quotes Howard Carter opening Tutankhamun's tomb; {k3['misspelling']} is Sanborn's."),
    ]

    def block(lines, cls, words=None):
        """Rows of cells. With `words` (a word number per letter), each word's letters sit in one
        rounded box, split where a word runs onto the next line; the letter pitch is unchanged, so
        the solution stays aligned with the carved panel cell for cell."""
        rows, pos = [], 0
        for line in lines:
            cell = lambda ch: f'<i class="lc {cls}{" q" if ch == "?" else ""}">{esc(ch)}</i>'
            if words is None:
                rows.append(f'<div class="lrow start">{"".join(cell(ch) for ch in line)}</div>')
            else:
                parts, run, cur = [], [], None
                for j, ch in enumerate(line):
                    w = words[pos + j]
                    if run and w != cur:
                        parts.append(run); run = []
                    run.append(ch); cur = w
                if run:
                    parts.append(run)
                rows.append('<div class="lrow start">' + "".join(f'<span class="word">{"".join(cell(ch) for ch in run)}</span>' for run in parts) + "</div>")
            pos += len(line)
        return "".join(rows)

    def word_numbers(spaced):
        out = []
        for k, w in enumerate(spaced.split()):
            out += [k] * len(w)
        return out

    out = []
    for name, lines, plain, how, who in msgs:
        plain_lines, pos = [], 0
        for line in lines:
            plain_lines.append(plain[pos:pos + len(line)]); pos += len(line)
        n = sum(len(l) for l in lines)
        left = (f'<div class="lp-col"><p class="lp-eyebrow">in: {name} as carved</p><div class="lp"><div class="lp-box">'
                f'<div class="lp-title">{n} letters, {len(lines)} lines of the copper</div>{block(lines, "")}</div></div><p class="lp-note"><b>How.</b> {how}</p></div>')
        right = (f'<div class="lp-col"><p class="lp-eyebrow">out: {name} solved</p><div class="lp"><div class="lp-box">'
                 f'<div class="lp-title">the message, readable English; each word boxed</div>{block(plain_lines, "ink", word_numbers(SPACED[name]))}</div></div><p class="lp-note"><b>Who.</b> {who}</p></div>')
        arrow = '<div class="lp-arrow"><svg width="34" height="14" viewBox="0 0 34 14"><path d="M1,7 L28,7" stroke="currentColor" stroke-width="1.4"/><path d="M26,2 L33,7 L26,12 z" fill="currentColor"/></svg></div>'
        out.append((name, f'<div class="kpane"><div class="panel-wrap wide">{left}{arrow}{right}</div>{how_solved_html(name)}</div>'))
    return out


def crib_cells(html_text):
    """Write the two clue words in the house letter cells wherever they appear in running text."""
    def word(w):
        return '<span class="inl">' + "".join(f'<i class="lc known">{c}</i>' for c in w) + "</span>"
    for w in ("EASTNORTHEAST", "BERLINCLOCK"):
        html_text = re.sub(rf"(?<![A-Z>]){w}(?![A-Z])", word(w), html_text)
    return html_text


# The history under the sculpture model on the overview: (date, era, kind, title, text, [(source, url)]).
# kind: place, making, dedication, solved, clue, endgame, us. Sources checked in research_notes/timeline-sources.md.
HISTORY = [
    ("November 3, 1959", "The building", "place", "A cornerstone at Langley",
     "President Eisenhower lays the cornerstone of the CIA's headquarters in Langley, Virginia.",
     [("CIA, About the OHB Cornerstone", "https://www.cia.gov/legacy/headquarters/ohb-cornerstone/")]),
    ("1961", "The building", "place", "The Original Headquarters Building opens",
     "The CIA's own pages give March 1961 for completion and the autumn of 1961 for staff moving in. Kryptos will stand in the courtyard between this building and the next.",
     [("CIA, Original Headquarters Building", "https://www.cia.gov/legacy/headquarters/original-headquarters-building-ohb"),
      ("CIA, Sites to See (PDF)", "https://www.cia.gov/static/Sites-to-See.pdf")]),
    ("1988", "The commission", "making", "Art for the new building",
     "A small part of the New Headquarters Building's cost is set aside for art. The CIA's Fine Arts Commission recommends the GSA's Art-in-Architecture programme, and the GSA forms a selection team led by the NEA.",
     [("CIA, About the Kryptos Sculpture", "https://www.cia.gov/legacy/headquarters/kryptos-sculpture/")]),
    ("November 1988", "The commission", "making", "Jim Sanborn is chosen",
     "A combined NEA and CIA panel picks the Washington sculptor for a $250,000 commission. He reads extensively on intelligence and cryptography.",
     [("CIA, About the Kryptos Sculpture", "https://www.cia.gov/legacy/headquarters/kryptos-sculpture/")]),
    ("1989", "The making", "making", "Lessons from Ed Scheidt",
     "Sanborn works for four months with Ed Scheidt, the retiring chairman of the CIA's Cryptographic Center, to devise the codes; Scheidt teaches him \u201cmatrix codes.\u201d",
     [("CIA, About the Kryptos Sculpture", "https://www.cia.gov/legacy/headquarters/kryptos-sculpture/"),
      ("Washington Post, July 19, 1999", "https://www.washingtonpost.com/wp-srv/national/daily/july99/kryptos19.htm")]),
    ("November 9, 1989", "The making", "making", "The Berlin Wall falls",
     "Sanborn is at work on Kryptos the year the Wall falls. BERLIN and CLOCK will turn out to be in K4.",
     [("Wired, November 20, 2014", "https://www.wired.com/2014/11/second-kryptos-clue/")]),
    ("1989\u201390", "The making", "making", "The text is enciphered on the road",
     "Sanborn does the encryption on his own during a four-day drive trucking the petrified tree from Arizona. The whole project, by his count, took two and a half years.",
     [("Washington Post, July 19, 1999", "https://www.washingtonpost.com/wp-srv/national/daily/july99/kryptos19.htm")]),
    ("November 3, 1990", "The dedication", "dedication", "Kryptos is dedicated",
     "Director William Webster receives the solution in a sealed envelope. \u201cWe like to be tested.\u201d Other records give November 1 or 5, and the 1999 New York Times October.",
     [("CIA, About the Kryptos Sculpture", "https://www.cia.gov/legacy/headquarters/kryptos-sculpture/"),
      ("CIA, Sites to See (PDF)", "https://www.cia.gov/static/Sites-to-See.pdf")]),
    ("March 1991", "The dedication", "place", "The New Headquarters Building is finished",
     "The building behind the sculpture is completed.",
     [("CIA, Sites to See (PDF)", "https://www.cia.gov/static/Sites-to-See.pdf")]),
    ("November 1992", "The first solutions", "solved", "The NSA solves K1, K2 and K3, quietly",
     "A task force breaks the first three messages within two days, spends one more on K4 and stops. The NSA says so publicly only in June 1999, after Gillogly; the team's names come out in March 2000.",
     [("NSA, staff processing form Z-054-98 (PDF)", "https://media.defense.gov/2021/Jul/12/2002760460/-1/-1/0/DOC_2.PDF"),
      ("NSA FOIA releases, CIA Kryptos Sculpture", "https://www.nsa.gov/Helpful-Links/NSA-FOIA/Declassification-Transparency-Initiatives/FOIA-Reports-and-Releases/FOIA-Reports-and-Releases-List/")]),
    ("February\u2013March 1998", "The first solutions", "solved", "David Stein solves them by hand",
     "A CIA analyst breaks K2 with pencil and paper on February 21, 1998, and presents K1 to K3 to a packed headquarters auditorium on March 20.",
     [("Stein, Cracking the Courtyard Crypto (CIA)", "https://www.cia.gov/readingroom/document/06712772"),
      ("CIA Intellipedia, archived", "https://web.archive.org/web/20240107223455/https://www.cia.gov/readingroom/document/06498615")]),
    ("June 1999", "The first solutions", "solved", "Jim Gillogly solves them by computer, and the solutions go public",
     "Gillogly announces his solution on June 16; the New York Times reports Stein's earlier one the same day. The three messages, as carved and as read:",
     [("New York Times, June 16, 1999", "https://www.nytimes.com/library/tech/99/06/biztech/articles/16code.html"),
      ("Gillogly's post, June 16, 1999", "https://www.elonka.com/kryptos/mirrors/cypherpunks/1999/0930.html")]),
    ("April 26, 1999", "The first solutions", "place", "The compound becomes the George Bush Center for Intelligence",
     "Named by Act of Congress in October 1998 for George H. W. Bush, director of the CIA in 1976\u201377, and dedicated in April 1999.",
     [("Public Law 105-272, \u00a7309", "https://www.govinfo.gov/content/pkg/PLAW-105publ272/html/PLAW-105publ272.htm"),
      ("CIA, archived by NARA", "https://www.webharvest.gov/peth04/20041015010959/http://cia.gov/cia/information/bush.html")]),
    ("January 2005", "Clues from the creators", "clue", "Matrix codes, masking, instructions in the earlier text",
     "In interviews Sanborn says he used \u201csome matrix codes Ed gave me\u201d and \u201cleft instructions in the earlier text that refer to later text\u201d; Scheidt says he \u201cmasked the English language.\u201d",
     [("Wired, January 20, 2005", "https://www.wired.com/2005/01/questions-for-kryptos-creator/"),
      ("Scheidt Q&A, mirrored", "https://scirealm.org/KryptosHints.html")]),
    ("April 2006", "Clues from the creators", "clue", "A letter left out of K2",
     "Sanborn says he left a letter out of K2: what was read as ID BY ROWS should read X LAYER TWO.",
     [("Wired, April 20, 2006", "https://www.wired.com/2006/04/typo-confounds-kryptos-sleuths/")]),
    ("November 2010", "Clues from the creators", "clue", "BERLIN",
     "Letters 64\u201369 of K4, NYPVTT, read BERLIN.",
     [("New York Times, November 20, 2010", "https://www.nytimes.com/2010/11/21/us/21code.html")]),
    ("November 2014", "Clues from the creators", "clue", "CLOCK",
     "Letters 70\u201374 read CLOCK, on the 25th anniversary of the Wall's fall; the Berlin clock is named.",
     [("New York Times, November 20, 2014", "https://www.nytimes.com/2014/11/21/us/another-kryptos-clue-is-offered-in-a-24-year-old-mystery-at-the-cia.html"),
      ("Wired, November 20, 2014", "https://www.wired.com/2014/11/second-kryptos-clue/")]),
    ("January 2020", "Clues from the creators", "clue", "NORTHEAST",
     "Letters 26\u201334 read NORTHEAST; the phrase is \u201cin itself a riddle.\u201d",
     [("New York Times, January 29, 2020", "https://www.nytimes.com/interactive/2020/01/29/climate/kryptos-sculpture-final-clue.html"),
      ("NPR, January 29, 2020", "https://www.npr.org/2020/01/29/801323608/")]),
    ("August 2020", "Clues from the creators", "clue", "EAST",
     "Letters 22\u201325 read EAST, completing EASTNORTHEAST. Sanborn had sent it privately since April; it became public on August 24.",
     [("John Schwartz (NYT), August 24, 2020", "https://twitter.com/jswatz/status/1297658577914667008"),
      ("Schmeh, Klausis Krypto Kolumne", "https://scienceblogs.de/klausis-krypto-kolumne/2020/08/24/jim-sanborn-publishes-another-new-kryptos-clue/")]),
    ("August 2025", "Endgame", "endgame", "The solution goes to auction",
     "Sanborn announces he will sell the K4 solution at an auction timed to his 80th birthday.",
     [("Washington Post, August 14, 2025", "https://www.washingtonpost.com/entertainment/art/2025/08/14/kryptos-code-k4-solution-jim-sanborn-auction/"),
      ("Sanborn's open letter", "https://www.elonka.com/kryptos/OpenLetterAug2025.html")]),
    ("September 2025", "Endgame", "endgame", "The plaintext is found in an archive",
     "Two journalists find K4's plaintext on scraps of paper among Sanborn's papers at the Smithsonian's Archives of American Art and tell him; they do not publish it. The method is still unknown.",
     [("Smithsonian, Office of the Secretary", "https://www.smithsonianmag.com/blogs/office-of-the-secretary-of-the-smithsonian/2026/02/17/smithsonian-archives-help-unlock-mysteries-connect-americans-history/"),
      ("Scientific American, October 16, 2025", "https://www.scientificamerican.com/article/a-solution-to-the-cias-kryptos-code-is-found-after-35-years/")]),
    ("November 2025", "Endgame", "clue", "The World Clock, Egypt and the Wall",
     "On November 12, in an open letter and at the International Spy Museum, Sanborn names his 1986 Egypt trip, the 1989 fall of the Wall and the World Clock in Berlin as part of K4. On November 20 the archive sells for $962,500.",
     [("Scientific American, November 12, 2025", "https://www.scientificamerican.com/article/cia-kryptos-puzzle-creator-releases-final-clues/"),
      ("RR Auction, November 21, 2025", "https://content.rrauction.com/jim-sanborns-complete-kryptos-archive-sells-for-962500-at-auction/")]),
    ("October 2026", "Endgame", "us", "This loop starts",
     "An autoresearch loop sets out to find the method from the record alone.", []),
]

TL_CSS = """<style>
.tl{width:min(1200px,94vw);position:relative;left:50%;transform:translateX(-50%);margin:10px 0 28px}
.tl-ev{display:grid;grid-template-columns:150px 28px minmax(0,1fr);align-items:start}
.tl-date{font:600 12.5px/1.3 var(--serif);color:var(--muted);text-align:right;padding:3px 0 0}
.tl-rail{position:relative;align-self:stretch}
.tl-rail:before{content:'';position:absolute;left:13px;top:0;bottom:0;border-left:1px solid var(--rule)}
.tl-ev:first-of-type .tl-rail:before{top:9px}.tl-ev.last .tl-rail:before{bottom:auto;height:9px}
.tl-dot{position:absolute;left:8px;top:5px;width:11px;height:11px;border-radius:50%;background:var(--paper);border:2px solid var(--muted);box-sizing:border-box}
.tl-ev.k-solved .tl-dot{background:var(--accent);border-color:var(--accent)}
.tl-ev.k-clue .tl-dot{border-color:var(--ochre);background:var(--ochre)}
.tl-ev.k-dedication .tl-dot{background:var(--ink);border-color:var(--ink);width:13px;height:13px;left:7px;top:4px}
.tl-ev.k-endgame .tl-dot{border-color:var(--ink)}
.tl-ev.k-us .tl-dot{border:2px dashed var(--accent)}
.tl-body{padding:0 0 18px 6px;min-width:0}
.tl-body h4{font:400 18px/1.3 var(--serif);margin:0 0 3px}
.tl-body p{margin:0;font-size:15px;color:var(--muted);max-width:640px}
.tl-body p.tl-src{font-size:12px;color:var(--faint);margin-top:3px}.tl-src a{color:var(--faint);border-bottom:1px dotted var(--faint);text-decoration:none}.tl-src a:hover{color:var(--accent)}
.tl-era{display:grid;grid-template-columns:150px 28px minmax(0,1fr)}
.tl-era span{grid-column:3;font:600 11px var(--serif);text-transform:uppercase;letter-spacing:.1em;color:var(--accent);padding:10px 0 8px 6px}
.tl-era .tl-rail{grid-column:2;grid-row:1}
.tl-insert{margin:12px 0 4px}
.tl-insert h5{font:600 11px var(--serif);text-transform:uppercase;letter-spacing:.1em;color:var(--muted);margin:14px 0 2px}
.tl .panel-wrap.wide,.tl .how{width:auto;left:0;transform:none;max-width:none}
.tl .kpane{zoom:.8}
.tl-key{display:flex;flex-wrap:wrap;gap:6px 20px;font-size:13px;color:var(--muted);margin:0 0 14px 184px}
.tl-key i{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:-1px;box-sizing:border-box}
@media(max-width:760px){.tl-ev,.tl-era{grid-template-columns:0 22px minmax(0,1fr)}.tl-date{display:none}.tl-body .tl-d{display:block}.tl-key{margin-left:0}.tl .kpane{zoom:.55}.tl-rail:before{left:10px}.tl-dot{left:5px}}
.tl-d{display:none;font:600 12px var(--serif);color:var(--muted);margin-bottom:2px}
</style>"""


def history_timeline():
    """Kryptos from the cornerstone to today, vertically; the K1-K3 solution panels hang off the
    1999 entry, where the solutions went public."""
    solved = dict(solved_messages_block())
    out, era = [], None
    for i, (date, e, kind, title, text, src) in enumerate(HISTORY):
        if e != era:
            out.append(f'<div class="tl-era"><div class="tl-rail"></div><span>{esc(e)}</span></div>')
            era = e
        insert = ""
        if date == "June 1999":
            insert = '<div class="tl-insert">' + "".join(f"<h5>{k} solved</h5>{solved[k]}" for k in ("K1", "K2", "K3")) + "</div>"
        last = " last" if i == len(HISTORY) - 1 else ""
        out.append(f'<div class="tl-ev k-{kind}{last}"><div class="tl-date">{esc(date)}</div><div class="tl-rail"><i class="tl-dot"></i></div>'
                   f'<div class="tl-body"><span class="tl-d">{esc(date)}</span><h4>{esc(title)}</h4><p>{crib_cells(esc(text))}</p>'
                   + (f'<p class="tl-src">{" &middot; ".join(f"<a href=\"{esc(u)}\" target=\"_blank\" rel=\"noopener\">{esc(t)}</a>" for t, u in src)}</p>' if src else "")
                   + f'{insert}</div></div>')
    key = ('<div class="tl-key"><span><i style="border:2px solid var(--muted)"></i>place and making</span>'
           '<span><i style="background:var(--ink)"></i>the dedication</span>'
           '<span><i style="background:var(--accent)"></i>a message solved</span>'
           '<span><i style="background:var(--ochre)"></i>a clue from the creators</span>'
           '<span><i style="border:2px dashed var(--accent)"></i>this loop</span></div>')
    return TL_CSS + '<div class="tl">' + key + "".join(out) + "</div>"


def what_we_look_for():
    from kryptos.facts import KNOWN as _KNOWN, K4 as _K4
    panel = panel_block(_K4, None, _KNOWN)
    cols = [
        ("The 24 known letters", "Jim Sanborn has confirmed two stretches of the hidden message: EASTNORTHEAST at positions 22 to 34 and BERLINCLOCK at 64 to 74, in accent in the panels. They are the only hard facts about the message, and every experiment leans on them."),
        ("What the loss counts", "A candidate is a full 97-letter reading of the panel. It pays ten points for each known letter it gets wrong, then a little for how far the other 73 letters sit from English, then a charge for a secret word too long to remember. Zero would be solved."),
        ("The line at ten", "Above it, at least one known letter is wrong. Below it, all 24 are right and only the English of the rest and the length of the key remain. A dot below the line is not a solution until the text reads as English and the key is one a person could remember."),
    ]
    html = "".join(f'<div class="explain-col"><h4>{esc(h)}</h4><p>{crib_cells(esc(t))}</p></div>' for h, t in cols)
    sub = lambda n, t, d: f'<div class="subsec"><b>1.{n}</b><h3>{t}</h3></div><p class="subsec-sub">{d}</p>'
    # the 3D model may not be redistributed (only its author's zip may), so the public site has none
    model = MODEL.exists() and not EXPORT
    k = 1 if model else 0
    return ((sub(1, "The Kryptos sculpture by Jim Sanborn", "Hover a key below the model, or a plate, to see which message it carries.") + sculpture_block() if model else "")
            + sub(k + 1, "In context: The history of the sculpture", "The history of Kryptos, from the CIA's headquarters to today. The first three messages hang off 1999, when their solutions went public: carved letters in, readable English out, which is what solved looks like.")
            + history_timeline()
            + sub(k + 2, "The fourth message, as the loop sees it", "In: the 97 carved letters of K4, laid out as on the copper. Out: what every candidate must produce.") + panel
            + f'<div class="explain-row">{html}</div>')


def sec(n, title, sub=""):
    return f'<div class="rsec"><span class="rsec-n">{n}</span><h2 class="rsec-t">{esc(title)}</h2></div>' + (f'<p class="rsec-sub">{esc(sub)}</p>' if sub else "")


def overview():
    rows = load_results()
    ch = champion()
    n = len(rows)
    kept = sum(1 for r in rows if r["decision"] == "kept")
    best_hits = max((r["best_crib_hits"] for r in rows), default=0)
    best_loss = ch.get("loss") if ch else None
    fams = len({r["family"] for r in rows})
    secs = sum(sum((r.get("phases") or {}).values()) or r["seconds"] for r in rows)
    by_phase = {}
    for r in rows:
        for k, v in (r.get("phases") or {"run": r["seconds"]}).items():
            by_phase[k] = by_phase.get(k, 0.0) + v
    answer = (f'&ldquo;We believe so, and we have a champion: <a href="/exp/{esc(ch["experiment"])}">{esc(ch["experiment"])}</a>.&rdquo;' if ch
              else "&ldquo;We believe so, but we have not yet found our champion.&rdquo;")
    hero = f"""<p class="psub answer">{answer}</p>
<div class="stats">
<div class="stat"><b class="num">{n}</b><span>experiments</span></div>
<div class="stat"><b class="num">{kept}</b><span>kept</span></div>
<div class="stat"><b class="num">{secs/3600:.1f}</b><span>hours, all phases</span></div>
</div>"""
    if ch:
        from kryptos.facts import KNOWN as _KNOWN, K4 as _K4
        champ = f"""<div class="callout wide"><div class="callout-h">Champion: <a href="/exp/{esc(ch['experiment'])}">{esc(ch['experiment'])}</a></div>{panel_block(_K4, ch['plaintext'], _KNOWN)}<p class="muted" style="font-size:13px">{esc(ch['key_description'])}; loss {ch.get('loss', 0):.2f}, {pct(ch.get('loss'))} of the worst possible. A champion is the lowest-loss candidate that passed every gate; it is not a solution until its text reads as English and its key is memorable.{' Experiments 0001-0049 were kept by a different number, fitness, which is why a reverted experiment can sit below the champion in the chart; from 0050 the harness keeps by loss.' if ch['experiment'][:4] <= '0049' else ''}</p></div>"""
    else:
        champ = '<div class="callout"><div class="callout-h">Champion</div><p>None yet. No candidate has passed all four gates.</p></div>'
    body = ('<h1 class="home">&ldquo;Can an autonomous research loop find the secret of Kryptos K4?&rdquo;</h1>' + hero_flow()
            + hero   # champion callout hidden for now (Alexis, 2026-10-15: too noisy); `champ` is still built
            + sec(1, "What is Kryptos K4?", "A sculpture in the courtyard of the CIA, its history since 1959, and the fourth of its four messages, the one nobody has read.")
            + ('<p class="sec-lead">Kryptos is a sculpture by the artist Jim Sanborn, dedicated in 1990 in the courtyard of the '
               'CIA\'s headquarters in Langley, Virginia. Its centrepiece is a curved copper screen cut through with about 1,730 '
               'letters: four encrypted messages, K1 to K4, and the table of alphabets used to encrypt the first two.</p>'
               '<p class="sec-lead">K1, K2 and K3 were solved in the 1990s. K4, the last 97 letters, has never been publicly solved. Sanborn has confirmed '
               'only two stretches of its plaintext, EASTNORTHEAST and BERLINCLOCK. In 2025 the full plaintext turned up '
               'among his papers at the Smithsonian, but it has not been published, and the method that turns the 97 '
               'carved letters into that message is still unknown.</p>'
               '<p class="sec-lead">That method is what this loop is looking for.</p>')
            + what_we_look_for()
            + sec(2, "Where do you go from here?", "Two ways to follow the work as it goes.")
            + '<div class="explain-row cols-2">'
            + f'<div class="explain-col"><h4><a href="/experiments">The experiments &rarr;</a></h4><p>Every experiment so far, {n} of them, placed by what it found against scrambled copies of the carved text, updated as each new one lands.</p></div>'
            + '<div class="explain-col"><h4><a href="/lineage">The lineage &rarr;</a></h4><p>How each experiment built on an earlier one, family by family, in the order they ran.</p></div>'
            + '</div>')
    return page("Kryptos K4: can an AI research loop find its secret?", body, "/")


def experiments_table(rows):
    """Every experiment, newest first, with its loss, crib letters, candidates and time by phase."""
    scale_max = max((sum((r.get("phases") or {"run": r["seconds"]}).values()) for r in rows), default=0)
    pv_after = {p["after"]: p for p in load_pivots()}
    ncols = 9

    def pivot_row(p):
        return (f'<tr class="pivot-row"><td colspan="{ncols}"><a href="/pivot/{esc(p["id"])}">Pivot {esc(p["id"])}: {esc(p["from"])} &rarr; {esc(p["to"])}'
                '<svg width="9" height="7" viewBox="0 0 9 7"><path d="M0.5,0.5 L8.5,0.5 L4.5,6.5 z" fill="var(--accent)"/></svg></a></td></tr>')
    trs = "".join(
        (pivot_row(pv_after[r["tag"][:4]]) if r["tag"][:4] in pv_after else "") +
        f"""<tr><td class="num">{int(r['tag'][:4])}</td><td><a href="/exp/{esc(r['tag'])}">{esc(r['title'])}</a></td><td class="muted">{esc(r['family'].split('-', 1)[0] + ' ' + r['family'].split('-', 1)[-1].replace('-', ' '))}</td>
<td class="{esc(r['decision'])}">{esc(r['decision'])}</td>
<td class="num" title="{'' if row_loss(r) is None else f"{row_loss(r):.2f} of {WORST:.0f}"}">{pct(row_loss(r))}</td>
<td class="num" title="{esc(words_str(r))}">{r['best_crib_hits']}/24</td>
<td class="num">{r['n_candidates']}</td><td class="num" title="{esc(', '.join(f'{k} {fmt_dur(v)}' for k, v in (r.get('phases') or {}).items()))}">{fmt_dur(sum((r.get('phases') or {}).values()) or r['seconds'])}</td><td>{phase_bar(r.get('phases') or {'run': r['seconds']}, scale_max)}</td></tr>"""
        for r in reversed(rows)
    )
    table = f"""<table><thead><tr><th class="num">id</th><th>title</th><th>family</th><th>decision</th><th class="num" title="the best candidate's loss as a share of the worst possible, 240">loss</th><th class="num" title="known letters the best candidate got right, out of 24">crib letters</th><th class="num" title="full 97-letter decryptions the experiment handed to the gates">candidates</th><th class="num">time</th><th>by phase, scaled to the longest</th></tr></thead><tbody>{trs}</tbody></table>"""
    return (sec(2, "All experiments in sequence")
            + '<div class="xtable">' + table + "</div>")


OUTCOME_ROWS = [
    ("solved", "solved"),
    ("champion", "champion"),
    ("beat-chance", "a lead"),
    ("chance", "at chance"),
    ("ruled-out", "ruled out"),
    ("diagnostic", "not a decryption test"),
    ("other", "no comparison"),
    ("error", "errored"),
    ("ungraded", "not graded yet"),
]


def outcome_chart(rows):
    """One row per outcome against the scrambled copies (grades.tsv), one tick per experiment in run
    order, a running count at the end of each row. Built to stay legible at a thousand experiments."""
    if not rows:
        return "<p class='muted'>No experiments yet.</p>"
    grades = load_grades()
    W, L, R, T, band = 1480, 64, 220, 36, 46     # W at 95vw keeps the text the size it was at 1400 and 90vw
    n = len(rows)
    step = (W - L - R) / n
    dot_r = max(1.2, min(3.6, step * 0.42))     # the lineage page's dot, shrinking only when experiments crowd
    kinds = {}
    for r in rows:
        oc = grades.get(r["tag"][:4], {}).get("outcome")
        if oc == "solved" and not (EXPORT and r["tag"] not in confirmed()):
            kinds[r["tag"]] = "solved"
        elif r.get("decision") == "kept":
            kinds[r["tag"]] = "champion"
        else:
            kinds[r["tag"]] = ("error" if r.get("decision") in ("error", "timeout") else
                               oc if oc in ("beat-chance", "chance", "ruled-out", "diagnostic") else ("ungraded" if not oc else "other"))
    shown = [(k, lab) for k, lab in OUTCOME_ROWS if k != "ungraded" or "ungraded" in kinds.values()]
    yrow = {k: T + j * band for j, (k, _) in enumerate(shown)}
    H = T + band * len(shown) + 58
    g = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="What each experiment found against the scrambled copies, in run order">']
    for j, (k, _) in enumerate(shown):
        y0 = yrow[k]
        g.append(f'<line x1="{L}" x2="{W - R}" y1="{y0 + band / 2:.1f}" y2="{y0 + band / 2:.1f}" stroke="var(--rule-soft)" stroke-width="1"/>')
    # solid divides: below "solved"; above "at chance" the outcomes that could be the solution; above "not a decryption test" the rest that were not tests
    for k in ("champion", "chance", "diagnostic"):
        if k in yrow:
            g.append(f'<line x1="{L}" x2="{W - 16}" y1="{yrow[k]}" y2="{yrow[k]}" stroke="var(--muted)" stroke-width="1.2"/>')
    counts = {k: 0 for k, _ in shown}
    for i, r in enumerate(rows):
        k = kinds[r["tag"]]
        counts[k] += 1
        gr = grades.get(r["tag"][:4], {})
        x = L + (i + 0.5) * step
        y0 = yrow[k] + 9
        col = "var(--accent)" if k in ("solved", "champion", "beat-chance") else ("var(--faint)" if k == "ungraded" else "var(--disc)")
        tip = (f"{esc(r['tag'])}<br>{esc(r['title'])}<br><b>{esc(gr.get('outcome') or 'not graded yet')}</b>"
               f"{', ' + esc(gr['strength']) + ' test' if gr.get('strength') else ''}<br>{esc(gr.get('note', ''))}")
        cy = yrow[k] + band / 2
        dec, rec = r.get("decision"), r.get("decision_recorded")
        if dec == "kept":
            mark = f'<circle cx="{x:.2f}" cy="{cy:.1f}" r="{dot_r * 1.4:.1f}" fill="var(--ink)"/>'
        elif dec in ("error", "timeout"):
            e = dot_r
            mark = f'<path d="M{x - e:.2f},{cy - e:.1f} L{x + e:.2f},{cy + e:.1f} M{x + e:.2f},{cy - e:.1f} L{x - e:.2f},{cy + e:.1f}" stroke="var(--accent)" stroke-width="1.6"/>'
        else:
            mark = f'<circle cx="{x:.2f}" cy="{cy:.1f}" r="{dot_r:.1f}" fill="var(--disc)"/>'
        if rec == "kept" and dec != "kept":
            mark += f'<circle cx="{x:.2f}" cy="{cy:.1f}" r="{dot_r * 2:.1f}" fill="none" stroke="var(--ink)" stroke-width="1" stroke-dasharray="2 2"/>'
        g.append(f'<a href="/exp/{esc(r["tag"])}"><g data-tip="{tip}">{mark}'
                 f'<rect x="{x - max(step, 4) / 2:.2f}" y="{yrow[k]}" width="{max(step, 4):.2f}" height="{band}" fill="transparent"/></g></a>')
    for k, lab in shown:
        cy = yrow[k] + band / 2
        col = "var(--accent)" if k in ("solved", "champion", "beat-chance") else "var(--ink)"
        g.append(f'<text x="{W - R + 14}" y="{cy + 5:.1f}" font-size="15" fill="{col}">{lab}<tspan dx="9" font-size="13.5" fill="var(--muted)">{counts[k]}</tspan></text>')
    pos = {r["tag"][:4]: i for i, r in enumerate(rows)}
    for pv in load_pivots():
        if pv.get("after") in pos:
            px = L + (pos[pv["after"]] + 1) * step
            g.append(f'<a href="/pivot/{esc(pv["id"])}"><g data-tip="Pivot {esc(pv["id"])}, {esc(pv["date"])}<br>{esc(pv["from"])} &rarr; {esc(pv["to"])}">'
                     f'<path d="M{px - 3.5:.1f},{T - 6:.1f} L{px + 3.5:.1f},{T - 6:.1f} L{px:.1f},{T - 0.4:.1f} z" fill="var(--accent)" fill-opacity=".8"/>'
                     f'<rect x="{px - 7:.1f}" y="{T - 12:.1f}" width="14" height="16" fill="transparent"/></g></a>')
    tick_every = next(t for t in (10, 20, 50, 100, 200, 500, 1000) if n / t <= 14)
    for i, r in enumerate(rows):
        num = int(r["tag"][:4]) if r["tag"][:4].isdigit() else i + 1
        if num == 1 or num % tick_every == 0:
            g.append(f'<text x="{L + (i + 0.5) * step:.1f}" y="{H - 34}" font-size="12.5" fill="var(--faint)" text-anchor="middle">{num}</text>')
    g.append(f'<text x="{L + (W - L - R) / 2:.1f}" y="{H - 8}" font-size="13.5" font-style="italic" fill="var(--muted)" text-anchor="middle">experiment number, in the order it ran</text>')
    g.append(f'<text transform="translate({L - 24},{T + band * len(shown) / 2:.1f}) rotate(-90)" font-size="13.5" font-style="italic" fill="var(--muted)" text-anchor="middle">outcome against the scrambled copies</text>')
    g.append("</svg>")
    return "<div class='chart-wide' style='margin-top:14px;width:95vw'><figure class='chart' style='margin:0'>" + "".join(g) + "</figure></div>"


def load_pivots():
    """pivots/P*.md: frontmatter (id, date, after, from, to) and a markdown body, in run order."""
    out = []
    for f in sorted((ROOT / "pivots").glob("P*.md"), key=lambda f: int(f.stem[1:]) if f.stem[1:].isdigit() else 0):
        text = f.read_text()
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
        if not m:
            continue
        meta = dict(ln.split(": ", 1) for ln in m.group(1).splitlines() if ": " in ln)
        body = m.group(2)
        t = re.match(r"^# (.*)\n", body)
        meta["title"] = t.group(1).strip() if t else meta.get("id", f.stem)
        meta["body"] = body[t.end():] if t else body
        out.append(meta)
    return sorted(out, key=lambda p: p.get("after", ""))


def learnings_page():
    """What the search has taught us so far. For now only the hero; the content is to be agreed first."""
    hero = ('<h1 class="home">&ldquo;Results! Why, man, I have gotten a lot of results!<br>I know several thousand things that won&rsquo;t work.&rdquo;</h1>'
            '<p class="psub">Thomas Edison, as recalled by his associate Walter S. Mallory, in Dyer and Martin, '
            '<a href="https://quoteinvestigator.com/2012/07/31/edison-lot-results/" target="_blank" rel="noopener"><i>Edison: His Life and Inventions</i> (1910)</a></p>')
    arrow = ('<div class="learn-arrow"><svg width="14" height="90" viewBox="0 0 14 90">'
             '<path d="M7,0 L7,78" stroke="var(--muted)" stroke-width="1.4"/><path d="M1,76 L7,89 L13,76 z" fill="var(--muted)"/></svg></div>')
    soon = ('<div class="hf-method learn-soon"><b>Our learnings, coming soon</b>'
            '<span>What the experiments have taught us about K4, one finding at a time.</span></div>')
    return page("learnings", '<div class="learn-hero">' + hero + arrow + soon + "</div>", "/learnings", False)


def pivot_page(pid):
    pv = {p["id"]: p for p in load_pivots()}.get(pid)
    if not pv:
        return page("not found", f"<p>No pivot {esc(pid)}</p>")
    tags = {r["tag"][:4]: r["tag"] for r in load_results()}
    after = pv["after"]
    nxt = f"{int(after) + 1:04d}"
    facts = (f'{esc(pv["date"])}. After experiment <a href="/exp/{esc(tags.get(after, after))}">{int(after)}</a>'
             + (f', before <a href="/exp/{esc(tags[nxt])}">{int(nxt)}</a>' if nxt in tags else "")
             + f'. From {esc(pv["from"])} to {esc(pv["to"])}.')
    head = page_head(f'Pivot {esc(pv["id"])}', esc(pv["title"]),
                     "Why the search changed course at this point, what had happened before, and the change we believed was needed.", facts)
    foot = page_foot('All pivots are on the <a href="/pivots">pivots</a> page; the pivots are also marked on the '
                     '<a href="/experiments">experiments</a> chart and the <a href="/lineage">lineage</a>.')
    return page(f'pivot {pv["id"]}', head + "<article>" + link_exps_html(md(pv["body"])) + "</article>" + foot, "/pivots", False)


def pivots_page():
    pvs = load_pivots()
    tags = {r["tag"][:4]: r["tag"] for r in load_results()}
    rows = "".join(
        f'<tr><td><a href="/pivot/{esc(p["id"])}">{esc(p["id"])}</a></td><td>{esc(p["date"])}</td>'
        f'<td><a href="/exp/{esc(tags.get(p["after"], p["after"]))}">{int(p["after"])}</a></td>'
        f'<td>{esc(p["from"])}</td><td>{esc(p["to"])}</td><td><a href="/pivot/{esc(p["id"])}">{esc(p["title"])}</a></td></tr>'
        for p in pvs)
    table = ('<table><thead><tr><th>pivot</th><th>date</th><th>after</th><th>from</th><th>to</th><th>details</th></tr></thead>'
             f"<tbody>{rows}</tbody></table>")
    head = page_head("Pivots", "When the search changed family, and why",
                     "Each time the work moved from one family to another, with the experiment it followed. Each pivot has a page "
                     "that says why it happened then, what came before, and the change we believed was needed.",
                     f"{len(pvs)} pivots so far.")
    foot = page_foot('The families themselves are on the <a href="/families">families</a> page; the order they are worked in is on <a href="/priorities">Priorities</a>.')
    return page("pivots", head + "<article>" + table + "</article>" + foot, "/pivots", True)


def fam_num(r):
    return r["family"].split("-", 1)[0]


DECISION_LEGEND = ('<div class="lin-legend">'
                   '<span class="k"><span class="ldot lkept"></span>kept</span>'
                   '<span class="k"><span class="ldot" style="color:var(--disc)"></span>reverted</span>'
                   '<span class="k"><span class="lerr">&times;</span>error or timeout</span>'
                   '<span class="k"><span class="lwas"></span>reverted under today&rsquo;s rules</span>'
                   '<span class="k"><svg width="12" height="10" viewBox="0 0 12 10"><path d="M1,1 L11,1 L6,9 z" fill="var(--accent)"/></svg>pivot</span></div>')


def live_page():
    """The run as it goes: every experiment's best loss, newest on the right, then the table of
    experiments. Reloads when a new experiment lands."""
    rows = load_results()
    latest = rows[-1] if rows else None
    n = len(rows)
    fams = sorted({fam_num(r) for r in rows}, key=lambda k: (not k.isdigit(), int(k) if k.isdigit() else 0))
    days = len({(r.get("started") or "")[:10] for r in rows})
    hours = sum(sum((r.get("phases") or {}).values()) or r["seconds"] for r in rows) / 3600
    errs = sum(1 for r in rows if r.get("decision") in ("error", "timeout"))
    cand = sum(1 for r in rows if (r.get("n_candidates") or 0) > 0)
    none = n - cand - errs
    facts = (f"{n} experiments in {len(fams)} families over {days} days, {hours:.1f} hours of work. {none} ruled everything out before building a reading; "
             f"{cand} produced readings, and none of them beat the same search on scrambled copies of the carved text. {errs} errored.")
    names = {}
    for r in rows:
        k, _, rest = r["family"].partition("-")
        names.setdefault(k, rest.replace("-", " "))
    key = ('<div class="explain-row" style="row-gap:26px;margin-top:40px">'
           '<div class="explain-col"><h4>Solved</h4><p>Meets the success definition: the known letters in place, readable English, and a procedure a person could do by hand with a short key. A winning experiment lands in the dashed band.</p></div>'
           '<div class="explain-col"><h4>Champion</h4><p>Passes every gate: all 24 known letters, re-encrypts to the copper, beats every scrambled copy. Not yet shown to read as English from a memorable method.</p></div>'
           '<div class="explain-col"><h4>A lead</h4><p>K4 did better than every scrambled copy under the same search, but the reading fails another gate.</p></div>'
           '<div class="explain-col"><h4>At chance</h4><p>Settings or readings exist, but scrambled copies produce them just as well.</p></div>'
           '<div class="explain-col"><h4>Ruled out</h4><p>Nothing in the searched space fits the 24 known letters.</p></div>'
           '<div class="explain-col"><h4>Not a decryption test</h4><p>Statistics and simulations about the carved text, not attempts to read it.</p></div></div>')
    body = (page_head("Experiments", "The autonomous research loop, experiment by experiment",
                      "Every experiment, in the order it ran, placed by what it found against scrambled copies of the carved text: the "
                      "same search on the same letters in a random order. A result counts only if K4 does better than all of them. Then the "
                      "table of all experiments, newest first.")
            + sec(1, "Every experiment by outcome")
            + f'<div style="max-width:980px;margin:0 auto"><p class="facts" style="font-size:14.5px;color:var(--muted);margin:4px 0 12px;max-width:820px">{facts}</p>' + DECISION_LEGEND + "</div>"
            + outcome_chart(rows) + key
            + experiments_table(rows)
            + page_foot('How the experiments built on each other is on the <a href="/lineage">lineage</a> page; what is still open is on the <a href="/families">families</a> page.'))
    return page("experiments", body, "/experiments")


def all_candidates(r):
    """Every candidate the experiment returned. Records before experiment 50 stored only the first
    20; where the raw output holds more, the rest are gated and scored here with the same functions."""
    stored = [c for c in r.get("candidates", []) if c.get("plaintext")]
    raw_p = r["_dir"] / "raw.json"
    if len(stored) >= r.get("n_candidates", 0) or not raw_p.exists():
        return stored
    from kryptos.gates import run_gates
    from kryptos.scorer import loss as _loss, key_bits_of
    out = list(stored)
    # the harness scored the raw candidates in order and kept the first 20, so the rest follow on
    for c in json.loads(raw_p.read_text()).get("candidates", [])[len(r.get("candidates", [])):]:
        if not c.get("plaintext"):
            continue
        g = run_gates(c["plaintext"], c.get("reencrypted"))
        out.append({**c, "gate_passed": g.passed, "failed_at": g.failed_at, "crib_hits": g.crib_hits,
                    "loss": _loss(c["plaintext"], key_bits_of(c.get("key")), g.crib_hits) if g.failed_at in (None, "cribs") else None,
                    "key_bits": key_bits_of(c.get("key"))})
    return out


def bounds_html(b):
    """The bounds record as a readable list: names in words, numbers with separators, nested
    records indented, long letter strings wrapped in monospace."""
    def name(k):
        return esc(str(k).replace("_", " "))
    def val(v, depth=0):
        if isinstance(v, bool):
            return "yes" if v else "no"
        if isinstance(v, int):
            return f"{v:,}"
        if isinstance(v, float):
            return f"{v:,.3f}".rstrip("0").rstrip(".") if abs(v) < 1e6 else f"{v:,.0f}"
        if isinstance(v, str):
            return f'<code class="bd-text">{esc(v)}</code>' if v.isupper() and v.isalpha() and len(v) > 20 else esc(v)
        if isinstance(v, list):
            if all(not isinstance(x, (dict, list)) for x in v):
                return ", ".join(val(x) for x in v) or "none"
            return '<ol class="bd-list">' + "".join(f"<li>{val(x, depth + 1)}</li>" for x in v[:12]) + "</ol>" + (f'<span class="muted">and {len(v) - 12} more</span>' if len(v) > 12 else "")
        if isinstance(v, dict):
            return '<dl class="bd">' + "".join(f"<dt>{name(k)}</dt><dd>{val(x, depth + 1)}</dd>" for k, x in v.items()) + "</dl>"
        return esc(str(v))
    if not b:
        return ""
    return '<p class="score-sub">What was searched, as the harness recorded it.</p>' + val(b)


def result_section_html(r, tags, known):
    """The harness's record as a reader wants it: a row of figures, then each candidate as a
    full-size panel with its score and key, lowest loss first. Replaces the generated table."""
    cands = all_candidates(r)
    passed = [c for c in cands if c.get("gate_passed")]
    ranked = sorted(cands, key=lambda c: (not c.get("gate_passed"), c.get("loss") if c.get("loss") is not None else 1e9, -c.get("crib_hits", 0)))
    cb = (r.get("champion_before") or {}).get("experiment")
    cb_html = f'<a href="/exp/{esc(cb)}">{int(cb[:4])}</a>' if cb else "none"
    stats = [(str(r.get("n_candidates", len(cands))), "candidates returned"), (str(r.get("n_passed", len(passed))), "passed every gate"),
             (f"{r.get('best_crib_hits', 0)}/24", "known letters, best"), (pct(r.get("best_loss")) or "&ndash;", "lowest loss"), (cb_html, "champion before")]
    out = '<div class="res-stats">' + "".join(f"<div><b>{v}</b><span>{k}</span></div>" for v, k in stats) + "</div>"
    if not ranked:
        return out
    cards = []
    for k, c in enumerate(ranked, 1):
        status = "passed every gate" if c.get("gate_passed") else f"failed at {esc(c.get('failed_at') or '?')}"
        loss_s = pct(c.get("loss")) or "&ndash;"
        pt = c["plaintext"]
        body = letter_panel(pt, known, "candidate", "").replace('<div class="lp-title"></div>', "") if len(pt) == 97 and pt.isalpha() else f'<code>{esc(pt)}</code>'
        cards.append(f'<div class="res-card"><div class="res-side"><b class="res-rank">{k}</b><span>{status}</span><span>{c.get("crib_hits", 0)}/24 known letters</span><span class="res-loss">loss {loss_s}</span></div>'
                     f'<div class="res-main">{body}<p class="res-key">{esc(c.get("key_description", ""))}</p></div></div>')
    return out + f'<p class="score-sub">All {len(ranked)} candidates, lowest loss first.</p>' + "".join(cards)


def score_parts(c):
    """The loss of one candidate, taken apart the way kryptos.scorer.loss adds it up."""
    from kryptos.scorer import english_score, free_text, ENGLISH_TARGET, MEMORABLE_BITS
    misses = 24 - c.get("crib_hits", 0)
    eng = english_score(free_text(c["plaintext"]))
    deficit = max(0.0, ENGLISH_TARGET - eng)
    bits = c.get("key_bits") or 0.0
    key = max(0.0, bits - MEMORABLE_BITS) / MEMORABLE_BITS
    return {"misses": misses, "crib": 10.0 * misses, "english": eng, "deficit": deficit, "bits": bits, "key": key,
            "total": 10.0 * misses + deficit + key}


def score_section(n, r, best):
    """How the loss was reached: the kept or best candidate's three parts, then the other
    candidates that passed every gate, ranked by loss."""
    from kryptos.scorer import ENGLISH_TARGET, MEMORABLE_BITS
    if not best or best.get("loss") is None:
        return ""
    p = score_parts(best)
    rows = [
        ("Known letters missed", f"{p['misses']} of 24, ten points each", p["crib"]),
        ("English", f"the 73 free letters score {p['english']:.2f}; English text scores {ENGLISH_TARGET:.1f}", p["deficit"]),
        ("Key", f"{p['bits']:.0f} bits to write it down (key words are cheap, arbitrary letters 4.7 bits each); each 60 beyond {MEMORABLE_BITS:.0f} costs a point", p["key"]),
    ]
    trs = "".join(f'<tr><td>{a}</td><td class="muted">{esc(b)}</td><td class="num">{v:.2f}</td></tr>' for a, b, v in rows)
    trs += f'<tr class="total"><td>Loss</td><td class="muted">of {WORST:.0f}, the worst possible</td><td class="num">{p["total"]:.2f} <span class="pct">{pct(p["total"])}</span></td></tr>'
    who = "the candidate kept" if r.get("decision") == "kept" else "the best candidate"
    out = sec(n, "How the score is made", f"The loss of {who}, part by part. Zero is solved.") + f'<table class="score">{trs}</table>'
    passed = sorted([c for c in r.get("candidates", []) if c.get("gate_passed") and c.get("loss") is not None], key=lambda c: c["loss"])
    if len(passed) > 1:
        lines = []
        shown = list(enumerate(passed, 1))
        for j, (k, c) in enumerate(shown):
            if j and k != shown[j - 1][0] + 1:
                lines.append(f'<tr class="gap"><td class="num">&middot;&middot;&middot;</td><td colspan="6"></td></tr>')
            q = score_parts(c)
            mark = ("kept" if r.get("decision") == "kept" else "best") if c is best else ""
            lines.append(f'<tr{" class=kept" if mark == "kept" else ""}><td class="num">{k}</td><td class="num">{q["crib"]:.0f}</td><td class="num">{q["deficit"]:.2f}</td><td class="num">{q["key"]:.2f}</td><td class="num">{q["total"]:.2f}</td><td class="num">{pct(q["total"])}</td><td class="muted">{mark}</td></tr>')
        out += (f'<p class="score-sub">All {len(passed)} candidates that passed every gate, lowest loss first' + '.</p>'
                '<table class="score ranks"><thead><tr><th class="num">rank</th><th class="num">missed</th><th class="num">English</th><th class="num">key</th><th class="num">loss</th><th class="num">share</th><th></th></tr></thead><tbody>'
                + "".join(lines) + "</tbody></table>")
        if r.get("decision") == "kept" and passed[0] is not best:
            out += f'<p class="score-sub">Rank 1 has the lower loss. This experiment ran before experiment 50, when the harness kept by a different number, fitness, which charges long keys less; it kept the candidate marked kept.</p>'
    return out


FIG_SCALE = 1.48   # 7.5-unit letters become 11 px, the panels' 11.5 px; the figure is about 1,400 px wide


def cribmap_out_row(svg, hits):
    """Issue #49: in the OUT row, a known place is filled in accent only if the experiment's best reading
    produced that letter; otherwise it is outlined (the target, not an achievement). Also moves the OUT
    label from under the row to the top of the output arrow, centred."""
    lab = re.search(r'<text x="40" y="([\d.]+)"([^>]*)>(OUT:[^<]*)</text>', svg)
    if not lab:
        return svg
    ly = float(lab.group(1))
    ys = sorted({float(y) for y in re.findall(r'<rect x="[\d.]+" y="([\d.]+)" width="8.2" height="12"', svg) if float(y) < ly})
    if not ys:
        return svg
    row_y = ys[-1]
    if hits is not None:
        def cell(m):
            x = float(m.group(1)); pos = int(round((x - 40) / 9.5)) + 1
            if pos in hits:
                return m.group(0)
            rect = m.group(0).replace('fill="#8c2f1f"', 'fill="#fffff8" stroke="#8c2f1f" stroke-width="1.1"', 1)
            return re.sub(r'(<text[^>]*?)fill="#fffff8"', r'\1fill="#8c2f1f"', rect, count=1)
        ystr = f"{row_y:g}"
        svg = re.sub(rf'<rect x="([\d.]+)" y="{re.escape(ystr)}" width="8.2" height="12"[^>]*fill="#8c2f1f"[^>]*/>(<text[^>]*>[A-Z]</text>)?', cell, svg)
    # the label: off the bottom, onto the top of the last arrow above the row (found again: the cells changed length)
    lab = re.search(r'<text x="40" y="([\d.]+)"([^>]*)>(OUT:[^<]*)</text>', svg)
    arrows = list(re.finditer(r'<path d="M([\d.]+),([\d.]+) L\1,([\d.]+)" stroke="#6b6a60"[^>]*/>', svg))
    arrows = [a for a in arrows if float(a.group(3)) <= row_y]
    svg = svg[:lab.start()] + svg[lab.end():]
    if arrows:
        a = arrows[-1]; x, y0, y1 = float(a.group(1)), float(a.group(2)), float(a.group(3))
        moved = (f'<text x="{x:g}" y="{y0 + 8:g}" text-anchor="middle" paint-order="stroke" stroke="#fffff8" stroke-width="5" stroke-linejoin="round"{lab.group(2)}>{lab.group(3)}</text>'
                 + a.group(0).replace(f'M{a.group(1)},{a.group(2)}', f'M{a.group(1)},{y0 + 16:g}', 1))
        svg = svg[:a.start()] + moved + svg[a.end():]
    return svg


def label_bands(svg):
    """Stage labels (the small-caps headings such as "IN: THE COPPER...") drawn last, on a band of
    the page's colour, so the curves pass under them instead of through them (issue #91)."""
    labels = list(re.finditer(r'<text[^>]*letter-spacing="1.4" font-weight="600"[^>]*>[^<]*</text>', svg))
    if not labels:
        return svg
    for m in reversed(labels):
        svg = svg[:m.start()] + svg[m.end():]
    band = ('<defs><filter id="lbl-band" x="-0.02" y="-0.4" width="1.04" height="1.8">'
            '<feFlood style="flood-color:var(--paper)" result="bg"/>'
            '<feMerge><feMergeNode in="bg"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>')
    tops = "".join(m.group(0).replace("<text ", '<text filter="url(#lbl-band)" ', 1) for m in labels)
    i = svg.rfind("</svg>")
    return svg[:i] + band + tops + svg[i:]


def cribmap_figure(tag):
    """The experiment's crib map, if one has been drawn (figures/NNNN-cribmap.svg), wide, with its
    notes in short blocks underneath."""
    num = tag[:4]
    svg_p = ROOT / "figures" / f"{num}-cribmap.svg"
    if not svg_p.exists():
        return ""
    svg = svg_p.read_text()
    # draw it at the panels' letter size: the figures' cells are 8.2 x 12 units with 7.5-unit letters,
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    if m:
        # trim the empty side margins: the drawing spans x 26 to 970 of the 1000-unit canvas
        vx, vw = 26, 944
        svg = svg.replace(m.group(0), f'viewBox="{vx} 0 {vw} {m.group(2)}"', 1)
        w_, h_ = vw * FIG_SCALE, float(m.group(2)) * FIG_SCALE
        svg = re.sub(r'(<svg[^>]*?)\swidth="[^"]*"\s+height="[^"]*"', rf'\1 width="{w_:.0f}" height="{h_:.0f}"', svg, count=1)
    # which known places the best reading actually produced (issue #49)
    r = {x["tag"]: x for x in load_results()}.get(tag)
    hits = None
    if r is not None and r.get("best_crib_hits", 0) < 24:
        from kryptos.facts import KNOWN as _K
        b = best_candidate(r)
        pt = (b or {}).get("plaintext") or ""
        hits = {q for q, ch in _K.items() if len(pt) >= q and pt[q - 1] == ch}
    svg = cribmap_out_row(svg, hits)
    # the "IN:" heading sits above the copper row at the left edge; put it on the input arrow, centred,
    # the same way the OUT label sits on the output arrow
    inl = re.search(r'<text x="40" y="22"([^>]*)>(IN:[^<]*)</text>', svg)
    if inl:
        svg = svg[:inl.start()] + svg[inl.end():]
        a = next(iter(re.finditer(r'<path d="M([\d.]+),([\d.]+) L\1,([\d.]+)" stroke="#6b6a60"[^>]*/>', svg)), None)
        if a:
            x, y0 = float(a.group(1)), float(a.group(2))
            moved = (f'<text x="{x:g}" y="{y0 + 8:g}" text-anchor="middle"{inl.group(1)}>{inl.group(2)}</text>'
                     + a.group(0).replace(f'M{a.group(1)},{a.group(2)}', f'M{a.group(1)},{y0 + 16:g}', 1))
            svg = svg[:a.start()] + moved + svg[a.end():]
    svg = label_bands(svg)
    notes_p = ROOT / "figures" / f"{num}-cribmap-notes.json"
    notes = json.loads(notes_p.read_text()) if notes_p.exists() else []
    below = "".join(f'<div class="fig-note"><b>{esc(n.get("anchor", ""))}</b><p>{crib_cells(esc(n.get("text", "")))}</p></div>' for n in notes)
    return (f'<div class="fig-row"><figure class="fig-main"><div class="fig-scroll">{svg}</div></figure>'
            f'<div class="fig-notes">{below}</div></div>')


def worksheet_figure(tag):
    """The experiment's worksheet (figures/NNNN-worksheet.svg), drawn at the same scale as the crib
    map, under the walkthrough it illustrates."""
    p = ROOT / "figures" / f"{tag[:4]}-worksheet.svg"
    if not p.exists():
        return ""
    svg = p.read_text()
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    if m:
        vx, vw = 26, 948                     # the sheet spans x 30 to 970 of the 1000-unit canvas
        svg = svg.replace(m.group(0), f'viewBox="{vx} 0 {vw} {m.group(2)}"', 1)
        w_, h_ = vw * FIG_SCALE, float(m.group(2)) * FIG_SCALE
        svg = re.sub(r'(<svg[^>]*?)\swidth="[^"]*"\s+height="[^"]*"', rf'\1 width="{w_:.0f}" height="{h_:.0f}"', svg, count=1)
    svg = label_bands(svg)
    return (f'<div class="fig-row ws"><figure class="fig-main"><figcaption class="fig-eyebrow">the worksheet: the first steps by hand, on squared paper</figcaption>'
            f'<div class="fig-scroll">{svg}</div></figure></div>')


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
    kl = kept_loss(r)
    shown_loss = kl if kl is not None else r.get("best_loss")
    loss_note = ""
    if kl is not None and r.get("best_loss") is not None and r["best_loss"] < kl - 1e-9:
        loss_note = f"; its lowest candidate scored {pct(r['best_loss'])} ({r['best_loss']:.1f}), but the rule then in force, highest fitness, kept this one"
    dec_html = f'<span class="{esc(decision)}">{esc(decision)}</span>'
    facts = f"Family {esc(fam_num)}, {esc(fam_label)}. Decision: {dec_html}." + (f" Run {esc(started)}." if started else "")
    meta = f"""<div class="meta-row" style="grid-template-columns:repeat(5,1fr);border-bottom:none">
<div><b class="{esc(decision)}">{esc(decision)}</b><span>status</span></div>
<div><b>{parent_html}</b><span>parents</span></div>
<div><b>{fmt_dur(total)}</b><span>time, all phases</span></div>
<div><b>{r['n_candidates']}</b><span>candidates</span></div>
<div><b>{r['best_crib_hits']}/24</b><span>known letters</span></div>
</div>
<div class="meta-time">{phase_bar(ph if ph else {'run': r.get('seconds', 0)}, total or 1, width=980, height=8).replace('<svg width="980" height="8"', '<svg viewBox="0 0 980 8" preserveAspectRatio="none"', 1)}</div>"""
    note = meta + (f'<p class="verdict-note">Kept when it ran, under the rule of the time. Under the current rules it is not: '
                   f'{esc(r["verdict_note"])}.</p>' if r.get("verdict_note") else "")
    head = page_head(f"Experiment {num}", f'<span class="exp-q">&ldquo;{esc(r["title"])}&rdquo;</span>', esc(changed), "", note)
    # section 1: plain words with the glossary rail
    eli5 = r.get("eli5") or ""
    low = eli5.lower()
    found = []   # (start, end, term_id, term, definition)
    for k, (term, names, definition) in enumerate(load_glossary()):
        hit = None
        for n in names:
            m = _re.search(r"(?<![a-z])" + _re.escape(n.lower()) + r"(?![a-z])", low)
            if m and (hit is None or m.start() < hit[0]):
                hit = (m.start(), m.end())
        if hit:
            found.append((hit[0], hit[1], f"g{k}", term, definition))
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
        out.append(f'<span class="gl" data-gl="{gid}">{esc(eli5[st:en])}</span>'
                   f'<span class="sidenote gl-entry" data-gl="{gid}"><b>{esc(term)}</b> {esc(first_sentence(definition))}</span>')
        pos = en
    out.append(esc(eli5[pos:]))
    eli5_html = "<p>" + "".join(out).replace("\n\n", "</p><p>") + "</p>"
    # Tufte sidenotes: each word's definition sits in the margin beside the line where it appears
    more = '<p class="sidenote-more">Words in the margin are defined on the <a href="/glossary">glossary</a> page.</p>' if kept else ""
    cm = cribmap_figure(tag)
    off = 1
    lin = lineage_section(2, tag)
    plain = (sec(1, "The experiment method", "What the method does with the 24 known letters.")
             + f'<div class="plain tufte">{eli5_html}{more}</div>'
             + ('<div class="subsec"><b>1.1</b><h3>The method at work</h3></div>'
                '<p class="subsec-sub">The carved letters go in at the top; the reading comes out at the bottom.</p>' + cm if cm else ""))
    # section 2: best candidate
    cand = ""
    if best:
        how = "the lowest-loss reading that passed the original gates" if best.get("gate_passed") else "the candidate with most known letters right; none passed every gate"
        cand = sec(2 + off, "Best candidate against the known letters", f"Laid out as the copper carries K4: OBKR ends the line that finishes K3, then three lines of 31. Left, as carved, the 24 known places in accent. Right, the candidate: a known place it gets right is an accent cell, one it misses is outlined. This is {how}.") + panel_block(K4, best["plaintext"], KNOWN).replace('class="panel-wrap"', 'class="panel-wrap wide"', 1)
    else:
        cand = sec(2 + off, "Best candidate against the known letters", "This experiment produced no candidate: the search ruled everything out before a full text was built. Its product is the bounded negative under Result and bounds below.")
    # remaining sections from the record, numbered
    order = [("Walkthrough, by hand", "Walkthrough, by hand", "Redo the method on a few letters with pencil and paper."),
             ("Worked example (generated)", "Worked example, generated", "The same steps run by the code on the real letters."),
             ("Hypothesis (domain expert)", "Hypothesis, for a cryptanalyst", "Family, key space, the constraint under test, and the clues it reads."),
             ("Prediction", "Prediction", "Written before the run; the result decides it."),
             ("Method", "Method", ""),
             ("Result", "Result and bounds", "The harness's record: candidates, gates, loss, and the negative result this experiment leaves behind.")]
    body = [head, plain, lin, cand]
    n = 3 + off
    sc = score_section(n, r, best)
    if sc:
        body.append(sc); n += 1
    for key, title, sub in order:
        content = section(key)
        if not content:
            continue
        if key == "Result":
            notes = r.get("notes") or ""
            err = r.get("error") or ""
            html_c = (result_section_html(r, tags, KNOWN)
                      + (f'<p class="res-notes">{link_experiments(esc(notes), tags)}</p>' if notes else "")
                      + (f'<p class="res-notes err">The run stopped with an error: <code>{esc(err.splitlines()[-1] if err else "")}</code></p>' if err else "")
                      + bounds_html(r.get("bounds")))
        else:
            html_c = md(content)
            html_c = link_experiments(html_c, tags)
        extra = worksheet_figure(tag) if key == "Walkthrough, by hand" else ""
        body.append(sec(n, title, sub) + f'<article class="rec-body">{html_c}</article>' + extra)
        n += 1
    body.append(page_foot('How this experiment sits among the others is on the <a href="/lineage">lineage</a> page; its family\'s open hypotheses are on the <a href="/families">families</a> page.'))
    return page(f"experiment {num}", "".join(body))


LIN_CSS = """
.lin{--f0:#3d6b8c;--f1:#8a6a1e;--f2:#5b7f4a;--f3:#7a4f86;--f4:#b0603a;--f5:#2f7f7a;--f6:#9a5470;--f7:#5c5a8f;--f8:#7d7a3a;--f9:#6b6a60}
@media(prefers-color-scheme:dark){.lin{--f0:#7fa8c9;--f1:#c9a227;--f2:#8fb87a;--f3:#b48cc0;--f4:#e0936b;--f5:#6cbfb8;--f6:#d08aa6;--f7:#9a98d0;--f8:#bdb86a;--f9:#a39f90}}
.lin .f0{color:var(--f0)}.lin .f1{color:var(--f1)}.lin .f2{color:var(--f2)}.lin .f3{color:var(--f3)}.lin .f4{color:var(--f4)}
.lin .f5{color:var(--f5)}.lin .f6{color:var(--f6)}.lin .f7{color:var(--f7)}.lin .f8{color:var(--f8)}.lin .f9{color:var(--f9)}
.lin-head{max-width:980px;margin:0 auto}
.lin-head h1{font:400 34px/1.18 var(--serif);margin:18px 0 10px;letter-spacing:-.005em}
.lin-head .standfirst{max-width:760px}
.lin-box{position:relative;width:calc(100vw - 32px);margin:16px 0 0 calc(50% - 50vw + 16px);border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)}
#lin-heads{position:sticky;top:0;z-index:5;overflow:hidden;background:var(--paper);border-bottom:1px solid var(--rule)}
#lin-lanes{position:relative;will-change:transform}
#lin-diagram{overflow-x:auto;scrollbar-width:thin;scrollbar-color:var(--rule) transparent}
#lin-diagram::-webkit-scrollbar{height:6px}#lin-diagram::-webkit-scrollbar-thumb{background:var(--rule);border-radius:3px}
.lane-lab{position:absolute;top:0;bottom:0;padding:9px 8px 8px 10px;cursor:default;font:600 10.5px/1.3 var(--serif);font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);border-left:1px solid var(--rule-soft);overflow-wrap:break-word;hyphens:auto}
.lane-lab:first-child{border-left:0}
.lane-lab .sw{position:absolute;left:10px;top:12px;width:8px;height:8px;border-radius:50%;background:currentColor}.lane-lab .nm{display:block;text-indent:14px}
.lane-lab .cnt{display:block;color:var(--faint);font-weight:400;margin-top:2px;font-variant-numeric:lining-nums tabular-nums}
#lin{display:block}
#lin .lband{fill:currentColor;fill-opacity:.05}
#lin .lbound{stroke:var(--rule-soft);stroke-width:1}
#lin .lbase{stroke:var(--rule-soft);stroke-width:1}
#lin .lrow{stroke:var(--rule-soft);stroke-width:1;shape-rendering:crispEdges}
#lin .lpivot-lab{font:italic 400 10.5px var(--serif);fill:var(--accent);letter-spacing:.01em;paint-order:stroke;stroke:var(--paper);stroke-width:4px;stroke-linejoin:round}
#lin .lpivot-row{fill:var(--paper)}
#lin .lrow.ten{stroke:var(--rule);stroke-opacity:.6}
#lin .lrow.lit-direct{stroke:var(--muted);stroke-opacity:.45}
#lin .rhit{fill:var(--ink);fill-opacity:0;transition:fill-opacity .12s}
#lin .rhit.on{fill-opacity:.05}
#lin .lrow.row-on{stroke:var(--muted);stroke-opacity:.5}
#lin .ng.row-on .nlab{fill:var(--ink);font-weight:600}
#lin .edge{fill:none;stroke:var(--disc);stroke-width:1}
#lin .edge.x{stroke-dasharray:3 3}
#lin .ehit{fill:none;stroke:transparent;stroke-width:7;pointer-events:stroke}
#lin .ng{cursor:pointer;outline:none}
#lin .nr{fill:currentColor}
#lin .nk{fill:var(--ink)}
#lin .nwas{fill:none;stroke:var(--ink);stroke-width:1.3;stroke-dasharray:2 2}
#lin .ne{stroke:var(--accent);stroke-width:1.8;stroke-linecap:round}
#lin .ntitle{fill:var(--muted);font:12.5px/1 var(--serif)}
#lin .ng.row-on .ntitle{fill:var(--ink);font-weight:600}
#lin .nlab{fill:var(--faint);font:9.5px/1 var(--serif);font-variant-numeric:lining-nums tabular-nums}
#lin .ng:focus-visible .hit{stroke:var(--accent);stroke-width:1.5}
#lin .ng.lit .nlab,#lin .ng.lit-direct .nlab{fill:var(--ink)}
#lin .edge.lit,#lin .edge.lit-direct{stroke:var(--ink);stroke-width:2}
#lin-tip{position:fixed;z-index:30;pointer-events:none;opacity:0;transition:opacity .1s;background:var(--paper);color:var(--ink);border:1px solid var(--rule);border-radius:3px;font:13px/1.45 var(--serif);padding:12px 14px;max-width:min(430px,calc(100vw - 24px))}
#lin-tip:has(.pop-mini){display:flex;gap:18px;max-width:min(640px,calc(100vw - 24px))}#lin-tip .pop-main{flex:1;min-width:0}
#lin-tip .pop-mini{flex:none;width:150px;padding-left:16px;border-left:1px solid var(--rule-soft)}#lin-tip .pop-mini svg{display:block}
@media(max-width:640px){#lin-tip .pop-mini{display:none}}
#lin-tip .pop-title{font-weight:700;font-size:14.5px;line-height:1.25;margin-bottom:3px}
#lin-tip .pop-meta{color:var(--muted);font:600 10.5px/1.3 var(--serif);font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.05em;margin-bottom:9px}
#lin-tip .pop-h{font:600 10px/1 var(--serif);font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.07em;color:var(--faint);margin-bottom:4px}
#lin-tip p{margin:0;font:italic 13px/1.5 var(--serif);color:var(--muted)}
#lin-tip .pop-sec+.pop-sec{margin-top:10px}
#lin-tip .pop-parent{font:600 11px/1.35 var(--serif);font-feature-settings:"smcp" 1;text-transform:uppercase;letter-spacing:.03em;color:var(--accent)}
.lin-box.fit{width:min(980px,calc(100vw - 32px));margin:16px 0 0 max(0px,calc((100% - 980px) / 2))}
.lin-foot{max-width:980px;margin:12px auto 0;font-size:13.5px;color:var(--muted)}
@media(max-width:640px){.lin-head h1{font-size:26px}.lin-box{width:calc(100vw - 32px);margin-left:2px}.lane-lab{padding:8px 5px 7px 7px;font-size:9.5px;letter-spacing:.03em}.lane-lab .sw{left:7px;top:11px;width:7px;height:7px}.lane-lab .nm{text-indent:11px}.lane-lab .cw{display:none}}
"""

LIN_JS = r"""
<script>
(function(){
  var data={};try{data=JSON.parse(document.getElementById('lin-data').textContent||'{}');}catch(e){}
  var nodes=data.nodes||[],fams=data.families||[],pivots=data.pivots||[];
  var host=document.getElementById('lin-diagram'),lanesEl=document.getElementById('lin-lanes'),tip=document.getElementById('lin-tip');
  if(!host)return;
  if(!nodes.length){host.innerHTML='<p class="muted">No experiments yet.</p>';return;}
  var esc=function(s){return String(s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});};
  var byKey={};nodes.forEach(function(n){byKey[n.key]=n;});
  var short=function(t,n){if(t.length<=n)return t;var c=t.slice(0,n);return c.slice(0,c.lastIndexOf(' '))+'...';};
  var parentOf=function(k){var p=byKey[k]&&byKey[k].parent;return p&&byKey[p]?p:null;};
  var kids={};nodes.forEach(function(n){var p=parentOf(n.key);if(p)(kids[p]=kids[p]||[]).push(n.key);});
  var svg=null,geo=null,shownKey=null,lastPointer='mouse';

  // Geometry: y is run order, one column per family. Each column has a gutter for the
  // experiment numbers, then the line of dots; same-family arcs bulge right into the rest
  // of the column, never wider than the column allows.
  function layout(){
    var n=nodes.length,nf=fams.length,padY=data.current?20:16,sp=data.current?22:16,MINCOL=data.current?120:112,NUMW=30;
    var avail=host.clientWidth||1000;
    var y={},cols=[],py={},slot=0;
    var pAfter={};pivots.forEach(function(pv){pAfter[pv.after]=pv;});
    // a pivot takes a row of its own, right after the experiment it followed
    nodes.forEach(function(nd){y[nd.key]=padY+slot*sp;slot++;if(pAfter[nd.key]){py[pAfter[nd.key].id]=padY+slot*sp;slot++;}});
    var n=slot,L=lanes(y,sp);
    // a column is as wide as its lanes need, at least MINCOL; spare width is shared out evenly
    var need=fams.map(function(f,i){var word=data.current?Math.max.apply(null,f.label.split(' ').map(function(w){return w.length;}))*9.6+22:0;
      return Math.max(MINCOL,word,NUMW+6+LANE*(L.nl[i]||0)+12);}),tot=need.reduce(function(s,v){return s+v;},0),
        extra=data.current?0:Math.max(0,(avail-tot)/nf),left=0;
    fams.forEach(function(f,i){var w=need[i]+extra;cols.push({left:left,x:left+NUMW,w:w});left+=w;});
    // on an experiment's page the rest of the width names each experiment of the line
    var tl=left;if(data.current)left+=Math.max(240,avail-left);
    return {sp:sp,tl:tl,W:Math.floor(left),H:Math.ceil(2*padY+(n-1)*sp),y:y,py:py,cols:cols,padY:padY,laneOf:L.laneOf};
  }

  // Lanes: a same-family edge that skips an experiment gets a lane of its own beside the column.
  // Lanes are packed left-edge style (the channel router's rule), shortest span innermost, so
  // nested edges never cross and no two edges ever share a lane where they overlap.
  var LANE=5;
  // a parent directly above its child, with no experiment of the family between them, gets a
  // straight edge and no lane
  function direct(nd,p,y){var a=y[p],b=y[nd.key];return !nodes.some(function(o){return o.fam===nd.fam&&y[o.key]>a&&y[o.key]<b;});}
  // An edge to another family that spans four rows or more also takes a lane, in its parent's
  // column, and sweeps across to the child only at the end.
  function crossLane(nd,p,y,sp){return byKey[p].fam!==nd.fam&&y[nd.key]-y[p]>=4*sp;}
  function lanes(y,sp){
    var GAP=sp*0.4,busy={},laneOf={},nl={};
    nodes.filter(function(nd){var p=parentOf(nd.key);return p&&(byKey[p].fam===nd.fam?!direct(nd,p,y):crossLane(nd,p,y,sp));})
      .map(function(nd){var p=parentOf(nd.key);return {k:nd.key,f:byKey[p].fam,a:y[p],b:y[nd.key]};})
      .sort(function(u,v){return (u.b-u.a)-(v.b-v.a)||u.a-v.a;})
      .forEach(function(r){var iv=busy[r.f]||(busy[r.f]=[]),l=0;
        while(iv.some(function(q){return q.l===l&&q.a<r.b+GAP&&r.a<q.b+GAP;}))l++;
        iv.push({l:l,a:r.a,b:r.b});laneOf[r.k]=l;nl[r.f]=Math.max(nl[r.f]||0,l+1);});
    return {laneOf:laneOf,nl:nl};
  }

  function render(){
    geo=layout();
    var y=geo.y,cols=geo.cols,W=geo.W,H=geo.H,g='';
    var xOf=function(k){return cols[byKey[k].fam].x;};
    if(data.current)g+='<line class="lbound" x1="'+geo.tl.toFixed(1)+'" x2="'+geo.tl.toFixed(1)+'" y1="0" y2="'+H+'"/>';
    cols.forEach(function(C,i){
      g+='<rect class="lband f'+fams[i].c+'" x="'+C.left.toFixed(1)+'" y="0" width="'+C.w.toFixed(1)+'" height="'+H+'"/>';
      if(i)g+='<line class="lbound" x1="'+C.left.toFixed(1)+'" x2="'+C.left.toFixed(1)+'" y1="0" y2="'+H+'"/>';
    });
    // one faint rule per experiment across every column, so the sequence can be followed
    // from one family to the next; every tenth is a little stronger
    nodes.forEach(function(nd){var ty=y[nd.key],ten=typeof nd.n==='number'&&nd.n%10===0;
      g+='<rect class="rhit" data-key="'+esc(nd.key)+'" x="0" y="'+(ty-geo.sp/2)+'" width="'+W+'" height="'+geo.sp+'"/>'
        +'<line class="lrow'+(ten?' ten':'')+'" data-key="'+esc(nd.key)+'" x1="0" x2="'+W+'" y1="'+ty+'" y2="'+ty+'"/>';});
    // pivots: a plain paper row of their own, drawn over the bands and rules but under the edges
    // and dots, so the lineage stays visible across it
    pivots.forEach(function(pv){if(!(pv.id in geo.py))return;var cy=geo.py[pv.id],h=geo.sp;
      g+='<a href="/pivot/'+encodeURIComponent(pv.id)+'"><rect class="lpivot-row" x="0" y="'+(cy-h/2)+'" width="'+W+'" height="'+h+'"/>'
        +'</a>';});
    cols.forEach(function(C){g+='<line class="lbase" x1="'+C.x.toFixed(1)+'" x2="'+C.x.toFixed(1)+'" y1="'+geo.padY+'" y2="'+(H-geo.padY)+'"/>';});
    // edges, routed like tracks in a channel (a circuit board, a metro map): crossings are
    // allowed, overlaps are not. Each edge leaves the bottom centre of the parent and arrives at
    // the top centre of the child; a same-family edge runs in its own lane (see lanes()). The
    // edges leaving one dot are its ports: they fan out at evenly spread angles, inner lanes
    // steepest, then the lanes further out, then edges to other families, so they part at once
    // and never touch again. An arrival into a lane-routed child mirrors its departure.
    var R=4,H0=geo.sp*0.4,laneOf=geo.laneOf,yy=y,ang={};
    var f1=function(v){return v.toFixed(1);};
    var same=function(nd,p){return byKey[p].fam===nd.fam;};
    Object.keys(kids).forEach(function(p){
      var out=kids[p].filter(function(c){return !(same(byKey[c],p)&&direct(byKey[c],p,yy));});
      // sideways reach of each port: a lane's offset, or how far the other column lies
      var reach=function(c){return c in laneOf?6+LANE*laneOf[c]:xOf(c)-xOf(p);};
      [out.filter(function(c){return reach(c)>0;}),out.filter(function(c){return reach(c)<0;})].forEach(function(side){
        side.sort(function(u,v){return Math.abs(reach(u))-Math.abs(reach(v));});
        side.forEach(function(c,i){ang[c]=(side.length<2?40:25+45*i/(side.length-1))*Math.PI/180;});});
    });
    nodes.forEach(function(nd){
      var p=parentOf(nd.key);if(!p)return;
      var a=y[p],b=y[nd.key],a0=a+R,b0=b-R,d,t=ang[nd.key];
      if(same(nd,p)&&direct(nd,p,yy)){var xs=f1(xOf(nd.key));
        g+='<path class="edge" data-c="'+esc(nd.key)+'" data-p="'+esc(p)+'" d="M'+xs+','+a0+' L'+xs+','+b0+'"/>';}
      else if(same(nd,p)){var x=xOf(nd.key),o=6+LANE*laneOf[nd.key],lx=x+o,xh=x+0.35*o,
          q=o/Math.tan(t),h=Math.max(4,Math.min((b0-a0)/2,1.8*q+4)),k1=Math.min(0.45,0.45*h/Math.max(q,1e-6));
        // out of the port at its angle, easing into the lane over a drop longer than the reach,
        // so the bend is spread along the curve rather than a knee; the arrival is its reflection
        xh=x+k1*o;
        d='M'+f1(x)+','+a0+' C'+f1(xh)+','+f1(a0+k1*q)+' '+f1(lx)+','+f1(a0+0.4*h)+' '+f1(lx)+','+f1(a0+h)
          +' L'+f1(lx)+','+f1(b0-h)
          +' C'+f1(lx)+','+f1(b0-0.4*h)+' '+f1(xh)+','+f1(b0-k1*q)+' '+f1(x)+','+b0;
        g+='<path class="edge" data-c="'+esc(nd.key)+'" data-p="'+esc(p)+'" d="'+d+'"/>';}
      else if(nd.key in laneOf){var xa=xOf(p),xc=xOf(nd.key),o=6+LANE*laneOf[nd.key],lx=xa+o,
          q=o/Math.tan(t),h=Math.max(4,Math.min((b0-a0)/3,1.8*q+4)),k1=Math.min(0.45,0.45*h/Math.max(q,1e-6)),
          S=Math.min(b0-a0-h,Math.max(2*geo.sp,Math.min(10*geo.sp,0.3*Math.abs(xc-lx))));
        // to another family, far down: out of its port into a lane beside the parent's column,
        // as a same-family edge does, then an S across into the top of the child
        d='M'+f1(xa)+','+a0+' C'+f1(xa+k1*o)+','+f1(a0+k1*q)+' '+f1(lx)+','+f1(a0+0.4*h)+' '+f1(lx)+','+f1(a0+h)
          +' L'+f1(lx)+','+f1(b0-S)
          +' C'+f1(lx)+','+f1(b0-S/2)+' '+f1(xc)+','+f1(b0-S/2)+' '+f1(xc)+','+b0;
        g+='<path class="edge x" data-c="'+esc(nd.key)+'" data-p="'+esc(p)+'" d="'+d+'"/>';}
      else{var xa=xOf(p),xc=xOf(nd.key),dx=xc-xa,k=Math.min(2.5*H0,(b0-a0)/3);
        // to another family, a row or two down: out of its port at the port's angle, then one
        // curve into the top of the child
        d='M'+f1(xa)+','+a0+' C'+f1(xa+(dx<0?-1:1)*k*Math.sin(t))+','+f1(a0+k*Math.cos(t))+' '+f1(xc-0.2*dx)+','+f1(b0-H0)+' '+f1(xc)+','+b0;
        g+='<path class="edge x" data-c="'+esc(nd.key)+'" data-p="'+esc(p)+'" d="'+d+'"/>';}
    });
    nodes.forEach(function(nd){
      var cx=xOf(nd.key).toFixed(1),cy=y[nd.key],k=esc(nd.key),m='';
      if(nd.decision==='kept')m='<circle class="nk" cx="'+cx+'" cy="'+cy+'" r="5"/>';
      else if(nd.decision==='reverted')m='<circle class="nr" cx="'+cx+'" cy="'+cy+'" r="3.6"/>';
      else{var c=parseFloat(cx),s=3.6;m='<path class="ne" d="M'+(c-s)+','+(cy-s)+' L'+(c+s)+','+(cy+s)+' M'+(c+s)+','+(cy-s)+' L'+(c-s)+','+(cy+s)+'"/>';}
      if(nd.recorded==='kept'&&nd.decision!=='kept')m+='<circle class="nwas" cx="'+cx+'" cy="'+cy+'" r="7.5"/>';
      g+='<a class="ng f'+fams[nd.fam].c+(nd.key===data.current?' row-on':'')+'" data-key="'+k+'" href="/exp/'+encodeURIComponent(nd.key)+'" target="_blank" rel="noopener" aria-label="'+esc(nd.n+': '+nd.title)+'">'+m
        +'<circle class="hit" cx="'+cx+'" cy="'+cy+'" r="10" fill="transparent"/>'
        +'<text class="nlab" x="'+(parseFloat(cx)-10)+'" y="'+(cy+3.3)+'" text-anchor="end">'+nd.n+'</text>'
        +(data.current?'<text class="ntitle" x="'+(geo.tl+12)+'" y="'+(cy-3)+'">'+esc(short(nd.title,Math.floor((W-geo.tl-24)/6.4)))+'</text>':'')+'</a>';
    });
    pivots.forEach(function(pv){if(!(pv.id in geo.py))return;
      var ty=geo.py[pv.id];
      var W2=geo.W;
      g+='<a href="/pivot/'+encodeURIComponent(pv.id)+'"><path d="M'+(W2-15)+','+(ty-2.8)+' L'+(W2-8)+','+(ty-2.8)+' L'+(W2-11.5)+','+(ty+2.8)+' z" fill="var(--accent)"/>'
        +'<text class="lpivot-lab" x="'+(W2-20)+'" y="'+(ty+3.6)+'" text-anchor="end">'+esc(pv.label)+'</text></a>';});
    host.innerHTML='<svg id="lin" width="'+W+'" height="'+H+'" viewBox="0 0 '+W+' '+H+'">'+g+'</svg>';
    svg=document.getElementById('lin');
    lanesEl.style.width=W+'px';lanesEl.style.height='';
    lanesEl.innerHTML=cols.map(function(C,i){var f=fams[i];
      return '<div class="lane-lab f'+f.c+'" data-fam="'+i+'" title="'+esc(f.name)+'" style="left:'+C.left.toFixed(1)+'px;width:'+C.w.toFixed(1)+'px"><span class="sw"></span><span class="nm">'+esc(f.label)+'</span>'
        +'<span class="cnt">'+f.count+'<span class="cw">'+(f.count===1?' experiment':' experiments')+'</span></span></div>';}).join('')
      +(data.current?'<div class="lane-lab" style="left:'+geo.tl.toFixed(1)+'px;width:'+(W-geo.tl).toFixed(1)+'px"><span class="nm" style="text-indent:0">experiment</span><span class="cnt">'+nodes.length+' in this line</span></div>':'');
    // the heads are absolutely placed, so the strip takes the height of the tallest one
    var hh=0;lanesEl.querySelectorAll('.lane-lab').forEach(function(el){el.style.bottom='auto';hh=Math.max(hh,el.offsetHeight);el.style.bottom='';});
    lanesEl.style.height=hh+'px';syncHeads();
  }
  // On a narrow screen the figure scrolls sideways; the sticky heads follow it.
  function syncHeads(){lanesEl.style.transform='translateX('+(-host.scrollLeft)+'px)';}

  function clearLit(){svg.querySelectorAll('.lit,.lit-direct').forEach(function(el){el.classList.remove('lit','lit-direct');});
}
  // On an experiment's own page every node is its line: light all of it, the experiment itself strongest
  function reset(){clearLit();if(!data.current)return;
    nodes.forEach(function(nd){mark(nd.key,nd.key===data.current?'lit-direct':'lit');});
    svg.querySelectorAll('.edge').forEach(function(e){e.classList.add('lit');});}
  function mark(k,cls){var el=svg.querySelector('.ng[data-key="'+CSS.escape(k)+'"]');if(el)el.classList.add(cls);}
  // Trace a node's line back to its root, every ancestor and edge in full.
  function lit(key){
    clearLit();
    var chain=[key],cur=key;while((cur=parentOf(cur))&&chain.indexOf(cur)<0)chain.push(cur);
    chain.forEach(function(k,i){mark(k,i<2?'lit-direct':'lit');});
    var row=svg.querySelector('.lrow[data-key="'+CSS.escape(key)+'"]');if(row)row.classList.add('lit-direct');
    svg.querySelectorAll('.edge').forEach(function(e){var c=e.getAttribute('data-c'),i=chain.indexOf(c);
      if(i>=0&&e.getAttribute('data-p')===chain[i+1])e.classList.add(i===0?'lit-direct':'lit');});
  }
  // An edge alone: the edge and the two experiments it joins.
  function litEdge(c,p){
    clearLit();mark(c,'lit-direct');mark(p,'lit-direct');
    svg.querySelectorAll('.edge[data-c="'+CSS.escape(c)+'"]').forEach(function(e){e.classList.add('lit-direct');});
  }

  function placeTip(el){
    var r=el.getBoundingClientRect(),w=tip.offsetWidth,h=tip.offsetHeight,cx=r.left+r.width/2;
    var left=Math.max(8,Math.min(cx-w/2,window.innerWidth-w-8)),top=r.bottom+6;
    if(top+h>window.innerHeight-8)top=Math.max(8,r.top-h-6);
    tip.style.left=left+'px';tip.style.top=top+'px';
  }
  function showTip(key,el){
    var nd=byKey[key],f=fams[nd.fam],p=parentOf(key),ks=kids[key]||[];
    var verdict=nd.decision==='kept'?'kept':nd.decision==='reverted'?'reverted':esc(nd.decision||'no verdict');
    var meta='#'+nd.n+' · '+esc(f.label)+' · '+verdict+(nd.loss?' · loss '+esc(nd.loss):'')+' · '+nd.cribs+'/24 cribs';
    var html='<div class="pop-title">'+esc(nd.title)+'</div><div class="pop-meta">'+meta+'</div>';
    if(nd.summary)html+='<div class="pop-sec"><div class="pop-h">In plain words</div><p>'+esc(nd.summary)+'</p></div>';
    if(nd.note)html+='<div class="pop-sec"><div class="pop-h">Kept when it ran, reverted under today\'s rules</div><p>'+esc(nd.note)+'</p></div>';
    html+='<div class="pop-sec"><div class="pop-h">Built on</div>'+(p?'<span class="pop-parent">#'+byKey[p].n+' '+esc(short(byKey[p].title,60))+'</span>':'<p>Nothing: it starts a line.</p>')+'</div>';
    if(ks.length)html+='<div class="pop-sec"><div class="pop-h">Built on by</div><p>'+ks.map(function(k){return '#'+byKey[k].n;}).join(', ')+'</p></div>';
    if(!data.current)html='<div class="pop-main">'+html+'</div>'+minimap(key);
    tip.innerHTML=html;tip.style.opacity='1';shownKey=key;placeTip(el);
  }
  // The whole lineage in miniature beside the popover: family bands, every experiment a dot, the
  // hovered experiment's line back to its root in ink, and a frame for the part on screen, so the
  // line can be seen whole without scrolling away from it.
  function minimap(key){
    var w=150,h=250,pad=4,sx=w/geo.W,sy=(h-2*pad)/geo.H,X=function(k){return (geo.cols[byKey[k].fam].x*sx).toFixed(1);},Y=function(k){return (pad+geo.y[k]*sy).toFixed(1);},m='';
    geo.cols.forEach(function(C,i){m+='<rect class="f'+fams[i].c+'" x="'+(C.left*sx).toFixed(1)+'" y="0" width="'+Math.max(1,C.w*sx-1).toFixed(1)+'" height="'+h+'" fill="currentColor" fill-opacity=".07"/>';});
    // the part on screen: a soft shaded area under the marks, inside the map, following both scrolls
    var r=svg.getBoundingClientRect(),v0=Math.max(0,-r.top),v1=Math.min(geo.H,window.innerHeight-r.top),
        x0=Math.max(0,-r.left)+0,x1=Math.min(geo.W,window.innerWidth-r.left);
    if(v1>v0&&x1>x0){var fx=Math.max(1,x0*sx),fw=Math.min(w-1,x1*sx)-fx,fy=Math.max(1,pad+v0*sy-2),fh=Math.min(h-1,pad+v1*sy+2)-fy;
      m+='<rect x="'+fx.toFixed(1)+'" y="'+fy.toFixed(1)+'" width="'+Math.max(4,fw).toFixed(1)+'" height="'+Math.max(4,fh).toFixed(1)+'" rx="3" fill="var(--ink)" fill-opacity=".07" stroke="var(--muted)" stroke-opacity=".45" stroke-width="1"/>';}
    nodes.forEach(function(nd){m+='<circle cx="'+X(nd.key)+'" cy="'+Y(nd.key)+'" r=".9" fill="var(--faint)" fill-opacity=".7"/>';});
    var chain=[key],cur=key;while((cur=parentOf(cur))&&chain.indexOf(cur)<0)chain.push(cur);
    // the line's own edges, the same curves as the diagram scaled down: solid within a family, dotted across
    var e='';
    chain.forEach(function(k,i){if(!i&&chain.length<2)return;var p=chain[i+1];if(!p)return;
      var el=svg.querySelector('.edge[data-c="'+CSS.escape(k)+'"][data-p="'+CSS.escape(p)+'"]');if(!el)return;
      e+='<path d="'+el.getAttribute('d')+'" fill="none" stroke="var(--ink)" stroke-width="1.2" vector-effect="non-scaling-stroke"'+(el.classList.contains('x')?' stroke-dasharray="1.6 1.6"':'')+'/>';});
    m+='<g transform="translate(0,'+pad+') scale('+sx.toFixed(5)+','+sy.toFixed(5)+')">'+e+'</g>';
    chain.forEach(function(k,i){if(i)m+='<circle class="f'+fams[byKey[k].fam].c+'" cx="'+X(k)+'" cy="'+Y(k)+'" r="1.8" fill="currentColor"/>';});
    m+='<circle cx="'+X(key)+'" cy="'+Y(key)+'" r="3.2" fill="var(--ink)"/>';
    return '<div class="pop-mini"><div class="pop-h">Its line in the whole lineage</div><svg width="'+w+'" height="'+h+'" viewBox="0 0 '+w+' '+h+'">'+m+'</svg></div>';
  }
  function hideTip(){tip.style.opacity='0';shownKey=null;}

  // A light band across every column marks the row under the pointer, so the sequence can
  // be read across families; it never dims the rest.
  var rowOn=null;
  function rowHi(key){
    if(rowOn===key)return;
    if(rowOn)svg.querySelectorAll('.row-on,.rhit.on').forEach(function(el){if(el.getAttribute('data-key')!==data.current||!el.classList.contains('ng'))el.classList.remove('row-on','on');});
    rowOn=key;if(!key)return;
    var q='[data-key="'+CSS.escape(key)+'"]';
    var b=svg.querySelector('.rhit'+q),l=svg.querySelector('.lrow'+q),n=svg.querySelector('.ng'+q);
    if(b)b.classList.add('on');if(l)l.classList.add('row-on');if(n)n.classList.add('row-on');
  }
  function rowAt(e){
    var r=svg.getBoundingClientRect(),yy=e.clientY-r.top,best=null,bd=geo.sp/2+0.01;
    nodes.forEach(function(nd){var d=Math.abs(yy-geo.y[nd.key]);if(d<bd){bd=d;best=nd.key;}});
    return best;
  }
  function wire(){
    rowOn=null;
    svg.addEventListener('mousemove',function(e){rowHi(rowAt(e));});
    svg.addEventListener('mouseleave',function(){rowHi(null);});
    svg.addEventListener('pointerdown',function(e){lastPointer=e.pointerType||'mouse';});
    // a wider, invisible copy of each edge to hover; drawn under the dots, so a dot still wins
    svg.querySelectorAll('.edge').forEach(function(e){var h=document.createElementNS('http://www.w3.org/2000/svg','path');
      h.setAttribute('class','ehit');h.setAttribute('d',e.getAttribute('d'));h.setAttribute('data-c',e.getAttribute('data-c'));h.setAttribute('data-p',e.getAttribute('data-p'));e.after(h);});
    svg.addEventListener('mouseover',function(e){var h=e.target.closest('.ehit');if(h)litEdge(h.getAttribute('data-c'),h.getAttribute('data-p'));});
    svg.addEventListener('mouseout',function(e){if(e.target.closest('.ehit')&&!(e.relatedTarget&&e.relatedTarget.closest&&e.relatedTarget.closest('.ng')))reset();});
    svg.addEventListener('mouseover',function(e){var a=e.target.closest('.ng');if(!a)return;var k=a.getAttribute('data-key');lit(k);showTip(k,a);});
    svg.addEventListener('mouseout',function(e){var a=e.target.closest('.ng');if(!a||a.contains(e.relatedTarget))return;reset();hideTip();});
    svg.addEventListener('focusin',function(e){var a=e.target.closest('.ng');if(a){var k=a.getAttribute('data-key');lit(k);showTip(k,a);}});
    svg.addEventListener('focusout',function(){reset();hideTip();});
    // A click opens the record in a new tab (the dot's link); on a touch screen the first tap
    // shows the popover and the second opens the record.
    svg.addEventListener('click',function(e){var a=e.target.closest('.ng');if(!a)return;var k=a.getAttribute('data-key');
      if(lastPointer==='touch'&&shownKey!==k){e.preventDefault();lit(k);showTip(k,a);}});
  }
  // On opening, glide down and across to the most recent experiment (#106), unless the reader
  // has scrolled already or the address names a place on the page.
  // Both axes move together on one ease-in-out curve, slower for longer distances; a wheel,
  // touch or key from the reader stops it where it is.
  function toLatest(){
    var last=nodes[nodes.length-1];if(data.current||!last||location.hash||window.scrollY>0||host.scrollLeft>0)return;
    var C=geo.cols[last.fam],top=window.scrollY+svg.getBoundingClientRect().top+geo.y[last.key];
    var y0=window.scrollY,x0=host.scrollLeft,
        y1=Math.max(0,Math.min(top-window.innerHeight*0.6,document.documentElement.scrollHeight-window.innerHeight)),
        x1=Math.max(0,Math.min(C.x-host.clientWidth/2,host.scrollWidth-host.clientWidth));
    if(window.matchMedia('(prefers-reduced-motion: reduce)').matches){window.scrollTo(0,y1);host.scrollLeft=x1;return;}
    var dist=Math.hypot(y1-y0,x1-x0),dur=Math.min(2200,Math.max(900,500+dist*0.25)),t0=null,stopped=false;
    var stop=function(){stopped=true;};
    ['wheel','touchstart','keydown','mousedown'].forEach(function(ev){window.addEventListener(ev,stop,{passive:true,once:true});});
    var ease=function(t){return t<0.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;};
    requestAnimationFrame(function step(now){
      if(stopped)return;if(t0===null)t0=now;
      var t=Math.min(1,(now-t0)/dur),e=ease(t);
      window.scrollTo(0,y0+(y1-y0)*e);host.scrollLeft=x0+(x1-x0)*e;
      if(t<1)requestAnimationFrame(step);
    });
  }
  render();wire();reset();setTimeout(toLatest,500);
  host.addEventListener('scroll',function(){syncHeads();if(shownKey)hideTip();},{passive:true});
  window.addEventListener('scroll',function(){if(shownKey){reset();hideTip();}},{passive:true});
  var rw=null,lastW=host.clientWidth;
  window.addEventListener('resize',function(){clearTimeout(rw);rw=setTimeout(function(){if(host.clientWidth===lastW)return;lastW=host.clientWidth;
    render();wire();reset();},150);});
})();
</script>"""


def family_names():
    """{number: full name} from the table at the top of families.md."""
    p = ROOT / "families.md"
    out = {}
    if p.exists():
        for m in re.finditer(r"^\| (\d+) \| ([^|]+?) \|", p.read_text(), re.M):
            out.setdefault(m.group(1), m.group(2).strip())
    return out


def plain(text, limit=340):
    """Markdown stripped to plain text, cut at a sentence end near the limit."""
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text or "")
    t = re.sub(r"[*_`]+", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    if len(t) <= limit:
        return t
    cut = t.rfind(". ", 0, limit)
    return t[:cut + 1] if cut > limit // 3 else t[:limit].rsplit(" ", 1)[0] + "..."


def parent_tags(rows):
    """{tag: its parent's tag} for the experiments that name a parent in the record. Some records
    name the parent by a slug the parent's own tag no longer carries (0001-crib-consistent-periods);
    those are matched by the experiment number, so the line does not break there."""
    tags = {r["tag"] for r in rows}
    by_num = {r["tag"][:4]: r["tag"] for r in rows if r["tag"][:4].isdigit()}
    out = {}
    for r in rows:
        p = r.get("parent")
        if not p:
            continue
        t = p if p in tags else by_num.get(p[:4]) if p[:4].isdigit() else None
        if t and t != r["tag"]:
            out[r["tag"]] = t
    return out


def lineage_data(rows):
    """Nodes and family columns for the lineage page, built from the records on every request."""
    names = family_names()

    # a family is its number in families.md; slugs spelt two ways in the records share one lane
    def lane_of(slug):
        num = slug.split("-", 1)[0]
        return num if num.isdigit() else slug

    groups = {}
    for r in rows:
        groups.setdefault(lane_of(r["family"]), []).append(r["family"])
    keys = list(groups)       # rows come in run order, so columns go left to right by first experiment
    last = len(FAMILY_PALETTE) - 1
    fams = []
    for k in keys:
        slug = max(set(groups[k]), key=lambda s: (groups[k].count(s), s))
        num, _, rest = slug.partition("-")
        # name only: the columns run by first experiment, so numbers would read as out of order
        label = rest.replace('-', ' ') if num.isdigit() and rest else slug
        # colour by family number, as on the other pages, not by column
        c = min(int(k) - 1, last) if k.isdigit() else last
        fams.append({"slug": slug, "label": label, "name": names.get(num, label), "c": c,
                     "count": len(groups[k])})
    idx = {s: keys.index(lane_of(s)) for s in {r["family"] for r in rows}}
    par = parent_tags(rows)
    nodes = [{"key": r["tag"], "n": int(r["tag"][:4]) if r["tag"][:4].isdigit() else r["tag"],
              "title": r["title"], "fam": idx[r["family"]], "parent": par.get(r["tag"]),
              "decision": r.get("decision"), "recorded": r.get("decision_recorded"),
              "loss": pct(row_loss(r)), "cribs": r.get("best_crib_hits", 0),
              "summary": plain(r.get("eli5", "")), "note": r.get("verdict_note", "")} for r in rows]
    pivots = [{"id": p["id"], "after": next((r["tag"] for r in rows if r["tag"][:4] == p["after"]), None),
               "label": f'Pivot {p["id"]}: {p["from"]} \u2192 {p["to"]}'} for p in load_pivots()]
    return {"nodes": nodes, "families": fams, "pivots": [p for p in pivots if p["after"]]}


def lineage_section(n, tag):
    """The lineage diagram cut down to one experiment's ancestry: the experiment and every parent
    back to the root of its line, in the family columns that path touches, without pivot rows."""
    rows = load_results()
    par = parent_tags(rows)
    line = set()
    k = tag
    while k and k not in line:
        line.add(k)
        k = par.get(k)
    sub = [r for r in rows if r["tag"] in line]
    up = len(sub) - 1
    title = "Experiment lineage"
    if not up:
        return sec(n, title, "This experiment started a line of its own: it was built on no earlier experiment.")
    say = f"{up} experiment{'s' if up != 1 else ''} before it, back to the root of its line."
    data = lineage_data(sub)
    data["pivots"] = []
    data["current"] = tag
    blob = json.dumps(data).replace("</", "<\\/")
    return (f"<style>{LIN_CSS}</style>" + sec(n, title, "What this experiment was built on, from the lineage page: " + say + " Its number is in bold.")
            + '<div class="lin"><div style="max-width:980px;margin:0 auto">' + LIN_LEGEND.replace('<span class="k"><svg width="12" height="10" viewBox="0 0 12 10"><path d="M1,1 L11,1 L6,9 z" fill="var(--accent)"/></svg>pivot</span>\n', "") + "</div>"
            + '<div class="lin-box fit"><div id="lin-heads"><div id="lin-lanes"></div></div><div id="lin-diagram"></div></div>'
            + f'<div id="lin-tip" role="tooltip"></div><script id="lin-data" type="application/json">{blob}</script></div>{LIN_JS}')


LIN_LEGEND = """<div class="lin-legend">
<span class="k"><span class="ldot lkept"></span>kept</span>
<span class="k"><span class="ldot" style="color:var(--disc)"></span>reverted, in its family's colour</span>
<span class="k"><span class="lerr">&times;</span>error or timeout</span>
<span class="k"><span class="lwas"></span>reverted under today's rules</span>
<span class="k"><span class="larc"></span>built on a parent in the same family</span>
<span class="k"><span class="lx"></span>built on a parent in another family</span>
<span class="k"><svg width="12" height="10" viewBox="0 0 12 10"><path d="M1,1 L11,1 L6,9 z" fill="var(--accent)"/></svg>pivot</span>
</div>"""


def lineage_page():
    rows = load_results()
    data = lineage_data(rows)
    par = parent_tags(rows)
    built = [r for r in rows if r["tag"] in par]
    col = {nd["key"]: nd["fam"] for nd in data["nodes"]}     # a family spelt two ways is one column
    cross = sum(1 for r in built if col[par[r["tag"]]] != col[r["tag"]])
    kids = {}
    for r in built:
        kids[par[r["tag"]]] = kids.get(par[r["tag"]], 0) + 1
    top = max(kids.items(), key=lambda kv: (kv[1], kv[0]), default=None)
    n, nf, roots = len(rows), len(data["families"]), len(rows) - len(built)
    facts = (f"{n} experiments in {nf} families. {len(built)} built on an earlier one and {roots} started a line of their own. "
             f"{cross} borrowed a parent from another family.")
    if top:
        facts += f' The most built-on is <a href="/exp/{esc(top[0])}">{int(top[0][:4])}</a>, with {top[1]} children.'
    blob = json.dumps(data).replace("</", "<\\/")
    body = f"""<style>{LIN_CSS}</style><div class="lin">
{page_head("Lineage", "The lineage of each experiment", "Every experiment, top to bottom in the order it ran, in the column of its family. A curve beside a column joins an experiment to the one it built on, from the bottom of the parent to the top of the child. A dashed curve means the parent sits in another family. Hover a dot to trace its line back to the root, or an edge to light the two experiments it joins. Click a dot to open its record in a new tab.")}
{sec(1, "Every experiment by family")}<div style="max-width:980px;margin:0 auto"><p class="facts" style="font-size:14.5px;color:var(--muted);margin:4px 0 12px;max-width:820px">{facts}</p>{LIN_LEGEND}</div>
<div class="lin-box"><div id="lin-heads"><div id="lin-lanes"></div></div><div id="lin-diagram"></div></div>
{page_foot('Each family and its hypotheses are on the <a href="/families">families</a> page; the order they are worked in is on <a href="/priorities">Priorities</a>.')}
<div id="lin-tip" role="tooltip"></div>
<script id="lin-data" type="application/json">{blob}</script></div>{LIN_JS}"""
    return page("research lineage", body, "/lineage")


TREE_CSS = """<style>
.ht-wrap{width:calc(50% + 50vw - 32px);margin:4px 0 28px}
.ht li,.ht p{max-width:none}
.ht-eyebrow{font:600 11px var(--serif);text-transform:uppercase;letter-spacing:.1em;color:var(--muted);margin:0 0 4px;padding-top:10px;border-top:1px solid var(--rule)}
.ht-key{display:flex;flex-wrap:wrap;gap:6px 20px;font-size:13px;color:var(--muted);margin:4px 0 14px}
.ht,.ht ul{list-style:none;margin:0;padding:0}
.ht ul{margin-left:11px;padding-left:20px;border-left:1px solid var(--rule)}
.ht li{position:relative;margin:0;padding:3px 0}
.ht ul>li:before{content:'';position:absolute;left:-20px;top:15px;width:16px;border-top:1px solid var(--rule)}
.ht ul>li:last-child:after{content:'';position:absolute;left:-21px;top:16px;bottom:0;border-left:3px solid var(--paper)}
.ht details>summary{list-style:none;cursor:pointer}
.ht details>summary::-webkit-details-marker{display:none}
.ht summary .tw{display:inline-block;width:12px;color:var(--faint);font-size:11px;transition:transform .15s}
.ht details[open]>summary .tw{transform:rotate(90deg)}
.ht .row{display:inline;line-height:1.45}
.ht .lab{font-size:15px}
.ht .br>.row .lab{font-weight:600}
.ht .fam>details>summary .lab{font-size:16px;font-weight:600;color:var(--fc,var(--ink))}
.ht .fam>details>summary .sw{display:inline-block;width:9px;height:9px;border-radius:50%;background:var(--fc);margin:0 8px 0 0;vertical-align:1px}
.ht .fam>details>ul{border-left-color:color-mix(in srgb,var(--fc,var(--rule)) 45%,transparent)}
.ht .root>details>summary .lab{font-size:18px;font-style:italic;font-weight:400}
.ht-wrap .st,.ht-key2 .st{display:inline-block;width:9px;height:9px;border-radius:50%;margin:0 7px 0 1px;vertical-align:0}
.st-open{background:var(--accent)}
.st-closed{background:var(--disc)}
.st-blocked{background:transparent;border:1.5px dashed var(--faint);width:7px!important;height:7px!important}
.st-noted{background:transparent;border:2px solid var(--ochre);width:6px!important;height:6px!important}
.ht .meta{font-size:12.5px;color:var(--faint);margin-left:8px;white-space:nowrap}
.ht .meta a{color:var(--faint);text-decoration:none;border-bottom:1px dotted var(--faint)}
.ht .meta a:hover{color:var(--accent)}
.ht .roll{font-size:12.5px;color:var(--muted);margin-left:10px;white-space:nowrap}
.ht .roll b{font-weight:600;color:var(--accent)}
.ht .bar{display:inline-flex;width:70px;height:6px;margin-left:8px;vertical-align:1px;border-radius:3px;overflow:hidden;background:var(--rule-soft)}
.ht .bar i{display:block;height:100%}
.ht .rank{font:600 11px var(--serif);letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-right:8px}
.ht .next{font:600 10.5px var(--serif);letter-spacing:.08em;text-transform:uppercase;color:var(--paper);background:var(--accent);padding:1px 6px;border-radius:3px;margin-left:8px}
.ht li.is-open>.row .lab{color:var(--ink)}
.ht li.is-closed>.row .lab,.ht li.is-blocked>.row .lab{color:var(--muted)}
@media(max-width:640px){.ht ul{padding-left:12px;margin-left:6px}.ht ul>li:before{left:-12px;width:9px}.ht ul>li:last-child:after{left:-13px}.ht .meta,.ht .roll{white-space:normal;display:block;margin-left:22px}}
</style>"""


def parse_tree(text):
    """The nested list under '### Hypothesis tree' in families.md, as {label, status, strength, exps, kids}."""
    m = re.search(r"^(#{2,3}) Hypothesis tree\n(.*?)(?=^#{2,3} |\Z)", text, re.S | re.M)
    if not m:
        return None, text
    root, stack = None, []
    for ln in m.group(2).splitlines():
        mm = re.match(r"^( *)- (.*)$", ln)
        if not mm:
            continue
        depth = len(mm.group(1)) // 2
        body = mm.group(2).strip()
        node = {"label": body, "status": None, "strength": "", "exps": [], "kids": []}
        b = re.search(r"\{([^}]*)\}\s*$", body)
        if b:
            node["label"] = body[:b.start()].strip()
            parts = [x.strip() for x in b.group(1).split("·")]
            node["status"] = parts[0] if parts else None
            node["strength"] = parts[1] if len(parts) > 1 else ""
            node["exps"] = [e.strip() for e in parts[2].split(",")] if len(parts) > 2 else []
        while stack and stack[-1][0] >= depth:
            stack.pop()
        if stack:
            stack[-1][1]["kids"].append(node)
        else:
            root = node
        stack.append((depth, node))
    cut = text[:m.start()] + "<div class=\"ht-slot\"></div>\n\n" + text[m.end():]
    return root, cut


def own_open(n):
    """An item that carries its own open status and has sub-items (F1.5 with 0136's bound under it):
    it is still open work, whatever its sub-items say."""
    return bool(n["kids"]) and n["status"] == "open" and n["label"].startswith("**F")


def tree_html(root, text):
    tags = {r["tag"][:4]: r["tag"] for r in load_results()}
    order = (ROOT / "order-of-work.md").read_text() if (ROOT / "order-of-work.md").exists() else text
    ranks = {m.group(2): m.group(1) for m in re.finditer(r"^\| (\d+(?:st|nd|rd|th)) \| (F\d+)", order, re.M)}
    next_done = [False]

    def roll(n):
        if not n["kids"]:
            return {n["status"] or "open": 1}
        c = {}
        for k in n["kids"]:
            for s_, v in roll(k).items():
                c[s_] = c.get(s_, 0) + v
        if own_open(n) and not c.get("open"):
            c["open"] = 1
        return c

    def inline(label):
        return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", esc(label))

    def node(n, depth):
        kids = n["kids"]
        if not kids:
            st = n["status"] or "open"
            nx = ""
            if st == "open" and not next_done[0] and n["label"].startswith("**F"):
                nx = '<span class="next">next</span>'; next_done[0] = True
            exps = " ".join(f'<a href="/exp/{esc(tags[e])}">{int(e)}</a>' if e in tags else esc(e) for e in n["exps"])
            meta = " &middot; ".join(x for x in [esc(st), esc(n["strength"]), exps] if x)
            return (f'<li class="lf is-{esc(st)}"><span class="row"><i class="st st-{esc(st)}"></i>'
                    f'<span class="lab">{inline(n["label"])}</span>{nx}<span class="meta">{meta}</span></span></li>')
        c = roll(n)
        tot = sum(c.values())
        order = [("closed", "var(--disc)"), ("noted", "var(--ochre)"), ("blocked", "var(--faint)"), ("open", "var(--accent)")]
        bar = "".join(f'<i style="width:{100 * c.get(k, 0) / tot:.1f}%;background:{col}"></i>' for k, col in order if c.get(k))
        words = ", ".join(f"<b>{c[k]} {k}</b>" if k == "open" else f"{c[k]} {k}" for k, _ in reversed(order) if c.get(k))
        cls = "root" if depth == 0 else ("fam" if depth == 1 else "br")
        fm = re.match(r"(F\d+)\s", n["label"])
        rank = f'<span class="rank">{ranks[fm.group(1)]}</span>' if fm and fm.group(1) in ranks else ""
        if fm:
            cls += f" fc-{fm.group(1)[1:]}"
        is_open = depth <= 1 or c.get("open")
        own_nx = ""
        if own_open(n) and not next_done[0]:
            own_nx = '<span class="next">next</span>'; next_done[0] = True
        inner = "".join(node(k, depth + 1) for k in kids)
        lab = inline(n["label"])
        if fm:
            # spelled out on this page: "Family 6: A move, then the table", not "F6 A move..."
            lab = f'<span class="sw"></span>{inline(re.sub(r"^F(\d+)\s+", r"Family \1: ", n["label"]))}'
        return (f'<li class="{cls}"><details{" open" if is_open else ""}><summary><span class="row"><span class="tw">&#9656;</span>{rank}'
                f'<span class="lab">{lab}</span>{own_nx}<span class="roll">{words}</span><span class="bar">{bar}</span></span></summary>'
                f'<ul>{inner}</ul></details></li>')

    return TREE_CSS + f'<div class="ht-wrap"><ul class="ht">{node(root, 0)}</ul></div>'


TREE_KEY = ('<div class="ph-legend ht-key2" style="margin:6px 0 14px"><span><i class="st st-open"></i>open: still to test</span>'
            '<span><i class="st st-closed"></i>closed: ruled out by an exact test, or a sampled one against scrambled copies</span>'
            '<span><i class="st st-blocked"></i>blocked: cannot be tested with the known letters alone</span>'
            '<span><i class="st st-noted"></i>noted: a finding, not a hypothesis to close</span></div>')


def tree_counts(n):
    if not n["kids"]:
        return {n["status"] or "open": 1}
    c = {}
    for k in n["kids"]:
        for s_, v in tree_counts(k).items():
            c[s_] = c.get(s_, 0) + v
    if own_open(n) and not c.get("open"):
        c["open"] = 1
    return c


def first_open(n):
    if not n["kids"]:
        return n if (n["status"] or "open") == "open" and n["label"].startswith("**F") else None
    if own_open(n):
        return n
    for k in n["kids"]:
        f = first_open(k)
        if f:
            return f
    return None


def family_record_html(text):
    """The 'Full record by family' table, redrawn: one row per family with the lineage page's head,
    its status, every experiment linked, and the bounds split into findings, newest first, all shown."""
    m = re.search(r"^## Full record by family\n(.*?)(?=^## )", text, re.S | re.M)
    if not m:
        return None, text
    rows = load_results()
    tags = {r["tag"][:4]: r["tag"] for r in rows}
    by_fam = {}
    for r in rows:
        by_fam.setdefault(r["family"].split("-", 1)[0], []).append(r)
    short = {}
    for r in rows:
        num, _, rest = r["family"].partition("-")
        short.setdefault(num, rest.replace("-", " "))

    def chip(num4):
        return f'<a class="xchip" href="/exp/{esc(tags[num4])}">{int(num4)}</a>' if num4 in tags else esc(num4)

    def linkify(t):
        return re.sub(r"\b(0\d{3})\b", lambda mm: f'<a href="/exp/{esc(tags[mm.group(1)])}">{mm.group(1)}</a>' if mm.group(1) in tags else mm.group(1), t)

    fams = []
    for ln in m.group(1).splitlines():
        cells = [c.strip() for c in ln.strip().strip("|").split(" | ")]
        if len(cells) >= 5 and cells[0].isdigit():
            fams.append(cells)
    fams.sort(key=lambda c: int(c[0]))
    out = []
    for num, name, status, _exps, bounds, *_ in fams:
        # a finding ends with its experiment in brackets, "(0005)."; some start with it instead, "Both fingerprints (0077): ..."
        parts = [x.strip() for x in re.split(r"(?<=\))\.\s+(?=[A-Z])|\.\s+(?=[A-Z][^.]{0,90}\(0\d{3}\):)", bounds) if x and x.strip()]
        items = []
        for ptxt in parts:
            refs = sorted(set(re.findall(r"\b(0\d{3})\b", ptxt)))
            items.append((max(refs) if refs else "0000", refs, ptxt.rstrip(".") + "."))
        items.sort(key=lambda it: it[0], reverse=True)
        lis = "".join(f'<li><span class="fr-refs">{"".join(chip(x) for x in refs)}</span><span class="fr-t">{linkify(md_inline(t))}</span></li>'
                      for _, refs, t in items)
        first, rest = lis.split("</li>", 4)[:4], None
        li_list = re.findall(r"<li>.*?</li>", lis, re.S)
        body = f'<ul class="fr-list">{"".join(li_list)}</ul>'
        exps = by_fam.get(num, [])
        st_word, _, st_rest = status.partition(" ")
        out.append(f'<div class="fr-row fc-{esc(num)}"><div class="fr-head">'
                   f'<div class="famhead"><span class="sw"></span>{esc(num)} {esc(short.get(num, ""))}<span class="cnt">{len(exps)} experiments</span></div>'
                   f'<p class="fr-name">{md_inline(name)}</p>'
                   f'<p class="fr-status"><b>{esc(st_word)}</b> {md_inline(st_rest)}</p>'
                   '</div>'
                   f'<div class="fr-body">{body}</div></div>')
    html_ = FR_CSS + '<div class="fr">' + "".join(out) + "</div>"
    cut = text[:m.start()] + "## Full record by family\n\n<div class=\"fr-slot\"></div>\n\n" + text[m.end():]
    return html_, cut


def md_inline(t):
    """A table cell's markdown (code, bold, links) as inline HTML."""
    return re.sub(r"^<p>|</p>$", "", md(t).strip())


FR_CSS = """<style>
.fr{width:90vw;position:relative;left:50%;transform:translateX(-50%);margin:8px 0 10px;border-top:1px solid var(--rule)}
.fr-row{display:grid;grid-template-columns:260px minmax(0,1fr);gap:0 34px;padding:16px 0 14px;border-bottom:1px solid var(--rule-soft)}
.fr-head .famhead{font-size:12px}
.fr-name{font-size:14px;line-height:1.45;margin:8px 0 6px;max-width:none}
.fr-status{font-size:13px;color:var(--muted);margin:0 0 8px;max-width:none}.fr-status b{color:var(--fc);font-weight:600}
.fr-exps{line-height:1.5}
.fr-list{list-style:none;margin:0;padding:0}
.fr-list li{display:grid;grid-template-columns:96px minmax(0,1fr);gap:0 12px;padding:5px 0;border-bottom:1px dotted var(--rule-soft);font-size:14.5px;line-height:1.5;max-width:none}
.fr-list li:last-child{border-bottom:none}
.fr-refs{text-align:right}
.fr-t{color:var(--ink)}.fr-t a{color:inherit;border-bottom:1px dotted var(--faint);text-decoration:none}
.fr-more summary{cursor:pointer;font:600 11px var(--serif);text-transform:uppercase;letter-spacing:.08em;color:var(--fc);margin:6px 0 2px 108px}
@media(max-width:760px){.fr{width:calc(100vw - 32px)}.fr-row{grid-template-columns:1fr}.fr-list li{grid-template-columns:1fr}.fr-refs{text-align:left}.fr-more summary{margin-left:0}}
</style>"""


FAM_SECTIONS = {
    "/keys": ("Key sources", "Keys", "Where the secret words should come from",
              "The order in which every family draws its key material: the creators' remarks say the first three messages hold "
              "clues to the fourth, so their words come first, generic word lists last."),
    "/dead-ends": ("Dead ends", "Dead ends", "Approaches ruled out, and why",
                   "Every approach the known letters or an experiment has ruled out, with the reason and the source. Re-entering "
                   "one needs a stated reason."),
    "/pivots": ("Pivot log", "Pivots", "When the search changed family, and why",
                "Each time the work moved from one family to another, with the experiments that led to it and the reason."),
}


def families_section(text, prefix):
    """The '## <prefix>...' section of families.md: (heading line, body)."""
    m = re.search(rf"^## ({re.escape(prefix)}[^\n]*)\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return (m.group(1), m.group(2), m) if m else (None, "", None)


def link_exps_html(h):
    """Experiment numbers (0001-0999) in rendered text become links; tags and attributes are left alone."""
    tags = {r["tag"][:4]: r["tag"] for r in load_results()}
    parts = re.split(r"(<[^>]+>)", h)
    for i, part in enumerate(parts):
        if not part.startswith("<"):
            parts[i] = re.sub(r"\b(0\d{3})\b", lambda mm: f'<a href="/exp/{esc(tags[mm.group(1)])}">{mm.group(1)}</a>' if mm.group(1) in tags else mm.group(1), part)
    return "".join(parts)


def families_section_page(path):
    prefix, eyebrow, title, standfirst = FAM_SECTIONS[path]
    text = (ROOT / "families.md").read_text()
    heading, body, _ = families_section(text, prefix)
    nrows = len([ln for ln in body.splitlines() if ln.startswith("| ") and not ln.startswith("| Approach") and not ln.startswith("| Date")])
    facts = {"/dead-ends": f"{nrows} dead ends.", "/pivots": f"{nrows} pivots so far."}.get(path, "")
    head = page_head(eyebrow, title, standfirst, facts)
    foot = page_foot('The families themselves are on the <a href="/families">families</a> page; the order they are worked in is on <a href="/priorities">Priorities</a>.')
    return page(eyebrow.lower(), head + "<article>" + link_exps_html(md(body)) + "</article>" + foot, path, True)


def record_page():
    text = (ROOT / "families.md").read_text()
    rec, _ = family_record_html(text)
    rows = load_results()
    n_find = rec.count('<li><span class="fr-refs">') if rec else 0
    head = page_head("Full record", "What each family has covered",
                     "Every bound the search has set, family by family: the family's status, then each finding with the experiments "
                     "behind it, newest first. A finding says what was searched and what the scrambled copies of the carved text did "
                     "under the same search.",
                     f"{len(rows)} experiments, {n_find} findings.")
    foot = page_foot('The same families as a tree of open and closed hypotheses are on the <a href="/families">families</a> page; '
                     'the order they are worked in is on <a href="/priorities">Priorities</a>.')
    _, rec_body, _ = families_section(text, "Full record by family")
    note = re.search(r"^Parameter applied.*?(?=\n\n|\Z)", rec_body, re.S | re.M)
    note_html = f'<article><p class="muted">{link_exps_html(md_inline(note.group(0).replace(chr(10), " ")))}</p></article>' if note else ""
    return page("full record", head + (rec or "") + note_html + foot, "/record", True)


def families_page():
    text = (ROOT / "families.md").read_text()
    root, cut = parse_tree(text)
    _, cut = family_record_html(cut)
    for pre, *_ in FAM_SECTIONS.values():
        _, _, mm = families_section(cut, pre)
        if mm:
            cut = cut[:mm.start()] + cut[mm.end():]
    cut = cut.replace("## Full record by family\n\n<div class=\"fr-slot\"></div>\n\n", "")
    cut = re.sub(r"^# .*\n", "", cut, count=1, flags=re.M)
    body = md(cut)
    facts, key = "", ""
    if root:
        body = body.replace('<div class="ht-slot"></div>', tree_html(root, text))
        c = tree_counts(root)
        fams = sum(1 for k in root["kids"] if re.match(r"F\d", k["label"]))
        nx = first_open(root)
        facts = (f"{fams} families, {sum(c.values())} hypotheses at the leaves: <b>{c.get('open', 0)} open</b>, {c.get('closed', 0)} closed, "
                 f"{c.get('blocked', 0)} blocked, {c.get('noted', 0)} noted."
                 + (" Next: " + re.sub(r"[*][*](.+?)[*][*]", lambda m_: "<b>" + m_.group(1) + "</b>", esc(nx["label"])) + "." if nx else ""))
        key = TREE_KEY
    head = page_head("Families", "Where we believe the method is",
                     "Every hypothesis the search holds, from one root through the families to the single tests. Each leaf is open, closed, "
                     "blocked or noted, with the strength of the test and the experiments behind it. Families appear in the order they are "
                     "worked; click a branch to fold it, a number to open the experiment.", facts, key)
    foot = page_foot('The ranking and each family\'s open items as tables are on <a href="/priorities">Priorities</a>; what each family has covered, finding by finding, is in the <a href="/record">full record</a>; key sources, dead ends and pivots each have their own page; '
                     'how the experiments built on each other is on the <a href="/lineage">lineage</a> page.')
    return page("families", head + "<article>" + body + "</article>" + foot, "/families", True)


PROG_CSS = """<style>
.prog ol,.prog ul{padding-left:24px;margin:10px 0 16px}.prog li{margin:0 0 8px}
.prog li>ul{margin:6px 0 4px}.prog li p{margin:0 0 6px}
.prog a.fchip{text-decoration:none}.prog a.fchip code{color:var(--accent)}
.prompt{margin:8px 0 0}.prompt .ktabs{margin:8px 0 10px}
.prompt-box{background:var(--wash);border:1px solid var(--rule);border-radius:7px;padding:8px 34px 30px}
.prompt-box .rsec{margin-top:40px}
.prompt-raw{display:none}.prompt.raw .prompt-raw{display:block}.prompt.raw .prompt-rendered{display:none}
.prompt-raw pre{background:none;border:none;padding:18px 0 0;margin:0;white-space:pre-wrap;font-size:13px;line-height:1.6;color:var(--ink)}
@media(max-width:640px){.prompt-box{padding:6px 16px 22px}}
</style>"""

FILE_PAGES = {"order-of-work.md": "/priorities", "families.md": "/families", "11-clue-register.md": "/clues",
              "knowledge/11-clue-register.md": "/clues", "12-assumptions.md": "/assumptions", "knowledge/12-assumptions.md": "/assumptions", "NOTEBOOK.md": "/notebook", "GLOSSARY.md": "/glossary",
              "results.tsv": "/experiments", "grades.tsv": "/experiments", "program.md": "/program"}


def program_page():
    """program.md, rendered as a designed page: numbered sections, numbered lists as step rails, lists
    whose items open with a bold label as cards, file names linked to the pages that show them."""
    text = (ROOT / "program.md").read_text()
    text = re.sub(r"^# .*\n", "", text, count=1, flags=re.M)
    intro, *secs = re.split(r"^## ", text, flags=re.M)
    out = ['<article class="prog">' + md(intro) + "</article>"]
    for k, sec_text in enumerate(secs, 1):
        title, _, body = sec_text.partition("\n")
        decided = re.search(r"\((decided[^)]*)\)", title)
        title = re.sub(r"\s*\(decided[^)]*\)", "", title).strip()
        out.append(sec(k, title, decided.group(1)[0].upper() + decided.group(1)[1:] + "." if decided else "")
                   + '<article class="prog">' + md(body) + "</article>")
    h = "".join(out)

    def tag_lists(h):
        # top-level <ol> become step rails; <ul> whose first item opens with <strong> become cards
        res, depth, i = [], 0, 0
        for m in re.finditer(r"<(/?)(ol|ul)(\s[^>]*)?>", h):
            res.append(h[i:m.start()]); i = m.end()
            closing, kind = m.group(1), m.group(2)
            if closing:
                depth -= 1; res.append(m.group(0)); continue
            if depth == 0:
                nxt = h[m.end():m.end() + 40].lstrip()
                cls = "cards" if kind == "ul" and nxt.startswith("<li><strong>") else ""
                res.append(f'<{kind} class="{cls}">' if cls else m.group(0))
            else:
                res.append(m.group(0))
            depth += 1
        res.append(h[i:])
        return "".join(res)

    h = re.sub(r"<code>([^<]+)</code>", lambda m: (f'<a class="fchip" href="{FILE_PAGES[m.group(1)]}"><code>{m.group(1)}</code></a>'
                                                   if m.group(1) in FILE_PAGES else m.group(0)), h)
    h = crib_cells(h)
    head = page_head("Program", "Instructions for the loop agent",
                     "The rules the agent follows on every experiment: what it reads first, what success means, the gates a reading must "
                     "pass, what it may touch, the loop itself, and how it decides what to try next.",
                     'Below is the prompt itself, as the agent gets it; switch to the raw view to see the exact text.')
    foot = page_foot('The order the families are worked in is on <a href="/priorities">Priorities</a>; what has been tried is in the <a href="/record">full record</a>.')
    raw = (ROOT / "program.md").read_text()
    box = ('<div class="prompt" id="prompt"><p class="lp-eyebrow">Prompt &middot; program.md, read by the agent at the start of every session</p>'
           '<div class="ktabs"><button class="ktab on" data-v="rendered">rendered</button><button class="ktab" data-v="raw">as the agent reads it</button></div>'
           f'<div class="prompt-box"><div class="prompt-rendered">{h}</div><div class="prompt-raw"><pre>{esc(raw)}</pre></div></div></div>'
           "<script>(function(){var p=document.getElementById('prompt');p.querySelectorAll('.ktab').forEach(function(b){b.addEventListener('click',function(){"
           "p.querySelectorAll('.ktab').forEach(function(x){x.classList.toggle('on',x===b);});p.classList.toggle('raw',b.dataset.v==='raw');});});})();</script>")
    return page("program", head + PROG_CSS + box + foot, "/program", False)


def md_page(title, path, active, refresh=True, eyebrow="", h1="", standfirst="", facts="", foot="", take_intro=False):
    """A markdown file under the shared header. The file's own title is dropped; with take_intro its
    first paragraph becomes the standfirst."""
    text = (ROOT / path).read_text()
    text = re.sub(r"^# .*\n", "", text, count=1, flags=re.M)
    if take_intro:
        body = text.lstrip("\n")
        para, _, rest = body.partition("\n\n")
        if not para.startswith(("#", "|", "-", "1.")):
            standfirst = re.sub(r"^<p>|</p>$", "", md(para.replace("\n", " ")).strip())
            text = rest
    head = page_head(eyebrow or esc(title), h1 or esc(title), standfirst, facts)
    return page(title, head + "<article>" + md(text) + "</article>" + (page_foot(foot) if foot else ""), active, refresh)


def route(path):
    if path in ("/", "/index.html"):
        return overview()
    if path.startswith("/exp/"):
        return experiment_page(path[5:].strip("/"))
    if path == "/version":
        stamp = "|".join(str(int(p.stat().st_mtime)) for p in (ROOT / "results.tsv", ROOT / "champion.json", ROOT / "NOTEBOOK.md", ROOT / "controls.tsv") if p.exists()) + f"|{STARTED}"   # a restart (new code) also reloads open pages
        return ("text/plain", stamp)
    if path.startswith("/assets/"):
        f = ROOT / "assets" / path[len("/assets/"):]
        if f.exists() and f.suffix == ".js":
            return ("application/javascript", f.read_text())
        if f.exists() and f.suffix == ".glb":
            return ("model/gltf-binary", f.read_bytes())
    if path == "/lineage":
        return lineage_page()
    if path in ("/experiments", "/live"):
        return live_page()
    if path == "/glossary":
        g = load_glossary()
        return md_page("glossary", "GLOSSARY.md", "/glossary", refresh=False, eyebrow="Glossary", h1="The words the pages use",
                       facts=f"{len(g)} entries.", take_intro=True,
                       foot='Each experiment page shows, under its plain-words text, the entries its text uses.')
    if path == "/notebook":
        nb = (ROOT / "NOTEBOOK.md").read_text()
        days = len(re.findall(r"^## ", nb, re.M))
        return md_page("lab notebook", "NOTEBOOK.md", "/notebook", eyebrow="Notebook", h1="What was decided, run, found and left open",
                       facts=f"{days} working days so far, newest first.", take_intro=True,
                       foot='The bounds each experiment set are on the <a href="/families">families</a> page and in the <a href="/clues">clue register</a>.')
    if path == "/order":
        path = "/priorities"
    if path == "/priorities":
        return md_page("priorities", "order-of-work.md", "/priorities", eyebrow="Priorities", h1="How the search proceeds from here",
                       standfirst="The rules for working through the families, the order they are ranked in and why, and each family's open items as a table.",
                       facts='Decided 2026-10-16 (issue #29). The same items are drawn as a tree on the <a href="/families">families</a> page.',
                       foot='The same items as a tree are on the <a href="/families">families</a> page; the rules the loop follows are in the <a href="/program">program</a>.')
    if path == "/learnings":
        return learnings_page()
    if path == "/pivots":
        return pivots_page()
    if path.startswith("/pivot/"):
        return pivot_page(path[len("/pivot/"):].strip("/"))
    if path in FAM_SECTIONS:
        return families_section_page(path)
    if path == "/record":
        return record_page()
    if path == "/families":
        return families_page()
    if path == "/clues":
        cr = (ROOT / "knowledge/11-clue-register.md").read_text()
        nclues = len(set(re.findall(r"^\*\*(C\d+[a-z]?)\.", cr, re.M)))
        return md_page("clue register", "knowledge/11-clue-register.md", "/clues", eyebrow="Clues", h1="Every hint and its readings",
                       facts=f"{nclues} clues.", take_intro=True,
                       foot='Experiments cite clues by number in their expert hypothesis; the <a href="/families">families</a> page shows what each family has covered.')
    if path == "/assumptions":
        ar = (ROOT / "knowledge/12-assumptions.md").read_text()
        nass = len(set(re.findall(r"^\*\*(A\d+)\.", ar, re.M)))
        return md_page("assumptions", "knowledge/12-assumptions.md", "/assumptions", eyebrow="Assumptions", h1="What the project takes for granted",
                       facts=f"{nass} assumptions.", take_intro=True,
                       foot='The hints these rest on are in the <a href="/clues">clue register</a>; the order of work is on the <a href="/priorities">priorities</a> page.')
    if path == "/program":
        return program_page()
    if path == "/reference":
        return reference_page()
    if path == "/controls":
        return controls_page()
    return None


class H(BaseHTTPRequestHandler):
    def do_GET(self):
        out = route(self.path.split("?")[0])
        if out is None:
            self.send_response(404); self.end_headers(); return
        ctype = "text/html; charset=utf-8"
        if isinstance(out, tuple):
            ctype, out = out
        data = out if isinstance(out, bytes) else out.encode()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *a):
        pass


def export(out, base=""):
    """Write every page as a static site under out/ (a page at /x becomes out/x/index.html), with
    every root-relative link moved under base, for GitHub Pages at alexisrondeau.me/k4/."""
    import shutil
    from datetime import datetime, timezone
    EXPORT.update(base=base, date=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"))
    rows = load_results()
    paths = (["/", "/experiments", "/lineage", "/learnings", "/families", "/priorities", "/pivots", "/record",
              "/notebook", "/clues", "/assumptions", "/glossary", "/program", "/reference", "/controls"]
             + [p for p in FAM_SECTIONS if p != "/pivots"]
             + [f"/pivot/{p['id']}" for p in load_pivots()] + [f"/exp/{r['tag']}" for r in rows])
    rebase = lambda h: re.sub(r"""(["'])/(?=exp/|pivot/|assets/)""", lambda m: m.group(1) + base + "/",
                              re.sub(r'((?:href|src)=")/(?!/)', lambda m: m.group(1) + base + "/", h))
    out = Path(out)
    if out.exists():
        shutil.rmtree(out)
    for p in paths:
        html = route(p)
        if html is None:
            raise SystemExit(f"no page at {p}")
        f = out / p.strip("/") / "index.html"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(rebase(html))
    (out / "assets").mkdir(exist_ok=True)
    for a in (ROOT / "assets").iterdir():
        if a != MODEL and a.suffix == ".js":
            (out / "assets" / a.name).write_text(rebase(a.read_text()))
    shutil.copy(ROOT / "assets" / "share.png", out / "share.png")     # tools/share_card.py
    (out / ".nojekyll").write_text("")
    print(f"wrote {len(paths)} pages to {out}")


def build():
    STATIC.mkdir(exist_ok=True)
    (STATIC / "index.html").write_text(overview())
    (STATIC / "lineage.html").write_text(lineage_page())
    (STATIC / "live.html").write_text(live_page())
    for r in load_results():
        (STATIC / f"{r['tag']}.html").write_text(experiment_page(r["tag"]))
    print(f"wrote {STATIC}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--export", metavar="DIR", help="write the whole site as static pages to DIR")
    ap.add_argument("--base", default="", help="with --export: the path the site is served under, e.g. /k4")
    ap.add_argument("--port", type=int, default=8765)
    a = ap.parse_args()
    if a.export:
        export(a.export, a.base.rstrip("/"))
    elif a.build:
        build()
    else:
        print(f"dashboard at http://127.0.0.1:{a.port}")
        ThreadingHTTPServer(("127.0.0.1", a.port), H).serve_forever()
