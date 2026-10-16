# 0143-two-free-alphabets-climb-power: F1.2: design 2 carried to two free alphabets (Quagmire IV), its power measured on planted English at key lengths 8, 13 and 16 against copies that keep the known places

**Family:** 1-keyed-periodic  
**Parent:** 0139-parallel-tempering-climb-against-own-copies  
**Decision:** reverted  
**Run:** 2026-10-16T19:15:34+00:00, 1727.6 s, status ran  
**Time by phase:** unattributed 19 s, run 1728 s, record 0 s

## In plain words

The search that notices planted English under one scrambled alphabet is extended to two scrambled alphabets, one for the message and one for the carved letters, and checked on planted English at three key lengths. Each planted message is compared with copies that keep the letters at the 24 known places and scramble the rest, so only the order of the other letters differs. If it notices the English often enough, it may judge the carved text at that length.

## Walkthrough, by hand

1. Encipher a passage of English with two random alphabets and a random key of length 8, known words in place.
2. Make five copies that keep the carved letters at the 24 known places and shuffle the other 73.
3. Find one pair of alphabets that gives all 24 known letters; it works for the copies too, since their known places are the same.
4. Run sixteen searches side by side from that pair, swapping letters within either alphabet while every check holds, scoring the whole text as English.
5. The planted text is noticed if it beats all five copies; luck gives that one time in six.

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
```

## Lineage

Inherits from 0139-parallel-tempering-climb-against-own-copies. What changed: F1.2, the second half of 0141, which crashed. Design 2 (parallel tempering in the set that keeps every known-letter check) over two independent alphabets, C(c) = P(p) + k, at the three lengths 0136 leaves under the quadgram bound (open bits 89, 112, 126 against 130). Controls changed for cost: 0141 drew fully shuffled copies that fit, but the exact two-alphabet decider takes minutes per shuffle; here each copy keeps the plant's carved letters at the 24 known places and shuffles the other 73, so it fits by construction and differs from the plant only in the order of the letters the English test reads. Every text starts from the plant's exact witness (0123's decider), randomised by 400 check-keeping swaps; a text whose search finishes no run is reported, not dropped.

## Hypothesis (domain expert)

C27(c) (the 'slightly different' tableau), C1(b). Model: 0123's Quagmire IV, two unknown bijections P, C, key length L in {8, 13, 16}, checks 16, 11, 8. Search: replica exchange, 16 replicas, T 0.1 -> 0.002, 10 runs x 625 rounds x 1,000 moves per text (0139's effort), moves swap two places in one alphabet, repaired by a second swap when a check breaks; full-text quadgram mean. Power: 5 planted texts per length (Carter windows, seed 143), each against 5 copies keeping the 24 known places (seed 1431); null 1/6 per plant (0.83 of 5). Bar fixed before the run: at least 4 of 5 beat all their own copies. A passing length gets K4 against copies of K4 kept the same way in the next run; a failing length stays blocked (no power).

## Prediction

Power falls with the number of checks and the doubled freedom: at least 4 of 5 at length 8 (16 checks), fewer at 13 and 16. No planted text recovered. Zero candidates.

## Method

1. 5 planted Quagmire IV texts per length and 5 kept-place copies of each.
2. 0123's decider gives each plant an exact witness; it starts the plant and its copies.
3. The compiled two-alphabet tempering search on all 90 texts; decryption checked against Python.
4. Per length: plants beating all their own copies.

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
 "family": "two free alphabets (Quagmire IV), periodic key 8, 13, 16, no move: power of design 2 on planted English",
 "search": "parallel tempering, 10 runs x 16 replicas x 625 rounds x 1000 moves per text, T 0.1->0.002; start from the plant's exact witness (0123) randomised by 400 check-keeping swaps",
 "not_exhaustive": true,
 "runs_done": {
  "min": 0,
  "max": 10
 },
 "texts_with_no_finished_run": 27,
 "c_decryption_checked": true,
 "copies": "keep the carved letters at the 24 known places, shuffle the other 73 (fit by construction)",
 "bar": ">= 4 of 5 plants beat all 5 own copies (null 0.83)",
 "by_length": {
  "8": {
   "checks": 16,
   "found": 1,
   "passes_bar": false,
   "rows": [
    {
     "score": -5.239,
     "letters_right": 39,
     "runs": 4,
     "own_copies": [
      -99.0,
      -99.0,
      -99.0,
      -5.8206,
      -5.5762
     ],
     "rank_among_own": 1,
     "found_own": true,
     "recovered": false
    },
    {
     "score": -99.0,
     "letters_right": null,
     "runs": 0,
     "own_copies": [
      -99.0,
      -99.0,
      -99.0,
      -99.0,
      -99.0
     ],
     "rank_among_own": 1,
     "found_own": false,
     "recovered": false
    },
    {
     "score": -99.0,
     "letters_right": null,
     "runs": 0,
     "own_copies": [
      -99.0,
      -99.0,
      -99.0,
      -99.0,
      -99.0
     ],
     "rank_among_own": 1,
     "found_own": false,
     "recovered": false
    },
    {
     "score": -99.0,
     "letters_right": null,
     "runs": 0,
     "own_copies": [
      -99.0,
      -99.0,
      -99.0,
      -99.0,
      -99.0
     ],
     "rank_among_own": 1,
     "found_own": false,
     "recovered": false
    },
    {
     "score": -99.0,
     "letters_right": null,
     "runs": 0,
     "own_copies": [
      -99.0,
      -99.0,
      -99.0,
      -99.0,
      -99.0
     ],
     "rank_among_own": 1,
     "found_own": false,
     "recovered": false
    }
   ]
  },
  "13": {
   "checks": 11,
   "found": 5,
   "passes_bar": true,
   "rows": [
    {
     "score": -4.675,
     "letters_right": 41,
     "runs": 10,
     "own_copies": [
      -4.9297,
      -4.8314,
      -4.8109,
      -4.7382,
      -4.6822
     ],
     "rank_among_own": 1,
     "found_own": true,
     "recovered": false
    },
    {
     "score": -4.7332,
     "letters_right": 45,
     "runs": 10,
     "own_copies": [
      -4.9928,
      -4.989,
      -4.9874,
      -4.9283,
      -4.8092
     ],
     "rank_among_own": 1,
     "found_own": true,
     "recovered": false
    },
    {
     "score": -4.719,
     "letters_right": 35,
     "runs": 10,
     "own_copies": [
      -4.9267,
      -4.9209,
      -4.8982,
      -4.8543,
      -4.7561
     ],
     "rank_among_own": 1,
     "found_own": true,
     "recovered": false
    },
    {
     "score": -4.5159,
     "letters_right": 39,
     "runs": 10,
     "own_copies": [
      -4.8307,
      -4.8269,
      -4.8222,
      -4.71,
      -4.7069
     ],
     "rank_among_own": 1,
     "found_own": true,
     "recovered": false
    },
    {
     "score": -4.5796,
     "letters_right": 47,
     "runs": 10,
     "own_copies": [
      -5.0164,
      -4.9968,
      -4.9784,
      -4.8322,
      -4.7878
     ],
     "rank_among_own": 1,
     "found_own": true,
     "recovered": false
    }
   ]
  },
  "16": {
   "checks": 8,
   "found": 4,
   "passes_bar": true,
   "rows": [
    {
     "score": -4.5624,
     "letters_right": 39,
     "runs": 10,
     "own_copies": [
      -4.6937,
      -4.6768,
      -4.6354,
      -4.616,
      -4.6153
     ],
     "rank_among_own": 1,
     "found_own": true,
     "recovered": false
    },
    {
     "score": -4.5407,
     "letters_right": 35,
     "runs": 10,
     "own_copies": [
      -4.7296,
      -4.7002,
      -4.6591,
      -4.6291,
      -4.5307
     ],
     "rank_among_own": 2,
     "found_own": false,
     "recovered": false
    },
    {
     "score": -4.553,
     "letters_right": 32,
     "runs": 10,
     "own_copies": [
      -4.7538,
      -4.6894,
      -4.6559,
      -4.6366,
      -4.5878
     ],
     "rank_among_own": 1,
     "found_own": true,
     "recovered": false
    },
    {
     "score": -4.5669,
     "letters_right": 42,
     "runs": 10,
     "own_copies": [
      -4.6822,
      -4.6267,
      -4.6188,
      -4.6187,
      -4.6155
     ],
     "rank_among_own": 1,
     "found_own": true,
     "recovered": false
    },
    {
     "score": -4.3647,
     "letters_right": 52,
     "runs": 10,
     "own_copies": [
      -4.645,
      -4.6047,
      -4.5702,
      -4.5613,
      -4.4653
     ],
     "rank_among_own": 1,
     "found_own": true,
     "recovered": false
    }
   ]
  }
 },
 "controls": "per plant, 5 kept-place copies (seed 1431)"
}
```

Notes: Quagmire IV power: L8 1/5 (16 checks), L13 5/5 (11 checks), L16 4/5 (8 checks); runs per text 0-10


