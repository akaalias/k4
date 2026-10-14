# 0012-plaintext-autokey-chained-from-cribs: Plaintext autokey, chained: the 24 known letters force the rest, lag by lag

**Family:** 1-keyed-periodic  
**Parent:** 0003-plaintext-autokey-all-lags  
**Decision:** reverted  
**Run:** 2026-10-14T16:59:18+00:00, 0.5 s, status ran  
**Time by phase:** design 43 s, implement 56 s, test 1 s, run 0 s, record 0 s

## In plain words

In an autokey cipher the message is its own secret word: each letter is enciphered using the letter some fixed distance before it. That makes the 24 known letters very powerful. Each one was used to encipher a letter further on, so that letter can be worked out; and each one was itself enciphered by a letter further back, so that one can be worked out too. Repeating this spreads outward until, for short distances, the whole message is known. We try every distance and every way of using the table, and read what comes out.

## Walkthrough, by hand

1. Take lag 13 and the sculpture's alphabet with Vigenere.
2. Position 22 is E and its ciphertext is F; under the table, the key that turns E into F is R, so position 9 is R.
3. Position 35 was enciphered with key E, the letter at 22; the ciphertext at 35 is S, and S decrypted with key E is the letter at
35. 
4. Now 9 and 35 are known, so 48 and 61 follow, and so on, up and down by 13 until the chain leaves the text.
5. Do the same from every one of the 24 known letters.
6. Where two chains meet, the letters must agree, or lag 13 is dead under this convention.
7. If every position fills, read the text aloud.
8. The first 13 letters were enciphered with the primer; the key letter that maps each of them to its ciphertext is the primer, which should be a word.

## Worked example (generated)

```
lag 13, KRYPTOS alphabet throughout, Vigenere: chaining from the cribs

consistent: False; letters forced: 28 of 97
.....................EASTNORTHEASTS............N............K..BERLINCLOCK............K..........

position 22 (E, cipher F) forces position 9 = R; key E at 22 decrypts cipher O at 35 to Q
```

## Lineage

Inherits from 0003-plaintext-autokey-all-lags. What changed: 0003 only checked the cribs against each other. Here each known letter is also used as the key for the letter one lag later, and as the ciphertext's partner one lag earlier, and the forced letters are chained until nothing new follows. For small lags that fixes the whole text.

## Hypothesis (domain expert)

Plaintext autokey (the NSA's 1992 guess, C11a; a Scheidt-era hand system, C5): c[i] = E(p[i], p[i-L]) for i >= L after a primer of length L. A crib letter p[i] forces p[i-L] through c[i] and forces p[i+L] through c[i+L]; each forced letter forces two more. The closure from the 24 cribs covers every residue class modulo L that a crib position touches, so for L <= 13 the whole text is forced, for L up to about 24 most of it, and for larger L two or three stretches. 0003 found lags 1-11 and 30-52 inconsistent inside the cribs; lags 12-29 and 53-96 were undecided. Here, under each of the 24 conventions and each lag 1-96, we propagate to closure, reject on any conflict, and for a fully forced text derive the primer and submit the candidate. Partially forced texts are scored as English on their forced runs and compared with the same procedure on shuffled K4 letters. Bounds: complete for plaintext autokey with a primer of length L, any L 1-96, under these conventions.

## Prediction

Every lag from 1 to 25 either conflicts somewhere in the chain or yields a fully forced text that is not English, scoring below -6 per quadgram against -3.6 for English. Lags above 25 leave stretches that score no better than the shuffled control. No candidate passes the English standard; a fully forced text may pass the four gates by construction and will then stand as a champion with a loss of 3 to 4, which is a gibberish champion, not a solution.

## Method

1. For each convention and lag L, start with the 24 cribs as forced letters.
2. For each forced letter at i: if i >= L, force p[i-L] as the key that maps p[i] to c[i]; if i + L < 97, force p[i+L] by decrypting c[i+L] with key p[i].
3. Repeat until nothing new appears; any conflict kills the pair.
4. If all 97 letters are forced, derive the primer k[i] for i < L and submit the text.
5. Otherwise score the forced runs of four or more letters as English.
6. Run the same procedure on ten shuffles of K4 for a control.

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
 "family": "plaintext autokey with primer, chained closure from cribs",
 "conventions": 24,
 "lags": "1-96",
 "lags_dead_all_conventions": [
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
 "consistent_pairs_by_lag": {
  "26": 1,
  "27": 24,
  "28": 24,
  "29": 24,
  "53": 24,
  "54": 24,
  "55": 24,
  "56": 24,
  "57": 24,
  "58": 24,
  "59": 24,
  "60": 24,
  "61": 24,
  "62": 24,
  "63": 24,
  "64": 24,
  "65": 24,
  "66": 24,
  "67": 24,
  "68": 24,
  "69": 24,
  "70": 24,
  "71": 24,
  "72": 24,
  "73": 24,
  "74": 24,
  "75": 24,
  "76": 24,
  "77": 24,
  "78": 24,
  "79": 24,
  "80": 24,
  "81": 24,
  "82": 24,
  "83": 24,
  "84": 24,
  "85": 24,
  "86": 24,
  "87": 24,
  "88": 24,
  "89": 24,
  "90": 24,
  "91": 24,
  "92": 24,
  "93": 24,
  "94": 24,
  "95": 24,
  "96": 24
 },
 "fully_forced_candidates": 0,
 "best_english_of_forced_runs": [
  {
   "score": -4.095,
   "lag": 96,
   "convention": "std/std/std/vig",
   "forced_letters": 24,
   "runs": [
    "EASTNORTHEAST",
    "BERLINCLOCK"
   ]
  },
  {
   "score": -4.095,
   "lag": 96,
   "convention": "std/std/std/varbeau",
   "forced_letters": 24,
   "runs": [
    "EASTNORTHEAST",
    "BERLINCLOCK"
   ]
  },
  {
   "score": -4.095,
   "lag": 96,
   "convention": "std/std/std/beau",
   "forced_letters": 24,
   "runs": [
    "EASTNORTHEAST",
    "BERLINCLOCK"
   ]
  },
  {
   "score": -4.095,
   "lag": 96,
   "convention": "std/std/kry/vig",
   "forced_letters": 24,
   "runs": [
    "EASTNORTHEAST",
    "BERLINCLOCK"
   ]
  },
  {
   "score": -4.095,
   "lag": 96,
   "convention": "std/std/kry/varbeau",
   "forced_letters": 24,
   "runs": [
    "EASTNORTHEAST",
    "BERLINCLOCK"
   ]
  },
  {
   "score": -4.095,
   "lag": 96,
   "convention": "std/std/kry/beau",
   "forced_letters": 24,
   "runs": [
    "EASTNORTHEAST",
    "BERLINCLOCK"
   ]
  },
  {
   "score": -4.095,
   "lag": 96,
   "convention": "std/kry/std/vig",
   "forced_letters": 24,
   "runs": [
    "EASTNORTHEAST",
    "BERLINCLOCK"
   ]
  },
  {
   "score": -4.095,
   "lag": 96,
   "convention": "std/kry/std/varbeau",
   "forced_letters": 24,
   "runs": [
    "EASTNORTHEAST",
    "BERLINCLOCK"
   ]
  }
 ],
 "shuffled_control_best_per_seed": [
  -4.095,
  -4.064,
  -4.095,
  -4.083,
  -4.095,
  -4.095,
  -4.095,
  -4.095,
  -4.095,
  -4.095
 ]
}
```

Notes: 1129 consistent (lag, convention) pairs; 0 fully forced texts submitted. A fully forced text passes the crib gate by construction; only its English score matters.


