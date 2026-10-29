# 0253-f1.4-one-alphabet-residue-decided-by-the-one-run-decider: F1.4: every hand key schedule K4 fits on one free alphabet (2,093 settings, both forms), each decided by D1's one-run decider against copies climbed one at a time

**Family:** 1-keyed-periodic  
**Parent:** 0252-d2-one-run-decider-power-and-cost-on-schedules-and-moves  
**Decision:** reverted  
**Run:** 2026-10-29T15:48:02+00:00, 14649.7 s, status ran  
**Time by phase:** design 131 s, implement 3 s, test 13 s, run 14650 s, record 0 s

## In plain words

Sanborn may have used the cipher table with a twist in how he stepped through the key word (skipping a letter now and then, going back and forth) and with his own scrambled alphabet. About two thousand such twists are consistent with the 24 known letters, so those letters cannot tell them apart. For each one we search for the most English-looking reading of K4 and do the same on scrambled copies of K4 that fit the same twist equally well; a real answer should read better than all its copies.

## Walkthrough, by hand

1. Pick a schedule, say: key of 11 letters, skip one key letter after every 7 carved letters.
2. Write the key slot under each of the 97 carved letters.
3. Check with the 24 known letters that some alphabet makes them agree (two known places in one slot must differ by the same amount on the alphabet).
4. Search alphabets and keys for the most English-looking reading of K4 under that slot map.
5. Shuffle K4's letters until the shuffle also passes step 3, and search it the same way.
6. If the shuffle reads as well as K4, stop: K4 is ordinary there. Otherwise shuffle again, up to 12 times (100 if K4 keeps winning).
7. Count how often K4 won all 12; chance alone gives about one setting in 13.

## Worked example (generated)

```
F1.4: one free alphabet under a hand key schedule, decided setting by setting.

  setting      skip one key letter every 7 letters, 11 key letters
  slot map     place 1 2 3 4 5 6 7 8 9 ...
  key letter         1 2 3 4 5 6 8 9 10 ... (letter 7 skipped)

  K4 gets one tempering search under that slot map; then scrambled copies that fit the same 24 checks
  get one each, one at a time, until a copy reads as well as K4 (at most 12, or 100 if K4 keeps winning).
  Chance alone lets K4 win all 12 in about 1 setting of 13.
```

## Lineage

Inherits from 0252-d2-one-run-decider-power-and-cost-on-schedules-and-moves. What changed: F1.4, the one-alphabet residue reopened by D2 (0252). 0252 measured the one-run decider's power on F1.4's schedules (37 of 48 per group against 6 own copies) and costed the residue at about 41 core-hours. Here every one of the 2,093 (schedule, slot count, form) settings K4 fits is decided: K4 is climbed once, then shuffles that the exact decider also fits at that setting are climbed one at a time until one reaches K4's score, up to 12; where K4 beats all 12 the copies go on to 100. 24 plants (12 clean, 12 Sanborn-style) on settings K4 fits go through the same decision in the same run.

## Hypothesis (domain expert)

F1.4: a keyed table with a hand key schedule other than a plain repeat (C20(d): tableau rows as keys; the schedules of 0126-0128: one key letter skipped every m letters, stutter, back and forth, triangle, square, a restart per carved line), with one free alphabet on both sides (Quagmire III with an unknown order, Sanborn's 'slightly different' tableau, C27(c)), Beaufort or added form. 0127/0128 closed the standard and KRYPTOS tables exactly; on a free alphabet K4 fits 2,093 settings at the copies' rate (0252's exact recount: 2,016 skip schedules, 77 others), each with its 24 known letters satisfied by some alphabet, so the known letters cannot decide them and English must. The decider is 0140's tempering climb (one run, 16 x 625 x 1000) generalised to any slot map (0252, identical to 0140 on plain periodic keys), with copies drawn as shuffles the exact decider fits at the same setting, so K4 and its copies have the same freedom. Clue entries: C20(d), C27(c), C5(a).

## Prediction

No setting stands out: the number of settings where K4 beats all 12 copies is within the binomial range for 1/13 (about 161 of 2,093, sd about 12; anything above 186 is an excess to chase), and the settings where K4 beats 100 copies are about 1 in 101 (about 21, at most about 30). Plants found (above all 12 own copies) about 16 of 24 (0252's 37 of 48 against 6 copies, lower against 12). Zero candidates returned (see notes).

## Method

1. Settings: 0252's f14_settings() (every 0128 schedule at every slot count 2-31, as a slot map over the 97 places, deduplicated), both forms, each decided exactly on K4 by 0128's decide(); the fitting ones are the cell.
2. Per setting (one job, seeded by its index): climb K4 once with 0252's climb(); then draw shuffles of K4 until one fits the setting exactly, climb it, and stop at the first copy whose best is at or above K4's; at most 12 copies, and where K4 is above all 12, go on to at most 100. Record K4's score, reading, and the number of copies it stayed above.
3. Plants: 12 clean (Carter windows, 0120's rule) and 12 Sanborn-style (0226's classes), each on a setting drawn from the cell, random alphabet and key, decided by the same job without the escalation; found if above all 12.
4. Verdict: the count of settings where K4 beats all 12 against Binomial(n, 1/13); settings above 100 copies listed with their readings and known letters, to be chased in a row of their own if the count is in excess.

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
 "item": "F1.4 (one free alphabet residue, reopened by D2/0252)",
 "decider": "D1's one-run decider: 0140's tempering (16 x 625 x 1000) generalised to any slot map (0252); copies = shuffles the exact decider fits at the same setting, climbed one at a time, stop at the first at or above K4, at most 12, escalated to 100 where K4 beats all 12",
 "self_check_against_0140": [
  [
   23,
   -5.23832,
   -5.23832
  ],
  [
   26,
   -5.13042,
   -5.13042
  ]
 ],
 "settings_listed": {
  "F1.4 skip": 11164,
  "F1.4 other": 1482
 },
 "k4_fitting_settings": 2093,
 "k4_fitting_by_group": {
  "F1.4 skip": 2016,
  "F1.4 other": 77
 },
 "k4_above_all_12": 299,
 "expected_by_chance_12": 161.0,
 "binomial_p_12": 1.1193307301099235e-24,
 "k4_above_all_100": 66,
 "expected_by_chance_100": 20.7,
 "binomial_p_100": 1.2466201215349414e-15,
 "k4_copies_beaten_histogram": {
  "0": 822,
  "1-11": 972,
  "12-99": 233,
  "100": 66
 },
 "settings_with_copy_generation_failure": 0,
 "top_settings": [
  {
   "group": "F1.4 skip",
   "setting": "B skip m=8 phi=2 n=23",
   "form": "V",
   "slots": 23,
   "above": 100,
   "copies_climbed": 100,
   "score": -4.81163,
   "copies_max": -4.86148,
   "reading": "HAPSMADESISTBTONACOBLEASTNORTHEASTRTINTSOUNGAIFSALPMALEDFOSYNSABERLINCLOCKENDOBETOTEROYHERLTHAMPR",
   "known_in_place": 24
  },
  {
   "group": "F1.4 other",
   "setting": "D back and forth n=24 ends=once phi=13",
   "form": "B",
   "slots": 24,
   "above": 100,
   "copies_climbed": 100,
   "score": -4.84537,
   "copies_max": -4.88599,
   "reading": "IFKLATESDETOSOOFTHFFFEASTNORTHEASTBERSEWENEREDGMSEIDBEKINVERALOBERLINCLOCKDINARVIROPPALIKELACKIEZ",
   "known_in_place": 24
  },
  {
   "group": "F1.4 skip",
   "setting": "B skip m=13 phi=10 n=22",
   "form": "V",
   "slots": 22,
   "above": 100,
   "copies_climbed": 100,
   "score": -4.89366,
   "copies_max": -4.89862,
   "reading": "AOSLINBEIBMEBTHWELLINEASTNORTHEASTHETBENODENDAHEDNACALNICIATHMOBERLINCLOCKATIONMUTYRTIATYONDTABOO",
   "known_in_place": 24
  },
  {
   "group": "F1.4 skip",
   "setting": "B skip m=12 phi=5 n=22",
   "form": "V",
   "slots": 22,
   "above": 100,
   "copies_climbed": 100,
   "score": -4.93151,
   "copies_max": -5.04118,
   "reading": "FOWSHERKEPEIBTIMATIMMEASTNORTHEASTIOECDDITHPCASAIDSTALBEAPPLEIOBERLINCLOCKPLECONFOLLOMACORDERKMGB",
   "known_in_place": 24
  },
  {
   "group": "F1.4 skip",
   "setting": "B skip m=12 phi=6 n=22",
   "form": "V",
   "slots": 22,
   "above": 100,
   "copies_climbed": 100,
   "score": -4.96054,
   "copies_max": -4.98994,
   "reading": "EHISOWWAIDHEBTEORYSPREASTNORTHEASTECLITTEFORMIGHPSEDALANREEWAGHBERLINCLOCKMONEPEOSNEDVICKISHUKAHK",
   "known_in_place": 24
  },
  {
   "group": "F1.4 skip",
   "setting": "B skip m=26 phi=3 n=21",
   "form": "V",
   "slots": 21,
   "above": 100,
   "copies_climbed": 100,
   "score": -4.97528,
   "copies_max": -5.02852,
   "reading": "CIASAZAHITLOBTAKEITTLEASTNORTHEASTADDROUCANDLWTEERSHKUONEORWREIBERLINCLOCKHISLEAPROWOFANGORLIKEHT",
   "known_in_place": 24
  },
  {
   "group": "F1.4 skip",
   "setting": "B skip m=14 phi=13 n=22",
   "form": "V",
   "slots": 22,
   "above": 100,
   "copies_climbed": 100,
   "score": -4.98248,
   "copies_max": -4.98791,
   "reading": "CINGIMCAECANBTANKIRANEASTNORTHEASTATTISCRAWBUEYSDISYALDEICALLHUBERLINCLOCKINDAYTHRONEDEHMMIAMACUT",
   "known_in_place": 24
  },
  {
   "group": "F1.4 skip",
   "setting": "B skip m=28 phi=27 n=21",
   "form": "V",
   "slots": 21,
   "above": 100,
   "copies_climbed": 100,
   "score": -5.00013,
   "copies_max": -5.05167,
   "reading": "UEJOONSHEMIEBTACUSANREASTNORTHEASTAICKGREDNUNHAPILOFALMIKEHAQEEBERLINCLOCKATTOREYEAREDSORIGITKSEW",
   "known_in_place": 24
  },
  {
   "group": "F1.4 skip",
   "setting": "B skip m=30 phi=29 n=21",
   "form": "V",
   "slots": 21,
   "above": 100,
   "copies_climbed": 100,
   "score": -5.00376,
   "copies_max": -5.07623,
   "reading": "AMYMPICEMSWEBTALURMATEASTNORTHEASTATASEBELFICETOBSGUALAMILITIEMBERLINCLOCKNDDEABDEURAKEDTOSWLKEIR",
   "known_in_place": 24
  },
  {
   "group": "F1.4 skip",
   "setting": "B skip m=13 phi=9 n=22",
   "form": "V",
   "slots": 22,
   "above": 100,
   "copies_climbed": 100,
   "score": -5.00725,
   "copies_max": -5.04117,
   "reading": "QNISTLYNABDWBTMIESTSSEASTNORTHEASTMOUSINARCADOGPREMUALEVEORSCANBERLINCLOCKINCREAMATGRUORIHEDPACHV",
   "known_in_place": 24
  },
  {
   "group": "F1.4 skip",
   "setting": "B skip m=24 phi=23 n=21",
   "form": "B",
   "slots": 21,
   "above": 100,
   "copies_climbed": 100,
   "score": -5.01072,
   "copies_max": -5.06148,
   "reading": "TOPHEEAMYNAYETABERSTBEASTNORTHEASTANAGEDISCRYJPEDMLIIRSWELHOSEOBERLINCLOCKEFLEIROTSOIFTMASMARIZOP",
   "known_in_place": 24
  },
  {
   "group": "F1.4 skip",
   "setting": "B skip m=14 phi=12 n=22",
   "form": "V",
   "slots": 22,
   "above": 100,
   "copies_climbed": 100,
   "score": -5.01159,
   "copies_max": -5.04038,
   "reading": "RAGEWHLWNGLOBTEUSICATEASTNORTHEASTENTRALSANIGEXSREAGALMOMOTALIABERLINCLOCKADALCEISUKKTEDBYEPRACKB",
   "known_in_place": 24
  },
  {
   "group": "F1.4 skip",
   "setting": "B skip m=22 phi=13 n=21",
   "form": "V",
   "slots": 21,
   "above": 100,
   "copies_climbed": 100,
   "score": -5.01367,
   "copies_max": -5.04253,
   "reading": "AUXSBETEBNDEBTITSETSBEASTNORTHEASTIGIVINVANAFORBAJDIAWRESINUTESBERLINCLOCKSOANDERLLEADFAMAUDSKOKS",
   "known_in_place": 24
  },
  {
   "group": "F1.4 skip",
   "setting": "B skip m=13 phi=8 n=22",
   "form": "V",
   "slots": 22,
   "above": 100,
   "copies_climbed": 100,
   "score": -5.0192,
   "copies_max": -5.03305,
   "reading": "YSDSGLAMIOFEBTHAMISCREASTNORTHEASTHENAPOTFORBPULUENZALORPNAHMESBERLINCLOCKFUNARICTANCEPEOFEGYACKT",
   "known_in_place": 24
  },
  {
   "group": "F1.4 skip",
   "setting": "B skip m=27 phi=24 n=21",
   "form": "V",
   "slots": 21,
   "above": 100,
   "copies_climbed": 100,
   "score": -5.02011,
   "copies_max": -5.22285,
   "reading": "AQHATIGHRODEBTERTAREDEASTNORTHEASTEWARGOLICYRFMCLERSALOSENTHEETBERLINCLOCKFOYELEBLMELPETEINDJKPMB",
   "known_in_place": 24
  },
  {
   "group": "F1.4 skip",
   "setting": "B skip m=8 phi=3 n=23",
   "form": "V",
   "slots": 23,
   "above": 100,
   "copies_climbed": 100,
   "score": -5.02556,
   "copies_max": -5.03587,
   "reading": "HSTSAPGEEATEBRITOREBREASTNORTHEASTNLADUSINDUTCLEMNIRANGEORIONYSBERLINCLOCKPLEFFITIONMICKOSNKPKFIA",
   "known_in_place": 24
  },
  {
   "group": "F1.4 skip",
   "setting": "B skip m=29 phi=5 n=21",
   "form": "V",
   "slots": 21,
   "above": 100,
   "copies_climbed": 100,
   "score": -5.03793,
   "copies_max": -5.15281,
   "reading": "GETHPWAGETAEBTFITSRIEEASTNORTHEASTFONOTMALOEDOODSUBSAMATTHATHEEBERLINCLOCKVETSEMEABOGAINKADARKGUF",
   "known_in_place": 24
  },
  {
   "group": "F1.4 skip",
   "setting": "B skip m=23 phi=15 n=21",
   "form": "V",
   "slots": 21,
   "above": 100,
   "copies_climbed": 100,
   "score": -5.04482,
   "copies_max": -5.1295,
   "reading": "CIFSSEYEPDCSBTEREITEBEASTNORTHEASTEAMEANAKURDYTMATHEALASEUNSTEMBERLINCLOCKEWSAYIRTSLAWWASENCOKUKW",
   "known_in_place": 24
  },
  {
   "group": "F1.4 skip",
   "setting": "B skip m=26 phi=23 n=21",
   "form": "V",
   "slots": 21,
   "above": 100,
   "copies_climbed": 100,
   "score": -5.04703,
   "copies_max": -5.08671,
   "reading": "CHFUSEARASSSBTOCATASDEASTNORTHEASTOSTJUNIFYARMHBALNHALIAACEFRELBERLINCLOCKSGAYACOPMEDEASSHESZKLAH",
   "known_in_place": 24
  },
  {
   "group": "F1.4 skip",
   "setting": "B skip m=27 phi=23 n=21",
   "form": "V",
   "slots": 21,
   "above": 100,
   "copies_climbed": 100,
   "score": -5.06336,
   "copies_max": -5.11995,
   "reading": "XLOSTRPBIMANBTENTERTMEASTNORTHEASTEORISHANJPLBAMILOSALBUDDLEGEDBERLINCLOCKAFTIMIFASEDOUTRAIAWKUTS",
   "known_in_place": 24
  },
  {
   "group": "F1.4 skip",
   "setting": "B skip m=27 phi=25 n=21",
   "form": "V",
   "slots": 21,
   "above": 100,
   "copies_climbed": 100,
   "score": -5.07843,
   "copies_max": -5.09408,
   "reading": "DHQUEETBOSYOBTEDONISTEASTNORTHEASTENDEALADJUSGRAYSKAALOKOMSWREDBERLINCLOCKLISMSECASIASTEEABYJKEYT",
   "known_in_place": 24
  },
  {
   "group": "F1.4 skip",
   "setting": "B skip m=26 phi=22 n=21",
   "form": "V",
   "slots": 21,
   "above": 100,
   "copies_climbed": 100,
   "score": -5.07901,
   "copies_max": -5.18191,
   "reading": "WRESBYFASSAMBTRINTUNTEASTNORTHEASTROTEBREWBNHUUSIQBYALLINGRELEMBERLINCLOCKEECARLYEGWYLEBRITASKNTL",
   "known_in_place": 24
  },
  {
   "group": "F1.4 skip",
   "setting": "B skip m=25 phi=1 n=21",
   "form": "V",
   "slots": 21,
   "above": 100,
   "copies_climbed": 100,
   "score": -5.09811,
   "copies_max": -5.12131,
   "reading": "RDTHASHZRCINBTSDIRENCEASTNORTHEASTSAWACREDJUDDETORYFKIDLITYPREDBERLINCLOCKINDEDOPHONYCOGMDRITKUPF",
   "known_in_place": 24
  },
  {
   "group": "F1.4 skip",
   "setting": "B skip m=29 phi=28 n=21",
   "form": "V",
   "slots": 21,
   "above": 100,
   "copies_climbed": 100,
   "score": -5.10379,
   "copies_max": -5.10473,
   "reading": "ULMDSFOFORKBBTILYSWAMEASTNORTHEASTITHASBEINNIHADEVSDALMEIOREHELBERLINCLOCKOFDEIIVEAYOWHISACKOKALR",
   "known_in_place": 24
  },
  {
   "group": "F1.4 skip",
   "setting": "B skip m=27 phi=5 n=21",
   "form": "V",
   "slots": 21,
   "above": 100,
   "copies_climbed": 100,
   "score": -5.10662,
   "copies_max": -5.12417,
   "reading": "GMRSOFEVORINBTHINGUSTEASTNORTHEASTHODDEVICENDYSPADJMKWYENORTOEMBERLINCLOCKDOFSTOUDALLPMREYDIRKLUG",
   "known_in_place": 24
  }
 ],
 "plants": {
  "clean_found": [
   8,
   12
  ],
  "sanborn_found": [
   9,
   12
  ],
  "null_per_plant": "1/13",
  "each": {
   "0": {
    "cls": "clean",
    "setting": "B skip m=30 phi=16 n=25",
    "form": "B",
    "found": false,
    "above": 2,
    "score": -4.90021,
    "letters_right": 40
   },
   "1": {
    "cls": "clean",
    "setting": "B skip m=20 phi=6 n=24",
    "form": "B",
    "found": true,
    "above": 12,
    "score": -4.87688,
    "letters_right": 36
   },
   "2": {
    "cls": "clean",
    "setting": "B skip m=28 phi=16 n=17",
    "form": "B",
    "found": true,
    "above": 12,
    "score": -5.1028,
    "letters_right": 62
   },
   "3": {
    "cls": "clean",
    "setting": "B skip m=19 phi=1 n=24",
    "form": "B",
    "found": false,
    "above": 11,
    "score": -4.92727,
    "letters_right": 31
   },
   "4": {
    "cls": "clean",
    "setting": "D back and forth n=23 ends=repeated phi=2",
    "form": "B",
    "found": true,
    "above": 12,
    "score": -4.85418,
    "letters_right": 34
   },
   "5": {
    "cls": "clean",
    "setting": "B skip m=22 phi=1 n=20",
    "form": "B",
    "found": true,
    "above": 12,
    "score": -5.03699,
    "letters_right": 38
   },
   "6": {
    "cls": "clean",
    "setting": "B skip m=15 phi=5 n=26",
    "form": "V",
    "found": false,
    "above": 11,
    "score": -4.85201,
    "letters_right": 30
   },
   "7": {
    "cls": "clean",
    "setting": "B skip m=10 phi=2 n=15",
    "form": "V",
    "found": true,
    "above": 12,
    "score": -5.54702,
    "letters_right": 44
   },
   "8": {
    "cls": "clean",
    "setting": "B skip m=28 phi=0 n=14",
    "form": "V",
    "found": true,
    "above": 12,
    "score": -5.8326,
    "letters_right": 46
   },
   "9": {
    "cls": "clean",
    "setting": "B skip m=21 phi=18 n=16",
    "form": "B",
    "found": true,
    "above": 12,
    "score": -5.1423,
    "letters_right": 38
   },
   "10": {
    "cls": "clean",
    "setting": "B skip m=12 phi=3 n=25",
    "form": "B",
    "found": false,
    "above": 1,
    "score": -4.91033,
    "letters_right": 37
   },
   "11": {
    "cls": "clean",
    "setting": "B skip m=11 phi=6 n=17",
    "form": "B",
    "found": true,
    "above": 12,
    "score": -5.25981,
    "letters_right": 33
   },
   "12": {
    "cls": "xstops",
    "setting": "B skip m=28 phi=17 n=24",
    "form": "B",
    "found": true,
    "above": 12,
    "score": -4.69266,
    "letters_right": 46
   },
   "13": {
    "cls": "xstops",
    "setting": "B skip m=24 phi=21 n=24",
    "form": "B",
    "found": false,
    "above": 10,
    "score": -4.88669,
    "letters_right": 44
   },
   "14": {
    "cls": "xstops",
    "setting": "B skip m=24 phi=20 n=16",
    "form": "B",
    "found": true,
    "above": 12,
    "score": -5.55542,
    "letters_right": 45
   },
   "15": {
    "cls": "xstops",
    "setting": "B skip m=28 phi=24 n=21",
    "form": "V",
    "found": true,
    "above": 12,
    "score": -5.09052,
    "letters_right": 34
   },
   "16": {
    "cls": "xstops",
    "setting": "B skip m=21 phi=8 n=24",
    "form": "B",
    "found": true,
    "above": 12,
    "score": -4.69109,
    "letters_right": 40
   },
   "17": {
    "cls": "xstops",
    "setting": "B skip m=11 phi=8 n=25",
    "form": "B",
    "found": true,
    "above": 12,
    "score": -4.73929,
    "letters_right": 35
   },
   "18": {
    "cls": "xstops",
    "setting": "B skip m=12 phi=1 n=25",
    "form": "B",
    "found": true,
    "above": 12,
    "score": -4.69432,
    "letters_right": 40
   },
   "19": {
    "cls": "xstops",
    "setting": "B skip m=28 phi=17 n=20",
    "form": "B",
    "found": true,
    "above": 12,
    "score": -4.96326,
    "letters_right": 39
   },
   "20": {
    "cls": "xstops",
    "setting": "B skip m=30 phi=12 n=14",
    "form": "V",
    "found": false,
    "above": 1,
    "score": -6.16821,
    "letters_right": 36
   },
   "21": {
    "cls": "xstops",
    "setting": "B skip m=28 phi=3 n=16",
    "form": "B",
    "found": true,
    "above": 12,
    "score": -5.30005,
    "letters_right": 40
   },
   "22": {
    "cls": "xstops",
    "setting": "B skip m=6 phi=1 n=19",
    "form": "B",
    "found": false,
    "above": 10,
    "score": -5.22187,
    "letters_right": 45
   },
   "23": {
    "cls": "xstops",
    "setting": "B skip m=25 phi=1 n=24",
    "form": "B",
    "found": true,
    "above": 12,
    "score": -4.88685,
    "letters_right": 41
   }
  }
 },
 "climbs": 21878,
 "core_seconds": 417051,
 "compute_seconds": 14471,
 "exhaustive": true,
 "exhaustive_over": "every setting of 0128's schedules (slot counts 2-31) K4 fits on one free alphabet, both forms; each decided at one-run power",
 "resumed_units": 0,
 "modal_cost_estimate": "about 45-60 core-hours on 32 cores, about $3-6 of Modal credit (credit left about $23 after the 10% margin)",
 "expected_total_time": "about 2,093 x (1 + 3.1) + 21 x 26 + 24 x 13 climbs, about 9,500 at about 17 core-s: about 45 core-hours, 2-3 h on 32 cores"
}
```

Notes: F1.4 one-alphabet residue: 2093 settings; K4 above all 12 copies in 299 (chance 161, p 1.12e-24), above all 100 in 66 (chance 20.7, p 1.25e-15); plants found clean [8, 12], Sanborn-style [9, 12]. No candidate returned: a per-setting reading above its own copies is expected about 161 times by chance, so gate 4 on one setting's copies would not account for the 2093 settings searched; the verdict is the count, and the top readings are in bounds.


