# 0152-hill-slip-variants-on-scrambled-copies: F1.6, Hill controls: the same 5,044 single-letter errors on ten scrambled copies, against K4's 257 living Hill settings with a check

**Family:** 1-keyed-periodic  
**Parent:** 0151-one-carved-letter-wrong-through-hill-and-trifid  
**Decision:** reverted  
**Run:** 2026-10-16T21:16:49+00:00, 259.8 s, status ran  
**Time by phase:** unattributed 29 s, run 260 s, record 0 s

## In plain words

One slip in the carved text lets some Hill-cipher settings fit the known letters, a few hundred times out of half a million tries. Is that more than a scrambled copy of the carved text manages? We run the identical test on ten scrambled copies.

## Walkthrough, by hand

1. Shuffle the carved letters into a new order.
2. Make every single-letter error of the shuffled copy, as for K4.
3. Run the exact Hill test on each and count living settings with a check.
4. Compare with K4's count.

## Worked example (generated)

```
the errors tried, for every place of the copper:

  wrong:   place 21 W -> each of the other 25 letters
  missing: place 21 deleted, the rest moves left, a filler at the end
  extra:   each letter inserted before place 21, the last letter pushed out

each variant through Hill 2x2-5x5 (plain, affine, every alignment, four numberings) and trifid (periods 2-15, every offset)
```

## Lineage

Inherits from 0151-one-carved-letter-wrong-through-hill-and-trifid. What changed: F1.6. 0151 found 257 (variant, Hill setting) pairs alive with at least one check on K4's 5,044 single-letter variants, almost all 5x5 plain with a single check, and no trifid cube. An exact fit only means something against the same test on scrambled copies; here every copy gets the same 5,044 variants and Hill settings.

## Hypothesis (domain expert)

As 0151 (0105's Hill decider, sizes 2-5 plain and affine, every alignment, four numberings; a variant is a carved letter changed, deleted or inserted with the message numbering fixed). Ten shuffled coppers (seed 152). Statistic fixed before the run: alive-with-checks counts per size; K4's 0151 counts against the coppers' range; K4 above every copper in a size stops the queue for replication.

## Prediction

Each copper has a similar count (a few hundred, mostly 5x5 plain with one check); K4's 257 lies inside their range in every size.

## Method

1. Ten scrambled copies.
2. Each copy's 5,044 variants through 0105's Hill settings.
3. Counts per size against K4's.

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
 "family": "Hill 2-5 on every single-letter error of ten scrambled copies (0151's test)",
 "copies_done": 10,
 "controls_total_alive_with_checks": [
  269,
  123,
  243,
  30,
  225,
  366,
  87,
  6384,
  208,
  82
 ],
 "k4_total_0151": 257,
 "controls_by_size": {
  "5x5 plain": [
   269,
   123,
   243,
   30,
   225,
   366,
   87,
   6384,
   208,
   82
  ]
 },
 "k4_above_every_copper": false,
 "k4_rank": 4,
 "seconds": 260,
 "controls": "10 shuffled coppers (seed 152), the 5,044 variants of each"
}
```

Notes: copies alive-with-checks totals [269, 123, 243, 30, 225, 366, 87, 6384, 208, 82]; K4 (0151) 257, rank 4 of 11


