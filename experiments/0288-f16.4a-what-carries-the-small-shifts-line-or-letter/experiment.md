# 0288-f16.4a-what-carries-the-small-shifts-line-or-letter: F16.4a: what carries K4's small shifts (0286, 0287): the plaintext letter (Bean's grouping: the known letters that are in KRYPTOS, or the late half of the alphabet), the carved line with those letters held apart, or a free offset per carved line; each statistic against 100,000 shuffles

**Family:** 16-simple-hand-methods  
**Parent:** 0287-f16.4-r-small-shifts-replicated-on-fresh-shuffles-thresholds-1-6  
**Decision:** reverted  
**Run:** 2026-11-19T09:11:27+00:00, 106.2 s, status ran  
**Time by phase:** implement 0 s, test 252 s, design 103 s, run 106 s, record 0 s

## In plain words

K4's known letters near EASTNORTHEAST sit close to the carved letters. That stretch also holds most of the known S, T, O and R. So is it the place that makes the letters close, or the letters themselves? We count closeness for the same letters elsewhere, and for other letters in the same stretch, and check whether the second stretch (BERLINCLOCK) is close once a fixed number of steps is taken off, each against scrambled copies.

## Walkthrough, by hand

1. List the known places whose message letter is one of K, R, Y, P, T, O, S: ten of the 24.
2. For each, count the alphabet steps to the carved letter above it; nine are 2 or fewer.
3. Do the same for the six places of 22-34 whose letter is not one of those (E, A, N, H, E, A).
4. For BERLINCLOCK, try taking the same number of steps off every shift and count the small ones left.
5. Score each count by how rare it is by chance; repeat on scrambled copies and compare.

## Worked example (generated)

```
plain table, Vigenere: shift = carved - known, as -13..12

place known carved shift  in KRYPTOS
   22     E      F     1  
   23     A      L    11  
   24     S      R    -1  yes
   25     T      V     2  yes
   26     N      Q     3  
   27     O      Q     2  yes
   28     R      P    -2  yes
   29     T      R    -2  yes
   30     H      N     6  
   31     E      G     2  
   32     A      K    10  
   33     S      S     0  yes
   34     T      S    -1  yes
   64     B      N    12  
   65     E      Y    -6  
   66     R      P    -2  yes
   67     L      V    10  
   68     I      T    11  
   69     N      T     6  
   70     C      M    10  
   71     L      Z   -12  
   72     O      F    -9  yes
   73     C      P   -13  
   74     K      K     0  yes
```

## Lineage

Inherits from 0287-f16.4-r-small-shifts-replicated-on-fresh-shuffles-thresholds-1-6. What changed: F16.4a (issue #123). 0287 replicated the small shifts at 22-34 (p 0.004-0.008). Seven of the ten known plaintext letters that are in KRYPTOS sit in 22-34, so 'by line' and 'by letter' are confounded. Three statistics, each the best binomial score over the 8 table-form pairs and the cut-offs 1-6, as 0287's T*: (1) CLASS: groups by plaintext letter (in KRYPTOS: 10 places; not: 14; N-Z: 12; A-M: 12); (2) APART: the line with the letters held apart (22-34 without its KRYPTOS letters: 6 places) and the letters with the line held apart (the KRYPTOS letters outside 22-34: 3 places), scored separately; (3) OFFSET: shifts within the cut-off of some offset 0-25, on line 3 (64-66), line 4 (67-74) and 64-74. Strength aimed at: sampled.

## Hypothesis (domain expert)

Bean's closeness (04-structure.md, 'The minor differences': for the ten known plaintext letters in KRYPTOS the carved letter is within 2 of it in 9, summing to 21; bean-2018-kryptos-thoughts.txt), C27(b) (carved lines). A shift that depends on the letter is what a keyword-mixed alphabet set against the plain one leaves (letters after the keyword's letters barely move); a shift that depends on the place is what a key of small steps on one line, or a small-step key plus an offset per line, leaves. Forced key k as 0287. Null: shuffles of the 97 carved letters, known letters kept. Seen at the desk before this run, so descriptive, not tests: CLASS's KRYPTOS group (9 of 10 within 2) and APART's raw counts (3 of 6 within 3; 2 of 3 within 2). OFFSET was looked at by hand for the plain table only. Lines: each statistic's p against 100,000 shuffles; below 0.01 counts as carrying the pattern. The row that follows depends on which does: CLASS only: alphabets (F16.4d first); APART's line part or OFFSET: line-keyed schemes (F16.4b, F16.4c).

## Prediction

CLASS is the strongest (p below 0.002), by its KRYPTOS group. APART: the line without those letters is ordinary (p above 0.05); the letters outside the line cannot reach a small p with 3 places. OFFSET ordinary (p above 0.05). So the pattern goes with the letters, not the line.

## Method

1. For each of the 8 table-form pairs the forced key at the 24 known places.
2. CLASS, APART (two parts), OFFSET as defined, each the best -log10 binomial tail over tables, cut-offs 1-6 (and offsets 0-25 for OFFSET) and its groups.
3. K4 and 100,000 shuffles (200 jobs of 500, own seeds).
4. Sixteen plants (four of each kind), each against 2,000 own shuffles: a small-step key on carved line 2 only; a dictionary keyword alphabet on the plain side with a small-step key; a small-step key plus an offset per carved line; a random key.

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
 "item": "F16.4a",
 "shuffles": 100000,
 "thresholds": [
  1,
  2,
  3,
  4,
  5,
  6
 ],
 "tables": "standard and KRYPTOS, plain and cipher side; Vigenere and Beaufort (8)",
 "groups": {
  "CLASS": {
   "in KRYPTOS": [
    24,
    25,
    27,
    28,
    29,
    33,
    34,
    66,
    72,
    74
   ],
   "not in KRYPTOS": [
    22,
    23,
    26,
    30,
    31,
    32,
    64,
    65,
    67,
    68,
    69,
    70,
    71,
    73
   ],
   "N-Z": [
    24,
    25,
    26,
    27,
    28,
    29,
    33,
    34,
    66,
    69,
    72
   ],
   "A-M": [
    22,
    23,
    30,
    31,
    32,
    64,
    65,
    67,
    68,
    70,
    71,
    73,
    74
   ]
  },
  "APART_line": {
   "22-34 without KRYPTOS letters": [
    22,
    23,
    26,
    30,
    31,
    32
   ]
  },
  "APART_letters": {
   "KRYPTOS letters outside 22-34": [
    66,
    72,
    74
   ]
  },
  "OFFSET": {
   "line 3 (64-66)": [
    64,
    65,
    66
   ],
   "line 4 (67-74)": [
    67,
    68,
    69,
    70,
    71,
    72,
    73,
    74
   ],
   "run 64-74": [
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
   ]
  }
 },
 "summary": {
  "CLASS": {
   "k4": 5.5266,
   "k4_argmax": [
    "std",
    "std",
    "vig",
    "in KRYPTOS",
    9,
    10,
    2
   ],
   "at_or_above": 12,
   "p": 0.00013,
   "quantiles": {
    "0.5": 1.786,
    "0.9": 2.696,
    "0.99": 3.607,
    "0.999": 4.624
   }
  },
  "APART_line": {
   "k4": 1.8062,
   "k4_argmax": [
    "kry",
    "std",
    "vig",
    "22-34 without KRYPTOS letters",
    6,
    6,
    6
   ],
   "at_or_above": 20463,
   "p": 0.204638,
   "quantiles": {
    "0.5": 1.279,
    "0.9": 1.832,
    "0.99": 2.878,
    "0.999": 3.955
   }
  },
  "APART_letters": {
   "k4": 1.0145,
   "k4_argmax": [
    "std",
    "std",
    "vig",
    "KRYPTOS letters outside 22-34",
    2,
    3,
    2
   ],
   "at_or_above": 61491,
   "p": 0.614914,
   "quantiles": {
    "0.5": 1.121,
    "0.9": 1.71,
    "0.99": 2.814,
    "0.999": 2.814
   }
  },
  "OFFSET": {
   "k4": 2.9886,
   "k4_argmax": [
    "kry",
    "std",
    "vig",
    "line 4 (67-74)",
    8,
    8,
    5,
    5
   ],
   "at_or_above": 27525,
   "p": 0.275257,
   "quantiles": {
    "0.5": 2.696,
    "0.9": 3.311,
    "0.99": 4.27,
    "0.999": 5.426
   }
  }
 },
 "carried_by": [
  "CLASS"
 ],
 "line": "p < 0.01 per statistic (three questions: 0.0033 if corrected)",
 "seen_before_the_run": "CLASS's KRYPTOS group (9 of 10 within 2) and APART's raw counts on the plain table",
 "plants": [
  {
   "kind": "line2",
   "word": null,
   "offsets": null,
   "p": {
    "CLASS": 0.0575,
    "APART_line": 0.001,
    "APART_letters": 0.8631,
    "OFFSET": 0.4988
   },
   "flagged": [
    "APART_line"
   ],
   "expected": [
    "APART_line"
   ],
   "as_expected": true,
   "sizes": {
    "CLASS": {
     "in KRYPTOS": 10,
     "not in KRYPTOS": 14,
     "N-Z": 11,
     "A-M": 13
    },
    "APART_line": {
     "22-34 without KRYPTOS letters": 6
    },
    "APART_letters": {
     "KRYPTOS letters outside 22-34": 3
    },
    "OFFSET": {
     "line 3 (64-66)": 3,
     "line 4 (67-74)": 8,
     "run 64-74": 11
    }
   }
  },
  {
   "kind": "alphabet",
   "word": "BEARWORT",
   "offsets": null,
   "p": {
    "CLASS": 0.036,
    "APART_line": 0.1924,
    "APART_letters": 0.8936,
    "OFFSET": 0.022
   },
   "flagged": [],
   "expected": [
    "CLASS"
   ],
   "as_expected": false,
   "sizes": {
    "CLASS": {
     "in KRYPTOS": 10,
     "not in KRYPTOS": 14,
     "N-Z": 11,
     "A-M": 13
    },
    "APART_line": {
     "22-34 without KRYPTOS letters": 6
    },
    "APART_letters": {
     "KRYPTOS letters outside 22-34": 3
    },
    "OFFSET": {
     "line 3 (64-66)": 3,
     "line 4 (67-74)": 8,
     "run 64-74": 11
    }
   }
  },
  {
   "kind": "offsets",
   "word": null,
   "offsets": {
    "1": 0,
    "2": 0,
    "3": 6,
    "4": 19
   },
   "p": {
    "CLASS": 0.032,
    "APART_line": 0.0005,
    "APART_letters": 0.2909,
    "OFFSET": 0.0005
   },
   "flagged": [
    "APART_line",
    "OFFSET"
   ],
   "expected": [
    "OFFSET"
   ],
   "as_expected": true,
   "sizes": {
    "CLASS": {
     "in KRYPTOS": 10,
     "not in KRYPTOS": 14,
     "N-Z": 11,
     "A-M": 13
    },
    "APART_line": {
     "22-34 without KRYPTOS letters": 6
    },
    "APART_letters": {
     "KRYPTOS letters outside 22-34": 3
    },
    "OFFSET": {
     "line 3 (64-66)": 3,
     "line 4 (67-74)": 8,
     "run 64-74": 11
    }
   }
  },
  {
   "kind": "random",
   "word": null,
   "offsets": null,
   "p": {
    "CLASS": 0.4058,
    "APART_line": 0.7046,
    "APART_letters": 0.1599,
    "OFFSET": 0.4343
   },
   "flagged": [],
   "expected": [],
   "as_expected": true,
   "sizes": {
    "CLASS": {
     "in KRYPTOS": 10,
     "not in KRYPTOS": 14,
     "N-Z": 11,
     "A-M": 13
    },
    "APART_line": {
     "22-34 without KRYPTOS letters": 6
    },
    "APART_letters": {
     "KRYPTOS letters outside 22-34": 3
    },
    "OFFSET": {
     "line 3 (64-66)": 3,
     "line 4 (67-74)": 8,
     "run 64-74": 11
    }
   }
  },
  {
   "kind": "line2",
   "word": null,
   "offsets": null,
   "p": {
    "CLASS": 0.0015,
    "APART_line": 0.0025,
    "APART_letters": 0.0445,
    "OFFSET": 0.4948
   },
   "flagged": [
    "CLASS",
    "APART_line"
   ],
   "expected": [
    "APART_line"
   ],
   "as_expected": true,
   "sizes": {
    "CLASS": {
     "in KRYPTOS": 10,
     "not in KRYPTOS": 14,
     "N-Z": 11,
     "A-M": 13
    },
    "APART_line": {
     "22-34 without KRYPTOS letters": 6
    },
    "APART_letters": {
     "KRYPTOS letters outside 22-34": 3
    },
    "OFFSET": {
     "line 3 (64-66)": 3,
     "line 4 (67-74)": 8,
     "run 64-74": 11
    }
   }
  },
  {
   "kind": "alphabet",
   "word": "DISASTER",
   "offsets": null,
   "p": {
    "CLASS": 0.0625,
    "APART_line": 0.0175,
    "APART_letters": 0.6402,
    "OFFSET": 0.031
   },
   "flagged": [],
   "expected": [
    "CLASS"
   ],
   "as_expected": false,
   "sizes": {
    "CLASS": {
     "in KRYPTOS": 10,
     "not in KRYPTOS": 14,
     "N-Z": 11,
     "A-M": 13
    },
    "APART_line": {
     "22-34 without KRYPTOS letters": 6
    },
    "APART_letters": {
     "KRYPTOS letters outside 22-34": 3
    },
    "OFFSET": {
     "line 3 (64-66)": 3,
     "line 4 (67-74)": 8,
     "run 64-74": 11
    }
   }
  },
  {
   "kind": "offsets",
   "word": null,
   "offsets": {
    "1": 0,
    "2": 0,
    "3": 10,
    "4": 21
   },
   "p": {
    "CLASS": 0.002,
    "APART_line": 0.0035,
    "APART_letters": 0.3493,
    "OFFSET": 0.001
   },
   "flagged": [
    "CLASS",
    "APART_line",
    "OFFSET"
   ],
   "expected": [
    "OFFSET"
   ],
   "as_expected": true,
   "sizes": {
    "CLASS": {
     "in KRYPTOS": 10,
     "not in KRYPTOS": 14,
     "N-Z": 11,
     "A-M": 13
    },
    "APART_line": {
     "22-34 without KRYPTOS letters": 6
    },
    "APART_letters": {
     "KRYPTOS letters outside 22-34": 3
    },
    "OFFSET": {
     "line 3 (64-66)": 3,
     "line 4 (67-74)": 8,
     "run 64-74": 11
    }
   }
  },
  {
   "kind": "random",
   "word": null,
   "offsets": null,
   "p": {
    "CLASS": 0.4928,
    "APART_line": 0.2639,
    "APART_letters": 0.7376,
    "OFFSET": 0.5447
   },
   "flagged": [],
   "expected": [],
   "as_expected": true,
   "sizes": {
    "CLASS": {
     "in KRYPTOS": 10,
     "not in KRYPTOS": 14,
     "N-Z": 11,
     "A-M": 13
    },
    "APART_line": {
     "22-34 without KRYPTOS letters": 6
    },
    "APART_letters": {
     "KRYPTOS letters outside 22-34": 3
    },
    "OFFSET": {
     "line 3 (64-66)": 3,
     "line 4 (67-74)": 8,
     "run 64-74": 11
    }
   }
  },
  {
   "kind": "line2",
   "word": null,
   "offsets": null,
   "p": {
    "CLASS": 0.007,
    "APART_line": 0.0005,
    "APART_letters": 0.018,
    "OFFSET": 0.7256
   },
   "flagged": [
    "CLASS",
    "APART_line"
   ],
   "expected": [
    "APART_line"
   ],
   "as_expected": true,
   "sizes": {
    "CLASS": {
     "in KRYPTOS": 10,
     "not in KRYPTOS": 14,
     "N-Z": 11,
     "A-M": 13
    },
    "APART_line": {
     "22-34 without KRYPTOS letters": 6
    },
    "APART_letters": {
     "KRYPTOS letters outside 22-34": 3
    },
    "OFFSET": {
     "line 3 (64-66)": 3,
     "line 4 (67-74)": 8,
     "run 64-74": 11
    }
   }
  },
  {
   "kind": "alphabet",
   "word": "UNFITTING",
   "offsets": null,
   "p": {
    "CLASS": 0.0005,
    "APART_line": 0.0115,
    "APART_letters": 0.8701,
    "OFFSET": 0.0505
   },
   "flagged": [
    "CLASS"
   ],
   "expected": [
    "CLASS"
   ],
   "as_expected": true,
   "sizes": {
    "CLASS": {
     "in KRYPTOS": 10,
     "not in KRYPTOS": 14,
     "N-Z": 11,
     "A-M": 13
    },
    "APART_line": {
     "22-34 without KRYPTOS letters": 6
    },
    "APART_letters": {
     "KRYPTOS letters outside 22-34": 3
    },
    "OFFSET": {
     "line 3 (64-66)": 3,
     "line 4 (67-74)": 8,
     "run 64-74": 11
    }
   }
  },
  {
   "kind": "offsets",
   "word": null,
   "offsets": {
    "1": 0,
    "2": 0,
    "3": 6,
    "4": 12
   },
   "p": {
    "CLASS": 0.0365,
    "APART_line": 0.0005,
    "APART_letters": 0.1344,
    "OFFSET": 0.0015
   },
   "flagged": [
    "APART_line",
    "OFFSET"
   ],
   "expected": [
    "OFFSET"
   ],
   "as_expected": true,
   "sizes": {
    "CLASS": {
     "in KRYPTOS": 10,
     "not in KRYPTOS": 14,
     "N-Z": 11,
     "A-M": 13
    },
    "APART_line": {
     "22-34 without KRYPTOS letters": 6
    },
    "APART_letters": {
     "KRYPTOS letters outside 22-34": 3
    },
    "OFFSET": {
     "line 3 (64-66)": 3,
     "line 4 (67-74)": 8,
     "run 64-74": 11
    }
   }
  },
  {
   "kind": "random",
   "word": null,
   "offsets": null,
   "p": {
    "CLASS": 0.969,
    "APART_line": 0.919,
    "APART_letters": 0.7551,
    "OFFSET": 0.2594
   },
   "flagged": [],
   "expected": [],
   "as_expected": true,
   "sizes": {
    "CLASS": {
     "in KRYPTOS": 10,
     "not in KRYPTOS": 14,
     "N-Z": 11,
     "A-M": 13
    },
    "APART_line": {
     "22-34 without KRYPTOS letters": 6
    },
    "APART_letters": {
     "KRYPTOS letters outside 22-34": 3
    },
    "OFFSET": {
     "line 3 (64-66)": 3,
     "line 4 (67-74)": 8,
     "run 64-74": 11
    }
   }
  },
  {
   "kind": "line2",
   "word": null,
   "offsets": null,
   "p": {
    "CLASS": 0.001,
    "APART_line": 0.002,
    "APART_letters": 0.6192,
    "OFFSET": 0.1564
   },
   "flagged": [
    "CLASS",
    "APART_line"
   ],
   "expected": [
    "APART_line"
   ],
   "as_expected": true,
   "sizes": {
    "CLASS": {
     "in KRYPTOS": 10,
     "not in KRYPTOS": 14,
     "N-Z": 11,
     "A-M": 13
    },
    "APART_line": {
     "22-34 without KRYPTOS letters": 6
    },
    "APART_letters": {
     "KRYPTOS letters outside 22-34": 3
    },
    "OFFSET": {
     "line 3 (64-66)": 3,
     "line 4 (67-74)": 8,
     "run 64-74": 11
    }
   }
  },
  {
   "kind": "alphabet",
   "word": "ASPHETERISM",
   "offsets": null,
   "p": {
    "CLASS": 0.1044,
    "APART_line": 0.029,
    "APART_letters": 0.7401,
    "OFFSET": 0.022
   },
   "flagged": [],
   "expected": [
    "CLASS"
   ],
   "as_expected": false,
   "sizes": {
    "CLASS": {
     "in KRYPTOS": 10,
     "not in KRYPTOS": 14,
     "N-Z": 11,
     "A-M": 13
    },
    "APART_line": {
     "22-34 without KRYPTOS letters": 6
    },
    "APART_letters": {
     "KRYPTOS letters outside 22-34": 3
    },
    "OFFSET": {
     "line 3 (64-66)": 3,
     "line 4 (67-74)": 8,
     "run 64-74": 11
    }
   }
  },
  {
   "kind": "offsets",
   "word": null,
   "offsets": {
    "1": 0,
    "2": 0,
    "3": 12,
    "4": 4
   },
   "p": {
    "CLASS": 0.0245,
    "APART_line": 0.001,
    "APART_letters": 0.993,
    "OFFSET": 0.0015
   },
   "flagged": [
    "APART_line",
    "OFFSET"
   ],
   "expected": [
    "OFFSET"
   ],
   "as_expected": true,
   "sizes": {
    "CLASS": {
     "in KRYPTOS": 10,
     "not in KRYPTOS": 14,
     "N-Z": 11,
     "A-M": 13
    },
    "APART_line": {
     "22-34 without KRYPTOS letters": 6
    },
    "APART_letters": {
     "KRYPTOS letters outside 22-34": 3
    },
    "OFFSET": {
     "line 3 (64-66)": 3,
     "line 4 (67-74)": 8,
     "run 64-74": 11
    }
   }
  },
  {
   "kind": "random",
   "word": null,
   "offsets": null,
   "p": {
    "CLASS": 0.8471,
    "APART_line": 0.3393,
    "APART_letters": 0.8431,
    "OFFSET": 0.7121
   },
   "flagged": [],
   "expected": [],
   "as_expected": true,
   "sizes": {
    "CLASS": {
     "in KRYPTOS": 10,
     "not in KRYPTOS": 14,
     "N-Z": 11,
     "A-M": 13
    },
    "APART_line": {
     "22-34 without KRYPTOS letters": 6
    },
    "APART_letters": {
     "KRYPTOS letters outside 22-34": 3
    },
    "OFFSET": {
     "line 3 (64-66)": 3,
     "line 4 (67-74)": 8,
     "run 64-74": 11
    }
   }
  }
 ],
 "plants_as_expected": "13 of 16",
 "controls": "100000 shuffles of K4 with the known letters kept in place",
 "exhaustive": true,
 "aws_cost_estimate_dollars": 0.05
}
```

Notes: CLASS: K4 5.5266 ('std', 'std', 'vig', 'in KRYPTOS', 9, 10, 2) p 0.00013; APART_line: K4 1.8062 ('kry', 'std', 'vig', '22-34 without KRYPTOS letters', 6, 6, 6) p 0.204638; APART_letters: K4 1.0145 ('std', 'std', 'vig', 'KRYPTOS letters outside 22-34', 2, 3, 2) p 0.614914; OFFSET: K4 2.9886 ('kry', 'std', 'vig', 'line 4 (67-74)', 8, 8, 5, 5) p 0.275257; carried by ['CLASS']; plants as expected 13/16


