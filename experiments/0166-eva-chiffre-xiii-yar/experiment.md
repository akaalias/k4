# 0166-eva-chiffre-xiii-yar: F6.12, F6.13, F6.15: the Czech EVA double triangle and Chiffre XIII's five-row mask with its period-5 table, and the YAR '1-2-3' orderings, then the table

**Family:** 6-transposition-then-tableau  
**Parent:** 0164-disrupted-triangle-interrupted-trapezoid  
**Decision:** reverted  
**Run:** 2026-10-16T22:51:18+00:00, 36.0 s, status ran  
**Time by phase:** unattributed 57 s, run 36 s, record 0 s

## In plain words

Two ciphers of the Czech exiles in London: EVA wrote the message into a triangle twice over, and Chiffre XIII wrote it into five rows of a keyword's width, two of them short, then enciphered it with five shifted rows of one scrambled alphabet used in turn. Both are hand ciphers keyed by a sentence. And a third idea: Sanborn's raised letters YAR, reportedly spaced '1-2-3', as a way of counting off letters. Each is tested against the 24 known letters and scrambled copies.

## Walkthrough, by hand

1. EVA: write the 97 letters into rows of 1, 3, 5, ... cells, centred under 19 columns; copy out by the key's numbering; write into a second triangle; copy out again.
2. XIII: write into five rows of the key's width, rows 2 and 4 short (row 4 shifted), copy out by the key's numbering; then encipher letter 1 with row 1 of the shifted alphabet, letter 2 with row 2, ..., letter 6 with row 1 again.
3. Each known letter then forces one cell of the unknown alphabet; two known letters forcing different letters into one cell, or one letter into two cells, rule the setting out.
4. YAR: count 1, 2, 3, 1, 2, 3 around the text, taking each letter counted to, until all are taken.
5. Repeat for every key and choice, and on scrambled copies.

## Worked example (generated)

```
triangle: ten rows of 1, 3, ..., 19 cells, centred; key KRYPTOS repeated to 19 letters and numbered; columns read in that order

first 20 message places read: 82 5 11 19 29 41 55 71 89 36 48 62 78 96 17 27 39 53 69 87

place  letter  lands at  carved
   22       E        35       O
   23       A        77       D
   24       S        22       F
   64       B        96       A
   65       E        42       Q
   74       K        39       Q
```

## Lineage

Inherits from 0164-disrupted-triangle-interrupted-trapezoid. What changed: Three items, one run, a verdict each. F6.12 EVA (Czech exile, WWII, type TT): the text written into a triangle growing by two cells a row (ten rows under 19 columns for 97 letters, three cells empty), copied out by the 19-letter key's numbering, written into a second such triangle and copied out again under the same numbering; keys: 19-letter windows of the K1-K3 plaintexts, 19-letter dictionary words, pairs of puzzle words totalling 19; then a repeating key 1-26 on the standard or KRYPTOS table. F6.13 Chiffre XIII (type TS): five rows as wide as the key (24-31 letters: K1-K3 windows and puzzle phrases), rows 1, 3, 5 full, row 2 left-aligned and row 4 at every cyclic shift, their lengths every split of what is left of 97, columns read in key order; then the published substitution: plain A-Z over one unknown mixed alphabet, rows shifted by one and used in turn (position mod 5), either shift direction, decided exactly (the unknown alphabet's cells are forced one by one). F6.15: Sanborn's reported '1-2-3' spacing of the raised YAR as orderings: letters taken by counting 1, 2, 3 places in turn around the remaining text (every order of 1, 2, 3), and the same with 4, 5, 7 (Y, A, R's places in ENDYAHR), then the table. Ten scrambled coppers.

## Hypothesis (domain expert)

C1(a) ('double matrixes'), C22(d) (YAR's '1-2-3' spacing, clue register), C5; sources: foreign_agent_hand_systems.md section 4 (scz.bplaced.net §10.1: EVA, Chiffre XIII; the XIII substitution checked there on the published example), reports/Scheidt patents and field ciphers.md. Where the sources leave a rule open (XIII's partial-row lengths and row 4's shift; EVA's blank cells) every choice is enumerated; this is stated as a parametric family, not the documented one. Periodic-key items: orders A and B, 8 classes, 0134's statistic. XIII: a route is consistent if the forced cells M[(p + r) mod 26] = c (or p - r) are one-to-one; statistic: consistent routes with at least 4 checks, K4 against the coppers' range.

## Prediction

EVA and YAR: nothing below key length 20 beyond the coppers' rate. XIII: consistent routes at the coppers' rate. Zero candidates.

## Method

1. Keys: K1-K3 windows of 19 and 24-31 letters, 19-letter dictionary words, puzzle-word pairs.
2. EVA and YAR routes through the compiled periodic-key test (orders A, B, 8 classes).
3. XIII: each mask route; the 24 forced cells of the unknown alphabet checked for one-to-one, both shift directions; counts by checks.
4. K4 against the coppers per item.

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
 "family": "EVA double triangle and YAR orderings then or before a periodic key; Chiffre XIII five-row masks then its period-5 shifted unknown alphabet",
 "eva_keys": 1920,
 "xiii_keys": 6296,
 "items": {
  "F6.12 EVA": {
   "routes": 3840,
   "k4_live_by_period": {
    "A": [
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
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
    "B": [
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     1,
     1123
    ]
   },
   "controls_live_by_period_min": {
    "A": [
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
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
    "B": [
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     1072
    ]
   },
   "controls_live_by_period_max": {
    "A": [
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
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
    "B": [
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     4,
     1375
    ]
   },
   "k4_shortest_live": {
    "A": null,
    "B": 25
   },
   "coppers_shortest_live": {
    "A": 99,
    "B": 25
   },
   "k4_settings_live_below_20": {
    "A": 0,
    "B": 0
   },
   "controls_settings_live_below_20": {
    "A": [
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
    "B": [
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
    ]
   },
   "k4_live_below_20": [],
   "cells_k4_above_every_copper": [],
   "null_cells_above_rest_per_copper": [
    0,
    1,
    0,
    0,
    0,
    0,
    0,
    0,
    1,
    0
   ],
   "stop_queue": false
  },
  "F6.15 YAR": {
   "routes": 24,
   "k4_live_by_period": {
    "A": [
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
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
    "B": [
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     10
    ]
   },
   "controls_live_by_period_min": {
    "A": [
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
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
    "B": [
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     4
    ]
   },
   "controls_live_by_period_max": {
    "A": [
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
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
    "B": [
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     10
    ]
   },
   "k4_shortest_live": {
    "A": null,
    "B": 26
   },
   "coppers_shortest_live": {
    "A": 99,
    "B": 26
   },
   "k4_settings_live_below_20": {
    "A": 0,
    "B": 0
   },
   "controls_settings_live_below_20": {
    "A": [
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
    "B": [
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
    ]
   },
   "k4_live_below_20": [],
   "cells_k4_above_every_copper": [],
   "null_cells_above_rest_per_copper": [
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
   "stop_queue": false
  },
  "F6.13 Chiffre XIII": {
   "routes": 2248512,
   "keys": 6296,
   "consistent_ge": {
    "3": {
     "k4": 0,
     "coppers": [
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
     ]
    },
    "4": {
     "k4": 0,
     "coppers": [
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
     ]
    },
    "5": {
     "k4": 0,
     "coppers": [
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
     ]
    },
    "6": {
     "k4": 0,
     "coppers": [
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
     ]
    }
   },
   "k4_top": []
  }
 },
 "seconds": 36,
 "controls": "10 shuffled coppers (seed 1612)",
 "exhaustive": true
}
```

Notes: EVA: 3,840 routes, shortest live A None B 25; YAR: 24 routes, shortest live A None B 26; XIII: 2,248,512 masks, consistent with >=4 checks K4 0 (coppers 0-0)


