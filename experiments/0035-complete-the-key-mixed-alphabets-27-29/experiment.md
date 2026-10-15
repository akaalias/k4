# 0035-complete-the-key-mixed-alphabets-27-29: The same key completion at periods 27 to 29, with the table rebuilt from the puzzle's words

**Family:** 1-keyed-periodic  
**Parent:** 0034-complete-the-key-at-surviving-periods  
**Decision:** reverted  
**Run:** 2026-10-15T08:36:45+00:00, 97.6 s, status ran  
**Time by phase:** design 1148 s, implement 63 s, test 7 s, run 98 s, record 0 s

## In plain words

Experiment 34 showed that with a secret word of length 27, 28 or 29, filling in the few unknown letters never produces a readable message when the table is the sculpture's own. But the table could have been built from another word, like PALIMPSEST or ABSCISSA, and that changes every letter that comes out. So we rebuild the table from each word the puzzle knows, in turn for the message side and for the carved side, and run the same filling game again.

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

Inherits from 0034-complete-the-key-at-surviving-periods. What changed: Experiment 34 climbed the free key letters under the standard and KRYPTOS alphabets only. Here one of the two alphabets, for the message or for the carved letters, is rebuilt from each vocabulary word, and the key alphabet is dropped, since it does not change the decryption. Periods 27 to 29 only, where the key has three to five free letters and the climb cannot overfit.

## Hypothesis (domain expert)

At periods 27-29 the cribs force 24 of the key slots and leave 3-5 free, so the English climb of experiment 34 is close to exhaustive and cannot overfit; it found noise under the 8 distinct plain-cipher alphabet classes of the 24 conventions. The key alphabet only relabels the key and never changes the decrypted text, so the real variable is the pair of plain and cipher alphabets. Scheidt's keyword alphabets (C5) and the K1-K2 precedent make a table built from a puzzle word the natural extension: here one of the pair is standard or KRYPTOS and the other is the keyword mixing of any of 61 vocabulary words, both ways round, under three modes: 756 classes, 3 periods, five restarts each. The best free-letter English per class and period is compared with the same climb on one shuffle of K4. A true periodic cipher on such a table would give a text near -3.6 at its period; shuffled K4 gives about -6.8. Bounds: complete for this alphabet pool at periods 27-29; both alphabets mixed from words at once is not covered.

## Prediction

No class and period gives a text better than -5.5 per quadgram; the best over all 2,268 climbs is within 0.4 of the best on shuffled K4. Candidates pass the gates by construction but none reads as English; none beats the current champion's fitness.

## Method

1. Build the alphabet pool: standard, KRYPTOS and the keyword mixing of each vocabulary word.
2. For each pair with one side standard or KRYPTOS, each mode and each period 27-29, force the 24 key slots from the cribs; skip the pair if two cribs disagree on a slot.
3. Climb the free slots by coordinate descent on the English score of the 73 non-crib letters, five restarts.
4. Keep the best text per period and submit it.
5. Repeat on one shuffle of K4 for calibration.

## Result

Candidates returned: 3. Passed all gates: 3. Best crib hits among all candidates: 24/24
(EAST 4/4, NORTHEAST 9/9, BERLIN 6/6, CLOCK 5/5).
Best loss: 4.208020161263802 (0 is solved; 10 per missed crib letter). Best fitness: -7.971387858858304. Champion before this run: 0034-complete-the-key-at-surviving-periods.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | pass | 24/24 | -8.130 | `QGFMJOYSTOAEUHISNORDFEASTNORTHEASTSDKZSIZKIENYYISBUIIAWIVYLBOMOBERLINCLOCKFFEMXURMHAWYLVEERAJBUXH` | period 27, plain std, cipher HILL/keyword, vig; 3 free slots climbed |
| 2 | pass | 24/24 | -7.971 | `DWIVEFUEXNARRMGFNUECOEASTNORTHEASTMWSESLIBREUKSFOCUJPVHUNIJEFUNBERLINCLOCKCEDWJICYBUNUIPOBOZZHUQP` | period 28, plain WILLIAMWEBSTER/keyword, cipher std, beau; 4 free slots climbed |
| 3 | pass | 24/24 | -8.019 | `FFATRYYSOWADXNDJBUTHEEASTNORTHEASTYFINMGHFNESEAVOLPGLEXNZIANXBIBERLINCLOCKRTRAAJSAKOWAAGGQIRORYUK` | period 29, plain LANGLEY/keyword, cipher std, beau; 5 free slots climbed |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "periodic tableau at periods 27-29, one alphabet standard or KRYPTOS and the other keyword-mixed from the vocabulary, key completed by English climb",
 "alphabets": 63,
 "classes": 744,
 "periods": [
  27,
  28,
  29
 ],
 "restarts": 5,
 "climbs": 2232,
 "best_by_period": {
  "27": {
   "english": -6.822,
   "plain": "std",
   "cipher": "HILL/keyword",
   "mode": "vig",
   "free_slots": 3,
   "text": "QGFMJOYSTOAEUHISNORDFEASTNORTHEASTSDKZSIZKIENYYISBUIIAWIVYLBOMOBERLINCLOCKFFEMXURMHAWYLVEERAJBUXH"
  },
  "28": {
   "english": -6.615,
   "plain": "WILLIAMWEBSTER/keyword",
   "cipher": "std",
   "mode": "beau",
   "free_slots": 4,
   "text": "DWIVEFUEXNARRMGFNUECOEASTNORTHEASTMWSESLIBREUKSFOCUJPVHUNIJEFUNBERLINCLOCKCEDWJICYBUNUIPOBOZZHUQP"
  },
  "29": {
   "english": -6.614,
   "plain": "LANGLEY/keyword",
   "cipher": "std",
   "mode": "beau",
   "free_slots": 5,
   "text": "FFATRYYSOWADXNDJBUTHEEASTNORTHEASTYFINMGHFNESEAVOLPGLEXNZIANXBIBERLINCLOCKRTRAAJSAKOWAAGGQIRORYUK"
  }
 },
 "top_ten": [
  {
   "english": -6.614,
   "period": 29,
   "plain": "LANGLEY/keyword",
   "cipher": "std",
   "mode": "beau"
  },
  {
   "english": -6.615,
   "period": 28,
   "plain": "WILLIAMWEBSTER/keyword",
   "cipher": "std",
   "mode": "beau"
  },
  {
   "english": -6.62,
   "period": 29,
   "plain": "UNDERGRUUND/keyword",
   "cipher": "std",
   "mode": "beau"
  },
  {
   "english": -6.626,
   "period": 29,
   "plain": "WORLDCLOCK/keyword",
   "cipher": "std",
   "mode": "vig"
  },
  {
   "english": -6.626,
   "period": 29,
   "plain": "WORLDCLOCK/keyword",
   "cipher": "std",
   "mode": "varbeau"
  },
  {
   "english": -6.673,
   "period": 29,
   "plain": "kry",
   "cipher": "ORDINATE/keyword",
   "mode": "vig"
  },
  {
   "english": -6.673,
   "period": 29,
   "plain": "kry",
   "cipher": "ORDINATE/keyword",
   "mode": "varbeau"
  },
  {
   "english": -6.721,
   "period": 29,
   "plain": "kry",
   "cipher": "kry",
   "mode": "beau"
  },
  {
   "english": -6.723,
   "period": 29,
   "plain": "LUCIDMEMORY/keyword",
   "cipher": "kry",
   "mode": "vig"
  },
  {
   "english": -6.723,
   "period": 29,
   "plain": "LUCIDMEMORY/keyword",
   "cipher": "kry",
   "mode": "varbeau"
  }
 ],
 "shuffled_k4_best_by_period": {
  "27": -6.616,
  "28": -6.749,
  "29": -6.714
 },
 "english_reference": -3.6
}
```

Notes: 2232 climbs. Best by period: [(27, -6.822), (28, -6.615), (29, -6.614)]; shuffled K4 (22-alphabet subset): [(27, -6.616), (28, -6.749), (29, -6.714)].


