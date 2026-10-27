# 0237-f13-a-move-and-the-sculptures-table-ciphertext-only: F13.4d: every move of the type-1 library (27,852), before or after a periodic key on the sculpture's 8 table classes, key lengths 1-20, from the ciphertext alone; F6.1's free alphabet after a move blocked by 0236's power

**Family:** 13-ciphertext-only  
**Parent:** 0234-f13-periodic-key-on-the-sculptures-tables-ciphertext-only  
**Decision:** reverted  
**Run:** 2026-10-27T21:23:02+00:00, 273.6 s, status ran  
**Time by phase:** implement 94 s, test 47 s, run 274 s, record 42 s

## In plain words

Sanborn said he scrambled with 'matrix codes' and then used the table. Here the scramble is any of 27,852 grid moves we have listed, done before or after the table with a repeating secret word, and the whole thing is solved from the carved letters alone. For each guess of the scramble and the word length, the quick letter-count test picks each column's shift; the most English-looking guesses are then improved and compared with shuffles of K4.

## Walkthrough, by hand

1. Pick a grid move from the list, for instance K3's rule or a keyword columnar.
2. Either undo the move on the carved letters first (table last) or keep it for the end (table first).
3. Write the letters in as many columns as the key is long and choose each column's shift by letter counts.
4. Read the result in the message's order and score it as English.
5. Keep the best guesses, improve their shifts, and compare K4's best with what shuffles of K4 reach.

## Worked example (generated)

```
Order A on a planted message: K3's rule with step 7 (letter i goes to place 7i mod 97), then the KRYPTOS table with SHADOW:

  message   THEHOTAIRESCAPINGFROMTHECHAMBERCAUSEDTHEFLAMETOFLICKERBUTPRESENTLYDETAILSOFTHEROOMWITHINEMERGEDTH
  carved    DPILCFDYKUWKWYMWSBAQVXLSDZFPDXGNGVJRECNUCIGSGRXELPEUQRLIBXISWIQUJRSJFUESQZLIISQZBUWRGUNMCQQLZRKTU
  undone    THEHOTAIRESCAPINGFROMTHECHAMBERCAUSEDTHEFLAMETOFLICKERBUTPRESENTLYDETAILSOFTHEROOMWITHINEMERGEDTH

The search tries all 27,852 moves in both orders, every length 1-20 and the 8 ways of using the table.
```

## Lineage

Inherits from 0234-f13-periodic-key-on-the-sculptures-tables-ciphertext-only. What changed: F13.4d (issue #85). 0234 solved the sculpture's tables with no move from the ciphertext alone; here every move of 0129's type-1 library (K3's rule at every shift, quarter turns, columnar and double turns at every width, the keyword columnars of the vocabulary; forward and inverse) is put before (A: move, then the table) or after (B: the table, then the move) the periodic key, key lengths 1-20, 8 table classes. A climb per setting is about 12 hours per text, so: for A the column statistics do not depend on the move, so each column's shift comes from one letter-frequency screen per class and length and every move is then scored by quadgrams; for B each move is undone first and then screened. The 30 best settings per order and length get 0234's coordinate-ascent climb (the move held) and MIX8m rescoring. Statistic, copies and plants as 0234. F6.1 (one free alphabet after a move) is not run: 0236 found one free alphabet cannot be recovered from the ciphertext alone beyond length 5 with no move at all, and 27,852 moves only add alternatives. Cost stated before the run: 541 texts x about 25 s, about 4 core-hours.

## Hypothesis (domain expert)

F6 (Sanborn's 'matrix codes... then went back to this table', C1(a); K3's rule, C2(a)) read without the known letters: the hedge for A2 (the known letters defined on an intermediate text) and A1 on the family ranked second. F13.1 puts a move and a fixed-table key decidable by quadgrams (log2 27,852 = 14.8 bits for the move, 3 for the class and order, 4.7 per key letter: 112 bits at 20, under MIX8m's 189). Pre-registered: S = max over (order, length) of the z-score of the best MIX8m log-probability against K4's 100 climbed shuffles; K4 flags at p < 0.05; plants at lengths 3, 5, 8, 12, 20 (half each order, random move and class), each against 10 own shuffles; a length is decided at 6 of 8. The item closes for the decided lengths and is blocked above.

## Prediction

Plants found at 3 and 5 (8/8), most at 8, few at 12, none at 20: decided to about 8. K4 inside its shuffles (p above 0.05), its readings at most 4-5 known letters. F13.4d closes for the short lengths, blocked above; F6.1 blocked by 0236.

## Method

1. Moves: 0129's route_library (forward and inverse, distinct), rebuilt here from the vocabulary.
2. Order A: per class and length, each column's shift by English letter frequency on the carved text; the decryption read through each move (letter i of the message is carved at where[i]) and scored by quadgrams. Order B: each move undone on the carved text, then each column's shift by letter frequency, and the reading scored by quadgrams. The 30 best (move, class) per order and length kept (C).
3. Those climbed by coordinate ascent on the shifts, the move held (screen's shifts and 5 random starts); rescored by MIX8m (0233); per order and length the best.
4. S = max z over the 40 cells against K4's 100 shuffles; K4 ranked; each plant against 10 own shuffles.
5. K4's best reading per cell submitted (key: move, order, class, shifts).

## Result

Candidates returned: 40. Passed all gates: 0. Best crib hits among all candidates: 4/24
(EAST 2/4, NORTHEAST 1/9, BERLIN 0/6, CLOCK 1/5).
Best loss: 212.39771055071787 (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | cribs | 4/24 |  | `LDFCTSBAMCWZEIEDAYSHEEATINQLLVRDJEWINKWORNYDFCHUTVISMNBULOOBLNVCONTRYCFXPAIXHIWCJIPZADKJVBPREJIHG` |  |
| 2 | cribs | 2/24 |  | `HASCIPLYNELEDMLOPNEPPDEKWSIXOROHWFMJWSDAFREYTJORNTCUEJDUFNRMLZIPERUKIYUZPHXWILSHKESTLYQBVUSHOWGYF` |  |
| 3 | cribs | 0/24 |  | `QQAANDFJHMPQSWIXTNVYKGVDEVIHNETBAVSHRURTHEQUAOREBDXFQASRTEYSCPJSDECKFFGIKMRTOVEDRORHINAGRLUFILLME` |  |
| 4 | cribs | 2/24 |  | `BYFIEDARATSEASZUYDTCNGCEWPTRSGIXPHMQAISLVSCUMFHAUTIVOISASPDAJONANDYOJNMNIKOAMNEDRUPBYCOYRWSFIFMIL` |  |
| 5 | cribs | 0/24 |  | `NBCDNBBYGHSAFLCTRAPHGOHRELAMUFMHIPFIGHREITNEGYJLHEQURRBEFILIRSUAOVZYKMSEEDWOVIDEJPVLFOIORSIANGIEA` |  |
| 6 | cribs | 4/24 |  | `ICARMUNSSILHAYWWGAGESHINFANPAULSSHIRDAVZVISMONKSDXEMFUGDIEJINNSWITHDTKLOCDHFELIECCSXPXURGTFEWMRHC` |  |
| 7 | cribs | 0/24 |  | `PUPIODOSIROWDELSOASYABCFHABEXONSTERHIZMVNUNBUTFROMEPHMYBSOIDETEAJINJBSOPRSEMOFFEYIMJFCSTHHOUNGCZU` |  |
| 8 | cribs | 0/24 |  | `STBLENOOOZLASSNBCECATHUCHOFVISBRIKELNUWALFTHATMARANLYGAPCONAFTTYDOEFMPBDPOCPUCWOOLUTTENMHEGHHGHVI` |  |
| 9 | cribs | 2/24 |  | `ENTYOTFSUMJNLBALDHAMSRIORULMISTDEONELSACKEWCAMNITVSOKTPYKIRRTASFERALEIDEITUPWHENKBRAUNKISNTMCVLED` |  |
| 10 | cribs | 1/24 |  | `QWHYETNREJOURTORHUDOTCODRCBGAMMAASSANKVITANYIIILKUTDIUZPDENINTHEFOREUSTSINTSAWIYOMDEZCOLBFSOBTOHQ` |  |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "item": "F13.4d",
 "search_reads_known_letters": false,
 "moves": 27852,
 "orders": [
  "A move-then-table",
  "B table-then-move"
 ],
 "classes": [
  "std/std/vig",
  "std/std/beau",
  "std/kry/vig",
  "std/kry/beau",
  "kry/std/vig",
  "kry/std/beau",
  "kry/kry/vig",
  "kry/kry/beau"
 ],
 "key_lengths": [
  1,
  20
 ],
 "screen": "per-column letter-frequency shifts, every move scored by quadgrams; 30 best per order and length",
 "climb": "coordinate ascent, move held, screen's shifts and 5 random starts; MIX8m rescoring",
 "texts": 541,
 "k4_copies": 100,
 "k4_statistic": 5.055,
 "k4_best_cell": "B2",
 "k4_p": 0.0099,
 "copies_statistic_max": 3.742,
 "copies_statistic_median": 2.336,
 "k4_rank_per_cell_copies_at_or_above": {
  "A1": 8,
  "A2": 63,
  "A3": 99,
  "A4": 26,
  "A5": 29,
  "A6": 73,
  "A7": 43,
  "A8": 87,
  "A9": 31,
  "A10": 51,
  "A11": 88,
  "A12": 80,
  "A13": 50,
  "A14": 21,
  "A15": 36,
  "A16": 66,
  "A17": 65,
  "A18": 68,
  "A19": 75,
  "A20": 54,
  "B1": 8,
  "B2": 0,
  "B3": 76,
  "B4": 9,
  "B5": 54,
  "B6": 38,
  "B7": 67,
  "B8": 41,
  "B9": 80,
  "B10": 25,
  "B11": 3,
  "B12": 65,
  "B13": 62,
  "B14": 38,
  "B15": 4,
  "B16": 68,
  "B17": 8,
  "B18": 9,
  "B19": 22,
  "B20": 75
 },
 "plant_power": {
  "3": [
   8,
   8
  ],
  "5": [
   7,
   8
  ],
  "8": [
   8,
   8
  ],
  "12": [
   6,
   8
  ],
  "20": [
   1,
   8
  ]
 },
 "plant_exact_recovery": {
  "3": [
   6,
   8
  ],
  "5": [
   5,
   8
  ],
  "8": [
   8,
   8
  ],
  "12": [
   3,
   8
  ],
  "20": [
   1,
   8
  ]
 },
 "decided_lengths_at_6_of_8": [
  3,
  5,
  8,
  12
 ],
 "k4_best_reading": {
  "cell": "B2",
  "reading": "NBENDJZERANDBCKNFILLBAADWRONNWIIHLGARTNRHHKORCULLHCNCSIDEPXMEDFCKRHALORKYXQTRGROWDOJOWSMSHDVNLYAT",
  "move": "two turns cw 70,19 inverse"
 },
 "f6_1": "blocked: 0236 found one free alphabet cannot be recovered from the ciphertext alone beyond length 5 with no move",
 "expected_total_time": "541 texts x about 25 s = about 4 core-hours",
 "exhaustive": false,
 "compute_seconds": 253
}
```

Notes: K4 statistic 5.05 at B2, p 0.010 against 100 shuffles; plant power L3 8/8, L5 7/8, L8 8/8, L12 6/8, L20 1/8; decided lengths [3, 5, 8, 12]


