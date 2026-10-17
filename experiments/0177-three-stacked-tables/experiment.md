# 0177-three-stacked-tables: F3.4: Scheidt's patent with two keyed tables and three repeating keys (N = 2), tables from the KRYPTOS order and its inverse, key lengths 1-10 each: exact

**Family:** 3-two-component-key  
**Parent:** 0173-scheidt-patent-sandwich  
**Decision:** reverted  
**Run:** 2026-10-16T23:54:15+00:00, 1772.4 s, status ran  
**Time by phase:** unattributed 209 s, run 1772 s, record 0 s

## In plain words

Scheidt's patent can stack the shift-and-look-up step: shift, mixed alphabet, shift, mixed alphabet, shift. With three short secret words as the three shifts, each known letter ties a letter of each word together, and any two decide the third. A computer search tries every short length for the three words and every way of choosing the two mixed alphabets, on K4 and on scrambled copies.

## Walkthrough, by hand

1. Choose key lengths, say 5, 6 and 7, and the KRYPTOS order for both tables.
2. Place 22: E must become F. Guess the first key's slot 1 (21 mod 5) and the second key's slot 3 (21 mod 6); the third key's slot 0 (21 mod 7) is then fixed.
3. Every other known place sharing two guessed slots fixes its third slot, and so on.
4. A contradiction sends the search back to change a guess; if every guess dies, the cell is dead.
5. Every length triple and table choice, on K4 and scrambled copies.

## Worked example (generated)

```
key lengths 5, 6, 7: the three slots each known place ties together

place 22: E -> F: first key slot 1, second 3, third 0
place 23: A -> L: first key slot 2, second 4, third 1
place 24: S -> R: first key slot 3, second 5, third 2
place 25: T -> V: first key slot 4, second 0, third 3
place 26: N -> Q: first key slot 0, second 1, third 4
place 27: O -> Q: first key slot 1, second 2, third 5
place 28: R -> P: first key slot 2, second 3, third 6
place 29: T -> R: first key slot 3, second 4, third 0
place 30: H -> N: first key slot 4, second 5, third 1
place 31: E -> G: first key slot 0, second 0, third 2
place 32: A -> K: first key slot 1, second 1, third 3
place 33: S -> S: first key slot 2, second 2, third 4
place 34: T -> S: first key slot 3, second 3, third 5
place 64: B -> N: first key slot 3, second 3, third 0
place 65: E -> Y: first key slot 4, second 4, third 1
place 66: R -> P: first key slot 0, second 5, third 2
place 67: L -> V: first key slot 1, second 0, third 3
place 68: I -> T: first key slot 2, second 1, third 4
place 69: N -> T: first key slot 3, second 2, third 5
place 70: C -> M: first key slot 4, second 3, third 6
place 71: L -> Z: first key slot 0, second 4, third 0
place 72: O -> F: first key slot 1, second 5, third 1
place 73: C -> P: first key slot 2, second 0, third 2
place 74: K -> K: first key slot 3, second 1, third 3

slots used: 18; checks: 6
```

## Lineage

Inherits from 0173-scheidt-patent-sandwich. What changed: F3.4. 0173 decided the patent's text/key relation with one table between two keys. Here N = 2, as the patent writes it: v = d + P2[b + P1[u + a]] mod 26, three repeating keys a, b, d of length 1-10 each, P1 and P2 each the KRYPTOS order or its inverse (a standard table collapses to 0173's form), the message letter numbered by the standard, KRYPTOS or inverse order with either sign (u), and the carved letter read the same way (v): 144 classes. Each known place ties one slot of each key; any two fix the third, so a compiled search with propagation decides every cell exactly.

## Hypothesis (domain expert)

US 6,075,865 (Scheidt and Wack): O = a_N + pi_N[a_N-1 + ... + pi_1[I + a_0]] mod W; Sanborn's 'triple matrixes' (reports/Scheidt patents and field ciphers.md, issue #9); C5(b), C6. Model as in 'changed'. A cell (class, La, Lb, Ld) is live if some a, b, d satisfy all 24 known places; checks: 24 minus the key slots the known places use. Statistic: live cells by checks, K4 against 20 shuffled coppers; plants as a builder check.

## Prediction

No cell with 4 or more checks is live on K4; K4's live cells at each number of checks fall inside the coppers' range. Zero candidates.

## Method

1. For each class: the message number u and the carved number v at the 24 known places.
2. For each key-length triple 1-10: depth-first search over key slots with propagation (any two slots on a known place fix the third), node limit 2 million (undecided counted).
3. Count live cells by checks on K4 and 20 coppers; three planted texts must be live in their own cell.

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
 "family": "patent N = 2: v = d + P2[b + P1[u + a]], P1, P2 in {KRYPTOS, inverse}, u and v on std/KRYPTOS/inverse with signs (144 classes), key lengths 1-10 each, exact",
 "classes": 144,
 "length_triples": 916,
 "cells_per_text": 131904,
 "live_at_least_checks": {
  "1": {
   "k4": 124,
   "coppers_min": 98,
   "coppers_max": 130
  },
  "2": {
   "k4": 3,
   "coppers_min": 1,
   "coppers_max": 7
  },
  "4": {
   "k4": 0,
   "coppers_min": 0,
   "coppers_max": 0
  },
  "6": {
   "k4": 0,
   "coppers_min": 0,
   "coppers_max": 0
  },
  "8": {
   "k4": 0,
   "coppers_min": 0,
   "coppers_max": 0
  },
  "12": {
   "k4": 0,
   "coppers_min": 0,
   "coppers_max": 0
  }
 },
 "live_by_checks_k4": {
  "1": 121,
  "2": 3
 },
 "undecided": {
  "k4": 0,
  "coppers": [
   0,
   0,
   0,
   0,
   0
  ]
 },
 "max_nodes": 990419,
 "k4_live": [
  {
   "class": "kry/1/kry-inv/kry-inv/kry-inv/-1",
   "lengths": [
    9,
    8,
    5
   ],
   "checks": 2
  },
  {
   "class": "kry/-1/kry-inv/kry/std/-1",
   "lengths": [
    8,
    5,
    9
   ],
   "checks": 2
  },
  {
   "class": "kry-inv/-1/kry/kry/kry-inv/1",
   "lengths": [
    10,
    3,
    9
   ],
   "checks": 2
  },
  {
   "class": "std/1/kry/kry/std/-1",
   "lengths": [
    4,
    10,
    9
   ],
   "checks": 1
  },
  {
   "class": "std/1/kry/kry/std/-1",
   "lengths": [
    10,
    7,
    6
   ],
   "checks": 1
  },
  {
   "class": "std/1/kry/kry/kry/1",
   "lengths": [
    10,
    4,
    9
   ],
   "checks": 1
  },
  {
   "class": "std/1/kry/kry/kry-inv/1",
   "lengths": [
    4,
    9,
    10
   ],
   "checks": 1
  },
  {
   "class": "std/1/kry/kry-inv/std/1",
   "lengths": [
    4,
    9,
    10
   ],
   "checks": 1
  },
  {
   "class": "std/1/kry/kry-inv/kry/-1",
   "lengths": [
    10,
    9,
    4
   ],
   "checks": 1
  },
  {
   "class": "std/1/kry/kry-inv/kry-inv/1",
   "lengths": [
    8,
    9,
    6
   ],
   "checks": 1
  },
  {
   "class": "std/1/kry-inv/kry/std/-1",
   "lengths": [
    6,
    10,
    7
   ],
   "checks": 1
  },
  {
   "class": "std/1/kry-inv/kry/kry/-1",
   "lengths": [
    10,
    9,
    4
   ],
   "checks": 1
  },
  {
   "class": "std/1/kry-inv/kry/kry-inv/1",
   "lengths": [
    7,
    6,
    10
   ],
   "checks": 1
  },
  {
   "class": "std/1/kry-inv/kry/kry-inv/1",
   "lengths": [
    9,
    10,
    4
   ],
   "checks": 1
  },
  {
   "class": "std/1/kry-inv/kry/kry-inv/-1",
   "lengths": [
    8,
    9,
    6
   ],
   "checks": 1
  },
  {
   "class": "std/1/kry-inv/kry-inv/std/1",
   "lengths": [
    6,
    9,
    8
   ],
   "checks": 1
  },
  {
   "class": "std/1/kry-inv/kry-inv/std/1",
   "lengths": [
    7,
    6,
    10
   ],
   "checks": 1
  },
  {
   "class": "std/1/kry-inv/kry-inv/kry/1",
   "lengths": [
    7,
    7,
    9
   ],
   "checks": 1
  },
  {
   "class": "std/1/kry-inv/kry-inv/kry/1",
   "lengths": [
    10,
    6,
    7
   ],
   "checks": 1
  },
  {
   "class": "std/1/kry-inv/kry-inv/kry/-1",
   "lengths": [
    10,
    6,
    7
   ],
   "checks": 1
  },
  {
   "class": "std/1/kry-inv/kry-inv/kry/-1",
   "lengths": [
    10,
    7,
    6
   ],
   "checks": 1
  },
  {
   "class": "std/1/kry-inv/kry-inv/kry-inv/1",
   "lengths": [
    6,
    7,
    10
   ],
   "checks": 1
  },
  {
   "class": "std/1/kry-inv/kry-inv/kry-inv/-1",
   "lengths": [
    7,
    9,
    7
   ],
   "checks": 1
  },
  {
   "class": "std/-1/kry/kry-inv/kry-inv/1",
   "lengths": [
    4,
    10,
    9
   ],
   "checks": 1
  },
  {
   "class": "std/-1/kry-inv/kry/std/1",
   "lengths": [
    6,
    8,
    9
   ],
   "checks": 1
  },
  {
   "class": "std/-1/kry-inv/kry/std/1",
   "lengths": [
    9,
    4,
    10
   ],
   "checks": 1
  },
  {
   "class": "std/-1/kry-inv/kry/std/-1",
   "lengths": [
    4,
    9,
    10
   ],
   "checks": 1
  },
  {
   "class": "std/-1/kry-inv/kry/std/-1",
   "lengths": [
    9,
    4,
    10
   ],
   "checks": 1
  },
  {
   "class": "std/-1/kry-inv/kry/kry-inv/-1",
   "lengths": [
    8,
    7,
    8
   ],
   "checks": 1
  },
  {
   "class": "std/-1/kry-inv/kry-inv/kry/1",
   "lengths": [
    7,
    10,
    6
   ],
   "checks": 1
  },
  {
   "class": "std/-1/kry-inv/kry-inv/kry/1",
   "lengths": [
    9,
    8,
    6
   ],
   "checks": 1
  },
  {
   "class": "std/-1/kry-inv/kry-inv/kry/1",
   "lengths": [
    10,
    4,
    9
   ],
   "checks": 1
  },
  {
   "class": "std/-1/kry-inv/kry-inv/kry/-1",
   "lengths": [
    6,
    8,
    9
   ],
   "checks": 1
  },
  {
   "class": "std/-1/kry-inv/kry-inv/kry/-1",
   "lengths": [
    7,
    7,
    9
   ],
   "checks": 1
  },
  {
   "class": "std/-1/kry-inv/kry-inv/kry-inv/1",
   "lengths": [
    6,
    8,
    9
   ],
   "checks": 1
  },
  {
   "class": "kry/1/kry/kry/std/1",
   "lengths": [
    6,
    7,
    10
   ],
   "checks": 1
  },
  {
   "class": "kry/1/kry/kry/std/1",
   "lengths": [
    6,
    8,
    9
   ],
   "checks": 1
  },
  {
   "class": "kry/1/kry/kry/std/-1",
   "lengths": [
    6,
    8,
    9
   ],
   "checks": 1
  },
  {
   "class": "kry/1/kry/kry/kry/1",
   "lengths": [
    7,
    10,
    6
   ],
   "checks": 1
  },
  {
   "class": "kry/1/kry/kry/kry-inv/1",
   "lengths": [
    7,
    10,
    6
   ],
   "checks": 1
  }
 ],
 "plants": [
  {
   "class": "std/-1/kry/kry/kry-inv/-1",
   "lengths": [
    4,
    4,
    5
   ],
   "checks": 11,
   "status": 1
  },
  {
   "class": "kry/1/kry/kry-inv/kry/-1",
   "lengths": [
    7,
    5,
    5
   ],
   "checks": 7,
   "status": 1
  },
  {
   "class": "kry-inv/1/kry-inv/kry/kry/-1",
   "lengths": [
    5,
    8,
    8
   ],
   "checks": 3,
   "status": 1
  }
 ],
 "copies": "5 of 20 shuffled coppers run (seed 1770)",
 "seconds": 1772,
 "exhaustive": true
}
```

Notes: live cells with >=4 checks: K4 0 (coppers 0-0); >=1: K4 124 (coppers 98-130); undecided K4 0; plants live 3/3


