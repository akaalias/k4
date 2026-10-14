# 0002-ciphertext-autokey-all-lags: Ciphertext autokey is decided by the cribs at every lag and convention

**Family:** 1-keyed-periodic  
**Parent:** none (root)  
**Decision:** reverted  
**Run:** 2026-10-14T16:15:06+00:00, 0.1 s, status ran

## Lineage

Inherits from nothing; this is a root experiment. What changed: New root. Replaces keyword search with a decidable test the cribs settle outright.

## Hypothesis (domain expert)

K4 is a ciphertext-autokey cipher: after a primer of length L, each key letter is the ciphertext letter L positions earlier, so c[i] = f(p[i], c[i-L]). The NSA tested this against the interval-7 property in 2007 without cribs (knowledge/05-attacks.md). With 24 known plaintext letters the test is exact: at every crib position i > L both p[i] and c[i-L] are known, so the convention either reproduces c[i] or it does not. We test all 24 conventions in kryptos.alphabets (plain, cipher and key alphabet each standard or KRYPTOS; Vigenere, Beaufort, variant Beaufort) at every lag 1 to 96. A convention and lag that fits all checkable cribs decrypts positions L+1 to 97 with no key at all. Clue register: C4(d) is not touched; this tests the NSA's own first hypothesis. Bounds: complete for this family under these conventions.

## Prediction

No convention and lag reproduces all checkable cribs; zero candidates pass the crib gate. The family is excluded, not merely unexplored.

## Method

For each convention and each lag L in 1..96: for every crib position i with i > L, compute f(p[i], c[i-L]) and compare with c[i]. Record the number of checks and mismatches. For any (convention, L) with zero mismatches, decrypt positions L+1..97 from the ciphertext, fill positions 1..L with the crib letters where known and A elsewhere, and submit as a candidate with key_bits = 4.7*L for the primer.

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
 "family": "ciphertext autokey",
 "conventions": 24,
 "lags": "1-96",
 "pairs_tested": 2304,
 "survivors": 0,
 "decidability": "exact at every crib position i > lag"
}
```

Notes: A survivor must also reproduce the cribs inside the primer region, which the gate checks.


## Walkthrough (standalone)

1. Write the ciphertext in a row and number it 1 to 97. 2. Pick a distance, say 7. 3. Go to position 64, where the plaintext is B. Look seven back: position 57 is D. 4. Under the sculpture's alphabet KRYPTOSABCDEFGHIJLMNQUVWXZ, B is at 8 and D is at 10; add them, 18, and read the 18th letter, M. 5. The carved letter at 64 is N, not M, so distance 7 under this convention is wrong. 6. Repeat for every crib position, every distance, and every way of indexing the alphabets. One surviving distance would decrypt the rest by itself.

## Worked example (generated)

```
ciphertext autokey, lag 7, all alphabets KRYPTOS, Vigenere
alphabet: KRYPTOSABCDEFGHIJLMNQUVWXZ

pos  plain  key=c[pos-7]  idx(p)+idx(k)  predicted  carved
 64    B      I              8+15        W        N  x
 65    E      A             11+7         M        Y  x
 66    R      W              1+23        X        P  x
 67    L      I             17+15        S        V  x
 68    I      N             15+19        B        T  x
 69    N      F             19+12        O        T  x
```

## ELI5

In an autokey cipher the secret word only covers the first few letters. After that, the scrambled message itself becomes the key: to hide the twentieth letter you use the scrambled letter a fixed distance back. Because we know the scrambled text and we know 24 letters of the real message, we can check every possible distance back. If one works, most of the message falls out with no secret word at all. If none works, this whole kind of cipher is off the table for good.
