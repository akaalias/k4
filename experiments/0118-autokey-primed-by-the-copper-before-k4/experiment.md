# 0118-autokey-primed-by-the-copper-before-k4: Ciphertext autokey that runs on from K3: the key is the carved letter some distance back, K3's letters included

**Family:** 1-keyed-periodic  
**Parent:** 0002-ciphertext-autokey  
**Decision:** reverted  
**Run:** 2026-10-15T21:17:45+00:00, 0.5 s, status ran  
**Time by phase:** unattributed 7 s, run 0 s, record 0 s

## In plain words

In a self-feeding key, each letter is locked with a letter that was already carved some distance before. Experiment 2 tried this starting fresh at K4. But on the sculpture K4 just continues the lines of K3, so the first letters of K4 could take their key from K3's letters. We try every distance, and also the letter carved straight above on the line before, against all 24 known letters.

## Walkthrough, by hand

1. Write out the copper as carved: K1, K2, K3, the ?, then K4.
2. Choose a distance, say 31, one carved line.
3. Place 22 of K4 (F) takes its key from the carved letter 31 places earlier, which is in K3's last line.
4. On the sculpture's alphabet with Vigenere, F minus that key letter must give E; count a hit if it does.
5. Repeat for all 24 known places, every distance 1-200, every rule, and with the letter straight above on the plate.

## Worked example (generated)

```
the carved stream before K4 has 772 characters; lag 31 (one carved line), sculpture's alphabet, Vigenere

place  known  carved  key letter (31 back)  carved - key  hit
   22      E       F                     T             B  no
   23      A       L                     T             G  no
   24      S       R                     R             K  no
   25      T       V                     T             M  no
   26      N       Q                     V             X  no
   64      B       N                     S             G  no
```

## Lineage

Inherits from 0002-ciphertext-autokey. What changed: 0002 tested ciphertext autokey with the first key letters free, so known places within one lag of the start gave no check. On the copper K4 is not a separate text: it runs on from K3 on the same plate. Here the key for place i is the carved letter lag places earlier in the whole carved stream (K1, K2, K3 and the ? as carved), so every known place is a check, for every lag 1-200; and the geometric version, the letter carved directly above on the previous plate line, and two lines above.

## Hypothesis (domain expert)

C7 ('it will come back to the first part'; earlier text holds instructions), C3(a) (the carved plate as the grid), C11a (NSA 1992: autokey). Model: c_i = E(p_i, x_{i-lag}) where x is the carved stream K1+K2+K3+?+K4 as on the copper (with or without the ? characters, which can carry no key value and are skipped in one variant), lag 1-200; 12 conventions (Vigenere, Beaufort, variant; plain and cipher alphabets standard or KRYPTOS; key letters on the cipher alphabet). Geometric variant: the key for a K4 letter is the letter in the same column of the line above (or two above) on the lower-left plate, columns counted from the left and from the right. Every known place gives a check: 24 per setting. Ten shuffled coppers (K4 shuffled, the earlier text fixed).

## Prediction

No lag or geometric reading matches more than 6 of 24 known letters; same as the coppers. Zero candidates.

## Method

1. Build the carved stream before K4 from the plates.
2. For each lag, rule and stream variant, decrypt the 24 known places with the stream letter lag places back and count matches.
3. Do the same for the letter above on the plate.
4. Repeat on ten shuffled coppers.
5. Decrypt any full match.

## Result

Candidates returned: 0. Passed all gates: 0. Best crib hits among all candidates: 0/24
(no candidates).
Best loss: None (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| - | no candidates | | | | |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "ciphertext autokey continuing the carved stream from K3, and the letter above on the plate",
 "streams": {
  "with ?": 772,
  "letters only": 768
 },
 "lags": [
  1,
  200
 ],
 "rules": 12,
 "k4_best_lag_hits": 5,
 "controls_best_lag_hits": [
  5,
  5,
  5,
  5,
  6,
  5,
  5,
  6,
  5,
  6
 ],
 "k4_best_geometric_hits": 3,
 "controls_best_geometric_hits": [
  4,
  4,
  4,
  4,
  5,
  4,
  4,
  2,
  4,
  2
 ],
 "k4_full": [],
 "k4_top": [],
 "k4_geometric": {
  "2 up, right, beau/std/std": 3,
  "1 up, left, vig/kry/std": 2,
  "1 up, left, beau/std/kry": 2,
  "1 up, left, var/std/std": 2,
  "1 up, left, var/kry/std": 2,
  "1 up, right, vig/kry/std": 2,
  "1 up, right, beau/std/kry": 2,
  "1 up, right, var/std/std": 2,
  "1 up, right, var/kry/std": 2,
  "2 up, left, var/kry/std": 2
 },
 "controls": "10 shuffled coppers (K4 shuffled, earlier text fixed; seed 118), identical search"
}
```

Notes: Lags 1-200 x 12 rules x 2 streams: K4 best 5/24, controls [5, 5, 5, 5, 6, 5, 5, 6, 5, 6]; full 0. Letter above on the plate: K4 best 3/24, controls [4, 4, 4, 4, 5, 4, 4, 2, 4, 2].


