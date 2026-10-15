"""Experiment 0031. See program.md for the contract."""

EXPERIMENT = {
    "slug": "copper-off-by-one-autokey-and-two-words",
    "title": "The copper off by one letter: the chained autokey and the two-word tests rerun with a letter dropped or added anywhere",
    "family": "1-keyed-periodic",
    "parent": "0012-plaintext-autokey-chained-from-cribs",
    "changed": "The one-letter-error parameter applied to two exact tests at once. The carved text is taken with one letter deleted at each of 97 positions or one unknown letter inserted at each of 98, and the chained plaintext autokey (0012) and the two-word linear test (0014, total length up to 20) run on every variant.",
    "hypothesis_expert": (
        "K2 was carved with a letter dropped, and Sanborn has said 97, 98 and 100 in the same breath (C17, "
        "C18, family G). 0009 applied the parameter to the stretch scores only. The two tests most able to "
        "decide a family exactly are the chained plaintext autokey, where every crib forces letters up and "
        "down the chain, and the two-word composition, where 24 equations fall on a + b unknowns. Each runs "
        "here on 195 variants under the 24 conventions (autokey) and the standard and KRYPTOS alphabets "
        "with both signs (two words). An inserted unknown letter breaks the autokey chain where it sits and "
        "drops the equation at its position; a deleted letter shifts every later position by one. "
        "Convention: crib positions are kept as given in the variant's own numbering, since Sanborn's "
        "positions refer to the carved text. Bounds: complete for one insertion or deletion anywhere."
    ),
    "hypothesis_eli5": (
        "The second message on the sculpture was carved with one letter missing, and the artist has been "
        "vague about whether the fourth has 97 or 98 letters. So we redo the two sharpest tests from "
        "yesterday on every version of the text that has one letter removed, or one unknown letter slipped "
        "in, at every possible place. If a single carving slip was hiding the method, one of these versions "
        "would suddenly chain together or solve."
    ),
    "prediction": (
        "No variant makes the autokey chain consistent at any lag up to 25, and no variant makes a word pair "
        "of total length up to 20 consistent. Larger closures and longer pairs behave as on the carved text. "
        "Zero candidates pass."
    ),
    "method": (
        "1. Build the 195 variants. 2. Autokey: for each variant, lag and convention, chain forced letters "
        "from the cribs, treating an inserted unknown as a wall; reject on conflict; record consistent lags. "
        "3. Two words: for each variant, alphabet pair, sign and length pair with a + b <= 20, solve the crib "
        "equations by weighted union-find; record consistent pairs. 4. Submit fully forced autokey texts "
        "and vocabulary word matches."
    ),
    "walkthrough": (
        "1. Suppose the carver dropped a letter right after position 40. Then the carved letters from 41 on "
        "are one place early: the true position 65 is the carved 64, and so on. 2. Take lag 13 and the "
        "sculpture's alphabet with Vigenere. 3. Position 22 (E) is keyed by position 9, and in turn keys "
        "position 35, exactly as before, because the slip is after 40. 4. But position 64 (B) is now keyed "
        "by the true position 51, which is the carved 50, and keys the true 77, the carved 76. 5. Chain "
        "every known letter through its lag with the corrected numbering and see whether the chain closes "
        "without contradiction. 6. Repeat for a slip at every position, and for an extra letter at every position."
    ),
}

from math import lcm
from kryptos.alphabets import ALPHABETS, conventions, key_letter_for, decrypt_letter, encrypt_letter
from kryptos.facts import load_k1, load_k2, load_k3

N = 97
DEAD_PERIODS = set(range(1, 27)) | set(range(30, 53))


def letters(s):
    return "".join(c for c in s if "A" <= c <= "Z")


def variants(ct):
    yield "carved", ct
    for i in range(len(ct)):
        yield f"deleted {i+1}", ct[:i] + ct[i + 1:]
    for i in range(len(ct) + 1):
        yield f"inserted before {i+1}", ct[:i] + "-" + ct[i:]


def encrypt(plaintext, key):
    pa, ca, ka, m = key["pa"], key["ca"], key["ka"], key["m"]
    if key["kind"] == "autokey":
        L, primer = key["lag"], key["primer"]
        return "".join(encrypt_letter(p, primer[i] if i < L else plaintext[i - L], pa, ca, ka, m) for i, p in enumerate(plaintext))
    raise NotImplementedError


def closure(ct, known, L, conv):
    n = len(ct)
    pa, ca, ka, m = conv
    forced = {pos - 1: p for pos, p in known.items() if pos - 1 < n and ct[pos - 1] != "-"}
    queue = list(forced)
    while queue:
        i = queue.pop()
        p = forced[i]
        if i - L >= 0 and ct[i] != "-":
            k = key_letter_for(p, ct[i], pa, ca, ka, m); j = i - L
            if ct[j] != "-":
                if j in forced:
                    if forced[j] != k: return False, forced
                else:
                    forced[j] = k; queue.append(j)
        if i + L < n and ct[i + L] != "-":
            q = decrypt_letter(ct[i + L], p, pa, ca, ka, m); j = i + L
            if j in forced:
                if forced[j] != q: return False, forced
            else:
                forced[j] = q; queue.append(j)
    return True, forced


class WUF:
    def __init__(self, n):
        self.p = list(range(n)); self.w = [0] * n
    def find(self, x):
        if self.p[x] == x: return x, 0
        r, wr = self.find(self.p[x]); self.w[x] = (self.w[x] + wr) % 26; self.p[x] = r
        return r, self.w[x]
    def union(self, x, y, d):
        rx, wx = self.find(x); ry, wy = self.find(y)
        if rx == ry: return (wx - wy) % 26 == d % 26
        self.p[rx] = ry; self.w[rx] = (d - wx + wy) % 26
        return True


def two_words(ct, known, pairs):
    """Consistent (a, b, pa, ca, sign, s) cases on this variant."""
    out = []
    for pa in ("std", "kry"):
        for ca in ("std", "kry"):
            for psign in ("vig", "beau"):
                t = {pos: ALPHABETS["std"].index(key_letter_for(known[pos], ct[pos - 1], pa, ca, "std", psign)) for pos in known if pos - 1 < len(ct) and ct[pos - 1] != "-"}
                for a, b in pairs:
                    for s in (1, -1):
                        uf = WUF(a + b); ok = True
                        for pos, tv in t.items():
                            i = pos - 1
                            if not uf.union(i % a, a + (i % b), tv):
                                ok = False; break
                        if ok:
                            out.append((a, b, pa, ca, psign, s))
    return out


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    convs = list(conventions())
    pairs = [(a, b) for a in range(2, 19) for b in range(a + 1, 19) if a + b <= 20 and lcm(a, b) not in DEAD_PERIODS]
    auto_consistent = {}     # variant -> consistent lags <= 25
    auto_full = []
    tw_consistent = []
    n_var = 0
    for vname, c in variants(ct):
        n_var += 1
        lags = []
        for L in range(1, 26):
            for conv in convs:
                ok, forced = closure(c, known, L, conv)
                if ok:
                    lags.append((L, "/".join(conv), len(forced)))
                    if len(forced) == len(c) and "-" not in c:
                        pa, ca, ka, m = conv
                        pt = "".join(forced[i] for i in range(len(c)))
                        primer = "".join(key_letter_for(pt[i], c[i], pa, ca, ka, m) for i in range(L))
                        auto_full.append({"plaintext": pt, "key": {"kind": "autokey", "lag": L, "primer": primer, "pa": pa, "ca": ca, "ka": ka, "m": m},
                                          "key_bits": 4.7 * L, "key_description": f"{vname}; autokey lag {L} primer {primer}; {pa}/{ca}/{ka} {m}"})
        if lags:
            auto_consistent[vname] = lags[:10]
        for case in two_words(c, known, pairs):
            tw_consistent.append((vname,) + case)
        if ctx.time_left() < 60:
            break
    return {
        "candidates": auto_full[:50],
        "bounds": {"family": "one-letter error (insert or delete anywhere) x chained plaintext autokey lags 1-25 x two words a + b <= 20",
                   "variants": n_var, "conventions": 24, "two_word_pairs": len(pairs),
                   "autokey_variants_with_a_consistent_lag": len(auto_consistent),
                   "autokey_consistent_cases": {k: v for k, v in list(auto_consistent.items())[:20]},
                   "autokey_fully_forced": len(auto_full),
                   "two_word_consistent_cases": [{"variant": v, "a": a, "b": b, "plain": pa, "cipher": ca, "plain_sign": ps, "s": s} for v, a, b, pa, ca, ps, s in tw_consistent[:40]],
                   "n_two_word_consistent": len(tw_consistent)},
        "notes": f"{n_var} variants. Autokey lags 1-25: {len(auto_consistent)} variants have a consistent lag, {len(auto_full)} fully forced (97-letter variants only). Two words with a + b <= 20: {len(tw_consistent)} consistent cases.",
    }


def worked_example(ctx, key):
    c = ctx.K4[:40] + ctx.K4[41:]
    lines = ["variant: the carved letter at 41 deleted; lag 13; KRYPTOS alphabet throughout, Vigenere", ""]
    ok, forced = closure(c, ctx.KNOWN, 13, ("kry", "kry", "kry", "vig"))
    lines.append(f"chain from the cribs {'closes' if ok else 'breaks'} after forcing {len(forced)} letters")
    lines.append("".join(forced.get(i, ".") for i in range(len(c))))
    return "\n".join(lines)
