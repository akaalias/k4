# 0098-sculpture-running-key-on-an-unknown-alphabet: A running key from the sculpture's texts on an unknown mixed alphabet, the table 'slightly different'

**Family:** 1-keyed-periodic  
**Parent:** 0017-running-key-from-the-sculpture-itself  
**Decision:** reverted  
**Run:** 2026-10-15T19:58:10+00:00, 472.5 s, status ran  
**Time by phase:** unattributed 35 s, run 472 s, record 0 s

## In plain words

Experiment 17 used the sculpture's own texts as a long key, but only with the two alphabets we know. Sanborn said his table was slightly different, so here the alphabet along the top of the table can be any order of the 26 letters. We do not need to guess it: for each key text and starting point, simple arithmetic on the 24 known letters shows whether any alphabet at all could make them fit.

## Walkthrough, by hand

1. Take the Morse as carved as the key text, starting at offset 0, and the Vigenere rule.
2. At place 22 the known letter is E, the carved letter F, the key letter some letter K22: position of F = position of E + position of K22 in the unknown alphabet.
3. Write one such equation for each of the 24 known places.
4. Solve them mod 2 and mod 13; if two different letters are forced to the same position, no alphabet works.
5. Repeat for every key text, offset, direction and rule, and on scrambled coppers.

## Worked example (generated)

```
key text: the Morse as carved, offset 0, Vigenere on an unknown alphabet X

place  known  carved  key  equation
   22      E       F    E  X(F) = X(E) + X(E)
   23      A       L    T  X(L) = X(A) + X(T)
   24      S       R    A  X(R) = X(S) + X(A)
   25      T       V    L  X(V) = X(T) + X(L)
   64      B       N    Y  X(N) = X(B) + X(Y)
   65      E       Y    O  X(Y) = X(E) + X(O)

some alphabet fits all 24: False
```

## Lineage

Inherits from 0017-running-key-from-the-sculpture-itself. What changed: 0017, 0004, 0021 and 0078 slid running keys along K4 on the standard and KRYPTOS alphabets only. Here the table's alphabet is unknown, any of the 26! orders (Quagmire III, as K1 and K2 use, with the alphabet left free): for each key text and offset the 24 known letters give linear equations in the unknown letter positions, solved exactly mod 2 and mod 13.

## Hypothesis (domain expert)

Type 3 and type 5 of directions.md together: keys concealed at the sculpture (C6(a), Scheidt) on a table Sanborn called 'slightly different' from the carved one (C11a); 0071 tried only alphabets one swap or move away. Model, Quagmire III with unknown alphabet X: X(c_i) = X(p_i) + s X(k_{o+i}) mod 26, s = +1 (Vigenere) or -1 (variant), and X(c_i) = X(k_{o+i}) - X(p_i) (Beaufort); each known letter gives one homogeneous equation in the 26 unknowns X(letter). X must be a bijection: two letters forced to the same value mod 2 and mod 13, or three forced together mod 13, is a contradiction (as in 0097). Key texts as in 0090: the carved tableau by rows, rows with the index column, and columns; the Morse as carved and in reverse order; the four ciphertexts; the K1-K3 plaintexts; Sanborn's 1989 letter, the 1991 dedication texts and the 2025 open letter; each forward and backward at every cyclic offset. Ten shuffled coppers.

## Prediction

A random equation set like these is consistent with some alphabet only rarely; K4's consistent (text, offset, rule) count lies inside the ten shuffled coppers' range, and no consistent setting decrypts to English. Zero candidates.

## Method

1. Build the key texts.
2. For each text, direction, offset and rule, write the 24 equations.
3. Solve over GF(2) and GF(13) and test the bijection.
4. Count consistent settings on K4 and on ten shuffled coppers.
5. For K4's consistent settings, report how many letter positions the equations fix.

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
 "family": "running key from the sculpture's texts on an unknown mixed alphabet (Quagmire III)",
 "sources": {
  "tableau rows fwd": 781,
  "tableau rows bwd": 781,
  "tableau rows with index column fwd": 807,
  "tableau rows with index column bwd": 807,
  "tableau columns fwd": 781,
  "tableau columns bwd": 781,
  "morse as carved fwd": 80,
  "morse as carved bwd": 80,
  "morse reversed order fwd": 80,
  "morse reversed order bwd": 80,
  "panel ciphertexts K1-K4 fwd": 865,
  "panel ciphertexts K1-K4 bwd": 865,
  "K1-K3 plaintexts fwd": 768,
  "K1-K3 plaintexts bwd": 768,
  "Sanborn 1989 letter fwd": 2176,
  "Sanborn 1989 letter bwd": 2176,
  "1991 dedication texts fwd": 4880,
  "1991 dedication texts bwd": 4880,
  "2025 open letter fwd": 2228,
  "2025 open letter bwd": 2228
 },
 "rules": [
  "vigenere",
  "variant",
  "beaufort"
 ],
 "settings": 80676,
 "k4_consistent": 0,
 "controls_consistent": [
  57,
  0,
  0,
  40,
  0,
  0,
  30,
  1,
  6,
  43
 ],
 "k4_consistent_settings": [],
 "controls": "10 shuffled coppers (seed 98), identical search"
}
```

Notes: 80,676 (text, offset, rule) settings. Consistent with some alphabet: K4 0, controls [57, 0, 0, 40, 0, 0, 30, 1, 6, 43].


