# 0247-f14-two-dictionary-alphabets-with-a-carved-letter-lost: F14.5: 0244's two dictionary keyword alphabets and key word, with one carved letter lost (Scheidt's '98 characters'): the 23 distinct places a lost letter changes the key's alignment, every alphabet pair, key lengths 1-26; K4 against 20 shuffles per variant, a planted lost-letter message per variant

**Family:** 14-scheidt-mask-keyed-by-words  
**Parent:** 0244-f14-two-dictionary-keyword-alphabets-and-a-key-word  
**Decision:** reverted  
**Run:** 2026-10-28T04:02:36+00:00, 535.1 s, status ran  
**Time by phase:** unattributed 312 s, run 535 s, record 0 s

## In plain words

One of the creators once said there were 98 characters, not 97. If Sanborn dropped one letter when cutting the copper, as he did in an earlier section, then from that letter on the secret key would be off by one step, and every exact test so far would have missed it. We rerun the two-scrambled-alphabets test for every place where a lost letter would change anything.

## Walkthrough, by hand

1. Suppose Sanborn enciphered 98 letters and left one out when cutting, say between EASTNORTHEAST and BERLINCLOCK.
2. Then the key letter under each letter of BERLINCLOCK is the one for the next place.
3. Shift BERLINCLOCK's key places by one and rerun the alphabet-pair lookup of 0244.
4. Do the same for a letter lost inside either known word, at each of its places.
5. Compare K4 with shuffles treated the same way, and check that planted messages with a lost letter are found.

## Worked example (generated)

```
Key length 19: known places in the same key slot, and what they ask of the two alphabets (added form)

places   known  carved   the gap on the cipher alphabet must equal the gap on the plain alphabet
 26,64    NB     QN       gap(Q to N) on the cipher alphabet = gap(N to B) on the plain alphabet
 27,65    OE     QY       gap(Q to Y) on the cipher alphabet = gap(O to E) on the plain alphabet
 28,66    RR     PP       gap(P to P) on the cipher alphabet = gap(R to R) on the plain alphabet
 29,67    TL     RV       gap(R to V) on the cipher alphabet = gap(T to L) on the plain alphabet
 30,68    HI     NT       gap(N to T) on the cipher alphabet = gap(H to I) on the plain alphabet
 31,69    EN     GT       gap(G to T) on the cipher alphabet = gap(E to N) on the plain alphabet
 32,70    AC     KM       gap(K to M) on the cipher alphabet = gap(A to C) on the plain alphabet
 33,71    SL     SZ       gap(S to Z) on the cipher alphabet = gap(S to L) on the plain alphabet
 34,72    TO     SF       gap(S to F) on the cipher alphabet = gap(T to O) on the plain alphabet

Every cipher alphabet is filed by its gaps; every plain alphabet looks up the gaps it needs.
```

## Lineage

Inherits from 0244-f14-two-dictionary-keyword-alphabets-and-a-key-word. What changed: F14.5 (issue #93). Scheidt, 2005: 'I think there are 98 characters left' (C18(b)); A4, F1.6 and 0086 did this for earlier key sources. The enciphering ran over 98 letters and one carved letter was lost: the key index of a carved place at or after the loss is one more than its place. The known words stay where Sanborn put them on the copper. With a free key only the alignment between known places matters, so a loss before 22 or after 74 (and a '?' counted before OBKR) changes nothing that 0244 did not test; a loss at 23-34 or 65-74 splits a known run, and any loss at 35-64 moves BERLINCLOCK's key slots by one against EASTNORTHEAST's: 23 distinct variants. 0244's exact index search and key-word check run unchanged on each, with the key index shifted.

## Hypothesis (domain expert)

C18(b) and C17 (Scheidt 2005 '98 characters left'; Sanborn 'whether it's 97, whether it's 100'; K2 lost a letter for visual balance, 01-facts.md), F14.1's keyed mask (C4(a), C5). A lost letter misaligns the key from that place on, which can hide a fitting key from every exact test run on the 97 as carved (A1, A4). Pre-registered: in no variant does K4 match a key word; fitting-pair counts as the copies'. A plant (98-letter Carter, two random dictionary alphabets, a random dictionary key word of 16-24 letters, one carved letter dropped at the variant's place) is found when its true alphabets and key word are recovered under its own variant.

## Prediction

No key word on K4 in any of the 23 variants; fitting pairs at the copies' rate; plants found 23 of 23.

## Method

1. Variants: a letter lost at carved place j = 23..34, 35 (standing for 35-64), 65..74; key index of carved place q is q for q < j and q + 1 from j on.
2. For each variant: 0244's search (208,064 keyword alphabets, every ordered pair matched through the gap index, key lengths 1-26, both forms; key words of length L from the dictionary and the puzzle, 4 numberings, any shift).
3. K4 and 20 shuffles per variant; one plant per variant (98 letters enciphered, the letter at j dropped).
4. Any K4 key-word match decrypted with its variant and submitted.

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
 "item": "F14.5 (F14.1's half)",
 "variants": [
  23,
  24,
  25,
  26,
  27,
  28,
  29,
  30,
  31,
  32,
  33,
  34,
  35,
  65,
  66,
  67,
  68,
  69,
  70,
  71,
  72,
  73,
  74
 ],
 "variant_meaning": "a carved letter lost at place j; 35 stands for any place 35-64",
 "alphabets": 208064,
 "key_lengths": [
  1,
  26
 ],
 "copies_per_variant": 20,
 "texts": 506,
 "per_variant": {
  "23": {
   "k4_key_word_matches": 0,
   "copies_key_word_matches_max": 0,
   "k4_first_fitting_length": 23,
   "cells_k4_above_every_copy": [
    "25/added"
   ],
   "plant_found": true,
   "plant_L": 21,
   "plant_word": "ANTHROPOCLIMATOLOGIST"
  },
  "24": {
   "k4_key_word_matches": 0,
   "copies_key_word_matches_max": 0,
   "k4_first_fitting_length": 16,
   "cells_k4_above_every_copy": [
    "16/added"
   ],
   "plant_found": true,
   "plant_L": 21,
   "plant_word": "PENTAMETHYLENEDIAMINE"
  },
  "25": {
   "k4_key_word_matches": 0,
   "copies_key_word_matches_max": 0,
   "k4_first_fitting_length": 16,
   "cells_k4_above_every_copy": [],
   "plant_found": true,
   "plant_L": 16,
   "plant_word": "IMPERFECTIBILITY"
  },
  "26": {
   "k4_key_word_matches": 0,
   "copies_key_word_matches_max": 0,
   "k4_first_fitting_length": 23,
   "cells_k4_above_every_copy": [],
   "plant_found": true,
   "plant_L": 21,
   "plant_word": "INTERTRANSFORMABILITY"
  },
  "27": {
   "k4_key_word_matches": 0,
   "copies_key_word_matches_max": 0,
   "k4_first_fitting_length": 19,
   "cells_k4_above_every_copy": [
    "19/added"
   ],
   "plant_found": true,
   "plant_L": 16,
   "plant_word": "PHANTASMOGENESIS"
  },
  "28": {
   "k4_key_word_matches": 0,
   "copies_key_word_matches_max": 0,
   "k4_first_fitting_length": 19,
   "cells_k4_above_every_copy": [
    "19/added"
   ],
   "plant_found": true,
   "plant_L": 18,
   "plant_word": "PHYSICOTHEOLOGICAL"
  },
  "29": {
   "k4_key_word_matches": 0,
   "copies_key_word_matches_max": 0,
   "k4_first_fitting_length": 18,
   "cells_k4_above_every_copy": [],
   "plant_found": true,
   "plant_L": 17,
   "plant_word": "TRANSCENDENTALITY"
  },
  "30": {
   "k4_key_word_matches": 0,
   "copies_key_word_matches_max": 0,
   "k4_first_fitting_length": 18,
   "cells_k4_above_every_copy": [],
   "plant_found": true,
   "plant_L": 17,
   "plant_word": "CRYSTALLOCHEMICAL"
  },
  "31": {
   "k4_key_word_matches": 0,
   "copies_key_word_matches_max": 0,
   "k4_first_fitting_length": 18,
   "cells_k4_above_every_copy": [],
   "plant_found": true,
   "plant_L": 24,
   "plant_word": "THYROPARATHYROIDECTOMIZE"
  },
  "32": {
   "k4_key_word_matches": 0,
   "copies_key_word_matches_max": 0,
   "k4_first_fitting_length": 18,
   "cells_k4_above_every_copy": [],
   "plant_found": true,
   "plant_L": 17,
   "plant_word": "TEMPOROCEREBELLAR"
  },
  "33": {
   "k4_key_word_matches": 0,
   "copies_key_word_matches_max": 0,
   "k4_first_fitting_length": 18,
   "cells_k4_above_every_copy": [],
   "plant_found": true,
   "plant_L": 17,
   "plant_word": "MICROLEPIDOPTERAN"
  },
  "34": {
   "k4_key_word_matches": 0,
   "copies_key_word_matches_max": 0,
   "k4_first_fitting_length": 18,
   "cells_k4_above_every_copy": [],
   "plant_found": true,
   "plant_L": 16,
   "plant_word": "UNCONSPIRINGNESS"
  },
  "35": {
   "k4_key_word_matches": 0,
   "copies_key_word_matches_max": 0,
   "k4_first_fitting_length": 18,
   "cells_k4_above_every_copy": [],
   "plant_found": true,
   "plant_L": 17,
   "plant_word": "UNCONVERSABLENESS"
  },
  "65": {
   "k4_key_word_matches": 0,
   "copies_key_word_matches_max": 0,
   "k4_first_fitting_length": 16,
   "cells_k4_above_every_copy": [
    "16/added",
    "24/added"
   ],
   "plant_found": true,
   "plant_L": 19,
   "plant_word": "AUTOCHOLECYSTECTOMY"
  },
  "66": {
   "k4_key_word_matches": 0,
   "copies_key_word_matches_max": 0,
   "k4_first_fitting_length": 16,
   "cells_k4_above_every_copy": [
    "16/added"
   ],
   "plant_found": true,
   "plant_L": 18,
   "plant_word": "ACTINOELECTRICALLY"
  },
  "67": {
   "k4_key_word_matches": 0,
   "copies_key_word_matches_max": 0,
   "k4_first_fitting_length": 24,
   "cells_k4_above_every_copy": [],
   "plant_found": true,
   "plant_L": 23,
   "plant_word": "PSEUDOLAMELLIBRANCHIATE"
  },
  "68": {
   "k4_key_word_matches": 0,
   "copies_key_word_matches_max": 0,
   "k4_first_fitting_length": 19,
   "cells_k4_above_every_copy": [
    "19/added",
    "19/beaufort",
    "24/added"
   ],
   "plant_found": true,
   "plant_L": 22,
   "plant_word": "STEREOPHOTOMICROGRAPHY"
  },
  "69": {
   "k4_key_word_matches": 0,
   "copies_key_word_matches_max": 0,
   "k4_first_fitting_length": 19,
   "cells_k4_above_every_copy": [],
   "plant_found": true,
   "plant_L": 21,
   "plant_word": "STEREOPHOTOMICROGRAPH"
  },
  "70": {
   "k4_key_word_matches": 0,
   "copies_key_word_matches_max": 0,
   "k4_first_fitting_length": 19,
   "cells_k4_above_every_copy": [
    "19/beaufort"
   ],
   "plant_found": true,
   "plant_L": 19,
   "plant_word": "PSEUDOCHROMESTHESIA"
  },
  "71": {
   "k4_key_word_matches": 0,
   "copies_key_word_matches_max": 0,
   "k4_first_fitting_length": 19,
   "cells_k4_above_every_copy": [
    "19/added"
   ],
   "plant_found": true,
   "plant_L": 18,
   "plant_word": "DISCOMMENDABLENESS"
  },
  "72": {
   "k4_key_word_matches": 0,
   "copies_key_word_matches_max": 0,
   "k4_first_fitting_length": 19,
   "cells_k4_above_every_copy": [],
   "plant_found": true,
   "plant_L": 18,
   "plant_word": "COUNTERTRANSLATION"
  },
  "73": {
   "k4_key_word_matches": 0,
   "copies_key_word_matches_max": 0,
   "k4_first_fitting_length": 24,
   "cells_k4_above_every_copy": [],
   "plant_found": true,
   "plant_L": 19,
   "plant_word": "ANTHROPOSOCIOLOGIST"
  },
  "74": {
   "k4_key_word_matches": 0,
   "copies_key_word_matches_max": 0,
   "k4_first_fitting_length": 24,
   "cells_k4_above_every_copy": [
    "24/added"
   ],
   "plant_found": true,
   "plant_L": 23,
   "plant_word": "HEMATOSPECTROPHOTOMETER"
  }
 },
 "k4_key_word_matches_total": 0,
 "plants_found": 23,
 "plants_total": 23,
 "cells_k4_above_every_copy": 13,
 "cells": 1196,
 "subsumed_by_0244": "a '?' counted before OBKR, or a letter lost before 22 or after 74: every known place shifts alike, which a free key absorbs",
 "exhaustive": true,
 "compute_seconds": 472
}
```

Notes: 23 lost-letter variants x 4.3e10 alphabet pairs x lengths 1-26: K4 key-word matches 0; cells with K4 above all 20 copies 13 of 1196; plants found 23/23


