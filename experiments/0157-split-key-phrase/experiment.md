# 0157-split-key-phrase: F1.11: a split key phrase: its first part mixes the plain alphabet, its second the cipher alphabet, the whole phrase is the repeating key

**Family:** 1-keyed-periodic  
**Parent:** 0123-two-free-alphabets-exact-at-every-key-length  
**Decision:** reverted  
**Run:** 2026-10-16T22:24:47+00:00, 24.3 s, status ran  
**Time by phase:** unattributed 12 s, run 24 s, record 0 s

## In plain words

A wartime US Army manual describes a key phrase cut in two: the first half reorders the alphabet for the message, the second half reorders the alphabet for the carved letters, and the whole phrase is the repeating secret word. We try every pair of the puzzle's words and every short run of words from the first three messages as such a phrase, and count how many of the 24 known letters each one gives.

## Walkthrough, by hand

1. Take the phrase LAYER TWO: LAYER mixes the plain alphabet (LAYERBCDFG...), TWO the cipher alphabet (TWOABCDEFG...).
2. The key is LAYERTWO, eight letters, repeated under the message.
3. For a message letter, find its place in the plain alphabet, add the key letter's place in the cipher alphabet, and read the cipher alphabet there.
4. Run it backwards at the 24 known places: does each carved letter give the known letter?
5. Repeat for every phrase, the three numberings, the three rules, and scrambled copies.

## Worked example (generated)

```
phrase LAYER TWO: plain alphabet LAYERBCDFGHIJKMNOPQSTUVWXZ, cipher alphabet TWOABCDEFGHIJKLMNPQRSUVXYZ, key LAYERTWO

place  carved  key  cipher place  key value  plain place  letter  known
   22       F    T             8          0            8       F      E
   23       L    W            14          1           13       K      A
   24       R    O            19          2           17       P      S
   64       N    O            16          2           14       M      B
   65       Y    L            24         14           10       H      E
```

## Lineage

Inherits from 0123-two-free-alphabets-exact-at-every-key-length. What changed: F1.11 (added 2026-10-16 from Elementary Military Cryptography, 1935/1943, par. 59d: the key phrase CENTRAL AMERICA split into CENTRAL for one alphabet and AMERICA for the other, the whole phrase the key). 0123 showed two unknown alphabets admit K4 only at key lengths 8, 13, 16, 19, 20, 23, 24 and 26; here the alphabets and key are fixed by a phrase, so each phrase is one exact decryption. Phrases: every ordered pair of puzzle words, and every run of 2-4 consecutive words of the K1-K3 plaintexts split at each inner word boundary, of total length 3-30 (all lengths tried, not only 0123's eight, as a check).

## Hypothesis (domain expert)

C5(b) ('key word/s'), C6 (keys concealed at the sculpture, K1-K3 vocabulary), C7(a); source knowledge/sources (Elementary Military Cryptography par. 59d, per research_notes/Scheidt patents and field ciphers/addendum_downloaded_manuals.md). Model: plain alphabet P = keyword_mixed(part 1), cipher alphabet C = keyword_mixed(part 2), key = part 1 + part 2 repeating; key letters numbered by their place in C (the manual's rule: the key letter in the cipher component is set against the plain component's first letter), in P, or in the standard alphabet; rules Vigenere (C[P(p) + k]), Beaufort (C[k - P(p)]), variant (C[P(p) - k]). Exact: count the known letters each phrase reproduces. Ten scrambled coppers; statistic fixed before the run: phrases reproducing all 24 (a hit), and the best count on K4 against the coppers' best.

## Prediction

No phrase reproduces all 24 known letters; K4's best count is inside the coppers' range (about 6-9 of 24). Zero candidates.

## Method

1. Build the phrases.
2. For each phrase, numbering and rule: decrypt the 24 known places and count matches.
3. Same on 10 coppers; compare best counts; decrypt any full hit.

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
 "family": "split key phrase (EMC par. 59d): part 1 mixes the plain alphabet, part 2 the cipher alphabet, the whole phrase the key",
 "phrases": 29880,
 "numberings": [
  "cipher alphabet",
  "plain alphabet",
  "standard"
 ],
 "rules": [
  "vig",
  "beau",
  "var"
 ],
 "k4_best_hits": 7,
 "controls_best_hits": [
  7,
  8,
  8,
  7,
  7,
  7,
  7,
  7,
  7,
  7
 ],
 "k4_full_hits": 0,
 "controls_full_hits": [
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
 ],
 "k4_top": [],
 "controls": "10 shuffled coppers (seed 1411)",
 "exhaustive": true
}
```

Notes: 29,880 phrases x 3 numberings x 3 rules: K4 best 7/24 (coppers 7-8); full hits K4 0, coppers [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


