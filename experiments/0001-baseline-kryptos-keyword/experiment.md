# 0001-baseline-kryptos-keyword: Baseline: keyed Vigenere over the sculpture's own alphabet with key KRYPTOS

**Family:** 1-keyed-periodic  
**Parent:** none (root)  
**Decision:** reverted  
**Run:** 2026-10-14T16:08:01+00:00, 0.0 s, status ran  
**Time by phase:** run 0 s

## In plain words

The first two messages on the sculpture were locked with a simple scheme: a secret word is written over and over under the message, and each pair of letters is looked up in a table carved on the sculpture. We try the laziest possible secret word, KRYPTOS. We expect it to fail, and the way it fails tells us the checking machinery works: the 24 letters Sanborn has revealed will not show up where they should.

## Walkthrough, by hand

Take the keyed alphabet KRYPTOSABCDEFGHIJLMNQUVWXZ. Number its letters 0 to 25. For each ciphertext letter, find its number, subtract the number of the key letter beneath it (the key KRYPTOS repeating), wrap around 26, and read off the plaintext letter at that number. The harness then checks positions 22 to 34 for EASTNORTHEAST and 64 to 74 for BERLINCLOCK. If they are not there, the hypothesis is dead at that gate.

## Worked example (generated)

```
alphabet: KRYPTOSABCDEFGHIJLMNQUVWXZ
key:      KRYPTOS (repeating)

pos  cipher  key  (c - k) mod 26  plain
  1    O      K      5 -  0 =  5     O
  2    B      R      8 -  1 =  7     A
  3    K      Y      0 -  2 = 24     X
  4    R      P      1 -  3 = 24     X
  5    U      T     21 -  4 = 17     L
  6    O      O      5 -  5 =  0     K
```

## Lineage

Inherits from nothing; this is a root experiment. What changed: Root experiment; establishes the pipeline with the most naive attack.

## Hypothesis (domain expert)

K4 is a Quagmire-III Vigenere over the KRYPTOS-keyed alphabet, like K1 and K2, with the sculpture's own name as the keyword. This is the null hypothesis the community discarded in 1999; it is here to prove the gates and the record format, and to show the cribs rejecting it.

## Prediction

Fails the crib gate with at most a handful of chance hits out of 24; zero candidates pass.

## Method

Decrypt K4 with keyed_vigenere_decrypt(K4, 'KRYPTOS', KRYPTOS_ALPHABET). Submit that single plaintext as the candidate. Key bits counted as 4.7 per letter.

## Result

Candidates returned: 1. Passed all gates: 0. Best crib hits among all candidates: 2/24
(EAST 0/4, NORTHEAST 1/9, BERLIN 1/6, CLOCK 0/5).
Best loss: 224.67605782561338 (0 is solved; 10 per missed crib letter). Best fitness: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | cribs | 2/24 |  | `OAXXLKMOFFMGPKOJGCTPLFJZNJIWRMEWYRZTVYLYEHSOCWUQLAPHWGJTISUFIAYNRRNKZFZERWNBTKXVRFTTIFXMDJRUDXSPV` | keyed Vigenere, alphabet KRYPTOS, keyword KRYPTOS |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "keyed Vigenere over KRYPTOS alphabet",
 "keys_tried": [
  "KRYPTOS"
 ],
 "periods": [
  7
 ]
}
```

Notes: Pipeline check only.


