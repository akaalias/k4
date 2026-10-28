# 0251-f14-plaintext-style-as-the-mask-judge-bench: F14.7: plaintext style as the mask: vowel-dropped, telegraphese and abbreviated English added to the judge bench; power of the quadgram scorer, MIX8m and the blind judge against the bench's 200 hard negatives

**Family:** 14-scheidt-mask-keyed-by-words  
**Parent:** 0233-f13-how-many-bits-per-letter-each-english-judge-extracts  
**Decision:** reverted  
**Run:** 2026-10-28T07:20:19+00:00, 136.3 s, status ran  
**Time by phase:** unattributed 70 s, run 136 s, record 0 s

## In plain words

Messages sent by telegraph or radio were often written short: no little words, no vowels, long words cut down. If K4's hidden message was written that way, our English detectors might not recognise it. We make test messages in those styles from a real English book and check whether each detector can tell them from English-looking nonsense.

## Walkthrough, by hand

1. Take a sentence of Carter, say 'the remains of passage debris that encumbered the lower part of the doorway'.
2. Vowel-dropped: 'th rmns of pssg dbrs tht encmbrd th lwr prt of th drwy' (a word's first letter kept).
3. Telegraphese: 'remains passage debris encumbered lower part doorway X'.
4. Abbreviated: 'the rema of pass debris that encu the lower part of the door' (words of 7 letters or more cut to 4).
5. Score each with the detector and compare with the highest score any nonsense text reaches.

## Worked example (generated)

```
Carter: THE REMAINS OF PASSAGE DEBRIS THAT ENCUMBERED THE LOWER PART OF THE DOORWAY

  vowelless     THRMNSOFPSSGDBRSTHTENCMBRDTHLWRPRTOFTHDRWY
  telegraphese  REMAINSPASSAGEDEBRISENCUMBEREDLOWERPARTDOORWAYX
  abbreviated   THEREMAOFPASSDEBRISTHATENCUTHELOWERPARTOFTHEDOOR
```

## Lineage

Inherits from 0233-f13-how-many-bits-per-letter-each-english-judge-extracts. What changed: F14.7 (issue #93). The judge bench (reports/judge-bench.md, tools/judge_bench.py) measured clean Carter, misspellings, X stops and K1-K3's text; A6.2 (0226) added those classes to the climbs. A plaintext written to be short (Scheidt: 'you've gotta remember your process'; Sanborn's K2 'interrupted radio transmission'; 'it reads like it's disjointed', Scheidt 2015 on the plaintext) would score lower. Three new classes of 30 texts each, cut from Carter with the 24 known letters in place: vowel-dropped (every vowel removed except a word's first letter), telegraphese (articles, auxiliaries and common function words dropped, X for each full stop), abbreviated (every word of 7 or more letters cut to its first 4). Scored by the bench's quadgram measure, by MIX8m (0233) and by the blind judge, each against the bench's own 100 unigram and 100 Markov negatives (judge verdicts cached from the bench run).

## Hypothesis (domain expert)

C19 ('what's a period... special characters don't work', Scheidt 2015), C4(a) (a mask that is only a way of writing), A6 (the plaintext scores as English to our scorer) and A13 (the right decryption will look right). Every sampled close and every F13 statistic assumes the plaintext looks like prose. Pre-registered, as the bench: threshold T = the highest score any negative gets; a scorer 'sees' a class when at least 90% of it is above T. If neither the quadgram scorer, MIX8m nor the judge sees a class, the sampled closes are 'closed for ordinary English' only, and the class is written into A6.

## Prediction

The judge sees telegraphese and abbreviated text (90% or more) but not vowel-dropped text; MIX8m sees telegraphese only; the quadgram scorer sees none (it saw 10% of clean Carter on the bench).

## Method

1. Carter's text (the bench's source), words split on spaces and punctuation; 30 windows per class from random places (seed 251), the style applied, cut to 97 letters, the 24 known letters set in place.
2. Negatives: tools/judge_bench.py's build() (seed 76): 100 unigram and 100 Markov texts, verdicts cached.
3. Scores: the bench's quadgram measure on the free places; MIX8m on the free places' letters; the judge (one call for all, blind).
4. Power per class and scorer at T = the negatives' maximum; also clean Carter from the bench as the reference.

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
 "item": "F14.7",
 "classes": {
  "vowelless": 30,
  "telegraphese": 30,
  "abbreviated": 30
 },
 "negatives": {
  "unigram": 100,
  "markov": 100
 },
 "reference": [
  "clean",
  "xstops"
 ],
 "power_at_negatives_max": {
  "quadgram": {
   "T": -400,
   "clean": 0.1,
   "xstops": 0.033,
   "vowelless": 0.0,
   "telegraphese": 0.0,
   "abbreviated": 0.0
  },
  "mix8m": {
   "T": -204.47492468881808,
   "clean": 0.333,
   "xstops": 0.167,
   "vowelless": 0.0,
   "telegraphese": 0.1,
   "abbreviated": 0.133
  },
  "judge": {
   "T": 68,
   "clean": 1.0,
   "xstops": 1.0,
   "vowelless": 0.133,
   "telegraphese": 1.0,
   "abbreviated": 0.967
  }
 },
 "seen_by": {
  "vowelless": [],
  "telegraphese": [
   "judge"
  ],
  "abbreviated": [
   "judge"
  ]
 },
 "rule": "a scorer sees a class when at least 90% of it is above the highest negative",
 "judge_none": 0,
 "examples": {
  "vowelless": "FREXMPLTHRMYVRYLKLYBDEASTNORTHEASTPCSTHRARINMSMSWTHVGPRBBLYMDDLBERLINCLOCKBLSWHCHBYRFRNCTTHOBJCTS",
  "telegraphese": "TENROYALTOMBSONEFOUNDEASTNORTHEASTNINTOATTEMPTSBADMADETWOOTHERSBERLINCLOCKSTOMBSTWOPILLAGEDTWOINT",
  "abbreviated": "BYREMOANTIQUITIESTOMUEASTNORTHEASTASSUTHEIRSAFETYLEFTINSITUTHEYBERLINCLOCKNERORLATERBECOMETHEPREY"
 },
 "compute_seconds": 84
}
```

Notes: vowelless: quadgram 0.0, MIX8m 0.0, judge 0.133; telegraphese: quadgram 0.0, MIX8m 0.1, judge 1.0; abbreviated: quadgram 0.0, MIX8m 0.133, judge 0.967


