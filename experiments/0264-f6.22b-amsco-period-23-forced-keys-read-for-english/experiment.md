# 0264-f6.22b-amsco-period-23-forced-keys-read-for-english: F6.22b: the keys K4's AMSCO settings force at period 23, read for English (quadgrams), against the best forced key of each of 200 shuffles; 20 planted running-key messages for power

**Family:** 6-move-then-table  
**Parent:** 0263-f6-amsco-period-23-excess-against-200-shuffles-and-named-keys  
**Decision:** reverted  
**Run:** 2026-10-30T11:27:05+00:00, 64.2 s, status ran  
**Time by phase:** test 0 s, run 64 s, record 0 s

## In plain words

K4 fits a two-step cipher (a grid shuffle, then the table with a 23-letter key) in more ways than most scrambled copies do. For each way it fits, the known letters spell out almost the whole 23-letter key. If Sanborn took his key from a book or a sentence, that key should read like English; here we check whether K4's keys read more like English than the keys scrambled copies are forced to.

## Walkthrough, by hand

1. Take one of K4's agreeing settings: an AMSCO grid keyed by a word, then the table with a 23-letter key.
2. Undo the grid for the 24 known places: each lands on a carved place, whose number mod 23 is its key slot.
3. The key letter at that slot is the carved letter minus the known letter on the table (plus, for Beaufort).
4. Write the 23 slots in order, '?' where nothing lands, and score the runs of four letters for English.
5. Do the same for every agreeing setting of each scrambled copy, and compare the best scores.

## Worked example (generated)

```
F6.22b: the keys K4's AMSCO settings force at period 23, read for English.

  AMSCO keyed by a word, then the table with a 23-letter key: each known letter lands on a carved place p,
  and forces the key letter at slot p mod 23 (carved minus known on the table, or their sum for Beaufort).
  Written in slot order with '?' where nothing lands, a key taken from English text reads as English in runs of four.

  per text: the best such key over its agreeing settings; K4's against 200 shuffles'; 20 planted English keys for power.
```

## Lineage

Inherits from 0263-f6-amsco-period-23-excess-against-200-shuffles-and-named-keys. What changed: F6.22b, the chase of 0263 (Alexis, 2026-10-28, #100: a result that beats its copies, even at the edge, gets a row). 0263 put K4's count of agreeing AMSCO settings at period 23 in the top 2.5% of 200 shuffles (21; 4 of 200 at or above) and found no forced key that is a passage of a named text. A count is a property of a text; what would single out a message is its key. Here every setting that agrees at 23, for K4, the same 200 shuffles (seed 2620) and 20 plants, has its forced key (up to 23 letters, numbered on the standard or KRYPTOS alphabet) scored for English by quadgrams, as a running key from any English text would score; K4's best against the shuffles' bests.

## Hypothesis (domain expert)

F6 (C1(a): a matrix code, then the table). AMSCO keyed by a dictionary word (0114's 891,360 routes, 3-15 columns), then a period-23 key on the sculpture's 8 table classes. With 24 known letters on 23 slots the key is almost fully forced in every agreeing setting, so a key drawn from any English text (C7(a), C5: a phrase as key; F1.3's test on this move) shows as English letters in slot order. Statistic: per text, the highest mean quadgram score over the 4-grams fully forced (slots 1-23, no wrap), over its agreeing settings and two numberings. Power: 20 plants (Carter messages, random route and class, a 23-letter window of English as key).

## Prediction

K4's best forced key inside the 200 shuffles' bests (p above 0.05), its letters no English; most planted keys above every shuffle (power at least 15 of 20). Zero candidates.

## Method

1. 0263's exact count at period 23, unchanged, for K4, its 200 shuffles (seed 2620) and 20 plants, every agreeing setting kept with its forced shifts per slot.
2. Each forced key written as letters in slot order on the standard and on the KRYPTOS alphabet, '?' where no known letter reaches; scored by the mean log quadgram over the 4-grams with all four letters forced (at least 8).
3. Per text the best score over its settings and numberings; K4's rank among the 200 shuffles'; a plant is found when its best is above every shuffle's.
4. K4's forced keys listed in full.

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
 "item": "F6.22b (chase of 0263's AMSCO period-23 count)",
 "routes": 891360,
 "classes": 8,
 "period": 23,
 "order": "A (move, then the table)",
 "agreeing_settings": {
  "k4": 21,
  "copies_min_median_max": [
   1,
   8.0,
   31
  ]
 },
 "statistic": "per text: best mean log10 quadgram of a forced key (slots 1-23 in order, no wrap, standard or KRYPTOS numbering, at least 8 fully forced 4-grams) over its agreeing settings",
 "k4_best": -6.525,
 "k4_best_key": "SEV?HHEMTPMPXRMGRONEXHI",
 "copies_best_min_median_max": [
  -9.206,
  -7.094,
  -5.237
 ],
 "copies_at_or_above": 24,
 "p": 0.1244,
 "k4_forced_keys": [
  {
   "route": [
    "THIOPHOSPHATE",
    13,
    1,
    "inverse"
   ],
   "class": "kry/kry/True",
   "numbering": "std",
   "key": "SEV?HHEMTPMPXRMGRONEXHI",
   "score": -6.525
  },
  {
   "route": [
    "BLACKBIRDING",
    12,
    2,
    "inverse"
   ],
   "class": "std/std/True",
   "numbering": "kry",
   "key": "BSQNNRRODDEFPFIONECKOBZ",
   "score": -6.615
  },
  {
   "route": [
    "ADULTEROUSLY",
    12,
    2,
    "inverse"
   ],
   "class": "std/std/False",
   "numbering": "kry",
   "key": "KDDAIRNWDHCKITEOCCWDOKW",
   "score": -6.886
  },
  {
   "route": [
    "SNECKDRAWN",
    10,
    2,
    "inverse"
   ],
   "class": "kry/std/False",
   "numbering": "std",
   "key": "GESNGVEHUOLIOXCJNAQQF?A",
   "score": -7.46
  },
  {
   "route": [
    "TENORISTER",
    10,
    2,
    "inverse"
   ],
   "class": "kry/std/False",
   "numbering": "std",
   "key": "GESNGVEHUOLIOXCJNAQQF?A",
   "score": -7.46
  },
  {
   "route": [
    "UNIMAGINATIVENESS",
    10,
    2,
    "inverse"
   ],
   "class": "kry/std/False",
   "numbering": "std",
   "key": "GESNGVEHUOLIOXCJNAQQF?A",
   "score": -7.46
  },
  {
   "route": [
    "UNMINISTER",
    10,
    2,
    "inverse"
   ],
   "class": "kry/std/False",
   "numbering": "std",
   "key": "GESNGVEHUOLIOXCJNAQQF?A",
   "score": -7.46
  },
  {
   "route": [
    "INSPIRABILITY",
    13,
    2,
    "inverse"
   ],
   "class": "kry/std/False",
   "numbering": "std",
   "key": "YUIXGARKNOQ?UMOUVMHLMTF",
   "score": -7.492
  },
  {
   "route": [
    "THIOPHOSPHATE",
    13,
    1,
    "inverse"
   ],
   "class": "kry/kry/True",
   "numbering": "kry",
   "key": "MTU?AATFNIFIWLFSLHGTWAB",
   "score": -7.551
  },
  {
   "route": [
    "NATIONALNESS",
    12,
    2,
    "inverse"
   ],
   "class": "std/kry/False",
   "numbering": "std",
   "key": "NLJPZMUOWOKYEIRHMIDYTAE",
   "score": -7.614
  },
  {
   "route": [
    "TEMPERABILITY",
    13,
    1,
    "inverse"
   ],
   "class": "std/kry/False",
   "numbering": "kry",
   "key": "HERARWSWKHQTTMZBPIEDQDF",
   "score": -7.759
  },
  {
   "route": [
    "TRANSPROCESS",
    12,
    2,
    "inverse"
   ],
   "class": "std/kry/False",
   "numbering": "std",
   "key": "NLJPZMUOWOKYEIRH?IDYTAE",
   "score": -7.797
  },
  {
   "route": [
    "MATCHLESS",
    9,
    1,
    "inverse"
   ],
   "class": "std/kry/True",
   "numbering": "kry",
   "key": "HCGXWTLHKSSZLESOLKTG?ZD",
   "score": -7.912
  },
  {
   "route": [
    "MATCHLESSLY",
    9,
    1,
    "inverse"
   ],
   "class": "std/kry/True",
   "numbering": "kry",
   "key": "HCGXWTLHKSSZLESOLKTG?ZD",
   "score": -7.912
  },
  {
   "route": [
    "BLACKBIRDING",
    12,
    2,
    "inverse"
   ],
   "class": "std/std/True",
   "numbering": "std",
   "key": "IGUTTBBFKKLMDMPFTLJAFIZ",
   "score": -7.939
  },
  {
   "route": [
    "MATCHLESS",
    9,
    1,
    "inverse"
   ],
   "class": "std/kry/True",
   "numbering": "std",
   "key": "OJNYXEROAGGZRLGFRAEN?ZK",
   "score": -7.943
  },
  {
   "route": [
    "MATCHLESSLY",
    9,
    1,
    "inverse"
   ],
   "class": "std/kry/True",
   "numbering": "std",
   "key": "OJNYXEROAGGZRLGFRAEN?ZK",
   "score": -7.943
  },
  {
   "route": [
    "SNECKDRAWN",
    10,
    2,
    "inverse"
   ],
   "class": "kry/std/False",
   "numbering": "kry",
   "key": "STMGSUTAQHEBHWYCGKJJO?K",
   "score": -8.011
  },
  {
   "route": [
    "TENORISTER",
    10,
    2,
    "inverse"
   ],
   "class": "kry/std/False",
   "numbering": "kry",
   "key": "STMGSUTAQHEBHWYCGKJJO?K",
   "score": -8.011
  },
  {
   "route": [
    "UNIMAGINATIVENESS",
    10,
    2,
    "inverse"
   ],
   "class": "kry/std/False",
   "numbering": "kry",
   "key": "STMGSUTAQHEBHWYCGKJJO?K",
   "score": -8.011
  },
  {
   "route": [
    "UNMINISTER",
    10,
    2,
    "inverse"
   ],
   "class": "kry/std/False",
   "numbering": "kry",
   "key": "STMGSUTAQHEBHWYCGKJJO?K",
   "score": -8.011
  },
  {
   "route": [
    "MATCHLESS",
    9,
    1,
    "inverse"
   ],
   "class": "kry/kry/True",
   "numbering": "kry",
   "key": "QIQBBUYUAQFSXYGEXAEP?GU",
   "score": -8.179
  },
  {
   "route": [
    "MATCHLESSLY",
    9,
    1,
    "inverse"
   ],
   "class": "kry/kry/True",
   "numbering": "kry",
   "key": "QIQBBUYUAQFSXYGEXAEP?GU",
   "score": -8.179
  },
  {
   "route": [
    "MATCHLESS",
    9,
    1,
    "inverse"
   ],
   "class": "kry/kry/True",
   "numbering": "std",
   "key": "UPUIIVCVHUMGYCNLYHLD?NV",
   "score": -8.182
  },
  {
   "route": [
    "MATCHLESSLY",
    9,
    1,
    "inverse"
   ],
   "class": "kry/kry/True",
   "numbering": "std",
   "key": "UPUIIVCVHUMGYCNLYHLD?NV",
   "score": -8.182
  },
  {
   "route": [
    "TEMPERABILITY",
    13,
    1,
    "inverse"
   ],
   "class": "std/kry/False",
   "numbering": "std",
   "key": "OLBHBXGXAOUEESZIDPLKUKM",
   "score": -8.203
  },
  {
   "route": [
    "NATIONALNESS",
    12,
    2,
    "inverse"
   ],
   "class": "std/kry/True",
   "numbering": "std",
   "key": "PHJZDYCWEKMKQWVBOSLOTIE",
   "score": -8.376
  },
  {
   "route": [
    "ADULTEROUSLY",
    12,
    2,
    "inverse"
   ],
   "class": "std/std/False",
   "numbering": "std",
   "key": "AKKHPBTXKOJAPELFJJXKFAX",
   "score": -8.488
  },
  {
   "route": [
    "NATIONALNESS",
    12,
    2,
    "inverse"
   ],
   "class": "std/kry/True",
   "numbering": "kry",
   "key": "IACZPXYVTDFDJVURHMEHNBT",
   "score": -8.592
  },
  {
   "route": [
    "THIOPHOSPHATE",
    13,
    1,
    "inverse"
   ],
   "class": "kry/kry/False",
   "numbering": "kry",
   "key": "SQP?ZZVXAWKNNUXXCFLYUAM",
   "score": -8.709
  },
  {
   "route": [
    "INSPIRABILITY",
    13,
    2,
    "inverse"
   ],
   "class": "kry/std/False",
   "numbering": "kry",
   "key": "XQBWSKLDGHJ?QFHQUFAEFNO",
   "score": -8.736
  },
  {
   "route": [
    "TEMPERABILITY",
    13,
    1,
    "inverse"
   ],
   "class": "std/kry/True",
   "numbering": "std",
   "key": "KNNHFJQNAYCEMAVWXXTWYMO",
   "score": -8.737
  },
  {
   "route": [
    "PHENARSINE",
    10,
    1,
    "inverse"
   ],
   "class": "kry/std/True",
   "numbering": "kry",
   "key": "WIUSIWQIJV?EWRZYGFCKXBD",
   "score": -8.807
  },
  {
   "route": [
    "WINDOWWARD",
    10,
    1,
    "inverse"
   ],
   "class": "kry/std/True",
   "numbering": "kry",
   "key": "WIUSIWQIJV?EWRZYGFCKXBD",
   "score": -8.807
  },
  {
   "route": [
    "THIOPHOSPHATE",
    13,
    1,
    "inverse"
   ],
   "class": "kry/kry/False",
   "numbering": "std",
   "key": "GUD?ZZWYHXATTVYYJMRCVHS",
   "score": -8.855
  },
  {
   "route": [
    "JULYFLOWER",
    10,
    2,
    "inverse"
   ],
   "class": "kry/std/False",
   "numbering": "kry",
   "key": "JZLSGUOZTGH?HWQKZHUJOVS",
   "score": -8.873
  },
  {
   "route": [
    "NATIONALNESS",
    12,
    2,
    "inverse"
   ],
   "class": "std/kry/False",
   "numbering": "kry",
   "key": "GECIZFQHVHDXTBLAFBPXNKT",
   "score": -9.154
  },
  {
   "route": [
    "JULYFLOWER",
    10,
    2,
    "inverse"
   ],
   "class": "kry/std/False",
   "numbering": "std",
   "key": "QZRGNVFZENO?OXUAZOVQFWG",
   "score": -9.252
  },
  {
   "route": [
    "TRANSPROCESS",
    12,
    2,
    "inverse"
   ],
   "class": "std/kry/False",
   "numbering": "kry",
   "key": "GECIZFQHVHDXTBLA?BPXNKT",
   "score": -9.318
  },
  {
   "route": [
    "PHENARSINE",
    10,
    1,
    "inverse"
   ],
   "class": "kry/std/True",
   "numbering": "std",
   "key": "XPVGPXUPQW?LXBZCNMJAYIK",
   "score": -9.418
  },
  {
   "route": [
    "WINDOWWARD",
    10,
    1,
    "inverse"
   ],
   "class": "kry/std/True",
   "numbering": "std",
   "key": "XPVGPXUPQW?LXBZCNMJAYIK",
   "score": -9.418
  },
  {
   "route": [
    "TEMPERABILITY",
    13,
    1,
    "inverse"
   ],
   "class": "std/kry/True",
   "numbering": "kry",
   "key": "DGGAOCJGKXYTFKUVWWNVXFH",
   "score": -9.449
  }
 ],
 "plants": {
  "found": 6,
  "of": 20,
  "each": [
   {
    "route": [
     "VARIOLIZATION",
     13,
     1,
     "inverse"
    ],
    "class": "std/kry/beau",
    "key": "WARANDHOWDIFFICULTITWOU",
    "numbering": "std",
    "best": -7.189,
    "best_key": "GGDAQAULAUXSNTKLPEKFEEW",
    "found": false,
    "live": 8
   },
   {
    "route": [
     "UNSPONTANEOUSLY",
     15,
     1,
     "inverse"
    ],
    "class": "std/std/vig",
    "key": "ATURALLYONTHECONDITIONS",
    "numbering": "std",
    "best": -6.92,
    "best_key": "AX?FGYIHLYOMMTUEOPLTUOX",
    "found": false,
    "live": 3
   },
   {
    "route": [
     "PREVALESCENT",
     10,
     2,
     "inverse"
    ],
    "class": "std/kry/vig",
    "key": "LYDEDICATEDTOPLACIDREAD",
    "numbering": "std",
    "best": -4.824,
    "best_key": "LYDEDOLATEDTEJ??CIDHAD?",
    "found": true,
    "live": 36
   },
   {
    "route": [
     "NONZEALOUS",
     10,
     1,
     "inverse"
    ],
    "class": "kry/std/vig",
    "key": "YIMPRESSIVEORIGINALLYTH",
    "numbering": "kry",
    "best": -6.053,
    "best_key": "GRIDVOG?THMOUNKDGOEFAIL",
    "found": false,
    "live": 11
   },
   {
    "route": [
     "ESCHATOCOL",
     10,
     2,
     "forward"
    ],
    "class": "std/kry/beau",
    "key": "HEMSELVESUNDERSHELTERIN",
    "numbering": "kry",
    "best": -6.818,
    "best_key": "AIMNOVRA?KLDOCGRHRWAS?F",
    "found": false,
    "live": 10
   },
   {
    "route": [
     "OVERHEADINESS",
     10,
     2,
     "forward"
    ],
    "class": "std/kry/vig",
    "key": "PASSINGTHESTONESANDBASK",
    "numbering": "kry",
    "best": -3.574,
    "best_key": "?AS?ING?HESTONESAND??SK",
    "found": true,
    "live": 13
   },
   {
    "route": [
     "THERAPEUTIST",
     12,
     2,
     "forward"
    ],
    "class": "std/std/beau",
    "key": "EBUTALTHOUGHHEHADRESIGN",
    "numbering": "kry",
    "best": -7.385,
    "best_key": "ZDISPDBSS?LKBBTMUNYZLER",
    "found": false,
    "live": 11
   },
   {
    "route": [
     "PAMPRODACTYLOUS",
     15,
     1,
     "inverse"
    ],
    "class": "kry/kry/vig",
    "key": "SCOVEREDWITHTHINGOLDFOI",
    "numbering": "kry",
    "best": -8.108,
    "best_key": "ACXUSJJUOAYTSKG?HBHPLKH",
    "found": false,
    "live": 3
   },
   {
    "route": [
     "BLEMISHMENT",
     11,
     1,
     "inverse"
    ],
    "class": "kry/kry/beau",
    "key": "HEGOLDFOILFROMTHESMALLP",
    "numbering": "std",
    "best": -4.312,
    "best_key": "?EGOL?FOILFROMTHE??ALLP",
    "found": true,
    "live": 21
   },
   {
    "route": [
     "NONMAGNETIC",
     11,
     2,
     "forward"
    ],
    "class": "std/kry/beau",
    "key": "CAMEINTOTHEVILLAGEONEAF",
    "numbering": "kry",
    "best": -7.492,
    "best_key": "SAYJAQAVM?ETDGTJRDGICDU",
    "found": false,
    "live": 6
   },
   {
    "route": [
     "METEMPIRICALLY",
     10,
     2,
     "inverse"
    ],
    "class": "std/kry/vig",
    "key": "TTERTODEALWITHITWESHOUL",
    "numbering": "kry",
    "best": -7.409,
    "best_key": "BIZ?BFDSKUEWJUDAUXDSNSI",
    "found": false,
    "live": 8
   },
   {
    "route": [
     "MUNITIONER",
     10,
     1,
     "forward"
    ],
    "class": "std/kry/beau",
    "key": "TTEREDFROMTHESETRIALSAN",
    "numbering": "std",
    "best": -7.137,
    "best_key": "XAELDWEWWODJSOCHNDGXLUP",
    "found": false,
    "live": 5
   },
   {
    "route": [
     "SIPHONOGAMIC",
     10,
     2,
     "inverse"
    ],
    "class": "std/kry/vig",
    "key": "RKTOOVALUABLETOLEAVEAND",
    "numbering": "kry",
    "best": -6.887,
    "best_key": "E?POOVALZYX?ETO?SFVEAN?",
    "found": false,
    "live": 7
   },
   {
    "route": [
     "ANAPTOMORPHUS",
     13,
     2,
     "forward"
    ],
    "class": "kry/std/vig",
    "key": "ONEWITHINTHEOTHERBEFORE",
    "numbering": "std",
    "best": -3.427,
    "best_key": "ONEWITH?NTHEO??E?BEFOR?",
    "found": true,
    "live": 4
   },
   {
    "route": [
     "COLOMBIER",
     8,
     2,
     "inverse"
    ],
    "class": "std/kry/beau",
    "key": "GFROMTHEGOVERNMENTONCOM",
    "numbering": "kry",
    "best": -7.246,
    "best_key": "JLRBIICKYDOCVIVCOQNALD?",
    "found": false,
    "live": 19
   },
   {
    "route": [
     "VINOLENCE",
     9,
     2,
     "inverse"
    ],
    "class": "std/std/beau",
    "key": "MHEBANDAVAULTNOTAREALTO",
    "numbering": "std",
    "best": -5.147,
    "best_key": "MHEBA??AVAUL?NOTAREBLT?",
    "found": true,
    "live": 8
   },
   {
    "route": [
     "CYANCARBONIC",
     12,
     1,
     "inverse"
    ],
    "class": "std/std/vig",
    "key": "ANDBECAMEAPASSAGEFEETHI",
    "numbering": "kry",
    "best": -6.651,
    "best_key": "LDAEERWHYAMV?UXINOSVCCX",
    "found": false,
    "live": 13
   },
   {
    "route": [
     "MILLIVOLTMETER",
     8,
     2,
     "forward"
    ],
    "class": "std/std/beau",
    "key": "ESURFACEOFTHEROBEISCOVE",
    "numbering": "std",
    "best": -7.213,
    "best_key": "WODFRDERASZSHQOKNHDGETU",
    "found": false,
    "live": 9
   },
   {
    "route": [
     "NOCTAMBULATION",
     14,
     1,
     "forward"
    ],
    "class": "kry/std/vig",
    "key": "TOTHETOMBANDWHENTHREEHO",
    "numbering": "kry",
    "best": -4.064,
    "best_key": "?OTHETOMB??D??EN?HREEHO",
    "found": true,
    "live": 21
   },
   {
    "route": [
     "CALYCOZOON",
     10,
     1,
     "forward"
    ],
    "class": "kry/std/beau",
    "key": "TORATIONOFTHEBROKENANDM",
    "numbering": "std",
    "best": -6.734,
    "best_key": "FOPAIFANWLPSLAVBMAL?NSI",
    "found": false,
    "live": 9
   }
  ]
 },
 "copies": "200 fresh shuffles (seed 2620, as 0263)",
 "exhaustive": true,
 "compute_seconds": 45,
 "modal_cost_estimate": "as 0263 (65 s on 32 cores, $0.03) plus key scoring: about $0.05"
}
```

Notes: F6.22b: K4's best forced key at 23 scores -6.53 (SEV?HHEMTPMPXRMGRONEXHI); 200 shuffles' bests -9.21 to -5.24, 24 at or above K4 (p 0.124); plants found 6 of 20


