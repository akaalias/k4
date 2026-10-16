# 0161-two-tables-round-a-move: F6.7: change, move, change with the two keyed stages on different tables (standard then KRYPTOS, or the reverse), key lengths 2-14 each, solved exactly

**Family:** 6-transposition-then-tableau  
**Parent:** 0080-key-on-both-sides-of-the-move  
**Decision:** reverted  
**Run:** 2026-10-16T22:34:53+00:00, 102.1 s, status ran  
**Time by phase:** unattributed 101 s, run 102 s, record 0 s

## In plain words

Two secret words, one used on the plain alphabet's table and the other on the KRYPTOS table, with the letters moved in a grid between them. Because the tables differ, the two words cannot simply be added together, but each known letter still ties one letter of the first word to one letter of the second. Following those ties decides exactly whether any pair of words of lengths 2 to 14 fits, for each grid move, on the carved text and on scrambled copies.

## Walkthrough, by hand

1. Encipher with a first word of length 5 on the plain-alphabet table.
2. Write the result in rows of 9 and read down the columns.
3. Encipher again with a second word of length 7 on the KRYPTOS table: the carved text.
4. A known letter E at place 22 sits under first-word letter 22 mod 5 and, after the move, under second-word letter (its new place) mod 7.
5. Guess the first-word letter: the E becomes a definite middle letter, and the carved letter then fixes the second-word letter.
6. Follow every such tie; a contradiction for all 26 guesses rules the setting out.

## Worked example (generated)

```
first word on the plain-alphabet table, a grid move, second word on the KRYPTOS table

at a known place: guess the first-word letter v; the known letter plus v (plain alphabet) is the middle letter;
the carved letter minus the middle letter (KRYPTOS alphabet) is the second-word letter: one second letter per guess.
every known letter ties a first-word slot to a second-word slot this way; a contradiction for all 26 guesses rules the setting out.
```

## Lineage

Inherits from 0080-key-on-both-sides-of-the-move. What changed: F6.7 (pivot audit, issue #55, D5). 0080 tested a repeating key, a move, then a second repeating key, both on the same table. Here the two keyed stages use different tables: the standard alphabet first and the KRYPTOS alphabet second, or the reverse. With different tables the two keys no longer add, but each known letter still links one slot of the first key to one slot of the second by a one-to-one relation, so every connected group of slots has at most 26 consistent assignments: solved exactly. Moves: 0160's library (844 distinct: the four column readings at every width, K3's rule at every multiplier, forwards and inverted); key lengths 2-14 each; both orders of tables; each stage added or Beaufort-subtracted. Ten scrambled coppers.

## Hypothesis (domain expert)

C1(a)/(c), C20(a) ('layer two'), C5(b) ('key word/s': two words), C27(c) (Sanborn's 'slightly different' table: the two halves of the work use the two alphabets). Model: y_i = A^-1(A(p_i) + s1 k1[i mod m]); carved c_{M(i)} = B^-1(B(y_i) + s2 k2[M(i) mod n]) with (A, B) = (standard, KRYPTOS) or (KRYPTOS, standard), s1, s2 in {+1, -1}, m, n 2-14. Each known letter gives k2[M(i) mod n] = s2 (B(c) - B(A^-1(A(p) + s1 k1[i mod m]))), a bijection between the two slot values; consistency decided by propagation over each component (26 trials per component). Checks = links - slots + components. Statistic fixed before the run: consistent settings with at least five checks on K4 against the coppers' range (0080's threshold), and the same count per check level.

## Prediction

No setting with five or more checks fits K4; counts at each check level inside the coppers' range. Zero candidates.

## Method

1. Build the 844 moves.
2. For each text, move, table order, signs and key lengths m, n: the links (slot of k1, slot of k2) at the 24 known letters.
3. Propagate each component from each of 26 values; consistent if one value closes every link.
4. Count consistent settings by checks; compare K4 with the coppers.

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
 "family": "change (table A), move, change (table B != A): two repeating keys of lengths 2-14 on different tables round one of 844 moves",
 "moves": 844,
 "key_lengths": [
  2,
  14
 ],
 "table_orders": [
  "std then kry",
  "kry then std"
 ],
 "signs": 4,
 "consistent_by_checks": {
  "0": {
   "k4": 11816,
   "coppers_min": 11816,
   "coppers_max": 11816
  },
  "1": {
   "k4": 15084,
   "coppers_min": 14812,
   "coppers_max": 15448
  },
  "2": {
   "k4": 3772,
   "coppers_min": 3684,
   "coppers_max": 4052
  },
  "3": {
   "k4": 1220,
   "coppers_min": 1088,
   "coppers_max": 1332
  },
  "4": {
   "k4": 524,
   "coppers_min": 468,
   "coppers_max": 552
  },
  "5": {
   "k4": 348,
   "coppers_min": 276,
   "coppers_max": 460
  },
  "6": {
   "k4": 16,
   "coppers_min": 4,
   "coppers_max": 32
  },
  "7": {
   "k4": 16,
   "coppers_min": 0,
   "coppers_max": 20
  },
  "8": {
   "k4": 4,
   "coppers_min": 0,
   "coppers_max": 4
  }
 },
 "k4_consistent_with_5_or_more_checks": 388,
 "coppers_with_5_or_more": [
  444,
  300,
  432,
  344,
  372,
  388,
  432,
  468,
  504,
  360
 ],
 "k4_top": [
  {
   "move": "ccw84inv",
   "tables": "std then kry, signs +1+1",
   "m": 13,
   "n": 13,
   "checks": 9
  },
  {
   "move": "ccw84inv",
   "tables": "std then kry, signs +1-1",
   "m": 13,
   "n": 13,
   "checks": 9
  },
  {
   "move": "ccw84inv",
   "tables": "std then kry, signs -1+1",
   "m": 13,
   "n": 13,
   "checks": 9
  },
  {
   "move": "ccw84inv",
   "tables": "std then kry, signs -1-1",
   "m": 13,
   "n": 13,
   "checks": 9
  },
  {
   "move": "colr84inv",
   "tables": "std then kry, signs +1+1",
   "m": 13,
   "n": 13,
   "checks": 8
  },
  {
   "move": "colr84inv",
   "tables": "std then kry, signs +1-1",
   "m": 13,
   "n": 13,
   "checks": 8
  },
  {
   "move": "colr84inv",
   "tables": "std then kry, signs -1+1",
   "m": 13,
   "n": 13,
   "checks": 8
  },
  {
   "move": "colr84inv",
   "tables": "std then kry, signs -1-1",
   "m": 13,
   "n": 13,
   "checks": 8
  },
  {
   "move": "k3x23",
   "tables": "std then kry, signs +1+1",
   "m": 13,
   "n": 12,
   "checks": 7
  },
  {
   "move": "k3x23",
   "tables": "std then kry, signs +1-1",
   "m": 13,
   "n": 12,
   "checks": 7
  },
  {
   "move": "k3x23",
   "tables": "std then kry, signs -1+1",
   "m": 13,
   "n": 12,
   "checks": 7
  },
  {
   "move": "k3x23",
   "tables": "std then kry, signs -1-1",
   "m": 13,
   "n": 12,
   "checks": 7
  },
  {
   "move": "colr34inv",
   "tables": "std then kry, signs +1+1",
   "m": 12,
   "n": 12,
   "checks": 7
  },
  {
   "move": "colr34inv",
   "tables": "std then kry, signs +1-1",
   "m": 12,
   "n": 12,
   "checks": 7
  },
  {
   "move": "colr34inv",
   "tables": "std then kry, signs -1+1",
   "m": 12,
   "n": 12,
   "checks": 7
  },
  {
   "move": "colr34inv",
   "tables": "std then kry, signs -1-1",
   "m": 12,
   "n": 12,
   "checks": 7
  },
  {
   "move": "colr7",
   "tables": "std then kry, signs +1+1",
   "m": 13,
   "n": 12,
   "checks": 7
  },
  {
   "move": "colr7",
   "tables": "std then kry, signs +1-1",
   "m": 13,
   "n": 12,
   "checks": 7
  },
  {
   "move": "colr7",
   "tables": "std then kry, signs -1+1",
   "m": 13,
   "n": 12,
   "checks": 7
  },
  {
   "move": "colr7",
   "tables": "std then kry, signs -1-1",
   "m": 13,
   "n": 12,
   "checks": 7
  }
 ],
 "seconds": 102,
 "controls": "10 shuffled coppers (seed 1607)",
 "exhaustive": true
}
```

Notes: 844 moves x 169 key-length pairs x 8 table/sign settings: consistent with >= 5 checks K4 388 (coppers 300-504); by checks 1-4 K4 [15084, 3772, 1220, 524]


