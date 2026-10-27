# 0238-f13-replicate-k4-table-then-move-length-2-against-fresh-shuffles: F13.4d replication: 0237's K4 statistic (5.05 at table-then-move, key length 2, above all 100 shuffles, p 0.0099) against 300 fresh climbed shuffles, the search unchanged

**Family:** 13-ciphertext-only  
**Parent:** 0237-f13-a-move-and-the-sculptures-table-ciphertext-only  
**Decision:** reverted  
**Run:** 2026-10-27T21:29:39+00:00, 272.4 s, status ran  
**Time by phase:** design 0 s, test 32 s, run 272 s, record 0 s

## In plain words

In the last run K4 looked more like English, after one of our grid moves and a two-letter key, than any of 100 shuffles of its own letters did. That can happen by luck about once in a hundred tries. Here we shuffle K4 300 new times and ask again, with nothing else changed.

## Walkthrough, by hand

1. Shuffle K4's letters 300 times.
2. Run the same search on K4 and on every shuffle.
3. Count how many shuffles score at least as high as K4; fewer than 15 of 300 would replicate the result.

## Worked example (generated)

```
Order A on a planted message: K3's rule with step 7 (letter i goes to place 7i mod 97), then the KRYPTOS table with SHADOW:

  message   THEHOTAIRESCAPINGFROMTHECHAMBERCAUSEDTHEFLAMETOFLICKERBUTPRESENTLYDETAILSOFTHEROOMWITHINEMERGEDTH
  carved    DPILCFDYKUWKWYMWSBAQVXLSDZFPDXGNGVJRECNUCIGSGRXELPEUQRLIBXISWIQUJRSJFUESQZLIISQZBUWRGUNMCQQLZRKTU
  undone    THEHOTAIRESCAPINGFROMTHECHAMBERCAUSEDTHEFLAMETOFLICKERBUTPRESENTLYDETAILSOFTHEROOMWITHINEMERGEDTH

The search tries all 27,852 moves in both orders, every length 1-20 and the 8 ways of using the table.
```

## Lineage

Inherits from 0237-f13-a-move-and-the-sculptures-table-ciphertext-only. What changed: Replication (program.md: a result outside the scrambled copies stops the queue). 0237's search is run unchanged on K4 and on 300 fresh shuffles of K4 (seed 238), and the same statistic is recomputed with the fresh shuffles' means and spreads. No plants: 0237 measured the power (8/8, 7/8, 8/8, 6/8 at lengths 3, 5, 8, 12). The flagged reading (two turns cw 70,19 inverse, then the table standard/KRYPTOS Beaufort with key RI) put 3 of 24 known letters in place (harness), so under A2 it is not the message; the replication asks whether K4's excess at short keys after a move is real.

## Hypothesis (domain expert)

If K4's carved order holds a structure that a move plus a short periodic key turns into English-like text (C1(a), C11, the width-7 and width-21 fingerprints of 0056 read as a move), the excess should replicate against fresh shuffles; if it was the luck of 100 copies (the largest of 100 shuffles' statistics was 3.74, K4 5.05), it should not. Pre-registered: replicated when K4's statistic S (largest z over the 40 cells) is above all but a share p < 0.05 of 300 fresh shuffles; the B2 cell's own rank reported beside it. A replicated excess with the known letters out of place would be written up as a lead for the A2 question, not a solution.

## Prediction

Not replicated: K4's statistic falls inside the 300 fresh shuffles at p about 0.01-0.05 if the excess is real but small, or above 0.05 if it was luck; I expect above 0.05 against the fresh shuffles' wider spread. Zero candidates pass the gates.

## Method

1. 0237's attack unchanged except the seed (238), the shuffles (300) and no plants.
2. K4 and every shuffle solved by the same screen and climb (27,852 moves, both orders, 8 classes, lengths 1-20).
3. S = largest z over the 40 cells against the 300 shuffles; K4's p; B2's rank.

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
 "texts": 301,
 "k4_copies": 300,
 "k4_statistic": 4.623,
 "k4_best_cell": "B2",
 "k4_p": 0.0233,
 "copies_statistic_max": 5.385,
 "copies_statistic_median": 2.309,
 "k4_rank_per_cell_copies_at_or_above": {
  "A1": 18,
  "A2": 197,
  "A3": 292,
  "A4": 64,
  "A5": 89,
  "A6": 212,
  "A7": 151,
  "A8": 243,
  "A9": 96,
  "A10": 154,
  "A11": 242,
  "A12": 220,
  "A13": 157,
  "A14": 49,
  "A15": 88,
  "A16": 185,
  "A17": 116,
  "A18": 228,
  "A19": 134,
  "A20": 186,
  "B1": 18,
  "B2": 1,
  "B3": 239,
  "B4": 24,
  "B5": 174,
  "B6": 114,
  "B7": 173,
  "B8": 118,
  "B9": 232,
  "B10": 56,
  "B11": 22,
  "B12": 82,
  "B13": 257,
  "B14": 125,
  "B15": 10,
  "B16": 137,
  "B17": 115,
  "B18": 29,
  "B19": 40,
  "B20": 189
 },
 "replicated": true,
 "b2_copies_at_or_above": 1,
 "replicating": "0237 (S 5.05 at B2, p 0.0099 against 100)",
 "plant_power": {},
 "plant_exact_recovery": {},
 "decided_lengths_at_6_of_8": [],
 "k4_best_reading": {
  "cell": "B2",
  "reading": "NBENDJZERANDBCKNFILLBAADWRONNWIIHLGARTNRHHKORCULLHCNCSIDEPXMEDFCKRHALORKYXQTRGROWDOJOWSMSHDVNLYAT",
  "move": "two turns cw 70,19 inverse"
 },
 "f6_1": "blocked: 0236 found one free alphabet cannot be recovered from the ciphertext alone beyond length 5 with no move",
 "expected_total_time": "541 texts x about 25 s = about 4 core-hours",
 "exhaustive": false,
 "compute_seconds": 151
}
```

Notes: REPLICATED: K4 statistic 4.62 at B2, p 0.023 against 300 shuffles; plant power ; decided lengths []


