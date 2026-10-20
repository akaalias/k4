"""Experiment 0199 (F6.20). See program.md for the contract."""

EXPERIMENT = {
    "slug": "turning-grille-with-the-table",
    "title": "F6.20, part 1: a 10x10 turning grille (Fleissner) copied out by rows, before or after a repeating key on the table; free keys of 1-6 letters and every key word of 7 or more, every card, exact, with planted grilles in the same run",
    "family": "6-transposition-then-tableau",
    "parent": "0164-disrupted-triangle-interrupted-trapezoid",
    "changed": (
        "F6.20 (issue #78), a move never tested: the turning grille. A 10x10 card with one hole in each of its 25 "
        "rotation orbits (4^25, about 10^15 cards); the message is written through the holes row by row, the card "
        "turned a quarter, four times; 97 letters leave three cells empty, skipped when the grid is copied out row by "
        "row (Fleissner's read-off). Four procedures: turned clockwise or anticlockwise, the empty cells at the end of "
        "the writing or at its start (writing and reading by columns is the transpose, the same set of moves). Then a "
        "repeating key on the standard or KRYPTOS table after the grille (A) or before it (B). Two arms, both exact "
        "over every card: any key of 1-6 letters (8 table classes), and every dictionary or puzzle word of 7 letters "
        "or more as the key (24 conventions). A depth-first search walks the top half of the grid, fixing a cell's "
        "turn and its 180-degree partner's at once and checking each known letter as it lands. Copied out by columns "
        "is a different set of moves and far costlier; it follows as part 2. The F7 standing step rides along."
    ),
    "hypothesis_expert": (
        "C1(a) (a matrix stage, then the table), C3 (Sanborn's 'spatial systems... pattern, light and shadow': a "
        "grille is a card held to the light), C5 (a hand system keyed by 'key word/s'). Source: "
        "reports/agent-memorized-hand-ciphers.md (Fleissner 1881; German army 1916; Abwehr and RS44 stencils, Lewis, "
        "German Agent Systems). Model: c = T(sigma(p)) (order A) or sigma(T(p)) (order B), sigma the grille's "
        "permutation, T a periodic tableau key. Search: the top half of the grid in row order; a cell's rank in its "
        "turn is the count of earlier top cells of that turn, its 180-degree partner (turn + 2) has rank 24 minus that "
        "count, so both message places are known at once. Free key: each slot's value is set by its first known letter "
        "and checked by the rest; key words: every letter is a check (24 checks against about 50 bits of card). Count: "
        "distinct landing maps (the carved squares of the 24 known letters), since cards that differ only where unknown "
        "letters go are one reading of the known ones. Statistic fixed before the run: free key, per procedure and "
        "order, the shortest length with a landing map that fits and the cells (order, length) where K4's count "
        "exceeds every copy's; key words, the number of (word, convention, order, procedure) settings with a map, "
        "K4 against each copy. Measured cost: a free key of 7 letters takes 10^8-10^9 nodes per setting, 12 letters "
        "over 2 x 10^9: lengths 7-26 with a free key are blocked by cost. Not tested: stencils with arbitrary holes, "
        "the Abwehr's 13x19 card (no remembered rule for its holes in the source)."
    ),
    "hypothesis_eli5": (
        "A turning grille is a square card with holes in it. Lay it on a 10 by 10 grid and write the message "
        "through the holes; turn the card a quarter and write on; after four turns every square holds a letter (here "
        "three stay empty, since the message has 97). Copy the grid out row by row and the letters are scrambled. "
        "We ask whether such a card, with a repeating secret word on the sculpture's table, could have made K4. There "
        "are a thousand million million cards, too many to try one by one, but the known words rule most of them out "
        "a few squares in, so a careful search can check every card."
    ),
    "prediction": (
        "No card fits K4 with any key of 1-6 letters or any key word, in either order and any procedure; the "
        "scrambled copies the same. Each planted grille is found, on its own landing map. The grille plus a key makes "
        "the two fingerprints together at the random-letter rate (zero in 2,000). Zero candidates."
    ),
    "method": (
        "1. Orbits: the 25 cells of the top-left quarter; a card is one turn (0-3) per orbit. "
        "2. Walk the top half in row order; at a cell whose orbit is new, branch over its four turns; place the message "
        "letter there (turn, rank) and at the 180-degree partner (turn + 2, rank 24 minus). "
        "3. Mark the three empty cells (last three of turn 3, or first three of turn 0); a carved place is the row "
        "position less the empty cells before it. "
        "4. Each known letter landed: key slot = carved place (A) or message place (B) mod the length; free key: set or "
        "check the slot; key word: compare with the word's letter. Prune on a clash; stop a branch once all 24 landed. "
        "5. Every procedure, order, class and length 1-6, then every key word on 24 conventions, on K4, ten copies and "
        "four plants; compiled, checked against a literal Python builder on 25,600 cards and 32 plants."
    ),
    "walkthrough": (
        "1. Cut 25 holes in a 10 by 10 card so that turning it four times uncovers every square once. "
        "2. Lay it on the grid and write the first 25 letters through the holes, row by row. "
        "3. Turn the card a quarter clockwise and write the next 25; and twice more. The last three holes stay empty. "
        "4. Copy the grid out row by row, skipping the empty squares: 97 letters. "
        "5. Encipher those 97 on the table with a repeating key word (or encipher first, then use the card). "
        "6. To test a card against K4: follow each known letter to its square, read the carved letter there, and see "
        "whether the key letters it demands repeat with the key's length or spell the key word."
    ),
}

import ctypes
import os
import random
import subprocess
import tempfile
import time
from collections import Counter
from pathlib import Path
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
N_CONTROLS = 10
WORKERS = 8
COUNT_CAP = 1000
NODE_CAP = 400_000_000
PMAX = 6            # free keys decided exactly up to this length; 7-26 cost 10^8-10^10 nodes per setting
KEY_MIN = 7         # key words shorter than PMAX + 1 are inside the free-key arm already
ROOT = Path(__file__).resolve().parent
if not (ROOT / "kryptos").exists():
    ROOT = Path.cwd()
# procedures: (turn sense: 1 clockwise, 3 anticlockwise), (copy-out: 0 rows, 1 columns), (empty cells: 0 end, 1 start)
COPY_OUT = (0,)      # 0199: copied out by rows (the standard read-off); by columns is 0200
PROCS = [(rot, rd, bl) for rot in (1, 3) for rd in COPY_OUT for bl in (0, 1)]
PROC_NAME = lambda pr: f"{'cw' if pr[0] == 1 else 'ccw'}, out by {'rows' if pr[1] == 0 else 'columns'}, empty cells at the {'end' if pr[2] == 0 else 'start'}"
CLASSES = [(pa, ca, be) for pa in (0, 1) for ca in (0, 1) for be in (0, 1)]
CLASS_NAME = lambda c: f"{('std', 'kry')[c[0]]}/{('std', 'kry')[c[1]]}/{'beau' if c[2] else 'vig-var'}"
# key-word arm: plain, cipher and key alphabets, and the form (0 Vigenere c = p + k, 1 Beaufort c = k - p, 2 variant c = p - k)
CONVS = [(pa, ca, ka, be) for pa in (0, 1) for ca in (0, 1) for ka in (0, 1) for be in (0, 1, 2)]
CONV_NAME = lambda c: f"{('std', 'kry')[c[0]]}/{('std', 'kry')[c[1]]}/{('std', 'kry')[c[2]]}/{('vig', 'beau', 'var')[c[3]]}"


# ---------------------------------------------------------------------------------------------- the grille in Python
def orbit_of(r, c):
    """(orbit index, turn offset for clockwise) of cell (r, c): orbit = the top-left-quarter cell it comes from."""
    for s in range(4):
        if r <= 4 and c <= 4:
            return 5 * r + c, s
        r, c = 9 - c, r          # rotate anticlockwise: undo one clockwise step
    raise AssertionError


def grille_perm(u, proc):
    """u: 25 turn numbers (the turn on which each orbit's top-left cell is written). Returns where[m] = carved place
    of message place m (0-96), built literally: turn the card, fill holes in row order, copy out, skip empty cells."""
    rot, rd, bl = proc
    turn = {}
    for r in range(10):
        for c in range(10):
            o, s = orbit_of(r, c)
            off = s if rot == 1 else (4 - s) % 4
            turn[(r, c)] = (u[o] + off) % 4
    seq = []                                     # message slots in writing order
    for t in range(4):
        seq += [(r, c) for r in range(10) for c in range(10) if turn[(r, c)] == t]
    assert len(seq) == 100
    filled = {}
    msg = list(range(N)) + [None] * 3 if bl == 0 else [None] * 3 + list(range(N))
    for cell, m in zip(seq, msg):
        filled[cell] = m
    order = [(r, c) for r in range(10) for c in range(10)] if rd == 0 else [(r, c) for c in range(10) for r in range(10)]
    out = [filled[x] for x in order if filled[x] is not None]
    where = [0] * N
    for j, m in enumerate(out):
        where[m] = j
    return where


def _sub(text, pa, ca, be, key):
    out = []
    for i, ch in enumerate(text):
        k, P = key[i % len(key)], pa.index(ch)
        out.append(ca[(P + k) % 26] if be == 0 else ca[(k - P) % 26] if be == 1 else ca[(P - k) % 26])
    return "".join(out)


def _unsub(text, pa, ca, be, key):
    out = []
    for i, ch in enumerate(text):
        k, C = key[i % len(key)], ca.index(ch)
        out.append(pa[(C - k) % 26] if be == 0 else pa[(k - C) % 26] if be == 1 else pa[(C + k) % 26])
    return "".join(out)


def encrypt_with(plaintext, u, proc, order, cls, key):
    """Forward. cls = (plain alphabet, cipher alphabet, form) with form 0 Vigenere, 1 Beaufort, 2 variant; key = numbers.
    Order A: grille, then the key at carved places; order B: the key at message places, then the grille."""
    pa, ca, be = (STD, KRY)[cls[0]], (STD, KRY)[cls[1]], cls[2]
    wh = grille_perm(u, proc)
    src = plaintext if order == "A" else _sub(plaintext, pa, ca, be, key)
    moved = [""] * N
    for m, ch in enumerate(src):
        moved[wh[m]] = ch
    moved = "".join(moved)
    return _sub(moved, pa, ca, be, key) if order == "A" else moved


def decrypt_with(ct, u, proc, order, cls, key):
    pa, ca, be = (STD, KRY)[cls[0]], (STD, KRY)[cls[1]], cls[2]
    wh = grille_perm(u, proc)
    if order == "A":
        s_ = _unsub(ct, pa, ca, be, key)
        return "".join(s_[wh[m]] for m in range(N))
    return _unsub("".join(ct[wh[m]] for m in range(N)), pa, ca, be, key)


def consistent_py(text, known_list, u, proc, order, cls, p, key=None):
    """Reference test of one card: do the forced key values repeat with length p (or equal the given key)?"""
    pa, ca, be = (STD, KRY)[cls[0]], (STD, KRY)[cls[1]], cls[2]
    wh = grille_perm(u, proc)
    slot = {} if key is None else dict(enumerate(key))
    for q, a in known_list:
        m = q - 1
        j = wh[m]
        C, P = ca.index(text[j]), pa.index(a)
        f = (C - P) % 26 if be == 0 else (C + P) % 26 if be == 1 else (P - C) % 26
        s_ = (j if order == "A" else m) % p
        if slot.setdefault(s_, f) != f:
            return False
    return True


# ---------------------------------------------------------------------------------------------- the compiled search
C_SOURCE = r"""
#include <string.h>
#define N 97
static int TXT[2][N];            /* carved letter index under std (0) / kry (1) */
static int KP[24], KA[2][24];    /* known message places (0-based), known letter index std/kry */
static int ISK[100];             /* message place -> known index or -1 */
static int ORB[50], OFF[50];     /* top-half cell -> orbit, turn offset (clockwise) */
static int RP[100];              /* cell -> copy-out position */
static int ROT, RD, BL, ORD, PA, CA, BE, P;   /* BE: 0 vig (f = C - P), 1 beau (C + P), 2 variant (P - C) */
static int KEYED, KEYV[32];
static int u[25], dec[25];
static int cnt[4];
static int slotv[32];
static long nodes, count, node_cap, count_cap;
static int blank_rp[3], nb;
static int pend_rp[48], pend_m[48], npend, pdone;
static int found[64][25], nfound;
static int aborted;
static int FIX, fixu[25];
static int nland;           /* known letters landed on this path */
static int landj[24];       /* carved place of each known letter on this path */
static int found_land[64][24];
#define HS 8192
static unsigned long long hset[HS];
static int use_hash;

void setup(const int *txt_std, const int *txt_kry, const int *kp, const int *ka_std, const int *ka_kry,
           const int *orb, const int *off) {
    for (int j = 0; j < N; j++) { TXT[0][j] = txt_std[j]; TXT[1][j] = txt_kry[j]; }
    for (int m = 0; m < 100; m++) ISK[m] = -1;
    for (int e = 0; e < 24; e++) { KP[e] = kp[e]; KA[0][e] = ka_std[e]; KA[1][e] = ka_kry[e]; ISK[kp[e]] = e; }
    for (int i = 0; i < 50; i++) { ORB[i] = orb[i]; OFF[i] = off[i]; }
}

static int carved(int rp) {           /* copy-out position less the empty cells before it; needs nb == 3 */
    int b = 0;
    for (int x = 0; x < 3; x++) if (blank_rp[x] < rp) b++;
    return rp - b;
}

static int located_before(int rp) {
    int b = 0;
    for (int y = 0; y < nb; y++) if (blank_rp[y] < rp) b++;
    return b;
}

/* check one landing; returns 0 on clash; logs set slots in *log */
static int land(int j, int m, int *log, int *nlog) {
    int e = ISK[m];
    int C = TXT[CA][j], Pl = KA[PA][e];
    int f = BE == 1 ? (C + Pl) % 26 : BE == 2 ? (Pl - C + 26) % 26 : (C - Pl + 26) % 26;
    int s = (ORD == 0 ? j : m) % P;
    if (KEYED) return KEYV[s] == f;
    if (slotv[s] < 0) { slotv[s] = f; log[(*nlog)++] = s; return 1; }
    return slotv[s] == f;
}

static void dfs(int i);

/* land the cell's known letters one by one. Column copy-out before the three empty cells are all placed: guess
   B, the number of empty cells before the landing (between those placed and those that could still come), land it
   at rp - B, and keep (rp, B) to verify as the empty cells appear. Each card keeps exactly one surviving guess. */
static void land_rec(int i, const int *lrp, const int *lm, const int *lx, int n, int idx) {
    if (aborted) return;
    if (idx == n) { dfs(i + 1); return; }
    int rp = lrp[idx], m = lm[idx];
    int lo, hi;
    if (RD == 0) {
        /* row copy-out: every cell before a top cell, and after a bottom cell, is known */
        int j;
        if (lx[idx] == 0) j = rp - located_before(rp);
        else { int a = 0; for (int y = 0; y < nb; y++) if (blank_rp[y] > rp) a++; j = rp - (3 - a); }
        lo = hi = rp - j;
    } else if (nb == 3) { lo = hi = located_before(rp); }
    else { lo = located_before(rp); hi = lo + 3 - nb; }
    for (int B = lo; B <= hi; B++) {
        int j = rp - B;
        if (j < 0 || j >= N) continue;
        int log[2], nlog = 0;
        if (land(j, m, log, &nlog)) {
            int pushed = 0;
            if (RD == 1 && nb < 3) { pend_rp[npend] = rp; pend_m[npend] = B; npend++; pushed = 1; }
            nland++;
            landj[ISK[m]] = j;
            land_rec(i, lrp, lm, lx, n, idx + 1);
            nland--;
            if (pushed) npend--;
        }
        for (int x = 0; x < nlog; x++) slotv[log[x]] = -1;
        if (aborted) return;
    }
}

static void dfs(int i) {
    if (aborted) return;
    if (++nodes > node_cap) { aborted = 1; return; }
    /* all 24 known letters placed (and every guess about the empty cells settled): the orbits still open cannot
       move them, so this is one placement; count it once, open orbits written as -1 */
    if (i == 50 || (nland == 24 && (RD == 0 || nb == 3))) {
        if (nb != 3 && i == 50) return;     /* cannot happen: every card leaves exactly three empty cells */
        /* count distinct landing maps (where the 24 known letters sit), not card prefixes */
        if (use_hash) {
            unsigned long long h = 1469598103934665603ULL;
            for (int e = 0; e < 24; e++) { h ^= (unsigned long long)(landj[e] + 1); h *= 1099511628211ULL; }
            if (!h) h = 1;
            unsigned int b = (unsigned int)(h % HS);
            while (hset[b] && hset[b] != h) b = (b + 1) % HS;
            if (hset[b] == h) return;
            hset[b] = h;
        }
        if (nfound < 64) { for (int x = 0; x < 25; x++) found[nfound][x] = dec[x] ? u[x] : -1;
                           memcpy(found_land[nfound], landj, sizeof landj); nfound++; }
        if (++count >= count_cap) aborted = 1;
        return;
    }
    int o = ORB[i];
    int lo = 0, hi = 3;
    if (dec[o]) { lo = hi = u[o]; }
    else if (FIX) { lo = hi = fixu[o]; }
    for (int v = lo; v <= hi; v++) {
        int newdec = !dec[o];
        if (newdec) { dec[o] = 1; u[o] = v; }
        int off = ROT == 1 ? OFF[i] : (4 - OFF[i]) % 4;
        int T = (u[o] + off) % 4, k = cnt[T];
        cnt[T]++;
        int T2 = (T + 2) % 4, k2 = 24 - k;
        int top = i, bot = 99 - i;
        int mt = 25 * T + k - (BL ? 3 : 0), mb = 25 * T2 + k2 - (BL ? 3 : 0);
        int bt = BL ? (T == 0 && k <= 2) : (T == 3 && k >= 22);
        int bb = BL ? (T2 == 0 && k2 <= 2) : (T2 == 3 && k2 >= 22);
        int nb0 = nb, np0 = npend, pd0 = pdone;
        if (bt) blank_rp[nb++] = RP[top];
        if (bb) blank_rp[nb++] = RP[bot];
        int ok = 1;
        /* new empty cells placed: every guess so far must still be possible, and exact once all three are placed */
        if (RD == 1 && nb > nb0) {
            for (int x = pdone; x < npend && ok; x++) {
                int lb = located_before(pend_rp[x]);
                if (pend_m[x] < lb || pend_m[x] > lb + 3 - nb) ok = 0;
            }
            if (ok && nb == 3) pdone = npend;
        }
        if (ok) {
            int lrp[2], lm[2], lx[2], n = 0;
            int cells[2] = {top, bot}, ms[2] = {mt, mb}, bl[2] = {bt, bb};
            for (int x = 0; x < 2; x++) {
                if (bl[x] || ms[x] < 0 || ms[x] >= N || ISK[ms[x]] < 0) continue;
                lrp[n] = RP[cells[x]]; lm[n] = ms[x]; lx[n] = x; n++;
            }
            land_rec(i, lrp, lm, lx, n, 0);
        }
        npend = np0; pdone = pd0; nb = nb0;
        cnt[T]--;
        if (newdec) dec[o] = 0;
        if (aborted) return;
    }
}

/* count cards for one configuration; returns count, sets *complete (1 if not aborted by the node cap) */
long run_cfg(int t_idx_unused, int rot, int rd, int bl, int ord, int pa, int ca, int be, int p,
             const int *rp, long ncap, long ccap, int *complete, long *nodes_out, int *found_out, int *nfound_out, int *land_out) {
    ROT = rot; RD = rd; BL = bl; ORD = ord; PA = pa; CA = ca; BE = be; P = p; FIX = 0; KEYED = 0;
    for (int c = 0; c < 100; c++) RP[c] = rp[c];
    memset(dec, 0, sizeof dec); memset(u, 0, sizeof u); memset(cnt, 0, sizeof cnt);
    for (int s = 0; s < 32; s++) slotv[s] = -1;
    nodes = 0; count = 0; node_cap = ncap; count_cap = ccap; nb = 0; npend = 0; pdone = 0; nfound = 0; aborted = 0; nland = 0; use_hash = 0;
    use_hash = 1; memset(hset, 0, sizeof hset);
    dfs(0);
    use_hash = 0;
    memcpy(land_out, found_land, sizeof found_land);
    *complete = !(aborted && count < ccap);
    *nodes_out = nodes;
    *nfound_out = nfound;
    memcpy(found_out, found, sizeof found);
    return count;
}

/* the same walk for one fixed card: 1 if it fits */
int check_card(int rot, int rd, int bl, int ord, int pa, int ca, int be, int p, const int *rp, const int *card) {
    ROT = rot; RD = rd; BL = bl; ORD = ord; PA = pa; CA = ca; BE = be; P = p; KEYED = 0;
    for (int c = 0; c < 100; c++) RP[c] = rp[c];
    memset(dec, 0, sizeof dec); memset(u, 0, sizeof u); memset(cnt, 0, sizeof cnt);
    for (int s = 0; s < 32; s++) slotv[s] = -1;
    nodes = 0; count = 0; node_cap = 1000; count_cap = 2; nb = 0; npend = 0; pdone = 0; nfound = 0; aborted = 0; nland = 0; use_hash = 0;
    FIX = 1; for (int o = 0; o < 25; o++) fixu[o] = card[o];
    dfs(0);
    FIX = 0;
    return (int)count;
}

/* keyword arm: every key (values already numbered on the key alphabet) as the repeating key; a key fits if any
   card fits. Returns the number of keys that fit; writes up to maxhits key indices and their first card. */
long run_keys(int rot, int rd, int bl, int ord, int pa, int ca, int be, const int *rp, const int *kv, const int *koff,
              int nkeys, int *hits, int *hitn, int *hitcards, int *hitland, int maxhits, long *nodes_out) {
    ROT = rot; RD = rd; BL = bl; ORD = ord; PA = pa; CA = ca; BE = be; FIX = 0; KEYED = 1;
    for (int c = 0; c < 100; c++) RP[c] = rp[c];
    long nfit = 0, tot = 0;
    for (int w = 0; w < nkeys; w++) {
        P = koff[w + 1] - koff[w];
        if (P > 32) continue;
        for (int x = 0; x < P; x++) KEYV[x] = kv[koff[w] + x];
        memset(dec, 0, sizeof dec); memset(u, 0, sizeof u); memset(cnt, 0, sizeof cnt);
        nodes = 0; count = 0; node_cap = 100000000; count_cap = 1; nb = 0; npend = 0; pdone = 0; nfound = 0; aborted = 0; nland = 0; use_hash = 0;
        dfs(0);
        tot += nodes;
        if (count) {
            if (nfit < maxhits) {
                /* a fitting word: list up to 8 distinct landing maps (near twins differ in one letter's square) */
                memset(dec, 0, sizeof dec); memset(u, 0, sizeof u); memset(cnt, 0, sizeof cnt);
                nodes = 0; count = 0; count_cap = 8; nb = 0; npend = 0; pdone = 0; nfound = 0; aborted = 0; nland = 0;
                use_hash = 1; memset(hset, 0, sizeof hset);
                dfs(0);
                use_hash = 0;
                hits[nfit] = w; hitn[nfit] = nfound;
                for (int k = 0; k < nfound; k++) { memcpy(hitcards + 25 * (8 * nfit + k), found[k], sizeof u); memcpy(hitland + 24 * (8 * nfit + k), found_land[k], sizeof landj); }
            }
            nfit++;
        }
    }
    KEYED = 0;
    *nodes_out = tot;
    return nfit;
}

void set_text(const int *txt_std, const int *txt_kry) {
    for (int j = 0; j < N; j++) { TXT[0][j] = txt_std[j]; TXT[1][j] = txt_kry[j]; }
}
"""


def build_lib():
    d = tempfile.mkdtemp(prefix="k4_grille_")
    src, so = os.path.join(d, "g.c"), os.path.join(d, "g.so")
    open(src, "w").write(C_SOURCE)
    subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", so, src], check=True, capture_output=True)
    return ctypes.CDLL(so)


def tables():
    orb, off = [], []
    for i in range(50):
        o, s = orbit_of(i // 10, i % 10)
        orb.append(o); off.append(s)
    return orb, off


def readpos(rd):
    return [c for c in range(100)] if rd == 0 else [10 * (c % 10) + c // 10 for c in range(100)]


I = lambda v: (ctypes.c_int * len(v))(*v)


_LIB = {}


def lib_for(text, known_list):
    """One compiled library per process, re-pointed at each text."""
    pid = os.getpid()
    if pid not in _LIB:
        lib = build_lib()
        lib.run_cfg.restype = ctypes.c_long
        ip, lp = ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_long)
        lib.run_cfg.argtypes = [ctypes.c_int] * 9 + [ip, ctypes.c_long, ctypes.c_long, ip, lp, ip, ip, ip]
        lib.check_card.argtypes = [ctypes.c_int] * 8 + [ip, ip]
        _LIB[pid] = lib
    lib = _LIB[pid]
    orb, off = tables()
    kp = [q - 1 for q, _ in known_list]
    lib.setup(I([STD.index(ch) for ch in text]), I([KRY.index(ch) for ch in text]), I(kp),
              I([STD.index(a) for _, a in known_list]), I([KRY.index(a) for _, a in known_list]), I(orb), I(off))
    return lib


def count_cfg(lib, proc, order, cls, p, ncap=NODE_CAP, ccap=COUNT_CAP):
    rot, rd, bl = proc
    comp = ctypes.c_int(0); nodes = ctypes.c_long(0); nf = ctypes.c_int(0)
    fo = (ctypes.c_int * (64 * 25))(); fl = (ctypes.c_int * (64 * 24))()
    c = lib.run_cfg(0, rot, rd, bl, 0 if order == "A" else 1, cls[0], cls[1], cls[2], p, I(readpos(rd)),
                    ncap, ccap, ctypes.byref(comp), ctypes.byref(nodes), fo, ctypes.byref(nf), fl)
    found = [{"card": list(fo[25 * k: 25 * k + 25]), "land": list(fl[24 * k: 24 * k + 24])} for k in range(nf.value)]
    return c, bool(comp.value), nodes.value, found


def landing(card, proc, known_list):
    """Where the 24 known letters land under a card (carved places)."""
    wh = grille_perm(card, proc)
    return [wh[q - 1] for q, _ in known_list]


def matches(card, found, proc, known_list):
    """A found landing map is the card's own: the card puts the 24 known letters on those carved places."""
    return found["land"] == landing(card, proc, known_list)


def check_card_c(lib, card, proc, order, cls, p):
    rot, rd, bl = proc
    return lib.check_card(rot, rd, bl, 0 if order == "A" else 1, cls[0], cls[1], cls[2], p, I(readpos(rd)), I(card))


def key_arrays(words):
    """Key values of every word on the standard and the KRYPTOS alphabet, flattened, with offsets."""
    out = {}
    for ka, A_ in ((0, STD), (1, KRY)):
        kv, off = [], [0]
        for w in words:
            kv += [A_.index(ch) for ch in w]
            off.append(len(kv))
        out[ka] = (I(kv), I(off))
    return out


def run_keys_c(lib, proc, order, conv, karr, nkeys, maxhits=20):
    rot, rd, bl = proc
    pa, ca, ka, be = conv
    kv, off = karr[ka]
    hits = (ctypes.c_int * maxhits)(); hitn = (ctypes.c_int * maxhits)()
    cards = (ctypes.c_int * (25 * 8 * maxhits))(); land = (ctypes.c_int * (24 * 8 * maxhits))()
    nodes = ctypes.c_long(0)
    n = lib.run_keys(rot, rd, bl, 0 if order == "A" else 1, pa, ca, be, I(readpos(rd)), kv, off, nkeys,
                     hits, hitn, cards, land, maxhits, ctypes.byref(nodes))
    out = []
    for k in range(min(n, maxhits)):
        out.append((hits[k], [{"card": list(cards[25 * (8 * k + x): 25 * (8 * k + x) + 25]),
                               "land": list(land[24 * (8 * k + x): 24 * (8 * k + x) + 24])} for x in range(hitn[k])]))
    return n, out, nodes.value


def worker_free(args):
    """One text, one procedure, one key length: card counts for both orders and every class."""
    text, t_idx, proc, p, known_list = args
    lib = lib_for(text, known_list)
    out = {}
    for order in "AB":
        for ci, cls in enumerate(CLASSES):
            out[(order, ci)] = count_cfg(lib, proc, order, cls, p)
    return t_idx, proc, p, out


def worker_keys(args):
    """One text, one procedure: every key word on every convention, both orders."""
    text, t_idx, proc, words, known_list = args
    lib = lib_for(text, known_list)
    karr = key_arrays(words)
    out = {}
    nodes = 0
    for order in "AB":
        for vi, conv in enumerate(CONVS):
            n, hits, nd = run_keys_c(lib, proc, order, conv, karr, len(words))
            out[(order, vi)] = (n, [(words[w], card) for w, card in hits])
            nodes += nd
    return t_idx, proc, out, nodes


# ---------------------------------------------------------------------------------------------- checks and the plants
def self_check(known_list, rng):
    """The compiled search against the literal Python builder. Per trial: a random card and key make a text; the full
    free-key search must find the card; the keyword arm must find the key; and the same walk for one fixed card must
    agree with the Python test on 400 cards (the plant's neighbours in one or two orbits, and random cards) at four
    key lengths."""
    agree = fits = 0
    for trial in range(16):
        proc = PROCS[trial % len(PROCS)]
        order = "AB"[(trial // len(PROCS)) % 2]
        cls = CLASSES[(3 * trial) % 8]
        p = (3, 4, 5, 6)[trial % 4]
        u = [rng.randrange(4) for _ in range(25)]
        pt = "".join(rng.choice(STD) for _ in range(N))
        pt = "".join(dict(known_list).get(i + 1, ch) for i, ch in enumerate(pt))
        key = [rng.randrange(26) for _ in range(p)]
        ct = encrypt_with(pt, u, proc, order, cls, key)
        assert decrypt_with(ct, u, proc, order, cls, key) == pt
        assert consistent_py(ct, known_list, u, proc, order, cls, p)
        lib = lib_for(ct, known_list)
        c, comp, nodes, found = count_cfg(lib, proc, order, cls, p, ncap=2_000_000_000, ccap=100000)
        assert comp and any(matches(u, f, proc, known_list) for f in found), (trial, PROC_NAME(proc), order, cls, p, c, comp)
        assert check_card_c(lib, u, proc, order, cls, p)
        # the keyword arm on a three-mode key: the planted word among decoys
        conv = CONVS[(5 * trial) % 24]
        word = "".join(rng.choice(STD) for _ in range(rng.randrange(7, 12)))
        kv = [(STD, KRY)[conv[2]].index(ch) for ch in word]
        ct2 = encrypt_with(pt, u, proc, order, conv[:2] + (conv[3],), kv)
        lib = lib_for(ct2, known_list)
        decoys = ["".join(rng.choice(STD) for _ in range(len(word))) for _ in range(50)]
        n, hits, _ = run_keys_c(lib, proc, order, conv, key_arrays(decoys + [word]), 51)
        assert any(w == 50 for w, _ in hits), (trial, "keyword arm missed the plant")
        lib = lib_for(ct, known_list)
        cards = []
        for _ in range(150):
            v = list(u); v[rng.randrange(25)] = rng.randrange(4); cards.append(v)
        for _ in range(150):
            v = list(u); v[rng.randrange(25)] = rng.randrange(4); v[rng.randrange(25)] = rng.randrange(4); cards.append(v)
        cards += [[rng.randrange(4) for _ in range(25)] for _ in range(100)]
        for v in cards:
            for pp in (p, 19, 24, 26):
                a_ = consistent_py(ct, known_list, v, proc, order, cls, pp)
                b_ = check_card_c(lib, v, proc, order, cls, pp)
                assert bool(a_) == bool(b_), (trial, PROC_NAME(proc), order, pp, v)
                agree += 1
                fits += bool(a_)
    return {"planted_cards_found_by_full_search": 16, "planted_words_found_by_keyword_arm": 16,
            "cards_compared": agree, "of_which_fit": fits}


def plant_cases(words):
    """Planted cards strictly inside the space: a free key of length 5 (order A) and 6 (order B); a dictionary word
    (order B and A) on other conventions and procedures."""
    from kryptos.plants import english_plant
    cases = []
    for k, (proc, order, cls, p, seed) in enumerate([(PROCS[1], "A", CLASSES[3], min(5, PMAX), 1990), (PROCS[2], "B", CLASSES[5], min(6, PMAX), 1989)]):
        rng = random.Random(seed)
        u = [rng.randrange(4) for _ in range(25)]
        key = [rng.randrange(26) for _ in range(p)]
        pt = english_plant(seed)
        cases.append({"arm": "free", "proc": proc, "order": order, "cls": cls, "p": p, "u": u, "key": key, "pt": pt,
                      "ct": encrypt_with(pt, u, proc, order, cls, key)})
    for k, (proc, order, conv, seed) in enumerate([(PROCS[3], "B", CONVS[19], 1986), (PROCS[0], "A", CONVS[8], 1988)]):
        rng = random.Random(seed)
        u = [rng.randrange(4) for _ in range(25)]
        word = rng.choice([w for w in words if 8 <= len(w) <= 12])
        kv = [(STD, KRY)[conv[2]].index(ch) for ch in word]
        pt = english_plant(seed)
        cases.append({"arm": "keys", "proc": proc, "order": order, "conv": conv, "word": word, "u": u, "pt": pt,
                      "ct": encrypt_with(pt, u, proc, order, conv[:2] + (conv[3],), kv)})
    return cases


# ---------------------------------------------------------------------------------------------- F7: the fingerprints
def doublets(t):
    return [i for i in range(len(t) - 1) if t[i] == t[i + 1]]


def col_mark(t):
    dbl = doublets(t)
    if len(dbl) < 4:
        return False
    top = max(Counter(i % 7 for i in dbl).values())
    return len(dbl) - top <= 1 and top >= 4


def rep21(t):
    v = [t[i] + t[i + 21] for i in range(len(t) - 21)]
    return len(v) - len(set(v))


def fingerprints(rng, samples=4000):
    import re
    carter = re.sub("[^A-Z]", "", (ROOT / "knowledge/sources/carter-1923-tomb-of-tutankhamen-vol1.txt").read_text(errors="ignore").upper())
    res = {}
    for name, order, p in (("grille, then a length-7 key", "A", 7), ("length-7 key, then the grille", "B", 7),
                           ("grille, then a length-21 key", "A", 21), ("length-21 key, then the grille", "B", 21),
                           ("calibration: random letters", None, 0)):
        col = rep = both = 0
        for _ in range(samples):
            if order is None:
                ct = "".join(rng.choice(STD) for _ in range(N))
            else:
                o = rng.randrange(len(carter) - N)
                ct = encrypt_with(carter[o:o + N], [rng.randrange(4) for _ in range(25)], rng.choice(PROCS), order,
                                  CLASSES[rng.randrange(8)], [rng.randrange(26) for _ in range(p)])
            a_, b_ = col_mark(ct), rep21(ct) >= 11
            col += a_; rep += b_; both += a_ and b_
        res[name] = {"column": col / samples, "repeats21": rep / samples, "both": both / samples}
    return res


# ---------------------------------------------------------------------------------------------- run
def keywords(vocab):
    words = [w.strip().upper() for w in (ROOT / "kryptos" / "data" / "words.txt").read_text().split()]
    extra = ["PALIMPSEST", "ABSCISSA", "KRYPTOS", "IQLUSION", "UNDERGRUUND", "DESPARATLY", "LAYERTWO", "BERLINCLOCK",
             "WELTZEITUHR", "ALEXANDERPLATZ", "EASTNORTHEAST", "SHADOWFORCES", "LUCIDMEMORY", "VIRTUALLYINVISIBLE",
             "DIGETALINTERPRETATION", "TISYOURPOSITION", "WONDERFULTHINGS", "CANYOUSEEANYTHING", "TUTANKHAMUN",
             "HOWARDCARTER", "WILLIAMWEBSTER", "EDWARDSCHEIDT", "JAMESSANBORN", "PETRIFIEDWOOD", "LODESTONE"]
    seen, out = set(), []
    for w in [v.upper() for v in vocab] + extra + words:
        if w.isalpha() and KEY_MIN <= len(w) <= 32 and w not in seen:
            seen.add(w); out.append(w)
    return out


def summarise_free(per, T):
    """per[t][(proc, order, ci, p)] = (count, complete, nodes, found). Per procedure and order: cards by length (summed
    over classes), the shortest length with a card, and the cells (order, length) where K4 exceeds every copy."""
    out = {}
    for proc in PROCS:
        pn = PROC_NAME(proc)
        out[pn] = {}
        for order in "AB":
            tot = [[sum(per[t][(proc, order, ci, p)][0] for ci in range(8)) for p in range(1, PMAX + 1)] for t in range(T)]
            inc = [[any(not per[t][(proc, order, ci, p)][1] for ci in range(8)) for p in range(1, PMAX + 1)] for t in range(T)]
            first = lambda t: next((p for p in range(1, PMAX + 1) if tot[t][p - 1]), None)
            above = lambda t: [p for p in range(1, PMAX + 1) if tot[t][p - 1] > max(tot[s][p - 1] for s in range(T) if s != t)]
            out[pn][order] = {"k4_placements_by_length": tot[0], "copies_placements_by_length_max": [max(tot[t][i] for t in range(1, T)) for i in range(PMAX)],
                              "incomplete_lengths_any_text": [p for p in range(1, PMAX + 1) if any(inc[t][p - 1] for t in range(T))],
                              "k4_shortest_fit": first(0), "copies_shortest_fit": [first(t) for t in range(1, T)],
                              "k4_above_every_copy": above(0), "copy_cells_above_rest": [len(above(t)) for t in range(1, T)]}
    return out


def run(ctx):
    import multiprocessing as mp
    import sys
    import types
    ct, known = ctx.K4, ctx.KNOWN
    known_list = [(q, known[q]) for q in sorted(known)]
    t0 = time.time()
    rng = random.Random(2010)
    for proc in PROCS:
        assert sorted(grille_perm([rng.randrange(4) for _ in range(25)], proc)) == list(range(N))
    sc = self_check(known_list, rng)
    words = keywords(ctx.vocabulary)
    texts = [ct]
    srng = random.Random(1620)
    for _ in range(N_CONTROLS):
        sh = list(ct); srng.shuffle(sh); texts.append("".join(sh))
    plants = plant_cases(words)
    T = len(texts)
    all_texts = texts + [pl["ct"] for pl in plants]
    if getattr(sys.modules.get(__name__), "worker_free", None) is not worker_free:
        mod = types.ModuleType(__name__); mod.__dict__.update(globals()); sys.modules[__name__] = mod
    per_free = [dict() for _ in all_texts]
    per_keys = [dict() for _ in all_texts]
    nodes_free = nodes_keys = 0
    t_free = time.time()
    with mp.get_context("fork").Pool(WORKERS) as pool:
        # arm 1: free keys, lengths 1-6, longest first so the pool stays full
        jobs = [(tx, ti, proc, p, known_list) for p in range(PMAX, 0, -1) for ti, tx in enumerate(all_texts) for proc in PROCS]
        for ti, proc, p, out in pool.imap_unordered(worker_free, jobs):
            for (order, ci), v in out.items():
                per_free[ti][(proc, order, ci, p)] = v
                nodes_free += v[2]
        t_keys = time.time()
        # arm 2: key words of 7 letters or more
        jobs = [(tx, ti, proc, words, known_list) for ti, tx in enumerate(all_texts) for proc in PROCS]
        for ti, proc, out, nd in pool.imap_unordered(worker_keys, jobs):
            for (order, vi), v in out.items():
                per_keys[ti][(proc, order, vi)] = v
            nodes_keys += nd
    t_end = time.time()
    stat = summarise_free(per_free[:T], T)
    # key-word arm statistic: settings (word, convention, order, procedure) with a fitting card, per text
    key_fit = [sum(v[0] for v in per_keys[t].values()) for t in range(len(all_texts))]
    k4_key_hits = [{"procedure": PROC_NAME(pr), "order": o, "convention": CONV_NAME(CONVS[vi]), "words": [w for w, _ in v[1]][:20], "n": v[0]}
                   for (pr, o, vi), v in per_keys[0].items() if v[0]]
    plant_res = []
    for k, pl in enumerate(plants):
        t = T + k
        if pl["arm"] == "free":
            ci = CLASSES.index(pl["cls"])
            c, comp, nodes, found = per_free[t][(pl["proc"], pl["order"], ci, pl["p"])]
            shorter = sum(per_free[t][(pl["proc"], pl["order"], cj, q)][0] for cj in range(8) for q in range(1, pl["p"]))
            plant_res.append({"arm": "free key", "procedure": PROC_NAME(pl["proc"]), "order": pl["order"], "class": CLASS_NAME(pl["cls"]),
                              "length": pl["p"], "placements_fitting_at_its_setting": c, "complete": comp,
                              "planted_card_found": any(matches(pl["u"], f, pl["proc"], known_list) for f in found),
                              "placements_at_shorter_lengths": shorter})
        else:
            vi = CONVS.index(pl["conv"])
            n, hits = per_keys[t][(pl["proc"], pl["order"], vi)]
            plant_res.append({"arm": "key word", "procedure": PROC_NAME(pl["proc"]), "order": pl["order"], "convention": CONV_NAME(pl["conv"]),
                              "word": pl["word"], "words_fitting_at_its_setting": n, "planted_word_found": any(w == pl["word"] for w, _ in hits),
                              "planted_card_found": any(w == pl["word"] and any(matches(pl["u"], f, pl["proc"], known_list) for f in fs) for w, fs in hits),
                              "settings_fitting_anywhere": key_fit[t]})
    fp = fingerprints(random.Random(7), 2000) if ctx.time_left() > 120 else {"skipped": "time"}
    above_k4 = sum(len(stat[pn][o]["k4_above_every_copy"]) for pn in stat for o in "AB")
    null = [sum(stat[pn][o]["copy_cells_above_rest"][t] for pn in stat for o in "AB") for t in range(N_CONTROLS)]
    k4_free_fits = [{"procedure": PROC_NAME(pr), "order": o, "class": CLASS_NAME(CLASSES[ci]), "length": p, "placements": v[0], "first": v[3][:3]}
                    for (pr, o, ci, p), v in per_free[0].items() if v[0]]
    bounds = {
        "family": "10x10 turning grille (25 holes, three empty cells), then or before a repeating key on the standard/KRYPTOS tables; exact constraint search",
        "cards_per_procedure": 4 ** 25, "procedures": [PROC_NAME(p) for p in PROCS],
        "orders": {"A": "grille, then key", "B": "key, then grille"},
        "texts": f"K4, {N_CONTROLS} scrambled copies (seed 1620), {len(plants)} planted grilles",
        "free_key": {"lengths": f"1-{PMAX}", "classes": [CLASS_NAME(c) for c in CLASSES], "per_procedure": stat,
                     "k4_fits": k4_free_fits, "k4_cells_above_every_copy": above_k4, "copy_cells_above_rest": null,
                     "search_nodes": nodes_free, "seconds": round(t_keys - t_free),
                     "blocked": "lengths 7-26: one setting costs 0.9-7 x 10^8 nodes at length 7 and over 2 x 10^9 at 12 (measured on K4), about 10^5 settings: blocked by cost"},
        "key_words": {"words": len(words), "lengths": f"{KEY_MIN}-{max(len(w) for w in words)}", "conventions": [CONV_NAME(c) for c in CONVS],
                      "source": "the vocabulary, puzzle phrases, kryptos/data/words.txt", "settings_per_text": len(words) * 48 * len(PROCS),
                      "k4_settings_with_a_card": key_fit[0], "copies_settings_with_a_card": key_fit[1:T], "k4_hits": k4_key_hits[:20],
                      "search_nodes": nodes_keys, "seconds": round(t_end - t_keys)},
        "plants": plant_res,
        "stop_queue": above_k4 > max(null) or key_fit[0] > max(key_fit[1:T]),
        "self_check": {**sc, "note": "the compiled walk agrees with the literal Python builder (turn the card, fill holes by rows, copy out) on every card compared"},
        "fingerprints_F7": fp,
        "not_tested": "free keys of 7-26 letters (cost); stencils with arbitrary holes (any permutation); the Abwehr's 13x19 card (no rule for its holes in the source)",
        "seconds": round(time.time() - t0),
        "exhaustive": "yes for both arms: every card, every procedure, both orders; free keys 1-6, key words 7 letters and up",
    }
    notes = ("Plants: " + "; ".join(f"{p['arm']} {p['procedure']} {p['order']}: found {p['planted_card_found']}" for p in plant_res)
             + f". Free keys 1-{PMAX}: K4 fits {len(k4_free_fits)} settings; K4 above every copy in {above_k4} cells, copies {min(null)}-{max(null)}."
             + f" Key words ({len(words):,}): settings with a card K4 {key_fit[0]}, copies {min(key_fit[1:T])}-{max(key_fit[1:T])}.")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return encrypt_with(plaintext, key["u"], tuple(key["proc"]), key["order"], tuple(key["cls"]), key["key"])


def worked_example(ctx, key):
    u = [(3 * i + 1) % 4 for i in range(25)]
    proc = PROCS[0]
    wh = grille_perm(u, proc)
    turn = {}
    for r in range(10):
        for c in range(10):
            o, s_ = orbit_of(r, c)
            turn[(r, c)] = (u[o] + s_) % 4
    lines = ["a card: the turn on which each square is written (0-3), clockwise, copied out by rows", ""]
    for r in range(10):
        lines.append("  " + " ".join(str(turn[(r, c)]) for c in range(10)))
    lines += ["", "the holes of the first position are the 0s; the 97 letters fill the 0s row by row, then the 1s, 2s, 3s;",
              "the last three 3s stay empty", "", "place  known  lands at  carved"]
    for q in (22, 26, 34, 64, 74):
        lines.append(f"{q:5d}  {ctx.KNOWN[q]:>5}  {wh[q - 1] + 1:8d}  {ctx.K4[wh[q - 1]]:>6}")
    return "\n".join(lines)
