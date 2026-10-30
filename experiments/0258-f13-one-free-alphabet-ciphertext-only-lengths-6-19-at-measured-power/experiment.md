# 0258-f13-one-free-alphabet-ciphertext-only-lengths-6-19-at-measured-power: F13.4c at key lengths 6-19 (D3): one free alphabet with a periodic key, ciphertext only, K4 against 100 fresh shuffles climbed by 0236's frozen search, closed at the measured power

**Family:** 13-ciphertext-only  
**Parent:** 0236-f13-one-free-alphabet-ciphertext-only  
**Decision:** reverted  
**Run:** 2026-10-30T04:12:03+00:00, 8500.3 s, status ran  
**Time by phase:** test 10 s, run 8500 s, record 70 s

## In plain words

Suppose Sanborn used the cipher table with his own scrambled alphabet and a repeating key of 6 to 19 letters, and suppose we did not know any of the words he gave away. Our search can still find such messages sometimes, two to five times in eight. We run it on K4 and on 100 scrambled copies of K4 and ask whether K4 reads better than the copies. Only after that do we look at whether the known words came out in place.

## Walkthrough, by hand

1. Write a scrambled alphabet and a key of, say, 11 numbers.
2. To read the ciphertext, take each letter's place in the alphabet, subtract the key number for that position (Beaufort: subtract the place from the key), and read the alphabet at the result.
3. A computer searches alphabets and keys for the most English-looking reading of K4, without looking at the known words.
4. The same search runs on 100 scrambled copies of K4.
5. K4 counts only if it reads better than every copy; then the 24 known letters are checked.

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

Inherits from 0236-f13-one-free-alphabet-ciphertext-only. What changed: D3 (issue #77, Alexis #100: run power-blocked cells at their measured power). 0236 measured its search's power at 6-19 (plants 2-5 of 8) and climbed K4 there, but decided and recorded K4 only at 1-5, where power was 7-8 of 8. Here 0236's per-text search, unchanged (imported from its record), on K4 and 100 fresh shuffles at every length 6-19 in both forms, every cell recorded; plants at 6, 7, 8, 10, 13, 16, 19 redrawn in the same run (8 each, 6 own copies).

## Hypothesis (domain expert)

F13.4c: a periodic key on one free alphabet (Quagmire III with an unknown order, both forms), solved from the ciphertext alone: the search never reads the 24 known letters (program.md, F13); gate 2 checks them at keep time. 0236's design-2 tempering without known letters, 3 runs x 16 replicas x 625 rounds x 1000 moves, MIX8m rescoring (0233). F13.1 puts one free alphabet with a key within reach of 97 letters to length 19 by quadgrams; 0236 found the search's power falls from 7/8 at 5 to 2-5/8 at 6-19. Statistic: per cell, K4's MIX8m against the shuffles' (z); over the 28 cells the largest z against the shuffles' own largest z. Clue entries C27(c), C5(a).

## Prediction

K4 inside its shuffles: largest z over the 28 cells with p above 0.05; no cell where K4 beats all 100. Plant power as 0236 (2-5 of 8 at 6-19). K4's readings put at most 5 of the 24 known letters in place (harness gate 2).

## Method

1. Texts: K4 and 100 shuffles of K4 (seed 2560).
2. Each text at every key length 6-19 and both forms (Beaufort, added): 0236's climb(), unchanged.
3. Plants: 8 per length at 6, 7, 8, 10, 13, 16, 19 (0236's rule: Carter test windows, half with X stops, a random alphabet and key, forms alternating), 6 own shuffles each; found when above all its own copies.
4. Per cell: K4's rank among the 100 and its z; the statistic is the largest z, its p from the shuffles' own largest z.

## Result

Candidates returned: 28. Passed all gates: 0. Best crib hits among all candidates: 3/24
(EAST 1/4, NORTHEAST 2/9, BERLIN 0/6, CLOCK 0/5).
Best loss: 212.61476196518927 (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | cribs | 0/24 |  | `DHOUNCKSCKNETOKNCMTHROLDERYVKINEMAWHANYATSSOTHEBAYEDREMLDSONGGALSGENETEMIERIGAHMEDIRPFORAYWITHIKC` |  |
| 2 | cribs | 2/24 |  | `KDISLALSMALPANSEMHADTOBYOFFITWHINGCESOFGOLINALAMSVONGPEEURROURDMEFOOODAHMITBYTRGONSKDMIYDSTBALSUP` |  |
| 3 | cribs | 1/24 |  | `IRORCHEINNINCDISTHECASSPAPROUGZETUPMVIGTENFLDERMANOFENSSOFCULLIACRASARDAREKISHKMTOBSONOIMSWRIODIQ` |  |
| 4 | cribs | 1/24 |  | `OVEOFKTONATCOMOEYSTOAFEDEMABRWOAENDTOFFECHSTBAURAABRACHSIDINGIGNALESWIZULANDSKMCCOMSINETIHEUSEDYS` |  |
| 5 | cribs | 0/24 |  | `UHESNTINDBYOLNGSSTHISREDALLVESOGIOSTSOVLPLORRISHCAFFADTRSAWBURNORGITIPSAJEWEMISTERNATHRBLYAURIPFY` |  |
| 6 | cribs | 0/24 |  | `QYNJUDGENKAYBAYBODEDWHONHEFERWKCIZYAWOFUSEWIESTILLUSKEAGOLIONHESFORATITREHINDSTHANSRICNOCIPPESSYJ` |  |
| 7 | cribs | 2/24 |  | `YKYALITSSHIEFBIMTOCKABUCHNAMPSTHASSEDTRIFYSOTENFEDLCARTOPRIONPUALICOLLCOMBATAMABEZACSEMERBNILLMSO` |  |
| 8 | cribs | 2/24 |  | `FRMTODBEEMARHADSHYCRAZELINBNUSSUNTENEOFAPMTOIBEHINENTWHINNITESULWEGLEDAYNSASBOURNAPORSOFGCTATUMWV` |  |
| 9 | cribs | 3/24 |  | `BTISAGYPINVARREDSDODESPSPELOTHICERESFACAFIEROFANESREIVALSTELASRUDIVAREPSLECOURPOREACBONISTNUSEWHO` |  |
| 10 | cribs | 3/24 |  | `TIONTINTSDOUNTAWOSTYBEINOBELULDCUTAFLARECOUTCLINOGAROSTJOHOSPENIFRJAYINEYAMEYEEWARHMSEHOFTHATARSP` |  |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "item": "F13.4c lengths 6-19 (D3)",
 "search_reads_known_letters": false,
 "forms": [
  "beaufort",
  "added"
 ],
 "search": "0236's climb, unchanged (imported): 0140's parallel tempering with no known letter, 3 runs x 16 replicas x 625 rounds x 1000 moves; MIX8m rescoring",
 "k4_copies": 100,
 "cells": 28,
 "plant_power": {
  "6": [
   3,
   8
  ],
  "7": [
   5,
   8
  ],
  "8": [
   4,
   8
  ],
  "10": [
   4,
   8
  ],
  "13": [
   5,
   8
  ],
  "16": [
   4,
   8
  ],
  "19": [
   2,
   8
  ]
 },
 "plant_letters_right": {
  "6": [
   9,
   7,
   11,
   12,
   26,
   34,
   2,
   17
  ],
  "7": [
   9,
   7,
   7,
   2,
   6,
   2,
   24,
   10
  ],
  "8": [
   18,
   4,
   25,
   9,
   11,
   13,
   3,
   21
  ],
  "10": [
   12,
   8,
   22,
   23,
   13,
   6,
   10,
   10
  ],
  "13": [
   7,
   6,
   16,
   10,
   13,
   2,
   12,
   4
  ],
  "16": [
   10,
   6,
   11,
   6,
   5,
   2,
   5,
   10
  ],
  "19": [
   8,
   12,
   10,
   7,
   7,
   1,
   5,
   5
  ]
 },
 "k4_z_by_cell": {
  "6/beaufort": -1.573,
  "6/added": -0.952,
  "7/beaufort": -0.009,
  "7/added": -0.915,
  "8/beaufort": -2.01,
  "8/added": -0.66,
  "9/beaufort": 0.697,
  "9/added": -2.769,
  "10/beaufort": -0.565,
  "10/added": 0.913,
  "11/beaufort": 1.469,
  "11/added": -1.215,
  "12/beaufort": -1.398,
  "12/added": 0.615,
  "13/beaufort": -1.176,
  "13/added": 0.171,
  "14/beaufort": 1.447,
  "14/added": 1.377,
  "15/beaufort": 0.39,
  "15/added": -0.724,
  "16/beaufort": 0.104,
  "16/added": 0.104,
  "17/beaufort": -0.413,
  "17/added": -1.743,
  "18/beaufort": -2.717,
  "18/added": 0.104,
  "19/beaufort": 0.383,
  "19/added": -0.493
 },
 "k4_copies_at_or_above_by_cell": {
  "6/beaufort": 93,
  "6/added": 81,
  "7/beaufort": 49,
  "7/added": 81,
  "8/beaufort": 96,
  "8/added": 73,
  "9/beaufort": 24,
  "9/added": 100,
  "10/beaufort": 69,
  "10/added": 17,
  "11/beaufort": 11,
  "11/added": 90,
  "12/beaufort": 93,
  "12/added": 28,
  "13/beaufort": 89,
  "13/added": 42,
  "14/beaufort": 9,
  "14/added": 10,
  "15/beaufort": 33,
  "15/added": 74,
  "16/beaufort": 48,
  "16/added": 43,
  "17/beaufort": 66,
  "17/added": 94,
  "18/beaufort": 99,
  "18/added": 42,
  "19/beaufort": 39,
  "19/added": 67
 },
 "k4_cells_above_all_copies": 0,
 "k4_statistic": 1.469,
 "k4_best_cell": "11/beaufort",
 "k4_p": 0.8416,
 "k4_known_letters_in_place_by_cell": {
  "6/beaufort": 0,
  "6/added": 2,
  "7/beaufort": 1,
  "7/added": 1,
  "8/beaufort": 0,
  "8/added": 0,
  "9/beaufort": 2,
  "9/added": 2,
  "10/beaufort": 3,
  "10/added": 3,
  "11/beaufort": 3,
  "11/added": 3,
  "12/beaufort": 3,
  "12/added": 1,
  "13/beaufort": 3,
  "13/added": 1,
  "14/beaufort": 0,
  "14/added": 2,
  "15/beaufort": 1,
  "15/added": 2,
  "16/beaufort": 1,
  "16/added": 1,
  "17/beaufort": 3,
  "17/added": 3,
  "18/beaufort": 3,
  "18/added": 1,
  "19/beaufort": 1,
  "19/added": 1
 },
 "climbs": 3220,
 "exhaustive": false,
 "compute_seconds": 8485,
 "modal_cost_estimate": "3220 climbs x about 10 s (0236) = about 9 core-hours, about $0.6 of Modal credit"
}
```

Notes: F13.4c 6-19: K4 statistic 1.47 at 11/beaufort, p 0.842 against 100 shuffles; cells with K4 above all 0 of 28; plant power L6 3/8, L7 5/8, L8 4/8, L10 4/8, L13 5/8, L16 4/8, L19 2/8


