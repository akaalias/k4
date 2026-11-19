# 0286-f16.4-small-shifts-per-crib-and-carved-line-pre-registered: F16.4: small shifts at the known places, per crib run and per carved line, maximised over the plain and KRYPTOS tables and both forms, a statistic fixed before looking; K4 against 10,000 shuffles

**Family:** 16-simple-hand-methods  
**Parent:** 0029-small-shift-keys-closeness-under-all-alphabets  
**Decision:** reverted  
**Run:** 2026-11-19T08:53:08+00:00, 76.6 s, status ran  
**Time by phase:** design 5 s, test 23 s, run 77 s, record 0 s

## In plain words

Under the plain Vigenere table, most of EASTNORTHEAST's letters sit only one to three places from the carved letters above them. That could mean a key of small numbers, or one that changes line by line on the copper. We fix one measure of 'how many small shifts in a group' before looking, take its best value on K4, and see how often scrambled copies of K4 do as well.

## Walkthrough, by hand

1. Under each known letter of EASTNORTHEAST write the carved letter above it.
2. Count how many alphabet steps separate them (E to F is 1, A to L is 11, S to R is -1).
3. Mark the steps of size 3 or less: 10 of the 13.
4. Ask how likely 10 or more of 13 is when each has a 7 in 26 chance: about 1 in 5,000.
5. Do the same for every group, table and form, keep the best, and compare with scrambled copies of K4 treated the same way.

## Worked example (generated)

```
plain table, Vigenere: shift = carved - known, as -13..12

place known carved shift small
   22     E      F     1  yes
   23     A      L    11  
   24     S      R    -1  yes
   25     T      V     2  yes
   26     N      Q     3  yes
   27     O      Q     2  yes
   28     R      P    -2  yes
   29     T      R    -2  yes
   30     H      N     6  
   31     E      G     2  yes
   32     A      K    10  
   33     S      S     0  yes
   34     T      S    -1  yes

10 of 13 small; P(>= 10 of 13 at 7/26) = 2.47e-04
```

## Lineage

Inherits from 0029-small-shift-keys-closeness-under-all-alphabets. What changed: F16.4 (issue #123). 0029 tested Bean's closeness by the largest shift over all 24 known places, which one far letter spoils; the step-back review saw that under the plain table EASTNORTHEAST forces BLZCDCYYGCKAZ, 10 of 13 shifts within 3. Here the statistic counts shifts within 3 in groups (each crib run, each word, each carved line's share of the known places, all 24, the 20 official), scores each count by its binomial tail at 7/26, and takes the best over groups, tables and forms; the same maximum on 10,000 shuffles of K4 gives the p.

## Hypothesis (domain expert)

Bean's closeness (04-structure.md, 'The minor differences'; Materna; bean-2018-kryptos-thoughts.txt): the carved letter sits near the known letter on the standard alphabet, read by Bean as a cipher alphabet near the standard one (Gromark-like). A Gronsfeld key of small digits, or a key that changes by carved line (C27(b), the 31-letter lines of the BERLIN chart; Sanborn's 'positioning'), would leave runs of small shifts. Definition, fixed before any count: forced key k = A_c(c) - A_p(p) (Vigenere) or A_c(c) + A_p(p) (Beaufort), mod 26 as -13..12, tables (A_p, A_c) in {standard, KRYPTOS}^2; a shift is small when |k| <= 3 (chance 7/26). Groups: 22-34, 64-74, each word (EAST, NORTHEAST, BERLIN, CLOCK), carved lines 2 (22-34), 3 (64-66) and 4 (67-74), all 24, the 20 official. Score per group: -log10 P(Binomial(n, 7/26) >= count). T = max over 8 table-form pairs x 10 groups. p = share of 10,000 shuffles with T at or above K4's. Flag at p < 0.01: then rows for line-keyed schemes.

## Prediction

K4's T comes from 22-34 under the plain table (10 of 13 small); the shuffles reach it often enough that p is above 0.01 (the closeness is one of many patterns a 97-letter text can show somewhere). No candidates.

## Method

1. For each of the 8 table-form pairs, the forced key at the 24 known places, as -13..12.
2. Count |k| <= 3 in each of the 10 groups; score by the binomial tail at 7/26.
3. T = the best score.
4. The same on 10,000 shuffles of K4 (seed 16400).
5. p = (1 + shuffles at or above) / 10,001.
6. Report the best group, table and form for K4, and the per-group p's as diagnostics only.
7. Plants: four messages with small shifts (whole text, one carved line) and one without, each against 2,000 shuffles of its own.

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
 "item": "F16.4",
 "statistic": "T = max over (plain table, cipher table) in {std, KRYPTOS}^2, form in {Vigenere, Beaufort}, group in 10 groups of -log10 P(Binomial(n, 7/26) >= count of |k| <= 3)",
 "groups": {
  "run 22-34": [
   22,
   23,
   24,
   25,
   26,
   27,
   28,
   29,
   30,
   31,
   32,
   33,
   34
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
  ],
  "EAST": [
   22,
   23,
   24,
   25
  ],
  "NORTHEAST": [
   26,
   27,
   28,
   29,
   30,
   31,
   32,
   33,
   34
  ],
  "BERLIN": [
   64,
   65,
   66,
   67,
   68,
   69
  ],
  "CLOCK": [
   70,
   71,
   72,
   73,
   74
  ],
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
  "all 24": [
   22,
   23,
   24,
   25,
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
  "official 20": [
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
  ]
 },
 "k4_T": 3.607,
 "k4_argmax": [
  "std",
  "std",
  "vig",
  "run 22-34",
  10,
  13
 ],
 "shuffles": 10000,
 "shuffles_at_or_above": 64,
 "p": 0.0065,
 "flag_line": 0.01,
 "flag": true,
 "shuffle_T_quantiles": {
  "0.5": 1.444,
  "0.9": 2.28,
  "0.99": 3.419,
  "0.999": 3.724
 },
 "k4_per_group": {
  "run 22-34": {
   "best_score": 3.607,
   "table_form_count": [
    "std",
    "std",
    "vig",
    "run 22-34",
    10,
    13
   ]
  },
  "run 64-74": {
   "best_score": 0.467,
   "table_form_count": [
    "kry",
    "kry",
    "beau",
    "run 64-74",
    4,
    11
   ]
  },
  "EAST": {
   "best_score": 1.206,
   "table_form_count": [
    "std",
    "std",
    "vig",
    "EAST",
    3,
    4
   ]
  },
  "NORTHEAST": {
   "best_score": 2.666,
   "table_form_count": [
    "std",
    "std",
    "vig",
    "NORTHEAST",
    7,
    9
   ]
  },
  "BERLIN": {
   "best_score": 0.292,
   "table_form_count": [
    "std",
    "std",
    "beau",
    "BERLIN",
    2,
    6
   ]
  },
  "CLOCK": {
   "best_score": 0.39,
   "table_form_count": [
    "std",
    "kry",
    "vig",
    "CLOCK",
    2,
    5
   ]
  },
  "line 3 (64-66)": {
   "best_score": 0.215,
   "table_form_count": [
    "std",
    "std",
    "vig",
    "line 3 (64-66)",
    1,
    3
   ]
  },
  "line 4 (67-74)": {
   "best_score": 0.432,
   "table_form_count": [
    "kry",
    "std",
    "vig",
    "line 4 (67-74)",
    3,
    8
   ]
  },
  "all 24": {
   "best_score": 1.874,
   "table_form_count": [
    "std",
    "std",
    "vig",
    "all 24",
    12,
    24
   ]
  },
  "official 20": {
   "best_score": 1.201,
   "table_form_count": [
    "std",
    "std",
    "vig",
    "official 20",
    9,
    20
   ]
  }
 },
 "plants": [
  {
   "what": "small digits 0-3, period 7, plain table, whole text",
   "T": 13.677,
   "argmax": [
    "std",
    "std",
    "vig",
    "all 24",
    24,
    24
   ],
   "p": 0.0005,
   "found": true,
   "should_be_found": true
  },
  {
   "what": "small digits 0-3, period 5, KRYPTOS table, whole text",
   "T": 13.677,
   "argmax": [
    "kry",
    "kry",
    "vig",
    "all 24",
    24,
    24
   ],
   "p": 0.0005,
   "found": true,
   "should_be_found": true
  },
  {
   "what": "small digits on carved line 2 (places 5-35) only, a random key elsewhere",
   "T": 7.408,
   "argmax": [
    "std",
    "std",
    "vig",
    "run 22-34",
    13,
    13
   ],
   "p": 0.0005,
   "found": true,
   "should_be_found": true
  },
  {
   "what": "Beaufort, small key values on carved line 4 (places 67-97) only",
   "T": 4.779,
   "argmax": [
    "std",
    "std",
    "beau",
    "run 64-74",
    10,
    11
   ],
   "p": 0.0005,
   "found": true,
   "should_be_found": true
  },
  {
   "what": "a random key everywhere (must not be found)",
   "T": 1.444,
   "argmax": [
    "std",
    "kry",
    "vig",
    "run 22-34",
    7,
    13
   ],
   "p": 0.5322,
   "found": false,
   "should_be_found": false
  }
 ],
 "plants_as_expected": "5 of 5",
 "controls": "10000 shuffles of K4, seed 16400",
 "exhaustive": true,
 "aws_cost_estimate_dollars": 0.02
}
```

Notes: K4 T 3.607 from ('std', 'std', 'vig', 'run 22-34', 10, 13); 64 of 10000 shuffles at or above, p 0.0065 (flag below 0.01: True); plants as expected 5/5


