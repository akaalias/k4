# 0048-complete-the-key-both-alphabets-mixed-sampled: The last corner of family 1: both alphabets rebuilt from the puzzle's words, key completed at periods 27 to 29, sampled

**Family:** 1-keyed-periodic  
**Parent:** 0035-complete-the-key-mixed-alphabets-27-29  
**Decision:** reverted  
**Run:** 2026-10-15T09:57:00+00:00, 710.0 s, status ran  
**Time by phase:** design 0 s, implement 34 s, test 1 s, run 710 s, record 0 s

## In plain words

Experiments 34 and 35 filled in the few unknown letters of a secret word of length 27 to 29 and found only nonsense, with the sculpture's table and with tables rebuilt from one puzzle word on one side. The last version has both sides of the table rebuilt from puzzle words. There are too many pairs of words to finish in one sitting, so we draw pairs at random for half an hour and report how far we got.

## Walkthrough, by hand

1. Build the alphabet from PALIMPSEST: PALIMSETBCDFGHJKNOQRUVWXYZ, and use it for the message; keep KRYPTOS for the carved letters; Vigenere.
2. Period 27: position 22 is E, index 6 in the PALIMPSEST alphabet; carved F is index 11 in KRYPTOS; the key index is 5.
3. Do this for all 24 known letters; positions 22 and 49 share slot 21, but 49 is unknown, so no clash.
4. Three slots stay free.
5. Try every letter in each free slot in turn, decrypting the whole text each time, and keep the one that makes the 73 unknown letters read most like English.
6. Compare the best text's score with English, about -3.6, and with what the same game gives on shuffled letters, about -6.8.

## Worked example (generated)

```
plain alphabet PALIMPSEST/keyword PALIMSETBCDFGHJKNOQRUVWXYZ; cipher alphabet KRYPTOS; Vigenere; period 27; 3 free slots climbed

key indices [10, 20, 6, 7, 25, 1, 25, 11, 14, 11, 22, 10, 20, 1, 14, 9, 23, 21, 20, 11, 18, 6, 16, 22, 15, 4, 3]
text       VJUUWMZUZIZTJSOBQOJXSEASTNORTHEASTUNGBDGKEXCNEJTOOBAWJFNCPYJUAUBERLINCLOCKSTUMDUAEKMBJZWITWZAEBRQ
English of the free letters -8.243 (English about -3.6, noise about -6.8)
```

## Lineage

Inherits from 0035-complete-the-key-mixed-alphabets-27-29. What changed: Experiment 35 mixed one alphabet at a time. Here both the message alphabet and the carved alphabet are keyword mixings of vocabulary words, 61 x 61 pairs, drawn in random order with a fixed seed until the budget runs out; the record says how many pairs were reached. Periods 27 to 29, three restarts.

## Hypothesis (domain expert)

Experiments 34 and 35 found the key completion at periods 27-29 reads as noise under every pair with at most one keyword-mixed side. The remaining corner is both sides mixed: 3,721 pairs x 3 modes x 3 periods, about 33,000 climbs at 0.1 s each with three restarts, more than the budget allows, so pairs are visited in a fixed random order and the run stops at the clock; coverage is reported. A true periodic cipher on such a pair would give a text near -3.6 at its period; shuffled K4 gives about -6.8. Bounds: a stated fraction of the pair space, not exhaustive; the seed makes the sample reproducible and a later run can continue it.

## Prediction

Within the budget about a third of the pairs are reached. No pair and period gives a text better than -5.5 per quadgram; the best is within 0.4 of shuffled K4. Candidates pass the gates by construction but none reads as English or beats the current champion's fitness.

## Method

1. Build the alphabet pool: standard, KRYPTOS and the keyword mixing of each vocabulary word.
2. For each pair with one side standard or KRYPTOS, each mode and each period 27-29, force the 24 key slots from the cribs; skip the pair if two cribs disagree on a slot.
3. Climb the free slots by coordinate descent on the English score of the 73 non-crib letters, five restarts.
4. Keep the best text per period and submit it.
5. Repeat on one shuffle of K4 for calibration.

## Result

Candidates returned: 3. Passed all gates: 3. Best crib hits among all candidates: 24/24
(EAST 4/4, NORTHEAST 9/9, BERLIN 6/6, CLOCK 5/5).
Best loss: 3.811138054850904 (0 is solved; 10 per missed crib letter). Best fitness: -7.544626027359495. Champion before this run: 0034-complete-the-key-at-surviving-periods.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | pass | 24/24 | -7.663 | `UYUGNUWILATPSJGPEOMIFEASTNORTHEASTIAORTOOPSUPOUGHBHISCEBKRIFCSOBERLINCLOCKFWRZEIMDEXZEMBERHTJRETQ` | period 27, plain WEBSTER/keyword, cipher WORLDCLOCK/keyword, beau; 3 free slots climbed |
| 2 | pass | 24/24 | -7.877 | `ADJBNPTHULKBRUNTDELITEASTNORTHEASTYWBCIGZFRYRKWATWCULYBOLARSASWBERLINCLOCKALSKHOOJUOLBJCEGOTKPAKO` | period 28, plain SHADOW/keyword, cipher LODESTONE/keyword, varbeau; 4 free slots climbed |
| 3 | pass | 24/24 | -7.545 | `JGAFEEFGHJCJOUSTOLITIEASTNORTHEASTEHHUAODBULYMENDTRYFFLAWPKASEDBERLINCLOCKITHNDPRGADTYGABNDEDOZMS` | period 29, plain LUCID/keyword, cipher WONDERFUL/keyword, beau; 5 free slots climbed |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "periodic tableau at periods 27-29, one alphabet standard or KRYPTOS and the other keyword-mixed from the vocabulary, key completed by English climb",
 "alphabets": 63,
 "pairs_total": 3721,
 "pairs_reached": 3721,
 "coverage": 1.0,
 "periods": [
  27,
  28,
  29
 ],
 "restarts": 3,
 "climbs": 33489,
 "best_by_period": {
  "27": {
   "english": -6.355,
   "plain": "WEBSTER/keyword",
   "cipher": "WORLDCLOCK/keyword",
   "mode": "beau",
   "free_slots": 3,
   "text": "UYUGNUWILATPSJGPEOMIFEASTNORTHEASTIAORTOOPSUPOUGHBHISCEBKRIFCSOBERLINCLOCKFWRZEIMDEXZEMBERHTJRETQ"
  },
  "28": {
   "english": -6.52,
   "plain": "SHADOW/keyword",
   "cipher": "LODESTONE/keyword",
   "mode": "varbeau",
   "free_slots": 4,
   "text": "ADJBNPTHULKBRUNTDELITEASTNORTHEASTYWBCIGZFRYRKWATWCULYBOLARSASWBERLINCLOCKALSKHOOJUOLBJCEGOTKPAKO"
  },
  "29": {
   "english": -6.139,
   "plain": "LUCID/keyword",
   "cipher": "WONDERFUL/keyword",
   "mode": "beau",
   "free_slots": 5,
   "text": "JGAFEEFGHJCJOUSTOLITIEASTNORTHEASTEHHUAODBULYMENDTRYFFLAWPKASEDBERLINCLOCKITHNDPRGADTYGABNDEDOZMS"
  }
 },
 "top_ten": [
  {
   "english": -6.139,
   "period": 29,
   "plain": "LUCID/keyword",
   "cipher": "WONDERFUL/keyword",
   "mode": "beau"
  },
  {
   "english": -6.254,
   "period": 29,
   "plain": "CLOCK/keyword",
   "cipher": "RIDDLE/keyword",
   "mode": "beau"
  },
  {
   "english": -6.313,
   "period": 29,
   "plain": "WILLIAMWEBSTER/keyword",
   "cipher": "LUCID/keyword",
   "mode": "beau"
  },
  {
   "english": -6.355,
   "period": 27,
   "plain": "WEBSTER/keyword",
   "cipher": "WORLDCLOCK/keyword",
   "mode": "beau"
  },
  {
   "english": -6.401,
   "period": 29,
   "plain": "BURIED/keyword",
   "cipher": "BURIED/keyword",
   "mode": "varbeau"
  },
  {
   "english": -6.427,
   "period": 29,
   "plain": "TUTANKHAMEN/keyword",
   "cipher": "WALL/keyword",
   "mode": "vig"
  },
  {
   "english": -6.437,
   "period": 29,
   "plain": "TUTANKHAMEN/keyword",
   "cipher": "CIA/keyword",
   "mode": "varbeau"
  },
  {
   "english": -6.44,
   "period": 29,
   "plain": "HILL/keyword",
   "cipher": "BURIED/keyword",
   "mode": "beau"
  },
  {
   "english": -6.445,
   "period": 29,
   "plain": "ABSCISSAE/keyword",
   "cipher": "NORTH/keyword",
   "mode": "vig"
  },
  {
   "english": -6.475,
   "period": 29,
   "plain": "WELTZEITUHR/keyword",
   "cipher": "HILL/keyword",
   "mode": "beau"
  }
 ],
 "shuffled_k4_best_by_period": {
  "27": -6.875,
  "28": -6.362,
  "29": -6.77
 },
 "english_reference": -3.6
}
```

Notes: 33489 climbs over 3721 of 3721 pairs. Best by period: [(27, -6.355), (28, -6.52), (29, -6.139)]; shuffled K4 (22-alphabet subset): [(27, -6.875), (28, -6.362), (29, -6.77)].


