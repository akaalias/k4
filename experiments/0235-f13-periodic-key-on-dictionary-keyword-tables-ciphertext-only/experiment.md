# 0235-f13-periodic-key-on-dictionary-keyword-tables-ciphertext-only: F13.4b: a periodic key on 2.08 million dictionary keyword tables, key lengths 1-26, from the ciphertext alone: an exact per-column frequency screen of every table, then quadgram climbs and MIX8m on the best 50 per length

**Family:** 13-ciphertext-only  
**Parent:** 0234-f13-periodic-key-on-the-sculptures-tables-ciphertext-only  
**Decision:** reverted  
**Run:** 2026-10-27T16:52:04+00:00, 14753.2 s, status ran  
**Time by phase:** implement 85 s, test 144 s, run 14753 s, record 77 s

## In plain words

Like the last run, but the table is built from an ordinary English word instead of KRYPTOS: any of 208,062 words, used on either side. Too many tables to try the full method on each, so first every table gets the quick hand test (for each column of the secret word, which shift gives the most common English letters), and only the 50 best tables for each word length get the full treatment. Hidden test messages, made with random dictionary tables, tell us up to what length this still finds the answer.

## Walkthrough, by hand

1. Build a table from a word, say HYDRAULIC: HYDRAULICBEFGJKMNOPQSTVWXZ.
2. Guess a key length and write the carved letters in that many columns.
3. For each column, try all 26 shifts and keep the one whose letters are most like English (many E, T, A; few Q, Z).
4. Do this for every word in the dictionary and keep the 50 tables that look best.
5. For those, improve the shifts by how well the whole text reads, and compare K4's best with what shuffles of K4 reach.

## Worked example (generated)

```
The screen's first step on a planted message: plain alphabet HYDRAULIC-mixed, key SHADOW (6), standard cipher alphabet:

  plain alphabet  HYDRAULICBEFGJKMNOPQSTVWXZ
  carved          NHKDFRWODNIEWZHTAHVYPYOGAHESXGVPEIIGUCANZCWWKYFHYOIRYZ
  key, true       SHADOW
  key, by letter counts per column alone: SHADOW
  reading         THEHOTAIRESCAPINGFROMTHECHAMBERCAUSEDTHEFLAMETOFLICKER

Every one of 2.08 million tables gets this step at every key length; the 50 best per length are then climbed.
```

## Lineage

Inherits from 0234-f13-periodic-key-on-the-sculptures-tables-ciphertext-only. What changed: F13.4b (issue #85). 0234 solved the sculpture's 8 table classes from the ciphertext alone; here the tables are 0109's: every distinct keyword-mixed alphabet from the dictionary's words of 4 letters or more (208,062), on the plain side, the cipher side or both, against the standard or KRYPTOS alphabet (5 pairings), added or Beaufort form: 2,080,620 tables, key lengths 1-26. A climb per table is about 45 hours per text, so two stages: (1) for every table and length, each column's best shift by English letter frequencies, which is exact per column (compiled, about a minute per text), the 50 best tables per length kept; (2) for those, 0234's coordinate-ascent climb on quadgrams from the frequency optimum and 9 random starts, the best readings rescored by MIX8m (F13.3). Statistic, copies and plants as 0234 (K4 against 100 climbed shuffles; 40 plants at lengths 5-26 on random dictionary tables, each against 10 own shuffles). Cost stated before the run: 541 texts x about 70 s, about 10.5 core-hours.

## Hypothesis (domain expert)

F1 on dictionary keyword tables (0109: exact with the known letters, nothing below 26) read without them: the hedge for A1 and A2 on the table family Sanborn's K1-K2 belong to, with C27(c) (his chart 'slightly different from the one on Kryptos') and C5 (key word/s) read as a keyword-mixed alphabet. F13.1 puts the cell at 143 bits at length 26 (122 for the key, 20.3 for the 2.08 million tables), under MIX8m's 189. The frequency screen is the hand method's first step (each column's shift by letter counts; Friedman, Military Cryptanalysis I) and is exact per column; it loses the true table when columns are short, which the plants measure. Pre-registered: one statistic per text, S = max over L of the z-score of the best MIX8m log-probability at L against the shuffles; K4 flags at p < 0.05 against 100 shuffles; a planted length is decided when at least 6 of its 8 plants are above all 10 own shuffles. The item closes for the decided lengths and is blocked above them.

## Prediction

Plants found 8 of 8 at length 5, most at 10, few at 15-26: the frequency screen needs columns of 7 letters or more to keep the true table among 2 million, so decided to about 10. K4 inside its shuffles (p above 0.05); its 26 readings put at most 4-5 known letters in place. F13.4b closes for the short lengths and is blocked above.

## Method

1. Tables: 0109's 208,062 alphabets x 5 pairings (W/W, W/standard, standard/W, W/KRYPTOS, KRYPTOS/W) x 2 forms.
2. Screen (C): per text, table and length 1-26, the sum over columns of the best shift's English letter log-frequency; the 50 best tables per length kept.
3. Climb: for each kept table, coordinate ascent on the shifts by quadgrams from the screen's shifts and from 9 random starts; the best reading per table rescored by MIX8m (0233's weight 0.55); per length the best.
4. S = max over lengths of the z-score against K4's 100 shuffles; K4 ranked; each plant against its 10 own shuffles.
5. K4's best reading at each length submitted (key: the two alphabets, the form, the shifts); gate 4's controls are the shuffles' best readings scored as the harness scores.

## Result

Candidates returned: 26. Passed all gates: 0. Best crib hits among all candidates: 4/24
(EAST 1/4, NORTHEAST 2/9, BERLIN 1/6, CLOCK 0/5).
Best loss: 204.04903983334648 (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | cribs | 1/24 |  | `NLEBANXNHGAPLSNPTILLYIPBZCCDBMHESSNOYOCSFCSSJEVVYROFEPAUTRYTMILMWDZOOQVIDEYHUEVXOFKUTHEAGARAJEKRB` |  |
| 2 | cribs | 2/24 |  | `IGHLCSMSPYCRSOIROESGAEZLNMFAEKPNBOIDADFOJMBORNLVAPYCHRCTOPAUVESKTANDYQLEGNABDNLWYCUTOBHIKIWIRNUPE` |  |
| 3 | cribs | 1/24 |  | `NGSTRRSYVFRORDRJPURGHCUBYSAPOWETCUYEZWAUQAUDTIELZFEHTOXIYWAYMLNMCKYWELEUPTHEISDBEHHQGMSXNFWRTIHMT` |  |
| 4 | cribs | 2/24 |  | `DSRSUNGELWEPICNPFUSJEUYSVAAQRQVISCNUEDATNACTARIZELDOHYEDFLOGGUSHXZFUTJILPROMCRIXTXTDFVRVMELVARTCR` |  |
| 5 | cribs | 1/24 |  | `NTTAENDCWNYLANTDOYZRWRSADAIEAHIMONTOEDOFFIONWEBIKYONTREKOHKMBRAPAPFDCITRESCISTHBONGYMIMNVESGFSXSU` |  |
| 6 | cribs | 2/24 |  | `NGHGPQDRCSPOPELERHPGRNDWAWOCHSVONRCEEDORAVJETAONEBITEOFFUWKTGJEPMRADIDOHIORIZMCUITNCHKHOTILSTANDT` |  |
| 7 | cribs | 1/24 |  | `ROECFCLRTISRIERMONSIAGMAHCSMSFUANGIVEBRNAFTUSABRALINARTONKFTHETEDTHEHUQSTADPOMAGGYNONTESXTRIGEIOF` |  |
| 8 | cribs | 1/24 |  | `MIXTNICUINCCBCLEHMQUPOVVBTBEAFHDGAORPHYOUTIMERENCENAISZYHEENWONRESDRYTEAYPEODRELLORWUEUITUMGEROSN` |  |
| 9 | cribs | 2/24 |  | `FLAOREBCSJOBGCEPOOGLUHNTANGUCLIMBNCRSHECLUNSUMTISACRIDRAWASAFETYPDWDCTWOUVUIPLDURLIMBILEGMAONMESI` |  |
| 10 | cribs | 3/24 |  | `LCONTOAFTEDICTEMIURAFEINOURREOROTTEWSTDYPMTTFBCDISCHOITTIMITVECABQOTFHIELOSIDIMVCHDRIIHOONWUPONEY` |  |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "item": "F13.4b",
 "search_reads_known_letters": false,
 "alphabets": 208062,
 "tables": 2080620,
 "pairings": [
  "W/W",
  "W/STD",
  "STD/W",
  "W/KRY",
  "KRY/W"
 ],
 "forms": [
  "added",
  "Beaufort"
 ],
 "key_lengths": [
  1,
  26
 ],
 "screen": "per column best shift by English letter frequency, exact; best 50 tables per length",
 "climb": "coordinate ascent on quadgrams from the screen's shifts and 9 random starts; MIX8m rescoring",
 "texts": 541,
 "k4_copies": 100,
 "k4_statistic": 1.804,
 "k4_best_length": 5,
 "k4_p": 0.6634,
 "copies_statistic_max": 4.639,
 "copies_statistic_median": 2.052,
 "k4_rank_per_length_copies_at_or_above": {
  "1": 17,
  "2": 48,
  "3": 95,
  "4": 42,
  "5": 4,
  "6": 70,
  "7": 45,
  "8": 99,
  "9": 61,
  "10": 37,
  "11": 48,
  "12": 67,
  "13": 69,
  "14": 83,
  "15": 30,
  "16": 40,
  "17": 19,
  "18": 81,
  "19": 83,
  "20": 75,
  "21": 52,
  "22": 37,
  "23": 88,
  "24": 53,
  "25": 9,
  "26": 31
 },
 "plant_power": {
  "5": [
   8,
   8
  ],
  "10": [
   4,
   8
  ],
  "15": [
   2,
   8
  ],
  "20": [
   0,
   8
  ],
  "26": [
   2,
   8
  ]
 },
 "plant_exact_recovery": {
  "5": [
   7,
   8
  ],
  "10": [
   2,
   8
  ],
  "15": [
   0,
   8
  ],
  "20": [
   0,
   8
  ],
  "26": [
   0,
   8
  ]
 },
 "plant_true_table_best": {
  "5": [
   7,
   8
  ],
  "10": [
   2,
   8
  ],
  "15": [
   0,
   8
  ],
  "20": [
   0,
   8
  ],
  "26": [
   0,
   8
  ]
 },
 "decided_lengths_at_6_of_8": [
  5
 ],
 "k4_best_readings": {
  "5": {
   "reading": "NTTAENDCWNYLANTDOYZRWRSADAIEAHIMONTOEDOFFIONWEBIKYONTREKOHKMBRAPAPFDCITRESCISTHBONGYMIMNVESGFSXSU",
   "word": "ACCEPTOR"
  },
  "10": {
   "reading": "LCONTOAFTEDICTEMIURAFEINOURREOROTTEWSTDYPMTTFBCDISCHOITTIMITVECABQOTFHIELOSIDIMVCHDRIIHOONWUPONEY",
   "word": "DOESKIN"
  }
 },
 "expected_total_time": "541 texts x about 70 s = about 10.5 core-hours",
 "exhaustive": false,
 "compute_seconds": 12997
}
```

Notes: K4 statistic 1.80 at length 5, p 0.663 against 100 shuffles; plant power L5 8/8, L10 4/8, L15 2/8, L20 0/8, L26 2/8; decided lengths [5]


