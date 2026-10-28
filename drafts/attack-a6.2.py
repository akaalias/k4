"""Experiment 0222. See program.md for the contract."""

EXPERIMENT = {
    "slug": "a6-the-climbs-power-on-sanborn-style-plaintext",
    "title": "A6.2: the climbs' power on Sanborn-style plaintext: X stops, K1-K3 windows and three changed letters planted through F1.5's design 2 (one free alphabet at 23, two at 13) and 0125's running-key search, judged by quadgrams and by the blind judge",
    "family": "1-keyed-periodic",
    "parent": "0221-rejudge-the-sampled-verdicts-free-alphabets-and-running-english",
    "changed": (
        "A6.2 (Stage 2, step 4, issue #84). The sampled closes of F1.1 (0139-0142), F1.2 (0143-0146) and F1.3 (0125) "
        "measured their power on clean Carter. Here the planted messages are the judge bench's Sanborn-style classes "
        "(reports/judge-bench.md): Carter with X for every full stop (xstops), 97-letter windows of K1-K3's own plaintexts "
        "with their misspellings and X stops (k123), and clean English with three letters changed (sub3). Four of each go "
        "through each frozen search unchanged: 0140's tempering climb at one free alphabet, Beaufort form, length 23; 0144's "
        "two-alphabet climb at 13; 0125's running-key reading of the forced key. Each plant is found or not by quadgrams "
        "(the verdicts' rule) and by the judge, against the same copies the verdict's power used."
    ),
    "hypothesis_expert": (
        "A6 (knowledge/12-assumptions.md), with C19 (Scheidt 2015, 'what's a period... special characters don't work': X "
        "and Q as stops) and C17/C10 (Sanborn's deliberate misspellings, 'rife with mistakes on purpose', 2005). F1.5's "
        "design 2 (parallel tempering in the set of keys that keep the 24 known letters; 10 runs x 16 replicas x 625 rounds "
        "x 1000 moves) decided F1.1's Beaufort length 23 at 6 of 8 clean plants above their own 6 fitting shuffles (0139) "
        "and F1.2's length 13 at 5 of 5 above 5 kept-place shuffles (0143); 0125's running-key test (208,062 dictionary "
        "tables x 18 readings, the 24-letter forced key scored as English) found 11 of 20 Carter running keys above 50 "
        "shuffles. Those powers were measured on Carter's prose, which a quadgram model scores well. Sanborn's own "
        "plaintexts are not that: K2 has X stops and UNDERGRUUND, K1 IQLUSION, K3 DESPARATLY. The test: the same frozen "
        "searches on 12 plants per arm in the three bench classes; per plant, found when its score is strictly above every "
        "own copy's (6 fitting shuffles of the plant's ciphertext at 23, 6 kept-place shuffles at 13, 0125's 50 shuffles of "
        "K4 for the running key), by quadgram and, separately, by the judge in one blind call per arm. Null per plant: "
        "1/7 (0125: 1/51). Pre-registered rule: an arm whose quadgram power falls below the verdict's stated power (23: "
        "6/8; 13: 5/5, bar 4/5; 0125: 11/20) weakens the close it carried; the close stands only if the judge reaches that "
        "power here and A6.1 (0221) kept K4 inside its copies under the judge at that cell. Otherwise the item goes back "
        "to open in its family table and waits for Alexis."
    ),
    "hypothesis_eli5": (
        "Earlier experiments checked that their searches could find a hidden test message, but the test messages were "
        "clean English from a book. Sanborn's real messages are messier: X between sentences, deliberate misspellings, "
        "odd phrasing. Here we hide messy messages of that kind, run the same searches on them unchanged, and see how "
        "often the search, scored by letter statistics and separately by the judge (a language model that reads one text "
        "at a time without knowing where it came from), picks the hidden message out from scrambled copies of itself."
    ),
    "prediction": (
        "Quadgram power falls on the messy classes: at 23 about 6 of 12 (the climb's quadgram target fights X stops and "
        "K1-K3's misspellings less than it fights noise, so k123 and xstops lose most); at 13 about 9 of 12; 0125 about "
        "5 of 12 (a 24-letter window with an X or a changed letter loses quadgrams). The judge does at least as well as "
        "quadgrams on every arm and reaches the stated power at 13 but not at 23, where the climbed readings are only a "
        "third right. So F1.1's length 23 is weakened, F1.2's length 13 stands, and F1.3 is weakened for quadgrams but "
        "rescued by the judge if 0221's rejudge held. Zero candidates."
    ),
    "method": (
        "1. Plaintexts: per arm 4 xstops (tools/judge_bench.py's xstops_plant), 4 k123 windows (the bench's 12, split 4 per "
        "arm), 4 sub3 (kryptos.plants.english_plant with 3 free letters changed, the bench's damage); the 24 known letters "
        "set. "
        "2. Arm 23: Beaufort form, random alphabet and key of 23 (0120's make_plants rule); 6 own copies, shuffles of the "
        "plant's ciphertext that 0120's exact decider fits at 23 (0140's rule); every text through 0140's frozen _job. "
        "3. Arm 13: two random alphabets and key of 13 (0144's plant4 rule); witness from 0123's decider; 6 own copies "
        "keeping the 24 known places and shuffling the other 73; every text through 0144's frozen _any. "
        "4. Arm 0125: the class text is the running key, under English plaintext (english_plant), on a random table, rule "
        "and key alphabet from 0125's sets; through 0125's frozen _job; its 50 copies regenerated with 0125's seed and "
        "checked against its record. "
        "5. Found by quadgram: the climb's score strictly above every own copy's. Found by the judge: one call per arm on "
        "the plants' readings and their copies', the plant strictly above every own copy; None counts as not found."
    ),
    "walkthrough": (
        "1. Take a messy test message, say a window of K2: ...THEYUSEDTHEEARTHSMAGNETICFIELDXTHEINFORMATION.... "
        "2. Put EASTNORTHEAST and BERLINCLOCK at their places. "
        "3. Encipher it by hand the way the item says: one shuffled alphabet, a key of 23 numbers, Beaufort form. "
        "4. Make six scrambled copies of the ciphertext that the same key length can still fit. "
        "5. Run the same search on the seven texts and keep each best reading. "
        "6. The message is found if its reading scores above all six copies', once by letter statistics and once by the "
        "judge."
    ),
}

import importlib.util
import random
import time
from pathlib import Path

N = 97
ROOT = Path(__file__).resolve().parent
CLASSES = ("xstops", "k123", "sub3")
PER_CLASS = 4
N_OWN = 6
STATED = {"23": (6, 8), "13": (5, 5), "0125": (11, 20)}
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


def _bench():
    if "bench" not in _MODS:
        import sys
        spec = importlib.util.spec_from_file_location("judge_bench", ROOT / "tools/judge_bench.py")
        m = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = m
        spec.loader.exec_module(m)
        _MODS["bench"] = m
    return _MODS["bench"]


def class_texts(rng, arm_index):
    from kryptos.plants import english_plant
    jb = _bench()
    k123 = jb.k123_plants()
    out = []
    for cls in CLASSES:
        for i in range(PER_CLASS):
            if cls == "xstops":
                t = jb.xstops_plant(rng)
            elif cls == "k123":
                t = k123[arm_index * PER_CLASS + i]
            else:
                t = jb.damage(english_plant(22200 + arm_index * 100 + i), 3, rng)
            assert len(t) == N
            out.append((cls, t))
    return out


class _Slow(Exception):
    pass


def _witness_timed(m44, m23, pc, known, rng, secs=20):
    """0144's witness search under an alarm: on some keys 0123's depth-first search runs for minutes; give up and redraw."""
    import signal

    def _raise(*_):
        raise _Slow()
    old = signal.signal(signal.SIGALRM, _raise)
    signal.alarm(secs)
    try:
        return m44.witness4(pc, known, 13, rng, m23)
    except _Slow:
        return None
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)


def _dispatch(args):
    e, inner = args
    m = _MODS[e]
    return e, (m._any(inner) if e == "0144" else m._job(inner))


def running_key_plant(m, rng, alist, pt, key):
    """0125's make_plants with the key text given: the class text is the running key."""
    a = rng.choice(alist); cfg = rng.choice(m.CONFIGS); rule = rng.choice(m.RULES); ka = rng.choice(m.KEYALPHA)
    W = [ord(ch) - 65 for ch in a]
    posW = {le: i for i, le in enumerate(W)}
    ident = {i: i for i in range(26)}
    P = posW if cfg[0] == "W" else ident
    C = posW if cfg.endswith("W") else ident
    Cinv = {v: k for k, v in C.items()}
    kinv = {le: i for i, le in enumerate(W)} if ka == "W" else ident
    ct = []
    for i in range(N):
        kv = kinv[ord(key[i]) - 65]
        pv = P[ord(pt[i]) - 65]
        cv = {"vig": (pv + kv) % 26, "var": (pv - kv) % 26, "beau": (kv - pv) % 26}[rule]
        ct.append(chr(65 + Cinv[cv]))
    truth = "".join(key[q - 1] for a_, b_ in m.STRETCHES for q in range(a_, b_ + 1))
    return "".join(ct), truth


def window_text(w):
    """0125's 24-letter forced stretch, shown at places 35-47 and 49-59 so the judge's masking of 22-34 and 64-74 cannot hide it."""
    return "?" * 34 + w[:13] + "?" + w[13:] + "?" * (N - 34 - 25)


def _s(v):
    return -1 if v is None else v


def run(ctx):
    import json
    import multiprocessing as mp
    import sys
    import types
    from kryptos.plants import english_plant
    from kryptos.scorer import english_score, free_text
    t_start = time.time()
    known = ctx.KNOWN
    m40, m44, m25 = _load("0140"), _load("0144"), _load("0125")
    m20, m23 = m40.load_0120(), m44.load_0123()
    m40.lib(); m44.lib(); m44.lib4()
    deadline = ctx.deadline - 600
    jobs, meta = [], {}
    # arm 23: one free alphabet, Beaufort form (0140's climb, 0139's power rule)
    rng = random.Random(2223)
    for i, (cls, pt) in enumerate(class_texts(rng, 0)):
        alpha = list(ctx.STANDARD_ALPHABET); rng.shuffle(alpha); alpha = "".join(alpha)
        k = [rng.randrange(26) for _ in range(23)]
        pc = m20.beaufort_encrypt(pt, alpha, k)
        assert m20.decide(m20.equations(pc, known, 23), "B", rng)[0] == "fit"
        meta[("23", i)] = {"cls": cls, "pt": pt}
        jobs.append(("0140", ("plant", 23, i, pc, pt, rng.randrange(10 ** 9), deadline)))
        g = 0
        while g < N_OWN:
            sh = list(pc); rng.shuffle(sh); sh = "".join(sh)
            if m20.decide(m20.equations(sh, known, 23), "B", rng)[0] == "fit":
                jobs.append(("0140", ("own", 23, i * 100 + g, sh, None, rng.randrange(10 ** 9), deadline))); g += 1
    # arm 13: two free alphabets (0144's climb, 0143's power rule)
    rng = random.Random(2213)
    kidx = set(q - 1 for q in known)
    free = [j for j in range(N) if j not in kidx]
    redraws = 0
    for i, (cls, pt) in enumerate(class_texts(rng, 1)):
        y0 = None
        while y0 is None:      # the witness search is randomised and can stop 'undecided'; retry, then redraw the key
            P = list(range(26)); C = list(range(26)); rng.shuffle(P); rng.shuffle(C)
            Ci = {v: j for j, v in enumerate(C)}
            k = [rng.randrange(26) for _ in range(13)]
            pc = "".join(chr(65 + Ci[(P[ord(ch) - 65] + k[j % 13]) % 26]) for j, ch in enumerate(pt))
            for _ in range(5):
                y0 = _witness_timed(m44, m23, pc, known, rng)
                if y0 is not None:
                    break
            redraws += y0 is None
        meta[("13", i)] = {"cls": cls, "pt": pt}
        jobs.append(("0144", ("plant", 13, i, pc, pt, rng.randrange(10 ** 9), deadline, y0)))
        for g in range(N_OWN):
            letters = [pc[j] for j in free]; rng.shuffle(letters)
            cp = list(pc)
            for j, ch in zip(free, letters):
                cp[j] = ch
            jobs.append(("0144", ("own", 13, i * 100 + g, "".join(cp), None, rng.randrange(10 ** 9), deadline, y0)))
    # arm 0125: the class text as the running key; 0125's own 50 copies regenerated
    alist = list(m25.alphabets())
    r125 = random.Random(125)
    m25.make_plants(r125, alist, m25.N_PLANTS)            # consumes the seed exactly as 0125 did
    for i in range(m25.N_CONTROLS):
        sh = list(ctx.K4); r125.shuffle(sh)
        jobs.append(("0125", ("copper", i, "".join(sh), None)))
    rng = random.Random(2225)
    for i, (cls, key) in enumerate(class_texts(rng, 2)):
        pt = english_plant(22500 + i)
        pc, truth = running_key_plant(m25, rng, alist, pt, key)
        meta[("0125", i)] = {"cls": cls, "pt": key}
        jobs.append(("0125", ("plant", i, pc, truth)))
    me = sys.modules.get(__name__)
    if getattr(me, "_dispatch", None) is not _dispatch:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    jobs.sort(key=lambda j: {"0144": 0, "0140": 1, "0125": 2}[j[0]])   # longest first
    with mp.get_context("fork").Pool(8) as pool:
        res = pool.map(_dispatch, jobs, chunksize=1)
    compute_s = time.time() - t_start

    arms = {"23": {"plant": {}, "own": {}}, "13": {"plant": {}, "own": {}}, "0125": {"plant": {}, "copies": []}}
    done_all, ok_all = [], True
    for e, r in res:
        if e in ("0140", "0144"):
            kind, L, idx, sc, pt, alpha, k, agree, done, ok = r
            done_all.append(done); ok_all = ok_all and ok
            a = arms[str(L)]
            if kind == "plant":
                a["plant"][idx] = {"q": sc, "reading": pt, "agree": agree}
            else:
                a["own"].setdefault(idx // 100, []).append({"q": sc, "reading": pt})
        else:
            kind, idx, sc, rd, b1, b2, truth = r
            if kind == "copper":
                arms["0125"]["copies"].append({"q": sc, "reading": rd[4]})
            else:
                arms["0125"]["plant"][idx] = {"q": sc, "reading": rd[4], "agree": sum(1 for x, y in zip(rd[4], truth) if x == y),
                                              "recovered": rd[4] == truth}
    saved = json.loads((next((ROOT / "experiments").glob("0125-*")) / "raw.json").read_text())["bounds"]
    copies_ok = sorted(round(c["q"], 4) for c in arms["0125"]["copies"]) == sorted(c["score"] for c in saved["coppers"])

    out, calls, controls = {}, 0, []
    for arm in ("23", "13", "0125"):
        a = arms[arm]
        n = len(a["plant"])
        if arm == "0125":
            ptexts = [window_text(a["plant"][i]["reading"]) for i in range(n)]
            ctexts = [window_text(c["reading"]) for c in a["copies"]]
            v = ctx.judge(ptexts + ctexts); calls += len(ptexts) + len(ctexts)
            pj = [x["score"] for x in v[:n]]; cj = [x["score"] for x in v[n:]]
            qbar, jbar = max(c["q"] for c in a["copies"]), max(_s(x) for x in cj)
            rows = [{"cls": meta[(arm, i)]["cls"], "q": round(a["plant"][i]["q"], 4), "q_found": a["plant"][i]["q"] > qbar,
                     "judge": pj[i], "judge_found": pj[i] is not None and pj[i] > jbar,
                     "window_letters_right": a["plant"][i]["agree"], "recovered": a["plant"][i]["recovered"],
                     "reading": a["plant"][i]["reading"]} for i in range(n)]
            extra = {"copies_quad_max": round(qbar, 4), "copies_judge": cj, "copies_reproduced": copies_ok}
            nones = sum(1 for x in v if x["score"] is None)
        else:
            ptexts = [a["plant"][i]["reading"] or "?" * N for i in range(n)]
            otexts = [[o["reading"] or "?" * N for o in a["own"][i]] for i in range(n)]
            flat = [t for o in otexts for t in o]
            v = ctx.judge(ptexts + flat); calls += len(ptexts) + len(flat)
            pj = [x["score"] for x in v[:n]]
            rows, kpos = [], n
            for i in range(n):
                oj = [x["score"] for x in v[kpos:kpos + len(otexts[i])]]; kpos += len(otexts[i])
                oq = [o["q"] for o in a["own"][i]]
                controls += [english_score(free_text(t)) for t in otexts[i] if "?" not in t]
                rows.append({"cls": meta[(arm, i)]["cls"], "q": round(a["plant"][i]["q"], 4), "own_q": [round(x, 4) for x in oq],
                             "q_found": a["plant"][i]["q"] > max(oq), "judge": pj[i], "own_judge": oj,
                             "judge_found": pj[i] is not None and pj[i] > max(_s(x) for x in oj),
                             "letters_right": a["plant"][i]["agree"], "reading": a["plant"][i]["reading"]})
            extra = {}
            nones = sum(1 for x in v if x["score"] is None)
        qf = sum(r["q_found"] for r in rows); jf = sum(r["judge_found"] for r in rows)
        need, of = STATED[arm]
        out[arm] = {"rows": rows, "quad_found": qf, "judge_found": jf, "of": n,
                    "by_class": {c: {"quad": sum(r["q_found"] for r in rows if r["cls"] == c),
                                     "judge": sum(r["judge_found"] for r in rows if r["cls"] == c), "of": PER_CLASS} for c in CLASSES},
                    "stated_power": f"{need}/{of}", "quad_below_stated": qf / n < need / of,
                    "judge_below_stated": jf / n < need / of, "judge_none": nones, **extra}
    bounds = {
        "item": "A6.2", "classes": list(CLASSES), "per_class": PER_CLASS, "own_copies": N_OWN,
        "arms": {"23": "F1.1, one free alphabet, Beaufort form, length 23, 0140's frozen climb (design 2)",
                 "13": "F1.2, two free alphabets, length 13, 0144's frozen climb (design 2)",
                 "0125": "F1.3, running key on 208,062 dictionary tables, 0125's frozen search, the class text as the key"},
        "null_per_plant": {"23": "1/7", "13": "1/7", "0125": "1/51"},
        "runs_done": {"min": min(done_all), "max": max(done_all)}, "decryption_checked": ok_all,
        "judge_texts_sent": calls, "judge_calls_estimated": 230, "arm13_key_redraws": redraws,
        "result": out, "compute_seconds": round(compute_s), "exhaustive": False,
        "controls": "quadgram scores of the plants' own copies' readings (no candidate is submitted)",
    }
    notes = "; ".join(f"{a}: quadgram {o['quad_found']}/{o['of']}, judge {o['judge_found']}/{o['of']} (stated {o['stated_power']})"
                      for a, o in out.items())
    return {"candidates": [], "bounds": bounds, "notes": notes, "controls": controls}


def encrypt(plaintext, key):
    """No candidate is submitted; Beaufort form on one alphabet for completeness (0140's rule)."""
    return _load("0140").encrypt(plaintext, key)


def worked_example(ctx, key):
    jb = _bench()
    t = jb.k123_plants()[0]
    from kryptos.judge import mask
    return "\n".join(["A6.2 plants Sanborn-style messages. A K1-K3 window with the known words set:", "",
                      f"  message      {t}", f"  judge sees   {mask(t)}", "",
                      "  enciphered with one shuffled alphabet and a key of 23 (Beaufort form), climbed by 0140's search",
                      "  with six scrambled copies; found if its reading beats all six, by quadgrams and by the judge."])
