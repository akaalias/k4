# 0010-forced-key-stretches-mixed-alphabets: The same two forced key stretches, with the tableau's alphabets mixed from the puzzle's own words

**Family:** 1-keyed-periodic  
**Parent:** 0009-forced-key-stretches-read-as-english  
**Decision:** reverted  
**Run:** 2026-10-14T16:49:03+00:00, 80.0 s, status ran  
**Time by phase:** design 13 s, implement 52 s, test 76 s, run 80 s, record 0 s

## In plain words

The table on the sculpture starts with the word KRYPTOS and then the rest of the alphabet. The old hand methods the designer taught allowed any word to start the alphabet, and four ways of shuffling it afterwards. So we repeat the last experiment with every word from the puzzle's world, PALIMPSEST, ABSCISSA, BERLIN, CLOCK and the rest, as the word that starts the alphabet, for the message letters, the carved letters and the secret word alike. If some choice makes the 13 pinned letters of the secret word read like English, that choice is probably the real one.

## Walkthrough, by hand

1. Write the alphabet starting with PALIMPSEST, dropping repeats: PALIMSETBCDFGHJKNOQRUVWXYZ.
2. Use it for the plaintext; keep the carved KRYPTOS alphabet for the ciphertext.
3. Position 22 is plaintext E, index 6 in the PALIMPSEST alphabet; ciphertext F, index 11 in KRYPTOS; Vigenere gives key index 5.
4. Do the same for positions 23 to 34 to get 13 key indices.
5. Now choose a key alphabet, say ABSCISSA mixed by columns, and read off the letter at each index.
6. Score the 13 letters by how common each run of four is in English.
7. Repeat for every choice of the three alphabets.
8. A stretch that scores like English, about -4.3 or better, is the signal.

## Worked example (generated)

```
plain alphabet  PALIMPSEST/keyword  PALIMSETBCDFGHJKNOQRUVWXYZ
cipher alphabet KRYPTOS             KRYPTOSABCDEFGHIJLMNQUVWXZ
key alphabet    ABSCISSA/columnar   ADJOUZBEKPVSFLQWCGMRXIHNTY

pos  plain  cipher  key index  key letter
 22    E      F         6         B
 23    A      L        16         C
 24    S      R        22         H
 25    T      V        15         W
 26    N      Q         4         U
 27    O      Q         3         O
 28    R      P        10         V
 29    T      R        20         X
 30    H      N         6         B
 31    E      G         7         E
 32    A      K        25         Y
 33    S      S         1         D
 34    T      S        25         Y

stretch: BCHWUOVXBEYDY   score -8.44 per quadgram (English about -4.3 at this length, noise about -8.3)
```

## Lineage

Inherits from 0009-forced-key-stretches-read-as-english. What changed: The plain, cipher and key alphabets may each be a keyword-mixed alphabet built from any vocabulary word by any of the four Friedman mixings, not only the standard and KRYPTOS alphabets.

## Hypothesis (domain expert)

0009 showed that under the standard and KRYPTOS alphabets the key stretches forced by the two crib runs read as noise. Scheidt taught the 1900-1945 hand systems (knowledge/03-scheidt-said.md), whose tableaux use keyword-mixed alphabets: a keyword then the rest of the alphabet, or the same written into a block and read by columns, by keyed columns, or alternately vertically (Friedman's mixings, kryptos/alphabets.py). K1 and K2 used KRYPTOS; K4 may use another word from the puzzle's world (C5, C6, C8, C29). Here the plain and cipher alphabets range over standard, KRYPTOS and the keyword mixing of each vocabulary word, and the key alphabet over all four mixings of each word, under Vigenere, Beaufort and variant Beaufort. For each triple the 13-letter stretch under EASTNORTHEAST and the 11-letter stretch under BERLINCLOCK are scored as English against the 0009 calibration. A key alphabet is a bijection on the stretch, so this is the test 0009 could not do. Bounds: exact copper, periods 27 and above, every triple of alphabets drawn as stated.

## Prediction

About 3 million stretch pairs are scored, so the best will sit around 4 standard deviations above noise by chance alone and still below the English mean. No stretch scores above -4.3 per quadgram. Zero candidates pass.

## Method

1. Build the alphabet pools: plain and cipher from standard, KRYPTOS and the keyword mixing of each vocabulary word; key from all four mixings of each word plus the two basics.
2. For each plain alphabet, cipher alphabet and mode, compute the forced key index at each crib position of both runs.
3. For each key alphabet, map the indices to letters and score the two stretches by mean log10 quadgram probability.
4. Keep the best 20 overall and the best per mode; compare with the English and noise distributions from 0009.

## Result

Candidates returned: 0. Passed all gates: 0. Best crib hits among all candidates: 0/24
(no candidates).
Best loss: None (0 is solved; 10 per missed crib letter). Best fitness: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| - | no candidates | | | | |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "periodic tableau, period 27+, alphabets mixed from vocabulary; forced key stretches scored as English",
 "plain_cipher_alphabets": 63,
 "key_alphabets": 248,
 "modes": 3,
 "stretches_scored": 5905872,
 "calibration_from": "0009",
 "best_overall": {
  "score": -3.813,
  "stretch": "EFORMESTATU",
  "run": "64-74",
  "plain": "LANGLEY/keyword",
  "cipher": "LUCIDMEMORY/keyword",
  "key": "INVISIBLE/columnar",
  "mode": "beau",
  "z_vs_random": 4.15,
  "z_vs_english": 0.85
 },
 "top_twenty": [
  {
   "score": -3.813,
   "stretch": "EFORMESTATU",
   "run": "64-74",
   "plain": "LANGLEY/keyword",
   "cipher": "LUCIDMEMORY/keyword",
   "key": "INVISIBLE/columnar",
   "mode": "beau",
   "z_vs_random": 4.15,
   "z_vs_english": 0.85
  },
  {
   "score": -3.88,
   "stretch": "YDAMETHINGR",
   "run": "64-74",
   "plain": "CIA/keyword",
   "cipher": "BERLINCLOCK/keyword",
   "key": "CARNARVON/keyword",
   "mode": "varbeau",
   "z_vs_random": 4.09,
   "z_vs_english": 0.72
  },
  {
   "score": -4.002,
   "stretch": "KHISTOSEARL",
   "run": "64-74",
   "plain": "PALIMPSEST/keyword",
   "cipher": "VIRTUALLYINVISIBLE/keyword",
   "key": "DESPERATELY/keyword",
   "mode": "beau",
   "z_vs_random": 3.97,
   "z_vs_english": 0.48
  },
  {
   "score": -4.006,
   "stretch": "ERSTORSHINGHC",
   "run": "22-34",
   "plain": "WEBSTER/keyword",
   "cipher": "HILL/keyword",
   "key": "WORLDCLOCK/alt_vertical",
   "mode": "beau",
   "z_vs_random": 4.37,
   "z_vs_english": 0.53
  },
  {
   "score": -4.053,
   "stretch": "THEHELECANF",
   "run": "64-74",
   "plain": "DIGITAL/keyword",
   "cipher": "TUTANKHAMUN/keyword",
   "key": "WEST/keyword",
   "mode": "varbeau",
   "z_vs_random": 3.93,
   "z_vs_english": 0.38
  },
  {
   "score": -4.053,
   "stretch": "THEHELECANF",
   "run": "64-74",
   "plain": "DIGITAL/keyword",
   "cipher": "TUTANKHAMEN/keyword",
   "key": "WEST/keyword",
   "mode": "varbeau",
   "z_vs_random": 3.93,
   "z_vs_english": 0.38
  },
  {
   "score": -4.066,
   "stretch": "DERATOPLANG",
   "run": "64-74",
   "plain": "SANBORN/keyword",
   "cipher": "DESPERATELY/keyword",
   "key": "EAST/columnar",
   "mode": "vig",
   "z_vs_random": 3.92,
   "z_vs_english": 0.36
  },
  {
   "score": -4.066,
   "stretch": "DERATOPLANG",
   "run": "64-74",
   "plain": "SANBORN/keyword",
   "cipher": "DESPARATLY/keyword",
   "key": "EAST/columnar",
   "mode": "vig",
   "z_vs_random": 3.92,
   "z_vs_english": 0.36
  },
  {
   "score": -4.066,
   "stretch": "IFTHESTCESA",
   "run": "64-74",
   "plain": "SECRET/keyword",
   "cipher": "LOCATION/keyword",
   "key": "ILLUSION/columnar",
   "mode": "vig",
   "z_vs_random": 3.92,
   "z_vs_english": 0.36
  },
  {
   "score": -4.071,
   "stretch": "KHISTOSERAL",
   "run": "64-74",
   "plain": "PALIMPSEST/keyword",
   "cipher": "VIRTUALLYINVISIBLE/keyword",
   "key": "DESPARATLY/keyword",
   "mode": "beau",
   "z_vs_random": 3.91,
   "z_vs_english": 0.35
  },
  {
   "score": -4.086,
   "stretch": "ITTHASEDEDF",
   "run": "64-74",
   "plain": "NORTH/keyword",
   "cipher": "BURIED/keyword",
   "key": "CIA/alt_vertical",
   "mode": "varbeau",
   "z_vs_random": 3.9,
   "z_vs_english": 0.32
  },
  {
   "score": -4.1,
   "stretch": "NDENDTHENGY",
   "run": "64-74",
   "plain": "LUCID/keyword",
   "cipher": "UNDERGROUND/keyword",
   "key": "BERLINWALL/keyword",
   "mode": "varbeau",
   "z_vs_random": 3.88,
   "z_vs_english": 0.29
  },
  {
   "score": -4.108,
   "stretch": "NTOCATHETIP",
   "run": "64-74",
   "plain": "LAYERTWO/keyword",
   "cipher": "LANGLEY/keyword",
   "key": "SHADOWFORCES/alt_vertical",
   "mode": "vig",
   "z_vs_random": 3.88,
   "z_vs_english": 0.28
  },
  {
   "score": -4.121,
   "stretch": "MFEARTHEOFE",
   "run": "64-74",
   "plain": "LOCATION/keyword",
   "cipher": "TWO/keyword",
   "key": "DESPARATLY/keyword",
   "mode": "varbeau",
   "z_vs_random": 3.86,
   "z_vs_english": 0.25
  },
  {
   "score": -4.128,
   "stretch": "PERSINLANTF",
   "run": "64-74",
   "plain": "LUCIDMEMORY/keyword",
   "cipher": "INVISIBLE/keyword",
   "key": "CLOCK/keyed_columnar",
   "mode": "varbeau",
   "z_vs_random": 3.86,
   "z_vs_english": 0.24
  },
  {
   "score": -4.129,
   "stretch": "HINSTODISAC",
   "run": "64-74",
   "plain": "RIDDLE/keyword",
   "cipher": "COMPASS/keyword",
   "key": "CARTER/alt_vertical",
   "mode": "beau",
   "z_vs_random": 3.86,
   "z_vs_english": 0.24
  },
  {
   "score": -4.15,
   "stretch": "YTHIRTHEERP",
   "run": "64-74",
   "plain": "ABSCISSAE/keyword",
   "cipher": "ALEXANDERPLATZ/keyword",
   "key": "ORDINATE/columnar",
   "mode": "vig",
   "z_vs_random": 3.84,
   "z_vs_english": 0.2
  },
  {
   "score": -4.175,
   "stretch": "CTMENSIDEDG",
   "run": "64-74",
   "plain": "INTERPRETATION/keyword",
   "cipher": "IQLUSION/keyword",
   "key": "WILLIAMWEBSTER/keyed_columnar",
   "mode": "vig",
   "z_vs_random": 3.81,
   "z_vs_english": 0.15
  },
  {
   "score": -4.187,
   "stretch": "EMEDEALLOFI",
   "run": "64-74",
   "plain": "ABSCISSA/keyword",
   "cipher": "NORTH/keyword",
   "key": "SOUTH/keyed_columnar",
   "mode": "varbeau",
   "z_vs_random": 3.8,
   "z_vs_english": 0.13
  },
  {
   "score": -4.188,
   "stretch": "EZTONTHERFA",
   "run": "64-74",
   "plain": "SOMEWHERE/keyword",
   "cipher": "WEBSTER/keyword",
   "key": "UNDERGRUUND/alt_vertical",
   "mode": "varbeau",
   "z_vs_random": 3.8,
   "z_vs_english": 0.12
  }
 ],
 "null_control_best": [
  [
   -3.801,
   "OISTATTHEBY"
  ],
  [
   -3.94,
   "MOFSINTHEDB"
  ],
  [
   -3.944,
   "BUSIVEREDEC"
  ]
 ],
 "null_control": "same search on three shuffles of the K4 letters; best score and stretch each"
}
```

Notes: Diagnostic, no candidates. 5905872 stretches scored over 63^2 x 248 x 3 alphabet triples.


