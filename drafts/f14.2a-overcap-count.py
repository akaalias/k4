"""F14.2a desk count: settings of 0271 where the first KMAX=6 checks hold 3 or more equal-letter checks
(same known letter twice in one slot). There the index keys on 3 or fewer informative checks, chance pairs exceed
LIST_CAP, and 0271 counted unverified pairs and skipped the key-word step, for any text that passes the trivial
checks: the true setting always does. Text-independent. Run: uv run python drafts/f14.2a-overcap-count.py"""
import importlib.util, json, sys
from collections import Counter
from multiprocessing import Pool
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent; sys.path.insert(0, str(ROOT))
p = next((ROOT / "experiments").glob("0271-*")) / "attack.py"
s = importlib.util.spec_from_file_location("a271", p); m = importlib.util.module_from_spec(s); sys.modules["a271"] = m
s.loader.exec_module(m); m.ROOT = ROOT
from kryptos.facts import KNOWN
KP = sorted(KNOWN); m._G["KP"] = KP
lib = m.routes()

def job(rr):
    c = Counter(); lst = []
    for r in rr:
        for o in "AB":
            for L in range(1, 27):
                pairs, land, first = m.checks_of(lib[r][1], o, L)
                if len(pairs) < m.MIN_LIST:
                    continue
                eq = [KNOWN[KP[a]] == KNOWN[KP[b]] for a, b in pairs]
                inf_first = sum(not e for e in eq[:m.KMAX]); inf_all = sum(not e for e in eq)
                if inf_first <= 3:
                    c[(o, L, min(inf_all, 9))] += 1
                    if inf_all >= 5 or True:
                        lst.append((r, o, L, inf_all))
                c[("all", o, L)] += 1
    return c, lst

if __name__ == "__main__":
    chunks = [range(a, min(a + 300, len(lib))) for a in range(0, len(lib), 300)]
    with Pool(8) as pool:
        parts = pool.map(job, chunks)
    C = Counter(); S = []
    for c, l in parts: C.update(c); S += l
    tot = sum(v for k, v in C.items() if k[0] == "all")
    hit = len(S)
    by_inf = Counter(min(x[3], 9) for x in S)
    by_L = Counter((x[1], x[2]) for x in S if x[3] >= 5)
    print(json.dumps({"listed_settings": tot, "overcap_risk": hit, "by_informative_total": sorted(by_inf.items()),
                      "risk_with_5plus_informative_by_oL": sorted(by_L.items())}, default=str))
    json.dump(S, open("/tmp/f142a_overcap_settings.json", "w"))
