"""Experiment: F16.1c. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f16.1d-gromark-on-the-20-official-letters",
    "title": "F16.1d: Gromark with a free mixed alphabet on the 20 official known letters (EAST set aside): 0195 (bases 2-16 and 26, two- and three-term rules) and 0262 (the rules 0195 left, base 26 to lag 7), each run as recorded with only the known letters changed; K4 against their 10 copies, their plants",
    "family": "16-simple-hand-methods",
    "parent": "0262-f5.2-gromark-free-alphabet-base-26-lag-6-and-longer-lags",
    "changed": (
        "F16.1 (issue #123), fourth part. 0195's and 0262's attack.py loaded from their records and run with only the 20 "
        "official known places (26-34, 64-74): their module-level list of known letters replaced, and their compiled C "
        "and Python loops, which count the known places as 24 (`e < 24`, `range(24)`, `range(k + 1, 24)`), told 20; "
        "each replacement asserted. Everything else as recorded: rules, bases, lags, primers, forms, copies, plants."
    ),
    "hypothesis_expert": (
        "F5 Gromark (05-attacks.md: Bean 2021, 'Kryptos Thoughts'; Gillogly's suggestion 1999, 2004): a numeric running key "
        "from a primer expanded by a lagged sum mod a base, added to the plaintext's place in the standard alphabet and "
        "read off a free mixed cipher alphabet; four forms. 0195 and 0262 decided every primer of the listed rules exactly "
        "on 24 letters: no primer consistent on K4. Criteria revised 2026-11-17 (#124): EAST is second-hand. On 20 letters "
        "each primer faces 20 checks instead of 24, about 19 bits fewer; chance-consistent primers per rule rise by about "
        "26^4 x (alphabet freedom), so some K4 and copy primers are expected to fit; the test is whether K4 has more than "
        "its copies. Bean's base-10 length-5 survivors (05-attacks.md) are inside 0195's space."
    ),
    "hypothesis_eli5": (
        "Gromark makes a long key of digits from a few starting digits, each new digit the sum of earlier ones, and adds "
        "it to the message letter by letter through a scrambled alphabet. Two past experiments tried every starting set "
        "for many rules and found none that fits the known letters, but they needed EAST. Here they run again with the 20 "
        "letters Sanborn published himself."
    ),
    "prediction": (
        "Consistent primers appear on K4 and on the 10 copies in about the same numbers (K4 inside the copies' range in "
        "both runs); plants found as in the originals (0195 2/2, 0262 3/3). No candidates (the alphabet stays partly "
        "free; readings not built)."
    ),
    "method": (
        "1. Load 0195 and 0262 from their records; set their known letters to the 20 official ones and their loop counts "
        "to 20. 2. Run each as recorded. 3. Compare K4's consistent primers with the copies', and with the 24-letter "
        "records (both 0 on K4)."
    ),
    "walkthrough": (
        "1. Choose a base (10), a rule (each new digit is the sum of the digits 5 and 1 places back, mod 10) and five starting digits. "
        "2. Extend the digits to 97. "
        "3. At each official known place, the carved letter must sit in the scrambled alphabet at the known letter's place plus the digit there. "
        "4. If two places need the same carved letter at different places, or two letters at one place, the start fails. "
        "5. Count the starts that never fail, on K4 and on scrambled copies."
    ),
    "expected_minutes": 70,
}

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OFFICIAL = tuple(range(26, 35)) + tuple(range(64, 75))
GROM = [(r"e < 24", "e < 20", 3), (r"range\(24\)", "range(20)", 1), (r"range\(k \+ 1, 24\)", "range(k + 1, 20)", 1)]
PATCHES = {"0195": GROM, "0262": GROM}


def load(prefix):
    path = next((ROOT / "experiments").glob(prefix + "-*")) / "attack.py"
    src = path.read_text()
    for pat, rep, n in PATCHES[prefix]:
        src, k = re.subn(pat, rep, src)
        assert k and (n is None or k == n), (prefix, pat, k)
    assert not re.search(r"<\s*24\b|range\([^)]*24\)", src), prefix
    name = f"frozen{prefix}"
    spec = importlib.util.spec_from_loader(name, loader=None)
    m = importlib.util.module_from_spec(spec)
    m.__file__ = str(path)
    sys.modules[name] = m
    exec(compile(src, str(path), "exec"), m.__dict__)
    from kryptos.facts import KNOWN
    m.ITEMS = sorted((q, KNOWN[q]) for q in OFFICIAL)
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


def summary_24(prefix):
    raw = json.loads((next((ROOT / "experiments").glob(prefix + "-*")) / "raw.json").read_text())
    return raw["bounds"], raw["notes"]


def run(ctx):
    out_b, notes = {}, []
    for prefix in ("0195", "0262"):
        m = load(prefix)
        assert len(m.ITEMS) == 20
        r = m.run(Ctx20(ctx, prefix))
        b24, n24 = summary_24(prefix)
        out_b[prefix] = {"bounds_20": r["bounds"], "notes_20": r["notes"], "notes_24": n24}
        notes.append(f"{prefix}: {r['notes']}")
        ctx.save(f"done:{prefix}", True)
    return {"candidates": [], "bounds": {"item": "F16.1d", "known_places": list(OFFICIAL), **out_b,
                                         "aws_cost_estimate_dollars": 1.0, "modal_cost_estimate_dollars": 0},
            "notes": " | ".join(notes)}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    return load("0195").worked_example(Ctx20(ctx, "0195"), key)
