# 0107-three-term-gromark-with-a-free-alphabet: Gromark with a three-term digit rule and any mixed alphabet at all

**Family:** 5-gromark-lfsr  
**Parent:** 0069-gromark-with-a-free-alphabet  
**Decision:** reverted  
**Run:** 2026-10-15T20:18:50+00:00, 50.2 s, status ran  
**Time by phase:** unattributed 95 s, run 50 s, record 0 s

## In plain words

Gromark makes a long stream of key digits from a short starting number, each new digit the sum of earlier ones, and uses a scrambled alphabet. Experiment 69 tried every rule that adds two earlier digits, with any scrambled alphabet, and found nothing. Here each digit is the sum of three earlier ones, every such rule and every starting number up to six digits, again with any scrambled alphabet.

## Walkthrough, by hand

1. Take the rule: each digit the sum of the digits 1, 3 and 5 places earlier, mod 10, and the primer 1 2 3 4 5.
2. Extend the stream to place 74.
3. Places 26 and 27 both carve Q, from known N and O.
4. With the form M[P + d] = c, N plus the 26th digit and O plus the 27th digit must be the same slot of the alphabet, since both hold Q.
5. If not, the primer is dead; repeat for every primer, rule and form.

## Worked example (generated)

```
rule: each digit the sum of the digits 1, 3 and 5 places earlier, mod 10; primer 1 2 3 4 5
stream: 1 2 3 4 5 9 5 3 6 6 8 9 8 2 7 3 4 9 4 5 7 5 9 0 0 6 1 0 6 7 3 0 7 6

places 26 and 27 both carve Q, from known N and O; form M[P + d] = c:
  N (13) + digit 6 = slot 19;  O (14) + digit 1 = slot 15
  two different slots of one alphabet cannot both hold Q
```

## Lineage

Inherits from 0069-gromark-with-a-free-alphabet. What changed: 0069 closed two-term Gromark rules on a free alphabet; 0046 tried three-term rules only on alphabets built from the puzzle's words. Here the digit rule is d[i] = d[i-a] + d[i-b] + d[i-c] mod 10 for every 1 <= a < b < c <= 6 (20 rules) and every primer of c digits, with the mixed alphabet left free, tested by 0069's exact digit-difference method.

## Hypothesis (domain expert)

Family 5's open corner: 'three-term rules with a free alphabet' (families.md). Key digits base 10 from d[i] = d[i-a] + d[i-b] + d[i-c] mod 10, 1 <= a < b < c <= 6, every primer of c digits (10,631,000 primers in all). Four forms as in 0069 (M an unknown mixed alphabet, P and C standard indices): M[P + d] = c, M[P - d] = c, M[C - d] = p, M[C + d] = p. Pairs of known places with the same letter fix exact digit differences (digits are 0-9), then the full partial-bijection check. Exhaustive in base 10 for these rules. C22(a), C4(b). A planted text is recovered. Ten shuffled coppers.

## Prediction

No primer under any of the 20 rules and 4 forms is consistent, on K4 or on any shuffled copper. Zero candidates.

## Method

1. For each rule, generate the digit stream from every primer and keep the digits at the 24 known places.
2. For each form, pairs of known places with the same letter fix digit differences; keep primers meeting them.
3. Check the full one-to-one alphabet condition.
4. Repeat on ten shuffled coppers.

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
 "family": "three-term Gromark, base 10, free mixed alphabet",
 "rules": [
  [
   1,
   2,
   3
  ],
  [
   1,
   2,
   4
  ],
  [
   1,
   3,
   4
  ],
  [
   2,
   3,
   4
  ],
  [
   1,
   2,
   5
  ],
  [
   1,
   3,
   5
  ],
  [
   2,
   3,
   5
  ],
  [
   1,
   4,
   5
  ],
  [
   2,
   4,
   5
  ],
  [
   3,
   4,
   5
  ],
  [
   1,
   2,
   6
  ],
  [
   1,
   3,
   6
  ],
  [
   2,
   3,
   6
  ],
  [
   1,
   4,
   6
  ],
  [
   2,
   4,
   6
  ],
  [
   3,
   4,
   6
  ],
  [
   1,
   5,
   6
  ],
  [
   2,
   5,
   6
  ],
  [
   3,
   5,
   6
  ],
  [
   4,
   5,
   6
  ]
 ],
 "rules_planned": 20,
 "primers": 10631000,
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

Notes: 20 of 20 rules, 10,631,000 primers x 4 forms: K4 consistent primers 0; ten shuffled coppers [0, 0, 0, 0, 0, 0, 0, 0, 0, 0].


