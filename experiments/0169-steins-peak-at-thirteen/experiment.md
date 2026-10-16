# 0169-steins-peak-at-thirteen: F12.3: Stein's index-of-coincidence peak at 13 alphabets in K1 and K2: real or chance, against shuffles that keep each part's own key period

**Family:** 12-steins-way  
**Parent:** 0168-k4-statistics-against-a-thousand-shuffles  
**Decision:** reverted  
**Run:** 2026-10-16T23:01:37+00:00, 8.9 s, status ran  
**Time by phase:** unattributed 59 s, run 9 s, record 0 s

## In plain words

When Stein cut the first two messages into 13 interleaved strands, the letters matched a little more often than expected, and he wondered whether a second, 13-letter code lay underneath. We check whether that bump is bigger than what the known keys alone would give, by shuffling the letters only among positions that share a key letter, 10,000 times.

## Walkthrough, by hand

1. Write K1's 63 letters into 13 strands: letters 1, 14, 27, ...; 2, 15, 28, ...; and so on.
2. In each strand count the pairs of equal letters, divide by the possible pairs, and average over the 13 strands.
3. Shuffle K1's letters, but only among places that used the same key letter (places 1, 11, 21, ... together), and recompute; repeat 10,000 times.
4. If K1's value is above nearly all the shuffled values, the bump at 13 is more than the key explains.

## Worked example (generated)

```
K1's 63 letters in 13 strands (letter i goes to strand i mod 13):

  strand  1: EUGBY
  strand  2: MSNQQ
  strand  3: UDFVT
  strand  4: FJIYM
  strand  5: PKVUK
  strand  6: HZJVY
  strand  7: ZLYLR
  strand  8: LDQLD
  strand  9: RKTTM
  strand 10: FRQRF
  strand 11: ANUED
  strand 12: XSXV
  strand 13: YHQJ

average index of coincidence over the 13 strands: 0.0744; over 10 strands (the key length): 0.0914
```

## Lineage

Inherits from 0168-k4-statistics-against-a-thousand-shuffles. What changed: F12.3 (C28). Stein found a peak in the average index of coincidence at m = 13 alphabets in K1 (his Part I, key length 10) and in K2's Part II (the 125 letters between the panel's first two question marks, key length 8) and asked: 'Could this be a sign of another code overlaid on top of the others... Or just a coincidence?' Here the question is answered against the right null: shuffles that keep each part's key-period structure (letters permuted only within their own key column), 10,000 per text; also plain shuffles. Statistics: the I.C. at 13 and the local peak (I.C. at 13 minus the larger of 12 and 14). Texts: K1, K2 Part II (Stein's), K2 Part III, all of K2, and the K1 and K2 plaintexts. K4's own value at 13 is in 0168 (p 0.21).

## Hypothesis (domain expert)

C28 (knowledge/11-clue-register.md); Stein 1999 (knowledge/sources/stein-1999-cracking-the-courtyard-crypto.txt), Figures 7, 17, 26: 'I knew that the peak at m = 10 was caused by the 10-letter keyword, and the peaks at 5 and 15 are expected artifacts... But what was this peak at m = 13? ... it also showed up in the I.C. plot for Part II.' Model of the null: a Quagmire III ciphertext of period L has column multisets fixed by the plaintext and key; permuting letters within each column (place mod L) keeps every period-L property and destroys any other structure. If K1's and Part II's I.C. at 13 sit inside that null, the peak is a coincidence of the plaintext's letters; if outside, something keyed at 13 exists and K4 would be tested for it.

## Prediction

The m = 13 values sit inside the key-period null for K1 and Part II (p above 0.05): a coincidence of short texts. Zero candidates.

## Method

1. Texts: K1 (63), K2 Part II (125), Part III (61), K2 without '?' (369), K1 and K2 plaintexts.
2. I.C. averaged over m interleaved strands, m 12-14; the peak statistic.
3. 10,000 within-column shuffles (key period 10 for K1, 8 for K2) and 10,000 plain shuffles per text: one-sided p.

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
 "family": "observation: the I.C. at 13 alphabets in K1 and K2 against key-period-preserving shuffles",
 "shuffles": 10000,
 "rows": [
  {
   "text": "K1 ciphertext (Stein's Part I, key 10)",
   "letters": 63,
   "ic13": 0.07436,
   "peak13": 0.04817,
   "p_ic13 (within key columns)": 0.0075,
   "p_peak13 (within key columns)": 0.0046,
   "p_ic13 (plain shuffles)": 0.0359,
   "p_peak13 (plain shuffles)": 0.0102
  },
  {
   "text": "K2 Part II (Stein's 125 letters, key 8)",
   "letters": 125,
   "ic13": 0.04231,
   "peak13": 0.0083,
   "p_ic13 (within key columns)": 0.2435,
   "p_peak13 (within key columns)": 0.0478,
   "p_ic13 (plain shuffles)": 0.331,
   "p_peak13 (plain shuffles)": 0.1256
  },
  {
   "text": "K2 Part III (key 8)",
   "letters": 61,
   "ic13": 0.04103,
   "peak13": -0.0062,
   "p_ic13 (within key columns)": 0.4051,
   "p_peak13 (within key columns)": 0.531,
   "p_ic13 (plain shuffles)": 0.4586,
   "p_peak13 (plain shuffles)": 0.4235
  },
  {
   "text": "K2 ciphertext without '?' (key 8)",
   "letters": 369,
   "ic13": 0.04837,
   "peak13": -0.00635,
   "p_ic13 (within key columns)": 0.0894,
   "p_peak13 (within key columns)": 0.1197,
   "p_ic13 (plain shuffles)": 0.1486,
   "p_peak13 (plain shuffles)": 0.8993
  },
  {
   "text": "K1 plaintext",
   "letters": 63,
   "ic13": 0.04359,
   "peak13": -0.0453,
   "p_ic13 (plain shuffles)": 0.8613,
   "p_peak13 (plain shuffles)": 0.8601
  },
  {
   "text": "K2 plaintext",
   "letters": 369,
   "ic13": 0.06619,
   "peak13": -0.00239,
   "p_ic13 (plain shuffles)": 0.3845,
   "p_peak13 (plain shuffles)": 0.5514
  }
 ],
 "stein_texts_below_p_0_01": [
  "K1 ciphertext (Stein's Part I, key 10)"
 ],
 "controls": "10000 within-key-column shuffles and 10000 plain shuffles per text (seed 1613)"
}
```

Notes: K1 ciphertext (Stein's Part I, key 10): I.C.13 0.07436, p within-columns 0.0075, plain 0.0359; K2 Part II (Stein's 125 letters, key 8): I.C.13 0.04231, p within-columns 0.2435, plain 0.331; K2 Part III (key 8): I.C.13 0.04103, p within-columns 0.4051, plain 0.4586; K2 ciphertext without '?' (key 8): I.C.13 0.04837, p within-columns 0.0894, plain 0.1486; K1 plaintext: I.C.13 0.04359, p within-columns -, plain 0.8613; K2 plaintext: I.C.13 0.06619, p within-columns -, plain 0.3845


