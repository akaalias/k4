# 0047-running-key-carter-and-sculpture-mixed-alphabets: Carter's book and the sculpture's own texts as running keys, on tables rebuilt from the puzzle's words

**Family:** 1-keyed-periodic  
**Parent:** 0045-running-key-k1-k3-mixed-alphabets  
**Decision:** reverted  
**Run:** 2026-10-15T09:49:23+00:00, 399.4 s, status ran  
**Time by phase:** design 0 s, implement 51 s, test 13 s, run 399 s, record 0 s

## In plain words

Experiments 17 and 21 slid the sculpture's own texts and Howard Carter's book along the fourth message as a long secret word, using the sculpture's table, and found nothing. Here the table is rebuilt from each word the puzzle knows, on one side at a time, and the sliding is done again, forwards and backwards, at every starting point.

## Walkthrough, by hand

1. Build the alphabet from BERLIN for the message letters and from CLOCK for the carved letters.
2. Lay the K1 plaintext under the fourth message starting at some offset, so each position has a key letter.
3. Position 22 is E: find E in the BERLIN alphabet, add the key letter's place in the plain alphabet, and read the result in the CLOCK alphabet; compare with the carved F.
4. A miss counts one; three misses end this offset.
5. Slide the offset along the whole text, then reverse the text, then try the next pair of alphabets.

## Worked example (generated)

```
plain alphabet BERLIN/keyword BERLINACDFGHJKMOPQSTUVWXYZ
cipher alphabet CLOCK/keyword CLOKABDEFGHIJMNPQRSTUVWXYZ
key text: Carter volume one at offset 0, key letters on the standard order; Vigenere

pos  plain  key  result  carved  match
 22    E     U     V       F     no
 23    A     M     S       L     no
 24    S     L     K       R     no
 25    T     I     L       V     no
 64    B     C     O       N     no
 65    E     A     L       Y     no
```

## Lineage

Inherits from 0045-running-key-k1-k3-mixed-alphabets. What changed: The key texts are Carter's Tomb of Tut-ankh-Amen and the sculpture's carved texts (experiments 17 and 21) instead of K1-K3; one of the two alphabets is standard or KRYPTOS and the other the keyword mixing of a vocabulary word, since the full 63 x 63 pool over 570,000 offsets is beyond the budget.

## Hypothesis (domain expert)

Experiments 17 and 21 killed the sculpture's texts and Carter's book as running keys under 24 conventions; 45 killed K1-K3 under keyword-mixed alphabets. The remaining corner is these longer texts under mixed alphabets (C5, C7, C25). Sources: Carter volume one as scanned, the carved tableau by rows and columns, the Morse plaintexts, the right-hand panel, each forward and backward, every cyclic offset. Alphabet pairs: one side standard or KRYPTOS, the other any of the 61 keyword mixings, both ways round, with the key letters on the standard or KRYPTOS order and three modes. About 900 million trials with early exit at three mismatches. Bounds: complete for these texts and this restricted pool; both sides mixed is not covered.

## Prediction

No text, offset, direction or alphabet pair explains all 24 known letters, and none comes within two mismatches. Zero candidates pass.

## Method

1. Build the key texts and the alphabet pool.
2. For each plain and cipher alphabet, key alphabet and mode, precompute the cipher letter for every (plain, key) pair.
3. For each text, direction and offset, count mismatches at the 24 cribs, stopping at the third.
4. Keep trials within two mismatches; decrypt and submit any with zero.

## Result

Candidates returned: 0. Passed all gates: 0. Best crib hits among all candidates: 0/24
(no candidates).
Best loss: None (0 is solved; 10 per missed crib letter). Best fitness: None. Champion before this run: 0034-complete-the-key-at-surviving-periods.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| - | no candidates | | | | |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "running key from Carter and the sculpture texts, one alphabet keyword-mixed",
 "alphabet_pairs": 248,
 "alphabets": 63,
 "key_alphabets": [
  "std",
  "kry"
 ],
 "modes": 3,
 "sources": {
  "carter vol1 fwd": 284914,
  "carter vol1 bwd": 284914,
  "tableau rows fwd": 781,
  "tableau rows bwd": 781,
  "tableau columns fwd": 781,
  "tableau columns bwd": 781,
  "morse as carved fwd": 80,
  "morse as carved bwd": 80,
  "morse reversed order fwd": 80,
  "morse reversed order bwd": 80,
  "right panel K1-K4 fwd": 865,
  "right panel K1-K4 bwd": 865
 },
 "trials": 855602976,
 "stopped_by_clock": false,
 "fewest_mismatches": "more than 2",
 "near_misses": [],
 "survivors": 0
}
```

Notes: 855602976 trials; 0 survivors; 0 within two mismatches.


