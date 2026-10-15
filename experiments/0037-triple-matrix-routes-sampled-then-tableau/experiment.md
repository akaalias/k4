# 0037-triple-matrix-routes-sampled-then-tableau: Sanborn's triple matrixes: three grid stages in a row, sampled, then the tableau

**Family:** 6-transposition-then-tableau  
**Parent:** 0016-routes-then-tableau-forced-key-english  
**Decision:** reverted  
**Run:** 2026-10-15T08:42:16+00:00, 86.2 s, status ran  
**Time by phase:** design 0 s, implement 60 s, test 10 s, run 86 s, record 0 s

## In plain words

The artist said he sometimes scrambled the letters through three grids before using the table. There are over a million ways to pick three grids from our set, too many to try with the slow English check, so we draw two hundred thousand at random. For each, we follow the 24 known letters through all three grids, ask whether a short secret word could then produce the carved letters where they land, and whether the letters of that word look like English. Three grids in a row behave like a random shuffle, so the answer should look like the earlier grid experiments.

## Walkthrough, by hand

1. Pick three grids: rows of 7 read down, then a quarter turn of a 12-wide grid, then columns in the order of the letters of KRYPTOS.
2. Follow position 22, the E of EAST, through the first grid to its new place, then through the second, then the third.
3. Do this for all 24 known letters.
4. The carved letter at each final place, with the known letter, forces one key letter on the table.
5. Two final places a multiple of p apart share a key letter at period p; a disagreement kills p.
6. The smallest surviving p is this triple's score; write its forced letters into their slots and read them.

## Worked example (generated)

```
stages: columnar 7, then rotate 12, then keyed columnar KRYPTOS; convention kry/kry/kry Vigenere

plain pos  letter  final place  carved  forced key letter
       22    E         88        U       D
       23    A         62        F       O
       24    S         37        W       L
       64    B         26        Q       F
       65    E         97        R       J
       66    R         30        N       M
```

## Lineage

Inherits from 0016-routes-then-tableau-forced-key-english. What changed: Three transposition stages instead of one or two. The space is too large to enumerate, so 200,000 triples are drawn at random from plain columnar widths 2-30, rotations, and keyed columnar from vocabulary words, each stage forward or inverse. The survival test and English scoring of experiments 6 and 16 are unchanged.

## Hypothesis (domain expert)

Sanborn, CNN 2005 (C1): 'double matrixes and triple matrixes... then went back to this table'. Experiments 6, 8, 16 and 26 covered single and double stages exhaustively for their route sets. Triples of 110 stage choices number about 1.3 million, beyond the budget with the English scoring, so this is a sample: 200,000 triples drawn uniformly, with a fixed seed, each stage one of plain columnar at widths 2-30 forward or inverse, a quarter-turn rotation at widths 2-30, or a keyed columnar from a vocabulary word forward or inverse. For each triple under the 8 distinct plain-cipher conventions the forced tableau key letters give the live periods by the divisor rule; the smallest live period is recorded, and the forced key at live periods up to 40 is scored as English on runs of five or more slots against ten shuffled controls. A triple with a live period under 20 or an English key above the controls would be a lead. Bounds: a 15 percent sample, not exhaustive; the smallest-period distribution says whether triples behave as random permutations.

## Prediction

The smallest live period over the sample is 22 or 23, as for single and double stages. The best forced key scores inside the range of ten shuffled controls. No candidate.

## Method

1. Build the stage list.
2. Draw 200,000 triples with a fixed seed.
3. For each triple compose the three permutations and send the crib positions through.
4. For each of the 8 conventions force the key letters, find live periods by the divisor rule, and score the forced key at live periods up to 40.
5. Keep the twenty best keys and the smallest-period histogram.
6. Repeat on ten shuffles.

## Result

Candidates returned: 0. Passed all gates: 0. Best crib hits among all candidates: 0/24
(no candidates).
Best loss: None (0 is solved; 10 per missed crib letter). Best fitness: None. Champion before this run: 0034-complete-the-key-at-surviving-periods.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| - | no candidates | | | | |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "three transposition stages (sampled) then periodic tableau",
 "stages": 211,
 "triples_sampled": 200000,
 "conventions": 8,
 "keys_scored": 123792,
 "smallest_live_period": 20,
 "min_live_period_histogram": {
  "20": 1,
  "23": 32,
  "24": 492,
  "25": 211,
  "26": 1001,
  "27": 1412,
  "28": 3483,
  "29": 1643,
  "30": 5053,
  "31": 3371,
  "32": 9537,
  "33": 8251
 },
 "best": [
  {
   "score": -3.613,
   "stages": [
    "keyed ABSCISSAE inv",
    "keyed HILL",
    "keyed VIRTUALLYINVISIBLE"
   ],
   "convention": "kry/kry/kry/beau",
   "period": 35,
   "runs": [
    "INDERSH"
   ]
  },
  {
   "score": -3.894,
   "stages": [
    "keyed NORTH inv",
    "rotate 11",
    "rotate 5"
   ],
   "convention": "std/kry/kry/vig",
   "period": 39,
   "runs": [
    "TWEREPA"
   ]
  },
  {
   "score": -4.155,
   "stages": [
    "keyed PALIMPSEST",
    "columnar 18 inv",
    "columnar 26"
   ],
   "convention": "kry/kry/kry/beau",
   "period": 36,
   "runs": [
    "ORCESCO"
   ]
  },
  {
   "score": -4.181,
   "stages": [
    "keyed SHADOW inv",
    "columnar 12",
    "columnar 18 inv"
   ],
   "convention": "kry/kry/kry/vig",
   "period": 39,
   "runs": [
    "DARTHTH"
   ]
  },
  {
   "score": -4.251,
   "stages": [
    "columnar 15",
    "keyed BERLINWALL inv",
    "keyed CARTER inv"
   ],
   "convention": "kry/kry/kry/vig",
   "period": 40,
   "runs": [
    "RORIF",
    "EMONTI"
   ]
  },
  {
   "score": -4.281,
   "stages": [
    "keyed WEST",
    "rotate 2",
    "keyed BURIED"
   ],
   "convention": "std/std/kry/vig",
   "period": 40,
   "runs": [
    "ETINASCR"
   ]
  },
  {
   "score": -4.281,
   "stages": [
    "keyed WEST",
    "rotate 2",
    "keyed BURIED"
   ],
   "convention": "std/std/kry/vig",
   "period": 38,
   "runs": [
    "ETINASCR"
   ]
  },
  {
   "score": -4.281,
   "stages": [
    "keyed WEST",
    "rotate 2",
    "keyed BURIED"
   ],
   "convention": "std/std/kry/vig",
   "period": 36,
   "runs": [
    "ETINASCR"
   ]
  },
  {
   "score": -4.281,
   "stages": [
    "keyed WEST",
    "rotate 2",
    "keyed BURIED"
   ],
   "convention": "std/std/kry/vig",
   "period": 34,
   "runs": [
    "ETINASCR"
   ]
  },
  {
   "score": -4.281,
   "stages": [
    "keyed WEST",
    "rotate 2",
    "keyed BURIED"
   ],
   "convention": "std/std/kry/vig",
   "period": 32,
   "runs": [
    "ETINASCR"
   ]
  }
 ],
 "shuffled_control_best": [
  -4.821,
  -4.937,
  -5.151,
  -4.484,
  -4.663,
  -4.922,
  -4.484,
  -4.857,
  -4.623,
  -4.478
 ],
 "control_note": "controls use the first 6,000 triples of the same sample"
}
```

Notes: Diagnostic, no candidates. 200000 triples x 8 conventions; smallest live period 20; best forced key -3.613 vs shuffled [-4.821, -4.937, -5.151, -4.484, -4.663, -4.922, -4.484, -4.857, -4.623, -4.478].


