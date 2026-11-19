# 0284-f16.1b-s-r-length-19-one-slip-from-two-keyword-alphabets: F16.1b-s-r: 0282's edge at key length 19 (K4 one slip from fitting two dictionary keyword alphabets): the count against 1,000 fresh shuffles and against stand-ins that keep the R-to-P repeat at 28 and 66; K4's one-slip settings read with the key free against 1,000 copies that keep the 20 official places; plants with one slip

**Family:** 16-simple-hand-methods  
**Parent:** 0282-f16.1b-s-two-dictionary-keyword-alphabets-with-slips  
**Decision:** reverted  
**Run:** 2026-11-19T08:09:42+00:00, 2229.7 s, status ran  
**Time by phase:** design 22 s, test 19 s, run 2230 s, record 0 s

## In plain words

With a key 19 letters long, the two known stretches of K4 sit exactly under the same key letters, and K4 comes within one wrong letter of fitting a cipher built from two keyword alphabets (an alphabet that starts with a word and goes on with the unused letters). Scrambled copies rarely come that close. Part of the reason is known: the letter R turns into P at two places 38 apart. We check whether there is more to it than that, and we read the letters each near-fit would give, against scrambled copies read the same way.

## Walkthrough, by hand

1. Write K4 in rows of 19: places 26-34 fall under places 64-72, column for column.
2. Pick two keyword alphabets, say one from FOREST for the cipher side and one from BINDERY for the plain side.
3. In each column the two known pairs must need the same key letter; count the columns where they do not.
4. If exactly one column fails, call one of its two carved letters a slip and take the key letter from the other.
5. Columns 7-17 now have key letters: decrypt the three other rows of those columns (places 7-17, 45-55, 83-93).
6. Score those 33 letters as English; repeat for every pair of alphabets that comes this close.
7. Do the same on copies of K4 whose other 77 letters are shuffled, and compare the best scores.

## Worked example (generated)

```
K4 in rows of 19: the official runs 26-34 and 64-72 share columns 7-15

column  place  known  carved   place  known  carved   shift on the plain table (carved - known)
     7     26      N       Q      64      B       N    3 and 12
     8     27      O       Q      65      E       Y    2 and 20
     9     28      R       P      66      R       P   24 and 24   equal
    10     29      T       R      67      L       V   24 and 10
    11     30      H       N      68      I       T    6 and 11
    12     31      E       G      69      N       T    2 and  6
    13     32      A       K      70      C       M   10 and 10   equal
    14     33      S       S      71      L       Z    0 and 14
    15     34      T       S      72      O       F   25 and 17

Places 28 and 66 both turn R into P; 32 and 70 share the shift 10 (A to K, C to M).
```

## Lineage

Inherits from 0282-f16.1b-s-two-dictionary-keyword-alphabets-with-slips. What changed: F16.1b-s-r (issue #123). 0282 found K4 fitting a pair of dictionary keyword alphabets at key length 19 in 200 of 210 drop sets of one or two of the 20 official letters, its 20 shuffles in at most 39 (p 0.048, both forms). Here, length 19 only: (1) the same count for 1,000 fresh shuffles, for 300 stand-ins that keep the carved letters at 28 and 66 (R to P twice, 38 = 2 x 19 apart: one of the nine checks at 19 is then free, as on K4), and for 300 that also keep 32 and 70 (A to K, C to M: the same shift on the plain table); (2) every setting K4 fits with one letter dropped, the key free (a chart key, #124): the 11 forced key letters read 33 unknown letters in three runs of 11; quadgram score of the best setting against the same settings on 1,000 copies that keep the 20 official places and shuffle the other 77; the judge on the tops. Strength aimed at: sampled.

## Hypothesis (domain expert)

C27(c) and C1(c) (two keyword-mixed alphabets, Quagmire IV, a repeating key), C17 and A1 (one enciphering slip, as K2 has; 12-assumptions.md), the revised criteria (#124: a chart key, a named slip). Cipher: c = CA[PA^-1(p) + k_(i mod 19)] (added) or CA[k - PA^-1(p)] (Beaufort), PA and CA keyword alphabets of 208,064 dictionary and puzzle words, key free. At length 19 the official runs 26-34 and 64-72 share key slots 6-14 (nine checks), 73 and 74 sit alone in slots 15 and 16. A true period-19 system predicts the R/P repeat at 28 and 66 (same slot, same plain letter). 0123/0124 put the repeat at about 1 in 40 by chance; 0148 found K1/K2's own tables one slip (at 33) from fitting, with a decider too weak to read it. Tests: counts (drop sets with a fitting pair, per form; one-slip settings) against plain shuffles (replication of 0282) and against repeat-keeping stand-ins (the fair null: is there more than the repeat?); readings (max over K4's one-slip settings of the mean log10 quadgram probability over the three 11-letter runs at places 7-17, 45-55, 83-93) against kept-place copies under the same settings. Flag lines, set before the run: counts against the repeat-keeping stand-ins p < 0.01; reading p < 0.01. Plants: English with the known words, two random keyword alphabets, a random 19-letter key, one slip at a paired official place; found when the planted pair is listed, ranks first among the plant's settings and beats every one of the plant's 1,000 kept-place copies.

## Prediction

Against plain shuffles K4's count stays rare (p between 0.01 and 0.06); against stand-ins that keep the R/P repeat it is ordinary (p above 0.05). K4's best one-slip reading scores inside its kept-place copies (p above 0.05) and the judge gives it no more than the copies' tops. Plants found at least 6 of 8. No candidate (8 of 19 key letters stay open).

## Method

1. 0282's pair index (0275's, 0244's alphabets), key length 19 only, for each text and each of the 210 drop sets of one or two official letters: the number of fitting alphabet pairs per form; one-letter drops listed.
2. Texts: K4; 1,000 shuffles; 300 shuffles keeping the carved letters at 28, 66; 300 keeping 28, 66, 32, 70; 8 plants.
3. Counts: drop sets fitting per form, one-slip settings; p of K4 against each set of stand-ins.
4. Readings: for each one-slip setting (form, alphabets, dropped place) the key letter of each slot 6-16 from the remaining known letter there; decrypt places 7-17, 45-55, 83-93; score by quadgrams. K4's best against the best of each of 1,000 kept-place copies (20 official places kept, 77 shuffled) under the same settings.
5. Judge: K4's top 5 readings and the top reading of each of the first 100 kept-place copies, one call, '?' for open letters.
6. Plants: the same, each against its own 1,000 kept-place copies.

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
 "item": "F16.1b-s-r",
 "key_length": 19,
 "known_places": [
  26,
  27,
  28,
  29,
  30,
  31,
  32,
  33,
  34,
  64,
  65,
  66,
  67,
  68,
  69,
  70,
  71,
  72,
  73,
  74
 ],
 "drop_sets": 210,
 "alphabets_each_side": 208064,
 "counts": {
  "k4": {
   "drop_sets_added": 200,
   "drop_sets_beaufort": 200,
   "single_drops_fitting": 32,
   "one_slip_settings": 272
  },
  "sh": {
   "drop_sets_added": {
    "median": 28.0,
    "max": 210,
    "at_or_above": 16,
    "p": 0.017
   },
   "drop_sets_beaufort": {
    "median": 24.0,
    "max": 210,
    "at_or_above": 13,
    "p": 0.014
   },
   "single_drops_fitting": {
    "median": 0.0,
    "max": 40,
    "at_or_above": 8,
    "p": 0.009
   },
   "one_slip_settings": {
    "median": 0.0,
    "max": 1452,
    "at_or_above": 7,
    "p": 0.008
   }
  },
  "rp": {
   "drop_sets_added": {
    "median": 178.0,
    "max": 210,
    "at_or_above": 93,
    "p": 0.3123
   },
   "drop_sets_beaufort": {
    "median": 178.0,
    "max": 210,
    "at_or_above": 96,
    "p": 0.3223
   },
   "single_drops_fitting": {
    "median": 24.0,
    "max": 40,
    "at_or_above": 57,
    "p": 0.1927
   },
   "one_slip_settings": {
    "median": 93.0,
    "max": 6104,
    "at_or_above": 39,
    "p": 0.1329
   }
  },
  "rpam": {
   "drop_sets_added": {
    "median": 200.0,
    "max": 210,
    "at_or_above": 176,
    "p": 0.588
   },
   "drop_sets_beaufort": {
    "median": 189.0,
    "max": 210,
    "at_or_above": 122,
    "p": 0.4086
   },
   "single_drops_fitting": {
    "median": 30.0,
    "max": 40,
    "at_or_above": 127,
    "p": 0.4252
   },
   "one_slip_settings": {
    "median": 237.0,
    "max": 5492,
    "at_or_above": 132,
    "p": 0.4419
   }
  }
 },
 "count_flag_line": "p < 0.01 against the stand-ins that keep 28 and 66 (rp)",
 "reading": {
  "k4_one_slip_settings": 272,
  "letters_read": 33,
  "runs": [
   [
    7,
    17
   ],
   [
    45,
    55
   ],
   [
    83,
    93
   ]
  ],
  "k4_best": -6.664830624264806,
  "copies": 1000,
  "copies_best_median": -6.7310027987716685,
  "copies_best_max": -5.719431400135476,
  "at_or_above": 406,
  "p": 0.4066,
  "flag_line": "p < 0.01",
  "k4_top": [
   {
    "form": "added",
    "slip_at": 34,
    "plain_alphabet": "SYMBOLOGY",
    "cipher_alphabet": "GALLIVANT",
    "score": -6.665,
    "reading": "??????UMMIMHSSDRO????????NORTHEASIAA????????CSYSBFZRARV????????BERLINCLOCK????????GULYULLYTHF????",
    "judge": 4
   },
   {
    "form": "added",
    "slip_at": 33,
    "plain_alphabet": "RIBBONRY",
    "cipher_alphabet": "REFLECTOR",
    "score": -6.81,
    "reading": "??????EPSYMBRECSH????????NORTHEAETVY????????JZDSQAWOLST????????BERLINCLOCK????????MTUNFSOFDFI????",
    "judge": 3
   },
   {
    "form": "added",
    "slip_at": 29,
    "plain_alphabet": "ITHOMIID",
    "cipher_alphabet": "DEGASIFICATION",
    "score": -6.822,
    "reading": "??????UUODJWOSAAM????????NORJHEASTIB????????YZIRLFIHGAS????????BERLINCLOCK????????MGAVATMEIGI????",
    "judge": 3
   },
   {
    "form": "added",
    "slip_at": 68,
    "plain_alphabet": "SEXTUPLY",
    "cipher_alphabet": "ACETOTHIENONE",
    "score": -7.015,
    "reading": "??????ZYKJEUTSHAC????????NORTHEASTWY????????UJPCTJWNVAW????????BERLCNCLOCK????????TFFROCSECHL????",
    "judge": 2
   },
   {
    "form": "added",
    "slip_at": 33,
    "plain_alphabet": "TRIBUTIST",
    "cipher_alphabet": "DEBONAIRLY",
    "score": -7.058,
    "reading": "??????XBWABSPEFYS????????NORTHEAETPP????????TLEOSIGUWYQ????????BERLINCLOCK????????ETMSXOUGHGT????",
    "judge": 4
   },
   {
    "form": "added",
    "slip_at": 67,
    "plain_alphabet": "ITHOMIID",
    "cipher_alphabet": "DEGASIFICATION",
    "score": -7.091,
    "reading": "??????UUOUJWOSAAM????????NORTHEASTIB????????YZIBLFIHGAS????????BEROINCLOCK????????MGAFATMEIGI????"
   },
   {
    "form": "added",
    "slip_at": 64,
    "plain_alphabet": "SEXTUPLY",
    "cipher_alphabet": "ACANTHOID",
    "score": -7.113,
    "reading": "??????ZAKILUTSIAC????????NORTHEASTZY????????DJPCAJWNVAW????????UERLINCLOCK????????TCFRZCZECHG????"
   },
   {
    "form": "added",
    "slip_at": 26,
    "plain_alphabet": "SEXTUPLY",
    "cipher_alphabet": "ZOANTHIDAE",
    "score": -7.143,
    "reading": "??????UTKILUTSCAB????????WORTHEASTOY????????HJPCAKWNVAW????????BERLINCLOCK????????JBDRZCZEDHD????"
   },
   {
    "form": "added",
    "slip_at": 71,
    "plain_alphabet": "TRIBUTIST",
    "cipher_alphabet": "DEBONAIRLY",
    "score": -7.15,
    "reading": "??????XBWABSPSFYS????????NORTHEASTPP????????TLEOSIGTWYQ????????BERLINCGOCK????????ETMSXOUCHGT????"
   },
   {
    "form": "added",
    "slip_at": 26,
    "plain_alphabet": "SEXTUPLY",
    "cipher_alphabet": "JANTHINIDAE",
    "score": -7.159,
    "reading": "??????UMKILTUSZYC????????WORTHEASTBA????????HIPCAKZYRYZ????????BERLINCLOCK????????JBDRWCSEDHF????"
   }
  ]
 },
 "judge": {
  "sent": 105,
  "none": 0,
  "k4_top5": [
   4,
   3,
   3,
   2,
   4
  ],
  "k4_best": 4,
  "copies_best": 12,
  "k4_above_every_copy": false
 },
 "plants": [
  {
   "plant": "plant0",
   "form": "added",
   "slip": 64,
   "partner": 26,
   "settings": 232,
   "listed": true,
   "reading_right_fraction": 0.9818181818181818,
   "score": -3.966315017629947,
   "ranks_first": true,
   "copies_best_max": -5.604607254719906,
   "found": true
  },
  {
   "plant": "plant1",
   "form": "added",
   "slip": 67,
   "partner": 29,
   "settings": 206,
   "listed": true,
   "reading_right_fraction": 0.9818181818181818,
   "score": -3.852755108750578,
   "ranks_first": true,
   "copies_best_max": -5.467415075730524,
   "found": true
  },
  {
   "plant": "plant2",
   "form": "beaufort",
   "slip": 29,
   "partner": 67,
   "settings": 102,
   "listed": true,
   "reading_right_fraction": 0.9818181818181818,
   "score": -4.248737055816735,
   "ranks_first": true,
   "copies_best_max": -5.773631574711267,
   "found": true
  },
  {
   "plant": "plant3",
   "form": "beaufort",
   "slip": 65,
   "partner": 27,
   "settings": 136,
   "listed": true,
   "reading_right_fraction": 0.9818181818181818,
   "score": -3.5783169633614818,
   "ranks_first": true,
   "copies_best_max": -5.702186320666308,
   "found": true
  },
  {
   "plant": "plant4",
   "form": "added",
   "slip": 64,
   "partner": 26,
   "settings": 280,
   "listed": true,
   "reading_right_fraction": 0.9818181818181818,
   "score": -3.8946979890498246,
   "ranks_first": true,
   "copies_best_max": -5.80279810331982,
   "found": true
  },
  {
   "plant": "plant5",
   "form": "beaufort",
   "slip": 30,
   "partner": 68,
   "settings": 4000,
   "listed": true,
   "reading_right_fraction": 0.9818181818181818,
   "score": -4.2752958400815375,
   "ranks_first": true,
   "copies_best_max": -5.5100907657092995,
   "found": true
  },
  {
   "plant": "plant6",
   "form": "beaufort",
   "slip": 28,
   "partner": 66,
   "settings": 4,
   "listed": true,
   "reading_right_fraction": 0.9818181818181818,
   "score": -3.940800063249533,
   "ranks_first": true,
   "copies_best_max": -6.396287696968322,
   "found": true
  },
  {
   "plant": "plant7",
   "form": "beaufort",
   "slip": 66,
   "partner": 28,
   "settings": 10,
   "listed": true,
   "reading_right_fraction": 0.9818181818181818,
   "score": -4.298290172068515,
   "ranks_first": true,
   "copies_best_max": -5.929014881736335,
   "found": true
  }
 ],
 "plants_found": 8,
 "plants_total": 8,
 "not_covered": "settings needing two slips (pair drops) are counted, not read; 8 of 19 key letters stay open in every reading",
 "controls": "1000 plain shuffles, 300 keeping 28 and 66, 300 keeping 28, 66, 32, 70 (counts); 1000 kept-place copies (readings)",
 "exhaustive": "yes at key length 19 for the 210 drop sets; readings sampled against copies",
 "aws_cost_estimate_dollars": 1.3
}
```

Notes: counts: K4 {'drop_sets_added': 200, 'drop_sets_beaufort': 200, 'single_drops_fitting': 32, 'one_slip_settings': 272}; p against plain shuffles 0.017/0.014, against R/P-keeping stand-ins 0.3123/0.3223; reading: K4 best -6.664830624264806, 406 of 1000 kept-place copies at or above (p 0.4066); judge K4 4 vs copies 12; plants 8/8


