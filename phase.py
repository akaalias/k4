#!/usr/bin/env python3
"""Phase clock for the loop. The agent ticks it as it moves through an experiment:

    uv run python phase.py design       # thinking, reading the record, writing EXPERIMENT
    uv run python phase.py implement    # writing run/encrypt/worked_example
    uv run python phase.py test         # pytest and dry runs
    uv run python phase.py pause        # waiting on a person; time until the next tick is dropped

run_experiment.py adds the run and record phases itself, folds all of them into
result.json, and resets the clock. If the clock was never ticked, the time since the
previous experiment ended is recorded as "unattributed".
"""
import json
import sys
import time
from pathlib import Path

CLOCK = Path(__file__).resolve().parent / ".phase.json"
PHASES = ("design", "implement", "test", "pause")


def load():
    return json.loads(CLOCK.read_text()) if CLOCK.exists() else {"ticks": []}


def tick(name):
    d = load()
    d["ticks"].append({"phase": name, "t": time.time()})
    CLOCK.write_text(json.dumps(d))


def close(now=None):
    """Return {phase: seconds} and clear the clock. The last tick runs until `now`."""
    d = load()
    now = now or time.time()
    out = {}
    ticks = d.get("ticks", [])
    for i, tk in enumerate(ticks):
        end = ticks[i + 1]["t"] if i + 1 < len(ticks) else now
        if tk["phase"] == "pause":
            continue
        out[tk["phase"]] = out.get(tk["phase"], 0.0) + max(0.0, end - tk["t"])
    if CLOCK.exists():
        CLOCK.unlink()
    return out


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in PHASES:
        sys.exit(f"usage: phase.py {{{'|'.join(PHASES)}}}")
    tick(sys.argv[1])
    print(f"phase: {sys.argv[1]}")
