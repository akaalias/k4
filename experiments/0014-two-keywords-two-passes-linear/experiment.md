# 0014-two-keywords-two-passes-linear: Two key words, two passes through the tableau: the cribs as linear equations mod 26

**Family:** 3-two-component-key  
**Parent:** none (root)  
**Decision:** reverted  
**Run:** 2026-10-14T17:05:51+00:00, 9.7 s, status ran  
**Time by phase:** design 6 s, implement 87 s, test 72 s, run 10 s, record 0 s

## In plain words

Suppose the artist ran the message through the sculpture's table twice, with a different secret word each time. Two pushes along the alphabet add up to one push, so the two words act like one long key made by adding them letter by letter. The 24 known letters give 24 facts about that sum. If the two words are short, say 7 and 8 letters, 24 facts are more than enough to tell whether any pair of words can produce them, and if so, what the words are. We check every pair of lengths and read off the words where the facts agree.

## Walkthrough, by hand

1. Take lengths 7 and 8 and the KRYPTOS alphabet for everything, Vigenere both passes.
2. Position 22 needs a total key letter that sends E to F: R, index 1. Position 22 uses slot 0 of the 7-letter word (21 mod 7) and slot 5 of the 8-letter word (21 mod 8), so x0 + y5 = 1.
3. Position 29 uses slot 0 again and slot 4: x0 + y4 = its forced value.
4. Subtract: y5 - y4 is now fixed.
5. Walk all 24 positions this way; every slot gets tied to the others through shared positions.
6. When a loop closes, the values must agree, or the pair 7 and 8 is dead.
7. If they all agree, pick x0 freely; every other letter follows.
8. Twenty-six choices of x0 give twenty-six word pairs; see whether either word is one the puzzle knows.

## Worked example (generated)

```
lengths 7 and 8, KRYPTOS alphabet throughout, Vigenere both passes: equations from the first cribs

pos  plain  cipher  total key  index  x slot (pos-1 mod 7)  y slot (pos-1 mod 8)
 22    E      F        R         1           0                    5
 23    A      L        D        10           1                    6
 24    S      R        U        21           2                    7
 29    T      R        W        23           0                    4
 30    H      N        O         5           1                    5
 64    B      N        E        11           0                    7
 65    E      Y        L        17           1                    0

positions 22 and 29 share x slot 0, so y5 - y4 equals the difference of their totals; the chain of such ties must close consistently.
```

## Lineage

Inherits from nothing; this is a root experiment. What changed: New root in family 3. The key is the sum of two short repeating keys, one per pass, so the 24 cribs become linear equations in a + b unknowns and consistency is decided exactly.

## Hypothesis (domain expert)

Scheidt's habit of combining two key components (knowledge/people/scheidt.md, C6) and Sanborn's 'double' (C1 reading c, composed tableau passes) suggest two keywords X and Y applied in two passes. Two passes through the same tableau compose to one periodic key t[i] = x[i mod a] + s y[i mod b] mod 26 with s = +1 or -1 depending on the modes, of period lcm(a, b). 0005 excluded periods 1-26 and 30-52, so only pairs with lcm in {27, 28, 29} or 53 and above remain; within them the question is whether the forced total key factors into two short words. For each pair 2 <= a < b <= 30, each plain and cipher alphabet in {standard, KRYPTOS}, each sign of the plaintext (Vigenere-like or Beaufort-like) and each s, the 24 forced values give 24 equations x_u - y'_v = t over Z26, checked by a weighted union-find; with a + b - 1 effective unknowns there are 25 - a - b redundant checks, each passing by chance with probability 1/26. Survivors are enumerated (26 to the power of the number of components) and X, Y matched against the vocabulary and K1-K3 windows under both key alphabets and both signs; matches are decrypted and submitted. Bounds: complete for two-pass periodic keys with lengths 2-30 under the standard and KRYPTOS alphabets.

## Prediction

Length pairs with a + b above about 20 survive by chance under some settings, because they have few redundant checks. Pairs with a + b of 15 or less survive in at most a handful of settings. No surviving pair yields X or Y in the vocabulary or K1-K3 windows; zero candidates pass.

## Method

1. For each plain alphabet, cipher alphabet and plaintext sign, compute the forced total key value t at each crib position.
2. For each length pair (a, b) with lcm not in 1-26 or 30-52, and each sign s, build nodes for the a slots of X and the b slots of Y and add the edge x[i mod a] - s y[i mod b] = t[i] for each crib.
3. Reject on any inconsistent cycle.
4. Count components; enumerate the free values when there are at most three components.
5. Match X and Y against the vocabulary and K1-K3 windows under the standard and KRYPTOS key alphabets; decrypt and submit matches.

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
 "family": "two periodic keys composed through two tableau passes",
 "lengths": "2 <= a < b <= 30, lcm outside 1-26 and 30-52",
 "pairs": 306,
 "alphabets": "plain and cipher in {std, kry}; key words read in std or kry",
 "cases": 4896,
 "survivors": 3498,
 "survivors_by_a_plus_b": {
  "25": 18,
  "26": 16,
  "27": 50,
  "28": 34,
  "29": 96,
  "30": 80,
  "31": 160,
  "32": 148,
  "33": 176,
  "34": 192,
  "35": 144,
  "36": 144,
  "37": 192,
  "38": 176,
  "39": 160,
  "40": 128,
  "41": 160,
  "42": 144,
  "43": 144,
  "44": 128,
  "45": 112,
  "46": 112,
  "47": 112,
  "48": 96,
  "49": 96,
  "50": 80,
  "51": 80,
  "52": 64,
  "53": 64,
  "54": 48,
  "55": 48,
  "56": 32,
  "57": 32,
  "58": 16,
  "59": 16
 },
 "smallest_surviving_pairs": [],
 "vocab_or_k1k3_matches": 0
}
```

Notes: 4896 cases; 3498 consistent; 0 word matches submitted.


