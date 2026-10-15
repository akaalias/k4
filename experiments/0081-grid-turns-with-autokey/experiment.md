# 0081-grid-turns-with-autokey: A grid turn or K3's rule joined to an autokey, the message (or the cipher) feeding its own key, in both orders

**Family:** 6-transposition-then-tableau  
**Parent:** 0063-transposition-and-ciphertext-autokey  
**Decision:** reverted  
**Run:** 2026-10-15T15:29:43+00:00, 466.3 s, status ran  
**Time by phase:** design 32 s, implement 115 s, test 0 s, run 466 s, record 0 s

## In plain words

In an autokey cipher the secret word is used only to start; after that, each letter is hidden using a letter of the message itself from a fixed distance back (or a letter of the hidden text, in the other kind). The code-breakers at the NSA guessed in 1992 that K4 might be one. Here it is joined to the grid turn of the third message: turn first and then autokey, or autokey first and then turn. Because each letter is tied to the one a fixed distance back, two known letters the right distance apart must agree, whatever the starting word. We test every turn, every distance and both kinds, exactly, and the same on ten scrambled coppers.

## Walkthrough, by hand

1. Write the message in rows of 7 and turn the grid a quarter clockwise (columns read bottom-up, left column first). The L of CLOCK (place 71) lands at place 4 and the O after it (place 72) at place 18.
2. Take the plaintext autokey at lag 14 on the sculpture's alphabet, Vigenere: each letter of the turned text is the copper letter minus the turned-text letter 14 places earlier.
3. Places 4 and 18 are 14 apart, so they are tied directly.
4. The copper at 18 is F, index 12; L is index 17; 12 - 17 = -5, which is 21, the letter U.
5. The known letter there is O, not U: lag 14 under this turn is dead.
6. Do the same for every pair of known letters in one class of the lag, every lag, turn and table, in both orders and for the ciphertext autokey, and on ten scrambled coppers.

## Worked example (generated)

```
order A: one quarter turn clockwise at width 7, then plaintext autokey at lag 14, sculpture's alphabet, Vigenere

known place  letter  lands at  class mod 14
         71       L         4             3
         64       B         5             4
         29       T        10             9
         22       E        11            10
         72       O        18             3
         65       E        19             4
         30       H        24             9
         23       A        25            10

pair in class 3: place 71 (L) lands at 4, place 72 (O) at 18
  letter at 18 = copper F (12) minus previous (17) = 21 = U
  chain gives U, known letter O: disagrees, dead
```

## Lineage

Inherits from 0063-transposition-and-ciphertext-autokey. What changed: 0063 joined column shuffles to the ciphertext autokey only. Here the routes are K3's rule at every setting, one or two quarter turns at every width, and plain and keyed columnar, and the autokey is either kind: the plaintext autokey, which the NSA named in 1992 and which no public search has joined to a grid turn, and the ciphertext autokey. Both orders, every lag 1-96, on one alphabet throughout (standard or KRYPTOS), solved exactly.

## Hypothesis (domain expert)

Type 1 of directions.md, gap a2 of the prior-work database ('Rotation + plaintext autokey on the KA tableau... autokey under transposition is covered only for columnar <= 7 publicly; 0063 covered ciphertext autokey only'); also type 2's open item 'columnar plus autokey above width 7' (nitsuah). Clues C1(a) (02-sanborn-said.md, CNN 2005, 'double matrixes... then went back to this table'), C2(a) (the K3 matrix and its shifts) and C11a (NSA 1992, 'plain-text auto-key', Black Vault). Plaintext autokey at lag L on one alphabet A: C[j] = Z[j] (+) Z[j-L], so decryption is Z[j] = sigma Z[j-L] + tau C[j] (Vigenere sigma = -1, tau = 1; Beaufort 1, -1; variant 1, 1), linear mod 26 along each residue class mod L; two known letters in one class give one exact check, whatever the primer. Ciphertext autokey: Z[j] = dec(C[j], C[j-L]), every known letter past the primer is a check. Order A: move the message, then the autokey on the moved text (known letters at their landing places, W = the copper). Order B: autokey on the message, then move (known letters in place, W = the copper unmoved). Routes as 0080: K3's rule a + b i mod 97 (9,312), one quarter turn cw or ccw at widths 2-96, two cw turns at every width pair 2-96, plain columnar both directions, keyed columnar from every vocabulary word, each forward and inverse, deduplicated (27,752). Six conventions (one alphabet throughout, as on the carved table, three modes). Lags 1-96. Exact; ten shuffled coppers through the identical search. Left open: mixed plain/cipher/key alphabets with these routes, padded grids (gap a1).

## Prediction

No setting on K4 survives four or more checks in either kind or order. At every number of checks the count of consistent settings on K4 lies inside the range of the ten shuffled coppers, give or take the spread at one and two checks. Zero candidates.

## Method

1. Build the routes and keep one per distinct reordering.
2. For each route, lag, convention and order, list the pairs of known letters in the same class mod the lag (plaintext autokey) or the known letters past the primer (ciphertext autokey).
3. Walk each pair's chain through the copper, or through the copper unmoved, and compare; stop at the first disagreement.
4. Count consistent settings by number of checks.
5. Repeat on ten shuffled coppers.
6. Print any K4 setting with four or more checks.

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
 "family": "route (K3 rule, quarter turns, columnar) joined to plaintext or ciphertext autokey, both orders, solved exactly",
 "route_specs": 28246,
 "distinct_routes": 27752,
 "routes_done": 27752,
 "lags": [
  1,
  96
 ],
 "conventions": "one alphabet throughout (standard or KRYPTOS) x Vigenere, Beaufort, variant = 6",
 "planted_check": true,
 "by_kind_and_order": {
  "ptak order A": {
   "k4_at_least_c": {
    "1": 63778,
    "2": 2182,
    "3": 88,
    "4": 1,
    "5": 0,
    "6": 0
   },
   "controls_at_least_c": {
    "1": [
     65209,
     64452,
     64433,
     65043,
     64452,
     64391,
     64041,
     64855,
     66323,
     65109
    ],
    "2": [
     2279,
     2254,
     2310,
     2209,
     2381,
     2328,
     2274,
     2347,
     2447,
     2461
    ],
    "3": [
     66,
     76,
     69,
     65,
     97,
     74,
     88,
     89,
     81,
     77
    ],
    "4": [
     4,
     2,
     1,
     3,
     2,
     3,
     2,
     1,
     3,
     2
    ],
    "5": [
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
    "6": [
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
   "k4_exactly_c": {
    "1": 61596,
    "2": 2094,
    "3": 87,
    "4": 1
   },
   "max_checks_seen": 4
  },
  "ptak order B": {
   "k4_at_least_c": {
    "1": 20820,
    "2": 382,
    "3": 27,
    "4": 3,
    "5": 0,
    "6": 0
   },
   "controls_at_least_c": {
    "1": [
     21771,
     21629,
     21300,
     21626,
     21969,
     21140,
     21098,
     21475,
     21476,
     21940
    ],
    "2": [
     503,
     528,
     410,
     381,
     436,
     372,
     443,
     381,
     418,
     508
    ],
    "3": [
     58,
     31,
     39,
     19,
     31,
     41,
     39,
     39,
     44,
     103
    ],
    "4": [
     0,
     0,
     2,
     1,
     0,
     1,
     1,
     1,
     1,
     2
    ],
    "5": [
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
    "6": [
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
   "k4_exactly_c": {
    "1": 20438,
    "2": 355,
    "3": 24,
    "4": 3
   },
   "max_checks_seen": 4
  },
  "ctak order A": {
   "k4_at_least_c": {
    "1": 20772,
    "2": 794,
    "3": 20,
    "4": 0,
    "5": 0,
    "6": 0
   },
   "controls_at_least_c": {
    "1": [
     20838,
     17763,
     22060,
     21746,
     20529,
     17363,
     17809,
     21629,
     21460,
     21511
    ],
    "2": [
     1146,
     664,
     1247,
     930,
     950,
     680,
     840,
     1012,
     849,
     985
    ],
    "3": [
     29,
     32,
     25,
     34,
     41,
     25,
     32,
     35,
     32,
     18
    ],
    "4": [
     1,
     3,
     0,
     2,
     2,
     4,
     1,
     1,
     0,
     1
    ],
    "5": [
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
    "6": [
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
   "k4_exactly_c": {
    "1": 19978,
    "2": 774,
    "3": 20
   },
   "max_checks_seen": 4
  },
  "ctak order B": {
   "k4_at_least_c": {
    "1": 6825,
    "2": 214,
    "3": 7,
    "4": 0,
    "5": 0,
    "6": 0
   },
   "controls_at_least_c": {
    "1": [
     6602,
     6835,
     6566,
     6746,
     6759,
     6192,
     6390,
     6050,
     6910,
     6616
    ],
    "2": [
     250,
     263,
     236,
     254,
     248,
     235,
     243,
     231,
     247,
     235
    ],
    "3": [
     10,
     9,
     7,
     12,
     11,
     14,
     7,
     10,
     3,
     7
    ],
    "4": [
     0,
     1,
     0,
     1,
     0,
     0,
     2,
     2,
     0,
     0
    ],
    "5": [
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
    "6": [
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
   "k4_exactly_c": {
    "1": 6611,
    "2": 207,
    "3": 7
   },
   "max_checks_seen": 4
  }
 },
 "levels_outside_control_range": [
  "ptak A: [1, 2]",
  "ptak B: [1, 4]",
  "ctak B: [2]"
 ],
 "k4_settings_with_4_plus_checks": [
  {
   "kind": "plaintext autokey",
   "order": "B",
   "route": {
    "kind": "k3rule",
    "a": 85,
    "b": 43
   },
   "alphabet": "std",
   "mode": "var",
   "lag": 49,
   "checks": 4
  },
  {
   "kind": "plaintext autokey",
   "order": "B",
   "route": {
    "kind": "turn2",
    "w1": 38,
    "w2": 49,
    "dir": "inv"
   },
   "alphabet": "kry",
   "mode": "var",
   "lag": 33,
   "checks": 4
  },
  {
   "kind": "plaintext autokey",
   "order": "B",
   "route": {
    "kind": "turn2",
    "w1": 76,
    "w2": 37,
    "dir": "inv"
   },
   "alphabet": "kry",
   "mode": "var",
   "lag": 33,
   "checks": 4
  },
  {
   "kind": "plaintext autokey",
   "order": "A",
   "route": {
    "kind": "turn2",
    "w1": 84,
    "w2": 15,
    "dir": "inv"
   },
   "alphabet": "std",
   "mode": "var",
   "lag": 37,
   "checks": 4
  }
 ],
 "n_k4_4_plus": 4,
 "controls": "10 shuffled coppers (seed 81), identical search"
}
```

Notes: 27,752 distinct routes x 96 lags x 6 conventions x 2 kinds x 2 orders. ptak order A: K4 >=1..6 [63778, 2182, 88, 1, 0, 0], controls max [66323, 2461, 97, 4, 0, 0]; ptak order B: K4 >=1..6 [20820, 382, 27, 3, 0, 0], controls max [21969, 528, 103, 2, 0, 0]; ctak order A: K4 >=1..6 [20772, 794, 20, 0, 0, 0], controls max [22060, 1247, 41, 4, 0, 0]; ctak order B: K4 >=1..6 [6825, 214, 7, 0, 0, 0], controls max [6910, 263, 14, 2, 0, 0]. Outside the control range: ['ptak A: [1, 2]', 'ptak B: [1, 4]', 'ctak B: [2]']. K4 settings with 4+ checks: 4. Planted texts found: True.


