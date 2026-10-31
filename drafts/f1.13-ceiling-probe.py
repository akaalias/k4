"""F1.13 desk probe (2026-10-31): is each 0256 plant's true reading the best reading its cell allows?

For each of 0256's plants (regenerated with its seeds), run 0256's own compiled tempering (ptemper, one replica,
low temperature) started from the plant's TRUE alphabet. If it finds a reading with all checkable known places
right that scores above the true reading, the quadgram score cannot pick out the plant in that cell whatever the
search: a ceiling on the power of any climb that uses this score. Usage: uv run python drafts/f1.13-ceiling-probe.py ct|pt
"""
import ctypes
import importlib.util
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
spec = importlib.util.spec_from_file_location("probe", ROOT / "drafts" / "f1.13-split-probe.py")
P = importlib.util.module_from_spec(spec); spec.loader.exec_module(P)


def main():
    kind = sys.argv[1] if len(sys.argv) > 1 else "ct"
    rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    from kryptos.facts import KNOWN
    m56 = P.load("0256")
    L_ = m56.lib()
    plants, expect = P.plants_0256(kind)
    kp = sorted(KNOWN)
    above = 0
    for pl in plants:
        k_, form, L = pl["cell"]
        text = pl["ct"]
        L_.setup(m56._MODS["tab"], (ctypes.c_int * 97)(*[ord(c) - 65 for c in text]), 97, L, m56.KINDS.index(k_), m56.FORMS.index(form),
                 (ctypes.c_int * 24)(*[q - 1 for q in kp]), (ctypes.c_int * 24)(*[ord(KNOWN[q]) - 65 for q in kp]), 24)
        w = [pl["alpha"].index(chr(65 + i)) for i in range(26)]
        S = L if kind == "ct" else 0
        s_true = m56._load("0149") and None
        from kryptos.scorer import english_score
        s_true = english_score(pl["pt"][S:])
        bp, bx = (ctypes.c_int * 128)(), (ctypes.c_int * 26)()
        t0 = time.time()
        sc = L_.ptemper(7 + pl["idx"], (ctypes.c_int * 26)(*w), 1, rounds, 1000, 0.15, 0.02, 0.6, bp, bx)
        rd = "".join("?" if bp[i] < 0 else chr(65 + bp[i]) for i in range(97))
        right = sum(a == b for a, b in zip(rd[S:], pl["pt"][S:]))
        wrong_better = sc > s_true + 1e-6 and right < (97 - S) * 0.8
        above += wrong_better
        e = expect.get(f"{kind}/{pl['idx']}", {})
        print(f"{kind}/{pl['idx']:2d} {pl['cls']:7s} {'/'.join(map(str, pl['cell'])):8s} places {97 - S:2d} true {s_true:.3f} "
              f"from-true best {sc:.3f} letters {right}/{97 - S} wrong-better {wrong_better} | 0256 score {e.get('score')} found {e.get('found')} "
              f"letters {e.get('letters_right')} | {time.time() - t0:.1f}s", flush=True)
    print(f"{kind}: {above}/{len(plants)} plants where a wrong reading beats the true one")


if __name__ == "__main__":
    main()
