# 0213-plaintext-autokey-with-slips-and-a-lost-step: A1.4, part 2: plaintext autokey on the sculpture's and the vocabulary's tables, lags 1-52, with up to two carved slips breaking the chain, or one lost step that runs on through it; exact, the readings judged against scrambled copies, with planted slipped messages

**Family:** 1-keyed-periodic  
**Parent:** 0025-autokey-keyword-mixed-alphabets  
**Decision:** reverted  
**Run:** 2026-10-20T13:34:28+00:00, 219.2 s, status ran  
**Time by phase:** implement 246 s, test 81 s, run 219 s, record 61 s

## In plain words

In a plaintext autokey the message is its own key: each letter is enciphered with the message letter L places before it. The known words then let us work out letters further along the message, one step at a time, like a chain. One wrongly carved letter breaks the chain there, and a hand slip that loses one step shifts everything after it. Earlier experiments allowed neither. Here we allow two broken links, or one lost step anywhere, on the carving and on scrambled copies, and a language model reads what comes out, blind to which is which.

## Walkthrough, by hand

1. Choose a lag, say 12, and a table.
2. Known place 22 (E) and place 34 (T) are 12 apart: the carved letter at 34 and E as its key must give T on the table.
3. Work along each chain of places 12 apart, from one known letter to the next, and mark the pairs that disagree.
4. Each disagreeing pair needs one carved slip somewhere between them; allow up to two.
5. For a lost step, from some place on use the letter 13 (or 11) back as the key instead, and require every pair to agree.
6. Read every letter a known letter reaches through its chain, and compare with scrambled copies.

## Worked example (generated)

```
plaintext autokey, lag 12, KRYPTOS table, Vigenere: chains of places 12 apart, walked from one known letter to the next

  22 E -> 34: the chain gives U, known T   break needed
  23 A -> 71: the chain gives P, known L   break needed
  24 S -> 72: the chain gives X, known O   break needed
  25 T -> 73: the chain gives H, known C   break needed
  26 N -> 74: the chain gives D, known K   break needed
  28 R -> 64: the chain gives B, known B
  29 T -> 65: the chain gives H, known E   break needed
  30 H -> 66: the chain gives M, known R   break needed

breaks needed at lag 12: 11 (2 allowed)
```

## Lineage

Inherits from 0025-autokey-keyword-mixed-alphabets. What changed: A1.4 (Stage 2, step 2, issue #76), second part. 0003, 0012 and 0025 chained plaintext autokey from the known letters with no slip: lags 1-25 and 30-52 dead, 26-29 noise by quadgrams. In plaintext autokey a wrong carved letter does not change the message but breaks our derivation through it, so (a) every lag 1-52 is rerun allowing up to 2 breaks (slips anywhere in the chain, the known places included); (b) one lost step (from some place on, the key is the message letter L + 1 or L - 1 back), at every place, as its own setting: everything after it shifts; (c) at lags 26-29, where the known letters give 0-1 checks, every table's reading is scored and the best go to the blind judge, which reads past a slip that garbles the rest of a chain (bench class 'half'). 35,721 table setups (0025's), compiled; K4 against 20 scrambled copies; three planted messages.

## Hypothesis (domain expert)

A1 (knowledge/12-assumptions.md); C11a (NSA 1992: 'plain-text auto-key (if a high-frequency letter is assigned 0)'; NSA 2007 tested it without cribs), C27(a), Sanborn 2005 'Saying I was sloppy'. Model: c_i = C[E(P(p_i), K(p_{i-L}))] after a primer of L letters; P, C from 0025's 63 alphabets (standard, KRYPTOS, vocabulary keyword), K standard, KRYPTOS or the plain alphabet; Vigenere, Beaufort, variant. Each equation links p_i and p_{i-L} by a bijection, so the message splits into L chains; two known letters in one chain must agree through every carved letter between them. A slip at place j cuts the chain at j: the least number of cuts is the number of disagreeing neighbouring known pairs, at most 2 here (17.5 bits to name). A lost step at j: p_i keyed by p_{i-L-1} or p_{i-L+1} from j on, which joins the chains differently (a forest; known letters in one tree must agree), j = 2-74, about 7 bits. Readings: every letter whose chain holds a known letter. Counted per lag, K4 against each copy; readings keeping 3 or more checks, and at 26-29 the best by quadgrams of every text, go to the judge in one call.

## Prediction

No lag below 26 fits K4 with 2 breaks or one lost step where it keeps 3 or more checks beyond the copies' rate; at 26-29 K4's best reading is judged inside the copies'. All three plants found. Zero candidates pass gate 4.

## Method

1. For each table setup, lag and text, walk every chain between neighbouring known letters and count the pairs that disagree; keep up to
2. 2. For each lost step (lag L before place j, L + 1 or L - 1 from it), walk each known letter to the root of its tree and require known letters sharing a root to agree.
3. At lags 26-29, derive every reading and score it by quadgrams in the same compiled pass.
4. Readings to quadgrams; each text's 5 best and every reading at or above -5.0 to the judge, all texts in one call.
5. Counts per lag, K4 against 20 copies; plants and their own copies through the same search.

## Result

Candidates returned: 10. Passed all gates: 0. Best crib hits among all candidates: 24/24
(EAST 4/4, NORTHEAST 9/9, BERLIN 6/6, CLOCK 5/5).
Best loss: 10.846623634910173 (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | baseline | 24/24 | -15.054 | `IIDPVLMAAAAAAAAAAAAAAEASTNORTHEASTAFURGVTAAAAAAAAAAAAAECAITMOFDBERLINCLOCKAAAAAAAAAAAAAETAKTHIOXD` | plaintext autokey lag 33, WORLDCLOCK/keyword|UNDERGROUND/keyword|plain|beau, chain, cuts [67], lost step None; unknown letters filled with A, every disagreeing carved letter named as a slip |
| 2 | baseline | 24/24 | -12.020 | `BTUMOPAHOMRAVJABAIAAAEASTNORTHEASTANISHDHADEEXAAADFEGOGAVGWBGCABERLINCLOCKAAARCAMLOIYRJUSVAUIETHE` | plaintext autokey lag 28, WALL/keyword|PALIMPSEST/keyword|std|varbeau, bulk, cuts [], lost step None; unknown letters filled with A, every disagreeing carved letter named as a slip |
| 3 | baseline | 24/24 | -12.118 | `MWVTALAKJOVRJERINTAAAEASTNORTHEASTATFCKHUVHISAAAAAUEAOFWECTHLDABERLINCLOCKAAAKSIUZFINHAGUYAWHEOFA` | plaintext autokey lag 28, DIGETAL/keyword|WALL/keyword|std|varbeau, bulk, cuts [], lost step None; unknown letters filled with A, every disagreeing carved letter named as a slip |
| 4 | baseline | 24/24 | -12.564 | `STHASNALNGEJFADRAAAAAEASTNORTHEASTEJJABLYDSMRAAAAAFDFIROINMRGOVBERLINCLOCKAAAAAHGRTFEXWNVERZUVEMP` | plaintext autokey lag 29, CARNARVON/keyword|SOMEWHERE/keyword|kry|vig, bulk, cuts [], lost step None; unknown letters filled with A, every disagreeing carved letter named as a slip |
| 5 | baseline | 24/24 | -12.823 | `TAOSOMDDLOUFEILFAAAAAEASTNORTHEASTAQGGIROLCAXAAAAAPFLCADCOLOBENBERLINCLOCKAAAAASMVYONNACZSSAODFIR` | plaintext autokey lag 29, WONDERFUL/keyword|SOUTH/keyword|kry|vig, bulk, cuts [], lost step None; unknown letters filled with A, every disagreeing carved letter named as a slip |
| 6 | baseline | 24/24 | -12.109 | `PNYPMCLAAIDGAKLANUMAAEASTNORTHEASTAAISPRACRATALAEZAHOAYPUAAWCAABERLINCLOCKAIJJJWIOFQMPSJAAUHIKORY` | plaintext autokey lag 27, VIRTUALLYINVISIBLE/keyword|WEBSTER/keyword|plain|beau, bulk, cuts [], lost step None; unknown letters filled with A, every disagreeing carved letter named as a slip |
| 7 | baseline | 24/24 | -12.579 | `PSQLWELANGNIETSTAAAAAEASTNORTHEASTOFXINVXKIZRAAAAAAKRTUNMCSSGBZBERLINCLOCKAAAAADBLYGARMYTLEACPUKE` | plaintext autokey lag 29, HOWARDCARTER/keyword|LAYERTWO/keyword|plain|beau, bulk, cuts [], lost step None; unknown letters filled with A, every disagreeing carved letter named as a slip |
| 8 | baseline | 24/24 | -12.466 | `ROANOURMRJAOJOABAAAAAEASTNORTHEASTEAJAMNYMTNZAAAAAWDESQARTAMWCABERLINCLOCKAAAAATVJOFFIRIYBRIZHCFR` | plaintext autokey lag 29, BERLINCLOCK/keyword|ALEXANDERPLATZ/keyword|std|beau, bulk, cuts [], lost step None; unknown letters filled with A, every disagreeing carved letter named as a slip |
| 9 | baseline | 24/24 | -12.603 | `TPCMYCIAKPKAWHEEAAAAAEASTNORTHEASTDHRUPWBYBEKAAAAAPBDYGASOFTEANBERLINCLOCKAAAAAVVOCZYBETUVLGRODPR` | plaintext autokey lag 29, IQLUSION/keyword|WELTZEITUHR/keyword|kry|vig, bulk, cuts [], lost step None; unknown letters filled with A, every disagreeing carved letter named as a slip |
| 10 | baseline | 24/24 | -12.450 | `MBSRFWAOWHNWIMIDERAAAEASTNORTHEASTAVIJWTYVALYAAAAOBCCLTGKBCWOGABERLINCLOCKAAASUNDLMLARPUNGABYACCV` | plaintext autokey lag 28, ILLUSION/keyword|ABSCISSA/keyword|std|beau, bulk, cuts [], lost step None; unknown letters filled with A, every disagreeing carved letter named as a slip |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "plaintext autokey on 0025's tables, lags 1-52, up to 2 chain breaks (slips) or one lost step (A1.4)",
 "table_setups": 35343,
 "lags": "1-52 (53-96 blocked by 0136's bound)",
 "breaks": "0-2 anywhere in a chain between neighbouring known letters (known places included)",
 "lost_step": "lag L before place j, L+1 or L-1 from j on, j = 2-74; known letters in one tree must agree",
 "bulk": "lags 26-29 with no break: every table's reading scored by quadgrams; the top 20 and all at or above -5.0 per text to the judge",
 "by_lag": {
  "1": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "2": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "3": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "4": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "5": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "6": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "7": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "8": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "9": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "10": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "11": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "12": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "13": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "14": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "15": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "16": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "17": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    1
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "18": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    1
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "19": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "20": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "21": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "22": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "23": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "24": {
   "k4": [
    0,
    0,
    8
   ],
   "copies_max": [
    0,
    2,
    27
   ],
   "copies_min": [
    0,
    0,
    5
   ],
   "skip_k4": [
    88,
    1
   ],
   "skip_copies_max": [
    121,
    0
   ]
  },
  "25": {
   "k4": [
    3,
    120,
    3732
   ],
   "copies_max": [
    4,
    215,
    4330
   ],
   "copies_min": [
    0,
    101,
    3201
   ],
   "skip_k4": [
    45458,
    7
   ],
   "skip_copies_max": [
    52429,
    33
   ]
  },
  "26": {
   "k4": [
    1512,
    33831,
    0
   ],
   "copies_max": [
    1734,
    34306,
    0
   ],
   "copies_min": [
    1037,
    33609,
    0
   ],
   "skip_k4": [
    35885,
    1923
   ],
   "skip_copies_max": [
    41822,
    6413
   ]
  },
  "27": {
   "k4": [
    35343,
    0,
    0
   ],
   "copies_max": [
    35343,
    0,
    0
   ],
   "copies_min": [
    35343,
    0,
    0
   ],
   "skip_k4": [
    35113,
    71064
   ],
   "skip_copies_max": [
    39293,
    81498
   ]
  },
  "28": {
   "k4": [
    35343,
    0,
    0
   ],
   "copies_max": [
    35343,
    0,
    0
   ],
   "copies_min": [
    35343,
    0,
    0
   ],
   "skip_k4": [
    33522,
    0
   ],
   "skip_copies_max": [
    39794,
    0
   ]
  },
  "29": {
   "k4": [
    35343,
    0,
    0
   ],
   "copies_max": [
    35343,
    0,
    0
   ],
   "copies_min": [
    35343,
    0,
    0
   ],
   "skip_k4": [
    73128,
    0
   ],
   "skip_copies_max": [
    114130,
    0
   ]
  },
  "30": {
   "k4": [
    1234,
    34109,
    0
   ],
   "copies_max": [
    1963,
    34459,
    0
   ],
   "copies_min": [
    884,
    33380,
    0
   ],
   "skip_k4": [
    2502,
    12340
   ],
   "skip_copies_max": [
    8400,
    19630
   ]
  },
  "31": {
   "k4": [
    40,
    2601,
    32702
   ],
   "copies_max": [
    156,
    3539,
    33454
   ],
   "copies_min": [
    13,
    1862,
    31718
   ],
   "skip_k4": [
    65,
    79533
   ],
   "skip_copies_max": [
    675,
    126601
   ]
  },
  "32": {
   "k4": [
    1,
    93,
    3509
   ],
   "copies_max": [
    12,
    359,
    5563
   ],
   "copies_min": [
    0,
    61,
    2623
   ],
   "skip_k4": [
    0,
    2639
   ],
   "skip_copies_max": [
    113,
    9999
   ]
  },
  "33": {
   "k4": [
    0,
    4,
    247
   ],
   "copies_max": [
    2,
    61,
    804
   ],
   "copies_min": [
    0,
    1,
    186
   ],
   "skip_k4": [
    0,
    67
   ],
   "skip_copies_max": [
    3,
    758
   ]
  },
  "34": {
   "k4": [
    0,
    0,
    9
   ],
   "copies_max": [
    0,
    3,
    74
   ],
   "copies_min": [
    0,
    0,
    11
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    126
   ]
  },
  "35": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    1,
    4
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "36": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    2
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "37": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "38": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "39": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "40": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "41": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "42": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "43": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "44": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    0
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "45": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    1
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "46": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    1
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "47": {
   "k4": [
    0,
    0,
    0
   ],
   "copies_max": [
    0,
    0,
    4
   ],
   "copies_min": [
    0,
    0,
    0
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    0,
    0
   ]
  },
  "48": {
   "k4": [
    0,
    0,
    7
   ],
   "copies_max": [
    0,
    2,
    65
   ],
   "copies_min": [
    0,
    0,
    9
   ],
   "skip_k4": [
    0,
    0
   ],
   "skip_copies_max": [
    189,
    0
   ]
  },
  "49": {
   "k4": [
    0,
    2,
    262
   ],
   "copies_max": [
    3,
    36,
    392
   ],
   "copies_min": [
    0,
    0,
    179
   ],
   "skip_k4": [
    315,
    0
   ],
   "skip_copies_max": [
    635,
    2
   ]
  },
  "50": {
   "k4": [
    5,
    115,
    3436
   ],
   "copies_max": [
    10,
    260,
    4649
   ],
   "copies_min": [
    0,
    41,
    2678
   ],
   "skip_k4": [
    2530,
    2
   ],
   "skip_copies_max": [
    6067,
    229
   ]
  },
  "51": {
   "k4": [
    40,
    3166,
    32137
   ],
   "copies_max": [
    96,
    3581,
    33715
   ],
   "copies_min": [
    5,
    1623,
    31686
   ],
   "skip_k4": [
    91372,
    430
   ],
   "skip_copies_max": [
    112809,
    877
   ]
  },
  "52": {
   "k4": [
    1443,
    33900,
    0
   ],
   "copies_max": [
    1780,
    34316,
    0
   ],
   "copies_min": [
    1027,
    33563,
    0
   ],
   "skip_k4": [
    12028,
    5072
   ],
   "skip_copies_max": [
    17591,
    8591
   ]
  }
 },
 "k4_above_every_copy_lags": [],
 "copies_above_rest": [
  0,
  0,
  0,
  1,
  1,
  2,
  0,
  0,
  5,
  0,
  1,
  3,
  1,
  0,
  2,
  0,
  1,
  1,
  0,
  1
 ],
 "shortest_lag_with_breaks": {
  "K4": 24,
  "copy1": 24,
  "copy2": 24,
  "copy3": 17,
  "copy4": 24,
  "copy5": 24,
  "copy6": 17,
  "copy7": 18,
  "copy8": 17,
  "copy9": 24,
  "copy10": 24,
  "copy11": 18,
  "copy12": 24,
  "copy13": 18,
  "copy14": 24,
  "copy15": 24,
  "copy16": 24,
  "copy17": 17,
  "copy18": 24,
  "copy19": 24,
  "copy20": 24
 },
 "shortest_lag_lost_step": {
  "K4": 24,
  "copy1": 24,
  "copy2": 24,
  "copy3": 24,
  "copy4": 24,
  "copy5": 24,
  "copy6": 24,
  "copy7": 24,
  "copy8": 24,
  "copy9": 24,
  "copy10": 24,
  "copy11": 25,
  "copy12": 24,
  "copy13": 25,
  "copy14": 24,
  "copy15": 24,
  "copy16": 24,
  "copy17": 24,
  "copy18": 24,
  "copy19": 24,
  "copy20": 25
 },
 "readings": {
  "k4": 1169,
  "copies": [
   686,
   715,
   370,
   728,
   1015,
   316,
   787,
   960,
   1300,
   560,
   1279,
   590,
   1821,
   332,
   1143,
   1389,
   2371,
   574,
   1013,
   1111
  ]
 },
 "capped": [],
 "judge": {
  "sent": 194,
  "none": 0,
  "cut": -5.0,
  "rule": "each text's top 5 readings by quadgrams and every reading at or above -5.0; one call"
 },
 "k4_judge_best": 4,
 "copies_judge_best": [
  8,
  4,
  8,
  3,
  6,
  6,
  8,
  4,
  6,
  5,
  12,
  10,
  5,
  12,
  4,
  4,
  6,
  5,
  12,
  12
 ],
 "k4_readings_above_every_copy": 0,
 "k4_top": [
  {
   "reading": "IIDPVLMA?????????????EASTNORTHEASTAFURGVT?????????????ECAITMOFDBERLINCLOCK?????????????ETAKTHIOXD",
   "judge": 4,
   "quad": -6.504,
   "kind": "chain",
   "setup": "WORLDCLOCK/keyword|UNDERGROUND/keyword|plain|beau",
   "L": 33
  },
  {
   "reading": "BTUMOP?HOMRAVJABAI???EASTNORTHEAST?NISHDHADEEX???DFEGOGAVGWBGC?BERLINCLOCK???RCAMLOIYRJUSV?UIETHE",
   "judge": 4,
   "quad": -6.54,
   "kind": "bulk",
   "setup": "WALL/keyword|PALIMPSEST/keyword|std|varbeau",
   "L": 28
  },
  {
   "reading": "MWVTAL?KJOVRJERINT???EASTNORTHEAST?TFCKHUVHISA???AUEAOFWECTHLD?BERLINCLOCK???KSIUZFINHAGUY?WHEOFA",
   "judge": 4,
   "quad": -6.57,
   "kind": "bulk",
   "setup": "DIGETAL/keyword|WALL/keyword|std|varbeau",
   "L": 28
  },
  {
   "reading": "STHASNALNGEJFADR?????EASTNORTHEASTEJJABLYDSMR?????FDFIROINMRGOVBERLINCLOCK?????HGRTFEXWNVERZUVEMP",
   "judge": 3,
   "quad": -6.655,
   "kind": "bulk",
   "setup": "CARNARVON/keyword|SOMEWHERE/keyword|kry|vig",
   "L": 29
  },
  {
   "reading": "TAOSOMDDLOUFEILF?????EASTNORTHEASTAQGGIROLCAX?????PFLCADCOLOBENBERLINCLOCK?????SMVYONNACZSSAODFIR",
   "judge": 3,
   "quad": -6.662,
   "kind": "bulk",
   "setup": "WONDERFUL/keyword|SOUTH/keyword|kry|vig",
   "L": 29
  }
 ],
 "plants": [
  {
   "seed": 2131,
   "L": 12,
   "k": 2,
   "skip": null,
   "slips": [
    53,
    70
   ],
   "planted_setting_found": true,
   "wrong_letters_in_reading": 0,
   "quad": -3.96,
   "judge": 96,
   "own_copies_judge_best": [
    7,
    4,
    8,
    4,
    18
   ],
   "found": true
  },
  {
   "seed": 2132,
   "L": 20,
   "k": 0,
   "skip": [
    49,
    21
   ],
   "slips": [],
   "planted_setting_found": true,
   "wrong_letters_in_reading": 0,
   "quad": -4.488,
   "judge": 88,
   "own_copies_judge_best": [
    5,
    5,
    12,
    6,
    4
   ],
   "found": true
  },
  {
   "seed": 2133,
   "L": 8,
   "k": 1,
   "skip": null,
   "slips": [
    77
   ],
   "planted_setting_found": true,
   "wrong_letters_in_reading": 3,
   "quad": -5.034,
   "judge": 85,
   "own_copies_judge_best": [
    5,
    4,
    8,
    12,
    5
   ],
   "found": true
  }
 ],
 "slip_cost_bits": {
  "1": 9.3,
  "2": 17.5,
  "lost step": 7.2
 },
 "controls": "20 shuffled copies (seeds 2140-2159); each plant against 5 shuffles of its own ciphertext",
 "exhaustive": "yes"
}
```

Notes: 35,343 tables x lags 1-52; K4 shortest lag with <= 2 breaks 24, lost step 24; copies [17, 17, 17, 17, 18, 18, 18, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24]; judge sent 194, K4 best 4, copies best 12; plants found [True, True, True]


