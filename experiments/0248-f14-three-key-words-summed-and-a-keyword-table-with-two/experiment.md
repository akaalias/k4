# 0248-f14-three-key-words-summed-and-a-keyword-table-with-two: F14.6a: three puzzle key words summed on the sculpture's tables, and a puzzle keyword table with a puzzle word plus a dictionary word summed; the known letters force the last word, looked up among every rotation; K4 against 50 shuffles, plants of both forms

**Family:** 14-scheidt-mask-keyed-by-words  
**Parent:** 0115-a-puzzle-word-plus-any-english-word  
**Decision:** reverted  
**Run:** 2026-10-28T04:15:34+00:00, 178.3 s, status ran  
**Time by phase:** unattributed 242 s, run 178 s, record 0 s

## In plain words

Using the sculpture's table three times, each time with a different remembered word, is the same as using it once with a key made by adding the three words letter by letter. If we guess the first two words, the clue words tell us exactly what the third must be, so we only need to look it up. We also try a table scrambled by one puzzle word with a key made of two words. Shuffles of K4 go through the same search.

## Walkthrough, by hand

1. Pick a rule of the table and two puzzle words with their starting letters, say KRYPTOS from K and ABSCISSA from A.
2. At each known place work out the key letter the table needs, and take off the two words' letters there.
3. What is left at each known place is the third word's letter at that place; places a word-length apart must agree.
4. If they agree for some length, read the third word off and look it up among the puzzle words, from every starting letter.
5. Repeat for every pair, rule and length, and for the shuffles of K4.

## Worked example (generated)

```
Three words summed on the KRYPTOS table (Vigenere): KRYPTOS from K, ABSCISSA from A; the third word forced

place  known  carved  key value  KRYPTOS  ABSCISSA  third word's letter
   22      E       F          1        K         S                   U
   23      A       L         10        R         S                   P
   24      S       R         21        Y         A                   F
   25      T       V         18        P         A                   B
   26      N       Q          1        T         B                   I
   64      B       N         11        K         A                   T
   65      E       Y         17        R         A                   C

Places a word-length apart must ask the same letter; the forced word is looked up from every start.
```

## Lineage

Inherits from 0115-a-puzzle-word-plus-any-english-word. What changed: F14.6a (issue #93; reports/f14.6-grammar.md forms 8 and 11). 0059 summed two puzzle words, 0115 a puzzle word and a dictionary word, both on the standard and KRYPTOS tables only. Form 8: three puzzle words (171, every start) summed, 24 rules; for every pair of the first two (with starts) the 24 known letters force the third at the slots they cover, looked up among every rotation of every puzzle word of that length (2-30; for lengths with slots no known place covers, matched on the covered slots). Form 11: a keyword-mixed alphabet from a puzzle word (170) on the plain side, the cipher side or both, with a puzzle word plus a dictionary word (3-24) summed as the key: 5,100 table setups x 1,085 puzzle-word starts, the dictionary word forced and looked up as 0115.

## Hypothesis (domain expert)

Scheidt: 'building layers... mix and match' (2015), 'key word/s' (C5), keys from parts (his key-splitting habit); C20(a) 'layer two' as further passes; C4(a) a keyword-alphabet mask. Three passes over the table with three remembered words is one table with the summed key (period lcm of the lengths, often beyond 97), so no periodic test sees it, but the known letters force the last word once the others are guessed. Pre-registered: no setting fits K4 beyond the shuffles' rate (counts of forced-word hits per form, K4 against 50 shuffles, flag at p < 0.05/2); a fit is decrypted and judged by the gates. A plant of each form (Carter, keys drawn from the same lists) is found when its own keys come back.

## Prediction

Form 8: no hit on K4, a few or none on shuffles. Form 11: no hit on K4, as the shuffles. Plants 8 of 8 per form.

## Method

1. Puzzle words: 0115's 171 (every start: 1,085); keyword alphabets of the puzzle words: 170; dictionary rotations of 3-24 letters (0115).
2. Form 8: 24 rules (Vigenere, variant, Beaufort; plain, cipher and key alphabets standard or KRYPTOS). For each rule and each pair of puzzle-word starts, the forced remainder at the 24 known places; for each length 2-30, slots must agree, and the third word is looked up.
3. Form 11: 5,100 setups (keyword alphabet W on both sides, W with standard or KRYPTOS, either side; 3 rules; key letters numbered on standard or KRYPTOS); each puzzle-word start; the dictionary word of length 3-24 forced and looked up.
4. K4 and 50 shuffles; 8 plants per form with their own known letters.
5. K4's hits decrypted in full and submitted.

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
 "item": "F14.6a (forms 8 and 11)",
 "puzzle_words": 171,
 "puzzle_word_starts": 1085,
 "puzzle_alphabets": 170,
 "form8_settings_per_text": 14139720,
 "form8_third_word_lengths": [
  2,
  30
 ],
 "form11_setups": 5100,
 "form11_dictionary_word_lengths": [
  3,
  24
 ],
 "summary": {
  "form8": {
   "k4_hits": 0,
   "copies_hits_max": 0,
   "copies_hits_median": 0.0,
   "copies_with_any": 0,
   "p": 1.0
  },
  "form11": {
   "k4_hits": 0,
   "copies_hits_max": 0,
   "copies_hits_median": 0.0,
   "copies_with_any": 0,
   "p": 1.0
  }
 },
 "flag_alpha": 0.025,
 "plants_found": {
  "form8": 8,
  "form11": 8
 },
 "plants_per_form": 8,
 "k4_hits": {
  "form8": [],
  "form11": []
 },
 "texts": 67,
 "copies": 50,
 "exhaustive": true,
 "compute_seconds": 89
}
```

Notes: form 8 (three puzzle words): K4 0 hits, shuffles max 0; form 11 (puzzle table, puzzle + dictionary word): K4 0, shuffles max 0; plants {'form8': 8, 'form11': 8}


