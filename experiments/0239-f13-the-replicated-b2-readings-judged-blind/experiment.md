# 0239-f13-the-replicated-b2-readings-judged-blind: F13.4d follow-up: 0238's replicated cell (table, then a move, key length 2) regenerated for K4 and its 300 shuffles and judged blind: words, or statistics of the carved order?

**Family:** 13-ciphertext-only  
**Parent:** 0238-f13-replicate-k4-table-then-move-length-2-against-fresh-shuffles  
**Decision:** reverted  
**Run:** 2026-10-27T21:35:41+00:00, 734.0 s, status ran  
**Time by phase:** test 20 s, run 734 s, record 30 s

## In plain words

K4 really did score better than its shuffles in one setting, twice. But the scorer counts letter patterns, not words, and K4's letters are known to sit in slightly unusual patterns. So we show K4's reading and the 300 shuffles' readings to the language-model judge, blind, and ask whether any of them contains English words.

## Walkthrough, by hand

1. Rebuild the same readings as before for K4 and its 300 shuffles.
2. Show all 301, one at a time and unlabelled, to the judge, who scores how much reads as English.
3. If K4's reading is not among the top 5%, the excess was letter texture, not words.

## Worked example (generated)

```
Order A on a planted message: K3's rule with step 7 (letter i goes to place 7i mod 97), then the KRYPTOS table with SHADOW:

  message   THEHOTAIRESCAPINGFROMTHECHAMBERCAUSEDTHEFLAMETOFLICKERBUTPRESENTLYDETAILSOFTHEROOMWITHINEMERGEDTH
  carved    DPILCFDYKUWKWYMWSBAQVXLSDZFPDXGNGVJRECNUCIGSGRXELPEUQRLIBXISWIQUJRSJFUESQZLIISQZBUWRGUNMCQQLZRKTU
  undone    THEHOTAIRESCAPINGFROMTHECHAMBERCAUSEDTHEFLAMETOFLICKERBUTPRESENTLYDETAILSOFTHEROOMWITHINEMERGEDTH

The search tries all 27,852 moves in both orders, every length 1-20 and the 8 ways of using the table.
```

## Lineage

Inherits from 0238-f13-replicate-k4-table-then-move-length-2-against-fresh-shuffles. What changed: 0237 flagged K4 at table-then-move, key length 2 (p 0.0099 against 100 shuffles) and 0238 replicated it (p 0.023 against 300 fresh shuffles; in that cell 1 of 300 at or above). K4's reading there is junk with 3 of 24 known letters in place; its move reads the carved text down a width-19 grid. Here 0238's search is rerun with the same seeds for lengths 1-2 only, which reproduces the length-2 readings exactly, and K4's and the 300 shuffles' best B2 readings go to the blind judge in one call (F13.3: the judge reads the survivors).

## Hypothesis (domain expert)

The excess is measured by MIX8m, a letter n-gram model; K4's carved order is known to be non-random at widths 7 and 21 (0056: corrected p 0.005 and 0.010), and a move that reads it at width 19 can turn such structure into n-gram-friendly letter pairs without any words. If the judge, which reads for words in order and ignores n-gram texture (reports/judge-bench.md: it beats 4-gram soup, 0233), puts K4's reading above all but 5% of the shuffles' readings, the excess is word-level: a lead for A2 (the known letters defined on an intermediate text). Otherwise it is recorded as one more statistic of the carved order and F13.4d closes on 0237's power. Pre-registered: word-level when K4's judge score has at most 15 of 300 shuffles at or above it; None counts as 0.

## Prediction

The judge scores K4's reading low (under 20) and inside the shuffles' (most 0-20): not word-level. F13.4d closed for lengths 1-12 with the B2 excess written down as a statistic of the carved order.

## Method

1. 0238's attack with lengths 1-2 only (seeds unchanged, so the length-2 screens and climbs are identical).
2. K4's and each shuffle's best reading at B2.
3. All 301 to the judge in one call, blind; K4's rank.

## Result

Candidates returned: 4. Passed all gates: 0. Best crib hits among all candidates: 4/24
(EAST 2/4, NORTHEAST 1/9, BERLIN 0/6, CLOCK 1/5).
Best loss: 213.53775141654864 (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | cribs | 4/24 |  | `LDFCTSBAMCWZEIEDAYSHEEATINQLLVRDJEWINKWORNYDFCHUTVISMNBULOOBLNVCONTRYCFXPAIXHIWCJIPZADKJVBPREJIHG` |  |
| 2 | cribs | 2/24 |  | `HASCIPLYNELEDMLOPNEPPDEKWSIXOROHWFMJWSDAFREYTJORNTCUEJDUFNRMLZIPERUKIYUZPHXWILSHKESTLYQBVUSHOWGYF` |  |
| 3 | cribs | 4/24 |  | `LDFCTSBAMCWZEIEDAYSHEEATINQLLVRDJEWINKWORNYDFCHUTVISMNBULOOBLNVCONTRYCFXPAIXHIWCJIPZADKJVBPREJIHG` |  |
| 4 | cribs | 3/24 |  | `NBENDJZERANDBCKNFILLBAADWRONNWIIHLGARTNRHHKORCULLHCNCSIDEPXMEDFCKRHALORKYXQTRGROWDOJOWSMSHDVNLYAT` |  |

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
  2
 ],
 "screen": "per-column letter-frequency shifts, every move scored by quadgrams; 30 best per order and length",
 "climb": "coordinate ascent, move held, screen's shifts and 5 random starts; MIX8m rescoring",
 "texts": 301,
 "k4_copies": 300,
 "k4_statistic": 4.623,
 "k4_best_cell": "B2",
 "k4_p": 0.0066,
 "copies_statistic_max": 4.743,
 "copies_statistic_median": 0.764,
 "k4_rank_per_cell_copies_at_or_above": {
  "A1": 18,
  "A2": 197,
  "B1": 18,
  "B2": 1
 },
 "judge_k4_b2": 12,
 "judge_reading_k4": "N BEND ? AND ? FILL ? ? CULL ? SIDE ? MED ? ? GROW DO ? ? ? ? AT",
 "judge_copies_at_or_above": 14,
 "judge_copies_max": 15,
 "judge_copies_median": 4.0,
 "judge_none": 0,
 "word_level": true,
 "judge_calls": 301,
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
 "compute_seconds": 281
}
```

Notes: judge: K4's B2 reading 12, shuffles at or above 14 of 300 (max 15): WORD-LEVEL; K4 statistic 4.62 at B2, p 0.007 against 300 shuffles; plant power ; decided lengths []


