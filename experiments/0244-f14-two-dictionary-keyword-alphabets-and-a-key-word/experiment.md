# 0244-f14-two-dictionary-keyword-alphabets-and-a-key-word: F14.1: two different keyword alphabets from the whole dictionary, one on each side of the table, with a repeating key (free, then a key word): every pair of 208,064 alphabets matched exactly through an index, key lengths 1-26, both forms; K4 against 50 shuffles, plants at six lengths

**Family:** 14-scheidt-mask-keyed-by-words  
**Parent:** 0109-keyword-tables-from-the-whole-dictionary  
**Decision:** reverted  
**Run:** 2026-10-28T03:40:31+00:00, 93.5 s, status ran  
**Time by phase:** implement 140 s, test 114 s, run 94 s, record 29 s

## In plain words

Scheidt said he first disguised the English, then used the table. A simple way to do both by hand: scramble the alphabet with one secret word, and set the table's other alphabet with a second word, then use a repeating key word. That is two scrambled alphabets, which earlier tests left open because there are too many to try one by one. But if each scrambled alphabet comes from an English word, there are only about 200,000 of each, and the clue words tell us, for each key length, a few facts that link the two. We file every alphabet by those facts so that matching pairs fall out of a lookup, then check whether the key the clues force is an English word.

## Walkthrough, by hand

1. Choose a key length, say 19, and list the pairs of known places 19 apart: places 26 and 64 hold N and B, carved Q and N.
2. In the added form the same key letter took N to Q and B to N, so on the cipher alphabet Q sits as far after N as N sits after B on the plain alphabet.
3. For every cipher alphabet write down how far Q is from N (and the same for every other pair): that is its file number.
4. For every plain alphabet work out the file number it needs and look it up: the alphabets filed there are the only partners.
5. For each partner pair read off the key letters the known letters force and check whether they spell an English word from some starting letter.

## Worked example (generated)

```
Key length 19: known places in the same key slot, and what they ask of the two alphabets (added form)

places   known  carved   the gap on the cipher alphabet must equal the gap on the plain alphabet
 26,64    NB     QN       gap(Q to N) on the cipher alphabet = gap(N to B) on the plain alphabet
 27,65    OE     QY       gap(Q to Y) on the cipher alphabet = gap(O to E) on the plain alphabet
 28,66    RR     PP       gap(P to P) on the cipher alphabet = gap(R to R) on the plain alphabet
 29,67    TL     RV       gap(R to V) on the cipher alphabet = gap(T to L) on the plain alphabet
 30,68    HI     NT       gap(N to T) on the cipher alphabet = gap(H to I) on the plain alphabet
 31,69    EN     GT       gap(G to T) on the cipher alphabet = gap(E to N) on the plain alphabet
 32,70    AC     KM       gap(K to M) on the cipher alphabet = gap(A to C) on the plain alphabet
 33,71    SL     SZ       gap(S to Z) on the cipher alphabet = gap(S to L) on the plain alphabet
 34,72    TO     SF       gap(S to F) on the cipher alphabet = gap(T to O) on the plain alphabet

Every cipher alphabet is filed by its gaps; every plain alphabet looks up the gaps it needs.
```

## Lineage

Inherits from 0109-keyword-tables-from-the-whole-dictionary. What changed: F14.1 (issue #93), the first F14 item. 0109 put one dictionary keyword alphabet on both sides (or one side with the standard or KRYPTOS alphabet); 0020 paired the 248 puzzle words. Here the plain and cipher alphabets are any two of the 208,062 dictionary keyword alphabets plus standard and KRYPTOS (4.3 x 10^10 ordered pairs). At key length L the 24 known letters give checks only between places in the same key slot, and each check splits into a cipher-side difference (the cipher alphabet's places of the two carved letters) and a plain-side one (the plain alphabet's places of the two known letters), so every cipher alphabet is indexed by its difference vector and every plain alphabet looked up: all pairs in about 0.4 million lookups per length and form, exactly. Where pairs fit, the key letters the known letters force are checked against every dictionary and puzzle word of length L, every start, key letters numbered on the standard, KRYPTOS, plain or cipher alphabet with any indicator shift.

## Hypothesis (domain expert)

Scheidt's mask in its keyed form (C4(a), C5; 03-scheidt-said.md: 'I masked the English language', 'executed with the correct key word/s', 'building layers... mix and match'): a keyword monoalphabetic substitution before a keyed tableau, which is one Quagmire IV (plain alphabet = the mask's keyword alphabet, cipher alphabet = the table's). With free alphabets this is F1.2, consistent at lengths 8, 13, 16, 19, 20, 23, 24, 26 at the copies' rate (0123, 0124; prior-attempts database: 'satisfiable at random-text rates'), and 0136's bound leaves it to English. Two keyword alphabets are about 35 bits, not 176, so the known letters decide them: expected chance fits per form, 4.3 x 10^10 / 26^c with c same-slot checks, are under 0.01 at every length to 22, 5 at 23, 3,600 at 24 (where a key word of 24 letters, 5 in the dictionary, decides), and 2.5 x 10^6 and 1.7 x 10^9 at 25 and 26 (no dictionary word that long: counted only). Pre-registered: K4 fits no pair at 1-22 or matches no key word at 23-24 beyond the copies' counts; a plant (two random dictionary alphabets and a random dictionary key word) is found when its true pair fits and its key word is recovered.

## Prediction

K4 fits no alphabet pair at lengths 1-22 (copies: none or almost none); at 23 a handful of pairs on K4 and copies alike, none with a key word; at 24 thousands of pairs on both, none with a dictionary key word; 25-26 counted, as the copies. Plants found at every planted length (19, 20, 21, 22, 23, 24). Zero candidates.

## Method

1. Alphabets: the keyword-mixed alphabet of every dictionary word of 4+ letters (0109's 208,062 distinct), plus standard and KRYPTOS.
2. For each text, key length L = 1-26 and form (added: c = CA[p + k]; Beaufort: c = CA[k - p]): the same-slot pairs of known places; each cipher alphabet's vector of place differences of the carved letters, indexed; each plain alphabet's vector of the known letters' differences (negated for Beaufort) looked up. 25-26: counts only.
3. For each fitting pair at 1-24: the forced key at the covered slots, checked against every rotation of every dictionary word (3-24) and puzzle word of length L, key letters numbered on standard, KRYPTOS, the plain or the cipher alphabet, any shift. 3b. Where every key slot holds a known place (lengths to 13, and 15, 16), a fitting pair fixes the whole key and reading: those readings are kept for K4 and every copy and scored alike (added after a dry run showed 5 fitting pairs on K4 at 16 and none on 3 copies).
4. K4 and 50 shuffles (same search); 12 plants (2 per length 19-24) with their own search.
5. Any K4 key-word fit decrypted in full and submitted.

## Result

Candidates returned: 5. Passed all gates: 0. Best crib hits among all candidates: 24/24
(EAST 4/4, NORTHEAST 9/9, BERLIN 6/6, CLOCK 5/5).
Best loss: 7.76067198827605 (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | baseline | 24/24 | -10.662 | `KVXCCXHPKGLNYPWRRYQFBEASTNORTHEASTEIBHVVNNPTPYTMBJGPLYWHAVISBUCBERLINCLOCKIHOYTJNLRJRFTDMPDAPYANP` |  |
| 2 | baseline | 24/24 | -11.322 | `CGBDEWKNHHYPZKVEOJYGFEASTNORTHEASTTIFZBBKNCTVFSMVFVMYJGLZAICEDIBERLINCLOCKIKMFSLRMROKBDFJQNUVFDZI` |  |
| 3 | baseline | 24/24 | -10.920 | `KVXCCXZPKHLNYOWRRYQFBEASTNORTHEASTEIBZVVNNPTPFTMBJHPLYWZAVISBACBERLINCLOCKIZOFTJNLRJRFTDMPDAPFANP` |  |
| 4 | baseline | 24/24 | -11.088 | `JVXCAXPNJHLMZLWRRZQFDEASTNORTHEASTEIDPVVMNNTNGTKBHGNYZWPAWISBBCBERLINCLOCKIPOGTHMLRHSFTDKQDANGAMN` |  |
| 5 | baseline | 24/24 | -10.920 | `KVXCCXZPKHLNYOWRRYQFBEASTNORTHEASTEIBZVVNNPTPFTMBJHPLYWZAVISBACBERLINCLOCKIZOFTJNLRJRFTDMPDAPFANP` |  |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "item": "F14.1",
 "alphabets": 208064,
 "alphabet_pairs_per_form": 43290628096,
 "alphabet_source": "keyword-mixed alphabet of every dictionary word of 4+ letters (0109) plus standard and KRYPTOS",
 "key_lengths": [
  1,
  26
 ],
 "key_word_check_lengths": [
  1,
  24
 ],
 "key_word_rotations": {
  "3": 3384,
  "4": 18210,
  "5": 48505,
  "6": 103593,
  "7": 165249,
  "8": 238028,
  "9": 290340,
  "10": 308065,
  "11": 285659,
  "12": 245436,
  "13": 194025,
  "14": 136710,
  "15": 88845,
  "16": 54016,
  "17": 30838,
  "18": 15174,
  "19": 8132,
  "20": 3960,
  "21": 1722,
  "22": 902,
  "23": 391,
  "24": 120
 },
 "key_numbering": "standard, KRYPTOS, the plain alphabet or the cipher alphabet, any indicator shift 0-25",
 "fitting_pairs_k4_and_copies": {
  "1/added": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "1/beaufort": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "2/added": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "2/beaufort": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "3/added": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "3/beaufort": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "4/added": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "4/beaufort": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "5/added": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "5/beaufort": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "6/added": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "6/beaufort": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "7/added": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "7/beaufort": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "8/added": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "8/beaufort": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "9/added": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "9/beaufort": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "10/added": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "10/beaufort": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "11/added": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "11/beaufort": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "12/added": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "12/beaufort": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "13/added": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "13/beaufort": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "14/added": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "14/beaufort": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "15/added": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "15/beaufort": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "16/added": {
   "k4": 5,
   "copies_max": 4,
   "copies_median": 0.0,
   "copies_with_any": 8
  },
  "16/beaufort": {
   "k4": 0,
   "copies_max": 4,
   "copies_median": 0.0,
   "copies_with_any": 6
  },
  "17/added": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "17/beaufort": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "18/added": {
   "k4": 0,
   "copies_max": 34,
   "copies_median": 2.5,
   "copies_with_any": 33
  },
  "18/beaufort": {
   "k4": 0,
   "copies_max": 19,
   "copies_median": 3.0,
   "copies_with_any": 35
  },
  "19/added": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "19/beaufort": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "20/added": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "20/beaufort": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "21/added": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "21/beaufort": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "22/added": {
   "k4": 0,
   "copies_max": 0,
   "copies_median": 0.0,
   "copies_with_any": 0
  },
  "22/beaufort": {
   "k4": 0,
   "copies_max": 1,
   "copies_median": 0.0,
   "copies_with_any": 1
  },
  "23/added": {
   "k4": 5,
   "copies_max": 26,
   "copies_median": 2.0,
   "copies_with_any": 36
  },
  "23/beaufort": {
   "k4": 1,
   "copies_max": 47,
   "copies_median": 1.0,
   "copies_with_any": 33
  },
  "24/added": {
   "k4": 9037,
   "copies_max": 14361,
   "copies_median": 2173.0,
   "copies_with_any": 38
  },
  "24/beaufort": {
   "k4": 388,
   "copies_max": 78611,
   "copies_median": 2268.0,
   "copies_with_any": 38
  },
  "25/added": {
   "k4": 0,
   "copies_max": 15229012,
   "copies_median": 2140214.5,
   "copies_with_any": 43
  },
  "25/beaufort": {
   "k4": 0,
   "copies_max": 18163313,
   "copies_median": 1848049.5,
   "copies_with_any": 43
  },
  "26/added": {
   "k4": 3462413949,
   "copies_max": 3060173201,
   "copies_median": 1587679701.0,
   "copies_with_any": 48
  },
  "26/beaufort": {
   "k4": 605057178,
   "copies_max": 3060173201,
   "copies_median": 1797970116.0,
   "copies_with_any": 48
  }
 },
 "lowest_length_with_a_fit_k4": 16,
 "key_word_matches": {
  "k4": 0,
  "copies": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ]
 },
 "fully_fixed_readings": {
  "k4_count": 5,
  "k4_best": [
   [
    -7.907341560203145,
    16,
    "added",
    "HOLOZOIC",
    "AEOLOTROPISM",
    "KVXCCXHPKGLNYPWRRYQFBEASTNORTHEASTEIBHVVNNPTPYTMBJGPLYWHAVISBUCBERLINCLOCKIHOYTJNLRJRFTDMPDAPYANP"
   ],
   [
    -8.165019034515787,
    16,
    "added",
    "ZOOLOGIC",
    "AEOLOTROPISM",
    "KVXCCXZPKHLNYOWRRYQFBEASTNORTHEASTEIBZVVNNPTPFTMBJHPLYWZAVISBACBERLINCLOCKIZOFTJNLRJRFTDMPDAPFANP"
   ],
   [
    -8.165019034515787,
    16,
    "added",
    "OLOGICAL",
    "AEOLOTROPISM",
    "KVXCCXZPKHLNYOWRRYQFBEASTNORTHEASTEIBZVVNNPTPFTMBJHPLYWZAVISBACBERLINCLOCKIZOFTJNLRJRFTDMPDAPFANP"
   ],
   [
    -8.33359988119151,
    16,
    "added",
    "POLYOPIC",
    "AEOLOTROPISM",
    "JVXCAXPNJHLMZLWRRZQFDEASTNORTHEASTEIDPVVMNNTNGTKBHGNYZWPAWISBBCBERLINCLOCKIPOGTHMLRHSFTDKQDANGAMN"
   ],
   [
    -8.567795827200191,
    16,
    "added",
    "OCYROIDAE",
    "DIOPTROMETRY",
    "CGBDEWKNHHYPZKVEOJYGFEASTNORTHEASTTIFZBBKNCTVFSMVFVMYJGLZAICEDIBERLINCLOCKIKMFSLRMROKBDFJQNUVFDZI"
   ]
  ],
  "copies_count": [
   0,
   1,
   0,
   0,
   0,
   4,
   0,
   0,
   0,
   4,
   2,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   3,
   0,
   1,
   0,
   0,
   0,
   2,
   0,
   0,
   0,
   2,
   0,
   0,
   1,
   0,
   0,
   0,
   0,
   0,
   1,
   0,
   0,
   0,
   4,
   0,
   0,
   1,
   1,
   0
  ],
  "copies_best_score": [
   null,
   -8.549861192261597,
   null,
   null,
   null,
   -7.974335497600713,
   null,
   null,
   null,
   -8.180078342456236,
   -8.215046399430229,
   null,
   null,
   null,
   null,
   null,
   null,
   null,
   null,
   null,
   null,
   -7.634986792338311,
   null,
   -8.064764849437768,
   null,
   null,
   null,
   -8.281618839609017,
   null,
   null,
   null,
   -7.726176365298633,
   null,
   null,
   -8.348534247644848,
   null,
   null,
   null,
   null,
   null,
   -8.157110435173957,
   null,
   null,
   null,
   -7.80958043423949,
   null,
   null,
   -7.999165306323981,
   -8.243768985411782,
   null
  ],
  "k4_above_every_copy": false
 },
 "plants": {
  "plant19_0": {
   "L": 19,
   "found": true,
   "fits_at_L": 1,
   "matches": 1,
   "pa_word": "TELARY",
   "ca_word": "SCUMLIKE",
   "key_word": "UNOBJECTIONABLENESS",
   "key_numbering": "std"
  },
  "plant19_1": {
   "L": 19,
   "found": true,
   "fits_at_L": 3,
   "matches": 1,
   "pa_word": "PHARYNGES",
   "ca_word": "PSYCHOPANNYCHISM",
   "key_word": "PROCTOELYTROPLASTIC",
   "key_numbering": "std"
  },
  "plant20_0": {
   "L": 20,
   "found": true,
   "fits_at_L": 1,
   "matches": 1,
   "pa_word": "ADDUCE",
   "ca_word": "CULTURE",
   "key_word": "DIPHENYLQUINOMETHANE",
   "key_numbering": "plain"
  },
  "plant20_1": {
   "L": 20,
   "found": true,
   "fits_at_L": 1,
   "matches": 1,
   "pa_word": "CAPICHA",
   "ca_word": "OUTBOLTING",
   "key_word": "DIPHENYLCHLOROARSINE",
   "key_numbering": "std"
  },
  "plant21_0": {
   "L": 21,
   "found": true,
   "fits_at_L": 1,
   "matches": 1,
   "pa_word": "TREMATOID",
   "ca_word": "ECHITES",
   "key_word": "PHARYNGOEPIGLOTTIDEAN",
   "key_numbering": "std"
  },
  "plant21_1": {
   "L": 21,
   "found": true,
   "fits_at_L": 5,
   "matches": 1,
   "pa_word": "SUITOR",
   "ca_word": "UNORIGINATIVE",
   "key_word": "PHONETICOHIEROGLYPHIC",
   "key_numbering": "std"
  },
  "plant22_0": {
   "L": 22,
   "found": true,
   "fits_at_L": 15,
   "matches": 1,
   "pa_word": "HYPOSTASIZATION",
   "ca_word": "UPTIDE",
   "key_word": "HYDROPNEUMOPERICARDIUM",
   "key_numbering": "plain"
  },
  "plant22_1": {
   "L": 22,
   "found": true,
   "fits_at_L": 94,
   "matches": 3,
   "pa_word": "BREATH",
   "ca_word": "GLOSSINA",
   "key_word": "AQUOPENTAMMINECOBALTIC",
   "key_numbering": "kry"
  },
  "plant23_0": {
   "L": 23,
   "found": true,
   "fits_at_L": 8,
   "matches": 1,
   "pa_word": "EURYPROSOPIC",
   "ca_word": "PROANGIOSPERMIC",
   "key_word": "PSEUDOLAMELLIBRANCHIATE",
   "key_numbering": "kry"
  },
  "plant23_1": {
   "L": 23,
   "found": true,
   "fits_at_L": 73,
   "matches": 1,
   "pa_word": "UNDECIDEDNESS",
   "ca_word": "SULFHYDRYL",
   "key_word": "PSEUDOLAMELLIBRANCHIATE",
   "key_numbering": "cipher"
  },
  "plant24_0": {
   "L": 24,
   "found": true,
   "fits_at_L": 12295,
   "matches": 1,
   "pa_word": "GERMPROOF",
   "ca_word": "BRICKLENESS",
   "key_word": "TETRAIODOPHENOLPHTHALEIN",
   "key_numbering": "plain"
  },
  "plant24_1": {
   "L": 24,
   "found": true,
   "fits_at_L": 182305,
   "matches": 1,
   "pa_word": "SYNANGIC",
   "ca_word": "CHEMOTROPICALLY",
   "key_word": "TETRAIODOPHENOLPHTHALEIN",
   "key_numbering": "plain"
  }
 },
 "plants_found": 12,
 "plants_total": 12,
 "texts": 63,
 "copies": 50,
 "exhaustive": true,
 "compute_seconds": 74
}
```

Notes: 208,064 alphabets, 43,290,628,096 ordered pairs per form, key lengths 1-26. K4: first fit at L 16; key-word matches K4 0, copies max 0; plants found 12/12


