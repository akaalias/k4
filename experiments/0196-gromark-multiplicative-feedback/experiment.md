# 0196-gromark-multiplicative-feedback: F5.1: Gromark with multiplicative feedback (each digit the product of two earlier ones) on a free mixed alphabet, bases 2-16 and 26, every primer: exact; YAR as a primer by subsumption

**Family:** 5-gromark  
**Parent:** 0195-gromark-free-alphabet-other-bases  
**Decision:** reverted  
**Run:** 2026-10-17T01:38:10+00:00, 56.3 s, status ran  
**Time by phase:** design 0 s, implement 0 s, test 0 s, run 56 s, record 0 s

## In plain words

A variation of the Gromark key: each new digit is the product, not the sum, of two earlier digits. We try every base from 2 to 16 and 26, every pair of earlier positions up to six back, every set of starting digits, with any mixed alphabet.

## Walkthrough, by hand

1. Base 10, rule 'multiply the digits 2 and 5 places back', primer of 5 digits.
2. The digit stream often collapses to zeros; then the key is constant and K4's three different carved letters under the known E rule it out at once.
3. Otherwise the same checks as the additive Gromark: equal known letters must land on equal slots.
4. Every primer, rule, base and form; then scrambled copies.

## Worked example (generated)

```
base 10, each digit the product of the digits 2 and 5 places back, primer 3 7 9 1 4:
3 7 9 1 4 3 8 7 8 8 4 4 8 2 4 8 6 4 2 6 6 6 4 2 4 2 4 8 8 2 6 8 8 4 6 4 8 2 2 2
```

## Lineage

Inherits from 0195-gromark-free-alphabet-other-bases. What changed: F5.1. Every Gromark rule tested so far adds earlier digits. Here d[i] = d[i-a] * d[i-b] mod B, 1 <= a < b <= 6, every primer, bases 2-16 (base 26 with b <= 5: lag 6 is 1.5 billion primers), four forms, a free mixed alphabet, with 0195's compiled decider in product mode. YAR as a primer (Y A R as 24 0 17 in base 26, or any digits) is one of the primers every exhaustive sweep already enumerates (0076 two-term base 26, 0195 three-term base 26), so it is closed by subsumption.

## Hypothesis (domain expert)

F5.1 (low value: no creator remark points here), C22(a) (YAR as a primer). Model as 0107/0195 with the recurrence multiplicative. Statistic: consistent (rule, primer, form) settings, K4 against 10 copies; plants.

## Prediction

No setting consistent on K4 or the copies. Zero candidates.

## Method

1. For each base, rule and form: equal-letter pairs fix digit differences (or kill the form).
2. Every primer (compiled, 4 processes), product recurrence, pair checks, then the one-to-one check.
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
 "family": "Gromark with multiplicative feedback d[i] = d[i-a] d[i-b] mod B, free mixed alphabet, bases 2-16 (lags to 6) and 26 (lags to 5), four forms, exact",
 "rule_jobs": 235,
 "primers": 299394061,
 "per_base": {
  "2": {
   "rules": 15,
   "primers": 516,
   "k4": 0
  },
  "3": {
   "rules": 15,
   "primers": 4923,
   "k4": 0
  },
  "4": {
   "rules": 15,
   "primers": 25488,
   "k4": 0
  },
  "5": {
   "rules": 15,
   "primers": 92775,
   "k4": 0
  },
  "6": {
   "rules": 15,
   "primers": 268740,
   "k4": 0
  },
  "7": {
   "rules": 15,
   "primers": 663411,
   "k4": 0
  },
  "8": {
   "rules": 15,
   "primers": 1455168,
   "k4": 0
  },
  "9": {
   "rules": 15,
   "primers": 2914623,
   "k4": 0
  },
  "10": {
   "rules": 15,
   "primers": 5432100,
   "k4": 0
  },
  "11": {
   "rules": 15,
   "primers": 9548715,
   "k4": 0
  },
  "12": {
   "rules": 15,
   "primers": 15991056,
   "k4": 0
  },
  "13": {
   "rules": 15,
   "primers": 25709463,
   "k4": 0
  },
  "14": {
   "rules": 15,
   "primers": 39919908,
   "k4": 0
  },
  "15": {
   "rules": 15,
   "primers": 60149475,
   "k4": 0
  },
  "16": {
   "rules": 15,
   "primers": 88285440,
   "k4": 0
  },
  "26": {
   "rules": 10,
   "primers": 48932260,
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
   32
  ]
 },
 "plants": [
  {
   "base": 13,
   "lags": [
    1,
    4
   ],
   "primer": [
    1,
    5,
    2,
    3
   ]
  },
  {
   "base": 26,
   "lags": [
    2,
    5
   ],
   "primer": [
    16,
    18,
    10,
    20,
    19
   ]
  }
 ],
 "k4_consistent": [],
 "blocked": "base 26 with lag 6 (1.5 billion primers)",
 "yar_primer": "subsumed: every primer enumerated in 0076 and 0195",
 "copies": "10 shuffled copies (seed 1970)",
 "seconds": 56,
 "exhaustive": true
}
```

Notes: 299,394,061 primers x 4 forms; consistent K4 0 (copies 0-0); plants [1, 32]


