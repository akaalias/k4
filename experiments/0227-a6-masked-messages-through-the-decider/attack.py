"""Experiment 0227. See program.md for the contract."""

EXPERIMENT = {
    "slug": "a6-masked-messages-through-the-decider",
    "title": "A6.3: masked messages (reversed, an X every kth letter, the message in every nth place) planted through F1.5's design 2 at one free alphabet, Beaufort length 23, found by the decider, by the mask's own battery test and by the judge on the unmasked reading",
    "family": "1-keyed-periodic",
    "parent": "0226-a6-the-climbs-power-on-sanborn-style-plaintext",
    "changed": (
        "A6.3 (Stage 2, step 4, issue #84). A13 found that a forward English climb overwrites a masked message (1 of 22 "
        "masked plants survived 0034/0140/0142's climbs, 0216-0217). Here the question is put to F1.5's design 2, the "
        "decider behind F1.1 and F1.2's sampled closes: the three masks A13.1's battery sees well (reversal: eng_reverse 20 "
        "of 20; an X every kth letter: eng_drop_nth 20 of 20; the message in every nth place, random letters between: "
        "eng_keep_nth 20 of 20) are applied to Carter, the 24 known letters set, enciphered at F1.1's Beaufort length 23 "
        "and climbed by 0140's frozen search with six fitting shuffles of each plant's own ciphertext."
    ),
    "hypothesis_expert": (
        "A6 and A13 (knowledge/12-assumptions.md); C4(a) (Scheidt 2005, 2015: 'I masked the English language', a "
        "plaintext transform before the keyed stage; 'more than one stage'), C19 (X as a stop). Method under test: F1.5 "
        "design 2 (parallel tempering in the check-keeping set, 10 runs x 16 replicas x 625 rounds x 1000 moves) on F1.1's "
        "Beaufort form, one alphabet, length 23 (7 checks), whose close (0139-0140) rests on design 2 finding 6 of 8 clean "
        "plants above their own copies. A masked plaintext has the right key and the right alphabet but its free letters "
        "are not forward English, so the climb, scored by forward quadgrams, has no reason to settle on them. Three ways to "
        "find a masked plant, each against its own 6 copies (null 1/7): (a) the decider's own rule, the climb's quadgram "
        "score; (b) the mask's own test from tools/a13_structure.py on the reading (eng_reverse, eng_drop_nth, "
        "eng_keep_nth); (c) the judge on the reading unmasked with the planted mask's own parameters (an oracle unmask, "
        "applied to the copies' readings alike, the 24 known places set to '?' before unmasking so the judge sees no known "
        "word), one blind call. Pre-registered: if no way finds at least 6 of 8 plants of a mask (0139's bar), the "
        "sampled closes of F1.1 and F1.2 stand as 'closed for unmasked English' only, for that mask."
    ),
    "hypothesis_eli5": (
        "Scheidt said he disguised the English before enciphering it. If the message was written backwards, or had an X "
        "every few letters, or was spread out with junk letters between, a search that tunes the key toward ordinary "
        "English may walk straight past the right key. Here we hide disguised messages, run the same search on them, and "
        "check three ways of noticing them: the search's own score, a pattern test made for that disguise, and the judge "
        "reading the text after the disguise is undone."
    ),
    "prediction": (
        "The decider's own rule finds 0-2 of 8 per mask; the mask's own test finds at most 2 of 8 (the climb fills the free "
        "letters with forward junk, as in 0216); the judge on the unmasked reading finds at most 2 of 8, because the climbed "
        "readings get about a third of the letters right. So F1.1 and F1.2's sampled closes hold for unmasked English only. "
        "Zero candidates."
    ),
    "method": (
        "1. Per mask, 8 plants: Carter (from place 20,000 on, random start), masked as tools/a13_check.py's power test "
        "masks it (reversal; X at every kth place, k 5-11; the message at every nth place from offset o, n 2-4, random "
        "letters between), the 24 known letters set after masking. "
        "2. Enciphered with a random alphabet and key of 23 in the Beaufort form (0120's rule); 6 own copies, shuffles of "
        "the ciphertext that 0120's exact decider fits at 23. "
        "3. Every text through 0140's frozen _job (design 2), all runs to the end. "
        "4. (a) climb score above all 6 own copies'; (b) the mask's battery test above all 6; (c) one judge call on every "
        "reading unmasked with the plant's parameters, known places '?', spacers inserted at the judge's withheld places "
        "22-34 and 64-74 (it masks those places of any text) so no unmasked letter is hidden; above all 6."
    ),
    "walkthrough": (
        "1. Take a sentence from Carter and write it backwards. "
        "2. Put EASTNORTHEAST and BERLINCLOCK at their places. "
        "3. Encipher it with a shuffled alphabet and a key of 23 numbers in the Beaufort form. "
        "4. Make six scrambled copies that the same key length still fits, and run the same search on all seven. "
        "5. Undo the disguise (read the reading backwards) on all seven and ask the judge which reads as English. "
        "6. The disguised message is found if it beats all six copies."
    ),
    "expected_minutes": 45,
}

import importlib.util
import random
import re
import time
from pathlib import Path

N = 97
ROOT = Path(__file__).resolve().parent
MASKS = {"reversal": "eng_reverse", "X every kth": "eng_drop_nth", "message in every nth": "eng_keep_nth"}
PER_MASK = 8
N_OWN = 6
STD = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_MODS = {}


def _load(e):
    if e not in _MODS:
        import sys
        path = next((ROOT / "experiments").glob(f"{e}-*")) / "attack.py"
        spec = importlib.util.spec_from_file_location(f"frozen{e}", path)
        m = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = m
        spec.loader.exec_module(m)
        _MODS[e] = m
    return _MODS[e]


def _a13():
    if "a13" not in _MODS:
        import sys
        spec = importlib.util.spec_from_file_location("a13_structure", ROOT / "tools/a13_structure.py")
        m = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = m
        spec.loader.exec_module(m)
        _MODS["a13"] = m
    return _MODS["a13"]


def _batteries(readings):
    """tools/a13_structure.py's battery on each reading, unchanged, in one subprocess: numpy is not a project
    dependency and the battery is run with `uv run --with numpy` (tools/a13_structure.py's own usage line)."""
    import json
    import subprocess
    code = ("import json, sys; sys.path.insert(0, 'tools'); sys.path.insert(0, '.'); import a13_structure as a; "
            "print(json.dumps([{k: float(v) for k, v in a.battery(r).items()} for r in json.load(sys.stdin)]))")
    out = subprocess.run(["uv", "run", "--quiet", "--with", "numpy", "python", "-c", code], cwd=ROOT,
                         input=json.dumps(readings), capture_output=True, text=True, check=True)
    return json.loads(out.stdout.strip().splitlines()[-1])


def _carter():
    src = (ROOT / "knowledge/sources/carter-1923-tomb-of-tutankhamen-vol1.txt").read_text(errors="ignore").upper()
    return re.sub("[^A-Z]", "", src)


def masked(mask, rng, letters):
    """-> (masked text with the known letters set, parameters); the masks of tools/a13_check.py's power test."""
    from kryptos.facts import KNOWN
    s0 = rng.randrange(20000, len(letters) - 400)
    plain = list(letters[s0:s0 + 2 * N])
    if mask == "reversal":
        t, par = "".join(plain[:N])[::-1], {}
    elif mask == "X every kth":
        k = rng.randrange(5, 12)
        t, par = "".join("X" if i % k == k - 1 else plain.pop(0) for i in range(N)), {"k": k}
    else:
        n, o = rng.randrange(2, 5), None
        o = rng.randrange(n)
        t, par = "".join(plain.pop(0) if i % n == o else rng.choice(STD) for i in range(N)), {"n": n, "o": o}
    t = list(t)
    for q, ch in KNOWN.items():
        t[q - 1] = ch
    return "".join(t), par


def unmask(reading, mask, par):
    """The planted mask undone with its own parameters; the 24 known places blanked first; spacers at the judge's
    withheld places 22-34 and 64-74 so that every unmasked letter stays visible."""
    from kryptos.facts import KNOWN
    r = ["?" if (i + 1) in KNOWN else c for i, c in enumerate(reading)]
    if mask == "reversal":
        u = r[::-1]
    elif mask == "X every kth":
        u = [c for i, c in enumerate(r) if i % par["k"] != par["k"] - 1]
    else:
        u = [c for i, c in enumerate(r) if i % par["n"] == par["o"]]
    u = "".join(u)
    # the judge withholds places 22-34 and 64-74 of whatever it reads ('#'); spacers there, so no unmasked letter is lost
    return u[:21] + "?" * 13 + u[21:50] + "?" * 11 + u[50:]


def _job(args):
    return _MODS["0140"]._job(args)


def _s(v):
    return -1 if v is None else v


def run(ctx):
    import multiprocessing as mp
    import sys
    import types
    t_start = time.time()
    known = ctx.KNOWN
    m40 = _load("0140"); m20 = m40.load_0120(); m40.lib()
    letters = _carter()
    deadline = ctx.deadline - 600
    rng = random.Random(2233)
    jobs, meta = [], {}
    i = 0
    for mask in MASKS:
        for _ in range(PER_MASK):
            pt, par = masked(mask, rng, letters)
            alpha = list(STD); rng.shuffle(alpha); alpha = "".join(alpha)
            k = [rng.randrange(26) for _ in range(23)]
            pc = m20.beaufort_encrypt(pt, alpha, k)
            assert m20.decide(m20.equations(pc, known, 23), "B", rng)[0] == "fit"
            meta[i] = {"mask": mask, "par": par, "pt": pt}
            jobs.append(("plant", 23, i, pc, pt, rng.randrange(10 ** 9), deadline))
            g = 0
            while g < N_OWN:
                sh = list(pc); rng.shuffle(sh); sh = "".join(sh)
                if m20.decide(m20.equations(sh, known, 23), "B", rng)[0] == "fit":
                    jobs.append(("own", 23, i * 100 + g, sh, None, rng.randrange(10 ** 9), deadline)); g += 1
            i += 1
    me = sys.modules.get(__name__)
    if getattr(me, "_job", None) is not _job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    res = []
    ctx.progress(0, len(jobs), "climbs")
    with mp.get_context("fork").Pool(8) as pool:
        for r in pool.imap_unordered(_job, jobs, chunksize=1):
            res.append(r)
            ctx.progress(len(res), len(jobs), "climbs")
    compute_s = time.time() - t_start
    plant, own, done_all, ok_all = {}, {}, [], True
    for kind, L, idx, sc, pt, alpha, k, agree, done, ok in res:
        done_all.append(done); ok_all = ok_all and ok
        if kind == "plant":
            plant[idx] = {"q": sc, "reading": pt, "agree": agree}
        else:
            own.setdefault(idx // 100, []).append({"q": sc, "reading": pt})
    # (c) one blind judge call: every reading unmasked with its plant's own parameters
    texts, spans = [], []
    for i in sorted(plant):
        mk, par = meta[i]["mask"], meta[i]["par"]
        a = len(texts)
        texts.append(unmask(plant[i]["reading"], mk, par))
        texts += [unmask(o["reading"], mk, par) for o in own[i]]
        spans.append((a, len(texts)))
    v = ctx.judge(texts)
    order = [(i, None) for i in sorted(plant)] + [(i, g) for i in sorted(plant) for g in range(len(own[i]))]
    bat = dict(zip(order, _batteries([plant[i]["reading"] if g is None else own[i][g]["reading"] for i, g in order])))
    rows = []
    for i, (a, b) in zip(sorted(plant), spans):
        mk = meta[i]["mask"]; test = MASKS[mk]
        sp = bat[(i, None)][test]
        so = [bat[(i, g)][test] for g in range(len(own[i]))]
        jp, jo = v[a]["score"], [x["score"] for x in v[a + 1:b]]
        rows.append({"mask": mk, "par": meta[i]["par"], "letters_right": plant[i]["agree"],
                     "q": round(plant[i]["q"], 4), "own_q": [round(o["q"], 4) for o in own[i]],
                     "found_decider": plant[i]["q"] > max(o["q"] for o in own[i]),
                     "test": test, "test_value": sp, "own_test": so, "found_test": sp > max(so),
                     "judge_unmasked": jp, "own_judge_unmasked": jo,
                     "found_judge": jp is not None and jp > max(_s(x) for x in jo),
                     "reading": plant[i]["reading"], "unmasked": texts[a], "judge_reading": v[a]["reading"]})
    by_mask = {}
    for mk in MASKS:
        rs = [r for r in rows if r["mask"] == mk]
        by_mask[mk] = {"decider": sum(r["found_decider"] for r in rs), "test": sum(r["found_test"] for r in rs),
                       "judge": sum(r["found_judge"] for r in rs), "any": sum(r["found_decider"] or r["found_test"] or r["found_judge"] for r in rs),
                       "of": len(rs), "letters_right": [r["letters_right"] for r in rs],
                       "verdict": "found at power" if max(sum(r["found_decider"] for r in rs), sum(r["found_test"] for r in rs),
                                                         sum(r["found_judge"] for r in rs)) * 4 >= 3 * len(rs) else "not found: closes hold for unmasked English only"}
    from kryptos.scorer import english_score, free_text
    controls = [english_score(free_text(o["reading"])) for i in own for o in own[i] if o["reading"]]
    bounds = {
        "item": "A6.3", "masks": {m: {"test": t, "power_on_flat_noise_A13.1": "20 of 20"} for m, t in MASKS.items()},
        "decider": "0140's frozen climb (F1.5 design 2), one free alphabet, Beaufort form, length 23",
        "per_mask": PER_MASK, "own_copies": N_OWN, "null_per_plant": "1/7", "bar": "6 of 8 (0139's 6/8)",
        "runs_done": {"min": min(done_all), "max": max(done_all)}, "decryption_checked": ok_all,
        "judge_texts_sent": len(texts), "judge_calls_estimated": 168,
        "expected_total_time": "168 texts at about 110 s each (0140's climb) = about 18,500 core-seconds, 40-50 min on 8 cores",
        "judge_none": sum(1 for x in v if x["score"] is None),
        "by_mask": by_mask, "rows": rows, "compute_seconds": round(compute_s), "exhaustive": False,
        "controls": "quadgram scores of the plants' own copies' readings (no candidate is submitted)",
    }
    notes = "; ".join(f"{m}: decider {b['decider']}/{b['of']}, test {b['test']}/{b['of']}, judge {b['judge']}/{b['of']}" for m, b in by_mask.items())
    return {"candidates": [], "bounds": bounds, "notes": notes, "controls": controls}


def encrypt(plaintext, key):
    """No candidate is submitted; Beaufort form on one alphabet for completeness (0140's rule)."""
    return _load("0140").encrypt(plaintext, key)


def worked_example(ctx, key):
    rng = random.Random(1)
    pt, par = masked("reversal", rng, _carter())
    return "\n".join(["A6.3 plants a masked message. A reversed Carter passage with the known words set after masking:", "",
                      f"  plant        {pt}", f"  unmasked     {unmask(pt, 'reversal', par)}", "",
                      "  enciphered at one free alphabet, Beaufort, key length 23; climbed by 0140's search with six copies;",
                      "  found by the climb's score, by eng_reverse, or by the judge on the reading read backwards."])
