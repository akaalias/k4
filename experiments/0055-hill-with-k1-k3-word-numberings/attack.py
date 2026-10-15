"""Experiment 0055. See program.md for the contract."""

EXPERIMENT = {
    "slug": "hill-with-k1-k3-word-numberings",
    "title": "Hill again, with the letters numbered by alphabets built from the solved messages' words",
    "family": "8-hill-polygraphic",
    "parent": "0044-hill-with-keyword-numberings",
    "changed": "Experiment 44 numbered the letters by alphabets built from the puzzle's vocabulary. Here the numberings come from every word of the three solved messages and from the words of Sanborn's 2025 letter, 0-based and 1-based, with the same exact solver.",
    "hypothesis_expert": (
        "Hill cipher (C21), block sizes 2-4, plain and affine, matrix encrypting or decrypting, every "
        "alignment, solved exactly from the whole crib blocks by the mod-13 and mod-2 solver of 0044 and "
        "tested on the partial-block cribs. The variable is the numbering: A=0 and A=1 on the keyword mixing "
        "of every K1-K3 plaintext word with three or more distinct letters and of EGYPT, CAIRO, LUXOR, WALL, "
        "NOVEMBER, MESSAGE, DELIVER, DELIVERING, TRANSMIT (C7, C13, C14), skipping alphabets already covered "
        "by 0015 and 0044. Bounds: complete for these numberings and forms."
    ),
    "hypothesis_eli5": (
        "A Hill cipher turns letters into numbers, mixes them in small groups with a table of numbers, and "
        "turns them back into letters. The answer depends on which number each letter gets, which depends "
        "on the order of the alphabet. Experiment 44 tried orders built from the puzzle's word list; this "
        "one tries orders built from every word of the solved messages. As before, the mixing table is "
        "worked out directly from the groups of known letters and then checked on the rest."
    ),
    "prediction": (
        "Every 2x2 and 3x3 setting is inconsistent on its whole crib blocks; some 4x4 settings are "
        "consistent with no check to spare and all of them fail the partial-block cribs. Zero candidates "
        "pass the gates."
    ),
    "method": (
        "1. Build the numberings from the new word pool, 0-based and 1-based. 2. For each block size, alignment "
        "and direction, list the whole crib blocks. 3. Solve plain and affine forms exactly; reject on "
        "inconsistency. 4. Decrypt with each solution and submit; the gates test the partial-block cribs. "
        "5. Record per setting how many blocks were available and whether they agreed."
    ),
    "walkthrough": (
        "1. Build the alphabet from SHADING: SHADINGBCEFJKLMOPQRTUVWXYZ, and number it S=0, H=1 and on. "
        "2. Take blocks of two from place 1, so places 23-24 (AS) and 25-26 (TN) are whole blocks of known "
        "letters. 3. In this numbering AS is (2,0) and TN is (19,5). 4. The carved letters there are LR and "
        "VQ: (13,18) and (21,17). 5. Find the 2x2 table M that sends (2,0) to (13,18) and (19,5) to (21,17), "
        "modulo 26. 6. Test M on places 27-28, OR, which must become the carved QP. 7. If not, this numbering "
        "and alignment are dead. 8. Repeat for every numbering, alignment and direction."
    ),
}

from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
from kryptos.alphabets import keyword_mixed
from kryptos.facts import load_vocabulary


SPACED = (
    "BETWEEN SUBTLE SHADING AND THE ABSENCE OF LIGHT LIES THE NUANCE OF IQLUSION "
    "IT WAS TOTALLY INVISIBLE HOWS THAT POSSIBLE THEY USED THE EARTHS MAGNETIC FIELD X THE INFORMATION WAS GATHERED AND "
    "TRANSMITTED UNDERGRUUND TO AN UNKNOWN LOCATION X DOES LANGLEY KNOW ABOUT THIS THEY SHOULD ITS BURIED OUT THERE "
    "SOMEWHERE X WHO KNOWS THE EXACT LOCATION ONLY WW THIS WAS HIS LAST MESSAGE X THIRTY EIGHT DEGREES FIFTY SEVEN "
    "MINUTES SIX POINT FIVE SECONDS NORTH SEVENTY SEVEN DEGREES EIGHT MINUTES FORTY FOUR SECONDS WEST ID BY ROWS "
    "SLOWLY DESPARATLY SLOWLY THE REMAINS OF PASSAGE DEBRIS THAT ENCUMBERED THE LOWER PART OF THE DOORWAY WAS REMOVED "
    "WITH TREMBLING HANDS I MADE A TINY BREACH IN THE UPPER LEFT HAND CORNER AND THEN WIDENING THE HOLE A LITTLE I "
    "INSERTED THE CANDLE AND PEERED IN THE HOT AIR ESCAPING FROM THE CHAMBER CAUSED THE FLAME TO FLICKER BUT PRESENTLY "
    "DETAILS OF THE ROOM WITHIN EMERGED FROM THE MIST X CAN YOU SEE ANYTHING Q"
)
EXTRA = ["EGYPT", "CAIRO", "LUXOR", "WALL", "NOVEMBER", "MESSAGE", "DELIVER", "DELIVERING", "TRANSMIT"]
def _numberings():
    covered = {STD, KRY} | {keyword_mixed(w) for w in load_vocabulary() if len(set(w)) >= 3}
    words = sorted({w for w in SPACED.split() if len(set(w)) >= 3} | set(EXTRA))
    out, seen = {}, set(covered)
    for w in words:
        A = keyword_mixed(w)
        if A in seen:
            continue
        seen.add(A)
        out[f"{w}0"] = (A, 0); out[f"{w}1"] = (A, 1)
    return out


NUMBERINGS = _numberings()


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
                   "settings_consistent_on_all_crib_blocks": [{k: r[k] for k in ("numbering", "n", "offset", "direction", "affine", "crib_blocks", "solutions", "english") if k in r} for r in consistent][:40],
                   "settings_inconsistent": sum(1 for r in log if not r["solved"] and r.get("note") == "inconsistent on the crib blocks"),
                   "log_size": len(log), "numberings_count": len(NUMBERINGS)},
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
