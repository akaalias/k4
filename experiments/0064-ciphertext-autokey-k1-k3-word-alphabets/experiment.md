# 0064-ciphertext-autokey-k1-k3-word-alphabets: The scrambled text as its own key, on tables rebuilt from the solved messages' words

**Family:** 1-keyed-periodic  
**Parent:** 0025-autokeys-with-mixed-alphabets  
**Decision:** reverted  
**Run:** 2026-10-15T12:33:15+00:00, 90.5 s, status ran  
**Time by phase:** design 0 s, implement 8 s, test 0 s, run 90 s, record 0 s

## In plain words

In this cipher each letter is hidden using the hidden letter some fixed distance earlier, so once it starts it needs no secret word at all. Each of the 24 known letters then tells us exactly which carved letter must sit that distance before it. We check every distance from 1 to 95 on tables rebuilt from every word of the solved messages, and count how close any of them comes, compared with scrambled copies of the copper.

## Walkthrough, by hand

1. Take SHADING for the message alphabet, INVISIBLE for the carved alphabet and KRYPTOS for the key alphabet, with Vigenere.
2. Place 22 holds E (9 in SHADING) under carved F (10 in INVISIBLE), so the key letter there is the one at index 1 of KRYPTOS: R.
3. At distance 21 the key letter is the carved letter at place 1, which is O, not R, so place 22 fails at lag 21.
4. At distance 10 the key letter would be the carved letter at place 12, L, which also fails.
5. Count the failures over all known places past the starter, for every distance and table.

## Worked example (generated)

```
place  plain  carved  key letter needed (KRYPTOS)  carved 21 back
   22    E      F               R                    O
   23    A      L               P                    B
   24    S      R               N                    K
   25    T      V               C                    R
```

## Lineage

Inherits from 0025-autokeys-with-mixed-alphabets. What changed: Experiment 25 tested the cipher that feeds on its own output on tables rebuilt from the puzzle's vocabulary. Experiment 62 then showed this recipe is the one that makes the copper's width-21 mark. Here the tables come from every word of the solved messages and Sanborn's 2025 letter, at every distance, with scrambled coppers as the control.

## Hypothesis (domain expert)

Ciphertext autokey, key letter = carved letter L back read in the key alphabet, lags 1-95, plain and cipher alphabets from the 102-alphabet pool of 0053 (K1-K3 plaintext words, C13/C14 words, standard, KRYPTOS), key alphabet standard, KRYPTOS, the plain alphabet or the cipher alphabet, three modes. Each crib at place i > L requires a specific key letter, hence a specific carved letter at i - L; the count of satisfied cribs per lag is exact and needs no primer. Motivation: 0062 found ciphertext autokey at lag 21 the only generator that raises the width-21 repeats (0056). Report the fewest mismatches over all settings against ten shuffled coppers. Bounds: complete for this pool.

## Prediction

No setting satisfies every crib past the starter; the fewest mismatches is about the same on K4 as on the shuffles (several). Zero candidates.

## Method

1. Build the alphabet pool.
2. For each plain, cipher and key alphabet and mode, find the carved letter each crib requires L places back.
3. For each lag, count satisfied and violated cribs using the positions of each letter on the copper.
4. Keep the fewest violations.
5. Repeat on ten shuffles.

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
 "family": "ciphertext autokey on K1-K3-word and C13/C14-word alphabets",
 "alphabets": 102,
 "key_alphabets": "standard, KRYPTOS, plain, cipher",
 "modes": 3,
 "lags": "1-95 (at least 6 cribs past the primer)",
 "fewest_mismatches": 3,
 "best_setting": {
  "plain": "kry",
  "cipher": "LOWER/keyword",
  "key": "cipher",
  "mode": "vig",
  "lag": 68,
  "cribs_checked": 6
 },
 "full_matches": 0,
 "control_fewest_mismatches": [
  2,
  2,
  2,
  3,
  2,
  2,
  2,
  2,
  3,
  2
 ]
}
```

Notes: Fewest mismatches over all settings: 3 (('kry', 'LOWER/keyword', 'cipher', 'vig', 68, 6)); ten shuffled coppers: [2, 2, 2, 2, 2, 2, 2, 2, 3, 3]. Full matches: 0.


