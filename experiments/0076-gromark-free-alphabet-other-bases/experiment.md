# 0076-gromark-free-alphabet-other-bases: Gromark with any mixed alphabet, in number bases other than ten

**Family:** 5-gromark  
**Parent:** 0069-gromark-with-a-free-alphabet  
**Decision:** reverted  
**Run:** 2026-10-15T13:30:55+00:00, 123.4 s, status ran  
**Time by phase:** design 37 s, implement 0 s, test 13 s, run 123 s, record 0 s

## In plain words

Experiment 69 showed that a Gromark cipher, whose key is a growing stream of digits plus a scrambled alphabet, cannot have made the copper if the digits run from 0 to 9. Scheidt has talked about other number systems, base 16 and the Maya's base 20, and the Berlin clock counts in fives. So we run the same exact test with digits in every base from 2 to 16 and in base 26, again with any scrambled alphabet at all.

## Walkthrough, by hand

1. Base 2, each digit the sum of the digits five and four back, mod 2, primer 1 0 1 1 0.
2. The stream begins 1 0 1 1 0 1 1 0 1 1 0 1 1 0 1 1 0 1 1 0 1 1 0 1 1 0 1.
3. Places 26 and 27 both carve Q, from known N (13) and O (14).
4. With the form M[P + d] = c: 13 + 0 = 13 and 14 + 1 = 15, two different slots, which cannot both hold Q.
5. This primer is dead.
6. Repeat for every primer, rule, base and form.

## Worked example (generated)

```
base 2, digits 5 and 4 back, primer 10110
stream 1011011011011011011011011011011011

place  known  carved  digit  slot (M[P+d]=c)
   26      N       Q      0    13
   27      O       Q      1    15
   22      E       F      1     5
   23      A       L      0     0
```

## Lineage

Inherits from 0069-gromark-with-a-free-alphabet. What changed: Experiment 69 closed base-10 Gromark for any alphabet. Scheidt mentioned base 16 and Mayan base 20 and 60, and the Berlin clock counts in fives. Here the running digits are in base 2 to 16 (except 10) and base 26, with every two-term rule up to five digits back and every primer, and the alphabet is again left completely free.

## Hypothesis (domain expert)

Family 5, free-alphabet Gromark beyond base 10 (C4(b): Scheidt's remarks on 'base 16' and Mayan bases, 03-scheidt-said.md; C12(b): the Mengenlehreuhr counts in fives and ones, sources/nyt-2010-berlin-clue.txt). Key digits d[i] = d[i-a] + d[i-b] mod B, 1 <= a < b <= 5 (10 rules), every primer of b digits, bases B = 2-9 and 11-16 (and 26 for rules with b <= 4); the digit is added to the letter index mod 26 as in Gromark. Four forms as in 0069 (M[P+d]=c, M[P-d]=c, M[C-d]=p, M[C+d]=p; M an unknown mixed alphabet). Same-letter crib pairs fix the digit difference to one or two values (d_k - d_l = need or need - 26 within -(B-1)..B-1), which filters almost every primer; the rest get the full bijection check. Exhaustive for these bases and rules. K4 and ten shuffled coppers.

## Prediction

No primer under any base, rule and form gives a consistent alphabet on K4; the ten shuffled coppers give none either, except possibly in base 26 where the digit differences are least constrained, and there no more often on K4 than on the shuffles. Zero candidates pass.

## Method

1. For each base and rule, generate the digit stream from every primer and keep the digits at the 24 known places.
2. For each form, list same-letter pairs and the digit differences they allow.
3. Keep primers that meet every pair, then check the full one-to-one condition.
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
 "family": "Gromark, free mixed alphabet, bases 2-9, 11-16 and 26",
 "rules": "two-term, lags up to 5 (base 26: up to 4)",
 "settings_done": 146,
 "settings_planned": 146,
 "primers": 15135782,
 "forms": [
  "M[P+d]=c",
  "M[P-d]=c",
  "M[C-d]=p",
  "M[C+d]=p"
 ],
 "by_base": {
  "2": {
   "k4": 0,
   "controls": [
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
   "primers": 196
  },
  "3": {
   "k4": 0,
   "controls": [
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
   "primers": 1278
  },
  "4": {
   "k4": 0,
   "controls": [
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
   "primers": 5008
  },
  "5": {
   "k4": 0,
   "controls": [
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
   "primers": 14650
  },
  "6": {
   "k4": 0,
   "controls": [
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
   "primers": 35460
  },
  "7": {
   "k4": 0,
   "controls": [
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
   "primers": 75166
  },
  "8": {
   "k4": 0,
   "controls": [
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
   "primers": 144448
  },
  "9": {
   "k4": 0,
   "controls": [
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
   "primers": 257418
  },
  "11": {
   "k4": 0,
   "controls": [
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
   "primers": 690910
  },
  "12": {
   "k4": 0,
   "controls": [
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
   "primers": 1061136
  },
  "13": {
   "k4": 0,
   "controls": [
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
   "primers": 1575418
  },
  "14": {
   "k4": 0,
   "controls": [
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
   "primers": 2272228
  },
  "15": {
   "k4": 0,
   "controls": [
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
   "primers": 3196350
  },
  "16": {
   "k4": 0,
   "controls": [
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
   "primers": 4399360
  },
  "26": {
   "k4": 0,
   "controls": [
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
   "primers": 1406756
  }
 }
}
```

Notes: 146 of 146 base-rule settings, 15,135,782 primers x 4 forms. Consistent primers by base, K4 (controls): base 2: 0 (0-0); base 3: 0 (0-0); base 4: 0 (0-0); base 5: 0 (0-0); base 6: 0 (0-0); base 7: 0 (0-0); base 8: 0 (0-0); base 9: 0 (0-0); base 11: 0 (0-0); base 12: 0 (0-0); base 13: 0 (0-0); base 14: 0 (0-0); base 15: 0 (0-0); base 16: 0 (0-0); base 26: 0 (0-0).


