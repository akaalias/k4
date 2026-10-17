# 0187-chaocipher-keyword-left-wheels: F10.1: Chaocipher with the left (cipher) wheel started from any keyword-mixed alphabet at any rotation and the right (plain) wheel free: exact

**Family:** 10-self-changing-alphabets  
**Parent:** 0119-one-free-alphabet-exact  
**Decision:** reverted  
**Run:** 2026-10-17T00:41:25+00:00, 72.4 s, status ran  
**Time by phase:** design 0 s, implement 0 s, test 2 s, run 72 s, record 0 s

## In plain words

Chaocipher uses two alphabet wheels that are shuffled a little after every letter, so the same letter almost never turns into the same code letter twice. A neat property: how the wheels move depends only on the code letters, which we can all read on the copper. So if we guess how the cipher wheel started, the 24 known letters tell us exactly where letters must sit on the other wheel, and contradictions show at once. We try every starting cipher wheel made from an English word, at every turn.

## Walkthrough, by hand

1. Start the left wheel as the alphabet mixed from, say, BERLIN, turned 5 places.
2. Find the carved O on it: its place i says how far both wheels turn; do the same for every carved letter in order.
3. At place 22 the carved F sits at some place i on the left wheel; the known E must sit at place i of the right wheel at that moment, which traces back to one place of the right wheel's start.
4. Every known letter fixes one place of the right wheel's start; two Es must trace back to the same place, two different letters to different places.
5. One contradiction rules the starting wheel out.

## Worked example (generated)

```
left wheel starts as the BERLIN alphabet BERLINACDFGHJKMOPQSTUVWXYZ

place 1: carved O at left-wheel place 15: the left wheel turns by 15, the right by 16
place 2: carved B at left-wheel place 10: the left wheel turns by 10, the right by 11
place 3: carved K at left-wheel place 14: the left wheel turns by 14, the right by 15
place 4: carved R at left-wheel place 12: the left wheel turns by 12, the right by 13
place 5: carved U at left-wheel place 19: the left wheel turns by 19, the right by 20
place 6: carved O at left-wheel place 22: the left wheel turns by 22, the right by 23
place 7: carved X at left-wheel place 5: the left wheel turns by 5, the right by 6
place 8: carved O at left-wheel place 21: the left wheel turns by 21, the right by 22
place 9: carved G at left-wheel place 20: the left wheel turns by 20, the right by 21
place 10: carved H at left-wheel place 13: the left wheel turns by 13, the right by 14
place 11: carved U at left-wheel place 20: the left wheel turns by 20, the right by 21
place 12: carved L at left-wheel place 6: the left wheel turns by 6, the right by 7
place 13: carved B at left-wheel place 23: the left wheel turns by 23, the right by 24
place 14: carved S at left-wheel place 5: the left wheel turns by 5, the right by 6
place 15: carved O at left-wheel place 16: the left wheel turns by 16, the right by 17
place 16: carved L at left-wheel place 6: the left wheel turns by 6, the right by 7
place 17: carved I at left-wheel place 14: the left wheel turns by 14, the right by 15
place 18: carved F at left-wheel place 21: the left wheel turns by 21, the right by 22
place 19: carved B at left-wheel place 14: the left wheel turns by 14, the right by 15
place 20: carved B at left-wheel place 0: the left wheel turns by 0, the right by 1
place 21: carved W at left-wheel place 5: the left wheel turns by 5, the right by 6
place 22: carved F at left-wheel place 4: the left wheel turns by 4, the right by 5
place 23: carved L at left-wheel place 2: the left wheel turns by 2, the right by 3
place 24: carved R at left-wheel place 14: the left wheel turns by 14, the right by 15
```

## Lineage

Inherits from 0119-one-free-alphabet-exact. What changed: F10.1, first family run. Counting checks first: in Chaocipher both wheels turn by the same amount, the place of the carved letter on the left wheel, and the left wheel's moves depend only on carved letters. So once the left wheel's start is fixed, the whole motion is fixed by the carved text, and each known letter says which letter stands at one place of the right wheel's start. The 24 known letters (13 different) then give 11 equalities plus distinctness on a right wheel that is otherwise free: a strong exact test. A free left wheel (26!, about 88 bits) cannot be searched; every keyword-mixed alphabet from the dictionary and the vocabulary (208,627 distinct alphabets) at all 26 rotations can: 5.4 million left wheels, K4 and 10 shuffled copies, compiled.

## Hypothesis (domain expert)

A10 (alphabets that change after every letter; knowledge/12-assumptions.md, for information); Chaocipher, J. F. Byrne 1918, offered to US agencies, method published 2010 (Rubin). Model: left wheel L (cipher), right wheel R (plain), zenith 0, nadir 13; encipher p as L[i] where R[i] = p; then L turned by i and its place-1 letter moved to the nadir, R turned by i + 1 and its place-2 letter moved to the nadir. Given L0, every i_t is fixed by the carved text, R_t[j] = R0[sigma_t(j)], and a known p_t requires R0[sigma_t(i_t)] = p_t. Statistic: consistent left wheels, K4 against 10 copies; plants as builder checks; implementation checked on Byrne's published test vector.

## Prediction

No keyword-started left wheel is consistent on K4 or on the copies (11 equalities each); plants are found. Zero candidates.

## Method

1. Check the implementation on Byrne's test vector (WELLDONEISBETTERTHANWELLSAID).
2. Build every distinct keyword-mixed alphabet from the dictionary and the vocabulary.
3. For each alphabet and rotation as the left wheel's start, run the wheels along each text to the last known place, collecting the right wheel's forced letters; stop at the first contradiction.
4. Count consistent wheels on K4, 10 copies and 3 planted texts.

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
 "family": "Chaocipher, left wheel from any keyword-mixed alphabet (dictionary + vocabulary) at any rotation, right wheel free, exact",
 "test_vector_ok": true,
 "alphabets": 208651,
 "left_wheels": 5424926,
 "consistent": {
  "k4": 0,
  "copies": [
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
  "plants": [
   26,
   26,
   26
  ]
 },
 "plants": [
  {
   "keyword": "SOCIOLOGIAN",
   "rotation": 0
  },
  {
   "keyword": "STRADIVARI",
   "rotation": 10
  },
  {
   "keyword": "TURBOEXCITER",
   "rotation": 5
  }
 ],
 "k4_hits": [],
 "checks": "24 known letters, 13 different: 11 equalities on the right wheel's start, plus distinctness",
 "free_left_wheel": "26! starts (about 88 bits) against about 51 bits of checks: not searchable; blocked",
 "copies": "10 shuffled copies (seed 1870)",
 "seconds": 72,
 "exhaustive": true
}
```

Notes: 5,424,926 left wheels; consistent K4 0 (copies 0-0); plants [26, 26, 26]; Byrne's test vector reproduced


