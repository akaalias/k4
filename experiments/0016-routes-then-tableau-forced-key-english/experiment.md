# 0016-routes-then-tableau-forced-key-english: Every route from 0006 and 0008, then the tableau: does any route make the forced key read as English?

**Family:** 6-transposition-then-tableau  
**Parent:** 0008-k3-formula-all-shifts-then-tableau  
**Decision:** reverted  
**Run:** 2026-10-14T17:11:36+00:00, 80.6 s, status ran  
**Time by phase:** design 11 s, implement 53 s, test 17 s, run 81 s, record 0 s

## In plain words

Earlier we asked whether a grid scramble followed by the table could use a short secret word; none could. Now we ask a softer question: for each scramble, the 24 known letters pin down 24 letters of the secret word, scattered through it. Do those pinned letters ever spell something that looks like English? We check every scramble we have, and we run the same check on the carved letters shuffled at random, so we know what a meaningless best looks like.

## Walkthrough, by hand

1. Take the route: write in rows of 7, read down the columns.
2. The known letters at 22 to 34 land at 4, 18, 32, 46, 60, 74, 88, 5, 19, 33, 47, 61, 75; those at 64 to 74 land elsewhere.
3. Under the sculpture's alphabet with Vigenere, each landing spot has a forced key letter.
4. Choose period 28: slot is the landing spot minus one, mod
28. 
5. Write the 28 slots in a row and fill in the forced letters; 24 of 28 are filled.
6. Read the filled stretches.
7. Score them as English; compare with what random letters would give.

## Worked example (generated)

```
route: columnar width 7, read columns left to right; convention kry/kry/kry Vigenere; period 28

slot:  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
key:   .  .  .  Q  G  .  .  .  .  L  E  .  .  .  .  .  .  U  N  .  .  .  .  O  K  .  .  .

runs scored: 
```

## Lineage

Inherits from 0008-k3-formula-all-shifts-then-tableau. What changed: 0006 and 0008 matched forced key fragments against a word list. Here the forced key under every route and live period up to 40 is scored as English, with a shuffled-letter control, as 0009 did for the plain tableau.

## Hypothesis (domain expert)

Under K4 = tableau(T(P)) with a periodic key of period p, each route T sends the 24 cribs to 24 intermediate positions whose forced key letters fill 24 slots of the key, most of them distinct when p is 27 or more. If the key is a word or phrase (C5, C6), the filled slots read as English in slot order. Routes: the 2,905 columnar routes of 0006 and the 21,025 K3-rule and double-rotation routes of 0008, under all 24 conventions; for each live period up to 40 the forced slots are collected, runs of five or more consecutive filled slots, at least four quadgrams in all, are scored by quadgram log-probability, and the best (route, convention, period) is compared with the same procedure on two shuffles of the K4 letters. Chance expectation: the best of about a million scores sits where the shuffled best sits. Bounds: complete for these route sets, conventions and periods, for readable keys.

## Prediction

The best forced key over all routes, conventions and periods scores within 0.2 of the best from shuffled K4 letters, and the top entries show no recognisable word of five or more letters. Zero candidates pass.

## Method

1. Build the route sets of 0006 and 0008.
2. For each route, send each crib position to its intermediate position.
3. For each convention, force the key letter there.
4. For each period from 2 to 40 that the forced letters allow, place them in slots and score runs of four or more consecutive filled slots.
5. Keep the best twenty overall.
6. Repeat on two shuffles of K4.

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
 "family": "transposition then periodic tableau; forced key scored as English",
 "routes": 23930,
 "conventions": 24,
 "periods": "2-40, live only",
 "scores": 461692,
 "best": [
  {
   "score": -3.547,
   "route": "K3 rule a=78 b=11 fwd",
   "convention": "kry/std/std/varbeau",
   "period": 40,
   "runs": [
    "UHAVETHE"
   ]
  },
  {
   "score": -3.547,
   "route": "K3 rule a=37 b=53 inv",
   "convention": "kry/std/std/varbeau",
   "period": 40,
   "runs": [
    "UHAVETHE"
   ]
  },
  {
   "score": -3.891,
   "route": "K3 rule a=48 b=94 fwd",
   "convention": "kry/std/std/beau",
   "period": 34,
   "runs": [
    "VEDANGE"
   ]
  },
  {
   "score": -3.891,
   "route": "K3 rule a=16 b=32 inv",
   "convention": "kry/std/std/beau",
   "period": 34,
   "runs": [
    "VEDANGE"
   ]
  },
  {
   "score": -3.949,
   "route": "K3 rule a=27 b=11 fwd",
   "convention": "std/kry/std/vig",
   "period": 40,
   "runs": [
    "MTHESFI"
   ]
  },
  {
   "score": -3.949,
   "route": "K3 rule a=24 b=53 inv",
   "convention": "std/kry/std/vig",
   "period": 40,
   "runs": [
    "MTHESFI"
   ]
  },
  {
   "score": -3.965,
   "route": "K3 rule a=90 b=25 fwd",
   "convention": "std/std/kry/varbeau",
   "period": 34,
   "runs": [
    "POINGAA"
   ]
  },
  {
   "score": -3.965,
   "route": "K3 rule a=74 b=66 inv",
   "convention": "std/std/kry/varbeau",
   "period": 34,
   "runs": [
    "POINGAA"
   ]
  },
  {
   "score": -4.162,
   "route": "K3 rule a=88 b=51 fwd",
   "convention": "std/kry/std/vig",
   "period": 30,
   "runs": [
    "RENTHAPSS"
   ]
  },
  {
   "score": -4.162,
   "route": "K3 rule a=23 b=78 inv",
   "convention": "std/kry/std/vig",
   "period": 30,
   "runs": [
    "RENTHAPSS"
   ]
  },
  {
   "score": -4.213,
   "route": "K3 rule a=72 b=52 inv",
   "convention": "kry/std/std/beau",
   "period": 32,
   "runs": [
    "REATHL",
    "OHARR"
   ]
  },
  {
   "score": -4.213,
   "route": "K3 rule a=21 b=28 fwd",
   "convention": "kry/std/std/beau",
   "period": 32,
   "runs": [
    "REATHL",
    "OHARR"
   ]
  },
  {
   "score": -4.232,
   "route": "K3 rule a=86 b=31 inv",
   "convention": "std/kry/std/beau",
   "period": 34,
   "runs": [
    "DONITER"
   ]
  },
  {
   "score": -4.232,
   "route": "K3 rule a=16 b=72 fwd",
   "convention": "std/kry/std/beau",
   "period": 34,
   "runs": [
    "DONITER"
   ]
  },
  {
   "score": -4.299,
   "route": "keyed columnar WALL inv",
   "convention": "kry/kry/kry/beau",
   "period": 33,
   "runs": [
    "HECEOFM"
   ]
  },
  {
   "score": -4.352,
   "route": "K3 rule a=59 b=94 fwd",
   "convention": "kry/std/kry/varbeau",
   "period": 34,
   "runs": [
    "HATORNS"
   ]
  },
  {
   "score": -4.352,
   "route": "K3 rule a=52 b=32 inv",
   "convention": "kry/std/kry/varbeau",
   "period": 34,
   "runs": [
    "HATORNS"
   ]
  },
  {
   "score": -4.364,
   "route": "K3 rule a=86 b=66 inv",
   "convention": "std/std/std/vig",
   "period": 34,
   "runs": [
    "OVENOTM"
   ]
  },
  {
   "score": -4.364,
   "route": "K3 rule a=81 b=25 fwd",
   "convention": "std/std/std/vig",
   "period": 34,
   "runs": [
    "OVENOTM"
   ]
  },
  {
   "score": -4.365,
   "route": "K3 rule a=94 b=72 fwd",
   "convention": "kry/kry/kry/vig",
   "period": 34,
   "runs": [
    "IANTIVA"
   ]
  }
 ],
 "shuffled_control": [
  {
   "best": -3.808,
   "route": "K3 rule a=64 b=77 inv",
   "period": 38,
   "runs": [
    "POSENTST"
   ]
  },
  {
   "best": -4.025,
   "route": "K3 rule a=79 b=72 fwd",
   "period": 38,
   "runs": [
    "STHEDNA"
   ]
  }
 ]
}
```

Notes: Diagnostic, no candidates. 461692 (route, convention, period) keys scored; best -3.547 vs shuffled [-3.808, -4.025].


