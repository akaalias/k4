# 0054-gromark-bases-k1-k3-word-alphabets: Number keys that grow by a rule, on tables rebuilt from the words of the solved messages

**Family:** 5-gromark  
**Parent:** 0028-gromark-small-bases-two-to-nine  
**Decision:** reverted  
**Run:** 2026-10-15T12:13:19+00:00, 1.1 s, status ran  
**Time by phase:** design 0 s, implement 11 s, test 0 s, run 1 s, record 0 s

## In plain words

In a Gromark cipher the secret is a short string of digits that grows by itself: each new digit is the sum of two earlier ones, keeping only the last digit. Each known letter tells us how far the table had to shift it, and with ordinary digits no shift can be bigger than 9. So the biggest shift the known letters demand says how large the number system must be. We work that out for tables rebuilt from every word of the solved messages, and check scrambled copies of the copper the same way.

## Walkthrough, by hand

1. Take SHADING for the message alphabet and INVISIBLE for the carved one.
2. Place 22: E is 9, carved F is 10, a shift of 1.
3. Place 23: A is 2, carved L is 5, a shift of 3.
4. Place 24: S is 0, carved R is 19, a shift of 19.
5. A shift of 19 cannot be a single digit, so this pair of tables needs a number base of at least 20 and an ordinary Gromark is out.
6. Do the same for every pair and every way of using the table, and keep the smallest such base.

## Worked example (generated)

```
plain  SHADINGBCEFJKLMOPQRTUVWXYZ
cipher INVSBLEACDFGHJKMOPQRTUWXYZ

place  plain  carved  shift (Vigenere)
   22    E      F       1
   23    A      L       3
   24    S      R      19
   25    T      V       9
   26    N      Q      13
```

## Lineage

Inherits from 0028-gromark-small-bases-two-to-nine. What changed: Experiments 13, 28 and 46 tested Gromark keys, a string of digits that grows by adding earlier digits, on tables rebuilt from the puzzle's vocabulary. Here the tables come from every word of the solved messages and Sanborn's 2025 letter, and the test asks first how small a number base the 24 known letters allow, then whether any growth rule fits.

## Hypothesis (domain expert)

Gromark and its generalisations: the key is a digit stream in base B with k[i] = k[i-a] + k[i-b] mod B (a > b >= 1, a up to 13), applied as an additive shift through a plain and a cipher alphabet (C22(a) reads the raised YAR as such a primer). Every forced shift must be a digit below B, so the largest of the 24 forced shifts bounds B from below for each plain-cipher pair and mode. Pool: the 102 alphabets of 0053 (K1-K3 plaintext words and the C13/C14 words, plus standard and KRYPTOS), three modes. Report the smallest admissible base over all 10,404 pairs, against ten shuffled coppers; for every pair admissible at B <= 15, test every rule (a, b) on all crib triples where positions i, i-a and i-b are all known. Bounds: exact for these alphabets.

## Prediction

No pair admits base 10: the smallest admissible base is about 18 to 20 on K4, as on the shuffles. No pair admits a base of 15 or less, so no growth rule needs testing. Zero candidates.

## Method

1. Build the alphabet pool as in experiment 53.
2. For each plain and cipher alphabet and mode, compute the 24 forced shifts and their maximum.
3. Record the smallest maximum, the smallest admissible base.
4. Repeat on ten shuffles.
5. For pairs admissible at 15 or less, test every two-term rule on the crib triples.

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
 "family": "Gromark-type digit keys, k[i] = k[i-a] + k[i-b] mod B, on K1-K3-word and C13/C14-word alphabets",
 "alphabets": 102,
 "pairs": 10404,
 "modes": 3,
 "smallest_admissible_base_k4": 17,
 "smallest_admissible_base_controls": [
  19,
  17,
  17,
  18,
  18,
  18,
  19,
  18,
  19,
  19
 ],
 "pairs_admissible_at_15_or_less": 0,
 "rules_consistent": 0
}
```

Notes: Smallest base any pair admits on K4: 17; on ten shuffles: [17, 17, 18, 18, 18, 18, 19, 19, 19, 19]. Pairs admissible at base 15 or less: 0; consistent rules among them: 0.


