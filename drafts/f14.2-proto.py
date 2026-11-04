"""F14.2 desk prototype (2026-11-04): the per-setting two-alphabet test with the plain-side index shared by all texts.
Checks: the identity move reproduces 0244's fit counts on K4 (no move); timing per (setting, text).
Run: uv run python drafts/f14.2-proto.py"""
import importlib.util
import json
import random
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from kryptos.facts import KNOWN, load_vocabulary  # noqa: E402

N = 97


def load(e):
    path = next((ROOT / "experiments").glob(f"{e}-*")) / "attack.py"
    spec = importlib.util.spec_from_file_location(f"f{e}", path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    if hasattr(m, "ROOT"):
        m.ROOT = ROOT
    return m


m44 = load("0244")
A, names, pos = m44.alphabets()
pos = pos.astype(np.int64)
NA = len(A)
KP = sorted(KNOWN)
KL = np.array([ord(KNOWN[q]) - 65 for q in KP])
POW = 26 ** np.arange(8, dtype=np.int64)
KMAX = 6


def checks_of(where, o, L):
    """Known places grouped by key slot -> list of (a, b) index pairs into KP, and each known place's carved place."""
    land = [where[q - 1] for q in KP]                 # message place q-1 lands at carved place where[q-1]
    slot = [(land[e] % L) if o == "A" else ((q - 1) % L) for e, q in enumerate(KP)]
    groups = {}
    for e, s in enumerate(slot):
        groups.setdefault(s, []).append(e)
    pairs = [(g[0], u) for g in groups.values() for u in g[1:]]
    return pairs, land


def plain_index(pairs, form):
    """Sorted keys of every plain alphabet on the first k checks, and the order."""
    k = min(len(pairs), KMAX)
    a = np.array([p[0] for p in pairs[:k]]); b = np.array([p[1] for p in pairs[:k]])
    d = (pos[:, KL[a]] - pos[:, KL[b]]) % 26
    if form == "B":
        d = (-d) % 26
    key = (d * POW[:k]).sum(axis=1)
    order = np.argsort(key, kind="stable")
    return key[order], order, k


def count(text, where, o, L, form):
    pairs, land = checks_of(where, o, L)
    if not pairs:
        return None
    tix = np.array([ord(c) - 65 for c in text])
    pidx = plain_index(pairs, form)
    skey, sorder, k = pidx
    cl = tix[np.array(land)]
    a = np.array([p[0] for p in pairs]); b = np.array([p[1] for p in pairs])
    dc = (pos[:, cl[a[:k]]] - pos[:, cl[b[:k]]]) % 26
    ckey = (dc * POW[:k]).sum(axis=1)
    lo = np.searchsorted(skey, ckey, "left"); hi = np.searchsorted(skey, ckey, "right")
    n = hi - lo
    tot = int(n.sum())
    if tot == 0 or len(pairs) <= k:
        return tot
    if tot > 5_000_000:
        return ("too many", tot)
    ci = np.repeat(np.arange(NA), n)
    off = np.arange(tot) - np.repeat(np.cumsum(n) - n, n)
    pi = sorder[np.repeat(lo, n) + off]
    s = 1 if form == "V" else -1
    ok = np.ones(tot, bool)
    for e in range(k, len(pairs)):
        x, y = pairs[e]
        ok &= ((pos[ci, cl[x]] - pos[ci, cl[y]]) % 26) == ((s * (pos[pi, KL[x]] - pos[pi, KL[y]])) % 26)
    return int(ok.sum())


if __name__ == "__main__":
    k4 = (ROOT / "data" / "k4.txt").read_text().strip()
    rec = json.loads((next((ROOT / "experiments").glob("0244-*")) / "raw.json").read_text())
    ref = rec["bounds"]["fitting_pairs_k4_and_copies"]
    ident = list(range(N))
    for L in (8, 13, 16, 19, 20, 22, 23):
        for form, f44 in (("V", "added"), ("B", "beaufort")):
            t = time.time()
            got = count(k4, ident, "A", L, form)
            print(f"L{L} {form}: proto {got}, 0244 {ref[f'{L}/{f44}']['k4']}  ({time.time() - t:.3f} s)")
    lib = load("0129").route_library(load_vocabulary())
    print("routes", len(lib))
    rng = random.Random(1)
    t = time.time(); n = 0; dist = {}
    for _ in range(300):
        r = rng.randrange(len(lib)); o = rng.choice("AB"); L = rng.randrange(1, 27)
        pairs, _ = checks_of(lib[r][1], o, L)
        dist[min(len(pairs), 9)] = dist.get(min(len(pairs), 9), 0) + 1
        for form in "VB":
            count(k4, lib[r][1], o, L, form); n += 1
    print(f"{n} (setting, form) on K4 in {time.time() - t:.1f} s: {1000 * (time.time() - t) / n:.1f} ms each; checks {sorted(dist.items())}")
