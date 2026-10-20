# 0209-two-free-alphabets-with-slips-at-known-places: A1.2, step 3: two alphabets in unknown orders (Quagmire IV), a repeating key of length 1-26, with up to three of the 24 known letters carved wrong, decided exactly, against scrambled copies, with planted slipped messages

**Family:** 1-keyed-periodic  
**Parent:** 0123-two-free-alphabets-exact-at-every-key-length  
**Decision:** reverted  
**Run:** 2026-10-20T12:31:35+00:00, 101.7 s, status ran  
**Time by phase:** implement 5 s, test 107 s, run 102 s, record 0 s

## In plain words

The same question as experiment 208, with one more freedom: the alphabet used to look up the message letter and the one used to write the carved letter may be two different scrambles. That is so much freedom that scrambled copies of the carving often fit already; we want to know up to which word length a search allowing two or three slips can still tell anything apart, and whether the carving fits anywhere the copies do not.

## Walkthrough, by hand

1. Choose a key length, say 4, and write the 24 known places with their slot (place mod 4).
2. For each place write: position of the carved letter in the cipher alphabet = position of the known letter in the plain alphabet + key value of the slot.
3. Cross out up to three of the 24 places, as if Sanborn had slipped there.
4. Try to place the letters in two alphabets and choose key values so every remaining line holds, backing up when two letters of one alphabet need the same position.
5. If it works, the length fits with those slips; if every branch backs up, it does not.
6. Repeat for every choice of crossed-out places, every length, and on scrambled copies.

## Worked example (generated)

```
key length 4, two free alphabets: C(carved) = P(known) + k[slot]

  slips at none: dead
  slips at [66]: dead
  slips at [66, 73]: dead
  slips at [28, 66, 73]: dead
```

## Lineage

Inherits from 0123-two-free-alphabets-exact-at-every-key-length. What changed: A1.2 (Stage 2, step 2, issue #76), last part: two free alphabets, run because the cost allows (about 1 s per length per text). 0123 decided every key length 1-26 exactly with all 24 known letters required (K4 fits at 8, 13, 16, 19, 20, 23, 24, 26; dead at the rest). Here 1-3 of the 24 equations may be dropped as slips: 0123's exact decider, unchanged, on every drop set (2,325 per length, supersets of a fitting set skipped), K4 against 20 scrambled copies, planted slipped messages in the same run (three pre-registered at lengths 4, 5, 7; three more at 3 and 9 added after a dry run showed copies fit at 4-8, to locate the reach). 0208 found the reach of one free alphabet near length 9; two alphabets have 25 more free places, so the reach is expected lower.

## Hypothesis (domain expert)

A1 (knowledge/12-assumptions.md); C27(c) (Sanborn's own tableau 'slightly different', 02-sanborn-said.md), C27(a) (the PALIMPCEST slip), Sanborn 2005 'Saying I was sloppy is a good way of saying it', Scheidt 2015 on Jim's encoding errors (03-scheidt-said.md). Model as 0123: two unknown bijections P, C from letters to Z26 (plain and cipher sides), key k of length L: C(c_i) = P(p_i) + k[i mod L] (the Beaufort form is the same family with P negated). A slip at known place q removes its equation. For every set D of 0-3 known places decide exactly (0123's decide(two=True), witness re-checked) whether alphabets and key satisfy the rest. Count minimal fitting sets per length by size, K4 against each copy. Where K4 fits, the reading is undetermined (two free alphabets), so the judge cannot read it; only F1.5's decider could, and two alphabets are above 0136's English bound from length 19. Cost of naming the slips: 17.5 bits for 2, 25.1 for 3.

## Prediction

K4 has no fitting pair of alphabets at lengths 1-4 even with 3 slips; from about 5 the copies fit as well, and K4 fits where they do, inside their range (K4 above every copy in no more cells than a copy is above the rest). A plant at length 4 with 2 slips is found; plants at 5 and 7 with 3 slips may not be told from their copies (the reach). Zero candidates.

## Method

1. For each text and key length L 1-26: the 24 equations (slot, known letter, carved letter).
2. Decide the system with no drop, then every drop set of 1, 2, 3 known places, skipping supersets of a set already fitting.
3. Count the minimal fitting sets by size; record undecided ones.
4. K4 and 20 copies on every length; three planted messages and 10 copies of each on their own length.
5. Compare K4's count with the copies' per length and per k.

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
 "family": "two unknown alphabets (Quagmire IV), periodic key 1-26, with 0-3 known letters slipped (A1.2)",
 "key_lengths": [
  1,
  26
 ],
 "forms": {
  "V": "C(c) = P(p) + k (Beaufort is the same family with P negated)"
 },
 "drop_sets": "every set of 0-3 of the 24 known places (2,325 per cell), supersets of a fitting set skipped; 0123's decide(two=True) unchanged",
 "slip_cost_bits": {
  "1": 9.3,
  "2": 17.5,
  "3": 25.1
 },
 "cells": {
  "V1": {
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ],
   "copies_fitting_at_k_or_less": [
    0,
    0,
    0,
    0
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": []
  },
  "V2": {
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ],
   "copies_fitting_at_k_or_less": [
    0,
    0,
    0,
    0
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": []
  },
  "V3": {
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ],
   "copies_fitting_at_k_or_less": [
    0,
    0,
    0,
    0
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": []
  },
  "V4": {
   "k4": [
    0,
    0,
    0,
    8
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    2,
    8
   ],
   "copies_fitting_at_k_or_less": [
    0,
    0,
    4,
    11
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     25,
     28,
     67
    ],
    [
     25,
     28,
     71
    ],
    [
     25,
     66,
     67
    ],
    [
     25,
     66,
     71
    ],
    [
     28,
     29,
     67
    ],
    [
     28,
     29,
     71
    ],
    [
     29,
     66,
     67
    ],
    [
     29,
     66,
     71
    ]
   ]
  },
  "V5": {
   "k4": [
    0,
    0,
    0,
    2
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    2,
    8
   ],
   "copies_fitting_at_k_or_less": [
    0,
    0,
    1,
    8
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     28,
     29,
     72
    ],
    [
     29,
     72,
     73
    ]
   ]
  },
  "V6": {
   "k4": [
    0,
    0,
    0,
    8
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    8,
    10,
    18
   ],
   "copies_fitting_at_k_or_less": [
    2,
    11,
    16,
    19
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     25,
     28,
     32
    ],
    [
     25,
     28,
     74
    ],
    [
     25,
     32,
     66
    ],
    [
     25,
     66,
     74
    ],
    [
     28,
     32,
     67
    ],
    [
     28,
     67,
     74
    ],
    [
     32,
     66,
     67
    ],
    [
     66,
     67,
     74
    ]
   ]
  },
  "V7": {
   "k4": [
    0,
    0,
    0,
    8
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    4,
    12,
    8
   ],
   "copies_fitting_at_k_or_less": [
    3,
    13,
    18,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     25,
     32,
     66
    ],
    [
     25,
     32,
     73
    ],
    [
     25,
     66,
     74
    ],
    [
     25,
     73,
     74
    ],
    [
     32,
     66,
     67
    ],
    [
     32,
     67,
     73
    ],
    [
     66,
     67,
     74
    ],
    [
     67,
     73,
     74
    ]
   ]
  },
  "V8": {
   "k4": [
    1,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    2,
    4,
    8
   ],
   "copies_fitting_at_k_or_less": [
    1,
    13,
    18,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    []
   ]
  },
  "V9": {
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ],
   "copies_fitting_at_k_or_less": [
    0,
    0,
    0,
    0
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": []
  },
  "V10": {
   "k4": [
    0,
    2,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    4,
    4,
    6
   ],
   "copies_fitting_at_k_or_less": [
    3,
    17,
    19,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     22
    ],
    [
     72
    ]
   ]
  },
  "V11": {
   "k4": [
    0,
    4,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    2,
    4,
    8
   ],
   "copies_fitting_at_k_or_less": [
    13,
    18,
    19,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     22
    ],
    [
     28
    ],
    [
     66
    ],
    [
     72
    ]
   ]
  },
  "V12": {
   "k4": [
    0,
    4,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    4,
    4,
    0
   ],
   "copies_fitting_at_k_or_less": [
    12,
    19,
    20,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     28
    ],
    [
     30
    ],
    [
     64
    ],
    [
     66
    ]
   ]
  },
  "V13": {
   "k4": [
    1,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    2,
    0,
    0
   ],
   "copies_fitting_at_k_or_less": [
    14,
    20,
    20,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    []
   ]
  },
  "V14": {
   "k4": [
    0,
    0,
    4,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    4,
    4,
    0
   ],
   "copies_fitting_at_k_or_less": [
    13,
    19,
    20,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     25,
     32
    ],
    [
     25,
     74
    ],
    [
     32,
     67
    ],
    [
     67,
     74
    ]
   ]
  },
  "V15": {
   "k4": [
    0,
    0,
    4,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    2,
    4,
    8
   ],
   "copies_fitting_at_k_or_less": [
    0,
    16,
    19,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     27,
     28
    ],
    [
     27,
     73
    ],
    [
     28,
     72
    ],
    [
     72,
     73
    ]
   ]
  },
  "V16": {
   "k4": [
    1,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    2,
    4,
    0
   ],
   "copies_fitting_at_k_or_less": [
    14,
    19,
    20,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    []
   ]
  },
  "V17": {
   "k4": [
    0,
    0,
    4,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    2,
    8,
    0
   ],
   "copies_fitting_at_k_or_less": [
    1,
    15,
    20,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     30,
     31
    ],
    [
     30,
     65
    ],
    [
     31,
     64
    ],
    [
     64,
     65
    ]
   ]
  },
  "V18": {
   "k4": [
    0,
    4,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    2,
    0,
    0
   ],
   "copies_fitting_at_k_or_less": [
    18,
    20,
    20,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     28
    ],
    [
     30
    ],
    [
     64
    ],
    [
     66
    ]
   ]
  },
  "V19": {
   "k4": [
    1,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    2,
    4,
    8
   ],
   "copies_fitting_at_k_or_less": [
    1,
    17,
    19,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    []
   ]
  },
  "V20": {
   "k4": [
    1,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    2,
    4,
    0
   ],
   "copies_fitting_at_k_or_less": [
    7,
    19,
    20,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    []
   ]
  },
  "V21": {
   "k4": [
    0,
    0,
    4,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    4,
    4,
    0
   ],
   "copies_fitting_at_k_or_less": [
    13,
    19,
    20,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     25,
     32
    ],
    [
     25,
     74
    ],
    [
     32,
     67
    ],
    [
     67,
     74
    ]
   ]
  },
  "V22": {
   "k4": [
    0,
    4,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    2,
    0,
    0
   ],
   "copies_fitting_at_k_or_less": [
    17,
    20,
    20,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     22
    ],
    [
     28
    ],
    [
     66
    ],
    [
     72
    ]
   ]
  },
  "V23": {
   "k4": [
    1,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    2,
    0,
    0
   ],
   "copies_fitting_at_k_or_less": [
    18,
    20,
    20,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    []
   ]
  },
  "V24": {
   "k4": [
    1,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    2,
    0,
    0
   ],
   "copies_fitting_at_k_or_less": [
    15,
    20,
    20,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    []
   ]
  },
  "V25": {
   "k4": [
    0,
    2,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    2,
    0,
    0
   ],
   "copies_fitting_at_k_or_less": [
    18,
    20,
    20,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    [
     22
    ],
    [
     72
    ]
   ]
  },
  "V26": {
   "k4": [
    1,
    0,
    0,
    0
   ],
   "copies_min": [
    1,
    0,
    0,
    0
   ],
   "copies_max": [
    1,
    0,
    0,
    0
   ],
   "copies_fitting_at_k_or_less": [
    20,
    20,
    20,
    20
   ],
   "k4_undecided": 0,
   "copies_undecided": 0,
   "k4_sets": [
    []
   ]
  }
 },
 "k4_above_every_copy": [
  "V18",
  "V22"
 ],
 "copies_above_the_rest_cells": [
  2,
  0,
  0,
  0,
  0,
  1,
  1,
  0,
  2,
  0,
  0,
  0,
  1,
  0,
  0,
  0,
  0,
  1,
  1,
  0
 ],
 "shortest_fitting_length": {
  "k0": {
   "K4": {
    "V": 8
   },
   "copies": [
    {
     "V": 14
    },
    {
     "V": 10
    },
    {
     "V": 7
    },
    {
     "V": 7
    },
    {
     "V": 6
    },
    {
     "V": 13
    },
    {
     "V": 12
    },
    {
     "V": 11
    },
    {
     "V": 12
    },
    {
     "V": 11
    },
    {
     "V": 11
    },
    {
     "V": 11
    },
    {
     "V": 6
    },
    {
     "V": 11
    },
    {
     "V": 8
    },
    {
     "V": 7
    },
    {
     "V": 12
    },
    {
     "V": 12
    },
    {
     "V": 11
    },
    {
     "V": 11
    }
   ]
  },
  "k1": {
   "K4": {
    "V": 8
   },
   "copies": [
    {
     "V": 7
    },
    {
     "V": 6
    },
    {
     "V": 6
    },
    {
     "V": 7
    },
    {
     "V": 6
    },
    {
     "V": 6
    },
    {
     "V": 6
    },
    {
     "V": 6
    },
    {
     "V": 7
    },
    {
     "V": 7
    },
    {
     "V": 8
    },
    {
     "V": 10
    },
    {
     "V": 6
    },
    {
     "V": 6
    },
    {
     "V": 7
    },
    {
     "V": 6
    },
    {
     "V": 6
    },
    {
     "V": 8
    },
    {
     "V": 7
    },
    {
     "V": 6
    }
   ]
  },
  "k2": {
   "K4": {
    "V": 8
   },
   "copies": [
    {
     "V": 6
    },
    {
     "V": 6
    },
    {
     "V": 4
    },
    {
     "V": 6
    },
    {
     "V": 6
    },
    {
     "V": 6
    },
    {
     "V": 6
    },
    {
     "V": 6
    },
    {
     "V": 6
    },
    {
     "V": 4
    },
    {
     "V": 6
    },
    {
     "V": 10
    },
    {
     "V": 6
    },
    {
     "V": 6
    },
    {
     "V": 7
    },
    {
     "V": 6
    },
    {
     "V": 4
    },
    {
     "V": 7
    },
    {
     "V": 4
    },
    {
     "V": 6
    }
   ]
  },
  "k3": {
   "K4": {
    "V": 4
   },
   "copies": [
    {
     "V": 6
    },
    {
     "V": 4
    },
    {
     "V": 4
    },
    {
     "V": 4
    },
    {
     "V": 4
    },
    {
     "V": 6
    },
    {
     "V": 4
    },
    {
     "V": 4
    },
    {
     "V": 5
    },
    {
     "V": 4
    },
    {
     "V": 4
    },
    {
     "V": 5
    },
    {
     "V": 6
    },
    {
     "V": 4
    },
    {
     "V": 5
    },
    {
     "V": 6
    },
    {
     "V": 4
    },
    {
     "V": 6
    },
    {
     "V": 4
    },
    {
     "V": 6
    }
   ]
  }
 },
 "plants": [
  {
   "seed": 2091,
   "key_length": 4,
   "form": "V",
   "k": 2,
   "slips": [
    34,
    72
   ],
   "alphabet": "KAXBWSMIQZFUYLDTCJHOENRVGP/ULCQWGIKASBZXRMYPJTFNDEHOV",
   "minimal_fits_by_k": [
    0,
    1,
    1,
    4
   ],
   "planted_slips_fit": true,
   "exact_planted_set_minimal": false,
   "count_at_k": 2,
   "own_copies_count_at_k": [
    0,
    0,
    2,
    0,
    0,
    0,
    0,
    4,
    0,
    2
   ],
   "found": false
  },
  {
   "seed": 2092,
   "key_length": 5,
   "form": "V",
   "k": 3,
   "slips": [
    70,
    71,
    74
   ],
   "alphabet": "DNIGCFTHLBQSUVMOREJPWXAYKZ/GSUTOZDLIYEABWVCRJMFPNXKQH",
   "minimal_fits_by_k": [
    0,
    2,
    0,
    0
   ],
   "planted_slips_fit": true,
   "exact_planted_set_minimal": false,
   "count_at_k": 2,
   "own_copies_count_at_k": [
    0,
    0,
    8,
    0,
    3,
    8,
    8,
    16,
    4,
    8
   ],
   "found": false
  },
  {
   "seed": 2093,
   "key_length": 7,
   "form": "V",
   "k": 3,
   "slips": [
    66,
    67,
    71
   ],
   "alphabet": "WGOJVQSLNKRXTZAMBYEDUHIFCP/ZADHMLKPIWBRFOSEQXVTNUYGJC",
   "minimal_fits_by_k": [
    0,
    0,
    8,
    0
   ],
   "planted_slips_fit": true,
   "exact_planted_set_minimal": false,
   "count_at_k": 8,
   "own_copies_count_at_k": [
    2,
    8,
    2,
    1,
    1,
    4,
    2,
    4,
    8,
    1
   ],
   "found": false
  },
  {
   "seed": 2094,
   "key_length": 3,
   "form": "V",
   "k": 2,
   "slips": [
    29,
    34
   ],
   "alphabet": "XZRMEVANBYFTWOGJHKUQSLDIPC/PCQGTNKFYRZEWABUVDLSXJHMOI",
   "minimal_fits_by_k": [
    0,
    1,
    0,
    1
   ],
   "planted_slips_fit": true,
   "exact_planted_set_minimal": false,
   "count_at_k": 1,
   "own_copies_count_at_k": [
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
   ],
   "found": true
  },
  {
   "seed": 2095,
   "key_length": 3,
   "form": "V",
   "k": 3,
   "slips": [
    22,
    26,
    69
   ],
   "alphabet": "CEAUDWVNYQRTFLHXKZBIJMGPOS/ITVAMLBHXQOUESGCPYNFRJKWDZ",
   "minimal_fits_by_k": [
    0,
    2,
    0,
    0
   ],
   "planted_slips_fit": true,
   "exact_planted_set_minimal": false,
   "count_at_k": 2,
   "own_copies_count_at_k": [
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
   ],
   "found": true
  },
  {
   "seed": 2096,
   "key_length": 9,
   "form": "V",
   "k": 3,
   "slips": [
    66,
    70,
    73
   ],
   "alphabet": "ZGIYKNPECUAMJRHDQSFBXVTWOL/RHSCZPTGWOMIAQFEDUXLYNJVBK",
   "minimal_fits_by_k": [
    1,
    0,
    0,
    0
   ],
   "planted_slips_fit": true,
   "exact_planted_set_minimal": false,
   "count_at_k": 1,
   "own_copies_count_at_k": [
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
   ],
   "found": true
  }
 ],
 "judge": "not called: where two free alphabets fit, both are undetermined and so is the reading; F1.5's decider only below 0136's bound (length 19)",
 "texts_done": "546 of 546 cells",
 "controls": "20 shuffled copies (seeds 2100-2119); each plant against 10 shuffles of its own ciphertext",
 "exhaustive": "yes (exact per drop set; undecided sets counted)"
}
```

Notes: K4 above every copy in 2 cells ['V18', 'V22']; copies above the rest 0-2; plants found [False, False, False, True, True, True]


