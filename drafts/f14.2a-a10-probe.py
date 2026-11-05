"""F14.2a desk probe: which settings give K4 its fitting keyword-alphabet pairs at 0271's edge cells
(order A, key length 10, both forms; K4 1 setting each, 50 shuffles 0 and at most 1), and what reading each forces.

Uses 0271's frozen attack.py unchanged. Run: uv run python drafts/f14.2a-a10-probe.py [L] [o]
"""
import importlib.util, json, sys, time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
path = next((ROOT / "experiments").glob("0271-*")) / "attack.py"
spec = importlib.util.spec_from_file_location("a271", path)
m = importlib.util.module_from_spec(spec); sys.modules["a271"] = m; spec.loader.exec_module(m)
m.ROOT = ROOT

from kryptos.facts import load_vocabulary, K4, KNOWN

L = int(sys.argv[1]) if len(sys.argv) > 1 else 10
O = sys.argv[2] if len(sys.argv) > 2 else "A"
m.setup(load_vocabulary())
lib = m.routes()
tix = np.array([ord(c) - 65 for c in K4])


def job(rr):
    out = []
    for r in rr:
        pairs, land, first = m.checks_of(lib[r][1], O, L)
        if len(pairs) < m.MIN_LIST:
            continue
        cl = tix[land]
        k = min(len(pairs), m.KMAX)
        ck = m.cipher_key(cl, pairs, k)
        for form in "VB":
            n, lst = m.fits(cl, pairs, m.plain_index(pairs, form), ck, form)
            if n and lst is not None:
                for ci, pi in zip(*lst):
                    out.append((r, form, int(ci), int(pi), len(pairs), sorted(first)))
            elif n:
                out.append((r, form, -1, -1, len(pairs), n))
    return out


if __name__ == "__main__":
    t0 = time.time()
    chunks = [range(a, min(a + 200, len(lib))) for a in range(0, len(lib), 200)]
    with Pool(8) as p:
        hits = [h for part in p.map(job, chunks) for h in part]
    A = m._G["A"]; names = m._G["names"]; pos = m._G["pos"]
    KP = m._G["KP"]
    res = []
    for r, form, ci, pi, c, cover in hits:
        if ci < 0:
            res.append({"route": r, "form": form, "checks": c, "count_only": cover}); continue
        where = lib[r][1]
        slot, mpos = m.geometry(where, O, L)
        PA, CA = A[pi], A[ci]
        k = [None] * L
        for q in KP:
            j = where[q - 1]
            cv, pv = CA.index(K4[j]), PA.index(KNOWN[q])
            k[slot[j]] = (cv - pv) % 26 if form == "V" else (cv + pv) % 26
        pt = []
        for i in range(m.N):
            j = where[i]
            kk = k[slot[j]]
            if kk is None:
                pt.append("?"); continue
            c = CA.index(K4[j])
            pt.append(PA[(c - kk) % 26] if form == "V" else PA[(kk - c) % 26])
        res.append({"route": r, "route_name": str(lib[r][0]), "form": form, "checks": c,
                    "pa": PA, "pa_name": str(names[pi]), "ca": CA, "ca_name": str(names[ci]),
                    "key": "".join("?" if v is None else m.STD[v] for v in k),
                    "reading": "".join(pt), "open": pt.count("?")})
    print(json.dumps({"L": L, "o": O, "secs": round(time.time() - t0), "hits": res}, indent=1))
