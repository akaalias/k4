# 0120-one-free-alphabet-english-climb-at-23-and-26: The two key lengths a free alphabet survives (Beaufort form, 23 and 26): climb the alphabet toward English with the 24 known letters fixed, against scrambled coppers at equal effort

**Family:** 1-keyed-periodic  
**Parent:** 0119-one-free-alphabet-exact-at-every-key-length  
**Decision:** reverted  
**Run:** 2026-10-16T08:09:36+00:00, 968.2 s, status ran  
**Time by phase:** design 45 s, implement 410 s, test 229 s, run 968 s, record 36 s

## In plain words

The last experiment showed that with one scrambled alphabet on both sides of the table, only two key lengths, 23 and 26, can produce the 24 known letters at all, and only with the table used the Beaufort way (key minus letter). For those two lengths we now let a computer shuffle the alphabet and the key bit by bit, keeping the known letters right, and push the other 73 letters toward English. A climb like this always makes some English-looking fragments, so the same climb is run on scrambled copies of the carved text; K4 only counts if it does better than all of them. To know whether the climb could find a real answer, we also hide real English under random alphabets and see whether the climb digs it out.

## Walkthrough, by hand

1. Take key length 23 and write K4 in rows of 23, so each column is one key slot.
2. Guess an order for the alphabet (26 letters in some sequence) and number its places 0-25.
3. In a column holding a known letter, the key value is (place of the carved letter + place of the known letter) mod 26; every known letter in that column must give the same value.
4. In the six columns with no known letter, guess a key value.
5. Decipher every letter: known-letter place = key value minus carved-letter place, mod 26, read back through the alphabet.
6. Score the 73 unknown letters by how English their four-letter groups are.
7. Swap two letters of the alphabet or change one free key value; keep the change if the score improves (sometimes even if not, less often as the search cools); repeat many thousands of times.
8. Do exactly the same with scrambled copies of K4 and with hidden English, and compare the best scores.

## Worked example (generated)

```
key length 23, Beaufort form: K4 in rows of 23; each column is one key slot

  O B K R U O X O G H U L B S O L I F B B W F L
  R V Q Q P R N G K S S O T W T Q S J Q S S E K
  Z Z W A T J K L U D I A W I N F B N Y P V T T
  M Z F P K W G D K Z X T J C D I G K U H U A U
  E K C A R

columns holding two known letters (each gives one check: place(c1)+place(p1) = place(c2)+place(p2)):
  column 0: S under R (24), C under M (70)
  column 1: T under V (25), L under Z (71)
  column 2: N under Q (26), O under F (72)
  column 3: O under Q (27), C under P (73)
  column 4: R under P (28), K under K (74)
  column 21: E under F (22), I under T (68)
  column 22: A under L (23), N under T (69)

best climbed alphabet: JCRBOQYZPXVWHSMGAUKNFTIELD
key values: [15, 5, 24, 9, 10, 23, 5, 12, 8, 0, 8, 6, 24, 17, 18, 21, 0, 22, 3, 10, 8, 17, 14]
place 22: carved F at 20, key 17: 17 - 20 = 23 -> E
```

## Lineage

Inherits from 0119-one-free-alphabet-exact-at-every-key-length. What changed: F1.1, second step (English climb). 0119 left one unknown alphabet on both sides alive only in the Beaufort form at key lengths 23 (7 checks) and 26 (1 check). Consistency cannot decide those, so here the alphabet and the free key values are climbed by simulated annealing toward English on the 73 unknown letters, with the 24 known letters held by a penalty that must reach zero. The same climb, same effort, runs on 12 scrambled coppers per length that also fit at that length (drawn by 0119's exact test), and on 6 planted English texts per length to measure power.

## Hypothesis (domain expert)

C27(c) (a tableau 'slightly different from the one on Kryptos'), C1(b) (the table alone). Model: one unknown bijection A on both sides, key k of length L in {23, 26}, Beaufort form A(c_i) = k[i mod L] - A(p_i) (decryption p_i = A^-1(k[i mod L] - A(c_i))); the 0119 exact test shows only these two (form, length) pairs admit any alphabet for 1-26. Given A, the key at every slot holding a known letter is forced (majority value; disagreements are violations); the remaining slots (6 at 23, 3 at 26) are free. Search: simulated annealing over A (swap two letters' places) and the free key values, objective = mean log10 quadgram score of the 73 non-crib letters (the harness's english_score of free_text) minus 1.0 per violation, linear cooling from 0.05 to 0.002, 20 restarts of 200,000 moves; only zero-violation states count. These settings were chosen in dry runs on planted texts before the run (penalty 0.4 and hotter schedules did worse); in those dry runs no setting got a planted text back, and the climb could not even return to the true alphabet from two swaps away, because one swap changes letters in every slot and the forced key values with them. Controls: shuffles of K4 that fit exactly at the same length and form (0119's decider), 12 per length, same restarts and iterations. Power: 6 planted texts per length, 97-letter windows of Carter's Tomb of Tut-ankh-Amen vol. 1 (knowledge/sources) with EASTNORTHEAST and BERLINCLOCK written in at 22 and 64, enciphered under a random alphabet and key of that length; a plant counts as found when the climb's best scores above every copper at that length. A key from such a climb costs about 88 bits for the alphabet plus 4.7 per key letter.

## Prediction

Power: the climb finds at least 4 of 6 planted texts at length 23 (best score above every copper) and at least 3 of 6 at 26. K4: its best zero-violation score lies inside the range of the 12 coppers at both lengths, so F1.1 closes as sampled at stated power. If plants are found in fewer than half the trials at a length, that length is recorded as not decidable by this climb and the item stays open there. A K4 score above every copper stops the queue for a replication against fresh coppers.

## Method

1. Draw 12 shuffles of K4 that fit at length 23 in the Beaufort form and 12 that fit at 26 (exact test from 0119).
2. Build 6 planted texts per length from Carter's English.
3. For K4, each copper and each plant, run the same annealing climb (restarts x iterations fixed in the bounds) over the alphabet and the free key values, the known letters held by a penalty.
4. Keep the best zero-violation English score per text.
5. Compare K4 with the coppers per length; report the plants found and how many of their letters the climb got right.

## Result

Candidates returned: 2. Passed all gates: 0. Best crib hits among all candidates: 24/24
(EAST 4/4, NORTHEAST 9/9, BERLIN 6/6, CLOCK 5/5).
Best loss: 4.232233564811935 (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | baseline | 24/24 | -7.857 | `WRYZNNIPNMUPTOMEORJZEEASTNORTHEASTRBYEASILETFIPLSNGESMUCHASTDCEBERLINCLOCKHASANDWLANDWOHLUCEKSENP` | Beaufort form, one alphabet JCRBOQYZPXVWHSMGAUKNFTIELD on both sides, key length 23 |
| 2 | baseline | 24/24 | -7.481 | `QBHEFEULCLATLYEPHUVALEASTNORTHEASTPOILTYNESTUCOOTEVELHOURKMRTISBERLINCLOCKTBYINAROMTHEENEIGNORGHF` | Beaufort form, one alphabet NDPEAFCIXWRMUHGYZKOBTJVSQL on both sides, key length 26 |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "one unknown alphabet on both sides, Beaufort form, periodic key 23 or 26, no move (the only pairs 0119 left)",
 "search": "simulated annealing, 20 restarts x 200,000 moves per text, penalty 1.0 per known-letter violation, T 0.05->0.002",
 "not_exhaustive": true,
 "coppers_per_length": 12,
 "plants_per_length": 6,
 "summary": {
  "23": {
   "k4": -5.810638731843756,
   "coppers_min": -5.89937258245918,
   "coppers_max": -5.4458110913041535,
   "k4_above_all_coppers": false,
   "plants_found": 3,
   "plants_letters_right": [
    37,
    41,
    34,
    34,
    32,
    36
   ],
   "plants_scores": [
    -5.5,
    -5.503,
    -5.455,
    -5.383,
    -5.364,
    -5.295
   ],
   "plants_true_scores": [
    -4.351,
    -4.067,
    -4.379,
    -4.165,
    -4.053,
    -4.013
   ]
  },
  "26": {
   "k4": -5.288900231478601,
   "coppers_min": -5.326072645614461,
   "coppers_max": -5.008216737672375,
   "k4_above_all_coppers": false,
   "plants_found": 1,
   "plants_letters_right": [
    29,
    37,
    38,
    38,
    43,
    36
   ],
   "plants_scores": [
    -5.052,
    -5.096,
    -5.075,
    -5.227,
    -4.794,
    -5.092
   ],
   "plants_true_scores": [
    -4.271,
    -4.325,
    -4.075,
    -4.12,
    -4.089,
    -4.351
   ]
  }
 },
 "coppers_scores": {
  "23": [
   -5.729,
   -5.815,
   -5.729,
   -5.713,
   -5.446,
   -5.611,
   -5.54,
   -5.702,
   -5.899,
   -5.812,
   -5.671,
   -5.757
  ],
  "26": [
   -5.118,
   -5.008,
   -5.326,
   -5.264,
   -5.218,
   -5.029,
   -5.104,
   -5.065,
   -5.108,
   -5.161,
   -5.228,
   -5.211
  ]
 },
 "k4_best": {
  "23": {
   "score": -5.810638731843756,
   "plaintext": "WRYZNNIPNMUPTOMEORJZEEASTNORTHEASTRBYEASILETFIPLSNGESMUCHASTDCEBERLINCLOCKHASANDWLANDWOHLUCEKSENP",
   "alphabet": "JCRBOQYZPXVWHSMGAUKNFTIELD",
   "key": [
    15,
    5,
    24,
    9,
    10,
    23,
    5,
    12,
    8,
    0,
    8,
    6,
    24,
    17,
    18,
    21,
    0,
    22,
    3,
    10,
    8,
    17,
    14
   ]
  },
  "26": {
   "score": -5.288900231478601,
   "plaintext": "QBHEFEULCLATLYEPHUVALEASTNORTHEASTPOILTYNESTUCOOTEVELHOURKMRTISBERLINCLOCKTBYINAROMTHEENEIGNORGHF",
   "alphabet": "NDPEAFCIXWRMUHGYZKOBTJVSQL",
   "key": [
    16,
    12,
    4,
    13,
    17,
    21,
    20,
    17,
    20,
    12,
    16,
    19,
    18,
    12,
    21,
    1,
    20,
    17,
    15,
    23,
    8,
    8,
    3,
    7,
    16,
    24
   ]
  }
 },
 "controls": "12 shuffled coppers per length that fit exactly at that length and form (seed 120), identical climb"
}
```

Notes: L23: K4 -5.811, coppers -5.899 to -5.446, plants found 3/6 (letters right [37, 41, 34, 34, 32, 36]); L26: K4 -5.289, coppers -5.326 to -5.008, plants found 1/6 (letters right [29, 37, 38, 38, 43, 36])


