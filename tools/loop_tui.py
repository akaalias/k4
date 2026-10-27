"""Full-screen dashboard for the autoresearch loop (issue #98).

    tools/loop_tui.sh        open it (tools/run_loop.sh --unattended opens it too)

Panels: the loop's status, the backlog by section with what comes next, the current experiment (item,
title, phase, time against its estimate or its reported progress, busy processes, last log line), the
recent experiments with their verdicts, and the loop's latest activity. Keys: s asks for a graceful stop
(again takes it back), q closes the dashboard; the loop keeps running either way.
It only reads the record and the logs; the one file it writes is data/loop-stop-request.
"""
import collections
import importlib.util
import json
import re
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

from rich import box
from rich.console import Group
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("loop_watch", ROOT / "tools" / "loop_watch.py")
lw = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lw)          # reuse its phase, item, estimate, CPU and event helpers
lw.footer.on = False

REQ = ROOT / "data" / "loop-stop-request"
STOP = ROOT / "data" / "loop-stop.json"
PID = ROOT / "data" / "loop.pid"
ACCENT, MUTED, OK, BAD = "#c0614a", "grey58", "green3", "red3"


def mins(sec):
    return lw.mins(max(0, sec))


def bar(frac, width=30, colour=ACCENT):
    n = max(0, min(width, round(frac * width)))
    return Text("█" * n, style=colour) + Text("░" * (width - n), style="grey35")


def alive(pid):
    import os
    try:
        os.kill(int(pid), 0)
        return True
    except (OSError, ValueError):
        return False


def runner_running():
    import subprocess
    try:
        return subprocess.run(["pgrep", "-f", "tools/run_loop.sh"], capture_output=True).returncode == 0
    except OSError:
        return False


_spend = {"t": 0.0, "v": 0.0}


def compute_setting():
    try:
        return json.loads((ROOT / "data" / "compute.json").read_text())
    except (OSError, ValueError):
        return {"where": "local"}


def modal_spend_this_month():
    """Dollars the month's Modal runs cost, from each record's raw.json (issue #99); rechecked every minute."""
    if time.time() - _spend["t"] > 60:
        month, total = time.strftime("%Y-%m"), 0.0
        for raw in (ROOT / "experiments").glob("*/raw.json"):
            if time.strftime("%Y-%m", time.localtime(raw.stat().st_mtime)) != month:
                continue
            try:
                c = json.loads(raw.read_text()).get("compute") or {}
            except (OSError, ValueError):
                continue
            if c.get("where") == "modal":
                total += float(c.get("dollars", 0))
        _spend.update(t=time.time(), v=total)
    return _spend["v"]


def remote_run():
    """The Modal run in progress, if any (tools/remote_run.py writes data/remote-run.json while it runs)."""
    try:
        r = json.loads((ROOT / "data" / "remote-run.json").read_text())
        return r if alive(r.get("pid", 0)) else None
    except (OSError, ValueError):
        return None


# ---- data -------------------------------------------------------------------------------------------

def backlog():
    """[(section, done, total, first open (id, text))] in page order, and the overall counts."""
    text = (ROOT / "order-of-work.md").read_text()
    out = []
    for part in re.split(r"^## ", text, flags=re.M)[1:]:
        head = part.splitlines()[0]
        rows = re.findall(r"^\| \*\*([A-Z][\w.]*)\*\* ?([^|]*)\| ([^|]+?) \|", part, re.M)
        if not rows:
            continue
        st = [(i, d.strip(), s.strip().strip("*").split()[0]) for i, d, s in rows]
        done = sum(1 for _, _, s in st if s in ("closed", "blocked"))
        nxt = next(((i, d) for i, d, s in st if s not in ("closed", "blocked")), None)
        name = re.sub(r"\s*\(issues? [^)]*\)", "", head)
        name = re.sub(r"^Stage 2, step (\d): ", r"S2.\1 ", name)
        out.append((name, done, len(st), nxt))
    return out


def recent(n=8):
    rows = (ROOT / "results.tsv").read_text().splitlines()[1:]
    grades = {}
    try:
        for ln in (ROOT / "grades.tsv").read_text().splitlines()[1:]:
            f = ln.split("\t")
            grades[f[0]] = f[1]
    except OSError:
        pass
    try:
        now = json.loads((ROOT / "data" / "replay.json").read_text()).get("experiments", {})
    except (OSError, ValueError):
        now = {}
    out = []
    for ln in reversed(rows[-n:]):
        f = ln.split("\t")
        if len(f) < 11:
            continue
        secs = float(f[10]) if f[10] else 0.0
        dec = f[4]
        if f[1] in now and dec in ("kept", "reverted"):
            dec = now[f[1]]["verdict_now"]          # today's verdict: 0219 and 0224 were kept by mistake
        out.append((f[0], f[1][5:].replace("-", " "), dec, grades.get(f[0], ""), secs))
    return out


class Activity:
    """The latest events of the newest loop session log, read incrementally."""

    def __init__(self):
        self.path, self.pos = None, 0
        self.events = collections.deque(maxlen=40)

    def poll(self):
        logs = sorted((ROOT / "logs").glob("loop-*.log"))
        if not logs:
            return
        if logs[-1] != self.path:
            first = self.path is None
            self.path, self.pos = logs[-1], 0
            self.events.clear()
            if first and len(logs) > 1:                    # on opening, the end of the previous session too
                self._read(logs[-2], 0)
            m = re.search(r"loop-(\d{8}-\d{6})", self.path.name)
            t0 = datetime.strptime(m.group(1), "%Y%m%d-%H%M%S").timestamp() if m else time.time()
            self.events.append((t0, "loop session started"))
        self.pos = self._read(self.path, self.pos)

    def _read(self, path, pos):
        with open(path, "rb") as f:
            f.seek(pos)
            chunk = f.read()
        nl = chunk.rfind(b"\n")
        if nl < 0:
            return pos
        for ln in chunk[: nl + 1].splitlines():
            try:
                ev = json.loads(ln)
            except ValueError:
                continue
            t = lw.ev_time(ev) or time.time()
            if ev.get("type") == "assistant":
                for c in ev.get("message", {}).get("content", []):
                    if c.get("type") == "tool_use":
                        txt = re.sub(r"\x1b\[[0-9;]*m", "", lw.tool_line(c.get("name", ""), c.get("input", {}) or {}))
                        self.events.append((t, txt))
                    elif c.get("type") == "text" and c.get("text", "").strip():
                        self.events.append((t, "» " + c["text"].strip().splitlines()[0]))
            elif ev.get("type") == "result":
                self.events.append((t, "turn ended"))
        return pos + nl + 1


# ---- panels -----------------------------------------------------------------------------------------

def header():
    pid = PID.read_text().strip() if PID.exists() else ""
    if STOP.exists():
        state = Text(f"stopped: {json.loads(STOP.read_text()).get('reason', '?')}", style=BAD)
    elif REQ.exists():
        state = Text("stopping after the current experiment", style=ACCENT)
    elif (pid and alive(pid)) or runner_running():
        state = Text("running", style=OK)
    else:
        state = Text("not running", style=BAD)
    t = Table.grid(expand=True)
    t.add_column(); t.add_column(justify="right")
    cs = compute_setting()
    if cs.get("where") == "modal":
        where = Text("compute: Modal", style=OK) + Text(f" ${modal_spend_this_month():.2f}"
                                                        + (f" of ${cs['budget_dollars']:.2f}" if cs.get("budget_dollars") else "")
                                                        + " this month   ", style=MUTED)
    else:
        where = Text("compute: laptop   ", style=MUTED)
    t.add_row(Text("KRYPTOS K4 · autoresearch loop", style="bold"),
              where + Text("loop: ") + state + Text(f"   {time.strftime('%H:%M')}", style=MUTED))
    return Panel(t, box=box.HEAVY, style="bold")


def backlog_panel():
    secs = backlog()
    running_item = lw.attack_info()[0] if lw.current_phase()[2] else None
    done = sum(d for _, d, _, _ in secs)
    total = sum(t for _, _, t, _ in secs) or 1
    n_exp = max(0, len((ROOT / "results.tsv").read_text().splitlines()) - 1)
    top = Text.assemble(bar(done / total, 26), f"  {done}/{total} done", (f" · {total - done} open · {n_exp} experiments", MUTED))
    t = Table(box=None, expand=True, show_header=False, padding=(0, 1))
    t.add_column(ratio=5); t.add_column(width=12); t.add_column(justify="right", width=6)
    nxt = None
    text = (ROOT / "order-of-work.md").read_text()
    opens = [(i, d) for i, d, st in re.findall(r"^\| \*\*([A-Z][\w.]*)\*\* ?([^|]*)\| ([^|]+?) \|", text, re.M)
             if st.strip().strip("*").split()[0] not in ("closed", "blocked")]
    after = [o for o in opens if o[0] != running_item]
    nxt = after[0] if after else None
    for name, d, n, first in secs:
        if d == n:
            continue
        t.add_row(Text(name, overflow="ellipsis", no_wrap=True), bar(d / n, 12), Text(f"{d}/{n}", style=MUTED))
    closed = sum(1 for _, d, n, _ in secs if d == n)
    t.add_row(Text(f"{closed} more sections closed or blocked", style=MUTED), Text(""), Text(""))
    nx = Text("next after this  " if running_item else "next  ", style=MUTED)
    if nxt:
        d = re.sub(r"[*`]", "", nxt[1]).strip()
        nx += Text(f"{nxt[0]}  ", style="bold") + Text(d if len(d) <= 160 else d[:159] + "…", style="default")
    else:
        nx += Text("nothing open", style=BAD)
    return Panel(Group(top, Text(""), t, Text(""), nx), title="backlog", title_align="left", border_style="grey50")


def experiment_panel(tick):
    phase, secs, run, started = lw.current_phase()
    item, expected = lw.attack_info()
    try:
        a = (ROOT / "attack.py").read_text()
        title = re.search(r'"title":\s*\(?\s*"([^"]+)', a).group(1)
    except (OSError, AttributeError):
        title = ""
    try:
        num = max(int(d.name[:4]) for d in (ROOT / "experiments").iterdir() if d.name[:4].isdigit())
        num = num if run else num + 1
    except ValueError:
        num = 0
    if item and title.startswith(item):
        title = title[len(item):].lstrip(" :")
    lines = [Text.assemble((f"{num:04d}", "bold"), ("  " + (item or ""), ACCENT + " bold")), Text(title, style="default")]
    steps = Text("phase  ", style=MUTED)
    order = lw.PHASES
    cur = order.index(phase) if phase in order else -1
    for i, p in enumerate(order):
        if i < cur:
            steps += Text(f"✓ {p}   ", style=OK)
        elif i == cur:
            steps += Text(f"▶ {p}", style=ACCENT + " bold") + Text(f" {mins(secs)}   " if secs is not None else "   ", style=ACCENT)
        else:
            steps += Text(f"○ {p}   ", style=MUTED)
    if phase == "pause":
        steps += Text("⏸ paused for Alexis", style=ACCENT + " bold")
    lines += [Text(""), steps]
    if run:
        el = time.time() - started
        prog = None
        try:
            pr = json.loads(lw.PROGRESS.read_text())
            prog = min(1.0, float(pr["done"]) / (float(pr["total"]) or 1.0)), pr.get("label", "")
        except (OSError, ValueError, KeyError):
            pass
        if prog:
            frac, lab = prog
            left = f"  ·  about {mins(el * (1 - frac) / frac)} left" if 0 < frac < 1 else ""
            lines.append(Text("done   ", style=MUTED) + bar(frac) + Text(f"  {frac * 100:.0f}% {lab}{left}"))
        elif expected:
            frac = el / (expected * 60)
            colour = BAD if frac > 1 else ACCENT
            lines.append(Text("time   ", style=MUTED) + bar(min(frac, 1.0), colour=colour)
                         + Text(f"  {mins(el)} of about {expected} min", style=colour if frac > 1 else "default")
                         + Text("  (estimate)", style=MUTED))
        else:
            lines.append(Text("time   ", style=MUTED) + Text(f"{mins(el)} running, no estimate stated", style="default"))
        when = Text(f"started {datetime.fromtimestamp(started).strftime('%H:%M')}", style=MUTED)
        if expected:
            when += Text(f"  ·  expected to end about {datetime.fromtimestamp(started + expected * 60).strftime('%H:%M')}", style=MUTED)
        lines.append(Text("       ") + when)
        rr = remote_run()
        n = lw.busy_workers(int(run.get("pid", 0)))
        if rr:
            lines.append(Text("cpu    ", style=MUTED) + Text(f"on Modal, {rr['cpu']} cores", style=OK)
                         + Text("  ·  the laptop stays cool", style=MUTED))
            lines.append(Text(f"       {rr['url']}", style=MUTED, overflow="ellipsis", no_wrap=True))
        else:
            lines.append(Text("cpu    ", style=MUTED) + (Text(f"{n} processes on the laptop", style=OK) if n
                                                        else Text("no process using the CPU: check the run", style=BAD)))
        try:
            last = [ln for ln in (ROOT / run["log"]).read_text().splitlines() if ln.strip()][-1:]
            if last:
                lines.append(Text("log    ", style=MUTED) + Text(last[0][-110:], style="default", overflow="ellipsis", no_wrap=True))
        except OSError:
            pass
    else:
        lines.append(Text("no run in progress: the loop is preparing the next experiment", style=MUTED))
    return Panel(Group(*lines), title="current experiment", title_align="left", border_style=ACCENT)


def recent_panel():
    t = Table(box=box.SIMPLE_HEAD, expand=True, padding=(0, 1), header_style=MUTED)
    t.add_column("#", width=4); t.add_column("experiment", ratio=1, no_wrap=True, overflow="ellipsis")
    t.add_column("verdict", width=9); t.add_column("outcome", width=11); t.add_column("time", justify="right", width=7)
    for num, name, dec, oc, secs in recent():
        col = OK if dec == "kept" else (BAD if dec in ("error", "timeout") else "default")
        t.add_row(num, name, Text(dec, style=col), Text(oc or "–", style=MUTED), mins(secs))
    return Panel(t, title="recent experiments", title_align="left", border_style="grey50")


def activity_panel(act, rows):
    t = Table(box=None, expand=True, show_header=False, padding=(0, 1))
    t.add_column(width=5, style=MUTED); t.add_column(ratio=1, no_wrap=True, overflow="ellipsis")
    for ts, txt in list(act.events)[-max(3, rows):]:
        t.add_row(datetime.fromtimestamp(ts).strftime("%H:%M"), Text(txt, style=MUTED if txt.startswith("»") else "default"))
    return Panel(t, title="loop activity", title_align="left", border_style="grey50")


def footer():
    s = "take back the stop" if REQ.exists() else "stop gracefully (after this experiment)"
    return Text.assemble(("  s ", "bold reverse"), f" {s}     ", ("  q ", "bold reverse"), " close the dashboard (the loop keeps running)")


def render(act, tick, height):
    lay = Layout()
    lay.split_column(Layout(header(), size=3), Layout(name="top", ratio=5), Layout(name="bottom", ratio=4), Layout(footer(), size=1))
    lay["top"].split_row(Layout(experiment_panel(tick), ratio=6), Layout(backlog_panel(), ratio=5))
    lay["bottom"].split_row(Layout(recent_panel(), ratio=6), Layout(activity_panel(act, max(3, height * 4 // 9 - 3)), ratio=5))
    return lay


def keys(state):
    try:
        import atexit
        import termios
        import tty
        fd = open("/dev/tty", "rb", buffering=0)
        old = termios.tcgetattr(fd)
        tty.setcbreak(fd)
        atexit.register(lambda: termios.tcsetattr(fd, termios.TCSADRAIN, old))
    except (OSError, ImportError):
        return
    while True:
        ch = fd.read(1).lower()
        if ch == b"q":
            state["quit"] = True
            return
        if ch == b"s":
            if REQ.exists():
                REQ.unlink(missing_ok=True)
            else:
                REQ.write_text(time.strftime("%Y-%m-%d %H:%M:%S") + "\n")


def main():
    act = Activity()
    state = {"quit": False}
    threading.Thread(target=keys, args=(state,), daemon=True).start()
    tick = 0
    with Live(screen=True, auto_refresh=False) as live:
        while not state["quit"]:
            try:
                act.poll()
                live.update(render(act, tick, live.console.size.height), refresh=True)
            except Exception as e:  # noqa: BLE001  a half-written file must not take the dashboard down
                live.update(Panel(Text(f"reading the record: {e!r}"), title="dashboard"), refresh=True)
            tick += 1
            for _ in range(10):
                if state["quit"]:
                    break
                time.sleep(0.1)


if __name__ == "__main__":
    sys.exit(main())
