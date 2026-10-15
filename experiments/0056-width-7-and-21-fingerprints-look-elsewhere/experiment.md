# 0056-width-7-and-21-fingerprints-look-elsewhere: Are the copper's two odd patterns odd at all once every width is counted?

**Family:** 7-construction-simulation  
**Parent:** 0027-simulator-round-two-width-21-hunt  
**Decision:** reverted  
**Run:** 2026-10-15T12:16:21+00:00, 4.3 s, status ran  
**Time by phase:** design 0 s, implement 9 s, test 0 s, run 4 s, record 0 s

## In plain words

If you write the copper in rows of 7 letters, five of its six doubled letters line up in one column, and in rows of 21 the same letter pairs stack up more than usual. That looks like a clue to how it was made. But we found those widths by trying many widths, and if you try enough widths something always lines up. So we scramble the copper ten thousand times, try every width from 2 to 48 on each scramble, and see how often a scramble looks at least this odd at its best width.

## Walkthrough, by hand

1. Find the doubled letters in the copper: BB at places 19-20, QQ at 26-27, SS at 33-34, SS at 43-44, ZZ at 47-48 and TT at 68-69.
2. Write the copper in rows of 7: the first letter of each doublet sits in column 19 mod 7 = 5, 26 mod 7 = 5, 33 mod 7 = 5, 43 mod 7 = 1, 47 mod 7 = 5, 68 mod 7 = 5.
3. Count: column 5 holds five of the six doublets.
4. Shuffle the 97 letters, find the doubled letters again, and count the fullest column at every width from 2 to 48.
5. Note how odd the fullest column is at its best width.
6. Do it ten thousand times and see where the copper falls.

## Worked example (generated)

```
doublets (place of first letter, 1-based):
  BB at 19-20: column (0-based index mod 7) 4
  QQ at 26-27: column (0-based index mod 7) 4
  SS at 33-34: column (0-based index mod 7) 4
  SS at 43-44: column (0-based index mod 7) 0
  ZZ at 47-48: column (0-based index mod 7) 4
  TT at 68-69: column (0-based index mod 7) 4
```

## Lineage

Inherits from 0027-simulator-round-two-width-21-hunt. What changed: Experiments 18 and 27 found two patterns in K4 that no construction reproduced well: five of its six doubled letters fall in one column when the text is written in rows of 7, and pairs of letters 21 places apart repeat eleven times. Both were found by looking at many widths. This asks how often a scrambled copper shows a pattern that strong at some width, which is the fair comparison.

## Hypothesis (domain expert)

The width-7 doublet column (5 of 6 doublets at one position mod 7) and the width-21 vertical repeats (11 repeated pairs (c[i], c[i+21])) were selected after scanning widths, so their nominal p-values (0.01-0.1 in 0018) overstate them. For every width w in 2-48 compute both statistics on K4 and on 10,000 letter-preserving shuffles; turn each into a per-width tail probability from the shuffle distribution; take the smallest tail probability over widths as the scan statistic; and compare K4's scan statistic with the shuffles' (the look-elsewhere correction). Also condition the doublet statistic on shuffles with exactly six doublets, since K4 has six. If K4's corrected p-values exceed 0.05, family 7's two unexplained features are not evidence for any construction. Bounds: widths 2-48, 10,000 controls.

## Prediction

After the correction neither pattern is unusual: K4's scan p-value is above 0.05 for both, so the two features need no explanation. Zero candidates.

## Method

1. For widths 2-48 compute, on K4, the largest number of doublets sharing a column and the number of repeated vertical pairs.
2. Do the same on 10,000 shuffles.
3. Per width, the tail probability of each value among the shuffles.
4. Per text, the smallest tail probability over widths.
5. K4's rank among the shuffles is the corrected p-value; repeat with six-doublet shuffles only.

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
 "family": "look-elsewhere test of the width fingerprints",
 "widths": "2-48",
 "controls": 10000,
 "k4_doublets": 6,
 "k4_col7": 5,
 "k4_rep21": 11,
 "nominal_p_col7": 0.0005,
 "nominal_p_rep21": 0.0004,
 "k4_best_width_col": 7,
 "k4_best_width_rep": 21,
 "corrected_p_doublet_column": 0.0049,
 "corrected_p_doublet_column_six_doublet_shuffles": 0.0178,
 "six_doublet_shuffles": 729,
 "corrected_p_vertical_repeats": 0.0099
}
```

Notes: 10000 shuffles, widths 2-48. Doublet column: nominal p at width 7 0.0005, corrected over widths 0.0049 (0.0178 among the 729 shuffles with 6 doublets). Vertical repeats: nominal p at width 21 0.0004, corrected 0.0099.


