"""Experiment 0105. See program.md for the contract."""

EXPERIMENT = {
    "slug": "affine-hill-solved-letter-by-letter",
    "title": "Affine Hill ciphers of size 2 to 5, solved from every known letter, not only whole blocks",
    "family": "8-hill-polygraphic",
    "parent": "0015-hill-2x2-3x3-4x4-exact",
    "changed": "0015 and 0044 solved Hill matrices from whole crib blocks and used the partial blocks only as checks, which left the 4x4 affine case open (it needs five whole blocks). Written as decryption, p = B c + w, every known plaintext letter gives one linear equation in one row of B, because the carved block is always known. So each row of an n x n affine Hill is solved from all the known letters in that row position, partial blocks included, for n = 2 to 5.",
    "hypothesis_expert": (
        "Family 8 open item 'the 4x4 affine' (families.md); the HILL column of the tableau (C21, Bauer 2016-17). Model: "
        "blocks of n carved letters c (n = 2-5), message block p = B c + w mod 26, B invertible mod 26, w any vector "
        "(w = 0 is plain Hill). Row r of (B, w) has n + 1 unknowns; each block whose r-th message letter is known gives one "
        "equation. Solved exactly mod 2 and mod 13 (all solutions enumerated when a row is underdetermined, up to a cap) "
        "and joined by the Chinese remainder theorem; a setting survives if every row has a solution and some choice "
        "makes B invertible. Block alignments 0 to n-1 (the last partial block left plain); numberings: standard or "
        "KRYPTOS order, 0- or 1-based. Ten shuffled coppers."
    ),
    "hypothesis_eli5": (
        "A Hill cipher cuts the message into blocks of a few letters and mixes each block with a small table of "
        "numbers. Experiments 15 and 44 solved the table from blocks where all letters are known. Turning the method "
        "around, every single known letter gives one equation, even in a block that is only partly known. With that, "
        "even the 4-letter version with an extra shift, which had too few whole blocks before, can be solved exactly."
    ),
    "prediction": (
        "No setting with at least one check survives for n = 2-4, plain or affine; n = 5 affine has no checks (6 "
        "unknowns per row, about 5 equations) and is reported as untestable. Zero candidates."
    ),
    "method": (
        "1. For each n, alignment and numbering, group the known letters by block and row position. 2. For each row, "
        "solve the equations mod 2 and mod 13. 3. Join the rows, require B invertible mod 26, and count the spare "
        "equations (checks). 4. Decrypt survivors. 5. Repeat on ten shuffled coppers."
    ),
    "walkthrough": (
        "1. Cut the copper into blocks of 4 from place 1: OBKR, UOXO, and so on; place 22 is the second letter of block 6 (places 21-24, WFLR). "
        "2. Number the letters, A = 0 ... Z = 25. "
        "3. Place 22 holds E = 4, the second letter of its block, so row 2 of the table times the block's four numbers, plus shift 2, equals 4 mod 26. "
        "4. Every known letter in a block's second position gives such an equation for row 2: five unknowns, about six equations. "
        "5. Solve each row; if all rows have solutions and the table can be undone, the setting fits."
    ),
}

import random
from itertools import product
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
N_CONTROLS = 10
CAP = 200


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


def setting(ct, known, n, align, num, affine):
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
        blocks.setdefault(r, []).append(([idx[ct[start + k]] for k in range(n)], idx[ch]))
    nv = n + (1 if affine else 0)
    row_sols, checks = [], 0
    for r in range(n):
        eqs = blocks.get(r, [])
        rows = [cv + ([1] if affine else []) for cv, _ in eqs]
        rhs = [p for _, p in eqs]
        s2 = solve_mod_prime(rows, rhs, nv, 2); s13 = solve_mod_prime(rows, rhs, nv, 13)
        if s2 == [] or s13 == []:
            return "dead", 0, None
        if s2 is None or s13 is None:
            return "open", 0, None
        sols = [crt(x, y) for x in s2 for y in s13]
        if len(sols) > CAP:
            return "open", 0, None
        checks += max(0, len(eqs) - nv)
        row_sols.append(sols)
    total = 1
    for s in row_sols:
        total *= len(s)
    if total > 5000:
        return "open", checks, None
    for combo in product(*row_sols):
        B = [x[:n] for x in combo]
        if invertible(B):
            return "alive", checks, (B, [x[n] if affine else 0 for x in combo])
    return "dead", checks, None


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    rng = random.Random(105)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    assert plant_check()
    nums = [(STD, 0), (STD, 1), (KRY, 0), (KRY, 1)]
    table = {}
    k4_alive = []
    for n in range(2, 6):
        for affine in (False, True):
            key = f"{n}x{n} {'affine' if affine else 'plain'}"
            res = []
            for t, txt in enumerate(texts):
                counts = {"alive": 0, "dead": 0, "open": 0}
                for align in range(n):
                    for ni, num in enumerate(nums):
                        st, chk, sol = setting(txt, known, n, align, num, affine)
                        counts[st] += 1
                        if t == 0 and st == "alive":
                            k4_alive.append({"n": n, "affine": affine, "align": align, "numbering": ni, "checks": chk, "B": sol[0], "w": sol[1]})
                res.append(counts)
            table[key] = {"k4": res[0], "controls_alive": [r["alive"] for r in res[1:]], "controls_open": [r["open"] for r in res[1:]]}
    cands = []
    for s in k4_alive:
        if s["checks"] == 0:
            continue
        A, base = nums[s["numbering"]]
        idx = {c: (i + base) % 26 for i, c in enumerate(A)}
        n = s["n"]; out = list(ct)
        for start in range(s["align"], N - n + 1, n):
            cv = [idx[ct[start + k]] for k in range(n)]
            for r in range(n):
                v = (sum(s["B"][r][k] * cv[k] for k in range(n)) + s["w"][r]) % 26
                out[start + r] = A[(v - base) % 26]
        cands.append({"plaintext": "".join(out), "key": f"Hill {n}x{n} {'affine' if s['affine'] else 'plain'} align {s['align']} numbering {s['numbering']} B={s['B']} w={s['w']}"})
    bounds = {"family": "affine and plain Hill, sizes 2-5, every alignment, four numberings, solved row by row from every known letter",
              "by_size": table, "k4_alive": k4_alive[:20],
              "controls": f"{N_CONTROLS} shuffled coppers (seed 105), identical test"}
    notes = "; ".join(f"{k}: K4 {v['k4']}, controls alive {v['controls_alive']}" for k, v in table.items()) + f". K4 alive with checks: {len(cands)}."
    return {"candidates": cands, "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    I = {c: i for i, c in enumerate(STD)}
    lines = ["4x4 affine Hill, blocks from place 1, letters A = 0: equations for row 2 (the second letter of each block)", "",
             "block places  carved block  numbers          known second letter"]
    for q in sorted(known):
        j = q - 1
        b, r = divmod(j, 4)
        if r == 1:
            s = b * 4
            blk = ct[s:s + 4]
            lines.append(f"{s + 1:>4}-{s + 4:<6}  {blk:>12}  {str([I[x] for x in blk]):<16} {known[q]} = {I[known[q]]}")
    lines += ["", "row 2 has five unknowns (four table entries and a shift); each line above is one equation"]
    return "\n".join(lines)


def plant_check():
    """A planted affine Hill text (random invertible B, random w) must come out alive for n = 2-4."""
    from kryptos.facts import KNOWN
    rng = random.Random(7)
    for n in (2, 3, 4):
        while True:
            B = [[rng.randrange(26) for _ in range(n)] for _ in range(n)]
            if invertible(B):
                break
        w = [rng.randrange(26) for _ in range(n)]
        # build ciphertext: choose random carved blocks, plaintext = B c + w; force known letters by solving is hard,
        # so instead plant the cribs into the plaintext of a random copper decrypted with (B, w):
        ct = [rng.choice(STD) for _ in range(N)]
        pt = list(ct)
        for s in range(0, N - n + 1, n):
            cv = [STD.index(ct[s + k]) for k in range(n)]
            for r in range(n):
                pt[s + r] = STD[(sum(B[r][k] * cv[k] for k in range(n)) + w[r]) % 26]
        fake_known = {q: pt[q - 1] for q in KNOWN}
        st, chk, sol = setting("".join(ct), fake_known, n, 0, (STD, 0), True)
        if st != "alive":
            return False
    return True
