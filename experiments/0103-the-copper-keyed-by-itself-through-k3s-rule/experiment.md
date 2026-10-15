# 0103-the-copper-keyed-by-itself-through-k3s-rule: The copper as its own key, read through K3's counting rule: key letter for place i is the carved letter at a + b i mod 97

**Family:** 1-keyed-periodic  
**Parent:** 0002-ciphertext-autokey  
**Decision:** reverted  
**Run:** 2026-10-15T20:12:59+00:00, 10.5 s, status ran  
**Time by phase:** unattributed 19 s, run 10 s, record 0 s

## In plain words

A cipher can use its own letters as the key. Experiment 2 tried taking the key for each letter from a fixed number of letters earlier. Here the key letter is picked from anywhere in the copper by K3's own counting rule: start somewhere, step by a fixed amount, wrap around at 97. That includes reading the copper backwards, like a mirror. We try every start and step, alone and with a short secret word added, against the 24 known letters.

## Walkthrough, by hand

1. Choose a start a = 0 and a step b = 96, which reads the copper backwards: place i takes its key from place 99 - i.
2. Place 22 (E, carved F) takes its key from place 77, a D.
3. On the sculpture's alphabet with Vigenere, F minus D must give E; count a hit if it does.
4. Do this for all 24 known places, every start and step, and every table rule.
5. With a secret word added, the leftover at each known place must repeat with the word's length.

## Worked example (generated)

```
the copper read backwards as its own key: place i takes its key from place 99 - i (a = 0, b = 96)
sculpture's alphabet, Vigenere

place  known  carved  key place  key letter  carved - key  hit
   22      E       F         77           D             Y  no
   23      A       L         76           G             T  no
   24      S       R         75           W             T  no
   25      T       V         74           K             V  no
   64      B       N         35           O             H  no
   65      E       Y         34           S             V  no
   74      K       K         25           V             T  no
```

## Lineage

Inherits from 0002-ciphertext-autokey. What changed: 0002 tested ciphertext autokey, where the key for place i is the carved letter a fixed distance back (i - lag). Here the key is the carved letter at any place given by K3's rule, a + b i mod 97 for every a and b, which includes the copper read backwards (b = -1, a mirror) and every decimation; alone, or with a repeating key of length 1-26 added.

## Hypothesis (domain expert)

Scheidt: 'mirrors and obfuscation' (C13), the system 'conveys not only the encrypted data, but also the key' (C6); K3's transposition is the rule i -> 191 + 192 i mod 337 (01-facts.md). Model: p_i = D(c_i, c_{f(i)}) with f(i) = a + b i mod 97, b = 1-96, a = 0-96, f(i) != i for the 24 known places, D the tableau decryption in one of 8 classes (plain and cipher alphabets standard or KRYPTOS; Vigenere, Beaufort, variant; key letters numbered on the cipher alphabet). The key is the copper itself, so every known letter is a check: 24 checks per setting. Second part: p_i = D(c_i, c_{f(i)} + k[i mod L]), L = 1-26; the residual must be periodic, tested by slot agreement. Ten shuffled coppers. 0002's lags are the case b = 1.

## Prediction

Alone: no (a, b, class) fits more than 6 of 24 known letters, as on the coppers. With a repeating key: nothing consistent below period 20, counts in the coppers' range. Zero candidates.

## Method

1. For each a, b and class, compute the residual r_i = (key value needed at known place i) - (number of c_{f(i)}).
2. Alone: count known places with r_i = 0.
3. With a key of length L: residuals sharing slot i mod L must agree.
4. Repeat on ten shuffled coppers.
5. Decrypt any full fit.

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
 "family": "the copper as its own key through K3's rule f(i) = a + b i mod 97, alone or plus a periodic key",
 "maps": 7031,
 "classes": 16,
 "k4_best_hits_alone": 7,
 "controls_best_hits_alone": [
  7,
  7,
  7,
  7,
  7,
  7,
  7,
  9,
  7,
  7
 ],
 "k4_full_alone": 0,
 "k4_live_by_period": [
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  2,
  4309
 ],
 "controls_live_min": [
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  3,
  4285
 ],
 "controls_live_max": [
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  13,
  4430
 ],
 "periods_outside_control_range": [
  25
 ],
 "k4_live_below_20": [],
 "n_k4_live_below_20": 0,
 "controls": "10 shuffled coppers (seed 103), identical search"
}
```

Notes: 7,031 maps x 16 rules. Alone: K4 best 7/24, controls [7, 7, 7, 7, 7, 7, 7, 9, 7, 7]; full fits 0. With a periodic key: K4 live below 20: 0; periods outside the control range: [25].


