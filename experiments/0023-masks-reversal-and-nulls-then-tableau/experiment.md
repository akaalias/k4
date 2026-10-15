# 0023-masks-reversal-and-nulls-then-tableau: Masks that move the known letters: the message written backwards, or padded with nulls, before a periodic tableau

**Family:** 2-masked-plaintext  
**Parent:** none (root)  
**Decision:** reverted  
**Run:** 2026-10-15T06:39:50+00:00, 17.6 s, status ran  
**Time by phase:** design 12 s, implement 64 s, test 23 s, run 18 s, record 0 s

## In plain words

The cipher's designer said he first disguised the English before enciphering it. Two simple disguises change where the known letters sit without changing them: writing the message backwards, or slipping a meaningless letter in after every few real ones. We try each disguise, work out where EASTNORTHEAST and BERLINCLOCK would then sit, and ask again whether a short repeating secret word could have produced the carved letters at those spots.

## Walkthrough, by hand

1. Write the message backwards: the E of EAST at position 22 is now at position 76, and the K of CLOCK at 74 is now at 24.
2. Under the sculpture's alphabet with Vigenere, the carved letter at 76 and plaintext E force one key letter; the carved letter at 24 and plaintext K force another.
3. The reversed EASTNORTHEAST occupies 64 to 76 and the reversed BERLINCLOCK 24 to 34.
4. Positions whose distance is a multiple of the period share a key letter; if their forced letters differ, that period is dead.
5. Now try padding instead: a null after every third letter pushes position 22 to 29 and position 64 to 85.
6. Repeat the forcing and the period test for each padding pattern.

## Worked example (generated)

```
mask: the message written backwards; convention kry/kry/kry Vigenere

plain pos  letter  sits at  carved there  forced key letter
       22    E        76        G            Y
       23    A        75        W            J
       24    S        74        K            Q
       64    B        34        S            X
       65    E        33        S            U
       74    K        24        R            R

mask: a null before every 3rd letter: position 22 sits at 30, position 64 at 86
```

## Lineage

Inherits from nothing; this is a root experiment. What changed: New root in family 2. The mask is a known rearrangement or padding of the plaintext applied before a periodic tableau: reversal, a null before every k-th letter, or a run of nulls at the start. The cribs then sit at computable intermediate positions.

## Hypothesis (domain expert)

Scheidt: 'I masked the English language' (C4); the NPR 2005 guesses were nulls and phonetic spelling, and reversal is the simplest Sanborn-style 'visual system' (C3). A mask that only moves letters or inserts nulls is a monotone or mirrored map from plaintext position to intermediate position; after it a periodic tableau with separate alphabets forces key letters at the mapped positions, and the divisor rule gives the live periods exactly as in 0006. Masks: reversal; a null before every k-th letter for k = 2 to 24 at every phase; a prefix of 1 to 24 nulls; and reversal combined with each. For each mask and each of the 24 conventions the smallest live period is found; periods up to 30 have their forced fragments matched against the vocabulary and K1-K3 windows and scored as English, with ten shuffled controls. Bounds: complete for these masks and conventions.

## Prediction

Reversal and every null pattern leave the smallest live period in the 20s or above, as random position maps do. No forced fragment matches a word or beats the shuffled controls. Zero candidates pass.

## Method

1. Build the masks as position maps from plaintext index to intermediate index.
2. For each mask and convention, force the key letter at each crib's intermediate position.
3. Find live periods by the divisor rule.
4. For live periods up to 30, match the forced fragment against the vocabulary and K1-K3 windows and score it as English.
5. Repeat the scoring on ten shuffles of K4.

## Result

Candidates returned: 0. Passed all gates: 0. Best crib hits among all candidates: 0/24
(no candidates).
Best loss: None (0 is solved; 10 per missed crib letter). Best fitness: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| - | no candidates | | | | |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "masked plaintext (reversal, regular nulls, prefix nulls) then periodic tableau",
 "masks": 648,
 "conventions": 24,
 "smallest_live_period_histogram": {
  "26": 11,
  "27": 41,
  "28": 403,
  "29": 110,
  "30": 36,
  "31": 21,
  "32": 6,
  "33": 6
 },
 "masks_dropping_a_crib": 14,
 "best_forced_fragments": [
  {
   "score": -5.378,
   "mask": "reversed, null before every 10th letter, phase 2",
   "convention": "kry/kry/kry/vig",
   "period": 30,
   "fragment": "TALIT.FV..USVICCCUS.KDYZ..QQVY"
  },
  {
   "score": -5.473,
   "mask": "null before every 9th letter, phase 7",
   "convention": "std/kry/std/varbeau",
   "period": 30,
   "fragment": "ETBYVOW...CSOLLAS.MQYU.DEYZ.MV"
  },
  {
   "score": -5.519,
   "mask": "null before every 10th letter, phase 0",
   "convention": "std/kry/std/vig",
   "period": 30,
   "fragment": "WHZ.BEFL..YIMPPAI.OKCG..SUCKOF"
  },
  {
   "score": -5.617,
   "mask": "reversed, 10 nulls first",
   "convention": "std/kry/kry/beau",
   "period": 28,
   "fragment": "IL...JAMBSAHREDA.NIGHAMIMPYY"
  },
  {
   "score": -5.682,
   "mask": "reversed, null before every 10th letter, phase 3",
   "convention": "kry/kry/kry/vig",
   "period": 30,
   "fragment": "TALITN.V..USVICCCUSQ.DYZ..QQVY"
  },
  {
   "score": -5.683,
   "mask": "reversed, 10 nulls first",
   "convention": "std/kry/kry/beau",
   "period": 29,
   "fragment": "....JAMBSAHREDANIGHAMIMPYYIL."
  },
  {
   "score": -5.704,
   "mask": "null before every 10th letter, phase 3",
   "convention": "std/kry/std/varbeau",
   "period": 30,
   "fragment": "ETBYVO.P..CSOLLASLPE.U.DE.YQMV"
  },
  {
   "score": -5.719,
   "mask": "null before every 13th letter, phase 6",
   "convention": "kry/kry/std/beau",
   "period": 29,
   "fragment": "URORN.KB..MDADSTGE.FIY.MDAYWG"
  },
  {
   "score": -5.727,
   "mask": "null before every 10th letter, phase 1",
   "convention": "std/kry/std/vig",
   "period": 30,
   "fragment": "WHZC.EFL..YIMPPAIP.KCG..SUCKOF"
  },
  {
   "score": -5.731,
   "mask": "reversed, null before every 11th letter, phase 10",
   "convention": "kry/kry/std/beau",
   "period": 30,
   "fragment": "GPXH.PF.IY.TOOBOPTDELB...UDISC"
  },
  {
   "score": -5.738,
   "mask": "reversed, null before every 11th letter, phase 9",
   "convention": "kry/kry/std/beau",
   "period": 30,
   "fragment": "GPX.GPF.I.FTOOBOPTDEL.U..UDISC"
  },
  {
   "score": -5.766,
   "mask": "reversed, 10 nulls first",
   "convention": "std/kry/kry/beau",
   "period": 27,
   "fragment": "PYYIL.JAMBSAHREDA..NIGHAMIM"
  },
  {
   "score": -5.768,
   "mask": "reversed, null before every 12th letter, phase 7",
   "convention": "kry/kry/std/beau",
   "period": 30,
   "fragment": "GPX.GPF.IYGX.OBOPTDELB...UDISC"
  },
  {
   "score": -5.79,
   "mask": "reversed, null before every 10th letter, phase 2",
   "convention": "std/kry/std/beau",
   "period": 30,
   "fragment": "PNORW.BF..SEDEEGBOM.XIJO..EFPE"
  },
  {
   "score": -5.806,
   "mask": "null before every 22th letter, phase 1",
   "convention": "kry/kry/std/beau",
   "period": 28,
   "fragment": "GURORNLI..EPFJ.BWJOSTACI.AYW"
  }
 ],
 "shuffled_control_best": [
  -5.209,
  -5.11,
  -4.894,
  -5.524,
  -5.188,
  -5.528,
  -5.534,
  -4.888,
  -5.255,
  -5.415
 ],
 "vocab_matches": 0
}
```

Notes: 648 masks x 24 conventions. Smallest live period over all masks: 26. Best fragment -5.378 vs shuffled best -4.888. 0 matches.


