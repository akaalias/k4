# 0156-friedman-key-advance-schedules: F1.10: Friedman's keyword-only key-advance schedules (run length by letter value, the CHRISTMAS expansion, EXTINGUISHER windows; ciphertext and plaintext interruptors; fraction-digit runs) on the sculpture's tables, exact, with scrambled copies

**Family:** 1-keyed-periodic  
**Parent:** 0126-hand-key-schedules-listed-and-tested  
**Decision:** reverted  
**Run:** 2026-10-16T22:23:57+00:00, 38.7 s, status ran  
**Time by phase:** unattributed 27 s, run 39 s, record 0 s

## In plain words

A wartime US Army training text lists simple rules for when the secret word's next letter comes into use: each letter used for as many places as its position in the alphabet, the word expanded by a counting rule, the word restarted whenever a chosen letter appears, run lengths taken from the digits of a fraction, or overlapping three-letter windows of the word. Each needs only a word and a rule anyone can remember. We test every rule with every dictionary word (or with the word's letters left unknown) on the sculpture's tables, against the 24 known letters and against scrambled copies of the carved text.

## Walkthrough, by hand

1. Run length by value: with the word KEY, K (11th letter) is used for 11 places, E for 5, Y for 25, then K again.
2. Count along to place 22: which letter of the word is in use there, and at every other known place.
3. On the sculpture's table, the known letter and the carved letter at each place fix the key letter that must be in use.
4. The word fits only if it puts exactly those letters there, at all 24 places.
5. The other rules work the same way, with their own counting; for the interruptors and fractions the word's letters are left unknown and only need to agree with themselves.

## Worked example (generated)

```
word KRYPTOS: the key letter in use at each known place, by schedule

  runlen A=1       places 22-34: RRRRRRRRYYYYY   64-74: PPPPPPPTTTT
  runlen A=0       places 22-34: RRRRRRYYYYYYY   64-74: PPPTTTTTTTT
  christmas        places 22-34: RYPTKRYKKRYPT   64-74: KRYPKRKRYPT
  extinguisher 2   places 22-34: OSKRKRKRYPYPP   64-74: TOTOTOSOKRK
  extinguisher 3   places 22-34: KRRYPRYYPTOPT   64-74: PRYPRYPTPTO
  extinguisher 4   places 22-34: RYYPTOYPKRYPR   64-74: YPKRYRYPYPT
  extinguisher 5   places 22-34: YPKRYPTRYPTOK   64-74: PTORYYPTKRY

sculpture's table (KRYPTOS alphabets, Vigenere): the key letters the known letters force
  places 22-34: RDUMRIYWOYNKY   64-74: ELYOIECBAQK

CHRISTMAS expands to CHRISTMACCHCHRICHRISTMCHRCHRISCHRISTMASCHRIST (45 letters, as MC III §35c)
```

## Lineage

Inherits from 0126-hand-key-schedules-listed-and-tested. What changed: F1.10. The report on Scheidt's patents and field ciphers ran scratch checks without controls showing no dictionary word fits the run-length and CHRISTMAS schedules on the standard or KRYPTOS tables, and no ciphertext-interruptor setting fits; the fraction-digit runs and the plaintext interruptor were untested, and TM 32-220 par. 126d's EXTINGUISHER windows were found later. Here all six, as an experiment with ten scrambled copies. Word schedules (each dictionary word gives one key): run length = the key letter's value (A = 1; and A = 0 with zero-length runs skipped), the CHRISTMAS expansion (sections ending at the letters numbered 1, 2, 3, ...), EXTINGUISHER windows of 2-5 letters. Free-letter schedules (key letters unknown, the 24 known letters force them): ciphertext interruptor (the key restarts after each occurrence of a chosen carved letter), plaintext interruptor (restarts after a chosen message letter; testable only inside the two known runs, each run starting at an unknown key place), fraction digits (each key letter used for as many letters as the next digit of 1/d, d 3-99, zeros dropped). Tables: plain and cipher alphabets standard or KRYPTOS, Vigenere, Beaufort or variant, key letters numbered on either alphabet.

## Hypothesis (domain expert)

C5(a) ('simple, can be remembered... with the correct key word/s', Scheidt 2011 via Bean), C20 (hand schedules), F1.4's list extended. Sources: Friedman, Military Cryptanalysis III §16b, §19, §21, §35c-d; TM 32-220 pars. 125-126 (126b plaintext interruptor, 126d EXTINGUISHER windows, 126e fraction 1/7), 89e (zeros dropped); reports/Scheidt patents and field ciphers.md and research_notes/Scheidt patents and field ciphers/addendum_downloaded_manuals.md. Note from the report: adjacent known pairs 26-27 (N, O under Q), 33-34 (T, S under S), 68-69 (I, N under T) can never share an alphabet. Word list kryptos/data/words.txt (234,428 words; lengths 3-20 used). EXTINGUISHER: windows W[t:t+m] cycled within a group whose length is the next number of W's alphabetical numbering (ties left to right), windows and numbers each cycling. Exact; statistic fixed before the run: per schedule, K4's count (word hits, or consistent free settings with at least one check) against ten coppers' range.

## Prediction

No dictionary word fits any word schedule on K4 (as the report's scratch checks found), coppers 0 as well; the free-letter schedules fit K4 only at the coppers' rate, the plaintext interruptor most often (few checks inside the runs). Zero candidates.

## Method

1. For each word schedule and word: the key letter at each known place (positions 22-34, 64-74).
2. For each text, table and numbering: the forced key value at each known place; a word fits if its 24 values match exactly (hash lookup).
3. Free schedules: the slot of each known place per setting; a setting is consistent if no slot has two different forced values; count those with a check.
4. K4 against the coppers per schedule.

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
 "family": "Friedman key-advance schedules (MC III, TM 32-220) on the 12 standard/KRYPTOS tables x 2 key numberings",
 "words": 234143,
 "word_lengths": [
  3,
  20
 ],
 "summary": {
  "christmas": {
   "k4_word_hits": 0,
   "coppers_word_hits": [
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
  "extinguisher 2": {
   "k4_word_hits": 0,
   "coppers_word_hits": [
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
  "extinguisher 3": {
   "k4_word_hits": 0,
   "coppers_word_hits": [
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
  "extinguisher 4": {
   "k4_word_hits": 0,
   "coppers_word_hits": [
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
  "extinguisher 5": {
   "k4_word_hits": 0,
   "coppers_word_hits": [
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
  "runlen A=0": {
   "k4_word_hits": 0,
   "coppers_word_hits": [
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
  "runlen A=1": {
   "k4_word_hits": 0,
   "coppers_word_hits": [
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
  "ct interruptor": {
   "k4_consistent_with_check": 0,
   "coppers": [
    2,
    0,
    2,
    10,
    4,
    2,
    0,
    9,
    14,
    3
   ]
  },
  "fraction digits": {
   "k4_consistent_with_check": 0,
   "coppers": [
    0,
    0,
    0,
    8,
    8,
    0,
    0,
    4,
    8,
    4
   ]
  },
  "pt interruptor": {
   "k4_consistent_with_check": 160,
   "coppers": [
    220,
    130,
    1762,
    3074,
    2854,
    120,
    2994,
    7165,
    2999,
    1632
   ]
  }
 },
 "k4_word_hits": {},
 "free_settings": {
  "ct interruptor": "26 letters x key lengths 1-26",
  "fraction digits": "denominators 3-99 x key lengths 1-26, zeros dropped",
  "pt interruptor": "26 letters x key lengths 1-26 x start place of each known run"
 },
 "controls": "10 shuffled coppers (seed 1510), identical test",
 "exhaustive": true
}
```

Notes: christmas: K4 0 (coppers 0-0); extinguisher 2: K4 0 (coppers 0-0); extinguisher 3: K4 0 (coppers 0-0); extinguisher 4: K4 0 (coppers 0-0); extinguisher 5: K4 0 (coppers 0-0); runlen A=0: K4 0 (coppers 0-0); runlen A=1: K4 0 (coppers 0-0); ct interruptor: K4 0 (coppers 0-14); fraction digits: K4 0 (coppers 0-8); pt interruptor: K4 160 (coppers 120-7165)


