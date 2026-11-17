# 0272-f14.2a-0271s-flawed-settings-decided-in-full: F14.2a: 0271's 41,986 settings where repeated known letters filled the first checks, decided in full (repeated-letter checks tested directly, the index on informative checks only), K4 against the same 50 shuffles, plants on those settings

**Family:** 14-scheidt-mask-keyed-by-words  
**Parent:** 0271-f14.2-a-remembered-route-plus-two-dictionary-keyword-alphabets  
**Decision:** reverted  
**Run:** 2026-11-17T12:10:53+00:00, 190.9 s, status ran  
**Time by phase:** design 14 s, implement 143 s, test 42 s, run 191 s, record 0 s

## In plain words

The last run tested about 1.4 million recipes: shuffle the message through a grid, then encipher it with a table whose two alphabets are scrambled by English words and a key word. A shortcut in the code skipped about 3 in 100 recipes: those where the first known letters to be compared were the same letter twice, which says nothing about the alphabets. The true recipe would always pass those comparisons, so it could have hidden there. This run tests exactly those recipes, comparing only the letters that say something, on K4 and the same 50 scrambled copies.

## Walkthrough, by hand

1. Take one recipe: a grid move, before or after the table, and a key length.
2. Follow the 24 known letters to their carved places and key slots.
3. Two known letters in one slot that are the same letter (E and E) must sit over the same carved letter; if not, the recipe is out for every alphabet.
4. Two different known letters in one slot must be as far apart on the plain alphabet as their carved letters are on the cipher alphabet: use only these to pair up the word-scrambled alphabets.
5. For each pair that passes every comparison, read off the key and look for a word that gives it.
6. Repeat for the 50 scrambled copies and compare.

## Worked example (generated)

```
F14.2a: 0271's flawed settings, every check tested.

  setting    a grid move, before or after the table, and a key length (41,986 of them)
  repeats    two known E's in one key slot must sit over one carved letter; that holds for every alphabet or none
  index      only checks between different known letters pair up the word-scrambled alphabets
  key word   each fitting pair forces the key; a word of the key's length must give it
  0271 keyed on the first six checks, repeats included: three repeats left too few, and it counted instead of testing.
```

## Lineage

Inherits from 0271-f14.2-a-remembered-route-plus-two-dictionary-keyword-alphabets. What changed: F14.2a, the rerun of 0271's flaw. 0271 keyed its alphabet-pair index on the first six same-slot checks. A check whose two known letters are the same (E with E) has gap 0 on every plain alphabet, so it holds for every pair when the carved letters are equal and for none when they differ: it carries no information about the alphabets. Where three or more of the first six were such checks, the index keyed on three or fewer informative checks, more than LIST_CAP (2 million) pairs passed, and 0271 counted them without testing the remaining checks and never ran the key-word step. Here: repeated-letter checks are tested directly (equal carved letters, else no pair fits), the index is keyed on the first six informative checks, the rest are verified, then 0271's key-word step unchanged. Only the 41,986 affected settings (text-independent: the first six checks hold three or more repeats) are run; 0271's code is used unchanged for everything else, from its frozen attack.py. Restarted from scratch after the first start (2026-11-05) hung: each job cached every setting's 40 MB index across the 51 texts, the 32 workers ran the machine out of memory, and the pool waited for killed workers; now each job loops settings outside and texts inside, holding one index at a time (same counts).

## Hypothesis (domain expert)

F14 (Scheidt's mask keyed by words; C4(a), C5; 03-scheidt-said.md 'masked the English language', 'executed with the correct key word/s') with Sanborn's matrix step (C1(a): 'I used a matrix code, and then... this [tableau]'): a type-1 move of 0129's library before or after a Quagmire IV table whose alphabets are dictionary keyword alphabets, keyed by a repeating word. 0271 searched all 1,448,304 (move, order, key length) settings but, through the flaw above, left 41,986 of its 1,363,532 listed settings undecided; a true setting always passes its repeated-letter checks, so it is exactly where the flaw would hide the answer. These settings are decided here as 0271 decided the rest: pairs of the 208,064 alphabets (0244's list: 0109's dictionary keyword alphabets plus standard and KRYPTOS) fitting every check exactly; where 5 or more checks are informative (38,203 settings; chance pairs 4.3 x 10^10 / 26^c per form), every fitted pair's forced key matched against every rotation of every dictionary and puzzle word of the key's length, numbered on standard or KRYPTOS (or the pair's own alphabets when 20 or fewer fit), any shift; settings with 4 or fewer informative checks (3,783) counted only, as 0271 counted its few-check settings. Prior attempts (reports/Kryptos K4 prior attempts database.md): a move with two dictionary keyword alphabets is not covered anywhere. Clue entries C1(a), C4(a), C5, C27(c).

## Prediction

No key word on K4; K4's fitting-setting counts per (order, length, form) inside the 50 shuffles' range; K4's A10 setting (route 'two turns cw 17,95 inverse') fits no pair once its 11 informative checks are all tested; plants on these settings missed by 0271's code and found by this one. Zero candidates kept.

## Method

1. Settings: every (move, order, key length) of 0271 with 5 or more same-slot checks whose first six checks hold three or more with equal known letters: 41,986, the same for every text.
2. Per text and setting: a repeated-letter check needs equal carved letters, else no pair fits; the informative checks (different known letters) are keyed into 0271's index (first six), the rest verified on the candidate pairs.
3. Settings with 5+ informative checks: fitted pairs listed and 0271's key-word step run on them; 4 or fewer: pairs counted.
4. Texts: K4 and 0271's 50 shuffles (seed 1420, the same texts). Plants: 12 English messages with the known words, enciphered on random settings of this list (5+ informative checks) with two random dictionary alphabets and a dictionary key word, 4 per length band 6-10, 11-18, 19-24 where the list has them; each searched with 0271's code and with this one.
5. Self-checks: on 300 random unaffected settings the fixed test gives 0271's counts on K4 and two shuffles; K1 through the identity move.
6. Verdict: K4's fitting settings and key-word matches per (order, length, form) ranked among the shuffles; key-word readings submitted as candidates.

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
 "item": "F14.2a",
 "settings": 41986,
 "settings_5plus_informative": 38203,
 "settings_4_or_fewer_informative": 3783,
 "of_0271_listed": 1363532,
 "routes": 27852,
 "alphabets": 208064,
 "forms": [
  "added",
  "Beaufort"
 ],
 "key_word_lengths": [
  1,
  24
 ],
 "key_numbering": "standard or KRYPTOS (and the pair's own alphabets when 20 or fewer pairs fit), any shift",
 "selfcheck_unaffected_settings_agree": "1800/1800",
 "k4_a10_setting_0271_vs_fixed": {
  "two turns cw 17,95 inverse/V": {
   "checks": 14,
   "informative": 11,
   "0271_count": 3476236,
   "fixed_count": 0
  },
  "two turns cw 17,95 inverse/B": {
   "checks": 14,
   "informative": 11,
   "0271_count": 2590349,
   "fixed_count": 0
  }
 },
 "per_class": {
  "A4B": {
   "settings": 39,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A4V": {
   "settings": 39,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A5B": {
   "settings": 152,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A5V": {
   "settings": 152,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A6B": {
   "settings": 185,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A6V": {
   "settings": 185,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A7B": {
   "settings": 328,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A7V": {
   "settings": 328,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A8B": {
   "settings": 495,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A8V": {
   "settings": 495,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A9B": {
   "settings": 3193,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A9V": {
   "settings": 3193,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A10B": {
   "settings": 631,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A10V": {
   "settings": 631,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A11B": {
   "settings": 915,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A11V": {
   "settings": 915,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A12B": {
   "settings": 674,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A12V": {
   "settings": 674,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A13B": {
   "settings": 612,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A13V": {
   "settings": 612,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A14B": {
   "settings": 562,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A14V": {
   "settings": 562,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A15B": {
   "settings": 457,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A15V": {
   "settings": 457,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A16B": {
   "settings": 258,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A16V": {
   "settings": 258,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A17B": {
   "settings": 278,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A17V": {
   "settings": 278,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A18B": {
   "settings": 599,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A18V": {
   "settings": 599,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A19B": {
   "settings": 171,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A19V": {
   "settings": 171,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A20B": {
   "settings": 127,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A20V": {
   "settings": 127,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A21B": {
   "settings": 157,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 1,
   "p_at_or_above": 1.0
  },
  "A21V": {
   "settings": 157,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 1,
   "p_at_or_above": 1.0
  },
  "A22B": {
   "settings": 106,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A22V": {
   "settings": 106,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A23B": {
   "settings": 112,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A23V": {
   "settings": 112,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A24B": {
   "settings": 62,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A24V": {
   "settings": 62,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A25B": {
   "settings": 131,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A25V": {
   "settings": 131,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A26B": {
   "settings": 107,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 1,
   "p_at_or_above": 1.0
  },
  "A26V": {
   "settings": 107,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 1,
   "p_at_or_above": 1.0
  },
  "B9B": {
   "settings": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "B9V": {
   "settings": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  }
 },
 "few_informative_counted": {
  "A13B": {
   "settings": 2,
   "k4_pairs": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A13V": {
   "settings": 2,
   "k4_pairs": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A15B": {
   "settings": 37,
   "k4_pairs": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A15V": {
   "settings": 37,
   "k4_pairs": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A16B": {
   "settings": 112,
   "k4_pairs": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A16V": {
   "settings": 112,
   "k4_pairs": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A17B": {
   "settings": 175,
   "k4_pairs": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A17V": {
   "settings": 175,
   "k4_pairs": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A18B": {
   "settings": 1183,
   "k4_pairs": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A18V": {
   "settings": 1183,
   "k4_pairs": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A19B": {
   "settings": 243,
   "k4_pairs": 0,
   "copies_median": 0.0,
   "copies_max": 4084314,
   "p_at_or_above": 1.0
  },
  "A19V": {
   "settings": 243,
   "k4_pairs": 0,
   "copies_median": 0.0,
   "copies_max": 4680815,
   "p_at_or_above": 1.0
  },
  "A20B": {
   "settings": 236,
   "k4_pairs": 0,
   "copies_median": 0.0,
   "copies_max": 2665977,
   "p_at_or_above": 1.0
  },
  "A20V": {
   "settings": 236,
   "k4_pairs": 0,
   "copies_median": 0.0,
   "copies_max": 2258647,
   "p_at_or_above": 1.0
  },
  "A21B": {
   "settings": 319,
   "k4_pairs": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A21V": {
   "settings": 319,
   "k4_pairs": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A22B": {
   "settings": 354,
   "k4_pairs": 0,
   "copies_median": 0.0,
   "copies_max": 8736489,
   "p_at_or_above": 1.0
  },
  "A22V": {
   "settings": 354,
   "k4_pairs": 0,
   "copies_median": 0.0,
   "copies_max": 9426297,
   "p_at_or_above": 1.0
  },
  "A23B": {
   "settings": 274,
   "k4_pairs": 0,
   "copies_median": 0.0,
   "copies_max": 1730114,
   "p_at_or_above": 1.0
  },
  "A23V": {
   "settings": 274,
   "k4_pairs": 0,
   "copies_median": 0.0,
   "copies_max": 5549017,
   "p_at_or_above": 1.0
  },
  "A24B": {
   "settings": 307,
   "k4_pairs": 0,
   "copies_median": 0.0,
   "copies_max": 6471770,
   "p_at_or_above": 1.0
  },
  "A24V": {
   "settings": 307,
   "k4_pairs": 0,
   "copies_median": 0.0,
   "copies_max": 2107709,
   "p_at_or_above": 1.0
  },
  "A25B": {
   "settings": 295,
   "k4_pairs": 3718027,
   "copies_median": 0.0,
   "copies_max": 3444844,
   "p_at_or_above": 0.02
  },
  "A25V": {
   "settings": 295,
   "k4_pairs": 3150163,
   "copies_median": 0.0,
   "copies_max": 5292102,
   "p_at_or_above": 0.039
  },
  "A26B": {
   "settings": 246,
   "k4_pairs": 0,
   "copies_median": 0.0,
   "copies_max": 4754714,
   "p_at_or_above": 1.0
  },
  "A26V": {
   "settings": 246,
   "k4_pairs": 0,
   "copies_median": 0.0,
   "copies_max": 4894728,
   "p_at_or_above": 1.0
  }
 },
 "smallest_class_p": null,
 "classes": 48,
 "capped_settings": {
  "k4": 0,
  "copies_max": 0
 },
 "key_word_matches": {
  "k4": 0,
  "copies_median": 0.0,
  "copies_max": 0,
  "p_at_or_above": 1.0
 },
 "k4_best_readings": [],
 "plants": [
  {
   "L": 9,
   "o": "B",
   "route": "K3 rule a=6 b=3 inverse",
   "checks": 15,
   "informative": 10,
   "found_0271": true,
   "found": true
  },
  {
   "L": 9,
   "o": "B",
   "route": "two turns cw 8,81",
   "checks": 15,
   "informative": 10,
   "found_0271": false,
   "found": true
  },
  {
   "L": 9,
   "o": "B",
   "route": "two turns cw 49,52 inverse",
   "checks": 15,
   "informative": 10,
   "found_0271": false,
   "found": true
  },
  {
   "L": 9,
   "o": "A",
   "route": "two turns cw 43,45",
   "checks": 15,
   "informative": 11,
   "found_0271": false,
   "found": true
  },
  {
   "L": 11,
   "o": "A",
   "route": "two turns cw 10,93 inverse",
   "checks": 13,
   "informative": 10,
   "found_0271": false,
   "found": true
  },
  {
   "L": 13,
   "o": "A",
   "route": "K3 rule a=12 b=23",
   "checks": 11,
   "informative": 6,
   "found_0271": false,
   "found": true
  },
  {
   "L": 12,
   "o": "A",
   "route": "K3 rule a=90 b=36 inverse",
   "checks": 13,
   "informative": 10,
   "found_0271": true,
   "found": true
  },
  {
   "L": 12,
   "o": "A",
   "route": "K3 rule a=82 b=70",
   "checks": 12,
   "informative": 9,
   "found_0271": false,
   "found": true
  },
  {
   "L": 24,
   "o": "A",
   "route": "K3 rule a=15 b=70",
   "checks": 10,
   "informative": 7,
   "found_0271": false,
   "found": true
  },
  {
   "L": 19,
   "o": "A",
   "route": "K3 rule a=8 b=82",
   "checks": 10,
   "informative": 7,
   "found_0271": false,
   "found": true
  },
  {
   "L": 19,
   "o": "A",
   "route": "two turns cw 77,23",
   "checks": 9,
   "informative": 5,
   "found_0271": false,
   "found": true
  },
  {
   "L": 19,
   "o": "A",
   "route": "two turns cw 36,44",
   "checks": 10,
   "informative": 6,
   "found_0271": true,
   "found": true
  }
 ],
 "plants_found": 12,
 "plants_found_by_0271": 3,
 "plants_total": 12,
 "texts": 51,
 "exhaustive": true,
 "core_seconds": 1352,
 "compute_seconds": 127,
 "resumed_units": 0,
 "cost_estimate": "41,986 settings x 51 texts at 0271's rate (about 0.008 core-s per setting and text) plus one index per setting: about 5-6 core-hours; AWS 32 cores about 15 min, under $0.30"
}
```

Notes: F14.2a: 0271's 41,986 flawed settings decided in full (38,203 with 5+ informative checks); key-word matches K4 0, copies median 0.0, max 0; smallest per-class p None over 48 classes; plants found 12/12 (0271's code: 3); K4's A10 setting: {'two turns cw 17,95 inverse/V': {'checks': 14, 'informative': 11, '0271_count': 3476236, 'fixed_count': 0}, 'two turns cw 17,95 inverse/B': {'checks': 14, 'informative': 11, '0271_count': 2590349, 'fixed_count': 0}}.


