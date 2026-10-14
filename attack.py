"""Experiment 0015. See program.md for the contract."""

EXPERIMENT = {
    "slug": "hill-solved-from-crib-blocks",
    "title": "Hill ciphers 2x2, 3x3 and 4x4 solved straight from the crib blocks, with and without an added vector",
    "family": "8-hill-polygraphic",
    "parent": None,
    "changed": "New root in family 8. The matrix is solved from the known blocks by linear algebra mod 26 rather than searched; every numbering, block alignment and direction is covered, and the affine form Bauer left untested.",
    "hypothesis_expert": (
        "The HILL column and Bauer's conjecture (knowledge/sources/bauer-2017-unsolved-chapter-notes.md, C21 "
        "reading a): K4 is a Hill cipher. Bauer and Edkins exhausted 2x2 and 3x3 under six numberings by "
        "search; 4x4, the affine form C = MP + v, and shifted numberings are open. A crib run of 13 letters "
        "contains, for block size n and alignment o, several whole blocks; with n of them whose plaintext "
        "matrix is invertible mod 26, M = C P^-1 is determined, and any further block is a check with chance "
        "26^-n. For the affine form, block differences remove v and one more block is needed. Numberings: "
        "standard and KRYPTOS order, each 0-based and 1-based; both directions (the matrix encrypts or "
        "decrypts); alignments 0 to n-1. For every determined matrix the remaining crib blocks are checked, "
        "the text decrypted (the odd last letter left as is) and submitted if the cribs hold. 4x4 has four "
        "whole crib blocks at best, so it is determined with no check and must stand on the English of the "
        "rest; 4x4 affine needs five and is not determined here. Bounds: complete for the stated forms."
    ),
    "hypothesis_eli5": (
        "A Hill cipher turns letters into numbers, takes them two, three or four at a time, and mixes "
        "each group with a fixed table of numbers. The sculpture's grid has an extra L that spells HILL "
        "down one column, which some take as a hint. We know enough letters in a row that we can work the "
        "mixing table out directly, like solving simultaneous equations, instead of guessing it. If the "
        "table we work out from EASTNORTHEAST also turns the carved letters at 64 to 74 into BERLINCLOCK, "
        "it is real; if it does not, that kind of Hill cipher is out."
    ),
    "prediction": (
        "For 2x2 and 3x3, every numbering, alignment and direction gives a matrix from the first crib "
        "blocks that fails the remaining blocks, as Bauer found. The affine 2x2 and 3x3 forms fail the same "
        "way. For 4x4 a matrix exists for some settings with nothing left to check; its decryption of the "
        "other 73 letters is not English. Zero candidates pass."
    ),
    "method": (
        "1. For each numbering map letters to 0-25. 2. For each block size n, alignment o and direction, "
        "list the whole crib blocks and their ciphertext blocks. 3. Plain form: pick n blocks with an "
        "invertible plaintext matrix, solve M, check the rest. Affine form: use differences between blocks "
        "to solve M, then v from one block, check the rest. 4. Decrypt the text with the inverse map; submit "
        "if all 24 cribs hold. 5. Record, per setting, how many blocks were available and how many checks passed."
    ),
    "walkthrough": (
        "1. Number the letters A=0 to Z=25. 2. Take blocks of two starting at position 1, so 23-24 and "
        "25-26 are whole blocks inside EASTNORTHEAST: AS and TN, which are (0,18) and (19,13). 3. The carved "
        "letters there are LR and VQ: (11,17) and (21,16). 4. We want a 2x2 table M with M times (0,18) = "
        "(11,17) and M times (19,13) = (21,16), all mod 26. 5. Put the plaintext pairs side by side as a "
        "2x2 matrix, invert it mod 26 if its determinant is coprime to 26, and multiply: that is M. 6. Now "
        "test M on the next block, 27-28, OR, which must come out as the carved QP. 7. If it does not, this "
        "setting is dead. 8. Repeat for every numbering, every alignment and the other direction."
    ),
}

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
NUMBERINGS = {"std0": (STD, 0), "std1": (STD, 1), "kry0": (KRY, 0), "kry1": (KRY, 1)}


def num(ch, alpha, base):
    return (alpha.index(ch) + base) % 26


def let(v, alpha, base):
    return alpha[(v - base) % 26]


def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y


def inv26(a):
    g, x, _ = egcd(a % 26, 26)
    return None if g != 1 else x % 26


def det(M):
    n = len(M)
    if n == 1:
        return M[0][0] % 26
    if n == 2:
        return (M[0][0] * M[1][1] - M[0][1] * M[1][0]) % 26
    d = 0
    for j in range(n):
        minor = [row[:j] + row[j + 1:] for row in M[1:]]
        d += (-1) ** j * M[0][j] * det(minor)
    return d % 26


def inverse(M):
    n = len(M)
    di = inv26(det(M))
    if di is None:
        return None
    adj = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [row[:j] + row[j + 1:] for k, row in enumerate(M) if k != i]
            adj[j][i] = ((-1) ** (i + j) * (det(minor) if n > 1 else 1)) % 26
    return [[(adj[i][j] * di) % 26 for j in range(n)] for i in range(n)]


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) % 26 for j in range(len(B[0]))] for i in range(len(A))]


def solve_mod_p(rows, rhs, p):
    """Solve rows . x = rhs over GF(p). Returns (particular, nullspace basis) or None."""
    m, n = len(rows), len(rows[0])
    A = [[x % p for x in r] + [b % p] for r, b in zip(rows, rhs)]
    pivots = []
    r = 0
    for c in range(n):
        piv = next((i for i in range(r, m) if A[i][c] % p), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = pow(A[r][c], -1, p)
        A[r] = [(x * inv) % p for x in A[r]]
        for i in range(m):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [(x - f * y) % p for x, y in zip(A[i], A[r])]
        pivots.append(c); r += 1
        if r == m:
            break
    for i in range(r, m):
        if A[i][n] % p:
            return None
    free = [c for c in range(n) if c not in pivots]
    part = [0] * n
    for i, c in enumerate(pivots):
        part[c] = A[i][n]
    basis = []
    for fc in free:
        v = [0] * n; v[fc] = 1
        for i, c in enumerate(pivots):
            v[c] = (-A[i][fc]) % p
        basis.append(v)
    return part, basis


def all_solutions_mod_p(rows, rhs, p, cap):
    sol = solve_mod_p(rows, rhs, p)
    if sol is None:
        return []
    part, basis = sol
    out = []
    from itertools import product
    for coeffs in product(range(p), repeat=len(basis)):
        x = list(part)
        for cf, v in zip(coeffs, basis):
            if cf:
                x = [(a + cf * b) % p for a, b in zip(x, v)]
        out.append(x)
        if len(out) >= cap:
            break
    return out


def crt26(x13, x2):
    """Combine residues mod 13 and mod 2 into mod 26."""
    return [next(v for v in range(26) if v % 13 == a and v % 2 == b) for a, b in zip(x13, x2)]


def solve_rows(src, dst, n, affine, cap=4096):
    """All (M, v) with M src_k + v = dst_k for every block k, enumerated row by row and combined."""
    per_row = []
    for r in range(n):
        rows = [list(sv) + ([1] if affine else []) for sv in src]
        rhs = [dv[r] for dv in dst]
        s13 = all_solutions_mod_p(rows, rhs, 13, cap)
        s2 = all_solutions_mod_p(rows, rhs, 2, cap)
        if not s13 or not s2:
            return []
        combined = [crt26(a, b) for a in s13 for b in s2][:cap]
        per_row.append(combined)
    from itertools import product
    out = []
    for choice in product(*per_row):
        M = [c[:n] for c in choice]
        v = [c[n] for c in choice] if affine else None
        out.append((M, v))
        if len(out) >= cap:
            break
    return out


def cols(blocks):
    """Blocks (lists of n ints) as an n x n matrix with blocks as columns."""
    n = len(blocks[0])
    return [[blocks[j][i] for j in range(len(blocks))] for i in range(n)]


def apply(M, v, add=None):
    out = [sum(M[i][k] * v[k] for k in range(len(v))) % 26 for i in range(len(M))]
    if add:
        out = [(o + a) % 26 for o, a in zip(out, add)]
    return out


def encrypt(plaintext, key):
    alpha, base = NUMBERINGS[key["numbering"]]
    n, o, M, v, direction = key["n"], key["offset"], key["M"], key.get("v"), key["direction"]
    # direction "enc": C = M P + v; "dec": P = M C + v, so encryption uses the inverse
    if direction == "enc":
        Menc, venc = M, v
    else:
        Minv = inverse(M)
        Menc = Minv
        venc = [(-x) % 26 for x in apply(Minv, v)] if v else None
    out = list(plaintext)
    i = o
    while i + n <= N:
        blk = [num(plaintext[j], alpha, base) for j in range(i, i + n)]
        c = apply(Menc, blk, venc)
        for j in range(n):
            out[i + j] = let(c[j], alpha, base)
        i += n
    return "".join(out)


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    candidates, log = [], []
    n_settings = 0
    for nname, (alpha, base) in NUMBERINGS.items():
        for n in (2, 3, 4):
            for o in range(n):
                blocks = []  # (plain block ints, cipher block ints, start pos)
                i = o
                while i + n <= N:
                    if all((i + j + 1) in known for j in range(n)):
                        blocks.append(([num(known[i + j + 1], alpha, base) for j in range(n)],
                                       [num(ct[i + j], alpha, base) for j in range(n)], i + 1))
                    i += n
                for direction in ("enc", "dec"):
                    # in "enc" the unknown M maps plain -> cipher; in "dec" it maps cipher -> plain
                    src = [b[0] if direction == "enc" else b[1] for b in blocks]
                    dst = [b[1] if direction == "enc" else b[0] for b in blocks]
                    for affine in (False, True):
                        n_settings += 1
                        need = n + (1 if affine else 0)
                        rec = {"numbering": nname, "n": n, "offset": o, "direction": direction, "affine": affine,
                               "crib_blocks": len(blocks), "solved": False, "checks": 0, "checks_passed": 0}
                        if len(blocks) < need:
                            rec["note"] = "too few whole crib blocks"; log.append(rec); continue
                        sols = solve_rows(src, dst, n, affine)
                        if not sols:
                            rec["note"] = "inconsistent on the crib blocks"; log.append(rec); continue
                        rec["solved"] = True; rec["solutions"] = len(sols)
                        # keep decryptable solutions; prefer the first few
                        kept = 0
                        for M, v in sols:
                            Mdec, vdec = (M, v) if direction == "dec" else (None, None)
                            if direction == "enc":
                                Minv = inverse(M)
                                if Minv is None:
                                    continue
                                Mdec = Minv; vdec = [(-x) % 26 for x in apply(Minv, v)] if v else None
                            elif inverse(M) is None:
                                continue
                            pt = list(ct); i = o
                            while i + n <= N:
                                blk = [num(ct[j], alpha, base) for j in range(i, i + n)]
                                pp = apply(Mdec, blk, vdec)
                                for j in range(n):
                                    pt[i + j] = let(pp[j], alpha, base)
                                i += n
                            pt = "".join(pt)
                            key = {"numbering": nname, "n": n, "offset": o, "M": M, "v": v, "direction": direction}
                            rec.setdefault("english", []).append(round(ctx.english_score(pt), 3))
                            candidates.append({"plaintext": pt, "key": key, "key_bits": 4.7 * n * n + (4.7 * n if affine else 0),
                                               "key_description": f"Hill {n}x{n}{' affine' if affine else ''} {nname} offset {o} {direction}; M={M}{' v=' + str(v) if v else ''}",
                                               "notes": f"{len(blocks)} crib blocks all consistent; {len(sols)} solutions in this setting"})
                            kept += 1
                            if kept >= 8:
                                break
                        rec["checks"] = len(blocks); rec["checks_passed"] = len(blocks)
                        log.append(rec)
                        continue
    consistent = [r for r in log if r["solved"] and r["checks"] == r["checks_passed"]]
    return {
        "candidates": candidates[:50],
        "bounds": {"family": "Hill cipher, block sizes 2-4, plain and affine, solved from crib blocks",
                   "numberings": list(NUMBERINGS), "alignments": "0..n-1", "directions": ["enc", "dec"],
                   "settings": n_settings, "settings_solved": sum(1 for r in log if r["solved"]),
                   "settings_consistent_on_all_crib_blocks": [{k: r[k] for k in ("numbering", "n", "offset", "direction", "affine", "crib_blocks", "solutions", "english") if k in r} for r in consistent],
                   "settings_inconsistent": sum(1 for r in log if not r["solved"] and r.get("note") == "inconsistent on the crib blocks"),
                   "log": log},
        "notes": f"{n_settings} settings; {len(consistent)} consistent with every whole crib block; {len(candidates)} decryptions submitted.",
    }


def worked_example(ctx, key):
    alpha, base = STD, 0
    lines = ["2x2, standard numbering A=0, blocks from position 1, matrix encrypts: solve from blocks 23-24 and 25-26", ""]
    P = [[num(ctx.KNOWN[p], alpha, base) for p in (23, 24)], [num(ctx.KNOWN[p], alpha, base) for p in (25, 26)]]
    C = [[num(ctx.K4[p - 1], alpha, base) for p in (23, 24)], [num(ctx.K4[p - 1], alpha, base) for p in (25, 26)]]
    lines.append(f"plain blocks  AS={P[0]}  TN={P[1]};  cipher blocks  {ctx.K4[22:24]}={C[0]}  {ctx.K4[24:26]}={C[1]}")
    Pm = cols(P); Pi = inverse(Pm)
    if Pi is None:
        lines.append(f"plaintext matrix {Pm} has determinant {det(Pm)}, not invertible mod 26: use another pair of blocks")
    else:
        M = matmul(cols(C), Pi)
        lines.append(f"M = C P^-1 = {M}")
        nxt = [num(ctx.KNOWN[p], alpha, base) for p in (27, 28)]
        lines.append(f"check on block 27-28 OR={nxt}: M OR = {apply(M, nxt)} vs carved {ctx.K4[26:28]}={[num(ctx.K4[p-1], alpha, base) for p in (27, 28)]}")
    return "\n".join(lines)
