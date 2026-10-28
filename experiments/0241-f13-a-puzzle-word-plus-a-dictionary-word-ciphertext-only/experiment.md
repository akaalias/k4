# 0241-f13-a-puzzle-word-plus-a-dictionary-word-ciphertext-only: F13.4f, part 1: two key words added, one from the puzzle and one from the whole dictionary (0115's space), solved from the ciphertext alone: every puzzle word, start and rule subtracted, every dictionary rotation scored per column, the best read by quadgrams and MIX8m; K4 against 100 shuffles, plants at four word lengths

**Family:** 13-ciphertext-only  
**Parent:** 0234-f13-periodic-key-on-the-sculptures-tables-ciphertext-only  
**Decision:** reverted  
**Run:** 2026-10-27T22:16:55+00:00, 16511.2 s, status ran  
**Time by phase:** design 21 s, implement 101 s, test 100 s, run 16511 s, record 60 s

## In plain words

Using the sculpture's table twice, first with a word from the puzzle (like KRYPTOS or ABSCISSA) and then with any English word, is the same as using one key made by adding the two words. Earlier we used the known clue words to work out the second word directly. Here we pretend we know no clue word: for every puzzle word we take its effect off, then try every English word, from every starting letter, and keep the ones whose letters come out with English letter frequencies, then read the best in full. K4 is compared with shuffles of its own letters treated the same way, and hidden test messages tell us how long a second word this can still find.

## Walkthrough, by hand

1. Pick a rule (say Vigenere on the KRYPTOS table), a puzzle word (ABSCISSA) and where it starts (its first A at place 1).
2. Write ABSCISSA repeated under the carved letters and take it off each letter on the table: the text that remains has a single repeating key word left in it.
3. Guess that word's length, say 9, and write the remaining text in 9 columns.
4. For each column and each of the 26 shifts, note how English the column's letters look by their frequencies.
5. For every 9-letter English word, read from every starting letter, add up its letters' column scores; keep the 10 best.
6. Read those in full and keep the most English; do this for every puzzle word, start, rule and length, and compare K4's best with what shuffles of K4 reach.

## Worked example (generated)

```
Rule var on plain std, cipher std, key letters numbered on std; first word ORDINATE from 7, second HUP from 1

  carved            OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZ
  first word        EORDINATEORDINATEORDINATEORDINATEORDINATEORDINAT
  first word off    SPBUCBXHKVLOJFOEMTSEESLKZEHSZAGDWGFWEGQLNEJVMXZS
  second word       UPHUPHUPHUPHUPHUPHUPHUPHUPHUPHUPHUPHUPHUPHUPHUPH
  reading           MEIORIRWRPAVDUVYBAMTLMARTTOMOHASDAUDYVXFCLDKTROZ

The search never reads the known letters: the second word is chosen by how English its columns look.
```

## Lineage

Inherits from 0234-f13-periodic-key-on-the-sculptures-tables-ciphertext-only. What changed: F13.4f (issue #85), part 1. 0115 closed this space exactly with the 24 known letters, which force the second word letter by letter (a lookup). Here the known letters are not read. For each of 24 rules (Vigenere, Beaufort or variant; plain, cipher and key alphabets standard or KRYPTOS), each puzzle word (0115's 171) and start (1,085 pairs), the puzzle word's stream is subtracted; what is left is a periodic key of the dictionary word's length n (3-24). Every rotation of every dictionary word of that length (2,248,310 rotations in all) is scored exactly by the English letter frequencies of the columns it decrypts (compiled, with early abandon), the 10 best per setting and length read in full by quadgrams, the 10 best per length over all settings rescored by MIX8m (0233). Statistic, copies and plants as 0234: max z over n against K4's 100 climbed shuffles; plants at n = 5, 10, 15, 20, 8 each, each against 10 own shuffles.

## Hypothesis (domain expert)

F3 (two-part key with a combiner; Scheidt's 'key word/s', C5; his key-splitting habit, 03-scheidt-said.md) and C20(a) 'layer two' as a second pass with a second word: the table applied twice with words of lengths m and n is one key k_i = a[(i + o1) mod m] + b[(i + o2) mod n]. 0115 killed it exactly for every puzzle word and every dictionary word of 3-24 letters, but only if the known letters sit where stated, letter for letter, with no slip (A1, A2); F13 is the hedge that never reads them. F13.1 (reports/f13-solvability-map.md): the space is about 24 x 1,085 x 2.2 million, 35 bits, far under the 173 that 97 letters carry by quadgrams, so it is decidable in principle; the question is whether a search can reach it. Subtracting the puzzle word leaves a periodic key, and a dictionary word scored per column by letter counts is the Friedman hand method with the key restricted to words. Pre-registered: S = max over n of (best MIX8m at n minus the shuffles' mean at n) / their sd; K4 flags at p < 0.05 against 100 shuffles (one test). A plant is found when its S is above all 10 own shuffles' S (null 1/11); a length is decided when at least 6 of its 8 plants are found.

## Prediction

Plants found 8 of 8 at n = 5 and 10, most at 15, fewer at 20 (columns of about 5 letters, where the per-column screen loses the true word among 2 million): decided to about n = 15. K4 inside its shuffles (p above 0.05), its readings English-like junk with at most 3-4 of 24 known letters in place (harness gate 2). F13.4f part 1 closes for the decided lengths and is blocked above them.

## Method

1. Texts: K4; 100 shuffles of K4; 32 plants (n = 5, 10, 15, 20; 8 each, half with X stops; random rule, puzzle word, start, dictionary word and rotation; Carter's held-out last 20%, no known word) and 10 shuffles of each: 453 texts.
2. Per text, rule (24) and puzzle word and start (1,085): x_i = the carved letter with the puzzle word's stream taken off. Per n = 3-24: a 26 x n table of column scores (sum of English log letter frequencies of the letters each shift gives); every dictionary rotation of length n scored as the sum of its letters' column scores, with early abandon against the 10th best; the 10 best read in full and scored by the harness's quadgram table.
3. Per n, the 10 best readings over all settings rescored by MIX8m; the best kept.
4. z per n against K4's shuffles; S = the largest z; K4 ranked among its shuffles; each plant among its own copies.
5. K4's best reading at each n submitted (key: rule, the two words and starts); gate 4's controls are the shuffles' best readings, scored as the harness scores.

## Result

Candidates returned: 22. Passed all gates: 0. Best crib hits among all candidates: 4/24
(EAST 2/4, NORTHEAST 2/9, BERLIN 0/6, CLOCK 0/5).
Best loss: 203.32894417471746 (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | cribs | 4/24 |  | `MEIORIRWRPAVDUVYBAMTLMARTTOMOHASDAUDYVXFCLDKTROZUDRGHFOLTICSPHIARKGLITOFNNUDAETFERINKIRHAPLMTRRAP` |  |
| 2 | cribs | 2/24 |  | `OTHENTPAGHGLEWINNJJGMBRATHAKRIRDTODSWTFSNEJBITATMPHVBEBAIPEZLEGUYPHTACCHATOMOVCTFDVAICHOFQFWEKRAT` |  |
| 3 | cribs | 1/24 |  | `ARNFRODSSRARYAKDETYEXIUNMPOHOGINZLETCOGNYTKASNULLDONTCLNKMRCUORTBPBOWOEVWRMSSMNRONGYEVESMICHTEIAG` |  |
| 4 | cribs | 3/24 |  | `FKWEAKDYTOMRKOIGUDEMBEDUBELDRUTCOFROCAHJASLOOFFTSLOICIAXCUSJETHAERBALDWUHWWBJICHOIRAUREILYXNLTIFT` |  |
| 5 | cribs | 0/24 |  | `MOZYGIRSESSMPSATBRCLEBOOMBAMULUUENMERMYZETEETSAIEPGWAPESFTENSSOOPHAKUKMXISTVMGNEJRNSFDZOKUTFCCHAN` |  |
| 6 | cribs | 2/24 |  | `DMAHUVEUVGFRHUXITISASOLYMAGFOHPZCOVESWITSAUCEADALNWSPJHPTNDTWOUGGREELIDNFUDVFADBEERYANCEUZTNEATSH` |  |
| 7 | cribs | 2/24 |  | `YROHYUNASJRCOSULMEAERSISDOMEXSVEUNIWDCGLURNOFTULLLGZVIOOBADEZHIMLRCHTHURYWITWPTVWIFEVERCINIRKINVI` |  |
| 8 | cribs | 1/24 |  | `SUKSPOTRRNPNUCDPILFYAANVOYTOMTDOOALESJURPOSEEOMYTITLOANYESCKRLIVITKUTSHOPJPDBFDHELTLUMCTPHENELXAN` |  |
| 9 | cribs | 0/24 |  | `PLOIFNARONARFWDLHSCOTHWERPAAFNIWVEHUNNGSMOAMHZDEJURAMCEINOPEPDIAMOTPAGFAIGNOLANMGWORAOJAONITXFCDI` |  |
| 10 | cribs | 2/24 |  | `SQMUJIBDFMWCPSHEPBRAVOASBESSDUMIMUMPAUSPOTTCHASUARIFEWEYDTUEEMECCKDEOISHUYPIUNAKOKIJILMAQSSNHAIMW` |  |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "item": "F13.4f part 1",
 "search_reads_known_letters": false,
 "rules": 24,
 "puzzle_words": 171,
 "puzzle_word_starts": 1085,
 "settings_per_text": 26040,
 "second_word_lengths": [
  3,
  24
 ],
 "dictionary_rotations": {
  "3": 3381,
  "4": 18210,
  "5": 48505,
  "6": 103593,
  "7": 165214,
  "8": 238012,
  "9": 290331,
  "10": 308035,
  "11": 285593,
  "12": 245412,
  "13": 194025,
  "14": 136682,
  "15": 88830,
  "16": 54016,
  "17": 30838,
  "18": 15156,
  "19": 8132,
  "20": 3960,
  "21": 1722,
  "22": 902,
  "23": 391,
  "24": 120
 },
 "rotations_scored_per_text_exhaustive": 58357202400,
 "screen": "per-column English letter frequencies, exact over every rotation (early abandon only drops rotations that cannot reach the top 10); top 10 per setting and n read by quadgrams; top 10 per n rescored by MIX8m (0233)",
 "texts": 453,
 "k4_copies": 100,
 "k4_statistic": 2.26,
 "k4_best_n": 4,
 "k4_p": 0.4158,
 "copies_statistic_max": 4.449,
 "copies_statistic_median": 2.081,
 "k4_rank_per_n_copies_at_or_above": {
  "3": 81,
  "4": 3,
  "5": 54,
  "6": 58,
  "7": 49,
  "8": 60,
  "9": 6,
  "10": 67,
  "11": 90,
  "12": 75,
  "13": 73,
  "14": 72,
  "15": 50,
  "16": 57,
  "17": 99,
  "18": 89,
  "19": 78,
  "20": 40,
  "21": 93,
  "22": 64,
  "23": 24,
  "24": 35
 },
 "plant_power": {
  "5": [
   8,
   8
  ],
  "10": [
   8,
   8
  ],
  "15": [
   8,
   8
  ],
  "20": [
   8,
   8
  ]
 },
 "plant_exact_recovery": {
  "5": [
   8,
   8
  ],
  "10": [
   8,
   8
  ],
  "15": [
   8,
   8
  ],
  "20": [
   8,
   8
  ]
 },
 "decided_n_at_6_of_8": [
  5,
  10,
  15,
  20
 ],
 "plants": {
  "plant5_0": {
   "kind": "clean",
   "S": 31.37,
   "own_max": 4.11,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "KOKRA",
   "word2_found_at_n": "KOKRA"
  },
  "plant5_1": {
   "kind": "xstops",
   "S": 28.65,
   "own_max": 3.33,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "GROVY",
   "word2_found_at_n": "GROVY"
  },
  "plant5_2": {
   "kind": "clean",
   "S": 41.48,
   "own_max": 3.59,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "MITCH",
   "word2_found_at_n": "MITCH"
  },
  "plant5_3": {
   "kind": "xstops",
   "S": 24.8,
   "own_max": 3.03,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "PECAN",
   "word2_found_at_n": "PECAN"
  },
  "plant5_4": {
   "kind": "clean",
   "S": 28.43,
   "own_max": 2.47,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "GONYS",
   "word2_found_at_n": "GONYS"
  },
  "plant5_5": {
   "kind": "xstops",
   "S": 30.32,
   "own_max": 3.38,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "DRONY",
   "word2_found_at_n": "DRONY"
  },
  "plant5_6": {
   "kind": "clean",
   "S": 37.08,
   "own_max": 4.35,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "MIRAK",
   "word2_found_at_n": "MIRAK"
  },
  "plant5_7": {
   "kind": "xstops",
   "S": 36.79,
   "own_max": 3.81,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "TROOP",
   "word2_found_at_n": "TROOP"
  },
  "plant10_0": {
   "kind": "clean",
   "S": 31.87,
   "own_max": 3.03,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "FORESTLIKE",
   "word2_found_at_n": "FORESTLIKE"
  },
  "plant10_1": {
   "kind": "xstops",
   "S": 30.05,
   "own_max": 3.51,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "SEDENTARIA",
   "word2_found_at_n": "SEDENTARIA"
  },
  "plant10_2": {
   "kind": "clean",
   "S": 32.31,
   "own_max": 3.89,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "TETRIGIDAE",
   "word2_found_at_n": "TETRIGIDAE"
  },
  "plant10_3": {
   "kind": "xstops",
   "S": 29.66,
   "own_max": 2.9,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "TYPOGRAPHY",
   "word2_found_at_n": "TYPOGRAPHY"
  },
  "plant10_4": {
   "kind": "clean",
   "S": 32.98,
   "own_max": 3.63,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "RHYACOLITE",
   "word2_found_at_n": "RHYACOLITE"
  },
  "plant10_5": {
   "kind": "xstops",
   "S": 18.52,
   "own_max": 3.03,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "OVERNIMBLE",
   "word2_found_at_n": "OVERNIMBLE"
  },
  "plant10_6": {
   "kind": "clean",
   "S": 30.92,
   "own_max": 2.74,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "NEOGRAPHIC",
   "word2_found_at_n": "NEOGRAPHIC"
  },
  "plant10_7": {
   "kind": "xstops",
   "S": 31.46,
   "own_max": 3.42,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "ASTERACEAE",
   "word2_found_at_n": "ASTERACEAE"
  },
  "plant15_0": {
   "kind": "clean",
   "S": 36.6,
   "own_max": 3.45,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "IMPENETRABILITY",
   "word2_found_at_n": "IMPENETRABILITY"
  },
  "plant15_1": {
   "kind": "xstops",
   "S": 32.65,
   "own_max": 2.88,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "GENIOHYOGLOSSAL",
   "word2_found_at_n": "GENIOHYOGLOSSAL"
  },
  "plant15_2": {
   "kind": "clean",
   "S": 32.76,
   "own_max": 3.2,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "HEMICRYSTALLINE",
   "word2_found_at_n": "HEMICRYSTALLINE"
  },
  "plant15_3": {
   "kind": "xstops",
   "S": 40.44,
   "own_max": 3.93,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "COUNTERVOLITION",
   "word2_found_at_n": "COUNTERVOLITION"
  },
  "plant15_4": {
   "kind": "clean",
   "S": 35.93,
   "own_max": 5.22,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "CHORIOALLANTOIC",
   "word2_found_at_n": "CHORIOALLANTOIC"
  },
  "plant15_5": {
   "kind": "xstops",
   "S": 35.69,
   "own_max": 2.73,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "AMALGAMATIONIST",
   "word2_found_at_n": "AMALGAMATIONIST"
  },
  "plant15_6": {
   "kind": "clean",
   "S": 28.97,
   "own_max": 4.38,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "PROPORTIONALISM",
   "word2_found_at_n": "PROPORTIONALISM"
  },
  "plant15_7": {
   "kind": "xstops",
   "S": 42.76,
   "own_max": 3.06,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "GLOSSOCARCINOMA",
   "word2_found_at_n": "GLOSSOCARCINOMA"
  },
  "plant20_0": {
   "kind": "clean",
   "S": 29.91,
   "own_max": 3.36,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "HYPSIBRACHYCEPHALISM",
   "word2_found_at_n": "HYPSIBRACHYCEPHALISM"
  },
  "plant20_1": {
   "kind": "xstops",
   "S": 30.11,
   "own_max": 2.73,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "TRANSUBSTANTIATIVELY",
   "word2_found_at_n": "TRANSUBSTANTIATIVELY"
  },
  "plant20_2": {
   "kind": "clean",
   "S": 30.6,
   "own_max": 2.85,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "COUNTERREVOLUTIONIZE",
   "word2_found_at_n": "COUNTERREVOLUTIONIZE"
  },
  "plant20_3": {
   "kind": "xstops",
   "S": 31.45,
   "own_max": 2.52,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "SYNCATEGOREMATICALLY",
   "word2_found_at_n": "SYNCATEGOREMATICALLY"
  },
  "plant20_4": {
   "kind": "clean",
   "S": 28.63,
   "own_max": 3.52,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "INTERNATIONALIZATION",
   "word2_found_at_n": "INTERNATIONALIZATION"
  },
  "plant20_5": {
   "kind": "xstops",
   "S": 33.84,
   "own_max": 4.35,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "PARAPHENYLENEDIAMINE",
   "word2_found_at_n": "PARAPHENYLENEDIAMINE"
  },
  "plant20_6": {
   "kind": "clean",
   "S": 36.14,
   "own_max": 3.38,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "UNPROPORTIONABLENESS",
   "word2_found_at_n": "UNPROPORTIONABLENESS"
  },
  "plant20_7": {
   "kind": "xstops",
   "S": 41.54,
   "own_max": 3.71,
   "found": true,
   "read_exactly_at_n": true,
   "true_word2": "KERATOCONJUNCTIVITIS",
   "word2_found_at_n": "KERATOCONJUNCTIVITIS"
  }
 },
 "scan_selfcheck": {
  "plant": "plant10_0",
  "key": {
   "mode": "beau",
   "pa": "kry",
   "ca": "kry",
   "ka": "std",
   "word1": "THIRTY",
   "start1": 4,
   "word2": "FORESTLIKE",
   "start2": 5
  },
  "reading_at_10_is_plant": true
 },
 "k4_best_readings": {
  "4": [
   "OTHENTPAGHGLEWINNJJGMBRATHAKRIRDTODSWTFSNEJBITATMPHVBEBAIPEZLEGUYPHTACCHATOMOVCTFDVAICHOFQFWEKRAT",
   {
    "mode": "vig",
    "pa": "kry",
    "ca": "kry",
    "ka": "kry",
    "word1": "DOORWAY",
    "start1": 1,
    "word2": "ZENU",
    "start2": 3
   }
  ],
  "7": [
   "MOZYGIRSESSMPSATBRCLEBOOMBAMULUUENMERMYZETEETSAIEPGWAPESFTENSSOOPHAKUKMXISTVMGNEJRNSFDZOKUTFCCHAN",
   {
    "mode": "vig",
    "pa": "kry",
    "ca": "std",
    "ka": "std",
    "word1": "THIS",
    "start1": 1,
    "word2": "POTWARE",
    "start2": 0
   }
  ],
  "10": [
   "SUKSPOTRRNPNUCDPILFYAANVOYTOMTDOOALESJURPOSEEOMYTITLOANYESCKRLIVITKUTSHOPJPDBFDHELTLUMCTPHENELXAN",
   {
    "mode": "var",
    "pa": "std",
    "ca": "std",
    "ka": "kry",
    "word1": "INVISIBLE",
    "start1": 3,
    "word2": "DILIGENTIA",
    "start2": 3
   }
  ]
 },
 "exhaustive": "the screen is exhaustive over the stated space; the readings kept per setting are its top 10",
 "expected_total": "about 14 core-minutes per text x 453 texts = about 106 core-hours, about 3.3 h on 32 cores (stated before the run)",
 "compute_seconds": 16487
}
```

Notes: K4 statistic 2.26 at n 4, p 0.416 against 100 shuffles; plant power n5 8/8, n10 8/8, n15 8/8, n20 8/8; decided n [5, 10, 15, 20]; 26,040 settings x 2,241,060 rotations per text


