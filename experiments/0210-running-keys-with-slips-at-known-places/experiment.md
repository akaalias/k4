# 0210-running-keys-with-slips-at-known-places: A1.3: running keys from the named texts (K1-K3, the sculpture's texts, Carter, Sanborn's letters) on the standard, KRYPTOS and keyword tables, with up to seven of the 24 known letters carved wrong, exact, against scrambled copies, with planted slipped messages

**Family:** 1-keyed-periodic  
**Parent:** 0047-running-key-carter-and-sculpture-mixed-alphabets  
**Decision:** reverted  
**Run:** 2026-10-20T12:43:38+00:00, 143.6 s, status ran  
**Time by phase:** test 182 s, run 144 s, record 0 s

## In plain words

A running key uses a long text, a page of a book or the sculpture's own letters, as the secret word, one letter of the text for each letter of the message. Earlier experiments slid every text we could think of along the carving and found none that gives the 24 known letters. If Sanborn slipped at two or three of those places, the right text would have been thrown away. Here we let up to seven of them be wrong, on the carving and on scrambled copies, and we hide three messages of our own, with slips, to check they are found.

## Walkthrough, by hand

1. Write the key text (say Carter's book) under K4 from some starting letter.
2. At each of the 24 known places, look up on the table which carved letter the known letter and the key letter give.
3. Count the places where it is not the carved letter: those would be Sanborn's slips.
4. Keep the starting letter if 3 or fewer places disagree, and read the whole message with it.
5. Move the key text one letter and repeat, for every starting letter, both directions, every table.
6. Do the same on scrambled copies of the carving.

## Worked example (generated)

```
Carter's book as the key, from letter 1000, standard plain and KRYPTOS cipher alphabet, key letters on KRYPTOS, Vigenere

place  known  key  gives  carved
   22      E    Y      S       F   slip?
   23      A    P      P       L   slip?
   24      S    R      N       R   slip?
   25      T    E      T       V   slip?
   64      B    N      Q       N   slip?
   65      E    A      E       Y   slip?
   66      R    T      U       P   slip?

places that disagree, of 24: 24 (7 or fewer would be kept)
```

## Lineage

Inherits from 0047-running-key-carter-and-sculpture-mixed-alphabets. What changed: A1.3 (Stage 2, step 2, issue #76). 0004, 0017, 0021, 0045, 0047 and 0078 slid running keys from the named texts along K4 and asked for 0, at most 2 (0021, 0045, 0047) or at most 3 (0017) mismatches at the 24 known places; 0004 and 0078 reported best 16 and 15. Here every one of those searches is rerun in one pass allowing up to 7 slips, exact, by a pigeonhole index (with 7 or fewer slips, one of 8 blocks of 3 known places matches exactly), K4 against 20 scrambled copies, with three planted running-key messages carrying 2-3 slips. The item asks for k = 1-3; k up to 7 costs nothing more and shows how far the test reaches.

## Hypothesis (domain expert)

A1 (knowledge/12-assumptions.md); C7(a) and C6(a) (keys from the earlier texts and the sculpture: Sanborn 2005 'instructions in the earlier text that refer to later text', Scheidt 2003 'the keys were concealed at the sculpture'), C17 (a copper not as intended), C27(a) (the PALIMPCEST slip). A running key fixes every key letter from the text and the offset, so each setting gives one full reading and 24 checks. Setups: plain and cipher alphabets standard, KRYPTOS or keyword-mixed from the 61 vocabulary words (0045's pool of 63); K1-K3 sources with every pair (as 0045); Carter's Tomb of Tut-ankh-Amen vol. 1, the carved tableau (rows, rows with the index column, columns), the Morse (as carved, reversed order), the four ciphertexts as one panel and Sanborn's 1989 letter, the 1991 dedication texts and the 2025 open letter with one side standard or KRYPTOS or both sides the same keyword alphabet (as 0047, 0017, 0078); key letters on the standard or KRYPTOS order (or the keyword alphabet itself when both sides share it, as 0078); Vigenere, Beaufort, variant; every cyclic offset, forward and backward. A slip at a known place is one failed check; settings with 24 - k checks matched are counted for k = 0-7. Chance of one setting with k <= 3 among the ~1.2 x 10^9 trials: about 10^-17; with k <= 7 about 10^-9, so the 24 checks decide the running key at every k <= 7 (the key costs a source name and an offset, about 25 bits; the slips 4.7 k + log2 C(24, k) bits). Readings of any setting found go to quadgrams and the blind judge with the copies'.

## Prediction

No setting with 7 or fewer slips on K4 or on any copy (chance about 10^-9). The three planted messages are found at their own source, offset and table, each with exactly its planted slips, and their readings judged as English. Zero candidates on K4.

## Method

1. Build the sources and the alphabet pool as 0045, 0047, 0017, 0078.
2. For every source and key alphabet, index each offset by the key letters it puts on each of 8 blocks of 3 known places.
3. For every setup, compute the key letter each known place needs; look up the offsets that match a whole block; check those offsets on all 24 places.
4. Keep every setting with 7 or fewer mismatches, by count.
5. K4, 20 copies and three planted messages (with 10 copies each); readings of any setting found to quadgrams and the judge in one call.

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
 "family": "running keys from the named texts on standard, KRYPTOS and keyword tables, 0-7 known letters slipped (A1.3)",
 "alphabet_pool": 63,
 "setups": {
  "A (K1-K3, every pair)": 23997,
  "B (other sources, one side std/kry or both the same word)": 2037
 },
 "sources": {
  "K1 plain fwd": 63,
  "K1 plain bwd": 63,
  "K2 plain fwd": 369,
  "K2 plain bwd": 369,
  "K3 plain fwd": 336,
  "K3 plain bwd": 336,
  "K1+K2+K3 plain fwd": 768,
  "K1+K2+K3 plain bwd": 768,
  "K1 cipher fwd": 63,
  "K1 cipher bwd": 63,
  "K2 cipher fwd": 369,
  "K2 cipher bwd": 369,
  "K3 cipher fwd": 336,
  "K3 cipher bwd": 336,
  "K1+K2+K3 cipher fwd": 768,
  "K1+K2+K3 cipher bwd": 768,
  "K2 plain corrected ending fwd": 13,
  "K2 plain corrected ending bwd": 13,
  "carter vol1 fwd": 284914,
  "carter vol1 bwd": 284914,
  "tableau rows fwd": 781,
  "tableau rows bwd": 781,
  "tableau rows with index column fwd": 807,
  "tableau rows with index column bwd": 807,
  "tableau columns fwd": 781,
  "tableau columns bwd": 781,
  "morse as carved fwd": 80,
  "morse as carved bwd": 80,
  "morse reversed order fwd": 80,
  "morse reversed order bwd": 80,
  "right panel K1-K4 fwd": 865,
  "right panel K1-K4 bwd": 865,
  "letter 1989 fwd": 2176,
  "letter 1989 bwd": 2176,
  "Cryptogram 1991 fwd": 4880,
  "Cryptogram 1991 bwd": 4880,
  "open letter 2025 fwd": 2228,
  "open letter 2025 bwd": 2228
 },
 "trials": 1360451298,
 "offsets": "every cyclic offset, forward and backward",
 "max_slips": 7,
 "method": "pigeonhole index: 8 blocks of 3 known places, offsets bucketed by their key letters; every offset matching a whole block checked on all 24 (exact for <= 7)",
 "slip_cost_bits": {
  "1": 9.3,
  "2": 17.5,
  "3": 25.1,
  "4": 32.2,
  "5": 38.9,
  "6": 45.2,
  "7": 51.3
 },
 "chance_settings_at_k": {
  "0": "1.5e-25",
  "1": "9.0e-23",
  "2": "2.6e-20",
  "3": "4.7e-18",
  "4": "6.2e-16",
  "5": "6.2e-14",
  "6": "4.9e-12",
  "7": "3.2e-10"
 },
 "k4_settings_by_mismatches": [
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0
 ],
 "k4_settings": [],
 "copies_settings_by_mismatches": [
  [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ]
 ],
 "copies_done": 20,
 "copies_judge_best": [
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null
 ],
 "judge": {
  "sent": 3,
  "none": 0
 },
 "plants": [
  {
   "seed": 2101,
   "source": "carter vol1 fwd",
   "offset": 189303,
   "setup": "std/kry/kry/vig",
   "k": 3,
   "slips": [
    23,
    27,
    74
   ],
   "settings_found": 1,
   "by_mismatches": [
    0,
    0,
    0,
    1,
    0,
    0,
    0,
    0
   ],
   "planted_setting_mismatches": 3,
   "quad": -4.328,
   "judge": 96,
   "judge_reading": "FF TO A FURTHER DEBAUCH OF ### ELSEWHERE THIS WINTER DRAGOMAN AND T### ### WERE DISREGARDED ALIKE AN",
   "own_copies_settings": [
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
   "found": true
  },
  {
   "seed": 2102,
   "source": "K1+K2+K3 plain fwd",
   "offset": 307,
   "setup": "SHADOW/keyword/std/std/beau",
   "k": 2,
   "slips": [
    67,
    73
   ],
   "settings_found": 4,
   "by_mismatches": [
    0,
    0,
    2,
    0,
    0,
    0,
    0,
    2
   ],
   "planted_setting_mismatches": 2,
   "quad": -4.376,
   "judge": 90,
   "judge_reading": "(M)ATTERS IN THE VALLEY WENT ############# D TO WORSE THE TOMBS OF AMENHETEP II ########### INESESII ARE MENTIONED IN T",
   "own_copies_settings": [
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
   "found": true
  },
  {
   "seed": 2103,
   "source": "tableau rows bwd",
   "offset": 81,
   "setup": "kry/kry/kry/varbeau",
   "k": 3,
   "slips": [
    23,
    32,
    67
   ],
   "settings_found": 20,
   "by_mismatches": [
    0,
    0,
    0,
    2,
    4,
    6,
    4,
    4
   ],
   "planted_setting_mismatches": 3,
   "quad": -4.182,
   "judge": 93,
   "judge_reading": "CLOSE TO YOUR WORK AND EVE # # # # EING FOUND AT THE MOMENT YOU WILL NO # # # ME TO BE IDLE TO BEGIN WITH EV",
   "own_copies_settings": [
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
   "found": true
  }
 ],
 "covers": "0004, 0017, 0021, 0045, 0047, 0078 (their sources, tables and rules); not 0098/0154 (free alphabet) or 0117 (with moves)",
 "controls": "20 shuffled copies (seeds 2110-2129); each plant against 10 shuffles of its own ciphertext",
 "exhaustive": "yes"
}
```

Notes: 1,360,451,298 trials; K4 settings with <= 7 slips 0; copies [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]; plants found [True, True, True]


