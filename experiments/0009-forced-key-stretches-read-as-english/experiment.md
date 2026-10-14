# 0009-forced-key-stretches-read-as-english: Do the two crib runs force a readable key, with the copper exact or off by one letter?

**Family:** 1-keyed-periodic  
**Parent:** 0005-quagmire-period-sweep-forced-keys  
**Decision:** reverted  
**Run:** 2026-10-14T16:46:08+00:00, 0.5 s, status ran  
**Time by phase:** design 14 s, implement 81 s, test 0 s, run 0 s, record 0 s

## In plain words

If the fourth message used a secret word with the sculpture's table, the 13 known letters of EASTNORTHEAST pin down 13 letters of that secret word in a row, and BERLINCLOCK pins down 11 more. A secret word made of English should look like English in those stretches. We read them off under every way the table can be used and ask a simple question: does any stretch look like English rather than noise? We also allow for the sculptor having dropped or added one letter somewhere, as he did in the second message, which would shift everything after that point by one.

## Walkthrough, by hand

1. Take the convention: plaintext and key on the sculpture's alphabet, Vigenere.
2. Position 22 is plaintext E, ciphertext F. In the sculpture's alphabet E is index 10 and F is index 11, so the key letter has index 1: R.
3. Position 23 is A against L: A is 7, L is 18, key index 11: D.
4. Carry on through position 34 to get 13 key letters in a row.
5. Read them aloud. A real key word gives something like a word; noise gives something like RDQXJ.
6. Score it by counting how common each run of four letters is in English.
7. Now suppose the sculptor dropped a letter somewhere before position 22: shift the ciphertext one place and repeat.
8. The best stretch across all of this is the answer; compare it with real English windows of the same length.

## Worked example (generated)

```
forced key stretch under EASTNORTHEAST, convention kry/std/kry Vigenere, exact copper

pos  plain  cipher  key letter
 22    E      F       Q
 23    A      L       T
 24    S      R       E
 25    T      V       L
 26    N      Q       W
 27    O      Q       E
 28    R      P       H
 29    T      R       G
 30    H      N       Z
 31    E      G       U
 32    A      K       P
 33    S      S       F
 34    T      S       H

stretch: QTELWEHGZUPFH   score -7.72 per quadgram (English about -3.6, noise about -6.5)
```

## Lineage

Inherits from 0005-quagmire-period-sweep-forced-keys. What changed: Instead of matching forced key fragments against a word list, score them as English. Add the one-letter-error parameter: a letter inserted or deleted at every position.

## Hypothesis (domain expert)

Under any periodic tableau whose period the cribs allow (27 and above, 0005), EASTNORTHEAST at 22-34 forces 13 consecutive key letters and BERLINCLOCK at 64-74 forces 11, under each of the 24 conventions. If the key is a word or phrase, as Scheidt insists (C5, C6), those stretches must read as English. Schridde 2017 found them gibberish under the plain tableau; 0005 matched them against 62 vocabulary words and K1-K3 windows only. This experiment scores every stretch by quadgram log-probability per letter and compares it with the distribution of random strings and of true English windows of the same length from K1-K3. Then the one-letter-error parameter (family G, C17, C18, the K2 precedent): a letter inserted or deleted at each of 97 positions shifts the ciphertext under every crib past that point by one, giving new stretches. Expected under the null: the best of about 9,400 stretches sits around two standard deviations above the random mean and well below the English mean. Bounds: all 24 conventions, exact copper and every single insertion or deletion, both crib runs, keys at any period of 27 or more.

## Prediction

No forced stretch scores as well as a typical English window of its length. The best stretch scores below -4.5 per quadgram, against about -3.6 for English and about -6.5 for noise. Allowing one inserted or deleted letter does not change that. Zero candidates pass.

## Method

1. For each convention, force the key letter at each crib position from the plaintext and the ciphertext letter.
2. Join the forced letters of positions 22-34 into a 13-letter stretch and 64-74 into an 11-letter stretch.
3. Score each stretch by mean log10 quadgram probability.
4. Repeat with the ciphertext altered by one deleted letter at each position, then by one inserted blank at each position, which shifts every crib beyond that point.
5. Calibrate: score all 13- and 11-letter windows of the K1-K3 plaintexts, and 20,000 random strings.
6. Report the best stretches with their z-scores against both distributions.

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
 "family": "periodic tableau, separate alphabets, period 27+; forced key stretches scored as English",
 "conventions": 24,
 "copper_variants": 196,
 "stretches_scored": 9408,
 "calibration_mean_sd": {
  "english_13": [
   -4.251,
   0.466
  ],
  "english_11": [
   -4.252,
   0.518
  ],
  "random_13": [
   -8.292,
   0.98
  ],
  "random_11": [
   -8.295,
   1.08
  ]
 },
 "best_overall": {
  "score": -5.795,
  "stretch": "FNOEEADIAG",
  "copper": "inserted before 74",
  "convention": "kry/std/std/vig",
  "run": "64-74",
  "z_vs_random": 2.32,
  "z_vs_english": -2.98
 },
 "best_exact_copper": {
  "score": -6.149,
  "stretch": "FNOEEADIAGK",
  "copper": "exact",
  "convention": "kry/std/std/vig",
  "run": "64-74",
  "z_vs_random": 1.99,
  "z_vs_english": -3.66
 },
 "top_ten": [
  {
   "score": -5.795,
   "stretch": "FNOEEADIAG",
   "copper": "inserted before 74",
   "convention": "kry/std/std/vig",
   "run": "64-74",
   "z_vs_random": 2.32,
   "z_vs_english": -2.98
  },
  {
   "score": -5.852,
   "stretch": "FNOEEADIAP",
   "copper": "inserted before 73",
   "convention": "kry/std/std/vig",
   "run": "64-74",
   "z_vs_random": 2.26,
   "z_vs_english": -3.09
  },
  {
   "score": -5.926,
   "stretch": "SVICPIFGROWH",
   "copper": "inserted before 34",
   "convention": "kry/std/kry/varbeau",
   "run": "22-34",
   "z_vs_random": 2.41,
   "z_vs_english": -3.59
  },
  {
   "score": -5.947,
   "stretch": "SVICPIFGROWF",
   "copper": "inserted before 33",
   "convention": "kry/std/kry/varbeau",
   "run": "22-34",
   "z_vs_random": 2.39,
   "z_vs_english": -3.64
  },
  {
   "score": -5.99,
   "stretch": "FQXDESREPO",
   "copper": "inserted before 70",
   "convention": "std/std/kry/vig",
   "run": "64-74",
   "z_vs_random": 2.13,
   "z_vs_english": -3.36
  },
  {
   "score": -6.012,
   "stretch": "FNOEEADIAGW",
   "copper": "deleted 74",
   "convention": "kry/std/std/vig",
   "run": "64-74",
   "z_vs_random": 2.11,
   "z_vs_english": -3.4
  },
  {
   "score": -6.043,
   "stretch": "JLJODEIGNOSKH",
   "copper": "deleted 28",
   "convention": "std/std/std/beau",
   "run": "22-34",
   "z_vs_random": 2.29,
   "z_vs_english": -3.84
  },
  {
   "score": -6.061,
   "stretch": "FNOEEADIABW",
   "copper": "deleted 73",
   "convention": "kry/std/std/vig",
   "run": "64-74",
   "z_vs_random": 2.07,
   "z_vs_english": -3.49
  },
  {
   "score": -6.077,
   "stretch": "SYMORCHLKT",
   "copper": "inserted before 67",
   "convention": "std/kry/std/vig",
   "run": "64-74",
   "z_vs_random": 2.05,
   "z_vs_english": -3.52
  },
  {
   "score": -6.078,
   "stretch": "PAGIFORWLYA",
   "copper": "deleted 9",
   "convention": "std/kry/kry/beau",
   "run": "64-74",
   "z_vs_random": 2.05,
   "z_vs_english": -3.53
  }
 ],
 "exact_copper_all_24": [
  {
   "score": -6.149,
   "stretch": "FNOEEADIAGK",
   "copper": "exact",
   "convention": "kry/std/std/vig",
   "run": "64-74",
   "z_vs_random": 1.99,
   "z_vs_english": -3.66
  },
  {
   "score": -6.151,
   "stretch": "SVICPIFGROWHF",
   "copper": "exact",
   "convention": "kry/std/kry/varbeau",
   "run": "22-34",
   "z_vs_random": 2.18,
   "z_vs_english": -4.08
  },
  {
   "score": -6.818,
   "stretch": "SJRXTUOSORAMN",
   "copper": "exact",
   "convention": "std/kry/std/varbeau",
   "run": "22-34",
   "z_vs_random": 1.5,
   "z_vs_english": -5.51
  },
  {
   "score": -7.004,
   "stretch": "QRTPHIUUARAYZ",
   "copper": "exact",
   "convention": "std/kry/std/beau",
   "run": "22-34",
   "z_vs_random": 1.31,
   "z_vs_english": -5.91
  },
  {
   "score": -7.178,
   "stretch": "ELYOIECBAQK",
   "copper": "exact",
   "convention": "kry/kry/kry/vig",
   "run": "64-74",
   "z_vs_random": 1.03,
   "z_vs_english": -5.65
  },
  {
   "score": -7.205,
   "stretch": "CECHPTSDQDDDE",
   "copper": "exact",
   "convention": "std/std/kry/beau",
   "run": "22-34",
   "z_vs_random": 1.11,
   "z_vs_english": -6.34
  },
  {
   "score": -7.304,
   "stretch": "XYHANZEFHYHMK",
   "copper": "exact",
   "convention": "kry/kry/std/beau",
   "run": "22-34",
   "z_vs_random": 1.01,
   "z_vs_english": -6.55
  },
  {
   "score": -7.383,
   "stretch": "UGUHMRUKAFK",
   "copper": "exact",
   "convention": "std/kry/std/beau",
   "run": "64-74",
   "z_vs_random": 0.84,
   "z_vs_english": -6.05
  },
  {
   "score": -7.467,
   "stretch": "ICXUEILMNSK",
   "copper": "exact",
   "convention": "kry/kry/kry/varbeau",
   "run": "64-74",
   "z_vs_random": 0.77,
   "z_vs_english": -6.21
  },
  {
   "score": -7.477,
   "stretch": "JLJODEGKUKKKL",
   "copper": "exact",
   "convention": "std/std/std/beau",
   "run": "22-34",
   "z_vs_random": 0.83,
   "z_vs_english": -6.92
  },
  {
   "score": -7.532,
   "stretch": "RDUMRIYWOYNKY",
   "copper": "exact",
   "convention": "kry/kry/kry/vig",
   "run": "22-34",
   "z_vs_random": 0.78,
   "z_vs_english": -7.04
  },
  {
   "score": -7.558,
   "stretch": "VNMWWAXSAUQ",
   "copper": "exact",
   "convention": "kry/std/std/varbeau",
   "run": "64-74",
   "z_vs_random": 0.68,
   "z_vs_english": -6.38
  },
  {
   "score": -7.645,
   "stretch": "LRCFPLJIHUA",
   "copper": "exact",
   "convention": "kry/kry/std/vig",
   "run": "64-74",
   "z_vs_random": 0.6,
   "z_vs_english": -6.55
  },
  {
   "score": -7.667,
   "stretch": "BLCPASFBFCKHG",
   "copper": "exact",
   "convention": "std/kry/kry/vig",
   "run": "22-34",
   "z_vs_random": 0.64,
   "z_vs_english": -7.33
  },
  {
   "score": -7.688,
   "stretch": "MUYKLGKORNA",
   "copper": "exact",
   "convention": "std/std/std/vig",
   "run": "64-74",
   "z_vs_random": 0.56,
   "z_vs_english": -6.63
  },
  {
   "score": -7.719,
   "stretch": "QTELWEHGZUPFH",
   "copper": "exact",
   "convention": "kry/std/kry/vig",
   "run": "22-34",
   "z_vs_random": 0.58,
   "z_vs_english": -7.44
  },
  {
   "score": -7.744,
   "stretch": "HYSSRSHDNLQ",
   "copper": "exact",
   "convention": "std/std/kry/beau",
   "run": "64-74",
   "z_vs_random": 0.51,
   "z_vs_english": -6.74
  },
  {
   "score": -7.792,
   "stretch": "UELRXLONZVDMO",
   "copper": "exact",
   "convention": "kry/std/std/vig",
   "run": "22-34",
   "z_vs_random": 0.51,
   "z_vs_english": -7.6
  },
  {
   "score": -7.8,
   "stretch": "PJYVLPRSTGA",
   "copper": "exact",
   "convention": "kry/kry/std/varbeau",
   "run": "64-74",
   "z_vs_random": 0.46,
   "z_vs_english": -6.85
  },
  {
   "score": -7.823,
   "stretch": "OGHTTKPBKSD",
   "copper": "exact",
   "convention": "kry/std/kry/vig",
   "run": "64-74",
   "z_vs_random": 0.44,
   "z_vs_english": -6.89
  },
  {
   "score": -7.829,
   "stretch": "BYHITCDFYZD",
   "copper": "exact",
   "convention": "std/kry/kry/varbeau",
   "run": "64-74",
   "z_vs_random": 0.43,
   "z_vs_english": -6.91
  },
  {
   "score": -7.877,
   "stretch": "ICOPEJKMCZK",
   "copper": "exact",
   "convention": "std/kry/std/varbeau",
   "run": "64-74",
   "z_vs_random": 0.39,
   "z_vs_english": -7.0
  },
  {
   "score": -7.965,
   "stretch": "OCGGBGOKTRU",
   "copper": "exact",
   "convention": "std/std/std/beau",
   "run": "64-74",
   "z_vs_random": 0.31,
   "z_vs_english": -7.17
  },
  {
   "score": -7.999,
   "stretch": "FQXDESDHLGK",
   "copper": "exact",
   "convention": "std/std/kry/vig",
   "run": "64-74",
   "z_vs_random": 0.27,
   "z_vs_english": -7.23
  },
  {
   "score": -8.044,
   "stretch": "BKVSBPCXFCTAC",
   "copper": "exact",
   "convention": "kry/kry/std/vig",
   "run": "22-34",
   "z_vs_random": 0.25,
   "z_vs_english": -8.14
  },
  {
   "score": -8.122,
   "stretch": "IRJDHGMIMJAON",
   "copper": "exact",
   "convention": "std/kry/std/vig",
   "run": "22-34",
   "z_vs_random": 0.17,
   "z_vs_english": -8.3
  },
  {
   "score": -8.189,
   "stretch": "WXAKGZTOAXAFD",
   "copper": "exact",
   "convention": "kry/kry/kry/beau",
   "run": "22-34",
   "z_vs_random": 0.1,
   "z_vs_english": -8.45
  },
  {
   "score": -8.271,
   "stretch": "ZJOBZEXPUXAKX",
   "copper": "exact",
   "convention": "kry/kry/kry/varbeau",
   "run": "22-34",
   "z_vs_random": 0.02,
   "z_vs_english": -8.62
  },
  {
   "score": -8.632,
   "stretch": "BNENTXBQRMA",
   "copper": "exact",
   "convention": "kry/kry/std/beau",
   "run": "64-74",
   "z_vs_random": -0.31,
   "z_vs_english": -8.46
  },
  {
   "score": -8.745,
   "stretch": "ZQFIZLYDVYHAY",
   "copper": "exact",
   "convention": "kry/kry/std/varbeau",
   "run": "22-34",
   "z_vs_random": -0.46,
   "z_vs_english": -9.64
  },
  {
   "score": -8.865,
   "stretch": "JMWZCUJURLLXV",
   "copper": "exact",
   "convention": "kry/std/kry/beau",
   "run": "22-34",
   "z_vs_random": -0.58,
   "z_vs_english": -9.9
  },
  {
   "score": -8.942,
   "stretch": "REZYPYXXSYDKZ",
   "copper": "exact",
   "convention": "std/std/kry/vig",
   "run": "22-34",
   "z_vs_random": -0.66,
   "z_vs_english": -10.06
  },
  {
   "score": -8.951,
   "stretch": "ZPBYXYCCUYQAB",
   "copper": "exact",
   "convention": "std/std/std/varbeau",
   "run": "22-34",
   "z_vs_random": -0.67,
   "z_vs_english": -10.08
  },
  {
   "score": -9.047,
   "stretch": "RGTGNWRJLFK",
   "copper": "exact",
   "convention": "kry/kry/kry/beau",
   "run": "64-74",
   "z_vs_random": -0.7,
   "z_vs_english": -9.26
  },
  {
   "score": -9.07,
   "stretch": "GWPJDPMNBFXOM",
   "copper": "exact",
   "convention": "kry/std/std/varbeau",
   "run": "22-34",
   "z_vs_random": -0.79,
   "z_vs_english": -10.34
  },
  {
   "score": -9.091,
   "stretch": "QSQAFLQDKOD",
   "copper": "exact",
   "convention": "std/kry/kry/beau",
   "run": "64-74",
   "z_vs_random": -0.74,
   "z_vs_english": -9.34
  },
  {
   "score": -9.283,
   "stretch": "BLZCDCYYGCKAZ",
   "copper": "exact",
   "convention": "std/std/std/vig",
   "run": "22-34",
   "z_vs_random": -1.01,
   "z_vs_english": -10.8
  },
  {
   "score": -9.646,
   "stretch": "MCLWNQHMHLKFG",
   "copper": "exact",
   "convention": "std/kry/kry/varbeau",
   "run": "22-34",
   "z_vs_random": -1.38,
   "z_vs_english": -11.57
  },
  {
   "score": -9.708,
   "stretch": "JLNIABQQKLKXZ",
   "copper": "exact",
   "convention": "std/kry/kry/beau",
   "run": "22-34",
   "z_vs_random": -1.44,
   "z_vs_english": -11.71
  },
  {
   "score": -9.77,
   "stretch": "SYMLWRQOYBQ",
   "copper": "exact",
   "convention": "std/kry/std/vig",
   "run": "64-74",
   "z_vs_random": -1.37,
   "z_vs_english": -10.65
  },
  {
   "score": -9.853,
   "stretch": "MXFEVLJHXRJ",
   "copper": "exact",
   "convention": "std/kry/kry/vig",
   "run": "64-74",
   "z_vs_random": -1.44,
   "z_vs_english": -10.81
  },
  {
   "score": -9.941,
   "stretch": "UCJFBFUJDXD",
   "copper": "exact",
   "convention": "kry/std/kry/beau",
   "run": "64-74",
   "z_vs_random": -1.52,
   "z_vs_english": -10.98
  },
  {
   "score": -9.962,
   "stretch": "ZIRXWXYYQXJKR",
   "copper": "exact",
   "convention": "std/std/kry/varbeau",
   "run": "22-34",
   "z_vs_random": -1.7,
   "z_vs_english": -12.25
  },
  {
   "score": -9.968,
   "stretch": "QSXZJVQVBRRYW",
   "copper": "exact",
   "convention": "kry/std/std/beau",
   "run": "22-34",
   "z_vs_random": -1.71,
   "z_vs_english": -12.27
  },
  {
   "score": -10.181,
   "stretch": "VJQMIMVQKYK",
   "copper": "exact",
   "convention": "kry/std/std/beau",
   "run": "64-74",
   "z_vs_random": -1.75,
   "z_vs_english": -11.45
  },
  {
   "score": -10.278,
   "stretch": "UGFVVKWMKQJ",
   "copper": "exact",
   "convention": "kry/std/kry/varbeau",
   "run": "64-74",
   "z_vs_random": -1.84,
   "z_vs_english": -11.64
  },
  {
   "score": -10.287,
   "stretch": "OGCQPUQMJNA",
   "copper": "exact",
   "convention": "std/std/std/varbeau",
   "run": "64-74",
   "z_vs_random": -1.84,
   "z_vs_english": -11.65
  },
  {
   "score": -10.922,
   "stretch": "HSYJIQJFCGK",
   "copper": "exact",
   "convention": "std/std/kry/varbeau",
   "run": "64-74",
   "z_vs_random": -2.43,
   "z_vs_english": -12.88
  }
 ]
}
```

Notes: Diagnostic: no full key is implied, so no candidates. The verdict is the gap between the best stretch and the English distribution.


