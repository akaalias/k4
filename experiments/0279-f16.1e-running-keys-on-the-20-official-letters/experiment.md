# 0279-f16.1e-running-keys-on-the-20-official-letters: F16.1e: the named running keys (0210: K1-K3 plain and cipher, Carter, the tableau and the other named texts, every offset, both directions, on the standard, KRYPTOS and keyword tables) on the 20 official known letters (EAST set aside), with up to five slips; K4 against 0210's 20 copies, its plants and the judge

**Family:** 16-simple-hand-methods  
**Parent:** 0210-running-keys-with-slips-at-known-places  
**Decision:** reverted  
**Run:** 2026-11-17T16:27:36+00:00, 219.3 s, status ran  
**Time by phase:** unattributed 43 s, run 219 s, record 0 s

## In plain words

A running key takes its key letters from a book or an earlier passage, starting at some page and line. Experiment 210 tried every starting place in every text we named, allowing up to seven slips, and found nothing, but it counted EAST. Here we try again with the 20 letters Sanborn published himself, allowing up to five slips.

## Walkthrough, by hand

1. Take a text, say K3's plaintext, and a starting letter in it.
2. Write the text from there under K4, one letter per place.
3. At each of the 20 official known places, look up on the table what the known letter and the text letter give.
4. Count the places where that is not the carved letter; five or fewer may be slips.
5. Try every starting letter, both directions, every table; read the message wherever a start passes.

## Worked example (generated)

```
Carter's book as the key, from letter 1000, standard plain and KRYPTOS cipher alphabet, key letters on KRYPTOS, Vigenere

place  known  key  gives  carved
   64      B    N      Q       N   slip?
   65      E    A      E       Y   slip?
   66      R    T      U       P   slip?

places that disagree, of 24: 20 (7 or fewer would be kept)
```

## Lineage

Inherits from 0210-running-keys-with-slips-at-known-places. What changed: F16.1 (issue #123), fifth part; reruns 0278, which stopped before searching because the loaded 0210 looked for its data under its own folder (its ROOT now set to the repository). 0210's attack.py loaded from its record and run with only the 20 official known places (26-34, 64-74). Its pigeonhole index used 8 blocks of 3 known places to be exact for up to 7 slips; 20 places give 6 whole blocks, so the blocks are taken over the first 18 places and the slip limit is 5 (exact for 5 or fewer), each replacement asserted; the bit counts use 20 places. Everything else as recorded: sources, tables, offsets, copies, plants, judge.

## Hypothesis (domain expert)

F1's running-key arm (C7, C9: the earlier texts as instructions or key; Gillogly 1999 and Schridde 2017 found the K1-K3 running keys give nonsense, 05-attacks.md). Model as 0210: c = table(p, key letter from a named text at offset o + i), forward or backward, Vigenere, Beaufort or variant, on the standard, KRYPTOS or keyword tables, 1.36 x 10^9 trials. Criteria revised 2026-11-17 (#124): EAST is second-hand. With 20 checks and up to 5 slips, chance settings stay near 10^-6 per run: any K4 setting would be a lead; the judge reads every setting found.

## Prediction

No setting on K4 or any copy at up to 5 slips; plants found 3 of 3 (their planted offset, no setting on their own copies). Zero candidates.

## Method

1. Load 0210 from its record; give it the 20 official known letters; blocks of 3 over the first 18 places, slip limit 5.
2. Run it as recorded: every source, offset, direction, table and form, through the block index, each hit checked on all 20 places.
3. Readings of every setting found go to quadgrams and the judge, K4's and the copies' together.

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
 "family": "running keys from the named texts on standard, KRYPTOS and keyword tables, 0-7 known letters slipped (A1.3)",
 "alphabet_pool": 63,
 "setups": {
  "A (K1-K3, every pair)": 23997,
  "B (other sources, one side std/kry or both the same word)": 2037
 },
 "sources": {
  "K1 plain fwd": 63,
  "K1 plain bwd": 63,
  "K2 plain fwd": 369,
  "K2 plain bwd": 369,
  "K3 plain fwd": 336,
  "K3 plain bwd": 336,
  "K1+K2+K3 plain fwd": 768,
  "K1+K2+K3 plain bwd": 768,
  "K1 cipher fwd": 63,
  "K1 cipher bwd": 63,
  "K2 cipher fwd": 369,
  "K2 cipher bwd": 369,
  "K3 cipher fwd": 336,
  "K3 cipher bwd": 336,
  "K1+K2+K3 cipher fwd": 768,
  "K1+K2+K3 cipher bwd": 768,
  "K2 plain corrected ending fwd": 13,
  "K2 plain corrected ending bwd": 13,
  "carter vol1 fwd": 284914,
  "carter vol1 bwd": 284914,
  "tableau rows fwd": 781,
  "tableau rows bwd": 781,
  "tableau rows with index column fwd": 807,
  "tableau rows with index column bwd": 807,
  "tableau columns fwd": 781,
  "tableau columns bwd": 781,
  "morse as carved fwd": 80,
  "morse as carved bwd": 80,
  "morse reversed order fwd": 80,
  "morse reversed order bwd": 80,
  "right panel K1-K4 fwd": 865,
  "right panel K1-K4 bwd": 865,
  "letter 1989 fwd": 2176,
  "letter 1989 bwd": 2176,
  "Cryptogram 1991 fwd": 4880,
  "Cryptogram 1991 bwd": 4880,
  "open letter 2025 fwd": 2228,
  "open letter 2025 bwd": 2228
 },
 "trials": 1360451298,
 "offsets": "every cyclic offset, forward and backward",
 "max_slips": 5,
 "method": "pigeonhole index: 8 blocks of 3 known places, offsets bucketed by their key letters; every offset matching a whole block checked on all 24 (exact for <= 7)",
 "slip_cost_bits": {
  "1": 9.0,
  "2": 17.0,
  "3": 24.3,
  "4": 31.0,
  "5": 37.4
 },
 "chance_settings_at_k": {
  "0": "6.8e-20",
  "1": "3.4e-17",
  "2": "8.1e-15",
  "3": "1.2e-12",
  "4": "1.3e-10",
  "5": "1.0e-08"
 },
 "k4_settings_by_mismatches": [
  0,
  0,
  0,
  0,
  0,
  0
 ],
 "k4_settings": [],
 "copies_settings_by_mismatches": [
  [
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0
  ],
  [
   0,
   0,
   0,
   0,
   0,
   0
  ]
 ],
 "copies_done": 20,
 "copies_judge_best": [
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null
 ],
 "judge": {
  "sent": 3,
  "none": 0
 },
 "plants": [
  {
   "seed": 2101,
   "source": "carter vol1 fwd",
   "offset": 189303,
   "setup": "std/kry/kry/vig",
   "k": 3,
   "slips": [
    27,
    31,
    34
   ],
   "settings_found": 1,
   "by_mismatches": [
    0,
    0,
    0,
    1,
    0,
    0
   ],
   "planted_setting_mismatches": 3,
   "quad": -4.326,
   "judge": 96,
   "judge_reading": "FF TO A FURTHER DEBAUCH OF ### ELSEWHERE THIS WINTER DRAGOMAN AND T### ### WERE DISREGARDED ALIKE AN",
   "own_copies_settings": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
   ],
   "found": true
  },
  {
   "seed": 2102,
   "source": "K1+K2+K3 plain fwd",
   "offset": 307,
   "setup": "SHADOW/keyword/std/std/beau",
   "k": 2,
   "slips": [
    29,
    71
   ],
   "settings_found": 2,
   "by_mismatches": [
    0,
    0,
    2,
    0,
    0,
    0
   ],
   "planted_setting_mismatches": 2,
   "quad": -4.361,
   "judge": 90,
   "judge_reading": "(M)ATTERS IN THE VALLEY WENT ############# D TO WORSE THE TOMBS OF AMENHETEP II ########### INESESII ARE MENTIONED IN T",
   "own_copies_settings": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
   ],
   "found": true
  },
  {
   "seed": 2103,
   "source": "tableau rows bwd",
   "offset": 81,
   "setup": "kry/kry/kry/varbeau",
   "k": 3,
   "slips": [
    27,
    65,
    71
   ],
   "settings_found": 12,
   "by_mismatches": [
    0,
    0,
    0,
    2,
    6,
    4
   ],
   "planted_setting_mismatches": 3,
   "quad": -4.164,
   "judge": 93,
   "judge_reading": "CLOSE TO YOUR WORK AND EVE # # # # EING FOUND AT THE MOMENT YOU WILL NO # # # ME TO BE IDLE TO BEGIN WITH EV",
   "own_copies_settings": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
   ],
   "found": true
  }
 ],
 "covers": "0004, 0017, 0021, 0045, 0047, 0078 (their sources, tables and rules); not 0098/0154 (free alphabet) or 0117 (with moves)",
 "controls": "20 shuffled copies (seeds 2110-2129); each plant against 10 shuffles of its own ciphertext",
 "exhaustive": "yes",
 "item": "F16.1e",
 "known_places": [
  26,
  27,
  28,
  29,
  30,
  31,
  32,
  33,
  34,
  64,
  65,
  66,
  67,
  68,
  69,
  70,
  71,
  72,
  73,
  74
 ],
 "notes_24": "1,360,451,298 trials; K4 settings with <= 7 slips 0; copies [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]; plants found [True, True, True]",
 "aws_cost_estimate_dollars": 0.1,
 "judge_calls_estimate": "the readings of every setting found: 3 on 24 letters; expected under 50"
}
```

Notes: 1,360,451,298 trials; K4 settings with <= 5 slips 0; copies [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]; plants found [True, True, True]


