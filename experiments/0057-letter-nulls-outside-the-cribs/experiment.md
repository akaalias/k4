# 0057-letter-nulls-outside-the-cribs: Filler letters chosen by letter: drop every copy of one or two letters, then the repeating secret word

**Family:** 2-masked-then-keyed  
**Parent:** 0023-masks-reversal-and-nulls-then-tableau  
**Decision:** reverted  
**Run:** 2026-10-15T12:18:20+00:00, 1.1 s, status ran  
**Time by phase:** design 0 s, implement 0 s, test 0 s, run 1 s, record 0 s

## In plain words

A message can be padded with filler letters that the reader is told to ignore, for example every Q. Experiment 23 tried filler at regular spacing. Here the filler is every copy of one letter, or of two letters, outside the known stretches. Striking them out moves the known letters to new places, and we ask again whether a repeating secret word of any length could fit them. Random strike-outs of the same size are the control.

## Walkthrough, by hand

1. Take Q as the filler.
2. Q appears at places 26, 27, 39 and 42; 26 and 27 lie inside EASTNORTHEAST, so only 39 and 42 are struck.
3. No known letter lies before place 39, so EASTNORTHEAST stays at 22-34; BERLINCLOCK, after two strike-outs, now sits at 62-72.
4. With a secret word of 7 letters, place 22 (E under F) and place 29 (T under R) share a slot and must force the same key letter on the sculpture's table.
5. They do not, so 7 is dead for this filler.
6. Repeat for every length, table and filler.

## Worked example (generated)

```
Q at [26, 27, 39, 42]; struck outside the crib ranges: [39, 42]; BERLINCLOCK moves from 64-74 to 62-72
```

## Lineage

Inherits from 0023-masks-reversal-and-nulls-then-tableau. What changed: Experiment 23 removed filler letters at regular spacings. Here the filler is chosen by letter instead: every copy of one letter, or of a pair of letters, is struck out wherever it falls outside the two known stretches, the known letters move to their new places, and the repeating-secret-word test is run at every length.

## Hypothesis (domain expert)

C4 masking and C18 ('a bit of stego', 98 characters) allow nulls; a null letter that is a real letter chosen by rule is listed open in families.md. Model: every occurrence of a null letter (each of 26) or of a null pair (325) is removed from the carved text outside the crib ranges 22-34 and 64-74 (a null inside a range would contradict Sanborn's positions), shifting the cribs' plaintext indices by the nulls before them; the rest is a periodic tableau text. Test periods 1-52 under the plain and cipher alphabets standard and KRYPTOS and three modes (the key alphabet drops out of consistency, 0006), exactly. Control: for each mask, ten masks removing the same number of letters at random positions outside the ranges. Bounds: complete for 351 letter masks and periods 1-52.

## Prediction

No letter mask makes any period below 26 consistent more often than random strike-outs do; the smallest consistent period stays in the high twenties. Zero candidates.

## Method

1. For each letter and pair of letters, strike every copy outside places 22-34 and 64-74.
2. Shift the known places by the strike-outs before them.
3. For each period 1-52, alphabet pair and mode, check that known letters sharing a key slot force the same key letter.
4. Record the smallest consistent period.
5. Repeat with random strike-outs of the same count.

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
 "family": "null letters (every copy of one or two letters outside the crib ranges), then periodic tableau",
 "masks": 351,
 "controls_per_mask": 10,
 "periods": "1-52",
 "alphabet_pairs": 4,
 "modes": 3,
 "smallest_period_histogram": {
  "24": 18,
  "25": 117,
  "26": 168,
  "27": 45,
  "47": 3
 },
 "control_histogram_per_10": {
  "24": 17.1,
  "25": 104.6,
  "26": 174.3,
  "27": 48.4,
  "45": 0.4,
  "46": 1.0,
  "47": 5.2
 },
 "masks_below_26": [
  {
   "letters": "AS",
   "struck": 8,
   "period": 24
  },
  {
   "letters": "AT",
   "struck": 8,
   "period": 24
  },
  {
   "letters": "AW",
   "struck": 9,
   "period": 24
  },
  {
   "letters": "IS",
   "struck": 8,
   "period": 24
  },
  {
   "letters": "IT",
   "struck": 8,
   "period": 24
  },
  {
   "letters": "IW",
   "struck": 9,
   "period": 24
  },
  {
   "letters": "JS",
   "struck": 7,
   "period": 24
  },
  {
   "letters": "JT",
   "struck": 7,
   "period": 24
  },
  {
   "letters": "JW",
   "struck": 8,
   "period": 24
  },
  {
   "letters": "KS",
   "struck": 10,
   "period": 24
  },
  {
   "letters": "KT",
   "struck": 10,
   "period": 24
  },
  {
   "letters": "KW",
   "struck": 11,
   "period": 24
  },
  {
   "letters": "QS",
   "struck": 6,
   "period": 24
  },
  {
   "letters": "QT",
   "struck": 6,
   "period": 24
  },
  {
   "letters": "QW",
   "struck": 7,
   "period": 24
  },
  {
   "letters": "SZ",
   "struck": 7,
   "period": 24
  },
  {
   "letters": "TZ",
   "struck": 7,
   "period": 24
  },
  {
   "letters": "WZ",
   "struck": 8,
   "period": 24
  },
  {
   "letters": "S",
   "struck": 4,
   "period": 25
  },
  {
   "letters": "T",
   "struck": 4,
   "period": 25
  }
 ]
}
```

Notes: 351 letter masks; smallest consistent period per mask: {24: 18, 25: 117, 26: 168, 27: 45, 47: 3}; random strike-outs of the same size (per 10): {24: 17.1, 25: 104.6, 26: 174.3, 27: 48.4, 45: 0.4, 46: 1.0, 47: 5.2}. Masks below 26: 135.


