"""A13's cheap check, passes 1 and 2: run tools/a13_structure.py's battery on readings that put
all 24 known letters in place, and on the same method's readings of scrambled copies of K4.

    uv run --with numpy python tools/a13_check.py pass1-regen   # copies' readings, own methods (about 1 h on 8 cores)
    uv run --with numpy python tools/a13_check.py pass2         # whole-setting readings, K4 and copies
    uv run --with numpy python tools/a13_check.py pass4         # A13.4: 0207, 0212-0214, K4 and their copies
    uv run --with numpy python tools/a13_check.py power         # the battery on planted masked English
    uv run --with numpy python tools/a13_check.py report        # tables for reports/a13-structure-check.md
    uv run --with numpy python tools/a13_check.py replicate TEST N SEED   # a pass-2 candidate against N fresh copies

Pass 1: the 31 saved candidates in experiments/*/raw.json with all 24 known letters. Their
controls are the same experiment's search, imported from its frozen attack.py and run unchanged
on fresh scrambled copies of K4 made the way that experiment made them (plain shuffles where any
shuffle fits; shuffles that pass 0120's exact decider for the free-alphabet cells; shuffles of the
73 unknown places for 0148). For each experiment and test the statistic is the best value over
that text's readings; K4's is ranked among the copies'.

Pass 2: settings that fix the reading by themselves, with no climb. A repeating key on a fixed
pair of alphabets at key lengths 26-29 is fixed by the known letters in all but 3-5 key slots;
the reading is written with "." where a free slot falls, and every test uses the fixed letters
only. Alphabet pool: standard, KRYPTOS and every vocabulary word's keyword mixing (0035, 0048),
all ordered pairs, three modes. K4 and 20 plain shuffles (at 27-29 every shuffle fits; at 26
only the settings that fit are kept, as on K4).

Outputs go to reports/a13-structure-data/ (JSON).
"""
import importlib.util
import json
import math
import random
import sys
import time
from multiprocessing import get_context
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np  # noqa: E402

from kryptos.facts import K4, KNOWN, load_vocabulary  # noqa: E402
from kryptos.scorer import english_score  # noqa: E402
from tools.a13_structure import TESTS, battery  # noqa: E402

N = 97
OUT = ROOT / "reports" / "a13-structure-data"
EXP = {e: next((ROOT / "experiments").glob(f"{e}-*")) for e in
       ("0034", "0035", "0048", "0120", "0137", "0140", "0142", "0148")}
_MODS = {}


def mod(e):
    if e not in _MODS:
        spec = importlib.util.spec_from_file_location(f"a{e}", EXP[e] / "attack.py")
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        _MODS[e] = m
    return _MODS[e]


def fits24(pt):
    return len(pt) == N and all(pt[q - 1] == a for q, a in KNOWN.items())


def saved_candidates():
    """Every saved candidate with all 24 known letters: {experiment: [(label, reading)]}."""
    out = {}
    for d in sorted((ROOT / "experiments").glob("*/raw.json")):
        try:
            raw = json.loads(d.read_text())
        except Exception:  # noqa: BLE001
            continue
        rows = [c for c in raw.get("candidates", []) if fits24(c["plaintext"])]
        if rows:
            out[d.parent.name[:4]] = [(c.get("key_description", "")[:60], c["plaintext"]) for c in rows]
    return out


# ---- pass 1: the same search on copies ---------------------------------------------------------

def _best_by_period(res, ip, ipt):
    best = {}
    for r in res:
        if r[ip] not in best or r[0] > best[r[ip]][0]:
            best[r[ip]] = r
    return [(f"period {P}", best[P][ipt]) for P in sorted(best)]


def p1_job(args):
    e, idx, text, seed = args
    t0 = time.time()
    far = lambda: 10 ** 9  # noqa: E731
    m = mod(e)
    rng = random.Random(seed)
    if e == "0034":
        from kryptos.alphabets import conventions
        res = m.sweep(text, KNOWN, list(conventions()), english_score, rng, m.RESTARTS, far, m.PERIODS)
        rows = _best_by_period(res, 1, 3)
    elif e in ("0035", "0048"):
        pool = m.pool_of(load_vocabulary())
        res = m.sweep(text, KNOWN, pool, english_score, rng, m.RESTARTS, far)
        rows = _best_by_period(res, 1, 5)
    elif e == "0120":
        rows = []
        for L in m.LENGTHS:
            sc, alpha, k, pt = m.climb(text[L], KNOWN, L, seed + L)
            rows.append((f"length {L}", pt))
    elif e == "0137":
        rows = []
        for L in m.LENGTHS:
            r = m.climb_text(text[L], KNOWN, L, seed + L, m.RESTARTS, time.time() + 10 ** 6)
            rows.append((f"length {L}", r[1]))
    else:  # 0140 (23), 0142 (26), 0148 (19, slip at 33)
        L = {"0140": 23, "0142": 26, "0148": 19}[e]
        r = m.climb_text(text, KNOWN, L, seed, 1000, time.time() + 10 ** 6)
        rows = [(f"length {L}", r[1])]
    return e, idx, rows, time.time() - t0


def p1_copies(n_fixed=10, n_free=12):
    """Copies made the way each experiment made its own."""
    rng = random.Random(1300)
    jobs = []
    for e in ("0034", "0035", "0048"):
        for i in range(n_fixed):
            sh = list(K4); rng.shuffle(sh)
            jobs.append((e, i, "".join(sh), rng.randrange(10 ** 9)))
    m0120 = mod("0120")

    def fitting(L):
        while True:
            sh = list(K4); rng.shuffle(sh); sh = "".join(sh)
            if m0120.decide(m0120.equations(sh, KNOWN, L), "B", rng)[0] == "fit":
                return sh
    for e in ("0120", "0137"):  # both lengths; one copy per length per job
        for i in range(n_free):
            jobs.append((e, i, {23: fitting(23), 26: fitting(26)}, rng.randrange(10 ** 9)))
    for e, L in (("0140", 23), ("0142", 26)):
        for i in range(n_free):
            jobs.append((e, i, fitting(L), rng.randrange(10 ** 9)))
    free = [i for i in range(N) if (i + 1) not in KNOWN]
    for i in range(n_free):
        cp = list(K4); letters = [K4[j] for j in free]; rng.shuffle(letters)
        for j, ch in zip(free, letters):
            cp[j] = ch
        jobs.append(("0148", i, "".join(cp), rng.randrange(10 ** 9)))
    return jobs


def pass1_regen():
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "pass1_copies.json"
    done = json.loads(path.read_text()) if path.exists() else {}
    jobs = [j for j in p1_copies() if f"{j[0]}/{j[1]}" not in done]
    # long jobs first
    cost = {"0034": 0, "0048": 1, "0120": 2, "0137": 3}
    jobs.sort(key=lambda j: cost.get(j[0], 9))
    print(f"{len(jobs)} jobs", flush=True)
    with get_context("fork").Pool(8) as pool:
        for e, idx, rows, secs in pool.imap_unordered(p1_job, jobs):
            done[f"{e}/{idx}"] = {"rows": rows, "seconds": round(secs, 1)}
            path.write_text(json.dumps(done, indent=0))
            print(f"{e} copy {idx}: {len(rows)} readings, {secs:.0f} s", flush=True)


# ---- pass 4 (A13.4): readings kept since 2026-10-18 --------------------------------------------
# 0207, 0212, 0213 and 0214 saved K4's readings but only the copies' scores. Their frozen attack.py
# is imported, its search state rebuilt the way its run() builds it, and its own per-text search
# called on K4 and on the same seeded copies; every reading it returns ("?" for an undetermined
# letter, read as "."), with the 24 known letters set as the candidates set them, goes through the
# battery. Plants are not rerun.

P4 = {"0207": 2070, "0212": 2130, "0213": 2140, "0214": 2150}  # first copy seed, as each run()
P4_COPIES = 20


def _p4_mod(e):
    if e not in EXP:
        EXP[e] = next((ROOT / "experiments").glob(f"{e}-*"))
    return mod(e)


def p4_setup(e):
    from array import array
    import ctypes
    m = _p4_mod(e)
    vocab = list(load_vocabulary())
    if e == "0212":
        m._STATE["ca"], m._STATE["known"] = m.CA(m.table_setups(vocab), KNOWN), KNOWN
    elif e == "0213":
        m._STATE["pa"] = m.PA(m.table_setups(vocab), KNOWN)
    elif e == "0214":
        kq = sorted(KNOWN)
        routes, seen, lands = [], set(), array("i")
        for fam, name, wh in m.route_maps(vocab):
            land = tuple(wh[q - 1] for q in kq)
            if land in seen:
                continue
            seen.add(land)
            routes.append((fam, name, wh))
            lands.extend(land)
        m._KEEP.append(lands)
        m._STATE["lands"] = (ctypes.c_int * len(lands)).from_buffer(lands)
        m._STATE["routes"], m._STATE["known"] = routes, KNOWN
    return m


def p4_readings(e, text):
    m = _p4_mod(e)
    if e == "0207":
        recs = m.search(text, KNOWN, english_score)[1]
    else:
        recs = m.one_text(text)["recs"]
    out = set()
    for r in recs:  # a slipped known place reads the carved letter; the candidate's plaintext carries the known word
        x = list(r["reading"].replace("?", "."))
        for q, a in KNOWN.items():
            x[q - 1] = a
        out.add("".join(x))
    return sorted(out)


def p4_texts(e):
    m = _p4_mod(e)
    return [("k4", K4)] + [(f"copy{i}", m.shuffled(K4, P4[e] + i)) for i in range(P4_COPIES)]


def p4_job(args):
    e, tag, text = args
    t0 = time.time()
    rd = p4_readings(e, text)
    best = {t: (-math.inf, None) for t in TESTS}
    for s in rd:
        for t, v in battery(s).items():
            if v > best[t][0]:
                best[t] = (v, s)
    return e, tag, {"n_readings": len(rd), "best": best, "seconds": round(time.time() - t0, 1)}


def pass4():
    path = OUT / "pass4.json"
    done = json.loads(path.read_text()) if path.exists() else {}
    for e in P4:
        if e in done and len(done[e]) == P4_COPIES + 1:
            continue
        p4_setup(e)  # before the fork, so every worker inherits the state
        jobs = [(e, tag, t) for tag, t in p4_texts(e)]
        done[e] = {}
        with get_context("fork").Pool(8) as pool:
            for e_, tag, r in pool.imap_unordered(p4_job, jobs):
                done[e][tag] = r
                print(f"{e} {tag}: {r['n_readings']} readings, {r['seconds']} s", flush=True)
        path.write_text(json.dumps(done, indent=0, default=float))


# ---- pass 2: settings that fix the reading -----------------------------------------------------

P2_PERIODS = (26, 27, 28, 29)
P2_COPIES = 20


def p2_pool():
    m = mod("0035")
    pool = m.pool_of(load_vocabulary())
    return list(pool.items())


def p2_readings(text, pool):
    """Every fitting setting's reading, '.' where the key slot is free. Returns {reading: label}."""
    known = sorted(KNOWN)
    out = {}
    idx_cache = {name: {ch: i for i, ch in enumerate(A)} for name, A in pool}
    for pname, pa in pool:
        pidx = idx_cache[pname]
        for cname, ca in pool:
            cidx = idx_cache[cname]
            cts = [cidx[c] for c in text]
            for m in ("vig", "beau", "varbeau"):
                for P in P2_PERIODS:
                    fixed = {}
                    ok = True
                    for q in known:
                        p, c = pidx[KNOWN[q]], cts[q - 1]
                        k = (c - p) % 26 if m == "vig" else (c + p) % 26 if m == "beau" else (p - c) % 26
                        s = (q - 1) % P
                        if fixed.setdefault(s, k) != k:
                            ok = False
                            break
                    if not ok:
                        continue
                    r = []
                    for i in range(N):
                        k = fixed.get(i % P)
                        if k is None:
                            r.append(".")
                        else:
                            c = cts[i]
                            r.append(pa[(c - k) % 26 if m == "vig" else (k - c) % 26 if m == "beau" else (c + k) % 26])
                    s = "".join(r)
                    assert all(s[q - 1] == KNOWN[q] for q in known)
                    out.setdefault(s, f"P{P} {m} {pname} | {cname}")
    return out


def p2_text_job(args):
    tag, text = args
    t0 = time.time()
    pool = p2_pool()
    rd = p2_readings(text, pool)
    best = {t: (-math.inf, None, None) for t in TESTS}
    by_period = {P: {t: -math.inf for t in TESTS} for P in P2_PERIODS}
    for s, label in rd.items():
        b = battery(s)
        P = int(label.split()[0][1:])
        for t, v in b.items():
            if v > best[t][0]:
                best[t] = (v, s, label)
            if v > by_period[P][t]:
                by_period[P][t] = v
    return tag, {"n_readings": len(rd), "best": best, "by_period": by_period, "seconds": round(time.time() - t0, 1)}


def p2_one_job(args):
    """One test only, on one text: the best value over every fitting setting's reading."""
    tag, text, test = args
    from tools.a13_structure import N as _N, _sep_stats, carter_stats, codes
    rd = p2_readings(text, p2_pool())
    best = -math.inf
    for s in rd:
        if test in ("sep_words", "sep_regular"):
            w, r = _sep_stats(codes(s), carter_stats()[1])
            v = w if test == "sep_words" else r
        else:
            v = battery(s)[test]
        best = max(best, v)
    return tag, best


def replicate(test, n, seed):
    """A pass-2 candidate on one test against n fresh plain shuffles (seed given in the report)."""
    rng = random.Random(seed)
    texts = [("k4", K4, test)]
    for i in range(n):
        sh = list(K4); rng.shuffle(sh); texts.append((f"copy{i}", "".join(sh), test))
    res = {}
    with get_context("fork").Pool(8) as pool:
        for tag, v in pool.imap_unordered(p2_one_job, texts):
            res[tag] = v
    k = res.pop("k4")
    above = sum(1 for v in res.values() if v >= k)
    out = {"test": test, "seed": seed, "copies": n, "k4": k, "copies_at_or_above": above,
           "p": (above + 1) / (n + 1), "copies_max": max(res.values()), "values": res}
    (OUT / f"replicate-{test}.json").write_text(json.dumps(out, indent=0, default=float))
    print(f"{test}: K4 {k:.4f}, {above} of {n} copies at or above (p = {(above + 1) / (n + 1):.4f}), copies max {max(res.values()):.4f}")


def pass2():
    OUT.mkdir(parents=True, exist_ok=True)
    rng = random.Random(1302)
    texts = [("k4", K4)]
    for i in range(P2_COPIES):
        sh = list(K4); rng.shuffle(sh); texts.append((f"copy{i}", "".join(sh)))
    res = {}
    with get_context("fork").Pool(8) as pool:
        for tag, r in pool.imap_unordered(p2_text_job, texts):
            res[tag] = r
            print(tag, r["n_readings"], r["seconds"], flush=True)
    (OUT / "pass2.json").write_text(json.dumps(res, indent=0, default=float))


# ---- power: does each test see the mask it is built for? ---------------------------------------

def power():
    """Planted 97-letter English (Carter 1923 passages with the 24 known letters set), masked in
    the way each test targets, against random letters drawn from K4's letter counts with the
    known letters fixed. Reports, per test, how many of 20 plants beat all 200 random texts."""
    import re
    from kryptos.facts import KRYPTOS_ALPHABET as KRY, STANDARD_ALPHABET as STD
    src = re.sub("[^A-Z ]", "", re.sub(r"\s+", " ", (ROOT / "knowledge/sources/carter-1923-tomb-of-tutankhamen-vol1.txt").read_text(errors="ignore").upper()))
    words_src = src.split()
    letters_src = src.replace(" ", "")
    rng = random.Random(1303)

    def setk(t):
        t = list(t)
        for q, a in KNOWN.items():
            t[q - 1] = a
        return "".join(t)

    def plain():
        s0 = rng.randrange(20000, len(letters_src) - 200)
        return letters_src[s0:s0 + N]

    def xspaced():
        w0 = rng.randrange(5000, len(words_src) - 100)
        return "X".join(words_src[w0:w0 + 40])[:N]

    def affine():
        a = rng.choice([3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]); b = rng.randrange(26)
        return "".join(STD[(a * STD.index(c) + b) % 26] for c in plain())

    def affine_kry():
        a = rng.choice([3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]); b = rng.randrange(26)
        return "".join(STD[STD.index(KRY[(a * KRY.index(c) + b) % 26])] for c in plain())

    def subst():
        al = list(STD); rng.shuffle(al)
        return "".join(al[STD.index(c)] for c in plain())

    def columns():
        w = rng.randrange(3, 30); t = plain()
        fwd = [r * w + c for c in range(w) for r in range((N + w - 1) // w) if r * w + c < N]
        return "".join(t[i] for i in fwd)

    def nulls():
        n = rng.randrange(3, 9); o = rng.randrange(n); t = list(plain()); out = []
        for i in range(N):
            out.append(rng.choice(STD) if i % n == o else t.pop(0))
        return "".join(out)

    def step():
        k = rng.randrange(2, 96); t = plain(); out = [""] * N
        for i in range(N):
            out[(i * k) % N] = t[i]
        return "".join(out)

    def reverse():
        return plain()[::-1]

    def pairs():  # a 5x5-style pair code over 6 letters
        sym = rng.sample(STD, 6); t = plain()
        return "".join(sym[STD.index(c) // 6 % 6] + sym[STD.index(c) % 6] for c in t)[:N]

    def interleaved():  # the message in every nth place, random letters between
        n = rng.randrange(2, 5); o = rng.randrange(n); t = list(plain())
        return "".join(t.pop(0) if i % n == o else rng.choice(STD) for i in range(N))

    def xregular():  # an X every k letters
        k = rng.randrange(5, 12); t = list(plain())
        return "".join("X" if i % k == k - 1 else t.pop(0) for i in range(N))

    masks = {"none": plain, "X spaces": xspaced, "X every kth": xregular, "message in every nth": interleaved, "affine std": affine, "affine KRYPTOS": affine_kry,
             "letter swap": subst, "columns": columns, "nulls every nth": nulls, "ring step": step,
             "reversal": reverse, "pair code": pairs}
    cnt = np.bincount([ord(c) - 65 for c in K4], minlength=26) / N
    nulls_b = [battery(setk("".join(rng.choices(STD, weights=cnt, k=N)))) for _ in range(200)]
    top = {t: max(b[t] for b in nulls_b) for t in TESTS}
    out = {}
    for name, f in masks.items():
        bs = [battery(setk(f())) for _ in range(20)]
        out[name] = {t: sum(1 for b in bs if b[t] > top[t]) for t in TESTS}
    (OUT).mkdir(parents=True, exist_ok=True)
    (OUT / "power.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


def _rank_rows(k4_stats, copy_stats):
    """Per test: K4's value, the copies' range, K4's rank (1 = above every copy), ties counted against K4."""
    rows = {}
    for t in TESTS:
        k = k4_stats[t]
        cs = [c[t] for c in copy_stats]
        rows[t] = {"k4": k, "min": min(cs), "max": max(cs), "rank": 1 + sum(1 for c in cs if c >= k) if k > -math.inf else len(cs) + 1,
                   "n": len(cs), "outside": k > max(cs)}
    return rows


def _fmt(v):
    return "none" if v == -math.inf else f"{v:.3f}"


def report():
    sc = saved_candidates()
    cp = json.loads((OUT / "pass1_copies.json").read_text())
    summary = {"pass1": {}, "pass2": {}}
    print("## Pass 1\n")
    cells = outside = 0
    expect = 0.0
    for e, cands in sc.items():
        k4b = [battery(r) for _, r in cands]
        k4s = {t: max(b[t] for b in k4b) for t in TESTS}
        copies = [v["rows"] for k, v in cp.items() if k.startswith(e + "/")]
        cstats = []
        for rows in copies:
            bs = [battery(r) for _, r in rows if r and fits24(r)]
            if bs:
                cstats.append({t: max(b[t] for b in bs) for t in TESTS})
        if not cstats:
            print(f"{e}: no copies yet\n")
            continue
        rr = _rank_rows(k4s, cstats)
        summary["pass1"][e] = {"k4_readings": len(cands), "copies": len(cstats), "rows": rr}
        print(f"### {e}: {len(cands)} K4 readings, {len(cstats)} copies\n")
        print("| test | K4 | copies min | copies max | K4 rank |\n|---|---|---|---|---|")
        for t in TESTS:
            r = rr[t]
            if t != "eng_base":
                cells += 1; outside += r["outside"]; expect += 1 / (r["n"] + 1)
            print(f"| {t} | {_fmt(r['k4'])} | {_fmt(r['min'])} | {_fmt(r['max'])} | {r['rank']} of {r['n'] + 1} |")
        print()
    print(f"pass 1: {outside} of {cells} cells outside (eng_base excluded); luck alone expects {expect:.1f}\n")
    summary["pass1_totals"] = {"cells": cells, "outside": outside, "expected": expect}
    p2 = json.loads((OUT / "pass2.json").read_text())
    cop = [k for k in p2 if k != "k4"]
    rr = _rank_rows({t: p2["k4"]["best"][t][0] for t in TESTS}, [{t: p2[c]["best"][t][0] for t in TESTS} for c in cop])
    print(f"## Pass 2: K4 {p2['k4']['n_readings']} readings; copies {min(p2[c]['n_readings'] for c in cop)}-{max(p2[c]['n_readings'] for c in cop)} each, {len(cop)} copies\n")
    print("| test | K4 | copies min | copies max | K4 rank | K4's best setting |\n|---|---|---|---|---|---|")
    o2 = 0
    for t in TESTS:
        r = rr[t]
        o2 += r["outside"] and t != "eng_base"
        print(f"| {t} | {_fmt(r['k4'])} | {_fmt(r['min'])} | {_fmt(r['max'])} | {r['rank']} of {r['n'] + 1} | {p2['k4']['best'][t][2]} |")
    print(f"\npass 2: {o2} of {len(TESTS) - 1} outside; luck alone expects {(len(TESTS) - 1) / (len(cop) + 1):.2f}")
    for t in TESTS:
        if rr[t]["outside"]:
            print(f"  outside: {t}: {p2['k4']['best'][t][1]}  ({p2['k4']['best'][t][2]})")
    summary["pass2"] = {"rows": rr, "outside": o2}
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1, default=float))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "report":
        report()
        sys.exit()
    if cmd == "pass1-regen":
        pass1_regen()
    elif cmd == "pass2":
        pass2()
    elif cmd == "power":
        power()
    elif cmd == "pass4":
        pass4()
    elif cmd == "replicate":
        replicate(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
    else:
        sys.exit(__doc__)
