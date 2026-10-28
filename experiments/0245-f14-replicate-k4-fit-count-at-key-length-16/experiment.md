# 0245-f14-replicate-k4-fit-count-at-key-length-16: F14.1 replication: K4's 5 fitting dictionary alphabet pairs at key length 16 (added form) against 1,000 fresh shuffles, counted as pairs and as distinct cipher alphabets

**Family:** 14-scheidt-mask-keyed-by-words  
**Parent:** 0244-f14-two-dictionary-keyword-alphabets-and-a-key-word  
**Decision:** reverted  
**Run:** 2026-10-28T03:43:32+00:00, 196.5 s, status ran  
**Time by phase:** unattributed 58 s, run 196 s, record 0 s

## In plain words

In the last test K4 had slightly more matching alphabet pairs at one key length than any of 50 shuffled copies. That happens by luck now and then when many lengths are looked at, so we count again on 1,000 new shuffles to see how unusual it really is.

## Walkthrough, by hand

1. Take K4 and shuffle its letters, 1,000 times.
2. For each, file every cipher alphabet by the gaps that key length 16 asks for, and look up every plain alphabet.
3. Count the matching pairs, and the different cipher alphabets among them.
4. See how many shuffles reach K4's counts.

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

Inherits from 0244-f14-two-dictionary-keyword-alphabets-and-a-key-word. What changed: Replication only (program.md: a result outside the copies' range is replicated against fresh controls before anything else). 0244's search unchanged, run at key length 16 alone, both forms, on K4 and 1,000 fresh shuffles (seed 245). In 0244 K4 had 5 fitting pairs at 16/added, the 50 copies at most 4; the 5 share two cipher alphabets (AEOLOTROPISM four times), so the count is also taken as distinct cipher alphabets.

## Hypothesis (domain expert)

F14.1 (0244): two dictionary keyword alphabets with a free periodic key, exact. One of 52 (length, form) cells had K4 above all 50 copies in its fit count (5 against 4), with readings below the copies' best by English (-7.91 against -7.63). Pre-registered: the cell flags only if K4's count is reached by fewer than 5% of 1,000 fresh shuffles after the 52-cell correction, p < 0.05/52 = 0.00096, on either count.

## Prediction

Several percent of fresh shuffles reach 5 or more pairs at 16/added: p well above 0.001, not a flag.

## Method

1. 0244's index search at key length 16, both forms, no key-word step needed (16-letter keys are fully forced).
2. K4 and 1,000 fresh shuffles; per text the number of fitting pairs and of distinct cipher alphabets among them.
3. p = (1 + shuffles at or above K4) / 1,001, per count; flag below 0.00096.

## Result

Candidates returned: 5. Passed all gates: 0. Best crib hits among all candidates: 24/24
(EAST 4/4, NORTHEAST 9/9, BERLIN 6/6, CLOCK 5/5).
Best loss: 7.76067198827605 (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | resubmitted | 24/24 |  | `KVXCCXHPKGLNYPWRRYQFBEASTNORTHEASTEIBHVVNNPTPYTMBJGPLYWHAVISBUCBERLINCLOCKIHOYTJNLRJRFTDMPDAPYANP` |  |
| 2 | resubmitted | 24/24 |  | `CGBDEWKNHHYPZKVEOJYGFEASTNORTHEASTTIFZBBKNCTVFSMVFVMYJGLZAICEDIBERLINCLOCKIKMFSLRMROKBDFJQNUVFDZI` |  |
| 3 | resubmitted | 24/24 |  | `KVXCCXZPKHLNYOWRRYQFBEASTNORTHEASTEIBZVVNNPTPFTMBJHPLYWZAVISBACBERLINCLOCKIZOFTJNLRJRFTDMPDAPFANP` |  |
| 4 | resubmitted | 24/24 |  | `JVXCAXPNJHLMZLWRRZQFDEASTNORTHEASTEIDPVVMNNTNGTKBHGNYZWPAWISBBCBERLINCLOCKIPOGTHMLRHSFTDKQDANGAMN` |  |
| 5 | resubmitted | 24/24 |  | `KVXCCXZPKHLNYOWRRYQFBEASTNORTHEASTEIBZVVNNPTPFTMBJHPLYWZAVISBACBERLINCLOCKIZOFTJNLRJRFTDMPDAPFANP` |  |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "item": "F14.1 replication",
 "key_length": 16,
 "copies": 1000,
 "seed": 245,
 "alpha_corrected": 0.000962,
 "cells": {
  "added": {
   "k4_pairs": 5,
   "k4_distinct_cipher_alphabets": 2,
   "p_pairs": 0.00899,
   "p_distinct": 0.03796,
   "copies_with_any": 120,
   "copies_max_pairs": 16,
   "copies_pairs_histogram": {
    "0": 880,
    "1": 78,
    "2": 22,
    "3": 9,
    "4": 3,
    "5": 4,
    "7": 1,
    "8": 1,
    "10": 1,
    "16": 1
   }
  },
  "beaufort": {
   "k4_pairs": 0,
   "k4_distinct_cipher_alphabets": 0,
   "p_pairs": 1.0,
   "p_distinct": 1.0,
   "copies_with_any": 106,
   "copies_max_pairs": 17,
   "copies_pairs_histogram": {
    "0": 894,
    "1": 68,
    "2": 18,
    "3": 6,
    "4": 4,
    "5": 3,
    "6": 1,
    "7": 2,
    "8": 1,
    "9": 1,
    "12": 1,
    "17": 1
   }
  }
 },
 "flag": false,
 "alphabets": 208064,
 "compute_seconds": 36,
 "k4_readings": [
  [
   "HOLOZOIC",
   "AEOLOTROPISM",
   "KVXCCXHPKGLNYPWRRYQFBEASTNORTHEASTEIBHVVNNPTPYTMBJGPLYWHAVISBUCBERLINCLOCKIHOYTJNLRJRFTDMPDAPYANP"
  ],
  [
   "OCYROIDAE",
   "DIOPTROMETRY",
   "CGBDEWKNHHYPZKVEOJYGFEASTNORTHEASTTIFZBBKNCTVFSMVFVMYJGLZAICEDIBERLINCLOCKIKMFSLRMROKBDFJQNUVFDZI"
  ],
  [
   "OLOGICAL",
   "AEOLOTROPISM",
   "KVXCCXZPKHLNYOWRRYQFBEASTNORTHEASTEIBZVVNNPTPFTMBJHPLYWZAVISBACBERLINCLOCKIZOFTJNLRJRFTDMPDAPFANP"
  ],
  [
   "POLYOPIC",
   "AEOLOTROPISM",
   "JVXCAXPNJHLMZLWRRZQFDEASTNORTHEASTEIDPVVMNNTNGTKBHGNYZWPAWISBBCBERLINCLOCKIPOGTHMLRHSFTDKQDANGAMN"
  ],
  [
   "ZOOLOGIC",
   "AEOLOTROPISM",
   "KVXCCXZPKHLNYOWRRYQFBEASTNORTHEASTEIBZVVNNPTPFTMBJHPLYWZAVISBACBERLINCLOCKIZOFTJNLRJRFTDMPDAPFANP"
  ]
 ]
}
```

Notes: 16/added: K4 5 pairs (2 cipher alphabets), p 0.00899 / 0.03796 against 1000 fresh shuffles; flag False


