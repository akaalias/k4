# 0252-d2-one-run-decider-power-and-cost-on-schedules-and-moves: D2: the one-run decider's power and cost on F1.4's hand key schedules and on F6.1's moves, one free alphabet: 24 clean and 24 Sanborn-style plants per class, each on a setting K4 itself fits

**Family:** 1-keyed-periodic  
**Parent:** 0229-d1-one-free-alphabet-power-per-run-with-enough-plants  
**Decision:** reverted  
**Run:** 2026-10-28T13:07:27+00:00, 925.1 s, status ran  
**Time by phase:** design 188 s, implement 548 s, test 1466 s, run 925 s, record 0 s

## In plain words

Two groups of possible ciphers were left untested because each candidate setting took half an hour to judge, and there are hundreds (key-skipping rules) or hundreds of thousands (a shuffle of the letters, then the cipher table). A faster judge was approved yesterday. Before using it here we check that it still finds hidden test messages in these two groups, and time it, so we know what testing every candidate would cost.

## Walkthrough, by hand

1. Pick a key-skipping rule (say: one key letter skipped every 7 letters, key of 11 letters) or a letter shuffle followed by a key of 9 letters.
2. Write down, for each of the 97 carved letters, which key letter enciphered it.
3. Hide a test message under that rule with a shuffled alphabet and a random key.
4. Make six scrambled copies of its ciphertext that the same rule could still have produced.
5. Run one tempering search on the hidden message and on each copy, scoring the readings as English.
6. The rule's judge works if the hidden message scores above all six copies; repeat for 48 messages per group and time each search.

## Worked example (generated)

```
D2 measures the one-run decider on settings other than a plain repeating key.

  setting      skip one key letter every 7 letters, 11 key letters
  slot map     place 1 2 3 4 5 6 7 8 9 ...
  key letter         1 2 3 4 5 6 8 9 10 ... (letter 7 skipped)

  a hidden message under that slot map and its six scrambled copies get one tempering search each;
  found when the hidden message's best English score is above all six copies'.
  The time per search times the settings K4 fits gives the cost of deciding the whole cell.
```

## Lineage

Inherits from 0229-d1-one-free-alphabet-power-per-run-with-enough-plants. What changed: D2 (issue #77), first measurement. D1 was decided on 2026-10-28 (#100): one design-2 run, copies climbed one at a time, qualifies for one free alphabet. Its power was measured only on plain periodic keys (F1.1, L23 and L26). Here 0140's compiled climb is generalised from 'key letter i mod L, reading in carved order' to any slot map and any reading order, so the same climb runs on F1.4's key schedules (skip, stutter, back and forth, triangle, square, line restart) and on F6.1's moves (0129/0130's type-1 library, either order); its power is measured per cell class on settings K4 itself fits, with the time per climb, and every cost-blocked one-alphabet cell is re-costed from it.

## Hypothesis (domain expert)

F1.4 (hand key schedules, C20(d), 0126-0128) and F6.1 (one free alphabet before or after a type-1 move, C1(a), 0129, 0130) were closed exact where no setting fits and blocked by cost where K4 fits at the copies' rate: 555 one-alphabet slot partitions under the schedules (0127, 0128) and about 443,000 (move, order, form, length) settings (0129, 0130), each needing F1.5's design-2 decider at 20-30 min. D1 (0228, 0229) found one tempering run as strong as ten for one free alphabet (pooled 66 of 96 plants against 67), and Alexis allowed it with every close stating its measured power. The decider's climb (0140) only needs, for each carved letter, which key slot enciphered it and where it stands in the message; the known letters give the same same-slot checks. So one generalised climb covers both families. Unknown: its power on these slot structures (a schedule gives uneven slot sizes; a move scatters the known places over the slots) and its time per setting. Measured on settings drawn from those K4 fits, so the power is the power of the decisions D2 reopens. Clue entries: C20(d) (the tableau rows and schedules as Sanborn's 'slightly different' use of the table), C1(a) (a move, then the table).

## Prediction

Generalised climb reproduces 0140's scores exactly on plain periodic settings. One-run power (found above all 6 own copies, null 1/7): F1.4 schedules clean about 0.8, Sanborn-style about 0.6; F6.1 at lengths 8-10 higher (about 0.9 and 0.7, more checks per slot); F6.1 at 11-26 about 0.7 and 0.55. Every class pooled at least 0.5. Cost: F1.4's one-alphabet residue (a few thousand full settings over both forms) under 100 core-hours, so it reopens within the $20 line; F6.1 at lengths 6-10 (about 7,400 settings) around 150 core-hours, near the line; F6.1 at 11-26 above 5,000 core-hours, which waits for money. Zero candidates.

## Method

1. The climb: 0140's C source, patched in four places (a slot per carved letter instead of i mod L, a message place per carved letter, the added form beside Beaufort, the known places given as carved places), checked against 0140's unpatched library on the same seeds.
2. F1.4 settings: every schedule of 0128 (skip m 2-30, stutter, triangle, square, line restart, back and forth) at every slot count, as a slot map over all 97 places, deduplicated; each decided exactly on K4 in both forms with 0128's decide(); the fitting ones are the cost count.
3. F6.1 settings: 0129's library (27,852 maps), order A (move, then table) and B (table, then move), both forms; K4's fits recounted exactly at lengths 6-10 with 0129's decide(); 11-26 taken from 0129 and 0130's records.
4. Four classes: F1.4 skip, F1.4 other schedules, F6.1 lengths 8-10, F6.1 lengths 11-26. Per class 24 clean plants (Carter windows, 0120's rule) and 24 Sanborn-style (0226's classes: X stops, K1-K3 windows, three letters changed), each on its own setting drawn at random from K4's fitting settings in the class, random alphabet and key; 6 own copies each, shuffles that the exact decider fits at that setting.
5. One tempering run per text (16 replicas x 625 rounds x 1000 moves, 0140's temperatures), time recorded. A plant is found when its best is strictly above all 6 own copies' bests.
6. Cost per setting = time per climb x (1 + 3.10, the expected copies climbed one at a time against 12) + time to make the copies; total per cell = cost x K4's fitting settings, in core-hours and Modal dollars.

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
 "item": "D2",
 "decider": "D1's one-run decider: 0140's compiled tempering, one run (16 x 625 x 1000), generalised to any slot map and reading order",
 "self_check_against_0140": [
  [
   23,
   -5.23832,
   -5.23832
  ],
  [
   26,
   -5.13042,
   -5.13042
  ]
 ],
 "f14_settings_listed": {
  "F1.4 skip": 11164,
  "F1.4 other": 1482
 },
 "f14_k4_fitting_settings": 2093,
 "f14_k4_fitting_by_group": {
  "F1.4 skip": 2016,
  "F1.4 other": 77
 },
 "f14_k4_fitting_partitions": {
  "F1.4 skip": 461,
  "F1.4 other": 52
 },
 "f61_k4_fits_6_10_recount": {
  "BV10": 2831,
  "BV8": 782,
  "BB10": 1389,
  "BB8": 221,
  "AV8": 191,
  "AV9": 444,
  "AB9": 174,
  "AB10": 301,
  "BV7": 230,
  "BB7": 89,
  "AV10": 641,
  "AV7": 48,
  "BB6": 8,
  "AB8": 54,
  "AB7": 14,
  "BV6": 23,
  "AB6": 1,
  "AV6": 2
 },
 "f61_k4_fits_11_26_from_0129_0130": 435693,
 "f61_records_6_10": {
  "AV": [
   2,
   48,
   191,
   444,
   641
  ],
  "AB": [
   1,
   16,
   54,
   174,
   301
  ],
  "BV": [
   23,
   231,
   782,
   0,
   2831
  ],
  "BB": [
   8,
   89,
   221,
   0,
   1389
  ]
 },
 "plants_per_class": 48,
 "own_copies": 6,
 "null_per_plant": "1/7",
 "plants_without_copies": [],
 "power": {
  "F1.4 skip/clean": [
   18,
   24
  ],
  "F1.4 skip/sanborn": [
   19,
   24
  ],
  "F1.4 skip/pooled": [
   37,
   48
  ],
  "F1.4 other/clean": [
   19,
   24
  ],
  "F1.4 other/sanborn": [
   18,
   24
  ],
  "F1.4 other/pooled": [
   37,
   48
  ],
  "F6.1 8-10/clean": [
   12,
   24
  ],
  "F6.1 8-10/sanborn": [
   19,
   24
  ],
  "F6.1 8-10/pooled": [
   31,
   48
  ],
  "F6.1 11-26/clean": [
   15,
   24
  ],
  "F6.1 11-26/sanborn": [
   17,
   24
  ],
  "F6.1 11-26/pooled": [
   32,
   48
  ]
 },
 "reference_one_run_0229": {
  "L23": {
   "clean": [
    23,
    24
   ],
   "sanborn": [
    14,
    24
   ]
  },
  "L26": {
   "clean": [
    15,
    24
   ],
   "sanborn": [
    14,
    24
   ]
  },
  "pooled": [
   66,
   96
  ]
 },
 "seconds_per_climb": {
  "F1.4 skip": 16.56,
  "F1.4 other": 16.1,
  "F6.1 8-10": 28.75,
  "F6.1 11-26": 14.97
 },
 "copy_core_seconds_each": 0.152,
 "copy_tries_median": 17,
 "sequential_copies_expected": 3.1,
 "cost": {
  "F1.4 skip": {
   "settings": 2016,
   "core_seconds_per_setting": 69.8,
   "core_hours": 39.1,
   "modal_dollars_ideal": 1.9,
   "modal_dollars_at_half_efficiency": 3.8,
   "power_pooled": [
    37,
    48
   ]
  },
  "F1.4 other": {
   "settings": 77,
   "core_seconds_per_setting": 67.9,
   "core_hours": 1.5,
   "modal_dollars_ideal": 0.1,
   "modal_dollars_at_half_efficiency": 0.1,
   "power_pooled": [
    37,
    48
   ]
  },
  "F6.1 6-10": {
   "settings": 7443,
   "core_seconds_per_setting": 119.8,
   "core_hours": 247.7,
   "modal_dollars_ideal": 12.2,
   "modal_dollars_at_half_efficiency": 24.4,
   "power_pooled": [
    31,
    48
   ]
  },
  "F6.1 11-26": {
   "settings": 435693,
   "core_seconds_per_setting": 63.2,
   "core_hours": 7648.8,
   "modal_dollars_ideal": 376.0,
   "modal_dollars_at_half_efficiency": 752.0,
   "power_pooled": [
    32,
    48
   ]
  }
 },
 "dollars_per_core_hour": 0.0492,
 "plants": {
  "F1.4 skip/0": {
   "cls": "clean",
   "setting": "B skip m=18 phi=6 n=26",
   "nslots": 26,
   "form": "B",
   "found": true,
   "margin": 0.1238,
   "letters_right": 46
  },
  "F1.4 skip/1": {
   "cls": "clean",
   "setting": "B skip m=25 phi=24 n=17",
   "nslots": 17,
   "form": "B",
   "found": false,
   "margin": -0.1412,
   "letters_right": 43
  },
  "F1.4 skip/2": {
   "cls": "clean",
   "setting": "B skip m=12 phi=2 n=25",
   "nslots": 25,
   "form": "B",
   "found": true,
   "margin": 0.2137,
   "letters_right": 38
  },
  "F1.4 skip/3": {
   "cls": "clean",
   "setting": "B skip m=22 phi=20 n=12",
   "nslots": 12,
   "form": "B",
   "found": true,
   "margin": 0.2274,
   "letters_right": 42
  },
  "F1.4 skip/4": {
   "cls": "clean",
   "setting": "B skip m=14 phi=10 n=22",
   "nslots": 22,
   "form": "V",
   "found": true,
   "margin": 0.2114,
   "letters_right": 37
  },
  "F1.4 skip/5": {
   "cls": "clean",
   "setting": "B skip m=28 phi=18 n=24",
   "nslots": 24,
   "form": "B",
   "found": false,
   "margin": -0.0233,
   "letters_right": 42
  },
  "F1.4 skip/6": {
   "cls": "clean",
   "setting": "B skip m=29 phi=10 n=21",
   "nslots": 21,
   "form": "V",
   "found": true,
   "margin": 0.005,
   "letters_right": 30
  },
  "F1.4 skip/7": {
   "cls": "clean",
   "setting": "B skip m=27 phi=22 n=14",
   "nslots": 14,
   "form": "V",
   "found": true,
   "margin": 0.6493,
   "letters_right": 51
  },
  "F1.4 skip/8": {
   "cls": "clean",
   "setting": "B skip m=20 phi=14 n=16",
   "nslots": 16,
   "form": "B",
   "found": true,
   "margin": 0.2011,
   "letters_right": 42
  },
  "F1.4 skip/9": {
   "cls": "clean",
   "setting": "B skip m=28 phi=2 n=24",
   "nslots": 24,
   "form": "B",
   "found": true,
   "margin": 0.1476,
   "letters_right": 34
  },
  "F1.4 skip/10": {
   "cls": "clean",
   "setting": "B skip m=8 phi=6 n=23",
   "nslots": 23,
   "form": "V",
   "found": true,
   "margin": 0.1435,
   "letters_right": 39
  },
  "F1.4 skip/11": {
   "cls": "clean",
   "setting": "B skip m=20 phi=14 n=16",
   "nslots": 16,
   "form": "B",
   "found": false,
   "margin": -0.2297,
   "letters_right": 35
  },
  "F1.4 skip/12": {
   "cls": "clean",
   "setting": "B skip m=28 phi=7 n=26",
   "nslots": 26,
   "form": "B",
   "found": true,
   "margin": 0.031,
   "letters_right": 33
  },
  "F1.4 skip/13": {
   "cls": "clean",
   "setting": "B skip m=22 phi=0 n=24",
   "nslots": 24,
   "form": "B",
   "found": true,
   "margin": 0.1904,
   "letters_right": 38
  },
  "F1.4 skip/14": {
   "cls": "clean",
   "setting": "B skip m=11 phi=5 n=17",
   "nslots": 17,
   "form": "B",
   "found": false,
   "margin": -0.1469,
   "letters_right": 41
  },
  "F1.4 skip/15": {
   "cls": "clean",
   "setting": "B skip m=23 phi=5 n=16",
   "nslots": 16,
   "form": "B",
   "found": true,
   "margin": 0.2762,
   "letters_right": 44
  },
  "F1.4 skip/16": {
   "cls": "clean",
   "setting": "B skip m=18 phi=10 n=26",
   "nslots": 26,
   "form": "B",
   "found": false,
   "margin": -0.0286,
   "letters_right": 33
  },
  "F1.4 skip/17": {
   "cls": "clean",
   "setting": "B skip m=24 phi=23 n=24",
   "nslots": 24,
   "form": "B",
   "found": true,
   "margin": 0.1567,
   "letters_right": 42
  },
  "F1.4 skip/18": {
   "cls": "clean",
   "setting": "B skip m=24 phi=20 n=21",
   "nslots": 21,
   "form": "B",
   "found": true,
   "margin": 0.1318,
   "letters_right": 44
  },
  "F1.4 skip/19": {
   "cls": "clean",
   "setting": "B skip m=25 phi=20 n=16",
   "nslots": 16,
   "form": "B",
   "found": true,
   "margin": 0.1167,
   "letters_right": 45
  },
  "F1.4 skip/20": {
   "cls": "clean",
   "setting": "B skip m=10 phi=2 n=18",
   "nslots": 18,
   "form": "B",
   "found": false,
   "margin": -0.0809,
   "letters_right": 43
  },
  "F1.4 skip/21": {
   "cls": "clean",
   "setting": "B skip m=22 phi=13 n=17",
   "nslots": 17,
   "form": "B",
   "found": true,
   "margin": 0.1546,
   "letters_right": 40
  },
  "F1.4 skip/22": {
   "cls": "clean",
   "setting": "B skip m=15 phi=0 n=26",
   "nslots": 26,
   "form": "B",
   "found": true,
   "margin": 0.0329,
   "letters_right": 44
  },
  "F1.4 skip/23": {
   "cls": "clean",
   "setting": "B skip m=12 phi=2 n=17",
   "nslots": 17,
   "form": "B",
   "found": true,
   "margin": 0.1306,
   "letters_right": 37
  },
  "F1.4 skip/24": {
   "cls": "xstops",
   "setting": "B skip m=21 phi=7 n=24",
   "nslots": 24,
   "form": "B",
   "found": true,
   "margin": 0.1572,
   "letters_right": 39
  },
  "F1.4 skip/25": {
   "cls": "xstops",
   "setting": "B skip m=27 phi=2 n=14",
   "nslots": 14,
   "form": "V",
   "found": true,
   "margin": 0.0009,
   "letters_right": 40
  },
  "F1.4 skip/26": {
   "cls": "xstops",
   "setting": "B skip m=5 phi=1 n=19",
   "nslots": 19,
   "form": "B",
   "found": true,
   "margin": 0.1496,
   "letters_right": 43
  },
  "F1.4 skip/27": {
   "cls": "xstops",
   "setting": "B skip m=28 phi=5 n=16",
   "nslots": 16,
   "form": "B",
   "found": true,
   "margin": 0.141,
   "letters_right": 43
  },
  "F1.4 skip/28": {
   "cls": "k123",
   "setting": "B skip m=27 phi=14 n=20",
   "nslots": 20,
   "form": "B",
   "found": true,
   "margin": 0.1438,
   "letters_right": 37
  },
  "F1.4 skip/29": {
   "cls": "k123",
   "setting": "B skip m=16 phi=8 n=21",
   "nslots": 21,
   "form": "V",
   "found": true,
   "margin": 0.4927,
   "letters_right": 38
  },
  "F1.4 skip/30": {
   "cls": "k123",
   "setting": "B skip m=22 phi=11 n=17",
   "nslots": 17,
   "form": "B",
   "found": false,
   "margin": -0.0115,
   "letters_right": 41
  },
  "F1.4 skip/31": {
   "cls": "k123",
   "setting": "B skip m=15 phi=5 n=26",
   "nslots": 26,
   "form": "V",
   "found": true,
   "margin": 0.2235,
   "letters_right": 38
  },
  "F1.4 skip/32": {
   "cls": "sub3",
   "setting": "B skip m=11 phi=0 n=17",
   "nslots": 17,
   "form": "B",
   "found": true,
   "margin": 0.1598,
   "letters_right": 44
  },
  "F1.4 skip/33": {
   "cls": "sub3",
   "setting": "B skip m=26 phi=18 n=24",
   "nslots": 24,
   "form": "B",
   "found": true,
   "margin": 0.014,
   "letters_right": 36
  },
  "F1.4 skip/34": {
   "cls": "sub3",
   "setting": "B skip m=29 phi=20 n=24",
   "nslots": 24,
   "form": "B",
   "found": false,
   "margin": -0.0614,
   "letters_right": 28
  },
  "F1.4 skip/35": {
   "cls": "sub3",
   "setting": "B skip m=30 phi=3 n=16",
   "nslots": 16,
   "form": "B",
   "found": false,
   "margin": -0.0473,
   "letters_right": 40
  },
  "F1.4 skip/36": {
   "cls": "xstops",
   "setting": "B skip m=27 phi=11 n=24",
   "nslots": 24,
   "form": "B",
   "found": true,
   "margin": 0.0396,
   "letters_right": 38
  },
  "F1.4 skip/37": {
   "cls": "xstops",
   "setting": "B skip m=15 phi=2 n=22",
   "nslots": 22,
   "form": "V",
   "found": false,
   "margin": -0.0373,
   "letters_right": 35
  },
  "F1.4 skip/38": {
   "cls": "xstops",
   "setting": "B skip m=18 phi=8 n=26",
   "nslots": 26,
   "form": "B",
   "found": true,
   "margin": 0.0135,
   "letters_right": 37
  },
  "F1.4 skip/39": {
   "cls": "xstops",
   "setting": "B skip m=26 phi=9 n=16",
   "nslots": 16,
   "form": "B",
   "found": true,
   "margin": 0.4844,
   "letters_right": 40
  },
  "F1.4 skip/40": {
   "cls": "k123",
   "setting": "B skip m=30 phi=3 n=24",
   "nslots": 24,
   "form": "B",
   "found": true,
   "margin": 0.1391,
   "letters_right": 37
  },
  "F1.4 skip/41": {
   "cls": "k123",
   "setting": "B skip m=22 phi=8 n=24",
   "nslots": 24,
   "form": "B",
   "found": true,
   "margin": 0.0733,
   "letters_right": 35
  },
  "F1.4 skip/42": {
   "cls": "k123",
   "setting": "B skip m=27 phi=0 n=17",
   "nslots": 17,
   "form": "B",
   "found": true,
   "margin": 0.006,
   "letters_right": 35
  },
  "F1.4 skip/43": {
   "cls": "k123",
   "setting": "B skip m=17 phi=12 n=24",
   "nslots": 24,
   "form": "B",
   "found": false,
   "margin": -0.0443,
   "letters_right": 38
  },
  "F1.4 skip/44": {
   "cls": "sub3",
   "setting": "B skip m=11 phi=4 n=20",
   "nslots": 20,
   "form": "B",
   "found": true,
   "margin": 0.1032,
   "letters_right": 43
  },
  "F1.4 skip/45": {
   "cls": "sub3",
   "setting": "B skip m=15 phi=12 n=26",
   "nslots": 26,
   "form": "B",
   "found": true,
   "margin": 0.0516,
   "letters_right": 39
  },
  "F1.4 skip/46": {
   "cls": "sub3",
   "setting": "B skip m=30 phi=7 n=14",
   "nslots": 14,
   "form": "V",
   "found": true,
   "margin": 0.1414,
   "letters_right": 37
  },
  "F1.4 skip/47": {
   "cls": "sub3",
   "setting": "B skip m=29 phi=17 n=16",
   "nslots": 16,
   "form": "B",
   "found": true,
   "margin": 0.2814,
   "letters_right": 40
  },
  "F1.4 other/0": {
   "cls": "clean",
   "setting": "D back and forth n=17 ends=once phi=11",
   "nslots": 17,
   "form": "B",
   "found": true,
   "margin": 0.1792,
   "letters_right": 39
  },
  "F1.4 other/1": {
   "cls": "clean",
   "setting": "F line restart from K4's first letter n=29",
   "nslots": 29,
   "form": "B",
   "found": true,
   "margin": 0.0881,
   "letters_right": 39
  },
  "F1.4 other/2": {
   "cls": "clean",
   "setting": "D back and forth n=26 ends=repeated phi=22",
   "nslots": 26,
   "form": "B",
   "found": true,
   "margin": 0.0121,
   "letters_right": 35
  },
  "F1.4 other/3": {
   "cls": "clean",
   "setting": "D back and forth n=24 ends=once phi=8",
   "nslots": 24,
   "form": "B",
   "found": true,
   "margin": 0.044,
   "letters_right": 39
  },
  "F1.4 other/4": {
   "cls": "clean",
   "setting": "F line restart from K4's first letter n=31",
   "nslots": 31,
   "form": "B",
   "found": true,
   "margin": 0.0966,
   "letters_right": 38
  },
  "F1.4 other/5": {
   "cls": "clean",
   "setting": "D back and forth n=23 ends=repeated phi=7",
   "nslots": 23,
   "form": "B",
   "found": true,
   "margin": 0.0056,
   "letters_right": 39
  },
  "F1.4 other/6": {
   "cls": "clean",
   "setting": "D back and forth n=23 ends=repeated phi=8",
   "nslots": 23,
   "form": "B",
   "found": true,
   "margin": 0.0779,
   "letters_right": 36
  },
  "F1.4 other/7": {
   "cls": "clean",
   "setting": "F line restart from line start n=30",
   "nslots": 30,
   "form": "B",
   "found": true,
   "margin": 0.048,
   "letters_right": 34
  },
  "F1.4 other/8": {
   "cls": "clean",
   "setting": "D back and forth n=24 ends=once phi=6",
   "nslots": 24,
   "form": "B",
   "found": true,
   "margin": 0.0771,
   "letters_right": 30
  },
  "F1.4 other/9": {
   "cls": "clean",
   "setting": "D back and forth n=24 ends=once phi=16",
   "nslots": 24,
   "form": "B",
   "found": true,
   "margin": 0.0232,
   "letters_right": 34
  },
  "F1.4 other/10": {
   "cls": "clean",
   "setting": "E square phi=5 n=23",
   "nslots": 12,
   "form": "B",
   "found": true,
   "margin": 0.3429,
   "letters_right": 40
  },
  "F1.4 other/11": {
   "cls": "clean",
   "setting": "F line restart from line start n=16",
   "nslots": 16,
   "form": "B",
   "found": true,
   "margin": 0.4549,
   "letters_right": 45
  },
  "F1.4 other/12": {
   "cls": "clean",
   "setting": "D back and forth n=24 ends=once phi=3",
   "nslots": 24,
   "form": "B",
   "found": true,
   "margin": 0.0326,
   "letters_right": 34
  },
  "F1.4 other/13": {
   "cls": "clean",
   "setting": "D back and forth n=24 ends=once phi=10",
   "nslots": 24,
   "form": "B",
   "found": false,
   "margin": -0.0672,
   "letters_right": 35
  },
  "F1.4 other/14": {
   "cls": "clean",
   "setting": "D back and forth n=14 ends=repeated phi=3",
   "nslots": 14,
   "form": "V",
   "found": false,
   "margin": -0.1634,
   "letters_right": 41
  },
  "F1.4 other/15": {
   "cls": "clean",
   "setting": "F line restart from K4's first letter n=15",
   "nslots": 15,
   "form": "B",
   "found": false,
   "margin": -0.2377,
   "letters_right": 37
  },
  "F1.4 other/16": {
   "cls": "clean",
   "setting": "D back and forth n=17 ends=once phi=8",
   "nslots": 17,
   "form": "B",
   "found": true,
   "margin": 0.1678,
   "letters_right": 37
  },
  "F1.4 other/17": {
   "cls": "clean",
   "setting": "D back and forth n=26 ends=repeated phi=8",
   "nslots": 26,
   "form": "B",
   "found": false,
   "margin": -0.03,
   "letters_right": 32
  },
  "F1.4 other/18": {
   "cls": "clean",
   "setting": "D back and forth n=24 ends=once phi=5",
   "nslots": 24,
   "form": "B",
   "found": true,
   "margin": 0.0396,
   "letters_right": 38
  },
  "F1.4 other/19": {
   "cls": "clean",
   "setting": "D back and forth n=17 ends=once phi=10",
   "nslots": 17,
   "form": "B",
   "found": true,
   "margin": 0.0202,
   "letters_right": 32
  },
  "F1.4 other/20": {
   "cls": "clean",
   "setting": "D back and forth n=26 ends=repeated phi=16",
   "nslots": 26,
   "form": "B",
   "found": true,
   "margin": 0.0402,
   "letters_right": 37
  },
  "F1.4 other/21": {
   "cls": "clean",
   "setting": "D back and forth n=16 ends=once phi=6",
   "nslots": 16,
   "form": "B",
   "found": true,
   "margin": 0.1923,
   "letters_right": 43
  },
  "F1.4 other/22": {
   "cls": "clean",
   "setting": "D back and forth n=14 ends=repeated phi=3",
   "nslots": 14,
   "form": "V",
   "found": true,
   "margin": 0.1089,
   "letters_right": 33
  },
  "F1.4 other/23": {
   "cls": "clean",
   "setting": "D back and forth n=24 ends=once phi=16",
   "nslots": 24,
   "form": "B",
   "found": false,
   "margin": -0.0706,
   "letters_right": 30
  },
  "F1.4 other/24": {
   "cls": "xstops",
   "setting": "D back and forth n=17 ends=once phi=9",
   "nslots": 17,
   "form": "B",
   "found": false,
   "margin": -0.0201,
   "letters_right": 41
  },
  "F1.4 other/25": {
   "cls": "xstops",
   "setting": "D back and forth n=17 ends=once phi=13",
   "nslots": 17,
   "form": "B",
   "found": true,
   "margin": 0.2263,
   "letters_right": 43
  },
  "F1.4 other/26": {
   "cls": "xstops",
   "setting": "D back and forth n=26 ends=repeated phi=16",
   "nslots": 26,
   "form": "B",
   "found": false,
   "margin": -0.0041,
   "letters_right": 34
  },
  "F1.4 other/27": {
   "cls": "xstops",
   "setting": "F line restart from line start n=30",
   "nslots": 30,
   "form": "B",
   "found": true,
   "margin": 0.0738,
   "letters_right": 37
  },
  "F1.4 other/28": {
   "cls": "k123",
   "setting": "D back and forth n=23 ends=repeated phi=7",
   "nslots": 23,
   "form": "B",
   "found": true,
   "margin": 0.0818,
   "letters_right": 33
  },
  "F1.4 other/29": {
   "cls": "k123",
   "setting": "D back and forth n=24 ends=once phi=8",
   "nslots": 24,
   "form": "B",
   "found": false,
   "margin": -0.1195,
   "letters_right": 31
  },
  "F1.4 other/30": {
   "cls": "k123",
   "setting": "D back and forth n=26 ends=repeated phi=18",
   "nslots": 26,
   "form": "B",
   "found": true,
   "margin": 0.069,
   "letters_right": 32
  },
  "F1.4 other/31": {
   "cls": "k123",
   "setting": "D back and forth n=24 ends=once phi=8",
   "nslots": 24,
   "form": "B",
   "found": true,
   "margin": 0.0476,
   "letters_right": 37
  },
  "F1.4 other/32": {
   "cls": "sub3",
   "setting": "D back and forth n=26 ends=repeated phi=15",
   "nslots": 26,
   "form": "B",
   "found": true,
   "margin": 0.1773,
   "letters_right": 40
  },
  "F1.4 other/33": {
   "cls": "sub3",
   "setting": "D back and forth n=26 ends=repeated phi=14",
   "nslots": 26,
   "form": "B",
   "found": true,
   "margin": 0.0542,
   "letters_right": 38
  },
  "F1.4 other/34": {
   "cls": "sub3",
   "setting": "D back and forth n=23 ends=repeated phi=2",
   "nslots": 23,
   "form": "B",
   "found": false,
   "margin": -0.1354,
   "letters_right": 33
  },
  "F1.4 other/35": {
   "cls": "sub3",
   "setting": "D back and forth n=15 ends=repeated phi=0",
   "nslots": 15,
   "form": "B",
   "found": true,
   "margin": 0.3203,
   "letters_right": 43
  },
  "F1.4 other/36": {
   "cls": "xstops",
   "setting": "D back and forth n=26 ends=repeated phi=18",
   "nslots": 26,
   "form": "B",
   "found": true,
   "margin": 0.089,
   "letters_right": 30
  },
  "F1.4 other/37": {
   "cls": "xstops",
   "setting": "E triangle phi=2 n=23",
   "nslots": 12,
   "form": "B",
   "found": true,
   "margin": 0.619,
   "letters_right": 45
  },
  "F1.4 other/38": {
   "cls": "xstops",
   "setting": "D back and forth n=23 ends=repeated phi=10",
   "nslots": 23,
   "form": "B",
   "found": false,
   "margin": -0.0829,
   "letters_right": 33
  },
  "F1.4 other/39": {
   "cls": "xstops",
   "setting": "F line restart from line start n=25",
   "nslots": 25,
   "form": "B",
   "found": true,
   "margin": 0.0494,
   "letters_right": 39
  },
  "F1.4 other/40": {
   "cls": "k123",
   "setting": "D back and forth n=23 ends=repeated phi=2",
   "nslots": 23,
   "form": "B",
   "found": true,
   "margin": 0.1911,
   "letters_right": 30
  },
  "F1.4 other/41": {
   "cls": "k123",
   "setting": "F line restart from K4's first letter n=16",
   "nslots": 16,
   "form": "B",
   "found": true,
   "margin": 0.626,
   "letters_right": 36
  },
  "F1.4 other/42": {
   "cls": "k123",
   "setting": "D back and forth n=26 ends=repeated phi=22",
   "nslots": 26,
   "form": "B",
   "found": true,
   "margin": 0.0483,
   "letters_right": 36
  },
  "F1.4 other/43": {
   "cls": "k123",
   "setting": "D back and forth n=24 ends=once phi=12",
   "nslots": 24,
   "form": "B",
   "found": true,
   "margin": 0.0634,
   "letters_right": 38
  },
  "F1.4 other/44": {
   "cls": "sub3",
   "setting": "D back and forth n=26 ends=repeated phi=22",
   "nslots": 26,
   "form": "B",
   "found": false,
   "margin": -0.072,
   "letters_right": 29
  },
  "F1.4 other/45": {
   "cls": "sub3",
   "setting": "E triangle phi=4 n=23",
   "nslots": 12,
   "form": "B",
   "found": true,
   "margin": 0.3222,
   "letters_right": 41
  },
  "F1.4 other/46": {
   "cls": "sub3",
   "setting": "E square phi=3 n=23",
   "nslots": 12,
   "form": "B",
   "found": true,
   "margin": 0.2201,
   "letters_right": 39
  },
  "F1.4 other/47": {
   "cls": "sub3",
   "setting": "D back and forth n=23 ends=repeated phi=14",
   "nslots": 23,
   "form": "B",
   "found": true,
   "margin": 0.084,
   "letters_right": 39
  },
  "F6.1 8-10/0": {
   "cls": "clean",
   "setting": "K3 rule a=32 b=45 inverse order B L=10 V",
   "nslots": 10,
   "form": "V",
   "found": false,
   "margin": -0.3531,
   "letters_right": 38
  },
  "F6.1 8-10/1": {
   "cls": "clean",
   "setting": "two turns cw 95,20 inverse order B L=10 V",
   "nslots": 10,
   "form": "V",
   "found": true,
   "margin": 0.1314,
   "letters_right": 40
  },
  "F6.1 8-10/2": {
   "cls": "clean",
   "setting": "two turns cw 33,87 inverse order A L=10 V",
   "nslots": 10,
   "form": "V",
   "found": false,
   "margin": -0.4161,
   "letters_right": 40
  },
  "F6.1 8-10/3": {
   "cls": "clean",
   "setting": "K3 rule a=48 b=11 order A L=9 B",
   "nslots": 9,
   "form": "B",
   "found": false,
   "margin": -0.1935,
   "letters_right": 47
  },
  "F6.1 8-10/4": {
   "cls": "clean",
   "setting": "K3 rule a=19 b=9 inverse order A L=9 V",
   "nslots": 9,
   "form": "V",
   "found": true,
   "margin": 1.253,
   "letters_right": 47
  },
  "F6.1 8-10/5": {
   "cls": "clean",
   "setting": "K3 rule a=55 b=10 order B L=10 B",
   "nslots": 10,
   "form": "B",
   "found": true,
   "margin": 0.3546,
   "letters_right": 49
  },
  "F6.1 8-10/6": {
   "cls": "clean",
   "setting": "two turns cw 56,85 inverse order B L=10 V",
   "nslots": 10,
   "form": "V",
   "found": false,
   "margin": -0.1841,
   "letters_right": 46
  },
  "F6.1 8-10/7": {
   "cls": "clean",
   "setting": "two turns cw 18,87 inverse order B L=10 B",
   "nslots": 10,
   "form": "B",
   "found": true,
   "margin": 1.8346,
   "letters_right": 97
  },
  "F6.1 8-10/8": {
   "cls": "clean",
   "setting": "two turns cw 62,79 inverse order A L=10 V",
   "nslots": 10,
   "form": "V",
   "found": false,
   "margin": -0.5164,
   "letters_right": 37
  },
  "F6.1 8-10/9": {
   "cls": "clean",
   "setting": "K3 rule a=82 b=59 order A L=8 V",
   "nslots": 8,
   "form": "V",
   "found": true,
   "margin": 0.5983,
   "letters_right": 51
  },
  "F6.1 8-10/10": {
   "cls": "clean",
   "setting": "two turns cw 58,48 order B L=10 V",
   "nslots": 10,
   "form": "V",
   "found": true,
   "margin": 0.5523,
   "letters_right": 48
  },
  "F6.1 8-10/11": {
   "cls": "clean",
   "setting": "K3 rule a=57 b=33 inverse order B L=10 V",
   "nslots": 10,
   "form": "V",
   "found": true,
   "margin": 0.5384,
   "letters_right": 46
  },
  "F6.1 8-10/12": {
   "cls": "clean",
   "setting": "two turns cw 25,87 inverse order B L=8 V",
   "nslots": 8,
   "form": "V",
   "found": true,
   "margin": 0.9399,
   "letters_right": 48
  },
  "F6.1 8-10/13": {
   "cls": "clean",
   "setting": "two turns cw 74,33 inverse order A L=9 V",
   "nslots": 9,
   "form": "V",
   "found": true,
   "margin": 0.4347,
   "letters_right": 43
  },
  "F6.1 8-10/14": {
   "cls": "clean",
   "setting": "two turns cw 6,54 inverse order A L=10 B",
   "nslots": 10,
   "form": "B",
   "found": false,
   "margin": -0.1565,
   "letters_right": 47
  },
  "F6.1 8-10/15": {
   "cls": "clean",
   "setting": "K3 rule a=32 b=13 order B L=8 V",
   "nslots": 8,
   "form": "V",
   "found": true,
   "margin": 0.4231,
   "letters_right": 47
  },
  "F6.1 8-10/16": {
   "cls": "clean",
   "setting": "K3 rule a=90 b=16 order B L=10 V",
   "nslots": 10,
   "form": "V",
   "found": false,
   "margin": -0.2421,
   "letters_right": 49
  },
  "F6.1 8-10/17": {
   "cls": "clean",
   "setting": "two turns cw 42,6 order B L=10 B",
   "nslots": 10,
   "form": "B",
   "found": false,
   "margin": -0.3072,
   "letters_right": 40
  },
  "F6.1 8-10/18": {
   "cls": "clean",
   "setting": "two turns cw 81,57 order B L=10 B",
   "nslots": 10,
   "form": "B",
   "found": false,
   "margin": -0.3966,
   "letters_right": 44
  },
  "F6.1 8-10/19": {
   "cls": "clean",
   "setting": "K3 rule a=63 b=43 inverse order B L=8 V",
   "nslots": 8,
   "form": "V",
   "found": true,
   "margin": 0.57,
   "letters_right": 54
  },
  "F6.1 8-10/20": {
   "cls": "clean",
   "setting": "K3 rule a=46 b=44 inverse order B L=10 V",
   "nslots": 10,
   "form": "V",
   "found": false,
   "margin": -0.4707,
   "letters_right": 34
  },
  "F6.1 8-10/21": {
   "cls": "clean",
   "setting": "K3 rule a=47 b=96 order B L=8 V",
   "nslots": 8,
   "form": "V",
   "found": false,
   "margin": -0.4522,
   "letters_right": 44
  },
  "F6.1 8-10/22": {
   "cls": "clean",
   "setting": "two turns cw 19,94 order B L=10 B",
   "nslots": 10,
   "form": "B",
   "found": false,
   "margin": -0.1536,
   "letters_right": 37
  },
  "F6.1 8-10/23": {
   "cls": "clean",
   "setting": "two turns cw 3,84 order B L=10 B",
   "nslots": 10,
   "form": "B",
   "found": true,
   "margin": 0.2928,
   "letters_right": 45
  },
  "F6.1 8-10/24": {
   "cls": "xstops",
   "setting": "K3 rule a=75 b=21 inverse order A L=9 B",
   "nslots": 9,
   "form": "B",
   "found": true,
   "margin": 0.3139,
   "letters_right": 46
  },
  "F6.1 8-10/25": {
   "cls": "xstops",
   "setting": "two turns cw 83,96 order B L=10 B",
   "nslots": 10,
   "form": "B",
   "found": true,
   "margin": 0.1241,
   "letters_right": 55
  },
  "F6.1 8-10/26": {
   "cls": "xstops",
   "setting": "two turns cw 95,28 order B L=10 V",
   "nslots": 10,
   "form": "V",
   "found": false,
   "margin": -0.0734,
   "letters_right": 39
  },
  "F6.1 8-10/27": {
   "cls": "xstops",
   "setting": "two turns cw 50,63 order B L=10 V",
   "nslots": 10,
   "form": "V",
   "found": true,
   "margin": 0.5039,
   "letters_right": 59
  },
  "F6.1 8-10/28": {
   "cls": "k123",
   "setting": "K3 rule a=92 b=10 order A L=9 V",
   "nslots": 9,
   "form": "V",
   "found": true,
   "margin": 0.0414,
   "letters_right": 42
  },
  "F6.1 8-10/29": {
   "cls": "k123",
   "setting": "two turns cw 51,27 order B L=8 V",
   "nslots": 8,
   "form": "V",
   "found": false,
   "margin": -0.5381,
   "letters_right": 47
  },
  "F6.1 8-10/30": {
   "cls": "k123",
   "setting": "two turns cw 77,13 inverse order B L=10 V",
   "nslots": 10,
   "form": "V",
   "found": true,
   "margin": 0.1497,
   "letters_right": 51
  },
  "F6.1 8-10/31": {
   "cls": "k123",
   "setting": "K3 rule a=59 b=3 order B L=8 V",
   "nslots": 8,
   "form": "V",
   "found": true,
   "margin": 0.0581,
   "letters_right": 42
  },
  "F6.1 8-10/32": {
   "cls": "sub3",
   "setting": "two turns cw 74,84 order B L=10 B",
   "nslots": 10,
   "form": "B",
   "found": true,
   "margin": 0.4983,
   "letters_right": 56
  },
  "F6.1 8-10/33": {
   "cls": "sub3",
   "setting": "two turns cw 7,88 order B L=8 B",
   "nslots": 8,
   "form": "B",
   "found": true,
   "margin": 0.3352,
   "letters_right": 61
  },
  "F6.1 8-10/34": {
   "cls": "sub3",
   "setting": "two turns cw 87,51 order B L=8 V",
   "nslots": 8,
   "form": "V",
   "found": true,
   "margin": 1.6838,
   "letters_right": 97
  },
  "F6.1 8-10/35": {
   "cls": "sub3",
   "setting": "K3 rule a=4 b=31 inverse order B L=10 V",
   "nslots": 10,
   "form": "V",
   "found": true,
   "margin": 0.9722,
   "letters_right": 61
  },
  "F6.1 8-10/36": {
   "cls": "xstops",
   "setting": "two turns cw 47,88 order B L=10 B",
   "nslots": 10,
   "form": "B",
   "found": true,
   "margin": 0.6122,
   "letters_right": 58
  },
  "F6.1 8-10/37": {
   "cls": "xstops",
   "setting": "two turns cw 24,41 inverse order B L=10 V",
   "nslots": 10,
   "form": "V",
   "found": false,
   "margin": -0.153,
   "letters_right": 42
  },
  "F6.1 8-10/38": {
   "cls": "xstops",
   "setting": "two turns cw 96,92 order A L=10 V",
   "nslots": 10,
   "form": "V",
   "found": true,
   "margin": 0.2926,
   "letters_right": 43
  },
  "F6.1 8-10/39": {
   "cls": "xstops",
   "setting": "two turns cw 48,60 order A L=10 V",
   "nslots": 10,
   "form": "V",
   "found": true,
   "margin": 0.4107,
   "letters_right": 43
  },
  "F6.1 8-10/40": {
   "cls": "k123",
   "setting": "two turns cw 2,81 inverse order A L=9 B",
   "nslots": 9,
   "form": "B",
   "found": false,
   "margin": -0.2518,
   "letters_right": 47
  },
  "F6.1 8-10/41": {
   "cls": "k123",
   "setting": "two turns cw 34,42 order B L=10 V",
   "nslots": 10,
   "form": "V",
   "found": false,
   "margin": -0.0338,
   "letters_right": 45
  },
  "F6.1 8-10/42": {
   "cls": "k123",
   "setting": "K3 rule a=31 b=20 inverse order A L=9 V",
   "nslots": 9,
   "form": "V",
   "found": true,
   "margin": 0.5578,
   "letters_right": 42
  },
  "F6.1 8-10/43": {
   "cls": "k123",
   "setting": "two turns cw 86,60 order B L=8 V",
   "nslots": 8,
   "form": "V",
   "found": true,
   "margin": 0.5009,
   "letters_right": 61
  },
  "F6.1 8-10/44": {
   "cls": "sub3",
   "setting": "two turns cw 92,65 order B L=8 V",
   "nslots": 8,
   "form": "V",
   "found": true,
   "margin": 2.0907,
   "letters_right": 97
  },
  "F6.1 8-10/45": {
   "cls": "sub3",
   "setting": "two turns cw 79,36 inverse order A L=10 V",
   "nslots": 10,
   "form": "V",
   "found": true,
   "margin": 0.1152,
   "letters_right": 45
  },
  "F6.1 8-10/46": {
   "cls": "sub3",
   "setting": "two turns cw 46,19 inverse order B L=10 V",
   "nslots": 10,
   "form": "V",
   "found": true,
   "margin": 0.5165,
   "letters_right": 46
  },
  "F6.1 8-10/47": {
   "cls": "sub3",
   "setting": "two turns cw 24,38 order B L=8 V",
   "nslots": 8,
   "form": "V",
   "found": true,
   "margin": 1.6787,
   "letters_right": 97
  },
  "F6.1 11-26/0": {
   "cls": "clean",
   "setting": "two turns cw 90,38 inverse order B L=20 B",
   "nslots": 20,
   "form": "B",
   "found": false,
   "margin": -0.2531,
   "letters_right": 40
  },
  "F6.1 11-26/1": {
   "cls": "clean",
   "setting": "K3 rule a=85 b=16 inverse order B L=25 B",
   "nslots": 25,
   "form": "B",
   "found": true,
   "margin": 0.0281,
   "letters_right": 34
  },
  "F6.1 11-26/2": {
   "cls": "clean",
   "setting": "two turns cw 39,8 inverse order A L=19 V",
   "nslots": 19,
   "form": "V",
   "found": true,
   "margin": 0.0033,
   "letters_right": 39
  },
  "F6.1 11-26/3": {
   "cls": "clean",
   "setting": "two turns cw 95,39 order A L=24 B",
   "nslots": 24,
   "form": "B",
   "found": true,
   "margin": 0.206,
   "letters_right": 41
  },
  "F6.1 11-26/4": {
   "cls": "clean",
   "setting": "keyword SECRET (repeats dropped) order A L=17 V",
   "nslots": 17,
   "form": "V",
   "found": true,
   "margin": 0.0493,
   "letters_right": 39
  },
  "F6.1 11-26/5": {
   "cls": "clean",
   "setting": "two turns cw 85,44 order A L=20 B",
   "nslots": 20,
   "form": "B",
   "found": false,
   "margin": -0.0224,
   "letters_right": 37
  },
  "F6.1 11-26/6": {
   "cls": "clean",
   "setting": "two turns cw 43,39 order B L=11 B",
   "nslots": 11,
   "form": "B",
   "found": false,
   "margin": -0.6186,
   "letters_right": 39
  },
  "F6.1 11-26/7": {
   "cls": "clean",
   "setting": "K3 rule a=35 b=48 inverse order A L=23 V",
   "nslots": 23,
   "form": "V",
   "found": false,
   "margin": -0.1675,
   "letters_right": 30
  },
  "F6.1 11-26/8": {
   "cls": "clean",
   "setting": "two turns cw 80,13 order B L=25 V",
   "nslots": 25,
   "form": "V",
   "found": true,
   "margin": 0.1158,
   "letters_right": 45
  },
  "F6.1 11-26/9": {
   "cls": "clean",
   "setting": "two turns cw 23,76 order B L=23 V",
   "nslots": 23,
   "form": "V",
   "found": true,
   "margin": 0.265,
   "letters_right": 38
  },
  "F6.1 11-26/10": {
   "cls": "clean",
   "setting": "two turns cw 39,60 order B L=24 V",
   "nslots": 24,
   "form": "V",
   "found": true,
   "margin": 0.0693,
   "letters_right": 41
  },
  "F6.1 11-26/11": {
   "cls": "clean",
   "setting": "two turns cw 17,39 inverse order A L=19 V",
   "nslots": 19,
   "form": "V",
   "found": false,
   "margin": -0.0328,
   "letters_right": 40
  },
  "F6.1 11-26/12": {
   "cls": "clean",
   "setting": "K3 rule a=19 b=20 order A L=26 V",
   "nslots": 26,
   "form": "V",
   "found": false,
   "margin": -0.0876,
   "letters_right": 27
  },
  "F6.1 11-26/13": {
   "cls": "clean",
   "setting": "two turns cw 45,72 inverse order A L=18 V",
   "nslots": 18,
   "form": "V",
   "found": false,
   "margin": -0.1875,
   "letters_right": 37
  },
  "F6.1 11-26/14": {
   "cls": "clean",
   "setting": "K3 rule a=38 b=51 order A L=15 B",
   "nslots": 15,
   "form": "B",
   "found": true,
   "margin": 0.2101,
   "letters_right": 44
  },
  "F6.1 11-26/15": {
   "cls": "clean",
   "setting": "two turns cw 11,72 inverse order B L=26 V",
   "nslots": 26,
   "form": "V",
   "found": true,
   "margin": 0.1729,
   "letters_right": 38
  },
  "F6.1 11-26/16": {
   "cls": "clean",
   "setting": "two turns cw 62,5 order A L=24 V",
   "nslots": 24,
   "form": "V",
   "found": true,
   "margin": 0.1501,
   "letters_right": 37
  },
  "F6.1 11-26/17": {
   "cls": "clean",
   "setting": "K3 rule a=39 b=2 order A L=16 V",
   "nslots": 16,
   "form": "V",
   "found": true,
   "margin": 0.0382,
   "letters_right": 35
  },
  "F6.1 11-26/18": {
   "cls": "clean",
   "setting": "K3 rule a=86 b=3 order A L=24 B",
   "nslots": 24,
   "form": "B",
   "found": true,
   "margin": 0.1409,
   "letters_right": 42
  },
  "F6.1 11-26/19": {
   "cls": "clean",
   "setting": "K3 rule a=30 b=8 order A L=20 V",
   "nslots": 20,
   "form": "V",
   "found": true,
   "margin": 0.2611,
   "letters_right": 39
  },
  "F6.1 11-26/20": {
   "cls": "clean",
   "setting": "two turns cw 83,72 order B L=18 B",
   "nslots": 18,
   "form": "B",
   "found": true,
   "margin": 0.0302,
   "letters_right": 33
  },
  "F6.1 11-26/21": {
   "cls": "clean",
   "setting": "K3 rule a=10 b=83 inverse order A L=23 B",
   "nslots": 23,
   "form": "B",
   "found": true,
   "margin": 0.2147,
   "letters_right": 33
  },
  "F6.1 11-26/22": {
   "cls": "clean",
   "setting": "two turns cw 67,13 inverse order A L=25 V",
   "nslots": 25,
   "form": "V",
   "found": false,
   "margin": -0.1048,
   "letters_right": 39
  },
  "F6.1 11-26/23": {
   "cls": "clean",
   "setting": "two turns cw 61,56 inverse order A L=23 B",
   "nslots": 23,
   "form": "B",
   "found": false,
   "margin": -0.0496,
   "letters_right": 40
  },
  "F6.1 11-26/24": {
   "cls": "xstops",
   "setting": "K3 rule a=49 b=9 inverse order B L=22 B",
   "nslots": 22,
   "form": "B",
   "found": false,
   "margin": -0.0815,
   "letters_right": 32
  },
  "F6.1 11-26/25": {
   "cls": "xstops",
   "setting": "two turns cw 24,71 inverse order B L=25 B",
   "nslots": 25,
   "form": "B",
   "found": true,
   "margin": 0.0194,
   "letters_right": 34
  },
  "F6.1 11-26/26": {
   "cls": "xstops",
   "setting": "K3 rule a=9 b=28 order B L=18 B",
   "nslots": 18,
   "form": "B",
   "found": true,
   "margin": 0.2053,
   "letters_right": 43
  },
  "F6.1 11-26/27": {
   "cls": "xstops",
   "setting": "two turns cw 18,28 inverse order B L=23 V",
   "nslots": 23,
   "form": "V",
   "found": true,
   "margin": 0.1579,
   "letters_right": 41
  },
  "F6.1 11-26/28": {
   "cls": "k123",
   "setting": "turn ccw 74 order B L=26 V",
   "nslots": 26,
   "form": "V",
   "found": true,
   "margin": 0.0687,
   "letters_right": 41
  },
  "F6.1 11-26/29": {
   "cls": "k123",
   "setting": "two turns cw 38,54 order A L=15 B",
   "nslots": 15,
   "form": "B",
   "found": true,
   "margin": 0.2203,
   "letters_right": 44
  },
  "F6.1 11-26/30": {
   "cls": "k123",
   "setting": "two turns cw 65,67 inverse order B L=18 B",
   "nslots": 18,
   "form": "B",
   "found": true,
   "margin": 0.0065,
   "letters_right": 39
  },
  "F6.1 11-26/31": {
   "cls": "k123",
   "setting": "K3 rule a=2 b=16 inverse order B L=23 V",
   "nslots": 23,
   "form": "V",
   "found": true,
   "margin": 0.0037,
   "letters_right": 32
  },
  "F6.1 11-26/32": {
   "cls": "sub3",
   "setting": "two turns cw 45,58 order B L=20 B",
   "nslots": 20,
   "form": "B",
   "found": true,
   "margin": 0.1092,
   "letters_right": 39
  },
  "F6.1 11-26/33": {
   "cls": "sub3",
   "setting": "two turns cw 73,17 order B L=24 B",
   "nslots": 24,
   "form": "B",
   "found": true,
   "margin": 0.0997,
   "letters_right": 38
  },
  "F6.1 11-26/34": {
   "cls": "sub3",
   "setting": "two turns cw 21,91 order A L=24 V",
   "nslots": 24,
   "form": "V",
   "found": false,
   "margin": -0.0627,
   "letters_right": 33
  },
  "F6.1 11-26/35": {
   "cls": "sub3",
   "setting": "K3 rule a=8 b=44 order A L=25 V",
   "nslots": 25,
   "form": "V",
   "found": false,
   "margin": -0.0555,
   "letters_right": 36
  },
  "F6.1 11-26/36": {
   "cls": "xstops",
   "setting": "two turns cw 9,5 order B L=24 V",
   "nslots": 24,
   "form": "V",
   "found": true,
   "margin": 0.1025,
   "letters_right": 38
  },
  "F6.1 11-26/37": {
   "cls": "xstops",
   "setting": "two turns cw 82,45 order A L=23 B",
   "nslots": 23,
   "form": "B",
   "found": true,
   "margin": 0.1023,
   "letters_right": 45
  },
  "F6.1 11-26/38": {
   "cls": "xstops",
   "setting": "two turns cw 18,67 inverse order B L=25 B",
   "nslots": 25,
   "form": "B",
   "found": true,
   "margin": 0.0964,
   "letters_right": 34
  },
  "F6.1 11-26/39": {
   "cls": "xstops",
   "setting": "two turns cw 92,83 order B L=14 B",
   "nslots": 14,
   "form": "B",
   "found": false,
   "margin": -0.0352,
   "letters_right": 40
  },
  "F6.1 11-26/40": {
   "cls": "k123",
   "setting": "K3 rule a=65 b=20 order B L=25 V",
   "nslots": 25,
   "form": "V",
   "found": false,
   "margin": -0.0804,
   "letters_right": 32
  },
  "F6.1 11-26/41": {
   "cls": "k123",
   "setting": "two turns cw 61,5 order B L=23 B",
   "nslots": 23,
   "form": "B",
   "found": true,
   "margin": 0.088,
   "letters_right": 35
  },
  "F6.1 11-26/42": {
   "cls": "k123",
   "setting": "two turns cw 83,51 inverse order B L=13 B",
   "nslots": 13,
   "form": "B",
   "found": true,
   "margin": 0.2463,
   "letters_right": 48
  },
  "F6.1 11-26/43": {
   "cls": "k123",
   "setting": "two turns cw 29,19 inverse order A L=26 B",
   "nslots": 26,
   "form": "B",
   "found": false,
   "margin": -0.1264,
   "letters_right": 29
  },
  "F6.1 11-26/44": {
   "cls": "sub3",
   "setting": "K3 rule a=92 b=60 order B L=24 B",
   "nslots": 24,
   "form": "B",
   "found": true,
   "margin": 0.2069,
   "letters_right": 39
  },
  "F6.1 11-26/45": {
   "cls": "sub3",
   "setting": "two turns cw 67,46 inverse order B L=14 B",
   "nslots": 14,
   "form": "B",
   "found": true,
   "margin": 0.2351,
   "letters_right": 43
  },
  "F6.1 11-26/46": {
   "cls": "sub3",
   "setting": "K3 rule a=83 b=24 inverse order B L=21 V",
   "nslots": 21,
   "form": "V",
   "found": false,
   "margin": -0.2766,
   "letters_right": 29
  },
  "F6.1 11-26/47": {
   "cls": "sub3",
   "setting": "two turns cw 38,27 order B L=26 B",
   "nslots": 26,
   "form": "B",
   "found": true,
   "margin": 0.1238,
   "letters_right": 39
  }
 },
 "climbs_without_start": 0,
 "texts_climbed": 1344,
 "compute_seconds": 869,
 "exhaustive": false,
 "expected_total_time": "about 1,350 one-run climbs at about 17 s (0229) = about 6.4 core-hours, plus the exact counts"
}
```

Notes: power pooled: F1.4 skip [37, 48], F1.4 other [37, 48], F6.1 8-10 [31, 48], F6.1 11-26 [32, 48]; cost: F1.4 skip 2016 settings 39.1 core-h, F1.4 other 77 settings 1.5 core-h, F6.1 6-10 7443 settings 247.7 core-h, F6.1 11-26 435693 settings 7648.8 core-h


