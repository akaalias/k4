"""Experiment 0036. See program.md for the contract."""

EXPERIMENT = {
    "slug": "hill-variants-chained-and-paired",
    "title": "The Hill variants Bauer left open: blocks chained to their neighbours, and two matrices taking turns",
    "family": "8-hill-polygraphic",
    "parent": "0015-hill-solved-from-crib-blocks",
    "changed": "Four variants of the Hill cipher instead of the plain and affine forms: each block also adds the previous carved block, or the previous message block, or is mixed together with it, or alternates between two matrices. The exact solver of experiment 15 handles every one.",
    "hypothesis_expert": (
        "Bauer (knowledge/sources/bauer-2017-unsolved-chapter-notes.md, C21) lists chaining and paired 2x2 "
        "matrices as untested Hill variants. Chained forms: c_i = M p_i + c_(i-1) (ciphertext feedback), "
        "c_i = M p_i + p_(i-1) (plaintext feedback), c_i = M (p_i + p_(i-1)) (summed input), with the "
        "first block's predecessor taken as zeros. Paired form: M_A on even blocks, M_B on odd. Each is "
        "linear in the matrix given the known blocks, since the previous carved block is always known and "
        "the previous message block is known inside a crib run, so the whole crib blocks give rows of "
        "equations and the exact mod-13 and mod-2 solver of experiment 15 enumerates every matrix. "
        "Block sizes 2-4, four numberings, every alignment, matrix encrypting or decrypting. A matrix "
        "consistent with all its blocks decrypts the text and the partial-block cribs test it. Bounds: "
        "complete for these four variants under the stated settings."
    ),
    "hypothesis_eli5": (
        "Experiment 15 ruled out the plain Hill cipher, where every group of letters is mixed by the same "
        "table of numbers on its own. A cryptologist who studied the sculpture listed the variants nobody "
        "had tried: mixing each group together with the group before it, or using two tables that take "
        "turns. Because the carved letters are all known, and the known message letters come in two long "
        "runs, each variant can be solved directly from the known groups rather than guessed."
    ),
    "prediction": (
        "No variant, size, numbering, alignment or direction gives a matrix consistent with all its whole "
        "crib blocks that also reproduces the known letters in partial blocks. Zero candidates pass."
    ),
    "method": (
        "1. For each numbering, block size, alignment and variant, list the whole crib blocks and their "
        "partners (previous carved block or previous message block). 2. Build the linear rows for the "
        "matrix, in each direction. 3. Enumerate all solutions mod 26 by elimination mod 13 and mod 2. "
        "4. Decrypt the text with each invertible solution and count known letters right. 5. Submit any "
        "decryption with all 24."
    ),
    "walkthrough": (
        "1. Number the letters A=0 to Z=25, blocks of two from position 1. 2. Ciphertext feedback: the "
        "carved pair at 25-26 equals M times the message pair at 25-26 plus the carved pair at 23-24. "
        "3. Subtract the carved 23-24 from the carved 25-26: that difference is M times TN. 4. Do the same "
        "for the next whole pairs inside EASTNORTHEAST and BERLINCLOCK: six equations in four unknowns. "
        "5. Solve; if no M fits all of them, this setting is dead. 6. For two matrices taking turns, split "
        "the pairs into even and odd and solve each separately."
    ),
}

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
NUMBERINGS = {"std0": (STD, 0), "std1": (STD, 1), "kry0": (KRY, 0), "kry1": (KRY, 1)}
VARIANTS = ("chain-c", "chain-p", "sum-p", "paired")


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




def apply(M, v, add=None):
    out = [sum(M[i][k] * v[k] for k in range(len(v))) % 26 for i in range(len(M))]
    if add:
        out = [(o + a) % 26 for o, a in zip(out, add)]
    return out


def vsub(a, b):
    return [(x - y) % 26 for x, y in zip(a, b)]


def vadd(a, b):
    return [(x + y) % 26 for x, y in zip(a, b)]


def blocks_of(text, n, o, alpha, base):
    """Whole blocks from offset o as lists of ints; index -> (start, ints)."""
    out = []
    i = o
    while i + n <= N:
        out.append((i, [num(text[j], alpha, base) for j in range(i, i + n)]))
        i += n
    return out


def encrypt(plaintext, key):
    alpha, base = NUMBERINGS[key["numbering"]]
    n, o, variant = key["n"], key["offset"], key["variant"]
    Ms = key["M"] if variant == "paired" else [key["M"]]
    out = list(plaintext)
    prev_c = [0] * n; prev_p = [0] * n
    for k, (s, p) in enumerate(blocks_of(plaintext, n, o, alpha, base)):
        M = Ms[k % len(Ms)]
        if variant == "chain-c":
            c = vadd(apply(M, p), prev_c)
        elif variant == "chain-p":
            c = vadd(apply(M, p), prev_p)
        elif variant == "sum-p":
            c = apply(M, vadd(p, prev_p))
        else:
            c = apply(M, p)
        for j in range(n):
            out[s + j] = let(c[j], alpha, base)
        prev_c, prev_p = c, p
    return "".join(out)


def decrypt_with(ct, Minvs, n, o, variant, alpha, base):
    out = list(ct)
    prev_c = [0] * n; prev_p = [0] * n
    for k, (s, c) in enumerate(blocks_of(ct, n, o, alpha, base)):
        Mi = Minvs[k % len(Minvs)]
        if variant == "chain-c":
            p = apply(Mi, vsub(c, prev_c))
        elif variant == "chain-p":
            p = apply(Mi, vsub(c, prev_p))
        elif variant == "sum-p":
            p = vsub(apply(Mi, c), prev_p)
        else:
            p = apply(Mi, c)
        for j in range(n):
            out[s + j] = let(p[j], alpha, base)
        prev_c, prev_p = c, p
    return "".join(out)


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    candidates, log = [], []
    n_settings = 0
    for nname, (alpha, base) in NUMBERINGS.items():
        for n in (2, 3, 4):
            for o in range(n):
                cblocks = blocks_of(ct, n, o, alpha, base)
                # whole crib blocks with their index k
                crib_k = [k for k, (s, _) in enumerate(cblocks) if all((s + j + 1) in known for j in range(n))]
                pblock = {k: [num(known[cblocks[k][0] + j + 1], alpha, base) for j in range(n)] for k in crib_k}
                for variant in VARIANTS:
                    n_settings += 1
                    rec = {"numbering": nname, "n": n, "offset": o, "variant": variant, "crib_blocks": len(crib_k), "solved": False}
                    # rows: M x src = dst, grouped by matrix index (paired: 2 groups)
                    groups = {0: ([], []), 1: ([], [])} if variant == "paired" else {0: ([], [])}
                    for k in crib_k:
                        c = cblocks[k][1]
                        if variant == "chain-c":
                            prev = cblocks[k - 1][1] if k > 0 else [0] * n
                            src, dst = pblock[k], vsub(c, prev)
                        elif variant == "chain-p":
                            if k == 0:
                                prevp = [0] * n
                            elif (k - 1) in pblock:
                                prevp = pblock[k - 1]
                            else:
                                continue
                            src, dst = pblock[k], vsub(c, prevp)
                        elif variant == "sum-p":
                            if k == 0:
                                prevp = [0] * n
                            elif (k - 1) in pblock:
                                prevp = pblock[k - 1]
                            else:
                                continue
                            src, dst = vadd(pblock[k], prevp), c
                        else:
                            src, dst = pblock[k], c
                        g = (k % 2) if variant == "paired" else 0
                        groups[g][0].append(src); groups[g][1].append(dst)
                    need = n
                    if any(len(groups[g][0]) < need for g in groups):
                        rec["note"] = "too few usable crib blocks"; log.append(rec); continue
                    sols = {}
                    ok = True
                    for g in groups:
                        s_ = solve_rows(groups[g][0], groups[g][1], n, False, cap=512)
                        if not s_:
                            ok = False; break
                        sols[g] = [M for M, _ in s_ if inverse(M) is not None][:64]
                        if not sols[g]:
                            ok = False; break
                    if not ok:
                        rec["note"] = "inconsistent or singular"; log.append(rec); continue
                    rec["solved"] = True
                    rec["solutions"] = {str(g): len(v) for g, v in sols.items()}
                    best_hits = 0
                    from itertools import product
                    for combo in product(*[sols[g] for g in sorted(sols)]):
                        Minvs = [inverse(M) for M in combo]
                        pt = decrypt_with(ct, Minvs, n, o, variant, alpha, base)
                        hits = sum(1 for pos, ch in known.items() if pt[pos - 1] == ch)
                        best_hits = max(best_hits, hits)
                        if hits == 24:
                            key = {"numbering": nname, "n": n, "offset": o, "variant": variant, "M": list(combo) if variant == "paired" else combo[0]}
                            candidates.append({"plaintext": pt, "key": key, "key_bits": 4.7 * n * n * len(combo), "key_description": f"Hill {variant} {n}x{n} {nname} offset {o}; M={combo}"})
                    rec["best_hits"] = best_hits
                    log.append(rec)
    solved = [r for r in log if r["solved"]]
    return {
        "candidates": candidates[:50],
        "bounds": {"family": "Hill variants: ciphertext feedback, plaintext feedback, summed input, paired matrices; sizes 2-4", "numberings": list(NUMBERINGS),
                   "settings": n_settings, "settings_solved": len(solved),
                   "solved_settings": [{k: r[k] for k in ("numbering", "n", "offset", "variant", "crib_blocks", "solutions", "best_hits")} for r in solved[:30]],
                   "best_hits_over_solved": max((r["best_hits"] for r in solved), default=0)},
        "notes": f"{n_settings} settings; {len(solved)} consistent on their whole crib blocks; best known-letter count among them {max((r['best_hits'] for r in solved), default=0)} of 24; {len(candidates)} full hits.",
    }


def worked_example(ctx, key):
    alpha, base = STD, 0
    cb = blocks_of(ctx.K4, 2, 0, alpha, base)
    lines = ["ciphertext feedback, blocks of two from position 1, A=0: the equation for the pair at 25-26", ""]
    k = 12   # block index of positions 25-26
    c, prev = cb[k][1], cb[k - 1][1]
    lines.append(f"carved 25-26 {ctx.K4[24:26]} = {c};  carved 23-24 {ctx.K4[22:24]} = {prev};  difference {vsub(c, prev)}")
    lines.append(f"message 25-26 TN = {[num('T', alpha, base), num('N', alpha, base)]}")
    lines.append(f"so M x (19, 13) = {tuple(vsub(c, prev))} mod 26; the pairs 27-28, 29-30, 31-32 and 33-34 give four more such equations.")
    return "\n".join(lines)
