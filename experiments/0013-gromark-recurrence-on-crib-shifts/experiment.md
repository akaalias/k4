# 0013-gromark-recurrence-on-crib-shifts: Gromark and its cousins: must the 13 known shifts in a row obey a lagged-Fibonacci rule?

**Family:** 5-gromark-lfsr  
**Parent:** none (root)  
**Decision:** reverted  
**Run:** 2026-10-14T17:01:52+00:00, 2.1 s, status ran  
**Time by phase:** design 19 s, implement 60 s, test 8 s, run 2 s, record 0 s

## In plain words

Gromark is a cipher where the secret is a short number, say five digits, that grows into a long stream of digits by adding pairs of earlier digits, like a Fibonacci sequence. Each letter of the message is pushed along the alphabet by the next digit. The 13 known letters of EASTNORTHEAST tell us 13 pushes in a row, and in a Fibonacci-style stream each push must equal the sum of two earlier ones. We test every pair of positions the rule might add, in base 10 and in base 26, and with every alphabet the puzzle's words can build. A rule that fits the known pushes would be found out at once.

## Walkthrough, by hand

1. Take the standard alphabet for the plaintext and the KRYPTOS alphabet for the ciphertext, Vigenere.
2. Position 22: plaintext E is index 4 in the standard alphabet; ciphertext F is index 11 in KRYPTOS; the shift is 11 - 4 =
7. 
3. Position 23: A is 0, L is 18; shift
18. 
4. Continue to position 34 for 13 shifts in a row.
5. Try the Gromark rule, a = 5, b = 4: the sixth shift must equal the first plus the second, mod 10, and all shifts must be digits. The shift 18 already fails base
10. 
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
Gromark rule a=5 b=4 base 10: all digits? False; base 26 check at i=5: 6 vs 25
```

## Lineage

Inherits from nothing; this is a root experiment. What changed: New root in family 5. The key is a running number stream from a short primer, as in the ACA Gromark; the cribs give 13 consecutive key values, which a recurrence must reproduce.

## Hypothesis (domain expert)

Gromark (Gillogly 1999, 2004; Bean, HistoCrypt 2021, knowledge/05-attacks.md): a primer of a digits expands by k[i] = k[i-a] + k[i-b] mod B, and each plaintext letter shifts by k[i] between a plain and a cipher alphabet. Bean exhausted base 10 with a = 5, b = 4 under free annealed alphabets. Here the rule is the variable: every lag pair 1 <= b < a <= 12 and bases 10 and 26, under plain and cipher alphabets drawn from the standard, KRYPTOS and the four Friedman mixings of every vocabulary word, with the three tableau modes. Positions 22-34 force 13 consecutive shifts and 64-74 force 11; the recurrence is checked on both runs, giving 24 - 2a checks per rule. In base 10 every forced shift must also be a digit. A survivor with at least six passing checks has chance probability below 26 to the minus six per trial; with about 700,000 trials per rule, chance survivors should be rare. For each survivor the recurrence runs backward and forward from the 22-34 window to a full key stream, the text is decrypted and submitted. Bounds: complete for the stated rules, bases and alphabet pools; free alphabets outside the vocabulary remain Bean's.

## Prediction

In base 10 almost no alphabet pair makes all 24 forced shifts digits, and none of those also satisfies a recurrence. In base 26, a handful of (rule, alphabet) survivors appear at the long lags where only a few checks apply, none with six or more checks. No decrypted candidate is English; zero pass.

## Method

1. Build the alphabet pool: standard, KRYPTOS and the four mixings of each vocabulary word.
2. For each plain alphabet, cipher alphabet and mode, compute the forced shift at each of the 24 crib positions.
3. For base 10, drop any triple with a shift above
9. 
4. For each lag pair (a, b) check k[i] = k[i-a] + k[i-b] mod B on both crib runs; keep triples with every check passing and at least six checks.
5. For each survivor, extend the stream over all 97 positions from the 22-34 window, confirm it reproduces 64-74, decrypt and submit.

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
  10,
  26
 ],
 "alphabets": 248,
 "alphabet_triples": 184512,
 "modes": 3,
 "base10_all_digit_triples": 0,
 "min_checks": 6,
 "survivors": [],
 "n_survivors": 0,
 "n_survivors_consistent_with_second_run": 0
}
```

Notes: 184512 alphabet triples x 66 rules x 2 bases. 0 survivors with >= 6 checks; 0 full-stream candidates submitted.


