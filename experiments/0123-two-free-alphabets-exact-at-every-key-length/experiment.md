# 0123-two-free-alphabets-exact-at-every-key-length: Two alphabets in unknown orders, one for the message and one for the carved letters (Quagmire IV), no move: which key lengths 1-26 can any pair fit, and is that unusual against scrambled coppers?

**Family:** 1-keyed-periodic  
**Parent:** 0119-one-free-alphabet-exact-at-every-key-length  
**Decision:** reverted  
**Run:** 2026-10-16T08:29:24+00:00, 10.3 s, status ran  
**Time by phase:** unattributed 21 s, run 10 s, record 0 s

## In plain words

K1 and K2 used one scrambled alphabet for the whole table. A variant uses two: one scrambled order to look up the message letter and another to write the carved letter. With both orders unknown there are vastly more tables. For each key length 1 to 26 we ask, by exact arithmetic on the 24 known letters, whether any pair of orders and any key could produce them, and how often the same is true of scrambled copies of the carved text.

## Walkthrough, by hand

1. Choose a key length, say 8, and group the known places by slot (place mod 8).
2. For each known place write: place of the carved letter in the cipher alphabet = place of the known letter in the plain alphabet + key value of the slot.
3. Two known places in one slot give one check with the key removed: C(c1) - P(p1) = C(c2) - P(p2).
4. If one slot holds the same known letter over two different carved letters, those carved letters would share a place: dead.
5. Otherwise solve the checks modulo 13 and modulo 2 and search the solutions for one where each alphabet keeps its letters apart.
6. Repeat for every length 1-26 and for 100 scrambled copies of the carved text.

## Worked example (generated)

```
key length 8: known letters by slot (place mod 8)
  slot 0: T->V (25), S->S (33), E->Y (65), C->P (73)
  slot 1: N->Q (26), T->S (34), R->P (66), K->K (74)
  slot 2: O->Q (27), L->V (67)
  slot 3: R->P (28), I->T (68)
  slot 4: T->R (29), N->T (69)
  slot 5: E->F (22), H->N (30), C->M (70)
  slot 6: A->L (23), E->G (31), L->Z (71)
  slot 7: S->R (24), A->K (32), B->N (64), O->F (72)
  plain alphabet places: T=0 R=1 I=3 E=7 L=8 O=9 S=10 C=11 N=17 H=21 A=22 B=23 K=24
  cipher alphabet places: L=0 T=1 F=9 R=10 G=11 Z=12 M=13 V=14 Q=15 Y=21 K=22 N=23 S=24 P=25
  key: [14, 24, 6, 24, 10, 2, 4, 0]

key length 9: known letters by slot (place mod 9)
  slot 0: R->P (28), B->N (64), C->P (73)
  slot 1: T->R (29), E->Y (65), K->K (74)
  slot 2: H->N (30), R->P (66)
  slot 3: E->F (22), E->G (31), L->V (67)
  slot 4: A->L (23), A->K (32), I->T (68)
  slot 5: S->R (24), S->S (33), N->T (69)
  slot 6: T->V (25), T->S (34), C->M (70)
  slot 7: N->Q (26), L->Z (71)
  slot 8: O->Q (27), O->F (72)
  dead: no pair of alphabets fits

```

## Lineage

Inherits from 0119-one-free-alphabet-exact-at-every-key-length. What changed: F1.2. 0097 tested two unknown alphabets only at key lengths 3, 7 and 21, by a relaxation. Here every length 1-26 is decided exactly with 0119's method generalised to two independent alphabets (each one-to-one), on K4 and 100 scrambled coppers. Power is stated before running: at each length, the share of coppers on which the exact test fails is the test's power to reject a random text there; lengths where K4 fits are then compared with that rate.

## Hypothesis (domain expert)

C27(c) (Sanborn's 'slightly different' tableau), C1(b). Model: plain alphabet P and cipher alphabet C, unknown bijections letters -> Z26, key k of length L: C(c_i) = P(p_i) + k[i mod L] (Quagmire IV; the Beaufort form C(c) = k - P(p) is the same family with P reflected, so one form covers both; a key alphabet drops out). 24 linear equations over Z26; exact decision by CRT: solve mod 13 and mod 2, each alphabet's letters at most two per residue class mod 13 with each pair differing mod 2; refute at once on forced coincidences; otherwise enumerate the mod-13 letter space up to the two translations and scaling (rank <= 5) or search it depth first with pruning, a node limit reporting 'undecided'. The generalised decider agreed with 0119's on 780 one-alphabet cases and recovered planted Quagmire IV texts at lengths 3-26 in a dry run, which also showed K4 fitting at lengths 8, 13, 16, 19, 20, 23, 24 and 26. Power and copper comparison are what this run adds. Two alphabets have more freedom than one, so where both K4 and most coppers fit, 0120's finding (a climb on one alphabet already has weak power at 23 and none at 26) means an English climb here could not decide; such lengths are recorded blocked, not run weakly.

## Prediction

Power: the exact test rejects nearly all coppers (at least 90%) at lengths 1-7 and fewer than half at lengths with 7 or fewer checks (17, 18, 23-26). K4's 8 fitting lengths lie inside the middle 90% of the coppers' counts, and at every length where K4 fits at least 5% of coppers fit too; if K4 fits at a length where fewer than 5% of coppers do (length 8, 16 checks, is the candidate), that is outside the range and stops the queue for a replication. Zero candidates.

## Method

1. For each key length 1-26 write the 24 equations.
2. Decide exactly whether a pair of one-to-one alphabets and a key satisfy them; re-check every witness.
3. Do the same on 100 scrambled coppers (seed 121).
4. Report per length the checks, K4's verdict, the share of coppers that fit (the power is one minus that share), and K4's count of fitting lengths against the coppers'.

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
 "family": "two unknown alphabets (Quagmire IV, any pair of 26! orders), periodic key, no move",
 "key_lengths": [
  1,
  26
 ],
 "exhaustive": "exact decision per length (witness re-checked)",
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
 "k4_fits": [
  8,
  13,
  16,
  19,
  20,
  23,
  24,
  26
 ],
 "k4_dead": [
  1,
  2,
  3,
  4,
  5,
  6,
  7,
  9,
  10,
  11,
  12,
  14,
  15,
  17,
  18,
  21,
  22,
  25
 ],
 "copper_share_fitting_by_length": [
  0.0,
  0.0,
  0.0,
  0.0,
  0.0,
  0.14,
  0.17,
  0.31,
  0.0,
  0.39,
  0.61,
  0.51,
  0.71,
  0.57,
  0.02,
  0.75,
  0.01,
  0.73,
  0.03,
  0.55,
  0.57,
  0.73,
  0.83,
  0.85,
  0.91,
  0.99
 ],
 "power_by_length": [
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  0.86,
  0.83,
  0.69,
  1.0,
  0.61,
  0.39,
  0.49,
  0.29,
  0.43,
  0.98,
  0.25,
  0.99,
  0.27,
  0.97,
  0.45,
  0.43,
  0.27,
  0.17,
  0.15,
  0.09,
  0.01
 ],
 "k4_fitting_lengths": 8,
 "coppers_fitting_lengths_sorted": [
  5,
  5,
  5,
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
  8,
  8,
  8,
  8,
  8,
  8,
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
  10,
  10,
  10,
  10,
  10,
  11,
  11,
  11,
  11,
  11,
  11,
  11,
  11,
  11,
  11,
  11,
  11,
  11,
  11,
  12,
  12,
  12,
  12,
  12,
  12,
  12,
  12,
  12,
  13,
  13,
  13,
  13,
  13,
  13,
  13,
  13,
  13,
  14,
  14,
  14,
  14,
  14,
  14,
  14,
  14,
  15,
  15,
  15,
  15,
  15,
  16,
  16,
  16
 ],
 "coppers_5th_95th": [
  6,
  15
 ],
 "k4_fits_where_under_5pct_of_coppers_fit": [
  19
 ],
 "k4_undecided": [],
 "controls_undecided_total": 0,
 "texts_done": 101,
 "k4_witnesses": {
  "8": {
   "plain_letters_in_place_order": "TRIELOSCNHABK",
   "cipher_letters_in_place_order": "LTFRGZMVQYKNSP",
   "key": [
    14,
    24,
    6,
    24,
    10,
    2,
    4,
    0
   ]
  },
  "13": {
   "plain_letters_in_place_order": "TSRAEKIHLONCB",
   "cipher_letters_in_place_order": "FKMPYSRGZLNVQT",
   "key": [
    1,
    1,
    11,
    1,
    9,
    24,
    9,
    10,
    22,
    12,
    10,
    22,
    0
   ]
  },
  "16": {
   "plain_letters_in_place_order": "TIOEACKHNSRBL",
   "cipher_letters_in_place_order": "ZVTYGKLPRQSFNM",
   "key": [
    20,
    16,
    2,
    1,
    11,
    13,
    1,
    18,
    1,
    24,
    10,
    16,
    14,
    10,
    0,
    0
   ]
  },
  "19": {
   "plain_letters_in_place_order": "TLRSABNIKOECH",
   "cipher_letters_in_place_order": "FMLPTSGKNQYRVZ",
   "key": [
    null,
    null,
    5,
    18,
    9,
    20,
    4,
    22,
    2,
    19,
    17,
    18,
    4,
    22,
    6,
    6,
    0,
    null,
    null
   ]
  },
  "20": {
   "plain_letters_in_place_order": "TRALCISENOBHK",
   "cipher_letters_in_place_order": "STFLMQZYRKGNPV",
   "key": [
    null,
    20,
    6,
    6,
    25,
    22,
    21,
    22,
    14,
    4,
    8,
    18,
    18,
    0,
    null,
    null,
    null,
    null,
    null,
    null
   ]
  },
  "23": {
   "plain_letters_in_place_order": "TLHOANSIRBCEK",
   "cipher_letters_in_place_order": "SVZGLTPNRYFKQM",
   "key": [
    2,
    1,
    13,
    15,
    24,
    14,
    11,
    11,
    13,
    14,
    0,
    null,
    null,
    null,
    null,
    null,
    null,
    24,
    17,
    24,
    0,
    24,
    0
   ]
  },
  "24": {
   "plain_letters_in_place_order": "TOBRNCLKHISEA",
   "cipher_letters_in_place_order": "FKZNVSYGLMPQRT",
   "key": [
    5,
    14,
    17,
    14,
    19,
    15,
    17,
    3,
    13,
    6,
    null,
    null,
    null,
    null,
    null,
    2,
    10,
    14,
    18,
    4,
    16,
    4,
    16,
    0
   ]
  },
  "26": {
   "plain_letters_in_place_order": "TAKHLNREBCIOS",
   "cipher_letters_in_place_order": "VYFLMQSTZGKNPR",
   "key": [
    13,
    12,
    25,
    14,
    1,
    15,
    13,
    12,
    null,
    null,
    null,
    2,
    7,
    12,
    16,
    16,
    2,
    14,
    4,
    10,
    2,
    14,
    2,
    0,
    0,
    0
   ]
  }
 },
 "controls": "100 shuffled coppers (seed 121), identical test"
}
```

Notes: K4 fits at [8, 13, 16, 19, 20, 23, 24, 26] (8 lengths); coppers 5th-95th (6, 15); share of coppers fitting where K4 fits: {8: 0.31, 13: 0.71, 16: 0.75, 19: 0.03, 20: 0.55, 23: 0.83, 24: 0.85, 26: 0.99}; unusual: [19].


