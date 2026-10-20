# 0211-running-keys-through-the-shifts-and-moves-with-slips: A1.3, with moves: 0117's running keys from the sculpture's texts and Carter, plus any constant shift of the table, with or without every type-1 move, either order, allowing up to three of the 24 known letters to be slips, exact, against scrambled copies, with planted slipped messages

**Family:** 1-keyed-periodic  
**Parent:** 0117-running-keys-through-all-the-shifts  
**Decision:** reverted  
**Run:** 2026-10-20T12:59:06+00:00, 275.7 s, status ran  
**Time by phase:** implement 101 s, test 558 s, run 276 s, record 0 s

## In plain words

Experiment 117 took the sculpture's own texts as a long key, let the whole table slide by any of 26 places, and tried it with and without the grid scrambles of experiments 80-83. Nothing gave the 24 known letters. Here the same search allows Sanborn up to three slips at those 24 places, on the carving and on scrambled copies, with two messages of our own hidden the same way, slips included, to check the search finds them.

## Walkthrough, by hand

1. Take the four ciphertexts as the key text, from some offset, and the KRYPTOS table with Vigenere.
2. At each known place, the key needed is the carved letter minus the known letter, and the key text offers its own letter.
3. With a constant shift, needed minus offered must come out the same at every known place.
4. Allow up to 3 places where it does not: those would be Sanborn's slips.
5. Slide the offset, and repeat for every text, rule, and every grid scramble before or after the table.

## Worked example (generated)

```
key text: the four ciphertexts as one panel, offset 0; KRYPTOS table, Vigenere, no move

place  known  carved  needed  offered  needed - offered
   22      E       F       1        0                1
   23      A       L      10        1                9
   24      S       R      21       19                2
   25      T       V      18        6               12
   64      B       N      11       22               15
   65      E       Y      17       12                5
   74      K       K       0       23                3

the most common value of the last column covers 2 of 24 places; a shift with 3 slips needs 21
```

## Lineage

Inherits from 0117-running-keys-through-all-the-shifts. What changed: A1.3 (Stage 2, step 2, issue #76), the part 0210 left out: 0117 required all 24 known letters (change then move: the 23 key differences matched by hash; move then change: a pair index filtered check by check, deepest 8 of 24). Here both orders allow up to 3 failed checks: change then move by a pigeonhole index (4 blocks of 6 known places; 3 slips leave one block whole, whose 5 key differences are looked up), move then change by 4 disjoint pairs of known places (3 slips leave one pair whole, looked up by its key difference at its gap). Both compiled; same sources, numberings, 12 conventions and 0117's route library unchanged; K4 against 10 scrambled copies; two planted messages (one per order) with 3 and 2 slips.

## Hypothesis (domain expert)

C2(b) (Sanborn 2003: 'surprised that no one had tried recovering the original matrix and running it through all the possible shifts'), C6(a) (keys concealed at the sculpture), C1(a) (a matrix stage), with A1 (knowledge/12-assumptions.md) and C27(a) (the PALIMPCEST slip). Model as 0117: c = E(p, y[o + i] + s) for a key text y numbered on the standard or KRYPTOS alphabet, offset o, constant s 0-25, E one of 12 conventions (Vigenere, Beaufort, variant; plain and cipher alphabets standard or KRYPTOS); with a type-1 move before the table (move then change: key aligned to carved places) or after it (change then move: key aligned to message places); key texts the carved tableau (rows, rows with index, columns), the Morse (carved, reversed order), the four ciphertexts, K1-K3 plaintexts, Sanborn's 1989 letter, the 1991 dedication texts, the 2025 open letter, forward and backward, every cyclic offset; Carter's book in the change-then-move order only (as 0117). A slip at known place q makes its equation fail; settings with at most 3 failures are counted, K4 against each copy. Chance of any setting with 3 or fewer slips on a text: about 10^-15 (change then move, 4 x 10^11 trials) and 10^-17 (move then change), so the 24 checks decide at k <= 3.

## Prediction

No setting with 3 or fewer slips on K4 or on any copy, in either order. Both planted messages are found at their own route, convention, key text, offset and shift, with exactly their slips. Zero candidates on K4.

## Method

1. Build 0117's key texts (both numberings) and route library.
2. Change then move: index every offset of every key text by the 5 key differences inside each of 4 blocks of 6 known places; for each route, convention and text, compute the key each known place needs and look up its block differences; check every offset found on all 24 places with the shift its clean block gives.
3. Move then change: for 4 disjoint pairs of known places, the moved places' gap and needed key difference are looked up in a per-gap index of each key text; check every offset found on all 24.
4. Keep settings with at most 3 failures.
5. K4, 10 copies, two plants with 5 copies each.

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
 "family": "0117's running keys plus a constant shift, with or without a type-1 move, either order, 0-3 known letters slipped (A1.3)",
 "routes_distinct": 27852,
 "conventions": 12,
 "shifts": 26,
 "key_texts": {
  "change_then_move": 44,
  "move_then_change": 40,
  "letters_cm": 1193440,
  "letters_mc": 53784
 },
 "trials": {
  "change_then_move": 10370783554560,
  "move_then_change": 467373494016
 },
 "chance_settings_with_3_or_fewer_slips": {
  "change_then_move": "4.1e-14",
  "move_then_change": "1.8e-15"
 },
 "method": "change then move: 4 blocks of 6 known places, key differences indexed; move then change: 4 disjoint pairs, per-gap difference index; compiled; every hit checked on all 24",
 "k4_settings_by_order_and_slips": [
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0
 ],
 "copies_settings_by_order_and_slips": [
  [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ]
 ],
 "copies_done": 10,
 "k4_hits": [],
 "plants": [
  {
   "seed": 2111,
   "order": "change then move",
   "route": "keyword KRYPTOS (repeats dropped)",
   "keytext": "Carter vol 1 fwd [kry]",
   "offset": 182002,
   "shift": 15,
   "conv": "vig/kry/kry",
   "k": 3,
   "slips": [
    33,
    65,
    70
   ],
   "settings_by_order_and_slips": [
    0,
    0,
    0,
    1,
    0,
    0,
    0,
    0
   ],
   "planted_found": true,
   "planted_mismatches": 3,
   "same_reading_routes": 1,
   "own_copies_settings": [
    0,
    0,
    0,
    0,
    0
   ],
   "found": true
  },
  {
   "seed": 2112,
   "order": "move then change",
   "route": "turn cw 9",
   "keytext": "panel ciphertexts K1-K4 fwd [std]",
   "offset": 96,
   "shift": 15,
   "conv": "beau/std/kry",
   "k": 2,
   "slips": [
    30,
    31
   ],
   "settings_by_order_and_slips": [
    0,
    0,
    0,
    0,
    0,
    0,
    1,
    0
   ],
   "planted_found": true,
   "planted_mismatches": 2,
   "same_reading_routes": 1,
   "own_copies_settings": [
    0,
    0,
    0,
    0,
    0
   ],
   "found": true
  }
 ],
 "slip_cost_bits": {
  "1": 9.3,
  "2": 17.5,
  "3": 25.1
 },
 "controls": "10 shuffled copies (seeds 2120-2129); each plant against 5 shuffles of its own ciphertext",
 "exhaustive": "yes"
}
```

Notes: K4 settings with <= 3 slips (change-then-move 0-3, move-then-change 0-3): [0, 0, 0, 0, 0, 0, 0, 0]; copies [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]; plants found [True, True]


