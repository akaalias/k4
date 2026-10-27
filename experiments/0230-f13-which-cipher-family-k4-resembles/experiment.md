# 0230-f13-which-cipher-family-k4-resembles: F13.2: a classifier trained on 17 cipher families' own 97-letter ciphertexts (no known words), its power on held-out texts, and K4 named against 2,000 shuffles of itself

**Family:** 13-ciphertext-only  
**Parent:** 0168-k4-statistics-against-a-thousand-shuffles  
**Decision:** error  
**Run:** 2026-10-27T16:05:11+00:00, 40.3 s, status error  
**Time by phase:** design 235 s, implement 169 s, test 28 s, run 40 s, record 0 s

## In plain words

Before attacking a cipher, codebreakers often ask what kind it is: some kinds leave fingerprints, such as letters repeating at a fixed spacing. Here we build a sorting machine (a classifier): we make 4,000 fake K4s with each of 17 kinds of cipher, measure 155 things about each, and teach the machine to tell the kinds apart. We test it on fakes it has never seen, to know how often it is right, and then show it K4. Because K4's letter counts alone could fool it, K4 counts as looking like a kind only if it looks more like that kind than 2,000 shuffles of its own letters do.

## Walkthrough, by hand

1. Take 97 letters of English and encipher them with one kind of cipher and a random key.
2. Measure the result: how evenly letters are spread, how often a letter recurs 1, 2, 3 ... 60 places later, repeated pairs and triples, doublets.
3. Do this thousands of times for each of 17 kinds, and fit weights that turn the measurements into a guess of the kind.
4. Check the guesses on fresh fakes: the share right is the machine's power.
5. Measure K4 and 2,000 shuffles of K4's letters; a kind is named only if K4 scores higher for it than nearly every shuffle.

## Worked example (generated)

```

```

## Lineage

Inherits from 0168-k4-statistics-against-a-thousand-shuffles. What changed: F13.2 (issue #85), the first F13 run. 0168 measured K4 on 71 statistics one at a time against shuffles and found nothing outside them; F7 (0018, 0027) built ciphers by family and compared single statistics. Here the statistics are combined: 17 generators (one per family or cell of the map, keys drawn at random inside each family's space, plaintext from Carter's book with no known word, half of it Sanborn-style) make 4,000 ciphertexts each; every text is measured by 0168's 71 statistics, A13's 14 tests and 70 classic cipher-identification statistics (kappa at shifts 1-60, digraphic and even-pair I.C., delta I.C., repeats); a multinomial logistic classifier is trained on 3,000 per family and its power measured on 1,000 held-out per family, written from the other end of the book. Then K4's posterior for each family is ranked against 2,000 shuffles of K4, which keep its letter counts, so a family is named only for structure beyond the counts. The search never reads the 24 known letters.

## Hypothesis (domain expert)

Cipher-type identification (the ACA's and NCID's practice; Sinkov's statistics) asks which generator a ciphertext is typical of. F13.1 (reports/f13-solvability-map.md) lists the families English alone could decide; F13.2 asks whether K4's own statistics point at any of them, without the known letters. Classes: monoalphabetic, columnar transposition (width 2-30), substitution then transposition (F9), periodic key on any of six alphabet pairs (standard, KRYPTOS, mixed; Quagmire I-IV) in three forms at lengths 2-12, 13-26 and 27-60 (F1, F1.1, F1.2), progressive key (F1.9), ciphertext and plaintext autokey with primers 1-30 (F1.7), running key from English (F1.3), Gromark base 10 (F5), Hill 2x2 and 3x3, plain or affine (F8), trifid 27-cell cube with no 27th symbol in the output (F4), Chaocipher (F10.1), a move then the table and the table then a move (F6), and uniform random letters (the one-time pad, the null). Features: 0168's 71 (segment chi-squares, I.C. at 1-48 alphabets, repeats at widths 7, 21, 31: the width-7 doublet column and width-21 repeats among them, 04-structure.md), A13's 14 (tools/a13_structure.py), and 70 more. Tests C4(a)-(b) (a mask leaves a type signature?), C1(a) (move then table), C11a ('interval 7') and F7's fingerprints as features rather than single tests. Pre-registered: 34 cells (17 families x two feature sets: the item's named 85 and all 155); K4 names a family when its posterior for that family is above all but a share p < 0.05/34 = 0.00147 of 2,000 shuffles of K4, and that family's positive control (12 held-out plants per family, each against 1,000 of its own shuffles, the same rule) finds at least 6 of 12. A named family is a candidate, replicated with a retrained classifier and fresh shuffles before anything else.

## Prediction

Held-out accuracy well above chance (1/17) overall, near 100% for monoalphabetic, transposition, substitution then transposition and Hill; high for short periodic keys; but the flat families (long periodic keys, running key, autokeys, Gromark, Chaocipher, the move-and-table pairs, random letters) confused with each other near chance among themselves. K4 is put among the flat families; against its shuffles no family is named (p above 0.00147 in all 34 cells). Plants of the distinctive families are found against their own shuffles; plants of the flat families are not. Zero candidates.

## Method

1. Plaintexts: 97-letter windows of Carter's Tomb of Tut-ankh-Amen (the plants' source), half clean, half Sanborn-style (full stops as X, three letters changed); training from the first 80% of the book, held-out texts and plants from the last 20%. No known word is written in.
2. 17 generators, keys at random inside each family's space; 3,000 training and 1,000 held-out texts per family, in jobs of 100 with their own seeds.
3. 155 features per text: 0168's all_stats (frozen), A13's battery, and kappa at shifts 1-60, digraphic and even-pair I.C., delta I.C. on both alphabets, doublets, longest repeat, distinct letters, top count, English letter log-likelihood.
4. Multinomial logistic regression (numpy, L2 1e-3, Adam 3,000 steps, standardized features), one on the named 85 features and one on all 155. Power: held-out confusion matrix, recall per family, AUC of each family against random letters.
5. K4 and 2,000 shuffles of K4 through both models; per family the share of shuffles at or above K4's posterior.
6. Positive control: 12 held-out plants per family, each against 1,000 of its own shuffles, the same rule.

## Result

Candidates returned: 0. Passed all gates: 0. Best crib hits among all candidates: 0/24
(no candidates).
Best loss: None (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| - | no candidates | | | | |

### Bounds searched (the negative result this experiment leaves behind)

```
(none recorded)
```


Error:
```
Traceback (most recent call last):
  File "/repo/_runner.py", line 80, in main
    res = attack.run(ctx) or {}
          ~~~~~~~~~~^^^^^
  File "/repo/attack.py", line 516, in run
    for cls, split, chunk, F in pool.imap_unordered(_feat_job, jobs, chunksize=1):
                                ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.14/multiprocessing/pool.py", line 873, in next
    raise value
  File "/usr/local/lib/python3.14/multiprocessing/pool.py", line 540, in _handle_tasks
    put(task)
    ~~~^^^^^^
  File "/usr/local/lib/python3.14/multiprocessing/connection.py", line 212, in send
    self._send_bytes(_ForkingPickler.dumps(obj))
                     ~~~~~~~~~~~~~~~~~~~~~^^^^^
  File "/usr/local/lib/python3.14/multiprocessing/reduction.py", line 51, in dumps
    cls(buf, protocol).dump(obj)
    ~~~~~~~~~~~~~~~~~~~~~~~^^^^^
_pickle.PicklingError: Can't pickle <function _feat_job at 0x2abf1c5066c0>: it's not the same object as attack._feat_job
when serializing tuple item 2

```

