# 0263-f6-amsco-period-23-excess-against-200-shuffles-and-named-keys: F6.22: 0114's AMSCO excess at period 23 (K4 21 live settings against 1-15 on 10 shuffles): the same exact count against 200 fresh shuffles, and K4's live settings' forced keys checked against every 23-letter window of the named texts

**Family:** 6-move-then-table  
**Parent:** 0114-amsco-keyed-by-the-dictionary  
**Decision:** reverted  
**Run:** 2026-10-30T11:22:04+00:00, 81.4 s, status ran  
**Time by phase:** test 17 s, implement 0 s, run 81 s, record 0 s

## In plain words

An old run found that K4 fits one kind of two-step cipher (a grid shuffle called AMSCO, then the cipher table with a 23-letter key) in 21 ways where scrambled copies fit in at most 15. That count is more about the letters than about a message, so we check it against 200 copies, and for each of K4's 21 fits we ask the question that matters: is the 23-letter key it needs a passage from a text Sanborn had to hand?

## Walkthrough, by hand

1. Write the message into a grid under a keyword, alternating cells of one and two letters (AMSCO), and read the columns in the keyword's alphabetical order.
2. Encipher the result on the cipher table with a key of 23 letters, repeating.
3. Each known letter then fixes the key letter at its place mod 23; two known letters at the same key place must agree.
4. Count the grid keywords and tables where they all agree, for K4 and for scrambled copies.
5. For K4's agreeing settings, write out the key letters the known letters force and look for them as a passage of 23 letters in K1-K3, Carter's book or Sanborn's letters.

## Worked example (generated)

```
F6.22: AMSCO keyed by a word, then the table with a 23-letter key.

  AMSCO: write the message in rows of cells holding 1 and 2 letters alternately, read the columns in keyword order
  the table: each moved letter shifted by the key letter at its place mod 23
  the known letters force the key letter at their places mod 23; two known letters in one key place must agree

  count the agreeing settings for K4 and 200 shuffles; for K4's, look for the forced key as a 23-letter passage.
```

## Lineage

Inherits from 0114-amsco-keyed-by-the-dictionary. What changed: F6.22 (Alexis, 2026-10-28, #100: a result that beats its copies gets a row to chase it). 0114 counted AMSCO routes keyed by every dictionary word (3-15 columns, either first cell), then a periodic tableau key on the 8 table classes: at period 23 with the move first, K4 had 21 consistent settings where its 10 shuffles had 1-15, noted and not chased. Here the same exact count at periods 22-24 for K4 and 200 fresh shuffles (vectorised over texts, 0114's routes unchanged), and every setting K4 fits at 23 has its forced key (the shift at each key slot the known letters reach) compared with every 23-letter window of 0210's named texts, both directions, numbered on the standard and KRYPTOS alphabets: a period-23 key taken from a text Sanborn had is the only reading these settings could give.

## Hypothesis (domain expert)

F6 (C1(a): a matrix code, then the table). AMSCO (cells of one and two letters alternately) keyed by a word, then a periodic key of period 23 on the sculpture's table classes (standard or KRYPTOS plain and cipher alphabets, Beaufort or not). A count of consistent settings is a property of a text (0254, 0255: each text has its own level) and a true setting adds only one, so the count cannot single out a message; what can is the key: a period-23 key forced at the known slots that matches a window of K1-K3, the sculpture's texts, Carter or Sanborn's letters. Plant: a Carter message through a random AMSCO route and a 23-letter key from K3's plaintext; its setting must be live and its key window found.

## Prediction

K4's count at 23 inside the 200 shuffles' range (rank under the top 5%); no forced key matches a named-text window; the plant's setting live and its key window found. Zero candidates.

## Method

1. 0114's settings unchanged: every dictionary word's keyword and full-word column order (3-15 columns), first cell 1 or 2, the route and its inverse, deduplicated.
2. For K4, 200 shuffles (seed 2620) and one plant: per route and table class, the shifts at the 24 known places (move first: the key slot is the carved place mod p); live at p when every pair of known places in one slot agrees; counted at p = 22, 23, 24.
3. K4's live settings at 23: the forced shift per slot, matched against every 23-letter window of 0210's named texts (both directions), key letters numbered on the standard or KRYPTOS alphabet.
4. K4's count ranked among the shuffles'; matches listed.

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
 "item": "F6.22 (0114's AMSCO excess at period 23)",
 "routes": 891360,
 "classes": 8,
 "periods": [
  22,
  23,
  24
 ],
 "order": "A (move, then the table)",
 "counts": {
  "22": {
   "k4": 2,
   "copies_min_median_max": [
    0,
    1.0,
    16
   ],
   "copies_at_or_above": 81
  },
  "23": {
   "k4": 21,
   "copies_min_median_max": [
    1,
    8.0,
    31
   ],
   "copies_at_or_above": 4
  },
  "24": {
   "k4": 4184,
   "copies_min_median_max": [
    3962,
    4197.5,
    4537
   ],
   "copies_at_or_above": 111
  }
 },
 "k4_live_at_23": 21,
 "k4_key_matches": [],
 "n_k4_key_matches": 0,
 "named_texts": 38,
 "plant": {
  "route": [
   "MARTINETISM",
   11,
   2,
   "inverse"
  ],
  "class": "kry/std/beau",
  "key": "YBREACHINTHEUPPERLEFTHA",
  "numbering": "std",
  "live": true,
  "key_window_found": true
 },
 "copies": "200 fresh shuffles (seed 2620)",
 "exhaustive": true,
 "compute_seconds": 64,
 "modal_cost_estimate": "891,360 routes x 8 classes, vectorised over 202 texts: about 1-2 core-hours (laptop)"
}
```

Notes: F6.22: K4 live at 23 in 21 settings; 200 shuffles 1-31 (median 8), 4 at or above K4; forced keys matching a named-text window: 0; plant live True, key found True


