# 0153-carter-running-key-on-an-unknown-alphabet: F1.8: Carter's book as a running key on one unknown alphabet (both directions, every offset, three forms), solved exactly; and how many checks two unknown alphabets would leave for each running-key source

**Family:** 1-keyed-periodic  
**Parent:** 0098-sculpture-running-keys-on-an-unknown-alphabet  
**Decision:** error  
**Run:** 2026-10-16T21:21:20+00:00, 1860.1 s, status error  
**Time by phase:** unattributed 11 s, run 1860 s, record 0 s

## In plain words

A running key takes a long text, here Carter's book about opening Tutankhamun's tomb, which K3 quotes, and uses its letters one after another as the key. With an alphabet in an unknown order, each known letter gives an equation about the alphabet alone. For every starting point in the book, forwards and backwards, a search decides whether any alphabet satisfies all 24, on the carved text and on scrambled copies. We also count whether, with two unknown alphabets, the known letters could ever rule anything out.

## Walkthrough, by hand

1. Write Carter's book as one long string of letters and lay it under K4 from some letter onwards.
2. At known place 22 (E under F) the book's letter there, say T, gives: place(F) = place(E) + place(T) in the unknown alphabet.
3. The 24 known places give 24 such equations in the 26 unknown places.
4. Search for one alphabet order that satisfies them all; none means this starting point is dead.
5. Repeat from every letter of the book, with the book reversed, for the three ways of using the table, and on scrambled copies.

## Worked example (generated)

```

```

## Lineage

Inherits from 0098-sculpture-running-keys-on-an-unknown-alphabet. What changed: F1.8. 0098 solved the sculpture's running keys on an unknown alphabet exactly but left Carter's book out; 0021 and 0047 ran Carter only on fixed and keyword tables. Here every offset of Carter's Tomb of Tut-ankh-Amen vol. 1 (284,914 letters as scanned), forwards and backwards, under one unknown alphabet on both sides, three forms: each known letter gives an equation in alphabet places only, decided by a compiled propagation search (checked against a Python solver on 300 random offsets and on a planted text), node limit 20,000, then 400,000 for the undecided. Ten scrambled coppers. Second part, counted not searched: for two unknown alphabets, the checks the 24 equations leave (24 minus their rank mod 13) at sampled offsets of each running-key source.

## Hypothesis (domain expert)

C7(d) (K3 is Carter's text; 'instructions in the earlier text that refer to later text', knowledge/02-sanborn-said.md), C13, C27(c), C5 ('a named text and a place in it' is a short key description). Model: x a bijection letters -> Z26 on both sides; key letter k_i = Carter[o + i] (forward) or the reversed book; forms V x(c) = x(p) + x(k), B x(c) = x(k) - x(p), R x(c) = x(p) - x(k). Source: knowledge/sources/carter-1923-tomb-of-tutankhamen-vol1.txt, letters only. Exact per offset (undecided counted). Statistic fixed before the run: fitting offsets per (direction, form) on K4 against the ten coppers' range. Two-alphabet count: C(c) = P(p) + N(k) with the key numbered on P or on C; rank of the 24 equations mod 13 over the place variables, checks = 24 - rank, at 2,000 offsets per source (Carter, K1-K3 plaintexts, the sculpture's ciphertext panel).

## Prediction

No offset fits K4 in any form or direction; the coppers give 0 or a handful; undecided offsets resolve to dead at the higher limit. Two unknown alphabets leave no checks at any offset of any source (the equations' unknowns outnumber them), so that cell is blocked by structure. Zero candidates.

## Method

1. Compile the solver; check it against Python on 300 random Carter offsets on K4 and on a planted text.
2. For K4 and 10 coppers, both directions: every offset, three forms, limit 20,000; re-decide the undecided at 400,000.
3. Count fits per (direction, form); decrypt K4's fits.
4. Two alphabets: rank mod 13 at 2,000 offsets of each source.

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
no output
```

