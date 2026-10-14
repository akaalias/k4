# 0017-running-key-from-the-sculpture-itself: A running key read off the sculpture: the carved tableau, the Morse, and the whole right-hand panel

**Family:** 1-keyed-periodic  
**Parent:** 0004-running-key-from-k1-k3  
**Decision:** reverted  
**Run:** 2026-10-14T17:19:37+00:00, 0.3 s, status ran  
**Time by phase:** design 15 s, implement 43 s, test 0 s, run 0 s, record 0 s

## In plain words

A running key is a long text used as the secret, one letter per message letter, so the key is as long as the message. The designer said the keys were hidden at the sculpture. The sculpture carries plenty of text: the big table of shifted alphabets, the Morse code messages on the stones outside, and the three solved messages. We slide each of those texts along the fourth message at every possible starting point and ask whether any position explains all 24 known letters.

## Walkthrough, by hand

1. Take the tableau read row by row: KRYPTOSABCDEFGHIJLMNQUVWXZKRYP, then RYPTOSABCD..., and so on.
2. Choose an offset, say 0, so key letter 1 is K, key letter 2 is R, and so on.
3. Position 22 of the message is E; its key letter is the 22nd letter of the text, H.
4. Under the sculpture's alphabet and Vigenere, E shifted by H should give the carved F; it gives something else, so count one mismatch.
5. Do this for all 24 known letters.
6. Slide the offset by one and repeat, through the whole text, forward and backward, under each way of using the table.

## Worked example (generated)

```
key text: tableau rows, offset 0, KRYPTOS alphabet throughout, Vigenere

key text begins KRYPTOSABCDEFGHIJLMNQUVWXZKRYPRYPTOSABCD...

pos  plain  key letter  E+key  carved  match
 22    E        U         S      F     no
 23    A        V         P      L     no
 24    S        W         P      R     no
 25    T        X         Y      V     no
 64    B        O         G      N     no
 65    E        S         L      Y     no
```

## Lineage

Inherits from 0004-running-key-from-k1-k3. What changed: Key sources are the sculpture's own carved texts rather than the K1-K3 solutions: the tableau read by rows and by columns, the Morse plaintexts, and the four ciphertexts as one panel. Family 1 re-entered with a new key source, as its parked status requires.

## Hypothesis (domain expert)

Scheidt: 'the keys were concealed at the sculpture' (C6); the Morse and the tableau are the texts concealed there in plain sight (C9, C25). 0004 slid the K1-K3 plaintexts and ciphertexts past K4 under 24 conventions and found nothing. Here the sources are: the carved tableau as 26 rows of 30 letters plus the extra L, read row by row and column by column; the left-hand index column plus the rows; the seven Morse plaintexts as carved and in reverse order; the right-hand panel's four ciphertexts as one 869-letter text; each forward and backward, at every cyclic offset, under the 24 conventions, scored by crib mismatches. Zero mismatches is a survivor and is decrypted; one or two mismatches are reported for the one-letter-error reading (C17). About 200,000 trials; chance survival per trial is 26 to the minus 24. Bounds: complete for these sources.

## Prediction

No source, direction, offset or convention explains all 24 known letters. The best trial has no fewer than 5 mismatches, which is what chance gives among 200,000 trials. Zero candidates pass.

## Method

1. Build the key texts from data/site_texts.json and the K1-K4 ciphertexts, letters only.
2. For each text, each direction, each convention and each cyclic offset, encrypt the 24 known plaintext letters with the key letters at their positions and count mismatches against the carved letters.
3. Keep the best few trials.
4. Decrypt and submit any zero-mismatch trial.

## Result

Candidates returned: 0. Passed all gates: 0. Best crib hits among all candidates: 0/24
(no candidates).
Best loss: None (0 is solved; 10 per missed crib letter). Best fitness: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| - | no candidates | | | | |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "running key from the sculpture's own texts",
 "sources": {
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
  "right panel ciphertexts K1-K4 fwd": 865,
  "right panel ciphertexts K1-K4 bwd": 865
 },
 "conventions": 24,
 "offsets": "all cyclic",
 "trials": 162912,
 "fewest_mismatches": "more than 3",
 "trials_with_at_most_3_mismatches": [],
 "survivors": 0
}
```

Notes: 162912 trials; 0 zero-mismatch survivors; 0 trials with three or fewer mismatches.


