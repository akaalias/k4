# 0004-running-key-from-k1-k3: A running key drawn from K1, K2 or K3 at every offset

**Family:** 1-keyed-periodic  
**Parent:** 0003-plaintext-autokey-all-lags  
**Decision:** reverted  
**Run:** 2026-10-14T16:16:30+00:00, 0.8 s, status ran

## Lineage

Inherits from 0003-plaintext-autokey-all-lags. What changed: The key is a stretch of the solved sections or their ciphertext, not the message itself.

## Hypothesis (domain expert)

K4 uses a running key: a 97-letter stretch of text the solver already has, applied through the tableau. Sanborn said he left 'instructions in the earlier text that refer to later text' and that K4 'will come back to the first part' (clue register C7). Gillogly guessed running key in 1999; Schridde tried the K1 to K3 plaintexts under two conventions. We make it exhaustive: key sources are the K1, K2 (as carved and corrected) and K3 plaintexts, the three ciphertexts, and the concatenations of each set, read forward and backward, at every offset including wrap-around, under all 24 conventions. Every crib position is checkable, so each (source, direction, offset, convention) is excluded or survives. Bounds: complete for these sources. Not covered: the tableau text, the Morse, external books.

## Prediction

No source, direction, offset or convention reproduces all 24 cribs. The best alignment matches fewer than 8 of 24, which is chance for this many trials.

## Method

Build key texts: K1, K2 carved, K2 corrected, K3 plaintexts (letters only); K1, K2, K3 ciphertexts (letters only); K1+K2+K3 plaintext and ciphertext concatenations. For each, both directions. For offset o in 0..len-1 with cyclic wrap, key[i] = text[(o+i) mod len]. For each convention compare encrypt(p[pos], key[pos]) with c[pos] at all 24 cribs. Survivors are submitted as candidates by decrypting all 97 letters; key_bits is log2(trials).

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
 "family": "running key from K1-K3",
 "sources": [
  "K123ct_fwd",
  "K123ct_rev",
  "K123pt_fwd",
  "K123pt_rev",
  "K1ct_fwd",
  "K1ct_rev",
  "K1pt_fwd",
  "K1pt_rev",
  "K2ct_fwd",
  "K2ct_rev",
  "K2pt_corr_fwd",
  "K2pt_corr_rev",
  "K2pt_fwd",
  "K2pt_rev",
  "K3ct_fwd",
  "K3ct_rev",
  "K3pt_fwd",
  "K3pt_rev"
 ],
 "conventions": 24,
 "offsets": "all, cyclic",
 "trials": 165216,
 "survivors": 0,
 "best_mismatches_of_24": 16,
 "best_alignment": [
  "K1ct_fwd",
  [
   "std",
   "std",
   "kry",
   "varbeau"
  ],
  48
 ]
}
```

Notes: Every trial is decided at all 24 crib positions.


## Walkthrough (standalone)

1. Write K1's plaintext, BETWEENSUBTLE..., under the K4 ciphertext starting at some offset. 2. At position 64 the plaintext must be B. Suppose the key letter above it is T. 3. Under the sculpture's alphabet, B is 8 and T is 4; add, 12, read F. 4. The carved letter is N, so this offset fails. 5. Slide one letter and repeat, for every text, direction and alphabet convention. 6. An offset that passes all 24 checks decrypts the rest at once.

## Worked example (generated)

```
running key = K1 plaintext at offset 0, all alphabets KRYPTOS, Vigenere
alphabet: KRYPTOSABCDEFGHIJLMNQUVWXZ

pos  plain  key          idx(p)+idx(k)  predicted  carved
 64    B      B            8+8         J        N  x
 65    E      E           11+11        V        Y  x
 66    R      T            1+4         O        P  x
 67    L      W           17+23        H        V  x
 68    I      E           15+11        K        T  x
 69    N      E           19+11        T        T  ok
```

## ELI5

Instead of a short secret word, the key might be a long piece of text the solver already knows, such as the first three messages on the sculpture. We slide each of those texts along the fourth message in every possible position, forwards and backwards, and check whether any position explains all 24 known letters. If none does, those texts are not the key, full stop.
