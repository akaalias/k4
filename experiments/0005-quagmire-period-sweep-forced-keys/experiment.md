# 0005-quagmire-period-sweep-forced-keys: Periodic keyed tableau with separate alphabets: which periods survive, and what key they force

**Family:** 1-keyed-periodic  
**Parent:** 0004-running-key-from-k1-k3  
**Decision:** reverted  
**Run:** 2026-10-14T16:17:13+00:00, 0.3 s, status ran

## Lineage

Inherits from 0004-running-key-from-k1-k3. What changed: Periodic key instead of running key; plain, cipher and key alphabets may differ (Quagmire I to IV).

## Hypothesis (domain expert)

K4 is a periodic tableau cipher like K1 and K2 but with a period the cribs allow and possibly different alphabets for plaintext, ciphertext and key (Quagmire I, II, III, IV under the ACA names). kryptos.cribsweep showed that for single-alphabet additive systems only periods 27, 28, 29 and 53 to 97 survive; nobody has published the same sweep for separate alphabets (knowledge/05-attacks.md, open). For each of the 24 conventions and each period 1 to 97 we derive the key letter forced at every crib position and test whether positions congruent modulo the period agree. For each surviving (convention, period) we record the forced key fragment, then score it two ways: does any vocabulary word or K1 to K3 phrase of that length contain the fragment at the forced slots, and if so submit the decryption. Clue register C5(a), C8(a). Bounds: complete for periodic single-key tableau systems under these 24 conventions and all periods.

## Prediction

Periods 1 to 26 and 30 to 52 are excluded under every convention, as in the single-alphabet sweep. Surviving periods force key fragments that match no vocabulary word. Zero candidates pass.

## Method

For convention (pa, ca, ka, m) and period P: forced[slot] = key_letter_for(p, c) for each crib; a conflict at any slot excludes (convention, P). For survivors, build the fragment pattern of length P with forced letters and wildcards, and match it against every word and phrase in data/vocabulary.txt plus the K1 to K3 plaintexts as sliding windows of length P. Each match yields a full key; decrypt and submit.

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
 "family": "periodic tableau, separate alphabets (Quagmire I-IV)",
 "conventions": 24,
 "periods": "1-97",
 "periods_excluded_all_conventions": [
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
  12,
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
 "periods_surviving_some_convention": [
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
  96,
  97
 ],
 "survivor_pairs": 1152,
 "vocab_matches": 0,
 "key_pool": "vocabulary words of length P plus all length-P windows of K1-K3 plaintexts"
}
```

Notes: 0 forced-fragment matches submitted as candidates.


## Walkthrough (standalone)

1. Choose a period, say 28, and a convention: plaintext on the sculpture's alphabet, ciphertext on the standard one, key on the sculpture's, Vigenere. 2. Position 22 is plaintext E, ciphertext F; the key letter that does that is forced. Position 50 would use the same key slot, but 50 is not a crib, so no conflict. 3. Positions 26 and 54: 54 is not a crib either. 4. Positions 64 and 36: neither pair conflicts. 5. Collect the forced letters into a 28-slot pattern with blanks. 6. Slide every word and phrase from the puzzle's vocabulary across the pattern. 7. A fit gives the whole key; decrypt and check the cribs.

## Worked example (generated)

```
forced key letters, period 28, plain kry / cipher std / key kry, Vigenere

pos  plain  cipher  slot(pos-1 mod 28)  forced key letter
 22    E      F        21                 Q
 23    A      L        22                 T
 24    S      R        23                 E
 25    T      V        24                 L
 26    N      Q        25                 W
 64    B      N         7                 O
 65    E      Y         8                 G
 66    R      P         9                 H
```

## ELI5

The first two messages used a repeating secret word and the table on the sculpture. We ask: if the fourth message used the same trick with a longer secret word, how long could that word be? The 24 known letters tell us which lengths are impossible, because two letters that would use the same letter of the secret word must agree. For the lengths that survive, the known letters also tell us some letters of the secret word, so we check whether any word from the puzzle's own world fits those letters.
