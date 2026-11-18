# 0282-f16.1b-s-two-dictionary-keyword-alphabets-with-slips: F16.1b-s: 0275 (two dictionary keyword alphabets, every pair, key lengths 1-26, the 20 official letters) with one or two of the 20 known letters slipped: every drop set, the key word screened where the fitting pairs can be listed; K4 against 20 shuffles, 6 plants with slips

**Family:** 16-simple-hand-methods  
**Parent:** 0275-f16.1b-two-dictionary-keyword-alphabets-on-the-20-official-letters  
**Decision:** reverted  
**Run:** 2026-11-18T09:03:09+00:00, 4196.3 s, status ran  
**Time by phase:** unattributed 56714 s, run 4196 s, record 0 s

## In plain words

Experiment 275 tried every pair of dictionary-word alphabets with a key word on the 20 letters Sanborn published. If he miscopied one or two of those letters, it would have missed. Here we drop each one and each pair in turn and look again for a key word.

## Walkthrough, by hand

1. Strike out one of the 20 known letters, say the K at 74, as a slip.
2. Repeat 0275's test on the other 19: for each pair of word alphabets, the same-slot distances must agree.
3. Read the key letters the pair forces and look for a word.
4. Do this for each letter struck out, and each pair struck out, on the carving and on scrambled copies.

## Worked example (generated)

```
key length 16: the 20 official places by slot (place - 1 mod 16); same-slot places share a key letter

  slot  0: 33 S->S, 65 E->Y
  slot  1: 34 T->S, 66 R->P
  slot  2: 67 L->V
  slot  3: 68 I->T
  slot  4: 69 N->T
  slot  5: 70 C->M
  slot  6: 71 L->Z
  slot  7: 72 O->F
  slot  8: 73 C->P
  slot  9: 26 N->Q, 74 K->K
  slot 10: 27 O->Q
  slot 11: 28 R->P
  slot 12: 29 T->R
  slot 13: 30 H->N
  slot 14: 31 E->G
  slot 15: 32 A->K, 64 B->N

A pair of alphabets fits when, in every slot with two places, the cipher-alphabet distance of the carved letters equals the plain-alphabet distance of the known letters.
```

## Lineage

Inherits from 0275-f16.1b-two-dictionary-keyword-alphabets-on-the-20-official-letters. What changed: F16.1b-s (issue #123): 0275's search, imported unchanged (0244's index and matcher, 0275's hash screen), run on the 20 official letters less each set of 1 or 2 places (20 + 190 drop sets). Where a length and form has more than 5 million fitting pairs the pairs are counted, not listed, and the key word is not checked there (the reach, reported per cell).

## Hypothesis (domain expert)

As 0275 and 0244 (C4(a), C5; Quagmire IV with two keyword-mixed alphabets from the dictionary and a key word), with A1's slip at a known place (Sanborn 2005, 'Saying I was sloppy'; K2's carved errors, 01-facts.md) and EAST set aside (#124). A slip at known place q removes q's equation; the key word still has to match the forced key on every slot the remaining places cover. With 18 or 19 places the slots covered at lengths 3-16 still leave word matches far below one per text by chance; at the long lengths the fitting pairs run to billions and only counts are possible.

## Prediction

No key word on K4 at any drop set where the screen reaches; shuffles the same; plants (one or two slips) found 6 of 6; fit counts inside the shuffles. Zero candidates unless a key word fits.

## Method

1. 0275's alphabets and word rotations.
2. For each text and each drop set of 1 or 2 of the 20 places: 0244's pair index over the remaining places, lengths 1-26, both forms; pairs listed when 5 million or fewer, then 0275's screen and 0244's matcher.
3. K4, 20 shuffles, 6 plants (two random dictionary alphabets, a dictionary key word, 1 or 2 letters changed at official places).
4. Matches and counts against the shuffles.

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
 "item": "F16.1b-s",
 "drop_sets": 210,
 "known_places": [
  26,
  27,
  28,
  29,
  30,
  31,
  32,
  33,
  34,
  64,
  65,
  66,
  67,
  68,
  69,
  70,
  71,
  72,
  73,
  74
 ],
 "cap_pairs_listed": 5000000,
 "key_word_check_lengths": [
  3,
  23
 ],
 "fitting": {
  "1/added": {
   "k4_drop_sets_fitting": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p": null,
   "k4_unscreened_drop_sets": 0
  },
  "1/beaufort": {
   "k4_drop_sets_fitting": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p": null,
   "k4_unscreened_drop_sets": 0
  },
  "2/added": {
   "k4_drop_sets_fitting": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p": null,
   "k4_unscreened_drop_sets": 0
  },
  "2/beaufort": {
   "k4_drop_sets_fitting": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p": null,
   "k4_unscreened_drop_sets": 0
  },
  "3/added": {
   "k4_drop_sets_fitting": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p": null,
   "k4_unscreened_drop_sets": 0
  },
  "3/beaufort": {
   "k4_drop_sets_fitting": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p": null,
   "k4_unscreened_drop_sets": 0
  },
  "4/added": {
   "k4_drop_sets_fitting": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p": null,
   "k4_unscreened_drop_sets": 0
  },
  "4/beaufort": {
   "k4_drop_sets_fitting": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p": null,
   "k4_unscreened_drop_sets": 0
  },
  "5/added": {
   "k4_drop_sets_fitting": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p": null,
   "k4_unscreened_drop_sets": 0
  },
  "5/beaufort": {
   "k4_drop_sets_fitting": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p": null,
   "k4_unscreened_drop_sets": 0
  },
  "6/added": {
   "k4_drop_sets_fitting": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p": null,
   "k4_unscreened_drop_sets": 0
  },
  "6/beaufort": {
   "k4_drop_sets_fitting": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p": null,
   "k4_unscreened_drop_sets": 0
  },
  "7/added": {
   "k4_drop_sets_fitting": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p": null,
   "k4_unscreened_drop_sets": 0
  },
  "7/beaufort": {
   "k4_drop_sets_fitting": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p": null,
   "k4_unscreened_drop_sets": 0
  },
  "8/added": {
   "k4_drop_sets_fitting": 0,
   "copies_median": 0.0,
   "copies_max": 2,
   "p": null,
   "k4_unscreened_drop_sets": 0
  },
  "8/beaufort": {
   "k4_drop_sets_fitting": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p": null,
   "k4_unscreened_drop_sets": 0
  },
  "9/added": {
   "k4_drop_sets_fitting": 0,
   "copies_median": 0.0,
   "copies_max": 16,
   "p": null,
   "k4_unscreened_drop_sets": 0
  },
  "9/beaufort": {
   "k4_drop_sets_fitting": 0,
   "copies_median": 0.0,
   "copies_max": 15,
   "p": null,
   "k4_unscreened_drop_sets": 0
  },
  "10/added": {
   "k4_drop_sets_fitting": 4,
   "copies_median": 16.0,
   "copies_max": 133,
   "p": 0.81,
   "k4_unscreened_drop_sets": 0
  },
  "10/beaufort": {
   "k4_drop_sets_fitting": 12,
   "copies_median": 9.0,
   "copies_max": 66,
   "p": 0.429,
   "k4_unscreened_drop_sets": 0
  },
  "11/added": {
   "k4_drop_sets_fitting": 28,
   "copies_median": 109.5,
   "copies_max": 207,
   "p": 0.857,
   "k4_unscreened_drop_sets": 0
  },
  "11/beaufort": {
   "k4_drop_sets_fitting": 52,
   "copies_median": 104.0,
   "copies_max": 150,
   "p": 0.667,
   "k4_unscreened_drop_sets": 0
  },
  "12/added": {
   "k4_drop_sets_fitting": 74,
   "copies_median": 189.0,
   "copies_max": 210,
   "p": 0.762,
   "k4_unscreened_drop_sets": 0
  },
  "12/beaufort": {
   "k4_drop_sets_fitting": 52,
   "copies_median": 189.0,
   "copies_max": 210,
   "p": 0.762,
   "k4_unscreened_drop_sets": 0
  },
  "13/added": {
   "k4_drop_sets_fitting": 143,
   "copies_median": 133.0,
   "copies_max": 179,
   "p": 0.429,
   "k4_unscreened_drop_sets": 0
  },
  "13/beaufort": {
   "k4_drop_sets_fitting": 132,
   "copies_median": 121.5,
   "copies_max": 172,
   "p": 0.429,
   "k4_unscreened_drop_sets": 0
  },
  "14/added": {
   "k4_drop_sets_fitting": 39,
   "copies_median": 210.0,
   "copies_max": 210,
   "p": 0.952,
   "k4_unscreened_drop_sets": 0
  },
  "14/beaufort": {
   "k4_drop_sets_fitting": 39,
   "copies_median": 210.0,
   "copies_max": 210,
   "p": 0.952,
   "k4_unscreened_drop_sets": 0
  },
  "15/added": {
   "k4_drop_sets_fitting": 4,
   "copies_median": 39.0,
   "copies_max": 210,
   "p": 1.0,
   "k4_unscreened_drop_sets": 0
  },
  "15/beaufort": {
   "k4_drop_sets_fitting": 4,
   "copies_median": 39.0,
   "copies_max": 210,
   "p": 1.0,
   "k4_unscreened_drop_sets": 0
  },
  "16/added": {
   "k4_drop_sets_fitting": 210,
   "copies_median": 210.0,
   "copies_max": 210,
   "p": 0.857,
   "k4_unscreened_drop_sets": 78
  },
  "16/beaufort": {
   "k4_drop_sets_fitting": 210,
   "copies_median": 210.0,
   "copies_max": 210,
   "p": 0.857,
   "k4_unscreened_drop_sets": 24
  },
  "17/added": {
   "k4_drop_sets_fitting": 4,
   "copies_median": 39.0,
   "copies_max": 210,
   "p": 0.952,
   "k4_unscreened_drop_sets": 0
  },
  "17/beaufort": {
   "k4_drop_sets_fitting": 4,
   "copies_median": 39.0,
   "copies_max": 210,
   "p": 0.952,
   "k4_unscreened_drop_sets": 0
  },
  "18/added": {
   "k4_drop_sets_fitting": 74,
   "copies_median": 210.0,
   "copies_max": 210,
   "p": 0.762,
   "k4_unscreened_drop_sets": 0
  },
  "18/beaufort": {
   "k4_drop_sets_fitting": 74,
   "copies_median": 210.0,
   "copies_max": 210,
   "p": 0.762,
   "k4_unscreened_drop_sets": 0
  },
  "19/added": {
   "k4_drop_sets_fitting": 200,
   "copies_median": 26.0,
   "copies_max": 39,
   "p": 0.048,
   "k4_unscreened_drop_sets": 0
  },
  "19/beaufort": {
   "k4_drop_sets_fitting": 200,
   "copies_median": 22.0,
   "copies_max": 39,
   "p": 0.048,
   "k4_unscreened_drop_sets": 0
  },
  "20/added": {
   "k4_drop_sets_fitting": 96,
   "copies_median": 135.5,
   "copies_max": 193,
   "p": 0.857,
   "k4_unscreened_drop_sets": 0
  },
  "20/beaufort": {
   "k4_drop_sets_fitting": 120,
   "copies_median": 123.5,
   "copies_max": 154,
   "p": 0.571,
   "k4_unscreened_drop_sets": 0
  },
  "21/added": {
   "k4_drop_sets_fitting": 39,
   "copies_median": 210.0,
   "copies_max": 210,
   "p": 0.952,
   "k4_unscreened_drop_sets": 0
  },
  "21/beaufort": {
   "k4_drop_sets_fitting": 39,
   "copies_median": 210.0,
   "copies_max": 210,
   "p": 0.952,
   "k4_unscreened_drop_sets": 0
  },
  "22/added": {
   "k4_drop_sets_fitting": 210,
   "copies_median": 210.0,
   "copies_max": 210,
   "p": 0.857,
   "k4_unscreened_drop_sets": 0
  },
  "22/beaufort": {
   "k4_drop_sets_fitting": 210,
   "copies_median": 210.0,
   "copies_max": 210,
   "p": 0.857,
   "k4_unscreened_drop_sets": 12
  },
  "23/added": {
   "k4_drop_sets_fitting": 210,
   "copies_median": 210.0,
   "copies_max": 210,
   "p": 0.762,
   "k4_unscreened_drop_sets": 105
  },
  "23/beaufort": {
   "k4_drop_sets_fitting": 210,
   "copies_median": 210.0,
   "copies_max": 210,
   "p": 0.762,
   "k4_unscreened_drop_sets": 105
  },
  "24/added": {
   "k4_drop_sets_fitting": 210,
   "copies_median": 210.0,
   "copies_max": 210,
   "p": 1.0,
   "k4_unscreened_drop_sets": 0
  },
  "24/beaufort": {
   "k4_drop_sets_fitting": 210,
   "copies_median": 210.0,
   "copies_max": 210,
   "p": 1.0,
   "k4_unscreened_drop_sets": 0
  },
  "25/added": {
   "k4_drop_sets_fitting": 210,
   "copies_median": 210.0,
   "copies_max": 210,
   "p": 1.0,
   "k4_unscreened_drop_sets": 0
  },
  "25/beaufort": {
   "k4_drop_sets_fitting": 210,
   "copies_median": 210.0,
   "copies_max": 210,
   "p": 1.0,
   "k4_unscreened_drop_sets": 0
  },
  "26/added": {
   "k4_drop_sets_fitting": 210,
   "copies_median": 210.0,
   "copies_max": 210,
   "p": 1.0,
   "k4_unscreened_drop_sets": 0
  },
  "26/beaufort": {
   "k4_drop_sets_fitting": 210,
   "copies_median": 210.0,
   "copies_max": 210,
   "p": 1.0,
   "k4_unscreened_drop_sets": 0
  }
 },
 "key_word_matches": {
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
 "k4_matches": [],
 "plants": {
  "plant0": {
   "L": 14,
   "slips": [
    30
   ],
   "found": true
  },
  "plant1": {
   "L": 16,
   "slips": [
    68,
    70
   ],
   "found": true
  },
  "plant2": {
   "L": 18,
   "slips": [
    74
   ],
   "found": true
  },
  "plant3": {
   "L": 20,
   "slips": [
    34,
    64
   ],
   "found": true
  },
  "plant4": {
   "L": 21,
   "slips": [
    28
   ],
   "found": true
  },
  "plant5": {
   "L": 22,
   "slips": [
    30,
    34
   ],
   "found": true
  }
 },
 "plants_found": 6,
 "copies": 20,
 "compute_seconds": 4132,
 "exhaustive": "yes where pairs are listed; cells above the cap counted only (k4_unscreened_drop_sets)",
 "aws_cost_estimate_dollars": 2.0
}
```

Notes: 210 drop sets; key-word matches K4 0, copies max 0; plants 6/6


