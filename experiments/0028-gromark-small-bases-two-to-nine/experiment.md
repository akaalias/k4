# 0028-gromark-small-bases-two-to-nine: Gromark in bases 2 to 9: the even bases that reproduce the width-21 repeats

**Family:** 5-gromark-lfsr  
**Parent:** 0013-gromark-recurrence-on-crib-shifts  
**Decision:** reverted  
**Run:** 2026-10-15T07:36:05+00:00, 0.9 s, status ran  
**Time by phase:** design 0 s, implement 0 s, test 6 s, run 1 s, record 0 s

## In plain words

Yesterday's workshop found one kind of fake that shares a real oddity of K4: a Gromark cipher whose growing number stream uses only the digits 0 and 1. Such streams repeat their rhythm every 21 letters, which is just what K4 shows. A Gromark in base 2 pushes each letter along by 0 or 1 only; in base 8, by 0 to 7. We already know the 24 pushes that the known letters demand under each alphabet, so we simply check whether any alphabet keeps all 24 pushes small enough, and then whether they follow the adding rule.

## Walkthrough, by hand

1. Take the standard alphabet for the plaintext and the KRYPTOS alphabet for the ciphertext, Vigenere.
2. Position 22: plaintext E is index 4 in the standard alphabet; ciphertext F is index 11 in KRYPTOS; the shift is 11 - 4 = 7.
3. Position 23: A is 0, L is 18; shift 18.
4. Continue to position 34 for 13 shifts in a row.
5. Try the Gromark rule, a = 5, b = 4: the sixth shift must equal the first plus the second, mod 10, and all shifts must be digits. The shift 18 already fails base 10.
6. In base 26, check the sixth against the first plus the second mod 26, the seventh against the second plus the third, and so on: eight checks.
7. One failure kills the rule under this alphabet pair; try the next pair.

## Worked example (generated)

```
plain alphabet standard, cipher alphabet KRYPTOS, Vigenere: forced shifts at 22-34

pos  plain  cipher  shift
 22    E      F       8
 23    A      L      17
 24    S      R       9
 25    T      V       3
 26    N      Q       7
 27    O      Q       6
 28    R      P      12
 29    T      R       8
 30    H      N      12
 31    E      G       9
 32    A      K       0
 33    S      S      14
 34    T      S      13

shifts: 8 17 9 3 7 6 12 8 12 9 0 14 13
largest shift 17: base 8 needs all below 8, so this alphabet pair is out at once
```

## Lineage

Inherits from 0013-gromark-recurrence-on-crib-shifts. What changed: Bases 2 to 9 instead of 10 and 26. 0027 showed Gromark base 2 is the only simulated construction that reproduces K4's width-21 repeats, and Bean found base-8 primers that fit the cribs. Every forced shift must now be below the base, a filter of (base/26) to the 24th power per alphabet triple.

## Hypothesis (domain expert)

Rogot, Deavours and Blackman: a Gromark key in an even base with a five-digit primer has an underlying period-21 structure, and Bean found base-8 primers that fit the cribs with period 84 (knowledge/04-structure.md, 05-attacks.md). 0027 confirmed that base 2 reproduces the width-21 repeats (p 0.34) where nothing else does. 0013 tested bases 10 and 26 only. Here the bases are 2 to 9, every lag pair 1 <= b < a <= 12, under the same 248-alphabet pool for plain and cipher and three modes. In base B every one of the 24 forced shifts must be below B, which alone has chance (B/26)^24 per triple, from 10^-27 at base 2 to 10^-11 at base 9; a triple passing that and six recurrence checks would be decisive. For each survivor the recurrence runs from the 22-34 window to a full key stream, the text is decrypted and submitted. Bounds: complete for these bases, rules and alphabets; Bean's free annealed alphabets remain his.

## Prediction

No alphabet triple keeps all 24 forced shifts below 9, let alone below 2, so no base from 2 to 9 reaches the recurrence test. Zero candidates pass.

## Method

1. Build the alphabet pool.
2. For each plain alphabet, cipher alphabet and mode, compute the forced shift at each of the 24 crib positions and record the largest.
3. For each base B from 2 to 9, keep triples whose largest shift is below B.
4. For those, check every lag pair's recurrence on both crib runs.
5. Extend survivors to a full stream, decrypt and submit.

## Result

Candidates returned: 0. Passed all gates: 0. Best crib hits among all candidates: 0/24
(no candidates).
Best loss: None (0 is solved; 10 per missed crib letter). Best fitness: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| - | no candidates | | | | |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "running numerical key, k[i] = k[i-a] + k[i-b] mod base",
 "rules": "66 lag pairs, 1 <= b < a <= 12",
 "bases": [
  2,
  3,
  4,
  5,
  6,
  7,
  8,
  9
 ],
 "smallest_largest_shift_over_all_triples": 15,
 "alphabets": 248,
 "alphabet_triples": 184512,
 "modes": 3,
 "triples_with_all_shifts_below_9": 0,
 "min_checks": 6,
 "survivors": [],
 "n_survivors": 0,
 "n_survivors_consistent_with_second_run": 0
}
```

Notes: 184512 alphabet triples; smallest largest-shift over all triples 15; bases 2-9 x 66 rules. 0 survivors with >= 6 checks; 0 full-stream candidates submitted.


