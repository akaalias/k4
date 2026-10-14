# 0020-short-periods-mixed-alphabets-consistency: The short periods come back: a periodic tableau at periods 1 to 52 with alphabets mixed from the puzzle's words

**Family:** 1-keyed-periodic  
**Parent:** 0005-quagmire-period-sweep-forced-keys  
**Decision:** reverted  
**Run:** 2026-10-14T18:04:15+00:00, 89.0 s, status ran  
**Time by phase:** design 28 s, implement 60 s, test 1366 s, run 89 s, record 0 s

## In plain words

Earlier we ruled out short secret words because two known letters that would share a letter of the word disagreed. But that reasoning assumed the table was built from the word KRYPTOS or the plain alphabet. If the table was built from another word, say PALIMPSEST, the same two known letters make a different demand and might agree. There is also a hint in the carved text that letters 21 apart were treated alike. So we rebuild the table from every word the puzzle knows, in four standard ways, and ask again which short lengths the 24 known letters allow.

## Walkthrough, by hand

1. Build the alphabet from PALIMPSEST: PALIMSETBCDFGHJKNOQRUVWXYZ, and use it for the plaintext; keep KRYPTOS for the ciphertext.
2. Position 22 is E, index 6; ciphertext F, index 11 in KRYPTOS; Vigenere gives key index 5.
3. Position 64, which is 42 later, is B, index 8; ciphertext N, index 19; key index 11.
4. At period 21 or 42 these two positions share a slot, so 5 must equal 11: it does not, and this alphabet pair is dead at 21 and 42.
5. Try the next pair; eleven such checks apply at period 21.
6. A pair that passes all eleven would be a real find: read off its forced key letters and see whether they spell a word.

## Worked example (generated)

```
plain alphabet PALIMPSEST/keyword PALIMSETBCDFGHJKNOQRUVWXYZ
cipher alphabet KRYPTOS KRYPTOSABCDEFGHIJLMNQUVWXZ

period 21 collisions: positions 42 apart share a slot

pos  plain  cipher  key index    pos  plain  cipher  key index   agree?
 22    E      F        6         64    B      N       11       no
 23    A      L       16         65    E      Y       22       no
 24    S      R       22         66    R      P       10       no
 25    T      V       15         67    L      V       20       no
 26    N      Q        4         68    I      T        1       no
 27    O      Q        3         69    N      T       14       no
```

## Lineage

Inherits from 0005-quagmire-period-sweep-forced-keys. What changed: 0005 excluded periods 1-26 and 30-52 under the standard and KRYPTOS alphabets only. Here the plain and cipher alphabets range over the four Friedman mixings of every vocabulary word, which changes every forced key letter and so every consistency check. Family 1 re-entered with a new alphabet source.

## Hypothesis (domain expert)

K4's eleven width-21 vertical repeats and the width-7 doublet column (0018, knowledge/04-structure.md) are what a key of period 21 or 42 would leave: positions 21 apart share a key letter, so English bigrams repeat vertically. 0005 and 0011 killed periods 1-26 and 30-52, but only with plain and cipher alphabets in {standard, KRYPTOS}; a tableau built on PALIMPSEST, ABSCISSA or any other word (Scheidt's keyword alphabets, C5, C29) gives different forced key indices and was never swept at these periods. For each pair of alphabets from the pool (standard, KRYPTOS, four mixings of each vocabulary word, 248 in all) and each of three modes, the forced key index at every crib position follows; for each period 1-52 the slots that collide must agree. Period 21 has eleven collisions, so a surviving pair there has chance probability 26 to the minus eleven per trial against 184,512 trials. Survivors at any period get the forced key letters read in the standard, KRYPTOS and keyword-mixed alphabets and scored as English; a vocabulary match is decrypted and submitted. Bounds: complete for this alphabet pool, periods 1-52, and the three modes.

## Prediction

No alphabet pair revives periods 1-26 or 30-52 except by chance at the periods with the fewest collisions, 23 to 26, where a few survivors appear per period; 30 to 52 are counted only. Period 21 and 42 have no survivor. No survivor's forced key matches the vocabulary; zero candidates pass.

## Method

1. Build the alphabet pool.
2. For each plain alphabet, cipher alphabet and mode, compute the forced key index at each of the 24 crib positions.
3. For each period 1-52, group the positions by slot and reject on any disagreement.
4. Count survivors by period, with a shuffled-K4 control.
5. For survivors, read the forced indices in each keyword-mixed key alphabet, match the fragment against the vocabulary and K1-K3 windows, score it as English, and decrypt any match.

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
 "family": "periodic tableau, alphabets mixed from the vocabulary, periods 1-52",
 "alphabets": 248,
 "alphabet_pairs_x_modes": 184512,
 "survivors_by_period": {
  "1": 0,
  "2": 0,
  "3": 0,
  "4": 0,
  "5": 0,
  "6": 0,
  "7": 0,
  "8": 0,
  "9": 0,
  "10": 0,
  "11": 0,
  "12": 0,
  "13": 0,
  "14": 0,
  "15": 0,
  "16": 0,
  "17": 0,
  "18": 0,
  "19": 0,
  "20": 0,
  "21": 0,
  "22": 0,
  "23": 0,
  "24": 1,
  "25": 0,
  "26": 7454,
  "27": 184512,
  "28": 184512,
  "29": 184512,
  "30": 7339,
  "31": 285,
  "32": 12,
  "33": 0,
  "34": 0,
  "35": 0,
  "36": 0,
  "37": 0,
  "38": 0,
  "39": 0,
  "40": 0,
  "41": 0,
  "42": 0,
  "43": 0,
  "44": 0,
  "45": 0,
  "46": 0,
  "47": 0,
  "48": 1,
  "49": 0,
  "50": 0,
  "51": 287,
  "52": 7454
 },
 "shuffled_k4_survivors_by_period": {
  "1": 0,
  "2": 0,
  "3": 0,
  "4": 0,
  "5": 0,
  "6": 0,
  "7": 0,
  "8": 0,
  "9": 0,
  "10": 0,
  "11": 0,
  "12": 0,
  "13": 0,
  "14": 0,
  "15": 0,
  "16": 0,
  "17": 0,
  "18": 0,
  "19": 0,
  "20": 0,
  "21": 0,
  "22": 0,
  "23": 0,
  "24": 0,
  "25": 19,
  "26": 7204,
  "27": 184512,
  "28": 184512,
  "29": 184512,
  "30": 7243,
  "31": 286,
  "32": 0,
  "33": 0,
  "34": 0,
  "35": 0,
  "36": 0,
  "37": 0,
  "38": 0,
  "39": 0,
  "40": 0,
  "41": 0,
  "42": 0,
  "43": 0,
  "44": 0,
  "45": 0,
  "46": 0,
  "47": 0,
  "48": 0,
  "49": 0,
  "50": 19,
  "51": 316,
  "52": 7204
 },
 "short_periods_with_survivors": {
  "24": 1,
  "26": 7454
 },
 "period_21_survivors": 0,
 "period_42_survivors": 0,
 "best_english_fragments": [
  {
   "score": -5.215,
   "period": 26,
   "plain": "CIA/alt_vertical",
   "cipher": "COMPASS/keyword",
   "key_alphabet": "POSITION/keyword",
   "mode": "beau",
   "fragment": "HPIEIAFL...MMPLEASUNISBYAT"
  },
  {
   "score": -5.23,
   "period": 26,
   "plain": "KRYPTOS/alt_vertical",
   "cipher": "DIGITAL/keyed_columnar",
   "key_alphabet": "WEBSTER/keyword",
   "mode": "vig",
   "fragment": "YUNFORPW...RNUINBATEPANGFW"
  },
  {
   "score": -5.249,
   "period": 26,
   "plain": "CIA/alt_vertical",
   "cipher": "COMPASS/keyword",
   "key_alphabet": "SOMEWHERE/keyword",
   "mode": "beau",
   "fragment": "ISEDERFL...NNSLDRMTHEMAYRW"
  },
  {
   "score": -5.253,
   "period": 26,
   "plain": "WORLDCLOCK/columnar",
   "cipher": "WILLIAMWEBSTER/columnar",
   "key_alphabet": "INVISIBLE/keyword",
   "mode": "beau",
   "fragment": "EAXORTOR...IXATTEESGROATAH"
  },
  {
   "score": -5.26,
   "period": 26,
   "plain": "SHADOWFORCES/alt_vertical",
   "cipher": "PALIMPSEST/alt_vertical",
   "key_alphabet": "CLOCK/keyword",
   "mode": "beau",
   "fragment": "WVMENATV...KOVEDTHUYWINITA"
  },
  {
   "score": -5.277,
   "period": 26,
   "plain": "KRYPTOS/keyed_columnar",
   "cipher": "TUTANKHAMEN/keyed_columnar",
   "key_alphabet": "SOUTH/keyword",
   "mode": "beau",
   "fragment": "BEENTFST...OKENAYEDRVEABSD"
  },
  {
   "score": -5.309,
   "period": 26,
   "plain": "CIA/alt_vertical",
   "cipher": "COMPASS/keyword",
   "key_alphabet": "INTERPRETATION/keyword",
   "mode": "beau",
   "fragment": "HIEDEAFL...MMILDATUPETOYAR"
  },
  {
   "score": -5.332,
   "period": 26,
   "plain": "MAGNETIC/alt_vertical",
   "cipher": "UNDERGRUUND/keyword",
   "key_alphabet": "TWO/keyword",
   "mode": "vig",
   "fragment": "SEIMPDFT...THETTENBIQUEROC"
  },
  {
   "score": -5.35,
   "period": 26,
   "plain": "ORDINATE/keyed_columnar",
   "cipher": "EAST/columnar",
   "key_alphabet": "ILLUSION/keyword",
   "mode": "beau",
   "fragment": "BOVECSZF...HGORSAFTENLEDDO"
  },
  {
   "score": -5.351,
   "period": 26,
   "plain": "DESPARATLY/alt_vertical",
   "cipher": "DESPERATELY/keyed_columnar",
   "key_alphabet": "WILLIAMWEBSTER/keyword",
   "mode": "varbeau",
   "fragment": "REATOLHW...VSEBUSEFCOFANIT"
  },
  {
   "score": -5.363,
   "period": 26,
   "plain": "CARNARVON/columnar",
   "cipher": "TUTANKHAMUN/keyed_columnar",
   "key_alphabet": "SHADOW/keyword",
   "mode": "beau",
   "fragment": "WSRINJUS...MASITBISONRDLEX"
  },
  {
   "score": -5.385,
   "period": 26,
   "plain": "TUTANKHAMUN/columnar",
   "cipher": "MAGNETIC/keyword",
   "key_alphabet": "INVISIBLE/keyword",
   "mode": "varbeau",
   "fragment": "RECPGUEA...YMEGRALAIMSTALU"
  },
  {
   "score": -5.41,
   "period": 26,
   "plain": "EGYPT/alt_vertical",
   "cipher": "WEST/alt_vertical",
   "key_alphabet": "MYSTERY/keyword",
   "mode": "beau",
   "fragment": "DLMAGGOD...IALLBACELESODJS"
  },
  {
   "score": -5.418,
   "period": 26,
   "plain": "SCHEIDT/columnar",
   "cipher": "SHADOW/alt_vertical",
   "key_alphabet": "INTERPRETATION/keyword",
   "mode": "beau",
   "fragment": "HSETPBIX...ZLSSESSEINTHAQC"
  },
  {
   "score": -5.418,
   "period": 26,
   "plain": "DIGITAL/alt_vertical",
   "cipher": "LUCID/keyed_columnar",
   "key_alphabet": "LOCATION/keyword",
   "mode": "varbeau",
   "fragment": "HITHIPYE...UCILPSWITFLASRE"
  }
 ],
 "vocab_matches": 0
}
```

Notes: 184512 alphabet pairs x modes, periods 1-52. Short periods with survivors: {24: 1, 26: 7454}. Period 21: 0, period 42: 0. 0 vocabulary matches.


