# 0003-plaintext-autokey-all-lags: Plaintext autokey, decided where two known letters line up

**Family:** 1-keyed-periodic  
**Parent:** 0002-ciphertext-autokey-all-lags  
**Decision:** reverted  
**Run:** 2026-10-14T16:15:46+00:00, 0.1 s, status ran  
**Time by phase:** run 0 s

## In plain words

This is the other autokey: the real message, not the scrambled one, becomes its own key after a short start. We can only test it where two of the 24 known letters sit the right distance apart, so some distances get a clear no and some get no answer at all. The point is to know exactly which distances are still alive, so no one wastes time on the dead ones.

## Walkthrough, by hand

1. Number the ciphertext 1 to 97 and mark the 24 known plaintext letters.
2. Pick a distance, say
3. 3. Position 25 is T and position 22, three back, is E.
4. Under the sculpture's alphabet, T is at 4 and E at 11; add them, 15, and read the letter there, I.
5. The carved letter at 25 is V, so distance 3 fails under this convention.
6. For a distance like 20 there is no pair of known letters that far apart, so the test says nothing; that distance stays open.

## Worked example (generated)

```
plaintext autokey, lag 3, all alphabets KRYPTOS, Vigenere
alphabet: KRYPTOSABCDEFGHIJLMNQUVWXZ

pos  plain  key=p[pos-3]  idx(p)+idx(k)  predicted  carved
 25    T      E             4+11        I        V  x
 26    N      A            19+7         K        Q  x
 27    O      S             5+6         E        Q  x
 28    R      T             1+4         O        P  x
 29    T      N             4+19        W        R  x
 30    H      O            14+5         N        N  ok
```

## Lineage

Inherits from 0002-ciphertext-autokey-all-lags. What changed: The key letter is now the plaintext letter L back, not the ciphertext letter.

## Hypothesis (domain expert)

K4 is a plaintext-autokey cipher: c[i] = f(p[i], p[i-L]) after a primer of length L. This is the NSA's 1992 first guess for the interval-7 property (knowledge/04-structure.md). The cribs decide it only where both p[i] and p[i-L] are known: within EASTNORTHEAST (lags 1 to 12), within BERLINCLOCK (lags 1 to 10), and between the two runs (lags 30 to 52). We test all 24 conventions at every lag 1 to 96, count the checkable pairs, and record three outcomes per lag: excluded (a mismatch), consistent (all checks pass, at least one check), or undecided (no overlapping pair). For consistent lags we cannot decrypt without the primer, so we report them as open and bound the primer space. Clue register C11a.

## Prediction

Lags 1 to 12 and 30 to 52 are excluded under every convention. Lags 13 to 29 and 53 to 96 stay undecided. No candidates pass the crib gate.

## Method

For each convention and lag L: over crib positions i with i-L also a crib position, compare f(p[i], p[i-L]) with c[i]. Tally excluded, consistent, undecided per lag across conventions. No candidates are generated because the primer is unknown; the bounds are the deliverable.

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
 "family": "plaintext autokey",
 "conventions": 24,
 "lags": "1-96",
 "lags_excluded_all_conventions": [
  1,
  2,
  3,
  4,
  5,
  6,
  7,
  8,
  9,
  10,
  11,
  30,
  31,
  32,
  33,
  34,
  35,
  36,
  37,
  38,
  39,
  40,
  41,
  42,
  43,
  44,
  45,
  46,
  47,
  48,
  49,
  50,
  51,
  52
 ],
 "lags_consistent_some_conventions": {
  "12": 1
 },
 "lags_undecided_no_overlapping_cribs": [
  13,
  14,
  15,
  16,
  17,
  18,
  19,
  20,
  21,
  22,
  23,
  24,
  25,
  26,
  27,
  28,
  29,
  53,
  54,
  55,
  56,
  57,
  58,
  59,
  60,
  61,
  62,
  63,
  64,
  65,
  66,
  67,
  68,
  69,
  70,
  71,
  72,
  73,
  74,
  75,
  76,
  77,
  78,
  79,
  80,
  81,
  82,
  83,
  84,
  85,
  86,
  87,
  88,
  89,
  90,
  91,
  92,
  93,
  94,
  95,
  96
 ]
}
```

Notes: No candidate can be built without the primer; this experiment exists for its bounds.


