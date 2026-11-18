# 0283-f16.2-a-book-plus-a-keyword: F16.2: a passage of a named text under the message plus a short repeated word on top, on the plain and KRYPTOS tables, Vigenere and Beaufort with the text added or taken away, every offset and direction, word lengths 1-16, decided exactly on the 24 and on the 20 official known letters with up to two slips (lengths 1-12); K4 against 20 shuffles, plants

**Family:** 16-simple-hand-methods  
**Parent:** 0210-running-keys-with-slips-at-known-places  
**Decision:** reverted  
**Run:** 2026-11-18T10:16:02+00:00, 352.4 s, status ran  
**Time by phase:** unattributed 177 s, run 352 s, record 0 s

## In plain words

A book cipher with a twist: write a passage of a known text under the message, add it letter by letter on the table, then add a short word repeated over and over. Experiment 210 tried the passages alone; here we add the repeated word, every length up to 16, for every starting place in twenty-odd texts Sanborn might have used, allowing two slips, on the carving and on scrambled copies.

## Walkthrough, by hand

1. Write K4, and under it a passage of the Gettysburg Address from some letter on.
2. On the plain table, at each known place, find the key letter that turns the known letter into the carved one.
3. Subtract the Gettysburg letter under it: what is left is the repeated word's letter for that place.
4. Choose a word length, say 5, and group the known places by place mod
5. 5. Within each group the leftover letters must agree, except at most two slips overall.
6. If they do, read the word's letters off the groups and decrypt the rest of K4 with text plus word.
7. Repeat for every starting letter, both directions, every text, both tables, and on scrambled copies.

## Worked example (generated)

```
plain table, Vigenere: the forced key at each known place minus the Gettysburg letter under it, offset 0

place  known  carved  key  text  word letter
   26      N       Q    D     O            P
   27      O       Q    C     U            I
   28      R       P    Y     R            H
   64      B       N    M     T            T
   65      E       Y    U     A            U
   66      R       P    Y     N            L

For a word of length L the word letters at places equal mod L must agree (two slips allowed at L <= 12).
```

## Lineage

Inherits from 0210-running-keys-with-slips-at-known-places. What changed: F16.2 (issue #123). 0210 tested the named texts as a running key alone; 0117 and 0211 added a one-letter shift. Here the running key carries a repeated word of length 1-16 on top: the forced key at the known places, minus the text letter there, must repeat with the word's period. Texts: 0210's (K1-K3 plain and cipher, Carter vol. 1, the tableau by rows and columns, the Morse, the right panel, Sanborn's 1989 letter, the 1991 Cryptogram, the 2025 open letter) plus eleven new ones (Carter vols. 2-3, KJV Genesis and John, the Declaration, the Constitution, Gettysburg, Poe's Gold-Bug, Kennedy 1963 and Reagan 1987 in Berlin, the National Security Act 1947), forward and backward, every cyclic offset.

## Hypothesis (domain expert)

C7, C9 (earlier text as key or instructions), C5 (Scheidt: 'executed years later when used with the correct key word/s', 03-scheidt-said.md), C3 (Scheidt's split keys: a book and a word as two parts combined, Family C in 06-hypotheses.md); Sanborn's NYPVTT=BERLIN one-to-one (C-dinner 2011, 02-sanborn-said.md). Model: two additive stages on one table (standard or KRYPTOS alphabet on both sides, letters numbered in it): c = p + t_{o+i} + w_{i mod L} (Vigenere) or c = t_{o+i} + w_{i mod L} - p (Beaufort), with the text added or subtracted (s = +/-1; variant forms coincide with these because the word is free). At each known place the forced key K_q (c - p or c + p) minus s t_{o+q-1} must equal w at slot (q-1) mod L. Exact: per offset and slot, the slips needed are the places outside the slot's most common residue; a setting fits at k when they total k or less. Known letters: all 24, and the 20 official ones (EAST second-hand, #124). Chance per setting at length L with c covered slots and n known places: 26^-(n - c - k) times the choice of slips; on 24 letters at L <= 12 with 2 slips, about 10^-3 fits per run; on 20 letters fits by chance appear from about L = 10 and are compared with the shuffles.

## Prediction

On 24 letters no setting fits K4 or any shuffle at word lengths 1-12 with up to 2 slips, nor at 13-16 with none; plants found 6 of 6 (their setting fits and their shuffles have no fit at its length). On 20 letters fits appear from about length 10 on K4 and shuffles alike, counts inside the shuffles; their readings judged no better than the shuffles'. Zero candidates beyond K4's 20-letter fits, which fail at EAST if EAST holds.

## Method

1. Texts: letters only, forward and backward, cyclic.
2. For each table (standard, KRYPTOS), form (Vigenere, Beaufort) and sign of the text: the forced key at each known place, minus the text letter at every offset (a matrix offsets x places).
3. For each word length 1-16: per slot, places outside the slot's most common value are slips; keep settings with 2 or fewer at lengths 1-12, none at 13-16.
4. The same for 20 shuffles of K4 and for 6 planted messages and their own 5 shuffles.
5. Each fit's reading (the word fixed where the known places reach) to quadgrams; the best of each text and every reading above -5.0 to the judge, all in one call.

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
 "item": "F16.2",
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
  "open letter 2025 bwd": 2228,
  "carter-1927-tomb-of-tutankhamen-vol2 fwd": 351185,
  "carter-1927-tomb-of-tutankhamen-vol2 bwd": 351185,
  "carter-1933-tomb-of-tutankhamen-vol3 fwd": 261363,
  "carter-1933-tomb-of-tutankhamen-vol3 bwd": 261363,
  "kjv-genesis fwd": 151872,
  "kjv-genesis bwd": 151872,
  "kjv-john fwd": 75525,
  "kjv-john bwd": 75525,
  "declaration-of-independence-1776 fwd": 6534,
  "declaration-of-independence-1776 bwd": 6534,
  "us-constitution-1787 fwd": 22328,
  "us-constitution-1787 bwd": 22328,
  "gettysburg-address-1863 fwd": 1152,
  "gettysburg-address-1863 bwd": 1152,
  "poe-1843-the-gold-bug fwd": 70739,
  "poe-1843-the-gold-bug bwd": 70739,
  "kennedy-1963-ich-bin-ein-berliner fwd": 2824,
  "kennedy-1963-ich-bin-ein-berliner bwd": 2824,
  "reagan-1987-brandenburg-gate fwd": 12576,
  "reagan-1987-brandenburg-gate bwd": 12576,
  "national-security-act-1947 fwd": 42536,
  "national-security-act-1947 bwd": 42536
 },
 "source_letters_both_directions": 2598622,
 "tables": [
  "std",
  "kry"
 ],
 "forms": "Vigenere (c = p + s t + w) and Beaufort (c = s t + w - p), s = +1 or -1; variant forms coincide",
 "word_lengths": [
  1,
  16
 ],
 "slips": "0-2 at lengths 1-12, 0 at 13-16",
 "settings_per_text": 332623616,
 "known_sets": {
  "k24": "all 24",
  "k20": "the 20 official (26-34, 64-74)"
 },
 "summary": {
  "k24": {
   "per_length": {
    "1": {
     "k4": 0,
     "copies_median": 0.0,
     "copies_max": 0,
     "at_or_above": 20,
     "p": null
    },
    "2": {
     "k4": 0,
     "copies_median": 0.0,
     "copies_max": 0,
     "at_or_above": 20,
     "p": null
    },
    "3": {
     "k4": 0,
     "copies_median": 0.0,
     "copies_max": 0,
     "at_or_above": 20,
     "p": null
    },
    "4": {
     "k4": 0,
     "copies_median": 0.0,
     "copies_max": 0,
     "at_or_above": 20,
     "p": null
    },
    "5": {
     "k4": 0,
     "copies_median": 0.0,
     "copies_max": 0,
     "at_or_above": 20,
     "p": null
    },
    "6": {
     "k4": 0,
     "copies_median": 0.0,
     "copies_max": 0,
     "at_or_above": 20,
     "p": null
    },
    "7": {
     "k4": 0,
     "copies_median": 0.0,
     "copies_max": 0,
     "at_or_above": 20,
     "p": null
    },
    "8": {
     "k4": 0,
     "copies_median": 0.0,
     "copies_max": 0,
     "at_or_above": 20,
     "p": null
    },
    "9": {
     "k4": 0,
     "copies_median": 0.0,
     "copies_max": 0,
     "at_or_above": 20,
     "p": null
    },
    "10": {
     "k4": 0,
     "copies_median": 0.0,
     "copies_max": 0,
     "at_or_above": 20,
     "p": null
    },
    "11": {
     "k4": 0,
     "copies_median": 0.0,
     "copies_max": 0,
     "at_or_above": 20,
     "p": null
    },
    "12": {
     "k4": 0,
     "copies_median": 0.0,
     "copies_max": 0,
     "at_or_above": 20,
     "p": null
    },
    "13": {
     "k4": 0,
     "copies_median": 0.0,
     "copies_max": 0,
     "at_or_above": 20,
     "p": null
    },
    "14": {
     "k4": 0,
     "copies_median": 0.0,
     "copies_max": 0,
     "at_or_above": 20,
     "p": null
    },
    "15": {
     "k4": 0,
     "copies_median": 0.0,
     "copies_max": 0,
     "at_or_above": 20,
     "p": null
    },
    "16": {
     "k4": 0,
     "copies_median": 0.0,
     "copies_max": 0,
     "at_or_above": 20,
     "p": null
    }
   },
   "k4_total": 0,
   "copies_total": [
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
   ],
   "k4_judge_best": null,
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
   "k4_above_every_copy_at_judge": false,
   "k4_top": []
  },
  "k20": {
   "per_length": {
    "1": {
     "k4": 0,
     "copies_median": 0.0,
     "copies_max": 0,
     "at_or_above": 20,
     "p": null
    },
    "2": {
     "k4": 0,
     "copies_median": 0.0,
     "copies_max": 0,
     "at_or_above": 20,
     "p": null
    },
    "3": {
     "k4": 0,
     "copies_median": 0.0,
     "copies_max": 0,
     "at_or_above": 20,
     "p": null
    },
    "4": {
     "k4": 0,
     "copies_median": 0.0,
     "copies_max": 0,
     "at_or_above": 20,
     "p": null
    },
    "5": {
     "k4": 0,
     "copies_median": 0.0,
     "copies_max": 0,
     "at_or_above": 20,
     "p": null
    },
    "6": {
     "k4": 0,
     "copies_median": 0.0,
     "copies_max": 0,
     "at_or_above": 20,
     "p": null
    },
    "7": {
     "k4": 0,
     "copies_median": 0.0,
     "copies_max": 0,
     "at_or_above": 20,
     "p": null
    },
    "8": {
     "k4": 0,
     "copies_median": 0.0,
     "copies_max": 0,
     "at_or_above": 20,
     "p": null
    },
    "9": {
     "k4": 0,
     "copies_median": 0.0,
     "copies_max": 0,
     "at_or_above": 20,
     "p": null
    },
    "10": {
     "k4": 0,
     "copies_median": 0.0,
     "copies_max": 0,
     "at_or_above": 20,
     "p": null
    },
    "11": {
     "k4": 0,
     "copies_median": 0.0,
     "copies_max": 1,
     "at_or_above": 20,
     "p": null
    },
    "12": {
     "k4": 1,
     "copies_median": 1.0,
     "copies_max": 5,
     "at_or_above": 14,
     "p": 0.714
    },
    "13": {
     "k4": 0,
     "copies_median": 0.0,
     "copies_max": 0,
     "at_or_above": 20,
     "p": null
    },
    "14": {
     "k4": 0,
     "copies_median": 0.0,
     "copies_max": 0,
     "at_or_above": 20,
     "p": null
    },
    "15": {
     "k4": 0,
     "copies_median": 1.0,
     "copies_max": 3,
     "at_or_above": 20,
     "p": null
    },
    "16": {
     "k4": 34,
     "copies_median": 43.5,
     "copies_max": 73,
     "at_or_above": 17,
     "p": 0.857
    }
   },
   "k4_total": 35,
   "copies_total": [
    41,
    36,
    39,
    42,
    46,
    48,
    50,
    50,
    58,
    42,
    36,
    52,
    46,
    52,
    78,
    53,
    64,
    42,
    34,
    33
   ],
   "k4_judge_best": 3,
   "copies_judge_best": [
    3,
    3,
    3,
    3,
    3,
    4,
    4,
    3,
    3,
    4,
    3,
    3,
    3,
    4,
    4,
    4,
    4,
    3,
    3,
    2
   ],
   "k4_above_every_copy_at_judge": false,
   "k4_top": [
    {
     "fit": [
      "carter-1927-tomb-of-tutankhamen-vol2 fwd",
      329442,
      "std",
      "beau",
      -1,
      16,
      0
     ],
     "reading": "CMSWAILEINRVBUCOOIVSUCZJONORTHEASTEJREQNDPXOEULYVRNPXDEPJCACTCCBERLINCLOCKPILULXYIEIZCHKELITOOWIZ",
     "word": "KYKNHZKSFHPRKMDB",
     "quad": -7.226,
     "judge": 3
    },
    {
     "fit": [
      "carter-1927-tomb-of-tutankhamen-vol2 bwd",
      64005,
      "kry",
      "vig",
      -1,
      16,
      0
     ],
     "reading": "KPDSOFSAEBWMYJFQDTONFUDJRNORTHEASTGGGJUSINHLSMLOFKFZLKNCSTCOMIHBERLINCLOCKKCBMVUNOHMCHPTCJALYNISQ",
     "word": "VLCVUYPFSAPEFNZT",
     "quad": -7.295,
     "judge": 3
    },
    {
     "fit": [
      "poe-1843-the-gold-bug bwd",
      22426,
      "kry",
      "vig",
      -1,
      16,
      0
     ],
     "reading": "YEFIDMDBNGSIERNXWBTSTLNBANORTHEASTEMMIFIDHEWSVTRSDPTUXPARHHNNLZBERLINCLOCKFWTDWKOROBPMNMNIXHUUAQA",
     "word": "SBIJJSZXRFJGECGT",
     "quad": -7.47,
     "judge": 3
    },
    {
     "fit": [
      "carter-1933-tomb-of-tutankhamen-vol3 bwd",
      25424,
      "kry",
      "beau",
      1,
      16,
      0
     ],
     "reading": "UPCNEEPVIDRCHYDHJSZJFLUIYNORTHEASTBHDRWAFTCDVTHDTWSKTSBREWVROXABERLINCLOCKKKMAYRMZQADEUBBOSCGKENR",
     "word": "UPYCMFDDUUTIWZCQ",
     "quad": -7.514,
     "judge": null
    },
    {
     "fit": [
      "carter vol1 bwd",
      183759,
      "std",
      "beau",
      -1,
      16,
      0
     ],
     "reading": "GONYHMLCXTLCVIVRTNJGBAWLPNORTHEASTHIUXBLMKBSRYJORBRSJVFQENIENKLBERLINCLOCKEETUAEWCHMITKCSDXPWWKSE",
     "word": "VTOTXSZKRBFYOIQV",
     "quad": -7.625,
     "judge": null
    },
    {
     "fit": [
      "reagan-1987-brandenburg-gate bwd",
      7952,
      "kry",
      "vig",
      -1,
      16,
      0
     ],
     "reading": "SKRZFMWSTQHCCBONIVRSRZSZWNORTHEASTKCOAPXIKTTHUMSLDWVITIRLFKGQAOBERLINCLOCKTNQUYCJFRIRNJIEUPREGFGV",
     "word": "DCHSYXFGGOBGECBT",
     "quad": -7.658,
     "judge": null
    },
    {
     "fit": [
      "kjv-john fwd",
      29953,
      "kry",
      "vig",
      -1,
      16,
      0
     ],
     "reading": "EVZMRBLVVDWJCCAIQACRSLCUWNORTHEASTVIFMIHXINDMSIXAXHRIFIBHYUQYCZBERLINCLOCKDLLSILMTACRRYNUCQUMMADT",
     "word": "RJJNZJFGONLHTCJT",
     "quad": -7.774,
     "judge": null
    },
    {
     "fit": [
      "carter-1927-tomb-of-tutankhamen-vol2 fwd",
      168514,
      "std",
      "beau",
      1,
      16,
      0
     ],
     "reading": "YFEHMOTOVWAPPGFFCVQHQMFMTNORTHEASTMYBCLPJZCSUXWAPAGJCHSQKRSCUJLBERLINCLOCKTKFEYGEVIZEITOHBPHREGOJ",
     "word": "TSMKTKMAKDBWCHEW",
     "quad": -7.882,
     "judge": null
    },
    {
     "fit": [
      "carter-1933-tomb-of-tutankhamen-vol3 bwd",
      22770,
      "kry",
      "vig",
      1,
      16,
      0
     ],
     "reading": "CGHCUVNXBEHBEMPMTIEOJOYIWNORTHEASTSMMUYKVMYWBCFFLDVRCVGZISTQMUOBERLINCLOCKFVATUDJGZLBHEWTCRLDFWKP",
     "word": "OMQEYXTYNWKJMZXD",
     "quad": -8.006,
     "judge": null
    },
    {
     "fit": [
      "kjv-john bwd",
      54934,
      "std",
      "vig",
      1,
      16,
      0
     ],
     "reading": "OHNTZQZUQRCDDIKGALXBLDWGANORTHEASTOZRRBPQXINIZZNEDMXSGHHFBEDKVJBERLINCLOCKFCEGCTXFLCZEVTHALZESBHK",
     "word": "OGGTSYUDPMYRFGXM",
     "quad": -8.074,
     "judge": null
    }
   ]
  }
 },
 "plants": [
  {
   "seed": 16301,
   "known": "k24",
   "source": "gettysburg-address-1863 fwd",
   "L": 5,
   "k": 0,
   "slips": [],
   "planted_setting_fits": true,
   "reading_right_fraction": 1.0,
   "own_copies_fits_at_L": [
    0,
    0,
    0,
    0,
    0
   ],
   "found": true
  },
  {
   "seed": 16301,
   "known": "k20",
   "source": "gettysburg-address-1863 fwd",
   "L": 5,
   "k": 0,
   "slips": [],
   "planted_setting_fits": true,
   "reading_right_fraction": 1.0,
   "own_copies_fits_at_L": [
    0,
    0,
    0,
    0,
    0
   ],
   "found": true
  },
  {
   "seed": 16302,
   "known": "k24",
   "source": "K1+K2+K3 plain fwd",
   "L": 7,
   "k": 1,
   "slips": [
    74
   ],
   "planted_setting_fits": true,
   "reading_right_fraction": 0.9896907216494846,
   "own_copies_fits_at_L": [
    0,
    0,
    0,
    0,
    0
   ],
   "found": true
  },
  {
   "seed": 16302,
   "known": "k20",
   "source": "K1+K2+K3 plain fwd",
   "L": 7,
   "k": 1,
   "slips": [
    74
   ],
   "planted_setting_fits": true,
   "reading_right_fraction": 0.9896907216494846,
   "own_copies_fits_at_L": [
    0,
    0,
    0,
    0,
    0
   ],
   "found": true
  },
  {
   "seed": 16303,
   "known": "k24",
   "source": "carter vol1 bwd",
   "L": 11,
   "k": 2,
   "slips": [
    33,
    71
   ],
   "planted_setting_fits": true,
   "reading_right_fraction": 0.9072164948453608,
   "own_copies_fits_at_L": [
    0,
    0,
    0,
    0,
    0
   ],
   "found": true
  },
  {
   "seed": 16303,
   "known": "k20",
   "source": "carter vol1 bwd",
   "L": 11,
   "k": 2,
   "slips": [
    33,
    71
   ],
   "planted_setting_fits": true,
   "reading_right_fraction": 0.9072164948453608,
   "own_copies_fits_at_L": [
    0,
    0,
    0,
    0,
    0
   ],
   "found": true
  },
  {
   "seed": 16304,
   "known": "k24",
   "source": "reagan-1987-brandenburg-gate fwd",
   "L": 3,
   "k": 2,
   "slips": [
    33,
    66
   ],
   "planted_setting_fits": true,
   "reading_right_fraction": 0.979381443298969,
   "own_copies_fits_at_L": [
    0,
    0,
    0,
    0,
    0
   ],
   "found": true
  },
  {
   "seed": 16304,
   "known": "k20",
   "source": "reagan-1987-brandenburg-gate fwd",
   "L": 3,
   "k": 2,
   "slips": [
    33,
    66
   ],
   "planted_setting_fits": true,
   "reading_right_fraction": 0.979381443298969,
   "own_copies_fits_at_L": [
    0,
    0,
    0,
    0,
    0
   ],
   "found": true
  },
  {
   "seed": 16305,
   "known": "k24",
   "source": "kjv-genesis fwd",
   "L": 14,
   "k": 0,
   "slips": [],
   "planted_setting_fits": true,
   "reading_right_fraction": 1.0,
   "own_copies_fits_at_L": [
    0,
    0,
    0,
    0,
    0
   ],
   "found": true
  },
  {
   "seed": 16305,
   "known": "k20",
   "source": "kjv-genesis fwd",
   "L": 14,
   "k": 0,
   "slips": [],
   "planted_setting_fits": true,
   "reading_right_fraction": 1.0,
   "own_copies_fits_at_L": [
    0,
    0,
    0,
    0,
    0
   ],
   "found": true
  },
  {
   "seed": 16306,
   "known": "k24",
   "source": "poe-1843-the-gold-bug bwd",
   "L": 9,
   "k": 1,
   "slips": [
    69
   ],
   "planted_setting_fits": true,
   "reading_right_fraction": 0.9896907216494846,
   "own_copies_fits_at_L": [
    0,
    0,
    0,
    0,
    0
   ],
   "found": true
  },
  {
   "seed": 16306,
   "known": "k20",
   "source": "poe-1843-the-gold-bug bwd",
   "L": 9,
   "k": 1,
   "slips": [
    69
   ],
   "planted_setting_fits": true,
   "reading_right_fraction": 0.9896907216494846,
   "own_copies_fits_at_L": [
    0,
    0,
    0,
    0,
    0
   ],
   "found": true
  }
 ],
 "plants_found": {
  "k24": 6,
  "k20": 6
 },
 "judge": {
  "sent": 63,
  "none": 0,
  "cut": -5.0,
  "rule": "each text's top 3 by quadgrams and every reading at or above -5.0; plants not sent"
 },
 "controls": "20 shuffles of K4 (seeds 16300-16319); each plant against 5 shuffles of its own",
 "exhaustive": "yes: every cyclic offset of every source, both directions; fits capped at 20,000 per text and known set (reported)",
 "aws_cost_estimate_dollars": 1.0
}
```

Notes: k24: K4 fits 0 (copies 0-0), judge K4 None vs copies' best None; k20: K4 fits 35 (copies 33-78), judge K4 3 vs copies' best 4; plants found [(16301, 'k24', True), (16301, 'k20', True), (16302, 'k24', True), (16302, 'k20', True), (16303, 'k24', True), (16303, 'k20', True), (16304, 'k24', True), (16304, 'k20', True), (16305, 'k24', True), (16305, 'k20', True), (16306, 'k24', True), (16306, 'k20', True)]


