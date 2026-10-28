# 0243-f13-memorable-keys-scored-by-english-alone-rerun: F13.5: memorable keys scored by English alone: key words, keyword tables, running keys from the named texts, autokey primers and keyword columnars from the source list, through the methods already built, no known letter read; K4 against 100 shuffles, plants per method

**Family:** 13-ciphertext-only  
**Parent:** 0242-f13-memorable-keys-scored-by-english-alone  
**Decision:** reverted  
**Run:** 2026-10-28T03:14:00+00:00, 829.2 s, status ran  
**Time by phase:** unattributed 370 s, run 829 s, record 68 s

## In plain words

The creators said the key could be remembered: a word, or a passage of a known text. Earlier runs checked every such key against the clue words. Here we check them again without looking at the clue words at all: every key word, every passage of the sculpture's texts and Carter's book, every keyword-scrambled table, read in full and kept only if the result reads as English. K4 is compared with shuffles of its own letters treated the same way, and hidden test messages made with keys from the same lists show whether a right key would stand out.

## Walkthrough, by hand

1. Take a key from the list, say the word ABSCISSA from its third letter, and a way of using the sculpture's table.
2. Decipher all 97 carved letters with it.
3. Score the result by how often its four-letter groups occur in English.
4. Do this for every key word and start, every passage of the named texts, every keyword table and every way of using the table; keep the best.
5. Do the same on shuffles of K4 and compare.

## Worked example (generated)

```
Key: method A, mode var, pa std, ca kry, ka kry, key MEZUZAH, start 4

  carved   OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWI
  reading  EPOTGETEUCNCHBEYDETHSLYPOFTYAABSRFADESMRPPFNZSKYSGLESCUFOOLH

Every key in the lists is read like this, in full, and scored by English alone; no known letter is read.
```

## Lineage

Inherits from 0242-f13-memorable-keys-scored-by-english-alone. What changed: F13.5 (issue #85); reruns 0242, which errored drawing a running-key plant from a named text shorter than 97 letters (plants now draw only from texts longer than 97; the search still reads every text). Every earlier key-source search (0004-0021, 0045-0053, 0109, 0115, 0117, 0154, 0210) decided by the 24 known letters. Here the same memorable keys are read with no known letter: five methods, every key from the source order (program.md: K1-K3 words, the sculpture's texts, the Morse, Carter, then the dictionary), every reading scored exhaustively by quadgrams, the 20 best per method rescored by MIX8m (0233). A: a periodic key word (every puzzle word and every dictionary word of 3-24 letters, every start) on the 24 rules of the sculpture's tables. B: keyword-mixed tables from the puzzle words (one side or both) with a puzzle key word. C: a running key from 0210's named texts, every offset, both directions, on the 24 rules. D: plaintext and ciphertext autokey primed by any puzzle or dictionary word, on the 24 rules. E: a keyword columnar keyed by a puzzle word, before or after the table with a puzzle key word. Statistic: max z over the five methods against K4's 100 shuffles; plants (8 per method, keys drawn from the same sources) each against 10 own shuffles.

## Hypothesis (domain expert)

C5 ('simple, can be remembered, executed with the correct key word/s'), C6(a) (keys concealed at the sculpture), C7(a) (K1-K3 words as keys), C25(a) (the Morse words), C20(a) (layer two). Each method was closed exactly with the known letters (0005, 0009-0011, 0020, 0053, 0109, 0115, 0117, 0154, 0210; autokeys 0002, 0003, 0025, 0064; keyword columnars 0110-0114). Those verdicts stand only if the 24 letters sit where stated, letter for letter, without slips (A1, A2) and the plaintext is not masked out of their places. F13.5 is that hedge: the key space is at most about 30 bits per method (log2 of 54 million settings), far under what 97 letters of English carry, and every setting is read, so where the known letters are exact this adds nothing; it decides only the cases where they are not. Pre-registered: S = max over the five methods of (best MIX8m minus the shuffles' mean) / their sd; K4 flags at p < 0.05 against 100 shuffles (one test); a plant is found when its S is above all 10 own shuffles' S; a method is decided when at least 6 of its 8 plants are found.

## Prediction

Plants found 8 of 8 in every method (the keys are read exhaustively, so the true key's reading is scored directly). K4 inside its shuffles (p above 0.05), its readings junk with at most 3-4 of 24 known letters in place (harness gate 2). F13.5 closes as exact over the stated key lists.

## Method

1. Key lists: 0115's 171 puzzle words (every start), the 234,288-word dictionary (lengths 3-24, every start: 2,241,060 rotations), keyword-mixed alphabets of the puzzle words, 0210's named texts both ways.
2. Every setting decrypted in compiled code and scored by the harness's quadgram table; the 20 best per method kept, rescored by MIX8m.
3. Texts: K4, 100 shuffles, 40 plants (8 per method, half with X stops, Carter's held-out text, keys drawn from the lists) and 10 shuffles of each.
4. z per method against K4's shuffles; S = the largest z; K4 ranked; each plant among its own copies.
5. K4's best reading per method submitted; gate 4's controls are the shuffles' best readings.

## Result

Candidates returned: 5. Passed all gates: 0. Best crib hits among all candidates: 2/24
(EAST 0/4, NORTHEAST 2/9, BERLIN 0/6, CLOCK 0/5).
Best loss: 222.92344391987373 (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | cribs | 1/24 |  | `EPOTGETEUCNCHBEYDETHSLYPOFTYAABSRFADESMRPPFNZSKYSGLESCUFOOLHELDSJROPDNYTRSIMFZGMWBIFOUONZUCUSOBSA` |  |
| 2 | cribs | 1/24 |  | `RDALSRDRIONBLURSJPFLCUSLIXPACBTAEJSDWMEEXBJCKARSCFPSABEZBOFJDUVIADIODOSHDAZVZZZGMNNZBIANMELEEARAC` |  |
| 3 | cribs | 2/24 |  | `SORDYKNOXGCWPBJRMAPCHSQMBGISTYSTOTARTPWRENOWJOTSTWEINHLQZTHTEZNEOFWHAROYBDHHOVFFBEVBIRECASOFMAMWE` |  |
| 4 | cribs | 2/24 |  | `AFLUEJTKWYOROMEGGSSNAMXWRCWAIDANIZPPPFOLFNUTCREMLTYDUPEADDLEXFEWIKNOTCHOBIKILIAFNXNMIMPMKFIFAYYFS` |  |
| 5 | cribs | 1/24 |  | `LRESBAMVEGLMVCDHFGHOFTESWTFUZAKPHEDKEAPOSSIXLYWEBOYFARWRFHEINEMQIUVZHURHOJYEVJMQNESHOCKVHKSCUDIEU` |  |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "item": "F13.5",
 "search_reads_known_letters": false,
 "methods": {
  "A": "24 rules x (1,084 puzzle-word starts + 2,241,060 dictionary rotations)",
  "B": "5,100 keyword-table setups (170 puzzle alphabets) x 1,084 puzzle-word starts",
  "C": "24 rules x 36 named texts (both directions), every offset: 596,530 offsets",
  "D": "24 rules x 2 kinds x 233,014 primer words",
  "E": "138 keyword columnars x 2 orders x 24 rules x 1,084 puzzle-word starts"
 },
 "exhaustive": true,
 "scoring": "every setting read in full and scored by the harness quadgram table; the 20 best per method rescored by MIX8m (0233)",
 "texts": 541,
 "k4_copies": 100,
 "k4_statistic": 2.228,
 "k4_best_method": "C",
 "k4_p": 0.099,
 "copies_statistic_max": 3.663,
 "copies_statistic_median": 1.122,
 "k4_rank_per_method_copies_at_or_above": {
  "A": 6,
  "B": 96,
  "C": 2,
  "D": 21,
  "E": 45
 },
 "plant_power": {
  "A": [
   8,
   8
  ],
  "B": [
   8,
   8
  ],
  "C": [
   8,
   8
  ],
  "D": [
   8,
   8
  ],
  "E": [
   8,
   8
  ]
 },
 "plant_exact_recovery": {
  "A": [
   8,
   8
  ],
  "B": [
   8,
   8
  ],
  "C": [
   8,
   8
  ],
  "D": [
   6,
   8
  ],
  "E": [
   6,
   8
  ]
 },
 "decided_methods_at_6_of_8": [
  "A",
  "B",
  "C",
  "D",
  "E"
 ],
 "plants": {
  "plantA_0": {
   "kind": "clean",
   "key": {
    "method": "A",
    "mode": "var",
    "pa": "std",
    "ca": "kry",
    "ka": "std",
    "key": "OVERDUE",
    "start": 6
   },
   "S": 40.96,
   "own_max": 2.74,
   "found": true,
   "read_exactly": true
  },
  "plantA_1": {
   "kind": "xstops",
   "key": {
    "method": "A",
    "mode": "vig",
    "pa": "kry",
    "ca": "std",
    "ka": "kry",
    "key": "CHOLECYSTOGASTROSTOMY",
    "start": 1
   },
   "S": 40.55,
   "own_max": 2.64,
   "found": true,
   "read_exactly": true
  },
  "plantA_2": {
   "kind": "clean",
   "key": {
    "method": "A",
    "mode": "vig",
    "pa": "std",
    "ca": "std",
    "ka": "std",
    "key": "NONRETRACEABLE",
    "start": 13
   },
   "S": 44.47,
   "own_max": 3.21,
   "found": true,
   "read_exactly": true
  },
  "plantA_3": {
   "kind": "xstops",
   "key": {
    "method": "A",
    "mode": "var",
    "pa": "kry",
    "ca": "kry",
    "ka": "std",
    "key": "LEK",
    "start": 1
   },
   "S": 38.91,
   "own_max": 2.84,
   "found": true,
   "read_exactly": true
  },
  "plantA_4": {
   "kind": "clean",
   "key": {
    "method": "A",
    "mode": "var",
    "pa": "kry",
    "ca": "std",
    "ka": "kry",
    "key": "PERQUADRAT",
    "start": 0
   },
   "S": 42.44,
   "own_max": 3.38,
   "found": true,
   "read_exactly": true
  },
  "plantA_5": {
   "kind": "xstops",
   "key": {
    "method": "A",
    "mode": "vig",
    "pa": "std",
    "ca": "std",
    "ka": "std",
    "key": "FORMALDEHYDESULPHOXYLIC",
    "start": 19
   },
   "S": 39.23,
   "own_max": 2.3,
   "found": true,
   "read_exactly": true
  },
  "plantA_6": {
   "kind": "clean",
   "key": {
    "method": "A",
    "mode": "var",
    "pa": "kry",
    "ca": "kry",
    "ka": "kry",
    "key": "BY",
    "start": 0
   },
   "S": 34.05,
   "own_max": 4.04,
   "found": true,
   "read_exactly": true
  },
  "plantA_7": {
   "kind": "xstops",
   "key": {
    "method": "A",
    "mode": "beau",
    "pa": "kry",
    "ca": "std",
    "ka": "std",
    "key": "RECOUNTENANCE",
    "start": 1
   },
   "S": 34.6,
   "own_max": 3.35,
   "found": true,
   "read_exactly": true
  },
  "plantB_0": {
   "kind": "clean",
   "key": {
    "method": "B",
    "mode": "var",
    "pa": "std",
    "ca": "PALIMSETBCDFGHJKNOQRUVWXYZ",
    "ka": "kry",
    "key": "HOWARDCARTER",
    "start": 5
   },
   "S": 51.24,
   "own_max": 3.12,
   "found": true,
   "read_exactly": true
  },
  "plantB_1": {
   "kind": "xstops",
   "key": {
    "method": "B",
    "mode": "vig",
    "pa": "kry",
    "ca": "FOURABCDEGHIJKLMNPQSTVWXYZ",
    "ka": "std",
    "key": "CARNARVON",
    "start": 1
   },
   "S": 28.54,
   "own_max": 1.97,
   "found": true,
   "read_exactly": true
  },
  "plantB_2": {
   "kind": "clean",
   "key": {
    "method": "B",
    "mode": "beau",
    "pa": "std",
    "ca": "SOMEWHRABCDFGIJKLNPQTUVXYZ",
    "ka": "std",
    "key": "PALIMPSEST",
    "start": 0
   },
   "S": 47.43,
   "own_max": 1.87,
   "found": true,
   "read_exactly": true
  },
  "plantB_3": {
   "kind": "xstops",
   "key": {
    "method": "B",
    "mode": "var",
    "pa": "kry",
    "ca": "POINTABCDEFGHJKLMQRSUVWXYZ",
    "ka": "std",
    "key": "INVISIBLE",
    "start": 1
   },
   "S": 43.45,
   "own_max": 2.87,
   "found": true,
   "read_exactly": true
  },
  "plantB_4": {
   "kind": "clean",
   "key": {
    "method": "B",
    "mode": "vig",
    "pa": "FORTYABCDEGHIJKLMNPQSUVWXZ",
    "ca": "kry",
    "ka": "kry",
    "key": "POSSIBLE",
    "start": 1
   },
   "S": 48.62,
   "own_max": 4.83,
   "found": true,
   "read_exactly": true
  },
  "plantB_5": {
   "kind": "xstops",
   "key": {
    "method": "B",
    "mode": "beau",
    "pa": "UNKOWABCDEFGHIJLMPQRSTVXYZ",
    "ca": "kry",
    "ka": "kry",
    "key": "ENCUMBERED",
    "start": 9
   },
   "S": 43.19,
   "own_max": 2.88,
   "found": true,
   "read_exactly": true
  },
  "plantB_6": {
   "kind": "clean",
   "key": {
    "method": "B",
    "mode": "beau",
    "pa": "REMAINSBCDFGHJKLOPQTUVWXYZ",
    "ca": "REMAINSBCDFGHJKLOPQTUVWXYZ",
    "ka": "std",
    "key": "FOUR",
    "start": 2
   },
   "S": 45.89,
   "own_max": 1.94,
   "found": true,
   "read_exactly": true
  },
  "plantB_7": {
   "kind": "xstops",
   "key": {
    "method": "B",
    "mode": "beau",
    "pa": "THEYABCDFGIJKLMNOPQRSUVWXZ",
    "ca": "kry",
    "ka": "kry",
    "key": "WAS",
    "start": 2
   },
   "S": 32.53,
   "own_max": 4.49,
   "found": true,
   "read_exactly": true
  },
  "plantC_0": {
   "kind": "clean",
   "key": {
    "method": "C",
    "mode": "var",
    "pa": "std",
    "ca": "std",
    "ka": "kry",
    "source": "tableau rows with index column fwd",
    "offset": 396
   },
   "S": 45.98,
   "own_max": 2.91,
   "found": true,
   "read_exactly": true
  },
  "plantC_1": {
   "kind": "xstops",
   "key": {
    "method": "C",
    "mode": "vig",
    "pa": "kry",
    "ca": "kry",
    "ka": "kry",
    "source": "tableau rows fwd",
    "offset": 157
   },
   "S": 35.2,
   "own_max": 3.05,
   "found": true,
   "read_exactly": true
  },
  "plantC_2": {
   "kind": "clean",
   "key": {
    "method": "C",
    "mode": "var",
    "pa": "std",
    "ca": "std",
    "ka": "std",
    "source": "Cryptogram 1991 bwd",
    "offset": 4527
   },
   "S": 33.69,
   "own_max": 2.35,
   "found": true,
   "read_exactly": true
  },
  "plantC_3": {
   "kind": "xstops",
   "key": {
    "method": "C",
    "mode": "vig",
    "pa": "kry",
    "ca": "kry",
    "ka": "kry",
    "source": "K3 cipher bwd",
    "offset": 32
   },
   "S": 44.77,
   "own_max": 2.73,
   "found": true,
   "read_exactly": true
  },
  "plantC_4": {
   "kind": "clean",
   "key": {
    "method": "C",
    "mode": "beau",
    "pa": "kry",
    "ca": "kry",
    "ka": "kry",
    "source": "K1+K2+K3 plain fwd",
    "offset": 128
   },
   "S": 47.21,
   "own_max": 4.4,
   "found": true,
   "read_exactly": true
  },
  "plantC_5": {
   "kind": "xstops",
   "key": {
    "method": "C",
    "mode": "beau",
    "pa": "kry",
    "ca": "kry",
    "ka": "std",
    "source": "Cryptogram 1991 bwd",
    "offset": 3182
   },
   "S": 31.3,
   "own_max": 2.4,
   "found": true,
   "read_exactly": true
  },
  "plantC_6": {
   "kind": "clean",
   "key": {
    "method": "C",
    "mode": "vig",
    "pa": "kry",
    "ca": "std",
    "ka": "std",
    "source": "Cryptogram 1991 fwd",
    "offset": 3834
   },
   "S": 44.78,
   "own_max": 3.16,
   "found": true,
   "read_exactly": true
  },
  "plantC_7": {
   "kind": "xstops",
   "key": {
    "method": "C",
    "mode": "beau",
    "pa": "kry",
    "ca": "kry",
    "ka": "std",
    "source": "K2 plain bwd",
    "offset": 205
   },
   "S": 47.76,
   "own_max": 2.55,
   "found": true,
   "read_exactly": true
  },
  "plantD_0": {
   "kind": "clean",
   "key": {
    "method": "D",
    "mode": "vig",
    "pa": "std",
    "ca": "kry",
    "ka": "kry",
    "kind": "cipher",
    "key": "ID"
   },
   "S": 32.03,
   "own_max": 3.08,
   "found": true,
   "read_exactly": true
  },
  "plantD_1": {
   "kind": "xstops",
   "key": {
    "method": "D",
    "mode": "var",
    "pa": "std",
    "ca": "kry",
    "ka": "kry",
    "kind": "cipher",
    "key": "BENIGNITY"
   },
   "S": 35.16,
   "own_max": 4.19,
   "found": true,
   "read_exactly": false
  },
  "plantD_2": {
   "kind": "clean",
   "key": {
    "method": "D",
    "mode": "var",
    "pa": "std",
    "ca": "std",
    "ka": "kry",
    "kind": "cipher",
    "key": "HYPERCONSCIENTIOUSNESS"
   },
   "S": 43.82,
   "own_max": 2.05,
   "found": true,
   "read_exactly": true
  },
  "plantD_3": {
   "kind": "xstops",
   "key": {
    "method": "D",
    "mode": "beau",
    "pa": "kry",
    "ca": "std",
    "ka": "kry",
    "kind": "cipher",
    "key": "ASSIMILATIVENESS"
   },
   "S": 36.03,
   "own_max": 3.54,
   "found": true,
   "read_exactly": false
  },
  "plantD_4": {
   "kind": "clean",
   "key": {
    "method": "D",
    "mode": "beau",
    "pa": "kry",
    "ca": "kry",
    "ka": "std",
    "kind": "cipher",
    "key": "ANEMOGRAPHICALLY"
   },
   "S": 33.63,
   "own_max": 3.85,
   "found": true,
   "read_exactly": true
  },
  "plantD_5": {
   "kind": "xstops",
   "key": {
    "method": "D",
    "mode": "var",
    "pa": "std",
    "ca": "kry",
    "ka": "std",
    "kind": "plain",
    "key": "TREILLAGE"
   },
   "S": 42.31,
   "own_max": 2.62,
   "found": true,
   "read_exactly": true
  },
  "plantD_6": {
   "kind": "clean",
   "key": {
    "method": "D",
    "mode": "var",
    "pa": "kry",
    "ca": "kry",
    "ka": "std",
    "kind": "cipher",
    "key": "LAUND"
   },
   "S": 39.07,
   "own_max": 2.6,
   "found": true,
   "read_exactly": true
  },
  "plantD_7": {
   "kind": "xstops",
   "key": {
    "method": "D",
    "mode": "beau",
    "pa": "kry",
    "ca": "std",
    "ka": "kry",
    "kind": "plain",
    "key": "MESODERMIC"
   },
   "S": 35.62,
   "own_max": 3.61,
   "found": true,
   "read_exactly": true
  },
  "plantE_0": {
   "kind": "clean",
   "key": {
    "method": "E",
    "mode": "vig",
    "pa": "kry",
    "ca": "std",
    "ka": "kry",
    "key": "NOVEMBER",
    "start": 5,
    "columnar": "DIGITAL",
    "order": "move_then_table"
   },
   "S": 35.58,
   "own_max": 2.41,
   "found": true,
   "read_exactly": true
  },
  "plantE_1": {
   "kind": "xstops",
   "key": {
    "method": "E",
    "mode": "vig",
    "pa": "std",
    "ca": "std",
    "ka": "std",
    "key": "WORLDCLOCK",
    "start": 3,
    "columnar": "USED",
    "order": "move_then_table"
   },
   "S": 33.51,
   "own_max": 2.84,
   "found": true,
   "read_exactly": false
  },
  "plantE_2": {
   "kind": "clean",
   "key": {
    "method": "E",
    "mode": "beau",
    "pa": "kry",
    "ca": "std",
    "ka": "kry",
    "key": "ID",
    "start": 0,
    "columnar": "COMPASS",
    "order": "move_then_table"
   },
   "S": 43.77,
   "own_max": 3.03,
   "found": true,
   "read_exactly": true
  },
  "plantE_3": {
   "kind": "xstops",
   "key": {
    "method": "E",
    "mode": "var",
    "pa": "kry",
    "ca": "std",
    "ka": "std",
    "key": "SHADOWFORCES",
    "start": 6,
    "columnar": "MADE",
    "order": "table_then_move"
   },
   "S": 45.32,
   "own_max": 2.37,
   "found": true,
   "read_exactly": true
  },
  "plantE_4": {
   "kind": "clean",
   "key": {
    "method": "E",
    "mode": "vig",
    "pa": "std",
    "ca": "kry",
    "ka": "kry",
    "key": "TUTANKHAMEN",
    "start": 0,
    "columnar": "WEBSTER",
    "order": "table_then_move"
   },
   "S": 45.43,
   "own_max": 2.67,
   "found": true,
   "read_exactly": true
  },
  "plantE_5": {
   "kind": "xstops",
   "key": {
    "method": "E",
    "mode": "var",
    "pa": "kry",
    "ca": "kry",
    "ka": "std",
    "key": "ENCUMBERED",
    "start": 9,
    "columnar": "THE",
    "order": "move_then_table"
   },
   "S": 32.77,
   "own_max": 3.0,
   "found": true,
   "read_exactly": false
  },
  "plantE_6": {
   "kind": "clean",
   "key": {
    "method": "E",
    "mode": "vig",
    "pa": "kry",
    "ca": "std",
    "ka": "std",
    "key": "LAYER",
    "start": 4,
    "columnar": "NORTHEAST",
    "order": "move_then_table"
   },
   "S": 37.61,
   "own_max": 3.17,
   "found": true,
   "read_exactly": true
  },
  "plantE_7": {
   "kind": "xstops",
   "key": {
    "method": "E",
    "mode": "vig",
    "pa": "kry",
    "ca": "std",
    "ka": "kry",
    "key": "SOMEWHERE",
    "start": 5,
    "columnar": "VIRTUALLYINVISIBLE",
    "order": "table_then_move"
   },
   "S": 38.55,
   "own_max": 3.67,
   "found": true,
   "read_exactly": true
  }
 },
 "k4_best_readings": {
  "A": [
   "EPOTGETEUCNCHBEYDETHSLYPOFTYAABSRFADESMRPPFNZSKYSGLESCUFOOLHELDSJROPDNYTRSIMFZGMWBIFOUONZUCUSOBSA",
   {
    "method": "A",
    "mode": "var",
    "pa": "std",
    "ca": "kry",
    "ka": "kry",
    "key": "MEZUZAH",
    "start": 4
   }
  ],
  "B": [
   "RDALSRDRIONBLURSJPFLCUSLIXPACBTAEJSDWMEEXBJCKARSCFPSABEZBOFJDUVIADIODOSHDAZVZZZGMNNZBIANMELEEARAC",
   {
    "method": "B",
    "mode": "vig",
    "pa": "kry",
    "ca": "VIRTUALYNSBECDFGHJKMOPQWXZ",
    "ka": "std",
    "key": "TOTALLY",
    "start": 2
   }
  ],
  "C": [
   "SORDYKNOXGCWPBJRMAPCHSQMBGISTYSTOTARTPWRENOWJOTSTWEINHLQZTHTEZNEOFWHAROYBDHHOVFFBEVBIRECASOFMAMWE",
   {
    "method": "C",
    "mode": "beau",
    "pa": "kry",
    "ca": "kry",
    "ka": "kry",
    "source": "carter vol1 fwd",
    "offset": 45124
   }
  ],
  "D": [
   "AFLUEJTKWYOROMEGGSSNAMXWRCWAIDANIZPPPFOLFNUTCREMLTYDUPEADDLEXFEWIKNOTCHOBIKILIAFNXNMIMPMKFIFAYYFS",
   {
    "method": "D",
    "mode": "var",
    "pa": "kry",
    "ca": "std",
    "ka": "kry",
    "kind": "plain",
    "key": "NEATLY"
   }
  ],
  "E": [
   "LRESBAMVEGLMVCDHFGHOFTESWTFUZAKPHEDKEAPOSSIXLYWEBOYFARWRFHEINEMQIUVZHURHOJYEVJMQNESHOCKVHKSCUDIEU",
   {
    "method": "E",
    "mode": "var",
    "pa": "kry",
    "ca": "kry",
    "ka": "kry",
    "key": "SCHEIDT",
    "start": 0,
    "columnar": "TRANSMIT",
    "order": "move_then_table"
   }
  ]
 },
 "compute_seconds": 801
}
```

Notes: K4 statistic 2.23 (method C), p 0.099 against 100 shuffles; plant power A 8/8, B 8/8, C 8/8, D 8/8, E 8/8; decided ['A', 'B', 'C', 'D', 'E']


