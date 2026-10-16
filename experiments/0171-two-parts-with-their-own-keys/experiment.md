# 0171-two-parts-with-their-own-keys: F12.5: K4 as two parts with their own repeating keys, split between the two known runs, on the sculpture's tables: exact, with the checks each part leaves

**Family:** 12-steins-way  
**Parent:** 0005-quagmire-period-sweep-forced-keys  
**Decision:** reverted  
**Run:** 2026-10-16T23:04:58+00:00, 0.1 s, status ran  
**Time by phase:** unattributed 39 s, run 0 s, record 0 s

## In plain words

K1 and K2 used different secret words. Perhaps K4's two halves did too: one word for the part with EAST NORTHEAST, another for the part with BERLIN CLOCK. Then each known word can only test its own half's secret word, and only word lengths shorter than itself. We check every length that can be checked, on the sculpture's tables, and on scrambled copies.

## Walkthrough, by hand

1. Take EASTNORTHEAST at places 22-34 and a first secret word of length 5.
2. Places 22 and 27 share a slot (27 - 22 = 5): on the table, E over F and O over Q must ask for the same key letter.
3. Check every pair five apart inside the run, and the same for every length up to 12.
4. Do the same for BERLINCLOCK with the second word, lengths up to 10.
5. Repeat on scrambled copies.

## Worked example (generated)

```
part 1, sculpture's table (KRYPTOS alphabets), Vigenere: key value forced at each place of EASTNORTHEAST

place 22: E under F -> key  1, slot at length 5: 0
place 23: A under L -> key 10, slot at length 5: 1
place 24: S under R -> key 21, slot at length 5: 2
place 25: T under V -> key 18, slot at length 5: 3
place 26: N under Q -> key  1, slot at length 5: 4
place 27: O under Q -> key 15, slot at length 5: 0
place 28: R under P -> key  2, slot at length 5: 1
place 29: T under R -> key 23, slot at length 5: 2
place 30: H under N -> key  5, slot at length 5: 3
place 31: E under G -> key  2, slot at length 5: 4
place 32: A under K -> key 19, slot at length 5: 0
place 33: S under S -> key  0, slot at length 5: 1
place 34: T under S -> key  2, slot at length 5: 2
```

## Lineage

Inherits from 0005-quagmire-period-sweep-forced-keys. What changed: F12.5 (assumption A7: one key for the whole text). Stein found K1 and K2 used different keys in different parts of the panel. F12.2 and F12.4 found no break inside K4, so the split is at the known stretches: a first part holding EASTNORTHEAST and a second holding BERLINCLOCK, each with its own repeating key of length 1-26 on one of the 8 standard/KRYPTOS table classes. With separate keys the split point does not matter for consistency (a key's slots inside one run depend only on distances), and each run checks only keys shorter than itself: 13 letters check lengths 1-12, 11 letters check 1-10. The checks each length leaves are stated; ten scrambled coppers.

## Hypothesis (domain expert)

Assumption A7 (knowledge/12-assumptions.md, for information), Stein 1999 (parts with their own keys: ABSCISSA and PALIMPSEST), C5(b) ('key word/s'). Model: c_i = T(p_i, k1[i mod a]) for i in part 1, T(p_i, k2[(i - s) mod b]) in part 2, T one of 8 classes (plain and cipher alphabets standard or KRYPTOS, Beaufort or not). Checks for part 1 at length a: 13 - (distinct slots of places 22-34 mod a); part 2: 11 - (distinct slots of 64-74 mod b). A length is live if no slot holds two different forced key letters. Statistic: live (class, length) cells per part with at least one check, K4 against the coppers' range.

## Prediction

No length below 11-13 is live on K4 in either part at more than the coppers' rate (the periodic sweep 0005 already fails at these lengths with one key; separate keys loosen it only by the cross-run checks). Zero candidates.

## Method

1. For each text, table class and part: the forced key value at each known place of that part.
2. For lengths 1-12 (part 1) and 1-10 (part 2): live if each slot holds one value; count checks.
3. Compare live cells on K4 with ten coppers.

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
 "family": "two parts with separate repeating keys (split between the runs), standard/KRYPTOS tables, lengths up to the run length - 1",
 "summary": {
  "part 1 (EASTNORTHEAST, 22-34)": {
   "k4_live_lengths": [],
   "k4_live_cells": 0,
   "coppers_live_cells": [
    0,
    1,
    0,
    0,
    0,
    1,
    0,
    0,
    0,
    0
   ],
   "checks_by_length": {
    "1": 12,
    "2": 11,
    "3": 10,
    "4": 9,
    "5": 8,
    "6": 7,
    "7": 6,
    "8": 5,
    "9": 4,
    "10": 3,
    "11": 2,
    "12": 1
   }
  },
  "part 2 (BERLINCLOCK, 64-74)": {
   "k4_live_lengths": [],
   "k4_live_cells": 0,
   "coppers_live_cells": [
    0,
    0,
    0,
    1,
    1,
    0,
    1,
    0,
    0,
    0
   ],
   "checks_by_length": {
    "1": 10,
    "2": 9,
    "3": 8,
    "4": 7,
    "5": 6,
    "6": 5,
    "7": 4,
    "8": 3,
    "9": 2,
    "10": 1
   }
  }
 },
 "k4_live": [],
 "controls": "10 shuffled coppers (seed 1615)",
 "exhaustive": true
}
```

Notes: part 1 (EASTNORTHEAST, 22-34): K4 live lengths [] (0 cells), coppers 0-1; part 2 (BERLINCLOCK, 64-74): K4 live lengths [] (0 cells), coppers 0-1


