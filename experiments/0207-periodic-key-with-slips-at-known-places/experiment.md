# 0207-periodic-key-with-slips-at-known-places: A1.2, step 1: a repeating key on the sculpture's tables with one, two or three of the 24 known letters carved wrong (a slip), every key length 1-26, exact, judged against scrambled copies, with planted slipped messages

**Family:** 1-keyed-periodic  
**Parent:** 0005-quagmire-period-sweep-forced-keys  
**Decision:** reverted  
**Run:** 2026-10-20T12:14:27+00:00, 41.9 s, status ran  
**Time by phase:** design 261 s, implement 83 s, test 45 s, run 42 s, record 64 s

## In plain words

K1 and K2 were enciphered with a repeating secret word on a printed table. Sanborn did it by hand and admits he was sloppy; if he took the wrong row of the table at one or two of the places we know, the old test, which needs all 24 known letters to agree, would have thrown away the right answer. Here we let one, two or three of them disagree, for every word length up to 26, and read what comes out. A language model reads the results without knowing which come from the real carving and which from scrambled copies of it, which is how we tell a real reading from luck. We also hide three messages of our own, with deliberate slips, and check that the search finds them.

## Walkthrough, by hand

1. Take the KRYPTOS table, a key word of length 13, and write the 24 known places with their slot (place minus 1, mod 13).
2. At each known place read off the key letter that turns the known letter into the carved one.
3. Places in the same slot should give the same key letter; where two disagree, one of them is a slip.
4. Count the slips the cheapest choice needs in every slot and add them up.
5. With 3 or fewer slips the setting lives: decrypt every letter with the chosen key letters.
6. Do the same on scrambled copies of the carving, and compare how many settings live and how well they read.

## Worked example (generated)

```
key length 13, KRYPTOS table on both sides, added form: key letter forced at each known place, by slot

  slot  0: 27:O->Q key P, 66:R->P key C   slips needed 1
  slot  1: 28:R->P key C, 67:L->V key F   slips needed 1
  slot  2: 29:T->R key X, 68:I->T key P   slips needed 1
  slot  3: 30:H->N key F, 69:N->T key L   slips needed 1
  slot  4: 31:E->G key C, 70:C->M key J   slips needed 1
  slot  5: 32:A->K key T, 71:L->Z key I   slips needed 1
  slot  6: 33:S->S key A, 72:O->F key H   slips needed 1
  slot  7: 34:T->S key C, 73:C->P key U   slips needed 1
  slot  8: 22:E->F key B, 74:K->K key A   slips needed 1
  slot  9: 23:A->L key K   slips needed 0
  slot 10: 24:S->R key V   slips needed 0
  slot 11: 25:T->V key S, 64:B->N key L   slips needed 1
  slot 12: 26:N->Q key B, 65:E->Y key R   slips needed 1

slips needed at length 13: 11 (more than 3: dead)
```

## Lineage

Inherits from 0005-quagmire-period-sweep-forced-keys. What changed: A1.2 (Stage 2, step 2, issue #76), first half: the tables. 0005 required all 24 known letters to agree with one repeating key (no slip). Here k = 1, 2, 3 of the 24 checks may fail, as they would if Sanborn took a wrong row or column of his chart at k of the known places. Every key length 1-26 on the 8 table classes (plain and cipher alphabet standard or KRYPTOS, added or Beaufort form; the key alphabet drops out), exact, K4 against 20 scrambled copies at the same k; every consistent setting's reading goes through the quadgram cut and the blind judge with the copies' readings in the same call; three planted messages with 2 or 3 slips at known places in the same run.

## Hypothesis (domain expert)

A1 (knowledge/12-assumptions.md): every exact verdict assumed no enciphering slip; K1-K3 carry one enciphering slip (K2's dropped S) and the PALIMPCEST worksheet shows Sanborn working one letter at a time against a written-out key (C27(a), 01-facts.md). Sanborn 2005: 'Saying I was sloppy is a good way of saying it' (02-sanborn-said.md). Scheidt 2015: if Jim made an encoding error he would not have known (03-scheidt-said.md). C1(c) and C27(c) for the table; C17(a)/(b) for a copper not as intended. Model: c_i = C[P(p_i) + k[i mod L]] or C[k[i mod L] - P(p_i)] with P, C each the standard or KRYPTOS alphabet (8 classes; variant Beaufort is the added form with the key negated; the key alphabet only relabels key values). A slip at known place q: the carved letter is not the one the key gives. For key length L each known place forces a key value in its slot (q - 1 mod L); a setting is a choice of value per slot among the values its known letters force; its number of slips is the number of known letters that disagree with their slot's chosen value. A slip at a known place alone in its slot fails no check: it garbles one column of the reading and is A1.0's case (the judge reads through it). Statistic: settings with exactly d = 0-3 failed checks per length, K4 against each copy; and the blind judge's best score on each text's readings. Cost of naming the slips: 4.7 k + log2 C(24, k) bits (9.3, 17.5, 25.1 for k = 1, 2, 3). Key lengths 27-29 and 53+ have no check at all on these tables, so no slip can show there and they are not rerun (F1/2, 0034, 0048, 0053).

## Prediction

On K4 no setting with 3 or fewer slips exists at key lengths 1-23 (at least 7 checks there, so 4 or more must hold by chance); at 24-26 settings exist on K4 and on every copy in about equal numbers, because 1-5 checks are all there is. No K4 reading clears the quadgram cut or scores above every copy's best with the judge. The three planted messages (key lengths 13, 20 and 25, with 2, 3 and 3 slips) are found, each its own text's top reading by the judge and above all of its own copies. Zero candidates pass gate 4.

## Method

1. For each text, key length L 1-26 and class, the forced key value at each known place.
2. Per slot: its distinct values, each with the number of its known letters that would then be slips.
3. Enumerate every setting with at most 3 slips (depth first over the slots).
4. Count by number of slips; K4 against 20 copies.
5. Each setting's reading ('?' where no known letter fixes the slot), quadgram score of the letters outside the known places.
6. For every text, its best reading and every reading at or above -5.0 go to the judge, K4's, the copies', the plants' and the plants' copies' in one call.
7. A text's reading counts only above every one of its own copies' best.

## Result

Candidates returned: 50. Passed all gates: 0. Best crib hits among all candidates: 24/24
(EAST 4/4, NORTHEAST 9/9, BERLIN 6/6, CLOCK 5/5).
Best loss: 5.301631602761004 (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | baseline | 24/24 | -8.926 | `LZMTOMNOHHULBGUNYUVRIEASTNORTHEASTOTWTEYLGHMUWIOWYQHMNOBYAXINFBBERLINCLOCKUDBMBRRZCEIGKUVACKTESMA` | key length 25, std/std vig, slips at [22, 24, 73], 4 slots open (filled with A) |
| 2 | baseline | 24/24 | -8.935 | `LZMTOMNOHHULBGUNYUVRIEASTNORTHEASTOTWTEYLGHMUWIMWYQHMNOBYAXINFBBERLINCLOCKUDBMBRRZCEIGKUVACKTESMA` | key length 25, std/std vig, slips at [22, 23, 24], 4 slots open (filled with A) |
| 3 | baseline | 24/24 | -9.323 | `CAUTFMCTMMFJSOBDSAJMNEASTNORTHEASTVWDWAAENGLJKRSWIDSUDFHLRCLHOSBERLINCLOCKSUYUVCNKPPLNAFGLNMBRLDP` | key length 25, std/kry beau, slips at [72, 73, 74], 4 slots open (filled with A) |
| 4 | baseline | 24/24 | -8.977 | `LZMTOMNOHHULBGUNYUVRIEASTNORTHEASTOTWTEYLGHMUWIOXYQHMNOBYAXINFBBERLINCLOCKUDBMBRRZCEIGKUVACKTESMA` | key length 25, std/std vig, slips at [22, 73, 74], 4 slots open (filled with A) |
| 5 | baseline | 24/24 | -9.150 | `PGWMZEEKSAQSHTDABYNRJEASTNORTHEASTHNVHPTOFMIVDNOMIYFZWATGWDQGORBERLINCLOCKMUFGHCSDAKVMDQAIGSKSYWC` | key length 26, kry/std vig, slips at [74], 3 slots open (filled with A) |
| 6 | baseline | 24/24 | -9.341 | `CAUTFMCTMMFJSOBDSAJMNEASTNORTHEASTVWDWAAENGLJKRSNIDSUDFHLRCLHOSBERLINCLOCKSUYUVCNKPPLNAFGLNMBRLDP` | key length 25, std/kry beau, slips at [24, 72, 73], 4 slots open (filled with A) |
| 7 | baseline | 24/24 | -9.371 | `CAUTFMCTMMFJSOBDSAJMNEASTNORTHEASTVWDWAAENGLJKRGWIDSUDFHLRCLHOSBERLINCLOCKSUYUVCNKPPLNAFGLNMBRLDP` | key length 25, std/kry beau, slips at [23, 72, 74], 4 slots open (filled with A) |
| 8 | baseline | 24/24 | -9.024 | `LZMTOMNOHHULBGUNYUVRIEASTNORTHEASTOTWTEYLGHMUWIMXYQHMNOBYAXINFBBERLINCLOCKUDBMBRRZCEIGKUVACKTESMA` | key length 25, std/std vig, slips at [22, 23, 74], 4 slots open (filled with A) |
| 9 | baseline | 24/24 | -9.383 | `CAUTFMCTMMFJSOBDSAJMNEASTNORTHEASTVWDWAAENGLJKBSWIDSUDFHLRCLHOSBERLINCLOCKSUYUVCNKPPLNAFGLNMBRLDZ` | key length 25, std/kry beau, slips at [22, 73, 74], 4 slots open (filled with A) |
| 10 | baseline | 24/24 | -9.201 | `PGWMZEEKSAQSHTDABYNRJEASTNORTHEASTHNVHPTOFMIVDNIMIYFZWATGWDQGORBERLINCLOCKMUFGHCSDAKVMDQAIGSKSYWC` | key length 26, kry/std vig, slips at [22], 3 slots open (filled with A) |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "periodic key on the sculpture's tables, k known letters slipped (A1.2 tables)",
 "classes": 8,
 "key_lengths": "1-26",
 "slips": "0-3 at the 24 known places (exact enumeration)",
 "not_rerun": "key lengths 27-29 and 53+: no check on these tables, so a slip cannot show (F1/2)",
 "slip_cost_bits": {
  "1": 9.3,
  "2": 17.5,
  "3": 25.1
 },
 "by_length": {
  "1": {
   "checks": 23,
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ]
  },
  "2": {
   "checks": 22,
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ]
  },
  "3": {
   "checks": 21,
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ]
  },
  "4": {
   "checks": 20,
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ]
  },
  "5": {
   "checks": 19,
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ]
  },
  "6": {
   "checks": 18,
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ]
  },
  "7": {
   "checks": 17,
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ]
  },
  "8": {
   "checks": 16,
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ]
  },
  "9": {
   "checks": 15,
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ]
  },
  "10": {
   "checks": 14,
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ]
  },
  "11": {
   "checks": 13,
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ]
  },
  "12": {
   "checks": 12,
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ]
  },
  "13": {
   "checks": 11,
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ]
  },
  "14": {
   "checks": 11,
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ]
  },
  "15": {
   "checks": 9,
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ]
  },
  "16": {
   "checks": 8,
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ]
  },
  "17": {
   "checks": 7,
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ]
  },
  "18": {
   "checks": 7,
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ]
  },
  "19": {
   "checks": 9,
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ]
  },
  "20": {
   "checks": 11,
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ]
  },
  "21": {
   "checks": 11,
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ]
  },
  "22": {
   "checks": 9,
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ]
  },
  "23": {
   "checks": 7,
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    0
   ]
  },
  "24": {
   "checks": 5,
   "k4": [
    0,
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0,
    16
   ],
   "k4_rank_by_total": 20
  },
  "25": {
   "checks": 3,
   "k4": [
    0,
    0,
    0,
    64
   ],
   "copies_min": [
    0,
    0,
    0,
    48
   ],
   "copies_max": [
    0,
    0,
    8,
    64
   ],
   "k4_rank_by_total": 6
  },
  "26": {
   "checks": 1,
   "k4": [
    0,
    16,
    0,
    0
   ],
   "copies_min": [
    0,
    12,
    0,
    0
   ],
   "copies_max": [
    2,
    16,
    0,
    0
   ],
   "k4_rank_by_total": 11
  }
 },
 "shortest_length_by_slips": {
  "K4": [
   null,
   26,
   null,
   25
  ],
  "copies": [
   [
    null,
    26,
    25,
    25
   ],
   [
    null,
    26,
    null,
    25
   ],
   [
    null,
    26,
    25,
    25
   ],
   [
    26,
    26,
    25,
    25
   ],
   [
    26,
    26,
    25,
    24
   ],
   [
    26,
    26,
    null,
    25
   ],
   [
    null,
    26,
    null,
    25
   ],
   [
    null,
    26,
    25,
    25
   ],
   [
    null,
    26,
    null,
    25
   ],
   [
    null,
    26,
    25,
    25
   ],
   [
    26,
    26,
    25,
    25
   ],
   [
    null,
    26,
    25,
    25
   ],
   [
    26,
    26,
    null,
    25
   ],
   [
    null,
    26,
    25,
    25
   ],
   [
    26,
    26,
    25,
    25
   ],
   [
    null,
    26,
    25,
    25
   ],
   [
    26,
    26,
    25,
    24
   ],
   [
    26,
    26,
    25,
    25
   ],
   [
    null,
    26,
    25,
    25
   ],
   [
    26,
    26,
    null,
    24
   ]
  ]
 },
 "judge": {
  "sent": 62,
  "none": 0,
  "cut": -5.0,
  "rule": "each text's best reading by quadgrams plus every reading at or above the cut; one call"
 },
 "k4_settings": 80,
 "k4_best_quad": -7.534,
 "k4_judge_best": 3,
 "copies_judge_best": [
  8,
  2,
  3,
  2,
  3,
  2,
  2,
  3,
  3,
  2,
  4,
  2,
  3,
  2,
  6,
  2,
  3,
  4,
  1,
  6
 ],
 "k4_readings_above_every_copy": 0,
 "copies_best_quad": [
  -7.177,
  -7.629,
  -7.141,
  -7.874,
  -7.342,
  -7.507,
  -7.566,
  -7.331,
  -7.75,
  -7.814,
  -7.12,
  -7.582,
  -7.603,
  -7.517,
  -7.433,
  -7.476,
  -7.524,
  -7.428,
  -7.565,
  -7.181
 ],
 "plants": [
  {
   "name": "plant1",
   "seed": 2071,
   "key_length": 13,
   "class": "kry/kry/vig",
   "slips": [
    71,
    74
   ],
   "k": 2,
   "settings_by_slips": {
    "13": [
     0,
     0,
     4,
     0
    ],
    "25": [
     0,
     0,
     4,
     56
    ],
    "26": [
     0,
     16,
     0,
     0
    ]
   },
   "own_copies_settings_at_length": [
    [
     0,
     0,
     0,
     0
    ],
    [
     0,
     0,
     0,
     0
    ],
    [
     0,
     0,
     0,
     0
    ],
    [
     0,
     0,
     0,
     0
    ],
    [
     0,
     0,
     0,
     0
    ],
    [
     0,
     0,
     0,
     0
    ],
    [
     0,
     0,
     0,
     0
    ],
    [
     0,
     0,
     0,
     0
    ],
    [
     0,
     0,
     0,
     0
    ],
    [
     0,
     0,
     0,
     0
    ]
   ],
   "planted_setting_found": true,
   "planted_slips_named": [
    71,
    74
   ],
   "planted_quad": -4.742,
   "planted_judge": 88,
   "planted_judge_reading": "NGS SCEPTRE OF GOLD AND LA ????????????? GLASS B TWO SISTRA OF WOOD GILT AND B ??????????? RONE AND FOOTSTOOL BENEATH",
   "own_copies_judge_best": [
    3,
    2,
    3,
    3,
    2,
    3,
    4,
    3,
    2,
    2
   ],
   "found": true
  },
  {
   "name": "plant2",
   "seed": 2072,
   "key_length": 20,
   "class": "std/kry/beau",
   "slips": [
    28,
    64,
    70
   ],
   "k": 3,
   "settings_by_slips": {
    "20": [
     0,
     0,
     0,
     8
    ],
    "25": [
     0,
     0,
     0,
     64
    ],
    "26": [
     0,
     16,
     0,
     0
    ]
   },
   "own_copies_settings_at_length": [
    [
     0,
     0,
     0,
     0
    ],
    [
     0,
     0,
     0,
     0
    ],
    [
     0,
     0,
     0,
     0
    ],
    [
     0,
     0,
     0,
     0
    ],
    [
     0,
     0,
     0,
     0
    ],
    [
     0,
     0,
     0,
     0
    ],
    [
     0,
     0,
     0,
     0
    ],
    [
     0,
     0,
     0,
     0
    ],
    [
     0,
     0,
     0,
     0
    ],
    [
     0,
     0,
     0,
     0
    ]
   ],
   "planted_setting_found": true,
   "planted_slips_named": [
    28,
    64,
    70
   ],
   "planted_quad": -4.652,
   "planted_judge": 85,
   "planted_judge_reading": "?T OUT AGAIN AND T ??????? ############# ??????? BBLES WE MUST CO ??????? RS ########### ??????? CTUAL WORK IN TH ???",
   "own_copies_judge_best": [
    2,
    2,
    3,
    3,
    3,
    3,
    2,
    3,
    2,
    2
   ],
   "found": true
  },
  {
   "name": "plant3",
   "seed": 2073,
   "key_length": 25,
   "class": "kry/std/vig",
   "slips": [
    22,
    73,
    74
   ],
   "k": 3,
   "settings_by_slips": {
    "25": [
     0,
     0,
     4,
     56
    ],
    "26": [
     0,
     16,
     0,
     0
    ]
   },
   "own_copies_settings_at_length": [
    [
     0,
     0,
     4,
     56
    ],
    [
     0,
     0,
     4,
     56
    ],
    [
     0,
     0,
     0,
     64
    ],
    [
     0,
     2,
     4,
     48
    ],
    [
     0,
     0,
     0,
     64
    ],
    [
     0,
     0,
     0,
     64
    ],
    [
     0,
     0,
     0,
     64
    ],
    [
     0,
     0,
     0,
     64
    ],
    [
     0,
     0,
     0,
     64
    ],
    [
     0,
     0,
     8,
     48
    ]
   ],
   "planted_setting_found": true,
   "planted_slips_named": [
    22,
    73,
    74
   ],
   "planted_quad": -4.023,
   "planted_judge": 82,
   "planted_judge_reading": "OULDERS AN? ? ? ? PERFORAT? ? ? ? ESE CORRESPONDING EXACT ? ? ? ? N THE SCALES ? ? ? ? ED THAT THE",
   "own_copies_judge_best": [
    5,
    2,
    3,
    3,
    3,
    2,
    2,
    3,
    6,
    2
   ],
   "found": true
  }
 ],
 "decidable": "the remaining checks (24 minus the slots the known letters touch, minus k) decide the key at lengths 1-23 (7-23 checks, 4-20 after 3 slips); at 24-26 only 5, 3, 1 checks exist, so 3 slips leave 2, 0, 0 and the readings alone decide",
 "controls": "20 shuffled copies (seeds 2070-2089); each plant against 10 shuffles of its own ciphertext",
 "exhaustive": "yes"
}
```

Notes: K4 settings with <= 3 slips: 80 (shortest length by slips [None, 26, None, 25]); judge sent 62, K4 best 3, copies best 8; plants found [True, True, True]


