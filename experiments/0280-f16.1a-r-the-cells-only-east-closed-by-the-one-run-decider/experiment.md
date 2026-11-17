# 0280-f16.1a-r-the-cells-only-east-closed-by-the-one-run-decider: F16.1a-r: the free-alphabet cells only EAST closed (0274: K4 fits on the 20 official letters at key lengths 6-26, 0-2 slips), each decided by D1's one-run English decider: K4 climbed once, then fitting shuffles one at a time (at most 12, or 100 while K4 keeps winning); 24 plants

**Family:** 16-simple-hand-methods  
**Parent:** 0253-f1.4-one-alphabet-residue-decided-by-the-one-run-decider  
**Decision:** reverted  
**Run:** 2026-11-17T16:32:21+00:00, 1630.3 s, status ran  
**Time by phase:** test 18 s, run 1630 s, record 0 s

## In plain words

Without EAST, the K1/K2 kind of cipher with a scrambled alphabet fits the carving at a few key lengths where it did not before. Those fits cannot be told apart by the known letters alone, so we let a search build the most English-looking message for each, and do the same on scrambled copies that fit the same way. If the carving's message reads better than the copies' more often than chance, that length is worth a closer look.

## Walkthrough, by hand

1. Take one setting, say Beaufort, key length 11, no slip.
2. Let a search choose the scrambled alphabet and the 11 key letters to make K4's message as English as possible while NORTHEAST, BERLIN and CLOCK stay in place.
3. Scramble K4's letters until the scramble also fits length 11 with some alphabet; run the same search on it.
4. If the scramble reads as well as K4, stop: K4 is not special at this setting.
5. If K4 beats 12 scrambles in a row, it is unusual at the 1 in 13 level; go on to 100.
6. Do this for every setting and count the wins.

## Worked example (generated)

```
F16.1a-r: one free alphabet, a periodic key, the 20 official known letters; one setting at a time.

  setting      Beaufort, key length 11, no slip (0274: fits on 20 letters, not on 24)
  K4           one tempering search for the most English reading with NORTHEAST, BERLIN, CLOCK in place
  copies       scrambles of K4 that also fit length 11, one search each, until one reads as well as K4
  verdict      K4 beating 12 in a row happens 1 time in 13 by chance; count over all settings
```

## Lineage

Inherits from 0253-f1.4-one-alphabet-residue-decided-by-the-one-run-decider. What changed: F16.1a-r (issue #123): the settings come from 0274 (one free alphabet, periodic key, every minimal set of 0-2 slipped places where K4 fits the 20 official letters and not the 24); the decider is 0253's (0252's generalised 0140 tempering climb, copies drawn as shuffles that fit the same setting exactly), with the known letters the setting's own (the 20 official ones minus its slips, nk passed to the climb) instead of the 24. EAST's places (22-25) are read, not fixed.

## Hypothesis (domain expert)

F1.1/F1.6 with EAST set aside (#124): Quagmire III with an unknown alphabet (C27(c)), Beaufort or added, key length L. 0274 found 20 (cell, slip count) pairs where some alphabet satisfies the 20 official equations (less the slipped ones) on K4 though none satisfies all 24; 0136: a free alphabet leaves about 88 bits the known letters cannot fix, so English decides. D1 (0228, 0229; Alexis 2026-10-28, #100): one tempering run with copies climbed one at a time qualifies for one free alphabet. Per setting the null is that K4 beats all 12 fitting copies with probability 1/13; the verdict is the count against Binomial(n, 1/13) and, per setting, K4 above 100 copies at 1/101.

## Prediction

K4 beats all 12 copies in about n/13 settings (no excess beyond the binomial 1% tail) and all 100 in none or one; plants (clean Carter, and Sanborn-style X stops, K1-K3 windows, three changed letters) found about 2 in 3 at these lengths (fewer at 22-26). Zero candidates: the verdict is the count.

## Method

1. Settings: every (L, form, slipped places) from 0274's record where K4 fits on 20 letters and the cell is listed as only EAST closed, at its minimal slip count.
2. For each: the known letters are the 20 official ones less the slipped places.
3. Climb K4 once (0140's tempering, 16 x 625 x 1000, 0252's slot-map version); then shuffles of K4 that fit the setting exactly, climbed one at a time, stop at the first at or above K4; at most 12, 100 while K4 beats all.
4. Plants: 12 clean, 12 Sanborn-style, on settings drawn from the list, slips planted where the setting has them; found when above all 12 own copies.
5. Count against Binomial(n, 1/13).

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
 "item": "F16.1a-r",
 "settings": 49,
 "cells": [
  "B10",
  "B11",
  "B12",
  "B14",
  "B16",
  "B21",
  "B22",
  "B24",
  "B25",
  "B6",
  "B8",
  "B9",
  "V10",
  "V11",
  "V13",
  "V14",
  "V21",
  "V22",
  "V25",
  "V26"
 ],
 "decider": "0253's: 0252's generalised 0140 tempering (16 x 625 x 1000), copies = shuffles that fit the setting exactly on its own known letters, one at a time, stop at the first at or above K4, at most 12, 100 while K4 wins",
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
 "k4_above_all_12": 6,
 "expected_by_chance_12": 3.77,
 "binomial_p_12": 0.17251139872198787,
 "k4_above_all_100": 2,
 "expected_by_chance_100": 0.49,
 "binomial_p_100": 0.084962372725599,
 "per_setting": [
  {
   "cell": "V10",
   "slips": [
    73,
    74
   ],
   "above": 100,
   "copies_climbed": 100,
   "score": -5.61821,
   "copies_max": -5.63398,
   "lost": 0,
   "reading": "CDKLDCBCBETHBTROYGINFOLLKNORTHEASTRIVISOXISTTJULPLISKADAYSPMWOBBERLINCLOPCHEFJFGISCYSEPTCASBECBSS",
   "east_at_22_25": "OLLK"
  },
  {
   "cell": "B10",
   "slips": [
    69
   ],
   "above": 100,
   "copies_climbed": 100,
   "score": -5.77579,
   "copies_max": -5.86211,
   "lost": 0,
   "reading": "XTWAILFLONYSDTOOIMIKCOLANNORTHEASTOITISARHSTYHHJPSNEWDICIEPQTODBERLIRCLOCKZSAHADNEPLUSSUEVIDRKBEB",
   "east_at_22_25": "OLAN"
  },
  {
   "cell": "B9",
   "slips": [
    28,
    72
   ],
   "above": 60,
   "copies_climbed": 61,
   "score": -5.97807,
   "copies_max": -5.97776,
   "lost": 0,
   "reading": "OIZANDAAWTHECVDUMENIFYGAKNOCTHEASTAKSRSSPWTCFRPKQKNEDYALAREKYHABERLINCLECKFEMIOTKINDKLILFRUHLICRG",
   "east_at_22_25": "YGAK"
  },
  {
   "cell": "B10",
   "slips": [
    29
   ],
   "above": 40,
   "copies_climbed": 41,
   "score": -5.8385,
   "copies_max": -5.71439,
   "lost": 0,
   "reading": "JHIESOROSNAXLTCLEZVKTOBEANORWHEASTCIAIMLOISTYSYFRJWEIUSHEGRUROLBERLINCLOCKPANSOFWEPINAGBEIUWEKOGX",
   "east_at_22_25": "OBEA"
  },
  {
   "cell": "B9",
   "slips": [
    27,
    28
   ],
   "above": 15,
   "copies_climbed": 16,
   "score": -6.04679,
   "copies_max": -5.95098,
   "lost": 0,
   "reading": "AGFRYOWSHSALAGOGGONGMFOMBNDCTHEASTSUKRSKMYTOVWXUDKNEDALHDBWLAMIBERLINCLOCKMENUDRUYSINSUIETOABSCEK",
   "east_at_22_25": "FOMB"
  },
  {
   "cell": "B11",
   "slips": [],
   "above": 13,
   "copies_climbed": 14,
   "score": -5.84176,
   "copies_max": -5.66185,
   "lost": 0,
   "reading": "ORRFWFOCEDCVRATZELENQOVBYNORTHEASTENANGMSATSYPLEUHRSIVCHTSACKLEBERLINCLOCKDBYAFGODUNDEACDDSSPNPYO",
   "east_at_22_25": "OVBY"
  },
  {
   "cell": "V10",
   "slips": [
    33,
    74
   ],
   "above": 6,
   "copies_climbed": 7,
   "score": -5.71482,
   "copies_max": -5.64653,
   "lost": 0,
   "reading": "JPINKMFMUFFYOTRWASKUCOUNWNORTHEANTRINICOPHNTHUDHENONIGKCATEWIOOBERLINCLOCOLFTUBMONSETFEPGARTAODTU",
   "east_at_22_25": "OUNW"
  },
  {
   "cell": "B14",
   "slips": [
    74
   ],
   "above": 5,
   "copies_climbed": 6,
   "score": -5.58755,
   "copies_max": -5.56186,
   "lost": 0,
   "reading": "ULTTNIKLUKCHHDUBIDAKNSTPLNORTHEASTAYSOMEXYMRGATANELEBHASEAJEUPEBERLINCLOCALDTIVASUSSEETOECOZYHUGY",
   "east_at_22_25": "STPL"
  },
  {
   "cell": "B8",
   "slips": [
    28,
    29
   ],
   "above": 5,
   "copies_climbed": 6,
   "score": -6.16208,
   "copies_max": -6.13048,
   "lost": 0,
   "reading": "IEDGULAFWAPVIGNTOFFFSUZVANOUKHEASTQISAMEKNJJEELIGHISROCXOHETTUDBERLINCLOCKERVELDDOZKBSWMFDYPEEUKX",
   "east_at_22_25": "UZVA"
  },
  {
   "cell": "B6",
   "slips": [
    30,
    74
   ],
   "above": 4,
   "copies_climbed": 5,
   "score": -6.73934,
   "copies_max": -6.53967,
   "lost": 0,
   "reading": "QMYPDFUSEVDUROQUQORMDOZPLNORTBEASTOSDIOTPQSOGGLEDKNIKUXEFDAJTRRBERLINCLOCADKUGHHNIBAFUYLGLAGGGBDB",
   "east_at_22_25": "OZPL"
  },
  {
   "cell": "B8",
   "slips": [
    29,
    34
   ],
   "above": 3,
   "copies_climbed": 4,
   "score": -6.41644,
   "copies_max": -6.01499,
   "lost": 0,
   "reading": "ILZPPSPFHEPBAOFZOAALERZHMNORYHEASCQIEPTURNDCWELLDFNYZGSCOFETTRNBERLINCLOCKEDSELPLYHGILASGWBWWEDKJ",
   "east_at_22_25": "RZHM"
  },
  {
   "cell": "B6",
   "slips": [
    30,
    32
   ],
   "above": 3,
   "copies_climbed": 4,
   "score": -6.49716,
   "copies_max": -6.3463,
   "lost": 0,
   "reading": "SCCPOFTAYZODWGQDFOWCWOZPLNORTBEKSTUSBIOTNYOGAILHBONEDDIPVUCKYLLBERLINCLOCKWVKIKJNEWLUSCAVARHAIWUA",
   "east_at_22_25": "OZPL"
  },
  {
   "cell": "B8",
   "slips": [
    68,
    69
   ],
   "above": 2,
   "copies_climbed": 3,
   "score": -6.29883,
   "copies_max": -6.2652,
   "lost": 0,
   "reading": "VLYPGRAFXWEBKEYGIGGLLUZJONORTHEASTQSLAPDANNTDDLERUTEBITSIUACCURBERLSRCLOCKAFEDLMQECOOPMCUAWADDVKW",
   "east_at_22_25": "UZJO"
  },
  {
   "cell": "B6",
   "slips": [
    32,
    64
   ],
   "above": 2,
   "copies_climbed": 3,
   "score": -6.4,
   "copies_max": -6.14596,
   "lost": 0,
   "reading": "ZBIPOFFCXNOURAQUVORBBOZPLNORTHEKSTUSJIOTKYIALALIJSNEJUHFKKAZADWHERLINCLOCKBDDAORNECGSUILFLNGLACKB",
   "east_at_22_25": "OZPL"
  },
  {
   "cell": "B6",
   "slips": [
    28,
    74
   ],
   "above": 2,
   "copies_climbed": 3,
   "score": -6.81298,
   "copies_max": -6.52835,
   "lost": 0,
   "reading": "OFFRIFJSVPIGAOQUUOAFRZZPLNOHTHEASTDCWIOTJUNOEILEWKNAGGKJYJBISBHBERLINCLOCARDOVDLNANYQRFLAQBPEINSM",
   "east_at_22_25": "ZZPL"
  },
  {
   "cell": "V21",
   "slips": [
    74
   ],
   "above": 1,
   "copies_climbed": 2,
   "score": -4.98251,
   "copies_max": -4.93947,
   "lost": 0,
   "reading": "IKOCKPUSERSLURPATIMANEGDLNORTHEASTINECOUNDRINEVESOLGALLASSESHSLBERLINCLOCAWBABMINGORYRODUFFEINPAK",
   "east_at_22_25": "EGDL"
  },
  {
   "cell": "V22",
   "slips": [
    30
   ],
   "above": 1,
   "copies_climbed": 2,
   "score": -5.05293,
   "copies_max": -4.9643,
   "lost": 0,
   "reading": "ITHSKELOESUCHORWEELIPOFEYNORTNEASTEVEDATIOICACARDLEJANUOADERWELBERLINCLOCKOEDHISHEPOTFUNWASOYBOAD",
   "east_at_22_25": "OFEY"
  },
  {
   "cell": "B16",
   "slips": [],
   "above": 1,
   "copies_climbed": 2,
   "score": -5.45311,
   "copies_max": -5.24951,
   "lost": 0,
   "reading": "TJIGSICFLEINLYISGAOFIAZISNORTHEASTBIISEHENATERWOLFAYONJEHUDONWJBERLINCLOCKDEIRWTOBHOWERNIASXERMKB",
   "east_at_22_25": "AZIS"
  },
  {
   "cell": "B12",
   "slips": [
    30
   ],
   "above": 1,
   "copies_climbed": 2,
   "score": -5.79361,
   "copies_max": -5.77889,
   "lost": 0,
   "reading": "QIDPWTHUYBATTFQSPGALDNZDANORTBEASTELETOLBYCYARLWEDBASSJPOPSINSTBERLINCLOCKEFHEOENDTRYODUDUBOARTAX",
   "east_at_22_25": "NZDA"
  },
  {
   "cell": "B12",
   "slips": [
    28
   ],
   "above": 1,
   "copies_climbed": 2,
   "score": -5.90325,
   "copies_max": -5.79815,
   "lost": 0,
   "reading": "IONSWGSLPESKHXQALKOPJIZISNOFTHEASTPPDCORFYXHINLEDUSEDBAYEANREWDBERLINCLOCKYIKFRENGAHOENUGMUNINABU",
   "east_at_22_25": "IZIS"
  },
  {
   "cell": "B8",
   "slips": [
    28,
    69
   ],
   "above": 1,
   "copies_climbed": 2,
   "score": -6.04233,
   "copies_max": -6.03113,
   "lost": 0,
   "reading": "GFPQASIFOGNUPOFZIBBADEZCDNONTHEASTQIDGHURNYJMILLHCHSGASPICETJENBERLIRCLOCKEDWILINICGSTASWEZLMIRKJ",
   "east_at_22_25": "EZCD"
  },
  {
   "cell": "B8",
   "slips": [
    34,
    69
   ],
   "above": 1,
   "copies_climbed": 2,
   "score": -6.35393,
   "copies_max": -5.88625,
   "lost": 0,
   "reading": "OSXPMTRFMGEONQMIDDDSPAZTNNORTHEASBQIPOHCUNTBDELYKESYADIEDEWTBAYBERLIRCLOCKWHEELVBYAFLYNMFUCUDEWKA",
   "east_at_22_25": "AZTN"
  },
  {
   "cell": "B8",
   "slips": [
    29,
    66
   ],
   "above": 1,
   "copies_climbed": 2,
   "score": -6.36935,
   "copies_max": -6.35792,
   "lost": 0,
   "reading": "JORPOSSFFUDGDOOGHFFNYIZPNNORMHEASTQIYZJUONCUSELYDRHEZAIDHRATTIVBEWLINCLOCKALBELHALSDLUPSIHWSSERKX",
   "east_at_22_25": "IZPN"
  },
  {
   "cell": "B6",
   "slips": [
    64,
    74
   ],
   "above": 1,
   "copies_climbed": 2,
   "score": -6.48391,
   "copies_max": -6.29279,
   "lost": 0,
   "reading": "RJPPOFKWMNOUSLQUIOSJROZPLNORTHEASTUSMIOTQXBLFELVMKNAHUFFUJAYJDAHERLINCLOCARWMEDMNANBAYPLKLICFENJO",
   "east_at_22_25": "OZPL"
  },
  {
   "cell": "B6",
   "slips": [
    28,
    32
   ],
   "above": 1,
   "copies_climbed": 2,
   "score": -6.77626,
   "copies_max": -6.26551,
   "lost": 0,
   "reading": "QJDKOFMYEVOSRUQEWORJUIZPLNOZTHEKSTUGUIOTAXSUGRLIUVNDFSWCAUIZTZRBERLINCLOCKUYBEHRNDHMAMDACCISGRHWB",
   "east_at_22_25": "IZPL"
  },
  {
   "cell": "B6",
   "slips": [
    32,
    66
   ],
   "above": 1,
   "copies_climbed": 2,
   "score": -6.8111,
   "copies_max": -6.53999,
   "lost": 0,
   "reading": "QEZPAFISEVASUOQADOUERDZELNORTHEKSTMARIOTSYSOGULPRDNWFSBAXLXCTJUBEZLINCLOCKRIIJKUNWBXXZZKGWAXGUBTW",
   "east_at_22_25": "DZEL"
  },
  {
   "cell": "V25",
   "slips": [],
   "above": 0,
   "copies_climbed": 1,
   "score": -4.82823,
   "copies_max": -4.77616,
   "lost": 0,
   "reading": "IZATEDOORAIREGATOMOANOURINORTHEASTINDOURUNCRPJSAWREMAREPLAYOFVEBERLINCLOCKEMSAIDSUCOOLETTICBOUTUL",
   "east_at_22_25": "OURI"
  },
  {
   "cell": "B25",
   "slips": [],
   "above": 0,
   "copies_climbed": 1,
   "score": -4.87735,
   "copies_max": -4.69855,
   "lost": 0,
   "reading": "TRETATRALAMMEHSBUYSFNONTONORTHEASTRIAGEOGOLBORPOODOSELALCOMECHEBERLINCLOCKHEMEMCOURPERTOSANIAOMJY",
   "east_at_22_25": "ONTO"
  },
  {
   "cell": "V22",
   "slips": [
    74
   ],
   "above": 0,
   "copies_climbed": 1,
   "score": -4.99239,
   "copies_max": -4.91222,
   "lost": 0,
   "reading": "ARTOGEBLEFUNDONBATOTFOGTONORTHEASTWREETHESTAMWEHHMITHCUHLEEASTOBERLINCLOCIPIDDINOFORGEDDRGURANNGI",
   "east_at_22_25": "OGTO"
  },
  {
   "cell": "B24",
   "slips": [],
   "above": 0,
   "copies_climbed": 1,
   "score": -5.0035,
   "copies_max": -5.00021,
   "lost": 0,
   "reading": "TEDPHOTHTINTHIRADHERAAZENNORTHEASTALOATEANAMCOLIUSTTOLUCERIZERNBERLINCLOCKEINCPTGYHASMIXRDSACONDD",
   "east_at_22_25": "AZEN"
  },
  {
   "cell": "B22",
   "slips": [],
   "above": 0,
   "copies_climbed": 1,
   "score": -5.01538,
   "copies_max": -4.92841,
   "lost": 0,
   "reading": "SHCEWFIEESERSATTINANGOVERNORTHEASTODILLYROMSPDDAULRWOFEDESINUNABERLINCLOCKSPCINGOATRISTEDSESCNPST",
   "east_at_22_25": "OVER"
  },
  {
   "cell": "V26",
   "slips": [],
   "above": 0,
   "copies_climbed": 1,
   "score": -5.01701,
   "copies_max": -4.81645,
   "lost": 0,
   "reading": "YCRAPEXEMPTCCARASREENFISONORTHEASTHANYPATTELAULZERBUSTYTOFWGLIEBERLINCLOCKEWARISSENSICWEWRINKCRTY",
   "east_at_22_25": "FISO"
  },
  {
   "cell": "V21",
   "slips": [
    32
   ],
   "above": 0,
   "copies_climbed": 1,
   "score": -5.13158,
   "copies_max": -4.91175,
   "lost": 0,
   "reading": "GYTYRANSSFULATFEDERITYNOLNORTHEKSTREPLAWRUFIGHAEADILKLONTREMIWEBERLINCLOCKWENSUOPESORTTAUBBETICAP",
   "east_at_22_25": "YNOL"
  },
  {
   "cell": "B21",
   "slips": [
    74
   ],
   "above": 0,
   "copies_climbed": 1,
   "score": -5.13243,
   "copies_max": -5.0436,
   "lost": 0,
   "reading": "GPORWQBEDMETALAFICADUTIPLNORTHEASTOECONTANZKANMANDCOATITHISTOURBERLINCLOCAOFTRDHILLSMGOSEVEYLLOCY",
   "east_at_22_25": "TIPL"
  },
  {
   "cell": "B21",
   "slips": [
    32
   ],
   "above": 0,
   "copies_climbed": 1,
   "score": -5.20722,
   "copies_max": -5.03812,
   "lost": 0,
   "reading": "CDOWBQUOSISOLDTOKTANTISPLNORTHEKSTHOHEHEWARLATGDSAMAKOASAFULLIKBERLINCLOCKHISLEOFOODFFONOFEIDSAFO",
   "east_at_22_25": "ISPL"
  },
  {
   "cell": "V14",
   "slips": [
    74
   ],
   "above": 0,
   "copies_climbed": 1,
   "score": -5.57085,
   "copies_max": -5.54735,
   "lost": 0,
   "reading": "SRIOURCETTHEALSCHVBULKROLNORTHEASTROOSIDHHAMSAZOLLWMZEKERUMDNBUBERLINCLOCAWAISIKESSERBIBHEKCFAROU",
   "east_at_22_25": "KROL"
  },
  {
   "cell": "V14",
   "slips": [
    32
   ],
   "above": 0,
   "copies_climbed": 1,
   "score": -5.64973,
   "copies_max": -5.60269,
   "lost": 0,
   "reading": "BFORUGBUKTHELOBEVFBOIAFALNORTHEKSTSDPGEMUSEMIKZMISAYMEREMUZINCEBERLINCLOCKWAFOCLOBSEMWOUHERMOIDUK",
   "east_at_22_25": "AFAL"
  },
  {
   "cell": "B14",
   "slips": [
    32
   ],
   "above": 0,
   "copies_climbed": 1,
   "score": -5.65891,
   "copies_max": -5.63948,
   "lost": 0,
   "reading": "HUSREGUTOTBAIGHVANWKSRJPLNORTHEKSTDOIHRVRASKGKLASUSESAHIPITHAMABERLINCLOCKBOOMALWWEIPESTONBAYUPLJ",
   "east_at_22_25": "RJPL"
  },
  {
   "cell": "V13",
   "slips": [
    33
   ],
   "above": 0,
   "copies_climbed": 1,
   "score": -5.70795,
   "copies_max": -5.67436,
   "lost": 0,
   "reading": "ESRANSPHGBYGUGEKOSRLIFPUSNORTHEATTOREANGNAIOGJEZSTAAITSVUHINNINBERLINCLOCKSLYTHUIZVENDKHOROCKRDKN",
   "east_at_22_25": "FPUS"
  },
  {
   "cell": "V11",
   "slips": [
    33,
    74
   ],
   "above": 0,
   "copies_climbed": 1,
   "score": -5.74082,
   "copies_max": -5.71609,
   "lost": 0,
   "reading": "ALDKZGEMENAPLEVICLOGFOPNINORTHEANTXNIEVAACINNOPAHIVALSASUGIMPLOBERLINCLOCEQUECCTUFTOSEAARHGEASQKA",
   "east_at_22_25": "OPNI"
  },
  {
   "cell": "V11",
   "slips": [
    66,
    74
   ],
   "above": 0,
   "copies_climbed": 1,
   "score": -5.74633,
   "copies_max": -5.69213,
   "lost": 0,
   "reading": "FCWXFELUEJUICCUCLATHOFIDINORTHEASTGNSMMEEDUSOFKADDOEVPUAYOSNCATBEPLINCLOCOINDYEALITIKEAUXPORKJFMM",
   "east_at_22_25": "FIDI"
  },
  {
   "cell": "B12",
   "slips": [
    64
   ],
   "above": 0,
   "copies_climbed": 1,
   "score": -5.76141,
   "copies_max": -5.60987,
   "lost": 0,
   "reading": "NINPUTTRMENNUFQBGWWYANZAENORTHEASTSUSTOUSMYDULLESUHEMBJSJOTMOSEHERLINCLOCKICAZONNDAYDONSOSPVULARK",
   "east_at_22_25": "NZAE"
  },
  {
   "cell": "V11",
   "slips": [
    30,
    66
   ],
   "above": 0,
   "copies_climbed": 1,
   "score": -5.79035,
   "copies_max": -5.70047,
   "lost": 0,
   "reading": "FAPDRBGOETUEAMBYHEBALFENANORTNEASTUNFINDJOYSACOISERJCGURVSFVMEBBEPLINCLOCKSNDDLESPTSIEAUIRSAKYPAN",
   "east_at_22_25": "FENA"
  },
  {
   "cell": "B12",
   "slips": [
    66
   ],
   "above": 0,
   "copies_climbed": 1,
   "score": -5.833,
   "copies_max": -5.70492,
   "lost": 0,
   "reading": "YDEPQSHBMEYCRAQQHEDOANZEANORTHEASTHHTYOFAYADORLATSGDGLUSULKSGMWBEILINCLOCKBAODPENIANDEEMIRSLORAZB",
   "east_at_22_25": "NZEA"
  },
  {
   "cell": "V13",
   "slips": [
    72
   ],
   "above": 0,
   "copies_climbed": 1,
   "score": -5.89766,
   "copies_max": -5.80418,
   "lost": 0,
   "reading": "TYAATGXDGDRULATPESCBOFFUKNORTHEASTOGISNADYBYRKIZEOSQUEJIMNWANIMBERLINCLFCKENOTNBIGFSISKALFICMATGT",
   "east_at_22_25": "FFUK"
  },
  {
   "cell": "V11",
   "slips": [
    30,
    33
   ],
   "above": 0,
   "copies_climbed": 1,
   "score": -5.9175,
   "copies_max": -5.63948,
   "lost": 0,
   "reading": "PRBLYDBOEDPAREGINEBSMOAARNORTNEAITKNEBMOJAWINVWSHUPJNUPREOERCEBBERLINCLOCKLLADTYMUTSIEAPOOOHALUAM",
   "east_at_22_25": "OAAR"
  },
  {
   "cell": "B8",
   "slips": [
    29,
    68
   ],
   "above": 0,
   "copies_climbed": 1,
   "score": -6.36005,
   "copies_max": -6.24303,
   "lost": 0,
   "reading": "NWCPMIXFLDPYDBBLDMMWITZDMNOREHEASTQSIFFIUNDTRELEFUTIZXDRDUNJTTOBERLSNCLOCKNZBELPHIKHWAPTTAIAREAKA",
   "east_at_22_25": "TZDM"
  },
  {
   "cell": "B8",
   "slips": [
    66,
    69
   ],
   "above": 0,
   "copies_climbed": 1,
   "score": -6.46134,
   "copies_max": -5.63868,
   "lost": 0,
   "reading": "IMPPNLOFBUNNXQXMOXXVDIZZKNORTHEASTQIDATEDNFWIELRURRFPOATORDTUIPBEDLIRCLOCKDOWELGHEHEEDYCTHZMIEIKX",
   "east_at_22_25": "IZZK"
  },
  {
   "cell": "B6",
   "slips": [
    66,
    74
   ],
   "above": 0,
   "copies_climbed": 1,
   "score": -6.60976,
   "copies_max": -6.33696,
   "lost": 0,
   "reading": "ZGIPWFSRWZWBDEQGOODGGAZILNORTHEASTIZKIOTBAXEVELTKKNDHBYZKFURALMBEKLINCLOCAGLFPOWNDAVIBIUKSNPVEAQR",
   "east_at_22_25": "AZIL"
  }
 ],
 "plants": {
  "clean_found": [
   7,
   12
  ],
  "sanborn_found": [
   9,
   12
  ],
  "each": {
   "0": {
    "cls": "clean",
    "cell": "B21",
    "slips": [
     32
    ],
    "found": false,
    "above": 2,
    "score": -4.93037,
    "letters_right": 28
   },
   "1": {
    "cls": "clean",
    "cell": "V11",
    "slips": [
     66,
     74
    ],
    "found": true,
    "above": 12,
    "score": -5.45719,
    "letters_right": 34
   },
   "2": {
    "cls": "clean",
    "cell": "B10",
    "slips": [
     69
    ],
    "found": true,
    "above": 12,
    "score": -5.6761,
    "letters_right": 49
   },
   "3": {
    "cls": "clean",
    "cell": "B8",
    "slips": [
     68,
     69
    ],
    "found": false,
    "above": 3,
    "score": -5.92405,
    "letters_right": 41
   },
   "4": {
    "cls": "clean",
    "cell": "B9",
    "slips": [
     28,
     72
    ],
    "found": false,
    "above": 11,
    "score": -5.90306,
    "letters_right": 44
   },
   "5": {
    "cls": "clean",
    "cell": "B12",
    "slips": [
     30
    ],
    "found": true,
    "above": 12,
    "score": -5.37642,
    "letters_right": 39
   },
   "6": {
    "cls": "clean",
    "cell": "V14",
    "slips": [
     74
    ],
    "found": false,
    "above": 3,
    "score": -5.24738,
    "letters_right": 31
   },
   "7": {
    "cls": "clean",
    "cell": "V21",
    "slips": [
     74
    ],
    "found": false,
    "above": 3,
    "score": -4.89833,
    "letters_right": 27
   },
   "8": {
    "cls": "clean",
    "cell": "B25",
    "slips": [],
    "found": true,
    "above": 12,
    "score": -4.7357,
    "letters_right": 31
   },
   "9": {
    "cls": "clean",
    "cell": "B25",
    "slips": [],
    "found": true,
    "above": 12,
    "score": -4.60344,
    "letters_right": 32
   },
   "10": {
    "cls": "clean",
    "cell": "V21",
    "slips": [
     74
    ],
    "found": true,
    "above": 12,
    "score": -4.75429,
    "letters_right": 34
   },
   "11": {
    "cls": "clean",
    "cell": "V26",
    "slips": [],
    "found": true,
    "above": 12,
    "score": -4.63484,
    "letters_right": 44
   },
   "12": {
    "cls": "xstops",
    "cell": "B16",
    "slips": [],
    "found": false,
    "above": 11,
    "score": -5.32735,
    "letters_right": 35
   },
   "13": {
    "cls": "xstops",
    "cell": "V11",
    "slips": [
     33,
     74
    ],
    "found": true,
    "above": 12,
    "score": -5.3058,
    "letters_right": 37
   },
   "14": {
    "cls": "xstops",
    "cell": "B24",
    "slips": [],
    "found": true,
    "above": 12,
    "score": -4.61152,
    "letters_right": 36
   },
   "15": {
    "cls": "xstops",
    "cell": "B9",
    "slips": [
     28,
     72
    ],
    "found": true,
    "above": 12,
    "score": -5.30529,
    "letters_right": 37
   },
   "16": {
    "cls": "xstops",
    "cell": "B21",
    "slips": [
     74
    ],
    "found": true,
    "above": 12,
    "score": -4.77487,
    "letters_right": 31
   },
   "17": {
    "cls": "xstops",
    "cell": "V11",
    "slips": [
     30,
     33
    ],
    "found": false,
    "above": 3,
    "score": -5.63316,
    "letters_right": 41
   },
   "18": {
    "cls": "xstops",
    "cell": "V11",
    "slips": [
     30,
     66
    ],
    "found": false,
    "above": 1,
    "score": -5.63515,
    "letters_right": 34
   },
   "19": {
    "cls": "xstops",
    "cell": "B8",
    "slips": [
     34,
     69
    ],
    "found": true,
    "above": 12,
    "score": -5.64153,
    "letters_right": 46
   },
   "20": {
    "cls": "xstops",
    "cell": "B9",
    "slips": [
     28,
     72
    ],
    "found": true,
    "above": 12,
    "score": -5.50234,
    "letters_right": 44
   },
   "21": {
    "cls": "xstops",
    "cell": "V14",
    "slips": [
     32
    ],
    "found": true,
    "above": 12,
    "score": -5.27265,
    "letters_right": 30
   },
   "22": {
    "cls": "xstops",
    "cell": "B8",
    "slips": [
     68,
     69
    ],
    "found": true,
    "above": 12,
    "score": -5.38389,
    "letters_right": 46
   },
   "23": {
    "cls": "xstops",
    "cell": "B8",
    "slips": [
     29,
     34
    ],
    "found": true,
    "above": 12,
    "score": -5.64699,
    "letters_right": 41
   }
  }
 },
 "core_seconds": 9408,
 "compute_seconds": 1545,
 "exhaustive": true,
 "exhaustive_over": "every K4 setting 0274 lists as only EAST closed (one free alphabet, periodic key, minimal slip sets on the 20 official letters)",
 "aws_cost_estimate_dollars": 0.5
}
```

Notes: 49 settings in 20 cells; K4 above all 12 copies in 6 (chance 3.8, p 0.173), above all 100 in 2; plants clean [7, 12], Sanborn-style [9, 12]


