"""Experiment: F16.1c. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f16.1e-running-keys-on-the-20-official-letters",
    "title": "F16.1e: the named running keys (0210: K1-K3 plain and cipher, Carter, the tableau and the other named texts, every offset, both directions, on the standard, KRYPTOS and keyword tables) on the 20 official known letters (EAST set aside), with up to five slips; K4 against 0210's 20 copies, its plants and the judge",
    "family": "16-simple-hand-methods",
    "parent": "0210-running-keys-with-slips-at-known-places",
    "changed": (
        "F16.1 (issue #123), fifth part. 0210's attack.py loaded from its record and run with only the 20 official known "
        "places (26-34, 64-74). Its pigeonhole index used 8 blocks of 3 known places to be exact for up to 7 slips; 20 "
        "places give 6 whole blocks, so the blocks are taken over the first 18 places and the slip limit is 5 (exact for "
        "5 or fewer), each replacement asserted; the bit counts use 20 places. Everything else as recorded: sources, "
        "tables, offsets, copies, plants, judge."
    ),
    "hypothesis_expert": (
        "F1's running-key arm (C7, C9: the earlier texts as instructions or key; Gillogly 1999 and Schridde 2017 found the "
        "K1-K3 running keys give nonsense, 05-attacks.md). Model as 0210: c = table(p, key letter from a named text at "
        "offset o + i), forward or backward, Vigenere, Beaufort or variant, on the standard, KRYPTOS or keyword tables, "
        "1.36 x 10^9 trials. Criteria revised 2026-11-17 (#124): EAST is second-hand. With 20 checks and up to 5 slips, "
        "chance settings stay near 10^-6 per run: any K4 setting would be a lead; the judge reads every setting found."
    ),
    "hypothesis_eli5": (
        "A running key takes its key letters from a book or an earlier passage, starting at some page and line. "
        "Experiment 210 tried every starting place in every text we named, allowing up to seven slips, and found nothing, "
        "but it counted EAST. Here we try again with the 20 letters Sanborn published himself, allowing up to five slips."
    ),
    "prediction": (
        "No setting on K4 or any copy at up to 5 slips; plants found 3 of 3 (their planted offset, no setting on their "
        "own copies). Zero candidates."
    ),
    "method": (
        "1. Load 0210 from its record; give it the 20 official known letters; blocks of 3 over the first 18 places, slip "
        "limit 5. 2. Run it as recorded: every source, offset, direction, table and form, through the block index, each "
        "hit checked on all 20 places. 3. Readings of every setting found go to quadgrams and the judge, K4's and the "
        "copies' together."
    ),
    "walkthrough": (
        "1. Take a text, say K3's plaintext, and a starting letter in it. "
        "2. Write the text from there under K4, one letter per place. "
        "3. At each of the 20 official known places, look up on the table what the known letter and the text letter give. "
        "4. Count the places where that is not the carved letter; five or fewer may be slips. "
        "5. Try every starting letter, both directions, every table; read the message wherever a start passes."
    ),
    "expected_minutes": 15,
}

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OFFICIAL = tuple(range(26, 35)) + tuple(range(64, 75))
PATCHES = {"0210": [(r"range\(0, 24, 3\)", "range(0, 18, 3)", 1), (r"KMAX = 7", "KMAX = 5", 1),
                     (r"math\.comb\(24", "math.comb(20", 3), (r"\(24 - k\)", "(20 - k)", 1)]}


def load(prefix):
    path = next((ROOT / "experiments").glob(prefix + "-*")) / "attack.py"
    src = path.read_text()
    for pat, rep, n in PATCHES[prefix]:
        src, k = re.subn(pat, rep, src)
        assert k and (n is None or k == n), (prefix, pat, k)
    assert "range(0, 18, 3)" in src and "KMAX = 5" in src, prefix
    name = f"frozen{prefix}"
    spec = importlib.util.spec_from_loader(name, loader=None)
    m = importlib.util.module_from_spec(spec)
    m.__file__ = str(path)
    sys.modules[name] = m
    exec(compile(src, str(path), "exec"), m.__dict__)
    return m


class Ctx20:
    """The harness context with only the 20 official known letters; saves under a prefix."""

    def __init__(self, ctx, prefix):
        self._c, self._p = ctx, prefix
        self.KNOWN = {q: ctx.KNOWN[q] for q in OFFICIAL}
        self.saved = {k[len(prefix) + 1:]: v for k, v in (getattr(ctx, "saved", {}) or {}).items() if k.startswith(prefix + ":")}

    def save(self, key, value):
        self._c.save(f"{self._p}:{key}", value)

    def progress(self, done, total, label=""):
        self._c.progress(done, total, f"{self._p} {label}")

    def __getattr__(self, a):
        return getattr(self._c, a)


def run(ctx):
    m = load("0210")
    r = m.run(Ctx20(ctx, "0210"))
    raw = json.loads((next((ROOT / "experiments").glob("0210-*")) / "raw.json").read_text())
    b = r["bounds"]
    b.update({"item": "F16.1e", "known_places": list(OFFICIAL), "notes_24": raw["notes"], "aws_cost_estimate_dollars": 0.1,
              "judge_calls_estimate": "the readings of every setting found: 3 on 24 letters; expected under 50"})
    out = {"candidates": r.get("candidates", []), "bounds": b, "notes": r["notes"]}
    if r.get("controls"):
        out["controls"] = r["controls"]
    return out


def encrypt(plaintext, key):
    return load("0210").encrypt(plaintext, key)


def worked_example(ctx, key):
    return load("0210").worked_example(Ctx20(ctx, "0210"), key)
