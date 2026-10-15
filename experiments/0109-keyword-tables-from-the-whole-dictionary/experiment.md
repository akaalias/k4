# 0109-keyword-tables-from-the-whole-dictionary: Tables built from any English word, not just the puzzle's, with a repeating key of length 1 to 26

**Family:** 1-keyed-periodic  
**Parent:** 0053-periodic-tableau-k1-k3-word-alphabets  
**Decision:** reverted  
**Run:** 2026-10-15T20:24:19+00:00, 72.8 s, status ran  
**Time by phase:** unattributed 195 s, run 73 s, record 0 s

## In plain words

The table on Kryptos starts each alphabet with the word KRYPTOS and then the other letters in order. Any word can make such a table. Experiments 10 and 53 tried the puzzle's own words. Here we try every word in an English dictionary, about 233,000 of them, with a short repeating secret word on top, and ask whether any table lets the 24 known letters fit.

## Walkthrough, by hand

1. Take a word, say SHADOW: the alphabet is SHADOWBCEFGIJKLMNPQRTUVXYZ.
2. Use it for both the plain and cipher alphabets, Vigenere.
3. Place 22: E is letter 8 of the new alphabet and F letter 9, so the key value there is 1.
4. With a key of length p, places 22 and 22 + p (if known) must need the same key value.
5. Repeat for every word, side, key length 1-26 and rule, and on scrambled coppers.

## Worked example (generated)

```
keyword SHADOW: alphabet SHADOWBCEFGIJKLMNPQRTUVXYZ; both sides, Vigenere

place  known  carved  key value
   22      E       F          1
   23      A       L         12
   24      S       R         19
   25      T       V          2
   26      N       Q          2
   27      O       Q         14
   28      R       P         24
   29      T       R         25
   30      H       N         15
   31      E       G          2
   32      A       K         11
   33      S       S          0
   34      T       S          6
   64      B       N         10
   65      E       Y         16
   66      R       P         24
   67      L       V          8
   68      I       T          9
   69      N       T          4
   70      C       M          8
   71      L       Z         11
   72      O       F          5
   73      C       P         10
   74      K       K          0
```

## Lineage

Inherits from 0053-periodic-tableau-k1-k3-word-alphabets. What changed: 0010 and 0053 rebuilt the tableau from the puzzle's own 61 words and the K1-K3 and 2025-letter words, the way KRYPTOS builds the carved one. Here the keyword is any of the 233,000 words of four letters or more in the project dictionary, used for the plain alphabet, the cipher alphabet or both (with the standard or KRYPTOS alphabet on the other side), with a repeating key of length 1-26 and no move.

## Hypothesis (domain expert)

Sanborn: a 'slightly different tableau' (C11a); K1-K2 use a keyword-mixed Quagmire III (KRYPTOS). 0005 closed periods 1-26 for the carved and standard alphabets, 0010 and 0053 for puzzle words. Alphabet W = keyword's distinct letters then the rest in order. Classes (consistency depends only on the plain and cipher alphabets and Beaufort versus not, 0006): (W, W), (W, STD), (STD, W), (W, KRY), (KRY, W), each Beaufort or not: 10 per word. Exact slot agreement at every period 1-26. Distinct alphabets only (words giving the same W counted once). Ten shuffled coppers. C8, C11a.

## Prediction

No word gives a consistent period below 20; the number of (alphabet, class) pairs consistent at each period 21-26 lies inside the ten coppers' range. Zero candidates.

## Method

1. Build the distinct keyword alphabets from the dictionary.
2. For each alphabet and class, compute the key value forced at each known letter.
3. Test slot agreement at periods 1-26.
4. Count consistent pairs per period on K4 and ten shuffled coppers.
5. List K4's settings below period 20 and decrypt them.

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
 "family": "keyword-mixed tableau from the whole dictionary, periodic key 1-26, no move",
 "words_4_plus": 232989,
 "distinct_alphabets": 208062,
 "settings": 2080620,
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
  0,
  68051
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
  0,
  41874
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
  170,
  129809
 ],
 "k4_smallest_live_period": 26,
 "controls_smallest_live_period": [
  26,
  25,
  25,
  25,
  25,
  25,
  25,
  25,
  25,
  25
 ],
 "periods_outside_control_range": [],
 "k4_live_below_20": [],
 "n_k4_live_below_20": 0,
 "controls": "10 shuffled coppers (seed 109), identical search"
}
```

Notes: 208,062 distinct alphabets from 232,989 words x 10 classes = 2,080,620 settings, periods 1-26. Smallest live period: K4 26, controls [26, 25, 25, 25, 25, 25, 25, 25, 25, 25]. K4 live below 20: 0. Outside the control range: [].


