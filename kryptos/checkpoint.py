"""Checkpoints: a run keeps each finished unit of work, so a stop, a Modal drop or a crash loses nothing (issue #105).

An attack splits its search into units (a setting, a copy, a plant) and, from the main process, calls
ctx.save(key, value) as each one finishes. ctx.saved holds the units an earlier run of the same attack.py already
finished: skip those and use their values. Program.md gives every job its own seed, so a unit's value does not
depend on when or where it ran, and a resumed run ends where an unbroken one would.

The file is data/checkpoints/<hash of attack.py>.jsonl, one JSON line per unit: any change to attack.py starts
afresh. run_experiment.py deletes it when a run ends without an error.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "data" / "checkpoints"


def path_for(attack_path, root=None):
    """The checkpoint file of this exact attack.py."""
    digest = hashlib.sha256(Path(attack_path).read_bytes()).hexdigest()[:16]
    return (Path(root) / "data" / "checkpoints" if root else DIR) / f"{digest}.jsonl"


def load(path):
    """Units saved so far, {key: value}. A line cut short by a kill is skipped."""
    saved = {}
    try:
        lines = Path(path).read_text().splitlines()
    except OSError:
        return saved
    for line in lines:
        try:
            row = json.loads(line)
            saved[row["k"]] = row["v"]
        except (ValueError, KeyError, TypeError):
            continue
    return saved


class Saver:
    """ctx.save: appends one line per finished unit and flushes it at once."""

    def __init__(self, path):
        self.path = Path(path)
        self.count = 0

    def __call__(self, key, value):
        if not isinstance(key, str):
            raise TypeError(f"ctx.save: the key must be a string, got {type(key).__name__}")
        line = json.dumps({"k": key, "v": value}) + "\n"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "a") as f:
            f.write(line)
            f.flush()
        self.count += 1


def new_lines(path, offset):
    """Whole lines appended to path since offset: (bytes, new offset). For sending Modal's lines home."""
    try:
        with open(path, "rb") as f:
            f.seek(offset)
            data = f.read()
    except OSError:
        return b"", offset
    end = data.rfind(b"\n") + 1          # never send a line still being written
    return data[:end], offset + end
