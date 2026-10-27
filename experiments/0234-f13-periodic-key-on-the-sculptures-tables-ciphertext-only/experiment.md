# 0234-f13-periodic-key-on-the-sculptures-tables-ciphertext-only: F13.4a: a periodic key on the sculpture's 8 table classes, key lengths 1-36, solved from the ciphertext alone (quadgram climb, MIX8m rescoring), K4 against 200 climbed shuffles, plants at seven lengths

**Family:** 13-ciphertext-only  
**Parent:** 0233-f13-how-many-bits-per-letter-each-english-judge-extracts  
**Decision:** reverted  
**Run:** 2026-10-27T16:39:18+00:00, 116.2 s, status ran  
**Time by phase:** implement 73 s, test 15 s, run 116 s, record 70 s

## In plain words

The first two messages on the sculpture were made with its table and a repeating secret word. If K4 were made the same way, a codebreaker could recover the word without knowing any of the message, by trying every shift for each letter of the word and keeping the ones that make the text read best, as people did by hand a century ago. We do that for every word length up to 36 and for all eight ways of using the sculpture's two alphabets, never looking at the clue words, and compare K4 with 200 shuffles of its own letters treated the same way. Hidden test messages tell us up to what length this can work.

## Walkthrough, by hand

1. Guess a key length, say 7, and write the carved letters in 7 columns.
2. Pick one of the eight ways of using the sculpture's table.
3. For column 1 try all 26 shifts and keep the one that makes the whole text read best; then column 2, and so on, going round until nothing improves.
4. Start again from a few random keys and keep the best reading.
5. Do it for every length up to 36 and every way of using the table, and compare K4's best with the best that shuffles of K4's letters reach.

## Worked example (generated)

```
The same climb on K1's 63 carved letters, key length 10, the KRYPTOS table, no known letter:

  shifts found  PALIMPSEST
  reading       BETWEENSUBTLESHADINGANDTHEABSENCEOFLIGHTLIESTHENUANCEOFIQLUSION

On K4 the climb runs for every length 1-36 and all 8 ways of using the table, and K4's best is compared with
the best that 200 shuffles of K4's letters reach.
```

## Lineage

Inherits from 0233-f13-how-many-bits-per-letter-each-english-judge-extracts. What changed: F13.4a (issue #85), the first ciphertext-only solve. 0005 closed this cell exactly with the 24 known letters (lengths 1-26 and 30-52 dead on all 8 classes); here the known letters are not read. For each of the 8 classes (plain and cipher alphabets standard or KRYPTOS, added or Beaufort form; the key alphabet drops out) and each key length 1-36, a compiled coordinate-ascent climb on the shifts (30 restarts) maximizes the quadgram score; the 288 best readings are rescored by MIX8m, F13.3's out-of-domain model (1.95 bits per letter). Per length the best reading over the classes; the text's statistic is its largest z-score over the lengths against K4's 200 climbed shuffles. Plants (Carter's held-out last 20%, half with X stops, no known word) at lengths 5, 10, 15, 20, 26, 30 and 36, 8 each, each against 10 own climbed shuffles.

## Hypothesis (domain expert)

F1 with the sculpture's tables (K1, K2: Quagmire III on KRYPTOS with PALIMPSEST and ABSCISSA; 01-facts.md) is the first family in rank; C8(a), C27(c), C28. Every verdict on it rests on the known letters sitting at 22-34 and 64-74 of the final text, letter for letter (A2) and without slips (A1). F13.1 (reports/f13-solvability-map.md) puts a periodic key on a fixed table decidable by English alone to length 36 (125 bits at 26, under the 173 the quadgram scorer carries; 189 with MIX8m, 0233). The classic hand method (Stein; Friedman's Military Cryptanalysis) is exactly this: one shift per column, chosen by how well the decryption reads. Pre-registered: one statistic per text, S = max over L of (best MIX8m log-probability at L minus the shuffles' mean at L) / their sd; K4 flags at p < 0.05 against 200 shuffles (one test). Power per planted length: found when S is above all 10 own copies' S (null 1/11); a length is decided when at least 6 of its 8 plants are found (0120's bar as used by A6.2). The item closes for the lengths decided and is blocked above, by the measured power.

## Prediction

Plants found 8 of 8 at lengths 5-15, most at 20, falling to a few at 30-36 (columns of 2-3 letters): decided to about 20-26. K4's statistic inside its shuffles (p above 0.05), its best readings English-like junk with no known letter in place beyond chance (the harness's gate 2 on the 36 submitted readings: at most 3 of 24). So F13.4a closes for the decided lengths and is blocked above them.

## Method

1. Texts: K4; 200 shuffles of K4; 56 plants (lengths 5, 10, 15, 20, 26, 30, 36; 8 each, 4 clean and 4 with X stops; random class and shifts) and 10 shuffles of each plant: 817 texts.
2. Per text, per class (8) and length (1-36): coordinate ascent on the shifts, 30 random restarts, each pass trying all 26 shifts of every column in random order, scored by the harness's quadgram table.
3. The 288 best readings rescored by MIX8m (0233: KN8 on the manuals mixed with the quadgram table, weight 0.55); per length the best over classes.
4. z per length against K4's shuffles; S = the largest z; K4 ranked among its shuffles; each plant among its own copies.
5. K4's best reading at each length submitted as a candidate (key: class and shifts), so the harness checks the known letters only after the search; gate 4's controls are the shuffles' best readings, scored as the harness scores.

## Result

Candidates returned: 36. Passed all gates: 0. Best crib hits among all candidates: 5/24
(EAST 0/4, NORTHEAST 4/9, BERLIN 0/6, CLOCK 1/5).
Best loss: 192.2405531398806 (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | cribs | 1/24 |  | `DAIHNDKDVUNRACDRTWAALWRHMOOFHPVICCDELEOCSOCCXIJJLBESIRNYTBLTPWAPGFMEEQJWFILVYIJKESZYTVINUNBNXIZBH` |  |
| 2 | cribs | 3/24 |  | `RYWMAIDINBAFHNRFUSHYCSXMBLPJTHNEONRQCQPNVLONLEFKCRSDWFATURCCKSHHEJBQSGFSYECAJEFXSDITUAWUQUGULEIRT` |  |
| 3 | cribs | 3/24 |  | `EHSHADQRYTAAXODBURXHMYXGMPFFTCPWHIRINSFIVFIOKAFUNGISWALJTWCTDMWDEEMSICFRFWMPJSVDISIZONSLQJWAKAIVH` |  |
| 4 | cribs | 3/24 |  | `EINAOYSDNCCGXXIGLEYWPEMATKGCBPWHAXIOPWGSJKESUSTZPJDIIOCULJAJFEYERRBOSTTNDSAMVSTRSARULDNTMVPTUSRXB` |  |
| 5 | cribs | 4/24 |  | `MESSAMAWHNSOJTUJLNCHUITSBOTXSTENATURZBRYHTATKICHXGRMSMABLIXOLIJOENYBUSXIXLCEGSADRMKEOENCIAYXMLIYU` |  |
| 6 | cribs | 2/24 |  | `GCAREWSSQHECJAFLOTJCTFANTURPLEURGSUVOORSSFHAMKILOBEJJCPEVAGARGINMUTOEMITERTGKMAZEJZYWHAUTGIVMKZZC` |  |
| 7 | cribs | 1/24 |  | `ESSHHBLERMQMOCEWLPROMTWONINFIUNIPADFLYUPWUDBUIDHMCDJIMMORACKJRAWFPNOCWLYPIFKOJIBENTORRSQUMBUPSSYF` |  |
| 8 | cribs | 3/24 |  | `ESWOCFHTMYREPGOFOWEVEMAPVEQQITWOFQBREEDUPECTSAINWRADHREYORTCAMRHBNSRLSIACKTARAIMDAFXWNJJNFDISASVA` |  |
| 9 | cribs | 1/24 |  | `SYODYIRYFLRPNWIFSEFYARPLPAPTORSOMMYSAQUENKMCDOWDIENDUKYAMMACHPARVTHXNGJETHASHETHSNZHUKEORTERIWGUL` |  |
| 10 | cribs | 3/24 |  | `WWASSMUCBNCGRTMJFTWHEABSTONDMTOFITMRTHLYRLITCIWNRGBEAMSBFOROVAROWNSHOSHAFLUEAYUDBESEGEHICAIPULAYO` |  |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "item": "F13.4a",
 "search_reads_known_letters": false,
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
  36
 ],
 "restarts": 30,
 "climb": "coordinate ascent on the shifts, quadgram table; best per (class, length) rescored by MIX8m (0233)",
 "texts": 817,
 "k4_copies": 200,
 "k4_statistic": 2.147,
 "k4_best_length": 20,
 "k4_p": 0.6169,
 "copies_statistic_max": 5.383,
 "copies_statistic_median": 2.31,
 "k4_rank_per_length_copies_at_or_above": {
  "1": 136,
  "2": 194,
  "3": 179,
  "4": 51,
  "5": 8,
  "6": 77,
  "7": 11,
  "8": 156,
  "9": 168,
  "10": 107,
  "11": 61,
  "12": 122,
  "13": 38,
  "14": 43,
  "15": 73,
  "16": 126,
  "17": 168,
  "18": 137,
  "19": 138,
  "20": 7,
  "21": 53,
  "22": 27,
  "23": 135,
  "24": 175,
  "25": 38,
  "26": 62,
  "27": 76,
  "28": 17,
  "29": 18,
  "30": 16,
  "31": 83,
  "32": 8,
  "33": 94,
  "34": 140,
  "35": 14,
  "36": 176
 },
 "plant_power": {
  "5": [
   8,
   8
  ],
  "10": [
   8,
   8
  ],
  "15": [
   8,
   8
  ],
  "20": [
   7,
   8
  ],
  "26": [
   6,
   8
  ],
  "30": [
   5,
   8
  ],
  "36": [
   2,
   8
  ]
 },
 "plant_exact_recovery": {
  "5": [
   8,
   8
  ],
  "10": [
   8,
   8
  ],
  "15": [
   7,
   8
  ],
  "20": [
   0,
   8
  ],
  "26": [
   0,
   8
  ],
  "30": [
   0,
   8
  ],
  "36": [
   0,
   8
  ]
 },
 "decided_lengths_at_6_of_8": [
  5,
  10,
  15,
  20,
  26
 ],
 "k4_best_readings": {
  "20": "MIMESONTENSNVSATOMCLEELERMUSTHGOESALAYNURTEDISLIOUTPMZUBORHENEVIONPORINTHASYTHEPHAUSEWANDAMESAMEF",
  "7": "ESSHHBLERMQMOCEWLPROMTWONINFIUNIPADFLYUPWUDBUIDHMCDJIMMORACKJRAWFPNOCWLYPIFKOJIBENTORRSQUMBUPSSYF",
  "10": "WWASSMUCBNCGRTMJFTWHEABSTONDMTOFITMRTHLYRLITCIWNRGBEAMSBFOROVAROWNSHOSHAFLUEAYUDBESEGEHICAIPULAYO"
 },
 "exhaustive": false,
 "compute_seconds": 91
}
```

Notes: K4 statistic 2.15 at length 20, p 0.617 against 200 shuffles; plant power L5 8/8, L10 8/8, L15 8/8, L20 7/8, L26 6/8, L30 5/8, L36 2/8; decided lengths [5, 10, 15, 20, 26]


