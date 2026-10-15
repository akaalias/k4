# 0075-doublets-as-nulls: Are the doubled letters fillers? Three of them carry known letters; the other three are struck out

**Family:** 2-masked-then-keyed  
**Parent:** 0057-letter-nulls-outside-the-cribs  
**Decision:** reverted  
**Run:** 2026-10-15T13:29:17+00:00, 3.0 s, status ran  
**Time by phase:** design 42 s, implement 0 s, test 11 s, run 3 s, record 0 s

## In plain words

The copper has six places where a letter repeats its neighbour. One idea is that some of these are fillers, letters added to pad the text. Three of them sit inside EASTNORTHEAST and BERLINCLOCK, and each of their two letters stands for a different known letter, so they cannot be padding. The other three, BB, SS and ZZ, could be. We strike out one letter of each, in every combination, and test the shorter text with the simplest ciphers, against scrambled coppers treated the same way.

## Walkthrough, by hand

1. Strike out the S at place 43 as a null.
2. Every carved letter after it moves one place left: the B of BERLIN, carved N at place 64, becomes place 63 of the 96-letter text.
3. Places 22 and 64 were 42 apart; now they are 41 apart, so under a periodic key they share a slot at different periods than before.
4. Places 22 and 29 are both before the null and stay 7 apart.
5. Run the periodic test on the 96 letters as usual.
6. Repeat for every combination of nulls.

## Worked example (generated)

```
null at carved place 43 (S): text of 96 letters
carved place 22 (F, known E) -> reduced place 22; carved place 64 (N, known B) -> reduced place 63
distance 22 to 64: 42 before, 41 after
```

## Lineage

Inherits from 0057-letter-nulls-outside-the-cribs. What changed: The six doublets are the copper's strangest local feature. A doubled letter could be a filler, a letter written twice or a null. Three of them sit inside the known stretches and carry different known letters, so they cannot be fillers. The other three, BB, SS and ZZ, are struck out one letter each, in every combination, and the shorter text is tested with a repeating key, the self-feeding autokey, and both.

## Hypothesis (domain expert)

Family 2, nulls tied to a visible feature (C17(b), C18(a): 'a bit of stego', a working text of other than 97 letters; C11: 'the other 91 characters'). Structural part: the doublets QQ (26-27), SS (33-34) and TT (68-69) carry the known pairs N,O; S,T; I,N, so neither letter of any of them can be a null, a repeated letter or filler, and any reading of the 6 doublets as 6 nulls (97 - 6 = 91) is dead. Search part: one letter of BB (19-20), SS (43-44) and ZZ (47-48), in each of the 7 non-empty combinations, removed as a null; the cribs keep their carved letters and move to the reduced positions. A null before both cribs (BB) leaves every periodic test unchanged and matters only for the autokey; nulls between the cribs (43, 47) change the cross-crib distances. Systems on each reduced text: periodic key, periods 1-52; ciphertext autokey with a constant, every lag; autokey plus a periodic key up to 26; plain, cipher and key alphabets standard or KRYPTOS, Vigenere or Beaufort, either sign. Controls: ten shuffled coppers with the same positions removed.

## Prediction

No combination makes a periodic key of period 24 or less consistent; the autokey forms have no survivor with three or more checks beyond the controls. Zero candidates pass.

## Method

1. List the 7 combinations of nulls from BB, SS (43-44) and ZZ.
2. Remove them and move each known letter to its reduced place.
3. Run the periodic consistency test at every period up to 52, and the autokey tests at every lag.
4. Repeat on ten shuffled coppers with the same places removed.

## Result

Candidates returned: 0. Passed all gates: 0. Best crib hits among all candidates: 0/24
(no candidates).
Best loss: None (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: 0034-complete-the-key-at-surviving-periods.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| - | no candidates | | | | |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "doublet letters as nulls",
 "inside_crib_doublets": [
  {
   "place": 26,
   "carved": "Q",
   "known": "NO"
  },
  {
   "place": 33,
   "carved": "S",
   "known": "ST"
  },
  {
   "place": 68,
   "carved": "T",
   "known": "IN"
  }
 ],
 "null_combinations": 7,
 "periods": "1-52",
 "results": [
  {
   "nulls": [
    19
   ],
   "periodic_le26": 0,
   "smallest_period": 27,
   "autokey_2plus_checks": 0,
   "autokey_periodic_3plus": 0,
   "controls": {
    "periodic_le26": [
     0,
     0,
     1,
     2,
     0,
     0,
     0,
     1,
     0,
     1
    ],
    "autokey_2plus": [
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
    "autokey_periodic_3plus": [
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
    ]
   }
  },
  {
   "nulls": [
    43
   ],
   "periodic_le26": 8,
   "smallest_period": 26,
   "autokey_2plus_checks": 0,
   "autokey_periodic_3plus": 0,
   "controls": {
    "periodic_le26": [
     8,
     8,
     8,
     8,
     8,
     8,
     8,
     8,
     8,
     8
    ],
    "autokey_2plus": [
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
    "autokey_periodic_3plus": [
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
  {
   "nulls": [
    47
   ],
   "periodic_le26": 8,
   "smallest_period": 26,
   "autokey_2plus_checks": 0,
   "autokey_periodic_3plus": 0,
   "controls": {
    "periodic_le26": [
     8,
     8,
     8,
     8,
     8,
     8,
     8,
     8,
     8,
     8
    ],
    "autokey_2plus": [
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
    "autokey_periodic_3plus": [
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
  {
   "nulls": [
    19,
    43
   ],
   "periodic_le26": 8,
   "smallest_period": 26,
   "autokey_2plus_checks": 0,
   "autokey_periodic_3plus": 0,
   "controls": {
    "periodic_le26": [
     8,
     8,
     8,
     8,
     8,
     8,
     8,
     8,
     8,
     8
    ],
    "autokey_2plus": [
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
    "autokey_periodic_3plus": [
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
  {
   "nulls": [
    19,
    47
   ],
   "periodic_le26": 8,
   "smallest_period": 26,
   "autokey_2plus_checks": 0,
   "autokey_periodic_3plus": 0,
   "controls": {
    "periodic_le26": [
     8,
     8,
     8,
     8,
     8,
     8,
     8,
     8,
     8,
     8
    ],
    "autokey_2plus": [
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
    "autokey_periodic_3plus": [
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
  {
   "nulls": [
    43,
    47
   ],
   "periodic_le26": 8,
   "smallest_period": 26,
   "autokey_2plus_checks": 0,
   "autokey_periodic_3plus": 0,
   "controls": {
    "periodic_le26": [
     8,
     8,
     9,
     10,
     8,
     8,
     8,
     9,
     8,
     9
    ],
    "autokey_2plus": [
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
    "autokey_periodic_3plus": [
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     1,
     0,
     2
    ]
   }
  },
  {
   "nulls": [
    19,
    43,
    47
   ],
   "periodic_le26": 8,
   "smallest_period": 26,
   "autokey_2plus_checks": 0,
   "autokey_periodic_3plus": 0,
   "controls": {
    "periodic_le26": [
     8,
     8,
     9,
     10,
     8,
     8,
     8,
     9,
     8,
     9
    ],
    "autokey_2plus": [
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
    "autokey_periodic_3plus": [
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
    ]
   }
  }
 ]
}
```

Notes: Doublets inside the cribs carrying two different known letters: [(26, 'QQ', 'NO'), (33, 'SS', 'ST'), (68, 'TT', 'IN')], so not nulls. nulls [19]: periodic P<=26 0 (controls 0-2), autokey 2+ checks 0 (0-0), autokey+periodic 3+ 0 (0-1); nulls [43]: periodic P<=26 8 (controls 8-8), autokey 2+ checks 0 (0-0), autokey+periodic 3+ 0 (0-0); nulls [47]: periodic P<=26 8 (controls 8-8), autokey 2+ checks 0 (0-0), autokey+periodic 3+ 0 (0-0); nulls [19, 43]: periodic P<=26 8 (controls 8-8), autokey 2+ checks 0 (0-0), autokey+periodic 3+ 0 (0-0); nulls [19, 47]: periodic P<=26 8 (controls 8-8), autokey 2+ checks 0 (0-0), autokey+periodic 3+ 0 (0-0); nulls [43, 47]: periodic P<=26 8 (controls 8-10), autokey 2+ checks 0 (0-0), autokey+periodic 3+ 0 (0-2); nulls [19, 43, 47]: periodic P<=26 8 (controls 8-10), autokey 2+ checks 0 (0-0), autokey+periodic 3+ 0 (0-1).


