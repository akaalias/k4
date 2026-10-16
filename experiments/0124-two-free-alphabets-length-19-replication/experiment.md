# 0124-two-free-alphabets-length-19-replication: Replication: two unknown alphabets fit K4 at key length 19, where 3 of 100 scrambled coppers fit; against 1,000 fresh coppers, corrected for looking at every length, and against copies that keep the known places' letters

**Family:** 1-keyed-periodic  
**Parent:** 0123-two-free-alphabets-exact-at-every-key-length  
**Decision:** reverted  
**Run:** 2026-10-16T08:30:34+00:00, 553.2 s, status ran  
**Time by phase:** design 0 s, test 7 s, run 553 s, record 0 s

## In plain words

In the last run, two unknown alphabets with a 19-letter key could produce the 24 known letters, which happened for only 3 of 100 scrambled copies. One reason may be a coincidence in the carved text: two known R's, 38 places apart, both sit under a carved P. Here we try 1,000 new scrambled copies and ask how often any key length looks as rare as 19 did, since we looked at 26 lengths and something rare turns up by chance.

## Walkthrough, by hand

1. Write K4 in rows of 19; places 38 apart fall in the same column.
2. Pair the known places that share a column: 26 with 64, 27 with 65, and so on up to 34 with 72.
3. Places 28 and 66 are both R under carved P: whatever the alphabets, that pair agrees by itself.
4. The other eight pairs must each satisfy carved-place minus known-place equal in both, and some pair of alphabets does.
5. Scramble the carved letters, repeat, and count how often a scramble fits at 19, or at any length as rarely.

## Worked example (generated)

```
key length 8: known letters by slot (place mod 8)
  slot 0: T->V (25), S->S (33), E->Y (65), C->P (73)
  slot 1: N->Q (26), T->S (34), R->P (66), K->K (74)
  slot 2: O->Q (27), L->V (67)
  slot 3: R->P (28), I->T (68)
  slot 4: T->R (29), N->T (69)
  slot 5: E->F (22), H->N (30), C->M (70)
  slot 6: A->L (23), E->G (31), L->Z (71)
  slot 7: S->R (24), A->K (32), B->N (64), O->F (72)
  plain alphabet places: T=0 R=1 I=3 E=7 L=8 O=9 S=10 C=11 N=17 H=21 A=22 B=23 K=24
  cipher alphabet places: L=0 T=1 F=9 R=10 G=11 Z=12 M=13 V=14 Q=15 Y=21 K=22 N=23 S=24 P=25
  key: [14, 24, 6, 24, 10, 2, 4, 0]

key length 9: known letters by slot (place mod 9)
  slot 0: R->P (28), B->N (64), C->P (73)
  slot 1: T->R (29), E->Y (65), K->K (74)
  slot 2: H->N (30), R->P (66)
  slot 3: E->F (22), E->G (31), L->V (67)
  slot 4: A->L (23), A->K (32), I->T (68)
  slot 5: S->R (24), S->S (33), N->T (69)
  slot 6: T->V (25), T->S (34), C->M (70)
  slot 7: N->Q (26), L->Z (71)
  slot 8: O->Q (27), O->F (72)
  dead: no pair of alphabets fits

```

## Lineage

Inherits from 0123-two-free-alphabets-exact-at-every-key-length. What changed: F1.2, replication (order-of-work rule 5). 0123 found K4 consistent with Quagmire IV at key length 19 while only 3% of 100 coppers were. Here: (a) 1,000 fresh shuffles (seed 124), all lengths 1-26, give the share fitting at 19 and a look-elsewhere p: the share of shuffles whose rarest fitting length is as rare as K4's; (b) 1,000 copies that keep the 24 carved letters at the known places and shuffle only the other 73 (null B), which isolates whether the fit comes from the known places themselves.

## Hypothesis (domain expert)

Follow-up of 0123 (C27(c), C1(b)). Mechanism to test: at length 19 the known places pair up 38 apart (26-34 with 64-72), nine checks; places 28 and 66 are both R under P, so one check holds for free, and the other eight leave two free alphabets room to fit. Under null A (letters shuffled) that coincidence is rare. Under null B the carved letters at the 24 known places are those of K4, so the exact test, which reads only those letters, returns K4's verdict on every copy: null B is a check that the test depends only on the known places, and the honest null is A. Prediction is about A with the look-elsewhere correction. Same exact decider as 0123 (two independent alphabets, CRT mod 13 and mod 2, witness re-checked).

## Prediction

At length 19 about 2-5% of the 1,000 fresh coppers fit (K4's p near 0.03), but corrected for looking at every length the p is above 0.2: a copper usually fits at some length that few coppers fit at. So the length-19 fit is not a signal and F1.2 continues. If the corrected p is below 0.01, stop and report.

## Method

1. Draw 1,000 shuffles of K4 (seed 124).
2. For each, decide Quagmire IV consistency at lengths 1-26 exactly.
3. Share fitting per length; K4's p at 19.
4. For K4 and each shuffle, the rarest fitting length's share (shares estimated from the other shuffles); corrected p = share of shuffles at least as rare as K4.
5. Null B: 200 copies keeping the known places' carved letters, to confirm the verdict depends only on those.

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
 "family": "two unknown alphabets (Quagmire IV), periodic key 1-26, no move: replication of the length-19 fit",
 "fresh_coppers": 1000,
 "seed": 124,
 "undecided": 2,
 "k4_fits": [
  8,
  13,
  16,
  19,
  20,
  23,
  24,
  26
 ],
 "copper_share_fitting_by_length": [
  0.0,
  0.0,
  0.0,
  0.0,
  0.0,
  0.157,
  0.254,
  0.27,
  0.0,
  0.485,
  0.543,
  0.523,
  0.659,
  0.62,
  0.028,
  0.728,
  0.028,
  0.784,
  0.026,
  0.672,
  0.62,
  0.724,
  0.761,
  0.825,
  0.891,
  0.956
 ],
 "k4_p_at_19": 0.026,
 "k4_rarest_fitting_share": 0.026,
 "look_elsewhere_p": 0.026,
 "null_b_copies": 200,
 "null_b_same_verdict_as_k4_at_every_length": 200,
 "controls": "1000 fresh shuffled coppers (seed 124); null B 200 copies keeping the known places' letters"
}
```

Notes: Length 19: 26 of 1000 fresh coppers fit (p 0.026). K4's rarest fitting length share 0.026; look-elsewhere p 0.026. Null B: 200/200 copies give K4's verdict at every length.


