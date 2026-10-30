# 0255-f1.4-k4-among-40-stand-ins-through-the-same-procedure: F1.4: K4's rate of beating its copies ranked among 40 shuffled stand-ins, each on 80 of its own fitting key schedules through 0253's procedure

**Family:** 1-keyed-periodic  
**Parent:** 0254-f1.4-replicate-the-excess-with-fresh-copies-and-null-targets  
**Decision:** reverted  
**Run:** 2026-10-29T22:18:25+00:00, 8250.5 s, status ran  
**Time by phase:** test 10 s, run 8250 s, record 0 s

## In plain words

The test said K4 beats its scrambled copies more often than chance, but four scrambled copies of K4 put through the same test ranged from far below to above K4. Here 40 of them go through it beside K4, so we can see where K4 falls among texts that certainly hide no message.

## Walkthrough, by hand

1. Shuffle K4's letters 40 times to make 40 stand-ins.
2. For each, find the key-stepping rules it fits with some alphabet, and pick 80 at random.
3. For each rule, search for the stand-in's most English-looking reading, then search scrambled copies of it that fit the same rule, one at a time, until one reads as well (at most 12).
4. Each stand-in's share of rules where it beat all 12 is its rate. Do the same for K4.
5. Where does K4's rate fall among the 40?

## Worked example (generated)

```
K4 among 40 stand-ins: where does its rate fall?

  target       fitting schedules   80 drawn   above all 12 copies
  K4           2,093               80         ?   (0253: 14.3%, 0254: 13.3%)
  stand-in 1   its own             80         ?
  ... 40 stand-ins (shuffles of K4), the same procedure

  K4's rank among the 41 texts is the verdict.
```

## Lineage

Inherits from 0254-f1.4-replicate-the-excess-with-fresh-copies-and-null-targets. What changed: F1.4, second replication of 0253's excess. 0254 found K4 above all 12 copies in 13.3% of its schedules (0253: 14.3%), but four shuffled stand-ins through the identical procedure gave 10.2%, 7.2%, 1.5% and 17.5%: the rate belongs to the text and is shared across its schedules, so the per-schedule null (1 in 13) is wrong and 0253's binomial p meaningless. The pre-registered verdict was 'unclear' (pooled stand-ins 9.1%, z 2.47). Here the procedure's null is measured as a distribution over texts: 40 stand-ins and K4, 80 fitting schedules each, fresh seeds.

## Hypothesis (domain expert)

F1.4 (one free alphabet, hand key schedules; C20(d), C27(c)), decided by 0253's decide() (one tempering run on the target, fitting shuffles climbed one at a time, at most 12). The quantity is each text's rate of beating all 12 copies over its own fitting schedules. If K4 carries a message under some schedule, its rate is lifted only near that schedule; if the rate reflects how a text's letters sit at the 24 known places (shared by all schedules), stand-ins vary as much as K4. K4's rank among 41 texts gives p to 1/41.

## Prediction

K4's rate inside the stand-ins' spread: rank between 5th and 30th of 41 (one-sided p above 0.1); the stand-ins' rates spread with a standard deviation of about 5 points around 9%. Zero candidates.

## Method

1. Targets: K4 and 40 shuffles of K4 (seed 2551). Each target's cell: every schedule of 0252's list it fits exactly.
2. 80 schedules drawn at random from each cell; per schedule 0253's decide() without escalation.
3. Each target's rate (above all 12) and its rate of beating the first copy; K4's rank among the 41 on each, one-sided p = (1 + stand-ins at or above K4) / 41. A lead only if p is at most 1/41 on the rate.

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
 "item": "F1.4, K4 among 40 stand-ins (second replication of 0253's excess)",
 "decider": "0253's decide(), imported unchanged: one tempering run on the target, fitting shuffles climbed one at a time, at most 12",
 "targets": {
  "k4": {
   "cell_size": 2093,
   "sampled": 80,
   "above_all_12": 8,
   "rate": 0.1,
   "beat_first_copy": 52,
   "beat_first_rate": 0.65,
   "mean_copies_climbed": 4.06
  },
  "standin0": {
   "cell_size": 4586,
   "sampled": 80,
   "above_all_12": 7,
   "rate": 0.0875,
   "beat_first_copy": 43,
   "beat_first_rate": 0.5375,
   "mean_copies_climbed": 3.33
  },
  "standin1": {
   "cell_size": 4488,
   "sampled": 80,
   "above_all_12": 18,
   "rate": 0.225,
   "beat_first_copy": 56,
   "beat_first_rate": 0.7,
   "mean_copies_climbed": 5.53
  },
  "standin2": {
   "cell_size": 2240,
   "sampled": 80,
   "above_all_12": 2,
   "rate": 0.025,
   "beat_first_copy": 42,
   "beat_first_rate": 0.525,
   "mean_copies_climbed": 3.0
  },
  "standin3": {
   "cell_size": 2810,
   "sampled": 80,
   "above_all_12": 12,
   "rate": 0.15,
   "beat_first_copy": 42,
   "beat_first_rate": 0.525,
   "mean_copies_climbed": 3.55
  },
  "standin4": {
   "cell_size": 2079,
   "sampled": 80,
   "above_all_12": 7,
   "rate": 0.0875,
   "beat_first_copy": 43,
   "beat_first_rate": 0.5375,
   "mean_copies_climbed": 3.31
  },
  "standin5": {
   "cell_size": 7214,
   "sampled": 80,
   "above_all_12": 0,
   "rate": 0.0,
   "beat_first_copy": 30,
   "beat_first_rate": 0.375,
   "mean_copies_climbed": 1.95
  },
  "standin6": {
   "cell_size": 1994,
   "sampled": 80,
   "above_all_12": 12,
   "rate": 0.15,
   "beat_first_copy": 40,
   "beat_first_rate": 0.5,
   "mean_copies_climbed": 3.55
  },
  "standin7": {
   "cell_size": 4140,
   "sampled": 80,
   "above_all_12": 3,
   "rate": 0.0375,
   "beat_first_copy": 43,
   "beat_first_rate": 0.5375,
   "mean_copies_climbed": 3.02
  },
  "standin8": {
   "cell_size": 3933,
   "sampled": 80,
   "above_all_12": 8,
   "rate": 0.1,
   "beat_first_copy": 37,
   "beat_first_rate": 0.4625,
   "mean_copies_climbed": 3.25
  },
  "standin9": {
   "cell_size": 3583,
   "sampled": 80,
   "above_all_12": 2,
   "rate": 0.025,
   "beat_first_copy": 47,
   "beat_first_rate": 0.5875,
   "mean_copies_climbed": 2.92
  },
  "standin10": {
   "cell_size": 1784,
   "sampled": 80,
   "above_all_12": 19,
   "rate": 0.2375,
   "beat_first_copy": 49,
   "beat_first_rate": 0.6125,
   "mean_copies_climbed": 4.83
  },
  "standin11": {
   "cell_size": 2767,
   "sampled": 80,
   "above_all_12": 7,
   "rate": 0.0875,
   "beat_first_copy": 48,
   "beat_first_rate": 0.6,
   "mean_copies_climbed": 3.24
  },
  "standin12": {
   "cell_size": 3496,
   "sampled": 80,
   "above_all_12": 5,
   "rate": 0.0625,
   "beat_first_copy": 41,
   "beat_first_rate": 0.5125,
   "mean_copies_climbed": 3.09
  },
  "standin13": {
   "cell_size": 2001,
   "sampled": 80,
   "above_all_12": 5,
   "rate": 0.0625,
   "beat_first_copy": 34,
   "beat_first_rate": 0.425,
   "mean_copies_climbed": 2.59
  },
  "standin14": {
   "cell_size": 4788,
   "sampled": 80,
   "above_all_12": 5,
   "rate": 0.0625,
   "beat_first_copy": 46,
   "beat_first_rate": 0.575,
   "mean_copies_climbed": 3.38
  },
  "standin15": {
   "cell_size": 1889,
   "sampled": 80,
   "above_all_12": 4,
   "rate": 0.05,
   "beat_first_copy": 47,
   "beat_first_rate": 0.5875,
   "mean_copies_climbed": 2.99
  },
  "standin16": {
   "cell_size": 3847,
   "sampled": 80,
   "above_all_12": 13,
   "rate": 0.1625,
   "beat_first_copy": 60,
   "beat_first_rate": 0.75,
   "mean_copies_climbed": 4.94
  },
  "standin17": {
   "cell_size": 2416,
   "sampled": 80,
   "above_all_12": 11,
   "rate": 0.1375,
   "beat_first_copy": 45,
   "beat_first_rate": 0.5625,
   "mean_copies_climbed": 4.24
  },
  "standin18": {
   "cell_size": 3776,
   "sampled": 80,
   "above_all_12": 6,
   "rate": 0.075,
   "beat_first_copy": 39,
   "beat_first_rate": 0.4875,
   "mean_copies_climbed": 2.83
  },
  "standin19": {
   "cell_size": 5570,
   "sampled": 80,
   "above_all_12": 9,
   "rate": 0.1125,
   "beat_first_copy": 42,
   "beat_first_rate": 0.525,
   "mean_copies_climbed": 3.41
  },
  "standin20": {
   "cell_size": 2139,
   "sampled": 80,
   "above_all_12": 23,
   "rate": 0.2875,
   "beat_first_copy": 57,
   "beat_first_rate": 0.7125,
   "mean_copies_climbed": 5.69
  },
  "standin21": {
   "cell_size": 3760,
   "sampled": 80,
   "above_all_12": 6,
   "rate": 0.075,
   "beat_first_copy": 41,
   "beat_first_rate": 0.5125,
   "mean_copies_climbed": 3.15
  },
  "standin22": {
   "cell_size": 2382,
   "sampled": 80,
   "above_all_12": 17,
   "rate": 0.2125,
   "beat_first_copy": 54,
   "beat_first_rate": 0.675,
   "mean_copies_climbed": 4.74
  },
  "standin23": {
   "cell_size": 2299,
   "sampled": 80,
   "above_all_12": 13,
   "rate": 0.1625,
   "beat_first_copy": 55,
   "beat_first_rate": 0.6875,
   "mean_copies_climbed": 4.17
  },
  "standin24": {
   "cell_size": 4339,
   "sampled": 80,
   "above_all_12": 10,
   "rate": 0.125,
   "beat_first_copy": 47,
   "beat_first_rate": 0.5875,
   "mean_copies_climbed": 3.81
  },
  "standin25": {
   "cell_size": 4794,
   "sampled": 80,
   "above_all_12": 5,
   "rate": 0.0625,
   "beat_first_copy": 39,
   "beat_first_rate": 0.4875,
   "mean_copies_climbed": 2.75
  },
  "standin26": {
   "cell_size": 2830,
   "sampled": 80,
   "above_all_12": 12,
   "rate": 0.15,
   "beat_first_copy": 51,
   "beat_first_rate": 0.6375,
   "mean_copies_climbed": 4.41
  },
  "standin27": {
   "cell_size": 4660,
   "sampled": 80,
   "above_all_12": 9,
   "rate": 0.1125,
   "beat_first_copy": 51,
   "beat_first_rate": 0.6375,
   "mean_copies_climbed": 4.0
  },
  "standin28": {
   "cell_size": 4039,
   "sampled": 80,
   "above_all_12": 5,
   "rate": 0.0625,
   "beat_first_copy": 45,
   "beat_first_rate": 0.5625,
   "mean_copies_climbed": 3.16
  },
  "standin29": {
   "cell_size": 1670,
   "sampled": 80,
   "above_all_12": 7,
   "rate": 0.0875,
   "beat_first_copy": 42,
   "beat_first_rate": 0.525,
   "mean_copies_climbed": 3.1
  },
  "standin30": {
   "cell_size": 1811,
   "sampled": 80,
   "above_all_12": 15,
   "rate": 0.1875,
   "beat_first_copy": 54,
   "beat_first_rate": 0.675,
   "mean_copies_climbed": 5.17
  },
  "standin31": {
   "cell_size": 3301,
   "sampled": 80,
   "above_all_12": 8,
   "rate": 0.1,
   "beat_first_copy": 42,
   "beat_first_rate": 0.525,
   "mean_copies_climbed": 3.44
  },
  "standin32": {
   "cell_size": 2481,
   "sampled": 80,
   "above_all_12": 13,
   "rate": 0.1625,
   "beat_first_copy": 55,
   "beat_first_rate": 0.6875,
   "mean_copies_climbed": 4.69
  },
  "standin33": {
   "cell_size": 5040,
   "sampled": 80,
   "above_all_12": 2,
   "rate": 0.025,
   "beat_first_copy": 47,
   "beat_first_rate": 0.5875,
   "mean_copies_climbed": 2.88
  },
  "standin34": {
   "cell_size": 3779,
   "sampled": 80,
   "above_all_12": 10,
   "rate": 0.125,
   "beat_first_copy": 46,
   "beat_first_rate": 0.575,
   "mean_copies_climbed": 3.84
  },
  "standin35": {
   "cell_size": 2594,
   "sampled": 80,
   "above_all_12": 7,
   "rate": 0.0875,
   "beat_first_copy": 33,
   "beat_first_rate": 0.4125,
   "mean_copies_climbed": 2.79
  },
  "standin36": {
   "cell_size": 2542,
   "sampled": 80,
   "above_all_12": 14,
   "rate": 0.175,
   "beat_first_copy": 47,
   "beat_first_rate": 0.5875,
   "mean_copies_climbed": 4.49
  },
  "standin37": {
   "cell_size": 4757,
   "sampled": 80,
   "above_all_12": 8,
   "rate": 0.1,
   "beat_first_copy": 42,
   "beat_first_rate": 0.525,
   "mean_copies_climbed": 3.1
  },
  "standin38": {
   "cell_size": 6172,
   "sampled": 80,
   "above_all_12": 4,
   "rate": 0.05,
   "beat_first_copy": 44,
   "beat_first_rate": 0.55,
   "mean_copies_climbed": 2.94
  },
  "standin39": {
   "cell_size": 4640,
   "sampled": 80,
   "above_all_12": 4,
   "rate": 0.05,
   "beat_first_copy": 40,
   "beat_first_rate": 0.5,
   "mean_copies_climbed": 2.84
  }
 },
 "schedules_per_target": 80,
 "fair_rate_12": 0.0769,
 "k4_rate": 0.1,
 "standins_rate_mean": 0.1084,
 "standins_rate_sd": 0.0645,
 "standins_rate_min_max": [
  0.0,
  0.2875
 ],
 "standins_at_or_above_k4_rate": 20,
 "p_rate": 0.5122,
 "k4_beat_first_rate": 0.65,
 "standins_at_or_above_k4_beat_first": 7,
 "p_beat_first": 0.1951,
 "lead": false,
 "core_seconds": 250870,
 "compute_seconds": 8139,
 "exhaustive": false,
 "modal_cost_estimate": "41 targets x 80 schedules x about 4 climbs x about 17 s: about 223,000 core-seconds, about $3.5 of Modal credit (credit left about $15 after the margin)"
}
```

Notes: K4 among 40 stand-ins: K4 rate 0.100, stand-ins mean 0.108 (sd 0.065, range 0.000-0.287); 20 of 40 at or above K4, p 0.512; beat-first rate p 0.195. K4 inside its stand-ins.


