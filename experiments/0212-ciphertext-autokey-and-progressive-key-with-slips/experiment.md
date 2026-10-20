# 0212-ciphertext-autokey-and-progressive-key-with-slips: A1.4, part 1: ciphertext autokey on every keyword table tried so far, every lag, with up to two of the 24 known letters carved wrong or one skipped step in the chain; and the progressive key on the sculpture's tables with up to two slips; exact, judged against scrambled copies, with planted slipped messages

**Family:** 1-keyed-periodic  
**Parent:** 0064-ciphertext-autokey-k1-k3-word-alphabets  
**Decision:** reverted  
**Run:** 2026-10-20T13:21:34+00:00, 304.0 s, status ran  
**Time by phase:** implement 219 s, test 493 s, run 304 s, record 30 s

## In plain words

In an autokey cipher the key keeps growing out of the message itself: after a few starting letters, each new key letter is a letter already enciphered. Done by hand, one slip is easy: a wrong letter at one place, or losing your place in the chain and carrying on one letter off. Earlier experiments threw away any setting that missed even one known letter. Here we allow two wrong letters, or one lost place, on the carving and on scrambled copies, and we hide messages of our own made with such slips to check they are found. The same for the progressive key, whose key word shifts one step further along the table after every letter or every round.

## Walkthrough, by hand

1. Write K4 and, under each letter, the carved letter L places before it: that is the autokey's key.
2. At each of the 24 known places, look up on the table what the known letter and that key letter give.
3. Count the places where it is not the carved letter: up to 2 are allowed as slips.
4. For a lost place: from one known letter on, take the key from L + 1 (or L - 1) places back instead, and require every place to agree.
5. Read the message wherever the key is known, and do the same on scrambled copies of the carving.
6. For the progressive key, write the key word under the text, add d to every key letter's place on the table for every letter (or every round), and count the slips the same way.

## Worked example (generated)

```
ciphertext autokey, lag 9, KRYPTOS table, Vigenere: the key for each known place is the carved letter 9 before it

place  known  key(carved L back)  gives  carved
   22      E                   B      N       F   x
   23      A                   S      G       L   x
   24      S                   O      E       R   x
   25      T                   L      U       V   x
   64      B                   U      P       N   x
   65      E                   D      U       Y   x
   66      R                   I      J       P   x

failed checks: 24 of 24 (2 allowed as slips)
```

## Lineage

Inherits from 0064-ciphertext-autokey-k1-k3-word-alphabets. What changed: A1.4 (Stage 2, step 2, issue #76), first part. 0002, 0025, 0064, 0071 and 0072 required every known letter past the primer to agree with ciphertext autokey (0064's fewest was 3 mismatches on K4, 2-3 on copies); 0011 required all 24 for the progressive key. Here: (a) ciphertext autokey on the union of their tables (about 550,000 table setups), every lag 1-96, with up to 2 failed checks (a slip at a known place stays put: the next key letter is the letter he carved); (b) one skipped or repeated step in the autokey chain (from some known place on the lag is one more or one less), at every place, as its own setting; (c) the progressive key (0011) on the 8 table classes, periods 1-52, steps 1-25, both forms, up to 2 slips. Compiled for (a) and (b). Readings of settings that keep at least 3 checks go to quadgrams and the blind judge with the copies'. Plants for each part in the same run.

## Hypothesis (domain expert)

A1 (knowledge/12-assumptions.md); C11a (NSA 1992: 'plain-text auto-key'; the NSA analyst 2007 tested both autokeys), C5(a) (a key word and a hand schedule), C27(a) (Sanborn's PALIMPCEST slip), Sanborn 2005 'Saying I was sloppy is a good way of saying it'. Ciphertext autokey: c_i = C[E(P(p_i), K(c_{i-L}))], P, C, K alphabets from 0025's 63 (standard, KRYPTOS, vocabulary keyword), 0064's K1-K3 and C13/C14 words, 0072's compass words (pairs of any two; key alphabet standard, KRYPTOS, plain or cipher), and 0071's 925 near-KRYPTOS alphabets (with themselves or the standard alphabet); Vigenere, Beaufort, variant. Every known place q > L is a check; a slip at a known place fails only its own check, because the following key letters are the carved ones. A skipped step: the key for every known place from the e-th on is the carved letter L + 1 (or L - 1) back. Progressive key: key value at place i = w[i mod P] + d i (per letter) or + d floor(i / P) (per repeat), 8 table classes (the key alphabet drops out; variant Beaufort is a negated step). Counted: settings with 0, 1, 2 failed checks per lag (per period and step), K4 against 20 copies. Slip cost: 9.3 bits for 1, 17.5 for 2; a skipped step about log2(24 x 2) = 5.6 bits. Where 2 or fewer checks would remain the known letters decide nothing and the cell is counted only.

## Prediction

Ciphertext autokey: at lags with 8 or more checks no setting with 2 slips or one skipped step on K4, at the copies' rate elsewhere; nothing judged above every copy. Progressive key: nothing below period 24 with 2 slips (as 0207 for the plain periodic key). All plants found. Zero candidates pass gate 4.

## Method

1. Build the tables.
2. For each table setup and text: the key index each known place needs.
3. For each lag: compare with the key letter the carved text offers L back, count failures, keep up to 2; for each skipped step (lag L before the e-th known place, L + 1 or L - 1 from it), keep only exact fits.
4. Progressive key: per class, period, step and form, the forced base values per slot; enumerate settings with up to 2 slips.
5. Count by lag and slips, K4 against 20 copies.
6. Readings of settings keeping 3 or more checks: each text's best by quadgrams and every one at or above -5.0 go to the judge, all texts in one call.
7. Plants and their own copies through the same search.

## Result

Candidates returned: 10. Passed all gates: 0. Best crib hits among all candidates: 24/24
(EAST 4/4, NORTHEAST 9/9, BERLIN 6/6, CLOCK 5/5).
Best loss: 25.587429118904236 (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | baseline | 24/24 | -21.436 | `AAAAAAAAAAAAAAAAAAAAAEASTNORTHEASTAAAAAAAAAAAAAAAAAAAAAAAAAAAAABERLINCLOCKHROPCPRIVOTNOUGOBBVCTOC` | ciphertext autokey lag 69, LAYER/keyword|AND/keyword|std|varbeau, 2 slips at known places, skip None; free letters filled with A |
| 2 | baseline | 24/24 | -21.224 | `AAAAAAAAAAAAAAAAAAAAAEASTNORTHEASTAAAAAAAAAAAAAAAAAAAAAAAAAAAAABERLINCLOCKHROPCPRIWOTNOUGOCBTCUPC` | ciphertext autokey lag 69, LAYER/keyword|MADE/keyword|std|varbeau, 2 slips at known places, skip None; free letters filled with A |
| 3 | baseline | 24/24 | -21.005 | `AAAAAAAAAAAAAAAAAAAAAEASTNORTHEASTAAAAAAAAAAAAAAAAAAAAAAAAAAAAABERLINCLOCKGJFRWMJVCTURRFLIEVETSAM` | ciphertext autokey lag 71, BURIED/keyword|FIFTY/keyword|plain|varbeau, 0 slips at known places, skip (72, 72); free letters filled with A |
| 4 | baseline | 24/24 | -22.832 | `AAAAAAAAAAAAAAAAAAAAAEASTNORTHEASTAAAAAAAAAAAAAAAAAAAAAAAAAAAAABERLINCLOCKOQISSEYHKSOCKPDESPDPCWD` | ciphertext autokey lag 70, ESCAPING/keyword|LIGHT/keyword|cipher|varbeau, 1 slips at known places, skip None; free letters filled with A |
| 5 | baseline | 24/24 | -22.835 | `AAAAAAAAAAAAAAAAAAAAAEASTNORTHEASTAAAAAAAAAAAAAAAAAAAAAAAAAAAAABERLINCLOCKLDTSDUGHOTPPOFUVNTULGDK` | ciphertext autokey lag 69, SOUTHBYWEST|OFFSET|kry|vig, 2 slips at known places, skip None; free letters filled with A |
| 6 | baseline | 24/24 | -22.835 | `AAAAAAAAAAAAAAAAAAAAAEASTNORTHEASTAAAAAAAAAAAAAAAAAAAAAAAAAAAAABERLINCLOCKLDTSDUGHOTPPOFUVNTULGDK` | ciphertext autokey lag 69, SOUTHWESTBYSOUTH|OFFSET|kry|vig, 2 slips at known places, skip None; free letters filled with A |
| 7 | baseline | 24/24 | -23.053 | `AAAAAAAAAAAAAAAAAAAAAEASTNORTHEASTAAAAAAAAAAAAAAAAAAAAAAAAAAAAABERLINCLOCKGABAWKSTAUSIAGTSCWZRTWL` | ciphertext autokey lag 71, ABSENCE/keyword|FIVE/keyword|plain|varbeau, 0 slips at known places, skip (72, 72); free letters filled with A |
| 8 | baseline | 24/24 | -22.306 | `AAAAAAAAAAAAAAAAAAAAAEASTNORTHEASTAAAAAAAAAAAAAAAAAAAAAAAAAAAAABERLINCLOCKVHAMUDGSSEIEYPNGNXLYCHO` | ciphertext autokey lag 70, INTERPRETATION/keyword|TREMBLING/keyword|kry|vig, 0 slips at known places, skip (22, 71); free letters filled with A |
| 9 | baseline | 24/24 | -22.306 | `AAAAAAAAAAAAAAAAAAAAAEASTNORTHEASTAAAAAAAAAAAAAAAAAAAAAAAAAAAAABERLINCLOCKVHAMUDGSSEIEYPNGNXLYCHO` | ciphertext autokey lag 70, INTERPRETATION/keyword|TREMBLING/keyword|kry|vig, 0 slips at known places, skip (23, 71); free letters filled with A |
| 10 | baseline | 24/24 | -22.306 | `AAAAAAAAAAAAAAAAAAAAAEASTNORTHEASTAAAAAAAAAAAAAAAAAAAAAAAAAAAAABERLINCLOCKVHAMUDGSSEIEYPNGNXLYCHO` | ciphertext autokey lag 70, INTERPRETATION/keyword|TREMBLING/keyword|kry|vig, 0 slips at known places, skip (24, 71); free letters filled with A |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "ciphertext autokey (union of 0025/0064/0071/0072 tables) and progressive key (0011), 0-2 known letters slipped, or one skipped step (A1.4)",
 "ca_table_setups": 487734,
 "ca_lags": "1-96",
 "skip": "lag L before the e-th known place, L+1 or L-1 from it, e = 2-24, exact fit",
 "prog": "8 table classes, periods 1-52, steps 1-25, per letter and per repeat",
 "slips": "0-2 at known places",
 "readings_judged_when_checks_left": ">= 3",
 "ca_by_lag": {
  "1": {
   "checks": 24,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "2": {
   "checks": 24,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "3": {
   "checks": 24,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "4": {
   "checks": 24,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "5": {
   "checks": 24,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "6": {
   "checks": 24,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "7": {
   "checks": 24,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "8": {
   "checks": 24,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "9": {
   "checks": 24,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "10": {
   "checks": 24,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "11": {
   "checks": 24,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "12": {
   "checks": 24,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "13": {
   "checks": 24,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "14": {
   "checks": 24,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "15": {
   "checks": 24,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "16": {
   "checks": 24,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "17": {
   "checks": 24,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "18": {
   "checks": 24,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "19": {
   "checks": 24,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "20": {
   "checks": 24,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "21": {
   "checks": 24,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "22": {
   "checks": 23,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "23": {
   "checks": 22,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "24": {
   "checks": 21,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "25": {
   "checks": 20,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "26": {
   "checks": 19,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "27": {
   "checks": 18,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "28": {
   "checks": 17,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "29": {
   "checks": 16,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "30": {
   "checks": 15,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "31": {
   "checks": 14,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "32": {
   "checks": 13,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "33": {
   "checks": 12,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "34": {
   "checks": 11,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "35": {
   "checks": 11,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "36": {
   "checks": 11,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "37": {
   "checks": 11,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "38": {
   "checks": 11,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "39": {
   "checks": 11,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "40": {
   "checks": 11,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "41": {
   "checks": 11,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "42": {
   "checks": 11,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "43": {
   "checks": 11,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "44": {
   "checks": 11,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "45": {
   "checks": 11,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "46": {
   "checks": 11,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "47": {
   "checks": 11,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "48": {
   "checks": 11,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "49": {
   "checks": 11,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "50": {
   "checks": 11,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "51": {
   "checks": 11,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "52": {
   "checks": 11,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "53": {
   "checks": 11,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "54": {
   "checks": 11,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "55": {
   "checks": 11,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "56": {
   "checks": 11,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "57": {
   "checks": 11,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "58": {
   "checks": 11,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "59": {
   "checks": 11,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "60": {
   "checks": 11,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "61": {
   "checks": 11,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "62": {
   "checks": 11,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "63": {
   "checks": 11,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "64": {
   "checks": 10,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "65": {
   "checks": 9,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "66": {
   "checks": 8,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "67": {
   "checks": 7,
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    2
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "68": {
   "checks": 6,
   "k4": [
    0,
    0,
    3
   ],
   "copies_max": [
    0,
    4,
    85
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "69": {
   "checks": 5,
   "k4": [
    0,
    0,
    146
   ],
   "copies_max": [
    0,
    15,
    608
   ],
   "copies_min": [
    0,
    0,
    49
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    475,
    4
   ]
  },
  "70": {
   "checks": 4,
   "k4": [
    0,
    184,
    5264
   ],
   "copies_max": [
    25,
    458,
    8336
   ],
   "copies_min": [
    0,
    3,
    1427
   ],
   "skip_k4": [
    600,
    1
   ],
   "skip_copies_max": [
    4180,
    12
   ]
  },
  "71": {
   "checks": 3,
   "k4": [
    30,
    1954,
    55341
   ],
   "copies_max": [
    209,
    4628,
    74925
   ],
   "copies_min": [
    0,
    732,
    35290
   ],
   "skip_k4": [
    15550,
    103
   ],
   "skip_copies_max": [
    39711,
    802
   ]
  },
  "72": {
   "checks": 2,
   "k4": [
    739,
    39263,
    447732
   ],
   "copies_max": [
    1884,
    54692,
    467272
   ],
   "copies_min": [
    94,
    20368,
    431158
   ],
   "skip_k4": [
    341016,
    1851
   ],
   "skip_copies_max": [
    876911,
    6896
   ]
  },
  "73": {
   "checks": 1,
   "k4": [
    15495,
    472239,
    0
   ],
   "copies_max": [
    39730,
    482288,
    0
   ],
   "copies_min": [
    5446,
    448004,
    0
   ],
   "skip_k4": [
    0,
    39016
   ],
   "skip_copies_max": [
    0,
    78711
   ]
  },
  "74": {
   "checks": 0,
   "k4": [
    487734,
    0,
    0
   ],
   "copies_max": [
    487734,
    0,
    0
   ],
   "copies_min": [
    487734,
    0,
    0
   ],
   "skip_k4": [
    0,
    356385
   ],
   "skip_copies_max": [
    0,
    913790
   ]
  },
  "75": {
   "checks": 0,
   "k4": [
    487734,
    0,
    0
   ],
   "copies_max": [
    487734,
    0,
    0
   ],
   "copies_min": [
    487734,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "76": {
   "checks": 0,
   "k4": [
    487734,
    0,
    0
   ],
   "copies_max": [
    487734,
    0,
    0
   ],
   "copies_min": [
    487734,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "77": {
   "checks": 0,
   "k4": [
    487734,
    0,
    0
   ],
   "copies_max": [
    487734,
    0,
    0
   ],
   "copies_min": [
    487734,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "78": {
   "checks": 0,
   "k4": [
    487734,
    0,
    0
   ],
   "copies_max": [
    487734,
    0,
    0
   ],
   "copies_min": [
    487734,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "79": {
   "checks": 0,
   "k4": [
    487734,
    0,
    0
   ],
   "copies_max": [
    487734,
    0,
    0
   ],
   "copies_min": [
    487734,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "80": {
   "checks": 0,
   "k4": [
    487734,
    0,
    0
   ],
   "copies_max": [
    487734,
    0,
    0
   ],
   "copies_min": [
    487734,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "81": {
   "checks": 0,
   "k4": [
    487734,
    0,
    0
   ],
   "copies_max": [
    487734,
    0,
    0
   ],
   "copies_min": [
    487734,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "82": {
   "checks": 0,
   "k4": [
    487734,
    0,
    0
   ],
   "copies_max": [
    487734,
    0,
    0
   ],
   "copies_min": [
    487734,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "83": {
   "checks": 0,
   "k4": [
    487734,
    0,
    0
   ],
   "copies_max": [
    487734,
    0,
    0
   ],
   "copies_min": [
    487734,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "84": {
   "checks": 0,
   "k4": [
    487734,
    0,
    0
   ],
   "copies_max": [
    487734,
    0,
    0
   ],
   "copies_min": [
    487734,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "85": {
   "checks": 0,
   "k4": [
    487734,
    0,
    0
   ],
   "copies_max": [
    487734,
    0,
    0
   ],
   "copies_min": [
    487734,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "86": {
   "checks": 0,
   "k4": [
    487734,
    0,
    0
   ],
   "copies_max": [
    487734,
    0,
    0
   ],
   "copies_min": [
    487734,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "87": {
   "checks": 0,
   "k4": [
    487734,
    0,
    0
   ],
   "copies_max": [
    487734,
    0,
    0
   ],
   "copies_min": [
    487734,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "88": {
   "checks": 0,
   "k4": [
    487734,
    0,
    0
   ],
   "copies_max": [
    487734,
    0,
    0
   ],
   "copies_min": [
    487734,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "89": {
   "checks": 0,
   "k4": [
    487734,
    0,
    0
   ],
   "copies_max": [
    487734,
    0,
    0
   ],
   "copies_min": [
    487734,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "90": {
   "checks": 0,
   "k4": [
    487734,
    0,
    0
   ],
   "copies_max": [
    487734,
    0,
    0
   ],
   "copies_min": [
    487734,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "91": {
   "checks": 0,
   "k4": [
    487734,
    0,
    0
   ],
   "copies_max": [
    487734,
    0,
    0
   ],
   "copies_min": [
    487734,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "92": {
   "checks": 0,
   "k4": [
    487734,
    0,
    0
   ],
   "copies_max": [
    487734,
    0,
    0
   ],
   "copies_min": [
    487734,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "93": {
   "checks": 0,
   "k4": [
    487734,
    0,
    0
   ],
   "copies_max": [
    487734,
    0,
    0
   ],
   "copies_min": [
    487734,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "94": {
   "checks": 0,
   "k4": [
    487734,
    0,
    0
   ],
   "copies_max": [
    487734,
    0,
    0
   ],
   "copies_min": [
    487734,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "95": {
   "checks": 0,
   "k4": [
    487734,
    0,
    0
   ],
   "copies_max": [
    487734,
    0,
    0
   ],
   "copies_min": [
    487734,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "96": {
   "checks": 0,
   "k4": [
    487734,
    0,
    0
   ],
   "copies_max": [
    487734,
    0,
    0
   ],
   "copies_min": [
    487734,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  }
 },
 "ca_k4_above_every_copy_lags": [],
 "ca_copies_above_rest": [
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  2,
  0,
  0,
  0,
  0,
  0,
  0,
  1,
  0,
  0,
  1,
  0
 ],
 "ca_shortest_lag_fitting": {
  "K4": 68,
  "copy1": 68,
  "copy2": 67,
  "copy3": 68,
  "copy4": 67,
  "copy5": 68,
  "copy6": 67,
  "copy7": 67,
  "copy8": 67,
  "copy9": 68,
  "copy10": 67,
  "copy11": 68,
  "copy12": 67,
  "copy13": 68,
  "copy14": 68,
  "copy15": 69,
  "copy16": 67,
  "copy17": 67,
  "copy18": 67,
  "copy19": 68,
  "copy20": 68
 },
 "skip_shortest_lag_fitting": {
  "K4": 70,
  "copy1": 69,
  "copy2": 70,
  "copy3": 70,
  "copy4": 69,
  "copy5": 70,
  "copy6": 69,
  "copy7": 69,
  "copy8": 70,
  "copy9": 69,
  "copy10": 70,
  "copy11": 70,
  "copy12": 69,
  "copy13": 70,
  "copy14": 69,
  "copy15": 69,
  "copy16": 70,
  "copy17": 69,
  "copy18": 69,
  "copy19": 69,
  "copy20": 69
 },
 "prog_shortest_period": {
  "K4": {
   "per-letter": 25,
   "per-repeat": 25
  },
  "copy1": {
   "per-letter": 25,
   "per-repeat": 25
  },
  "copy2": {
   "per-letter": 25,
   "per-repeat": 25
  },
  "copy3": {
   "per-letter": 25,
   "per-repeat": 25
  },
  "copy4": {
   "per-letter": 24,
   "per-repeat": 24
  },
  "copy5": {
   "per-letter": 25,
   "per-repeat": 25
  },
  "copy6": {
   "per-letter": 25,
   "per-repeat": 25
  },
  "copy7": {
   "per-letter": 25,
   "per-repeat": 25
  },
  "copy8": {
   "per-letter": 25,
   "per-repeat": 25
  },
  "copy9": {
   "per-letter": 25,
   "per-repeat": 25
  },
  "copy10": {
   "per-letter": 25,
   "per-repeat": 25
  },
  "copy11": {
   "per-letter": 25,
   "per-repeat": 25
  },
  "copy12": {
   "per-letter": 25,
   "per-repeat": 25
  },
  "copy13": {
   "per-letter": 24,
   "per-repeat": 24
  },
  "copy14": {
   "per-letter": 25,
   "per-repeat": 25
  },
  "copy15": {
   "per-letter": 25,
   "per-repeat": 25
  },
  "copy16": {
   "per-letter": 25,
   "per-repeat": 25
  },
  "copy17": {
   "per-letter": 25,
   "per-repeat": 25
  },
  "copy18": {
   "per-letter": 25,
   "per-repeat": 25
  },
  "copy19": {
   "per-letter": 25,
   "per-repeat": 25
  },
  "copy20": {
   "per-letter": 25,
   "per-repeat": 25
  }
 },
 "prog_k4_counts": {
  "per-letter|25": [
   0,
   0,
   128
  ],
  "per-letter|26": [
   0,
   400,
   0
  ],
  "per-letter|27": [
   200,
   0,
   0
  ],
  "per-letter|28": [
   200,
   0,
   0
  ],
  "per-letter|29": [
   200,
   0,
   0
  ],
  "per-letter|30": [
   0,
   400,
   0
  ],
  "per-letter|31": [
   0,
   32,
   736
  ],
  "per-letter|32": [
   0,
   4,
   104
  ],
  "per-letter|33": [
   0,
   2,
   16
  ],
  "per-letter|49": [
   0,
   0,
   8
  ],
  "per-letter|50": [
   0,
   0,
   128
  ],
  "per-letter|51": [
   0,
   32,
   736
  ],
  "per-letter|52": [
   0,
   400,
   0
  ],
  "per-repeat|25": [
   0,
   0,
   128
  ],
  "per-repeat|26": [
   8,
   384,
   0
  ],
  "per-repeat|27": [
   200,
   0,
   0
  ],
  "per-repeat|28": [
   200,
   0,
   0
  ],
  "per-repeat|29": [
   200,
   0,
   0
  ],
  "per-repeat|30": [
   8,
   384,
   0
  ],
  "per-repeat|31": [
   0,
   32,
   736
  ],
  "per-repeat|32": [
   0,
   2,
   80
  ],
  "per-repeat|33": [
   0,
   2,
   16
  ],
  "per-repeat|49": [
   0,
   0,
   8
  ],
  "per-repeat|50": [
   0,
   0,
   96
  ],
  "per-repeat|51": [
   0,
   32,
   736
  ],
  "per-repeat|52": [
   8,
   384,
   0
  ]
 },
 "capped_texts": [],
 "readings": {
  "k4": 1732,
  "copies": [
   1325,
   451,
   554,
   866,
   853,
   2365,
   1369,
   4513,
   2752,
   845,
   709,
   445,
   1064,
   8482,
   1246,
   5064,
   655,
   9427,
   5066,
   5761
  ]
 },
 "judge": {
  "sent": 56,
  "none": 0,
  "cut": -5.0
 },
 "k4_judge_best": 4,
 "copies_judge_best": [
  4,
  4,
  8,
  4,
  8,
  12,
  8,
  3,
  4,
  6,
  4,
  4,
  8,
  8,
  4,
  8,
  8,
  4,
  8,
  4
 ],
 "k4_readings_above_every_copy": 0,
 "k4_top": [
  {
   "reading": "?????????????????????????????????????????????????????????????????????ALOCBHROPCPRIVOTNOUGOBBVCTOC",
   "judge": 4,
   "quad": -6.362,
   "setting": [
    "LAYER/keyword|AND/keyword|std|varbeau",
    [
     69,
     2,
     -1,
     -1
    ]
   ]
  },
  {
   "reading": "?????????????????????????????????????????????????????????????????????CCFCKSRLWIXSSQLDCVHUCFRNLOQY",
   "judge": null,
   "quad": -7.821,
   "setting": [
    "std|std|std|beau",
    [
     69,
     2,
     -1,
     -1
    ]
   ]
  },
  {
   "reading": "?????????????????????????????????????????????????????????????????????CCECKSQKWIXSSSKKBVHTCDRMLQOY",
   "judge": null,
   "quad": -8.611,
   "setting": [
    "std|CIA/keyword|std|beau",
    [
     69,
     2,
     -1,
     -1
    ]
   ]
  },
  {
   "reading": "?????????????????????????????????????????????????????????????????????CEECKSQKXJXSUSKKUWJVCERMLQOY",
   "judge": null,
   "quad": -8.754,
   "setting": [
    "std|CIA/keyword|cipher|beau",
    [
     69,
     2,
     -1,
     -1
    ]
   ]
  },
  {
   "reading": "?????????????????????????????????????????????????????????????????????CGLCKTPIXKYSVNILTPKWBWRPRLNY",
   "judge": null,
   "quad": -8.048,
   "setting": [
    "std|FIVE/keyword|cipher|beau",
    [
     69,
     2,
     -1,
     -1
    ]
   ]
  }
 ],
 "plants": [
  {
   "kind": "ca",
   "seed": 2121,
   "params": {
    "m": "vig",
    "L": 9
   },
   "k": 2,
   "skip": null,
   "slips": [
    65,
    73
   ],
   "planted_setting_found": true,
   "quad": -4.255,
   "judge": 93,
   "own_copies_judge_best": [
    6,
    6,
    4,
    6,
    8
   ],
   "found": true
  },
  {
   "kind": "ca",
   "seed": 2122,
   "params": {
    "m": "beau",
    "L": 60
   },
   "k": 2,
   "skip": null,
   "slips": [
    68,
    73
   ],
   "planted_setting_found": true,
   "quad": -4.705,
   "judge": 62,
   "own_copies_judge_best": [
    6,
    4,
    5,
    3,
    7
   ],
   "found": true
  },
  {
   "kind": "ca",
   "seed": 2123,
   "params": {
    "m": "vig",
    "L": 15
   },
   "k": 0,
   "skip": [
    63,
    16
   ],
   "slips": [],
   "planted_setting_found": true,
   "quad": -4.391,
   "judge": 60,
   "own_copies_judge_best": [
    8,
    4,
    6,
    8,
    4
   ],
   "found": true
  },
  {
   "kind": "prog",
   "seed": 2124,
   "params": {
    "P": 11,
    "d": 3,
    "form": "per-letter",
    "cls": [
     "kry",
     "kry",
     "vig"
    ]
   },
   "k": 2,
   "skip": null,
   "slips": [
    26,
    34
   ],
   "planted_setting_found": true,
   "quad": -5.299,
   "judge": 85,
   "own_copies_judge_best": [
    3,
    8,
    4,
    12,
    5
   ],
   "found": true
  },
  {
   "kind": "prog",
   "seed": 2125,
   "params": {
    "P": 20,
    "d": 5,
    "form": "per-repeat",
    "cls": [
     "std",
     "kry",
     "beau"
    ]
   },
   "k": 2,
   "skip": null,
   "slips": [
    26,
    71
   ],
   "planted_setting_found": true,
   "quad": -4.291,
   "judge": 82,
   "own_copies_judge_best": [
    3,
    6,
    8,
    6,
    6
   ],
   "found": true
  }
 ],
 "slip_cost_bits": {
  "1": 9.3,
  "2": 17.5,
  "skip": 5.6
 },
 "controls": "20 shuffled copies (seeds 2130-2149); each plant against 5 shuffles of its own ciphertext",
 "exhaustive": "yes"
}
```

Notes: 487,734 autokey table setups; K4 shortest fitting lag with <= 2 slips 68, copies [67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 68, 68, 68, 68, 68, 68, 68, 68, 68, 69]; judge sent 56, K4 best 4, copies best 12; plants found [True, True, True, True, True]


