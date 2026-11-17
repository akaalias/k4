# 0273-f14.2b-0272s-edge-cell-a25-on-2000-fresh-shuffles: F14.2b: 0272's edge cell (move then table, key length 25, settings with 4 or fewer informative checks) on K4 against 2,000 fresh shuffles

**Family:** 14-scheidt-mask-keyed-by-words  
**Parent:** 0272-f14.2a-0271s-flawed-settings-decided-in-full  
**Decision:** reverted  
**Run:** 2026-11-17T12:18:16+00:00, 82.3 s, status ran  
**Time by phase:** design 48 s, implement 0 s, test 37 s, run 82 s, record 0 s

## In plain words

The last run found one small corner where the real carved text did a little better than all 50 scrambled copies: recipes with a key 25 letters long, where the known words give too few comparisons to pick the alphabets, so the run only counted how many alphabet pairs fit. One corner in 76 beating 50 copies happens by chance about once in a run. This run tests that corner alone against 2,000 new scrambled copies, enough to tell chance from a real signal.

## Walkthrough, by hand

1. Take one recipe: a grid move, then the table, key length 25.
2. Follow the 24 known letters to their carved places and key slots.
3. Where two equal known letters (two E's) share a slot, their carved letters must be equal; if not, the recipe is out.
4. Count the alphabet pairs that put every other pair of known letters in a shared slot the right distance apart.
5. Do the same on 2,000 scrambled copies of the carved text.
6. Count how many copies reach K4's total.

## Worked example (generated)

```
F14.2b: one cell of 0272, against 2,000 fresh shuffles.

  cell       a grid move, then the table, key length 25; 295 settings with 4 or fewer informative checks
  repeats    two known E's in one key slot must sit over one carved letter, or the setting is out
  count      the alphabet pairs that fit every other check, exactly, out of 208,064 x 208,064
  verdict    K4's total ranked among the 2,000 shuffles' totals; a flag needs p below 0.05 / 76
```

## Lineage

Inherits from 0272-f14.2a-0271s-flawed-settings-decided-in-full. What changed: F14.2b, the chase of 0272's one edge cell. In 0272 the count-only class A25 Beaufort (order A: the move first, then the table; key length 25; 295 settings whose same-slot checks hold 4 or fewer between different known letters) gave K4 3,718,027 fitting alphabet pairs against a shuffle median of 0 and max 3,444,844 (p 0.02 of 76 cells, corrected line 0.00066). Same settings, same exact test (0272's code, frozen), on K4 and 2,000 fresh shuffles (seed 2272, not 0271's), both forms; which setting carries K4's count, and how many of its checks are repeated-letter checks.

## Hypothesis (domain expert)

F14 (C4(a), C5; 03-scheidt-said.md 'masked the English language', 'executed with the correct key word/s') with Sanborn's matrix step (C1(a)): a type-1 move of 0129's library, then a Quagmire IV table on two dictionary keyword alphabets (0244's 208,064), key length 25. At 4 or fewer informative checks the 24 known letters cannot pick an alphabet pair (4.3 x 10^10 / 26^c pairs fit by chance) and no dictionary word is 25 letters long, so 0271 and 0272 only counted pairs. A setting's count is non-zero only if its repeated-letter checks hold (two equal known letters in one key slot over equal carved letters), so the count measures how often K4's carved letters repeat where a move's slots put repeated known letters. Pre-registered: the primary statistic is K4's A25 Beaufort pair count, ranked among 2,000 fresh shuffles; it flags only at p below 0.05 / 76 = 0.00066 (0272's 76 cells). Secondary, reported: A25 added, and the number of A25 settings with any fit, both forms.

## Prediction

K4's A25 Beaufort count is not unusual against 2,000 fresh shuffles: p above 0.00066 (expected near 0.02-0.05, the rate at which shuffles pass a setting's repeated-letter checks). Plants on these settings pass their own setting 12/12.

## Method

1. Settings: 0272's list restricted to order A, key length 25, 4 or fewer informative checks (295).
2. Texts: K4 and 2,000 shuffles of it (seed 2272).
3. Per text, setting and form: repeated-letter checks need equal carved letters; if they hold, the informative checks count the fitting pairs among 208,064 x 208,064 keyword alphabets exactly (0271's index, as 0272).
4. Per text: total pairs and settings with a fit, per form.
5. p = (1 + shuffles at or above K4) / 2,001.
6. Plants: 12 English messages with the known words, enciphered on random settings of the 295 with two random dictionary keyword alphabets, a random 25-letter key and a random form; found if their own setting counts a fit and the true pair satisfies every check.

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
 "item": "F14.2b",
 "cell": "order A (move then table), key length 25, 4 or fewer informative checks",
 "settings": 295,
 "alphabets": 208064,
 "pairs_per_setting_and_form": 43290628096,
 "texts": 2001,
 "shuffle_seed": 2272,
 "exhaustive": true,
 "k4_reproduces_0272": true,
 "primary_A25_Beaufort_pairs": {
  "k4": 3718027,
  "copies_nonzero": 154,
  "copies_median": 0.0,
  "copies_max": 97342649,
  "at_or_above": 40,
  "p": 0.02049
 },
 "A25_added_pairs": {
  "k4": 3150163,
  "copies_nonzero": 154,
  "copies_median": 0.0,
  "copies_max": 128712794,
  "at_or_above": 54,
  "p": 0.02749
 },
 "settings_with_fit_Beaufort": {
  "k4": 1,
  "copies_nonzero": 154,
  "copies_median": 0.0,
  "copies_max": 4,
  "at_or_above": 154,
  "p": 0.07746
 },
 "settings_with_fit_added": {
  "k4": 1,
  "copies_nonzero": 154,
  "copies_median": 0.0,
  "copies_max": 4,
  "at_or_above": 154,
  "p": 0.07746
 },
 "corrected_line": 0.00066,
 "flag": false,
 "k4_settings_with_fit": [
  {
   "route": 13027,
   "form": "V",
   "pairs": 3150163,
   "checks": 5,
   "repeated": 2,
   "informative": 3,
   "route_name": "two turns cw 19,62 inverse"
  },
  {
   "route": 13027,
   "form": "B",
   "pairs": 3718027,
   "checks": 5,
   "repeated": 2,
   "informative": 3,
   "route_name": "two turns cw 19,62 inverse"
  }
 ],
 "plants": [
  {
   "route": "K3 rule a=27 b=12 inverse",
   "form": "V",
   "pairs_counted": 8330232444,
   "true_pair_fits": true,
   "found": true
  },
  {
   "route": "two turns cw 17,92",
   "form": "V",
   "pairs_counted": 5385841,
   "true_pair_fits": true,
   "found": true
  },
  {
   "route": "K3 rule a=8 b=8",
   "form": "V",
   "pairs_counted": 86069516,
   "true_pair_fits": true,
   "found": true
  },
  {
   "route": "two turns cw 16,77",
   "form": "B",
   "pairs_counted": 2169513,
   "true_pair_fits": true,
   "found": true
  },
  {
   "route": "two turns cw 86,12",
   "form": "V",
   "pairs_counted": 1055849260,
   "true_pair_fits": true,
   "found": true
  },
  {
   "route": "two turns cw 91,12",
   "form": "V",
   "pairs_counted": 68600042,
   "true_pair_fits": true,
   "found": true
  },
  {
   "route": "two turns cw 46,54 inverse",
   "form": "B",
   "pairs_counted": 6977051,
   "true_pair_fits": true,
   "found": true
  },
  {
   "route": "two turns cw 12,88",
   "form": "B",
   "pairs_counted": 68039,
   "true_pair_fits": true,
   "found": true
  },
  {
   "route": "two turns cw 12,93",
   "form": "B",
   "pairs_counted": 2817770,
   "true_pair_fits": true,
   "found": true
  },
  {
   "route": "two turns cw 66,57",
   "form": "V",
   "pairs_counted": 1632450,
   "true_pair_fits": true,
   "found": true
  },
  {
   "route": "K3 rule a=57 b=8",
   "form": "B",
   "pairs_counted": 437312812,
   "true_pair_fits": true,
   "found": true
  },
  {
   "route": "two turns cw 8,94 inverse",
   "form": "V",
   "pairs_counted": 765694186,
   "true_pair_fits": true,
   "found": true
  }
 ],
 "plants_found": 12,
 "plants_total": 12,
 "core_seconds": 11,
 "resumed_units": 0,
 "cost_estimate": "295 settings x 2,001 texts, the index built only where repeated-letter checks hold: minutes on 32 cores, under $0.10"
}
```

Notes: F14.2b: A25 Beaufort pairs K4 3,718,027, 40 of 2,000 fresh shuffles at or above (p 0.02049; line 0.00066; flag False); A25 added p 0.02749; settings with a fit (Beaufort) K4 1, p 0.07746. K4's fitting settings: [{'route': 13027, 'form': 'V', 'pairs': 3150163, 'checks': 5, 'repeated': 2, 'informative': 3, 'route_name': 'two turns cw 19,62 inverse'}, {'route': 13027, 'form': 'B', 'pairs': 3718027, 'checks': 5, 'repeated': 2, 'informative': 3, 'route_name': 'two turns cw 19,62 inverse'}]. Plants 12/12.


