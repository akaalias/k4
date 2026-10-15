# 0079-berlin-clock-as-a-key-schedule: The Berlin clocks as the key: lamp counts of the set-theory clock and the hours on the World Clock, minute by minute

**Family:** 1-keyed-periodic  
**Parent:** 0011-progressive-key-period-sweep  
**Decision:** reverted  
**Run:** 2026-10-15T13:45:08+00:00, 37.0 s, status ran  
**Time by phase:** design 41 s, implement 0 s, test 16 s, run 37 s, record 0 s

## In plain words

Berlin has a famous set-theory clock that tells the time with rows of lamps, and the World Clock where the crowds met when the Wall fell. Sanborn told people to 'delve into that particular clock'. Perhaps the key is the clock itself: start it at some minute, move it on a fixed amount for each letter, and use the number of lit lamps, or the hour, or the minutes, as the shift for that letter. Each such key is completely fixed by its starting time, so the 24 known letters test every one of them exactly.

## Walkthrough, by hand

1. Start the set-theory clock at midnight and move it one minute per letter, so place 22 shows 00:21 and place 23 shows 00:22.
2. At 00:21 the lamps lit are none for the hours, four five-minute lamps and one minute lamp: 5. At 00:22: 4 + 2 = 6.
3. On the sculpture's alphabet with Vigenere, place 22 needs total key F (12) minus E (11) = 1, so the constant is 1 - 5 = -4, which is 22.
4. Place 23 needs L (17) minus A (7) = 10, so the constant is 10 - 6 = 4.
5. 22 and 4 disagree: dead.
6. Repeat for every start minute, step, schedule and table.

## Worked example (generated)

```
set-theory clock from 00:00, one minute per letter, lit lamps as the key; sculpture's alphabet, Vigenere

place  time   lamps  needed  constant
   22  00:21      5       1        22
   23  00:22      6      10         4
   24  00:23      7      21        14
   25  00:24      8      18        10
```

## Lineage

Inherits from 0011-progressive-key-period-sweep. What changed: Sanborn told solvers to 'delve into that particular clock' (the Mengenlehreuhr, 2014) and later said the Berlin Clock is the World Clock (2025). Here the clocks themselves drive the key: as the time advances by a fixed step per letter, the key is the number of lit lamps, the hour, the minute, their sum, or the digits of the time, from every starting minute of the day. Every schedule is fully fixed by its start, so the 24 known letters test it exactly.

## Hypothesis (domain expert)

Family 1, a key schedule from the clocks (C12(b); 02-sanborn-said.md 2014 'delve into that particular clock... a lot of fodder there', 2025 'the Berlin Clock in K4 is the World Clock'). Mengenlehreuhr state at minute t of the day: a = hour div 5 and b = hour mod 5 (rows of four), c = minute div 5 (row of eleven) and d = minute mod 5 (row of four). Schedules: total lit lamps a+b+c+d (0-23), the hour, the minute, hour plus minute, the clock's five-minute row c, and the digit stream of the time HHMM read minute after minute. The time advances by s minutes per letter, s in {1, 2, 3, 5, 10, 15, 30}, from every start minute 0-1439. Weltzeituhr readings: the 24 facets read in turn give a period-24 key and a 24-letter ring is excluded by 0052, so only the minute-driven schedules are new; a step of 60 minutes gives period 24, dead by the crib sweep. Key value v added to (Vigenere), subtracted from (variant) or used Beaufort-style, with any constant offset, plain and cipher alphabets standard or KRYPTOS. A schedule survives only if all 24 residuals agree (23 checks); the closest fit is reported as mismatches against the most common residual, with ten shuffled coppers.

## Prediction

No schedule, step, start and setup makes all 24 known letters agree; the closest fit leaves about as many mismatches as on the ten shuffled coppers. Zero candidates pass.

## Method

1. For each schedule, step and start minute, compute the key value under each known place.
2. For each setup, subtract (or add) it from the total key the known letter needs; the residuals must all be the same constant.
3. Record survivors and the fewest mismatches.
4. Repeat on ten shuffled coppers.

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
 "family": "Berlin clock key schedules",
 "schedules": [
  "lit lamps",
  "hour",
  "minute",
  "hour plus minute",
  "five-minute row",
  "time digits"
 ],
 "steps_minutes": [
  1,
  2,
  3,
  5,
  10,
  15,
  30
 ],
 "starts": 1440,
 "setups": 12,
 "trials": 725760,
 "k4_best_agreeing": 8,
 "k4_fewest_mismatches": 16,
 "survivors": [],
 "controls_fewest_mismatches": [
  16,
  16,
  16,
  16,
  17,
  16,
  16,
  16,
  17,
  16
 ]
}
```

Notes: 725,760 trials. K4: at most 8 of 24 residuals agree (fewest mismatches 16); survivors 0. Ten shuffled coppers: fewest mismatches [16, 16, 16, 16, 17, 16, 16, 16, 17, 16].


