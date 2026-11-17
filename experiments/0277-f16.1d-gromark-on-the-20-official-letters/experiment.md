# 0277-f16.1d-gromark-on-the-20-official-letters: F16.1d: Gromark with a free mixed alphabet on the 20 official known letters (EAST set aside): 0195 (bases 2-16 and 26, two- and three-term rules) and 0262 (the rules 0195 left, base 26 to lag 7), each run as recorded with only the known letters changed; K4 against their 10 copies, their plants

**Family:** 16-simple-hand-methods  
**Parent:** 0262-f5.2-gromark-free-alphabet-base-26-lag-6-and-longer-lags  
**Decision:** reverted  
**Run:** 2026-11-17T14:55:58+00:00, 3865.9 s, status ran  
**Time by phase:** test 18 s, run 3866 s, record 0 s

## In plain words

Gromark makes a long key of digits from a few starting digits, each new digit the sum of earlier ones, and adds it to the message letter by letter through a scrambled alphabet. Two past experiments tried every starting set for many rules and found none that fits the known letters, but they needed EAST. Here they run again with the 20 letters Sanborn published himself.

## Walkthrough, by hand

1. Choose a base (10), a rule (each new digit is the sum of the digits 5 and 1 places back, mod 10) and five starting digits.
2. Extend the digits to 97.
3. At each official known place, the carved letter must sit in the scrambled alphabet at the known letter's place plus the digit there.
4. If two places need the same carved letter at different places, or two letters at one place, the start fails.
5. Count the starts that never fail, on K4 and on scrambled copies.

## Worked example (generated)

```
base 16, each digit the sum of the digits 1, 3 and 6 places back, primer 1 2 3 4 5 6:
1 2 3 4 5 6 11 2 11 10 1 2 7 10 7 8 3 12 11 8 11 14 9 0 9 10 5 12 15 4 9 2 11 0
places 26 and 27 (N, O over Q, Q), form M[P+d]=c: need d26 - d27 = 1; here 10 - 5 = 5
```

## Lineage

Inherits from 0262-f5.2-gromark-free-alphabet-base-26-lag-6-and-longer-lags. What changed: F16.1 (issue #123), fourth part. 0195's and 0262's attack.py loaded from their records and run with only the 20 official known places (26-34, 64-74): their module-level list of known letters replaced, and their compiled C and Python loops, which count the known places as 24 (`e < 24`, `range(24)`, `range(k + 1, 24)`), told 20; each replacement asserted. Everything else as recorded: rules, bases, lags, primers, forms, copies, plants.

## Hypothesis (domain expert)

F5 Gromark (05-attacks.md: Bean 2021, 'Kryptos Thoughts'; Gillogly's suggestion 1999, 2004): a numeric running key from a primer expanded by a lagged sum mod a base, added to the plaintext's place in the standard alphabet and read off a free mixed cipher alphabet; four forms. 0195 and 0262 decided every primer of the listed rules exactly on 24 letters: no primer consistent on K4. Criteria revised 2026-11-17 (#124): EAST is second-hand. On 20 letters each primer faces 20 checks instead of 24, about 19 bits fewer; chance-consistent primers per rule rise by about 26^4 x (alphabet freedom), so some K4 and copy primers are expected to fit; the test is whether K4 has more than its copies. Bean's base-10 length-5 survivors (05-attacks.md) are inside 0195's space.

## Prediction

Consistent primers appear on K4 and on the 10 copies in about the same numbers (K4 inside the copies' range in both runs); plants found as in the originals (0195 2/2, 0262 3/3). No candidates (the alphabet stays partly free; readings not built).

## Method

1. Load 0195 and 0262 from their records; set their known letters to the 20 official ones and their loop counts to 20.
2. Run each as recorded.
3. Compare K4's consistent primers with the copies', and with the 24-letter records (both 0 on K4).

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
 "item": "F16.1d",
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
 "0195": {
  "bounds_20": {
   "family": "Gromark, free mixed alphabet: three-term bases 2-9, 11-16 (lags to 6), 26 (lags to 5); two-term base 10 lags 7-8, bases 2-9, 11-16 lag 6; four forms; exact",
   "rule_jobs": 373,
   "primers": 1546784471,
   "per_base": {
    "2": {
     "rules": 25,
     "primers": 1208,
     "k4": 0
    },
    "3": {
     "rules": 25,
     "primers": 12663,
     "k4": 0
    },
    "4": {
     "rules": 25,
     "primers": 68416,
     "k4": 0
    },
    "5": {
     "rules": 25,
     "primers": 255125,
     "k4": 0
    },
    "6": {
     "rules": 25,
     "primers": 750600,
     "k4": 0
    },
    "7": {
     "rules": 25,
     "primers": 1873123,
     "k4": 0
    },
    "8": {
     "rules": 25,
     "primers": 4141568,
     "k4": 0
    },
    "9": {
     "rules": 25,
     "primers": 8346321,
     "k4": 0
    },
    "11": {
     "rules": 25,
     "primers": 27584975,
     "k4": 0
    },
    "12": {
     "rules": 25,
     "primers": 46346688,
     "k4": 0
    },
    "13": {
     "rules": 25,
     "primers": 74717773,
     "k4": 0
    },
    "14": {
     "rules": 25,
     "primers": 116287976,
     "k4": 0
    },
    "15": {
     "rules": 25,
     "primers": 175570875,
     "k4": 0
    },
    "16": {
     "rules": 25,
     "primers": 258150400,
     "k4": 0
    },
    "26": {
     "rules": 10,
     "primers": 72676760,
     "k4": 0
    },
    "10": {
     "rules": 13,
     "primers": 760000000,
     "k4": 0
    }
   },
   "consistent": {
    "k4": 0,
    "copies": [
     0,
     0,
     0,
     0,
     2,
     3,
     0,
     0,
     0,
     0
    ],
    "plants": [
     23,
     2
    ]
   },
   "plants": [
    {
     "base": 16,
     "lags": [
      1,
      3,
      6
     ],
     "primer": [
      8,
      15,
      0,
      0,
      2,
      7
     ]
    },
    {
     "base": 10,
     "lags": [
      2,
      7
     ],
     "primer": [
      4,
      1,
      1,
      7,
      4,
      6,
      2
     ]
    }
   ],
   "k4_consistent": [],
   "blocked": "three-term base 26 with lag 6 (3.1 billion primers); two-term other bases beyond lag 6",
   "copies": "10 shuffled copies (seed 1940)",
   "seconds": 45,
   "exhaustive": true
  },
  "notes_20": "1,546,784,471 primers x 4 forms; consistent K4 0 (copies 0-3); plants [23, 2]",
  "notes_24": "1,546,784,471 primers x 4 forms; consistent K4 0 (copies 0-0); plants [1, 1]"
 },
 "0262": {
  "bounds_20": {
   "family": "Gromark, free mixed alphabet, the rules 0195 left: three-term base 26 lag 6; three-term lag 7 in bases 2-16; two-term base 26 lags 6-7; two-term lags 7-8 in bases 2-9, 11-16; two-term base 10 lags 9-10; four forms; exact",
   "rule_jobs": 445,
   "primers": 234092726300,
   "per_base": {
    "10": {
     "rules": 32,
     "primers": 98150000000,
     "k4": 0
    },
    "26": {
     "rules": 21,
     "primers": 52824597696,
     "k4": 0
    },
    "16": {
     "rules": 28,
     "primers": 35701915648,
     "k4": 0
    },
    "15": {
     "rules": 28,
     "primers": 21528281250,
     "k4": 0
    },
    "14": {
     "rules": 28,
     "primers": 12544206976,
     "k4": 0
    },
    "13": {
     "rules": 28,
     "primers": 7027833904,
     "k4": 0
    },
    "12": {
     "rules": 28,
     "primers": 3762339840,
     "k4": 0
    },
    "11": {
     "rules": 28,
     "primers": 1909742758,
     "k4": 0
    },
    "9": {
     "rules": 28,
     "primers": 401769396,
     "k4": 0
    },
    "8": {
     "rules": 28,
     "primers": 161480704,
     "k4": 0
    },
    "7": {
     "rules": 28,
     "primers": 57648010,
     "k4": 0
    },
    "6": {
     "rules": 28,
     "primers": 17635968,
     "k4": 0
    },
    "5": {
     "rules": 28,
     "primers": 4375000,
     "k4": 0
    },
    "4": {
     "rules": 28,
     "primers": 802816,
     "k4": 0
    },
    "3": {
     "rules": 28,
     "primers": 91854,
     "k4": 0
    },
    "2": {
     "rules": 28,
     "primers": 4480,
     "k4": 0
    }
   },
   "consistent": {
    "k4": 0,
    "copies": [
     1,
     60,
     65,
     16,
     1158,
     110,
     241,
     48,
     23,
     4
    ],
    "plants": [
     42,
     55,
     2
    ]
   },
   "plants": [
    {
     "base": 26,
     "lags": [
      1,
      3,
      6
     ],
     "primer": [
      8,
      15,
      21,
      0,
      25,
      0
     ]
    },
    {
     "base": 16,
     "lags": [
      2,
      8
     ],
     "primer": [
      1,
      10,
      9,
      2,
      3,
      14,
      9,
      12
     ]
    },
    {
     "base": 26,
     "lags": [
      2,
      7
     ],
     "primer": [
      17,
      17,
      16,
      2,
      22,
      13,
      8
     ]
    }
   ],
   "k4_consistent": [],
   "not_covered": "three-term lag 8 and beyond; two-term base 26 lag 8 and beyond (26^8 = 2.1e11 primers per rule); two-term lags beyond 8 outside base 10",
   "copies": "10 shuffled copies (seed 1940)",
   "seconds": 3756,
   "exhaustive": true,
   "cost_estimate": "2.34e11 primers at about 2.4 million per core-second with 14 texts (desk timing 2026-10-29): about 27 core-hours, about 1 h on 32 cores, about $1.5 of Modal credit (about $3.4 left after the margin)"
  },
  "notes_20": "234,092,726,300 primers x 4 forms; consistent K4 0 (copies 1-1158); plants [42, 55, 2]",
  "notes_24": "234,092,726,300 primers x 4 forms; consistent K4 0 (copies 0-3); plants [4, 1, 2]"
 },
 "aws_cost_estimate_dollars": 1.0,
 "modal_cost_estimate_dollars": 0
}
```

Notes: 0195: 1,546,784,471 primers x 4 forms; consistent K4 0 (copies 0-3); plants [23, 2] | 0262: 234,092,726,300 primers x 4 forms; consistent K4 0 (copies 1-1158); plants [42, 55, 2]


