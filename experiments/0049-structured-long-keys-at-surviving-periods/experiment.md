# 0049-structured-long-keys-at-surviving-periods: Long keys with a shape: two puzzle words joined, a word and its mirror, a word doubled, at the periods the cribs allow

**Family:** 1-keyed-periodic  
**Parent:** 0005-quagmire-period-sweep-forced-keys  
**Decision:** reverted  
**Run:** 2026-10-15T10:13:12+00:00, 11.8 s, status ran  
**Time by phase:** design 0 s, implement 192 s, test 12 s, run 12 s, record 0 s

## In plain words

A secret word of 27 to 29 letters is probably not one word. It could be two of the puzzle's words joined, a word followed by itself, or a word followed by its mirror image. Each such key fixes the 24 letters that the known letters demand, so we simply build every key of that kind and check it against the 24 demands, on the sculpture's table and on tables rebuilt from the puzzle's words.

## Walkthrough, by hand

1. Join BERLIN and ALEXANDERPLATZ: BERLINALEXANDERPLATZ is 20 letters, too short; join WILLIAMWEBSTER and PALIMPSEST: 24, too short; join TUTANKHAMUN and SHADOWFORCES: 23.
2. Keep the pairs that reach 27, 28 or 29 letters, such as DIGITALINTERPRETATION joined with EGYPT.
3. On the sculpture's table with Vigenere, position 22 forces key letter R at slot 21 of a 27-letter key; position 23 forces D at slot 22, and so on for all 24 known letters.
4. Compare the joined key's letters at those slots; one mismatch and the key is out.
5. Repeat for every pair, every mirror and every doubling, under every table.

## Worked example (generated)

```
key DIGITALINTERPRETATIONEGYPT, length 26: a 26-letter join falls short of 27, so it is not tried; take instead

joined ABSCISSA+DIGITALINTERPRETATION: ABSCISSADIGITALINTERPRETATION (29 letters)

sculpture's alphabet throughout, Vigenere: forced key letters at the first slots
pos 22: slot 21 must be R; the key has R
pos 23: slot 22 must be D; the key has E
pos 24: slot 23 must be U; the key has T
pos 25: slot 24 must be M; the key has A
```

## Lineage

Inherits from 0005-quagmire-period-sweep-forced-keys. What changed: Experiment 5 matched the forced key fragments at periods 27 to 29 against single vocabulary words and K1-K3 windows. A 27 to 29 letter key is unlikely to be one word; here it is built from two: joined, joined with a separator letter, a word followed by its mirror, or a word doubled. The forced fragments are matched exactly under the standard, KRYPTOS and vocabulary-mixed alphabets.

## Hypothesis (domain expert)

Periods 27-29 survive the crib sweep under every alphabet pair (0005, 0020), and their forced key fragments read as noise (0009, 0010), which rules out an English phrase as key but not a key made of two puzzle words with no English transition, or a word and its reverse (Sanborn's mirrors, C3), or a doubled word. Key shapes: X+Y, X+c+Y for a separator letter c, X+reverse(X), X+X, X+reverse(Y), over the 62-word vocabulary and its K1-K3 windows, kept when the length is 27, 28 or 29. Under each plain-cipher alphabet pair (standard, KRYPTOS, 61 keyword mixings) and mode, the 24 forced key indices are compared with the key read in the standard, KRYPTOS or the plain alphabet; a match decrypts and submits. About 20,000 key shapes x 12,000 alphabet classes, exact. Bounds: complete for these shapes and alphabets.

## Prediction

No shaped key of length 27 to 29 matches all 24 forced letters under any alphabet pair and mode. Zero candidates pass.

## Method

1. Build the shaped keys of length 27-29 from the vocabulary.
2. For each plain and cipher alphabet and mode, compute the 24 forced key indices and their slots at each period.
3. For each key, read it in each key alphabet as indices and compare at the forced slots; count mismatches.
4. Decrypt and submit exact matches; report the fewest mismatches.

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
 "family": "shaped keys of length 27-29 from the vocabulary, periodic tableau, vocabulary-mixed alphabets",
 "keys": 272,
 "keys_by_length": {
  "27": 124,
  "28": 70,
  "29": 78
 },
 "alphabets": 63,
 "trials": 9716112,
 "fewest_mismatches": "more than 3",
 "nearest": [],
 "survivors": 0
}
```

Notes: 272 shaped keys x 63^2 alphabet pairs x 3 modes x 3 key readings: 9716112 trials; fewest mismatches more than 3; 0 exact matches.


