# 0267-f1.4-two-alphabet-residue-decided-by-four-runs-with-stand-ins: F1.4: every hand key schedule K4 fits on two free alphabets, each decided by D1b's four-run decider against kept-place copies one at a time, with 20 shuffled stand-ins through the same procedure

**Family:** 1-keyed-periodic  
**Parent:** 0253-f1.4-one-alphabet-residue-decided-by-the-one-run-decider  
**Decision:** reverted  
**Run:** 2026-11-04T09:28:11+00:00, 31943.3 s, status ran  
**Time by phase:** test 0 s, run 31943 s, record 0 s

## In plain words

Sanborn may have stepped through his key word with a twist (skipping a letter now and then, going back and forth) and used two scrambled alphabets of his own, one for the message and one for the cipher. About five thousand such twists agree with the 24 known letters, so those letters cannot tell them apart. For each one we search for the most English-looking reading of K4 and do the same on scrambled copies; to know what 'K4 wins often' means, twenty scrambled stand-ins for K4 go through the very same test.

## Walkthrough, by hand

1. Pick a schedule, say: a key of 11 letters, skip one key letter after every 7 carved letters.
2. Write the key slot under each of the 97 carved letters.
3. With two unknown alphabets, two known letters in one slot must satisfy C(c1) - P(p1) = C(c2) - P(p2); check that some pair of alphabets satisfies all of them.
4. Search alphabet pairs and keys for the most English-looking reading of K4, four times.
5. Shuffle the 73 letters at unknown places (the known places keep their carved letters, so step 3 still holds) and search the copy the same way; stop when a copy reads as well as K4, at most 12 copies.
6. Do steps 4-5 for every schedule, and for 20 shuffled stand-ins of K4; compare how often K4 wins all 12 with how often the stand-ins do.

## Worked example (generated)

```
F1.4: two free alphabets under a hand key schedule, decided setting by setting.

  setting      skip one key letter every 7 letters, 11 key letters
  slot map     place 1 2 3 4 5 6 7 8 9 ...
  key letter         1 2 3 4 5 6 8 9 10 ... (letter 7 skipped)
  cipher       C(carved) = P(plain) + key[slot], P and C two unknown alphabets

  K4 gets four tempering searches under that slot map; then copies that keep the carved letters at the 24 known
  places (so they fit the same checks) get the same, one at a time, until a copy reads as well as K4 (at most 12).
  20 shuffled stand-ins for K4 go through the same test: K4's rate of wins must stand out from theirs.
```

## Lineage

Inherits from 0253-f1.4-one-alphabet-residue-decided-by-the-one-run-decider. What changed: F1.4, the two-alphabet residue, which waited for D1b. 0253-0255 decided the one-alphabet residue (K4 inside 40 stand-ins, p 0.51). D1b (0257) qualified four runs of 0144's two-alphabet tempering (66 of 96 plants against ten runs' 71). Here 0144's climb is generalised to any slot map (the change 0252 made to 0140's), every 0128 schedule that fits K4 on two free alphabets (4,706 slot maps; the 1,346 in the record were distinct partitions of the 24 known places) is decided with it against kept-place copies climbed one at a time (stop at the first at or above K4, at most 12), and 20 stand-ins (K4 with its 73 unknown places shuffled, so the same settings fit) go through the same procedure on 60 settings each: the verdict is K4's rate against theirs (0254's lesson).

## Hypothesis (domain expert)

F1.4: a keyed table with a hand key schedule (C20(d): tableau rows as keys; 0126-0128's schedules: a key letter skipped every m letters, stutter, back and forth, triangle, square, a restart per carved line), on two free alphabets (Quagmire IV with unknown orders: Sanborn's 'slightly different' tableau on both sides, C27(c)). The added and Beaufort forms are one on two free alphabets (reverse the cipher alphabet). 0128 found the fitting settings at the copies' rate, so the 24 known letters cannot decide them and English must. Decider: D1b's four runs of 0144's tempering (16 x 625 x 1000) from the exact witness (0128's two-alphabet decider), patched only to read the key slot of each carved letter from the schedule; self-checked against 0144's library on periodic slot maps. Copies keep the carved letters at the 24 known places (same equations, same freedom; 0143, 0257). Clue entries: C20(d), C27(c), C5(a).

## Prediction

K4's rate of settings above all 12 copies inside the 20 stand-ins' spread (p above 0.05); plants (24, on settings K4 fits) found above all 12 own copies about 14 of 24; no reading English. Zero candidates.

## Method

1. Settings: 0252's f14_settings() (every 0128 schedule at every slot count 2-31, deduplicated); each decided on K4 by 0128's exact two-alphabet decider; the fitting ones are the cell (undecided ones counted).
2. Per setting (one job, own seed): K4 climbed with four runs of the generalised tempering from the exact witness; then kept-place copies (the 73 unknown places shuffled) climbed the same way one at a time, stopping at the first at or above K4, at most 12.
3. Stand-ins: 20 kept-place shuffles of K4 (seed 2630), each decided the same way on 60 settings drawn from the cell.
4. Plants: 12 clean and 12 Sanborn-style messages on settings drawn from the cell, two random alphabets and key; found if above all 12 own copies.
5. Verdict: K4's share of settings above all 12 copies, ranked among the stand-ins' shares.

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
 "item": "F1.4 (two free alphabets residue, after D1b)",
 "decider": "D1b's four-run decider: 4 runs of 0144's tempering (16 x 625 x 1000) generalised to any slot map, from 0128's exact two-alphabet witness; copies keep the carved letters at the 24 known places and shuffle the other 73, climbed one at a time, stop at the first at or above, at most 12",
 "self_check_against_0144": [
  [
   13,
   -5.2623,
   -5.2623
  ],
  [
   16,
   -4.89183,
   -4.89183
  ]
 ],
 "settings_listed": 12640,
 "decider_status": {
  "dead": 7933,
  "fit": 4706,
  "undecided": 1
 },
 "k4_fitting_settings": 4706,
 "k4_above_all_12": 363,
 "k4_rate": 0.0771,
 "chance_if_independent": 0.0769,
 "stand_ins": {
  "n": 20,
  "settings_each": 60,
  "rates": {
   "s0": 0.0667,
   "s1": 0.0167,
   "s2": 0.1333,
   "s3": 0.0333,
   "s4": 0.05,
   "s5": 0.05,
   "s6": 0.05,
   "s7": 0.0333,
   "s8": 0.0667,
   "s9": 0.0,
   "s10": 0.1167,
   "s11": 0.05,
   "s12": 0.0167,
   "s13": 0.0833,
   "s14": 0.1,
   "s15": 0.1,
   "s16": 0.15,
   "s17": 0.1,
   "s18": 0.0833,
   "s19": 0.0333
  },
  "at_or_above_k4": 8,
  "p": 0.4286,
  "how": "K4 with its 73 unknown places shuffled (seed 2631): the same 24 checks, so every setting fits; each decided as K4 on 60 settings drawn from the cell"
 },
 "top_settings": [
  {
   "setting": "D back and forth n=25 ends=once phi=16",
   "slots": 25,
   "above": 12,
   "score": -4.24547,
   "copies_max": -4.26944,
   "reading": "GRUSEINALLERSWAYSPEAREASTNORTHEASTRUCTOFAPETECTSANDMORENTELYTOTBERLINCLOCKENEADSORPIONTHEATDECKMC",
   "known_in_place": 24
  },
  {
   "setting": "B skip m=26 phi=5 n=26",
   "slots": 26,
   "above": 12,
   "score": -4.27159,
   "copies_max": -4.34119,
   "reading": "ONATOANYOGATROLLOMASNEASTNORTHEASTERSTRATEOVERATEADDAMONGTUNTERBERLINCLOCKETRAINSTCANDYNAGESWITHP",
   "known_in_place": 24
  },
  {
   "setting": "D back and forth n=24 ends=repeated phi=14",
   "slots": 24,
   "above": 12,
   "score": -4.27178,
   "copies_max": -4.39052,
   "reading": "NATYPROSSASINERSTHASPEASTNORTHEASTHEEYELYOUGROUSECOMEANDANDAEREBERLINCLOCKEDASTTERNOVESINGEBROWIU",
   "known_in_place": 24
  },
  {
   "setting": "B skip m=27 phi=7 n=26",
   "slots": 26,
   "above": 12,
   "score": -4.27658,
   "copies_max": -4.29856,
   "reading": "GNATTHEFLOSVEGIONNELREASTNORTHEASTHEENPRICHARRITENEWAITTHEENOREBERLINCLOCKMAMANORITANANDINMARIEBA",
   "known_in_place": 24
  },
  {
   "setting": "D back and forth n=25 ends=once phi=19",
   "slots": 25,
   "above": 12,
   "score": -4.27664,
   "copies_max": -4.32315,
   "reading": "URINTONSHWARAGEDRETHEEASTNORTHEASTHICKOVETATRASSESERORTOSSENTEMBERLINCLOCKENSUPONANDENTUNSFORAILM",
   "known_in_place": 24
  },
  {
   "setting": "B skip m=7 phi=4 n=26",
   "slots": 26,
   "above": 12,
   "score": -4.27748,
   "copies_max": -4.27917,
   "reading": "IBEREMALLEARLEASICSTREASTNORTHEASTHEROESORGERALLYAVEWITDICATERBBERLINCLOCKEEMALSEDITIONEVIETHETWT",
   "known_in_place": 24
  },
  {
   "setting": "B skip m=26 phi=17 n=25",
   "slots": 25,
   "above": 12,
   "score": -4.28533,
   "copies_max": -4.32642,
   "reading": "OLIONTASANDSIMPERISEMEASTNORTHEASTARELLCONTOTALEDBEELIMIWOUNDEDBERLINCLOCKSTENTFORMYGCALSHOUTABLE",
   "known_in_place": 24
  },
  {
   "setting": "B skip m=20 phi=10 n=26",
   "slots": 26,
   "above": 12,
   "score": -4.29819,
   "copies_max": -4.3191,
   "reading": "OWITERVEDINALWASCHALLEASTNORTHEASTHERPICHENDATLERETHAVESOLANAOLBERLINCLOCKTHEAMBYSPONSHERKISEDAYS",
   "known_in_place": 24
  },
  {
   "setting": "B skip m=17 phi=11 n=24",
   "slots": 24,
   "above": 12,
   "score": -4.29843,
   "copies_max": -4.36117,
   "reading": "RYAUGASTHECOANDEIVERDEASTNORTHEASTHETERTYTHIBALLATWORSETIOTTCOMBERLINCLOCKLEFORBEANSITISTATEDHEST",
   "known_in_place": 24
  },
  {
   "setting": "D back and forth n=25 ends=once phi=6",
   "slots": 25,
   "above": 12,
   "score": -4.2985,
   "copies_max": -4.33424,
   "reading": "RDWITHINLYESORPORATUBEASTNORTHEASTINEMSSTOMPORTTESTERMATIMSELONBERLINCLOCKSTEETODEHITEDTHEREOROFF",
   "known_in_place": 24
  },
  {
   "setting": "D back and forth n=24 ends=once phi=4",
   "slots": 24,
   "above": 12,
   "score": -4.29965,
   "copies_max": -4.32446,
   "reading": "SONDANTHEMOVEMPATEOFSEASTNORTHEASTICABICIAGOSPAYANDSENGEEANCELIBERLINCLOCKWASAMEDISTHEVERENGERSNM",
   "known_in_place": 24
  },
  {
   "setting": "B skip m=24 phi=2 n=26",
   "slots": 26,
   "above": 12,
   "score": -4.30112,
   "copies_max": -4.33595,
   "reading": "RDETERWAYSDESTOFFRETHEASTNORTHEASTHARTUKARLDAVERANTHEYELEMENTASBERLINCLOCKIECENATHEINGSBRANETODRS",
   "known_in_place": 24
  },
  {
   "setting": "B skip m=11 phi=9 n=26",
   "slots": 26,
   "above": 12,
   "score": -4.30135,
   "copies_max": -4.30487,
   "reading": "VEINARSTRESMINTHADTOBEASTNORTHEASTTOTHETREPAMILENININDTHEWINGOLBERLINCLOCKTOSEWNSILLPLAYISRELIODI",
   "known_in_place": 24
  },
  {
   "setting": "D back and forth n=24 ends=once phi=8",
   "slots": 24,
   "above": 12,
   "score": -4.30148,
   "copies_max": -4.38667,
   "reading": "YOISPUBLITHESSHEARSATEASTNORTHEASTTOFORBITITWARESTITHERMITIVEITBERLINCLOCKSALANDEATCTHEMABEGOINTF",
   "known_in_place": 24
  },
  {
   "setting": "B skip m=18 phi=12 n=24",
   "slots": 24,
   "above": 12,
   "score": -4.30306,
   "copies_max": -4.34748,
   "reading": "VESERINSTORAMANYSLACTEASTNORTHEASTTOTHANARANSPULLEDETTHEAMFOREDBERLINCLOCKISMAGEOPLESRETEDMATSCET",
   "known_in_place": 24
  },
  {
   "setting": "B skip m=2 phi=0 n=26",
   "slots": 26,
   "above": 12,
   "score": -4.30508,
   "copies_max": -4.34813,
   "reading": "ZAOVEDINANELYTHESTAALEASTNORTHEASTININGWITRENONPERFROTEASOURSAMBERLINCLOCKYLEDFOREINNEDEFELEAMERJ",
   "known_in_place": 24
  },
  {
   "setting": "B skip m=20 phi=13 n=26",
   "slots": 26,
   "above": 12,
   "score": -4.30578,
   "copies_max": -4.30967,
   "reading": "PEITSNUTLECANINDASTOREASTNORTHEASTHETALLEVEDWELLICTHADAPLEATIONBERLINCLOCKONRANTHEGOTOPERSEMEMMRL",
   "known_in_place": 24
  },
  {
   "setting": "B skip m=30 phi=9 n=25",
   "slots": 25,
   "above": 12,
   "score": -4.31074,
   "copies_max": -4.36858,
   "reading": "SHCONDSLIPSTOSTENDANTEASTNORTHEASTREATLISHECHILEALEFOUTEVALWHOSBERLINCLOCKONSONSOFILLINDMETOHIGHS",
   "known_in_place": 24
  },
  {
   "setting": "B skip m=10 phi=5 n=24",
   "slots": 24,
   "above": 12,
   "score": -4.31078,
   "copies_max": -4.34612,
   "reading": "GOALAGREENOFOSTINENCREASTNORTHEASTYPERUTTHITWAYORDSITEOFTREAVENBERLINCLOCKSINBALLSINSTOMESHANTEDC",
   "known_in_place": 24
  },
  {
   "setting": "D back and forth n=25 ends=once phi=8",
   "slots": 25,
   "above": 12,
   "score": -4.31985,
   "copies_max": -4.32358,
   "reading": "YTOISASTORMOGAPONEALLEASTNORTHEASTOUGHORSORIATEANDRYCONOMISTAMABERLINCLOCKESEELSENTISMANANDEATTIC",
   "known_in_place": 24
  }
 ],
 "plants": {
  "clean_found": [
   8,
   12
  ],
  "sanborn_found": [
   4,
   12
  ],
  "null_per_plant": "1/13",
  "each": {
   "0": {
    "cls": "clean",
    "setting": "B skip m=26 phi=18 n=8",
    "found": true,
    "above": 12,
    "score": -4.87147,
    "letters_right": 48
   },
   "1": {
    "cls": "clean",
    "setting": "B skip m=9 phi=0 n=23",
    "found": false,
    "above": 10,
    "score": -4.41639,
    "letters_right": 36
   },
   "2": {
    "cls": "clean",
    "setting": "B skip m=16 phi=15 n=19",
    "found": false,
    "above": 1,
    "score": -4.47262,
    "letters_right": 38
   },
   "3": {
    "cls": "clean",
    "setting": "B skip m=28 phi=19 n=19",
    "found": true,
    "above": 12,
    "score": -4.36386,
    "letters_right": 45
   },
   "4": {
    "cls": "clean",
    "setting": "B skip m=19 phi=5 n=26",
    "found": false,
    "above": 4,
    "score": -4.28469,
    "letters_right": 33
   },
   "5": {
    "cls": "clean",
    "setting": "B skip m=13 phi=10 n=13",
    "found": true,
    "above": 12,
    "score": -4.63294,
    "letters_right": 42
   },
   "6": {
    "cls": "clean",
    "setting": "B skip m=25 phi=7 n=12",
    "found": true,
    "above": 12,
    "score": -4.82042,
    "letters_right": 37
   },
   "7": {
    "cls": "clean",
    "setting": "B skip m=17 phi=7 n=20",
    "found": false,
    "above": 11,
    "score": -4.44795,
    "letters_right": 30
   },
   "8": {
    "cls": "clean",
    "setting": "B skip m=25 phi=12 n=8",
    "found": true,
    "above": 12,
    "score": -5.03408,
    "letters_right": 47
   },
   "9": {
    "cls": "clean",
    "setting": "B skip m=17 phi=3 n=14",
    "found": true,
    "above": 12,
    "score": -4.55837,
    "letters_right": 31
   },
   "10": {
    "cls": "clean",
    "setting": "B skip m=29 phi=6 n=12",
    "found": true,
    "above": 12,
    "score": -4.81209,
    "letters_right": 38
   },
   "11": {
    "cls": "clean",
    "setting": "B skip m=21 phi=3 n=14",
    "found": true,
    "above": 12,
    "score": -4.63822,
    "letters_right": 38
   },
   "12": {
    "cls": "xstops",
    "setting": "B skip m=28 phi=11 n=12",
    "found": true,
    "above": 12,
    "score": -4.64002,
    "letters_right": 40
   },
   "13": {
    "cls": "xstops",
    "setting": "B skip m=30 phi=18 n=21",
    "found": false,
    "above": 0,
    "score": -4.51065,
    "letters_right": 37
   },
   "14": {
    "cls": "xstops",
    "setting": "B skip m=27 phi=3 n=24",
    "found": false,
    "above": 7,
    "score": -4.33127,
    "letters_right": 33
   },
   "15": {
    "cls": "xstops",
    "setting": "B skip m=11 phi=0 n=26",
    "found": false,
    "above": 2,
    "score": -4.28149,
    "letters_right": 34
   },
   "16": {
    "cls": "xstops",
    "setting": "B skip m=26 phi=2 n=17",
    "found": true,
    "above": 12,
    "score": -4.32137,
    "letters_right": 42
   },
   "17": {
    "cls": "xstops",
    "setting": "B skip m=27 phi=22 n=20",
    "found": false,
    "above": 0,
    "score": -4.51671,
    "letters_right": 30
   },
   "18": {
    "cls": "xstops",
    "setting": "B skip m=27 phi=22 n=25",
    "found": false,
    "above": 1,
    "score": -4.3689,
    "letters_right": 32
   },
   "19": {
    "cls": "xstops",
    "setting": "B skip m=22 phi=0 n=21",
    "found": false,
    "above": 0,
    "score": -4.51402,
    "letters_right": 30
   },
   "20": {
    "cls": "xstops",
    "setting": "B skip m=23 phi=22 n=26",
    "found": true,
    "above": 12,
    "score": -4.2623,
    "letters_right": 34
   },
   "21": {
    "cls": "xstops",
    "setting": "B skip m=3 phi=1 n=21",
    "found": true,
    "above": 12,
    "score": -4.38733,
    "letters_right": 33
   },
   "22": {
    "cls": "xstops",
    "setting": "B skip m=27 phi=2 n=12",
    "found": false,
    "above": 3,
    "score": -4.72678,
    "letters_right": 39
   },
   "23": {
    "cls": "xstops",
    "setting": "D back and forth n=15 ends=repeated phi=0",
    "found": false,
    "above": 4,
    "score": -4.62644,
    "letters_right": 35
   }
  }
 },
 "climbs": 24309,
 "runs_per_climb": 4,
 "core_seconds": 1788075,
 "compute_seconds": 31891,
 "exhaustive": true,
 "exhaustive_over": "every setting of 0128's schedules (slot counts 2-31) K4 fits on two free alphabets; each decided at D1b's four-run power",
 "resumed_units": 821,
 "cost_estimate": "4,706 settings (desk count 2026-10-30; the 1,346 in the record counted distinct partitions of the 24 known places, 0127/0128, not slot maps over all 97 places, which is what a climb reads) x about 16.4 runs (4 for K4 plus about 3.1 copies of 4, H_12) plus 20 x 60 stand-in settings and 24 plants: about 98,000 tempering runs at 12-15 core-s (desk timing on the loaded laptop, 12.2 s): about 330-410 core-hours; about $5.6 on Modal, above the credit left, so on the laptop: several days"
}
```

Notes: F1.4 two-alphabet residue: 4706 settings; K4 above all 12 kept-place copies in 363 (7.7%); 20 stand-ins 0.0-15.0%, 8 at or above K4 (p 0.43); plants clean [8, 12], Sanborn-style [4, 12].


