# 0137-free-alphabet-climb-that-keeps-the-known-letters: F1.5 design 1: a climb that never breaks the 24 known letters, run in compiled code, measured on planted English before K4 (one free alphabet, Beaufort form, key lengths 23 and 26)

**Family:** 1-keyed-periodic  
**Parent:** 0120-one-free-alphabet-english-climb-at-23-and-26  
**Decision:** reverted  
**Run:** 2026-10-16T17:13:42+00:00, 725.7 s, status ran  
**Time by phase:** test 20 s, run 726 s, record 41 s

## In plain words

For one kind of cipher (one scrambled alphabet, a repeating key of 23 or 26 letters, used the Beaufort way), the 24 known letters cannot rule the carved text in or out, but 73 letters of English could, in principle. An earlier search failed to find hidden English of this kind even when we planted it ourselves. This search only ever moves between settings that keep the 24 known letters right, reads the whole message including the known words, and runs about 150 times faster, so it can try 1,000 fresh starts per text. Before believing what it says about the carved text, we check how often it notices planted messages compared with scrambled copies.

## Walkthrough, by hand

1. Write K4 in rows of 23; each column is one key slot.
2. Choose an order for the alphabet that keeps the known letters consistent: in every column holding two known letters, place(carved) + place(known) must come out the same for both.
3. The key value of a column with a known letter is that sum; give the other six columns any value.
4. Decipher every letter: message place = key value minus carved place, mod 26, read back through the alphabet.
5. Score the whole 97 letters, known words included, by how English their four-letter groups are.
6. Swap two letters of the alphabet; if a column's two known letters now disagree, swap another pair that makes every column agree again.
7. Keep the change if the score improves (sometimes even if not, less often as the search cools); repeat 100,000 times, then start again from a new order, 1,000 times.
8. Do the same on scrambled copies of K4 and on planted English, and compare the best scores.

## Worked example (generated)

```
key length 23, Beaufort form: K4 in rows of 23; each column is one key slot

  O B K R U O X O G H U L B S O L I F B B W F L
  R V Q Q P R N G K S S O T W T Q S J Q S S E K
  Z Z W A T J K L U D I A W I N F B N Y P V T T
  M Z F P K W G D K Z X T J C D I G K U H U A U
  E K C A R

the seven checks every move keeps (place(carved) + place(known) equal within a column):
  column 0: R+S (24) = M+C (70)
  column 1: V+T (25) = Z+L (71)
  column 2: Q+N (26) = F+O (72)
  column 3: Q+O (27) = P+C (73)
  column 4: P+R (28) = K+K (74)
  column 21: F+E (22) = T+I (68)
  column 22: L+A (23) = T+N (69)

best alphabet on K4: UWOXMQNVLFISRKPAZTECJDGYBH
key values: [23, 24, 11, 7, 0, 3, 5, 14, 2, 22, 2, 1, 9, 25, 17, 20, 2, 4, 15, 0, 15, 1, 23]
place 22: carved F at 9, key 1: 1 - 9 = 18 -> E
place 64: carved N at 6, key 4: 4 - 6 = 24 -> B
```

## Lineage

Inherits from 0120-one-free-alphabet-english-climb-at-23-and-26. What changed: F1.5, step 2, design 1, on F1.1's two cells (Beaufort form, key lengths 23 and 26), which 0136 showed decidable by the quadgram test in principle (open bits 75 and 90 against 130). Three changes to 0120's climb: (1) every move keeps the 24 known letters consistent (swap two letters' places; if a check breaks, repair with a second swap chosen among those that restore every check), so no penalty term and the forced key values move only as the checks allow; (2) the score is the quadgram mean over all 97 letters with the known letters in place, so the unknown letters next to the known runs are scored in context; (3) the inner loop is compiled C (written out and compiled by this file, loaded with ctypes; about 150 times faster than 0120's Python), so each text gets 1,000 restarts of 100,000 moves instead of 20. Power is measured on 12 planted texts per length before K4's verdict counts.

## Hypothesis (domain expert)

C27(c) (a tableau 'slightly different from the one on Kryptos', research_notes/sanborn_charts and the NYT 'Original Decoding Charts' email, knowledge/11-clue-register.md), C1(b) (the table alone). Model as 0120: one unknown bijection x (letter -> place) on both sides, Beaufort form x(c_i) + x(p_i) = k[i mod L] mod 26, L in {23, 26}; 0119 left only these (form, length) pairs. Given x, the key at a slot holding a known letter is forced; the other slots (6 at 23, 3 at 26) are free. Checks: 7 at L 23 (x(c1)+x(p1) = x(c2)+x(p2) for two known letters in a slot), 1 at L 26. Search: simulated annealing over x restricted to the set where every check holds (start: a random depth-first assignment that satisfies the checks; move: swap two letters' places, repaired by a second swap if a check breaks) and over the free key values; objective the mean log10 quadgram over the whole 97-letter text with the known letters in place; T 0.05 -> 0.002 geometric; 1,000 restarts x 100,000 moves per text. Dry runs on planted texts before this record (scratch, stated here): started from the true alphabet with k random check-keeping swaps (free key values true), the climb returned to the exact plaintext for k up to about 12 and rarely from 15-20; from random starts no restart of 960 (100,000 or 1,000,000 moves) recovered a plant, the best reaching -4.85 to -5.0 against true scores of -4.1 to -4.4, with 11-16 of the 73 unknown letters right. Bar, set before the run, stricter than 0120's half because 0120's 3 of 6 at that bar was judged weak: a plant is found if its best score is above every copper's best at that length; the design passes at a length if at least 9 of 12 plants are found. Recovery (90 or more of 97 letters right) is reported apart. Key cost of a reading here: 88.4 bits of alphabet plus 4.7 per key letter.

## Prediction

No planted text recovered (90+ letters right) at either length, as in the dry runs. Detection only through the partial correctness the dry runs showed: at 23, fewer than 9 of 12 plants above every copper, so the design fails the bar; at 26 (one check) fewer still. K4 inside its coppers' range at both lengths. If a length reaches 9 of 12, that length's K4 verdict counts as sampled at the measured power, and a K4 score above every copper stops the queue for a replication.

## Method

1. Compile the C climb; check on a planted text that its plaintext equals a Python Beaufort decryption under the alphabet and key it returns.
2. Draw 12 shuffles of K4 that fit exactly at each length (0119's decider) and 12 planted texts per length (Carter windows, known letters written in, random alphabet and key; 0120's generator).
3. For K4, each copper and each plant: 1,000 restarts x 100,000 moves, best score kept, restarts done recorded.
4. Per length: plants found (above every copper), plants recovered, K4 against the coppers.
5. Return K4's best reading per length as a candidate with the coppers' scores as controls.

## Result

Candidates returned: 2. Passed all gates: 0. Best crib hits among all candidates: 24/24
(EAST 4/4, NORTHEAST 9/9, BERLIN 6/6, CLOCK 5/5).
Best loss: 4.12173839979672 (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | baseline | 24/24 | -7.460 | `DUBDUWORNYOCSPAREDTOPEASTNORTHEASTHEBUATIIAMFIVLIEFFENOWERLASSMBERLINCLOCKOFCANHIANGINTAWARYQSEEP` | Beaufort form, one alphabet UWOXMQNVLFISRKPAZTECJDGYBH on both sides, key length 23 |
| 2 | baseline | 24/24 | -7.408 | `QEVEDENGETOPTOANHEANGEASTNORTHEASTCHERIONYMNSVAGIEVELMAFTKALLYSBERLINCLOCKINMCUARLOTBORGJANGEREDW` | Beaufort form, one alphabet AKDPGNBMLEVURJIXHQOFWCYSZT on both sides, key length 26 |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "one unknown alphabet on both sides, Beaufort form, periodic key 23 or 26, no move (F1.1's two cells)",
 "search": "simulated annealing in the set where every known-letter check holds, compiled C, 1000 restarts x 100,000 moves per text (chunks of 50), T 0.05->0.002 geometric, full-text quadgram mean",
 "not_exhaustive": true,
 "restarts_done": {
  "min": 1000,
  "max": 1000
 },
 "c_decryption_checked": true,
 "bar": "plant found if its best score is above every copper's best; design passes at a length if >= 9 of 12 found",
 "coppers_per_length": 12,
 "plants_per_length": 12,
 "summary": {
  "23": {
   "k4": -5.0497,
   "coppers_min": -5.1297,
   "coppers_max": -4.9412,
   "k4_rank_among_coppers": 9,
   "k4_above_all_coppers": false,
   "plants_found": 10,
   "plants_recovered": 0,
   "passes_bar": true,
   "plants_scores": [
    -4.969,
    -4.9442,
    -4.9295,
    -4.8887,
    -4.848,
    -4.8398,
    -4.7927,
    -4.7407,
    -4.735,
    -4.7303,
    -4.7265,
    -4.7234
   ],
   "plants_true_scores": [
    -4.5553,
    -4.4331,
    -4.2901,
    -4.2829,
    -4.2819,
    -4.266,
    -4.2339,
    -4.2169,
    -4.2098,
    -4.1888,
    -4.1627,
    -4.0994
   ],
   "plants_letters_right": [
    42,
    34,
    45,
    37,
    39,
    38,
    36,
    34,
    36,
    37,
    36,
    39
   ]
  },
  "26": {
   "k4": -4.9538,
   "coppers_min": -5.1355,
   "coppers_max": -4.7089,
   "k4_rank_among_coppers": 12,
   "k4_above_all_coppers": false,
   "plants_found": 5,
   "plants_recovered": 0,
   "passes_bar": false,
   "plants_scores": [
    -4.8361,
    -4.8191,
    -4.8053,
    -4.7666,
    -4.766,
    -4.7587,
    -4.7133,
    -4.7088,
    -4.6874,
    -4.662,
    -4.6499,
    -4.5894
   ],
   "plants_true_scores": [
    -4.4538,
    -4.4364,
    -4.4229,
    -4.4022,
    -4.3379,
    -4.2946,
    -4.2804,
    -4.2797,
    -4.2214,
    -4.181,
    -4.0682,
    -3.9617
   ],
   "plants_letters_right": [
    36,
    34,
    35,
    34,
    38,
    31,
    37,
    31,
    36,
    31,
    37,
    40
   ]
  }
 },
 "coppers": {
  "23": [
   -5.1297,
   -5.1221,
   -5.0693,
   -5.0532,
   -5.0309,
   -5.0295,
   -5.0268,
   -5.013,
   -4.9936,
   -4.9586,
   -4.9427,
   -4.9412
  ],
  "26": [
   -5.1355,
   -4.922,
   -4.9031,
   -4.8531,
   -4.814,
   -4.8049,
   -4.8043,
   -4.8027,
   -4.8003,
   -4.7331,
   -4.7275,
   -4.7089
  ]
 },
 "k4_best": {
  "23": {
   "score": -5.0497,
   "english_free": -5.4134,
   "restarts": 1000,
   "plaintext": "DUBDUWORNYOCSPAREDTOPEASTNORTHEASTHEBUATIIAMFIVLIEFFENOWERLASSMBERLINCLOCKOFCANHIANGINTAWARYQSEEP",
   "alphabet": "UWOXMQNVLFISRKPAZTECJDGYBH",
   "key": [
    23,
    24,
    11,
    7,
    0,
    3,
    5,
    14,
    2,
    22,
    2,
    1,
    9,
    25,
    17,
    20,
    2,
    4,
    15,
    0,
    15,
    1,
    23
   ]
  },
  "26": {
   "score": -4.9538,
   "english_free": -5.2167,
   "restarts": 1000,
   "plaintext": "QEVEDENGETOPTOANHEANGEASTNORTHEASTCHERIONYMNSVAGIEVELMAFTKALLYSBERLINCLOCKINMCUARLOTBORGJANGEREDW",
   "alphabet": "AKDPGNBMLEVURJIXHQOFWCYSZT",
   "key": [
    9,
    15,
    11,
    21,
    13,
    1,
    20,
    22,
    13,
    15,
    3,
    11,
    5,
    15,
    18,
    13,
    4,
    2,
    6,
    11,
    24,
    2,
    8,
    9,
    9,
    22
   ]
  }
 },
 "plants": {
  "23": [
   {
    "score": -4.7927,
    "english_free": -5.0237,
    "restarts": 1000,
    "letters_right": 42,
    "true_score": -4.2098,
    "plaintext": "INLTFPWOROSEELISPENISEASTNORTHEASTISHINGASEACETHEBATBYESSIRETWOBERLINCLOCKTOPLSSENJOATERASLMYINGH",
    "found": true,
    "recovered": false
   },
   {
    "score": -4.7303,
    "english_free": -4.9521,
    "restarts": 1000,
    "letters_right": 34,
    "true_score": -4.1888,
    "plaintext": "PMHISGARANMENDARREMLLEASTNORTHEASTAGERSETITYFUMMTOWHALLGIUNSHREBERLINCLOCKINDTHARDCORETLYWEIRMAJT",
    "found": true,
    "recovered": false
   },
   {
    "score": -4.735,
    "english_free": -4.8218,
    "restarts": 1000,
    "letters_right": 45,
    "true_score": -4.0994,
    "plaintext": "OHEHASANSESHINGERGYCAEASTNORTHEASTOSODINCURIAFTHEDATEROUNELINOCBERLINCLOCKRYONUSSUPIESTOFIKYWINAS",
    "found": true,
    "recovered": false
   },
   {
    "score": -4.9295,
    "english_free": -5.2683,
    "restarts": 1000,
    "letters_right": 37,
    "true_score": -4.2901,
    "plaintext": "LORYDDKNEPSSENTOFAMIBEASTNORTHEASTHANOFEIGHTHUMMNDFEEWSHINTCAVEBERLINCLOCKBONWADOCADAMMITEDELINYM",
    "found": true,
    "recovered": false
   },
   {
    "score": -4.8887,
    "english_free": -5.1359,
    "restarts": 1000,
    "letters_right": 39,
    "true_score": -4.2169,
    "plaintext": "PAZUQUAPEKAVALINWANTREASTNORTHEASTASTEDLINKOOKEEEDIDABLISTANKLYBERLINCLOCKNELIHISNUCOOKEDCIOSTOMI",
    "found": true,
    "recovered": false
   },
   {
    "score": -4.969,
    "english_free": -5.1992,
    "restarts": 1000,
    "letters_right": 38,
    "true_score": -4.4331,
    "plaintext": "ZSEMRELOGGEDROLOILNGEEASTNORTHEASTEFALSHIGCCCMSANALORALYECOSTERBERLINCLOCKSTPOUDMISALCONKERSICECA",
    "found": false,
    "recovered": false
   },
   {
    "score": -4.7234,
    "english_free": -4.9186,
    "restarts": 1000,
    "letters_right": 36,
    "true_score": -4.266,
    "plaintext": "GEHRMEHEATTESITOOMCHTEASTNORTHEASTTHEMELEMEDIGATHGATIOINFADEANDBERLINCLOCKNACCIONHOUSTAYHEEDLPCDI",
    "found": true,
    "recovered": false
   },
   {
    "score": -4.7407,
    "english_free": -4.9706,
    "restarts": 1000,
    "letters_right": 34,
    "true_score": -4.5553,
    "plaintext": "TCATOLIFSTICAAWSONADREASTNORTHEASTSHORNSFOREEROPORYTHEGITEDHEETBERLINCLOCKNSAYPEPILEUSTBAHALTORYT",
    "found": true,
    "recovered": false
   },
   {
    "score": -4.8398,
    "english_free": -5.0248,
    "restarts": 1000,
    "letters_right": 36,
    "true_score": -4.2829,
    "plaintext": "MEIRAHSHORSHANSEVEINNEASTNORTHEASTORMERONTABYFRECASEYOIICSESCARBERLINCLOCKCKPITTHIPRISRUNGTMATHHU",
    "found": true,
    "recovered": false
   },
   {
    "score": -4.848,
    "english_free": -5.0511,
    "restarts": 1000,
    "letters_right": 37,
    "true_score": -4.2819,
    "plaintext": "GTALMALLETHRODESTCSHEEASTNORTHEASTGERSQUIOREBESETELTELFNORUCESUBERLINCLOCKHDUDITINCEDFOXESPILAIRD",
    "found": true,
    "recovered": false
   },
   {
    "score": -4.7265,
    "english_free": -4.9193,
    "restarts": 1000,
    "letters_right": 36,
    "true_score": -4.1627,
    "plaintext": "VMULTHTHRNRILYIEMIENCEASTNORTHEASTEDINEACTHADGUNUNDEACATEADEMEMBERLINCLOCKOTHEYRERSENRBANKNOFFRBR",
    "found": true,
    "recovered": false
   },
   {
    "score": -4.9442,
    "english_free": -5.1568,
    "restarts": 1000,
    "letters_right": 39,
    "true_score": -4.2339,
    "plaintext": "NPADORYRIAHEREMWASPHYEASTNORTHEASTTHSKEDIIALOPPITHINGRILEDGISADBERLINCLOCKHDOCUNTPLACTSOGGHADERHO",
    "found": false,
    "recovered": false
   }
  ],
  "26": [
   {
    "score": -4.7666,
    "english_free": -5.0788,
    "restarts": 1000,
    "letters_right": 36,
    "true_score": -4.4229,
    "plaintext": "OCHUPWARETHEORCOGAORHEASTNORTHEASTRIRIKETOYERYADEINANSIDEVENIGMBERLINCLOCKHOFHTOCIAEARDSTOCASINHF",
    "found": false,
    "recovered": false
   },
   {
    "score": -4.662,
    "english_free": -4.8245,
    "restarts": 1000,
    "letters_right": 34,
    "true_score": -4.2804,
    "plaintext": "UEELEGTOHOFNATESERNEDEASTNORTHEASTESERFANCESOFTITOBEINGFIRDCELYBERLINCLOCKSMYBALRESEAPABYPOEITTOP",
    "found": true,
    "recovered": false
   },
   {
    "score": -4.6499,
    "english_free": -4.7985,
    "restarts": 1000,
    "letters_right": 35,
    "true_score": -4.4022,
    "plaintext": "WXTHEYTHESRECUTLEISHREASTNORTHEASTLCHASRESONYOUTONSEEONERMYLEDEBERLINCLOCKFOFANTSLONISDIDYENAITEX",
    "found": true,
    "recovered": false
   },
   {
    "score": -4.7088,
    "english_free": -4.8074,
    "restarts": 1000,
    "letters_right": 34,
    "true_score": -4.4538,
    "plaintext": "NGAZELALFUNDGUEDALATAEASTNORTHEASTFOURIWINNHISOROWNBUTNETEQUARDBERLINCLOCKEANDYMADELSTHECOUONYOUN",
    "found": true,
    "recovered": false
   },
   {
    "score": -4.6874,
    "english_free": -4.9456,
    "restarts": 1000,
    "letters_right": 38,
    "true_score": -4.181,
    "plaintext": "RTFIAGAMEYSESKISCABELEASTNORTHEASTERCHIDATSTRODSTANNAMOUFFTAYAMBERLINCLOCKTOESUITHEDFEREENDROGERZ",
    "found": true,
    "recovered": false
   },
   {
    "score": -4.7587,
    "english_free": -4.9635,
    "restarts": 1000,
    "letters_right": 31,
    "true_score": -4.2797,
    "plaintext": "LMFIZEBAYENDOZFRUARCHEASTNORTHEASTERETHECOMIRTOTORSTOSORDSINTOIBERLINCLOCKHEALWEVEMEHATTAGWALEEKH",
    "found": false,
    "recovered": false
   },
   {
    "score": -4.7133,
    "english_free": -4.8727,
    "restarts": 1000,
    "letters_right": 37,
    "true_score": -4.2946,
    "plaintext": "HEGAMETOCONUESITOBEACEASTNORTHEASTORYHAROBOICINJLRDGONPHONETREABERLINCLOCKKELDANRATEDANICROVERENF",
    "found": false,
    "recovered": false
   },
   {
    "score": -4.8361,
    "english_free": -5.1778,
    "restarts": 1000,
    "letters_right": 31,
    "true_score": -3.9617,
    "plaintext": "NMEDINLTUNIERIONYANTHEASTNORTHEASTWESSRALLSZLESSIMUHADNEANFEIRABERLINCLOCKETODEUSWEPULSWERAWSTOYM",
    "found": false,
    "recovered": false
   },
   {
    "score": -4.766,
    "english_free": -5.0097,
    "restarts": 1000,
    "letters_right": 36,
    "true_score": -4.2214,
    "plaintext": "XVERATERANCHSPASINBOREASTNORTHEASTSIBLINTOPILESASSFLEATTONCEPTOBERLINCLOCKLYKOEBUPTEDIHOHIFECLLCO",
    "found": false,
    "recovered": false
   },
   {
    "score": -4.8191,
    "english_free": -5.0369,
    "restarts": 1000,
    "letters_right": 31,
    "true_score": -4.0682,
    "plaintext": "TZOSARPYTOANNESASOLOREASTNORTHEASTLONTOSCASORETAPRERUTIEGOEYSANBERLINCLOCKNDBYACHRSHANINNEFIONITE",
    "found": false,
    "recovered": false
   },
   {
    "score": -4.8053,
    "english_free": -5.1028,
    "restarts": 1000,
    "letters_right": 37,
    "true_score": -4.3379,
    "plaintext": "IKERSITICESESTLYMNAPLEASTNORTHEASTREREDENTTASITSGYETEDSINTEKVISBERLINCLOCKAFOCUHAMBREHEMOHRALWISU",
    "found": false,
    "recovered": false
   },
   {
    "score": -4.5894,
    "english_free": -4.8245,
    "restarts": 1000,
    "letters_right": 40,
    "true_score": -4.4364,
    "plaintext": "NIOCHEATTRETEREEENTUREASTNORTHEASTORSODILLENAOHHESPERANLEROPOSIBERLINCLOCKEARCIACIESTTECEOUTSOFNW",
    "found": true,
    "recovered": false
   }
  ]
 },
 "controls": "12 shuffled coppers per length that fit exactly at that length and form (0119's decider, seed 137), identical climb"
}
```

Notes: L23: K4 -5.050 (rank 9 of 13), coppers -5.130 to -4.941, plants found 10/12, recovered 0; L26: K4 -4.954 (rank 12 of 13), coppers -5.136 to -4.709, plants found 5/12, recovered 0


