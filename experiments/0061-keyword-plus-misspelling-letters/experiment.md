# 0061-keyword-plus-misspelling-letters: A puzzle word plus the misspelled letters as a second, short secret word

**Family:** 3-two-component-key  
**Parent:** 0024-keyword-plus-k2-coordinate-digits  
**Decision:** reverted  
**Run:** 2026-10-15T12:28:11+00:00, 1.4 s, status ran  
**Time by phase:** design 0 s, implement 0 s, test 30 s, run 1 s, record 0 s

## In plain words

Sanborn misspelled three words on purpose and said the misspellings matter. The wrong letters are Q, U and A; the right ones would be L, O and E. A few letters on the sculpture are also raised, spelling YAR. Here those letters become a second, very short secret word, added on top of a longer word from the puzzle or the solved messages, and the two together are used on the table. With both words fixed there is nothing to guess, so we simply count how many of the 24 known letters come out right, and compare with scrambled copies of the copper.

## Walkthrough, by hand

1. Take the word KRYPTOS and the short key QUA, on the standard alphabet: K=10, R=17, Y=24, P=15, T=19, O=14, S=18 and Q=16, U=20, A=0.
2. Place 22 uses letter 21 mod 7 = 0 of KRYPTOS, K=10, and letter 21 mod 3 = 0 of QUA, Q=16: the key is 10 + 16 = 26 = 0.
3. Under plain Vigenere on the standard alphabet the carved F at place 22 then reads F - 0 = F.
4. The message has E there, so this setting misses place 22.
5. Count the misses over all 24 known places, then do the same for every word, short key, sign and table.

## Worked example (generated)

```
place  word letter  short letter  key  carved  reads  message
   22      K            Q         0     F      F      E
   23      R            U        11     L      A      A
   24      Y            A        24     R      T      S
   25      P            Q         5     V      Q      T
```

## Lineage

Inherits from 0024-keyword-plus-k2-coordinate-digits. What changed: Experiments 24 and 38 added the K2 coordinates or numbers from the story to a puzzle word. Sanborn said the misspellings matter for their orientation, so here the second part is made of letters instead: the wrong letters Q, U and A from IQLUSION, UNDERGRUUND and DESPARATLY, the right letters L, O and E, the raised YAR, and their reorderings, added to every puzzle word and every word of the solved messages.

## Hypothesis (domain expert)

C10(a) and C22: the misspelt letters (Q in IQLUSION, U in UNDERGRUUND, A in DESPARATLY, and the dropped E of DESPERATELY) and the raised YAR as key material. Two-component key k[i] = W[i mod a] + s S[i mod b] (family 3, Scheidt's combined keys), W any vocabulary word or K1-K3/C13/C14 word, S every ordering of QUA, LOE, QUAE, LOEE and YAR, and DYAHR in carved order, s = +1 or -1; letters read as indices on the standard or KRYPTOS order; plain and cipher alphabets standard or KRYPTOS; Vigenere, Beaufort, variant Beaufort. The key is fully determined, so each setting decrypts and the 24 cribs are counted exactly. Control: the best count on ten shuffled coppers under the same settings. Bounds: complete for these words, orderings and conventions.

## Prediction

No setting recovers more than about 8 of the 24 known letters, the same as on the shuffles. Zero candidates pass.

## Method

1. List the long words and the short-key orderings.
2. For each convention, compute the key index each crib requires.
3. For each word, ordering, sign and key alphabet, form the key at the crib places and count matches.
4. Decrypt the best settings and submit any with all 24.
5. Repeat the count on ten shuffles.

## Result

Candidates returned: 1. Passed all gates: 0. Best crib hits among all candidates: 8/24
(EAST 1/4, NORTHEAST 1/9, BERLIN 3/6, CLOCK 3/5).
Best loss: 164.41576998481048 (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: 0034-complete-the-key-at-surviving-periods.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | cribs | 8/24 |  | `GIELISQGAHQIXAEFPFVXYEDLHQXFPBEJGAEXBRGGLTWKYWOVKORKOHYNPKAQHENPERSBNCLOJIWKUAXBBAMZUADAZUKZUIQQG` | KNOWS - QEAU on std; plain std, cipher std, beau |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "two-component key: a word plus a short key from the misspelt or raised letters",
 "long_words": 171,
 "short_keys": 55,
 "settings": 451440,
 "best_hits": 8,
 "best_setting": {
  "word": "KNOWS",
  "short": "QEAU",
  "sign": -1,
  "key_alphabet": "std",
  "plain": "std",
  "cipher": "std",
  "mode": "beau"
 },
 "control_best_hits": [
  8,
  8,
  11,
  7,
  8,
  8,
  9,
  7,
  7,
  7
 ]
}
```

Notes: 451,440 settings; best 8/24 known letters; ten shuffled coppers best [7, 7, 7, 7, 8, 8, 8, 8, 9, 11].


