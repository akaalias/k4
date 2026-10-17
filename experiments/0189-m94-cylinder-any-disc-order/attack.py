"""Experiment 0189 (F11.1). See program.md for the contract."""

EXPERIMENT = {
    "slug": "m94-cylinder-any-disc-order",
    "title": "F11.1: the US Army's M-94 cylinder (25 published discs) in any disc order, any cipher row per group of 25, any group alignment: exact",
    "family": "11-agency-hand-systems",
    "parent": "0119-one-free-alphabet-exact",
    "changed": (
        "F11.1, first family run. The community tried M-94 with hill climbs only (knowledge/05-attacks.md); no bounded "
        "result exists. The 25 disc alphabets as published (jproc.ca/crypto/m94.html, credited to George Mace; disc B1 "
        "matches the Cryptogram 1982 reprint; each alphabet checked to be a permutation starting A then its disc letter). "
        "Use (TM 32-220 par. 144): 25 discs in the day's order, 25 plaintext letters set on the guide row, any other row "
        "taken as cipher. K4 as consecutive groups of 25 from an unknown alignment (0-24), each group with its own row "
        "offset (1-25). Each known letter allows a set of discs at its slot; slots must take distinct discs (a matching). "
        "Exact over every alignment and every offset triple; K4 against 10 shuffled copies; plants."
    ),
    "hypothesis_expert": (
        "A9 (methods known to the creators in 1990; the M-94 was declassified long before), C1 ('matrix codes'), F11. "
        "Model: c_i = D_{k[s]}[(pos(p_i) + g_group) mod 26], s = (i + a) mod 25, k a disc order. The 24 known letters fall "
        "in at most three groups; for fixed (a, g's), each slot's allowed discs are the intersection over its known "
        "letters; consistent iff a system of distinct discs exists. Statistic: consistent (a, g) cells, K4 against 10 "
        "copies."
    ),
    "hypothesis_eli5": (
        "The US Army's M-94 was a stack of 25 lettered discs on a rod: line up the message along one row, copy out any "
        "other row. The discs' alphabets are published; only their order and the row chosen were secret. Each known "
        "letter says which discs could sit at its place; if no ordering of the 25 discs fits all of them, the M-94 did "
        "not make K4."
    ),
    "prediction": "No alignment and row choice admits a disc order on K4 or on the copies (about 24 strong checks); plants are found. Zero candidates.",
    "method": (
        "1. Load the 25 published alphabets and check them. "
        "2. For each alignment (0-24) and each row offset for every group holding known letters: allowed discs per slot. "
        "3. Any empty slot kills the cell; otherwise look for distinct discs by bipartite matching. "
        "4. K4 against 10 shuffled copies; two planted texts as builder checks."
    ),
    "walkthrough": (
        "1. Suppose the groups of 25 start at place 1: places 1-25, 26-50, 51-75, 76-97. "
        "2. Place 22 is slot 22 of the first group; with that group's cipher row 7 places below the guide row, the disc "
        "there must carry the carved F seven places after the known E. "
        "3. List the discs that do; do the same for every known letter. "
        "4. Places 22 and 72 share slot 22 (different groups, different rows): one disc must satisfy both. "
        "5. If every slot keeps a disc and the discs can all be different, that setting survives."
    ),
}

import random
import time

from kryptos.facts import KNOWN

N_CONTROLS = 10
A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DISCS = """B1 ABCEIGDJFVUYMHTQKZOLRXSPWN
C2 ACDEHFIJKTLMOUVYGZNPQXRWSB
D3 ADKOMJUBGEPHSCZINXFYQRTVWL
E4 AEDCBIFGJHLKMRUOQVPTNWYXZS
F5 AFNQUKDOPITJBRHCYSLWEMZVXG
G6 AGPOCIXLURNDYZHWBJSQFKVMET
H7 AHXJEZBNIKPVROGSYDULCFMQTW
I8 AIHPJOBWKCVFZLQERYNSUMGTDX
J9 AJDSKQOIVTZEFHGYUNLPMBXWCR
K10 AKELBDFJGHONMTPRQSVZUXYWIC
L11 ALTMSXVQPNOHUWDIZYCGKRFBEJ
M12 AMNFLHQGCUJTBYPZKXISRDVEWO
N13 ANCJILDHBMKGXUZTSWQYVORPFE
O14 AODWPKJVIUQHZCTXBLEGNYRSMF
P15 APBVHIYKSGUENTCXOWFQDRLJZM
Q16 AQJNUBTGIMWZRVLXCSHDEOKFPY
R17 ARMYOFTHEUSZJXDPCWGQIBKLNV
S18 ASDMCNEQBOZPLGVJRKYTFUIWXH
T19 ATOJYLFXNGWHVCMIRBSEKUPDZQ
U20 AUTRZXQLYIOVBPESNHJWMDGFCK
V21 AVNKHRGOXEYBFSJMUDQCLZWTIP
W22 AWVSFDLIEBHKNRJQZGMXPUCOTY
X23 AXKWREVDTUFOYHMLSIQNJCPGBZ
Y24 AYJPXMVKBQWUGLOSTECHNZFRID
Z25 AZDNBUHYFWJLVGRCQMPSOEXTKI"""
NAMES = [l.split()[0] for l in DISCS.splitlines()]
ALPH = [l.split()[1] for l in DISCS.splitlines()]
PLACES = sorted(KNOWN)


def check_discs():
    for n, a in zip(NAMES, ALPH):
        assert sorted(a) == list(A) and a[0] == "A" and a[1] == n[0], n
    return True


def match(slot_masks):
    """Is there a system of distinct discs? slot_masks: list of 25-bit masks."""
    owner = {}

    def aug(s, seen):
        m = slot_masks[s]
        d = 0
        while m:
            if m & 1 and d not in seen:
                seen.add(d)
                if d not in owner or aug(owner[d], seen):
                    owner[d] = s
                    return True
            m >>= 1; d += 1
        return False
    return all(aug(s, set()) for s in range(len(slot_masks)))


def consistent_cells(text):
    pos = [{ch: i for i, ch in enumerate(a)} for a in ALPH]
    # M[e][g]: mask of discs carrying the carved letter g places after the known letter
    M = []
    for q in PLACES:
        p, c = KNOWN[q], text[q - 1]
        M.append([sum(1 << d for d in range(25) if ALPH[d][(pos[d][p] + g) % 26] == c) for g in range(26)])
    cells = []
    for a in range(25):
        grp = [(q - 1 + a) // 25 for q in PLACES]
        slot = [(q - 1 + a) % 25 for q in PLACES]
        groups = sorted(set(grp))
        idx = {g: k for k, g in enumerate(groups)}

        def rec(k, gs):
            if k == len(groups):
                masks = {}
                for e in range(24):
                    s = slot[e]
                    masks[s] = masks.get(s, (1 << 25) - 1) & M[e][gs[idx[grp[e]]]]
                    if not masks[s]:
                        return
                if match(list(masks.values())):
                    cells.append((a, tuple(gs)))
                return
            for g in range(1, 26):
                # early prune: letters of this group alone
                ok = True
                for e in range(24):
                    if grp[e] == groups[k] and not M[e][g]:
                        ok = False
                        break
                if ok:
                    rec(k + 1, gs + [g])
        rec(0, [])
    return cells


def encipher(p, order, a, gs):
    out = []
    pos = [{ch: i for i, ch in enumerate(x)} for x in ALPH]
    for i, ch in enumerate(p):
        grp, s = (i + a) // 25, (i + a) % 25
        d = order[s]
        out.append(ALPH[d][(pos[d][ch] + gs[grp]) % 26])
    return "".join(out)


def run(ctx):
    t0 = time.time()
    assert check_discs()
    ct = ctx.K4
    rng = random.Random(1890)
    texts = [ct]
    for _ in range(N_CONTROLS):
        sh = list(ct); rng.shuffle(sh); texts.append("".join(sh))
    PLANT_P = "USEDTHEEARTHSMAGNETICEASTNORTHEASTRMATIONWASGATHEREDANDTRANSMITBERLINCLOCKUNDTOANUNKNOWNLOCATIONX"
    plants = []
    for k in range(2):
        order = list(range(25)); rng.shuffle(order)
        a = rng.randrange(25); gs = [rng.randint(1, 25) for _ in range(6)]
        c = encipher(PLANT_P, order, a, gs)
        cells = consistent_cells(c)
        true = (a, tuple(gs[g] for g in sorted({(q - 1 + a) // 25 for q in PLACES})))
        plants.append({"alignment": a, "cells": len(cells), "true_cell_found": true in cells})
    res = [consistent_cells(t) for t in texts]
    bounds = {
        "family": "M-94 cylinder, 25 published discs in any order, any cipher row per group of 25, any alignment, exact (bipartite matching)",
        "discs_source": "jproc.ca/crypto/m94.html (George Mace); checked: permutations, A then the disc letter; B1 as the Cryptogram 1982 reprint",
        "consistent_cells": {"k4": len(res[0]), "copies": [len(r) for r in res[1:]]},
        "k4_cells": res[0][:20], "plants": plants,
        "not_tested": "Jefferson's own wheel (alphabets not recorded), M-138-A strip sets (not published): blocked",
        "copies": f"{N_CONTROLS} shuffled copies (seed 1890)", "seconds": round(time.time() - t0), "exhaustive": True,
    }
    notes = f"consistent (alignment, rows) cells: K4 {len(res[0])} (copies {min(len(r) for r in res[1:])}-{max(len(r) for r in res[1:])}); plants {plants}"
    return {"candidates": [], "bounds": bounds, "notes": notes}


def encrypt(plaintext, key):
    return plaintext


def worked_example(ctx, key):
    ct = ctx.K4
    pos = [{ch: i for i, ch in enumerate(x)} for x in ALPH]
    lines = ["groups of 25 from place 1; first group's cipher row 7 below the guide row: discs that can stand at place 22 (E over carved F)", ""]
    ok = [NAMES[d] for d in range(25) if ALPH[d][(pos[d]["E"] + 7) % 26] == ct[21]]
    lines.append(f"place 22: {ok}")
    return "\n".join(lines)
