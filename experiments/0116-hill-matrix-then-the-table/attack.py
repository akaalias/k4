"""Experiment 0116. See program.md for the contract."""

EXPERIMENT = {
    "slug": "hill-matrix-then-the-table",
    "title": "A Hill matrix and a repeating key on the table, in either order: 'matrix codes', then 'back to this table'",
    "family": "8-hill-polygraphic",
    "parent": "0105-affine-hill-solved-letter-by-letter",
    "changed": "0105 solved Hill and affine Hill alone. Sanborn's words, 'matrix codes Ed gave me' and 'double matrixes... then went back to this table to do the ultimate', and the HILL column read literally give a Hill matrix followed by the Vigenere table, or the table followed by the matrix. On one numbering both orders give p = B c + u, where the shift vector u depends on the block's place modulo the key length: still linear, so each row of B is solved exactly from every known letter for key lengths 1-26.",
    "hypothesis_expert": (
        "C1 ('double matrixes and triple matrixes... then went back to this table'), C21 (the HILL column; Bauer), C3 "
        "('matrix codes'). Model, one numbering for both stages (standard or KRYPTOS order, 0- or 1-based): blocks of n = "
        "2-4 carved letters; message block p = B c + u_kappa mod 26, B invertible, kappa = (block start) mod L "
        "classes, L = 1-26 the key length, u_kappa free. This covers Hill then a periodic Vigenere key (u = -B k) and a "
        "periodic key then Hill (u = w - k) alike, and an affine Hill. Row r of (B, u) has n + #classes unknowns; each known "
        "letter in row position r gives one equation. Solved exactly mod 2 and mod 13 with the Chinese remainder "
        "theorem; a setting dies if a row has no solution or no choice makes B invertible; rows with more unknowns than "
        "equations leave it open. Block alignments 0 to n-1. Ten shuffled coppers."
    ),
    "hypothesis_eli5": (
        "Sanborn said he used the matrix codes Ed Scheidt gave him, and then went back to the table. A Hill cipher is "
        "literally a matrix code: blocks of letters are multiplied by a small square of numbers. Here a Hill matrix of "
        "size 2, 3 or 4 is combined with a short repeating secret word on the table, in either order. Every known "
        "letter gives one equation, and the equations are solved exactly."
    ),
    "prediction": (
        "No setting with spare equations survives for any size, key length, alignment or numbering; settings with no "
        "spare equations are reported as open. Counts match the coppers. Zero candidates."
    ),
    "method": (
        "1. For each size, key length, alignment and numbering, group the known letters by block, row position and block class. "
        "2. Solve each row mod 2 and mod 13; join by the Chinese remainder theorem. 3. Require an invertible B. 4. Count "
        "alive (with spare equations), dead and open settings. 5. Repeat on ten shuffled coppers."
    ),
    "walkthrough": (
        "1. Cut the copper into blocks of 2 from place 1 and use a key of length 4: blocks starting at places 1, 5, 9, ... share one key pair, those at 3, 7, 11, ... the other. "
        "2. For each known letter, write: its number = row of the matrix times the block's two carved numbers + the shift for its row and block class. "
        "3. Row 1 then has 2 matrix entries and 2 shifts as unknowns, against about 12 equations. "
        "4. Solve mod 2 and mod 13; if no solution, or no invertible matrix, the setting dies. "
        "5. Repeat for sizes 2-4, key lengths 1-26, alignments and numberings, and on scrambled coppers."
    ),
}

import random
from itertools import product
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
N_CONTROLS = 10
CAP = 200
LMAX = 26


def solve_mod_prime(rows, rhs, nv, q):
    """All solutions of rows x = rhs mod q (prime), enumerated if the nullity is small; [] if none; None if too many."""
    M = [[x % q for x in r] + [b % q] for r, b in zip(rows, rhs)]
    piv, r = [], 0
    for c in range(nv):
        pr = next((i for i in range(r, len(M)) if M[i][c]), None)
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        inv = pow(M[r][c], q - 2, q)
        M[r] = [(x * inv) % q for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [(a - f * b) % q for a, b in zip(M[i], M[r])]
        piv.append(c); r += 1
    if any(all(x == 0 for x in row[:nv]) and row[nv] for row in M):
        return []
    free = [c for c in range(nv) if c not in piv]
    if q ** len(free) > CAP:
        return None
    sols = []
    for vals in product(range(q), repeat=len(free)):
        x = [0] * nv
        for c, v in zip(free, vals):
            x[c] = v
        for i, c in enumerate(piv):
            x[c] = (M[i][nv] - sum(M[i][f] * x[f] for f in free)) % q
        sols.append(x)
    return sols


def crt(a2, a13):
    return [(x13 + 13 * ((x2 - x13) % 2)) % 26 for x2, x13 in zip(a2, a13)]


def det_mod(M, q):
    M = [[x % q for x in r] for r in M]
    n, d = len(M), 1
    for c in range(n):
        pr = next((i for i in range(c, n) if M[i][c]), None)
        if pr is None:
            return 0
        if pr != c:
            M[c], M[pr] = M[pr], M[c]; d = -d
        d = d * M[c][c] % q
        inv = pow(M[c][c], q - 2, q)
        for i in range(c + 1, n):
            f = M[i][c] * inv % q
            M[i] = [(a - f * b) % q for a, b in zip(M[i], M[c])]
    return d % q


def invertible(B):
    return det_mod(B, 2) != 0 and det_mod(B, 13) != 0


def setting(ct, known, n, align, num, L):
    A, base = num
    idx = {c: (i + base) % 26 for i, c in enumerate(A)}
    blocks = {}
    for q, ch in known.items():
        j = q - 1 - align
        if j < 0:
            continue
        b, r = divmod(j, n)
        start = align + b * n
        if start + n > N:
            continue
        kappa = start % L
        blocks.setdefault(r, []).append(([idx[ct[start + k]] for k in range(n)], kappa, idx[ch]))
    classes = sorted({k for eqs in blocks.values() for _, k, _ in eqs})
    cpos = {k: i for i, k in enumerate(classes)}
    nv = n + len(classes)
    row_sols, checks, open_ = [], 0, False
    for r in range(n):
        eqs = blocks.get(r, [])
        rows = [cv + [1 if cpos[k] == i else 0 for i in range(len(classes))] for cv, k, _ in eqs]
        rhs = [p for _, _, p in eqs]
        used = set(cpos[k] for _, k, _ in eqs)
        nv_r = n + len(used)
        if len(eqs) <= nv_r:
            open_ = True
        s2 = solve_mod_prime(rows, rhs, nv, 2); s13 = solve_mod_prime(rows, rhs, nv, 13)
        if s2 == [] or s13 == []:
            return "dead", 0
        if s2 is None or s13 is None:
            open_ = True
            row_sols.append(None)
            continue
        sols = {tuple(crt(x, y)[:n]) for x in s2 for y in s13}
        checks += max(0, len(eqs) - nv_r)
        row_sols.append(sorted(sols))
    if open_ or any(s is None for s in row_sols):
        return "open", checks
    total = 1
    for s in row_sols:
        total *= len(s)
    if total > 20000:
        return "open", checks
    for combo in product(*row_sols):
        if invertible([list(x) for x in combo]):
            return "alive", checks
    return "dead", checks


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    rng = random.Random(116)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    assert plant_check()
    nums = [(STD, 0), (STD, 1), (KRY, 0), (KRY, 1)]
    table = {}
    k4_alive = []
    for n in (2, 3, 4):
        for L in range(1, LMAX + 1):
            res = []
            for t, txt in enumerate(texts):
                counts = {"alive": 0, "dead": 0, "open": 0}
                for align in range(n):
                    for ni, num in enumerate(nums):
                        st, chk = setting(txt, known, n, align, num, L)
                        counts[st] += 1
                        if t == 0 and st == "alive":
                            k4_alive.append({"n": n, "L": L, "align": align, "numbering": ni, "checks": chk})
                res.append(counts)
            table[f"{n}x{n} L={L}"] = {"k4": res[0], "controls_alive": [r["alive"] for r in res[1:]]}
    decided = {k: v for k, v in table.items() if v["k4"]["open"] < sum(v["k4"].values())}
    bounds = {"family": "Hill matrix with a periodic tableau key, either order (p = B c + u_kappa), sizes 2-4, key lengths 1-26",
              "by_size_and_key_length": table, "k4_alive": k4_alive[:30], "n_k4_alive": len(k4_alive),
              "controls": f"{N_CONTROLS} shuffled coppers (seed 116), identical test"}
    alive_ctl = [sum(v["controls_alive"][t] for v in table.values()) for t in range(N_CONTROLS)]
    open_k4 = sum(v["k4"]["open"] for v in table.values()); dead_k4 = sum(v["k4"]["dead"] for v in table.values())
    notes = (f"{len(table)} (size, key length) cells x alignments x 4 numberings. K4: alive {len(k4_alive)}, dead {dead_k4}, open "
             f"{open_k4}; controls alive {alive_ctl}. Largest key length with any decided setting per size: "
             + ", ".join(f"{n}x{n}: {max([int(k.split('L=')[1]) for k, v in table.items() if k.startswith(f'{n}x{n}') and v['k4']['dead'] + v['k4']['alive'] > 0] or [0])}" for n in (2, 3, 4)) + ".")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    I = {c: i for i, c in enumerate(STD)}
    lines = ["2x2 Hill with a key of length 4, blocks from place 1, letters A = 0: equations for row 1", "",
             "block places  carved  numbers   block class  known first letter"]
    for q in sorted(known):
        j = q - 1
        b, r = divmod(j, 2)
        if r == 0:
            s = 2 * b
            lines.append(f"{s + 1:>4}-{s + 2:<6}  {ct[s:s + 2]:>6}  {str([I[x] for x in ct[s:s + 2]]):<9} {s % 4:>11}  {known[q]} = {I[known[q]]}")
    lines += ["", "row 1: two matrix entries and one shift per block class (2 classes) against the equations above"]
    return "\n".join(lines)


def plant_check():
    """Planted p = B c + u_kappa texts (2x2 with L = 4, 3x3 with L = 6) must come out alive."""
    from kryptos.facts import KNOWN
    rng = random.Random(11)
    for n, L in ((2, 4), (3, 6)):
        while True:
            B = [[rng.randrange(26) for _ in range(n)] for _ in range(n)]
            if invertible(B):
                break
        U = {k: [rng.randrange(26) for _ in range(n)] for k in range(L)}
        ct = [rng.choice(STD) for _ in range(N)]
        pt = list(ct)
        for s in range(0, N - n + 1, n):
            cv = [STD.index(ct[s + k]) for k in range(n)]
            for r in range(n):
                pt[s + r] = STD[(sum(B[r][k] * cv[k] for k in range(n)) + U[s % L][r]) % 26]
        st, _ = setting("".join(ct), {q: pt[q - 1] for q in KNOWN}, n, 0, (STD, 0), L)
        if st != "alive":
            return False
    return True
