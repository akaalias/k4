# 0150-one-carved-letter-wrong-through-free-alphabet-gromark: F1.6, second part: one carved letter wrong at a known place, or one letter missing or extra, through the exact free-alphabet Gromark verdicts (base 10 two- and three-term, other bases)

**Family:** 1-keyed-periodic  
**Parent:** 0147-one-carved-letter-wrong-through-the-free-alphabet-tests  
**Decision:** reverted  
**Run:** 2026-10-16T20:52:37+00:00, 1359.1 s, status ran  
**Time by phase:** unattributed 86 s, run 1359 s, record 0 s

## In plain words

Gromark is a cipher whose key is a stream of digits grown from a few starting digits, used with a scrambled alphabet; earlier experiments showed no starting digits and no alphabet fit the 24 known letters. If one carved letter is wrong, or one is missing or extra, that verdict might be unfair. We change each carved letter at the known places to every other letter, shift the known words by one place, and rerun the exact Gromark tests.

## Walkthrough, by hand

1. Take Rogers' rule (each digit the sum of the digits 5 and 4 places back, mod 10) and a primer.
2. Suppose the carved Q at place 27 should have been another letter, say R.
3. Places 26 and 27 no longer carve the same letter, so their digit difference is no longer forced; other equal pairs still are.
4. Test every primer against the remaining pairs, then check that the slots and letters pair one to one.
5. Repeat for every changed letter, every shift of the known words, every rule, base and form.

## Worked example (generated)

```
the carved letters at the known places and the changes tried:

place 22: carved F under known E; tried the other 25 letters
place 26: carved Q under known N; tried the other 25 letters
place 27: carved Q under known O; tried the other 25 letters
place 33: carved S under known S; tried the other 25 letters
place 74: carved K under known K; tried the other 25 letters

plus every known place's carved letter moved one place left or right (a letter extra or missing before EAST),
and BERLINCLOCK's alone moved (a letter extra or missing between the two known words)
```

## Lineage

Inherits from 0147-one-carved-letter-wrong-through-the-free-alphabet-tests. What changed: F1.6, Gromark verdicts. 0069, 0076 and 0107 showed no primer of any two- or three-term Gromark rule gives a one-to-one alphabet consistent with the 24 known letters, in base 10 and bases 2-9, 11-16, 26. Here every single-letter error those tests can see: the carved letter at each known place changed to each other letter (600), and one letter missing or extra before EAST (every known place moves by one) or between the runs (BERLINCLOCK moves by one): 604 variants of K4. The Gromark key depends on absolute position, so the shifts matter here, unlike for periodic keys. K4's variants first; scrambled copies only if a variant fits.

## Hypothesis (domain expert)

Family G and C17 (a carving slip), C22(a) (the raised YAR as a Gromark primer), family E (Bean's Gromark case, knowledge/sources/bean-2021-cryptodiagnosis-of-k4.txt). Models and deciders unchanged from 0069 (base 10, two-term rules with lags up to 6, every primer, four forms), 0076 (bases 2-9 and 11-16 with lags up to 5, base 26 with lags up to 4) and 0107 (three-term rules, base 10, lags up to 6): equal-letter pairs fix exact digit differences, then a full one-to-one check. Exact. If no variant of K4 fits, the result is exact and needs no controls; any fit is compared with the same variants of ten scrambled copies in a follow-up.

## Prediction

No variant fits under any rule, base or form: Gromark stays dead with a single carving error. Zero candidates.

## Method

1. Load 0069, 0076 and 0107's deciders unchanged.
2. For each rule and base: the digit stream at the known places for the copper's positions and for the four shifts.
3. For each of 604 variants: the equal-letter pairs, then every primer, then the one-to-one check.
4. List any variant that fits.

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
 "family": "free-alphabet Gromark (0069, 0076, 0107) on 604 one-letter variants of K4",
 "variants": 605,
 "settings": {
  "0069": {
   "settings": 15,
   "settings_with_a_fit": 0
  },
  "0076": {
   "settings": 146,
   "settings_with_a_fit": 0
  },
  "0107": {
   "settings": 20,
   "settings_with_a_fit": 0
  }
 },
 "fits": [],
 "n_settings_with_fit": 0,
 "seconds": 1359,
 "exhaustive": true,
 "controls": "none needed if nothing fits (exact); any fit is compared with the same variants of 10 scrambled copies in a follow-up"
}
```

Notes: 605 variants x 181 rule/base settings: settings with any fitting variant 0


