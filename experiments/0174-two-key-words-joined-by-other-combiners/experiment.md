# 0174-two-key-words-joined-by-other-combiners: F3.1: a puzzle word and a dictionary word joined by a combiner other than plain addition: through a table on a third, keyword-mixed alphabet, or by multiplication

**Family:** 3-two-component-key  
**Parent:** 0115-two-key-words-added  
**Decision:** reverted  
**Run:** 2026-10-16T23:45:53+00:00, 4.6 s, status ran  
**Time by phase:** implement 0 s, test 0 s, run 5 s, record 0 s

## In plain words

Scheidt's professional habit is a key built from two parts joined by a rule. We already tried two secret words added together letter by letter. Here the rule for joining them changes: the words are combined through a table made from a third word's alphabet, or their letter numbers are multiplied. For each first word from the puzzle, the 24 known letters then dictate the second word letter by letter; we check whether any real English word fits, and compare with scrambled copies of the carved text.

## Walkthrough, by hand

1. Take the sculpture's table (KRYPTOS alphabet, Vigenere) and number letters by the alphabet mixed from the word BERLIN: B=0, E=1, R=2, L=3, I=4, N=5, A=6 and so on.
2. At each known place, the table gives the key value: carved place minus known place.
3. Write the first word, say PALIMPSEST, under the message from some letter, and number its letters the same way.
4. The second word's number at that place is the key value minus the first word's number (or, for multiplication, the number that times the first word's number gives the key value).
5. If the second word repeats every n letters, places n apart must ask for the same letter.
6. When every letter of the second word is forced, look it up in the dictionary, in every rotation.
7. Do the same on scrambled copies of the carved text.

## Worked example (generated)

```
numbering by the alphabet mixed from BERLIN: BERLINACDFGHJKMOPQSTUVWXYZ
sculpture's table (KRYPTOS alphabet, Vigenere); first word PALIMPSEST from its P at place 1; second word of length 8

place  known  carved  key value  first letter (number)  second word's number  slot (mod 8)
   22      E       F          1                  A (6)                    21             5
   23      A       L         10                  L (3)                     7             6
   24      S       R         21                  I (4)                    17             7
   25      T       V         18                 M (14)                     4             0
   30      H       N          5                 T (19)                    12             5
   31      E       G          2                 P (16)                    12             6
   64      B       N         11                  I (4)                     7             7

slots asked for two different numbers: [0, 1, 2, 3, 4, 5, 6, 7]: this pair is dead
```

## Lineage

Inherits from 0115-two-key-words-added. What changed: F3.1. 0115 tested two key words added letter by letter, with letters numbered on the standard or KRYPTOS order. Here the combiner changes: (a) the two words are joined through a table built on a third alphabet, the keyword-mixed alphabet of any of the 62 vocabulary words, which numbers both words' letters (so the combined key is a + b on that numbering); (b) the two words' numbers are multiplied mod 26, on the standard, KRYPTOS or any vocabulary numbering. Everything else as 0115: first word any puzzle word from every start, second word any dictionary word of 3-24 letters in every rotation, 12 table rules, exact, ten scrambled coppers.

## Hypothesis (domain expert)

C5(b) ('executed years later when used with the correct key word/s', Scheidt 2011 via Bean, knowledge/sources/bean-2021-cryptodiagnosis-of-k4.txt and 03-scheidt-said.md), C6 (Scheidt's constructive key management: a working key built from splits through a combiner, knowledge/07-people.md), F3 family. Model: carved = T(plain, k_i) for one of 12 table rules (Vigenere, Beaufort, variant; plain and cipher alphabets standard or KRYPTOS), key value k_i = g(N(a[(i + o) mod m]), N(b[i mod n])) with N a numbering of letters (standard, KRYPTOS, or the keyword-mixed alphabet of a vocabulary word: 64) and g in {addition (new only for the 62 mixed numberings), multiplication mod 26}. a: every puzzle word (0115's list: vocabulary, K1-K3 plaintext words, theme words), every start o. The 24 known letters force k at their places; g^-1 gives b's number (multiplication: all solutions of a x = k mod 26, none when gcd fails); b repeating with period n must agree within each slot; a fully forced b (or, for multiplication, every b allowed by the slot sets) is looked up among the rotations of dictionary words of length n (kryptos/data/words.txt). Exact.

## Prediction

No pair fits on K4 under either combiner; the coppers give no or almost no dictionary hits either (0115 had none on K4). Multiplication leaves more consistent cases than addition (zero divisors make b ambiguous), at the coppers' rate. Zero candidates, or only candidates inside the coppers' hit counts.

## Method

1. Build the puzzle word list (0115's) and the 64 numberings.
2. For each text (K4, ten coppers), table rule, numbering, combiner, first word and start: the forced key value at each known place, then the second word's number (or numbers) there.
3. For each length 3-24: slot agreement; fully forced second words looked up among dictionary rotations; for multiplication with ambiguous slots, dictionary rotations matched against the slot sets.
4. Count consistent cases and hits per text; decrypt K4's hits.

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
 "family": "two key words joined by a combiner other than addition on the std/KRYPTOS numbering",
 "combiners": {
  "add": "a + b on a keyword-mixed numbering of a vocabulary word (new numberings; std/KRY were 0115)",
  "mul": "a x b mod 26 on std, KRYPTOS or any vocabulary numbering"
 },
 "numberings": 63,
 "puzzle_words": 171,
 "table_rules": 12,
 "second_word_lengths": [
  3,
  24
 ],
 "cases_per_text": {
  "add": 17472840,
  "mul": 18045720
 },
 "consistent_k4": {
  "add": 0,
  "mul": 0
 },
 "consistent_controls": {
  "add": [
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
  "mul": [
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
  ]
 },
 "fully_forced_k4": {
  "add": 0,
  "mul": 0
 },
 "fully_forced_controls": {
  "add": [
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
  "mul": [
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
  ]
 },
 "too_open_k4": {
  "add": 0,
  "mul": 0
 },
 "too_open_controls": {
  "add": [
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
  "mul": [
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
  ]
 },
 "hits_k4": {
  "add": 0,
  "mul": 0
 },
 "hits_controls": {
  "add": [
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
  "mul": [
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
  ]
 },
 "plants": [
  {
   "key": {
    "combiner": "mul/vig/kry/kry/mix:BERLIN",
    "word1": "PALIMPSEST",
    "start1": 3,
    "word2": "GARDEN",
    "rotation2": 0
   },
   "found": true
  },
  {
   "key": {
    "combiner": "add/beau/std/kry/mix:BERLIN",
    "word1": "PALIMPSEST",
    "start1": 3,
    "word2": "SHADOW",
    "rotation2": 2
   },
   "found": true
  }
 ],
 "k4_hits": {
  "add": [],
  "mul": []
 },
 "seconds": 4,
 "controls": "10 shuffled coppers (seed 1740), identical search",
 "exhaustive": true
}
```

Notes: add: consistent K4 0 (coppers 0-0), dictionary hits K4 0 (coppers 0-0); mul: consistent K4 0 (coppers 0-0), dictionary hits K4 0 (coppers 0-0); plants found 2/2


