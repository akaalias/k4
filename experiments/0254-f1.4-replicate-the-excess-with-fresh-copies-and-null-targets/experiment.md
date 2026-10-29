# 0254-f1.4-replicate-the-excess-with-fresh-copies-and-null-targets: F1.4: replicate 0253's excess (K4 above all 12 copies in 299 of 2,093 settings, chance 161): K4 on 400 of its settings with fresh copies, four shuffled stand-ins for K4 through the same procedure, and the 25 strongest of K4's 66 settings above all 100 against 100 fresh copies

**Family:** 1-keyed-periodic  
**Parent:** 0253-f1.4-one-alphabet-residue-decided-by-the-one-run-decider  
**Decision:** reverted  
**Run:** 2026-10-29T19:57:37+00:00, 8277.9 s, status ran  
**Time by phase:** test 10 s, run 8278 s, record 0 s

## In plain words

Yesterday's test said K4 reads more like English than its scrambled copies far more often than chance allows, but its best readings are gibberish. Before believing it, we check the test itself: we pretend four scrambled copies of K4 are the real thing and put each through exactly the same procedure. If they also 'beat their copies' too often, the test is biased, not K4 special.

## Walkthrough, by hand

1. Shuffle K4's letters to make a stand-in.
2. Find every key-stepping rule that the stand-in fits with some alphabet (the 24 known letters agree), as was done for K4.
3. Pick 400 of those rules at random. For each, search for the stand-in's most English-looking reading, then make scrambled copies of the stand-in that fit the same rule and search them one at a time until one reads as well.
4. Count the rules where the stand-in beat 12 copies.
5. A fair test gives about 1 in 13. Do the same for K4 and compare.

## Worked example (generated)

```
Replication of 0253: is the excess K4's or the test's?

  target      its fitting settings   400 drawn   above all 12 copies
  K4          2,093                   400         ?   (0253: 14.3%)
  stand-in 1  its own                 400         ?
  ... four stand-ins (shuffles of K4), the same procedure

  a fair test gives 1 in 13 (7.7%) for every target.
```

## Lineage

Inherits from 0253-f1.4-one-alphabet-residue-decided-by-the-one-run-decider. What changed: F1.4, replication (program.md: a result outside the copies' range stops the queue). 0253 found K4 above all 12 of its own copies in 299 of 2,093 settings (chance 161, binomial p 1e-24) and above all 100 in 66 (chance 21), with junk readings and the excess spread over the whole cell (K4 beat its first copy in 61% of settings, not 50%). Before reading it as K4's, test the procedure: (A) K4 on 400 of its fitting settings drawn at random, fresh seeds and copies; (B) four shuffles of K4 stand in for K4: each gets its own fitting settings (the same exact decider over the same schedule list), 400 drawn at random, and the identical decision; (C) the 25 strongest of K4's 66 settings above all 100 (all that 0253's record lists), each against 100 fresh copies. The selection of settings by the target, and the copies being fitting shuffles, are the same in A and B, so B is the procedure's own null.

## Hypothesis (domain expert)

F1.4 (a keyed table with a hand key schedule, one free alphabet on both sides, Beaufort or added; C20(d), C27(c)). 0253 decided each of K4's 2,093 fitting settings with D1's one-run decider (0140's tempering generalised to slot maps, 0252) against fitting shuffles climbed one at a time. The per-setting null (1/13 above all 12) assumes K4 and a fitting shuffle are exchangeable once both fit. They may not be: the setting list was filtered by K4 (a setting that K4 fits may fit it more loosely than a random fitting shuffle), and a fitting shuffle may keep fewer free alphabet letters. If the stand-ins (B) show the same excess as K4 (A), the excess belongs to the procedure and 0253's verdict must be read against B's rate, not 1/13; if B sits at 1/13 and A replicates, the excess is K4's and is chased (C says whether particular settings carry it).

## Prediction

B shows an excess like A's (stand-ins above all 12 copies in about 12-15% of their settings, against 7.7% for a fair test), so the excess belongs to the procedure; A replicates 0253's rate (about 14%); C: K4 above all 100 fresh copies in a few of the 25, well under 25 but above the 1% a fair test gives. Zero candidates.

## Method

1. Targets: K4 and four shuffles of K4 (seed 2541). For each target, every setting of 0252's list (0128's schedules at slot counts 2-31, back and forth, both forms) is decided exactly; the target's fitting settings are its cell.
2. A and B: 400 settings drawn at random from each target's cell (seed per target); per setting 0253's decide(): one tempering run on the target, then fitting shuffles of the target climbed one at a time, stop at the first at or above, at most 12 (no escalation). Count settings where the target is above all 12.
3. C: the 25 settings 0253's record lists (the strongest of the 66 where K4 was above all 100), each with 100 fresh fitting copies (decide with escalation, new seeds).
4. Verdict, pre-registered: the procedure's null rate is the stand-ins' pooled rate p_B; K4's A rate against p_B by a two-proportion test; if p_B is within 2 points of K4's, the excess is the procedure's.

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
 "item": "F1.4 replication of 0253's excess",
 "decider": "0253's decide(), imported unchanged: one tempering run on the target, fitting shuffles climbed one at a time, at most 12 (A, B), escalated to 100 (C)",
 "targets": {
  "k4": {
   "cell_size": 2093,
   "sampled": 400,
   "above_all_12": 53,
   "rate": 0.1325,
   "beat_first_copy": 231,
   "beat_first_rate": 0.5775,
   "mean_copies_climbed": 3.98
  },
  "standin0": {
   "cell_size": 3246,
   "sampled": 400,
   "above_all_12": 41,
   "rate": 0.1025,
   "beat_first_copy": 205,
   "beat_first_rate": 0.5125,
   "mean_copies_climbed": 3.48
  },
  "standin1": {
   "cell_size": 3696,
   "sampled": 400,
   "above_all_12": 29,
   "rate": 0.0725,
   "beat_first_copy": 170,
   "beat_first_rate": 0.425,
   "mean_copies_climbed": 2.75
  },
  "standin2": {
   "cell_size": 2997,
   "sampled": 400,
   "above_all_12": 6,
   "rate": 0.015,
   "beat_first_copy": 136,
   "beat_first_rate": 0.34,
   "mean_copies_climbed": 2.0
  },
  "standin3": {
   "cell_size": 3917,
   "sampled": 400,
   "above_all_12": 70,
   "rate": 0.175,
   "beat_first_copy": 281,
   "beat_first_rate": 0.7025,
   "mean_copies_climbed": 4.6
  }
 },
 "fair_rate_12": 0.0769,
 "standins_pooled": {
  "sampled": 1600,
  "above_all_12": 146,
  "rate": 0.0912
 },
 "k4_rate": 0.1325,
 "two_proportion_z_k4_vs_standins": 2.47,
 "verdict": "unclear",
 "C_top_settings": {
  "count": 25,
  "above_all_100_fresh": 9,
  "fair_expected": 0.25,
  "each": [
   {
    "setting": "B skip m=13 phi=10 n=22",
    "form": "V",
    "above": 100,
    "score": -4.94684
   },
   {
    "setting": "B skip m=12 phi=6 n=22",
    "form": "V",
    "above": 100,
    "score": -5.00267
   },
   {
    "setting": "B skip m=30 phi=29 n=21",
    "form": "V",
    "above": 100,
    "score": -4.99819
   },
   {
    "setting": "B skip m=13 phi=9 n=22",
    "form": "V",
    "above": 100,
    "score": -4.96796
   },
   {
    "setting": "B skip m=14 phi=12 n=22",
    "form": "V",
    "above": 100,
    "score": -4.99032
   },
   {
    "setting": "B skip m=22 phi=13 n=21",
    "form": "V",
    "above": 100,
    "score": -5.13838
   },
   {
    "setting": "B skip m=13 phi=8 n=22",
    "form": "V",
    "above": 100,
    "score": -5.0119
   },
   {
    "setting": "B skip m=23 phi=15 n=21",
    "form": "V",
    "above": 100,
    "score": -5.0779
   },
   {
    "setting": "B skip m=29 phi=28 n=21",
    "form": "V",
    "above": 100,
    "score": -5.08657
   },
   {
    "setting": "B skip m=8 phi=3 n=23",
    "form": "V",
    "above": 76,
    "score": -4.97785
   },
   {
    "setting": "B skip m=14 phi=13 n=22",
    "form": "V",
    "above": 59,
    "score": -5.01746
   },
   {
    "setting": "B skip m=26 phi=23 n=21",
    "form": "V",
    "above": 59,
    "score": -5.05232
   },
   {
    "setting": "B skip m=12 phi=5 n=22",
    "form": "V",
    "above": 57,
    "score": -5.07215
   },
   {
    "setting": "B skip m=28 phi=27 n=21",
    "form": "V",
    "above": 47,
    "score": -5.05354
   },
   {
    "setting": "B skip m=27 phi=23 n=21",
    "form": "V",
    "above": 36,
    "score": -5.16435
   },
   {
    "setting": "B skip m=8 phi=2 n=23",
    "form": "V",
    "above": 20,
    "score": -4.98344
   },
   {
    "setting": "B skip m=27 phi=24 n=21",
    "form": "V",
    "above": 17,
    "score": -5.10536
   },
   {
    "setting": "B skip m=26 phi=3 n=21",
    "form": "V",
    "above": 16,
    "score": -5.18671
   },
   {
    "setting": "B skip m=26 phi=22 n=21",
    "form": "V",
    "above": 15,
    "score": -5.07151
   },
   {
    "setting": "B skip m=27 phi=25 n=21",
    "form": "V",
    "above": 7,
    "score": -5.1335
   },
   {
    "setting": "B skip m=25 phi=1 n=21",
    "form": "V",
    "above": 7,
    "score": -5.23552
   },
   {
    "setting": "B skip m=29 phi=5 n=21",
    "form": "V",
    "above": 3,
    "score": -5.2066
   },
   {
    "setting": "D back and forth n=24 ends=once phi=13",
    "form": "B",
    "above": 2,
    "score": -4.97627
   },
   {
    "setting": "B skip m=24 phi=23 n=21",
    "form": "B",
    "above": 1,
    "score": -5.23469
   },
   {
    "setting": "B skip m=27 phi=5 n=21",
    "form": "V",
    "above": 1,
    "score": -5.21078
   }
  ]
 },
 "core_seconds": 140831,
 "compute_seconds": 2569,
 "exhaustive": false,
 "modal_cost_estimate": "5 x 400 settings x about 5 climbs + 25 x about 100 climbs, about 17 s each: about 210,000 core-seconds, about $3.5 of Modal credit (credit left about $17 after the margin)"
}
```

Notes: 0253 replication: K4 above all 12 in 53/400 (0.133); stand-ins 146/1600 (0.091); fair 0.077; z 2.47; verdict: unclear. C: 9 of 25 top settings above all 100 fresh copies.


