# 0033-trifid-keyword-cubes-and-annealing: Trifid: the 27-cell cube that fractionates letters, with keyword cubes tested exactly and free cubes annealed

**Family:** 4-visual-spatial  
**Parent:** none (root)  
**Decision:** reverted  
**Run:** 2026-10-15T07:47:21+00:00, 107.5 s, status ran  
**Time by phase:** design 17 s, implement 67 s, test 84 s, run 108 s, record 0 s

## In plain words

Trifid turns each letter into three small digits, like an address with floor, row and seat in a 27-seat cube, writes the addresses of a few letters in rows, and then reads the digits off in a different grouping, so each new letter is made from pieces of three old ones. It is one of the few old ciphers that can handle all 26 letters plus the question mark the sculpture already uses. We first try cubes built from the puzzle's words, then let a computer rearrange the cube by trial and error, rewarding every known letter it gets right.

## Walkthrough, by hand

1. Fill a cube with KRYPTOSABCDEFGHIJLMNQUVWXZ? in order: K is at (0,0,0), R at (0,0,1), ... the 27th symbol ? at (2,2,2).
2. Take period 5 and the first carved block OBKRU.
3. Write each letter's three digits in a column: O gives (0,1,2) in this cube, and so on for five letters.
4. Read the 15 digits row by row into one line and cut it into five triples: those are the five message letters' addresses.
5. Look them up in the cube.
6. Do this for every block, then check positions 22 to 34 and 64 to 74 against EASTNORTHEAST and BERLINCLOCK.
7. Count the hits; 24 means the cube and period are right.

## Worked example (generated)

```
cube in KRYPTOS order with ? last; period 5, first block OBKRU

O -> (0, 1, 2)
B -> (0, 2, 2)
K -> (0, 0, 0)
R -> (0, 0, 1)
U -> (2, 1, 0)
digits in a line: 012022000001210; cut into rows of 5: [[0, 1, 2, 0, 2], [2, 0, 0, 0, 0], [0, 1, 2, 1, 0]]
message letters: SDQRM

full decryption at period 5: SDQRMRDVZW?CSJQEWUEQMG?JDXRWMRECIRYSEFWILMJMYTBSWZOEEDUDYJHXMRIILTDOUCMMHDEHDEESPGDEUDLHRPKUDXCPN; crib hits 2 of 24
```

## Lineage

Inherits from nothing; this is a root experiment. What changed: New root in family 4. Trifid is the one classical fractionating cipher that fits 26 letters plus the question mark; the 25-letter-square systems are dead because all 26 letters occur in K4. Keyword-built cubes are tested exactly; free cubes are searched by simulated annealing on crib hits.

## Hypothesis (domain expert)

Delastelle's trifid (1901; in the ACA list and the manuals Scheidt taught from, C5) maps each of 27 symbols to a point in a 3x3x3 cube, writes a block of p letters as three coordinate rows, and reads the rows off in triples: a spatial system in Sanborn's sense (C3) and a matrix in his (C1), with the sculpture's own '?' as the 27th symbol. Playfair, bifid and the four-square family are dead because K4 uses all 26 letters (knowledge/04-structure.md); a 2x13 grid cannot fractionate; trifid can. Two tests. Exact: cubes built from every vocabulary word by the four Friedman mixings with '?' first or last, periods 2-20, every alignment, scored by crib hits after decryption. Search: for periods 2-15 and every alignment, simulated annealing over free cubes with crib hits as the objective, two restarts each, then more iterations for the best settings. A true cube gives 24 of 24; chance gives about 1 of 24 per decryption. In a dry run the annealer, with a coordinate-level objective, reached only 17 of 24 on a planted free cube at the planted cube's own period and alignment, so the search is weak and its result is not a bound. Bounds: complete for keyword cubes only; free cubes stay open.

## Prediction

No keyword cube at any period and alignment gets more than 5 of 24 crib letters right. Annealing on free cubes reaches at most 10 of 24 at its best setting, the same as on shuffled K4. Zero candidates pass.

## Method

1. Build keyword cubes: for each vocabulary word and mixing, the 26-letter mixed alphabet with '?' appended or prepended, filled into the cube in order.
2. For each cube, period 2-20 and alignment, decrypt and count crib hits.
3. For periods 2-15 and alignments, anneal a random cube by swapping two symbols, accepting by crib hits with a temperature schedule, two restarts of 4,000 steps.
4. Re-anneal the five best settings with 20,000 steps.
5. Repeat the search on two shuffles of K4 for calibration.
6. Submit any decryption with all 24 cribs.

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
 "family": "trifid, 27-symbol cube, periods 2-20",
 "keyword_cubes": 498,
 "exact_decryptions": 104082,
 "exact_best_hits": [
  {
   "hits": 7,
   "cube": "CARNARVON/alt_vertical/?first",
   "period": 14,
   "offset": 9
  },
  {
   "hits": 6,
   "cube": "WONDERFULTHINGS/keyed_columnar/?last",
   "period": 10,
   "offset": 6
  },
  {
   "hits": 6,
   "cube": "WEBSTER/keyword/?last",
   "period": 8,
   "offset": 2
  },
  {
   "hits": 6,
   "cube": "SHADOWFORCES/keyed_columnar/?last",
   "period": 12,
   "offset": 9
  },
  {
   "hits": 6,
   "cube": "SHADOW/keyed_columnar/?first",
   "period": 14,
   "offset": 11
  },
  {
   "hits": 6,
   "cube": "INTERPRETATION/columnar/?last",
   "period": 2,
   "offset": 0
  },
  {
   "hits": 6,
   "cube": "DIGETAL/columnar/?first",
   "period": 19,
   "offset": 4
  },
  {
   "hits": 6,
   "cube": "CARTER/columnar/?first",
   "period": 16,
   "offset": 8
  },
  {
   "hits": 6,
   "cube": "BERLIN/columnar/?last",
   "period": 7,
   "offset": 5
  },
  {
   "hits": 6,
   "cube": "ALEXANDERPLATZ/keyword/?last",
   "period": 19,
   "offset": 17
  }
 ],
 "annealing_settings": 119,
 "annealing_best_by_setting": [
  {
   "hits": 17,
   "period": 14,
   "offset": 8
  },
  {
   "hits": 17,
   "period": 2,
   "offset": 0
  },
  {
   "hits": 16,
   "period": 15,
   "offset": 7
  },
  {
   "hits": 16,
   "period": 14,
   "offset": 7
  },
  {
   "hits": 16,
   "period": 8,
   "offset": 2
  },
  {
   "hits": 16,
   "period": 7,
   "offset": 5
  },
  {
   "hits": 16,
   "period": 5,
   "offset": 3
  },
  {
   "hits": 15,
   "period": 15,
   "offset": 4
  },
  {
   "hits": 15,
   "period": 14,
   "offset": 4
  },
  {
   "hits": 15,
   "period": 13,
   "offset": 7
  }
 ],
 "refined_best": [
  {
   "hits": 17,
   "period": 14,
   "offset": 8,
   "cube": "GDUSW?RNBLTPXJAKQVHYMCZFOIE"
  },
  {
   "hits": 17,
   "period": 2,
   "offset": 0,
   "cube": "UKBJSYEVGL?AZTQORMFPWCINXDH"
  },
  {
   "hits": 16,
   "period": 15,
   "offset": 7,
   "cube": "LMEFTKISZWJDNRO?HCQYBVUPAGX"
  }
 ],
 "shuffled_control_best_hits": [
  14,
  11
 ]
}
```

Notes: Keyword cubes: best 7 of 24 hits over 104082 decryptions. Annealing: best 17 of 24 after refinement (settings best 17); shuffled K4 reaches [14, 11].


