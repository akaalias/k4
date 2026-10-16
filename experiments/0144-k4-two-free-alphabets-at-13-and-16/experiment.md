# 0144-k4-two-free-alphabets-at-13-and-16: F1.2 decided at key lengths 13 and 16 with design 2 on two free alphabets: K4 against 12 copies of itself that keep the known places

**Family:** 1-keyed-periodic  
**Parent:** 0143-two-free-alphabets-climb-power  
**Decision:** reverted  
**Run:** 2026-10-16T19:45:23+00:00, 765.4 s, status ran  
**Time by phase:** unattributed 61 s, run 765 s, record 0 s

## In plain words

With two scrambled alphabets, one for the message and one for the carved letters, the search noticed planted English nearly every time at key lengths 13 and 16. Now it runs on the carved text at those lengths, against copies of the carved text that keep the letters at the 24 known places and scramble the rest.

## Walkthrough, by hand

1. Find one pair of alphabets that gives K4's 24 known letters at key length 13.
2. Make 12 copies of K4 that keep the carved letters at the known places and shuffle the other 73; the same pair of alphabets fits them.
3. Run the search from that pair on K4 and on each copy, keeping the checks, scoring the whole text as English.
4. K4 anywhere inside the pack closes the length at the measured strength. Repeat at 16.

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

Inherits from 0143-two-free-alphabets-climb-power. What changed: F1.2 at 13 and 16. 0143 measured design 2 on two free alphabets (Quagmire IV): planted English beat all five of its kept-place copies 5 of 5 times at 13 and 4 of 5 at 16 (bar 4); length 8 did not finish. Here K4 runs at 13 and 16 against 12 copies of K4 made the same way (carved letters kept at the 24 known places, the other 73 shuffled), from K4's own exact witness (0123's decider).

## Hypothesis (domain expert)

C27(c), C1(b). Model: 0123's Quagmire IV, C(c) = P(p) + k[i mod L], two unknown bijections, L 13 (11 checks) and 16 (8 checks); 0123 found K4 consistent at both. Search: 0143's compiled tempering over both alphabets, 10 runs x 16 replicas x 625 rounds x 1,000 moves per text, start from an exact witness randomised by 400 check-keeping swaps. Copies: K4's carved letters kept at the 24 known places, the other 73 shuffled (seed 144); they share K4's witness. Rule fixed before the run: K4 above all 12 copies at a length stops the queue for replication; otherwise that length closes, sampled at the power measured in 0143 (5/5 at 13, 4/5 at 16, against 5 copies).

## Prediction

K4 inside its copies at both lengths; F1.2 at 13 and 16 closes sampled. No reading.

## Method

1. K4's exact witness at 13 and at 16 (0123's decider); 12 kept-place copies of K4 per length.
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
 "family": "two free alphabets (Quagmire IV), key length 13 and 16, no move: K4 against 12 kept-place copies of itself (design 2)",
 "search": "parallel tempering, 10 runs x 16 replicas x 625 rounds x 1000 moves per text; start from K4's exact witness (0123) randomised by 400 check-keeping swaps",
 "not_exhaustive": true,
 "runs_done": {
  "min": 10,
  "max": 10
 },
 "texts_with_no_finished_run": 0,
 "c_decryption_checked": true,
 "by_length": {
  "13": {
   "k4": {
    "score": -5.116,
    "plaintext": "DBUGHHPROLEITEDREOFVIEASTNORTHEASTLYOWNENWASINENOHWCITAFFMYSBURBERLINCLOCKOBAYGUIORYFAKELYUSFUMWO",
    "english_free": -5.4156,
    "runs": 10
   },
   "copies": [
    -5.0336,
    -5.0059,
    -4.9846,
    -4.9762,
    -4.9579,
    -4.957,
    -4.9351,
    -4.9216,
    -4.9167,
    -4.852,
    -4.8433,
    -4.8039
   ],
   "k4_rank_of_13": 13,
   "k4_above_all_copies": false
  },
  "16": {
   "k4": {
    "score": -4.6694,
    "plaintext": "KDOWBOOFGOLPREATINCEREASTNORTHEASTYIRTIDONTTOSTENEETSBEIPHYAVAMBERLINCLOCKYWASTILINGLDPREVELOSINP",
    "english_free": -4.8738,
    "runs": 10
   },
   "copies": [
    -4.7664,
    -4.7276,
    -4.711,
    -4.7105,
    -4.7047,
    -4.6997,
    -4.6504,
    -4.6451,
    -4.6342,
    -4.6308,
    -4.6252,
    -4.6016
   ],
   "k4_rank_of_13": 7,
   "k4_above_all_copies": false
  }
 },
 "stop_queue": false,
 "power_measured_0143": {
  "13": "5 of 5 against 5 kept-place copies",
  "16": "4 of 5"
 },
 "controls": "12 kept-place copies of K4 per length (seed 144)"
}
```

Notes: L13: K4 -5.116 rank 13 of 13; L16: K4 -4.669 rank 7 of 13; stop False


