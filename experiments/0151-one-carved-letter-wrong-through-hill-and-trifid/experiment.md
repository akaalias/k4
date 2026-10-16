# 0151-one-carved-letter-wrong-through-hill-and-trifid: F1.6, third part: every single-letter error in the copper (wrong, missing or extra, anywhere) through the exact Hill (sizes 2-5, plain and affine) and trifid (free cube) verdicts

**Family:** 1-keyed-periodic  
**Parent:** 0147-one-carved-letter-wrong-through-the-free-alphabet-tests  
**Decision:** reverted  
**Run:** 2026-10-16T21:15:30+00:00, 50.0 s, status ran  
**Time by phase:** unattributed 14 s, run 50 s, record 0 s

## In plain words

The Hill cipher (suggested by the HILL letters on the sculpture's table) and trifid (a three-dimensional letter cube) were ruled out exactly. Both work on groups of neighbouring letters, so a single wrong, missing or extra carved letter anywhere could spoil the test. We try every such error and rerun both exact tests.

## Walkthrough, by hand

1. Change one carved letter, say the W at place 21, to A.
2. Hill 2x2: the block holding places 21-22 now has carved letters A, F; the known E at 22 gives one equation in the matrix row.
3. Solve each matrix row from all its equations modulo 2 and 13; no solution means the setting is dead.
4. Trifid: rebuild the coordinate equalities with the new letter and search for a cube.
5. Repeat for every place, every replacement, every deletion and insertion.

## Worked example (generated)

```
the errors tried, for every place of the copper:

  wrong:   place 21 W -> each of the other 25 letters
  missing: place 21 deleted, the rest moves left, a filler at the end
  extra:   each letter inserted before place 21, the last letter pushed out

each variant through Hill 2x2-5x5 (plain, affine, every alignment, four numberings) and trifid (periods 2-15, every offset)
```

## Lineage

Inherits from 0147-one-carved-letter-wrong-through-the-free-alphabet-tests. What changed: F1.6, Hill and trifid verdicts. 0105 solved Hill letter by letter (sizes 2-5, plain and affine, every alignment, four numberings) and 0040 solved trifid with any 27-symbol cube (periods 2-15, every offset) exactly: no fit on K4. These ciphers read the carved letters around each known letter too, so every single-letter error anywhere matters: each of the 97 carved letters changed to each other letter (2,425), each deleted (97), and a letter inserted before each place, every letter tried (2,522); the known places keep their numbering. K4's 5,044 variants first; scrambled copies only if a variant fits.

## Hypothesis (domain expert)

Family G, C17, C21 (the HILL column: Hill under a slip), trifid as Sanborn's 'visual' cube (C3). Deciders unchanged: 0105's setting() (rows solved mod 2 and 13, CRT, invertibility; 'open' when too few equations), 0040's solve_setting() (union-find on coordinate variables, backtracking with the all-different rule, caps). Exact where decided; open settings counted. An error is modelled on the copper with the message numbering fixed (a deleted letter's place filled at the end; an inserted letter pushes the last one out).

## Prediction

No variant fits Hill or trifid with at least one check; open settings at the rate 0105 found (5x5 affine). Zero candidates.

## Method

1. Build the 5,044 variants.
2. For each: 0105's Hill settings (4 sizes x plain/affine x alignments x 4 numberings) and 0040's trifid settings (periods 2-15 x offsets).
3. List any variant with a living Hill setting that has checks, or a consistent cube.

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
 "family": "Hill 2-5 (plain, affine) and trifid (free cube) on every single-letter error of the copper",
 "variants": 5044,
 "variants_done": 5044,
 "hill_settings_per_variant": "4 sizes x plain/affine x alignments x 4 numberings (112)",
 "trifid_settings_per_variant": "periods 2-15 x every offset (119)",
 "hill_alive_with_checks": [
  {
   "variant": "sub 21 W->M",
   "n": 5,
   "affine": false,
   "align": 0,
   "numbering": 1,
   "checks": 1
  },
  {
   "variant": "sub 34 S->H",
   "n": 5,
   "affine": false,
   "align": 4,
   "numbering": 0,
   "checks": 1
  },
  {
   "variant": "sub 36 T->W",
   "n": 5,
   "affine": false,
   "align": 1,
   "numbering": 1,
   "checks": 1
  },
  {
   "variant": "ins W before 73",
   "n": 5,
   "affine": false,
   "align": 0,
   "numbering": 1,
   "checks": 1
  },
  {
   "variant": "sub 24 R->C",
   "n": 5,
   "affine": false,
   "align": 4,
   "numbering": 1,
   "checks": 1
  },
  {
   "variant": "sub 29 R->F",
   "n": 5,
   "affine": false,
   "align": 1,
   "numbering": 0,
   "checks": 1
  },
  {
   "variant": "sub 72 F->T",
   "n": 5,
   "affine": false,
   "align": 4,
   "numbering": 0,
   "checks": 1
  },
  {
   "variant": "sub 26 Q->S",
   "n": 5,
   "affine": false,
   "align": 1,
   "numbering": 1,
   "checks": 1
  },
  {
   "variant": "sub 70 M->F",
   "n": 5,
   "affine": false,
   "align": 4,
   "numbering": 1,
   "checks": 1
  },
  {
   "variant": "sub 75 W->I",
   "n": 5,
   "affine": false,
   "align": 1,
   "numbering": 1,
   "checks": 1
  },
  {
   "variant": "del 74",
   "n": 5,
   "affine": false,
   "align": 1,
   "numbering": 0,
   "checks": 1
  },
  {
   "variant": "ins E before 27",
   "n": 5,
   "affine": false,
   "align": 0,
   "numbering": 2,
   "checks": 1
  },
  {
   "variant": "ins C before 64",
   "n": 5,
   "affine": false,
   "align": 3,
   "numbering": 2,
   "checks": 1
  },
  {
   "variant": "sub 26 Q->T",
   "n": 5,
   "affine": false,
   "align": 4,
   "numbering": 0,
   "checks": 1
  },
  {
   "variant": "sub 31 G->W",
   "n": 5,
   "affine": false,
   "align": 1,
   "numbering": 1,
   "checks": 1
  },
  {
   "variant": "sub 62 F->P",
   "n": 5,
   "affine": false,
   "align": 4,
   "numbering": 0,
   "checks": 1
  },
  {
   "variant": "sub 65 Y->D",
   "n": 5,
   "affine": false,
   "align": 1,
   "numbering": 0,
   "checks": 1
  },
  {
   "variant": "sub 67 V->R",
   "n": 5,
   "affine": false,
   "align": 4,
   "numbering": 2,
   "checks": 1
  },
  {
   "variant": "sub 72 F->V",
   "n": 5,
   "affine": false,
   "align": 1,
   "numbering": 0,
   "checks": 1
  },
  {
   "variant": "ins P before 66",
   "n": 5,
   "affine": false,
   "align": 3,
   "numbering": 0,
   "checks": 1
  },
  {
   "variant": "sub 29 R->I",
   "n": 5,
   "affine": false,
   "align": 0,
   "numbering": 1,
   "checks": 1
  },
  {
   "variant": "sub 70 M->H",
   "n": 5,
   "affine": false,
   "align": 4,
   "numbering": 0,
   "checks": 1
  },
  {
   "variant": "sub 75 W->K",
   "n": 5,
   "affine": false,
   "align": 0,
   "numbering": 1,
   "checks": 1
  },
  {
   "variant": "ins C before 69",
   "n": 5,
   "affine": false,
   "align": 4,
   "numbering": 1,
   "checks": 1
  },
  {
   "variant": "ins A before 74",
   "n": 5,
   "affine": false,
   "align": 1,
   "numbering": 0,
   "checks": 1
  },
  {
   "variant": "ins M before 76",
   "n": 5,
   "affine": false,
   "align": 1,
   "numbering": 1,
   "checks": 1
  },
  {
   "variant": "sub 29 R->J",
   "n": 5,
   "affine": false,
   "align": 1,
   "numbering": 1,
   "checks": 1
  },
  {
   "variant": "sub 29 R->J",
   "n": 5,
   "affine": false,
   "align": 4,
   "numbering": 0,
   "checks": 1
  },
  {
   "variant": "sub 21 W->S",
   "n": 5,
   "affine": false,
   "align": 4,
   "numbering": 0,
   "checks": 1
  },
  {
   "variant": "sub 24 R->H",
   "n": 5,
   "affine": false,
   "align": 0,
   "numbering": 1,
   "checks": 1
  },
  {
   "variant": "sub 34 S->N",
   "n": 5,
   "affine": false,
   "align": 4,
   "numbering": 1,
   "checks": 1
  },
  {
   "variant": "sub 26 Q->X",
   "n": 5,
   "affine": false,
   "align": 4,
   "numbering": 1,
   "checks": 1
  },
  {
   "variant": "sub 34 S->O",
   "n": 5,
   "affine": false,
   "align": 1,
   "numbering": 0,
   "checks": 1
  },
  {
   "variant": "sub 62 F->T",
   "n": 5,
   "affine": false,
   "align": 1,
   "numbering": 0,
   "checks": 1
  },
  {
   "variant": "sub 62 F->T",
   "n": 5,
   "affine": false,
   "align": 1,
   "numbering": 1,
   "checks": 1
  },
  {
   "variant": "sub 70 M->K",
   "n": 5,
   "affine": false,
   "align": 1,
   "numbering": 0,
   "checks": 1
  },
  {
   "variant": "sub 75 W->N",
   "n": 5,
   "affine": false,
   "align": 1,
   "numbering": 0,
   "checks": 1
  },
  {
   "variant": "ins T before 66",
   "n": 5,
   "affine": false,
   "align": 3,
   "numbering": 1,
   "checks": 1
  },
  {
   "variant": "sub 29 R->M",
   "n": 5,
   "affine": false,
   "align": 4,
   "numbering": 1,
   "checks": 1
  },
  {
   "variant": "ins M before 22",
   "n": 5,
   "affine": false,
   "align": 1,
   "numbering": 1,
   "checks": 1
  },
  {
   "variant": "ins G before 69",
   "n": 5,
   "affine": false,
   "align": 1,
   "numbering": 0,
   "checks": 1
  },
  {
   "variant": "ins E before 74",
   "n": 5,
   "affine": false,
   "align": 1,
   "numbering": 1,
   "checks": 1
  },
  {
   "variant": "ins E before 74",
   "n": 5,
   "affine": false,
   "align": 4,
   "numbering": 0,
   "checks": 1
  },
  {
   "variant": "sub 32 K->C",
   "n": 5,
   "affine": false,
   "align": 0,
   "numbering": 1,
   "checks": 1
  },
  {
   "variant": "sub 73 P->B",
   "n": 5,
   "affine": false,
   "align": 0,
   "numbering": 1,
   "checks": 1
  },
  {
   "variant": "sub 24 R->L",
   "n": 5,
   "affine": false,
   "align": 1,
   "numbering": 0,
   "checks": 1
  },
  {
   "variant": "sub 27 Q->A",
   "n": 5,
   "affine": false,
   "align": 4,
   "numbering": 0,
   "checks": 1
  },
  {
   "variant": "sub 32 K->D",
   "n": 5,
   "affine": false,
   "align": 1,
   "numbering": 1,
   "checks": 1
  },
  {
   "variant": "sub 34 S->R",
   "n": 5,
   "affine": false,
   "align": 1,
   "numbering": 1,
   "checks": 1
  },
  {
   "variant": "ins S before 76",
   "n": 5,
   "affine": false,
   "align": 1,
   "numbering": 0,
   "checks": 1
  }
 ],
 "n_hill_alive_with_checks": 257,
 "hill_open_settings": 70218,
 "trifid_consistent": [],
 "n_trifid_consistent": 0,
 "seconds": 50,
 "exhaustive": "exact where decided; Hill open settings counted",
 "controls": "none needed if nothing fits (exact)"
}
```

Notes: 5044 variants: Hill alive with checks 257, Hill open settings 70218; trifid consistent 0


