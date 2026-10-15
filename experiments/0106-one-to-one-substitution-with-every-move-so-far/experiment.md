# 0106-one-to-one-substitution-with-every-move-so-far: A one-to-one letter substitution with every move built so far: paths, mixed turns, triple turns and the type-1 library

**Family:** 9-substitution-then-transposition  
**Parent:** 0019-substitution-then-route-crib-images-one-to-one  
**Decision:** reverted  
**Run:** 2026-10-15T20:16:52+00:00, 22.6 s, status ran  
**Time by phase:** unattributed 92 s, run 23 s, record 0 s

## In plain words

The simplest two-step cipher swaps each letter for another by a fixed table and then moves the letters around. Experiment 19 tried this with about 24,000 ways of moving letters. Since then we have built ways of moving letters by the million. For each one we check whether a single swap table can turn the known letters into the carved letters where they land: the same letter must always become the same letter.

## Walkthrough, by hand

1. Pick a move, say snake rows of 10 read by columns.
2. Find where each known letter lands and read the carved letter there.
3. E occurs three times among the known letters (places 22, 31 and 65): all three must land on the same carved letter.
4. And two different known letters must never land on the same carved letter.
5. Repeat for every move in the four sets and on scrambled coppers.

## Worked example (generated)

```
snake rows of 10, read by columns: the known letters and the carved letters where they land

letter  places (lands at: carved)
     A  23 (23: L), 32 (83: C)
     B  64 (37: W)
     C  70 (95: C), 73 (78: K)
     E  22 (13: B), 31 (92: U), 65 (47: Z)
     H  30 (91: A)
     I  68 (77: D)
     K  74 (68: T)
     L  67 (67: V), 71 (96: A)
     N  26 (53: K), 69 (86: G)
     O  27 (63: B), 72 (87: K)
     R  28 (73: P), 66 (57: I)
     S  24 (33: S), 33 (74: K)
     T  25 (43: S), 29 (82: J), 34 (64: N)

a single swap table needs every row to show one carved letter, different from every other row
```

## Lineage

Inherits from 0019-substitution-then-route-crib-images-one-to-one. What changed: 0019 tested a monoalphabetic substitution with 23,931 routes. Since then experiments 80-99 built far larger move sets: the type-1 library (27,852), grid paths (43,579), mixed-sense double turns (53,743) and every triple clockwise turn (1.7 million). A one-to-one substitution commutes with any move, so one test covers both orders: the known letters must land on carved letters that a single one-to-one table can explain.

## Hypothesis (domain expert)

Family 9 (least covered, two experiments), open 'only for routes outside the set (spirals, diagonals, keyed routes)' (families.md); 0018 found substitution-then-transposition the only construction reproducing the width-21 repeats. Model: c = route(sigma(p)) = sigma(route(p)), sigma any permutation of 26 letters. Test: for the 24 known letters at their landing places, equal message letters must land on equal carved letters and different on different. Route sets: the type-1 library (K3's rule, one and two clockwise turns, plain and true-keyword columnar, forward and inverse); 0092's 30 x 29 path pairs at widths 2-96; 0099's mixed-sense double turns; 0083's triple clockwise turns at widths 2-96; all deduplicated. Ten shuffled coppers. Survivors decrypt wherever sigma is fixed and are scored.

## Prediction

No route of any set survives on K4, and none on the shuffled coppers, as in 0019. Zero candidates.

## Method

1. Build the four route sets and deduplicate (by a 64-bit hash of each route).
2. For each route and text, map each known letter to the carved letter at its landing place; reject on a clash.
3. Count survivors per set on K4 and ten shuffled coppers.
4. Decrypt survivors where the table is fixed and score them.

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
 "family": "one-to-one substitution (commutes with the move) with four route sets",
 "routes_by_set": {
  "type-1 library": 27852,
  "grid paths": 42978,
  "mixed double turns": 53214,
  "triple clockwise turns": 1711697
 },
 "stopped": null,
 "consistent_by_set": {},
 "k4_survivors": [],
 "n_k4_survivors": 0,
 "controls": "10 shuffled coppers (seed 106), identical test"
}
```

Notes: Routes tested: {'type-1 library': 27852, 'grid paths': 42978, 'mixed double turns': 53214, 'triple clockwise turns': 1711697}. Consistent (K4 / controls): none on any text.


