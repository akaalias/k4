# 0236-f13-one-free-alphabet-ciphertext-only-power-first: F13.4c: one free alphabet with a periodic key (Quagmire III, both forms), lengths 1-19, from the ciphertext alone: power on planted messages first, then K4 against 50 climbed shuffles in the lengths the plants decide

**Family:** 13-ciphertext-only  
**Parent:** 0234-f13-periodic-key-on-the-sculptures-tables-ciphertext-only  
**Decision:** reverted  
**Run:** 2026-10-27T21:00:31+00:00, 1024.3 s, status ran  
**Time by phase:** test 5 s, run 1024 s, record 70 s

## In plain words

The same as before, but now the table's alphabet is also unknown: any of the 400 million million million million orders of the 26 letters. Without the clue words the computer has to guess the alphabet and the secret word together from how English the result looks. First we find out, with hidden test messages, up to what word length that can work at all; only there do we compare K4 with shuffles of itself.

## Walkthrough, by hand

1. Hide a test message under a shuffled alphabet and a short repeating key.
2. Let the computer swap alphabet letters and change key letters, keeping changes that make the text read more like English, with some randomness to escape dead ends.
3. Do the same to six shuffles of the hidden message's letters; if the message scores above all six, it was found.
4. Repeat at longer keys until test messages stop being found.
5. Only at the key lengths where they are found, compare K4 with 50 shuffles of itself.

## Worked example (generated)

```
A planted message from K3's own words, a shuffled alphabet and a key of 3, Beaufort form, no known letter:

  alphabet, true   CKEMJNZWSYGDRPVFBHOAQULXIT
  carved           TUMWQZNVALJNNTWAEBRQETUMIURULMRRRMJMPPVLXYNYMTQBEVNXGASHZDCMBGCTBLPGZNVYBQBTUMRQPUNWTUWAGELCULK
  alphabet, found  TUYVAIMHKQPEWRJLDZXBSCNGFO
  reading          THEJOTAIRESCAKINGFROMTHECHAOBERCASSEDFJEDLAMETOFLICKERMUTPREHENTLYDETAILHOFTHEROHOWITHINEMERDETRN

  letters right: 81 of 97
```

## Lineage

Inherits from 0234-f13-periodic-key-on-the-sculptures-tables-ciphertext-only. What changed: F13.4c (issue #85). F1.5's design 2 (0140's compiled parallel tempering) is run with no known letter: every key slot free, no check-keeping, the alphabet and key climbed together by quadgrams, a second form (added) beside 0140's Beaufort. A probe before this run (one tempering run per plant) read 54 of 97 letters of a plant at length 5 and nothing at 10 or 15, so power comes first, in the same run: 8 plants at each of the lengths 2-8, 10, 13, 16, 19 (no known words; half X stops; half each form), each against 6 own shuffles climbed the same way (null 1/7), 3 tempering runs per text, best reading rescored by MIX8m. Then K4 and 50 shuffles at every length 1-19 in both forms; the statistic is the largest z-score over the cells the plants decide (6 of 8). Cost stated before the run: 616 + 1,938 climbs x about 10 s, about 7 core-hours.

## Hypothesis (domain expert)

F1.1 (Quagmire III with an unknown order: K1-K2's system with Sanborn's 'slightly different' chart, C27(c)) read without the 24 known letters: the hedge for A1/A2 on the family closed exactly at 1-22, 24, 25 (0119) and reopened at Beaufort 23 and 26 (0228, 0229). F13.1 puts one free alphabet decidable by quadgrams to length 19 (80 bits for the alphabet plus 4.7 per key letter, under 173), which is necessary, not sufficient: a climb must also find the key, and with no known letter design 2 has no anchor. Pre-registered: a cell (length, form) is decided when the planted length bracketing it from above found at least 6 of 8 (lengths below the shortest failing planted length); S = max z over decided cells against 50 shuffles; K4 flags at p < 0.05. If no length is decided the item is blocked by power with the numbers.

## Prediction

Plants found at lengths 2-4, some at 5-6, none from 8: the decided range ends near 5. K4 inside its shuffles in that range (p above 0.05). F13.4c closed for the short lengths, blocked from about 6 by power.

## Method

1. Plants: Carter's held-out last 20% (clean or X stops), a random alphabet, key and form, lengths 2-8, 10, 13, 16, 19; 8 per length; 6 own shuffles each.
2. Every text climbed at its length and form: 3 runs of 0140's parallel tempering (16 replicas x 625 rounds x 1,000 moves), no known letter, the best reading rescored by MIX8m (0233).
3. A plant is found when its score is above all 6 own shuffles'. A cell is decided below the first planted length under 6 of 8.
4. K4 and 50 shuffles of K4 at every length 1-19 and both forms, climbed the same way; S = max z over decided cells; K4 ranked.
5. K4's best reading per decided cell submitted (key: alphabet, form, shifts) for the harness's gates.

## Result

Candidates returned: 10. Passed all gates: 0. Best crib hits among all candidates: 5/24
(EAST 0/4, NORTHEAST 3/9, BERLIN 1/6, CLOCK 1/5).
Best loss: 192.65850614735126 (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | cribs | 2/24 |  | `UGAWOUMUBVONGSUNFIGGRINWHYYZWLBASSUEREYSDYSSTAPPRKEDANOJFKRFLIGLQZHEEXPIZARBJAPMEDCJFBAOVOKOTACKW` |  |
| 2 | cribs | 3/24 |  | `MGAKIMVMSDINGFMNYUGGRUNKWOOLKHSAFFMEREOFCOFFJAPPRTECANIBYTRYHUGHQLWEEXPULARSBAPVECZBYSAIDITIJAZTK` |  |
| 3 | cribs | 2/24 |  | `NHPPIUJULBIDDANDUNDHANGPEYMRZFLECANTATMAXYCAVERCASHIPDILUSAJONDFFRETHGRNKEAMBERWHISLUMPOTOWOVESSZ` |  |
| 4 | cribs | 0/24 |  | `UGHDOWLWPVONNOUNTINGAIXDEFMHYPPECOURARMOFFCOVEDCALITHNOSTLAYBINPRHERIJDIGEAKZEDBITSSTKHAKAWAVESLY` |  |
| 5 | cribs | 0/24 |  | `LYAWIREKHKINBNROUSBYDIFOYPYMALTOFAKERCYAMYANTHECRRECONNHISGIULPUBBYCEPESMODTHADVECTWFWANDUSITHTKW` |  |
| 6 | cribs | 2/24 |  | `QGULLADDJFLTIHABYDIGHJUSSVEOWLYNPTDOUFETMETHICEYUCORNTGOWERWATMAINSFOWEDONHYOUPPORACKBUGSFELICABL` |  |
| 7 | cribs | 1/24 |  | `BTHODHERNORTOASTRLAGALVOCEMKIMYPKASLABMFLEOFTINWASWISFRARSTJGLANFULLENNSHITBUINCERFARCHUPPBUTIFDI` |  |
| 8 | cribs | 0/24 |  | `VYCIMAKCOMARTINRELUZALTIPSIGURJVKINWAHIONSFODEEMANMPJPATENDAYLUSHTYWIVENSEDFREEHIDSTEWCEFOREDESQU` |  |
| 9 | cribs | 2/24 |  | `GHISSGPABRAAFREQUBGWWOUSPLESSTORPREITEOUSEPROFSMEMINITSCUOECHOFFLECELAYOSABOMICKINGHCORLDSUITAIUK` |  |
| 10 | cribs | 5/24 |  | `HQATIHAEFUGISALUSZKEPOWTORCOTHENTALAYINFICTAWYEROBARAPIOSMORTOSINCHIMSBOOLKELASTARHERENPRILMFLXLF` |  |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "item": "F13.4c",
 "search_reads_known_letters": false,
 "forms": [
  "beaufort",
  "added"
 ],
 "search": "0140's parallel tempering, no known letter, 3 runs x 16 replicas x 625 rounds x 1000 moves; MIX8m rescoring",
 "plant_power": {
  "2": [
   8,
   8
  ],
  "3": [
   8,
   8
  ],
  "4": [
   7,
   8
  ],
  "5": [
   7,
   8
  ],
  "6": [
   4,
   8
  ],
  "7": [
   5,
   8
  ],
  "8": [
   3,
   8
  ],
  "10": [
   3,
   8
  ],
  "13": [
   2,
   8
  ],
  "16": [
   4,
   8
  ],
  "19": [
   3,
   8
  ]
 },
 "plant_letters_right": {
  "2": [
   87,
   90,
   79,
   92,
   90,
   93,
   71,
   91
  ],
  "3": [
   58,
   22,
   69,
   82,
   68,
   70,
   87,
   78
  ],
  "4": [
   20,
   44,
   40,
   17,
   5,
   72,
   29,
   15
  ],
  "5": [
   11,
   27,
   0,
   24,
   16,
   33,
   6,
   11
  ],
  "6": [
   6,
   19,
   10,
   30,
   5,
   11,
   4,
   19
  ],
  "7": [
   27,
   6,
   10,
   15,
   17,
   15,
   5,
   4
  ],
  "8": [
   12,
   8,
   25,
   1,
   35,
   7,
   24,
   10
  ],
  "10": [
   13,
   23,
   11,
   12,
   13,
   28,
   9,
   14
  ],
  "13": [
   8,
   5,
   9,
   5,
   18,
   14,
   5,
   13
  ],
  "16": [
   6,
   14,
   15,
   4,
   10,
   13,
   8,
   15
  ],
  "19": [
   5,
   10,
   27,
   5,
   4,
   4,
   5,
   14
  ]
 },
 "decided_up_to_length": 5,
 "decided_cells": [
  "1/beaufort",
  "1/added",
  "2/beaufort",
  "2/added",
  "3/beaufort",
  "3/added",
  "4/beaufort",
  "4/added",
  "5/beaufort",
  "5/added"
 ],
 "k4_z_by_cell": {
  "1/beaufort": 1.243,
  "1/added": 0.125,
  "2/beaufort": 1.08,
  "2/added": 1.167,
  "3/beaufort": -1.039,
  "3/added": -0.981,
  "4/beaufort": -0.077,
  "4/added": 0.763,
  "5/beaufort": 1.667,
  "5/added": 0.802
 },
 "k4_statistic": 1.6670400541040789,
 "k4_p": 0.37254901960784315,
 "k4_copies": 50,
 "climbs": 2554,
 "expected_total_time": "2,554 climbs x about 10 s, about 7 core-hours",
 "exhaustive": false,
 "compute_seconds": 990
}
```

Notes: plant power L2 8/8, L3 8/8, L4 7/8, L5 7/8, L6 4/8, L7 5/8, L8 3/8, L10 3/8, L13 2/8, L16 4/8, L19 3/8; decided to length 5; K4 statistic 1.67, p 0.373


