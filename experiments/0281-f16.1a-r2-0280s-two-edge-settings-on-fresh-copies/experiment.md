# 0281-f16.1a-r2-0280s-two-edge-settings-on-fresh-copies: F16.1a-r2: 0280's two settings where K4 beat 100 fitting copies (V10 with slips at 73-74, B10 with a slip at 69), each on 1,000 fresh fitting copies with one fresh climb for K4; flag below 0.001

**Family:** 16-simple-hand-methods  
**Parent:** 0280-f16.1a-r-the-cells-only-east-closed-by-the-one-run-decider  
**Decision:** reverted  
**Run:** 2026-11-17T17:01:17+00:00, 998.4 s, status ran  
**Time by phase:** test 18 s, run 998 s, record 0 s

## In plain words

In experiment 280 the carving's best message beat 100 scrambled copies at two settings, which by luck happens about once in ten runs of that size. Here each of the two gets a new search and 1,000 new copies.

## Walkthrough, by hand

1. Fix the setting: key length 10, the added form, the letters at 73 and 74 treated as slips.
2. Search once for the most English message K4 gives under it.
3. Make 1,000 scrambles of K4 that fit the same setting and search each once.
4. Count the scrambles whose message reads at least as well as K4's.

## Worked example (generated)

```
F16.1a-r2: two settings from 0280, one fresh search for K4 each, 1,000 fresh fitting copies each.

  V10, slips at 73 and 74: 0280's K4 reading CDKLDCBCBETHBTROYGINFOLLK... beat 100 copies
  B10, slip at 69:         0280's K4 reading XTWAILFLONYSDTOOIMIKCOLAN... beat 100 copies
  flag only if no fresh copy reads as well (p < 0.001, for the 49 settings 0280 looked at)
```

## Lineage

Inherits from 0280-f16.1a-r-the-cells-only-east-closed-by-the-one-run-decider. What changed: F16.1a-r2 (issue #123): replication of 0280's two edge settings. 0280's attack.py imported unchanged for its witness and climb; K4 climbed once with a new seed, then 1,000 shuffles of K4 that fit the same setting on the same known letters, each climbed once with its own seed (no stopping rule).

## Hypothesis (domain expert)

As 0280 (F1.1/F1.6 without EAST, Quagmire III with a free alphabet, C27(c)); a result outside its copies is replicated against fresh controls before anything else (program.md). Pre-registered: per setting, p = (1 + fresh copies scoring at or above K4's fresh climb) / 1,001; a flag needs p below 0.05/49 = 0.001 (49 settings were looked at in 0280), so at most 0 copies at or above. Readings in 0280 were not English, so the expectation is chance.

## Prediction

Both settings p above 0.001 (most likely above 0.05); K4's fresh reading not English. No candidates.

## Method

1. The two settings from 0280's record, with their known letters (the 20 official ones less the slips).
2. K4: one climb, seed 16120 + setting.
3. 1,000 fitting shuffles per setting (seeds 16130+), one climb each.
4. p per setting; flag below 0.001.

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
 "item": "F16.1a-r2",
 "settings": {
  "V10 [73, 74]": {
   "k4_score": -5.59547,
   "k4_reading": "MUKEMMVMVPPCBTRASGISHOLEDNORTHEASTRIXISGFRSTOSALGOINKCMWSTGJOOBBERLINCLOPATEHSBRINCIVEDPETTFEASTY",
   "copies": 1000,
   "at_or_above": 12,
   "p": 0.01299,
   "flag": false,
   "copies_max": -5.47406,
   "copies_median": -5.89616,
   "lost_copies": 0
  },
  "B10 [69]": {
   "k4_score": -5.8559,
   "k4_reading": "JVIALLPLINBNMTRORVSTCODATNORTHEASTRIKIKDOHSTYSFBYUNIIILYRCYOTOMBERLIRCLOCKSMBSVENIPMCMWEMASGEKICI",
   "copies": 1000,
   "at_or_above": 35,
   "p": 0.03596,
   "flag": false,
   "copies_max": -5.60502,
   "copies_median": -6.17202,
   "lost_copies": 0
  }
 },
 "flag_line": 0.001,
 "flagged": [],
 "decider": "0280's witness and climb (0252's generalised 0140 tempering), one climb per text",
 "exhaustive": true,
 "aws_cost_estimate_dollars": 0.2
}
```

Notes: V10 [73, 74]: K4 -5.59547, 12 of 1000 fresh copies at or above, p 0.01299; B10 [69]: K4 -5.8559, 35 of 1000 fresh copies at or above, p 0.03596


