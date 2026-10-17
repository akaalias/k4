# 0195-gromark-free-alphabet-other-bases: F5.2: Gromark on a free mixed alphabet: three-term rules in bases 2-9, 11-16 and 26, and two-term rules with longer lags (base 10 to 8, other bases to 6): exact

**Family:** 5-gromark  
**Parent:** 0107-three-term-gromark-with-a-free-alphabet  
**Decision:** reverted  
**Run:** 2026-10-17T01:34:57+00:00, 161.8 s, status ran  
**Time by phase:** design 0 s, implement 0 s, test 0 s, run 162 s, record 0 s

## In plain words

A Gromark key is a run of digits that grows by adding earlier digits together. Scheidt mentioned other number bases. We try the three-term and longer two-term rules in every base from 2 to 16 and 26, every starting digits, with any mixed alphabet, and see whether any fits the 24 known letters.

## Walkthrough, by hand

1. Base 16, rule 'add the digits 1, 3 and 6 places back', primer of 6 hex digits.
2. Places 26 and 27 carve Q twice from N and O: in form M[P+d]=c, N + d26 and O + d27 must be the same slot.
3. So d26 - d27 must be exactly 1; most primers fail here at once.
4. A survivor must give one-to-one slots for all 24 known letters.
5. Every primer, rule, base and form; then scrambled copies.

## Worked example (generated)

```
base 16, each digit the sum of the digits 1, 3 and 6 places back, primer 1 2 3 4 5 6:
1 2 3 4 5 6 11 2 11 10 1 2 7 10 7 8 3 12 11 8 11 14 9 0 9 10 5 12 15 4 9 2 11 0
places 26 and 27 (N, O over Q, Q), form M[P+d]=c: need d26 - d27 = 1; here 10 - 5 = 5
```

## Lineage

Inherits from 0107-three-term-gromark-with-a-free-alphabet. What changed: F5.2. 0107 closed three-term Gromark on a free alphabet in base 10 (lags up to 6); two-term free-alphabet rules were closed to lag 6 in base 10 and lag 5 in other bases (0069, 0076). Here, with 0107's decider compiled: three-term rules d[i] = d[i-a] + d[i-b] + d[i-c] mod B, 1 <= a < b < c <= 6, every primer, in bases 2-9 and 11-16 (base 26 to c = 5; c = 6 there is 3 billion primers, blocked by cost); two-term rules with b = 7, 8 in base 10 and b = 6 in bases 2-9, 11-16. Four forms (M[P+d]=c, M[P-d]=c, M[C-d]=p, M[C+d]=p), M a free alphabet; same known letters fix digit differences, then the partial one-to-one check. K4 against 10 shuffled copies; plants.

## Hypothesis (domain expert)

C22(a) (YAR as a Gromark primer), C4(b) ('base 16', non-standard bases; Scheidt), F5. Model as 0107 with base B and the rule's lags. Exhaustive over primers. Statistic: consistent (rule, primer, form) settings, K4 against copies.

## Prediction

No setting consistent on K4 or the copies, as in 0107; plants found. Zero candidates.

## Method

1. For each base, rule and form: equal-letter pairs among the known letters fix digit differences (or kill the form).
2. Every primer (compiled, 4 processes): the digit stream to place 74, the pair checks, then the one-to-one check.
3. K4, 10 shuffled copies, 2 planted texts.

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
   0,
   0,
   0,
   0,
   0,
   0
  ],
  "plants": [
   1,
   1
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
 "seconds": 162,
 "exhaustive": true
}
```

Notes: 1,546,784,471 primers x 4 forms; consistent K4 0 (copies 0-0); plants [1, 1]


