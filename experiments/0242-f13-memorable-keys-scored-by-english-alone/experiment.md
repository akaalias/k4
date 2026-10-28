# 0242-f13-memorable-keys-scored-by-english-alone: F13.5: memorable keys scored by English alone: key words, keyword tables, running keys from the named texts, autokey primers and keyword columnars from the source list, through the methods already built, no known letter read; K4 against 100 shuffles, plants per method

**Family:** 13-ciphertext-only  
**Parent:** 0241-f13-a-puzzle-word-plus-a-dictionary-word-ciphertext-only  
**Decision:** error  
**Run:** 2026-10-28T03:07:19+00:00, 31.3 s, status error  
**Time by phase:** test 742 s, run 31 s, record 0 s

## In plain words

The creators said the key could be remembered: a word, or a passage of a known text. Earlier runs checked every such key against the clue words. Here we check them again without looking at the clue words at all: every key word, every passage of the sculpture's texts and Carter's book, every keyword-scrambled table, read in full and kept only if the result reads as English. K4 is compared with shuffles of its own letters treated the same way, and hidden test messages made with keys from the same lists show whether a right key would stand out.

## Walkthrough, by hand

1. Take a key from the list, say the word ABSCISSA from its third letter, and a way of using the sculpture's table.
2. Decipher all 97 carved letters with it.
3. Score the result by how often its four-letter groups occur in English.
4. Do this for every key word and start, every passage of the named texts, every keyword table and every way of using the table; keep the best.
5. Do the same on shuffles of K4 and compare.

## Worked example (generated)

```

```

## Lineage

Inherits from 0241-f13-a-puzzle-word-plus-a-dictionary-word-ciphertext-only. What changed: F13.5 (issue #85). Every earlier key-source search (0004-0021, 0045-0053, 0109, 0115, 0117, 0154, 0210) decided by the 24 known letters. Here the same memorable keys are read with no known letter: five methods, every key from the source order (program.md: K1-K3 words, the sculpture's texts, the Morse, Carter, then the dictionary), every reading scored exhaustively by quadgrams, the 20 best per method rescored by MIX8m (0233). A: a periodic key word (every puzzle word and every dictionary word of 3-24 letters, every start) on the 24 rules of the sculpture's tables. B: keyword-mixed tables from the puzzle words (one side or both) with a puzzle key word. C: a running key from 0210's named texts, every offset, both directions, on the 24 rules. D: plaintext and ciphertext autokey primed by any puzzle or dictionary word, on the 24 rules. E: a keyword columnar keyed by a puzzle word, before or after the table with a puzzle key word. Statistic: max z over the five methods against K4's 100 shuffles; plants (8 per method, keys drawn from the same sources) each against 10 own shuffles.

## Hypothesis (domain expert)

C5 ('simple, can be remembered, executed with the correct key word/s'), C6(a) (keys concealed at the sculpture), C7(a) (K1-K3 words as keys), C25(a) (the Morse words), C20(a) (layer two). Each method was closed exactly with the known letters (0005, 0009-0011, 0020, 0053, 0109, 0115, 0117, 0154, 0210; autokeys 0002, 0003, 0025, 0064; keyword columnars 0110-0114). Those verdicts stand only if the 24 letters sit where stated, letter for letter, without slips (A1, A2) and the plaintext is not masked out of their places. F13.5 is that hedge: the key space is at most about 30 bits per method (log2 of 54 million settings), far under what 97 letters of English carry, and every setting is read, so where the known letters are exact this adds nothing; it decides only the cases where they are not. Pre-registered: S = max over the five methods of (best MIX8m minus the shuffles' mean) / their sd; K4 flags at p < 0.05 against 100 shuffles (one test); a plant is found when its S is above all 10 own shuffles' S; a method is decided when at least 6 of its 8 plants are found.

## Prediction

Plants found 8 of 8 in every method (the keys are read exhaustively, so the true key's reading is scored directly). K4 inside its shuffles (p above 0.05), its readings junk with at most 3-4 of 24 known letters in place (harness gate 2). F13.5 closes as exact over the stated key lists.

## Method

1. Key lists: 0115's 171 puzzle words (every start), the 234,288-word dictionary (lengths 3-24, every start: 2,241,060 rotations), keyword-mixed alphabets of the puzzle words, 0210's named texts both ways.
2. Every setting decrypted in compiled code and scored by the harness's quadgram table; the 20 best per method kept, rescored by MIX8m.
3. Texts: K4, 100 shuffles, 40 plants (8 per method, half with X stops, Carter's held-out text, keys drawn from the lists) and 10 shuffles of each.
4. z per method against K4's shuffles; S = the largest z; K4 ranked; each plant among its own copies.
5. K4's best reading per method submitted; gate 4's controls are the shuffles' best readings.

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
  File "/repo/attack.py", line 477, in run
    key = make_plant_key(m, rng)
  File "/repo/attack.py", line 441, in make_plant_key
    return {**base, "source": name, "offset": rng.randrange(len(K["sources"][name]) - N)}
                                              ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.14/random.py", line 312, in randrange
    raise ValueError("empty range for randrange()")
ValueError: empty range for randrange()

```

