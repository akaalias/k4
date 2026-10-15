# 0045-running-key-k1-k3-mixed-alphabets: The earlier messages as a running key, on tables rebuilt from the puzzle's words

**Family:** 1-keyed-periodic  
**Parent:** 0004-running-key-from-k1-k3  
**Decision:** reverted  
**Run:** 2026-10-15T09:39:03+00:00, 62.7 s, status ran  
**Time by phase:** design 0 s, implement 53 s, test 5 s, run 63 s, record 0 s

## In plain words

Experiment 4 asked whether the first three messages, lined up under the fourth as a long secret word, could explain the known letters, using the sculpture's own table. The table might have been built from another word, so we rebuild it from each word the puzzle knows and slide the three messages past the fourth again, at every starting point, forwards and backwards.

## Walkthrough, by hand

1. Build the alphabet from BERLIN for the message letters and from CLOCK for the carved letters.
2. Lay the K1 plaintext under the fourth message starting at some offset, so each position has a key letter.
3. Position 22 is E: find E in the BERLIN alphabet, add the key letter's place in the plain alphabet, and read the result in the CLOCK alphabet; compare with the carved F.
4. A miss counts one; three misses end this offset.
5. Slide the offset along the whole text, then reverse the text, then try the next pair of alphabets.

## Worked example (generated)

```
(worked_example failed: IndexError('string index out of range'))
```

## Lineage

Inherits from 0004-running-key-from-k1-k3. What changed: Experiment 4 slid the K1-K3 plaintexts and ciphertexts past K4 under the standard and KRYPTOS alphabets. Here the plain and cipher alphabets are the keyword mixings of every vocabulary word, with the key letters read on the standard or KRYPTOS order.

## Hypothesis (domain expert)

Sanborn's 'clues to the last section are contained in previously deciphered parts' (C7) read as a running key was killed under 24 conventions in experiment 4. Under keyword-mixed plain and cipher alphabets (C5, C29) every trial changes, so the sweep is rerun: sources are the K1, K2 (as carved and corrected) and K3 plaintexts, the three ciphertexts, and the concatenations of each set, read forward and backward at every cyclic offset; 63 plain x 63 cipher alphabets x 2 key alphabets x 3 modes; mismatches counted with early exit at three. Chance survival per trial is 26 to the minus 24, with about 180 million trials. Bounds: complete for these texts and alphabets.

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
 "family": "running key from K1-K3 plaintexts and ciphertexts, keyword-mixed alphabets",
 "alphabets": 63,
 "key_alphabets": [
  "std",
  "kry"
 ],
 "modes": 3,
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
  "K2 plain corrected ending bwd": 13
 },
 "trials": 146932380,
 "stopped_by_clock": false,
 "fewest_mismatches": "more than 2",
 "near_misses": [],
 "survivors": 0
}
```

Notes: 146932380 trials; 0 survivors; 0 within two mismatches.


