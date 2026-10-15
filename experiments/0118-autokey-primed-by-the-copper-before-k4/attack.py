"""Experiment 0118. See program.md for the contract."""

EXPERIMENT = {
    "slug": "autokey-primed-by-the-copper-before-k4",
    "title": "Ciphertext autokey that runs on from K3: the key is the carved letter some distance back, K3's letters included",
    "family": "1-keyed-periodic",
    "parent": "0002-ciphertext-autokey",
    "changed": "0002 tested ciphertext autokey with the first key letters free, so known places within one lag of the start gave no check. On the copper K4 is not a separate text: it runs on from K3 on the same plate. Here the key for place i is the carved letter lag places earlier in the whole carved stream (K1, K2, K3 and the ? as carved), so every known place is a check, for every lag 1-200; and the geometric version, the letter carved directly above on the previous plate line, and two lines above.",
    "hypothesis_expert": (
        "C7 ('it will come back to the first part'; earlier text holds instructions), C3(a) (the carved plate as the "
        "grid), C11a (NSA 1992: autokey). Model: c_i = E(p_i, x_{i-lag}) where x is the carved stream K1+K2+K3+?+K4 as on "
        "the copper (with or without the ? characters, which can carry no key value and are skipped in one variant), lag "
        "1-200; 12 conventions (Vigenere, Beaufort, variant; plain and cipher alphabets standard or KRYPTOS; key letters on "
        "the cipher alphabet). Geometric variant: the key for a K4 letter is the letter in the same column of the line "
        "above (or two above) on the lower-left plate, columns counted from the left and from the right. Every known "
        "place gives a check: 24 per setting. Ten shuffled coppers (K4 shuffled, the earlier text fixed)."
    ),
    "hypothesis_eli5": (
        "In a self-feeding key, each letter is locked with a letter that was already carved some distance before. "
        "Experiment 2 tried this starting fresh at K4. But on the sculpture K4 just continues the lines of K3, so the "
        "first letters of K4 could take their key from K3's letters. We try every distance, and also the letter carved "
        "straight above on the line before, against all 24 known letters."
    ),
    "prediction": "No lag or geometric reading matches more than 6 of 24 known letters; same as the coppers. Zero candidates.",
    "method": (
        "1. Build the carved stream before K4 from the plates. 2. For each lag, rule and stream variant, decrypt the 24 "
        "known places with the stream letter lag places back and count matches. 3. Do the same for the letter above on "
        "the plate. 4. Repeat on ten shuffled coppers. 5. Decrypt any full match."
    ),
    "walkthrough": (
        "1. Write out the copper as carved: K1, K2, K3, the ?, then K4. "
        "2. Choose a distance, say 31, one carved line. "
        "3. Place 22 of K4 (F) takes its key from the carved letter 31 places earlier, which is in K3's last line. "
        "4. On the sculpture's alphabet with Vigenere, F minus that key letter must give E; count a hit if it does. "
        "5. Repeat for all 24 known places, every distance 1-200, every rule, and with the letter straight above on the plate."
    ),
}

import random
from kryptos.facts import STANDARD_ALPHABET as STD, KRYPTOS_ALPHABET as KRY

N = 97
ALPH = {"std": STD, "kry": KRY}
N_CONTROLS = 10

UPPER_LEFT = """EMUFPHZLRFAXYUSDJKZLDKRNSHGNFIVJ
YQTQUXQBQVYUVLLTREVJYQTMKYRDMFD
VFPJUDEEHZWETZYVGWHKKQETGFQJNCE
GGWHKK?DQMCPFQZDQMMIAGPFXHQRLG
TIMVMZJANQLVKQEDAGDVFRPJUNGEUNA
QZGZLECGYUXUEENJTBJLBQCRTBJDFHRR
YIZETKZEMVDUFKSJHKFWHKUWQLSZFTI
HHDDDUVH?DWKBFUFPWNTDFIYCUQZERE
EVLDKFEZMOQQJLTTUGSYQPFEUNLAVIDX
FLGGTEZ?FKZBSFDQVGOGIPUFXHHDRKF
FHQNTGPUAECNUVPDJMQCLQUMUNEDFQ
ELZZVRRGKFFVOEEXBDMVPNFQXEZLGRE
DNQFMPNZGLFLPMRJQYALMGNUVPDXVKP
DQUMEBEDMHDAFMJGZNUPLGEWJLLAETG""".split()
LOWER_LEFT = """ENDYAHROHNLSRHEOCPTEOIBIDYSHNAIA
CHTNREYULDSLLSLLNOHSNOSMRWXMNE
TPRNGATIHNRARPESLNNELEBLPIIACAE
WMTWNDITEENRAHCTENEUDRETNHAEOE
TFOLSEDTIWENHAEIOYTEYQHEENCTAYCR
EIFTBRSPAMHHEWENATAMATEGYEERLB
TEEFOASFIOTUETUAEOTOARMAEERTNRTI
BSEDDNIAAHTTMSTEWPIEROAGRIEWFEB
AECTDDHILCEIHSITEGOEAOSDDRYDLORIT
RKLMLEHAGTDHARDPNEOHMGFMFEUHE
ECDMRIPFEIMEHNLSSTTRTVDOHW?OBKR
UOXOGHULBSOLIFBBWFLRVQQPRNGKSSO
TWTQSJQSSEKZZWATJKLUDIAWINFBNYP
VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR""".split()


def k4_cells():
    cells = []
    for p in range(1, 98):
        if p <= 4:
            cells.append((10, 26 + p))           # 0-based line 10, 0-based column 27-30
        else:
            q = p - 5
            cells.append((11 + q // 31, q % 31))
    return cells


def run(ctx):
    ct, known = ctx.K4, ctx.KNOWN
    places = sorted(known)
    before_q = "".join(UPPER_LEFT + LOWER_LEFT)
    before_q = before_q[:before_q.index("?OBKR") + 1]          # everything carved before K4, ? included
    assert "".join(LOWER_LEFT)[ "".join(LOWER_LEFT).index("?OBKR") + 1:] == ct
    streams = {"with ?": before_q, "letters only": before_q.replace("?", "")}
    rng = random.Random(118)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    rules = [(m, pa, ca) for m in ("vig", "beau", "var") for pa in ALPH for ca in ALPH]
    best = {k: [0] * len(texts) for k in ("lag", "geometric")}
    full = []
    top = []
    for sname, pre in streams.items():
        for t, txt in enumerate(texts):
            stream = pre + txt
            base = len(pre)
            for lag in range(1, 201):
                for mode, pa, ca in rules:
                    PI = {c: i for i, c in enumerate(ALPH[pa])}; CI = {c: i for i, c in enumerate(ALPH[ca])}
                    hits = 0
                    for q in places:
                        j = base + q - 1 - lag
                        kc = stream[j]
                        if kc == "?":
                            continue
                        c, k = CI[txt[q - 1]], CI[kc]
                        v = {"vig": (c - k) % 26, "beau": (k - c) % 26, "var": (c + k) % 26}[mode]
                        hits += ALPH[pa][v] == known[q]
                    if hits > best["lag"][t]:
                        best["lag"][t] = hits
                    if t == 0:
                        if hits == 24:
                            full.append((sname, lag, mode, pa, ca))
                        if hits >= 6:
                            top.append({"stream": sname, "lag": lag, "rule": f"{mode}/{pa}/{ca}", "hits": hits})
    # geometric: the letter in the same column one or two lines above on the lower-left plate
    cells = k4_cells()
    geo = {}
    for t, txt in enumerate(texts):
        lines = list(LOWER_LEFT[:10]) + [LOWER_LEFT[10][:27] + txt[:4], txt[4:35], txt[35:66], txt[66:97]]
        for up in (1, 2):
            for side in ("left", "right"):
                for mode, pa, ca in rules:
                    PI = {c: i for i, c in enumerate(ALPH[pa])}; CI = {c: i for i, c in enumerate(ALPH[ca])}
                    hits = 0
                    for q in places:
                        li, col = cells[q - 1]
                        above = lines[li - up]
                        if side == "left":
                            kc = above[col] if col < len(above) else None
                        else:
                            fr = len(lines[li]) - 1 - col
                            kc = above[len(above) - 1 - fr] if fr < len(above) else None
                        if kc is None or kc == "?":
                            continue
                        c, k = CI[txt[q - 1]], CI[kc]
                        v = {"vig": (c - k) % 26, "beau": (k - c) % 26, "var": (c + k) % 26}[mode]
                        hits += ALPH[pa][v] == known[q]
                    if hits > best["geometric"][t]:
                        best["geometric"][t] = hits
                    if t == 0:
                        geo[f"{up} up, {side}, {mode}/{pa}/{ca}"] = hits
    top.sort(key=lambda r: -r["hits"])
    bounds = {"family": "ciphertext autokey continuing the carved stream from K3, and the letter above on the plate",
              "streams": {k: len(v) for k, v in streams.items()}, "lags": [1, 200], "rules": len(rules),
              "k4_best_lag_hits": best["lag"][0], "controls_best_lag_hits": best["lag"][1:],
              "k4_best_geometric_hits": best["geometric"][0], "controls_best_geometric_hits": best["geometric"][1:],
              "k4_full": full, "k4_top": top[:15], "k4_geometric": dict(sorted(geo.items(), key=lambda kv: -kv[1])[:10]),
              "controls": f"{N_CONTROLS} shuffled coppers (K4 shuffled, earlier text fixed; seed 118), identical search"}
    notes = (f"Lags 1-200 x {len(rules)} rules x 2 streams: K4 best {best['lag'][0]}/24, controls {best['lag'][1:]}; full {len(full)}. "
             f"Letter above on the plate: K4 best {best['geometric'][0]}/24, controls {best['geometric'][1:]}.")
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct, known = ctx.K4, ctx.KNOWN
    pre = "".join(UPPER_LEFT + LOWER_LEFT)
    pre = pre[:pre.index("?OBKR") + 1]
    stream = pre + ct
    I = {c: i for i, c in enumerate(KRY)}
    lines = [f"the carved stream before K4 has {len(pre)} characters; lag 31 (one carved line), sculpture's alphabet, Vigenere", "",
             "place  known  carved  key letter (31 back)  carved - key  hit"]
    for q in (22, 23, 24, 25, 26, 64):
        kc = stream[len(pre) + q - 1 - 31]
        d = KRY[(I[ct[q - 1]] - I[kc]) % 26] if kc != "?" else "?"
        lines.append(f"{q:>5}  {known[q]:>5}  {ct[q - 1]:>6}  {kc:>20}  {d:>12}  {'yes' if d == known[q] else 'no'}")
    return "\n".join(lines)
