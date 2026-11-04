# 0269-f1.14-gate-ten-runs-against-four-on-0267s-own-plants: F1.14's gate: 0267's 24 plants (hand key schedules on two free alphabets) and 12 kept-place copies each, climbed ten times, power after r runs for r = 1-10

**Family:** 1-keyed-periodic  
**Parent:** 0267-f1.4-two-alphabet-residue-decided-by-four-runs-with-stand-ins  
**Decision:** reverted  
**Run:** 2026-11-04T20:11:36+00:00, 1306.4 s, status ran  
**Time by phase:** test 1237 s, run 1306 s, record 0 s

## In plain words

Last run, our search found only half of the test messages we hid, in a version of the cipher where Sanborn steps through his key word with a twist and uses two scrambled alphabets. Searching each text ten times instead of four might find more. Before paying for the full ten-times rerun, we check on the same 24 hidden messages whether ten searches find at least three more than four.

## Walkthrough, by hand

1. Take one of 0267's hidden test messages, enciphered with a skipping key schedule and two scrambled alphabets.
2. Make 12 copies with the 73 letters at unknown places shuffled.
3. Search each of the 13 texts ten separate times for its most English-looking reading; write down each search's best.
4. For r = 1 to 10, compare the message's best of its first r searches with each copy's best of its first r.
5. Count the messages that beat all 12 copies at r = 4 and at r = 10.

## Worked example (generated)

```
F1.14's gate: does searching ten times instead of four find more hidden messages?

  one hidden message and its 12 shuffled copies, each searched ten times; best of the first r searches:
  found at r when the message's best beats all 12 copies' bests.
  24 messages (0267's own); run the full rerun only if r = 10 finds at least 3 more than r = 4.
```

## Lineage

Inherits from 0267-f1.4-two-alphabet-residue-decided-by-four-runs-with-stand-ins. What changed: F1.14 (rerun of F1.4's two-alphabet residue at ten runs) waits on this gate: does ten runs lift 0267's plants by 3 or more of 24 over four? 0267's plants are regenerated exactly (its frozen setting scan and plant draws), and each plant and 12 kept-place copies (from the plant's own witness, as 0267) are climbed with ten independent runs of 0267's generalised tempering, every run's best kept, as D1b (0257) did for periodic keys.

## Hypothesis (domain expert)

0267 found 12 of 24 plants (8 clean, 4 Sanborn-style) with D1b's four runs on hand key schedules (0128's skip, stutter, back and forth, triangle, square, restart per line) over two free alphabets (Quagmire IV), against D1b's 66 of 96 for periodic keys at 13 and 16. The settings here have up to 31 slots, so the climb has more key letters to find and may profit more from extra runs than D1b measured (+5 of 96 from four to ten). The gate set in F1.14's row: run F1.14 (about $25 on AWS) only if ten runs find at least 3 more of these 24 than four. Clue entries C20(d), C27(c).

## Prediction

Four runs find 11-13 of 24 (0267: 12); ten runs find 1-3 more (D1b's +5 of 96 scaled, a little more for the longer keys). Gate likely not met. Zero candidates.

## Method

1. 0267's run() steps 1-2 unchanged from its frozen attack.py: every 0128 schedule decided exactly on K4 on two free alphabets (4,706 fit), then its 24 plants (12 clean, 12 Sanborn-style) drawn on fitting settings with its seed, each with an exact witness.
2. Per plant: the plant and 12 kept-place copies of its ciphertext, each climbed with 10 independent runs of 0267's climb (one run per seed), every run's best score kept.
3. Found after r runs: the plant's best of runs 1..r above all 12 copies' bests of runs 1..r.
4. Gate: found(10) - found(4) >= 3.

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
 "item": "F1.14 gate",
 "settings_fit_k4": 4706,
 "plants_match_0267_settings": 24,
 "plants": 24,
 "own_copies": 12,
 "null_per_plant": "1/13",
 "decider": "0267's climb (0144's tempering generalised to any slot map, 16 x 625 x 1000 per run) from the plant's exact witness",
 "runs": 10,
 "power_by_runs": {
  "1": {
   "clean": 8,
   "sanborn": 6,
   "total": 14
  },
  "2": {
   "clean": 7,
   "sanborn": 7,
   "total": 14
  },
  "3": {
   "clean": 6,
   "sanborn": 6,
   "total": 12
  },
  "4": {
   "clean": 6,
   "sanborn": 6,
   "total": 12
  },
  "5": {
   "clean": 7,
   "sanborn": 6,
   "total": 13
  },
  "6": {
   "clean": 8,
   "sanborn": 5,
   "total": 13
  },
  "7": {
   "clean": 8,
   "sanborn": 5,
   "total": 13
  },
  "8": {
   "clean": 9,
   "sanborn": 5,
   "total": 14
  },
  "9": {
   "clean": 9,
   "sanborn": 5,
   "total": 14
  },
  "10": {
   "clean": 9,
   "sanborn": 5,
   "total": 14
  }
 },
 "gain_10_over_4": 2,
 "gate": 3,
 "gate_met": false,
 "record_0267_plants": "8/12 clean, 4/12 Sanborn-style at four runs, copies one at a time",
 "each": {
  "0": {
   "cls": "clean",
   "setting": "B skip m=26 phi=18 n=8",
   "slots": 8,
   "found_at_4": true,
   "found_at_10": true,
   "letters_right_10": 53
  },
  "1": {
   "cls": "clean",
   "setting": "B skip m=9 phi=0 n=23",
   "slots": 23,
   "found_at_4": false,
   "found_at_10": false,
   "letters_right_10": 29
  },
  "2": {
   "cls": "clean",
   "setting": "B skip m=16 phi=15 n=19",
   "slots": 19,
   "found_at_4": false,
   "found_at_10": false,
   "letters_right_10": 36
  },
  "3": {
   "cls": "clean",
   "setting": "B skip m=28 phi=19 n=19",
   "slots": 19,
   "found_at_4": true,
   "found_at_10": true,
   "letters_right_10": 41
  },
  "4": {
   "cls": "clean",
   "setting": "B skip m=19 phi=5 n=26",
   "slots": 26,
   "found_at_4": true,
   "found_at_10": false,
   "letters_right_10": 36
  },
  "5": {
   "cls": "clean",
   "setting": "B skip m=13 phi=10 n=13",
   "slots": 13,
   "found_at_4": false,
   "found_at_10": true,
   "letters_right_10": 49
  },
  "6": {
   "cls": "clean",
   "setting": "B skip m=25 phi=7 n=12",
   "slots": 12,
   "found_at_4": false,
   "found_at_10": true,
   "letters_right_10": 38
  },
  "7": {
   "cls": "clean",
   "setting": "B skip m=17 phi=7 n=20",
   "slots": 20,
   "found_at_4": true,
   "found_at_10": true,
   "letters_right_10": 35
  },
  "8": {
   "cls": "clean",
   "setting": "B skip m=25 phi=12 n=8",
   "slots": 8,
   "found_at_4": true,
   "found_at_10": true,
   "letters_right_10": 47
  },
  "9": {
   "cls": "clean",
   "setting": "B skip m=17 phi=3 n=14",
   "slots": 14,
   "found_at_4": false,
   "found_at_10": true,
   "letters_right_10": 34
  },
  "10": {
   "cls": "clean",
   "setting": "B skip m=29 phi=6 n=12",
   "slots": 12,
   "found_at_4": true,
   "found_at_10": true,
   "letters_right_10": 40
  },
  "11": {
   "cls": "clean",
   "setting": "B skip m=21 phi=3 n=14",
   "slots": 14,
   "found_at_4": false,
   "found_at_10": true,
   "letters_right_10": 39
  },
  "12": {
   "cls": "xstops",
   "setting": "B skip m=28 phi=11 n=12",
   "slots": 12,
   "found_at_4": true,
   "found_at_10": true,
   "letters_right_10": 42
  },
  "13": {
   "cls": "xstops",
   "setting": "B skip m=30 phi=18 n=21",
   "slots": 21,
   "found_at_4": false,
   "found_at_10": false,
   "letters_right_10": 36
  },
  "14": {
   "cls": "xstops",
   "setting": "B skip m=27 phi=3 n=24",
   "slots": 24,
   "found_at_4": false,
   "found_at_10": false,
   "letters_right_10": 38
  },
  "15": {
   "cls": "xstops",
   "setting": "B skip m=11 phi=0 n=26",
   "slots": 26,
   "found_at_4": true,
   "found_at_10": true,
   "letters_right_10": 39
  },
  "16": {
   "cls": "xstops",
   "setting": "B skip m=26 phi=2 n=17",
   "slots": 17,
   "found_at_4": true,
   "found_at_10": true,
   "letters_right_10": 41
  },
  "17": {
   "cls": "xstops",
   "setting": "B skip m=27 phi=22 n=20",
   "slots": 20,
   "found_at_4": false,
   "found_at_10": false,
   "letters_right_10": 28
  },
  "18": {
   "cls": "xstops",
   "setting": "B skip m=27 phi=22 n=25",
   "slots": 25,
   "found_at_4": false,
   "found_at_10": false,
   "letters_right_10": 34
  },
  "19": {
   "cls": "xstops",
   "setting": "B skip m=22 phi=0 n=21",
   "slots": 21,
   "found_at_4": false,
   "found_at_10": false,
   "letters_right_10": 35
  },
  "20": {
   "cls": "xstops",
   "setting": "B skip m=23 phi=22 n=26",
   "slots": 26,
   "found_at_4": true,
   "found_at_10": true,
   "letters_right_10": 34
  },
  "21": {
   "cls": "xstops",
   "setting": "B skip m=3 phi=1 n=21",
   "slots": 21,
   "found_at_4": true,
   "found_at_10": true,
   "letters_right_10": 33
  },
  "22": {
   "cls": "xstops",
   "setting": "B skip m=27 phi=2 n=12",
   "slots": 12,
   "found_at_4": true,
   "found_at_10": false,
   "letters_right_10": 44
  },
  "23": {
   "cls": "xstops",
   "setting": "D back and forth n=15 ends=repeated phi=0",
   "slots": 15,
   "found_at_4": false,
   "found_at_10": false,
   "letters_right_10": 34
  }
 },
 "texts": 312,
 "core_seconds": 37508,
 "compute_seconds": 1249,
 "resumed_units": 0,
 "exhaustive": false,
 "cost_estimate": "312 texts x 10 runs x about 13 s = about 11 core-hours, plus 0267's setting scan; on AWS about 30 min, about $0.30"
}
```

Notes: F1.14 gate: 0267's plants found after 4 runs 12/24, after 10 14/24 (gain 2, gate 3: not met, F1.14 closed); power by runs [14, 14, 12, 12, 13, 13, 13, 14, 14, 14].


