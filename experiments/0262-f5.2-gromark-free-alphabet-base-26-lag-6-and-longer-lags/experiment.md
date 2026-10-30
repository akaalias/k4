# 0262-f5.2-gromark-free-alphabet-base-26-lag-6-and-longer-lags: F5.2: Gromark on a free mixed alphabet, the rules 0195 left for cost: three-term base 26 to lag 6, three-term lag 7 in bases 2-16, two-term base 26 lags 6-7, two-term lags 7-8 in bases 2-16, base 10 lags 9-10: exact

**Family:** 5-gromark  
**Parent:** 0195-gromark-free-alphabet-other-bases  
**Decision:** reverted  
**Run:** 2026-10-30T10:49:06+00:00, 1251.3 s, status ran  
**Time by phase:** unattributed 13892 s, run 1251 s, record 0 s

## In plain words

A Gromark key is a run of digits that grows by adding earlier digits together, from a few starting digits. Some longer versions, and the version that counts in 26s (one digit per letter), were never tried because they took too long. Now there is no time limit, so every starting run is tried for each of them, with any scrambled alphabet, to see whether any fits the 24 known letters.

## Walkthrough, by hand

1. Base 26, rule 'add the digits 1, 3 and 6 places back', primer of 6 digits 0-25 (a six-letter word read A=0).
2. Grow the digit stream to place 74.
3. Places 26 and 27 carve Q twice from N and O: in form M[P+d]=c, N + d26 and O + d27 must be the same slot, so d26 - d27 must be 1 (or -25).
4. A survivor must give one-to-one slots for all 24 known letters.
5. Every primer, rule and form; then the scrambled copies.

## Worked example (generated)

```
base 16, each digit the sum of the digits 1, 3 and 6 places back, primer 1 2 3 4 5 6:
1 2 3 4 5 6 11 2 11 10 1 2 7 10 7 8 3 12 11 8 11 14 9 0 9 10 5 12 15 4 9 2 11 0
places 26 and 27 (N, O over Q, Q), form M[P+d]=c: need d26 - d27 = 1; here 10 - 5 = 5
```

## Lineage

Inherits from 0195-gromark-free-alphabet-other-bases. What changed: F5.2, reopened by D2 (0252): 0195 left three-term base 26 at lag 6 (3.1 billion primers) and longer two-term lags blocked under the old 30-minute budget; issue #96 removed the time limit. Same compiled exact test as 0195 (equal known letters fix digit differences, then the one-to-one check on the free alphabet), now split by the primer's last digit so the work spreads over any number of workers; the rule set widened to every rule up to about 2.3 x 10^11 primers in total.

## Hypothesis (domain expert)

C22(a) (YAR as a Gromark primer; base 26 lets a letter primer be read directly as digits), C4(b) (Scheidt's other bases), F5. Model as 0107/0195: d[i] = sum of d[i - lag] over the rule's two or three lags mod B, the primer the first max(lag) digits, four forms M[P+d]=c, M[P-d]=c, M[C-d]=p, M[C+d]=p with M a free alphabet. Exhaustive over primers. Statistic: consistent (rule, primer, form) settings, K4 against 10 shuffled copies; three plants.

## Prediction

No setting consistent on K4 or the copies (as 0195); every plant found. Zero candidates.

## Method

1. For each base, rule and form: equal letters among the known places fix digit differences (or kill the form).
2. Every primer, split by its last digit into one job per (rule, digit): the digit stream to place 74, the pair checks, then the one-to-one check.
3. K4, 10 shuffled copies (0195's seed) and 3 planted texts in the same scan.

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
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   3,
   0
  ],
  "plants": [
   4,
   1,
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
 "seconds": 1230,
 "exhaustive": true,
 "cost_estimate": "2.34e11 primers at about 2.4 million per core-second with 14 texts (desk timing 2026-10-29): about 27 core-hours, about 1 h on 32 cores, about $1.5 of Modal credit (about $3.4 left after the margin)"
}
```

Notes: 234,092,726,300 primers x 4 forms; consistent K4 0 (copies 0-3); plants [4, 1, 2]


