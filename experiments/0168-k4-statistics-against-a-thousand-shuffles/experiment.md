# 0168-k4-statistics-against-a-thousand-shuffles: F12.2: Stein's way, step one: K4's statistics by segment and by width (letter counts per segment, index of coincidence for 1-48 alphabets, repeats at widths 7, 21 and 31), each against 1,000 shuffles, with the number of comparisons stated

**Family:** 12-steins-way  
**Parent:** 0056-look-elsewhere-for-the-two-fingerprints  
**Decision:** reverted  
**Run:** 2026-10-16T23:00:37+00:00, 1.5 s, status ran  
**Time by phase:** unattributed 222 s, run 2 s, record 0 s

## In plain words

Before attacking a cipher, Stein measured it: how evenly each letter is spread along the text, and how the letters behave when the text is cut into a number of interleaved strands. We measure K4 the same way, seventy-one measurements in all, and compare each with a thousand random shufflings of K4's own letters. Only a measurement that no shuffling matches is reported as a real feature; with this many measurements, about one in seven of a single such accident would be expected by luck.

## Walkthrough, by hand

1. Cut K4 at the ends of its carved lines and count each letter in each piece; compare how uneven the counts are with the same for shuffled K4.
2. Write K4 in m interleaved strands (every m-th letter) for m = 1 to 48; in each strand count how often two letters drawn at random match; average.
3. Write K4 in rows of 7, 21 and 31; count letters that repeat directly below, or diagonally below, and the doublets falling in one column.
4. Shuffle K4's letters 1,000 times and repeat every count; a feature is real only if K4 is more extreme than every shuffle.

## Worked example (generated)

```
K4 in rows of 7 (doublets marked by the column they start in):

  O B K R U O X
  O G H U L B S
  O L I F B B W
  F L R V Q Q P
  R N G K S S O
  T W T Q S J Q
  S S E K Z Z W
  A T J K L U D
  I A W I N F B
  N Y P V T T M
  Z F P K W G D
  K Z X T J C D
  I G K U H U A
  U E K C A R

doublets by starting column (0-6): {0: 1, 4: 5}
index of coincidence of all 97 letters: 0.0361 (random 26 letters: 0.0385; English: 0.066)
```

## Lineage

Inherits from 0056-look-elsewhere-for-the-two-fingerprints. What changed: F12.2. Stein began K1-K3 by quantifying impressions: letter counts by carved row (his Figure 3 split the panel at row 14/15) and the index of coincidence against the number of alphabets (his Figures 7, 17, 26). 0056 measured two of K4's patterns. Here a fixed battery, set before the run: (1) whether K4's letters are spread evenly across segments (the carved lines 1-4, 5-35, 36-66, 67-97; halves at 48/49; thirds; the stretch before EAST, between the runs, after CLOCK): chi-square of the segment-by-letter table; (2) the average index of coincidence when K4 is cut into m alphabets, m 1-48; (3) at widths 7, 21 and 31: repeated vertical bigrams (0056's statistic), vertical repeats (same letter directly below), diagonal repeats (one row down, one column right and left), and the largest number of horizontal doublets in one column. Each statistic against 1,000 letter-preserving shuffles: the two-sided rank p. An observation counts as outside the shuffles only if no shuffle is as extreme (p < 0.001, two-sided 0.002), and the number of statistics is stated so the expected number of such accidents is known.

## Hypothesis (domain expert)

Stein 1999 (knowledge/sources/stein-1999-cracking-the-courtyard-crypto.txt): 'I seemed to see different patterns throughout, but I wanted to quantify these impressions'; the row-wise frequency break between rows 14 and 15; the I.C. plots. C28 (the m = 13 peak) is F12.3. 0056: the width-7 doublet column and width-21 vertical repeats against 10,000 shuffles (corrected p 0.005 and 0.010). Shuffles keep K4's letters and permute positions. Statistics: S = 8 segment tables + 48 I.C. values + 3 widths x 5 repeat statistics = 71; at p < 0.002 two-sided about 0.14 false outliers expected. Any statistic outside every shuffle becomes a new item (F12.5 if it is a segment break).

## Prediction

The two known fingerprints come out at the edge (the width-7 doublet column near p 0.002-0.005, the width-21 vertical repeats near p 0.01), but with 71 statistics nothing lies outside every shuffle; no segment break; no I.C. peak at any m. Zero candidates.

## Method

1. Compute the 71 statistics on K4.
2. 1,000 shuffles of K4's letters (seed 1612): the same statistics.
3. For each, the two-sided rank p; list those beyond every shuffle; state the multiple-comparison count.

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
 "family": "observation, not a cipher: K4's statistics against 1,000 shuffles",
 "statistics": 71,
 "shuffles": 1000,
 "expected_outliers_by_chance_at_p_0_002": 0.14,
 "outside_every_shuffle": [],
 "smallest_p": [
  {
   "statistic": "width 7: most doublets in one column",
   "k4": 5,
   "shuffles_min": 0,
   "shuffles_max": 5,
   "p_two_sided": 0.002,
   "outside_every_shuffle": false
  },
  {
   "statistic": "width 21: repeated vertical bigrams (0056's statistic)",
   "k4": 11,
   "shuffles_min": 0,
   "shuffles_max": 11,
   "p_two_sided": 0.004,
   "outside_every_shuffle": false
  },
  {
   "statistic": "width 7: vertical repeats",
   "k4": 9,
   "shuffles_min": 0,
   "shuffles_max": 11,
   "p_two_sided": 0.008,
   "outside_every_shuffle": false
  },
  {
   "statistic": "segments: quarters",
   "k4": 102.24878,
   "shuffles_min": 50.02506,
   "shuffles_max": 107.53932,
   "p_two_sided": 0.014,
   "outside_every_shuffle": false
  },
  {
   "statistic": "width 21: most doublets in one column",
   "k4": 3,
   "shuffles_min": 0,
   "shuffles_max": 4,
   "p_two_sided": 0.014,
   "outside_every_shuffle": false
  },
  {
   "statistic": "segments: before EAST, the runs and between, after CLOCK",
   "k4": 124.07492,
   "shuffles_min": 66.84583,
   "shuffles_max": 141.1318,
   "p_two_sided": 0.064,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 3 alphabets",
   "k4": 0.02967,
   "shuffles_min": 0.0237,
   "shuffles_max": 0.05232,
   "p_two_sided": 0.064,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 36 alphabets",
   "k4": 0.0,
   "shuffles_min": 0.0,
   "shuffles_max": 0.12963,
   "p_two_sided": 0.076,
   "outside_every_shuffle": false
  },
  {
   "statistic": "width 7: repeated vertical bigrams (0056's statistic)",
   "k4": 9,
   "shuffles_min": 0,
   "shuffles_max": 13,
   "p_two_sided": 0.116,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 39 alphabets",
   "k4": 0.0,
   "shuffles_min": 0.0,
   "shuffles_max": 0.13675,
   "p_two_sided": 0.124,
   "outside_every_shuffle": false
  }
 ],
 "all": [
  {
   "statistic": "segments: carved lines (1-4, 5-35, 36-66, 67-97)",
   "k4": 69.19724,
   "shuffles_min": 50.32527,
   "shuffles_max": 134.31371,
   "p_two_sided": 0.55,
   "outside_every_shuffle": false
  },
  {
   "statistic": "segments: halves at 48/49",
   "k4": 33.82662,
   "shuffles_min": 9.75739,
   "shuffles_max": 44.99447,
   "p_two_sided": 0.182,
   "outside_every_shuffle": false
  },
  {
   "statistic": "segments: thirds",
   "k4": 60.02487,
   "shuffles_min": 30.25815,
   "shuffles_max": 77.52652,
   "p_two_sided": 0.266,
   "outside_every_shuffle": false
  },
  {
   "statistic": "segments: before EAST, the runs and between, after CLOCK",
   "k4": 124.07492,
   "shuffles_min": 66.84583,
   "shuffles_max": 141.1318,
   "p_two_sided": 0.064,
   "outside_every_shuffle": false
  },
  {
   "statistic": "segments: quarters",
   "k4": 102.24878,
   "shuffles_min": 50.02506,
   "shuffles_max": 107.53932,
   "p_two_sided": 0.014,
   "outside_every_shuffle": false
  },
  {
   "statistic": "segments: before and after BERLINCLOCK's start",
   "k4": 27.9626,
   "shuffles_min": 9.25734,
   "shuffles_max": 45.49649,
   "p_two_sided": 0.636,
   "outside_every_shuffle": false
  },
  {
   "statistic": "segments: first 21, rest",
   "k4": 35.44258,
   "shuffles_min": 11.36985,
   "shuffles_max": 51.55657,
   "p_two_sided": 0.132,
   "outside_every_shuffle": false
  },
  {
   "statistic": "segments: fifths",
   "k4": 112.9348,
   "shuffles_min": 71.11632,
   "shuffles_max": 142.13053,
   "p_two_sided": 0.296,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 1 alphabets",
   "k4": 0.03608,
   "shuffles_min": 0.03608,
   "shuffles_max": 0.03608,
   "p_two_sided": 1.0,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 2 alphabets",
   "k4": 0.03522,
   "shuffles_min": 0.0299,
   "shuffles_max": 0.04908,
   "p_two_sided": 0.856,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 3 alphabets",
   "k4": 0.02967,
   "shuffles_min": 0.0237,
   "shuffles_max": 0.05232,
   "p_two_sided": 0.064,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 4 alphabets",
   "k4": 0.03286,
   "shuffles_min": 0.02402,
   "shuffles_max": 0.06105,
   "p_two_sided": 0.504,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 5 alphabets",
   "k4": 0.03918,
   "shuffles_min": 0.0193,
   "shuffles_max": 0.05766,
   "p_two_sided": 0.566,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 6 alphabets",
   "k4": 0.03007,
   "shuffles_min": 0.0174,
   "shuffles_max": 0.06013,
   "p_two_sided": 0.324,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 7 alphabets",
   "k4": 0.04186,
   "shuffles_min": 0.01753,
   "shuffles_max": 0.06096,
   "p_two_sided": 0.442,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 8 alphabets",
   "k4": 0.02622,
   "shuffles_min": 0.01807,
   "shuffles_max": 0.06993,
   "p_two_sided": 0.194,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 9 alphabets",
   "k4": 0.02559,
   "shuffles_min": 0.01504,
   "shuffles_max": 0.06375,
   "p_two_sided": 0.218,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 10 alphabets",
   "k4": 0.04333,
   "shuffles_min": 0.01389,
   "shuffles_max": 0.06778,
   "p_two_sided": 0.428,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 11 alphabets",
   "k4": 0.04401,
   "shuffles_min": 0.01335,
   "shuffles_max": 0.07612,
   "p_two_sided": 0.368,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 12 alphabets",
   "k4": 0.02315,
   "shuffles_min": 0.00893,
   "shuffles_max": 0.07242,
   "p_two_sided": 0.154,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 13 alphabets",
   "k4": 0.02289,
   "shuffles_min": 0.00916,
   "shuffles_max": 0.08059,
   "p_two_sided": 0.212,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 14 alphabets",
   "k4": 0.03537,
   "shuffles_min": 0.0068,
   "shuffles_max": 0.07483,
   "p_two_sided": 1.0,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 15 alphabets",
   "k4": 0.03683,
   "shuffles_min": 0.00889,
   "shuffles_max": 0.0946,
   "p_two_sided": 0.95,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 16 alphabets",
   "k4": 0.0375,
   "shuffles_min": 0.00417,
   "shuffles_max": 0.08393,
   "p_two_sided": 0.878,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 17 alphabets",
   "k4": 0.03725,
   "shuffles_min": 0.0,
   "shuffles_max": 0.08824,
   "p_two_sided": 0.93,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 18 alphabets",
   "k4": 0.01852,
   "shuffles_min": 0.00741,
   "shuffles_max": 0.08333,
   "p_two_sided": 0.166,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 19 alphabets",
   "k4": 0.02807,
   "shuffles_min": 0.00351,
   "shuffles_max": 0.08246,
   "p_two_sided": 0.654,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 20 alphabets",
   "k4": 0.03,
   "shuffles_min": 0.005,
   "shuffles_max": 0.105,
   "p_two_sided": 0.774,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 21 alphabets",
   "k4": 0.03651,
   "shuffles_min": 0.00476,
   "shuffles_max": 0.1127,
   "p_two_sided": 0.98,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 22 alphabets",
   "k4": 0.03485,
   "shuffles_min": 0.0,
   "shuffles_max": 0.1,
   "p_two_sided": 0.968,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 23 alphabets",
   "k4": 0.01594,
   "shuffles_min": 0.0,
   "shuffles_max": 0.1058,
   "p_two_sided": 0.214,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 24 alphabets",
   "k4": 0.02083,
   "shuffles_min": 0.0,
   "shuffles_max": 0.09028,
   "p_two_sided": 0.42,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 25 alphabets",
   "k4": 0.05333,
   "shuffles_min": 0.0,
   "shuffles_max": 0.1,
   "p_two_sided": 0.358,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 26 alphabets",
   "k4": 0.01923,
   "shuffles_min": 0.0,
   "shuffles_max": 0.11538,
   "p_two_sided": 0.452,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 27 alphabets",
   "k4": 0.03704,
   "shuffles_min": 0.0,
   "shuffles_max": 0.09259,
   "p_two_sided": 1.0,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 28 alphabets",
   "k4": 0.04762,
   "shuffles_min": 0.0,
   "shuffles_max": 0.10119,
   "p_two_sided": 0.598,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 29 alphabets",
   "k4": 0.02874,
   "shuffles_min": 0.0,
   "shuffles_max": 0.11494,
   "p_two_sided": 0.846,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 30 alphabets",
   "k4": 0.04444,
   "shuffles_min": 0.0,
   "shuffles_max": 0.11111,
   "p_two_sided": 0.704,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 31 alphabets",
   "k4": 0.05376,
   "shuffles_min": 0.0,
   "shuffles_max": 0.10215,
   "p_two_sided": 0.402,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 32 alphabets",
   "k4": 0.03125,
   "shuffles_min": 0.0,
   "shuffles_max": 0.10417,
   "p_two_sided": 1.0,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 33 alphabets",
   "k4": 0.0303,
   "shuffles_min": 0.0,
   "shuffles_max": 0.12121,
   "p_two_sided": 1.0,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 34 alphabets",
   "k4": 0.06863,
   "shuffles_min": 0.0,
   "shuffles_max": 0.11765,
   "p_two_sided": 0.2,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 35 alphabets",
   "k4": 0.00952,
   "shuffles_min": 0.0,
   "shuffles_max": 0.14286,
   "p_two_sided": 0.288,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 36 alphabets",
   "k4": 0.0,
   "shuffles_min": 0.0,
   "shuffles_max": 0.12963,
   "p_two_sided": 0.076,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 37 alphabets",
   "k4": 0.00901,
   "shuffles_min": 0.0,
   "shuffles_max": 0.12613,
   "p_two_sided": 0.308,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 38 alphabets",
   "k4": 0.07895,
   "shuffles_min": 0.0,
   "shuffles_max": 0.15789,
   "p_two_sided": 0.138,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 39 alphabets",
   "k4": 0.0,
   "shuffles_min": 0.0,
   "shuffles_max": 0.13675,
   "p_two_sided": 0.124,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 40 alphabets",
   "k4": 0.03333,
   "shuffles_min": 0.0,
   "shuffles_max": 0.16667,
   "p_two_sided": 1.0,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 41 alphabets",
   "k4": 0.04878,
   "shuffles_min": 0.0,
   "shuffles_max": 0.14634,
   "p_two_sided": 0.594,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 42 alphabets",
   "k4": 0.06349,
   "shuffles_min": 0.0,
   "shuffles_max": 0.12698,
   "p_two_sided": 0.368,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 43 alphabets",
   "k4": 0.07752,
   "shuffles_min": 0.0,
   "shuffles_max": 0.13953,
   "p_two_sided": 0.176,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 44 alphabets",
   "k4": 0.06818,
   "shuffles_min": 0.0,
   "shuffles_max": 0.15909,
   "p_two_sided": 0.3,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 45 alphabets",
   "k4": 0.06667,
   "shuffles_min": 0.0,
   "shuffles_max": 0.15556,
   "p_two_sided": 0.324,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 46 alphabets",
   "k4": 0.02899,
   "shuffles_min": 0.0,
   "shuffles_max": 0.13768,
   "p_two_sided": 1.0,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 47 alphabets",
   "k4": 0.0,
   "shuffles_min": 0.0,
   "shuffles_max": 0.15603,
   "p_two_sided": 0.28,
   "outside_every_shuffle": false
  },
  {
   "statistic": "I.C. at 48 alphabets",
   "k4": 0.04167,
   "shuffles_min": 0.0,
   "shuffles_max": 0.13194,
   "p_two_sided": 1.0,
   "outside_every_shuffle": false
  },
  {
   "statistic": "width 7: repeated vertical bigrams (0056's statistic)",
   "k4": 9,
   "shuffles_min": 0,
   "shuffles_max": 13,
   "p_two_sided": 0.116,
   "outside_every_shuffle": false
  },
  {
   "statistic": "width 7: vertical repeats",
   "k4": 9,
   "shuffles_min": 0,
   "shuffles_max": 11,
   "p_two_sided": 0.008,
   "outside_every_shuffle": false
  },
  {
   "statistic": "width 7: diagonal repeats right",
   "k4": 2,
   "shuffles_min": 0,
   "shuffles_max": 9,
   "p_two_sided": 0.916,
   "outside_every_shuffle": false
  },
  {
   "statistic": "width 7: diagonal repeats left",
   "k4": 3,
   "shuffles_min": 0,
   "shuffles_max": 10,
   "p_two_sided": 1.0,
   "outside_every_shuffle": false
  },
  {
   "statistic": "width 7: most doublets in one column",
   "k4": 5,
   "shuffles_min": 0,
   "shuffles_max": 5,
   "p_two_sided": 0.002,
   "outside_every_shuffle": false
  },
  {
   "statistic": "width 21: repeated vertical bigrams (0056's statistic)",
   "k4": 11,
   "shuffles_min": 0,
   "shuffles_max": 11,
   "p_two_sided": 0.004,
   "outside_every_shuffle": false
  },
  {
   "statistic": "width 21: vertical repeats",
   "k4": 3,
   "shuffles_min": 0,
   "shuffles_max": 9,
   "p_two_sided": 1.0,
   "outside_every_shuffle": false
  },
  {
   "statistic": "width 21: diagonal repeats right",
   "k4": 2,
   "shuffles_min": 0,
   "shuffles_max": 10,
   "p_two_sided": 1.0,
   "outside_every_shuffle": false
  },
  {
   "statistic": "width 21: diagonal repeats left",
   "k4": 4,
   "shuffles_min": 0,
   "shuffles_max": 8,
   "p_two_sided": 0.546,
   "outside_every_shuffle": false
  },
  {
   "statistic": "width 21: most doublets in one column",
   "k4": 3,
   "shuffles_min": 0,
   "shuffles_max": 4,
   "p_two_sided": 0.014,
   "outside_every_shuffle": false
  },
  {
   "statistic": "width 31: repeated vertical bigrams (0056's statistic)",
   "k4": 3,
   "shuffles_min": 0,
   "shuffles_max": 11,
   "p_two_sided": 1.0,
   "outside_every_shuffle": false
  },
  {
   "statistic": "width 31: vertical repeats",
   "k4": 4,
   "shuffles_min": 0,
   "shuffles_max": 8,
   "p_two_sided": 0.436,
   "outside_every_shuffle": false
  },
  {
   "statistic": "width 31: diagonal repeats right",
   "k4": 3,
   "shuffles_min": 0,
   "shuffles_max": 7,
   "p_two_sided": 0.758,
   "outside_every_shuffle": false
  },
  {
   "statistic": "width 31: diagonal repeats left",
   "k4": 4,
   "shuffles_min": 0,
   "shuffles_max": 8,
   "p_two_sided": 0.376,
   "outside_every_shuffle": false
  },
  {
   "statistic": "width 31: most doublets in one column",
   "k4": 1,
   "shuffles_min": 0,
   "shuffles_max": 3,
   "p_two_sided": 1.0,
   "outside_every_shuffle": false
  }
 ],
 "controls": "1000 letter-preserving shuffles of K4 (seed 1612)"
}
```

Notes: 71 statistics x 1000 shuffles: outside every shuffle 0 ([]); smallest p width 7: most doublets in one column 0.002, width 21: repeated vertical bigrams (0056's statistic) 0.004, width 7: vertical repeats 0.008, segments: quarters 0.014


