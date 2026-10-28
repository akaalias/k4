"""Experiment 0252. See program.md for the contract."""

EXPERIMENT = {
    "slug": "d2-one-run-decider-power-and-cost-on-schedules-and-moves",
    "title": "D2: the one-run decider's power and cost on F1.4's hand key schedules and on F6.1's moves, one free alphabet: 24 clean and 24 Sanborn-style plants per class, each on a setting K4 itself fits",
    "family": "1-keyed-periodic",
    "parent": "0229-d1-one-free-alphabet-power-per-run-with-enough-plants",
    "changed": (
        "D2 (issue #77), first measurement. D1 was decided on 2026-10-28 (#100): one design-2 run, copies climbed one at "
        "a time, qualifies for one free alphabet. Its power was measured only on plain periodic keys (F1.1, L23 and L26). "
        "Here 0140's compiled climb is generalised from 'key letter i mod L, reading in carved order' to any slot map and "
        "any reading order, so the same climb runs on F1.4's key schedules (skip, stutter, back and forth, triangle, "
        "square, line restart) and on F6.1's moves (0129/0130's type-1 library, either order); its power is measured per "
        "cell class on settings K4 itself fits, with the time per climb, and every cost-blocked one-alphabet cell is "
        "re-costed from it."
    ),
    "hypothesis_expert": (
        "F1.4 (hand key schedules, C20(d), 0126-0128) and F6.1 (one free alphabet before or after a type-1 move, C1(a), "
        "0129, 0130) were closed exact where no setting fits and blocked by cost where K4 fits at the copies' rate: 555 "
        "one-alphabet slot partitions under the schedules (0127, 0128) and about 443,000 (move, order, form, length) "
        "settings (0129, 0130), each needing F1.5's design-2 decider at 20-30 min. D1 (0228, 0229) found one tempering run "
        "as strong as ten for one free alphabet (pooled 66 of 96 plants against 67), and Alexis allowed it with every "
        "close stating its measured power. The decider's climb (0140) only needs, for each carved letter, which key slot "
        "enciphered it and where it stands in the message; the known letters give the same same-slot checks. So one "
        "generalised climb covers both families. Unknown: its power on these slot structures (a schedule gives uneven "
        "slot sizes; a move scatters the known places over the slots) and its time per setting. Measured on settings drawn "
        "from those K4 fits, so the power is the power of the decisions D2 reopens. Clue entries: C20(d) (the tableau "
        "rows and schedules as Sanborn's 'slightly different' use of the table), C1(a) (a move, then the table)."
    ),
    "hypothesis_eli5": (
        "Two groups of possible ciphers were left untested because each candidate setting took half an hour to judge, "
        "and there are hundreds (key-skipping rules) or hundreds of thousands (a shuffle of the letters, then the cipher "
        "table). A faster judge was approved yesterday. Before using it here we check that it still finds hidden test "
        "messages in these two groups, and time it, so we know what testing every candidate would cost."
    ),
    "prediction": (
        "Generalised climb reproduces 0140's scores exactly on plain periodic settings. One-run power (found above all 6 "
        "own copies, null 1/7): F1.4 schedules clean about 0.8, Sanborn-style about 0.6; F6.1 at lengths 8-10 higher "
        "(about 0.9 and 0.7, more checks per slot); F6.1 at 11-26 about 0.7 and 0.55. Every class pooled at least 0.5. "
        "Cost: F1.4's one-alphabet residue (a few thousand full settings over both forms) under 100 core-hours, so it "
        "reopens within the $20 line; F6.1 at lengths 6-10 (about 7,400 settings) around 150 core-hours, near the line; "
        "F6.1 at 11-26 above 5,000 core-hours, which waits for money. Zero candidates."
    ),
    "method": (
        "1. The climb: 0140's C source, patched in four places (a slot per carved letter instead of i mod L, a message "
        "place per carved letter, the added form beside Beaufort, the known places given as carved places), checked "
        "against 0140's unpatched library on the same seeds. "
        "2. F1.4 settings: every schedule of 0128 (skip m 2-30, stutter, triangle, square, line restart, back and forth) "
        "at every slot count, as a slot map over all 97 places, deduplicated; each decided exactly on K4 in both forms "
        "with 0128's decide(); the fitting ones are the cost count. "
        "3. F6.1 settings: 0129's library (27,852 maps), order A (move, then table) and B (table, then move), both forms; "
        "K4's fits recounted exactly at lengths 6-10 with 0129's decide(); 11-26 taken from 0129 and 0130's records. "
        "4. Four classes: F1.4 skip, F1.4 other schedules, F6.1 lengths 8-10, F6.1 lengths 11-26. Per class 24 clean "
        "plants (Carter windows, 0120's rule) and 24 Sanborn-style (0226's classes: X stops, K1-K3 windows, three letters "
        "changed), each on its own setting drawn at random from K4's fitting settings in the class, random alphabet and "
        "key; 6 own copies each, shuffles that the exact decider fits at that setting. "
        "5. One tempering run per text (16 replicas x 625 rounds x 1000 moves, 0140's temperatures), time recorded. A "
        "plant is found when its best is strictly above all 6 own copies' bests. "
        "6. Cost per setting = time per climb x (1 + 3.10, the expected copies climbed one at a time against 12) + time "
        "to make the copies; total per cell = cost x K4's fitting settings, in core-hours and Modal dollars."
    ),
    "walkthrough": (
        "1. Pick a key-skipping rule (say: one key letter skipped every 7 letters, key of 11 letters) or a letter shuffle "
        "followed by a key of 9 letters. "
        "2. Write down, for each of the 97 carved letters, which key letter enciphered it. "
        "3. Hide a test message under that rule with a shuffled alphabet and a random key. "
        "4. Make six scrambled copies of its ciphertext that the same rule could still have produced. "
        "5. Run one tempering search on the hidden message and on each copy, scoring the readings as English. "
        "6. The rule's judge works if the hidden message scores above all six copies; repeat for 48 messages per group "
        "and time each search."
    ),
    "expected_minutes": 45,
}

import ctypes
import importlib.util
import os
import random
import time
from pathlib import Path

N = 97
ROOT = Path(__file__).resolve().parent
PLANTS = 24
N_OWN = 6
RUNS = 1
SEQ_COPIES = sum(1 / (j + 1) for j in range(12))     # expected copies climbed one at a time against 12 (0228)
DOLLARS_PER_CORE_HOUR = 0.04716 + 0.00799 / 4        # tools/remote_run.py's rate per vCPU (memory = cpu / 4)
CLASSES = ("F1.4 skip", "F1.4 other", "F6.1 8-10", "F6.1 11-26")
_MODS = {}


def _load(e):
    if e not in _MODS:
        import sys
        path = next((ROOT / "experiments").glob(f"{e}-*")) / "attack.py"
        spec = importlib.util.spec_from_file_location(f"frozen{e}", path)
        m = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = m
        spec.loader.exec_module(m)
        if hasattr(m, "ROOT"):
            m.ROOT = ROOT
        _MODS[e] = m
    return _MODS[e]


# ---- the generalised climb: 0140's C source, patched ----

PATCHES = [
    ("static int NCH, CH[64][4],",
     "static int SLOT[128], MPOS[128], FORM;\nstatic int NCH, CH[64][4],", 1),
    ("for (int j = 0; j < NREP; j++) k[REPS[j]] = (x[REPC[j]] + x[REPP[j]]) % 26;",
     "for (int j = 0; j < NREP; j++) k[REPS[j]] = FORM ? (x[REPC[j]] + x[REPP[j]]) % 26 : (x[REPC[j]] - x[REPP[j]] + 26) % 26;", 2),
    ("for (int j = 0; j < NREP; j++) k[REPS[j]] = (rx[REPC[j]] + rx[REPP[j]]) % 26;",
     "for (int j = 0; j < NREP; j++) k[REPS[j]] = FORM ? (rx[REPC[j]] + rx[REPP[j]]) % 26 : (rx[REPC[j]] - rx[REPP[j]] + 26) % 26;", 1),
    ("static int init(int *x) {\n    for (int t = 0; t < 100000; t++) if (init_try(x)) return 1;\n    return 0;\n}",
     "static int HAVEW, WX[26];\nint set_witness(const int *w, int on) { HAVEW = on; for (int i = 0; i < 26; i++) WX[i] = w[i]; return 0; }\n"
     "static int init(int *x) {\n    for (int t = 0; t < (HAVEW ? 200 : 100000); t++) if (init_try(x)) return 1;\n"
     "    if (HAVEW) { for (int i = 0; i < 26; i++) x[i] = WX[i]; return 1; }\n    return 0;\n}", 1),
    ("for (int i = 0; i < N; i++) pt[i] = inv[((k[i % L] - x[C[i]]) % 26 + 26) % 26];",
     "for (int i = 0; i < N; i++) pt[MPOS[i]] = inv[FORM ? ((k[SLOT[i]] - x[C[i]]) % 26 + 26) % 26 : ((x[C[i]] - k[SLOT[i]]) % 26 + 26) % 26];", 1),
]

SETUP2 = r"""
// setup2: as setup, with a slot and a message place per carved letter, the form (1 Beaufort, 0 added), and the
// known places given as carved places. Same-slot checks: Beaufort x[c0]+x[p0] = x[c]+x[p]; added x[c0]-x[p0] = x[c]-x[p].
int setup2(const double *tab, const int *ct, int n, int l, const int *slot, const int *mpos, int form,
           const int *kpos, const int *klet, int nk) {
    TAB = tab; N = n; L = l; NCH = 0; NREP = 0; NFREE = 0; FORM = form;
    for (int i = 0; i < n; i++) { C[i] = ct[i]; SLOT[i] = slot[i]; MPOS[i] = mpos[i]; }
    int first[64]; for (int s = 0; s < l; s++) first[s] = -1;
    for (int le = 0; le < 26; le++) INCH[le] = 0;
    for (int j = 0; j < nk; j++) {
        int s = slot[kpos[j]], c = ct[kpos[j]], p = klet[j];
        if (first[s] < 0) { first[s] = j; REPS[NREP] = s; REPC[NREP] = c; REPP[NREP] = p; NREP++; }
        else {
            int j0 = first[s];
            if (form) { CH[NCH][0] = ct[kpos[j0]]; CH[NCH][1] = klet[j0]; CH[NCH][2] = c; CH[NCH][3] = p; }
            else      { CH[NCH][0] = ct[kpos[j0]]; CH[NCH][1] = p; CH[NCH][2] = c; CH[NCH][3] = klet[j0]; }
            for (int q = 0; q < 4; q++) INCH[CH[NCH][q]] = 1;
            NCH++;
        }
    }
    for (int s = 0; s < l; s++) if (first[s] < 0) FREE[NFREE++] = s;
    return 0;
}
"""


def glib():
    """The patched library (compiled once per process) and 0140's quadgram table."""
    if "g" not in _MODS:
        import subprocess
        import tempfile
        m = _load("0140")
        m.lib()                                  # builds 0140's table (and its own library, for the check)
        src = m.C_SOURCE
        for old, new, count in PATCHES:
            assert src.count(old) == count, (old, src.count(old))
            src = src.replace(old, new)
        src += SETUP2
        d = tempfile.mkdtemp(prefix="k4_0252_")
        open(os.path.join(d, "g.c"), "w").write(src)
        subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", os.path.join(d, "g.so"), os.path.join(d, "g.c")],
                       check=True, capture_output=True)
        L_ = ctypes.CDLL(os.path.join(d, "g.so"))
        L_.ptemper.restype = ctypes.c_double
        L_.ptemper.argtypes = m.lib().ptemper.argtypes
        _MODS["g"] = L_
    return _MODS["g"]


def full_alphabet(w, seed):
    """The decider's witness (places of the letters in the checks) completed with the free places at random."""
    rng = random.Random(seed)
    x = dict(w[0])
    free = [v for v in range(26) if v not in set(x.values())]
    rng.shuffle(free)
    return [x[le] if le in x else free.pop() for le in range(26)]


def climb(text, st, seed, witness=None):
    """One run of 0140's tempering on the setting st = (slot, mpos, nslots, form). -> (best, seconds, reading).
    witness: the exact decider's alphabet, used as the start only when 200 of 0140's random depth-first starts fail
    (many checks at short lengths), so that a text the decider fits always gets a climb."""
    from kryptos.facts import KNOWN
    m = _MODS["0140"]
    L_ = glib()
    slot, mpos, n, form = st
    carved = {mp: j for j, mp in enumerate(mpos)}
    kp = sorted(KNOWN)
    CT = (ctypes.c_int * N)(*[ord(ch) - 65 for ch in text])
    KP = (ctypes.c_int * 24)(*[carved[q - 1] for q in kp])
    KL = (ctypes.c_int * 24)(*[ord(KNOWN[q]) - 65 for q in kp])
    L_.setup2(m._LIB["tab"], CT, N, n, (ctypes.c_int * N)(*slot), (ctypes.c_int * N)(*mpos), int(form == "B"), KP, KL, 24)
    L_.set_witness((ctypes.c_int * 26)(*(full_alphabet(witness, seed) if witness else [0] * 26)), int(bool(witness)))
    t0 = time.time()
    bp = (ctypes.c_int * 128)(); bx = (ctypes.c_int * 52)(); bk = (ctypes.c_int * 64)()
    sc = L_.ptemper(seed * 100003, 1, m.PT_R, m.PT_ROUNDS, m.PT_MOVES, m.PT_T0, m.T1, bp, bx, bk)
    return round(sc, 5), round(time.time() - t0, 2), "".join(chr(65 + bp[i]) for i in range(N))


def self_check(ctx):
    """The patched library on plain periodic Beaufort settings gives 0140's own scores on the same seeds."""
    from kryptos.facts import KNOWN
    m = _load("0140")
    L0 = m.lib()
    out = []
    for L, seed in ((23, 7), (26, 11)):
        kp = sorted(KNOWN)
        CT = (ctypes.c_int * N)(*[ord(ch) - 65 for ch in ctx.K4])
        KP = (ctypes.c_int * 24)(*[q - 1 for q in kp])
        KL = (ctypes.c_int * 24)(*[ord(KNOWN[q]) - 65 for q in kp])
        L0.setup(m._LIB["tab"], CT, N, L, KP, KL, 24)
        bp = (ctypes.c_int * 128)(); bx = (ctypes.c_int * 52)(); bk = (ctypes.c_int * 64)()
        a = round(L0.ptemper(seed * 100003, 1, m.PT_R, 60, m.PT_MOVES, m.PT_T0, m.T1, bp, bx, bk), 5)
        st = (tuple(i % L for i in range(N)), tuple(range(N)), L, "B")
        g = glib()
        carved = list(range(N))
        g.setup2(m._LIB["tab"], CT, N, L, (ctypes.c_int * N)(*st[0]), (ctypes.c_int * N)(*carved), 1, KP, KL, 24)
        bp2 = (ctypes.c_int * 128)()
        b = round(g.ptemper(seed * 100003, 1, m.PT_R, 60, m.PT_MOVES, m.PT_T0, m.T1, bp2, bx, bk), 5)
        out.append((L, a, b))
        assert a == b, (L, a, b)
    return out


# ---- settings ----

def canon(labels):
    m, t = {}, []
    for x in labels:
        m.setdefault(x, len(m)); t.append(m[x])
    return tuple(t)


def f14_settings():
    """{group: [(name, slot map over 97 places, slot count)]}, every 0128 schedule at every slot count, deduplicated."""
    m = _load("0128")
    out, seen = {"F1.4 skip": [], "F1.4 other": []}, set()

    def add(group, name, labels):
        c = canon(labels)
        if (group, c) not in seen:
            seen.add((group, c)); out[group].append((name, c, max(c) + 1))
    for fam, setting, f in m.schedules():
        nmax = 31 if fam.startswith("F") else 26
        for n in range(2, nmax + 1):
            add("F1.4 skip" if fam.startswith("B") else "F1.4 other", f"{fam} {setting} n={n}", [f(i) % n for i in range(N)])
    for n in range(2, 27):
        for ends in (True, False):
            seq = m.back_and_forth(n, ends)
            if len(seq) < 2:
                continue
            for phi in range(len(seq)):
                add("F1.4 other", f"D back and forth n={n} ends={'repeated' if ends else 'once'} phi={phi}",
                    [seq[(i + phi) % len(seq)] for i in range(N)])
    return out


def eqs_for(text, st):
    from kryptos.facts import KNOWN
    slot, mpos, n, form = st
    carved = {mp: j for j, mp in enumerate(mpos)}
    return [(slot[carved[q - 1]], ord(KNOWN[q]) - 65, ord(text[carved[q - 1]]) - 65) for q in sorted(KNOWN)]


def witness(text, st, rng=None):
    """The exact decider's witness if the setting fits the text (re-checked), else None."""
    eqs = eqs_for(text, st)
    if not _load("0129").l1_ok(eqs):
        return None
    status, w = _load("0128").decide(eqs, st[3], rng)
    if status != "fit":
        return None
    w = ({a[1]: v for a, v in w[0].items()}, w[1])          # 0128 files places under ("x", letter)
    assert _load("0129").check_witness(eqs, st[3], w)
    return w


def fits(text, st, rng=None):
    return witness(text, st, rng) is not None


def move_setting(where, o, L, form):
    """Slot and message place of each carved letter: A move then table, B table then move (0129's planted())."""
    slot, mpos = [0] * N, [0] * N
    for i in range(N):
        j = where[i]
        mpos[j] = i
        slot[j] = j % L if o == "A" else i % L
    return (tuple(slot), tuple(mpos), L, form)


def encipher(pt, st, order, key):
    """order[letter] = place in the free alphabet; Beaufort x[c] = k - x[p], added x[c] = x[p] + k."""
    slot, mpos, n, form = st
    inv = {v: i for i, v in enumerate(order)}
    out = []
    for j in range(N):
        p = ord(pt[mpos[j]]) - 65
        v = (key[slot[j]] - order[p]) % 26 if form == "B" else (order[p] + key[slot[j]]) % 26
        out.append(chr(65 + inv[v]))
    return "".join(out)


def decipher(ct, st, order, key):
    slot, mpos, n, form = st
    inv = {v: i for i, v in enumerate(order)}
    pt = [""] * N
    for j in range(N):
        c = order[ord(ct[j]) - 65]
        pt[mpos[j]] = chr(65 + inv[(key[slot[j]] - c) % 26 if form == "B" else (c - key[slot[j]]) % 26])
    return "".join(pt)


# ---- workers ----

def _f14_job(args):
    group, items, k4 = args
    rng = random.Random(len(items))
    return group, [(name, slot, n, form) for name, slot, n in items for form in ("V", "B")
                   if fits(k4, (slot, tuple(range(N)), n, form), rng)]


def _f61_job(args):
    lo, hi, k4, Ls = args
    lib = _MODS["lib"]
    rng = random.Random(lo)
    cnt = {}
    for r in range(lo, hi):
        for o in ("A", "B"):
            for L in Ls:
                for form in ("V", "B"):
                    if fits(k4, move_setting(lib[r][1], o, L, form), rng):
                        cnt[f"{o}{form}{L}"] = cnt.get(f"{o}{form}{L}", 0) + 1
    return cnt


def _copies_job(args):
    key, pc, st, seed = args
    rng = random.Random(seed)
    out, tries = [], 0
    while len(out) < N_OWN and tries < 200000:
        sh = list(pc); rng.shuffle(sh); sh = "".join(sh); tries += 1
        w = witness(sh, st, rng)
        if w is not None:
            out.append((sh, w))
    return key, out, tries


def _climb_job(args):
    key, text, st, seed, w = args
    return key, climb(text, st, seed, w)


def run(ctx):
    import multiprocessing as mp
    import sys
    import types
    t_start = time.time()
    W = int(os.environ.get("K4_WORKERS", 8))
    me = sys.modules.get(__name__)
    if getattr(me, "_climb_job", None) is not _climb_job:
        mm = types.ModuleType(__name__); mm.__dict__.update(globals()); sys.modules[__name__] = mm
    m20, m26 = _load("0140").load_0120(), _load("0226")
    _load("0128"); _load("0129")
    check = self_check(ctx)
    _MODS["lib"] = _load("0129").route_library(ctx.vocabulary)
    lib = _MODS["lib"]
    k4 = ctx.K4
    ctx.progress(0, 4, "settings")

    # 1. F1.4's settings and K4's fits, both forms (exact)
    f14 = f14_settings()
    jobs = [(g, items[i::W * 4], k4) for g, items in f14.items() for i in range(W * 4)]
    k4fit = {g: [] for g in f14}
    with mp.get_context("fork").Pool(W) as pool:
        for g, got in pool.imap_unordered(_f14_job, jobs):
            k4fit[g].extend(got)
        for g in k4fit:
            k4fit[g].sort()
        ctx.progress(1, 4, "settings")
        # 2. F6.1: K4's fits at lengths 6-10 recounted exactly
        step = max(1, len(lib) // (W * 8))
        f61 = {}
        for cnt in pool.imap_unordered(_f61_job, [(lo, min(len(lib), lo + step), k4, (6, 7, 8, 9, 10))
                                                  for lo in range(0, len(lib), step)]):
            for k, v in cnt.items():
                f61[k] = f61.get(k, 0) + v
    ctx.progress(2, 4, "settings")

    # 3. plants, each on a setting K4 fits, drawn per class
    rng = random.Random(2520)
    prng = random.Random(2521)
    src_clean = {c: m20.make_plants(ctx.KNOWN, 10, rng, PLANTS) for c in CLASSES}
    arms = {"F1.4 skip": (0, 1), "F1.4 other": (2, 0), "F6.1 8-10": (1, 2), "F6.1 11-26": (0, 1)}
    plants, meta = [], {}
    for c in CLASSES:
        texts = [("clean", pt) for _, pt in src_clean[c]]
        for a in arms[c]:
            texts += m26.class_texts(rng, a)
        for idx, (cls, pt) in enumerate(texts):
            while True:
                if c.startswith("F1.4"):
                    name, slot, n, form = k4fit[c][prng.randrange(len(k4fit[c]))]
                    st = (slot, tuple(range(N)), n, form)
                else:
                    Ls = range(8, 11) if c == "F6.1 8-10" else range(11, 27)
                    r = prng.randrange(len(lib)); o = prng.choice("AB"); L = prng.choice(list(Ls)); form = prng.choice("VB")
                    st = move_setting(lib[r][1], o, L, form)
                    name = f"{lib[r][0]} order {o} L={L} {form}"
                    if not fits(k4, st, prng):
                        continue
                break
            order = list(range(26)); prng.shuffle(order)
            key = [prng.randrange(26) for _ in range(st[2])]
            pc = encipher(pt, st, order, key)
            assert decipher(pc, st, order, key) == pt and fits(pc, st, prng), (c, idx, name)
            meta[(c, idx)] = {"cls": cls, "setting": name, "nslots": st[2], "form": st[3], "pt": pt}
            plants.append(((c, idx), pc, st))
    ctx.progress(3, 4, "settings")

    # 4. own copies (shuffles the exact decider fits at the plant's setting)
    own, tries, copy_secs = {}, {}, {}
    with mp.get_context("fork").Pool(W) as pool:
        t0 = time.time()
        for key, out, ntry in pool.imap_unordered(_copies_job, [(k, pc, st, prng.randrange(10 ** 9)) for k, pc, st in plants]):
            own[key], tries[key] = out, ntry
        copy_wall = time.time() - t0
        bad = [k for k in own if len(own[k]) < N_OWN]
        # 5. one run per text
        cj = []
        for k, pc, st in plants:
            if k in bad:
                continue
            cj.append(((k, "plant", 0), pc, st, prng.randrange(10 ** 9), witness(pc, st, random.Random(1))))
            for g, (sh, w) in enumerate(own[k]):
                cj.append(((k, "own", g), sh, st, prng.randrange(10 ** 9), w))
        res = {}
        ctx.progress(0, len(cj), "climbs")
        for key, out in pool.imap_unordered(_climb_job, cj, chunksize=1):
            res[key] = out
            ctx.progress(len(res), len(cj), "climbs")

    # 6. power and cost
    power, secs = {}, {}
    for c in CLASSES:
        for which in ("clean", "sanborn"):
            f = n = 0
            for (cc, idx), v in meta.items():
                if cc != c or (cc, idx) in bad or (v["cls"] == "clean") != (which == "clean"):
                    continue
                best = res[((c, idx), "plant", 0)][0]
                omax = max(res[((c, idx), "own", g)][0] for g in range(N_OWN))
                v["found"], v["margin"] = best > omax, round(best - omax, 4)
                v["letters_right"] = sum(a == b for a, b in zip(res[((c, idx), "plant", 0)][2], v["pt"]))
                f += best > omax; n += 1
            power[f"{c}/{which}"] = [f, n]
        power[f"{c}/pooled"] = [power[f"{c}/clean"][0] + power[f"{c}/sanborn"][0], power[f"{c}/clean"][1] + power[f"{c}/sanborn"][1]]
        ts = [v[1] for (k, kind, g), v in res.items() if k[0] == c]
        secs[c] = round(sum(ts) / max(1, len(ts)), 2)
    copy_cost = round(copy_wall * W / max(1, len(plants) * N_OWN), 3)   # core-seconds per fitting copy
    f61_short = sum(f61.values())
    a_counts = {s: _rec("0129")["summary"][s]["k4_fits_full_library_by_L"] for s in ("AV", "AB")}
    b_counts = {s: _rec("0130")["summary"][s]["k4_fits_full_library_by_L"] for s in ("BV", "BB")}
    f61_long = sum(sum(v[10:26]) for v in list(a_counts.values()) + list(b_counts.values()))
    counts = {"F1.4 skip": len(k4fit["F1.4 skip"]), "F1.4 other": len(k4fit["F1.4 other"]),
              "F6.1 6-10": f61_short, "F6.1 11-26": f61_long}
    per_setting = {c: round(secs[c] * (1 + SEQ_COPIES) + copy_cost * 12, 1) for c in CLASSES}
    cost = {}
    for cell, c in (("F1.4 skip", "F1.4 skip"), ("F1.4 other", "F1.4 other"), ("F6.1 6-10", "F6.1 8-10"), ("F6.1 11-26", "F6.1 11-26")):
        ch = counts[cell] * per_setting[c] / 3600
        cost[cell] = {"settings": counts[cell], "core_seconds_per_setting": per_setting[c], "core_hours": round(ch, 1),
                      "modal_dollars_ideal": round(ch * DOLLARS_PER_CORE_HOUR, 1),
                      "modal_dollars_at_half_efficiency": round(2 * ch * DOLLARS_PER_CORE_HOUR, 1),
                      "power_pooled": power[f"{c}/pooled"]}
    bounds = {
        "item": "D2", "decider": "D1's one-run decider: 0140's compiled tempering, one run (16 x 625 x 1000), generalised to any slot map and reading order",
        "self_check_against_0140": check,
        "f14_settings_listed": {g: len(v) for g, v in f14.items()}, "f14_k4_fitting_settings": counts["F1.4 skip"] + counts["F1.4 other"],
        "f14_k4_fitting_by_group": {g: len(v) for g, v in k4fit.items()},
        "f14_k4_fitting_partitions": {g: len({canon([s[q - 1] for q in sorted(ctx.KNOWN)]) for _, s, _, _ in v}) for g, v in k4fit.items()},
        "f61_k4_fits_6_10_recount": f61, "f61_k4_fits_11_26_from_0129_0130": f61_long,
        "f61_records_6_10": {s: v[5:10] for s, v in list(a_counts.items()) + list(b_counts.items())},
        "plants_per_class": 2 * PLANTS, "own_copies": N_OWN, "null_per_plant": "1/7", "plants_without_copies": [list(k) for k in bad],
        "power": power, "reference_one_run_0229": {"L23": {"clean": [23, 24], "sanborn": [14, 24]}, "L26": {"clean": [15, 24], "sanborn": [14, 24]}, "pooled": [66, 96]},
        "seconds_per_climb": secs, "copy_core_seconds_each": copy_cost, "copy_tries_median": sorted(tries.values())[len(tries) // 2],
        "sequential_copies_expected": round(SEQ_COPIES, 2), "cost": cost,
        "dollars_per_core_hour": round(DOLLARS_PER_CORE_HOUR, 4),
        "plants": {f"{k[0]}/{k[1]}": {kk: vv for kk, vv in v.items() if kk != "pt"} for k, v in meta.items()},
        "climbs_without_start": sum(1 for v in res.values() if v[0] <= -99), "texts_climbed": len(res), "compute_seconds": round(time.time() - t_start), "exhaustive": False,
        "expected_total_time": "about 1,350 one-run climbs at about 17 s (0229) = about 6.4 core-hours, plus the exact counts",
    }
    notes = (f"power pooled: " + ", ".join(f"{c} {power[c + '/pooled']}" for c in CLASSES) +
             "; cost: " + ", ".join(f"{k} {v['settings']} settings {v['core_hours']} core-h" for k, v in cost.items()))
    controls = [v[0] for (k, kind, g), v in res.items() if kind == "own"]
    return {"candidates": [], "bounds": bounds, "notes": notes, "controls": controls}


def _rec(e):
    import json
    return json.loads((next((ROOT / "experiments").glob(f"{e}-*")) / "result.json").read_text())["bounds"]


def encrypt(plaintext, key):
    """No candidate is submitted. key = {'slot': [...], 'mpos': [...], 'n': n, 'form': 'V'|'B', 'order': [...], 'key': [...]}."""
    st = (tuple(key["slot"]), tuple(key["mpos"]), key["n"], key["form"])
    return encipher(plaintext, st, key["order"], key["key"])


def worked_example(ctx, key):
    return "\n".join([
        "D2 measures the one-run decider on settings other than a plain repeating key.", "",
        "  setting      skip one key letter every 7 letters, 11 key letters",
        "  slot map     place 1 2 3 4 5 6 7 8 9 ...",
        "  key letter         1 2 3 4 5 6 8 9 10 ... (letter 7 skipped)", "",
        "  a hidden message under that slot map and its six scrambled copies get one tempering search each;",
        "  found when the hidden message's best English score is above all six copies'.",
        "  The time per search times the settings K4 fits gives the cost of deciding the whole cell."])
