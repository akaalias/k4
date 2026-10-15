# 0095-riddle-words-dragged-at-the-live-periods: Words a riddle would use, dragged across K4 at every repeating-key length the known letters allow

**Family:** 1-keyed-periodic  
**Parent:** 0001-crib-consistent-periods  
**Decision:** reverted  
**Run:** 2026-10-15T19:40:52+00:00, 16.4 s, status ran  
**Time by phase:** unattributed 9 s, run 16 s, record 0 s

## In plain words

If the message is a riddle like K2, which spelled out numbers and directions, it probably uses words such as THIRTY, DEGREES, NORTH or SHADOW. For every length of repeating secret word that fits the 24 known letters, we slide each such word along the message and ask whether it agrees with the key letters the known letters already fix. Random strings of letters, slid the same way, show how often agreement happens by luck.

## Walkthrough, by hand

1. Take the sculpture's alphabet, Vigenere, and a key of length 60; the known letters fix the key letters at slots 21-33 and 3-13.
2. Place the word DEGREES so that it starts at place 80.
3. Its letters fall on slots 19-25 (place mod 60); slots 21-25 are already fixed by EASTNORTHEAST's letters at places 22-26.
4. For each of those, the key letter that turns the word's letter into the carved letter must equal the fixed one.
5. All agree: a consistent placement with that many checks. One disagreement: rejected.
6. Repeat for every word, start, period and table rule, then for random strings.

## Worked example (generated)

```
sculpture's alphabet, Vigenere, key length 60: slots fixed by the known letters: [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]

DEGREES starting at place 80
place  letter  copper  slot  needed  fixed
   80       D       X    19      14       
   81       E       T    20      19       
   82       G       J    21       3      1
   83       R       C    22       8     10
   84       E       D    23      25     21
   85       E       I    24       4     18
   86       S       G    25       7      1
```

## Lineage

Inherits from 0001-crib-consistent-periods. What changed: Earlier periodic experiments at the live lengths (27-29 and 53 and up) filled the free key letters by climbing toward English, which cannot beat its own controls. Here nothing is climbed: each word of a fixed riddle lexicon (spelled numbers, units, compass words, the puzzle's own words, Sanborn's themes) is placed at every position, and a placement counts only if the key letters it forces agree with the ones the known letters already fix. Random letter strings of the same lengths are the control.

## Hypothesis (domain expert)

Type 8 of directions.md, 'a plaintext that is itself a riddle'. K2 spells out its coordinates (THIRTY EIGHT DEGREES FIFTY SEVEN MINUTES...) and ends LAYER TWO (01-facts.md); Sanborn 2025: the plaintext joins the 1986 Egypt trip, the 1989 Wall and 'delivering a message' (site_texts.json); issue #11 asks for credit for spelled numbers and the puzzle's words. Classical probable-word attack: for every single-alphabet periodic key the cribs allow (each of 8 tableau classes, every consistent period 27-96), each lexicon word w at every start x forces key values at slots (x + i) mod p; it is consistent if they agree with the slots fixed by the 24 known letters; placements overlapping the known stretches are skipped. The number of such agreements is its check count. Null: 40 random strings per word length on the same text and keys. A real word that is the plaintext would show up as a placement with many checks, or as an excess of 3+-check placements over the decoys.

## Prediction

Lexicon words reach consistent placements with three or more checks at the same rate as random strings of the same length (within the decoys' spread), and no placement has five or more checks. Zero candidates.

## Method

1. For each class and period 27-96, test crib consistency and keep the consistent pairs with their fixed key slots.
2. For each lexicon word and start clear of the known stretches, count agreements with fixed slots; reject on any disagreement.
3. Do the same for 40 random strings per length.
4. Compare counts of placements with 2, 3 and 4+ checks between words and decoys, per word length.
5. List the real-word placements with 3 or more checks.

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
 "family": "probable-word drag under every crib-consistent single-alphabet periodic key",
 "classes": 8,
 "consistent_class_period_pairs": 376,
 "periods_by_class": {
  "std/std/vig-var": [
   27,
   28,
   29,
   53,
   54,
   55,
   56,
   57,
   58,
   59,
   60,
   61,
   62,
   63,
   64,
   65,
   66,
   67,
   68,
   69,
   70,
   71,
   72,
   73,
   74,
   75,
   76,
   77,
   78,
   79,
   80,
   81,
   82,
   83,
   84,
   85,
   86,
   87,
   88,
   89,
   90,
   91,
   92,
   93,
   94,
   95,
   96
  ],
  "std/std/beau": [
   27,
   28,
   29,
   53,
   54,
   55,
   56,
   57,
   58,
   59,
   60,
   61,
   62,
   63,
   64,
   65,
   66,
   67,
   68,
   69,
   70,
   71,
   72,
   73,
   74,
   75,
   76,
   77,
   78,
   79,
   80,
   81,
   82,
   83,
   84,
   85,
   86,
   87,
   88,
   89,
   90,
   91,
   92,
   93,
   94,
   95,
   96
  ],
  "std/kry/vig-var": [
   27,
   28,
   29,
   53,
   54,
   55,
   56,
   57,
   58,
   59,
   60,
   61,
   62,
   63,
   64,
   65,
   66,
   67,
   68,
   69,
   70,
   71,
   72,
   73,
   74,
   75,
   76,
   77,
   78,
   79,
   80,
   81,
   82,
   83,
   84,
   85,
   86,
   87,
   88,
   89,
   90,
   91,
   92,
   93,
   94,
   95,
   96
  ],
  "std/kry/beau": [
   27,
   28,
   29,
   53,
   54,
   55,
   56,
   57,
   58,
   59,
   60,
   61,
   62,
   63,
   64,
   65,
   66,
   67,
   68,
   69,
   70,
   71,
   72,
   73,
   74,
   75,
   76,
   77,
   78,
   79,
   80,
   81,
   82,
   83,
   84,
   85,
   86,
   87,
   88,
   89,
   90,
   91,
   92,
   93,
   94,
   95,
   96
  ],
  "kry/std/vig-var": [
   27,
   28,
   29,
   53,
   54,
   55,
   56,
   57,
   58,
   59,
   60,
   61,
   62,
   63,
   64,
   65,
   66,
   67,
   68,
   69,
   70,
   71,
   72,
   73,
   74,
   75,
   76,
   77,
   78,
   79,
   80,
   81,
   82,
   83,
   84,
   85,
   86,
   87,
   88,
   89,
   90,
   91,
   92,
   93,
   94,
   95,
   96
  ],
  "kry/std/beau": [
   27,
   28,
   29,
   53,
   54,
   55,
   56,
   57,
   58,
   59,
   60,
   61,
   62,
   63,
   64,
   65,
   66,
   67,
   68,
   69,
   70,
   71,
   72,
   73,
   74,
   75,
   76,
   77,
   78,
   79,
   80,
   81,
   82,
   83,
   84,
   85,
   86,
   87,
   88,
   89,
   90,
   91,
   92,
   93,
   94,
   95,
   96
  ],
  "kry/kry/vig-var": [
   27,
   28,
   29,
   53,
   54,
   55,
   56,
   57,
   58,
   59,
   60,
   61,
   62,
   63,
   64,
   65,
   66,
   67,
   68,
   69,
   70,
   71,
   72,
   73,
   74,
   75,
   76,
   77,
   78,
   79,
   80,
   81,
   82,
   83,
   84,
   85,
   86,
   87,
   88,
   89,
   90,
   91,
   92,
   93,
   94,
   95,
   96
  ],
  "kry/kry/beau": [
   27,
   28,
   29,
   53,
   54,
   55,
   56,
   57,
   58,
   59,
   60,
   61,
   62,
   63,
   64,
   65,
   66,
   67,
   68,
   69,
   70,
   71,
   72,
   73,
   74,
   75,
   76,
   77,
   78,
   79,
   80,
   81,
   82,
   83,
   84,
   85,
   86,
   87,
   88,
   89,
   90,
   91,
   92,
   93,
   94,
   95,
   96
  ]
 },
 "lexicon_words": 93,
 "lexicon": [
  "THREE",
  "SEVEN",
  "EIGHT",
  "ELEVEN",
  "TWELVE",
  "THIRTEEN",
  "FOURTEEN",
  "FIFTEEN",
  "SIXTEEN",
  "SEVENTEEN",
  "EIGHTEEN",
  "NINETEEN",
  "TWENTY",
  "THIRTY",
  "FORTY",
  "FIFTY",
  "SIXTY",
  "SEVENTY",
  "EIGHTY",
  "NINETY",
  "HUNDRED",
  "THOUSAND",
  "FIRST",
  "SECOND",
  "THIRD",
  "FOURTH",
  "FIFTH",
  "NINETEENEIGHTYSIX",
  "NINETEENEIGHTYNINE",
  "DEGREES",
  "DEGREE",
  "MINUTES",
  "SECONDS",
  "POINT",
  "YARDS",
  "PACES",
  "METERS",
  "MILES",
  "HOURS",
  "OCLOCK",
  "NORTH",
  "SOUTH",
  "NORTHEAST",
  "NORTHWEST",
  "SOUTHEAST",
  "SOUTHWEST",
  "NORTHNORTHEAST",
  "EASTSOUTHEAST",
  "BEARING",
  "COMPASS",
  "LODESTONE",
  "MAGNETIC",
  "EGYPT",
  "CAIRO",
  "LUXOR",
  "PYRAMID",
  "SPHINX",
  "BERLIN",
  "CLOCK",
  "WORLDCLOCK",
  "ALEXANDERPLATZ",
  "MESSAGE",
  "DELIVER",
  "DELIVERING",
  "DELIVERED",
  "NOVEMBER",
  "NINTH",
  "CHECKPOINT",
  "CHARLIE",
  "BRANDENBURG",
  "LAYER",
  "SHADOW",
  "SHADOWS",
  "INVISIBLE",
  "POSITION",
  "LOCATION",
  "BURIED",
  "UNDERGROUND",
  "SECRET",
  "HIDDEN",
  "AGENT",
  "LANGLEY",
  "KRYPTOS",
  "PALIMPSEST",
  "ABSCISSA",
  "ILLUSION",
  "IQLUSION",
  "LIGHT",
  "DARKNESS",
  "CANDLE",
  "CHAMBER",
  "PASSAGE",
  "DOORWAY"
 ],
 "decoys_per_length": 40,
 "by_length_and_checks": {
  "5": {
   "2": {
    "words_mean": 0.92,
    "decoys_mean": 0.68,
    "decoys_95th": 3,
    "decoys_max": 3
   },
   "3": {
    "words_mean": 0.0,
    "decoys_mean": 0.05,
    "decoys_95th": 0,
    "decoys_max": 1
   },
   "4": {
    "words_mean": 0.0,
    "decoys_mean": 0.0,
    "decoys_95th": 0,
    "decoys_max": 0
   },
   "5": {
    "words_mean": 0.0,
    "decoys_mean": 0.0,
    "decoys_95th": 0,
    "decoys_max": 0
   }
  },
  "6": {
   "2": {
    "words_mean": 0.61,
    "decoys_mean": 0.53,
    "decoys_95th": 2,
    "decoys_max": 3
   },
   "3": {
    "words_mean": 0.0,
    "decoys_mean": 0.05,
    "decoys_95th": 0,
    "decoys_max": 1
   },
   "4": {
    "words_mean": 0.0,
    "decoys_mean": 0.0,
    "decoys_95th": 0,
    "decoys_max": 0
   },
   "5": {
    "words_mean": 0.0,
    "decoys_mean": 0.0,
    "decoys_95th": 0,
    "decoys_max": 0
   }
  },
  "7": {
   "2": {
    "words_mean": 0.58,
    "decoys_mean": 0.6,
    "decoys_95th": 2,
    "decoys_max": 4
   },
   "3": {
    "words_mean": 0.0,
    "decoys_mean": 0.1,
    "decoys_95th": 1,
    "decoys_max": 1
   },
   "4": {
    "words_mean": 0.0,
    "decoys_mean": 0.03,
    "decoys_95th": 0,
    "decoys_max": 1
   },
   "5": {
    "words_mean": 0.0,
    "decoys_mean": 0.0,
    "decoys_95th": 0,
    "decoys_max": 0
   }
  },
  "8": {
   "2": {
    "words_mean": 0.46,
    "decoys_mean": 0.55,
    "decoys_95th": 2,
    "decoys_max": 2
   },
   "3": {
    "words_mean": 0.0,
    "decoys_mean": 0.03,
    "decoys_95th": 0,
    "decoys_max": 1
   },
   "4": {
    "words_mean": 0.0,
    "decoys_mean": 0.0,
    "decoys_95th": 0,
    "decoys_max": 0
   },
   "5": {
    "words_mean": 0.0,
    "decoys_mean": 0.0,
    "decoys_95th": 0,
    "decoys_max": 0
   }
  },
  "9": {
   "2": {
    "words_mean": 0.62,
    "decoys_mean": 0.3,
    "decoys_95th": 1,
    "decoys_max": 2
   },
   "3": {
    "words_mean": 0.0,
    "decoys_mean": 0.05,
    "decoys_95th": 0,
    "decoys_max": 1
   },
   "4": {
    "words_mean": 0.0,
    "decoys_mean": 0.0,
    "decoys_95th": 0,
    "decoys_max": 0
   },
   "5": {
    "words_mean": 0.0,
    "decoys_mean": 0.0,
    "decoys_95th": 0,
    "decoys_max": 0
   }
  },
  "10": {
   "2": {
    "words_mean": 0.25,
    "decoys_mean": 0.55,
    "decoys_95th": 2,
    "decoys_max": 3
   },
   "3": {
    "words_mean": 0.0,
    "decoys_mean": 0.03,
    "decoys_95th": 0,
    "decoys_max": 1
   },
   "4": {
    "words_mean": 0.0,
    "decoys_mean": 0.0,
    "decoys_95th": 0,
    "decoys_max": 0
   },
   "5": {
    "words_mean": 0.0,
    "decoys_mean": 0.0,
    "decoys_95th": 0,
    "decoys_max": 0
   }
  },
  "11": {
   "2": {
    "words_mean": 0.0,
    "decoys_mean": 0.3,
    "decoys_95th": 1,
    "decoys_max": 2
   },
   "3": {
    "words_mean": 0.0,
    "decoys_mean": 0.0,
    "decoys_95th": 0,
    "decoys_max": 0
   },
   "4": {
    "words_mean": 0.0,
    "decoys_mean": 0.0,
    "decoys_95th": 0,
    "decoys_max": 0
   },
   "5": {
    "words_mean": 0.0,
    "decoys_mean": 0.0,
    "decoys_95th": 0,
    "decoys_max": 0
   }
  },
  "13": {
   "2": {
    "words_mean": 1.0,
    "decoys_mean": 0.33,
    "decoys_95th": 1,
    "decoys_max": 2
   },
   "3": {
    "words_mean": 0.0,
    "decoys_mean": 0.03,
    "decoys_95th": 0,
    "decoys_max": 1
   },
   "4": {
    "words_mean": 0.0,
    "decoys_mean": 0.0,
    "decoys_95th": 0,
    "decoys_max": 0
   },
   "5": {
    "words_mean": 0.0,
    "decoys_mean": 0.0,
    "decoys_95th": 0,
    "decoys_max": 0
   }
  },
  "14": {
   "2": {
    "words_mean": 0.5,
    "decoys_mean": 0.2,
    "decoys_95th": 1,
    "decoys_max": 1
   },
   "3": {
    "words_mean": 0.0,
    "decoys_mean": 0.03,
    "decoys_95th": 0,
    "decoys_max": 1
   },
   "4": {
    "words_mean": 0.0,
    "decoys_mean": 0.0,
    "decoys_95th": 0,
    "decoys_max": 0
   },
   "5": {
    "words_mean": 0.0,
    "decoys_mean": 0.0,
    "decoys_95th": 0,
    "decoys_max": 0
   }
  },
  "17": {
   "2": {
    "words_mean": 0.0,
    "decoys_mean": 0.15,
    "decoys_95th": 1,
    "decoys_max": 2
   },
   "3": {
    "words_mean": 0.0,
    "decoys_mean": 0.0,
    "decoys_95th": 0,
    "decoys_max": 0
   },
   "4": {
    "words_mean": 0.0,
    "decoys_mean": 0.0,
    "decoys_95th": 0,
    "decoys_max": 0
   },
   "5": {
    "words_mean": 0.0,
    "decoys_mean": 0.0,
    "decoys_95th": 0,
    "decoys_max": 0
   }
  },
  "18": {
   "2": {
    "words_mean": 0.0,
    "decoys_mean": 0.17,
    "decoys_95th": 1,
    "decoys_max": 1
   },
   "3": {
    "words_mean": 0.0,
    "decoys_mean": 0.03,
    "decoys_95th": 0,
    "decoys_max": 1
   },
   "4": {
    "words_mean": 0.0,
    "decoys_mean": 0.0,
    "decoys_95th": 0,
    "decoys_max": 0
   },
   "5": {
    "words_mean": 0.0,
    "decoys_mean": 0.0,
    "decoys_95th": 0,
    "decoys_max": 0
   }
  }
 },
 "words_above_all_decoys": [],
 "max_checks_real": 2,
 "max_checks_decoys": 4,
 "top_real_placements": [],
 "controls": "40 random strings per word length (seed 95), same text, keys and drag"
}
```

Notes: 93 words x 376 consistent (class, period) keys, every start. Most checks: real words 2, decoys 4. Words above every decoy of their length at 3+ checks: []; at 4+: [].


