"""F13.6 desk probe: do masked messages survive into the readings an F13 search keeps?
Masked Carter (A13's mask makers, as in tools/a13_check.py) enciphered with a key word on the sculpture's tables
(0243 method A: a dictionary word, random rule), solved by 0243's frozen search; found = the kept method-A reading
is the masked plaintext itself, so A13's battery would be looking at it."""
import importlib.util, json, random, sys
from multiprocessing import get_context
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
p = next((ROOT / "experiments").glob("0243-*")) / "attack.py"
spec = importlib.util.spec_from_file_location("f243", p); A = importlib.util.module_from_spec(spec); spec.loader.exec_module(A)
A.ROOT = ROOT
from kryptos import facts
STD = A.STD
A.lib(); A.models(); A.prepare(facts.load_vocabulary()); A._G["sources"] = A._G["lists"]["sources"]
src = A._G["corpus"]["test"]
rng = random.Random(246)
def plain(): o = rng.randrange(len(src) - 200); return src[o:o + 97]
def reverse(): return plain()[::-1]
def xregular():
    k = rng.randrange(5, 12); t = list(plain()); return "".join("X" if i % k == k - 1 else t.pop(0) for i in range(97))
def interleaved():
    n = rng.randrange(2, 5); o = rng.randrange(n); t = list(plain()); return "".join(t.pop(0) if i % n == o else rng.choice(STD) for i in range(97))
def columns():
    w = rng.randrange(3, 30); t = plain(); return "".join(t[i] for c in range(w) for i in range(c, 97, w))
def nulls():
    n = rng.randrange(3, 9); o = rng.randrange(n); t = list(plain()); return "".join(rng.choice(STD) if i % n == o else t.pop(0) for i in range(97))
def affine():
    a = rng.choice([3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]); b = rng.randrange(26); return "".join(STD[(a * STD.index(c) + b) % 26] for c in plain())
MASKS = {"none": plain, "reversal": reverse, "X every kth": xregular, "message in every nth": interleaved, "columns": columns, "nulls every nth": nulls, "affine std": affine}
jobs = []
for name, f in MASKS.items():
    for j in range(4):
        pt = f()
        n = rng.choice([5, 8, 11]); w, r = rng.choice(A._G["lists"]["drot"][n])[1]
        rule = A.RULES[rng.randrange(24)]
        key = {"method": "A", "mode": rule[0], "pa": rule[1], "ca": rule[2], "ka": rule[3], "key": w, "start": r}
        jobs.append((name, pt, A.encrypt(pt, key)))
def job(a):
    name, pt, ct = a
    out = A.solve(ct)
    return name, out["A"][1] == pt
if __name__ == "__main__":
    with get_context("fork").Pool(8) as pool:
        res = pool.map(job, jobs)
    tally = {}
    for name, ok in res: tally.setdefault(name, [0, 0]); tally[name][0] += ok; tally[name][1] += 1
    print(json.dumps(tally))
