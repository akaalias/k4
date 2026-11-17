# 0275-f16.1b-two-dictionary-keyword-alphabets-on-the-20-official-letters: F16.1b: two keyword alphabets from the whole dictionary, one on each side of the table, a repeating key (free, then a key word), on the 20 official known letters (EAST set aside): every pair of 208,064 alphabets through 0244's exact index, key lengths 1-26, both forms; K4 against 50 shuffles, 12 plants

**Family:** 16-simple-hand-methods  
**Parent:** 0244-f14-two-dictionary-keyword-alphabets-and-a-key-word  
**Decision:** reverted  
**Run:** 2026-11-17T14:40:16+00:00, 353.9 s, status ran  
**Time by phase:** test 18 s, run 354 s, record 0 s

## In plain words

Sanborn may have scrambled the alphabet on each side of his table with a different word, then used a repeating key word. Experiment 244 tried every pair of dictionary words for the two alphabets and found nothing, but it relied on EAST, which Sanborn confirmed only privately. Here we use only the 20 letters he published, try every pair again, and ask whether the key the known letters force is itself a word, on the carving and on 50 scrambled copies of it.

## Walkthrough, by hand

1. Pick two words, say SHADOW and LUCID, and write the keyword alphabets SHADOWBCEF... and LUCIDABEFG...
2. Choose a key length, say 16, and give each of the 20 known places its slot (place minus 1, mod 16).
3. For two known places in the same slot, the key is the same, so the cipher-alphabet distance between their two carved letters must equal the plain-alphabet distance between their two known letters.
4. If every such pair agrees, the alphabet pair fits length 16.
5. Read off the key letter each slot needs and see whether the letters spell a word, in some rotation and numbering.
6. Do the same on scrambled copies of the carving and compare.

## Worked example (generated)

```
key length 16: the 20 official places by slot (place - 1 mod 16); same-slot places share a key letter

  slot  0: 33 S->S, 65 E->Y
  slot  1: 34 T->S, 66 R->P
  slot  2: 67 L->V
  slot  3: 68 I->T
  slot  4: 69 N->T
  slot  5: 70 C->M
  slot  6: 71 L->Z
  slot  7: 72 O->F
  slot  8: 73 C->P
  slot  9: 26 N->Q, 74 K->K
  slot 10: 27 O->Q
  slot 11: 28 R->P
  slot 12: 29 T->R
  slot 13: 30 H->N
  slot 14: 31 E->G
  slot 15: 32 A->K, 64 B->N

A pair of alphabets fits when, in every slot with two places, the cipher-alphabet distance of the carved letters equals the plain-alphabet distance of the known letters.
```

## Lineage

Inherits from 0244-f14-two-dictionary-keyword-alphabets-and-a-key-word. What changed: F16.1 (issue #123), second part: 0244's search on the 20 letters Sanborn published himself (26-34, 64-74). The alphabets, the pair index and the key-word matcher are imported from 0244's attack.py unchanged. New: the fitting pairs are first screened for a key word by a vectorised hash of the forced key (every rotation of every dictionary and puzzle word, numbered on the standard, KRYPTOS, plain or cipher alphabet, any shift), and every hit is confirmed by 0244's own match_key_word; key words checked to length 23 (0244: 24), lengths 24-26 counted only, because without EAST length 24 has about 3 x 10^9 fitting pairs on K4.

## Hypothesis (domain expert)

As 0244: Scheidt's mask in its keyed form (C4(a), C5; 03-scheidt-said.md), a keyword monoalphabet before a keyed tableau, one Quagmire IV with the plain alphabet the mask's and the cipher alphabet the table's, both keyword-mixed from any dictionary word of 4+ letters (or standard, KRYPTOS), key free or a word. Criteria revised 2026-11-17 (#124): EAST (22-25) is second-hand, so the known letters are the 20 official ones. Constraint: at key length L, places in the same slot give one equation each; four fewer known letters remove the checks EAST gave, so pairs fit from about L = 14 (0244: 16 on K4) and the count rises steeply. Two tests: (a) fitting-pair counts per length and form against 50 shuffles (counts only; the key is free, a chart key under #124); (b) a key word (dictionary or puzzle, any rotation, numbering and shift) for the forced key at lengths 3-23, where chance matches stay far below one per text because the 20 places cover 9-17 slots.

## Prediction

No key word on K4 at any length 3-23 (shuffles: none or almost none). Fitting-pair counts per length and form inside the shuffles' range (K4 at or below the median in most cells; no cell where K4 beats all 50 by more than chance across 52 cells). Plants found 12 of 12 (their true pair fits and their key word is recovered). Candidates only if a key word fits: none expected.

## Method

1. Build 0244's 208,064 keyword alphabets and its rotation lists of every dictionary and puzzle word of 3-24 letters.
2. For each text, key length 1-26 and form: 0244's pair index over the 20 known places gives every (plain, cipher) alphabet pair that fits.
3. For lengths up to 23: the forced key on the covered slots, hashed against every word rotation in each numbering (standard, KRYPTOS: by differences; plain, cipher: by letters, for each of 26 first letters); every hit confirmed by 0244's match_key_word.
4. K4, 50 shuffles, 12 plants (Carter's text, two random dictionary alphabets, a random dictionary key word, at lengths 16-23).
5. Compare counts and matches with the shuffles.

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
 "item": "F16.1b",
 "known_places": [
  26,
  27,
  28,
  29,
  30,
  31,
  32,
  33,
  34,
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
  74
 ],
 "alphabets": 208064,
 "alphabet_pairs_per_form": 43290628096,
 "alphabet_source": "0244's: keyword-mixed alphabet of every dictionary word of 4+ letters plus standard and KRYPTOS",
 "key_lengths": [
  1,
  26
 ],
 "key_word_check_lengths": [
  3,
  23
 ],
 "count_only_lengths": [
  24,
  26
 ],
 "key_numbering": "standard, KRYPTOS, the plain alphabet or the cipher alphabet, any indicator shift 0-25",
 "screen": "64-bit hash of the forced key on covered slots against every rotation (differences for standard/KRYPTOS, letters for each of 26 first letters for plain/cipher); every hit confirmed by 0244's match_key_word",
 "fitting_pairs": {
  "1/added": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "copies_with_any": 0,
   "at_or_above": 50,
   "p": 1.0
  },
  "1/beaufort": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "copies_with_any": 0,
   "at_or_above": 50,
   "p": 1.0
  },
  "2/added": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "copies_with_any": 0,
   "at_or_above": 50,
   "p": 1.0
  },
  "2/beaufort": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "copies_with_any": 0,
   "at_or_above": 50,
   "p": 1.0
  },
  "3/added": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "copies_with_any": 0,
   "at_or_above": 50,
   "p": 1.0
  },
  "3/beaufort": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "copies_with_any": 0,
   "at_or_above": 50,
   "p": 1.0
  },
  "4/added": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "copies_with_any": 0,
   "at_or_above": 50,
   "p": 1.0
  },
  "4/beaufort": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "copies_with_any": 0,
   "at_or_above": 50,
   "p": 1.0
  },
  "5/added": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "copies_with_any": 0,
   "at_or_above": 50,
   "p": 1.0
  },
  "5/beaufort": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "copies_with_any": 0,
   "at_or_above": 50,
   "p": 1.0
  },
  "6/added": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "copies_with_any": 0,
   "at_or_above": 50,
   "p": 1.0
  },
  "6/beaufort": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "copies_with_any": 0,
   "at_or_above": 50,
   "p": 1.0
  },
  "7/added": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "copies_with_any": 0,
   "at_or_above": 50,
   "p": 1.0
  },
  "7/beaufort": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "copies_with_any": 0,
   "at_or_above": 50,
   "p": 1.0
  },
  "8/added": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "copies_with_any": 0,
   "at_or_above": 50,
   "p": 1.0
  },
  "8/beaufort": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "copies_with_any": 0,
   "at_or_above": 50,
   "p": 1.0
  },
  "9/added": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "copies_with_any": 0,
   "at_or_above": 50,
   "p": 1.0
  },
  "9/beaufort": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "copies_with_any": 0,
   "at_or_above": 50,
   "p": 1.0
  },
  "10/added": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "copies_with_any": 0,
   "at_or_above": 50,
   "p": 1.0
  },
  "10/beaufort": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "copies_with_any": 0,
   "at_or_above": 50,
   "p": 1.0
  },
  "11/added": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "copies_with_any": 0,
   "at_or_above": 50,
   "p": 1.0
  },
  "11/beaufort": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "copies_with_any": 0,
   "at_or_above": 50,
   "p": 1.0
  },
  "12/added": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 33,
   "copies_with_any": 5,
   "at_or_above": 50,
   "p": 1.0
  },
  "12/beaufort": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 2,
   "copies_with_any": 4,
   "at_or_above": 50,
   "p": 1.0
  },
  "13/added": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "copies_with_any": 0,
   "at_or_above": 50,
   "p": 1.0
  },
  "13/beaufort": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "copies_with_any": 0,
   "at_or_above": 50,
   "p": 1.0
  },
  "14/added": {
   "k4": 0,
   "copies_median": 2.0,
   "copies_max": 29,
   "copies_with_any": 37,
   "at_or_above": 50,
   "p": 1.0
  },
  "14/beaufort": {
   "k4": 0,
   "copies_median": 2.5,
   "copies_max": 32,
   "copies_with_any": 41,
   "at_or_above": 50,
   "p": 1.0
  },
  "15/added": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 124911,
   "copies_with_any": 3,
   "at_or_above": 50,
   "p": 1.0
  },
  "15/beaufort": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 262808,
   "copies_with_any": 3,
   "at_or_above": 50,
   "p": 1.0
  },
  "16/added": {
   "k4": 312778,
   "copies_median": 57895.0,
   "copies_max": 1055253,
   "copies_with_any": 45,
   "at_or_above": 4,
   "p": 0.098
  },
  "16/beaufort": {
   "k4": 10940,
   "copies_median": 60565.5,
   "copies_max": 3492231,
   "copies_with_any": 45,
   "at_or_above": 44,
   "p": 0.8824
  },
  "17/added": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 83074,
   "copies_with_any": 1,
   "at_or_above": 50,
   "p": 1.0
  },
  "17/beaufort": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 91826,
   "copies_with_any": 1,
   "at_or_above": 50,
   "p": 1.0
  },
  "18/added": {
   "k4": 0,
   "copies_median": 3.0,
   "copies_max": 992,
   "copies_with_any": 34,
   "at_or_above": 50,
   "p": 1.0
  },
  "18/beaufort": {
   "k4": 0,
   "copies_median": 2.5,
   "copies_max": 31,
   "copies_with_any": 36,
   "at_or_above": 50,
   "p": 1.0
  },
  "19/added": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "copies_with_any": 0,
   "at_or_above": 50,
   "p": 1.0
  },
  "19/beaufort": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "copies_with_any": 0,
   "at_or_above": 50,
   "p": 1.0
  },
  "20/added": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "copies_with_any": 0,
   "at_or_above": 50,
   "p": 1.0
  },
  "20/beaufort": {
   "k4": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "copies_with_any": 0,
   "at_or_above": 50,
   "p": 1.0
  },
  "21/added": {
   "k4": 0,
   "copies_median": 2.0,
   "copies_max": 29,
   "copies_with_any": 37,
   "at_or_above": 50,
   "p": 1.0
  },
  "21/beaufort": {
   "k4": 0,
   "copies_median": 2.5,
   "copies_max": 32,
   "copies_with_any": 41,
   "at_or_above": 50,
   "p": 1.0
  },
  "22/added": {
   "k4": 83,
   "copies_median": 1818.5,
   "copies_max": 77415,
   "copies_with_any": 46,
   "at_or_above": 45,
   "p": 0.902
  },
  "22/beaufort": {
   "k4": 3574,
   "copies_median": 2472.0,
   "copies_max": 79735,
   "copies_with_any": 46,
   "at_or_above": 22,
   "p": 0.451
  },
  "23/added": {
   "k4": 3206250,
   "copies_median": 1847044.5,
   "copies_max": 11327771,
   "copies_with_any": 42,
   "at_or_above": 11,
   "p": 0.2353
  },
  "23/beaufort": {
   "k4": 410571,
   "copies_median": 1725622.5,
   "copies_max": 6298711,
   "copies_with_any": 42,
   "at_or_above": 42,
   "p": 0.8431
  },
  "24/added": {
   "k4": 2654922390,
   "copies_median": 1464269229.5,
   "copies_max": 5207052069,
   "copies_with_any": 47,
   "at_or_above": 4,
   "p": 0.098
  },
  "24/beaufort": {
   "k4": 287773089,
   "copies_median": 1471262525.5,
   "copies_max": 6735212072,
   "copies_with_any": 47,
   "at_or_above": 47,
   "p": 0.9412
  },
  "25/added": {
   "k4": 43290628096,
   "copies_median": 43290628096.0,
   "copies_max": 43290628096,
   "copies_with_any": 50,
   "at_or_above": 50,
   "p": 1.0
  },
  "25/beaufort": {
   "k4": 43290628096,
   "copies_median": 43290628096.0,
   "copies_max": 43290628096,
   "copies_with_any": 50,
   "at_or_above": 50,
   "p": 1.0
  },
  "26/added": {
   "k4": 43290628096,
   "copies_median": 43290628096.0,
   "copies_max": 43290628096,
   "copies_with_any": 50,
   "at_or_above": 50,
   "p": 1.0
  },
  "26/beaufort": {
   "k4": 43290628096,
   "copies_median": 43290628096.0,
   "copies_max": 43290628096,
   "copies_with_any": 50,
   "at_or_above": 50,
   "p": 1.0
  }
 },
 "k4_above_every_copy_cells": [],
 "copies_above_the_rest_cells": {
  "min": 0,
  "max": 2
 },
 "lowest_length_with_a_fit_k4": 16,
 "key_word_matches": {
  "k4": 0,
  "copies": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
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
  ]
 },
 "screen_hits_k4": 0,
 "plants": {
  "plant16_0": {
   "L": 16,
   "found": true,
   "fits_at_L": 2175002,
   "matches": 1,
   "key_word": "EQUIDISTRIBUTION",
   "key_numbering": "cipher",
   "pa_word": "STERNUTATIVE",
   "ca_word": "RECORDATIVELY"
  },
  "plant16_1": {
   "L": 16,
   "found": true,
   "fits_at_L": 314558,
   "matches": 1,
   "key_word": "DISCOLOURIZATION",
   "key_numbering": "cipher",
   "pa_word": "ERMELIN",
   "ca_word": "STUMBLER"
  },
  "plant18_0": {
   "L": 18,
   "found": true,
   "fits_at_L": 391,
   "matches": 2,
   "key_word": "PSYCHOANALYTICALLY",
   "key_numbering": "cipher",
   "pa_word": "OVERSTOUT",
   "ca_word": "COTYLIGEROUS"
  },
  "plant18_1": {
   "L": 18,
   "found": true,
   "fits_at_L": 21,
   "matches": 1,
   "key_word": "TRANSRECTIFICATION",
   "key_numbering": "kry",
   "pa_word": "DESMODACTYLI",
   "ca_word": "GISMONDITE"
  },
  "plant20_0": {
   "L": 20,
   "found": true,
   "fits_at_L": 2,
   "matches": 4,
   "key_word": "ELECTROPHYSIOLOGICAL",
   "key_numbering": "plain",
   "pa_word": "COSTOTOMY",
   "ca_word": "PAMPHILIUS"
  },
  "plant20_1": {
   "L": 20,
   "found": true,
   "fits_at_L": 13,
   "matches": 6,
   "key_word": "SUPERPHLOGISTICATION",
   "key_numbering": "kry",
   "pa_word": "TASTEABLE",
   "ca_word": "SPIFF"
  },
  "plant21_0": {
   "L": 21,
   "found": true,
   "fits_at_L": 142,
   "matches": 1,
   "key_word": "NONINTERCHANGEABILITY",
   "key_numbering": "cipher",
   "pa_word": "CASTLEWISE",
   "ca_word": "THREADMAKER"
  },
  "plant21_1": {
   "L": 21,
   "found": true,
   "fits_at_L": 17,
   "matches": 1,
   "key_word": "CHOLEDOCHOLITHOTRIPSY",
   "key_numbering": "std",
   "pa_word": "FACTICE",
   "ca_word": "UNDEFRAYED"
  },
  "plant22_0": {
   "L": 22,
   "found": true,
   "fits_at_L": 37924,
   "matches": 1,
   "key_word": "PHILOSOPHICOHISTORICAL",
   "key_numbering": "kry",
   "pa_word": "DOUGHBIRD",
   "ca_word": "AZONIUM"
  },
  "plant22_1": {
   "L": 22,
   "found": true,
   "fits_at_L": 76766,
   "matches": 1,
   "key_word": "PYOPNEUMOCHOLECYSTITIS",
   "key_numbering": "kry",
   "pa_word": "PHELLOGEN",
   "ca_word": "ASPICULATE"
  },
  "plant23_0": {
   "L": 23,
   "found": true,
   "fits_at_L": 1477409,
   "matches": 1,
   "key_word": "GASTROENTEROANASTOMOSIS",
   "key_numbering": "kry",
   "pa_word": "SCLERETINITE",
   "ca_word": "BEKNOW"
  },
  "plant23_1": {
   "L": 23,
   "found": true,
   "fits_at_L": 5850818,
   "matches": 1,
   "key_word": "PERICARDIOMEDIASTINITIS",
   "key_numbering": "cipher",
   "pa_word": "AFFECTIBLE",
   "ca_word": "SURREY"
  }
 },
 "plants_found": 12,
 "plants_total": 12,
 "texts": 63,
 "copies": 50,
 "exhaustive": true,
 "compute_seconds": 282,
 "aws_cost_estimate_dollars": 0.5
}
```

Notes: 20 official letters; K4 first fit at L 16; key-word matches K4 0, copies max 0; K4 above every copy in 0 of 52 cells [] (copies 0-2); plants found 12/12


