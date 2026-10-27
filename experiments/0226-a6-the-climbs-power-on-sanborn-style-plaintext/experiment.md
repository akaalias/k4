# 0226-a6-the-climbs-power-on-sanborn-style-plaintext: A6.2: the climbs' power on Sanborn-style plaintext: X stops, K1-K3 windows and three changed letters planted through F1.5's design 2 (one free alphabet at 23, two at 13) and 0125's running-key search, judged by quadgrams and by the blind judge

**Family:** 1-keyed-periodic  
**Parent:** 0221-rejudge-the-sampled-verdicts-free-alphabets-and-running-english  
**Decision:** reverted  
**Run:** 2026-10-27T11:04:57+00:00, 4172.2 s, status ran  
**Time by phase:** design 91 s, implement 223 s, test 10 s, run 4172 s, record 0 s

## In plain words

Earlier experiments checked that their searches could find a hidden test message, but the test messages were clean English from a book. Sanborn's real messages are messier: X between sentences, deliberate misspellings, odd phrasing. Here we hide messy messages of that kind, run the same searches on them unchanged, and see how often the search, scored by letter statistics and separately by the judge (a language model that reads one text at a time without knowing where it came from), picks the hidden message out from scrambled copies of itself.

## Walkthrough, by hand

1. Take a messy test message, say a window of K2: ...THEYUSEDTHEEARTHSMAGNETICFIELDXTHEINFORMATION....
2. Put EASTNORTHEAST and BERLINCLOCK at their places.
3. Encipher it by hand the way the item says: one shuffled alphabet, a key of 23 numbers, Beaufort form.
4. Make six scrambled copies of the ciphertext that the same key length can still fit.
5. Run the same search on the seven texts and keep each best reading.
6. The message is found if its reading scores above all six copies', once by letter statistics and once by the judge.

## Worked example (generated)

```
A6.2 plants Sanborn-style messages. A K1-K3 window with the known words set:

  message      BETWEENSUBTLESHADINGAEASTNORTHEASTFLIGHTLIESTHENUANCEOFIQLUSIONBERLINCLOCKYINVISIBLEHOWSTHATPOSSI
  judge sees   BETWEENSUBTLESHADINGA#############FLIGHTLIESTHENUANCEOFIQLUSION###########YINVISIBLEHOWSTHATPOSSI

  enciphered with one shuffled alphabet and a key of 23 (Beaufort form), climbed by 0140's search
  with six scrambled copies; found if its reading beats all six, by quadgrams and by the judge.
```

## Lineage

Inherits from 0221-rejudge-the-sampled-verdicts-free-alphabets-and-running-english. What changed: A6.2 (Stage 2, step 4, issue #84). The sampled closes of F1.1 (0139-0142), F1.2 (0143-0146) and F1.3 (0125) measured their power on clean Carter. Here the planted messages are the judge bench's Sanborn-style classes (reports/judge-bench.md): Carter with X for every full stop (xstops), 97-letter windows of K1-K3's own plaintexts with their misspellings and X stops (k123), and clean English with three letters changed (sub3). Four of each go through each frozen search unchanged: 0140's tempering climb at one free alphabet, Beaufort form, length 23; 0144's two-alphabet climb at 13; 0125's running-key reading of the forced key. Each plant is found or not by quadgrams (the verdicts' rule) and by the judge, against the same copies the verdict's power used.

## Hypothesis (domain expert)

A6 (knowledge/12-assumptions.md), with C19 (Scheidt 2015, 'what's a period... special characters don't work': X and Q as stops) and C17/C10 (Sanborn's deliberate misspellings, 'rife with mistakes on purpose', 2005). F1.5's design 2 (parallel tempering in the set of keys that keep the 24 known letters; 10 runs x 16 replicas x 625 rounds x 1000 moves) decided F1.1's Beaufort length 23 at 6 of 8 clean plants above their own 6 fitting shuffles (0139) and F1.2's length 13 at 5 of 5 above 5 kept-place shuffles (0143); 0125's running-key test (208,062 dictionary tables x 18 readings, the 24-letter forced key scored as English) found 11 of 20 Carter running keys above 50 shuffles. Those powers were measured on Carter's prose, which a quadgram model scores well. Sanborn's own plaintexts are not that: K2 has X stops and UNDERGRUUND, K1 IQLUSION, K3 DESPARATLY. The test: the same frozen searches on 12 plants per arm in the three bench classes; per plant, found when its score is strictly above every own copy's (6 fitting shuffles of the plant's ciphertext at 23, 6 kept-place shuffles at 13, 0125's 50 shuffles of K4 for the running key), by quadgram and, separately, by the judge in one blind call per arm. Null per plant: 1/7 (0125: 1/51). Pre-registered rule: an arm whose quadgram power falls below the verdict's stated power (23: 6/8; 13: 5/5, bar 4/5; 0125: 11/20) weakens the close it carried; the close stands only if the judge reaches that power here and A6.1 (0221) kept K4 inside its copies under the judge at that cell. Otherwise the item goes back to open in its family table and waits for Alexis.

## Prediction

Quadgram power falls on the messy classes: at 23 about 6 of 12 (the climb's quadgram target fights X stops and K1-K3's misspellings less than it fights noise, so k123 and xstops lose most); at 13 about 9 of 12; 0125 about 5 of 12 (a 24-letter window with an X or a changed letter loses quadgrams). The judge does at least as well as quadgrams on every arm and reaches the stated power at 13 but not at 23, where the climbed readings are only a third right. So F1.1's length 23 is weakened, F1.2's length 13 stands, and F1.3 is weakened for quadgrams but rescued by the judge if 0221's rejudge held. Zero candidates.

## Method

1. Plaintexts: per arm 4 xstops (tools/judge_bench.py's xstops_plant), 4 k123 windows (the bench's 12, split 4 per arm), 4 sub3 (kryptos.plants.english_plant with 3 free letters changed, the bench's damage); the 24 known letters set.
2. Arm 23: Beaufort form, random alphabet and key of 23 (0120's make_plants rule); 6 own copies, shuffles of the plant's ciphertext that 0120's exact decider fits at 23 (0140's rule); every text through 0140's frozen _job.
3. Arm 13: two random alphabets and key of 13 (0144's plant4 rule); witness from 0123's decider; 6 own copies keeping the 24 known places and shuffling the other 73; every text through 0144's frozen _any.
4. Arm 0125: the class text is the running key, under English plaintext (english_plant), on a random table, rule and key alphabet from 0125's sets; through 0125's frozen _job; its 50 copies regenerated with 0125's seed and checked against its record.
5. Found by quadgram: the climb's score strictly above every own copy's. Found by the judge: one call per arm on the plants' readings and their copies', the plant strictly above every own copy; None counts as not found.

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
 "item": "A6.2",
 "classes": [
  "xstops",
  "k123",
  "sub3"
 ],
 "per_class": 4,
 "own_copies": 6,
 "arms": {
  "23": "F1.1, one free alphabet, Beaufort form, length 23, 0140's frozen climb (design 2)",
  "13": "F1.2, two free alphabets, length 13, 0144's frozen climb (design 2)",
  "0125": "F1.3, running key on 208,062 dictionary tables, 0125's frozen search, the class text as the key"
 },
 "null_per_plant": {
  "23": "1/7",
  "13": "1/7",
  "0125": "1/51"
 },
 "runs_done": {
  "min": 10,
  "max": 10
 },
 "decryption_checked": true,
 "judge_texts_sent": 230,
 "judge_calls_estimated": 230,
 "expected_total_time": "about 31,000 core-seconds (84 texts at about 110 s in arm 23, 84 at about 235 s in arm 13, 62 at about 35 s for 0125; from 0140, 0144, 0125's runs), so 65-90 min on 8 cores",
 "arm13_key_redraws": 1,
 "result": {
  "23": {
   "rows": [
    {
     "cls": "xstops",
     "q": -4.8059,
     "own_q": [
      -5.2723,
      -5.1094,
      -4.8284,
      -4.9603,
      -4.8965,
      -5.0226
     ],
     "q_found": true,
     "judge": 12,
     "own_judge": [
      8,
      12,
      12,
      7,
      4,
      6
     ],
     "judge_found": false,
     "letters_right": 44,
     "reading": "THATTNEERTRECYREAIINDEASTNORTHEASTSSUGMECEATLEGSBOBRTSCBEECHAILBERLINCLOCKSENDETHISINENOFJENTHENN"
    },
    {
     "cls": "xstops",
     "q": -4.7998,
     "own_q": [
      -4.9677,
      -4.9768,
      -5.1043,
      -4.9889,
      -4.9601,
      -5.0428
     ],
     "q_found": true,
     "judge": 12,
     "own_judge": [
      12,
      8,
      8,
      8,
      12,
      8
     ],
     "judge_found": false,
     "letters_right": 32,
     "reading": "MYLOTULOUHANTSSTREAFREASTNORTHEASTOGEDEPAPPANOORSMUSIOMBWILINERBERLINCLOCKIDEESIRESOBEFENIACOREYI"
    },
    {
     "cls": "xstops",
     "q": -4.7844,
     "own_q": [
      -4.9729,
      -4.9939,
      -4.9206,
      -4.9878,
      -4.861,
      -5.0692
     ],
     "q_found": true,
     "judge": 14,
     "own_judge": [
      6,
      12,
      8,
      4,
      12,
      8
     ],
     "judge_found": true,
     "letters_right": 35,
     "reading": "PITHTTHEPEVINCESCARSIEASTNORTHEASTADIATDECHGMPOTSIDNTISMEBEWINSBERLINCLOCKYISHOLYOUBBONTHATMOTHDW"
    },
    {
     "cls": "xstops",
     "q": -4.8675,
     "own_q": [
      -5.0167,
      -4.9252,
      -5.1212,
      -5.0288,
      -4.9116,
      -5.0873
     ],
     "q_found": true,
     "judge": 8,
     "own_judge": [
      12,
      15,
      6,
      12,
      8,
      8
     ],
     "judge_found": false,
     "letters_right": 38,
     "reading": "VTAGGESNIGHAMMENALVESEASTNORTHEASTATEPLOADBERATDIPAYEYFOFSETTHEBERLINCLOCKTXOPORBIOLIALSTHALAFEYE"
    },
    {
     "cls": "k123",
     "q": -5.0364,
     "own_q": [
      -5.1767,
      -4.9028,
      -4.784,
      -5.0346,
      -5.0082,
      -5.0387
     ],
     "q_found": false,
     "judge": 12,
     "own_judge": [
      12,
      12,
      8,
      12,
      6,
      12
     ],
     "judge_found": false,
     "letters_right": 33,
     "reading": "DOHAVINHPRTALSINTRACEEASTNORTHEASTHSLOOOYLSITPIIFETSMIFIGATSTERBERLINCLOCKEONRIBEATROIDMENDFUMANZ"
    },
    {
     "cls": "k123",
     "q": -4.7561,
     "own_q": [
      -5.0535,
      -4.9742,
      -4.9857,
      -5.0145,
      -4.8217,
      -5.0641
     ],
     "q_found": true,
     "judge": 6,
     "own_judge": [
      7,
      12,
      8,
      8,
      12,
      22
     ],
     "judge_found": false,
     "letters_right": 37,
     "reading": "BIJESSELRCYLEINFACCONEASTNORTHEASTINICAISHELEGEEMESMNITIELLITHOBERLINCLOCKCRITISSORSEATHPHSASHINH"
    },
    {
     "cls": "k123",
     "q": -4.829,
     "own_q": [
      -5.0728,
      -4.9517,
      -4.9419,
      -5.0744,
      -4.9807,
      -4.991
     ],
     "q_found": true,
     "judge": 12,
     "own_judge": [
      10,
      12,
      6,
      12,
      5,
      12
     ],
     "judge_found": false,
     "letters_right": 32,
     "reading": "OHHSCOFLADANDRETHETYYEASTNORTHEASTBALLALICUTEEBADERABHUNTERCKINBERLINCLOCKGLACEOTFEWELIGHESERHUJS"
    },
    {
     "cls": "k123",
     "q": -4.7928,
     "own_q": [
      -5.0175,
      -4.9779,
      -4.9476,
      -4.9708,
      -4.8288,
      -4.9815
     ],
     "q_found": true,
     "judge": 8,
     "own_judge": [
      8,
      12,
      12,
      8,
      8,
      12
     ],
     "judge_found": false,
     "letters_right": 35,
     "reading": "HTLADEDDPANDEPINKTHEDEASTNORTHEASTGADTOLOHENOTTONOTORYEETULREABBERLINCLOCKEERPOINTHFOREBYPECMUCAB"
    },
    {
     "cls": "sub3",
     "q": -4.7241,
     "own_q": [
      -4.9747,
      -4.8819,
      -4.9198,
      -5.0631,
      -4.9571,
      -4.8657
     ],
     "q_found": true,
     "judge": 12,
     "own_judge": [
      8,
      12,
      12,
      8,
      12,
      8
     ],
     "judge_found": false,
     "letters_right": 41,
     "reading": "TNMOSTHEEZEREELYMORATEASTNORTHEASTICIEVEWARTSGREONEINUSGAMEHELIBERLINCLOCKESTPPGRETAWSUNCHMRTREGU"
    },
    {
     "cls": "sub3",
     "q": -4.7725,
     "own_q": [
      -5.0466,
      -4.8966,
      -4.9518,
      -4.9901,
      -4.9307,
      -5.0147
     ],
     "q_found": true,
     "judge": 8,
     "own_judge": [
      8,
      12,
      8,
      8,
      8,
      6
     ],
     "judge_found": false,
     "letters_right": 33,
     "reading": "RBBWHIMLOUTDEASIGRECREASTNORTHEASTREDHENTNOPTHOLLREFDERINDANOCKBERLINCLOCKOULIMCOLDMATENBRUSICESJ"
    },
    {
     "cls": "sub3",
     "q": -4.9993,
     "own_q": [
      -5.0022,
      -5.0084,
      -4.9071,
      -5.0021,
      -4.9469,
      -5.0562
     ],
     "q_found": false,
     "judge": 12,
     "own_judge": [
      8,
      12,
      8,
      12,
      8,
      7
     ],
     "judge_found": false,
     "letters_right": 33,
     "reading": "KRLMCGNERGYOTHINDULTYEASTNORTHEASTEVISPEEDWPANPORAHENOGAMASTGOMBERLINCLOCKHOWUSANADATRIVEUSPYEFAI"
    },
    {
     "cls": "sub3",
     "q": -4.6449,
     "own_q": [
      -5.3063,
      -5.0295,
      -4.9492,
      -5.0814,
      -5.0785,
      -5.0108
     ],
     "q_found": true,
     "judge": 12,
     "own_judge": [
      7,
      8,
      12,
      8,
      8,
      12
     ],
     "judge_found": false,
     "letters_right": 38,
     "reading": "DSHADDARGELSONNESAAREEASTNORTHEASTRACHANANSTRUEMITDOINRETLTHEFTBERLINCLOCKNONMEINDULLYOFTHTHSSFRG"
    }
   ],
   "quad_found": 10,
   "judge_found": 1,
   "of": 12,
   "by_class": {
    "xstops": {
     "quad": 4,
     "judge": 1,
     "of": 4
    },
    "k123": {
     "quad": 3,
     "judge": 0,
     "of": 4
    },
    "sub3": {
     "quad": 3,
     "judge": 0,
     "of": 4
    }
   },
   "stated_power": "6/8",
   "quad_below_stated": false,
   "judge_below_stated": true,
   "judge_none": 0
  },
  "13": {
   "rows": [
    {
     "cls": "xstops",
     "q": -4.7417,
     "own_q": [
      -4.76,
      -4.8349,
      -4.8339,
      -4.9048,
      -4.8721,
      -4.7346
     ],
     "q_found": false,
     "judge": 8,
     "own_judge": [
      8,
      12,
      12,
      12,
      12,
      32
     ],
     "judge_found": false,
     "letters_right": 37,
     "reading": "HUSNODOSINTPUGHTDOHEWEASTNORTHEASTBELELOMBUTORMOMETSGASABEREVEABERLINCLOCKMYOUTEDWILALADETHEEMOOH"
    },
    {
     "cls": "xstops",
     "q": -4.6247,
     "own_q": [
      -4.8665,
      -4.7787,
      -4.7888,
      -4.6581,
      -4.7093,
      -4.8393
     ],
     "q_found": true,
     "judge": 12,
     "own_judge": [
      15,
      8,
      8,
      12,
      12,
      8
     ],
     "judge_found": false,
     "letters_right": 39,
     "reading": "IEASORSTHEMOFDANDYSCEEASTNORTHEASTOPLEYEBRIGOODOETERELSOTERMINTBERLINCLOCKLONHADRWITNINERCHCAUSTE"
    },
    {
     "cls": "xstops",
     "q": -4.6289,
     "own_q": [
      -5.081,
      -5.0302,
      -4.9261,
      -5.0011,
      -4.8742,
      -5.049
     ],
     "q_found": true,
     "judge": 12,
     "own_judge": [
      8,
      12,
      12,
      12,
      12,
      12
     ],
     "judge_found": false,
     "letters_right": 41,
     "reading": "DRELLNOTDSAWHIMTHESBREASTNORTHEASTEADYFINTASSEHEPEOFANAGEELIMANBERLINCLOCKWEVESKNIGITIAMEOFNIFRUL"
    },
    {
     "cls": "xstops",
     "q": -4.5964,
     "own_q": [
      -4.7843,
      -4.8333,
      -4.8621,
      -4.8222,
      -4.779,
      -4.7826
     ],
     "q_found": true,
     "judge": 12,
     "own_judge": [
      12,
      12,
      6,
      12,
      18,
      12
     ],
     "judge_found": false,
     "letters_right": 50,
     "reading": "GIONSMTHEETOHATENTIMEEASTNORTHEASTHERTEREHARENTIDIPLOVEUTRDEMYOBERLINCLOCKINDIUMOKEWAGREREGIEMEDC"
    },
    {
     "cls": "k123",
     "q": -4.7899,
     "own_q": [
      -5.0919,
      -5.0758,
      -4.965,
      -5.1654,
      -5.0804,
      -5.2391
     ],
     "q_found": true,
     "judge": 12,
     "own_judge": [
      12,
      12,
      5,
      6,
      8,
      8
     ],
     "judge_found": false,
     "letters_right": 41,
     "reading": "IKEGREEASPECLEGIARFISEASTNORTHEASTWILDEREDIBRWOMOSTYHEDUCELPLAYBERLINCLOCKESOOZYIDIASTWISPOVEDABO"
    },
    {
     "cls": "k123",
     "q": -4.6645,
     "own_q": [
      -4.7117,
      -4.8337,
      -4.8078,
      -4.8508,
      -4.961,
      -4.9099
     ],
     "q_found": true,
     "judge": 12,
     "own_judge": [
      10,
      12,
      12,
      8,
      14,
      12
     ],
     "judge_found": false,
     "letters_right": 35,
     "reading": "PATRIENTOTEINGOFEAREVEASTNORTHEASTRALOWWHILANDAFRISECRLBRIENANSBERLINCLOCKCYNTOMYILYMOROFINATYUMU"
    },
    {
     "cls": "k123",
     "q": -4.4983,
     "own_q": [
      -4.7823,
      -4.7376,
      -4.7459,
      -4.8329,
      -4.7873,
      -4.5977
     ],
     "q_found": true,
     "judge": 15,
     "own_judge": [
      12,
      12,
      12,
      10,
      18,
      15
     ],
     "judge_found": false,
     "letters_right": 39,
     "reading": "IGPOSITYEINGTHEDTEESWEASTNORTHEASTHEARNORTHMONROMPREDORDEBYREUNBERLINCLOCKTISALHECTEACHEARFIGTOPP"
    },
    {
     "cls": "k123",
     "q": -4.7688,
     "own_q": [
      -4.9212,
      -4.8306,
      -4.7328,
      -4.6979,
      -4.8602,
      -4.9024
     ],
     "q_found": false,
     "judge": 12,
     "own_judge": [
      12,
      12,
      18,
      12,
      12,
      4
     ],
     "judge_found": false,
     "letters_right": 36,
     "reading": "ADRSEDSOGERTOSAGRENEVEASTNORTHEASTINGOUSEXPAINSIDESYMEAKUATIMDIBERLINCLOCKTOWNTOPFONSIOCLAPRIMRBA"
    },
    {
     "cls": "sub3",
     "q": -4.699,
     "own_q": [
      -4.8295,
      -4.8396,
      -4.9352,
      -4.8247,
      -4.768,
      -4.8769
     ],
     "q_found": true,
     "judge": 14,
     "own_judge": [
      12,
      12,
      8,
      12,
      18,
      12
     ],
     "judge_found": false,
     "letters_right": 33,
     "reading": "MMIGTHERRESUSICAROTHLEASTNORTHEASTTTITISOUCOMANYSQUOTCHOFWHENEDBERLINCLOCKATTHTMAUNCYSTIRAINHOHOK"
    },
    {
     "cls": "sub3",
     "q": -4.7594,
     "own_q": [
      -4.7921,
      -4.8675,
      -4.8461,
      -4.8875,
      -4.9556,
      -4.9038
     ],
     "q_found": true,
     "judge": 14,
     "own_judge": [
      14,
      12,
      8,
      8,
      12,
      15
     ],
     "judge_found": false,
     "letters_right": 36,
     "reading": "IBOLUMBARERTECHADAGEVEASTNORTHEASTTONYNETHEMYSHADPRIZESIRCAMOSTBERLINCLOCKKTOFAWNWEINERRTAINISENG"
    },
    {
     "cls": "sub3",
     "q": -4.8497,
     "own_q": [
      -4.8871,
      -4.8017,
      -4.9725,
      -4.9927,
      -5.0249,
      -4.9803
     ],
     "q_found": false,
     "judge": 12,
     "own_judge": [
      12,
      8,
      6,
      12,
      12,
      6
     ],
     "judge_found": false,
     "letters_right": 36,
     "reading": "ZAKKUNASHEENTCASSOMETEASTNORTHEASTDOWSAGENCYFLTINJAMPHONDANROUPBERLINCLOCKSEVELSIOSEDACCKFALPOSRE"
    },
    {
     "cls": "sub3",
     "q": -4.9625,
     "own_q": [
      -5.0314,
      -5.1024,
      -5.0498,
      -5.0867,
      -5.0737,
      -5.1098
     ],
     "q_found": true,
     "judge": 12,
     "own_judge": [
      12,
      10,
      7,
      12,
      12,
      8
     ],
     "judge_found": false,
     "letters_right": 43,
     "reading": "HPLAYWILSFLNADURNEDLYEASTNORTHEASTERBEADDTOLEAPSMARXCHERANGIMGEBERLINCLOCKPITCHHURHTELLLATWOWIFAT"
    }
   ],
   "quad_found": 9,
   "judge_found": 0,
   "of": 12,
   "by_class": {
    "xstops": {
     "quad": 3,
     "judge": 0,
     "of": 4
    },
    "k123": {
     "quad": 3,
     "judge": 0,
     "of": 4
    },
    "sub3": {
     "quad": 3,
     "judge": 0,
     "of": 4
    }
   },
   "stated_power": "5/5",
   "quad_below_stated": true,
   "judge_below_stated": true,
   "judge_none": 0
  },
  "0125": {
   "rows": [
    {
     "cls": "xstops",
     "q": -4.095,
     "q_found": true,
     "judge": 60,
     "judge_found": true,
     "window_letters_right": 24,
     "recovered": true,
     "reading": "EASTNORTHEASTBERLINCLOCK"
    },
    {
     "cls": "xstops",
     "q": -4.095,
     "q_found": true,
     "judge": 60,
     "judge_found": true,
     "window_letters_right": 24,
     "recovered": true,
     "reading": "EASTNORTHEASTBERLINCLOCK"
    },
    {
     "cls": "xstops",
     "q": -4.095,
     "q_found": true,
     "judge": 60,
     "judge_found": true,
     "window_letters_right": 24,
     "recovered": true,
     "reading": "EASTNORTHEASTBERLINCLOCK"
    },
    {
     "cls": "xstops",
     "q": -4.095,
     "q_found": true,
     "judge": 60,
     "judge_found": true,
     "window_letters_right": 24,
     "recovered": true,
     "reading": "EASTNORTHEASTBERLINCLOCK"
    },
    {
     "cls": "k123",
     "q": -4.095,
     "q_found": true,
     "judge": 60,
     "judge_found": true,
     "window_letters_right": 24,
     "recovered": true,
     "reading": "EASTNORTHEASTBERLINCLOCK"
    },
    {
     "cls": "k123",
     "q": -4.095,
     "q_found": true,
     "judge": 60,
     "judge_found": true,
     "window_letters_right": 24,
     "recovered": true,
     "reading": "EASTNORTHEASTBERLINCLOCK"
    },
    {
     "cls": "k123",
     "q": -4.095,
     "q_found": true,
     "judge": 60,
     "judge_found": true,
     "window_letters_right": 24,
     "recovered": true,
     "reading": "EASTNORTHEASTBERLINCLOCK"
    },
    {
     "cls": "k123",
     "q": -4.095,
     "q_found": true,
     "judge": 60,
     "judge_found": true,
     "window_letters_right": 24,
     "recovered": true,
     "reading": "EASTNORTHEASTBERLINCLOCK"
    },
    {
     "cls": "sub3",
     "q": -4.095,
     "q_found": true,
     "judge": 60,
     "judge_found": true,
     "window_letters_right": 24,
     "recovered": true,
     "reading": "EASTNORTHEASTBERLINCLOCK"
    },
    {
     "cls": "sub3",
     "q": -4.095,
     "q_found": true,
     "judge": 60,
     "judge_found": true,
     "window_letters_right": 24,
     "recovered": true,
     "reading": "EASTNORTHEASTBERLINCLOCK"
    },
    {
     "cls": "sub3",
     "q": -4.095,
     "q_found": true,
     "judge": 60,
     "judge_found": true,
     "window_letters_right": 24,
     "recovered": true,
     "reading": "EASTNORTHEASTBERLINCLOCK"
    },
    {
     "cls": "sub3",
     "q": -4.095,
     "q_found": true,
     "judge": 60,
     "judge_found": true,
     "window_letters_right": 24,
     "recovered": true,
     "reading": "EASTNORTHEASTBERLINCLOCK"
    }
   ],
   "quad_found": 12,
   "judge_found": 12,
   "of": 12,
   "by_class": {
    "xstops": {
     "quad": 4,
     "judge": 4,
     "of": 4
    },
    "k123": {
     "quad": 4,
     "judge": 4,
     "of": 4
    },
    "sub3": {
     "quad": 4,
     "judge": 4,
     "of": 4
    }
   },
   "stated_power": "11/20",
   "quad_below_stated": false,
   "judge_below_stated": false,
   "judge_none": 0,
   "copies_quad_max": -4.3004,
   "copies_judge": [
    7,
    22,
    12,
    6,
    8,
    8,
    8,
    12,
    12,
    15,
    12,
    12,
    15,
    12,
    12,
    6,
    12,
    12,
    7,
    12,
    14,
    15,
    15,
    12,
    10,
    8,
    4,
    6,
    12,
    6,
    6,
    8,
    12,
    8,
    12,
    12,
    14,
    8,
    12,
    12,
    12,
    22,
    8,
    8,
    22,
    12,
    6,
    12,
    8,
    8
   ],
   "copies_reproduced": true
  }
 },
 "compute_seconds": 4046,
 "exhaustive": false,
 "controls": "quadgram scores of the plants' own copies' readings (no candidate is submitted)"
}
```

Notes: 23: quadgram 10/12, judge 1/12 (stated 6/8); 13: quadgram 9/12, judge 0/12 (stated 5/5); 0125: quadgram 12/12, judge 12/12 (stated 11/20)


