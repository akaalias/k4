# 0108-the-copper-read-from-behind: K4 read from the back of the screen, each carved line right to left, with a repeating key or an autokey

**Family:** 4-visual-spatial  
**Parent:** 0089-the-screen-folded-onto-itself  
**Decision:** reverted  
**Run:** 2026-10-15T20:21:04+00:00, 0.3 s, status ran  
**Time by phase:** unattributed 84 s, run 0 s, record 0 s

## In plain words

The letters of Kryptos are cut right through the copper, so the text can be read from behind, where every line runs right to left. The CIA says the table of alphabets was flipped on purpose so that it reads properly only from the back. So perhaps K4 should be read from the back too. We read its four carved lines that way, and in the two other mirror orders, and test the usual short secret words and self-feeding keys against the 24 known letters.

## Walkthrough, by hand

1. Line 11 ends OBKR; from behind it reads RKBO. Line 12 is UOXOGHULBSOLIFBBWFLRVQQPRNGKSSO; from behind, OSSKGNRPQQVRLFWBBFILOSBLUHGOXOU.
2. Join them, line by line: RKBO + line 12 backwards + line 13 backwards + line 14 backwards.
3. The F at place 22 of the carved text now sits at place 4 + (31 - 18 + 1) = 18.
4. With a secret word of length p on the new order, the key letter at 18 is slot 18 mod p; it must turn E into F.
5. Repeat for every key length, table rule, autokey lag and mirror order.

## Worked example (generated)

```
K4 on its carved lines and as read from behind:

  OBKR                              RKBO
  UOXOGHULBSOLIFBBWFLRVQQPRNGKSSO   OSSKGNRPQQVRLFWBBFILOSBLUHGOXOU
  TWTQSJQSSEKZZWATJKLUDIAWINFBNYP   PYNBFNIWAIDULKJTAWZZKESSQJSQTWT
  VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR   RACKEUAUHUKGIDCJTXZKDGWKPFZMTTV

where the known letters sit in the reading from behind:
  22->18 23->17 24->16 25->15 64->38 74->90
```

## Lineage

Inherits from 0089-the-screen-folded-onto-itself. What changed: 0023 tested K4 reversed as a whole. Seen from behind the screen, the letters keep their line order but each carved line reads right to left: R K B O, then line 12 backwards, line 13 backwards, line 14 backwards. That order, and the other two mirror readings of the carved block (lines bottom to top, each forwards; and both, the full reversal), are tested with a repeating key of length 1-26 and with ciphertext and plaintext autokey at every lag, the reading before or after the table.

## Hypothesis (domain expert)

Family 4 open item 'mirrored readings beyond reversal' (families.md). The CIA: the tableau 'is intentionally flipped so it can only be read from the back of the sculpture'; the letters are cut through (01-facts.md); Scheidt: 'mirrors and obfuscation' (C13). On the plate K4 fills columns 28-31 of line 11 and lines 12-14 (31 letters each). Routes: (1) each line reversed, order kept (the view from behind); (2) line order reversed, each line forwards; (3) both (= the full reversal of 0023, kept as a check). Keys, with the route either before the table (the message written, read from behind, then enciphered) or after it: periodic key 1-26 in 8 tableau classes (slot agreement); ciphertext autokey at lags 1-96 (each known letter a direct check); plaintext autokey at lags 1-96 (propagated from the known letters to closure); autokey settings count only with 3+ checks. Ten shuffled coppers.

## Prediction

No reading and key fits: periodic keys dead below period 20, no autokey lag passes all checks, counts inside the coppers' range. Zero candidates.

## Method

1. Lay K4 on its carved lines and build the three mirror orders.
2. For each order, both placements and each class, test periodic keys 1-26 by slot agreement.
3. Ciphertext autokey: each known letter must equal the carved letter minus the carved letter lag places earlier, in the right order.
4. Plaintext autokey: propagate known letters along the lag to closure and stop at a contradiction.
5. Repeat on ten shuffled coppers.

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
 "family": "mirror readings of K4's carved lines with periodic keys and autokeys",
 "orders": [
  "lines reversed (from behind)",
  "line order reversed",
  "both (full reversal)"
 ],
 "placements": [
  "read then table",
  "table then read"
 ],
 "periods": [
  1,
  26
 ],
 "classes": 8,
 "autokey_lags": [
  1,
  96
 ],
 "results": {
  "lines reversed (from behind), read then table": {
   "k4_live_by_period": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
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
   "controls_live_min": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
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
   "controls_live_max": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
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
   "k4_smallest_period_rows": [],
   "ct_autokey_k4": 0,
   "ct_autokey_controls": [
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
   "pt_autokey_k4": 0,
   "pt_autokey_controls": [
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
   ]
  },
  "lines reversed (from behind), table then read": {
   "k4_live_by_period": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    1
   ],
   "controls_live_min": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
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
   "controls_live_max": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    1
   ],
   "k4_smallest_period_rows": [],
   "ct_autokey_k4": 0,
   "ct_autokey_controls": [
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
   "pt_autokey_k4": 0,
   "pt_autokey_controls": [
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
   ]
  },
  "line order reversed, read then table": {
   "k4_live_by_period": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
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
   "controls_live_min": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
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
   "controls_live_max": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
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
   "k4_smallest_period_rows": [],
   "ct_autokey_k4": 0,
   "ct_autokey_controls": [
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
   "pt_autokey_k4": 0,
   "pt_autokey_controls": [
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
   ]
  },
  "line order reversed, table then read": {
   "k4_live_by_period": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
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
   "controls_live_min": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
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
   "controls_live_max": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
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
   "k4_smallest_period_rows": [],
   "ct_autokey_k4": 0,
   "ct_autokey_controls": [
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
   "pt_autokey_k4": 0,
   "pt_autokey_controls": [
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
   ]
  },
  "both (full reversal), read then table": {
   "k4_live_by_period": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    1
   ],
   "controls_live_min": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
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
   "controls_live_max": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    1
   ],
   "k4_smallest_period_rows": [],
   "ct_autokey_k4": 0,
   "ct_autokey_controls": [
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
   "pt_autokey_k4": 0,
   "pt_autokey_controls": [
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
   ]
  },
  "both (full reversal), table then read": {
   "k4_live_by_period": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    1
   ],
   "controls_live_min": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
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
   "controls_live_max": [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    1
   ],
   "k4_smallest_period_rows": [],
   "ct_autokey_k4": 0,
   "ct_autokey_controls": [
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
   "pt_autokey_k4": 0,
   "pt_autokey_controls": [
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
   ]
  }
 },
 "k4_smallest_live_period": {
  "lines reversed (from behind), read then table": null,
  "lines reversed (from behind), table then read": 26,
  "line order reversed, read then table": null,
  "line order reversed, table then read": null,
  "both (full reversal), read then table": 26,
  "both (full reversal), table then read": 26
 },
 "controls": "10 shuffled coppers (seed 108), identical tests"
}
```

Notes: Smallest live period on K4: lines reversed (from behind), read then table: None; lines reversed (from behind), table then read: 26; line order reversed, read then table: None; line order reversed, table then read: None; both (full reversal), read then table: 26; both (full reversal), table then read: 26. Autokey survivors with 3+ checks (lag, class) K4 / controls max: lines reversed (from behind), read then table: CT 0/0, PT 0/0; lines reversed (from behind), table then read: CT 0/0, PT 0/0; line order reversed, read then table: CT 0/0, PT 0/0; line order reversed, table then read: CT 0/0, PT 0/0; both (full reversal), read then table: CT 0/0, PT 0/0; both (full reversal), table then read: CT 0/0, PT 0/0.


