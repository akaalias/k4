# 0183-repeated-letter-phrase-homophones: F2.3: a 26-letter phrase with repeated letters as the plain strip, so a letter may be enciphered from any of its places (homophones that keep the length), repeating key 1-26: exact

**Family:** 2-masked-then-keyed  
**Parent:** 0057-letter-nulls-outside-the-cribs  
**Decision:** reverted  
**Run:** 2026-10-17T00:31:29+00:00, 4.1 s, status ran  
**Time by phase:** design 0 s, implement 0 s, test 0 s, run 4 s, record 0 s

## In plain words

Write a phrase such as NOW IS THE TIME FOR ALL GOOD MEN on a strip instead of the alphabet. Letters that appear twice give the encipherer a choice, so the same plain letter can turn into different code letters, yet the message stays the same length. Slide the strip against an alphabet by a repeating secret word. For each phrase from the sculpture's own texts, the 24 known letters say which secret words remain possible.

## Walkthrough, by hand

1. Write the phrase on the plain strip; E stands at, say, places 3 and 9 of it.
2. The known E at place 22 is carved F: F sits at place 5 of the standard cipher strip.
3. So the key there is 5 - 3 = 2 or 5 - 9 = 22: either is allowed.
4. For a key of length 7, place 29 shares that slot: its allowed values must include 2 or 22.
5. A slot with no common value kills the length. Repeat for every phrase and length, and on copies.

## Worked example (generated)

```
phrase strip NOWISTHETIMEFORALLGOODMENT (lacks C, K: such a phrase is dropped)

place 22: E at strip places [7, 11, 23], carved F at 5: allowed keys [8, 20, 24]
place 23: A at strip places [15], carved L at 11: allowed keys [22]
place 24: S at strip places [4], carved R at 17: allowed keys [13]
place 25: T at strip places [5, 8, 25], carved V at 21: allowed keys [13, 16, 22]
place 26: N at strip places [0, 24], carved Q at 16: allowed keys [16, 18]
place 27: O at strip places [1, 13, 19, 20], carved Q at 16: allowed keys [3, 15, 22, 23]
place 28: R at strip places [14], carved P at 15: allowed keys [1]
place 29: T at strip places [5, 8, 25], carved R at 17: allowed keys [9, 12, 18]
```

## Lineage

Inherits from 0057-letter-nulls-outside-the-cribs. What changed: F2.3. Not a documented method: the reverse use of EMC par. 45b derived in research_notes/Scheidt patents and field ciphers/addendum_downloaded_manuals.md (issue #9), and stated as such. The plain strip is a 26-letter phrase with its repeats (NOWISTHETIMEFORALLGOODMENT...); a letter that occurs twice may be taken from either place; the cipher strip is the standard or KRYPTOS order, slid by a repeating key. Phrases: every 26-letter window of the K1, K2 and K3 plaintexts, the Morse texts, Carter's 1923 book (K3's source) and famous sentences, kept if they hold the 13 letters of the known words. At each known place the allowed key values form a set; sets intersect per key slot. Lengths 1-26, slide either way; K4 against 20 shuffled copies.

## Hypothesis (domain expert)

Scheidt: 'I masked the English language' (C2): homophones flatten letter counts without lengthening the text (K4's flat counts, 0056). EMC par. 45b (keyword phrases with repeated letters for components), reversed here as a derivation (addendum, candidate 3). Model: c_i = C[(j + k_{i mod L}) mod 26] or C[(k - j) mod 26] with phrase[j] = p_i, the choice of j free. Exact: allowed k per known place = {C^-1(c) -+ j : phrase[j] = p}, intersected per slot. Statistic: live (phrase, strip, form, L) cells with at least one check, K4 against copies.

## Prediction

Live cells with checks at the shuffled copies' rate; homophones loosen each check, so short lengths may survive on copies as on K4. Zero candidates.

## Method

1. Phrases: 26-letter windows of K1-K3, the Morse, Carter's book, famous sentences; keep those with E A S T N O R H B L I C K.
2. For each text, phrase, cipher strip (standard, KRYPTOS) and form (j + k, k - j): allowed key values per known place.
3. For lengths 1-26: intersect per slot; live if no slot is empty.
4. K4 against 20 shuffled copies; a planted text as a builder check.

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
 "family": "repeated-letter phrase as plain strip (homophones keeping the length), cipher strip std/KRYPTOS, slide j+k or k-j, repeating key 1-26, exact; a derivation from EMC 45b, not a documented method",
 "phrases": 1196,
 "cells_per_text": 124384,
 "live_cells": {
  "k4": 617,
  "copies": [
   685,
   693,
   424,
   734,
   737,
   516,
   0,
   501,
   600,
   386,
   611,
   703,
   555,
   548,
   574,
   638,
   366,
   616,
   386,
   574
  ]
 },
 "per_length": {
  "1": {
   "k4": 0,
   "copies_min": 0,
   "copies_max": 0,
   "checks": 23
  },
  "2": {
   "k4": 0,
   "copies_min": 0,
   "copies_max": 0,
   "checks": 22
  },
  "3": {
   "k4": 0,
   "copies_min": 0,
   "copies_max": 0,
   "checks": 21
  },
  "4": {
   "k4": 0,
   "copies_min": 0,
   "copies_max": 0,
   "checks": 20
  },
  "5": {
   "k4": 0,
   "copies_min": 0,
   "copies_max": 0,
   "checks": 19
  },
  "6": {
   "k4": 0,
   "copies_min": 0,
   "copies_max": 0,
   "checks": 18
  },
  "7": {
   "k4": 0,
   "copies_min": 0,
   "copies_max": 0,
   "checks": 17
  },
  "8": {
   "k4": 0,
   "copies_min": 0,
   "copies_max": 0,
   "checks": 16
  },
  "9": {
   "k4": 0,
   "copies_min": 0,
   "copies_max": 0,
   "checks": 15
  },
  "10": {
   "k4": 0,
   "copies_min": 0,
   "copies_max": 0,
   "checks": 14
  },
  "11": {
   "k4": 0,
   "copies_min": 0,
   "copies_max": 0,
   "checks": 13
  },
  "12": {
   "k4": 0,
   "copies_min": 0,
   "copies_max": 0,
   "checks": 12
  },
  "13": {
   "k4": 0,
   "copies_min": 0,
   "copies_max": 0,
   "checks": 11
  },
  "14": {
   "k4": 0,
   "copies_min": 0,
   "copies_max": 0,
   "checks": 11
  },
  "15": {
   "k4": 0,
   "copies_min": 0,
   "copies_max": 0,
   "checks": 9
  },
  "16": {
   "k4": 0,
   "copies_min": 0,
   "copies_max": 0,
   "checks": 8
  },
  "17": {
   "k4": 0,
   "copies_min": 0,
   "copies_max": 0,
   "checks": 7
  },
  "18": {
   "k4": 0,
   "copies_min": 0,
   "copies_max": 0,
   "checks": 7
  },
  "19": {
   "k4": 0,
   "copies_min": 0,
   "copies_max": 0,
   "checks": 9
  },
  "20": {
   "k4": 0,
   "copies_min": 0,
   "copies_max": 0,
   "checks": 11
  },
  "21": {
   "k4": 0,
   "copies_min": 0,
   "copies_max": 0,
   "checks": 11
  },
  "22": {
   "k4": 0,
   "copies_min": 0,
   "copies_max": 0,
   "checks": 9
  },
  "23": {
   "k4": 0,
   "copies_min": 0,
   "copies_max": 0,
   "checks": 7
  },
  "24": {
   "k4": 0,
   "copies_min": 0,
   "copies_max": 1,
   "checks": 5
  },
  "25": {
   "k4": 0,
   "copies_min": 0,
   "copies_max": 18,
   "checks": 3
  },
  "26": {
   "k4": 617,
   "copies_min": 0,
   "copies_max": 734,
   "checks": 1
  }
 },
 "lengths_k4_above_every_copy": [],
 "k4_live_shortest": [
  {
   "phrase": "THEFLAMETOFLICKERBUTPRESEN",
   "from": "k3 @248",
   "strip": "kry",
   "form": "k-j",
   "lengths": [
    26
   ]
  },
  {
   "phrase": "HEFLAMETOFLICKERBUTPRESENT",
   "from": "k3 @249",
   "strip": "kry",
   "form": "k-j",
   "lengths": [
    26
   ]
  },
  {
   "phrase": "ORTHEPUBLICATIONOFTHISBOOK",
   "from": "Carter 1923 @1314",
   "strip": "std",
   "form": "k-j",
   "lengths": [
    26
   ]
  },
  {
   "phrase": "RTHEPUBLICATIONOFTHISBOOKW",
   "from": "Carter 1923 @1315",
   "strip": "std",
   "form": "k-j",
   "lengths": [
    26
   ]
  },
  {
   "phrase": "INMETRESKETCHPLANOFTHETOMB",
   "from": "Carter 1923 @3438",
   "strip": "std",
   "form": "j+k",
   "lengths": [
    26
   ]
  },
  {
   "phrase": "NIMPORTANTBECAUSEOFTHELACK",
   "from": "Carter 1923 @3519",
   "strip": "kry",
   "form": "j+k",
   "lengths": [
    26
   ]
  },
  {
   "phrase": "IMPORTANTBECAUSEOFTHELACKO",
   "from": "Carter 1923 @3520",
   "strip": "kry",
   "form": "j+k",
   "lengths": [
    26
   ]
  },
  {
   "phrase": "ORTANTBECAUSEOFTHELACKOFLI",
   "from": "Carter 1923 @3523",
   "strip": "kry",
   "form": "j+k",
   "lengths": [
    26
   ]
  },
  {
   "phrase": "RTANTBECAUSEOFTHELACKOFLIT",
   "from": "Carter 1923 @3524",
   "strip": "kry",
   "form": "j+k",
   "lengths": [
    26
   ]
  },
  {
   "phrase": "ANTBECAUSEOFTHELACKOFLITER",
   "from": "Carter 1923 @3526",
   "strip": "kry",
   "form": "j+k",
   "lengths": [
    26
   ]
  },
  {
   "phrase": "NTBECAUSEOFTHELACKOFLITERA",
   "from": "Carter 1923 @3527",
   "strip": "kry",
   "form": "j+k",
   "lengths": [
    26
   ]
  },
  {
   "phrase": "RESENTTHEACTUALTOMBOFTHEKI",
   "from": "Carter 1923 @3661",
   "strip": "std",
   "form": "k-j",
   "lengths": [
    26
   ]
  },
  {
   "phrase": "TILITARIANOBJECTSSUCHAWALK",
   "from": "Carter 1923 @8602",
   "strip": "kry",
   "form": "k-j",
   "lengths": [
    26
   ]
  },
  {
   "phrase": "ILITARIANOBJECTSSUCHAWALKI",
   "from": "Carter 1923 @8603",
   "strip": "kry",
   "form": "k-j",
   "lengths": [
    26
   ]
  },
  {
   "phrase": "LITARIANOBJECTSSUCHAWALKIN",
   "from": "Carter 1923 @8604",
   "strip": "kry",
   "form": "k-j",
   "lengths": [
    26
   ]
  }
 ],
 "plant": {
  "phrase": "THEFLAMETOFLICKERBUTPRESEN",
  "length": 7,
  "live": true
 },
 "copies": "20 shuffled copies (seed 1830)",
 "exhaustive": true
}
```

Notes: 1196 phrases; live cells K4 617 (copies 0-737); lengths where K4 is above every copy: []; plant live True


