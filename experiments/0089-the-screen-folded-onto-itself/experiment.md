# 0089-the-screen-folded-onto-itself: The key letter behind each K4 letter: K4's carved lines laid over the tableau plate, straight or folded

**Family:** 4-visual-systems  
**Parent:** 0017-running-key-from-the-sculpture-itself  
**Decision:** reverted  
**Run:** 2026-10-15T18:45:03+00:00, 0.5 s, status ran  
**Time by phase:** implement 64 s, test 12 s, run 0 s, record 0 s

## In plain words

On the sculpture the secret text and the big table of alphabets stand side by side on one copper screen, and the letters are cut right through it. If you fold the screen in your mind, or look at it from behind, every letter of the fourth message lands on a letter of the table. That letter could be its key. We lay K4's four carved lines over every four lines of the table and of the other secret texts, straight across and folded, slide them a few columns either way, and check whether any lining-up gives all 24 known letters.

## Walkthrough, by hand

1. K4's O, B, K, R are columns 28-31 of line 11 of the lower-left plate; places 5-35 are line 12, 36-66 line 13, 67-97 line 14.
2. The lower-right plate holds tableau rows N to Z and the footer; its line 12 is row Y.
3. Place 22 is E on line 12, column 18. Straight across, row Y (label first) has key letter Y's 18th cell.
4. Folded at the centre, column 18 lands on column 32 - 18 = 14 of row Y.
5. With the sculpture's alphabet and Vigenere, E plus the key letter must give the carved F; count a hit if it does.
6. Repeat for all 24 known places, every window of four lines on every plate, both ways, shifts -4 to 4 and 12 conventions.

## Worked example (generated)

```
K4 over the lower-right tableau plate (rows N-Z, footer), natural lines, no shift
sculpture's alphabet, Vigenere: carved = known + key

place  known  carved  line  col  straight key  ->  folded key  ->
   22      E       F    12   18             H  Z           D  U
   23      A       L    12   19             I  V           C  J
   24      S       R    12   20             J  V           B  H
   25      T       V    12   21             L  U           A  E
   64      B       N    13   29             K  B           K  B
   65      E       Y    13   30             R  F           Z  D
   74      K       K    14    8             G  G           W  W
```

## Lineage

Inherits from 0017-running-key-from-the-sculpture-itself. What changed: 0017 slid the sculpture's texts along K4 as one long string. Here the key comes from the screen's geometry: each K4 letter sits at a carved line and column, and its key letter is the letter at the same line and column of another plate, or at the mirrored column when the screen is folded at its centre (the tableau reads correctly only from the back). Plate lines have different lengths, so these keys are not windows of 0017's strings.

## Hypothesis (domain expert)

Type 3 of directions.md: a key read off the sculpture by position. 01-facts.md: the screen's left half carries the ciphertext and the right half the tableau, each on two plates of 14 lines; the letters are cut through and the CIA says the tableau 'is intentionally flipped so it can only be read from the back'. K4 fills the last four cells of line 11 of the lower-left plate and lines 12-14. C6(a) ('the keys were concealed at the sculpture'), C9(b) (the tableau letters are the key), C11a, Sanborn's 'visual systems' (family 4). Key letter for K4 at plate line i, column c: the letter of a source plate at line i + d, column c + s (straight) or column 32 - c + s (folded), sources the two tableau plates (header, 26 rows with labels and the extra L, footer) and the two cipher plates, d over every window of four lines, s = -4..4, Vigenere, Beaufort and variant Beaufort with key and text numbered on the standard or KRYPTOS alphabet (12 conventions). Exact: a running key leaves no free letter, so the reading must hit all 24 known letters. Ten shuffled coppers set the chance level of the best hit count.

## Prediction

No overlay hits all 24 known letters; the best hit count on K4 lies inside the range of the ten shuffled coppers (about 6-7 of 24). Zero candidates.

## Method

1. Lay out the four plates as carved (01-facts.md and the tableau rows with the extra L in row N).
2. Give each K4 letter its plate line and column.
3. For each source plate, line offset, straight or folded, column shift and convention, read the key letter under each known place and count the places where it turns the known letter into the carved letter.
4. Do the same on ten shuffled coppers.
5. Decrypt and return any overlay that hits all 24.

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
 "family": "running key read by position off the carved screen",
 "sources": "tableau plates (header, 26 labelled rows, extra L in row N, footer) and cipher plates, 28 lines each",
 "line_windows": 25,
 "straight_or_folded": 2,
 "column_shifts": [
  -4,
  4
 ],
 "conventions": 12,
 "trials": 10800,
 "k4_best_hits": 5,
 "controls_best_hits": [
  5,
  6,
  6,
  6,
  7,
  6,
  5,
  5,
  5,
  5
 ],
 "k4_hit_histogram": {
  "0": 4872,
  "1": 3828,
  "2": 1595,
  "3": 387,
  "4": 98,
  "5": 20
 },
 "natural_alignment_hits": {
  "tableau straight": 2,
  "tableau folded": 2,
  "cipher straight": 2,
  "cipher folded": 3
 },
 "k4_top": [
  {
   "source": "tableau",
   "start_line": 6,
   "folded": false,
   "shift": 4,
   "convention": "vig/kry/std",
   "hits": 5
  },
  {
   "source": "tableau",
   "start_line": 7,
   "folded": false,
   "shift": 3,
   "convention": "vig/kry/std",
   "hits": 5
  },
  {
   "source": "tableau",
   "start_line": 8,
   "folded": false,
   "shift": 2,
   "convention": "vig/kry/std",
   "hits": 5
  },
  {
   "source": "tableau",
   "start_line": 9,
   "folded": false,
   "shift": 1,
   "convention": "vig/kry/std",
   "hits": 5
  },
  {
   "source": "tableau",
   "start_line": 12,
   "folded": false,
   "shift": 2,
   "convention": "varb/kry/kry",
   "hits": 5
  },
  {
   "source": "tableau",
   "start_line": 13,
   "folded": false,
   "shift": 1,
   "convention": "varb/kry/kry",
   "hits": 5
  },
  {
   "source": "tableau",
   "start_line": 14,
   "folded": false,
   "shift": 0,
   "convention": "varb/kry/kry",
   "hits": 5
  },
  {
   "source": "tableau",
   "start_line": 15,
   "folded": false,
   "shift": -1,
   "convention": "varb/kry/kry",
   "hits": 5
  },
  {
   "source": "tableau",
   "start_line": 16,
   "folded": false,
   "shift": -2,
   "convention": "varb/kry/kry",
   "hits": 5
  },
  {
   "source": "tableau",
   "start_line": 25,
   "folded": false,
   "shift": 4,
   "convention": "vig/kry/std",
   "hits": 5
  },
  {
   "source": "cipher",
   "start_line": 1,
   "folded": false,
   "shift": 0,
   "convention": "beau/std/std",
   "hits": 5
  },
  {
   "source": "cipher",
   "start_line": 8,
   "folded": true,
   "shift": 1,
   "convention": "beau/std/std",
   "hits": 5
  },
  {
   "source": "cipher",
   "start_line": 9,
   "folded": false,
   "shift": 0,
   "convention": "vig/kry/std",
   "hits": 5
  },
  {
   "source": "cipher",
   "start_line": 10,
   "folded": true,
   "shift": -3,
   "convention": "beau/kry/std",
   "hits": 5
  },
  {
   "source": "cipher",
   "start_line": 11,
   "folded": true,
   "shift": 1,
   "convention": "vig/kry/std",
   "hits": 5
  }
 ],
 "full_24": 0,
 "controls": "10 shuffled coppers (seed 89), identical search"
}
```

Notes: 10,800 overlays. K4 best 5/24; controls best 5-7. Overlays hitting all 24: 0. Natural alignment (lower plates, no shift), best hits: {'tableau straight': 2, 'tableau folded': 2, 'cipher straight': 2, 'cipher folded': 3}.


