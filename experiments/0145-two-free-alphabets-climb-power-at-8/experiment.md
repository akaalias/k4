# 0145-two-free-alphabets-climb-power-at-8: F1.2 at key length 8: design 2 on two free alphabets, its power on planted English against copies that keep the known places (0143's unfinished cell)

**Family:** 1-keyed-periodic  
**Parent:** 0143-two-free-alphabets-climb-power  
**Decision:** reverted  
**Run:** 2026-10-16T19:58:28+00:00, 698.2 s, status ran  
**Time by phase:** unattributed 20 s, run 698 s, record 0 s

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

Inherits from 0143-two-free-alphabets-climb-power. What changed: F1.2 at length 8 alone. In 0143 the length-8 texts ran last and 27 of 30 finished no search before the deadline, so that cell had no verdict. Same search, same copies (carved letters kept at the 24 known places), sized to finish: 4 planted texts, 4 copies each (20 texts at about 200-400 s each).

## Hypothesis (domain expert)

C27(c) (the 'slightly different' tableau), C1(b). Model: 0123's Quagmire IV, two unknown bijections P, C, key length 8, 16 checks. Search: replica exchange, 16 replicas, T 0.1 -> 0.002, 10 runs x 625 rounds x 1,000 moves per text (0139's effort), moves swap two places in one alphabet, repaired by a second swap when a check breaks; full-text quadgram mean. Power: 4 planted texts (seed 145), each against 4 copies keeping the 24 known places (seed 1451); null 1/5 per plant (0.8 of 4). Bar fixed before the run: at least 3 of 4 beat all their own copies. A passing length gets K4 against copies of K4 kept the same way in the next run; a failing length stays blocked (no power).

## Prediction

With 16 checks the climb is held tightest; at least 3 of 4 plants beat all their own copies (13 and 16 passed in 0143). No planted text recovered. Zero candidates.

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
  "min": 10,
  "max": 10
 },
 "texts_with_no_finished_run": 0,
 "c_decryption_checked": true,
 "copies": "keep the carved letters at the 24 known places, shuffle the other 73 (fit by construction)",
 "bar": ">= 3 of 4 plants beat all 4 own copies (null 0.80)",
 "by_length": {
  "8": {
   "checks": 16,
   "found": 4,
   "passes_bar": true,
   "rows": [
    {
     "score": -5.2996,
     "letters_right": 41,
     "runs": 10,
     "own_copies": [
      -5.8523,
      -5.7844,
      -5.6114,
      -5.5397
     ],
     "rank_among_own": 1,
     "found_own": true,
     "recovered": false
    },
    {
     "score": -5.3115,
     "letters_right": 39,
     "runs": 10,
     "own_copies": [
      -5.9513,
      -5.9304,
      -5.7284,
      -5.4626
     ],
     "rank_among_own": 1,
     "found_own": true,
     "recovered": false
    },
    {
     "score": -5.2386,
     "letters_right": 47,
     "runs": 10,
     "own_copies": [
      -5.6438,
      -5.5749,
      -5.4806,
      -5.2716
     ],
     "rank_among_own": 1,
     "found_own": true,
     "recovered": false
    },
    {
     "score": -5.251,
     "letters_right": 43,
     "runs": 10,
     "own_copies": [
      -5.7065,
      -5.5038,
      -5.489,
      -5.3695
     ],
     "rank_among_own": 1,
     "found_own": true,
     "recovered": false
    }
   ]
  }
 },
 "controls": "per plant, 4 kept-place copies (seed 1451)"
}
```

Notes: Quagmire IV power: L8 4/4 (16 checks); runs per text 10-10


