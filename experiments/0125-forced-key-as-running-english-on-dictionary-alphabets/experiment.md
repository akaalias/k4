# 0125-forced-key-as-running-english-on-dictionary-alphabets: If the key were running English text: do the key letters forced at EASTNORTHEAST and BERLINCLOCK read as English under any of the 208,062 dictionary-word alphabets, better than on scrambled coppers?

**Family:** 1-keyed-periodic  
**Parent:** 0010-mixed-alphabets-forced-key-english  
**Decision:** reverted  
**Run:** 2026-10-16T08:43:06+00:00, 305.1 s, status ran  
**Time by phase:** design 0 s, implement 13 s, test 6 s, run 305 s, record 0 s

## In plain words

A running key uses the letters of a book as the key, one book letter per message letter. If K4 were made that way, then where we know the message (EASTNORTHEAST and BERLINCLOCK), working backwards gives 24 letters of the book itself, which would read as English. We try this with tables built from every word in an English dictionary, and compare the most English-looking result with what the same search finds on scrambled copies of the carved text, where no book is hidden.

## Walkthrough, by hand

1. Pick a dictionary word, say WINTER, and build its table alphabet: WINTER then the unused letters in order.
2. Pick a rule, say Vigenere with WINTER on both sides.
3. At place 22 the message has E and the copper F: key value = place of F minus place of E in that alphabet.
4. Read the key value as a letter of the key alphabet.
5. Do this for places 22-34 and 64-74: two strings of 13 and 11 key letters.
6. Score both strings for English four-letter groups.
7. Repeat for every word, side, rule and key alphabet; keep the best.
8. Do the same with scrambled copies of K4 and compare.

## Worked example (generated)

```
alphabet from WINTER: WINTERABCDFGHJKLMOPQSUVXYZ; Vigenere, WINTER on both sides, key letters on the standard alphabet

place  known  carved  key value  key letter
   22      E       F          6           G
   23      A       L          9           J
   24      S       R         11           L
   25      T       V         19           T
   26      N       Q         17           R
   27      O       Q          2           C
   28      R       P         13           N
   29      T       R          2           C
   30      H       N         16           Q
   31      E       G          7           H
   32      A       K          8           I
   33      S       S          0           A
   34      T       S         17           R
   64      B       N         21           V
   65      E       Y         20           U
   66      R       P         13           N
   67      L       V          7           H
   68      I       T          2           C
   69      N       T          1           B
   70      C       M          8           I
   71      L       Z         10           K
   72      O       F         19           T
   73      C       P         10           K
   74      K       K          0           A
```

## Lineage

Inherits from 0010-mixed-alphabets-forced-key-english. What changed: F1.3. 0009 and 0010 read the forced key stretches as English under the standard, KRYPTOS and 61 puzzle-word alphabets (best -3.81, the same as shuffled K4). Here every keyword alphabet from the project dictionary (208,062 distinct, as in 0109) is used as the plain alphabet, the cipher alphabet or both, under three table rules and two key alphabets (standard, or the same keyword alphabet): 18 readings per alphabet, 3.7 million per text. The best English score of the two forced stretches together is compared with 50 scrambled coppers searched identically, and 20 planted running keys measure power.

## Hypothesis (domain expert)

C1(b) (the table alone), C27(c) (a different tableau), C5 ('key word/s', a running key from a named text). A running key from an English book on a keyword-mixed table: at each known place the key letter is forced, k = C(c) - P(p) (Vigenere), P(p) - C(c) (variant) or C(c) + P(p) (Beaufort), read through the key alphabet (standard or the keyword alphabet). The 13 forced letters at 22-34 and the 11 at 64-74 would then be two windows of English. Score: mean log10 quadgram over both windows (10 + 8 quadgrams, the harness's table). Alphabets: every word of four or more letters in kryptos/data/words.txt, keyword-mixed (repeats dropped, rest of the alphabet in order), standard and KRYPTOS excluded (0009); configurations (W, std), (std, W), (W, W). Exhaustive over this space. Controls: 50 shuffles of K4 (seed 125), identical search. Power: 20 planted texts, each a K4-length ciphertext made from a random English plaintext with the known letters in place, a running key from Carter's Tomb of Tut-ankh-Amen vol. 1 at a random offset, a random dictionary alphabet and configuration; a plant counts as found if its best score beats every copper. Tests reading C5 'a named text' for any text, without the text.

## Prediction

K4's best combined score lies inside the range of the 50 coppers (the space is 3.7 million readings per text, and the best of that much noise reaches near-English on 24 letters). Power is low: fewer than half of the 20 planted running keys beat every copper, because a true 24-letter English window scores about -4.2 while the best of 3.7 million noise readings is expected near -4.0. If so, F1.3 is recorded blocked (the forced letters are too few to tell a running key from chance), not closed.

## Method

1. Build the 208,062 keyword alphabets.
2. For K4, 50 shuffled coppers and 20 plants: for every alphabet, configuration, rule and key alphabet, compute the 24 forced key letters and score the two windows.
3. Keep the best combined score and the best per window.
4. Compare K4 with the coppers; count the plants found.

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
 "family": "running key from an unknown English text on keyword-mixed tables from the dictionary, no move",
 "alphabets": 208062,
 "readings_per_alphabet": 18,
 "readings_per_text": 3745116,
 "exhaustive": true,
 "windows": "22-34 (13 letters) and 64-74 (11), scored together (18 quadgrams)",
 "k4": {
  "score": -4.9365,
  "reading": [
   "IREPABLCDFGHJKMNOQSTUVWXYZ",
   "W-W",
   "vig",
   "W",
   "CEFEEREDADFIZGWENTACTTWI"
  ],
  "best_east": -4.3407,
  "best_berlin": -3.7804
 },
 "coppers": [
  {
   "score": -5.1047,
   "reading": [
    "OLDHAMITEBCFGJKNPQRSUVWXYZ",
    "W-W",
    "var",
    "W",
    "VOANIFTVATEPYYIMPENINTDO"
   ],
   "best_east": -4.2078,
   "best_berlin": -3.9763
  },
  {
   "score": -4.9964,
   "reading": [
    "ULOTRICHESABDFGJKMNPQVWXYZ",
    "W-std",
    "vig",
    "W",
    "EUMILDLOTTCAECAFORELIEVO"
   ],
   "best_east": -4.1113,
   "best_berlin": -3.9218
  },
  {
   "score": -4.9469,
   "reading": [
    "LETDOWNABCFGHIJKMPQRSUVXYZ",
    "W-std",
    "vig",
    "W",
    "YWAYSKEIMUSPAFALEDSTOMEF"
   ],
   "best_east": -4.1361,
   "best_berlin": -3.9328
  },
  {
   "score": -5.2121,
   "reading": [
    "SWEALBCDFGHIJKMNOPQRTUVXYZ",
    "W-W",
    "var",
    "W",
    "NYHEMUNZETHCAOFDENDESPSB"
   ],
   "best_east": -4.2407,
   "best_berlin": -4.0601
  },
  {
   "score": -5.0726,
   "reading": [
    "LEGAITYBCDFHJKMNOPQRSUVWXZ",
    "std-W",
    "beau",
    "W",
    "YPFOCATAICTERFWHEELICHEW"
   ],
   "best_east": -4.1285,
   "best_berlin": -4.0662
  },
  {
   "score": -5.0093,
   "reading": [
    "TROPHGENSIABCDFJKLMQUVWXYZ",
    "W-std",
    "beau",
    "W",
    "GVRELEHMENSTAGNCERTSASEH"
   ],
   "best_east": -3.6447,
   "best_berlin": -3.9664
  },
  {
   "score": -5.0992,
   "reading": [
    "CONVERGMTABDFHIJKLPQSUWXYZ",
    "std-W",
    "beau",
    "W",
    "BACASNRHERIMANSTTOPENAYK"
   ],
   "best_east": -4.1081,
   "best_berlin": -3.8772
  },
  {
   "score": -4.964,
   "reading": [
    "BUTSACDEFGHIJKLMNOPQRVWXYZ",
    "W-std",
    "vig",
    "W",
    "WANDASTISIINGNJEWINONKGR"
   ],
   "best_east": -4.1643,
   "best_berlin": -3.8658
  },
  {
   "score": -5.0524,
   "reading": [
    "FALDGEBCHIJKMNOPQRSTUVWXYZ",
    "W-std",
    "vig",
    "W",
    "GGSIMHAPSITWRMAYINASHAWE"
   ],
   "best_east": -4.2073,
   "best_berlin": -3.7527
  },
  {
   "score": -4.6741,
   "reading": [
    "METALIFCURBDGHJKNOPQSVWXYZ",
    "W-W",
    "vig",
    "std",
    "SECUBLESTSOFACOYWANDLOUT"
   ],
   "best_east": -3.7237,
   "best_berlin": -4.0697
  },
  {
   "score": -4.9596,
   "reading": [
    "SHOWINGABCDEFJKLMPQRTUVXYZ",
    "W-std",
    "vig",
    "std",
    "OERACONTOFPRHKIRYLERLIBR"
   ],
   "best_east": -4.2304,
   "best_berlin": -3.9638
  },
  {
   "score": -4.9254,
   "reading": [
    "CIRUTABLEDFGHJKMNOPQSVWXYZ",
    "W-std",
    "beau",
    "std",
    "SONOTISSHEYIDSIRSATEUNLV"
   ],
   "best_east": -4.3597,
   "best_berlin": -3.8727
  },
  {
   "score": -4.9516,
   "reading": [
    "DISENTHRALBCFGJKMOPQUVWXYZ",
    "std-W",
    "var",
    "std",
    "NDALELVELATDRHTSWONGDONG"
   ],
   "best_east": -4.2438,
   "best_berlin": -3.9701
  },
  {
   "score": -5.0569,
   "reading": [
    "BIOCHEMADFGJKLNPQRSTUVWXYZ",
    "W-W",
    "var",
    "W",
    "IAQUESGIVESZUIKETWINIAHU"
   ],
   "best_east": -4.3263,
   "best_berlin": -3.9694
  },
  {
   "score": -4.7763,
   "reading": [
    "SUMARINEBCDFGHJKLOPQTVWXYZ",
    "W-W",
    "beau",
    "std",
    "WWMUCHANCHESUYBYFUNDRMUL"
   ],
   "best_east": -4.1877,
   "best_berlin": -3.8565
  },
  {
   "score": -5.2092,
   "reading": [
    "CARNIFESBDGHJKLMOPQTUVWXYZ",
    "std-W",
    "var",
    "W",
    "SORGAUSATHISCCRPPUSMERJU"
   ],
   "best_east": -4.1629,
   "best_berlin": -4.0739
  },
  {
   "score": -4.9086,
   "reading": [
    "UNITERPDSABCFGHJKLMOQVWXYZ",
    "W-W",
    "beau",
    "W",
    "CTERELSSWEREOONALSATMNNO"
   ],
   "best_east": -4.0545,
   "best_berlin": -3.8475
  },
  {
   "score": -4.8321,
   "reading": [
    "HORSYIMABCDEFGJKLNPQTUVWXZ",
    "W-W",
    "vig",
    "std",
    "DIPPLEPATLEFOKCOFTEENOTL"
   ],
   "best_east": -3.9543,
   "best_berlin": -3.989
  },
  {
   "score": -5.0686,
   "reading": [
    "TUBERACOSDFGHIJKLMNPQVWXYZ",
    "W-W",
    "beau",
    "std",
    "RRIAHSASCHLEYWGISGAINARE"
   ],
   "best_east": -4.1045,
   "best_berlin": -4.1442
  },
  {
   "score": -4.9671,
   "reading": [
    "TRANSGEIVLYBCDFHJKMOPQUWXZ",
    "W-W",
    "var",
    "std",
    "AIXDUREELLLEMEMBEDERMINA"
   ],
   "best_east": -4.1884,
   "best_berlin": -3.6941
  },
  {
   "score": -5.0598,
   "reading": [
    "ANLCITEBDFGHJKMOPQRSUVWXYZ",
    "W-std",
    "var",
    "std",
    "DANMFOCATSEAGGVISONELITD"
   ],
   "best_east": -4.2433,
   "best_berlin": -4.0675
  },
  {
   "score": -4.8201,
   "reading": [
    "ROUTINSABCDEFGHJKLMPQVWXYZ",
    "W-std",
    "vig",
    "W",
    "UHNANWANTTODRDDOUTECURSM"
   ],
   "best_east": -4.1786,
   "best_berlin": -3.9351
  },
  {
   "score": -4.6021,
   "reading": [
    "BARKPELINGCDFHJMOQSTUVWXYZ",
    "std-W",
    "vig",
    "W",
    "OSCCONTOWESITROMALLEDPUT"
   ],
   "best_east": -4.1821,
   "best_berlin": -3.8881
  },
  {
   "score": -4.9993,
   "reading": [
    "UNGETILZABCDFHJKMOPQRSVWXY",
    "std-W",
    "var",
    "W",
    "KIENDSWINBEIHARADYINERMZ"
   ],
   "best_east": -4.3047,
   "best_berlin": -3.9219
  },
  {
   "score": -5.0314,
   "reading": [
    "TAROPCHBDEFGIJKLMNQSUVWXYZ",
    "W-std",
    "var",
    "W",
    "UETHESATROVFBHNDSUMIAMUS"
   ],
   "best_east": -4.1156,
   "best_berlin": -3.9608
  },
  {
   "score": -5.0862,
   "reading": [
    "PHILANTROSCBDEFGJKMQUVWXYZ",
    "std-W",
    "vig",
    "std",
    "IREGOATHKETYOTARECTFENTM"
   ],
   "best_east": -4.2485,
   "best_berlin": -3.9005
  },
  {
   "score": -5.281,
   "reading": [
    "PRECONSIATBDFGHJKLMQUVWXYZ",
    "W-W",
    "beau",
    "std",
    "YHOPINDTERPADTVSDIBEAFFF"
   ],
   "best_east": -4.3572,
   "best_berlin": -3.8949
  },
  {
   "score": -4.955,
   "reading": [
    "CORALVIUBDEFGHJKMNPQSTWXYZ",
    "std-W",
    "vig",
    "W",
    "HWERORRETMURBOANCERPLARO"
   ],
   "best_east": -4.2395,
   "best_berlin": -3.9175
  },
  {
   "score": -5.0279,
   "reading": [
    "EPITHLZABCDFGJKMNOQRSUVWXY",
    "W-W",
    "var",
    "W",
    "GIURIEDOHAMEAHILTAVERFIE"
   ],
   "best_east": -3.9452,
   "best_berlin": -3.9513
  },
  {
   "score": -5.1401,
   "reading": [
    "BUTCHERDOMAFGIJKLNPQSVWXYZ",
    "std-W",
    "vig",
    "W",
    "NDORATSOICSMCUHARSDONOUL"
   ],
   "best_east": -4.2036,
   "best_berlin": -4.1538
  },
  {
   "score": -4.8838,
   "reading": [
    "SUPERFLCTIONABDGHJKMQVWXYZ",
    "W-std",
    "var",
    "std",
    "EGALETENONROYDHORIAGEFEK"
   ],
   "best_east": -4.1691,
   "best_berlin": -4.143
  },
  {
   "score": -4.9236,
   "reading": [
    "PREONIGABCDFHJKLMQSTUVWXYZ",
    "W-W",
    "vig",
    "W",
    "SSSEDITHEHACYRYITLYEITFI"
   ],
   "best_east": -4.3072,
   "best_berlin": -4.0395
  },
  {
   "score": -4.8906,
   "reading": [
    "UNLACEDBFGHIJKMOPQRSTVWXYZ",
    "std-W",
    "var",
    "std",
    "OOTAGOAGASISANTSORERYDAU"
   ],
   "best_east": -4.1976,
   "best_berlin": -3.968
  },
  {
   "score": -4.9969,
   "reading": [
    "ENTLCHYABDFGIJKMOPQRSUVWXZ",
    "std-W",
    "var",
    "W",
    "THCOUPBILEDAZLALOWRISPUN"
   ],
   "best_east": -4.3499,
   "best_berlin": -3.9322
  },
  {
   "score": -5.0162,
   "reading": [
    "PHALNSTERICBDFGJKMOQUVWXYZ",
    "W-W",
    "vig",
    "W",
    "SLFPORTCOBSFLBILLASCOMOF"
   ],
   "best_east": -4.2073,
   "best_berlin": -4.1363
  },
  {
   "score": -4.3004,
   "reading": [
    "TANGSBCDEFHIJKLMOPQRUVWXYZ",
    "W-W",
    "vig",
    "W",
    "YNDANDGINERHBMATININGTHU"
   ],
   "best_east": -4.1536,
   "best_berlin": -3.7798
  },
  {
   "score": -4.9252,
   "reading": [
    "TUBIFERACDGHJKLMNOPQSVWXYZ",
    "W-W",
    "beau",
    "W",
    "EVENINASEASBIDDASSVARULF"
   ],
   "best_east": -4.0773,
   "best_berlin": -3.8911
  },
  {
   "score": -5.0611,
   "reading": [
    "CINHOZATBDEFGJKLMPQRSUVWXY",
    "W-std",
    "var",
    "std",
    "AVHATBERSTAFCJOOMAGIVISM"
   ],
   "best_east": -4.0975,
   "best_berlin": -3.8651
  },
  {
   "score": -4.9315,
   "reading": [
    "IGUANDBCEFHJKLMOPQRSTVWXYZ",
    "std-W",
    "beau",
    "std",
    "BLTSNETENEDYFSTEFOFINTEM"
   ],
   "best_east": -4.0138,
   "best_berlin": -3.9577
  },
  {
   "score": -5.0325,
   "reading": [
    "ORTHGAPICLYBDEFJKMNQSUVWXZ",
    "std-W",
    "vig",
    "W",
    "XMOGISTOFINTVPXBEANITIFY"
   ],
   "best_east": -4.3041,
   "best_berlin": -3.9926
  },
  {
   "score": -5.0038,
   "reading": [
    "HETROLYSINABCDFGJKMPQUVWXZ",
    "std-W",
    "beau",
    "std",
    "OURMINKSORDEASAMTASEISJA"
   ],
   "best_east": -4.2728,
   "best_berlin": -3.6542
  },
  {
   "score": -4.8123,
   "reading": [
    "PROSITNABCDEFGHJKLMQUVWXYZ",
    "W-W",
    "var",
    "std",
    "IKOVEDTOMILYTRHHITHEETFW"
   ],
   "best_east": -4.2447,
   "best_berlin": -3.8182
  },
  {
   "score": -5.1939,
   "reading": [
    "JURISDCTONALYBEFGHKMPQVWXZ",
    "W-W",
    "var",
    "W",
    "ACESTLOARETSUTTANTOLBMUM"
   ],
   "best_east": -4.173,
   "best_berlin": -3.8804
  },
  {
   "score": -4.9422,
   "reading": [
    "CUNILGSABDEFHJKMOPQRTVWXYZ",
    "W-std",
    "var",
    "W",
    "MEUSACCONCENSTTTEHOPINZB"
   ],
   "best_east": -4.2722,
   "best_berlin": -4.1516
  },
  {
   "score": -5.1224,
   "reading": [
    "IDOLATRYBCEFGHJKMNPQSUVWXZ",
    "std-W",
    "beau",
    "std",
    "NANWHONFUSTPHFLIENDYKNOV"
   ],
   "best_east": -4.0638,
   "best_berlin": -4.0201
  },
  {
   "score": -4.8439,
   "reading": [
    "SPECULABDFGHIJKMNOQRTVWXYZ",
    "std-W",
    "beau",
    "std",
    "JRCDTHATTNELYVIATINTHANX"
   ],
   "best_east": -4.2672,
   "best_berlin": -3.8783
  },
  {
   "score": -4.9334,
   "reading": [
    "SOLIDFCATNBEGHJKMPQRUVWXYZ",
    "std-W",
    "var",
    "W",
    "RERBEENGLERGQOTADIFCHENW"
   ],
   "best_east": -4.0891,
   "best_berlin": -4.0103
  },
  {
   "score": -4.9474,
   "reading": [
    "RUMONGEABCDFHIJKLPQSTVWXYZ",
    "W-W",
    "beau",
    "W",
    "WORLYNOISITHMIBROWADDROX"
   ],
   "best_east": -4.1821,
   "best_berlin": -3.822
  },
  {
   "score": -4.8746,
   "reading": [
    "STEALHIKBCDFGJMNOPQRUVWXYZ",
    "W-W",
    "beau",
    "W",
    "VIZETISCHADABOHNTAWASANJ"
   ],
   "best_east": -4.0826,
   "best_berlin": -3.8437
  },
  {
   "score": -4.956,
   "reading": [
    "UNFORESTALBCDGHIJKMPQVWXYZ",
    "W-std",
    "var",
    "std",
    "NCAIMMOTHANAPTCESOFMIKAR"
   ],
   "best_east": -4.215,
   "best_berlin": -4.0829
  }
 ],
 "plants": [
  {
   "score": -4.3548,
   "reading": [
    "EXARTICULONBDFGHJKMPQSVWYZ",
    "W-W",
    "var",
    "std",
    "AKEBUTSHOULDHTHEDOORBLOC"
   ],
   "best_east": -4.2098,
   "best_berlin": -3.697,
   "truth_window": "AKEBUTSHOULDHTHEDOORBLOC",
   "truth_score": -4.3548
  },
  {
   "score": -3.9762,
   "reading": [
    "CRANIOMLBDEFGHJKPQSTUVWXYZ",
    "W-W",
    "var",
    "std",
    "MSELVESWITHWAOOBJECTIONA"
   ],
   "best_east": -3.8719,
   "best_berlin": -3.8651,
   "truth_window": "MSELVESWITHWAOOBJECTIONA",
   "truth_score": -3.9762
  },
  {
   "score": -4.0154,
   "reading": [
    "UNAMLGTIBCDEFHJKOPQRSVWXYZ",
    "W-W",
    "vig",
    "W",
    "MSELFWITHSUCHVERTHELESSW"
   ],
   "best_east": -4.202,
   "best_berlin": -3.6055,
   "truth_window": "MSELFWITHSUCHVERTHELESSW",
   "truth_score": -4.0154
  },
  {
   "score": -4.3361,
   "reading": [
    "TAXIVEBCDFGHJKLMNOPQRSUWYZ",
    "std-W",
    "beau",
    "std",
    "MBERSTHETOMBSTEWINLOCKMR"
   ],
   "best_east": -3.885,
   "best_berlin": -4.0187,
   "truth_window": "MBERSTHETOMBSTEWINLOCKMR",
   "truth_score": -4.3361
  },
  {
   "score": -4.7758,
   "reading": [
    "HOMINEABCDFGJKLPQRSTUVWXYZ",
    "W-std",
    "var",
    "std",
    "RNTOLUXORIARRDIRECTOROFT"
   ],
   "best_east": -4.3109,
   "best_berlin": -3.8646,
   "truth_window": "RNTOLUXORIARRDIRECTOROFT",
   "truth_score": -4.7758
  },
  {
   "score": -4.7221,
   "reading": [
    "COPERLATBDFGHIJKMNQSUVWXYZ",
    "W-std",
    "var",
    "W",
    "ESBETWEENROYALYBELZONISE"
   ],
   "best_east": -4.1726,
   "best_berlin": -3.8735,
   "truth_window": "ESBETWEENROYALYBELZONISE",
   "truth_score": -4.7221
  },
  {
   "score": -4.4947,
   "reading": [
    "SCOMBRIFADEGHJKLNPQTUVWXYZ",
    "W-W",
    "beau",
    "std",
    "PSADMIRALKENNABLESINCEIT"
   ],
   "best_east": -4.2192,
   "best_berlin": -3.8812,
   "truth_window": "PSADMIRALKENNABLESINCEIT",
   "truth_score": -4.4947
  },
  {
   "score": -4.0601,
   "reading": [
    "BARMECIDLFGHJKNOPQSTUVWXYZ",
    "W-std",
    "var",
    "std",
    "ONTHEWHOLETHESPERHAPSWOR"
   ],
   "best_east": -3.5128,
   "best_berlin": -4.103,
   "truth_window": "ONTHEWHOLETHESPERHAPSWOR",
   "truth_score": -4.0601
  },
  {
   "score": -4.1793,
   "reading": [
    "PALISEBCDFGHJKMNOQRTUVWXYZ",
    "W-W",
    "beau",
    "std",
    "PACKINGFIRSTATHEUNPACKIN"
   ],
   "best_east": -3.9264,
   "best_berlin": -3.635,
   "truth_window": "PACKINGFIRSTATHEUNPACKIN",
   "truth_score": -4.1793
  },
  {
   "score": -4.3032,
   "reading": [
    "DURENABCFGHIJKLMOPQSTVWXYZ",
    "W-W",
    "vig",
    "W",
    "NSHOWSONLYTHEPPERTWODOUB"
   ],
   "best_east": -4.0807,
   "best_berlin": -3.6598,
   "truth_window": "NSHOWSONLYTHEPPERTWODOUB",
   "truth_score": -4.3032
  },
  {
   "score": -4.3046,
   "reading": [
    "VEGTABILYCDFHJKMNOPQRSUWXZ",
    "W-std",
    "vig",
    "W",
    "NSINCOLOUREDLPLESOFTAPES"
   ],
   "best_east": -4.2063,
   "best_berlin": -4.0717,
   "truth_window": "NSINCOLOUREDLPLESOFTAPES",
   "truth_score": -4.3046
  },
  {
   "score": -4.2424,
   "reading": [
    "UNJILTEDABCFGHKMOPQRSVWXYZ",
    "std-W",
    "beau",
    "W",
    "MAKEBUTSHOULDFTHEDOORBLO"
   ],
   "best_east": -4.1271,
   "best_berlin": -4.104,
   "truth_window": "MAKEBUTSHOULDFTHEDOORBLO",
   "truth_score": -4.2424
  },
  {
   "score": -4.1245,
   "reading": [
    "MUDSCKERABFGHIJLNOPQTVWXYZ",
    "W-W",
    "beau",
    "W",
    "SWEREINMUCHTOGISTERACCUR"
   ],
   "best_east": -4.1473,
   "best_berlin": -3.8267,
   "truth_window": "SWEREINMUCHTOGISTERACCUR",
   "truth_score": -4.1245
  },
  {
   "score": -4.1089,
   "reading": [
    "PROEISMABCDFGHJKLNQTUVWXYZ",
    "W-W",
    "beau",
    "W",
    "ANXIOUSLYFORERFACETHEREW"
   ],
   "best_east": -4.1123,
   "best_berlin": -3.5799,
   "truth_window": "ANXIOUSLYFORERFACETHEREW",
   "truth_score": -4.1089
  },
  {
   "score": -3.8174,
   "reading": [
    "BESCUTHONADFGIJKLMPQRVWXYZ",
    "W-std",
    "vig",
    "W",
    "HTHEYBELONGEDLARKINGTHER"
   ],
   "best_east": -4.0736,
   "best_berlin": -3.4971,
   "truth_window": "HTHEYBELONGEDLARKINGTHER",
   "truth_score": -3.8174
  },
  {
   "score": -4.2038,
   "reading": [
    "DISNCARETBFGHJKLMOPQUVWXYZ",
    "std-W",
    "beau",
    "std",
    "ASALSOAFFORDEOTABLESOFLU"
   ],
   "best_east": -4.2264,
   "best_berlin": -3.6728,
   "truth_window": "ASALSOAFFORDEOTABLESOFLU",
   "truth_score": -4.2038
  },
  {
   "score": -4.5298,
   "reading": [
    "KITENHARDBCFGJLMOPQSUVWXYZ",
    "W-W",
    "var",
    "std",
    "OYALBURIALHEROLDINGDOORS"
   ],
   "best_east": -4.074,
   "best_berlin": -4.0337,
   "truth_window": "OYALBURIALHEROLDINGDOORS",
   "truth_score": -4.5298
  },
  {
   "score": -4.3562,
   "reading": [
    "CHALUSBDEFGIJKMNOPQRTVWXYZ",
    "W-W",
    "vig",
    "W",
    "HEAXLESWEREDEISMOUNTEDAN"
   ],
   "best_east": -4.3074,
   "best_berlin": -3.8792,
   "truth_window": "HEAXLESWEREDEISMOUNTEDAN",
   "truth_score": -4.3562
  },
  {
   "score": -4.0832,
   "reading": [
    "SAXTILEBCDFGHJKMNOPQRUVWYZ",
    "std-W",
    "vig",
    "std",
    "WHILETHEFIFTHHEHOOKSONEA"
   ],
   "best_east": -3.7963,
   "best_berlin": -3.7032,
   "truth_window": "WHILETHEFIFTHHEHOOKSONEA",
   "truth_score": -4.0832
  },
  {
   "score": -4.2204,
   "reading": [
    "REDISTCABFGHJKLMNOPQUVWXYZ",
    "W-std",
    "vig",
    "std",
    "EYSUCCEEDEDINENFROMADIST"
   ],
   "best_east": -4.2797,
   "best_berlin": -4.0828,
   "truth_window": "EYSUCCEEDEDINENFROMADIST",
   "truth_score": -4.2204
  }
 ],
 "k4_rank_among_coppers": 18,
 "coppers_range": [
  -5.281,
  -4.3004
 ],
 "k4_above_all_coppers": false,
 "plants_found": 11,
 "plants_whose_true_window_beats_every_copper": 11,
 "controls": "50 shuffled coppers (seed 125), identical search"
}
```

Notes: K4 best -4.936 (('IREPABLCDFGHJKMNOQSTUVWXYZ', 'W-W', 'vig', 'W', 'CEFEEREDADFIZGWENTACTTWI')); coppers -5.281 to -4.300; plants found 11/20 (true windows above every copper: 11).


