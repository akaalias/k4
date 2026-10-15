# 0069-gromark-with-a-free-alphabet: Gromark with any mixed alphabet at all, not just ones built from the puzzle's words

**Family:** 5-gromark  
**Parent:** 0046-gromark-three-term-rules-and-higher-bases  
**Decision:** reverted  
**Run:** 2026-10-15T13:15:18+00:00, 28.8 s, status ran  
**Time by phase:** design 84 s, implement 0 s, test 11 s, run 29 s, record 0 s

## In plain words

Gromark is a cipher whose secret is a short starting number that grows into a long stream of digits, each digit the sum of two earlier ones, plus a scrambled alphabet. Earlier experiments only tried scrambled alphabets built from the puzzle's words. Here the alphabet can be any scramble at all. That sounds hopeless to search, but it is not: the same plain letter must always land on the same carved letter when the digit is the same, which pins the digits down so tightly that every starting number can be checked in a fraction of a second.

## Walkthrough, by hand

1. Take Rogers' rule, each digit the sum of the digits five and four places earlier, mod 10, and the primer 1 2 3 4 5.
2. The stream begins 1 2 3 4 5 3 5 7 9 8 8 2 6 7 6 0 8 3 3 6 8 1 6 9 4 9 7.
3. Places 26 and 27 both carve Q, from known N and O.
4. With the form M[P + d] = c, N (13) plus the 26th digit (9) gives slot 22, and O (14) plus the 27th digit (7) gives slot 21.
5. Two different slots of one alphabet cannot both hold Q, so this primer is dead.
6. Repeat for every primer, rule and form.

## Worked example (generated)

```
Rogers' rule (5 and 4 back), primer 12345
stream 1234535798826760833681694975336286

place  known  carved  digit  slot (M[P+d]=c)
   22      E       F      1     5
   23      A       L      6     6
   26      N       Q      9    22
   27      O       Q      7    21
   31      E       G      6    10
```

## Lineage

Inherits from 0046-gromark-three-term-rules-and-higher-bases. What changed: Experiments 13, 28, 46 and 54 tested the Gromark running-number key only on alphabets built from the puzzle's words. Here the mixed alphabet is left completely free: the 24 known letters must fit some one-to-one alphabet, which the run checks exactly for every starting number and every two-term rule up to six digits back.

## Hypothesis (domain expert)

Family 5, free-alphabet Gromark (the open corner named in families.md after 0028 and 0046). Key digits base 10 from a lagged-Fibonacci rule d[i] = d[i-a] + d[i-b] mod 10, 1 <= a < b <= 6 (15 rules, including Rogers' Gromark a = 4, b = 5), every primer of b digits (5,432,200 primers in all). Four forms, with P, C the standard-alphabet indices and M an unknown mixed alphabet: M[P + d] = c, M[P - d] = c, M[C - d] = p, M[C + d] = p (mod 26). For each primer the 24 cribs give slot-letter pairs that must be a partial bijection: equal slots need equal letters and equal letters need equal slots. Because the digits lie in 0-9, every pair of cribs with the same letter fixes an exact digit difference, so most primers die on the first two such pairs; survivors get the full bijection check. Exhaustive for these rules and forms in base 10. Run on K4 and ten shuffled coppers. Clue entries: C22(a) (the raised YAR / DYAHR as a Gromark primer), C4(b) (Scheidt: 'base', a non-standard number system), C5 ('not mathematical' argues against it, recorded).

## Prediction

No primer under any of the 15 rules and 4 forms gives a consistent alphabet, on K4 or on any of the ten shuffled coppers. Zero candidates pass.

## Method

1. For each rule, generate the digit stream from every primer and keep the digits at the 24 known places.
2. For each form, list pairs of known places with the same letter; each fixes the difference of their two digits.
3. Keep primers that meet every such difference, then check the full one-to-one alphabet condition.
4. Repeat on ten shuffled coppers.

## Result

Candidates returned: 0. Passed all gates: 0. Best crib hits among all candidates: 0/24
(no candidates).
Best loss: None (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: 0034-complete-the-key-at-surviving-periods.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| - | no candidates | | | | |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "Gromark, base 10, free mixed alphabet",
 "rules": [
  [
   1,
   2
  ],
  [
   1,
   3
  ],
  [
   2,
   3
  ],
  [
   1,
   4
  ],
  [
   2,
   4
  ],
  [
   3,
   4
  ],
  [
   1,
   5
  ],
  [
   2,
   5
  ],
  [
   3,
   5
  ],
  [
   4,
   5
  ],
  [
   1,
   6
  ],
  [
   2,
   6
  ],
  [
   3,
   6
  ],
  [
   4,
   6
  ],
  [
   5,
   6
  ]
 ],
 "rules_planned": 15,
 "primers": 5432100,
 "forms": [
  "M[P+d]=c",
  "M[P-d]=c",
  "M[C-d]=p",
  "M[C+d]=p"
 ],
 "k4_consistent": [],
 "k4_count": 0,
 "control_counts": [
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
}
```

Notes: 15 of 15 rules, 5,432,100 primers x 4 forms: K4 consistent primers 0; ten shuffled coppers [0, 0, 0, 0, 0, 0, 0, 0, 0, 0].


