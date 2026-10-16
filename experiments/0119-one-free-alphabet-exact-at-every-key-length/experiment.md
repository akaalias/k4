# 0119-one-free-alphabet-exact-at-every-key-length: One alphabet in an unknown order on both sides of the table (Quagmire III), no move: does any order fit the 24 known letters, key lengths 1-26, solved exactly?

**Family:** 1-keyed-periodic  
**Parent:** 0097-free-mixed-alphabets-after-a-move  
**Decision:** reverted  
**Run:** 2026-10-16T07:54:27+00:00, 6.8 s, status ran  
**Time by phase:** design 133 s, test 270 s, implement 249 s, run 7 s, record 0 s

## In plain words

K1 and K2 were enciphered on a table whose rows are one scrambled alphabet (it starts KRYPTOS), each row shifted one place, with a repeating key word choosing the row for each letter. Sanborn said his own table was slightly different. Here the scrambled alphabet may be any of the 400 million million million million orders. We do not guess it: for each key length from 1 to 26 a careful search asks whether any order at all, with any key, turns the carved letters into the 24 letters we know. If none does, that key length is finished for good.

## Walkthrough, by hand

1. Choose a key length, say 7, and write the 24 known places with their slot (place mod 7).
2. For each known place write: place-in-alphabet of the carved letter = place of the known letter + key value of the slot.
3. In slot 3 the known letters R (66) and C (73) both sit under carved P, so R and C would need the same place: no alphabet works, length 7 is dead.
4. When no such clash shows at once, set the first letter's place to 0 and try values for the busiest slot's key; each choice fixes further places through the equations.
5. Back up whenever two letters would need the same place or one letter two places.
6. If a full set of places and key values satisfies all 24 equations, the length is alive; if every branch backs up, it is dead.
7. Repeat with the Beaufort form (carved place = key value minus known place), for every length 1-26, then on scrambled coppers.

## Worked example (generated)

```
key length 7: known letters by slot (place mod 7)
  slot 0: E->F (22), T->R (29), B->N (64), L->Z (71)
  slot 1: A->L (23), H->N (30), E->Y (65), O->F (72)
  slot 2: S->R (24), E->G (31), R->P (66), C->P (73)
  slot 3: T->V (25), A->K (32), L->V (67), K->K (74)
  slot 4: N->Q (26), S->S (33), I->T (68)
  slot 5: O->Q (27), T->S (34), N->T (69)
  slot 6: R->P (28), C->M (70)
  form V: no alphabet fits
  form B: no alphabet fits

key length 12: known letters by slot (place mod 12)
  slot 0: T->V (25), C->P (73)
  slot 1: N->Q (26), K->K (74)
  slot 2: O->Q (27)
  slot 3: R->P (28), B->N (64)
  slot 4: T->R (29), E->Y (65)
  slot 5: H->N (30), R->P (66)
  slot 6: E->G (31), L->V (67)
  slot 7: A->K (32), I->T (68)
  slot 8: S->S (33), N->T (69)
  slot 9: E->F (22), T->S (34), C->M (70)
  slot 10: A->L (23), L->Z (71)
  slot 11: S->R (24), O->F (72)
  form V: no alphabet fits
  form B: no alphabet fits

```

## Lineage

Inherits from 0097-free-mixed-alphabets-after-a-move. What changed: F1.1, first step (exact consistency). 0097 tested one unknown alphabet only at key lengths 3, 7 and 21, and only with a linear relaxation that can refute but not confirm (it rejects when two letters are forced to the same place mod 2 and mod 13; a system can still have no one-to-one solution without any such forced pair). Here every key length 1-26 is solved exactly by a search over the alphabet with propagation, in both table forms (Vigenere-like: place(c) = place(p) + k; Beaufort-like: place(c) = k - place(p)), with no move, on K4 and on 100 scrambled coppers. Key lengths where K4 has no fitting alphabet are closed exactly; the rest go to the English climb (next experiment).

## Hypothesis (domain expert)

C27(c) (Sanborn, NYT 20 Nov 2010: his K1/K2 tableau was 'slightly different from the one on Kryptos'), C11a, C1(b) (the table alone, no move). K1 and K2 are Quagmire III on the KRYPTOS alphabet (keys PALIMPSEST, ABSCISSA). Covered so far: standard and KRYPTOS alphabets (0005, crib sweep), keyword alphabets from every dictionary word (0109), alphabets one swap or move from KRYPTOS (0071), any alphabet at lengths 3, 7, 21 by relaxation (0097). Model: one unknown bijection A: letters -> Z26 used for plain and cipher sides; key k of length L (free values, the key alphabet drops out); form V: A(c_i) = A(p_i) + k[i mod L]; form B: A(c_i) = k[i mod L] - A(p_i) (variant Beaufort is form V with k negated). The 24 known letters give 24 linear equations over Z26 = Z2 x Z13. Exact decision: solve mod 13 and mod 2; a one-to-one alphabet needs every residue class mod 13 to hold at most two letters, each such pair differing mod 2. Refute at once when two letters coincide mod 13 and mod 2 in every solution, or three mod 13 (0097's relaxation); otherwise enumerate the mod-13 letter space up to translation and scaling (rank <= 5), or search it depth first with pruning on class size and mod-2 solvability (larger ranks), with a node limit that reports 'undecided' rather than guessing. Every fit yields a witness alphabet and key re-checked against all 24 equations; cross-checked on 40 coppers against an independent propagation search (no fit it found was called dead). Planted texts at every length must come out consistent. Controls: 100 shuffles of K4 (seed 119), same test.

## Prediction

Key lengths 1-6 have no fitting alphabet on K4 (too many repeats of a slot); from about 8 upward most lengths fit in both forms, because a free alphabet has 25 free places and the known letters give fewer checks than that. K4's number of fitting lengths lies inside the middle 90% of the 100 scrambled coppers in each form. If K4 fits at a length where fewer than 5% of coppers fit, that is outside the coppers' range and stops the queue. Zero candidates (this step returns none).

## Method

1. For each key length L from 1 to 26 and each form, write the 24 equations (slot i mod L, known letter, carved letter).
2. Decide exactly whether a one-to-one alphabet and a key satisfy them, by linear algebra mod 13 and mod 2 with an exhaustive search of the mod-13 solutions; re-check every witness.
3. Do the same on 100 scrambled coppers.
4. Report, per length and form, K4 fit or not, the share of coppers that fit, and the number of checks (24 minus the slots that hold a known letter).
5. Validate on planted texts and against 0097's relaxation (every exact fit must also pass the relaxation).

## Result

Candidates returned: 0. Passed all gates: 0. Best crib hits among all candidates: 0/24
(no candidates).
Best loss: None (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| - | no candidates | | | | |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "one unknown alphabet on both sides (Quagmire III, any of 26! orders), periodic key, no move",
 "key_lengths": [
  1,
  26
 ],
 "forms": {
  "V": "A(c) = A(p) + k",
  "B": "A(c) = k - A(p)"
 },
 "exhaustive": "exact decision per length and form (search with propagation, witness re-checked)",
 "checks_by_length": {
  "1": 23,
  "2": 22,
  "3": 21,
  "4": 20,
  "5": 19,
  "6": 18,
  "7": 17,
  "8": 16,
  "9": 15,
  "10": 14,
  "11": 13,
  "12": 12,
  "13": 11,
  "14": 11,
  "15": 9,
  "16": 8,
  "17": 7,
  "18": 7,
  "19": 9,
  "20": 11,
  "21": 11,
  "22": 9,
  "23": 7,
  "24": 5,
  "25": 3,
  "26": 1
 },
 "k4_fits": {
  "V": [],
  "B": [
   23,
   26
  ]
 },
 "k4_dead": {
  "V": [
   1,
   2,
   3,
   4,
   5,
   6,
   7,
   8,
   9,
   10,
   11,
   12,
   13,
   14,
   15,
   16,
   17,
   18,
   19,
   20,
   21,
   22,
   23,
   24,
   25,
   26
  ],
  "B": [
   1,
   2,
   3,
   4,
   5,
   6,
   7,
   8,
   9,
   10,
   11,
   12,
   13,
   14,
   15,
   16,
   17,
   18,
   19,
   20,
   21,
   22,
   24,
   25
  ]
 },
 "copper_share_fitting_by_length": {
  "V": [
   0.0,
   0.0,
   0.0,
   0.0,
   0.0,
   0.0,
   0.0,
   0.02,
   0.0,
   0.06,
   0.13,
   0.18,
   0.21,
   0.21,
   0.01,
   0.39,
   0.02,
   0.39,
   0.01,
   0.2,
   0.21,
   0.32,
   0.44,
   0.62,
   0.69,
   0.87
  ],
  "B": [
   0.0,
   0.0,
   0.0,
   0.0,
   0.0,
   0.0,
   0.0,
   0.0,
   0.0,
   0.04,
   0.15,
   0.15,
   0.28,
   0.2,
   0.01,
   0.39,
   0.01,
   0.45,
   0.02,
   0.26,
   0.2,
   0.35,
   0.44,
   0.58,
   0.62,
   0.85
  ]
 },
 "k4_fitting_lengths_3_26": {
  "V": 0,
  "B": 2
 },
 "coppers_fitting_lengths_3_26_sorted": {
  "V": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   1,
   2,
   2,
   2,
   2,
   2,
   2,
   2,
   2,
   2,
   2,
   2,
   3,
   3,
   3,
   3,
   3,
   3,
   3,
   3,
   3,
   3,
   3,
   3,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   6,
   6,
   6,
   6,
   7,
   7,
   7,
   7,
   7,
   7,
   8,
   8,
   8,
   8,
   8,
   8,
   8,
   9,
   9,
   9,
   9,
   9,
   9,
   9,
   9,
   10,
   10,
   10,
   10,
   10,
   10,
   10,
   11,
   11,
   11,
   14,
   15
  ],
  "B": [
   1,
   1,
   2,
   2,
   2,
   2,
   2,
   2,
   2,
   2,
   2,
   2,
   2,
   3,
   3,
   3,
   3,
   3,
   3,
   3,
   3,
   3,
   3,
   3,
   3,
   3,
   3,
   3,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   4,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   6,
   6,
   6,
   6,
   6,
   6,
   6,
   6,
   6,
   6,
   6,
   7,
   7,
   7,
   7,
   7,
   7,
   7,
   7,
   7,
   7,
   7,
   7,
   7,
   7,
   8,
   8,
   8,
   8,
   8,
   9,
   9,
   9,
   9,
   9,
   11,
   11
  ]
 },
 "coppers_5th_95th_percentile": {
  "V": [
   0,
   10
  ],
  "B": [
   2,
   9
  ]
 },
 "k4_fits_where_under_5pct_of_coppers_fit": {
  "V": [],
  "B": []
 },
 "k4_witnesses": {
  "B23": {
   "places": {
    "A": 12,
    "B": 25,
    "C": 0,
    "E": 13,
    "F": 1,
    "G": 5,
    "H": 19,
    "I": 3,
    "K": 6,
    "L": 14,
    "M": 17,
    "N": 15,
    "O": 16,
    "P": 18,
    "Q": 2,
    "R": 20,
    "S": 23,
    "T": 11,
    "V": 7,
    "Y": 21,
    "Z": 4
   },
   "key": [
    17,
    18,
    17,
    18,
    12,
    5,
    8,
    18,
    18,
    20,
    8,
    null,
    null,
    null,
    null,
    null,
    null,
    14,
    8,
    12,
    21,
    14,
    0
   ]
  },
  "B26": {
   "places": {
    "A": 14,
    "B": 1,
    "C": 15,
    "E": 2,
    "F": 16,
    "G": 3,
    "H": 17,
    "I": 4,
    "K": 9,
    "L": 18,
    "M": 5,
    "N": 6,
    "O": 19,
    "P": 7,
    "Q": 20,
    "R": 21,
    "S": 8,
    "T": 22,
    "V": 10,
    "Y": 23,
    "Z": 24
   },
   "key": [
    13,
    2,
    17,
    23,
    5,
    23,
    16,
    4,
    null,
    null,
    null,
    7,
    25,
    2,
    2,
    0,
    2,
    20,
    16,
    9,
    22,
    18,
    6,
    3,
    6,
    0
   ]
  }
 },
 "relaxation_violations": 0,
 "k4_undecided": {
  "V": [],
  "B": []
 },
 "controls_undecided_total": {
  "V": 0,
  "B": 0
 },
 "texts_done": 101,
 "plants": "3 per length and form, all recovered as consistent",
 "controls": "100 shuffled coppers (seed 119), identical test"
}
```

Notes: K4 dead (no alphabet fits) at lengths V [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26], B [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25]. Fitting lengths 3-26: K4 V 0, B 2; coppers 5th-95th V (0, 10), B (2, 9). Unusual fits: {'V': [], 'B': []}.


