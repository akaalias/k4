"""Readable progress for a headless loop run (tools/run_loop.sh --unattended).

Reads Claude Code's stream-json, from stdin or from a log file, and prints one line per event worth
seeing: what the agent is doing, the phase clock, the experiment it is working on, each finished
experiment with its decision, and the elapsed time. The raw stream stays in logs/ untouched.

    tools/run_loop.sh --unattended                      # pipes through this automatically
    uv run python tools/loop_watch.py logs/loop-....log  # replay or follow a log from another shell
    uv run python tools/loop_watch.py --follow logs/loop-....log
"""

import json
import re
from datetime import datetime
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
T0 = time.time()
DIM, BOLD, RED, GREEN, RESET = "\033[2m", "\033[1m", "\033[31m", "\033[32m", "\033[0m"
if not sys.stdout.isatty():
    DIM = BOLD = RED = GREEN = RESET = ""

state = {"phase": None, "slug": None, "rows": None, "attack_mtime": 0.0, "start": None}


def stamp(ts=None):
    s = int((ts or time.time()) - (state["start"] or T0))
    return f"{DIM}[{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}]{RESET}"


def say(text, ts=None):
    print(f"{stamp(ts)} {text}", flush=True)


def short(s, n=110):
    s = " ".join(str(s).split())
    return s if len(s) <= n else s[: n - 1] + "…"


def check_files():
    """Phase clock, the experiment being written, and newly finished experiments."""
    try:
        ticks = json.loads((ROOT / ".phase.json").read_text()).get("ticks", [])
        ph = ticks[-1]["phase"] if ticks else None
        if ph and ph != state["phase"]:
            state["phase"] = ph
            say(f"{BOLD}phase{RESET} {ph}")
    except (OSError, ValueError, KeyError):
        pass
    a = ROOT / "attack.py"
    try:
        m = a.stat().st_mtime
        if m != state["attack_mtime"]:
            state["attack_mtime"] = m
            text = a.read_text()
            slug = re.search(r'"slug":\s*"([^"]+)"', text)
            changed = re.search(r'"changed":\s*"([^"]{0,200})', text)
            if slug and slug.group(1) != state["slug"]:
                state["slug"] = slug.group(1)
                item = re.search(r"\bF\d+\.\d+\b", changed.group(1)) if changed else None
                say(f"{BOLD}experiment{RESET} {slug.group(1)}" + (f"  ({item.group(0)})" if item else ""))
    except OSError:
        pass
    try:
        rows = (ROOT / "results.tsv").read_text().splitlines()[1:]
        if state["rows"] is None:
            state["rows"] = len(rows)
        elif len(rows) > state["rows"]:
            for r in rows[state["rows"]:]:
                f = r.split("\t")
                if len(f) >= 8:
                    col = GREEN if f[4] == "kept" else (RED if f[4] in ("error", "timeout") else "")
                    say(f"{BOLD}done{RESET} {f[1]}  {col}{f[4]}{RESET}  cribs {f[7]}/24  candidates {f[5]}")
            state["rows"] = len(rows)
    except OSError:
        pass


def tool_line(name, inp):
    if name == "Bash":
        d = inp.get("description") or inp.get("command", "")
        cmd = inp.get("command", "")
        if "run_experiment.py" in cmd:
            return f"{BOLD}running the experiment{RESET} (budget 30 min)"
        if "pytest" in cmd:
            return "running the tests"
        if cmd.startswith("git commit") or " git commit" in cmd:
            return "committing"
        return f"bash: {short(d, 90)}"
    if name in ("Read", "Edit", "Write"):
        p = inp.get("file_path", "")
        return f"{name.lower()} {p.replace(str(ROOT) + '/', '')}"
    if name in ("WebSearch", "WebFetch"):
        return f"{name}: {short(inp.get('query') or inp.get('url', ''), 90)}"
    return name


def ev_time(ev):
    ts = ev.get("timestamp")
    if ts:
        try:
            return datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()
        except ValueError:
            pass
    return None


def handle(ev):
    t = ev.get("type")
    et = ev_time(ev)
    if et and state["start"] is None:
        state["start"] = et
    if t == "system" and ev.get("subtype") == "init":
        say(f"{BOLD}loop started{RESET}  session {ev.get('session_id', '')[:8]}")
    elif t == "assistant":
        for c in ev.get("message", {}).get("content", []):
            if c.get("type") == "tool_use":
                say(tool_line(c.get("name", ""), c.get("input", {}) or {}), et)
            elif c.get("type") == "text" and c.get("text", "").strip():
                say(f"{DIM}{short(c['text'].strip().splitlines()[0], 140)}{RESET}", et)
    elif t == "result":
        cost = ev.get("total_cost_usd")
        mins = (ev.get("duration_ms") or 0) / 60000
        say(f"{BOLD}loop finished{RESET}  {mins:.0f} min" + (f", ${cost:.2f}" if cost else ""))
        if ev.get("result"):
            print("\n" + ev["result"], flush=True)
    check_files()


def lines(src, follow):
    while True:
        ln = src.readline()
        if ln:
            yield ln
        elif follow:
            check_files()
            time.sleep(1)
        else:
            return


def main():
    args = [a for a in sys.argv[1:] if a != "--follow"]
    follow = "--follow" in sys.argv
    src = open(args[0]) if args else sys.stdin
    check_files()
    for ln in lines(src, follow):
        try:
            handle(json.loads(ln))
        except ValueError:
            continue


if __name__ == "__main__":
    main()
