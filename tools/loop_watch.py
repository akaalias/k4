"""Readable progress for a headless loop run (tools/run_loop.sh --unattended).

Reads Claude Code's stream-json, from stdin or from a log file, and prints one line per event worth
seeing: what the agent is doing, the phase clock, the experiment it is working on, each finished
experiment with its decision, and the elapsed time. The raw stream stays in logs/ untouched.

    tools/run_loop.sh --unattended                      # pipes through this automatically
In a terminal, two live bars sit under the events (backlog items done; the running experiment's
progress from ctx.progress, else its elapsed time), and pressing s asks for a graceful stop (issue #97).
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

import threading as _threading
LOCK = _threading.RLock()

state = {"phase": None, "slug": None, "rows": None, "attack_mtime": 0.0, "start": None}


def stamp(ts=None):
    s = int((ts or time.time()) - (state["start"] or T0))
    return f"{DIM}[{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}]{RESET}"


def say(text, ts=None):
    footer.clear()
    print(f"{stamp(ts)} {text}", flush=True)
    footer.draw()


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
        # only a command that starts a run counts, not one that reads or greps the harness (issue #96)
        if "start_experiment.sh" in cmd or re.search(r"python[^|;&]*\brun_experiment\.py", cmd):
            m = re.search(r"--budget\s+(\d+)", cmd)
            return f"{BOLD}starting the experiment{RESET} " + (f"(capped at {int(m.group(1)) // 60} min)" if m else "(no time limit)")
        if "wait_experiment.sh" in cmd:
            return "waiting for the experiment"
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


# ---- live footer: two bars and the graceful stop (issue #97) ----------------------------------------

REQ = ROOT / "data" / "loop-stop-request"
MARKER = ROOT / "data" / "running-experiment.json"
PROGRESS = ROOT / "data" / "experiment-progress.json"


def bar(frac, width, moving=None):
    """A bar of `width` cells; frac in 0..1, or moving=tick for a run that reports no progress."""
    if moving is not None:
        pos = moving % (2 * (width - 3)) if width > 4 else 0
        pos = pos if pos < width - 3 else 2 * (width - 3) - pos
        return "░" * pos + "███" + "░" * (width - 3 - pos)
    n = max(0, min(width, round(frac * width)))
    return "█" * n + "░" * (width - n)


def mins(sec):
    sec = int(sec)
    return f"{sec // 3600}h{sec % 3600 // 60:02d}m" if sec >= 3600 else f"{sec // 60}m{sec % 60:02d}s"


def backlog_line(width):
    try:
        text = (ROOT / "order-of-work.md").read_text()
        st = [m.strip().strip("*").split()[0] for m in re.findall(r"^\| \*\*[A-Z][\w.]*\*\*[^|]*\| ([^|]+?) \|", text, re.M)]
        done = sum(1 for x in st if x in ("closed", "blocked"))
        n_exp = max(0, len((ROOT / "results.tsv").read_text().splitlines()) - 1)
    except OSError:
        return "backlog: not readable"
    total = len(st) or 1
    return (f"{BOLD}backlog   {RESET} {bar(done / total, width)} {done}/{total} items closed or blocked"
            f" · {total - done} open · {n_exp} experiments")


PHASES = ("design", "implement", "test", "run", "record")
_busy = {"t": 0.0, "n": 0}


def busy_workers(root_pid):
    """Processes under the run using the CPU (above 20%), checked every five seconds."""
    if time.time() - _busy["t"] < 5:
        return _busy["n"]
    _busy["t"] = time.time()
    try:
        import subprocess
        out = subprocess.run(["ps", "-A", "-o", "pid=,ppid=,%cpu="], capture_output=True, text=True, timeout=5).stdout
    except Exception:  # noqa: BLE001
        return _busy["n"]
    kids, cpu = {}, {}
    for ln in out.splitlines():
        f = ln.split()
        if len(f) == 3:
            kids.setdefault(int(f[1]), []).append(int(f[0]))
            cpu[int(f[0])] = float(f[2])
    todo, n = [root_pid], 0
    while todo:
        q = todo.pop()
        for c in kids.get(q, []):
            n += cpu.get(c, 0.0) > 20
            todo.append(c)
    _busy["n"] = n
    return n


def attack_info():
    """The experiment in attack.py: its item (A6.2, F13.1...) and expected minutes, if stated."""
    try:
        text = (ROOT / "attack.py").read_text()
    except OSError:
        return None, None
    ch = re.search(r'"changed":\s*\(?\s*"([^"]{0,300})', text)
    item = re.search(r"\b(?:[ADF]\d+(?:\.\d+)?)\b", ch.group(1)) if ch else None
    m = re.search(r'"expected_minutes":\s*(\d+)', text)
    if m:
        return (item.group(0) if item else None), int(m.group(1))
    m = re.search(r'expected_total_time[^\n]*?(\d+)(?:\s*-\s*(\d+))?\s*min', text)       # older free-text estimates
    return (item.group(0) if item else None), (int(m.group(2) or m.group(1)) if m else None)


def current_phase():
    """(phase, seconds in it, run marker or None). The run is known from the marker; record is the
    time after the search wrote raw.json; design, implement and test come from phase.py's clock."""
    try:
        run = json.loads(MARKER.read_text())
    except (OSError, ValueError):
        run = None
    if run:
        try:
            started = datetime.strptime(run.get("started", ""), "%Y-%m-%d %H:%M:%S").timestamp()
        except ValueError:
            started = time.time()
        dirs = sorted(d for d in (ROOT / "experiments").iterdir() if d.is_dir() and d.stat().st_mtime >= started - 5)
        raw = dirs[-1] / "raw.json" if dirs else None
        if raw and raw.exists():
            return "record", time.time() - raw.stat().st_mtime, run, started
        return "run", time.time() - started, run, started
    try:
        ticks = json.loads((ROOT / ".phase.json").read_text()).get("ticks", [])
        if ticks:
            return ticks[-1]["phase"], time.time() - ticks[-1]["t"], None, None
    except (OSError, ValueError, KeyError):
        pass
    return "design", None, None, None


def experiment_line(width, tick):
    """The bar: ctx.progress if the run reports it, else elapsed against the stated expected time,
    else a moving bar."""
    phase, _, run, started = current_phase()
    item, expected = attack_info()
    if not run:
        return f"{BOLD}experiment{RESET} {bar(0, width)} {DIM}no run yet: the loop is in {phase}{RESET}"
    el = time.time() - started
    try:
        pr = json.loads(PROGRESS.read_text())
        done, total = float(pr.get("done", 0)), float(pr.get("total", 0)) or 1.0
        frac = min(1.0, done / total)
        eta = f" · about {mins(el * (1 - frac) / frac)} left" if 0 < frac < 1 else ""
        lab = f" {pr['label']}" if pr.get("label") else ""
        return f"{BOLD}experiment{RESET} {bar(frac, width)} {frac * 100:.0f}%{lab} · {mins(el)}{eta}"
    except (OSError, ValueError, KeyError):
        pass
    if expected:
        frac = el / (expected * 60)
        over = f" {RED}over the estimate{RESET}" if frac > 1 else ""
        return (f"{BOLD}experiment{RESET} {bar(min(frac, 1.0), width)} {mins(el)} of about {expected} min expected{over}"
                f" {DIM}(time, not progress){RESET}")
    return f"{BOLD}experiment{RESET} {bar(0, width, moving=tick)} {mins(el)} {DIM}(no estimate stated){RESET}"


def phase_line():
    """Which experiment, which item, where in design · implement · test · run · record, and whether it computes."""
    phase, secs, run, _ = current_phase()
    item, _ = attack_info()
    name = state.get("slug") or "next experiment"
    try:
        num = max(int(d.name[:4]) for d in (ROOT / "experiments").iterdir() if d.name[:4].isdigit())
        num = num if run else num + 1
    except ValueError:
        num = None
    steps = " · ".join(f"{BOLD}[{p}]{RESET}" if p == phase else f"{DIM}{p}{RESET}" for p in PHASES)
    if phase == "pause":
        steps += f" · {BOLD}[paused for Alexis]{RESET}"
    t = f" · {mins(secs)} in {phase}" if secs is not None else ""
    cores = ""
    if run and phase == "run":
        n = busy_workers(int(run.get("pid", 0)))
        cores = f" · {n} processes computing" if n else f" · {RED}no process using the CPU{RESET}"
    head = f"{num:04d}" if isinstance(num, int) else ""
    return f"{BOLD}now{RESET}        {head}{f' ({item})' if item else ''} {short(name, 40)} · {steps}{t}{cores}"


def fit(row, cols):
    """Cut a row to `cols` visible characters, keeping its colour codes whole; a cut ends in …"""
    plain = re.sub(r"\033\[[0-9;]*m", "", row)
    if len(plain) <= cols:
        return row + RESET
    out, n = [], 0
    for part in re.split(r"(\033\[[0-9;]*m)", row):
        if part.startswith("\033["):
            out.append(part)
            continue
        take = part[: max(0, cols - 1 - n)]
        out.append(take)
        n += len(take)
    return "".join(out) + "…" + RESET


class Footer:
    """Two live bars under the event lines, redrawn once a second; s asks for a graceful stop."""

    def __init__(self):
        self.on = sys.stdout.isatty()
        self.drawn = 0
        self.tick = 0

    def clear(self):
        if self.on and self.drawn:
            sys.stdout.write(f"\033[{self.drawn}A\033[J")
            self.drawn = 0

    def draw(self):
        if not self.on:
            return
        import shutil
        cols = shutil.get_terminal_size((100, 20)).columns
        width = max(10, min(40, cols - 70))
        hint = (f"{RED}stop requested{RESET}: finishing and recording the current experiment, then stopping"
                f" {DIM}(s takes it back){RESET}" if REQ.exists() else f"{DIM}press s to stop gracefully{RESET}")
        rows = ["", backlog_line(width), experiment_line(width, self.tick), phase_line(), hint]
        # cut each row to the window so nothing wraps: a wrapped row would break the redraw
        sys.stdout.write("".join("\033[K" + fit(r, cols - 1) + "\n" for r in rows))
        sys.stdout.flush()
        self.drawn = len(rows)

    def refresh(self):
        self.tick += 1
        self.clear()
        self.draw()


footer = Footer()


def toggle_stop():
    if REQ.exists():
        REQ.unlink(missing_ok=True)
        say("stop request taken back; the loop carries on")
    else:
        REQ.write_text(time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
        say(f"{BOLD}stop requested{RESET}: no new experiment; the current one finishes and is recorded")


def listen_keys():
    """Read single keys from the terminal (not from the piped stream) in a background thread."""
    try:
        import termios
        import tty
        import atexit
        import threading
        fd = open("/dev/tty", "rb", buffering=0)
        old = termios.tcgetattr(fd)
        tty.setcbreak(fd)
        atexit.register(lambda: termios.tcsetattr(fd, termios.TCSADRAIN, old))
    except (OSError, ImportError):
        return

    def loop():
        while True:
            ch = fd.read(1)
            if not ch:
                return
            if ch.lower() == b"s":
                with LOCK:
                    toggle_stop()

    threading.Thread(target=loop, daemon=True).start()


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
        # the session wakes again on each background notification; only the first init is the start
        first = not state.get("started")
        state["started"] = True
        say(f"{BOLD}loop started{RESET}  session {ev.get('session_id', '')[:8]}" if first
            else f"{DIM}turn started (background work reported back){RESET}")
    elif t == "assistant":
        for c in ev.get("message", {}).get("content", []):
            if c.get("type") == "tool_use":
                say(tool_line(c.get("name", ""), c.get("input", {}) or {}), et)
            elif c.get("type") == "text" and c.get("text", "").strip():
                say(f"{DIM}{short(c['text'].strip().splitlines()[0], 140)}{RESET}", et)
    elif t == "result":
        cost = ev.get("total_cost_usd")
        mins = (ev.get("duration_ms") or 0) / 60000
        # a result ends one turn, not the loop: run_loop.sh prints "Loop finished" when the session exits
        say(f"{BOLD}turn ended{RESET}  {mins:.0f} min" + (f", ${cost:.2f} so far" if cost else ""))
        if ev.get("result"):
            footer.clear()
            print("\n" + ev["result"], flush=True)
            footer.draw()
    check_files()


def lines(src, follow):
    while True:
        ln = src.readline()
        if ln:
            yield ln
        elif follow:
            time.sleep(1)                     # the main thread checks files and redraws each second
        else:
            return


def main():
    import queue
    import threading
    args = [a for a in sys.argv[1:] if a != "--follow"]
    follow = "--follow" in sys.argv
    src = open(args[0]) if args else sys.stdin
    replay = bool(args) and not follow
    if replay:
        footer.on = False                     # replaying a finished log: no live bars
    q = queue.Queue()

    def read():
        for ln in lines(src, follow):
            q.put(ln)
        q.put(None)

    threading.Thread(target=read, daemon=True).start()
    if footer.on:
        listen_keys()
    with LOCK:
        check_files()
        footer.draw()
    while True:
        try:
            ln = q.get(timeout=1.0)
        except queue.Empty:
            with LOCK:
                check_files()
                footer.refresh()
            continue
        if ln is None:
            break
        with LOCK:
            try:
                handle(json.loads(ln))
            except ValueError:
                continue
    with LOCK:
        footer.clear()


if __name__ == "__main__":
    main()
