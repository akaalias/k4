# 0266-f6.22c-amsco-period-23-forced-keys-against-a-count-matched-null: F6.22c: K4's best forced period-23 AMSCO key against the best of 21 settings drawn from the shuffles' own (a count-matched null), and per setting

**Family:** 6-move-then-table  
**Parent:** 0265-f6.22b-amsco-period-23-forced-keys-by-english-likelihood-gaps-allowed  
**Decision:** reverted  
**Run:** 2026-10-30T11:34:14+00:00, 71.6 s, status ran  
**Time by phase:** test 0 s, run 72 s, record 0 s

## In plain words

K4's best 23-letter key reads less like English than random letters do, yet it beat most scrambled copies' best keys. K4 fits this cipher in 21 ways where a typical copy fits in 8, and the best of 21 tries is naturally higher than the best of 8. Here K4 is compared with the best of 21 keys drawn from the copies' own, so both get the same number of tries.

## Walkthrough, by hand

1. Take one of K4's agreeing settings: an AMSCO grid keyed by a word, then the table with a 23-letter key.
2. Undo the grid for the 24 known places: each lands on a carved place, whose number mod 23 is its key slot.
3. The key letter at that slot is the carved letter minus the known letter on the table (plus, for Beaufort).
4. Write the 23 slots in order, '?' where nothing lands, and score each run of letters for how much more likely it is as English than as random letters.
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

Inherits from 0265-f6.22b-amsco-period-23-forced-keys-by-english-likelihood-gaps-allowed. What changed: F6.22c, the chase of 0265 (Alexis, #100: a result that beats its copies at the edge gets a row). 0265: K4's best forced key -11.9 bits (below zero: less English than random letters), above 195 of the 200 shuffles' bests (p 0.03), every planted key +9 to +37. K4 has 21 agreeing settings where the median shuffle has 8, so its best is taken over more keys. Here the same scores per setting (unchanged), and K4's best of 21 against the best of 21 drawn from the pooled settings of the 200 shuffles (20,000 draws), K4's per-setting scores against the pool, and the shuffles with at least 21 settings.

## Hypothesis (domain expert)

F6 (C1(a): a matrix code, then the table). AMSCO keyed by a dictionary word (0114's 891,360 routes, 3-15 columns), then a period-23 key on the sculpture's 8 table classes. With 24 known letters on 23 slots the key is almost fully forced in every agreeing setting, so a key drawn from any English text (C7(a), C5: a phrase as key; F1.3's test on this move) shows as English letters in slot order. Statistic: per text, the highest English log-likelihood ratio of a forced key (bits against random letters, each forced letter conditioned on the forced letters before it in its run, slots 1-23 in order, no wrap), over its agreeing settings and two numberings. Power: 20 plants (Carter messages, random route and class, a 23-letter window of English as key).

## Prediction

Count-matched: K4's best of 21 inside the null (p above 0.05); K4's per-setting scores as the pool's (rank-sum p above 0.05). If K4 still beats the count-matched null, a row to look at its top keys by eye and by the judge. Zero candidates.

## Method

1. 0263's exact count at period 23, unchanged, for K4, its 200 shuffles (seed 2620) and 20 plants, every agreeing setting kept with its forced shifts per slot.
2. Each forced key written as letters in slot order on the standard and on the KRYPTOS alphabet, '?' where no known letter reaches; scored by its log-likelihood ratio, English against random letters, in bits: each forced letter's probability given the up to three forced letters before it in its run, from the quadgram table.
3. Per setting the better of its two numberings. K4's best of its 21 against the best of 21 drawn without replacement from the 200 shuffles' pooled settings (20,000 draws, seed 2661); K4's per-setting scores against the pool by rank sum; the shuffles with at least 21 settings, their bests. Plants as 0265.
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
 "statistic": "per text: best English log-likelihood ratio (bits, against random letters) of a forced key, slots 1-23 in order, no wrap, standard or KRYPTOS numbering, each forced letter conditioned on up to three forced letters before it in its run (quadgram table marginals), over its agreeing settings",
 "count_matched": {
  "k4_settings": 21,
  "pool_settings": 1723,
  "draws": 20000,
  "k4_best": -11.85,
  "null_best_of_n_5_50_95": [
   -36.0,
   -26.43,
   -11.11
  ],
  "p": 0.06
 },
 "per_setting": {
  "k4_mean": -54.53,
  "pool_mean": -52.5,
  "rank_sum_z": -1.0,
  "p_one_sided": 0.8401
 },
 "shuffles_with_at_least_k4s_count": [
  [
   31,
   -34.6
  ],
  [
   25,
   -23.05
  ],
  [
   23,
   -43.22
  ],
  [
   21,
   -36.4
  ]
 ],
 "k4_best": -11.85,
 "k4_best_key": "SEV?HHEMTPMPXRMGRONEXHI",
 "copies_best_min_median_max": [
  -63.85,
  -35.14,
  -6.76
 ],
 "copies_at_or_above": 5,
 "p": 0.0299,
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
   "score": -11.85
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
   "score": -33.14
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
   "score": -38.73
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
   "score": -43.73
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
   "score": -47.23
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
   "score": -47.23
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
   "score": -47.23
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
   "score": -47.23
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
   "score": -47.76
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
   "score": -48.07
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
   "score": -48.07
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
   "score": -48.07
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
   "score": -48.07
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
   "score": -53.97
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
   "score": -54.52
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
   "score": -56.37
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
   "score": -57.38
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
   "score": -57.38
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
   "score": -57.79
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
   "score": -57.79
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
   "score": -58.39
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
   "score": -58.39
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
   "score": -59.63
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
   "score": -62.42
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
   "score": -62.48
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
   "score": -64.64
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
   "score": -65.12
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
   "score": -67.29
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
   "score": -69.16
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
   "score": -69.16
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
   "score": -69.73
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
   "score": -70.35
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
   "score": -70.35
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
   "score": -74.96
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
   "score": -83.67
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
   "score": -84.28
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
   "score": -84.84
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
   "score": -84.84
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
   "score": -87.95
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
   "score": -89.29
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
   "score": -89.65
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
   "score": -104.24
  }
 ],
 "plants": {
  "found": 20,
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
    "best": 21.62,
    "best_key": "W?RA?DH?WDIFFICUL?IT?OU",
    "found": true,
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
    "best": 15.44,
    "best_key": "ATU???LYON?HE???DIT???S",
    "found": true,
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
    "best": 13.56,
    "best_key": "LYD????ATEDT???ACID???D",
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
    "best": 22.37,
    "best_key": "YIM???SSIVE??IGINAL?YTH",
    "found": true,
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
    "best": 22.35,
    "best_key": "HEM?E?VE??NDER??EL??RIN",
    "found": true,
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
    "best": 30.84,
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
    "best": 20.91,
    "best_key": "E?UTAL??O??H?EH?DRESIGN",
    "found": true,
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
    "best": 18.92,
    "best_key": "??OVEREDWI?????NGO???O?",
    "found": true,
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
    "best": 31.3,
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
    "best": 19.16,
    "best_key": "??MEINTO?H?VILL?GEON?AF",
    "found": true,
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
    "best": 16.09,
    "best_key": "TT?RTODEALWI?HITW??H?UL",
    "found": true,
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
    "best": 22.97,
    "best_key": "TTEREDF?OMT??SETR?ALSAN",
    "found": true,
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
    "best": 16.36,
    "best_key": "RK?OOVALU???ETOLEA?EAN?",
    "found": true,
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
    "best": 36.74,
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
    "best": 31.19,
    "best_key": "G?ROM?HEGOVER??E?TONCOM",
    "found": true,
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
    "best": 9.32,
    "best_key": "MHEBA??AVAUL?NOTARE?LT?",
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
    "best": 16.03,
    "best_key": "AN?BE??MEA???SA?EFEE?HI",
    "found": true,
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
    "best": 27.83,
    "best_key": "ESURFACEOF?HE??BEI?C??E",
    "found": true,
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
    "best": 21.98,
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
    "best": 28.49,
    "best_key": "TORATIO???TH??RO???ANDM",
    "found": true,
    "live": 9
   }
  ]
 },
 "copies": "200 fresh shuffles (seed 2620, as 0263)",
 "exhaustive": true,
 "compute_seconds": 50,
 "modal_cost_estimate": "as 0263 (65 s on 32 cores, $0.03) plus key scoring: about $0.05"
}
```

Notes: F6.22c: K4's best of 21 forced keys -11.9 bits against the best of 21 drawn from the shuffles' 1723 settings: p 0.060 (null median -26.4); per setting K4 mean -54.5 against -52.5 (one-sided p 0.840); shuffles with at least 21 settings: [(31, -34.6), (25, -23.05), (23, -43.22), (21, -36.4)]; plants found 20 of 20


