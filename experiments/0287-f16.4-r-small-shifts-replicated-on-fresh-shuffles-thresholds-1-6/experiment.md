# 0287-f16.4-r-small-shifts-replicated-on-fresh-shuffles-thresholds-1-6: F16.4-r: 0286's small-shift flag (10 of 13 shifts within 3 at 22-34 on the plain table, p 0.0065) on 100,000 fresh shuffles, and the same statistic maximised over the thresholds 1-6 as well, since the threshold 3 was picked after the review had seen K4's shifts

**Family:** 16-simple-hand-methods  
**Parent:** 0286-f16.4-small-shifts-per-crib-and-carved-line-pre-registered  
**Decision:** reverted  
**Run:** 2026-11-19T08:58:33+00:00, 93.3 s, status ran  
**Time by phase:** implement 5 s, test 160 s, run 93 s, record 0 s

## In plain words

The first test found that K4's known letters near EASTNORTHEAST sit unusually close to the carved letters, closer than all but 64 of 10,000 scrambled copies. But the cut-off for 'close' (three steps) was chosen after looking at K4. Here we repeat the count on 100,000 new scrambled copies and also let every copy pick its own best cut-off from one to six steps, which is the fair comparison.

## Walkthrough, by hand

1. Under each known letter of EASTNORTHEAST write the carved letter above it.
2. Count the alphabet steps between them (E to F is 1, A to L is 11, S to R is 1 back).
3. For a cut-off of 3 steps, 10 of the 13 are close; for 2 steps, 9; for 1 step,
4. 4. Work out how surprising each count is when letters fall by chance, and keep the most surprising.
5. Do exactly the same on scrambled copies of K4 and count how many are at least as surprising.

## Worked example (generated)

```
plain table, Vigenere: shift = carved - known, as -13..12

place known carved shift
   22     E      F     1
   23     A      L    11
   24     S      R    -1
   25     T      V     2
   26     N      Q     3
   27     O      Q     2
   28     R      P    -2
   29     T      R    -2
   30     H      N     6
   31     E      G     2
   32     A      K    10
   33     S      S     0
   34     T      S    -1

within 1: 4 of 13; P(>= 4 of 13 at 3/26) = 5.39e-02
within 2: 9 of 13; P(>= 9 of 13 at 5/26) = 1.21e-04
within 3: 10 of 13; P(>= 10 of 13 at 7/26) = 2.47e-04
within 4: 10 of 13; P(>= 10 of 13 at 9/26) = 2.29e-03
within 5: 10 of 13; P(>= 10 of 13 at 11/26) = 1.24e-02
within 6: 11 of 13; P(>= 11 of 13 at 13/26) = 1.12e-02
```

## Lineage

Inherits from 0286-f16.4-small-shifts-per-crib-and-carved-line-pre-registered. What changed: F16.4-r (issue #123). 0286's statistic T crossed its line (p 0.0065 < 0.01, 64 of 10,000 shuffles). A result outside the copies stops the queue and is replicated first. Two changes: (1) the same T against 100,000 fresh shuffles (new seeds), on all 24 letters and on the 20 official letters alone; (2) T* = the same maximum taken over the thresholds |k| <= 1..6 as well (each scored by its own binomial tail at (2t+1)/26), for K4 and for every shuffle: the threshold 3 was chosen by the step-back review after it had seen BLZCDCYYGCKAZ, so T's p is too small by the choice of threshold, and T* pays for that choice. Strength aimed at: sampled, 100,000 shuffles.

## Hypothesis (domain expert)

Bean's closeness (04-structure.md, 'The minor differences'; bean-2018-kryptos-thoughts.txt), C27(b) (carved lines), as 0286. Forced key k = A_c(c) - A_p(p) (Vigenere) or A_c(c) + A_p(p) (Beaufort) as -13..12, tables in {standard, KRYPTOS}^2, groups as 0286 (the two runs, the four words, carved lines 3 and 4, all 24, the 20 official). T (threshold 3) and T* (thresholds 1-6). Null: shuffles of the 97 carved letters with the known letters kept where they are. Lines fixed before the run: T replicates if p < 0.01 on the fresh shuffles; the flag stands as a lead only if T*'s p is also below 0.01; between the two it is recorded as 'at the edge, threshold-dependent' and the line-keyed rows are still added (run more experiments, #100) with that label.

## Prediction

T replicates (p between 0.004 and 0.01 on 100,000 shuffles). T* is weaker: p between 0.01 and 0.05, so the flag is threshold-dependent. On the 20 official letters alone (NORTHEAST 7 of 9) p is above 0.05.

## Method

1. For each of the 8 table-form pairs, the forced key at the known places, as a distance 0-13 from zero.
2. For each threshold t in 1-6 and each of the 10 groups, count distances <= t and score the count by the binomial tail at (2t+1)/26.
3. T = best score at t = 3; T* = best score over t = 1-6.
4. K4 and 100,000 shuffles (200 jobs of 500, each its own seed), on the 24 and on the 20 official letters.
5. p = (1 + shuffles at or above) / 100,001.
6. Plants as 0286: five messages (four with small shifts, one without), each against 2,000 own shuffles on T*.

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
 "item": "F16.4-r",
 "shuffles": 100000,
 "seeds": "16450000..16450199",
 "thresholds": [
  1,
  2,
  3,
  4,
  5,
  6
 ],
 "statistics": "T: 0286's (threshold 3). T*: the same maximum over thresholds 1-6, each count scored by its binomial tail at (2t+1)/26",
 "summary": {
  "k24": {
   "k4_T": 3.607,
   "k4_T_argmax": [
    "std",
    "std",
    "vig",
    "run 22-34",
    10,
    13,
    3
   ],
   "T_at_or_above": 401,
   "p_T": 0.00402,
   "k4_Tstar": 3.9187,
   "k4_Tstar_argmax": [
    "std",
    "std",
    "vig",
    "run 22-34",
    9,
    13,
    2
   ],
   "Tstar_at_or_above": 794,
   "p_Tstar": 0.00795,
   "T_quantiles": {
    "0.5": 1.444,
    "0.9": 2.28,
    "0.99": 3.388,
    "0.999": 4.141
   },
   "Tstar_quantiles": {
    "0.5": 2.038,
    "0.9": 2.872,
    "0.99": 3.838,
    "0.999": 4.855
   }
  },
  "k20": {
   "k4_T": 2.6655,
   "k4_T_argmax": [
    "std",
    "std",
    "vig",
    "NORTHEAST",
    7,
    9,
    3
   ],
   "T_at_or_above": 4991,
   "p_T": 0.04992,
   "k4_Tstar": 2.6655,
   "k4_Tstar_argmax": [
    "std",
    "std",
    "vig",
    "NORTHEAST",
    7,
    9,
    3
   ],
   "Tstar_at_or_above": 14570,
   "p_Tstar": 0.145709,
   "T_quantiles": {
    "0.5": 1.429,
    "0.9": 2.182,
    "0.99": 3.203,
    "0.999": 3.724
   },
   "Tstar_quantiles": {
    "0.5": 1.892,
    "0.9": 2.764,
    "0.99": 3.724,
    "0.999": 4.689
   }
  }
 },
 "k4_small_counts_22_34_plain_table": {
  "1": 4,
  "2": 9,
  "3": 10,
  "4": 10,
  "5": 10,
  "6": 11
 },
 "k4_shifts_22_34_plain_table": [
  1,
  11,
  -1,
  2,
  3,
  2,
  -2,
  -2,
  6,
  2,
  10,
  0,
  -1
 ],
 "lines": "T replicates below 0.01; a lead only if T* is below 0.01 too",
 "verdict": "replicated on both statistics",
 "plants": [
  {
   "what": "small digits 0-3, period 7, plain table, whole text",
   "Tstar": 13.677,
   "argmax": [
    "std",
    "std",
    "vig",
    "all 24",
    24,
    24,
    3
   ],
   "p": 0.0005,
   "found": true,
   "should_be_found": true
  },
  {
   "what": "small digits 0-3, period 5, KRYPTOS table, whole text",
   "Tstar": 13.677,
   "argmax": [
    "kry",
    "kry",
    "vig",
    "all 24",
    24,
    24,
    3
   ],
   "p": 0.0005,
   "found": true,
   "should_be_found": true
  },
  {
   "what": "small digits on carved line 2 (places 5-35) only, a random key elsewhere",
   "Tstar": 7.408,
   "argmax": [
    "std",
    "std",
    "vig",
    "run 22-34",
    13,
    13,
    3
   ],
   "p": 0.0005,
   "found": true,
   "should_be_found": true
  },
  {
   "what": "Beaufort, small key values on carved line 4 (places 67-97) only",
   "Tstar": 4.559,
   "argmax": [
    "std",
    "std",
    "beau",
    "line 4 (67-74)",
    8,
    8,
    3
   ],
   "p": 0.002,
   "found": true,
   "should_be_found": true
  },
  {
   "what": "a random key everywhere (must not be found)",
   "Tstar": 2.073,
   "argmax": [
    "std",
    "kry",
    "vig",
    "line 4 (67-74)",
    4,
    8,
    1
   ],
   "p": 0.4768,
   "found": false,
   "should_be_found": false
  }
 ],
 "plants_as_expected": "5 of 5",
 "controls": "100000 shuffles of K4 with the known letters kept in place",
 "exhaustive": true,
 "aws_cost_estimate_dollars": 0.05
}
```

Notes: 24 letters: T p 0.00402 (401 of 100000), T* 3.9187 from ('std', 'std', 'vig', 'run 22-34', 9, 13, 2) p 0.00795 (794); 20 official: T p 0.04992, T* p 0.145709; verdict: replicated on both statistics; plants as expected 5/5


