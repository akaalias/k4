# 0192-friedman-keyed-alphabet-box: F11.4: Friedman's keyed alphabet box (MC III 35b): the alphabet written n times into a rectangle as wide as a keyword, read out in the keyword's column order as the key stream; every dictionary keyword: exact

**Family:** 11-agency-hand-systems  
**Parent:** 0191-cia-key-box-running-key  
**Decision:** reverted  
**Run:** 2026-10-17T00:53:43+00:00, 25.5 s, status ran  
**Time by phase:** design 0 s, implement 0 s, test 0 s, run 26 s, record 0 s

## In plain words

Friedman taught a way to make a long key from one word: write the alphabet several times into a grid as wide as the word, then copy the columns out in the word's alphabetical order. That jumbled alphabet is the key. Only the word and the number of repeats need remembering. We try every dictionary word.

## Walkthrough, by hand

1. Take the word BERLIN: its letters in alphabetical order number B1 E2 I3 L4 N5 R6... as columns.
2. Write ABCDEFGHIJKLMNOPQRSTUVWXYZ four times into rows of 6.
3. Copy out column 1 (under B), then column 2 (under E), and so on: that is the key.
4. Start it anywhere; on the sculpture's table, each known letter needs one key letter at its place.
5. One disagreement ends the setting. Every word, repeat count, start and table; then scrambled copies.

## Worked example (generated)

```
BERLIN, the alphabet four times in rows of 6, columns read in BERLIN's order: AGMSYEKQWCIOUAGMSYBHNTZFLRXDJPVBHNTZEKQWCIOUAGMSYEKQWDJPVBHNTZFLRXDJPVFLRXDJPVBHNTZFLRXCIOUAGMSYEKQWCIOU
```

## Lineage

Inherits from 0191-cia-key-box-running-key. What changed: F11.4. Friedman, Military Cryptanalytics III par. 35b (report reports/Scheidt patents and field ciphers.md, issue #9): a keyword's numerical order is used as a columnar key on a rectangle holding the normal alphabet repeated an agreed number of times; the column read becomes the key stream. Here: the standard or KRYPTOS alphabet repeated 1-8 times, every distinct column order of the dictionary and vocabulary words of 2-32 letters, the stream used cyclically from every start, 8 table rules (Vigenere, Beaufort, variant, Bury's reciprocal on standard or KRYPTOS numbering); each setting checks all 24 known letters (compiled). K4 against 10 shuffled copies; plants. A free table (the report's partition test) is not run.

## Hypothesis (domain expert)

A9, F11: a keyword-only key stream from Friedman's training texts, the kind of rule a CIA cryptographer of Scheidt's generation learned; 'a matrix, then the table' (C1). Model: stream s = columnar_read(alphabet^n, keyword order), k_i = s[(o + i) mod 26n], c = T(p, k). Statistic: fitting settings, K4 against copies.

## Prediction

No setting fits all 24 known letters on K4 or on the copies; plants are found. Zero candidates.

## Method

1. Every distinct column order from dictionary and vocabulary words of 2-32 letters.
2. For each order, alphabet (standard, KRYPTOS) and n = 1-8: the stream.
3. Every start and table rule: all 24 known letters must agree (compiled).
4. K4 against 10 shuffled copies; two plants.

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
 "family": "Friedman's keyed alphabet box (MC III 35b): alphabet (std/KRYPTOS) x n (1-8) by rows, read by keyword column order, every dictionary keyword, every start, 8 tables, exact",
 "column_orders": 163726,
 "settings_per_text": 2451960576,
 "fits": {
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
   0
  ],
  "plants": [
   62,
   26
  ]
 },
 "plants": [
  {
   "keyword": "MORPHOPLASM",
   "alphabet": "kry",
   "n": 4,
   "start": 96,
   "rule": "std/beau"
  },
  {
   "keyword": "FORSAKENNESS",
   "alphabet": "std",
   "n": 6,
   "start": 149,
   "rule": "kry/recip25"
  }
 ],
 "k4_hits": [],
 "copies": "10 shuffled copies (seed 1920)",
 "seconds": 25,
 "exhaustive": true
}
```

Notes: 163,726 column orders; fits K4 0 (copies 0-0); plants [62, 26]


