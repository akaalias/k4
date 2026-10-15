# 0115-a-puzzle-word-plus-any-english-word: Two key words added, one from the puzzle and one from the whole dictionary (key word/s, layer two)

**Family:** 3-two-component-key  
**Parent:** 0059-two-keywords-two-passes-k1-k3-word-alphabets  
**Decision:** reverted  
**Run:** 2026-10-15T20:56:59+00:00, 5.8 s, status ran  
**Time by phase:** unattributed 360 s, run 6 s, record 0 s

## In plain words

Using the table twice, first with one secret word and then with another, is the same as using a single key made by adding the two words letter by letter. If one of the words is from the puzzle itself, like KRYPTOS or ABSCISSA, the 24 known letters tell us exactly what the other word must be, letter by letter. So we only have to look it up: is it an English word, read from some starting letter? We try every puzzle word and every dictionary word.

## Walkthrough, by hand

1. Take KRYPTOS as the first word, starting at its K at place 1, and the sculpture's alphabet with Vigenere.
2. At place 22 the key must turn E into F: key value 1 on the sculpture's alphabet. KRYPTOS gives letter 22 mod 7 = 0, K = 0, so the second word's letter there is value 1, R.
3. Do this at all 24 known places. For a second word of length 8, place 22 falls on slot 21 mod 8 = 5.
4. If two known places ask different letters of one slot, no word of that length fits; if all 8 slots are fixed, look up the 8-letter string in every rotation of every 8-letter word.
5. Repeat for every puzzle word and start, every length, rule, and on scrambled coppers.

## Worked example (generated)

```
first word KRYPTOS from its K at place 1; sculpture's alphabet, Vigenere; second word of length 8

place  known  carved  key value  KRYPTOS letter  second word's letter  slot (mod 8)
   22      E       F          1               K                     R             5
   23      A       L         10               R                     C             6
   24      S       R         21               Y                     N             7
   25      T       V         18               P                     I             0
   30      H       N          5               R                     T             5
   31      E       G          2               Y                     K             6
   64      B       N         11               K                     E             7

slots asked for two different letters: [0, 1, 2, 3, 4, 5, 6, 7]
```

## Lineage

Inherits from 0059-two-keywords-two-passes-k1-k3-word-alphabets. What changed: 0059 added two key words both taken from the puzzle. Here one word comes from the puzzle (the vocabulary, the words of K1-K3 and Sanborn's themes) and the other from the whole dictionary. Two words of lengths m and n make a key that repeats every lcm(m, n) letters, which can reach the lengths the cribs allow (KRYPTOS + ABSCISSA repeats every 56). Given the puzzle word and its starting place, the known letters force the other word at every slot it covers, so each case is a lookup among all rotations of dictionary words.

## Hypothesis (domain expert)

Scheidt: 'executed with the correct key word/s' (C5); K2 ends LAYER TWO; Vigenere applied twice with words of lengths m and n is one key k_i = a[(i + o1) mod m] + b[(i + o2) mod n] (0080 solved the free version for m, n <= 14 with no fit at 5+ checks, but long combined periods leave few checks, so only real words decide). Word a: every puzzle word of 2-30 letters (vocabulary.txt, the K1-K3 plaintext words, the extra theme words), every start o1. Word b: every dictionary word of 3-24 letters, every rotation (the start o2). For each table rule (Vigenere, Beaufort, variant; plain and cipher alphabets standard or KRYPTOS; key letters numbered on standard or KRYPTOS) the 24 known letters give b's letter at slot i mod n; a clash rejects; a fully forced b is looked up in the set of rotations. A hit decrypts all 97 letters. Ten shuffled coppers.

## Prediction

No pair fits on K4; the shuffled coppers give no or almost no hits either. Zero candidates.

## Method

1. Build the puzzle words and, for each length 3-24, the set of all rotations of dictionary words.
2. For each rule, puzzle word and start, compute the key value forced at each known place minus the puzzle word's letter there.
3. For each length n, place those values at slots (place mod n); reject a clash; if every slot is fixed, look the word up.
4. Decrypt hits.
5. Repeat on ten shuffled coppers.

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
 "family": "sum of a puzzle word and a dictionary word as the key",
 "puzzle_words": 171,
 "dictionary_rotations_by_length": {
  "3": 3381,
  "4": 18210,
  "5": 48505,
  "6": 103593,
  "7": 165214,
  "8": 238012,
  "9": 290331,
  "10": 308035,
  "11": 285593,
  "12": 245412,
  "13": 194025,
  "14": 136682,
  "15": 88830,
  "16": 54016,
  "17": 30838,
  "18": 15156,
  "19": 8132,
  "20": 3960,
  "21": 1722,
  "22": 902,
  "23": 391,
  "24": 120
 },
 "rules": 24,
 "cases_per_text": 572880,
 "fully_forced_cases_k4": 0,
 "fully_forced_cases_controls": [
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
 "k4_hits": [],
 "n_k4_hits": 0,
 "controls_hits": [
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
 "controls": "10 shuffled coppers (seed 115), identical search"
}
```

Notes: 171 puzzle words x starts x lengths 3-24 x 24 rules = 572,880 cases per text; fully forced second words: K4 0, controls [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]. Dictionary hits: K4 0, controls [0, 0, 0, 0, 0, 0, 0, 0, 0, 0].


