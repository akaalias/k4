# 0268-f15.3-do-the-drafts-help-the-climb-find-held-out-plants: F15.3: held-out drafts planted under two free alphabets at key lengths 13 and 20, each climbed with English alone and with English mixed with the drafts' quadgrams, against 12 kept-place copies climbed the same way

**Family:** 15-content-from-k1-k3  
**Parent:** 0257-d1b-two-free-alphabets-power-per-run-at-13-and-16  
**Decision:** reverted  
**Run:** 2026-11-04T18:45:55+00:00, 2133.9 s, status ran  
**Time by phase:** design 56 s, implement 12 s, test 20 s, run 2134 s, record 0 s

## In plain words

We wrote about 350 guesses at what K4 might say, based on the first three messages and on what Sanborn has said about it. Here we test whether those guesses help our search at all before using them on K4. We hide 24 other guesses, written separately, as secret messages, and see how often the search finds each one when it knows only English, and how often when it also knows the guesses' typical words. If the guesses do not help by at least two hidden messages in twelve, we drop the idea.

## Walkthrough, by hand

1. Take a guessed K4 text no search has seen, for example one written by a different model.
2. Encipher it with two scrambled alphabets and a 13-letter key.
3. Make 12 copies of the ciphertext with the 73 letters at unknown places shuffled.
4. Search each for the most English-looking reading with the 24 known letters held in place.
5. Search them again with a score that also rewards the four-letter pieces common in the other guesses.
6. Under each score, the plant is found if its best beats all 12 copies' bests.
7. Count found plants under each score; the drafts help if the second count is at least four higher over 24 plants.

## Worked example (generated)

```
F15.3 asks whether guessed texts help the search. For one hidden test message and its 12 shuffled copies:

  score E     English four-letter pieces only            plant best vs copies' bests
  score D50   half English, half the guesses' pieces     plant best vs copies' bests
  found when the plant beats all 12 copies under the same score.

24 test messages written by another model; the guesses help if D50 finds at least 4 more than E.
```

## Lineage

Inherits from 0257-d1b-two-free-alphabets-power-per-run-at-13-and-16. What changed: F15.3, power first (issue #118). 0257's harness (0144's compiled two-alphabet tempering, D1b's four runs, kept-place copies) with two changes: the plants are the 24 held-out drafts of F15.2 (written by another model and prompt, never in the prior), and every text is climbed under two score tables, English quadgrams (today's decider) and English mixed half and half with the quadgrams of the 329 corpus drafts (the draft prior). A third table (a fifth drafts) is reported, not used for the verdict.

## Hypothesis (domain expert)

F1.2's two-free-alphabet cells (Quagmire IV) at 13 and 20 are blocked for lack of checks: the 24 known letters fit copies as often as K4, and English alone finds about two thirds of plants (0257: 66 of 96 at four runs). If K4's plaintext is Sanborn's own prose on the subjects he named (reports/f15.1-content-model.md: a paced location, a meeting at the World Clock, the crowds of 1989, two breaches, light and shadow, K3 continued, a pointer onward), a score that knows that vocabulary should pull the climb towards the planted reading and away from English-like junk, and so find more plants against copies climbed with the same score. The prior is a quadgram table: log10 of 0.5 P_english(q) + 0.5 P_drafts(q), P_drafts from every quadgram of the 329 corpus drafts that touches a free place. Held-out drafts are never in it. Clue entries: C2 (instructions in the earlier text), C20(a) (K4 comes back to the first part), C27(c) (two alphabets).

## Prediction

English alone finds about 14-17 of 24 (0257's rate); the draft prior finds 2-5 more, because the held-out drafts share the corpus's subject words (CROWDS, PACES, SHADOW, MESSAGE). Copies climbed with the prior also score higher, so the gain is smaller than the gain in letters right. Pre-registered verdict: the bar (4 more of 24, the row's 2 of 12) is met or not; under it, F15.4-F15.6 close as weak.

## Method

1. Plants: the first 24 held-out drafts of data/drafts/drafts.jsonl, 12 at key length 13 and 12 at 20 (alternating), each enciphered on two random alphabets and a random key (seeded), with an exact witness (0123's decider through 0144's witness4).
2. Copies: 12 per plant, the 73 free places shuffled, the 24 known places kept.
3. Tables: E (English quadgrams, 0144's), D50 (log10 of 0.5 English + 0.5 drafts), D20 (0.8 English + 0.2 drafts).
4. Every text (24 plants and 288 copies) climbed under each table: four runs of 0144's tempering from the witness.
5. Found: the plant's best above all 12 of its copies' bests under the same table. Also letters right.
6. Verdict: found(D50) - found(E) over 24, bar 4.

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
 "item": "F15.3 (power first)",
 "cells": "F1.2 two free alphabets (Quagmire IV), key lengths 13 and 20",
 "decider": "0144's compiled tempering unchanged (16 x 625 x 1000), D1b's four runs, from the exact witness",
 "plants": "24 held-out drafts (claude-sonnet-5-5, prompt h1; never in the prior), alternating 13 and 20",
 "own_copies": 12,
 "null_per_plant": "1/13",
 "copies": "kept-place: the 24 known places kept, the 73 others shuffled",
 "tables": {
  "E": "English quadgrams (0144's)",
  "D50": "log10(0.5 P_eng + 0.5 P_drafts)",
  "D20": "log10(0.8 P_eng + 0.2 P_drafts)"
 },
 "draft_prior": "25004 quadgrams (6529 distinct) from the 329 corpus drafts, windows touching a free place",
 "found_by_table_and_length": {
  "E": {
   "13": 9,
   "20": 9
  },
  "D50": {
   "13": 8,
   "20": 8
  },
  "D20": {
   "13": 6,
   "20": 6
  }
 },
 "found_by_table": {
  "E": 18,
  "D50": 16,
  "D20": 12
 },
 "gain_D50_over_E": -2,
 "bar": 4,
 "bar_met": false,
 "mean_letters_right_by_table": {
  "E": 36.8,
  "D50": 37.9,
  "D20": 37.2
 },
 "each": {
  "0": {
   "draft": "h0329",
   "hyp": "H2",
   "L": 13,
   "E": {
    "found": true,
    "above": 12,
    "score": -4.68927,
    "letters_right": 43,
    "reading": "CCORTSARTYRDCINEIMEINEASTNORTHEASTOASTAKAYONTRYRIPLODGENEARUSUEBERLINCLOCKAHEDOIDTREUNIVEDINONNEW"
   },
   "D50": {
    "found": true,
    "above": 12,
    "score": -4.75798,
    "letters_right": 43,
    "reading": "UNARTSANTERDCEMEIBEIREASTNORTHEASTOASTAWAYORTHUROPEGDPENEAHHSDEBERLINCLOCKALLDOIDTHEFRIKEDINONNEX"
   },
   "D20": {
    "found": true,
    "above": 12,
    "score": -4.60328,
    "letters_right": 43,
    "reading": "YNORTSANTERDCEMEIVEIREASTNORTHEASTOASTAKAWORTHUROFLODGENEAHHSDEBERLINCLOCKALEDOIDTHEPRIKEDINONNEX"
   }
  },
  "1": {
   "draft": "h0330",
   "hyp": "H2",
   "L": 20,
   "E": {
    "found": true,
    "above": 12,
    "score": -4.43091,
    "letters_right": 37,
    "reading": "YEAHETHERINWHOREVERTREASTNORTHEASTANDREVEDMEEADCKDENTOMEONTHEPTBERLINCLOCKOWORESTMOFATHEBOADBEEHI"
   },
   "D50": {
    "found": true,
    "above": 12,
    "score": -4.46961,
    "letters_right": 44,
    "reading": "DEAVETHEPEARORNWAITHMEASTNORTHEASTUNSONISFRIEDANKMEFARYWINEASOCBERLINCLOCKATIONPOWNOFTHEYORSELLED"
   },
   "D20": {
    "found": true,
    "above": 12,
    "score": -4.3921,
    "letters_right": 39,
    "reading": "KEALETHEONGWHESASSTEDEASTNORTHEASTHOMINGSCHEEASAKLENNEBAHTANSOMBERLINCLOCKXTHINDONYONTHEBYADOFMEK"
   }
  },
  "2": {
   "draft": "h0331",
   "hyp": "H1",
   "L": 13,
   "E": {
    "found": true,
    "above": 12,
    "score": -4.73365,
    "letters_right": 37,
    "reading": "SRYDIVELBETEEEINEMBBLEASTNORTHEASTHRJUNGEREMISADOWNOFMATENTOIRIBERLINCLOCKSTONEOUSINAFTTDSOBESEYN"
   },
   "D50": {
    "found": true,
    "above": 12,
    "score": -4.87759,
    "letters_right": 36,
    "reading": "WRECAFTEDTOVEYUPETRHEEASTNORTHEASTBERONDIRETSSSYINGUNDATEDPRSEMBERLINCLOCKLOANYPORADMAUBYLUSINEXD"
   },
   "D20": {
    "found": false,
    "above": 11,
    "score": -4.79358,
    "letters_right": 41,
    "reading": "JROFTSHLYSOCEETSENDPLEASTNORTHEASTHERINGABENESATONSTHEQUETLOBEMBERLINCLOCKPORNEDWATTBMSTAKTMAVEKT"
   }
  },
  "3": {
   "draft": "h0332",
   "hyp": "H1",
   "L": 20,
   "E": {
    "found": true,
    "above": 12,
    "score": -4.48466,
    "letters_right": 36,
    "reading": "YTARKEYCAMIEVEDWITCALEASTNORTHEASTEWHEOFTBUTRIRUNEBEDAYSETHRENTBERLINCLOCKINTAINGEANSTIMENONSTPIE"
   },
   "D50": {
    "found": true,
    "above": 12,
    "score": -4.4151,
    "letters_right": 38,
    "reading": "AMAAGAYDOUNSANDOUTTEEEASTNORTHEASTFOREACCASEUTRANOUSTANATTWOFHEBERLINCLOCKINGUNDREAPOLEYEARDSTART"
   },
   "D20": {
    "found": true,
    "above": 12,
    "score": -4.43642,
    "letters_right": 36,
    "reading": "EYANCISADONCISVENTUSSEASTNORTHEASTHEMEYDIAPUBORENEXCROSSTTHEOREBERLINCLOCKXHECOMBEARIEDBEDGESTWOT"
   }
  },
  "4": {
   "draft": "h0333",
   "hyp": "H1",
   "L": 13,
   "E": {
    "found": false,
    "above": 3,
    "score": -4.82537,
    "letters_right": 30,
    "reading": "PANIDYWIAMIDTUMMERYTHEASTNORTHEASTTVWOOATALORACECRITUPORTSINGDUBERLINCLOCKLYAEDESKISHWASAREINNAMF"
   },
   "D50": {
    "found": false,
    "above": 3,
    "score": -4.92074,
    "letters_right": 30,
    "reading": "GZBYTHEIRMGLASUREGHTYEASTNORTHEASTTLIAMACAPARACENTMASFOGODIGARHBERLINCLOCKXASETOSSYDWARSECEINBRUG"
   },
   "D20": {
    "found": false,
    "above": 6,
    "score": -4.81116,
    "letters_right": 34,
    "reading": "YHREADEASSOUSINGANDWHEASTNORTHEASTTYPLIADARTEXCELHASIVEMOFTLIKEBERLINCLOCKPTPEWMCKSFISSUBSESTROPZ"
   }
  },
  "5": {
   "draft": "h0334",
   "hyp": "H2",
   "L": 20,
   "E": {
    "found": true,
    "above": 12,
    "score": -4.43099,
    "letters_right": 35,
    "reading": "GEONOLALEUNITTIONATAREASTNORTHEASTAGAMEONLYCEENTSWERESADENTUMBUBERLINCLOCKANARYEVEREURBOREARPERMU"
   },
   "D50": {
    "found": true,
    "above": 12,
    "score": -4.52751,
    "letters_right": 40,
    "reading": "JEWERGDEGLANTTHINTOISEASTNORTHEASTASACINELYDEVENAGEEEPACTROOKTOBERLINCLOCKAGAMETHEEOURALMEBELIVEE"
   },
   "D20": {
    "found": false,
    "above": 11,
    "score": -4.4692,
    "letters_right": 37,
    "reading": "UELEFACKANHEMTORYMINDEASTNORTHEASTASSETORSOMESHOSPERDGAMESIBELIBERLINCLOCKATSPARCEDFORBULDIRONEAJ"
   }
  },
  "6": {
   "draft": "h0335",
   "hyp": "H2",
   "L": 13,
   "E": {
    "found": true,
    "above": 12,
    "score": -4.66668,
    "letters_right": 39,
    "reading": "DWHETHREERLESFUPAMEETEASTNORTHEASTHOLLTIESHESIGNKINENECEACINEDIBERLINCLOCKSUMYNOTERKETUPTOAPOFHOT"
   },
   "D50": {
    "found": true,
    "above": 12,
    "score": -4.77188,
    "letters_right": 37,
    "reading": "WWORDEAVESANCHODKIDNTEASTNORTHEASTWEAPRDSSHEGUAINYMENSURYOUPERYBERLINCLOCKITLINETRKINTHOLDPSEXHAS"
   },
   "D20": {
    "found": true,
    "above": 12,
    "score": -4.69467,
    "letters_right": 40,
    "reading": "ZILEPELVEMURADBNSTHATEASTNORTHEASTITUNDIDWHEGUBSHELENDUESSUMEVEBERLINCLOCKXPAYNOTEOFATHECOMEORHRR"
   }
  },
  "7": {
   "draft": "h0336",
   "hyp": "H1",
   "L": 20,
   "E": {
    "found": true,
    "above": 12,
    "score": -4.45122,
    "letters_right": 34,
    "reading": "SOEVIOSAGASESEDLANTIMEASTNORTHEASTHETOBEROFEGGELDFROTHELEGENERSBERLINCLOCKNENDEDFOFPERYOUSAWINGAA"
   },
   "D50": {
    "found": true,
    "above": 12,
    "score": -4.45821,
    "letters_right": 34,
    "reading": "MAUDIOANDACESSANDGAIDEASTNORTHEASTRACHOLSANEXTYPENDONHINGREARYSBERLINCLOCKWASSENTANCERIORSULIFTUD"
   },
   "D20": {
    "found": false,
    "above": 11,
    "score": -4.44618,
    "letters_right": 32,
    "reading": "DOWNMESERMOUSINLINANGEASTNORTHEASTHEGOBINONEAPECURIOFFALAWEREHUBERLINCLOCKMENEETRONHERTTHEPREDIVI"
   }
  },
  "8": {
   "draft": "h0337",
   "hyp": "H3",
   "L": 13,
   "E": {
    "found": true,
    "above": 12,
    "score": -4.76723,
    "letters_right": 47,
    "reading": "NVEYCANHASWEDIDBIANTHEASTNORTHEASTSFTMEDITYHRHPOPERWHINDITAGINEBERLINCLOCKTOTRHOULPACHOKEVEOPENET"
   },
   "D50": {
    "found": true,
    "above": 12,
    "score": -4.79475,
    "letters_right": 50,
    "reading": "NGEYCAPERPONDGELDOGYEEASTNORTHEASTUNTMEDOTYFEELTLEGLAORULTARIVEBERLINCLOCKELTRANSERABETTEREOPENET"
   },
   "D20": {
    "found": true,
    "above": 12,
    "score": -4.75631,
    "letters_right": 41,
    "reading": "XTOFCARLASHALKSHISOPLEASTNORTHEASTOCKWEFETFGMARITERIHEWAYSDUGUEBERLINCLOCKIDTOHAREMAILIFECEOBONES"
   }
  },
  "9": {
   "draft": "h0338",
   "hyp": "H3",
   "L": 20,
   "E": {
    "found": true,
    "above": 12,
    "score": -4.40438,
    "letters_right": 35,
    "reading": "GFLICALLYIPTUFFERECAREASTNORTHEASTPALINANETHANDCOLLETWOMPELLLIEBERLINCLOCKHASSISANOFESTSOINEINLOB"
   },
   "D50": {
    "found": true,
    "above": 12,
    "score": -4.42527,
    "letters_right": 33,
    "reading": "NLEFUELLINDTOLSOFARTYEASTNORTHEASTDIDTOTHEDURNAPOOLENGINTANDPITBERLINCLOCKXISECOMALHESHEONUEARAME"
   },
   "D20": {
    "found": true,
    "above": 12,
    "score": -4.35721,
    "letters_right": 35,
    "reading": "BDTONALODESPEANDVANTHEASTNORTHEASTHOLOUTFEWLINDCHILEWOMEHATONCOBERLINCLOCKSONTOSTARGESEDHEMEANTHO"
   }
  },
  "10": {
   "draft": "h0339",
   "hyp": "H3",
   "L": 13,
   "E": {
    "found": false,
    "above": 10,
    "score": -4.79774,
    "letters_right": 33,
    "reading": "PGROUNGBECARALKMANDTHEASTNORTHEASTOCOLOALRESNRYEAIMHDRVICCLENEEBERLINCLOCKTISRSTFORCHICHADEEMEITK"
   },
   "D50": {
    "found": false,
    "above": 10,
    "score": -4.83281,
    "letters_right": 40,
    "reading": "NNAPLYIHERORDEALLTINGEASTNORTHEASTHRBYMILAIDYADEANWAHREACEHELIEBERLINCLOCKSNESSCOPPEDOADOPEFURAJK"
   },
   "D20": {
    "found": false,
    "above": 10,
    "score": -4.75773,
    "letters_right": 34,
    "reading": "TURIFTHSETHIKSOLONETHEASTNORTHEASTOTTAGALRESTAMEANDMKRCYCOMEQUEBERLINCLOCKONSSESDIAOPICKHOEDWAYTV"
   }
  },
  "11": {
   "draft": "h0340",
   "hyp": "H3",
   "L": 20,
   "E": {
    "found": false,
    "above": 11,
    "score": -4.49183,
    "letters_right": 35,
    "reading": "XPREASTOTHCOUNEESTATOEASTNORTHEASTSDEVEGARDOFMOVERNEREAWAASDENIBERLINCLOCKYSHIGNDPOLENTOSTBEISTED"
   },
   "D50": {
    "found": false,
    "above": 11,
    "score": -4.53814,
    "letters_right": 36,
    "reading": "XSTECORETHTOLDNANEANBEASTNORTHEASTHWANILEDINAMONYOUNREESUPTRAVEBERLINCLOCKAMEONOWSOFENREPAINALGAM"
   },
   "D20": {
    "found": true,
    "above": 12,
    "score": -4.4215,
    "letters_right": 32,
    "reading": "GRETHERETHTOFGREARODEEASTNORTHEASTMOFFEATPURASOLANDTRESTETHCOMIBERLINCLOCKILWEWERROVENREHESTOODEC"
   }
  },
  "12": {
   "draft": "h0341",
   "hyp": "H4",
   "L": 13,
   "E": {
    "found": true,
    "above": 12,
    "score": -4.77961,
    "letters_right": 34,
    "reading": "AHOGAFRADSNAFGIFFCSTYEASTNORTHEASTORIISCHEVERBARUPALSTHRATINMANBERLINCLOCKEDAENDSIGNIFIVEORECTGIV"
   },
   "D50": {
    "found": true,
    "above": 12,
    "score": -4.91895,
    "letters_right": 32,
    "reading": "PBYEACLORITSHCOATCHIREASTNORTHEASTOROFFSBUDEIGOTHMSGUNDIAGESHATBERLINCLOCKDISEEIKYSTEALLELSFATEFW"
   },
   "D20": {
    "found": false,
    "above": 11,
    "score": -4.81412,
    "letters_right": 31,
    "reading": "DOHEADWENGURAWCALCELHEASTNORTHEASTMEDWRYONRESPELWORDFILMAINGCAUBERLINCLOCKIGREATBAIGNWIDENTUATEXN"
   }
  },
  "13": {
   "draft": "h0342",
   "hyp": "H5",
   "L": 20,
   "E": {
    "found": false,
    "above": 2,
    "score": -4.64319,
    "letters_right": 31,
    "reading": "IFMYOURPOWANDWOFDEBANEASTNORTHEASTTERSTHAMILLTAKAKNOBIGIMONBALLBERLINCLOCKBOSTERSCHEDWATETGMALLYV"
   },
   "D50": {
    "found": false,
    "above": 6,
    "score": -4.68638,
    "letters_right": 28,
    "reading": "LOFMAHENBEPEDFIRDINGOEASTNORTHEASTCEITSHADERCOREVATONOPLAYAKALLBERLINCLOCKEASPEARNIXWARHANFULAYBC"
   },
   "D20": {
    "found": false,
    "above": 3,
    "score": -4.61965,
    "letters_right": 32,
    "reading": "MFLAMAEMPLACHESYESCUSEASTNORTHEASTPARTECOMFIRSTYREGOLIVICERNOLDBERLINCLOCKBEINLARRYFITTLEPNINSOMW"
   }
  },
  "14": {
   "draft": "h0343",
   "hyp": "H5",
   "L": 13,
   "E": {
    "found": true,
    "above": 12,
    "score": -4.74508,
    "letters_right": 36,
    "reading": "DRDBENFORUNAOURCPLIEDEASTNORTHEASTTWERSANTDINFOREEPVIDLYCOMPHENBERLINCLOCKILAGOVERNORTWOIDSECLORE"
   },
   "D50": {
    "found": false,
    "above": 11,
    "score": -4.87702,
    "letters_right": 38,
    "reading": "GROVENESSPEAPURLSWUNGEASTNORTHEASTHEIMSSATDONESSRIDGEGPACEIFIREBERLINCLOCKSDAYOFEITEATWOFFSNCPOMP"
   },
   "D20": {
    "found": false,
    "above": 11,
    "score": -4.79873,
    "letters_right": 32,
    "reading": "DRYBENEARNUDOFROMMUNDEASTNORTHEASTYLOWUPATRUNEARRORIEDRACEYOURUBERLINCLOCKMADSOWUPNEATHCPFUNCROWF"
   }
  },
  "15": {
   "draft": "h0344",
   "hyp": "H4",
   "L": 20,
   "E": {
    "found": true,
    "above": 12,
    "score": -4.44633,
    "letters_right": 43,
    "reading": "YANEOFOLEODSCITINTROVEASTNORTHEASTENDTOTHEISAALIGHOUREEPRAIGNTOBERLINCLOCKTHISTRICTMOTOMEAOKINSUS"
   },
   "D50": {
    "found": false,
    "above": 9,
    "score": -4.59967,
    "letters_right": 39,
    "reading": "ETINCEOPENARCHEINELIVEASTNORTHEASTNOBESOMERSAWLIBHDELINERRERTHEBERLINCLOCKETOGRANYJRCTOFEEDUPFIJI"
   },
   "D20": {
    "found": false,
    "above": 8,
    "score": -4.51805,
    "letters_right": 38,
    "reading": "ORNWASOLDEASCIENESHASEASTNORTHEASTHATSONEERSPOLIGHIRTCHICOVETOMBERLINCLOCKESWICHANCHATOEDNIINLYKM"
   }
  },
  "16": {
   "draft": "h0345",
   "hyp": "H5",
   "L": 13,
   "E": {
    "found": true,
    "above": 12,
    "score": -4.70943,
    "letters_right": 38,
    "reading": "TODITIPLELPENNYRATIPSEASTNORTHEASTHETOFILTDSETTINCREARMCCRYWHETBERLINCLOCKSWEATOLIPGATHCERSVIDCOL"
   },
   "D50": {
    "found": true,
    "above": 12,
    "score": -4.73986,
    "letters_right": 42,
    "reading": "DOPETORSELEINNPASTORNEASTNORTHEASTHERYFULTXDITTIRTHESRECCHHWHERBERLINCLOCKDAISDONEANDTHIGHAMUPCOL"
   },
   "D20": {
    "found": true,
    "above": 12,
    "score": -4.66369,
    "letters_right": 48,
    "reading": "TOLENOTSEYNONNGCONOTYEASTNORTHEASTISEDWALTIDBUTSDILEUREACTHUISEBERLINCLOCKGROUTORESEPTIMPLIBALABL"
   }
  },
  "17": {
   "draft": "h0346",
   "hyp": "H4",
   "L": 20,
   "E": {
    "found": true,
    "above": 12,
    "score": -4.44745,
    "letters_right": 38,
    "reading": "JORTERRIEDURITINGHISMEASTNORTHEASTHESSSCALPANYTSELYCOSSEDTORGORBERLINCLOCKSUNSEWASOFPLYERBEDFRUNA"
   },
   "D50": {
    "found": true,
    "above": 12,
    "score": -4.48515,
    "letters_right": 37,
    "reading": "FASTERTISESSATIVEDPASEASTNORTHEASTEATOCKNOUNSABUSTHEMETAMTHECASBERLINCLOCKTIGOWINTWILLNERVEHULDVA"
   },
   "D20": {
    "found": true,
    "above": 12,
    "score": -4.45493,
    "letters_right": 32,
    "reading": "RHEPERFISLYDUTISISINNEASTNORTHEASTHINEEDSOMEOUSASWAITEDITBROTHEBERLINCLOCKDUSENTSTXTDDALAMECASTSW"
   }
  },
  "18": {
   "draft": "h0347",
   "hyp": "H4",
   "L": 13,
   "E": {
    "found": true,
    "above": 12,
    "score": -4.5484,
    "letters_right": 41,
    "reading": "AEGRAMEOCORNEYLOUREOFEASTNORTHEASTHEMYNATHECIVATOPPEACTHEBILLSTBERLINCLOCKMSGLEDAHTHANTENDPOWEVES"
   },
   "D50": {
    "found": true,
    "above": 12,
    "score": -4.71319,
    "letters_right": 45,
    "reading": "SNSANDLACEFRELLOWLTOGEASTNORTHEASTXTHENSBADCRYPHECHESHTHEYALSCOBERLINCLOCKNSIGDOWHOURNHTEDCODEFEI"
   },
   "D20": {
    "found": true,
    "above": 12,
    "score": -4.61553,
    "letters_right": 44,
    "reading": "AEORAMTOCORNEYLLPRTOWEASTNORTHEASTHENYNATHECEKATOLDEACTHEBELLSTBERLINCLOCKMSULTICHTHANTEDITONGWES"
   }
  },
  "19": {
   "draft": "h0348",
   "hyp": "H6",
   "L": 20,
   "E": {
    "found": true,
    "above": 12,
    "score": -4.49043,
    "letters_right": 30,
    "reading": "ADEDFORBARYINENDEVESTEASTNORTHEASTODRESARMYNOLODIEANDPEATTAWADEBERLINCLOCKTONVEROLLICATITRIDNOUGC"
   },
   "D50": {
    "found": true,
    "above": 12,
    "score": -4.46288,
    "letters_right": 39,
    "reading": "THEWATBYASWHANCEEALSDEASTNORTHEASTHEWEENWARNBOOEXIFULLSGOTHATHEBERLINCLOCKITFALLALLOSSEITSMCAPTAB"
   },
   "D20": {
    "found": false,
    "above": 11,
    "score": -4.47735,
    "letters_right": 33,
    "reading": "ITELYMENDMUSENDEDTALLEASTNORTHEASTHEWEMANGTOSSOWEARRHIMPIONVITEBERLINCLOCKATOTADEMUCHIFITMACELLYP"
   }
  },
  "20": {
   "draft": "h0349",
   "hyp": "H5",
   "L": 13,
   "E": {
    "found": false,
    "above": 10,
    "score": -4.76382,
    "letters_right": 43,
    "reading": "WARYARDISNEELIGNERIANEASTNORTHEASTILLANLDQUEITYNDHEAPOBESLASUPRBERLINCLOCKANDKMANATMINUENTLEFTRWI"
   },
   "D50": {
    "found": false,
    "above": 11,
    "score": -4.80774,
    "letters_right": 38,
    "reading": "UEPARTAGLXWARNCERKEDEEASTNORTHEASTAMLONSOFBEEENDSTAITTOROLDITWEBERLINCLOCKAMDAMEEDSUNETOMTRINTYPE"
   },
   "D20": {
    "found": false,
    "above": 10,
    "score": -4.73608,
    "letters_right": 42,
    "reading": "GEMILIPFANDCHANERBEEIEASTNORTHEASTDOFUNJOSDEEREWSACTITORFLEDSIMBERLINCLOCKATSAFEEMUGLISETTHEYTORE"
   }
  },
  "21": {
   "draft": "h0350",
   "hyp": "H6",
   "L": 20,
   "E": {
    "found": true,
    "above": 12,
    "score": -4.36239,
    "letters_right": 33,
    "reading": "CEHORMWATHESECURSONLEEASTNORTHEASTALCOATWARENANCEPRILENOOFTHECEBERLINCLOCKSINEWAYOFEDOVEHIMILESCI"
   },
   "D50": {
    "found": true,
    "above": 12,
    "score": -4.39538,
    "letters_right": 36,
    "reading": "UEDEGUNDTHESPERAROUSLEASTNORTHEASTBECONANDSTIDEAMSPHERHILREPLAYBERLINCLOCKSTHEBETTETATFEELWHERSGI"
   },
   "D20": {
    "found": true,
    "above": 12,
    "score": -4.29176,
    "letters_right": 40,
    "reading": "RETPHORATHEMERHOMEDBEEASTNORTHEASTAPPEEDIALOLANDERWIDEINGRASEDEBERLINCLOCKSLASSETTHOFTHEBINIDESAC"
   }
  },
  "22": {
   "draft": "h0351",
   "hyp": "H7",
   "L": 13,
   "E": {
    "found": true,
    "above": 12,
    "score": -4.86266,
    "letters_right": 39,
    "reading": "TRDONTANDPOMOUSDAWAKPEASTNORTHEASTFINIDDITUHASMOTESEDBILYIEMERMBERLINCLOCKFACTHILMOSHEELYEXPEROBY"
   },
   "D50": {
    "found": true,
    "above": 12,
    "score": -4.90326,
    "letters_right": 37,
    "reading": "TRDOFTANDWOMOUSDAWAKWEASTNORTHEASTXITIDDITPHASMOTESEDBILVIEMERMBERLINCLOCKXACTHILMOSHOELVEYWEROBV"
   },
   "D20": {
    "found": true,
    "above": 12,
    "score": -4.83262,
    "letters_right": 39,
    "reading": "URDARIALDECRAVIDEBATHEASTNORTHEASTFORACTSTRGASEAHUGETWILYUGEEVEBERLINCLOCKTHDMESAMAMPBENKLSXTMANS"
   }
  },
  "23": {
   "draft": "h0352",
   "hyp": "H7",
   "L": 20,
   "E": {
    "found": false,
    "above": 11,
    "score": -4.51386,
    "letters_right": 36,
    "reading": "TASANSUSTIMSUDIFICEIVEASTNORTHEASTAAMERPETESAIDENNTEEACHARISALEBERLINCLOCKUNTEATOVERTALEGARYWINAJ"
   },
   "D50": {
    "found": false,
    "above": 11,
    "score": -4.56901,
    "letters_right": 38,
    "reading": "MCLCROWNTOFDEIATAMACLEASTNORTHEASTHERTIMPSESPANANUTIVETACROSINEBERLINCLOCKXBUTTHATENTPLAITANDSWEH"
   },
   "D20": {
    "found": false,
    "above": 11,
    "score": -4.50428,
    "letters_right": 37,
    "reading": "KBOTYSENTRUGHFLACUPESEASTNORTHEASTTEBANGPRESKASANDSDRESWICESTHEBERLINCLOCKATMAINATEATPLAIORTENEER"
   }
  }
 },
 "texts": 312,
 "climbs": 936,
 "runs_per_climb": 4,
 "core_seconds": 60744,
 "compute_seconds": 1965,
 "resumed_units": 0,
 "exhaustive": false,
 "cost_estimate": "312 texts x 3 tables x 4 runs x about 18 s: about 19 core-hours; on AWS 32 cores about 40 min, about $0.40"
}
```

Notes: F15.3: plants found against 12 own copies, English 18/24, drafts 50% 16/24, drafts 20% 12/24; gain -2 against the bar 4: not met. Letters right 36.8, 37.9, 37.2.


