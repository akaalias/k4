# 0090-sculpture-running-key-with-a-k3-move: A running key concealed at the sculpture, joined to a K3-style move before or after it

**Family:** 6-matrix-transposition-then-tableau  
**Parent:** 0017-running-key-from-the-sculpture-itself  
**Decision:** reverted  
**Run:** 2026-10-15T18:51:50+00:00, 60.3 s, status ran  
**Time by phase:** test 167 s, run 60 s, record 0 s

## In plain words

A running key is a long text used as the secret, one letter of it per letter of the message. The sculpture carries several such texts: the table, the Morse messages, the solved parts. Experiment 17 tried them on K4 directly. Here the letters are also moved the way K3's were, by turning a grid or reading columns, either before or after the table is used. Because a running key has no free letters, each combination either explains all 24 known letters or it does not.

## Walkthrough, by hand

1. Pick a move, say a clockwise quarter turn of a grid 8 letters wide, and a key text, say the Morse as carved.
2. Change then move: the letter at place 22 of the message ends up at some place j of the copper; read the carved letter there.
3. Find the key letter that turns E into that carved letter on the sculpture's table.
4. The key text, started at offset o, must have that letter at its place o + 22. Do this for all 24 known places.
5. Move then change: first move the message, so E of place 22 lands at place j; the key letter must sit at place o + j and turn E into the carved letter at j.
6. Slide o over the whole key text and repeat for every move, every key text, both directions and 12 table rules.

## Worked example (generated)

```
(worked_example failed: IndexError('string index out of range'))
```

## Lineage

Inherits from 0017-running-key-from-the-sculpture-itself. What changed: 0017, 0004, 0021 and 0078 tested running keys from the sculpture's texts, K1-K3, Carter's book and Sanborn's letters with no move. Here each of those keys is joined to every move of the type-1 route library (K3's counting rule, one or two quarter turns, plain and true-keyword column shuffles, 27,000-odd distinct routes), with the move either before the table or after it. A running key leaves no free letter, so both orders are exact tests.

## Hypothesis (domain expert)

Types 1 and 3 of directions.md crossed. Scheidt: 'the keys were concealed at the sculpture' (C6(a)), K4 is 'more than one stage'; Sanborn: 'double matrixes and triple matrixes... then went back to this table' (C1); earlier text holds instructions for later text (C7(a)). Key sources, each forward and backward at every cyclic offset: the carved tableau by rows, by rows with the index column and by columns; the Morse as carved and in reverse order; the four ciphertexts as one panel (0017); the K1-K3 plaintexts (0004); Sanborn's 1989 letter, the 1991 dedication texts and the 2025 open letter (0078); Carter's book (0021, change-then-move only). Moves: K3's rule i -> a + b i mod 97 for every a, b; one quarter turn at widths 2-96 either way; two clockwise turns at every pair of widths; plain columnar left-to-right or right-to-left; true-keyword columnar (issue #26) from the puzzle's words; each forward and inverse, deduplicated. 12 conventions (Vigenere, Beaufort, variant Beaufort; key and text numbered on standard or KRYPTOS). Change then move: the forced key at the 24 crib places must equal the source at those places, a dictionary lookup. Move then change: the key places are the moved crib places; offsets are filtered check by check. Exact, all 24 checks; the deepest partial match is compared with ten shuffled coppers.

## Prediction

No combination explains all 24 known letters in either order. Change then move: no source matches either whole crib stretch (13 or 11 letters). Move then change: the deepest partial match is 7-8 checks, inside the scrambled-copper range. Zero candidates.

## Method

1. Build the key texts and the deduplicated route library.
2. Change then move: for each route and convention, undo the move at the 24 crib places, compute the key letters forced there, and look them up in an index of every source window with the crib spacing (whole set, and each crib stretch alone).
3. Move then change: the forced key letters sit at the moved crib places; for each source keep the offsets that agree at the first moved place, then the second, and so on, and record how deep any offset gets.
4. Repeat both on ten shuffled coppers.
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
 "sources": {
  "tableau rows fwd": 781,
  "tableau rows bwd": 781,
  "tableau rows with index column fwd": 807,
  "tableau rows with index column bwd": 807,
  "tableau columns fwd": 781,
  "tableau columns bwd": 781,
  "morse as carved fwd": 80,
  "morse as carved bwd": 80,
  "morse reversed order fwd": 80,
  "morse reversed order bwd": 80,
  "panel ciphertexts K1-K4 fwd": 865,
  "panel ciphertexts K1-K4 bwd": 865,
  "K1-K3 plaintexts fwd": 768,
  "K1-K3 plaintexts bwd": 768,
  "Sanborn 1989 letter fwd": 2176,
  "Sanborn 1989 letter bwd": 2176,
  "1991 dedication texts fwd": 4880,
  "1991 dedication texts bwd": 4880,
  "2025 open letter fwd": 2228,
  "2025 open letter bwd": 2228,
  "Carter vol 1 fwd": 284914,
  "Carter vol 1 bwd": 284914
 },
 "change_then_move": {
  "k4_full_matches": 0,
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
  "k4_stretch13_matches": 0,
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
  "k4_stretch11_matches": 0,
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
  "sources": "all but Carter",
  "k4_full": 0,
  "k4_best_depth": 7,
  "controls_best_depth": [
   7,
   7,
   7,
   6,
   7,
   6,
   7,
   6,
   6,
   7
  ],
  "k4_depth_histogram": {
   "1": 8874,
   "2": 202095,
   "3": 111542,
   "4": 11288,
   "5": 407,
   "6": 16,
   "7": 2
  },
  "k4_top": [
   {
    "route": "K3 rule a=14 b=12 inverse",
    "conv": "varb/kry/std",
    "depth": 7
   },
   {
    "route": "two turns cw 8,95 inverse",
    "conv": "varb/kry/std",
    "depth": 7
   }
  ],
  "route_convention_pairs_on_k4": 334224,
  "key_letters_searched": 26892
 },
 "controls": "10 shuffled coppers (seed 90), identical search"
}
```

Notes: 27,852 distinct routes x 12 conventions. Change then move (22 key texts incl. Carter): full matches K4 0, controls [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]; EASTNORTHEAST stretch 0 (controls [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]), BERLINCLOCK stretch 0 (controls [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]). Move then change (20 key texts): full 0, deepest K4 7, controls [7, 7, 7, 6, 7, 6, 7, 6, 6, 7].


