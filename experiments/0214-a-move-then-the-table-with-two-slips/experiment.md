# 0214-a-move-then-the-table-with-two-slips: A1.5: a move, then the table (and the reverse), over every dictionary-keyed columnar, Myszkowski, double columnar, rail fence, AMSCO and type-1 route, with a repeating key of length 1-26 on the sculpture's tables and up to two of the 24 known letters carved wrong; exact, judged against scrambled copies, with planted slipped messages

**Family:** 6-transposition-then-tableau  
**Parent:** 0110-keyword-columnar-from-the-whole-dictionary  
**Decision:** reverted  
**Run:** 2026-10-20T14:37:52+00:00, 438.4 s, status ran  
**Time by phase:** unattributed 3523 s, run 438 s, record 55 s

## In plain words

Sanborn described writing the message into a grid, reading it out in another order, and then using the table with a key word. Experiments 110-114 tried every such grid keyed by any dictionary word, before and after the table, and found nothing with all 24 known letters right. If he slipped at two of those places, that test would have missed it. Here we allow two wrong, on the carving and on scrambled copies, and hide three messages of our own made that way, slips included, to check the search finds them.

## Walkthrough, by hand

1. Write the message into a grid under a key word and read the columns out in the word's order.
2. Choose a key length, say 11, and a table; each known letter now sits at a new carved place, and its key letter is read off the table from the carved letter.
3. Known letters in the same slot of the key must give the same key letter.
4. Count how many would have to be slips; keep the setting if 2 or fewer.
5. Read the message back through the key and the grid, and do the same on scrambled copies of the carving.

## Worked example (generated)

```
keyword columnar PYRAMID (move first), then the KRYPTOS table, key length 11: key letter forced at each known place

  slot  0: 26N@45:S
  slot  1: 33S@46:U  66R@79:Y  70C@24:S
  slot  2: 73C@80:P
  slot  3: 22E@59:M  25T@4:X  69N@37:E
  slot  4: 29T@60:L  32A@5:O  65E@93:A
  slot  5: 72O@94:V
  slot  6: 24S@73:X  28R@18:L  68I@51:P
  slot  7: 31E@74:P
  slot  8: 27O@31:I
  slot  9: 23A@87:T  34T@32:W  64B@65:U  67L@10:X
  slot 10: 30H@88:H  71L@66:M  74K@11:V

slips needed: 13 (2 allowed)
```

## Lineage

Inherits from 0110-keyword-columnar-from-the-whole-dictionary. What changed: A1.5 (Stage 2, step 2, issue #76). 0110-0114 and the type-1 library (0080-0129) required all 24 known letters to agree with one repeating key after or before the move (nothing below key length 21-22). k = 1 was run as 'one carved letter wrong' (0093); slipped columns are F6.21. Here k = 2: the union of 0110's keyword columnar, 0111's Myszkowski, 0112's double columnar, 0113's rail fence and redefence, 0114's AMSCO (all from the whole dictionary) and 0129's type-1 library, deduplicated by where the known letters land, both orders, 8 table classes, key lengths 1-26, compiled with an exact early exit; K4 against 20 scrambled copies; readings that keep 3 or more checks to quadgrams and the blind judge; three planted messages with two slips each.

## Hypothesis (domain expert)

C1(a) (Sanborn, CNN 2005: 'I used a matrix code... double matrixes and triple matrixes... then went back to this table'), C11 ('the other 91 characters and their proper order'), A1 (knowledge/12-assumptions.md), C27(a). Model: a transposition w (message place i to carved place w(i)) and a periodic key k of length L on the table, plain and cipher alphabets standard or KRYPTOS, added or Beaufort form (8 classes; the key alphabet drops out). Order A, move then table: the key runs along the carved places, slot w(q) mod L; order B, table then move: slot q mod L, carved letter at w(q). Each known letter forces a key value in its slot; the least number of slips is 24 minus the sum over slots of the most common forced value's count, at most 2 here (17.5 bits to name). Cost estimated before the run: about 1.8 million route maps x 2 orders x 8 classes x 26 lengths per text, compiled. Statistic: per order and length, the number of (route, class) cells with 0, 1, 2 slips, K4 against each copy; the shortest length that fits; the judge's best on readings keeping 3 or more checks.

## Prediction

With two slips the shortest key length that fits K4 drops from 21-22 to about 17-19, as on the copies; K4 above every copy in no more (order, length) cells than a copy is above the rest; nothing judged above every copy. The three plants are found. Zero candidates pass gate 4.

## Method

1. Build every route map of 0110-0114 and the type-1 library; keep one per distinct landing of the 24 known places.
2. Compiled: for each route, class, order and key length, add the known places one by one into their slots and count slips (a place whose forced value is not its slot's most common so far); stop at
3. 3. Count cells by slips, K4 and 20 copies.
4. For cells keeping 3 or more checks, enumerate the key choices and read; each text's top 5 by quadgrams and every reading at or above -5.0 go to the judge in one call.
5. Plants and their own copies through the same search.

## Result

Candidates returned: 10. Passed all gates: 0. Best crib hits among all candidates: 24/24
(EAST 4/4, NORTHEAST 9/9, BERLIN 6/6, CLOCK 5/5).
Best loss: 15.501600731134841 (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | baseline | 24/24 | -15.132 | `UDYWHEKOVYGWAKEKRAXHSEASTNORTHEASTEVHWOODNSOMAMALKEYKWHENPUXQKQBERLINCLOCKZOOZHTIKLPUBVIEQTUATMIQ` | 0112 double columnar: TOSHNAIL inverse, order B, key length 24, kry/kry/beau, slips [74, 22]; open slots filled with A |
| 2 | baseline | 24/24 | -15.266 | `TXAWUAEZPUGAJTKPUUTREEASTNORTHEASTYIQAMIRSPZVBRFWITHSITSCDQKEZIBERLINCLOCKMWNSLOKIRHLYCOHALSHKENZ` | 0112 double columnar: AVICULTURE, order B, key length 24, std/std/beau, slips [22, 23]; open slots filled with A |
| 3 | baseline | 24/24 | -15.049 | `HRGASSTPDNAEAEWADYMOVEASTNORTHEASTBRBDIUAREDHEBAZKGCARSIUTOHEDXBERLINCLOCKAFIFROVRXBPEHAVKSBLZDZR` | 0112 double columnar: IDIOPATHICAL inverse, order B, key length 24, std/kry/vig, slips [22, 72]; open slots filled with A |
| 4 | baseline | 24/24 | -15.767 | `YUCZOFOTSFGWPJPERLCISEASTNORTHEASTIGATCREPUAEFQSVCSEAGKNUZLDYKOBERLINCLOCKKOFDIJRSFJSDSCQTXMHWNYA` | 0114 AMSCO: OVERIMITATION first 1, order A, key length 25, kry/kry/vig, slips [68, 67]; open slots filled with A |
| 5 | baseline | 24/24 | -15.212 | `DBQIPWPFOROCENOUTDSSSEASTNORTHEASTCXIESKAOPCHMYSKESPCCOEXYDYEOBBERLINCLOCKYDKFFVBSBUESABCYEHTWJDK` | 0113 rail fence: 19 rails offset 9 order (18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0), order A, key length 25, kry/kry/beau, slips [72, 66]; open slots filled with A |
| 6 | baseline | 24/24 | -15.237 | `UVYWHEKOVYGWAKEKRAXHSEASTNORTHEASTEVHWOODNSOMAMALFEYKWHENPUXQKQBERLINCLOCKZOOZHTIKLPUBVIEQTUATMIQ` | 0112 double columnar: TOSHNAIL inverse, order B, key length 24, kry/kry/beau, slips [26, 22]; open slots filled with A |
| 7 | baseline | 24/24 | -15.551 | `MXHUCVUNYNFITQURESTSPEASTNORTHEASTIHMBWILNGVBJIRGGFDAUGEFUFMPIDBERLINCLOCKHOAPMALXCTWENXFBIVXZIIA` | 0114 AMSCO: UNMETHODIZED first 1, order A, key length 24, std/kry/vig, slips [28, 72]; open slots filled with A |
| 8 | baseline | 24/24 | -15.930 | `JGBAARMEWAUQKDNKKALLZEASTNORTHEASTZQBWOSCTGARSPDUOPTUASBMCVDOQSBERLINCLOCKPMOMUFGDZKGHWOPRPLBHAWS` | 0111 Myszkowski: SATURABILITY, order B, key length 24, kry/std/vig, slips [70, 72]; open slots filled with A |
| 9 | baseline | 24/24 | -15.777 | `HQMJMUHERSSGUNKSVSZJXEASTNORTHEASTWPMIUDIOBVWQUXMLWEANDTJITYDYMBERLINCLOCKLRJUUWINPFAWHBEWFYNBMOH` | 0112 double columnar: SELFHOOD, order A, key length 25, std/std/beau, slips [29, 67]; open slots filled with A |
| 10 | baseline | 24/24 | -15.772 | `ZUCZOFOTSFGWKJPERLCISEASTNORTHEASTIGATCREPUAEFQSVCSEAGKNUZLDYKOBERLINCLOCKKOFDIJRSFJSDSCQTXMHWNYA` | 0114 AMSCO: OVERIMITATION first 1, order A, key length 25, kry/kry/vig, slips [31, 67]; open slots filled with A |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "a move then the table and the reverse, 0110-0114 and the type-1 library, periodic key 1-26 on 8 table classes, 0-2 known letters slipped (A1.5)",
 "route_maps_by_family": {
  "0110 keyword columnar": 459268,
  "0112 double columnar": 459268,
  "0111 Myszkowski": 343990,
  "0113 rail fence": 25568,
  "0114 AMSCO": 891360,
  "type-1 library": 27852
 },
 "distinct_landings": 1847590,
 "orders": "A move then table, B table then move",
 "classes": 8,
 "key_lengths": "1-26",
 "slips": "0-2 at the known places",
 "by_order_and_length": {
  "A1": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "A2": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "A3": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "A4": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "A5": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "A6": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "A7": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "A8": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "A9": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "A10": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "A11": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "A12": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "A13": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "A14": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "A15": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "A16": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    1
   ]
  },
  "A17": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    3
   ]
  },
  "A18": {
   "k4": [
    0,
    0,
    17
   ],
   "copies_min": [
    0,
    0,
    6
   ],
   "copies_max": [
    0,
    2,
    26
   ]
  },
  "A19": {
   "k4": [
    0,
    1,
    109
   ],
   "copies_min": [
    0,
    0,
    108
   ],
   "copies_max": [
    0,
    6,
    164
   ]
  },
  "A20": {
   "k4": [
    0,
    39,
    1424
   ],
   "copies_min": [
    0,
    18,
    1124
   ],
   "copies_max": [
    2,
    56,
    1770
   ]
  },
  "A21": {
   "k4": [
    2,
    262,
    6865
   ],
   "copies_min": [
    0,
    191,
    6051
   ],
   "copies_max": [
    8,
    278,
    6831
   ]
  },
  "A22": {
   "k4": [
    41,
    1595,
    23973
   ],
   "copies_min": [
    8,
    1244,
    23380
   ],
   "copies_max": [
    53,
    1624,
    25417
   ]
  },
  "A23": {
   "k4": [
    226,
    7183,
    56501
   ],
   "copies_min": [
    160,
    6767,
    54885
   ],
   "copies_max": [
    233,
    7405,
    57413
   ]
  },
  "A24": {
   "k4": [
    3504,
    36743,
    124444
   ],
   "copies_min": [
    3124,
    36277,
    121775
   ],
   "copies_max": [
    3545,
    37648,
    124623
   ]
  },
  "A25": {
   "k4": [
    3650,
    31062,
    134534
   ],
   "copies_min": [
    3702,
    30545,
    131997
   ],
   "copies_max": [
    3919,
    31601,
    135204
   ]
  },
  "A26": {
   "k4": [
    12986,
    59296,
    202644
   ],
   "copies_min": [
    12428,
    58347,
    200157
   ],
   "copies_max": [
    13657,
    60762,
    205126
   ]
  },
  "B1": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "B2": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "B3": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "B4": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "B5": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "B6": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "B7": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "B8": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "B9": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "B10": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "B11": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "B12": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "B13": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "B14": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "B15": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "B16": {
   "k4": [
    0,
    0,
    1
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    1,
    4
   ]
  },
  "B17": {
   "k4": [
    0,
    0,
    24
   ],
   "copies_min": [
    0,
    0,
    14
   ],
   "copies_max": [
    0,
    2,
    46
   ]
  },
  "B18": {
   "k4": [
    0,
    1,
    14
   ],
   "copies_min": [
    0,
    0,
    10
   ],
   "copies_max": [
    0,
    2,
    36
   ]
  },
  "B19": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "B20": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "B21": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ]
  },
  "B22": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    2
   ]
  },
  "B23": {
   "k4": [
    0,
    0,
    27
   ],
   "copies_min": [
    0,
    0,
    11
   ],
   "copies_max": [
    0,
    2,
    66
   ]
  },
  "B24": {
   "k4": [
    0,
    236,
    7336
   ],
   "copies_min": [
    0,
    114,
    6883
   ],
   "copies_max": [
    4,
    334,
    9157
   ]
  },
  "B25": {
   "k4": [
    795,
    60178,
    1584744
   ],
   "copies_min": [
    633,
    59019,
    1506650
   ],
   "copies_max": [
    1055,
    67911,
    1624606
   ]
  },
  "B26": {
   "k4": [
    568249,
    14212471,
    0
   ],
   "copies_min": [
    551040,
    14185953,
    0
   ],
   "copies_max": [
    594767,
    14229680,
    0
   ]
  }
 },
 "k4_above_every_copy": [
  "A21"
 ],
 "copies_above_rest": [
  2,
  1,
  1,
  0,
  0,
  0,
  0,
  1,
  0,
  0,
  1,
  1,
  0,
  1,
  1,
  1,
  0,
  3,
  1,
  1
 ],
 "shortest_length_by_slips": {
  "K4": {
   "A": [
    21,
    19,
    18
   ],
   "B": [
    25,
    18,
    16
   ]
  },
  "copy1": {
   "A": [
    22,
    20,
    18
   ],
   "B": [
    25,
    24,
    16
   ]
  },
  "copy2": {
   "A": [
    20,
    20,
    17
   ],
   "B": [
    24,
    24,
    16
   ]
  },
  "copy3": {
   "A": [
    21,
    19,
    17
   ],
   "B": [
    24,
    17,
    17
   ]
  },
  "copy4": {
   "A": [
    20,
    19,
    18
   ],
   "B": [
    24,
    16,
    16
   ]
  },
  "copy5": {
   "A": [
    21,
    18,
    17
   ],
   "B": [
    24,
    24,
    16
   ]
  },
  "copy6": {
   "A": [
    21,
    19,
    16
   ],
   "B": [
    25,
    24,
    16
   ]
  },
  "copy7": {
   "A": [
    20,
    18,
    17
   ],
   "B": [
    25,
    24,
    16
   ]
  },
  "copy8": {
   "A": [
    20,
    19,
    17
   ],
   "B": [
    24,
    24,
    16
   ]
  },
  "copy9": {
   "A": [
    21,
    19,
    16
   ],
   "B": [
    24,
    24,
    17
   ]
  },
  "copy10": {
   "A": [
    21,
    18,
    18
   ],
   "B": [
    24,
    17,
    16
   ]
  },
  "copy11": {
   "A": [
    20,
    19,
    17
   ],
   "B": [
    25,
    24,
    16
   ]
  },
  "copy12": {
   "A": [
    21,
    19,
    16
   ],
   "B": [
    25,
    18,
    16
   ]
  },
  "copy13": {
   "A": [
    21,
    19,
    17
   ],
   "B": [
    24,
    18,
    16
   ]
  },
  "copy14": {
   "A": [
    20,
    19,
    17
   ],
   "B": [
    24,
    24,
    17
   ]
  },
  "copy15": {
   "A": [
    21,
    18,
    17
   ],
   "B": [
    24,
    24,
    16
   ]
  },
  "copy16": {
   "A": [
    21,
    19,
    18
   ],
   "B": [
    24,
    17,
    17
   ]
  },
  "copy17": {
   "A": [
    21,
    19,
    17
   ],
   "B": [
    24,
    23,
    16
   ]
  },
  "copy18": {
   "A": [
    21,
    18,
    17
   ],
   "B": [
    24,
    17,
    16
   ]
  },
  "copy19": {
   "A": [
    20,
    19,
    17
   ],
   "B": [
    24,
    17,
    17
   ]
  },
  "copy20": {
   "A": [
    22,
    19,
    18
   ],
   "B": [
    25,
    16,
    16
   ]
  }
 },
 "readings": {
  "k4": 53150,
  "copies": [
   53360,
   52732,
   54262,
   53213,
   58628,
   52820,
   54812,
   55804,
   54019,
   53037,
   56613,
   53311,
   52833,
   56645,
   53082,
   58540,
   55096,
   60290,
   51863,
   53933
  ]
 },
 "capped": [],
 "judge": {
  "sent": 195,
  "none": 0,
  "cut": -5.0,
  "rule": "each text's top 5 readings by quadgrams and every reading at or above -5.0; one call"
 },
 "k4_judge_best": 6,
 "copies_judge_best": [
  4,
  4,
  12,
  8,
  5,
  4,
  6,
  6,
  8,
  5,
  12,
  4,
  8,
  4,
  8,
  4,
  4,
  8,
  4,
  6
 ],
 "k4_readings_above_every_copy": 0,
 "k4_top": [
  {
   "reading": "UDYWHEKOVY?????KRAXHSDASTNORTHEAST?????ODNSOMAMALKEYKWHENP?????BERLINCLOCHZOOZHTIK?????IEQTUATMIQ",
   "judge": 6,
   "quad": -6.614,
   "route": "0112 double columnar: TOSHNAIL inverse",
   "order": "B",
   "L": 24,
   "class": "kry/kry/beau"
  },
  {
   "reading": "TXAWUAEZPU?????PUUTREYKSTNORTHEAST?????IRSPZVBRFWITHSITSCD?????BERLINCLOCKMWNSLOKI?????OHALSHKENZ",
   "judge": 5,
   "quad": -6.755,
   "route": "0112 double columnar: AVICULTURE",
   "order": "B",
   "L": 24,
   "class": "std/std/beau"
  },
  {
   "reading": "HRGASSTPDN?????ADYMOVLASTNORTHEAST?????UAREDHEBAZKGCARSIUT?????BERLINCLLCKAFIFROVR?????AVKSBLZDZR",
   "judge": 4,
   "quad": -6.586,
   "route": "0112 double columnar: IDIOPATHICAL inverse",
   "order": "B",
   "L": 24,
   "class": "std/kry/vig"
  },
  {
   "reading": "?B?IPWP?OR?CENO?TDSSSEASTNORTHEASTCXIESK?OP?H??SKES?CC???YD???BBEGLINCLECKYD?FFVBSB?E?ABCY??TW???",
   "judge": 3,
   "quad": -6.759,
   "route": "0113 rail fence: 19 rails offset 9 order (18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0)",
   "order": "A",
   "L": 25,
   "class": "kry/kry/beau"
  },
  {
   "reading": "Y?CZOF??S?G?P?PERLCISEASTNORTHEASTIGATCREP?AEF???CSEA???U?LDYKOBERMMNCLOCKKOFD?J???JSDSCQT?M?W???",
   "judge": 3,
   "quad": -6.705,
   "route": "0114 AMSCO: OVERIMITATION first 1",
   "order": "A",
   "L": 25,
   "class": "kry/kry/vig"
  }
 ],
 "plants": [
  {
   "seed": 2141,
   "route": "0110 keyword columnar: ODONTASPIDAE",
   "L": 11,
   "cls": "kry/kry/vig",
   "order": "A",
   "slips": [
    23,
    25
   ],
   "planted_setting_found": true,
   "slips_named": [
    25,
    23
   ],
   "quad": -4.787,
   "judge": 70,
   "own_copies_judge_best": [
    6,
    4,
    4,
    6,
    8
   ],
   "found": true
  },
  {
   "seed": 2142,
   "route": "0114 AMSCO: UNEXTINGUISHED first 2 inverse",
   "L": 9,
   "cls": "std/kry/beau",
   "order": "B",
   "slips": [
    31,
    64
   ],
   "planted_setting_found": true,
   "slips_named": [
    64,
    31
   ],
   "quad": -4.206,
   "judge": 90,
   "own_copies_judge_best": [
    4,
    8,
    6,
    6,
    6
   ],
   "found": true
  },
  {
   "seed": 2143,
   "route": "0113 rail fence: 31 rails offset 25 order (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30)",
   "L": 13,
   "cls": "kry/std/vig",
   "order": "A",
   "slips": [
    33,
    74
   ],
   "planted_setting_found": true,
   "slips_named": [
    74,
    33
   ],
   "quad": -4.306,
   "judge": 92,
   "own_copies_judge_best": [
    3,
    6,
    8,
    4,
    8
   ],
   "found": true
  }
 ],
 "slip_cost_bits": {
  "2": 17.5
 },
 "controls": "20 shuffled copies (seeds 2150-2169); each plant against 5 shuffles of its own ciphertext",
 "exhaustive": "yes"
}
```

Notes: 1,847,590 distinct landings; K4 shortest length with <= 2 slips A 18, B 16; K4 above every copy in 1 cells (copies 0-3); judge sent 195, K4 best 6, copies best 12; plants found [True, True, True]


