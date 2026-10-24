# 0215-a13-the-saved-readings-against-their-own-search-on-fresh-copies: A13.3: the 31 saved 24-of-24 readings of eight experiments put through the 14-test structure battery, against the same experiments' frozen searches run unchanged on fresh scrambled copies, with masked plants through two of the climbs

**Family:** 1-keyed-periodic  
**Parent:** 0140-k4-against-its-own-copies-with-the-tempering-climb  
**Decision:** error  
**Run:** 2026-10-24T16:47:19+00:00, 1.0 s, status error  
**Time by phase:** design 375 s, test 275569 s, implement 116 s, run 1 s, record 0 s

## In plain words

Some earlier searches produced readings with all 24 known letters right but the rest gibberish, and threw them away because they did not look like English. If Sanborn disguised the English before enciphering it (writing it backwards, or with X between words), the right reading would look like gibberish too. Here we test those saved readings for 14 kinds of hidden pattern, and run the very same searches on scrambled copies of the carving to see how much pattern luck alone produces. We also hide a few disguised messages of our own, run the same searches on them, and check whether the pattern tests would have noticed.

## Walkthrough, by hand

1. Take one saved reading, say 0142's, with all 24 known letters in place.
2. Score it on each of 14 pattern tests: read backwards, every nth letter, X as a word space, letter counts in any order, and so on.
3. Scramble the carved letters twelve times, keeping only scrambles the same search can fit, and run the same search on each.
4. Score each scramble's reading on the same 14 tests.
5. On each test, see whether the carving's reading beats all twelve scrambles; with 112 such comparisons about nine will by luck, so each one that does is rerun against fresh scrambles until one catches up.

## Worked example (generated)

```

```

## Lineage

Inherits from 0140-k4-against-its-own-copies-with-the-tempering-climb. What changed: A13.3 (Stage 2, step 3, issue #75). The 31 readings that put all 24 known letters in place and were saved in raw.json (0034: 18, 0035: 3, 0048: 3, 0120: 2, 0137: 2, 0140, 0142, 0148: 1 each) were thrown away on their quadgram score. Here they go through tools/a13_structure.py's 14 tests, each against the same experiment's frozen attack.py run unchanged on fresh copies built as that experiment built them (tools/a13_check.py pass1-regen, seed 1300, begun 2026-10-21 and finished 2026-10-24 before this run). Pre-registered 2026-10-21 in reports/a13-structure-check.md: 112 cells, flag at p < 0.05/112, candidates replicated sequentially on fresh copies (seed 3113). New in this run: masked planted messages through 0140's and 0142's climbs, to say what a 'nothing found' means for climbed readings.

## Hypothesis (domain expert)

A13 (knowledge/12-assumptions.md): if the English was masked before the keyed stage (C4(a), Scheidt 2005 and 2015: 'I masked the English language', 'more than one stage'; C19, X and Q as stops), the right decryption is masked English and its quadgram score sits with the copies'. The readings tested are the climbed completions of F1's sampled cells: 0034 (periodic key 27-29 and 53-95 on standard/KRYPTOS tables, 24 conventions), 0035 and 0048 (27-29, keyword-mixed tables), 0120, 0137, 0140, 0142 (one free alphabet, Beaufort form, 23 and 26) and 0148 (K1/K2's added form, length 19, slip at 33). Statistic: for each experiment and test, the best value over a text's readings; K4's rank among the copies' (ties against K4). Copies: plain shuffles (0034, 0035, 0048; 10 each), shuffles passing 0119's exact decider at the length (0120, 0137, 0140, 0142; 12 each), shuffles of the 73 unknown places (0148; 12). A cell is a candidate when K4 is strictly above every copy (chance about 112/12 = 9); a flag needs p < 0.00045, all of 2,242 copies below K4. Power: A13.1 (power.json) against flat noise; against climbed copies it is unmeasured, so masked plants (reversal, X between words, X every kth letter, and unmasked) are enciphered under 0140's and 0142's own method and climbed by their frozen search.

## Prediction

K4 is strictly above every copy in about 9 of 112 cells (chance), and none of those replicates: every candidate meets a fresh copy at or above K4 within a few dozen copies. No flag. The masked plants through the climbs are found less often than A13.1's flat-noise rate: the climb pulls a reversed or X-spaced message toward forward English junk, so most masked plants are not found by their own test. Zero candidates pass gate 4.

## Method

1. K4: every saved reading with 24 of 24 known letters in the eight experiments' raw.json, through the battery; per experiment and test, the best value.
2. Copies: the readings in reports/a13-structure-data/pass1_copies.json (any job still missing is run here, same seeds), through the battery the same way.
3. Rank K4 per cell; a cell where K4 is strictly above every copy is a candidate.
4. Replication, per experiment with candidates: fresh copies built the experiment's way (seed '3113'), its frozen search, eight at a time, until every candidate test has met a copy at or above K4 (not a flag), or 2,242 copies all below (a flag), or the clock (unresolved, reported with its p).
5. Plants: three per mask (none, reversal, X between words, X every kth letter), Carter 1923 with the 24 known letters set after masking, enciphered with a random alphabet and key under 0142's (length 26) and 0140's (length 23) Beaufort form, climbed by their frozen search; found when the mask's own test is above every one of that experiment's 12 copies.

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
  File "/Users/alexisrondeau/Workshop/cryptos/attack.py", line 232, in run
    cells[f"{e}/{t}"] = {"k4": kv, "copies_min": min(vals), "copies_max": max(vals), "n": len(vals),
                                                 ~~~^^^^^^
ValueError: min() iterable argument is empty

```

