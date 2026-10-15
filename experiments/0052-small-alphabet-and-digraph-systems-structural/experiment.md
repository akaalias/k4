# 0052-small-alphabet-and-digraph-systems-structural: Ciphers that cannot write all 26 letters, or cannot write an odd number of them

**Family:** 8-hill-and-polygraphic  
**Parent:** 0015-hill-solved-from-crib-blocks  
**Decision:** reverted  
**Run:** 2026-10-15T12:09:17+00:00, 0.0 s, status ran  
**Time by phase:** design 0 s, implement 0 s, test 0 s, run 0 s, record 0 s

## In plain words

Some famous ciphers use a five-by-five square of letters, which has room for only 25 of the 26, so one letter can never come out of them. Others swap letters two at a time, so the message they make always has an even number of letters. The copper has 97 letters, an odd number, and we check whether every letter of the alphabet appears on it. Either fact rules out a whole group of ciphers at once, without trying a single secret word.

## Walkthrough, by hand

1. Write the 26 letters A to Z in a row.
2. Read the copper's 97 letters and tick each letter as it appears.
3. J appears at place 41 and I at place 16, so a square that merges I and J cannot have made this text.
4. Q appears at places 26 and 27, so a square that drops Q cannot either.
5. Every one of the 26 ticks gets ticked, so no 25-letter square made it.
6. Count the letters: 97, an odd number, so no cipher that works two letters at a time made it without an extra letter.

## Worked example (generated)

```
letter counts on the copper:
A4  B5  C2  D3  E2  F4  G4  H2  I4  J3  K8  L4  M1  N3  O5  P3  Q4  R4  S6  T6  U6  V2  W5  X2  Y1  Z4
length 97
```

## Lineage

Inherits from 0015-hill-solved-from-crib-blocks. What changed: Experiments 15, 36 and 44 tested Hill ciphers. The other classic polygraphic systems, Playfair, two-square, four-square and bifid, work on a 5 by 5 square of 25 letters, and the Berlin World Clock reading of the clock clue suggests a 24-letter ring. Such systems leave a fingerprint in the ciphertext itself: a letter that never appears, or an even length. This checks the fingerprint before any key search.

## Hypothesis (domain expert)

Playfair, two-square and four-square encipher digraphs on 5x5 squares (25 symbols, I/J or Q dropped) and need an even-length text; bifid on a 5x5 square emits only the square's 25 letters; ADFGX and ADFGVX emit 5 or 6 letters; a cipher on the Weltzeituhr's 24-zone ring (C12b) emits at most 24 letters. Count the distinct letters of K4 and its length. If all 26 letters occur, every system whose ciphertext alphabet has at most 25 symbols is excluded, whatever the key; if the length is odd, every digraphic system without a null is excluded. Ten shuffles of K4 are not needed: the test is structural and exact.

## Prediction

All 26 letters occur in K4 and its length is odd, so Playfair, two-square, four-square, bifid on 5x5, ADFGX, ADFGVX and any 24-letter ring cipher are excluded. Zero candidates.

## Method

1. List the distinct letters of K4 and the count of each.
2. Note the length.
3. For each system, state its output alphabet size and length rule.
4. Mark each system excluded or open.
5. Say which escape routes remain: a null letter appended, a 6x6 square with digits spelled out, a 26-symbol variant.

## Result

Candidates returned: 0. Passed all gates: 0. Best crib hits among all candidates: 0/24
(no candidates).
Best loss: None (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: 0034-complete-the-key-at-surviving-periods.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| - | no candidates | | | | |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "ciphers with fewer than 26 output symbols or an even-length rule",
 "distinct_letters": 26,
 "length": 97,
 "rarest_letters": {
  "Y": 1,
  "M": 1,
  "X": 2,
  "H": 2,
  "V": 2,
  "E": 2
 },
 "verdicts": {
  "Playfair": "excluded: emits at most 25 letters; K4 has 26; needs an even length; K4 has 97",
  "two-square": "excluded: emits at most 25 letters; K4 has 26; needs an even length; K4 has 97",
  "four-square": "excluded: emits at most 25 letters; K4 has 26; needs an even length; K4 has 97",
  "bifid 5x5": "excluded: emits at most 25 letters; K4 has 26",
  "ADFGX": "excluded: emits at most 5 letters; K4 has 26; needs an even length; K4 has 97",
  "ADFGVX": "excluded: emits at most 6 letters; K4 has 26; needs an even length; K4 has 97",
  "Weltzeituhr 24-letter ring": "excluded: emits at most 24 letters; K4 has 26",
  "Polybius 5x5 to letters": "excluded: emits at most 25 letters; K4 has 26"
 },
 "escape_routes": [
  "a null letter appended to make the length even (then the 25-letter rule still applies)",
  "a 6x6 square with digits written out as words",
  "a variant on a 26-letter rectangle"
 ]
}
```

Notes: K4 uses all 26 letters and has 97 letters; every listed system is excluded: Playfair; two-square; four-square; bifid 5x5; ADFGX; ADFGVX; Weltzeituhr 24-letter ring; Polybius 5x5 to letters.


