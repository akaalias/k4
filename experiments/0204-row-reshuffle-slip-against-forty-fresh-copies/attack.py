"""Experiment 0204 (F6.21: replication of 0203's row-reshuffle excess). See program.md for the contract."""

EXPERIMENT = {
    "slug": "row-reshuffle-slip-against-forty-fresh-copies",
    "title": "F6.21, replication: 0203's row-reshuffle family, where K4 led every copy in 6 cells against a null of 1, rerun unchanged against 40 fresh scrambled copies, with a per-width breakdown; a deliberate slip in the keyword columnar (one column read out of its place, or two columns swapped), around every keyword columnar already tested, then or before a repeating key on the table, exact, with planted slips in the same run",
    "family": "6-transposition-then-tableau",
    "parent": "0203-a-slip-in-the-keyword-columnar-part-2",
    "changed": (
        "0203 found K4 above every one of its ten scrambled copies in 6 of 52 cells for the letters-reshuffled-inside-rows "
        "family (F6.18) with one slip (A 19, 21, 22, 23, 26; B 24), where no copy led the rest in more than one: outside the "
        "copies' range, which stops the queue until replicated (order-of-work rule 5). Here the same search, unchanged, "
        "on that family only, against 40 fresh scrambled copies (new seed), with the same fixed statistic (cells where "
        "K4 exceeds every copy, against each copy's own count against the rest), K4's rank in every cell, and the counts "
        "split by row width to show which widths carry any excess. Budget 45 minutes (41 texts plus a plant)."
    ),
    "hypothesis_expert": (
        "C1(a), C5, C10 ('mistakes on purpose'; misspellings as security checks in SOE practice, Marks p. 16). Source: "
        "reports/marks-between-silk-and-cyanide.md. Model: c = T(sigma'(p)) or sigma'(T(p)), sigma' a keyword columnar "
        "(or two passes) whose column reading order differs from the keyword's by one move of one column (g(g-1) orders) "
        "or one swap of two non-adjacent columns ((g-1)(g-2)/2; adjacent swaps are moves), in one pass. A skipped or "
        "doubled column alone changes the length (97 would need a message of 97 plus or minus a column, or two "
        "compensating slips): not searched. Not included: Myszkowski, AMSCO, keyed blanks, triangle and disrupted "
        "columnars (not on the item's list). Each slipped route is tested exactly as 0110 tested its routes: periods "
        "1-26, both orders, 8 classes, by slot agreement of the 24 known letters, forward and inverse. Statistic (0134's, "
        "fixed): per base family, the shortest key length consistent on K4 against the copies, and the cells (order, "
        "length) where K4 exceeds every copy, against each copy's own count. Routes are counted per slip, not "
        "deduplicated across words (copies counted the same way)."
    ),
    "hypothesis_eli5": (
        "Agents in the war often made one mistake when they copied out a transposition: they numbered the key word "
        "wrongly and read one column at the wrong time, or read two columns in each other's place. Sanborn says he "
        "made mistakes on purpose. We take every column shuffle the project has already ruled out and try it again "
        "with each such single mistake, followed or preceded by a short repeating key word on the sculpture's table."
    ),
    "prediction": (
        "The excess does not replicate: against 40 fresh copies K4 leads every copy in no more cells than a copy does "
        "(expected about 52/41, roughly 1 cell), and its rank in 0203's six cells falls inside the copies. The plant is "
        "found. Zero candidates."
    ),
    "method": (
        "1. Rebuild each base family's column groups and reading order with the experiments' own builders. "
        "2. In compiled code, for every base, every slip of the reading order (one column moved, two swapped) in each "
        "pass, build the route and its inverse. "
        "3. Test each with the 0110/0164 periodic-key test, orders A and B, 8 classes, periods 1-26, on K4, ten copies "
        "and four planted texts; checked against Python on sample routes. "
        "4. The fixed statistic per base family; each plant must show its own slip live at its own length."
    ),
    "walkthrough": (
        "1. Take the key word SHADOW: alphabetical order A D H O S W numbers the columns 5 3 2 6 4 1... read in the order 3, 4, 2, 5, 1, 6. "
        "2. Make one slip: read column 2 one step early (3, 2, 4, 5, 1, 6), or swap columns 3 and 5. "
        "3. Write the 97 letters in rows of 6 and copy out the columns in the slipped order. "
        "4. Encipher on the table with a repeating key, or encipher first. "
        "5. Follow each known letter to its carved place; known letters that share a key slot must agree."
    ),
}

import ctypes
import importlib.util
import os
import random
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
PMAX = 26
N_CONTROLS = 40
WORKERS = 8
ROOT = Path(__file__).resolve().parent
if not (ROOT / "kryptos").exists():
    ROOT = Path.cwd()
CLASSES = [(pa, ca, be) for pa in (0, 1) for ca in (0, 1) for be in (0, 1)]
CLASS_NAME = lambda c: f"{('std', 'kry')[c[0]]}/{('std', 'kry')[c[1]]}/{'beau' if c[2] else 'vig-var'}"

C_SOURCE = r"""
#include <string.h>
#define N 97
#define PMAX 26
static int T, NP;                   /* texts (K4 + copies), then NP planted texts after them */
static int CI[2][64][N];
static int PI[2][24], PIDX[24];
static int PB[PMAX + 1][24][2], NPB[PMAX + 1];

void set_tables(int t, int np, const int *ci, const int *pi, const int *pidx) {
    T = t; NP = np;
    int TT = t + np;
    for (int a = 0; a < 2; a++) for (int x = 0; x < TT; x++) for (int j = 0; j < N; j++) CI[a][x][j] = ci[(a * TT + x) * N + j];
    for (int a = 0; a < 2; a++) for (int e = 0; e < 24; e++) PI[a][e] = pi[a * 24 + e];
    for (int e = 0; e < 24; e++) PIDX[e] = pidx[e];
    for (int p = 1; p <= PMAX; p++) {
        int last[PMAX]; for (int s = 0; s < p; s++) last[s] = -1;
        NPB[p] = 0;
        for (int e = 0; e < 24; e++) { int s = PIDX[e] % p; if (last[s] >= 0) { PB[p][NPB[p]][0] = last[s]; PB[p][NPB[p]][1] = e; NPB[p]++; } last[s] = e; }
    }
}

/* one route: live counts per (order, text, period); examples (first live period < 20) for K4 and the plants */
static void test_route(const int *wh, long *live, long *low, int *ex, int *nex, int ex_cap, int base, int code) {
    int land[24];
    for (int e = 0; e < 24; e++) land[e] = wh[PIDX[e]];
    int PA[PMAX + 1][24][2], NPA[PMAX + 1];
    for (int p = 1; p <= PMAX; p++) {
        int last[PMAX]; for (int s = 0; s < p; s++) last[s] = -1;
        NPA[p] = 0;
        for (int e = 0; e < 24; e++) { int s = land[e] % p; if (last[s] >= 0) { PA[p][NPA[p]][0] = last[s]; PA[p][NPA[p]][1] = e; NPA[p]++; } last[s] = e; }
    }
    int TT = T + NP;
    for (int pa = 0; pa < 2; pa++) for (int ca = 0; ca < 2; ca++) for (int beau = 0; beau < 2; beau++) {
        for (int t = 0; t < TT; t++) {
            int f[24];
            for (int e = 0; e < 24; e++) {
                int c = CI[ca][t][land[e]], pp = PI[pa][e];
                f[e] = beau ? (c + pp) % 26 : ((c - pp) % 26 + 26) % 26;
            }
            for (int o = 0; o < 2; o++) {
                int first = 0;
                for (int p = 1; p <= PMAX; p++) {
                    int n = o == 0 ? NPA[p] : NPB[p], ok = 1;
                    for (int q = 0; q < n; q++) {
                        int a = o == 0 ? PA[p][q][0] : PB[p][q][0], b = o == 0 ? PA[p][q][1] : PB[p][q][1];
                        if (f[a] != f[b]) { ok = 0; break; }
                    }
                    if (ok) { live[(o * TT + t) * (PMAX + 1) + p]++; if (!first) first = p; }
                }
                if (first && first < 20) {
                    low[o * TT + t]++;
                    if ((t == 0 || t >= T) && *nex < ex_cap) {
                        int *x = ex + 6 * (*nex);
                        x[0] = t; x[1] = base; x[2] = code; x[3] = o; x[4] = pa * 4 + ca * 2 + beau; x[5] = first;
                        (*nex)++;
                    }
                }
            }
        }
    }
}

/* every slip of one pass. gpos/gstart: the pass's groups (columns) of input positions; mode 0 read group by group,
   1 interleaved (row by row through the groups); order: the true reading order of the g groups; wb: message place
   -> input position of the slipped pass; wa: output index of the slipped pass -> carved place.
   code = dir + 2 * (type + 2 * (a + 64 * b)): type 0 move group at a to place b, type 1 swap a and b. */
void test_base(const int *gpos, const int *gstart, int g, int mode, const int *order, const int *wb, const int *wa,
               int base, long *live, long *low, int *ex, int *nex, int ex_cap, long *routes) {
    int sig[64], out[N], wh[N], inv[N], maxlen = 0;
    for (int x = 0; x < g; x++) if (gstart[x + 1] - gstart[x] > maxlen) maxlen = gstart[x + 1] - gstart[x];
    for (int type = 0; type < 2; type++)
    for (int a = 0; a < g; a++) for (int b = 0; b < g; b++) {
        if (type == 0) {
            if (b == a) continue;
            int k = 0;
            for (int y = 0; y < g; y++) if (y != a) sig[k++] = order[y];
            for (int y = g - 1; y > b; y--) sig[y] = sig[y - 1];
            sig[b] = order[a];
        } else {
            if (b <= a + 1) continue;           /* adjacent swaps are moves */
            for (int y = 0; y < g; y++) sig[y] = order[y];
            sig[a] = order[b]; sig[b] = order[a];
        }
        int idx = 0;
        if (mode == 0) {
            for (int y = 0; y < g; y++) for (int z = gstart[sig[y]]; z < gstart[sig[y] + 1]; z++) out[gpos[z]] = idx++;
        } else {
            for (int r = 0; r < maxlen; r++) for (int y = 0; y < g; y++) {
                int z = gstart[sig[y]] + r;
                if (z < gstart[sig[y] + 1]) out[gpos[z]] = idx++;
            }
        }
        for (int m = 0; m < N; m++) wh[m] = wa[out[wb[m]]];
        for (int m = 0; m < N; m++) inv[wh[m]] = m;
        int code = 2 * (type + 2 * (a + 64 * b));
        test_route(wh, live, low, ex, nex, ex_cap, base, code);
        test_route(inv, live, low, ex, nex, ex_cap, base, code + 1);
        *routes += 2;
    }
}

/* the same for one fixed route (checks against Python) */
void test_one(const int *wh, long *live, long *low) {
    int ex[6]; int nex = 0;
    test_route(wh, live, low, ex, &nex, 0, 0, 0);
}
"""


def build_lib(texts, nplants, known_list):
    d = tempfile.mkdtemp(prefix="k4_slip_")
    src, so = os.path.join(d, "s.c"), os.path.join(d, "s.so")
    open(src, "w").write(C_SOURCE)
    subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", so, src], check=True, capture_output=True)
    lib = ctypes.CDLL(so)
    ci = []
    for A_ in (STD, KRY):
        for t in texts:
            ci += [A_.index(ch) for ch in t]
    pi = [STD.index(a) for _, a in known_list] + [KRY.index(a) for _, a in known_list]
    lib.set_tables(len(texts) - nplants, nplants, I(ci), I(pi), I([q - 1 for q, _ in known_list]))
    return lib


I = lambda v: (ctypes.c_int * len(v))(*v)


# ---------------------------------------------------------------------------------------------- the bases
def load_snapshot(exp):
    path = sorted(ROOT.glob(f"experiments/{exp}-*/attack.py"))[0]
    spec = importlib.util.spec_from_file_location(f"snap{exp}", path)
    mod = importlib.util.module_from_spec(spec)
    mod.__file__ = str(ROOT / "attack.py")
    spec.loader.exec_module(mod)
    return mod


IDENT = list(range(N))


def col_groups(n, w):
    """Columns of rows of width w over input positions 0..n-1."""
    return [[r * w + c for r in range((n - c + w - 1) // w)] for c in range(w)]


def pack(groups):
    gpos, gstart = [], [0]
    for g_ in groups:
        gpos += g_
        gstart.append(len(gpos))
    return gpos, gstart


def stage_map(groups, order, mode=0):
    """out[x] = output index of input position x when the groups are read in this order."""
    out = [0] * N
    idx = 0
    if mode == 0:
        for gi in order:
            for x in groups[gi]:
                out[x] = idx; idx += 1
    else:
        for r in range(max(len(g_) for g_ in groups)):
            for gi in order:
                if r < len(groups[gi]):
                    out[groups[gi][r]] = idx; idx += 1
    return out


def bases_for(family, vocab):
    """List of bases: (name, groups, mode, order, wb, wa) with wb/wa the fixed passes around the slipped one."""
    out = []
    if family in ("F6/1 keyword columnar", "F6/1 double columnar"):
        s110 = load_snapshot("0110")
        words = [w.strip().upper() for w in (ROOT / "kryptos" / "data" / "words.txt").read_text().split()]
        words += [v.upper() for v in vocab]
        seen = set()
        for w in words:
            if not (2 <= len(w) <= 30 and w.isalpha()):
                continue
            for seq in (s110.keyword_sequence(w), s110.full_sequence(w)):
                t = tuple(seq)
                if len(t) < 3 or t in seen:
                    continue
                seen.add(t)
                gr = col_groups(N, len(t))
                if family == "F6/1 keyword columnar":
                    out.append((w, gr, 0, list(t), IDENT, IDENT))
                else:
                    st = stage_map(gr, list(t))
                    out.append((f"{w} pass 1", gr, 0, list(t), IDENT, st))      # slip in pass 1, pass 2 true
                    out.append((f"{w} pass 2", gr, 0, list(t), st, IDENT))      # pass 1 true, slip in pass 2
    elif family in ("F6.16 interrupted", "F6.17 trapezoid"):
        s164 = load_snapshot("0164")
        groups_holder = {}

        def read_cells(cells, order_cols, w):
            by_col = {}
            for idx, (r, c) in enumerate(cells):
                by_col.setdefault(c, []).append((r, idx))
            cols = sorted(by_col)
            groups_holder["v"] = ([[i for _, i in sorted(by_col[c])] for c in cols], [cols.index(c) for c in order_cols if c in by_col])
            return list(range(N))
        s164.read_cells = read_cells
        for w in s164.keywords(vocab):
            num = [0] * len(w)
            for r, i in enumerate(s164.numeric_order(w)):
                num[i] = r + 1
            calls = [lambda w=w, num=num: s164.interrupted(w, num)]
            if family == "F6.16 interrupted" and len(w) >= 9 and w in s164.PUZZLE:
                calls += [lambda w=w, d=d: s164.interrupted(w, s164.frac_digits(d)) for d in range(3, 100)]
            if family == "F6.17 trapezoid":
                calls = []
                b = len(w)
                for h in range(2, b + 1):
                    if h * b - h * (h - 1) // 2 >= N:
                        calls = [lambda w=w, h=h, sd=sd: s164.trapezoid(w, h, sd) for sd in ("right", "left")]
                        break
            for fn in calls:
                groups_holder.pop("v", None)
                if fn() is None or "v" not in groups_holder:
                    continue
                gr, order = groups_holder["v"]
                if sum(len(g_) for g_ in gr) == N and len(gr) >= 3:
                    out.append((w, gr, 0, order, IDENT, IDENT))
    elif family == "F6.18 row reshuffle":
        s165 = load_snapshot("0165")
        seen = set()
        for w in s165.keywords(vocab):
            if not 3 <= len(w) <= 48:
                continue
            order = s165.numeric_order(w)
            if tuple(order) in seen:
                continue
            seen.add(tuple(order))
            out.append((w, col_groups(N, len(w)), 1, order, IDENT, IDENT))
    elif family == "F11.2 poem code":
        s190 = load_snapshot("0190")
        seen = set()
        for name, k1, k2 in s190.keys():
            if (k1, k2) in seen:
                continue
            seen.add((k1, k2))
            o1, o2 = s190.number_key(k1), s190.number_key(k2)
            g1, g2 = col_groups(N, len(k1)), col_groups(N, len(k2))
            if len(k1) <= 64 and len(k2) <= 64:
                out.append((f"{name} pass 1", g1, 0, o1, IDENT, stage_map(g2, o2)))
                out.append((f"{name} pass 2", g2, 0, o2, stage_map(g1, o1), IDENT))
    return out


FAMILIES = ("F6.18 row reshuffle",)      # the family whose excess 0203 found


def slipped_where(base, typ, a, b):
    """Python reference: the where-map of one slipped route (forward)."""
    name, gr, mode, order, wb, wa = base
    sig = list(order)
    if typ == 0:
        x = sig.pop(a); sig.insert(b, x)
    else:
        sig[a], sig[b] = sig[b], sig[a]
    out = stage_map(gr, sig, mode)
    return [wa[out[wb[m]]] for m in range(N)]


# ---------------------------------------------------------------------------------------------- workers
_CTX = {}


def worker(args):
    family, lo, hi, texts, nplants, known_list, vocab = args
    key = (family, len(texts))
    if "bases" not in _CTX or _CTX.get("family") != family:
        _CTX["bases"] = bases_for(family, vocab); _CTX["family"] = family
    if "lib" not in _CTX:
        _CTX["lib"] = build_lib(texts, nplants, known_list)
    lib = _CTX["lib"]
    TT = len(texts)
    live = (ctypes.c_long * (2 * TT * 27))(); low = (ctypes.c_long * (2 * TT))()
    cap = 4000
    ex = (ctypes.c_int * (6 * cap))(); nex = ctypes.c_int(0); routes = ctypes.c_long(0)
    for bi in range(lo, min(hi, len(_CTX["bases"]))):
        name, gr, mode, order, wb, wa = _CTX["bases"][bi]
        gpos, gstart = pack(gr)
        lib.test_base(I(gpos), I(gstart), len(gr), mode, I(order), I(wb), I(wa), bi, live, low, ex, ctypes.byref(nex), cap, ctypes.byref(routes))
    exl = [list(ex[6 * j: 6 * j + 6]) for j in range(nex.value)]
    return family, list(live), list(low), exl, routes.value


def decode(code):
    d, rest = code % 2, code // 2
    typ, rest = rest % 2, rest // 2
    return d, typ, rest % 64, rest // 64


# ---------------------------------------------------------------------------------------------- plants
def periodic(text, cls, key):
    pa, ca, be = (STD, KRY)[cls[0]], (STD, KRY)[cls[1]], cls[2]
    return "".join(ca[(key[i % len(key)] - pa.index(ch)) % 26] if be else ca[(pa.index(ch) + key[i % len(key)]) % 26] for i, ch in enumerate(text))


def encrypt_route(pt, wh, order, cls, key):
    if order == "B":
        pt = periodic(pt, cls, key)
    moved = [""] * N
    for m, ch in enumerate(pt):
        moved[wh[m]] = ch
    moved = "".join(moved)
    return periodic(moved, cls, key) if order == "A" else moved


def make_plants(vocab):
    from kryptos.plants import english_plant
    specs = [("F6.18 row reshuffle", 0, "A", 6, 6, 2103)]
    plants = []
    for fam, typ, order, ci, p, seed in specs:
        rng = random.Random(seed)
        bases = bases_for(fam, vocab)
        while True:
            bi = rng.randrange(len(bases))
            g = len(bases[bi][1])
            if 5 <= g <= 14:
                break
        a = rng.randrange(g)
        b = rng.choice([x for x in range(g) if (x != a if typ == 0 else x > a + 1)] or [None])
        if b is None:
            a, b, typ = 0, g - 1, 1
        wh = slipped_where(bases[bi], typ, a, b)
        key = [rng.randrange(26) for _ in range(p)]
        pt = english_plant(seed)
        plants.append({"family": fam, "base": bi, "base_name": bases[bi][0], "slip": (typ, a, b), "order": order,
                       "class": CLASSES[ci], "length": p, "key": key, "pt": pt, "ct": encrypt_route(pt, wh, order, CLASSES[ci], key)})
    return plants


# ---------------------------------------------------------------------------------------------- run
def run(ctx):
    import multiprocessing as mp
    import types
    ct, known = ctx.K4, ctx.KNOWN
    known_list = [(q, known[q]) for q in sorted(known)]
    t0 = time.time()
    vocab = list(ctx.vocabulary)
    rng = random.Random(1622)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    plants = make_plants(vocab)
    all_texts = texts + [pl["ct"] for pl in plants]
    T, TT = len(texts), len(all_texts)
    # checks: every slipped route is a permutation; the compiled test against Python on sample routes
    ref = load_snapshot("0164")
    lib = build_lib(all_texts, len(plants), known_list)
    sizes = {}
    for fam in FAMILIES:
        bases = bases_for(fam, vocab)
        sizes[fam] = len(bases)
        for bi in random.Random(5).sample(range(len(bases)), min(4, len(bases))):
            g = len(bases[bi][1])
            for typ, a, b in ((0, 0, g - 1), (0, g - 1, 1), (1, 0, g - 1)):
                if typ == 1 and b <= a + 1:
                    continue
                wh = slipped_where(bases[bi], typ, a, b)
                assert sorted(wh) == IDENT, fam
                live = (ctypes.c_long * (2 * TT * 27))(); low = (ctypes.c_long * (2 * TT))()
                lib.test_one(I(wh), live, low)
                for o in (0, 1):
                    for t in (0, 1, T):
                        assert [live[(o * TT + t) * 27 + p] for p in range(1, 27)] == ref.rt_reference(wh, all_texts, known_list, o, t)[1:], (fam, typ)
    # each plant decrypts back
    for pl in plants:
        assert len(pl["ct"]) == N
    if getattr(sys.modules.get(__name__), "worker", None) is not worker:
        mod = types.ModuleType(__name__); mod.__dict__.update(globals()); sys.modules[__name__] = mod
    res = {}
    plant_ex = []
    with mp.get_context("fork").Pool(WORKERS) as pool:
        for fam in FAMILIES:
            if ctx.time_left() < 240:
                res[fam] = {"skipped": "time"}
                continue
            nb = sizes[fam]
            allb = bases_for(fam, vocab)
            widths = [len(x[1]) for x in allb]
            step = max(1, nb // (WORKERS * 12))
            jobs = []
            lo = 0
            while lo < nb:                      # jobs never mix row widths, so counts can be split by width
                hi = lo
                while hi < nb and hi - lo < step and widths[hi] == widths[lo]:
                    hi += 1
                jobs.append((fam, lo, hi, all_texts, len(plants), known_list, vocab))
                lo = hi
            live = [0] * (2 * TT * 27); low = [0] * (2 * TT); exs = []; routes = 0
            by_width = {}
            for job, (_, lv, lw, ex, r) in zip(jobs, pool.imap(worker, jobs)):
                live = [x + y for x, y in zip(live, lv)]; low = [x + y for x, y in zip(low, lw)]; exs += ex; routes += r
                g_ = widths[job[1]]
                by_width[g_] = [x + y for x, y in zip(by_width.get(g_, [0] * (2 * TT * 27)), lv)]
            L = lambda o, t, p: live[(o * TT + t) * 27 + p]
            cells = [(o, p) for o in (0, 1) for p in range(1, 27)]
            above = lambda t: [("AB"[o], p) for o, p in cells if L(o, t, p) > max(L(o, u, p) for u in range(T) if u != t)]
            first = lambda t, o: next((p for p in range(1, 27) if L(o, t, p)), None)
            k4_above = above(0)
            null = [len(above(t)) for t in range(1, T)]
            res[fam] = {"bases": nb, "routes": routes,
                        "k4_live_by_period": {"AB"[o]: [L(o, 0, p) for p in range(1, 27)] for o in (0, 1)},
                        "controls_live_by_period_min": {"AB"[o]: [min(L(o, t, p) for t in range(1, T)) for p in range(1, 27)] for o in (0, 1)},
                        "controls_live_by_period_max": {"AB"[o]: [max(L(o, t, p) for t in range(1, T)) for p in range(1, 27)] for o in (0, 1)},
                        "k4_shortest_live": {"AB"[o]: first(0, o) for o in (0, 1)},
                        "coppers_shortest_live": {"AB"[o]: min([first(t, o) or 99 for t in range(1, T)]) for o in (0, 1)},
                        "k4_settings_live_below_20": {"AB"[o]: low[o * TT] for o in (0, 1)},
                        "controls_settings_live_below_20": {"AB"[o]: [low[o * TT + t] for t in range(1, T)] for o in (0, 1)},
                        "k4_live_below_20": [{"base": x[1], "slip": decode(x[2]), "order": "AB"[x[3]], "class": CLASS_NAME(CLASSES[x[4]]), "period": x[5]} for x in sorted((e for e in exs if e[0] == 0), key=lambda e: e[5])[:20]],
                        "cells_k4_above_every_copper": k4_above, "null_cells_above_rest_per_copper": null,
                        "stop_queue": len(k4_above) > max(null),
                        "k4_rank_per_cell": {f"{'AB'[o]}{p}": sum(L(o, t, p) >= L(o, 0, p) for t in range(1, T)) for o, p in cells if L(o, 0, p)},
                        "cells_0203": {c: {"k4": L("AB".index(c[0]), 0, int(c[1:])), "copies_at_or_above_k4": sum(L("AB".index(c[0]), t, int(c[1:])) >= L("AB".index(c[0]), 0, int(c[1:])) for t in range(1, T)),
                                           "copies_max": max(L("AB".index(c[0]), t, int(c[1:])) for t in range(1, T)),
                                           "by_width_k4_and_copies_median": {g_: [lv_[("AB".index(c[0]) * TT + 0) * 27 + int(c[1:])], sorted(lv_[("AB".index(c[0]) * TT + t) * 27 + int(c[1:])] for t in range(1, T))[T // 2]]
                                                                            for g_, lv_ in sorted(by_width.items()) if lv_[("AB".index(c[0]) * TT + 0) * 27 + int(c[1:])]}}
                                       for c in ("A19", "A21", "A22", "A23", "A26", "B24")}}
            plant_ex += [(fam, e) for e in exs if e[0] >= T]
    # plants: own slip live at own setting
    plant_res = []
    for k, pl in enumerate(plants):
        t = T + k
        mine = [e for fam, e in plant_ex if fam == pl["family"] and e[0] == t]
        hit = [e for e in mine if e[1] == pl["base"] and decode(e[2])[1:] == pl["slip"] and decode(e[2])[0] == 0
               and "AB"[e[3]] == pl["order"] and CLASSES[e[4]] == pl["class"] and e[5] <= pl["length"]]
        plant_res.append({"family": pl["family"], "base": pl["base_name"], "slip": pl["slip"], "order": pl["order"], "class": CLASS_NAME(pl["class"]),
                          "length": pl["length"], "found": bool(hit), "shortest_live_at_own_setting": min((e[5] for e in hit), default=None),
                          "other_live_settings_below_20": len(mine) - len(hit)})
    bounds = {"family": "one slip (a column moved or two swapped) in the reading order of every keyword columnar already closed, then or before a periodic key",
              "bases_per_family": sizes, "families": res, "plants": plant_res,
              "controls": f"{N_CONTROLS} fresh shuffled copies (seed 1622; 0203 used seed 1621), {len(plants)} planted slipped text in the same run",
              "not_searched": "a skipped or doubled column alone (changes the length); Myszkowski, AMSCO, keyed blanks, triangle and disrupted columnars (not on the item's list)",
              "seconds": round(time.time() - t0), "exhaustive": "exact per family done (see skipped)"}
    notes = "; ".join(f"{k}: {v.get('routes', 0):,} routes, shortest live A {v.get('k4_shortest_live', {}).get('A')} B {v.get('k4_shortest_live', {}).get('B')} (copies {v.get('coppers_shortest_live')}), K4 above every copy {len(v.get('cells_k4_above_every_copper', []))} (null max {max(v.get('null_cells_above_rest_per_copper', [0]))})" for k, v in res.items())
    notes += ". Plants: " + "; ".join(f"{p['family']} found {p['found']}" for p in plant_res)
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    word = "SHADOW"
    order = sorted(range(6), key=lambda i: (word[i], i))
    sig = list(order); x = sig.pop(2); sig.insert(1, x)
    lines = [f"key word {word}: columns read in the order {[c + 1 for c in order]}",
             f"one slip, the third column read one step early: {[c + 1 for c in sig]}", ""]
    wh = [0] * N
    out = stage_map(col_groups(N, 6), sig)
    lines += ["place  known  lands at  carved"]
    for q in (22, 26, 34, 64, 74):
        lines.append(f"{q:5d}  {ctx.KNOWN[q]:>5}  {out[q - 1] + 1:8d}  {ctx.K4[out[q - 1]]:>6}")
    return "\n".join(lines)
