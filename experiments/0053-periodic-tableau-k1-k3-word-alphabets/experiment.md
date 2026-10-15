# 0053-periodic-tableau-k1-k3-word-alphabets: The repeating secret word again, on tables rebuilt from the words of the solved messages

**Family:** 1-keyed-periodic  
**Parent:** 0020-short-periods-mixed-alphabets-consistency  
**Decision:** reverted  
**Run:** 2026-10-15T12:10:52+00:00, 73.1 s, status ran  
**Time by phase:** design 0 s, implement 13 s, test 0 s, run 73 s, record 0 s

## In plain words

The first two messages used the sculpture's table with a secret word repeated over and over. The table itself can be rebuilt from a word, and so far we rebuilt it only from the puzzle's own word list. The solved messages are full of other words, and Sanborn's last letter mentions Egypt and a message being delivered, so we rebuild the table from all of those and ask again, for every length of secret word up to 52, whether the 24 known letters can agree. Scrambled copies of the copper get the same test, so we can tell real agreement from luck.

## Walkthrough, by hand

1. Take the word SHADING from K1 and build its alphabet: SHADINGBCEFJKLMOPQRTUVWXYZ.
2. Take INVISIBLE from K2 for the carved letters: INVSBLEACDFGHJKMOPQRTUWXYZ.
3. Place 22 holds E under carved F: counting from 0, E is 9 in the first alphabet and F is 10 in the second, so Vigenere needs key 1.
4. With a secret word of 7 letters, places 22 and 29 share a slot, so place 29 (T under carved R) must also need key 1.
5. T is 19 in the first alphabet and R is 19 in the second, so it needs 0: a contradiction, and length 7 is dead for this pair.
6. Repeat for every pair, mode and length.

## Worked example (generated)

```
plain  SHADINGBCEFJKLMOPQRTUVWXYZ
cipher INVSBLEACDFGHJKMOPQRTUWXYZ

place  plain  carved  key (Vigenere)  slot at period 7
   22    E      F          1               0
   29    T      R          0               0
   23    A      L          3               1
   30    H      N          0               1
```

## Lineage

Inherits from 0020-short-periods-mixed-alphabets-consistency. What changed: Experiments 20 and 48 rebuilt the table's alphabets only from the puzzle's own vocabulary list. Here the alphabets are rebuilt from every word of the three solved messages and from the words Sanborn's 2025 letter points at (EGYPT, WALL, CAIRO, MESSAGE, DELIVER and others), and the crib test is rerun at every period from 1 to 52, with shuffled copies of the copper as the control.

## Hypothesis (domain expert)

Periodic tableau with separate plain and cipher alphabets (Quagmire family), alphabets keyword-mixed from words outside the 62-word vocabulary: every distinct word of the K1-K3 plaintexts with at least three distinct letters (C7, C30: earlier text may carry the key) and the C13/C14 words EGYPT, CAIRO, LUXOR, WALL, NOVEMBER, MESSAGE, DELIVER, DELIVERING, TRANSMIT, plus standard and KRYPTOS. For each plain-cipher pair and mode (Vigenere, Beaufort, variant Beaufort) the 24 cribs force 24 key indices; period P is consistent when every two cribs sharing a slot force the same index. Count consistent (pair, mode) cases per period on K4 and on ten shuffles of the copper with the same pool. At consistent periods up to 29, read the forced slots in the standard, KRYPTOS and plain alphabets and match against every word and every K1-K3 window of that length; a full match decrypts and submits. Bounds: complete for this pool and periods 1-52.

## Prediction

Periods 1-26 and 30-52 are consistent on K4 no more often than on the shuffles (near zero below 21); 27-29 are consistent for most pairs, as before, and no forced fragment matches a word or a K1-K3 window. Zero candidates.

## Method

1. Build the word pool and its keyword alphabets, dropping duplicates and those already in the vocabulary pool.
2. For every plain and cipher alphabet and mode, compute the 24 forced key indices.
3. For each period, check the slot-sharing pairs.
4. Repeat on ten shuffles.
5. At consistent periods up to 29, match forced fragments against words and K1-K3 windows; decrypt and submit matches.

## Result

Candidates returned: 0. Passed all gates: 0. Best crib hits among all candidates: 0/24
(no candidates).
Best loss: None (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: 0034-complete-the-key-at-surviving-periods.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| - | no candidates | | | | |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "periodic tableau, alphabets keyword-mixed from K1-K3 words and C13/C14 words",
 "alphabets": 102,
 "pairs": 10404,
 "modes": 3,
 "periods": "1-52",
 "controls": 10,
 "consistent_by_period_k4": {
  "25": 0,
  "26": 2139,
  "27": 31212,
  "28": 31212,
  "29": 31212,
  "30": 1339,
  "31": 47,
  "32": 6,
  "50": 0,
  "51": 10,
  "52": 2139
 },
 "consistent_by_period_controls_mean": {
  "25": 0.4,
  "26": 1166.2,
  "27": 31212.0,
  "28": 31212.0,
  "29": 31212.0,
  "30": 1163.2,
  "31": 38.1,
  "32": 0.5,
  "50": 0.4,
  "51": 26.1,
  "52": 1166.2
 },
 "consistent_by_period_controls_max": {
  "25": 2,
  "26": 1554,
  "27": 31212,
  "28": 31212,
  "29": 31212,
  "30": 1699,
  "31": 59,
  "32": 3,
  "50": 2,
  "51": 74,
  "52": 1554
 },
 "word_matches": 0
}
```

Notes: 102 alphabets, 10404 pairs, 3 modes, periods 1-52. Consistent cases on K4 by period (shown where K4 or a control has any): 25: 0 (controls mean 0.4, max 2), 26: 2139 (controls mean 1166.2, max 1554), 27: 31212 (controls mean 31212.0, max 31212), 28: 31212 (controls mean 31212.0, max 31212), 29: 31212 (controls mean 31212.0, max 31212), 30: 1339 (controls mean 1163.2, max 1699), 31: 47 (controls mean 38.1, max 59), 32: 6 (controls mean 0.5, max 3), 50: 0 (controls mean 0.4, max 2), 51: 10 (controls mean 26.1, max 74), 52: 2139 (controls mean 1166.2, max 1554). Word matches: 0.


