# 0146-k4-two-free-alphabets-at-8: F1.2 decided at key length 8 with design 2 on two free alphabets: K4 against 12 copies of itself that keep the known places

**Family:** 1-keyed-periodic  
**Parent:** 0145-two-free-alphabets-climb-power-at-8  
**Decision:** reverted  
**Run:** 2026-10-16T20:10:33+00:00, 405.9 s, status ran  
**Time by phase:** unattributed 27 s, run 406 s, record 0 s

## In plain words

With two scrambled alphabets, one for the message and one for the carved letters, the search noticed planted English every time at key length 8. Now it runs on the carved text at that length, against copies of the carved text that keep the letters at the 24 known places and scramble the rest.

## Walkthrough, by hand

1. Find one pair of alphabets that gives K4's 24 known letters at key length 8.
2. Make 12 copies of K4 that keep the carved letters at the known places and shuffle the other 73; the same pair of alphabets fits them.
3. Run the search from that pair on K4 and on each copy, keeping the checks, scoring the whole text as English.
4. K4 anywhere inside the pack closes the length at the measured strength.

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

Inherits from 0145-two-free-alphabets-climb-power-at-8. What changed: F1.2 at 8, the last of F1.2's three cells under 0136's bound. 0145 measured design 2 on two free alphabets at length 8 (16 checks): planted English beat all four of its kept-place copies 4 times in 4. K4 now runs at 8 against 12 copies of K4 made the same way, from K4's exact witness, as 0144 did at 13 and 16.

## Hypothesis (domain expert)

C27(c), C1(b). Model: 0123's Quagmire IV, C(c) = P(p) + k[i mod L], two unknown bijections, L 8 (16 checks); 0123 found K4 consistent at 8. Search: 0143's compiled tempering over both alphabets, 10 runs x 16 replicas x 625 rounds x 1,000 moves per text, start from an exact witness randomised by 400 check-keeping swaps. Copies: K4's carved letters kept at the 24 known places, the other 73 shuffled (seed 146); they share K4's witness. Rule fixed before the run: K4 above all 12 copies at a length stops the queue for replication; otherwise that length closes, sampled at the power measured in 0145 (4/4 against 4 copies).

## Prediction

K4 inside its copies; F1.2 at 8 closes sampled. No reading.

## Method

1. K4's exact witness at 8 (0123's decider); 12 kept-place copies of K4.
2. The compiled two-alphabet search on all 26 texts.
3. K4's rank per length; its best reading per length returned with the copies' scores as controls.

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
 "family": "two free alphabets (Quagmire IV), key length 8, no move: K4 against 12 kept-place copies of itself (design 2)",
 "search": "parallel tempering, 10 runs x 16 replicas x 625 rounds x 1000 moves per text; start from K4's exact witness (0123) randomised by 400 check-keeping swaps",
 "not_exhaustive": true,
 "runs_done": {
  "min": 10,
  "max": 10
 },
 "texts_with_no_finished_run": 0,
 "c_decryption_checked": true,
 "by_length": {
  "8": {
   "k4": {
    "score": -5.3391,
    "plaintext": "ZEMYBMWDBURGHAPTGCWEDEASTNORTHEASTYIDWCKUNDTOFLYPSHAYKINGSADVERBERLINCLOCKAVEFLIVATQUODEMOGOOFGLA",
    "english_free": -5.7126,
    "runs": 10
   },
   "copies": [
    -5.7181,
    -5.6145,
    -5.5193,
    -5.5123,
    -5.5076,
    -5.5048,
    -5.468,
    -5.4558,
    -5.4364,
    -5.4188,
    -5.3533,
    -5.2338
   ],
   "k4_rank_of_13": 2,
   "k4_above_all_copies": false
  }
 },
 "stop_queue": false,
 "power_measured_0145": {
  "8": "4 of 4 against 4 kept-place copies"
 },
 "controls": "12 kept-place copies of K4 per length (seed 146)"
}
```

Notes: L8: K4 -5.339 rank 2 of 13; stop False


