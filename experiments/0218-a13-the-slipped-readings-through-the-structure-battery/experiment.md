# 0218-a13-the-slipped-readings-through-the-structure-battery: A13.4: every 24-of-24 reading of 0207, 0212, 0213 and 0214 (A1's slipped searches) regenerated with their frozen searches for K4 and the same 20 scrambled copies, through the 14-test structure battery, with masked plants through 0207's search

**Family:** 1-keyed-periodic  
**Parent:** 0217-a13-the-backwards-reading-of-0034-against-more-fresh-copies  
**Decision:** error  
**Run:** 2026-10-25T13:25:34+00:00, 726.3 s, status error  
**Time by phase:** unattributed 1042 s, run 726 s, record 0 s

## In plain words

The searches that allowed for one or two enciphering mistakes produced readings with every known letter right but gibberish elsewhere. If the message was disguised before it was enciphered, the right one would look like gibberish too. We rerun those searches exactly, on the carving and on the same scrambled copies they used, and test every reading for 14 kinds of hidden pattern; the carving counts only if it beats all the copies. We also hide disguised messages with mistakes of our own and check the tests notice them.

## Walkthrough, by hand

1. Rerun one of the slip searches, say 0207, on the carving: every key length 1-26 and table, up to three known letters allowed wrong.
2. Keep every reading it lets through.
3. Score each reading on 14 pattern tests and keep the best value per test.
4. Do the same on the 20 scrambled copies 0207 used.
5. On each test, see whether the carving beats all 20 copies; about three of the 56 comparisons will by luck, so each that does is rerun against fresh copies until one catches up.

## Worked example (generated)

```

```

## Lineage

Inherits from 0217-a13-the-backwards-reading-of-0034-against-more-fresh-copies. What changed: A13.4 (Stage 2, step 3, issue #75). Since 2026-10-18 four experiments kept K4 readings with all 24 known letters in place: 0207 (periodic key on the sculpture's tables, up to 3 slips), 0212 (ciphertext autokey and progressive key, 2 slips or a lost step), 0213 (plaintext autokey, 2 broken links or a lost step) and 0214 (a move then the table, 2 slips). None kept its copies' readings. Here each frozen attack.py's own per-text search is called on K4 and on the same 20 seeded copies it used (tools/a13_check.py's pass 4), every reading it returns goes through the battery, and K4 is ranked per experiment and test. Pre-registered 2026-10-21 in reports/a13-structure-check.md: 56 cells, flag at p < 0.05/56, candidates replicated sequentially (seeds 4113 on). New in this run: masked planted messages with slips through 0207's search.

## Hypothesis (domain expert)

A13 with A1 (knowledge/12-assumptions.md): a masked plaintext (C4(a), Scheidt's 'I masked the English language'; C19, X and Q stops) enciphered with a slip or two (C17(b), Sanborn's 'sloppy'). The readings are those A1's exact searches let through: 0207 (8 table classes, key lengths 1-26, k <= 3), 0212 (ciphertext autokey on 487,734 table setups, k <= 2 or a lost step; progressive key, k <= 2), 0213 (plaintext autokey lags 1-52, 2 breaks or a lost step), 0214 (1,847,590 landings of 0110-0114 and the type-1 library, both orders, k <= 2). Statistic: per experiment and test, the best value over a text's readings ('?' read as unknown, the 24 known letters set as the candidates set them); K4's rank among its 20 copies, ties against K4. 0199, 0201-0206 and 0208-0211 kept no K4 reading (nothing fits K4, or a free alphabet leaves it undetermined): noted, not rerun.

## Prediction

K4 strictly above every copy in about 56/21 = 2.7 cells, none replicating; no flag. Every saved K4 candidate of the four experiments is among the regenerated readings. The masked plants through 0207 are found by their mask's own test in most cases, because 0207's readings at lengths 13 and 20 are fixed by the known letters and the planted reading itself is among them. Zero candidates pass gate 4.

## Method

1. For 0207, 0212, 0213, 0214: rebuild the frozen search's state as its run() does, call its per-text search on K4 and its 20 copies (its own shuffled, its own seeds), keep every reading.
2. Check every saved K4 candidate is among K4's regenerated readings.
3. Battery on every reading; per text and test the best value; rank K
4. 4. A cell where K4 is strictly above every copy is a candidate: fresh copies (the experiment's shuffled, seeds 4113 on) eight at a time until one is at or above K4 (not a flag), 1,123 all below (a flag), or the clock.
5. Plants: three per mask (none, reversal, X between words, X every kth letter), Carter 1923 masked then the known letters set, enciphered by 0207's own plant routine with 2 slips at lengths 13 and 20; found when the mask's own test on the plant's readings is strictly above every one of K4's 20 copies.

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
  File "/Users/alexisrondeau/Workshop/cryptos/_runner.py", line 41, in main
    res = attack.run(ctx) or {}
          ~~~~~~~~~~^^^^^
  File "/Users/alexisrondeau/Workshop/cryptos/attack.py", line 158, in run
    pt = _masked(mask, prng)
  File "/Users/alexisrondeau/Workshop/cryptos/attack.py", line 112, in _masked
    return m.masked_plant(mask, rng)
           ~~~~~~~~~~~~~~^^^^^^^^^^^
  File "/Users/alexisrondeau/Workshop/cryptos/experiments/0216-a13-the-saved-readings-against-their-own-search-on-fresh-copies-rerun/attack.py", line 157, in masked_plant
    words, letters = _carter()
                     ~~~~~~~^^
  File "/Users/alexisrondeau/Workshop/cryptos/experiments/0216-a13-the-saved-readings-against-their-own-search-on-fresh-copies-rerun/attack.py", line 150, in _carter
    src = (ROOT / "knowledge/sources/carter-1923-tomb-of-tutankhamen-vol1.txt").read_text(errors="ignore").upper()
          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/pathlib/__init__.py", line 787, in read_text
    with self.open(mode='r', encoding=encoding, errors=errors, newline=newline) as f:
         ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/pathlib/__init__.py", line 771, in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/Users/alexisrondeau/Workshop/cryptos/experiments/0216-a13-the-saved-readings-against-their-own-search-on-fresh-copies-rerun/knowledge/sources/carter-1923-tomb-of-tutankhamen-vol1.txt'

```

