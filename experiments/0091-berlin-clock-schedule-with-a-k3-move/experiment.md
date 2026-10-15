# 0091-berlin-clock-schedule-with-a-k3-move: The Berlin clock as a key schedule, joined to a K3-style move before or after the table

**Family:** 6-transposition-then-tableau  
**Parent:** 0079-berlin-clock-as-a-key-schedule  
**Decision:** reverted  
**Run:** 2026-10-15T18:59:29+00:00, 758.4 s, status ran  
**Time by phase:** unattributed 398 s, run 758 s, record 0 s

## In plain words

Experiment 79 used the Berlin clock as the key: set it to some time, read off a number for each letter, and move the clock on by a fixed number of minutes per letter. It found nothing. Sanborn also said he moved letters around in grids before going back to the table, so here every clock key is joined to every grid move of experiments 80 to 83, with the move before or after the table. A clock key has no free letters, so each combination either explains all 24 known letters or it does not.

## Walkthrough, by hand

1. Set the clock to 00:00 and advance it one minute per letter; the key number for a letter is the count of lit lamps.
2. Pick a move, say a clockwise quarter turn of a grid 8 letters wide.
3. Change then move: E of place 22 ends up at some carved place j; find the number that turns E into the carved letter there.
4. That number minus the lamp count at place 22 must be the same for all 24 known places.
5. Move then change: the clock runs along the carved text instead, so compare the needed number with the lamp count at place j.
6. Repeat for every start minute, step, clock reading, move and table rule.

## Worked example (generated)

```
clock from 00:00, one minute per letter, lit lamps; move: clockwise quarter turn of a grid 8 wide;
sculpture's alphabet, Vigenere

change then move: needed number minus lamps at the message place must be constant
place  known  moved to  carved  needed  lamps  difference
   22      E        71       Z      14      5           9
   23      A        83       C       2      6          22
   24      S        95       C       3      7          22
   25      T        10       H      10      8           2
   64      B        90       U      13      4           9

move then change: the lamps are read at the carved place instead
place  known  moved to  carved  needed  lamps  difference
   22      E        71       Z      14      3          11
   23      A        83       C       2      7          21
   24      S        95       C       3     11          18
   25      T        10       H      10      5           5
   64      B        90       U      13     10           3
```

## Lineage

Inherits from 0079-berlin-clock-as-a-key-schedule. What changed: 0079 read the key off the set-theory clock with no move. Here each of its 60,480 schedules (six readings, seven steps, every start minute) is joined to every move of the type-1 route library (27,852 distinct routes), the move either before the table or after it. A schedule plus a constant leaves no free letter, so both orders are exact tests.

## Hypothesis (domain expert)

Type 6 of directions.md: 'the same schedules combined with a moving stage (type 1)'. Scheidt: the system is 'simple, can be remembered' (C5); Sanborn pointed at the Mengenlehreuhr in 2014 and said BERLINCLOCK is a clue (C14, C11a). Schedules as in 0079: lit lamps, hour, minute, hour plus minute, the five-minute row and the time's digits, the clock advancing 1, 2, 3, 5, 10, 15 or 30 minutes per letter from every start minute, key value mod 26 plus one free constant. Moves as in 0090 (K3's rule, one or two quarter turns, plain and true-keyword columnar, forward and inverse). Change then move: the 23 key differences forced at the crib places must equal the schedule's, a dictionary lookup. Move then change: the clock runs over carved places, so the forced differences sit at the moved crib places; candidates come from a pair index and are filtered check by check (the time-digit reading only at one minute per letter here, where it is a cyclic text). 12 conventions (Vigenere, Beaufort, variant Beaufort; plain and cipher numbered on standard or KRYPTOS). The Carter and dedication dates of 0038 are periodic keys of period at most 10 and are covered exactly by 0080 and 0083. Ten shuffled coppers.

## Prediction

No combination explains all 24 known letters in either order. Change then move: no schedule matches either whole crib stretch beyond the scrambled-copper count. Move then change: the deepest partial match is about 6-8 checks, inside the scrambled-copper range. Zero candidates.

## Method

1. Build the 60,480 clock schedules and the deduplicated route library.
2. Change then move: for each route and convention, undo the move at the 24 crib places, compute the forced key numbers and their differences from the first, and look them up in an index of every schedule's differences at the crib places (all 24, and each crib stretch alone).
3. Move then change: for each clock reading and step, find the start minutes that agree at the first two moved crib places through a pair index, then filter by the other places, recording the deepest agreement.
4. K4 first, then ten shuffled coppers as time allows.
5. Decrypt and return any full match.

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
 "routes_distinct": 27852,
 "conventions": 12,
 "schedules": 60480,
 "readings": [
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
 "start_minutes": 1440,
 "change_then_move": {
  "k4_full": 0,
  "controls_full": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  "k4_stretch13": 0,
  "controls_stretch13": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  "k4_stretch11": 0,
  "controls_stretch11": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  "k4_stretch_hits": []
 },
 "move_then_change": {
  "clock_families": 36,
  "time_digits_steps": [
   1
  ],
  "k4_full": 0,
  "k4_best_depth": 7,
  "controls_best_depth": [
   7,
   7,
   7,
   7,
   7,
   7,
   7,
   7,
   7,
   7
  ],
  "controls_completed": 10,
  "k4_depth_histogram": {
   "1": 10513339,
   "2": 1352764,
   "3": 145672,
   "4": 19110,
   "5": 1123,
   "6": 54,
   "7": 2
  },
  "k4_top": []
 },
 "carter_dates": "periodic keys of period at most 10: covered exactly by 0080 and 0083",
 "controls": "10 shuffled coppers (seed 91), identical search"
}
```

Notes: 27,852 routes x 12 conventions x 60,480 clock schedules. Change then move: full K4 0, controls [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]; EASTNORTHEAST stretch 0 (controls [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]); BERLINCLOCK stretch 0 (controls [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]). Move then change: full 0, deepest K4 7, controls [7, 7, 7, 7, 7, 7, 7, 7, 7, 7] (10 completed).


