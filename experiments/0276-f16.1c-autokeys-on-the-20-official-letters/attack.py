"""Experiment: F16.1c. See program.md for the contract."""

EXPERIMENT = {
    "slug": "f16.1c-autokeys-on-the-20-official-letters",
    "title": "F16.1c: both autokeys on the 20 official known letters (EAST set aside): 0149 (one free alphabet, every lag), 0212 (ciphertext autokey on every keyword table, progressive key, 0-2 slips or a skipped step) and 0213 (plaintext autokey, 0-2 breaks or a lost step), each run as recorded with only the known letters changed; K4 against their own copies, their own plants, the judge as before",
    "family": "16-simple-hand-methods",
    "parent": "0213-plaintext-autokey-with-slips-and-a-lost-step",
    "changed": (
        "F16.1 (issue #123), third part. The three autokey attacks are loaded from their records and run with a context "
        "whose known letters are the 20 Sanborn published himself (26-34, 64-74), everything else as recorded: same "
        "tables, lags, slips, copies, plants, quadgram cut and judge. The only source edit: 0212's and 0213's compiled "
        "C loops have the count of known places written as 24 (`e<24`, `f<24`, `e0<24`); it is replaced by 20 and "
        "0212's `24 - len(slots)` by `len(known) - len(slots)`, each replacement asserted. Their 24-letter records are "
        "read back to list what only EAST closed."
    ),
    "hypothesis_expert": (
        "F1's autokey arm and A1 (C27(a), C27(c); NSA 1992 'plaintext autokey', 05-attacks.md; Gillogly; Bean 2024 "
        "'From Gromark to Autoclave'). Criteria revised 2026-11-17 (#124): EAST is second-hand. Models as recorded: "
        "0149 c_i = A^-1(A(p_i) +/- A(x_{i-L})) with x the plain (pt) or cipher (ct) letter L back, one free alphabet A, "
        "lags 1-96, three forms, decided exactly; 0212 ciphertext autokey on 487,734 keyword-table setups, lags 1-96, "
        "with 0-2 failed checks or one skipped step, and the progressive key; 0213 plaintext autokey on 35,343 tables, "
        "lags 1-52, chains between known letters with 0-2 breaks or one lost step. Without EAST, checks that tied 22-25 "
        "to 26-34 and 64-74 vanish: fits come at shorter lags and more often, on K4 and copies alike; the question is "
        "whether K4 stands outside its copies, and whether its readings beat theirs at the judge."
    ),
    "hypothesis_eli5": (
        "In an autokey cipher the key is the message itself (or the cipher text), shifted along by some distance. Three "
        "past experiments tested every such scheme we could list and found nothing, but each needed EAST, which Sanborn "
        "confirmed only privately. Here the same three searches run again with only the 20 letters he published, on the "
        "carving and on the same scrambled copies, with the same planted test messages."
    ),
    "prediction": (
        "More fitting cells than with 24 letters on K4 and copies alike; K4 inside its copies on every count (0149's fit "
        "counts per kind and form, 0212's and 0213's shortest fitting lag); K4's best judged reading not above every "
        "copy's; plants found as in the originals (0212 5/5, 0213 3/3) or nearly. No candidate passes."
    ),
    "method": (
        "1. Load 0149, 0212, 0213's attack.py from their records (0212 and 0213 with 24 -> 20 in the C loops). "
        "2. Give each a context whose known letters are the 20 official ones; run each unchanged otherwise. "
        "3. Compare each count with its own copies, as in the originals. 4. Read the 24-letter records and list the "
        "lags or cells that fit on 20 letters but not on 24. 5. Readings stay in the bounds."
    ),
    "walkthrough": (
        "1. Choose a table, a form and a lag, say 12. "
        "2. For each official known place q past 12, the key letter is the plain (or carved) letter 12 places earlier. "
        "3. Where that earlier letter is also known (or carved), look up the table: the known letter at q under that key must give the carved letter at q. "
        "4. Count the checks that fail; allow up to two as slips. "
        "5. Places 22-25 are not used: their letters are read, not checked. "
        "6. Do the same on scrambled copies and compare."
    ),
    "expected_minutes": 30,
}

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OFFICIAL = tuple(range(26, 35)) + tuple(range(64, 75))
PATCHES = {
    "0149": [],
    "0212": [(r"e<24", "e<20", 3), (r"e0<24", "e0<20", 1), (r"24 - len\(slots\)", "len(known) - len(slots)", 1)],
    "0213": [(r"e<24", "e<20", None), (r"f<24", "f<20", None)],
}


def load(prefix):
    path = next((ROOT / "experiments").glob(prefix + "-*")) / "attack.py"
    src = path.read_text()
    for pat, rep, n in PATCHES[prefix]:
        src, k = re.subn(pat, rep, src)
        assert k and (n is None or k == n), (prefix, pat, k)
    assert prefix == "0149" or not re.search(r"<\s*24\b", src), prefix
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


def summary_24(prefix):
    raw = json.loads((next((ROOT / "experiments").glob(prefix + "-*")) / "raw.json").read_text())
    return raw["bounds"], raw["notes"]


def run(ctx):
    out_b, notes, judged = {}, [], {}
    for prefix in ("0149", "0212", "0213"):
        m = load(prefix)
        c = Ctx20(ctx, prefix)
        r = m.run(c)
        b24, n24 = summary_24(prefix)
        cands = r.get("candidates", [])
        out_b[prefix] = {"bounds_20": r["bounds"], "notes_20": r["notes"], "notes_24": n24,
                         "readings_20": [{"plaintext": x.get("plaintext"), "key": x.get("key")} for x in cands[:20]],
                         "controls_20": r.get("controls")}
        notes.append(f"{prefix}: {r['notes']}")
        ctx.save(f"done:{prefix}", True)
    # what only EAST closed: 0149 per cell, 0212/0213 by shortest lag
    b49 = out_b["0149"]["bounds_20"]["summary"]
    s49 = summary_24("0149")[0]["summary"]
    only49 = {k: sorted(set(v["k4_fit_lags"]) - set(s49[k]["k4_fit_lags"])) for k, v in b49.items()}
    out_b["only_east_closed"] = {"0149_lags_by_kind_form": only49}
    return {"candidates": [], "bounds": {"item": "F16.1c", "known_places": list(OFFICIAL), **out_b,
                                         "aws_cost_estimate_dollars": 0.3, "judge_calls_estimate": "under 1,000 (0212: 56, 0213: 194 on 24 letters)"},
            "notes": " | ".join(notes)}


def encrypt(plaintext, key):
    return load("0212").encrypt(plaintext, key)


def worked_example(ctx, key):
    return load("0212").worked_example(Ctx20(ctx, "0212"), key)
