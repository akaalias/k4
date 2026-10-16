# 0148-k1-k2-system-with-a-slip-at-33: F1.6, the revived cell: K1 and K2's own system (one free alphabet, added form) at key length 19 with the carved S at place 33 taken as a slip; design 2's power on planted texts and K4 against its copies

**Family:** 1-keyed-periodic  
**Parent:** 0147-one-carved-letter-wrong-through-the-free-alphabet-tests  
**Decision:** reverted  
**Run:** 2026-10-16T20:33:23+00:00, 914.6 s, status ran  
**Time by phase:** unattributed 120 s, run 915 s, record 44 s

## In plain words

K1 and K2 were made with the table and a scrambled alphabet; the same method on K4 is ruled out only because two carved letters equal the message letters above them. If the S at place 33 is a slip of the chisel, the method comes back to life at a key length of 19. We let the search that tells hidden English from scrambled letters judge that one case, after checking on planted messages that it can.

## Walkthrough, by hand

1. Write K4 in rows of 19; each column is one key slot.
2. Leave place 33 out: its carved S is taken as a slip.
3. For every other known letter: place(carved) = place(known) + key value of its column, in one unknown alphabet.
4. Search alphabets that keep these equations, sixteen searches side by side, scoring the whole text as English, with S at 33.
5. Do the same on copies of K4 that keep the known places' carved letters and shuffle the rest, and on planted English.

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

best alphabet on K4: OVLIGSMJAZBFDXNCYPQRTWUHEK
key values: [10, 2, 13, 20, 14, 7, 4, 18, 24, 25, 17, 6, 17, 7, 11, 2, 0, 23, 6]
place 22: carved F at 11, key 13: 13 - 11 = 2 -> L
place 64: carved N at 14, key 4: 4 - 14 = 16 -> Y
```

## Lineage

Inherits from 0147-one-carved-letter-wrong-through-the-free-alphabet-tests. What changed: F1.6. 0147 found that replacing the carved S at 33 (S under S) revives K1 and K2's system with a free alphabet at key length 19, for 25 of the possible replacements, the one cell where K4 stood above every scrambled copy in that model (25 against at most 23; inside the multiple-comparison null overall). The exact test cannot judge it further. Here place 33's carved letter is treated as unknown (its equation dropped, the message letter S kept), and 0139's English decider, rewritten for the added form, judges the cell: power on 5 planted texts against copies of themselves, and K4 against 12 copies of itself, in one run.

## Hypothesis (domain expert)

C17(b), family G (a slip of the chisel, as K2's dropped letter and UNDERGRUUND), C27(c), C1(b): K1 and K2 are Quagmire III on the KRYPTOS alphabet (knowledge/01-facts.md); with a free alphabet the added form x(c) = x(p) + k[i mod L] dies at every length 1-26 only because S under S (33) and K under K (74) force key 0 in shared slots (0119). Model here: same, L 19, place 33's carved letter unknown (23 equations; its message letter is S). Search: 0139's compiled parallel tempering, check-keeping moves, added form, 10 runs x 16 replicas x 625 rounds x 1,000 moves per text. Power: 5 planted texts (Carter windows, random alphabet and key, added form, the carved letter at 33 then replaced by a random other letter; seed 148), each against 4 kept-place copies (carved letters kept at the 24 known places, other 73 shuffled; seed 1481); bar fixed before the run: at least 4 of 5 beat all their copies (luck 0.2 each). K4 against 12 kept-place copies (seed 1482); K4 above all 12 stops the queue for a replication; otherwise, if the bar is met, the cell closes sampled at that power, and if not, it stays blocked.

## Prediction

The decider has power here (at least 4 of 5 planted texts beat their copies: 23 equations, 4 checks); K4 sits inside its 12 copies, so the cell closes. No reading.

## Method

1. Compile the added-form search; check its decryption against Python.
2. 5 planted texts with a slip at 33, 4 kept-place copies each; K4 and 12 kept-place copies.
3. The search on all 38 texts, place 33 left out of the equations and read as S.
4. Plants beating all their copies; K4's rank among its copies.

## Result

Candidates returned: 1. Passed all gates: 0. Best crib hits among all candidates: 24/24
(EAST 4/4, NORTHEAST 9/9, BERLIN 6/6, CLOCK 5/5).
Best loss: 3.9320463881078194 (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | baseline | 24/24 | -7.348 | `YADKARZAMESURECOINGOREASTNORTHEASTETENAITEPETJFBGLIONOUCHERYTHIBERLINCLOCKEELHURMOFTSSAYMCHTELZEP` | added form, one alphabet OVLIGSMJAZBFDXNCYPQRTWUHEK, key length 19, carved letter at 33 read as a slip |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "one free alphabet, added form (K1/K2's system), key length 19, carved letter at place 33 taken as a slip (equation dropped, S kept)",
 "search": "parallel tempering (0139) in the added form, 10 runs x 16 replicas x 625 rounds x 1000 moves per text",
 "not_exhaustive": true,
 "runs_done": {
  "min": 10,
  "max": 10
 },
 "c_decryption_checked": true,
 "power": {
  "plants": 5,
  "copies_each": 4,
  "found": 3,
  "bar": ">= 4 of 5",
  "passes_bar": false,
  "null_expected": 1.0,
  "rows": [
   {
    "score": -4.2033,
    "letters_right": 97,
    "own_copies": [
     -5.2063,
     -5.145,
     -5.1365,
     -5.0593
    ],
    "rank_among_own": 1,
    "found_own": true,
    "recovered": true
   },
   {
    "score": -4.897,
    "letters_right": 38,
    "own_copies": [
     -5.1354,
     -5.0264,
     -5.0128,
     -4.9684
    ],
    "rank_among_own": 1,
    "found_own": true,
    "recovered": false
   },
   {
    "score": -4.8079,
    "letters_right": 35,
    "own_copies": [
     -5.0626,
     -5.022,
     -4.9493,
     -4.8041
    ],
    "rank_among_own": 2,
    "found_own": false,
    "recovered": false
   },
   {
    "score": -5.1223,
    "letters_right": 32,
    "own_copies": [
     -5.1363,
     -5.0745,
     -5.0601,
     -4.9811
    ],
    "rank_among_own": 4,
    "found_own": false,
    "recovered": false
   },
   {
    "score": -4.7782,
    "letters_right": 38,
    "own_copies": [
     -5.1225,
     -5.1091,
     -5.1074,
     -5.0659
    ],
    "rank_among_own": 1,
    "found_own": true,
    "recovered": false
   }
  ]
 },
 "k4": {
  "score": -5.1105,
  "plaintext": "YADKARZAMESURECOINGOREASTNORTHEASTETENAITEPETJFBGLIONOUCHERYTHIBERLINCLOCKEELHURMOFTSSAYMCHTELZEP",
  "alphabet": "OVLIGSMJAZBFDXNCYPQRTWUHEK",
  "key": [
   10,
   2,
   13,
   20,
   14,
   7,
   4,
   18,
   24,
   25,
   17,
   6,
   17,
   7,
   11,
   2,
   0,
   23,
   6
  ],
  "english_free": -5.427
 },
 "k4_copies": [
  -5.3087,
  -5.2374,
  -5.2213,
  -5.2112,
  -5.194,
  -5.1289,
  -5.0963,
  -5.0659,
  -5.0529,
  -5.0514,
  -5.0114,
  -5.0091
 ],
 "k4_rank_of_13": 7,
 "stop_queue": false,
 "controls": "kept-place copies (carved letters kept at the 24 known places, other 73 shuffled): 4 per plant (seed 1481), 12 for K4 (seed 1482)"
}
```

Notes: power 3/5 (bar 4, null 1.00); K4 -5.111 rank 7 of 13 (-5.309 to -5.009); stop False


