# 0139-parallel-tempering-climb-against-own-copies: F1.5 design 2: parallel tempering in the set that keeps the known letters, measured on planted English against scrambled copies of itself (one free alphabet, Beaufort form, key length 23)

**Family:** 1-keyed-periodic  
**Parent:** 0138-climb-power-against-each-plants-own-copies  
**Decision:** reverted  
**Run:** 2026-10-16T18:04:49+00:00, 1087.3 s, status ran  
**Time by phase:** unattributed 453 s, run 1087 s, record 0 s

## In plain words

A second way of searching for hidden English under one scrambled alphabet. Instead of starting the search a thousand times from scratch, sixteen searches run side by side, some bold and some cautious, and swap places when a bold one finds something promising. We again test it on planted English, comparing each planted message only with scrambled copies of itself. If it cannot tell them apart well, we stop trying to build such a search and record the cells as undecidable with today's tools.

## Walkthrough, by hand

1. Encipher a passage of English with a random alphabet and a random 23-letter key, the Beaufort way, with the known words in place.
2. Make six shuffles of its carved letters that could still give the known letters.
3. Start sixteen searches on the same text, each at its own boldness (temperature), each moving only between alphabets that keep the known letters right.
4. After every round, let neighbouring searches swap their current alphabets when the cooler one would gain.
5. Keep the best score seen; do the same on the six shuffles.
6. The planted text counts as noticed if it beats all six shuffles; luck gives that one time in seven.

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

Inherits from 0138-climb-power-against-each-plants-own-copies. What changed: F1.5, step 2, design 2. Design 1 (0137) failed its validity check (0138): against shuffles of themselves only 6 of 12 planted texts beat all six copies (bar 9). The climb never recovers a planted text; the true key is a narrow basin (about 12 check-keeping swaps wide, dry runs) in a landscape of false optima. Design 2 replaces independent annealing restarts with parallel tempering: 16 replicas at temperatures 0.1 to 0.002 that exchange states, the standard remedy for rugged landscapes, at the same compute per text (10 runs x 16 replicas x 625 rounds x 1,000 moves = 10^8 moves). Bar measured as in 0138, each plant against its own shuffles.

## Hypothesis (domain expert)

C27(c), C1(b) as 0137. Cell: one unknown alphabet, Beaufort form, key length 23 (7 checks), 75 open bits against 130 bits of quadgram evidence (0136). Search: replica exchange Monte Carlo over the alphabet in the set where every known-letter check holds (0137's moves and start), free key values as moves, full-text quadgram mean, geometric ladder T 0.1 -> 0.002, neighbour exchanges after every round. Dry run on 8 plants before this record (scratch): no plant recovered, best -4.71 to -4.91, 31-46 letters right. Plants: 8 Carter windows (seed 139, 0120's generator); own coppers: 6 shuffles of each plant's ciphertext that fit length 23 exactly (0119's decider). Null rate of a plant beating all 6: 1/7. Bar fixed before the run: design 2 passes if at least 6 of 8 plants beat all 6 of their own coppers. If it fails, F1.5 is blocked by its stop rule (two designs failed; issue #50).

## Prediction

No plant recovered; fewer than 6 of 8 plants beat all 6 of their own coppers (about the 50% of design 1), so design 2 fails the bar and F1.5 is blocked by its stop rule. Zero candidates.

## Method

1. Draw 8 planted texts at length 23 and 6 fitting shuffles of each.
2. Run the compiled parallel-tempering search on all 56 texts at equal effort.
3. Per plant: found if its best is above all 6 of its own coppers; rank; letters right.

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
 "family": "power check of 0137's climb: one unknown alphabet, Beaufort form, key length 23; each plant against shuffles of itself",
 "search": "parallel tempering, 10 runs x 16 replicas x 625 rounds x 1000 moves per text, T 0.1->0.002",
 "plants": 8,
 "own_coppers_per_plant": 6,
 "shuffles_tried": 110,
 "restarts_done": {
  "min": 10,
  "max": 10
 },
 "c_decryption_checked": true,
 "null_rate_found": 0.1429,
 "null_expected_found": 1.14,
 "bar": "design 1's power at 23 stands if >= 6 of 8 plants beat all 6 of their own coppers",
 "plants_found_against_own": 6,
 "passes_bar": true,
 "plants_recovered": 0,
 "plants_found_against_0137_k4_coppers": 8,
 "rows": [
  {
   "score": -4.764,
   "letters_right": 36,
   "true_score": -4.2609,
   "restarts": 10,
   "own_coppers": [
    -5.1035,
    -5.0232,
    -5.0203,
    -5.0013,
    -4.9526,
    -4.9313
   ],
   "rank_among_own": 1,
   "found_own": true,
   "rank_among_k4_coppers_0137": 1,
   "recovered": false
  },
  {
   "score": -4.8504,
   "letters_right": 39,
   "true_score": -4.3786,
   "restarts": 10,
   "own_coppers": [
    -5.145,
    -5.0631,
    -5.046,
    -4.9888,
    -4.9639,
    -4.9401
   ],
   "rank_among_own": 1,
   "found_own": true,
   "rank_among_k4_coppers_0137": 1,
   "recovered": false
  },
  {
   "score": -4.7096,
   "letters_right": 36,
   "true_score": -4.3703,
   "restarts": 10,
   "own_coppers": [
    -5.0463,
    -5.0373,
    -4.996,
    -4.9244,
    -4.871,
    -4.8517
   ],
   "rank_among_own": 1,
   "found_own": true,
   "rank_among_k4_coppers_0137": 1,
   "recovered": false
  },
  {
   "score": -4.9344,
   "letters_right": 38,
   "true_score": -4.554,
   "restarts": 10,
   "own_coppers": [
    -4.9851,
    -4.9755,
    -4.9335,
    -4.9292,
    -4.8888,
    -4.8845
   ],
   "rank_among_own": 5,
   "found_own": false,
   "rank_among_k4_coppers_0137": 1,
   "recovered": false
  },
  {
   "score": -4.6937,
   "letters_right": 41,
   "true_score": -4.2441,
   "restarts": 10,
   "own_coppers": [
    -5.1078,
    -5.0393,
    -5.0338,
    -5.0198,
    -4.9425,
    -4.8926
   ],
   "rank_among_own": 1,
   "found_own": true,
   "rank_among_k4_coppers_0137": 1,
   "recovered": false
  },
  {
   "score": -4.8052,
   "letters_right": 37,
   "true_score": -4.5324,
   "restarts": 10,
   "own_coppers": [
    -5.2018,
    -5.1629,
    -5.0567,
    -5.052,
    -5.0338,
    -4.9497
   ],
   "rank_among_own": 1,
   "found_own": true,
   "rank_among_k4_coppers_0137": 1,
   "recovered": false
  },
  {
   "score": -4.7305,
   "letters_right": 42,
   "true_score": -4.1924,
   "restarts": 10,
   "own_coppers": [
    -5.1441,
    -5.0191,
    -5.0034,
    -4.9353,
    -4.9318,
    -4.8795
   ],
   "rank_among_own": 1,
   "found_own": true,
   "rank_among_k4_coppers_0137": 1,
   "recovered": false
  },
  {
   "score": -4.7954,
   "letters_right": 34,
   "true_score": -4.1519,
   "restarts": 10,
   "own_coppers": [
    -5.0707,
    -5.042,
    -5.0247,
    -4.8955,
    -4.8608,
    -4.7722
   ],
   "rank_among_own": 2,
   "found_own": false,
   "rank_among_k4_coppers_0137": 1,
   "recovered": false
  }
 ],
 "controls": "per plant, 6 shuffles of its own ciphertext that fit length 23 exactly (0119's decider, seed 139)"
}
```

Notes: plants beating all 6 own coppers: 6/8 (null 1.1); beating all 0137 K4 coppers: 8/8; recovered 0; bar passed


