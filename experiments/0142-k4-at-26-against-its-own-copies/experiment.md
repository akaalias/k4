# 0142-k4-at-26-against-its-own-copies: F1.1 at key length 26 decided with design 2: K4 against 12 scrambled copies of itself (one free alphabet, Beaufort form)

**Family:** 1-keyed-periodic  
**Parent:** 0140-k4-against-its-own-copies-with-the-tempering-climb  
**Decision:** reverted  
**Run:** 2026-10-16T19:12:02+00:00, 150.1 s, status ran  
**Time by phase:** unattributed 185 s, run 150 s, record 42 s

## In plain words

The search that tells planted English from its own scrambled letters runs on the carved text for the last undecided case of one scrambled alphabet: a 26-letter key, where the known letters give only one check. The carved text is compared with scrambled copies of itself; if it were English enciphered this way it would usually come first.

## Walkthrough, by hand

1. Write K4 in rows of 26; each column is one key slot; one column holds two known letters, whose sums must agree.
2. Search alphabets that keep that sum, sixteen searches side by side, scoring the whole text as English.
3. Do the same on 12 shuffles of K4 that still allow the known letters.
4. If K4 is anywhere inside the pack, the cell is closed at the measured strength.

## Worked example (generated)

```
key length 23, Beaufort form: K4 in rows of 23; each column is one key slot

  O B K R U O X O G H U L B S O L I F B B W F L
  R V Q Q P R N G K S S O T W T Q S J Q S S E K
  Z Z W A T J K L U D I A W I N F B N Y P V T T
  M Z F P K W G D K Z X T J C D I G K U H U A U
  E K C A R

the seven checks every move keeps (place(carved) + place(known) equal within a column):
  column 0: R+S (24) = M+C (70)
  column 1: V+T (25) = Z+L (71)
  column 2: Q+N (26) = F+O (72)
  column 3: Q+O (27) = P+C (73)
  column 4: P+R (28) = K+K (74)
  column 21: F+E (22) = T+I (68)
  column 22: L+A (23) = T+N (69)

best alphabet on K4: UTVXRSWEPNHFLZDAOQBJICKGYM
key values: [7, 12, 5, 19, 4, 11, 10, 6, 23, 15, 7, 1, 5, 12, 14, 21, 10, 20, 25, 1, 3, 18, 1, 9, 3, 0]
place 22: carved F at 11, key 18: 18 - 11 = 7 -> E
place 64: carved N at 9, key 1: 1 - 9 = 18 -> B
```

## Lineage

Inherits from 0140-k4-against-its-own-copies-with-the-tempering-climb. What changed: F1.1 Beaufort 26, rerun alone after 0141 crashed (its two-alphabet part ran out of time while drawing fitting shuffles, and a text with no finished search broke the summary; no result survived). Same test as 0141's first part: 0140 found design 2 has power at 26 (5 of 6 planted texts beat all 6 of their own copies), so K4 runs against 12 shuffles of itself that fit at 26.

## Hypothesis (domain expert)

C27(c), C1(b). One unknown alphabet on both sides, Beaufort form x(c_i) + x(p_i) = k[i mod 26], 1 check (0119). Search: 0139's compiled parallel tempering in the set where the check holds, 10 runs x 16 replicas x 625 rounds x 1,000 moves per text, full-text quadgram mean. K4 vs 12 shuffles of K4 fitting at 26 (0119's decider, seed 142). Rule fixed before the run: K4 above all 12 stops the queue for a replication; otherwise the cell closes sampled at the measured power (5 of 6 at 6 copies, 0140).

## Prediction

K4 inside its copies (rank 2-13); the Beaufort-26 cell closes sampled at power about 0.8. No reading.

## Method

1. Draw 12 shuffles of K4 fitting at 26.
2. Run 0139's search on all 13 texts.
3. K4's rank; its best reading returned with the copies' English scores as controls.

## Result

Candidates returned: 1. Passed all gates: 0. Best crib hits among all candidates: 24/24
(EAST 4/4, NORTHEAST 9/9, BERLIN 6/6, CLOCK 5/5).
Best loss: 4.173335239079099 (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | baseline | 24/24 | -7.422 | `QINARCEOUSEAZEYNONENGEASTNORTHEASTEDTUDECRSABSOSCIVEFUSSHKRLDRABERLINCLOCKCLARINRUNGONTAGTOLEMASC` | Beaufort form, one alphabet UTVXRSWEPNHFLZDAOQBJICKGYM on both sides, key length 26 |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "one free alphabet, Beaufort form, key length 26: K4 vs 12 of its own fitting copies (design 2)",
 "search": "parallel tempering, 10 runs x 16 replicas x 625 rounds x 1000 moves per text, T 0.1->0.002; two-alphabet runs start from an exact witness (0123) randomised by 400 check-keeping swaps",
 "not_exhaustive": true,
 "runs_done": {
  "min": 10,
  "max": 10
 },
 "c_decryption_checked": true,
 "L26": {
  "k4": {
   "score": -4.9903,
   "plaintext": "QINARCEOUSEAZEYNONENGEASTNORTHEASTEDTUDECRSABSOSCIVEFUSSHKRLDRABERLINCLOCKCLARINRUNGONTAGTOLEMASC",
   "alphabet": "UTVXRSWEPNHFLZDAOQBJICKGYM",
   "key": [
    7,
    12,
    5,
    19,
    4,
    11,
    10,
    6,
    23,
    15,
    7,
    1,
    5,
    12,
    14,
    21,
    10,
    20,
    25,
    1,
    3,
    18,
    1,
    9,
    3,
    0
   ],
   "english_free": -5.23
  },
  "coppers": [
   -5.0511,
   -4.9275,
   -4.9134,
   -4.9108,
   -4.9003,
   -4.8917,
   -4.8625,
   -4.8347,
   -4.8166,
   -4.8027,
   -4.7829,
   -4.6881
  ],
  "k4_rank_of_13": 12,
  "k4_above_all_copies": false,
  "power_measured_0140": "5 of 6 planted texts beat all 6 own copies"
 },
 "quagmire_iv_power": {},
 "q4_bar": ">= 3 of 4 plants beat all 5 own copies (null 0.67)",
 "stop_queue": false,
 "controls": "12 shuffles of K4 fitting at 26 (seed 142)"
}
```

Notes: L26: K4 -4.990, rank 12 of 13 (-5.051 to -4.688); stop False.


