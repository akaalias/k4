# 0117-running-keys-through-all-the-shifts: The sculpture's texts as a running key plus one constant shift of the table, with or without a K3-style move

**Family:** 1-keyed-periodic  
**Parent:** 0090-sculpture-running-key-with-a-k3-move  
**Decision:** reverted  
**Run:** 2026-10-15T21:05:01+00:00, 757.5 s, status ran  
**Time by phase:** unattributed 354 s, run 758 s, record 0 s

## In plain words

Sanborn once said he was surprised nobody had taken the original matrix and run it through all the possible shifts. One reading: take one of the sculpture's texts as a long key, and slide the whole table by a fixed amount, any of 26, before using it. We test every text, every starting point and every shift, with and without the grid moves of experiments 80 to 83, against the 24 known letters.

## Walkthrough, by hand

1. Take the K1/K2 ciphertext block as the key text, from offset 0, and the sculpture's alphabet with Vigenere.
2. At each known place, the key needed is the carved letter minus the known letter; the key text offers its own letter there.
3. With a constant shift s, needed = offered + s at every known place, so needed minus offered must be the same 24 times.
4. Slide the offset through the whole text, both directions, and repeat for every text, rule, and every grid move before or after the table.

## Worked example (generated)

```
key text: the four ciphertexts as one panel (the K1/K2 block first), offset 0; sculpture's alphabet, Vigenere

place  known  carved  needed  key text  offered  needed - offered
   22      E       F       1         K        0                1
   23      A       L      10         R        1                9
   24      S       R      21         N       19                2
   25      T       V      18         S        6               12
   64      B       N      11         V       22               15
   65      E       Y      17         F       12                5
   74      K       K       0         W       23                3

a constant shift would make the last column the same at all 24 places
```

## Lineage

Inherits from 0090-sculpture-running-key-with-a-k3-move. What changed: 0017 and 0090 used the sculpture's texts (the K1/K2 matrix among them) as a running key letter for letter. Sanborn was 'surprised that no one had tried recovering the original matrix and running it through all the possible shifts'. Here every key text gets a constant shift of the table, all 26, on top: the known letters must then differ from the key text by one constant, which is tested exactly through difference signatures, with no move and with every move of the type-1 library, before or after the table.

## Hypothesis (domain expert)

C2(b): 'shifts' as the 26 row shifts of the tableau, the matrix as the K1/K2 block or another carved text; C6(a). Model: c_i = E(p_i, k_{o+i} + s) for a key text k, offset o and constant s; E in 12 conventions (Vigenere, Beaufort, variant; plain and cipher alphabets standard or KRYPTOS) and key letters numbered on the standard or KRYPTOS alphabet. Because s is free, only the differences between known places matter: the 23 differences of the forced key must equal the key text's. Key texts as in 0090 (tableau by rows, rows with index, columns; Morse as carved and reversed; the four ciphertexts; K1-K3 plaintexts; Sanborn's 1989 letter, 1991 dedication texts and 2025 letter), forward and backward, every cyclic offset; Carter's book in the change-then-move order only. Moves: the type-1 library (identity included). Change then move: a dictionary of window signatures; move then change: a pair index on differences, filtered check by check. Ten shuffled coppers.

## Prediction

No text, offset, shift and move fits all 24 known letters; the deepest partial agreement matches the scrambled coppers'. Zero candidates.

## Method

1. Build the key texts (both numberings) and the route library.
2. Change then move: index every window's 23 key differences at the crib places; for each route and convention, compute the forced differences and look them up (all 24, and each crib stretch alone).
3. Move then change: for each key text, find the offsets that agree on the first two moved crib places through a pair index on differences, then filter.
4. Repeat on ten shuffled coppers.

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
 "family": "running key from the sculpture's texts plus one constant tableau shift, with or without a type-1 move",
 "routes_distinct": 27852,
 "conventions": 12,
 "key_texts_change_then_move": {
  "tableau rows fwd [std]": 781,
  "tableau rows fwd [kry]": 781,
  "tableau rows bwd [std]": 781,
  "tableau rows bwd [kry]": 781,
  "tableau rows with index column fwd [std]": 807,
  "tableau rows with index column fwd [kry]": 807,
  "tableau rows with index column bwd [std]": 807,
  "tableau rows with index column bwd [kry]": 807,
  "tableau columns fwd [std]": 781,
  "tableau columns fwd [kry]": 781,
  "tableau columns bwd [std]": 781,
  "tableau columns bwd [kry]": 781,
  "morse as carved fwd [std]": 80,
  "morse as carved fwd [kry]": 80,
  "morse as carved bwd [std]": 80,
  "morse as carved bwd [kry]": 80,
  "morse reversed order fwd [std]": 80,
  "morse reversed order fwd [kry]": 80,
  "morse reversed order bwd [std]": 80,
  "morse reversed order bwd [kry]": 80,
  "panel ciphertexts K1-K4 fwd [std]": 865,
  "panel ciphertexts K1-K4 fwd [kry]": 865,
  "panel ciphertexts K1-K4 bwd [std]": 865,
  "panel ciphertexts K1-K4 bwd [kry]": 865,
  "K1-K3 plaintexts fwd [std]": 768,
  "K1-K3 plaintexts fwd [kry]": 768,
  "K1-K3 plaintexts bwd [std]": 768,
  "K1-K3 plaintexts bwd [kry]": 768,
  "Sanborn 1989 letter fwd [std]": 2176,
  "Sanborn 1989 letter fwd [kry]": 2176,
  "Sanborn 1989 letter bwd [std]": 2176,
  "Sanborn 1989 letter bwd [kry]": 2176,
  "1991 dedication texts fwd [std]": 4880,
  "1991 dedication texts fwd [kry]": 4880,
  "1991 dedication texts bwd [std]": 4880,
  "1991 dedication texts bwd [kry]": 4880,
  "2025 open letter fwd [std]": 2228,
  "2025 open letter fwd [kry]": 2228,
  "2025 open letter bwd [std]": 2228,
  "2025 open letter bwd [kry]": 2228,
  "Carter vol 1 fwd [std]": 284914,
  "Carter vol 1 fwd [kry]": 284914,
  "Carter vol 1 bwd [std]": 284914,
  "Carter vol 1 bwd [kry]": 284914
 },
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
  "k4_full_hits": []
 },
 "move_then_change": {
  "key_texts": 40,
  "k4_full": 0,
  "k4_best_depth": 8,
  "controls_best_depth": [
   8,
   8,
   8,
   8,
   8,
   7,
   9,
   8,
   8,
   8
  ],
  "controls_completed": 10,
  "k4_full_hits": []
 },
 "controls": "10 shuffled coppers (seed 117), identical search"
}
```

Notes: 27,852 routes x 12 conventions. Change then move (44 numbered key texts incl. Carter): full K4 0, controls [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]; EASTNORTHEAST stretch K4 0 (controls [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]); BERLINCLOCK stretch K4 0 (controls [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]). Move then change (40 key texts): full 0, deepest K4 8, controls [8, 8, 8, 8, 8, 7, 9, 8, 8, 8] (10 completed).


