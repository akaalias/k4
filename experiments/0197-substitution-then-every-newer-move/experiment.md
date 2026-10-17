# 0197-substitution-then-every-newer-move: F9.1: a one-to-one letter substitution, then each hand transposition built since 0106 (compass routes, keyword shapes, keyed blanks, row reshuffles, French diagonal, EVA, Chiffre XIII, YAR, the plate layout, the poem code): exact

**Family:** 9-substitution-then-transposition  
**Parent:** 0106-one-to-one-substitution-with-every-move-so-far  
**Decision:** reverted  
**Run:** 2026-10-17T01:39:40+00:00, 70.3 s, status ran  
**Time by phase:** design 0 s, implement 0 s, test 0 s, run 70 s, record 0 s

## In plain words

Perhaps the letters were first swapped for other letters by a fixed code alphabet and then shuffled into a new order. Then wherever the message has the same letter, the copper must have the same letter after unshuffling. That simple rule was checked for 1.86 million shuffles before; here for every newer shuffle the project has built since, about eight million of them.

## Walkthrough, by hand

1. Take a route: it says where each message letter is carved.
2. Follow the three Es of EASTNORTHEAST and BERLINCLOCK to their carved places: all three must show the same carved letter.
3. The A, S, T, N, O, R, L, C must likewise each show one carved letter, all different from one another.
4. One mismatch kills the route.
5. About eight million routes, on K4 and on scrambled copies.

## Worked example (generated)

```
the known letters and the carved letters they would have to match one to one, with no move at all:

place 22: E -> F
place 23: A -> L
place 24: S -> R
place 25: T -> V
place 26: N -> Q
place 27: O -> Q
place 28: R -> P
place 29: T -> R
place 30: H -> N
place 31: E -> G
place 32: A -> K
place 33: S -> S
place 34: T -> S
place 64: B -> N
place 65: E -> Y
place 66: R -> P
place 67: L -> V
place 68: I -> T
place 69: N -> T
place 70: C -> M
place 71: L -> Z
place 72: O -> F
place 73: C -> P
place 74: K -> K
```

## Lineage

Inherits from 0106-one-to-one-substitution-with-every-move-so-far. What changed: F9.1. The list first: hand transpositions outside 0106's 1.86 million routes, each built since for F6, with its size: compass-direction readings and pairs (0159, 110,820), keyword-disrupted, triangle, interrupted and trapezoid columnars (0164, 1.40 million), keyed blank cells, in-row reshuffles and the French diagonal (0165, 4.08 million), EVA's double triangle (0166, 3,840), Chiffre XIII's shaped mask as a move (0166, 2.25 million), YAR's counting-off orders (0166, 24), paths over the copper's layout (0184, 73) and the poem code's double columnars (0190, 6,092). Not in this run: the 105.5 million mixed matrix triples (0158), 20.4 million keyword triples (0162) and 116 million Nihilist routes (0167), whose builders are compiled into their experiments' testers. Each route, forward and inverse, with 0106's test: a one-to-one substitution commutes with the move, so equal known letters must land on equal carved letters and different on different. Builders reused from the committed experiments; the test compiled; K4 against 10 shuffled copies.

## Hypothesis (domain expert)

F9 (the Zodiac 340 construction: substitution first, transposition last; 0018 found it the only construction making the width-21 repeats), A9. Model: c = route(sigma(p)) with sigma any permutation of the 26 letters. 24 known letters, 13 different: 11 equalities and the inequalities between them, a strong test (0106 found no survivor in 1.86 million routes). Statistic: surviving routes, K4 against copies.

## Prediction

No route survives on K4 or on the copies, as in 0106. Zero candidates.

## Method

1. Load each committed experiment's route builder.
2. Build the routes in parallel chunks, forward and inverse.
3. For each route and text: the carved letters at the 24 known letters' landing places must match the known letters one to one (compiled).
4. Count survivors per text; K4 against 10 shuffled copies; a planted text as a builder check.

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
 "family": "one-to-one substitution, then each hand move built since 0106 (forward and inverse), exact",
 "routes_by_source": {
  "0159 compass": 110820,
  "0184 layout": 73,
  "0166 F6.15 YAR": 24,
  "0166 F6.12 EVA": 3840,
  "0166 F6.13 Chiffre XIII": 4497024,
  "0164 F6.11 disrupted": 327440,
  "0164 F6.11 triangle": 654876,
  "0164 F6.16 interrupted": 332817,
  "0164 F6.17 trapezoid": 89708,
  "0165 F6.10 keyed blanks": 1450196,
  "0165 F6.18 row reshuffle": 361698,
  "0165 F6.19 French diagonal": 2264476,
  "0190 poem code": 6118
 },
 "routes_total": 10099110,
 "survivors": {
  "k4": 0,
  "copies": [
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
  "plant": 1
 },
 "per_source": {
  "0159 compass": {
   "routes": 110820,
   "k4": 0,
   "copies": [
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
   "plant": 0
  },
  "0184 layout": {
   "routes": 73,
   "k4": 0,
   "copies": [
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
   "plant": 0
  },
  "0166 F6.15 YAR": {
   "routes": 24,
   "k4": 0,
   "copies": [
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
   "plant": 0
  },
  "0166 F6.12 EVA": {
   "routes": 3840,
   "k4": 0,
   "copies": [
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
   "plant": 0
  },
  "0166 F6.13 Chiffre XIII": {
   "routes": 4497024,
   "k4": 0,
   "copies": [
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
   "plant": 0
  },
  "0164 F6.11 disrupted": {
   "routes": 327440,
   "k4": 0,
   "copies": [
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
   "plant": 0
  },
  "0164 F6.11 triangle": {
   "routes": 654876,
   "k4": 0,
   "copies": [
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
   "plant": 0
  },
  "0164 F6.16 interrupted": {
   "routes": 332817,
   "k4": 0,
   "copies": [
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
   "plant": 0
  },
  "0164 F6.17 trapezoid": {
   "routes": 89708,
   "k4": 0,
   "copies": [
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
   "plant": 0
  },
  "0165 F6.10 keyed blanks": {
   "routes": 1450196,
   "k4": 0,
   "copies": [
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
   "plant": 1
  },
  "0165 F6.18 row reshuffle": {
   "routes": 361698,
   "k4": 0,
   "copies": [
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
   "plant": 0
  },
  "0165 F6.19 French diagonal": {
   "routes": 2264476,
   "k4": 0,
   "copies": [
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
   "plant": 0
  },
  "0190 poem code": {
   "routes": 6118,
   "k4": 0,
   "copies": [
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
   "plant": 0
  }
 },
 "k4_survivors": [],
 "not_run": "0158 mixed triples (105.5M), 0162 keyword triples (20.4M), 0167 Nihilist (116M): builders compiled into their testers",
 "copies": "10 shuffled copies (seed 1960)",
 "seconds": 70,
 "exhaustive": true
}
```

Notes: 10,099,110 routes; survivors K4 0 (copies 0-0); plant 1


