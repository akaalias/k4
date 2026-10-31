"""F1.13 desk probe (2026-10-31): 0256's check-keeping tempering ('keep', which 0256 used only to lag 12) on 0256's
plaintext-autokey plants at lags up to 26, started from the exact witness as 0256 starts. Usage: ... pt i [i ...]"""
import ctypes, importlib.util, random, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
spec = importlib.util.spec_from_file_location("probe", ROOT / "drafts" / "f1.13-split-probe.py")
P = importlib.util.module_from_spec(spec); spec.loader.exec_module(P)
from kryptos.facts import KNOWN
from kryptos.scorer import english_score
m56 = P.load("0256"); L_ = m56.lib()
plants, expect = P.plants_0256("pt")
kp = sorted(KNOWN)
for i in map(int, sys.argv[1:]):
    pl = plants[i]; k_, form, L = pl["cell"]
    t0 = time.time()
    rng = random.Random(i)
    w = m56.witness(pl["ct"], pl["cell"], rng)
    L_.setup(m56._MODS["tab"], (ctypes.c_int * 97)(*[ord(c) - 65 for c in pl["ct"]]), 97, L, 1, m56.FORMS.index(form),
             (ctypes.c_int * 24)(*[q - 1 for q in kp]), (ctypes.c_int * 24)(*[ord(KNOWN[q]) - 65 for q in kp]), 24)
    bp, bx, live = (ctypes.c_int * 128)(), (ctypes.c_int * 26)(), ctypes.c_int()
    sc = L_.keep(rng.randrange(1 << 62), (ctypes.c_int * 26)(*w), m56.K_R, m56.K_ROUNDS, m56.K_MOVES, m56.K_T0, m56.K_T1, bp, bx, ctypes.byref(live))
    rd = "".join("?" if bp[j] < 0 else chr(65 + bp[j]) for j in range(97))
    right = sum(a == b for a, b in zip(rd, pl["pt"]))
    print(f"pt/{i:2d} {pl['cls']:7s} {'/'.join(map(str, pl['cell'])):8s} true {english_score(pl['pt']):.3f} keep {sc:.3f} live {live.value} "
          f"letters {right}/97 | 0256 {expect[f'pt/{i}']['score']} | {time.time() - t0:.0f}s", flush=True)
