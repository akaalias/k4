# 0101-key-restarted-at-every-word: An interrupted key: the key word starts again at the first letter of every word of the message

**Family:** 1-keyed-periodic  
**Parent:** 0001-crib-consistent-periods  
**Decision:** reverted  
**Run:** 2026-10-15T20:09:27+00:00, 0.1 s, status ran  
**Time by phase:** unattributed 41 s, run 0 s, record 0 s

## In plain words

With a secret word as key, one usually runs it along the whole message. A trick to hide the pattern is to start the secret word again at the beginning of every word of the message. We know where some words begin, because the known letters spell EAST, NORTH, EAST, BERLIN and CLOCK. So for each length of secret word we can check whether starting it over at each of those words fits the carved letters.

## Walkthrough, by hand

1. Split the known letters into words: EAST at 22-25, NORTH at 26-30, EAST at 31-34, BERLIN at 64-69, CLOCK at 70-74.
2. Restart the key at each word: E at 22, N at 26, E at 31, B at 64 and C at 70 all take the first key letter.
3. On the sculpture's alphabet with Vigenere, the key letter for E to F at 22 and for N to Q at 26 must then be the same.
4. Do this for each offset, key length 1-26, the other word splits and table rules.

## Worked example (generated)

```
words EAST NORTH EAST BERLIN CLOCK, key restarted at each; sculpture's alphabet, Vigenere

place  letter  copper  offset in word  key value
   22       E       F               0          1
   23       A       L               1         10
   24       S       R               2         21
   25       T       V               3         18
   26       N       Q               0          1
   27       O       Q               1         15
   28       R       P               2          2
   29       T       R               3         23
   30       H       N               4          5
   31       E       G               0          2
   32       A       K               1         19
   33       S       S               2          0
   34       T       S               3          2
   64       B       N               0         11
   65       E       Y               1         17
   66       R       P               2          2
   67       L       V               3          5
   68       I       T               4         15
   69       N       T               5         11
   70       C       M               0          9
   71       L       Z               1          8
   72       O       F               2          7
   73       C       P               3         20
   74       K       K               4          0
```

## Lineage

Inherits from 0001-crib-consistent-periods. What changed: Every periodic test so far ran the key straight through the message. A classical hand variant restarts the key word at each new plaintext word, so the key letter depends on the place inside the word, not in the message. The cribs supply the word breaks (EAST NORTH EAST or EAST NORTHEAST; BERLIN CLOCK or BERLINCLOCK), which makes the test exact.

## Hypothesis (domain expert)

Scheidt: 'simple, can be remembered' (C5) and he 'masked the English language' (C4); an interrupted key is a standard field method (Friedman's 'interrupted key') that hides the period. Model: key letter of a plaintext letter = keyword[(offset inside its word) mod L], L = 1-26, the keyword restarting at each word; EAST and BERLIN assumed to start words (E at 22 and B at 64). Segmentations: EAST|NORTH|EAST, EAST|NORTHEAST, EASTNORTHEAST as one word, crossed with BERLIN|CLOCK and BERLINCLOCK (five splits). Eight tableau classes (standard or KRYPTOS plain and cipher alphabets, Beaufort or not). Known letters with the same in-word offset mod L must force the same key value. Ten shuffled coppers.

## Prediction

No segmentation, key length or table rule fits all 24 known letters except at key lengths long enough that no two known letters share a key letter (L at least 9 for the segmentations with NORTHEAST, 6 otherwise); counts at those lengths match the coppers'. Zero candidates.

## Method

1. For each segmentation, give each known letter its offset inside its word.
2. For each key length and class, compute the forced key value at each known letter and check that letters with equal offset mod L agree.
3. Record the smallest consistent L and the number of checks.
4. Repeat on ten shuffled coppers.

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
 "family": "interrupted key restarting at every plaintext word",
 "segmentations": [
  "EAST|NORTH|EAST + BERLIN|CLOCK",
  "EAST|NORTH|EAST + BERLINCLOCK",
  "EAST|NORTHEAST + BERLIN|CLOCK",
  "EAST|NORTHEAST + BERLINCLOCK",
  "EASTNORTHEAST + BERLIN|CLOCK"
 ],
 "key_lengths": [
  1,
  26
 ],
 "classes": 8,
 "by_segmentation": {
  "EAST|NORTH|EAST + BERLIN|CLOCK": {
   "k4_smallest_L_with_checks": null,
   "controls": [
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
   ]
  },
  "EAST|NORTH|EAST + BERLINCLOCK": {
   "k4_smallest_L_with_checks": null,
   "controls": [
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
   ]
  },
  "EAST|NORTHEAST + BERLIN|CLOCK": {
   "k4_smallest_L_with_checks": null,
   "controls": [
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
   ]
  },
  "EAST|NORTHEAST + BERLINCLOCK": {
   "k4_smallest_L_with_checks": null,
   "controls": [
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
   ]
  },
  "EASTNORTHEAST + BERLIN|CLOCK": {
   "k4_smallest_L_with_checks": null,
   "controls": [
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
   ]
  }
 },
 "k4_live_with_3_plus_checks": [],
 "n_k4_live_with_3_plus_checks": 0,
 "controls": "10 shuffled coppers (seed 101), identical test"
}
```

Notes: Smallest key length consistent with at least one check (None: no length 1-26 fits), K4 vs controls: EAST|NORTH|EAST + BERLIN|CLOCK: None vs [None, None, None, None, None, None, None, None, None, None]; EAST|NORTH|EAST + BERLINCLOCK: None vs [None, None, None, None, None, None, None, None, None, None]; EAST|NORTHEAST + BERLIN|CLOCK: None vs [None, None, None, None, None, None, None, None, None, None]; EAST|NORTHEAST + BERLINCLOCK: None vs [None, None, None, None, None, None, None, None, None, None]; EASTNORTHEAST + BERLIN|CLOCK: None vs [None, None, None, None, None, None, None, None, None, None]. K4 settings consistent with 3+ checks: 0.


