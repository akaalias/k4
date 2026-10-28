# 0246-f14-duress-reading-running-english-key-judged-by-mix8m-and-the-judge: F14.3: the duress reading, a running key from English text with an English message: 0125's 3.7 million forced keys on the dictionary tables (and the sculpture's), ranked by MIX8m instead of quadgrams, the best read by the blind judge; K4 against 50 shuffles, 0125's 20 plants

**Family:** 14-scheidt-mask-keyed-by-words  
**Parent:** 0125-forced-key-as-running-english-on-dictionary-alphabets  
**Decision:** reverted  
**Run:** 2026-10-28T03:53:12+00:00, 251.2 s, status ran  
**Time by phase:** unattributed 384 s, run 251 s, record 0 s

## In plain words

A trick for agents who might be captured: let the secret key be an ordinary passage of a book, so that a captor who forces you to give it up gets something that looks harmless. If K4 was made that way, then where we know the message, working backwards gives 24 letters of that passage, which should read as English. An earlier test scored them with a simple four-letter-group count; here we use our best English model and then ask the language model judge, comparing K4 with shuffles of its own letters treated the same way.

## Walkthrough, by hand

1. Take a table, say one built on the word HOLOZOIC on the plain side with the standard alphabet on the cipher side.
2. At place 22 the message has E and the copper F: find which key letter turns E into F on that table.
3. Do this at all 24 known places: 13 key letters for 22-34 and 11 for 64-74.
4. If the key were a passage of a book, these would be two pieces of English: score them with the English model.
5. Do it for every table and way of reading the table, keep the best, and compare K4's best with what shuffles of K4 reach; ask the judge to read the best pieces.

## Worked example (generated)

```
The key letters forced at the known places on the sculpture's own table (Vigenere, KRYPTOS alphabet both sides):

place  known  carved  key letter
   22      E       F           R
   23      A       L           D
   24      S       R           U
   25      T       V           M
   64      B       N           E
   65      E       Y           L
   66      R       P           Y

If the key were a passage of a book, the 13 letters at 22-34 and the 11 at 64-74 would read as English.
```

## Lineage

Inherits from 0125-forced-key-as-running-english-on-dictionary-alphabets. What changed: F14.3 (issue #93). 0125 asked whether the 24 key letters forced at the known places read as English, scored by quadgrams (power 11 of 20 plants); 0221 (A6.1) rejudged only each text's quadgram-best reading. Here the same exhaustive space (208,062 dictionary keyword tables x 3 configurations x 3 rules x 2 key alphabets, plus the 24 settings of the sculpture's own standard and KRYPTOS tables) is ranked by F13.3's MIX8m (1.95 bits per letter against the quadgrams' 1.75): each rule's 300 quadgram-best forced keys rescored by MIX8m over the two windows, and the 3 MIX8m-best of each text read by the blind judge, window by window.

## Hypothesis (domain expert)

Scheidt's duress codes (03-scheidt-said.md, 2011: 'similar to what would be provided agents or pilots in case of capture'; 2015: 'I used to make those codes, for captured people'; Gillogly 2013 on 'multi-layered ciphers for which you can give up a key to the enemy that produces credible plaintext'; C5(c), C6). A running key that is itself English text gives a captor a believable key; C5 'a named text' read for any text. 0125 closed F1.3 by quadgrams; A6.1 held it; the stronger model can only sharpen the ranking. Model: c = C[P(p) + k] (and the variant and Beaufort rules), k read through the standard or the table's keyword alphabet; the 24 forced key letters (13 at 22-34, 11 at 64-74) would be two windows of English. Pre-registered: statistic = the best MIX8m log2 probability over the two windows; K4 flags at p < 0.05 against 50 shuffles; the judge's mean score over the two windows of each text's MIX8m-best key, K4 counts only above every shuffle. A plant (0125's: Carter's text as the key) is found when its statistic is above every shuffle of K4's (as 0125).

## Prediction

Plants found more often than 0125's 11 of 20 (about 15 of 20). K4 inside its shuffles by MIX8m (p above 0.05) and by the judge (not above every shuffle). F14.3 closes as sampled.

## Method

1. 0125's tables (its frozen alphabets(): 208,062 dictionary keyword alphabets), configurations W-std, std-W, W-W, rules vig/var/beau, key alphabet standard or W; plus the sculpture's tables (plain and cipher standard or KRYPTOS, key alphabet standard or KRYPTOS, 3 rules).
2. Every forced key (24 letters) scored by quadgrams over the two windows (as 0125); the 300 best per rule rescored by MIX8m, each window from its own start; the 300 best overall kept.
3. Statistic: the best MIX8m; K4 ranked among 50 shuffles (seed 246).
4. The 3 MIX8m-best keys of K4, every shuffle and every plant read by the blind judge, window by window (in one call, blind to which is which); judge score of a text = the mean over its two windows of its MIX8m-best key.
5. 0125's 20 plants (its frozen make_plants with its seed) through the same search.

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
 "item": "F14.3",
 "tables": 1248380,
 "readings_per_text": 3745140,
 "space": "0125's 208,062 dictionary keyword tables x 3 configurations x 2 key alphabets, plus the sculpture's 4 table pairs x 2 key alphabets; 3 rules",
 "ranking": "quadgrams over both windows (as 0125), the 300 best per rule rescored by MIX8m (0233), window by window",
 "texts": 71,
 "copies": 50,
 "k4_best": [
  -103.30804578225288,
  -5.4726939611189245,
  "ILLTRICKFRKACMUCHUNKMUNT",
  "CATBIRD std-W key W",
  "vig"
 ],
 "k4_p_mix8m": 0.5882,
 "copies_best_mix8m_max": -95.7597394916042,
 "copies_best_mix8m_median": -102.48298306492792,
 "plants_found_mix8m": 20,
 "plants": 20,
 "plant_truth_rank_in_top300": [
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1
 ],
 "plant_best_mix8m": [
  -68.6357726830841,
  -56.62666375891124,
  -60.81236989274136,
  -88.27032597325928,
  -88.13248634127119,
  -78.6470380400131,
  -82.35692586962026,
  -57.18899927873768,
  -66.33930078558808,
  -71.65268280586108,
  -86.46312613302408,
  -68.34137789556496,
  -70.08654207299185,
  -66.7556256002935,
  -65.84425636568659,
  -70.36608692302698,
  -84.04568479394356,
  -65.50101677746365,
  -62.6798525535589,
  -61.89857185581242
 ],
 "judge_calls_estimated": 426,
 "judge_none": 0,
 "judge_k4": 18.5,
 "judge_copies_max": 46.0,
 "judge_copies_median": 10.0,
 "judge_k4_above_every_copy": false,
 "judge_plants": [
  55.0,
  58.5,
  60.0,
  33.5,
  37.0,
  26.5,
  45.0,
  62.5,
  62.0,
  42.0,
  52.5,
  43.5,
  37.5,
  51.0,
  55.0,
  53.5,
  62.0,
  33.5,
  51.0,
  63.5
 ],
 "judge_plants_found": 12,
 "k4_top3": [
  [
   -103.30804578225288,
   -5.4726939611189245,
   "ILLTRICKFRKACMUCHUNKMUNT",
   "CATBIRD std-W key W",
   "vig"
  ],
  [
   -106.71352372050777,
   -5.564993195592273,
   "RTHCLMANFSEAGANAMIXOPEDC",
   "SKIAMETRY W-W key std",
   "beau"
  ],
  [
   -107.10868948191133,
   -5.452160407274088,
   "TSBIZKSLOSTAKRESTINTPSIA",
   "POETHOOD W-W key std",
   "var"
  ]
 ],
 "exhaustive": true,
 "compute_seconds": 227
}
```

Notes: K4 best MIX8m -103.3 bits, p 0.588 against 50 shuffles; plants found 20/20 by MIX8m; judge K4 18.5 against copies max 46.0, plants above every copy 12/20


