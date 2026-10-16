# 0140-k4-against-its-own-copies-with-the-tempering-climb: F1.1 decided with F1.5's design 2: K4 against 12 scrambled copies of itself at key length 23 (one free alphabet, Beaufort form); design 2's power at length 26

**Family:** 1-keyed-periodic  
**Parent:** 0139-parallel-tempering-climb-against-own-copies  
**Decision:** reverted  
**Run:** 2026-10-16T18:25:55+00:00, 760.5 s, status ran  
**Time by phase:** unattributed 179 s, run 760 s, record 40 s

## In plain words

We finally have a search that, on planted messages, tells hidden English from its own scrambled letters about three times in four for one kind of cipher (one scrambled alphabet, a 23-letter key, used the Beaufort way). Now it runs on the carved text itself, against scrambled copies of the carved text. If the carved text were this kind of cipher, the search would usually rank it first. We also check whether the search works for a 26-letter key, where the known letters give only one check.

## Walkthrough, by hand

1. Write K4 in rows of 23; each column is one key slot; seven columns hold two known letters.
2. Run sixteen searches side by side over alphabets that keep those seven pairs consistent, swapping states between bold and cautious searches, and keep the best English score.
3. Shuffle K4's letters into 12 new orders that could still give the 24 known letters, and run the same search on each.
4. If K4 were English enciphered this way, it would usually come first; if it comes anywhere inside the pack, this cell is closed at the measured strength.
5. Do the same check of strength at 26 letters on planted English.

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

best alphabet on K4: RTKDPNVSXJQMUAZGOBILEYCHWF
key values: [7, 7, 15, 0, 4, 1, 2, 9, 15, 14, 8, 13, 14, 25, 21, 25, 12, 22, 15, 4, 25, 19, 6]
place 22: carved F at 25, key 19: 19 - 25 = 20 -> E
place 64: carved N at 5, key 22: 22 - 5 = 17 -> B
```

## Lineage

Inherits from 0139-parallel-tempering-climb-against-own-copies. What changed: F1.5 step 3 and F1.1. Design 2 (0139) noticed planted English against shuffles of itself 6 times in 8. Here it runs on K4 and on 12 shuffles of K4 that fit length 23 exactly, the like-for-like comparison 0138 showed is needed, so F1.1's Beaufort-23 cell gets a verdict at stated power. In the same run, design 2's power at length 26 (one check) is measured as in 0139: 6 planted texts, each against 6 fitting shuffles of itself.

## Hypothesis (domain expert)

C27(c) (a tableau 'slightly different from the one on Kryptos', clue register), C1(b) (the table alone). Model as 0137: one unknown alphabet on both sides, Beaufort form x(c_i) + x(p_i) = k[i mod L], L 23 (7 checks) and 26 (1 check), the only (form, length) pairs 0119 left. Search: 0139's compiled parallel tempering in the set where every check holds (10 runs x 16 replicas x 625 rounds x 1,000 moves, T 0.1 -> 0.002), full-text quadgram mean. L23: K4 and 12 shuffles of K4 that fit exactly (0119's decider, seed 140). Measured power (0139): a planted Beaufort-23 text beat all 6 of its own shuffles 6 times in 8; against 12 the power is lower, about 0.5-0.75. Verdict rule fixed before the run: K4 above all 12 of its copies stops the queue for a replication with fresh copies; otherwise the cell is closed, sampled at the stated power (false alarm rate 1/13). L26 power: 6 plants (seed 1400) x 6 own fitting shuffles; bar 5 of 6; if met, K4 at 26 is the next run, otherwise the 26 cell stays blocked.

## Prediction

K4 is not above all 12 of its copies at length 23 (inside the range), so F1.1 Beaufort 23 closes, sampled at power about 0.6. At 26, fewer than 5 of 6 planted texts beat all their own copies (one check gives the climb little to hold), so the 26 cell stays blocked. No reading. One candidate (K4's best at 23) carried to the gates with its copies as controls; it will not pass.

## Method

1. Draw 12 shuffles of K4 that fit length 23 exactly; draw 6 planted texts at length 26 and 6 fitting shuffles of each.
2. Run 0139's search on all 55 texts at equal effort.
3. L23: K4's rank among its 12 copies. L26: plants beating all their own copies.
4. Return K4's best L23 reading with the copies' English scores (free letters) as controls.

## Result

Candidates returned: 1. Passed all gates: 0. Best crib hits among all candidates: 24/24
(EAST 4/4, NORTHEAST 9/9, BERLIN 6/6, CLOCK 5/5).
Best loss: 3.983798779321207 (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | baseline | 24/24 | -7.322 | `BOARIMELRBCEHINVEHWATEASTNORTHEASTHATEGNANHIFPLLBADIRODMOROSORYBERLINCLOCKDAVARRUNDISHEDSAVEANLAP` | Beaufort form, one alphabet RTKDPNVSXJQMUAZGOBILEYCHWF on both sides, key length 23 |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "one unknown alphabet on both sides, Beaufort form, no move: K4 at key length 23 against its own copies; design 2's power at 26",
 "search": "parallel tempering (0139), 10 runs x 16 replicas x 625 rounds x 1000 moves per text, T 0.1->0.002",
 "not_exhaustive": true,
 "runs_done": {
  "min": 10,
  "max": 10
 },
 "c_decryption_checked": true,
 "L23": {
  "k4": {
   "score": -4.9891,
   "plaintext": "BOARIMELRBCEHINVEHWATEASTNORTHEASTHATEGNANHIFPLLBADIRODMOROSORYBERLINCLOCKDAVARRUNDISHEDSAVEANLAP",
   "alphabet": "RTKDPNVSXJQMUAZGOBILEYCHWF",
   "key": [
    7,
    7,
    15,
    0,
    4,
    1,
    2,
    9,
    15,
    14,
    8,
    13,
    14,
    25,
    21,
    25,
    12,
    22,
    15,
    4,
    25,
    19,
    6
   ],
   "english_free": -5.2755,
   "runs": 10
  },
  "coppers": [
   -5.1369,
   -5.1088,
   -5.066,
   -5.0613,
   -4.9486,
   -4.9439,
   -4.9273,
   -4.924,
   -4.9086,
   -4.895,
   -4.8572,
   -4.8326
  ],
  "k4_rank_of_13": 9,
  "k4_above_all_copies": false,
  "power_measured_0139": "6 of 8 planted texts beat all 6 own copies",
  "false_alarm_rate": 0.077
 },
 "L26_power": {
  "plants": 6,
  "own_coppers_per_plant": 6,
  "found": 5,
  "bar": ">= 5 of 6",
  "passes_bar": true,
  "null_expected": 0.86,
  "rows": [
   {
    "score": -4.782,
    "letters_right": 34,
    "true_score": -4.2931,
    "runs": 10,
    "own_coppers": [
     -5.0523,
     -5.0204,
     -4.9084,
     -4.8891,
     -4.8738,
     -4.8376
    ],
    "rank_among_own": 1,
    "found_own": true,
    "recovered": false
   },
   {
    "score": -4.7582,
    "letters_right": 35,
    "true_score": -4.3151,
    "runs": 10,
    "own_coppers": [
     -4.9262,
     -4.9212,
     -4.8524,
     -4.8503,
     -4.7999,
     -4.7665
    ],
    "rank_among_own": 1,
    "found_own": true,
    "recovered": false
   },
   {
    "score": -4.6909,
    "letters_right": 39,
    "true_score": -4.4263,
    "runs": 10,
    "own_coppers": [
     -4.9664,
     -4.9582,
     -4.9268,
     -4.8455,
     -4.8218,
     -4.8061
    ],
    "rank_among_own": 1,
    "found_own": true,
    "recovered": false
   },
   {
    "score": -4.7186,
    "letters_right": 36,
    "true_score": -4.2785,
    "runs": 10,
    "own_coppers": [
     -4.9963,
     -4.962,
     -4.9576,
     -4.9328,
     -4.9216,
     -4.7998
    ],
    "rank_among_own": 1,
    "found_own": true,
    "recovered": false
   },
   {
    "score": -4.9001,
    "letters_right": 33,
    "true_score": -4.3764,
    "runs": 10,
    "own_coppers": [
     -4.9369,
     -4.9135,
     -4.8763,
     -4.867,
     -4.7901,
     -4.7788
    ],
    "rank_among_own": 5,
    "found_own": false,
    "recovered": false
   },
   {
    "score": -4.702,
    "letters_right": 44,
    "true_score": -4.2656,
    "runs": 10,
    "own_coppers": [
     -4.9561,
     -4.9274,
     -4.8231,
     -4.8187,
     -4.766,
     -4.7232
    ],
    "rank_among_own": 1,
    "found_own": true,
    "recovered": false
   }
  ]
 },
 "stop_queue": false,
 "controls": "12 shuffles of K4 that fit length 23 exactly (0119's decider, seed 140); at 26 each plant's own fitting shuffles (seed 1400)"
}
```

Notes: L23: K4 -4.989, rank 9 of 13 among its own copies (-5.137 to -4.833); stop queue False. L26 power: 5/6 plants beat all 6 own copies (null 0.86, bar 5).


