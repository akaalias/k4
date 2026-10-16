# 0121-two-free-alphabets-exact-at-every-key-length: Two alphabets in unknown orders, one for the message and one for the carved letters (Quagmire IV), no move: which key lengths 1-26 can any pair fit, and is that unusual against scrambled coppers?

**Family:** 1-keyed-periodic  
**Parent:** 0119-one-free-alphabet-exact-at-every-key-length  
**Decision:** error  
**Run:** 2026-10-16T08:28:56+00:00, 0.9 s, status error  
**Time by phase:** design 7 s, test 1 s, run 1 s, record 0 s

## In plain words

K1 and K2 used one scrambled alphabet for the whole table. A variant uses two: one scrambled order to look up the message letter and another to write the carved letter. With both orders unknown there are vastly more tables. For each key length 1 to 26 we ask, by exact arithmetic on the 24 known letters, whether any pair of orders and any key could produce them, and how often the same is true of scrambled copies of the carved text.

## Walkthrough, by hand

1. Choose a key length, say 8, and group the known places by slot (place mod 8).
2. For each known place write: place of the carved letter in the cipher alphabet = place of the known letter in the plain alphabet + key value of the slot.
3. Two known places in one slot give one check with the key removed: C(c1) - P(p1) = C(c2) - P(p2).
4. If one slot holds the same known letter over two different carved letters, those carved letters would share a place: dead.
5. Otherwise solve the checks modulo 13 and modulo 2 and search the solutions for one where each alphabet keeps its letters apart.
6. Repeat for every length 1-26 and for 100 scrambled copies of the carved text.

## Worked example (generated)

```

```

## Lineage

Inherits from 0119-one-free-alphabet-exact-at-every-key-length. What changed: F1.2. 0097 tested two unknown alphabets only at key lengths 3, 7 and 21, by a relaxation. Here every length 1-26 is decided exactly with 0119's method generalised to two independent alphabets (each one-to-one), on K4 and 100 scrambled coppers. Power is stated before running: at each length, the share of coppers on which the exact test fails is the test's power to reject a random text there; lengths where K4 fits are then compared with that rate.

## Hypothesis (domain expert)

C27(c) (Sanborn's 'slightly different' tableau), C1(b). Model: plain alphabet P and cipher alphabet C, unknown bijections letters -> Z26, key k of length L: C(c_i) = P(p_i) + k[i mod L] (Quagmire IV; the Beaufort form C(c) = k - P(p) is the same family with P reflected, so one form covers both; a key alphabet drops out). 24 linear equations over Z26; exact decision by CRT: solve mod 13 and mod 2, each alphabet's letters at most two per residue class mod 13 with each pair differing mod 2; refute at once on forced coincidences; otherwise enumerate the mod-13 letter space up to the two translations and scaling (rank <= 5) or search it depth first with pruning, a node limit reporting 'undecided'. The generalised decider agreed with 0119's on 780 one-alphabet cases and recovered planted Quagmire IV texts at lengths 3-26 in a dry run, which also showed K4 fitting at lengths 8, 13, 16, 19, 20, 23, 24 and 26. Power and copper comparison are what this run adds. Two alphabets have more freedom than one, so where both K4 and most coppers fit, 0120's finding (a climb on one alphabet already has weak power at 23 and none at 26) means an English climb here could not decide; such lengths are recorded blocked, not run weakly.

## Prediction

Power: the exact test rejects nearly all coppers (at least 90%) at lengths 1-7 and fewer than half at lengths with 7 or fewer checks (17, 18, 23-26). K4's 8 fitting lengths lie inside the middle 90% of the coppers' counts, and at every length where K4 fits at least 5% of coppers fit too; if K4 fits at a length where fewer than 5% of coppers do (length 8, 16 checks, is the candidate), that is outside the range and stops the queue for a replication. Zero candidates.

## Method

1. For each key length 1-26 write the 24 equations.
2. Decide exactly whether a pair of one-to-one alphabets and a key satisfy them; re-check every witness.
3. Do the same on 100 scrambled coppers (seed 121).
4. Report per length the checks, K4's verdict, the share of coppers that fit (the power is one minus that share), and K4's count of fitting lengths against the coppers'.

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
  File "/Users/alexisrondeau/Workshop/cryptos/_runner.py", line 34, in main
    res = attack.run(ctx) or {}
          ~~~~~~~~~~^^^^^
  File "/Users/alexisrondeau/Workshop/cryptos/attack.py", line 379, in run
    pl = {f: "".join(a[1] for a, v in sorted(w[0].items(), key=lambda kv: kv[1]) if a[0] == f) for f in ("P", "C")}
             ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: sequence item 0: expected str instance, int found

```

