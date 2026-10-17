# 0188-wheatstone-cryptograph: F10.2: Wheatstone's cryptograph (a 27-place plain ring against a 26-letter cipher ring, the hands moved by the distance between plaintext letters), free or word-mixed cipher ring: exact

**Family:** 10-self-changing-alphabets  
**Parent:** 0187-chaocipher-keyword-left-wheels  
**Decision:** reverted  
**Run:** 2026-10-17T00:45:01+00:00, 9.4 s, status ran  
**Time by phase:** design 0 s, implement 0 s, test 0 s, run 9 s, record 0 s

## In plain words

Wheatstone's 1867 code machine looks like a clock: an outer ring with the alphabet, an inner ring with mixed letters, two hands geared slightly differently. To encode a letter you move the long hand forward to it, and read the letter under the short hand. Because the hands drift apart, the same letter comes out differently each time. Inside EASTNORTHEAST we know exactly how far the hand moves each time, so the known letters tell us where the code letters must sit on the inner ring.

## Walkthrough, by hand

1. The long hand stands on E (place 5 of the outer ring) at place 22.
2. To reach A it moves forward 23 places, to S then 18, to T 1, and so on through EASTNORTHEAST.
3. The short hand moves the same number of places on the 26-letter inner ring.
4. So the carved letters of places 22-34 sit on the inner ring at known distances from one another: two that land on the same inner place must be the same carved letter.
5. With an inner ring mixed from a word, the distances must match the word's alphabet exactly.

## Worked example (generated)

```
outer ring _ABC...Z, hands forward: long-hand steps through EASTNORTHEAST and the inner place each lands on

place 22: E, total steps   0, inner place b +  0, carved F
place 23: A, total steps  23, inner place b + 23, carved L
place 24: S, total steps  41, inner place b + 15, carved R
place 25: T, total steps  42, inner place b + 16, carved V
place 26: N, total steps  63, inner place b + 11, carved Q
place 27: O, total steps  64, inner place b + 12, carved Q
place 28: R, total steps  67, inner place b + 15, carved P
place 29: T, total steps  69, inner place b + 17, carved R
place 30: H, total steps  84, inner place b +  6, carved N
place 31: E, total steps 108, inner place b +  4, carved G
place 32: A, total steps 131, inner place b +  1, carved K
place 33: S, total steps 149, inner place b + 19, carved S
place 34: T, total steps 150, inner place b + 20, carved S
```

## Lineage

Inherits from 0187-chaocipher-keyword-left-wheels. What changed: F10.2. Wheatstone's cryptograph (1867): an outer ring of 27 places (blank and the 26 letters) and an inner ring of 26 mixed letters, two hands geared so that one turn of the long hand moves the short hand one turn and one letter. For each plaintext letter the long hand is moved forward to it; the short hand then points at the cipher letter. With S the long hand's total steps, the cipher letter is inner[S mod 26] and S mod 27 is the plain letter's place. Inside a known run the steps are known, so the inner places a run uses are known up to one offset per run; the runs are separated by unknown letters, so the second run's offset is free relative to the first (26 cases). Tested: the inner ring free (only coincidences of places check), and the inner ring mixed from any dictionary or vocabulary word (208,651 alphabets, exact); outer ring in standard or KRYPTOS order, blank first or last, hands forward or backward.

## Hypothesis (domain expert)

A10 (alphabets that change after every letter); Wheatstone's cryptograph (1867), an Alberti disk whose advance is set by the plaintext, a hand device a sculptor could have seen. Model as in 'changed', with the plaintext continuous (no blanks between words: the runs are carved as 13 and 11 consecutive letters). Each known letter fixes inner[(b_run + o_t) mod 26] = c_t, o_t known. Statistic: consistent (variant, offset) cells with the free ring and consistent (word, variant) cells with a mixed ring, K4 against 20 shuffled copies; plants.

## Prediction

With a free inner ring the known letters check little, so consistent cells at the copies' rate; with a word-mixed ring no word fits K4 or the copies. Zero candidates.

## Method

1. For each variant (outer order, blank first or last, direction): the long hand's steps inside each run.
2. Free inner ring: for each relative offset of the second run, collect inner place -> carved letter; consistent if one-to-one.
3. Mixed inner ring: for each word alphabet and run, the offsets that put every carved letter in place.
4. K4 against 20 shuffled copies; planted texts as builder checks.

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
 "family": "Wheatstone cryptograph: 27-place outer ring (std/KRYPTOS, blank first/last), 26-letter inner ring free or word-mixed, hands forward/backward; continuous plaintext; exact",
 "variants": 8,
 "word_alphabets": 208651,
 "free_ring_consistent_offsets": {
  "k4": 0,
  "copies": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ]
 },
 "mixed_ring_consistent": {
  "k4": 0,
  "copies": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ]
 },
 "k4_mixed_hits": [],
 "distinct_inner_places_per_run": {
  "std/first/fwd": {
   "run1_places": 12,
   "run2_places": 9
  },
  "std/first/bwd": {
   "run1_places": 10,
   "run2_places": 10
  },
  "std/last/fwd": {
   "run1_places": 12,
   "run2_places": 9
  },
  "std/last/bwd": {
   "run1_places": 10,
   "run2_places": 10
  },
  "kry/first/fwd": {
   "run1_places": 10,
   "run2_places": 11
  },
  "kry/first/bwd": {
   "run1_places": 10,
   "run2_places": 10
  },
  "kry/last/fwd": {
   "run1_places": 10,
   "run2_places": 11
  },
  "kry/last/bwd": {
   "run1_places": 10,
   "run2_places": 10
  }
 },
 "plants": [
  {
   "variant": "std/first/bwd",
   "inner": "CALXBDEFGHIJKMNOPQRSTUVWYZ",
   "free_offsets": 1,
   "mixed_found": true
  },
  {
   "variant": "std/first/fwd",
   "inner": "UNDERWFTABCGHIJKLMOPQSVXYZ",
   "free_offsets": 1,
   "mixed_found": true
  }
 ],
 "copies": "20 shuffled copies (seed 1880)",
 "seconds": 9,
 "exhaustive": true
}
```

Notes: free inner ring: consistent (variant, offset) K4 0 (copies 0-0) of 208; word-mixed inner ring: K4 0 (copies 0-0); plants [{'variant': 'std/first/bwd', 'inner': 'CALXBDEFGHIJKMNOPQRSTUVWYZ', 'free_offsets': 1, 'mixed_found': True}, {'variant': 'std/first/fwd', 'inner': 'UNDERWFTABCGHIJKLMOPQSVXYZ', 'free_offsets': 1, 'mixed_found': True}]


