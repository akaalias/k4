# 0271-f14.2-a-remembered-route-plus-two-dictionary-keyword-alphabets: F14.2: every type-1 move of 0129's library (27,852), both orders, key lengths 1-26, then a table with two dictionary keyword alphabets (208,064 each, standard and KRYPTOS among them) and a repeating key word; K4 against 50 shuffles, plants

**Family:** 14-scheidt-mask-keyed-by-words  
**Parent:** 0244-f14-two-dictionary-keyword-alphabets-and-a-key-word  
**Decision:** reverted  
**Run:** 2026-11-05T14:19:45+00:00, 88.2 s, status ran  
**Time by phase:** unattributed 27054 s, run 88 s, record 0 s

## In plain words

Sanborn said he wrote the message into a grid and read it out another way, then used the cipher table. Scheidt said the English was disguised first, and that the system is worked with key words. Here the grid step is any of about 28,000 ways of reading a grid, and both alphabets of the table are scrambled by English words. For each recipe, the 24 known letters tell us exactly which pairs of word-scrambled alphabets could work; then we check whether the key they force is a word. Fifty scrambled copies of K4 go through the same test, so we know how many matches chance gives.

## Walkthrough, by hand

1. Write the message in rows of 9 and read the columns in a key word's order (one of the moves).
2. For a key length, say 12, follow each of the 24 known letters to its carved place and its key slot.
3. Two known letters in one slot must be the same distance apart on the plain alphabet as their carved letters are on the cipher alphabet.
4. File every word-scrambled alphabet by those distances, plain side and cipher side, and pair up the matching files.
5. For each matching pair, read off the key letters the known letters force and look for a word that gives them.
6. Do the same for 50 scrambled copies of K4 and compare the counts.

## Worked example (generated)

```
F14.2: a remembered route, then a table with two word-scrambled alphabets and a key word.

  move       write the message in rows, read the columns in a key word's order (one of 27,852 moves)
  checks     two known letters that share a key slot after the move: their gap on the plain alphabet
             equals their carved letters' gap on the cipher alphabet (added form)
  index      every keyword alphabet filed by its gaps, plain side and cipher side; matching files pair up
  key word   the pair forces the key at the covered slots; a word of the key's length must give it
  50 scrambled copies of K4 through the same steps give chance's counts.
```

## Lineage

Inherits from 0244-f14-two-dictionary-keyword-alphabets-and-a-key-word. What changed: F14.2, the full run Alexis decided (#102). 0244's exact pair index (every plain and cipher keyword alphabet matched through the differences the known letters force) run after or before every move of 0129's type-1 library, at every key length 1-26, both forms. Faster than the design's estimate: which known places share a key slot depends only on the setting, so the plain-side index is built once per setting and K4 and its 50 shuffles are looked up in it; a difference table D[x, y] over all alphabets makes each check one contiguous row. Checked: with the identity move it reproduces 0244's fit counts on K4 (desk, 2026-11-04).

## Hypothesis (domain expert)

F14 (Scheidt's mask keyed by words; C4(a), C5; 03-scheidt-said.md 'masked the English language', 'executed with the correct key word/s') with Sanborn's matrix step first or last (C1(a): 'I used a matrix code, and then... this [tableau]'; 'double matrixes'): a remembered route (keyword columnar, K3's rule, turns, rail fence, grid paths: 0129's 27,852 distinct moves and their inverses) and a Quagmire IV table whose alphabets are keyword alphabets from the dictionary, keyed by a repeating word. F6.1 and F6.2 decided free alphabets around these moves at the copies' rate; keyword alphabets cost about 35 bits for the pair, so the known letters decide them where 5 or more same-slot checks fall (chance pairs 4.3 x 10^10 / 26^c per form: 3,600 at c = 5, 140 at 6, 5 at 7, 0.2 at 8). A fitted pair forces the key at the covered slots; a dictionary or puzzle word of length L (any rotation, numbered on standard or KRYPTOS, any shift) must give it. Settings with 4 or fewer checks are counted only (chance pairs 10^5 and more). Prior attempts (reports/Kryptos K4 prior attempts database.md): moves with periodic keys on the standard and KRYPTOS tables (keithadler, nitsuah, Zekios) and free-alphabet Quagmires without a move; a move with two dictionary keyword alphabets is not covered. Clue entries C1(a), C4(a), C5, C27(c).

## Prediction

K4's fitting pairs and key-word matches per (order, key length) inside the 50 shuffles' range; plants found at every band; no reading English. Zero candidates kept.

## Method

1. Settings: 0129's route library (27,852 moves) x order (A move then table, B table then move) x key length 1-26; for each, the 24 known places' carved places and key slots, and the same-slot checks (first place of a slot against each other).
2. Per setting and form, the plain-side key of every alphabet on the first min(c, 6) checks, sorted; per text, the cipher-side keys looked up (a bitmap first, then exact), the remaining checks verified on the candidate pairs. c <= 4: the number of fitting pairs counted exactly, not listed.
3. Key word (L <= 24, 3 or more covered slots): each fitted pair's forced key differences matched against every rotation of every dictionary and puzzle word of length L, numbered on standard or KRYPTOS (and on the pair's own alphabets when 20 or fewer pairs fit); a match fixes the whole key and so the reading.
4. Texts: K4 and 50 shuffles (seed 1420), every setting; 12 plants (English with the known words, a random move, order, two dictionary alphabets and a dictionary key word; 4 in each length band 6-10, 11-18, 19-24, on settings with 5 or more checks), each searched at its own setting with the same code.
5. Verdict: K4's fitting pairs (settings with 5+ checks) and key-word matches per (order, length) ranked among the shuffles; K4's key-word readings submitted as candidates, the shuffles' best as controls.

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
 "item": "F14.2",
 "routes": 27852,
 "orders": [
  "A move then table",
  "B table then move"
 ],
 "key_lengths": [
  1,
  26
 ],
 "forms": [
  "added",
  "Beaufort"
 ],
 "alphabets": 208064,
 "alphabet_pairs_per_setting_and_form": 43290628096,
 "settings_per_text": 1448304,
 "listed_at_checks": 5,
 "settings_listed_k4": 1363532,
 "key_word_lengths": [
  1,
  24
 ],
 "key_numbering": "standard or KRYPTOS (and the pair's own alphabets when 20 or fewer pairs fit), any shift",
 "self_check_identity_vs_0244": {
  "16/V": [
   5,
   5
  ],
  "16/B": [
   0,
   0
  ],
  "19/V": [
   0,
   0
  ],
  "19/B": [
   0,
   0
  ],
  "23/V": [
   5,
   5
  ],
  "23/B": [
   1,
   1
  ]
 },
 "per_class": {
  "A1B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A1V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A2B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 1,
   "p_at_or_above": 1.0
  },
  "A2V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A3B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 1,
   "p_at_or_above": 1.0
  },
  "A3V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 1,
   "p_at_or_above": 1.0
  },
  "A4B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 1,
   "p_at_or_above": 1.0
  },
  "A4V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A5B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 1,
   "p_at_or_above": 1.0
  },
  "A5V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 1,
   "p_at_or_above": 1.0
  },
  "A6B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 1,
   "p_at_or_above": 1.0
  },
  "A6V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 1,
   "p_at_or_above": 1.0
  },
  "A7B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 1,
   "p_at_or_above": 1.0
  },
  "A7V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 2,
   "p_at_or_above": 1.0
  },
  "A8B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 1,
   "p_at_or_above": 1.0
  },
  "A8V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 1,
   "p_at_or_above": 1.0
  },
  "A9B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 2,
   "p_at_or_above": 1.0
  },
  "A9V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 2,
   "p_at_or_above": 1.0
  },
  "A10B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 1,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 0.02
  },
  "A10V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 1,
   "copies_median": 0.0,
   "copies_max": 1,
   "p_at_or_above": 0.039
  },
  "A11B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A11V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A12B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A12V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "A13B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 2,
   "p_at_or_above": 1.0
  },
  "A13V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 1,
   "p_at_or_above": 1.0
  },
  "A14B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 6,
   "copies_median": 2.0,
   "copies_max": 7,
   "p_at_or_above": 0.098
  },
  "A14V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 2.0,
   "copies_max": 25,
   "p_at_or_above": 1.0
  },
  "A15B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 36,
   "copies_median": 32.0,
   "copies_max": 65,
   "p_at_or_above": 0.235
  },
  "A15V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 30,
   "copies_median": 33.5,
   "copies_max": 59,
   "p_at_or_above": 0.667
  },
  "A16B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 511,
   "copies_median": 513.0,
   "copies_max": 638,
   "p_at_or_above": 0.549
  },
  "A16V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 545,
   "copies_median": 510.0,
   "copies_max": 678,
   "p_at_or_above": 0.333
  },
  "A17B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 1991,
   "copies_median": 1958.0,
   "copies_max": 2359,
   "p_at_or_above": 0.431
  },
  "A17V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 1949,
   "copies_median": 1946.0,
   "copies_max": 2324,
   "p_at_or_above": 0.49
  },
  "A18B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 3445,
   "copies_median": 3053.0,
   "copies_max": 3725,
   "p_at_or_above": 0.078
  },
  "A18V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 3472,
   "copies_median": 3048.0,
   "copies_max": 3743,
   "p_at_or_above": 0.078
  },
  "A19B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 4731,
   "copies_median": 4616.0,
   "copies_max": 5258,
   "p_at_or_above": 0.392
  },
  "A19V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 4701,
   "copies_median": 4578.5,
   "copies_max": 5324,
   "p_at_or_above": 0.412
  },
  "A20B": {
   "settings_listed": 26243,
   "k4_settings_with_fit": 4366,
   "copies_median": 4117.5,
   "copies_max": 4814,
   "p_at_or_above": 0.255
  },
  "A20V": {
   "settings_listed": 26243,
   "k4_settings_with_fit": 4342,
   "copies_median": 4098.0,
   "copies_max": 4755,
   "p_at_or_above": 0.235
  },
  "A21B": {
   "settings_listed": 26366,
   "k4_settings_with_fit": 5140,
   "copies_median": 5348.5,
   "copies_max": 6192,
   "p_at_or_above": 0.706
  },
  "A21V": {
   "settings_listed": 26366,
   "k4_settings_with_fit": 5072,
   "copies_median": 5362.0,
   "copies_max": 6191,
   "p_at_or_above": 0.725
  },
  "A22B": {
   "settings_listed": 24447,
   "k4_settings_with_fit": 5503,
   "copies_median": 5382.0,
   "copies_max": 6053,
   "p_at_or_above": 0.412
  },
  "A22V": {
   "settings_listed": 24447,
   "k4_settings_with_fit": 5401,
   "copies_median": 5375.0,
   "copies_max": 6095,
   "p_at_or_above": 0.471
  },
  "A23B": {
   "settings_listed": 24535,
   "k4_settings_with_fit": 7240,
   "copies_median": 6619.5,
   "copies_max": 7979,
   "p_at_or_above": 0.157
  },
  "A23V": {
   "settings_listed": 24535,
   "k4_settings_with_fit": 7344,
   "copies_median": 6574.0,
   "copies_max": 7960,
   "p_at_or_above": 0.118
  },
  "A24B": {
   "settings_listed": 23226,
   "k4_settings_with_fit": 6853,
   "copies_median": 6365.5,
   "copies_max": 7262,
   "p_at_or_above": 0.157
  },
  "A24V": {
   "settings_listed": 23226,
   "k4_settings_with_fit": 6830,
   "copies_median": 6359.0,
   "copies_max": 7280,
   "p_at_or_above": 0.176
  },
  "A25B": {
   "settings_listed": 21230,
   "k4_settings_with_fit": 5428,
   "copies_median": 6383.5,
   "copies_max": 7503,
   "p_at_or_above": 0.98
  },
  "A25V": {
   "settings_listed": 21230,
   "k4_settings_with_fit": 5453,
   "copies_median": 6382.5,
   "copies_max": 7495,
   "p_at_or_above": 0.98
  },
  "A26B": {
   "settings_listed": 19849,
   "k4_settings_with_fit": 7681,
   "copies_median": 6603.0,
   "copies_max": 8023,
   "p_at_or_above": 0.078
  },
  "A26V": {
   "settings_listed": 19849,
   "k4_settings_with_fit": 7658,
   "copies_median": 6624.0,
   "copies_max": 8028,
   "p_at_or_above": 0.098
  },
  "B1B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "B1V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "B2B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "B2V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "B3B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 1,
   "p_at_or_above": 1.0
  },
  "B3V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 1,
   "p_at_or_above": 1.0
  },
  "B4B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "B4V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "B5B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "B5V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "B6B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "B6V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "B7B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "B7V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "B8B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "B8V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "B9B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 6,
   "p_at_or_above": 1.0
  },
  "B9V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 4,
   "p_at_or_above": 1.0
  },
  "B10B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "B10V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "B11B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "B11V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "B12B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "B12V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 0,
   "p_at_or_above": 1.0
  },
  "B13B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 2,
   "p_at_or_above": 1.0
  },
  "B13V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 1,
   "p_at_or_above": 1.0
  },
  "B14B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 1,
   "p_at_or_above": 1.0
  },
  "B14V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 1,
   "p_at_or_above": 1.0
  },
  "B15B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 118,
   "copies_median": 106.0,
   "copies_max": 136,
   "p_at_or_above": 0.255
  },
  "B15V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 88,
   "copies_median": 112.0,
   "copies_max": 144,
   "p_at_or_above": 1.0
  },
  "B16B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 2839,
   "copies_median": 2772.5,
   "copies_max": 2938,
   "p_at_or_above": 0.216
  },
  "B16V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 2802,
   "copies_median": 2771.0,
   "copies_max": 2937,
   "p_at_or_above": 0.373
  },
  "B17B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 725,
   "copies_median": 811.5,
   "copies_max": 896,
   "p_at_or_above": 0.98
  },
  "B17V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 725,
   "copies_median": 813.0,
   "copies_max": 897,
   "p_at_or_above": 0.98
  },
  "B18B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 18658,
   "copies_median": 18859.5,
   "copies_max": 19437,
   "p_at_or_above": 0.765
  },
  "B18V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 18838,
   "copies_median": 18843.0,
   "copies_max": 19386,
   "p_at_or_above": 0.529
  },
  "B19B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 119,
   "copies_median": 109.0,
   "copies_max": 136,
   "p_at_or_above": 0.235
  },
  "B19V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 108,
   "copies_median": 112.0,
   "copies_max": 151,
   "p_at_or_above": 0.588
  },
  "B20B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 1,
   "copies_median": 0.0,
   "copies_max": 2,
   "p_at_or_above": 0.275
  },
  "B20V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 2,
   "p_at_or_above": 1.0
  },
  "B21B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 1,
   "p_at_or_above": 1.0
  },
  "B21V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 0,
   "copies_median": 0.0,
   "copies_max": 1,
   "p_at_or_above": 1.0
  },
  "B22B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 150,
   "copies_median": 163.5,
   "copies_max": 201,
   "p_at_or_above": 0.824
  },
  "B22V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 186,
   "copies_median": 160.0,
   "copies_max": 208,
   "p_at_or_above": 0.137
  },
  "B23B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 18230,
   "copies_median": 18289.5,
   "copies_max": 18756,
   "p_at_or_above": 0.667
  },
  "B23V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 18215,
   "copies_median": 18285.0,
   "copies_max": 18716,
   "p_at_or_above": 0.667
  },
  "B24B": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 23286,
   "copies_median": 23149.0,
   "copies_max": 23540,
   "p_at_or_above": 0.196
  },
  "B24V": {
   "settings_listed": 27852,
   "k4_settings_with_fit": 23286,
   "copies_median": 23149.0,
   "copies_max": 23540,
   "p_at_or_above": 0.196
  }
 },
 "smallest_class_p": 0.02,
 "classes": 100,
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
   "o": "A",
   "route": "two turns cw 69,61",
   "checks": 15,
   "found": true,
   "matches_at_setting": 1
  },
  {
   "L": 7,
   "o": "B",
   "route": "K3 rule a=38 b=26 inverse",
   "checks": 17,
   "found": true,
   "matches_at_setting": 1
  },
  {
   "L": 7,
   "o": "B",
   "route": "K3 rule a=74 b=13",
   "checks": 17,
   "found": true,
   "matches_at_setting": 1
  },
  {
   "L": 10,
   "o": "A",
   "route": "K3 rule a=47 b=58 inverse",
   "checks": 16,
   "found": true,
   "matches_at_setting": 1
  },
  {
   "L": 14,
   "o": "B",
   "route": "K3 rule a=47 b=3 inverse",
   "checks": 11,
   "found": true,
   "matches_at_setting": 1
  },
  {
   "L": 15,
   "o": "A",
   "route": "two turns cw 30,94 inverse",
   "checks": 18,
   "found": true,
   "matches_at_setting": 1
  },
  {
   "L": 13,
   "o": "A",
   "route": "two turns cw 31,77 inverse",
   "checks": 13,
   "found": true,
   "matches_at_setting": 1
  },
  {
   "L": 15,
   "o": "B",
   "route": "K3 rule a=68 b=21 inverse",
   "checks": 9,
   "found": true,
   "matches_at_setting": 1
  },
  {
   "L": 19,
   "o": "A",
   "route": "two turns cw 88,51",
   "checks": 11,
   "found": true,
   "matches_at_setting": 1
  },
  {
   "L": 22,
   "o": "B",
   "route": "keyword LANGLEY (repeats dropped) inverse",
   "checks": 9,
   "found": true,
   "matches_at_setting": 3
  },
  {
   "L": 23,
   "o": "B",
   "route": "two turns cw 94,89",
   "checks": 7,
   "found": true,
   "matches_at_setting": 2
  },
  {
   "L": 21,
   "o": "A",
   "route": "columnar 47",
   "checks": 7,
   "found": true,
   "matches_at_setting": 1
  }
 ],
 "plants_found": 12,
 "plants_total": 12,
 "texts": 51,
 "exhaustive": true,
 "core_seconds": 597255,
 "compute_seconds": 11,
 "resumed_units": 697,
 "cost_estimate": "1.45 million settings x 51 texts, about 0.2 s per setting for all texts and both forms (desk 2026-11-04) plus the key-word step: about 80-120 core-hours; AWS 32 cores about 3-4 h, about $2-3"
}
```

Notes: F14.2: 27852 moves x 2 orders x 26 lengths x 2 forms, 208,064^2 keyword alphabet pairs each; key-word matches K4 0, copies median 0.0, max 0; smallest per-class p 0.02 over 100 classes; plants found 12/12.


