# 0046-gromark-three-term-rules-and-higher-bases: Gromark with three-term rules and the bases 16 to 26 that experiment 28 left alive

**Family:** 5-gromark-lfsr  
**Parent:** 0028-gromark-small-bases-two-to-nine  
**Decision:** reverted  
**Run:** 2026-10-15T09:47:27+00:00, 36.8 s, status ran  
**Time by phase:** design 10 s, implement 52 s, test 41 s, run 37 s, record 0 s

## In plain words

Gromark grows a long number stream from a short seed by adding earlier digits. Earlier we tried adding two earlier digits; now we also try adding three, with any spacing up to thirteen back, and we count in every base from 16 to 26, the only ones the known letters still allow. The 13 pushes in a row that EASTNORTHEAST pins down must follow the rule, or the rule is out.

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
three-term rule lags 5, 3, 1 in base 26: shift 6 should equal shifts 1 + 3 + 5 = 24, it is 6
```

## Lineage

Inherits from 0028-gromark-small-bases-two-to-nine. What changed: Rules with three terms, k[i] = k[i-a] + k[i-b] + k[i-c], alongside the two-term rules, lags up to 13; bases 16 to 26 only, since experiment 28 showed every alphabet triple forces a shift of 15 or more, which kills every smaller base before any rule is checked.

## Hypothesis (domain expert)

Experiments 13 and 28 killed two-term lagged-Fibonacci rules up to lag 12 in bases 10 and 26, and every base up to 15 outright, under the 248-alphabet pool. Bean (knowledge/05-attacks.md) names other expansion rules as untested. Here: two-term rules with lags up to 13 and three-term rules k[i] = k[i-a] + k[i-b] + k[i-c] with c < b < a <= 13, bases 16 to 26, under the same pool and three modes. For each triple the largest forced shift fixes the admissible bases; each rule is checked on the 13 and 11 consecutive forced shifts, at least six checks required, chance below 26 to the minus six per check set. Survivors extend to a full stream, decrypt and submit. Bounds: complete for these rules and bases over the pool; free alphabets remain Bean's.

## Prediction

No rule with six or more checks survives under any alphabet triple and base; zero candidates pass.

## Method

1. Build the alphabet pool: standard, KRYPTOS and the four mixings of each vocabulary word.
2. For each plain alphabet, cipher alphabet and mode, compute the forced shift at each of the 24 crib positions.
3. For base 10, drop any triple with a shift above 9.
4. For each lag pair (a, b) check k[i] = k[i-a] + k[i-b] mod B on both crib runs; keep triples with every check passing and at least six checks.
5. For each survivor, extend the stream over all 97 positions from the 22-34 window, confirm it reproduces 64-74, decrypt and submit.

## Result

Candidates returned: 0. Passed all gates: 0. Best crib hits among all candidates: 0/24
(no candidates).
Best loss: None (0 is solved; 10 per missed crib letter). Best fitness: None. Champion before this run: 0034-complete-the-key-at-surviving-periods.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| - | no candidates | | | | |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "running numerical key, k[i] = k[i-a] + k[i-b] mod base",
 "rules": "364 two- and three-term rules with lags up to 13",
 "bases": "16-26 as each triple allows",
 "alphabets": 248,
 "alphabet_triples": 184512,
 "modes": 3,
 "triples_with_all_shifts_below_16": 1,
 "min_checks": 6,
 "survivors": [],
 "n_survivors": 0,
 "n_survivors_consistent_with_second_run": 0
}
```

Notes: 184512 alphabet triples x 364 rules, bases 16-26. 0 survivors with >= 6 checks; 0 full-stream candidates submitted.


