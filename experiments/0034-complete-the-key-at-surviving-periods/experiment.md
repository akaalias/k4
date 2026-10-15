# 0034-complete-the-key-at-surviving-periods: Finish the job at the surviving periods: fix the 24 forced key letters, climb the rest by English, and see how English the text can get

**Family:** 1-keyed-periodic  
**Parent:** 0005-quagmire-period-sweep-forced-keys  
**Decision:** kept  
**Run:** 2026-10-15T07:51:28+00:00, 1408.0 s, status ran  
**Time by phase:** design 12 s, implement 89 s, test 14 s, run 1408 s, record 0 s

## In plain words

For a repeating secret word of length 27, 28 or 29, the 24 known letters fix 24 letters of the word and leave a few unknown. We fill the unknown ones in every way and read the message that comes out, keeping the one that reads most like English. If the cipher really were of this kind, one filling would read like a real message. We also run the same game on scrambled versions of the carved text, to see how English-looking a text can be made by filling alone.

## Walkthrough, by hand

1. Take period 27 and the sculpture's alphabet with Vigenere.
2. The 24 known letters force 24 of the 27 key letters; say slots 0, 9 and 17 are free.
3. Put any letters in the three free slots and decrypt all 97 letters.
4. Change slot 0 through A to Z, decrypting each time, and keep the letter that makes the 73 unknown letters read most like English.
5. Do the same for slots 9 and 17, then go round again until nothing changes.
6. Read the result.
7. Start again from different letters a few times and keep the best.

## Worked example (generated)

```
period 27, KRYPTOS alphabet throughout, Vigenere; 24 slots forced, 3 free, climbed by English (3 restarts)

key   YWOYNKYUYELYOIECBAQKMRDUMRI
text  PEUZYOVDEPTIPLQBAOHBOEASTNORTHEASTDYFGMRRCWXTSZAVWCXZYNGDOTILLSBERLINCLOCKOFKOAWIHFOGQKNNNVTCUQVM
English of the free letters -7.790 (English about -3.6, noise about -6.5)
```

## Lineage

Inherits from 0005-quagmire-period-sweep-forced-keys. What changed: The first experiment that produces full candidates. At every period the cribs allow (27-29, and 53-95 sampled every third) under the 24 conventions, the forced key slots are fixed and the free slots are chosen to maximise the English score of the other 73 letters. The question is how English the best text is, against the same procedure on shuffled K4.

## Hypothesis (domain expert)

0005 left periods 27-29 and 53-97 alive under every convention, and 0009 showed the forced key stretches are noise; but noise in the key is compatible with a real periodic cipher if the key is not a word. The remaining test is the plaintext: fix the 24 forced slots, choose the 3 to 73 free slots by coordinate descent on the quadgram score of the 73 non-crib letters, with twenty random restarts, and record the best score per period and convention. A true periodic cipher at one of these periods would give a text scoring near English, about -3.6, at that period and convention; the same climb on shuffled K4 calibrates what overfitting achieves, which rises with the number of free slots. Candidates are submitted; they pass the crib gate by construction, so the English deficit and the key cost carry the verdict, and a 27-letter random key costs about 67 points of loss on its own. Bounds: coordinate descent is not exhaustive above period 27; period 27 is close to exhaustive with twenty restarts over 3 free slots.

## Prediction

At periods 27-29 the best English score is below -5.0 per quadgram under every convention, the same as on shuffled K4, far from the -3.6 of English. At periods 53-97 the climb reaches -4.5 or better on both K4 and shuffled K4 because of the many free slots; the gap between them is under 0.2. Candidates pass the gates but carry a loss above 60 from the key cost; none reads as English.

## Method

1. For each convention and live period, force the key letters at the crib slots.
2. Start the free slots at random; repeat: for each free slot in turn, try all 26 letters and keep the one giving the best score of the non-crib letters; stop when a pass changes nothing.
3. Twenty restarts; keep the best.
4. Submit the best text per period as a candidate.
5. Repeat the whole procedure on three shuffles of K4.

## Result

Candidates returned: 18. Passed all gates: 18. Best crib hits among all candidates: 24/24
(EAST 4/4, NORTHEAST 9/9, BERLIN 6/6, CLOCK 5/5).
Best loss: 4.380566444030095 (0 is solved; 10 per missed crib letter). Best fitness: -7.289312943594226. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | pass | 24/24 | -7.880 | `RPRESIDENTHESTHERESANEASTNORTHEASTDERSTHEPRESINTHEREARENTHERETHBERLINCLOCKERESIDEDINGTHETHEREARTI` | period 95 key FALPWPOZKOFGDGYGYMDMJMCLWNQHMHLKFGXKQHZRHUEXABHQDWGHKKCPTKAYEAZBYHITCDFYZDATQMCOKGZPLSACOFWVNKB (71 free slots climbed); std/kry/kry/varbeau |
| 2 | pass | 24/24 | -7.791 | `OFORESTINTEDINTHEARENEASTNORTHEASTTHESTHESTHERENTERSANDINGANDINBERLINCLOCKGSTANDTHERENTERSARETHAL` | period 92 key KVUKDZQJQDDANGRPTOAWTRDUMRIYWOYNKYRJFXJMOHYMKZHSNVPDNXEUVQJVCWIELYOIECBAQKDASNSHKYXCTQVDGIKQ (68 free slots climbed); kry/kry/kry/vig |
| 3 | pass | 24/24 | -7.705 | `ISCOREATTHETHESTHEREAEASTNORTHEASTNDCONTHERESERINTHESTERANDERANBERLINCLOCKDRENTHEREARATERSTHEMARX` | period 89 key NACPMJYYGVZKPKXKWQZMXQRTPHIUUARAYZSHZSHZXYXKDEQHKALUSKZBPUATKMVUGUHMRUKAFKAEONSFIHNKGNTZF (65 free slots climbed); std/kry/std/beau |
| 4 | pass | 24/24 | -7.633 | `WAROUNTRETHEREATEDINTEASTNORTHEASTERESTOREASTEVERESANDINTHETHESBERLINCLOCKTATTHECONTHESTORATANAME` | period 86 key IZHXAZWDYMNTQMMIWYHMXZPBYXYCCUYQABQYIZDWIOIAPUWFVEZRDSOKLHILUZROGCQPUQMJNAXUQJIHJFLQZY (62 free slots climbed); std/std/std/varbeau |
| 5 | pass | 24/24 | -7.509 | `OAREACHALLIONTHEREINTEASTNORTHEASTHEWITHEARECOMENTHEREINTERESANBERLINCLOCKDRESTATINTHEDALECTINGMO` | period 83 key JSRDFXJVYXNXFNCNCSAFWSJRXTUOSORAMNCAZEZBOGLYRONFQMDORNNDEXUPZOFICOPEJKMCZKGEUSUCPSE (59 free slots climbed); std/kry/std/varbeau |
| 6 | pass | 24/24 | -7.467 | `BERSDATEDTOARELETHESTEASTNORTHEASTORESTHATTHEREATTHETHEAREANDINBERLINCLOCKTHERESANDITISREELETOURJ` | period 80 key XXZVLYUUDKQKHVOGLYXCTBKVSBPCXFCTACADMYQSJQCSAZOSTDQFWDKDOWQWJXPLRCFPLJIHUATZZZOS (56 free slots climbed); kry/kry/std/vig |
| 7 | pass | 24/24 | -7.345 | `TOVENOTHESTHERSTTHESAEASTNORTHEASTRERESIDENTERSAREARETOTHERATERBERLINCLOCKSONOFTHISFREETERSINEEDL` | period 77 key HSUPMCUYLTXJVEGYTUVDPMCLWNQHMHLKFGFKQKXYGDAGNLNRQWVRTYNCMWQEKMCBYHITCDFYZDURP (53 free slots climbed); std/kry/kry/varbeau |
| 8 | pass | 24/24 | -7.289 | `WHEUSHESTIONSTEONLYCOEASTNORTHEASTNTHETHESTATESTIMENTSANDINGATIBERLINCLOCKONTHEWARKENHISTHESOMESG` | period 74 key LGZVHKFBYMIMUHPSIHZMLQTELWEHGZUPFHUIBBFTXDHEKZNUABBJSOGDXEPUSRFOGHTTKPBKSD (50 free slots climbed); kry/std/kry/vig |
| 9 | pass | 24/24 | -7.448 | `HUKSALLTHAVICEFFICESAEASTNORTHEASTNATIONANDINATESTINANDATTHERESBERLINCLOCKENSTIONESERTERETOODSLCQ` | period 71 key KSDEGWSDMKXVMAYZNVJUIQTELWEHGZUPFHUFMTEZYWBPEPUHJVTJPMDVTVBWFQUOGHTTKPB (47 free slots climbed); kry/std/kry/vig |
| 10 | pass | 24/24 | -7.335 | `IRWAHOTALLISAREATHENTEASTNORTHEASTINANDSOMESANDINTHERENTHERSEARBERLINCLOCKSSIONESISSTINGETPVCHACT` | period 68 key SDHLGKTHUVFNRRDEIXWHPREZYPYXXSYDKZSSVSGKUTHKTWVLCAFONAADRVOJCODFQXDE (44 free slots climbed); std/std/kry/vig |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "periodic tableau at surviving periods, key completed by English climb",
 "conventions": 24,
 "periods": "27-29, then 53-95 every third",
 "restarts": 20,
 "best_by_period": {
  "27": {
   "english": -7.257,
   "convention": "kry/kry/std/beau",
   "free_slots": 3,
   "text": "ZWAWFAFIWGMGOGMDROTMAEASTNORTHEASTISTCDAPPUDSFROKLPDGBCUMLDWLBYBERLINCLOCKADHARIUHVWCQFISIQMNGDJK"
  },
  "28": {
   "english": -6.808,
   "convention": "kry/std/std/vig",
   "free_slots": 4,
   "text": "RYIHBKSCNNJARISEYUCCTEASTNORTHEASTWHCOFHCGDMXKAATSIXNHCIURRORLDBERLINCLOCKTHEJUFYFLIUAILUSCILVXVL"
  },
  "29": {
   "english": -6.709,
   "convention": "kry/kry/std/beau",
   "free_slots": 5,
   "text": "YJAEIVIZKOYDBEACIOSSLEASTNORTHEASTVCACZLEVESITMILANBACMIIXDCHKYBERLINCLOCKATTHIZQLLPDLOFDFOIJGUSM"
  },
  "53": {
   "english": -5.108,
   "convention": "std/std/kry/beau",
   "free_slots": 29,
   "text": "PATEOVERSCURFONVGFSQYEASTNORTHEASTARELEDFEATHESTHEPRESHANINTSTIBERLINCLOCKNFGEEHNBSHCEBUDGEARESSU"
  },
  "56": {
   "english": -4.781,
   "convention": "kry/std/std/varbeau",
   "free_slots": 32,
   "text": "ISINGHICNNJARISEYUNDEEASTNORTHEASTNETINTHEREINTEDTOTHERECORDSONBERLINCLOCKHIMJUFYFLIUAILUSOFFSOFV"
  },
  "59": {
   "english": -5.034,
   "convention": "kry/std/kry/beau",
   "free_slots": 35,
   "text": "RROURUNXYOROCSVIOLEISEASTNORTHEASTANDINTHERATINGTHESTINTERSAIDEBERLINCLOCKTANYLOWCUVRISRQWLTMEDSL"
  },
  "62": {
   "english": -4.902,
   "convention": "kry/std/kry/vig",
   "free_slots": 38,
   "text": "YVWPJDWEXAHRENTERNINOEASTNORTHEASTTHEPARTERANDANDINTHECONTERATIBERLINCLOCKSANDMEARECTUNWVSGUCAJFA"
  },
  "65": {
   "english": -4.313,
   "convention": "kry/kry/kry/beau",
   "free_slots": 41,
   "text": "ZONVSENAGRAYSTEDITSUREASTNORTHEASTESINTHERATIONANDTHESTIONSIDERBERLINCLOCKMICHEMWHATHEWPNOSTNOXLS"
  },
  "68": {
   "english": -4.04,
   "convention": "std/std/kry/vig",
   "free_slots": 44,
   "text": "IRWAHOTALLISAREATHENTEASTNORTHEASTINANDSOMESANDINTHERENTHERSEARBERLINCLOCKSSIONESISSTINGETPVCHACT"
  },
  "71": {
   "english": -4.008,
   "convention": "kry/std/kry/vig",
   "free_slots": 47,
   "text": "HUKSALLTHAVICEFFICESAEASTNORTHEASTNATIONANDINATESTINANDATTHERESBERLINCLOCKENSTIONESERTERETOODSLCQ"
  },
  "74": {
   "english": -3.704,
   "convention": "kry/std/kry/vig",
   "free_slots": 50,
   "text": "WHEUSHESTIONSTEONLYCOEASTNORTHEASTNTHETHESTATESTIMENTSANDINGATIBERLINCLOCKONTHEWARKENHISTHESOMESG"
  },
  "77": {
   "english": -3.614,
   "convention": "std/kry/kry/varbeau",
   "free_slots": 53,
   "text": "TOVENOTHESTHERSTTHESAEASTNORTHEASTRERESIDENTERSAREARETOTHERATERBERLINCLOCKSONOFTHISFREETERSINEEDL"
  },
  "80": {
   "english": -3.59,
   "convention": "kry/kry/std/vig",
   "free_slots": 56,
   "text": "BERSDATEDTOARELETHESTEASTNORTHEASTORESTHATTHEREATTHETHEAREANDINBERLINCLOCKTHERESANDITISREELETOURJ"
  },
  "83": {
   "english": -3.487,
   "convention": "std/kry/std/varbeau",
   "free_slots": 59,
   "text": "OAREACHALLIONTHEREINTEASTNORTHEASTHEWITHEARECOMENTHEREINTERESANBERLINCLOCKDRESTATINTHEDALECTINGMO"
  },
  "86": {
   "english": -3.466,
   "convention": "std/std/std/varbeau",
   "free_slots": 62,
   "text": "WAROUNTRETHEREATEDINTEASTNORTHEASTERESTOREASTEVERESANDINTHETHESBERLINCLOCKTATTHECONTHESTORATANAME"
  },
  "89": {
   "english": -3.392,
   "convention": "std/kry/std/beau",
   "free_slots": 65,
   "text": "ISCOREATTHETHESTHEREAEASTNORTHEASTNDCONTHERESERINTHESTERANDERANBERLINCLOCKDRENTHEREARATERSTHEMARX"
  },
  "92": {
   "english": -3.334,
   "convention": "kry/kry/kry/vig",
   "free_slots": 68,
   "text": "OFORESTINTEDINTHEARENEASTNORTHEASTTHESTHESTHERENTERSANDINGANDINBERLINCLOCKGSTANDTHERENTERSARETHAL"
  },
  "95": {
   "english": -3.277,
   "convention": "std/kry/kry/varbeau",
   "free_slots": 71,
   "text": "RPRESIDENTHESTHERESANEASTNORTHEASTDERSTHEPRESINTHEREARENTHERETHBERLINCLOCKERESIDEDINGTHETHEREARTI"
  }
 },
 "shuffled_k4_best_by_period": {
  "27": -6.831,
  "28": -6.886,
  "29": -6.51,
  "53": -4.88,
  "60": -4.771,
  "70": -4.018,
  "80": -3.564,
  "97": -3.234
 },
 "english_reference": -3.6
}
```

Notes: Best English at 27-29: [-7.257, -6.808, -6.709]; shuffled K4 at 27-29: [-6.831, -6.886, -6.51]. Best overall -3.277 at period 95 vs shuffled best -3.233920610278189.


