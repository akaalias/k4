# 0193-hill-2x2-unknown-numbering: F8.1: Hill 2x2 with an unknown one-to-one letter numbering (any of 26!), every invertible matrix, both alignments: exact; 3x3 counted and blocked

**Family:** 8-hill  
**Parent:** 0116-hill-plus-periodic-key  
**Decision:** error  
**Run:** 2026-10-17T01:25:04+00:00, 0.2 s, status error  
**Time by phase:** implement 0 s, test 0 s, run 0 s, record 0 s

## In plain words

The tableau's last column spells HILL, the name of a cipher that mixes letters in pairs with a little matrix of numbers. It was tried with the usual ways of numbering the letters. Here the numbering itself is a secret: any order of the alphabet. The known words still give enough pairs to decide it exactly, for every possible matrix.

## Walkthrough, by hand

1. Pair the message from place 1: places 21-22 are not both known, 23-24 (A S) are, over the carved L R.
2. With matrix (a b; c d): a*n(A) + b*n(S) = n(L) and c*n(A) + d*n(S) = n(R), where n is the secret numbering.
3. Eleven such pairs give 22 equations; choosing numbers for two or three letters forces the rest.
4. If no one-to-one numbering survives, that matrix is out.
5. All 157,248 invertible matrices, both pairings, K4 and scrambled copies.

## Worked example (generated)

```

```

## Lineage

Inherits from 0116-hill-plus-periodic-key. What changed: F8.1. Earlier Hill tests fixed the numbering (4 standard, 126 vocabulary, 200 K1-K3 words; 0015, 0044, 0055). Here the numbering is free. Counting first: at either alignment 11 digraphs of K4 lie wholly inside the known runs, 22 linear equations mod 26 (about 103 bits) in the numbers of 20-21 letters (79-81 bits) and the 4 matrix entries (17 bits): a surplus of 5-7 bits, so an exact test has power. For 3x3, 6-7 trigraphs give 18-21 equations against 76-81 + 41 bits: 21-32 bits short, no checks, blocked. For each of the 157,248 invertible 2x2 matrices and each alignment, a depth-first search with propagation looks for a one-to-one numbering satisfying all 22 equations (compiled). K4 against 5 shuffled copies (each takes minutes); plants with random numberings.

## Hypothesis (domain expert)

C21(a) (the HILL column of the tableau), F8. Model: x a one-to-one map letters -> Z26; for each aligned block, (x[c1], x[c2]) = M (x[p1], x[p2]) mod 26 with M invertible. Encryption and decryption matrices, row and column conventions are all covered by enumerating every invertible M. Statistic: matrices admitting a numbering, K4 against 5 copies; expected on a random text about 2^-5 to 2^-7 per alignment in total.

## Prediction

No matrix admits a numbering on K4 at either alignment; copies mostly none; plants found. Zero candidates.

## Method

1. For each alignment: the digraphs wholly inside the known runs (11 each).
2. For each invertible 2x2 matrix: two equations per digraph; search for a one-to-one numbering with propagation (node limit 200,000, undecided counted).
3. K4, 5 shuffled copies, 3 planted Hill texts with random numberings and matrices.

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
  File "/Users/alexisrondeau/Workshop/cryptos/attack.py", line 227, in run
    out = pool.map(job, [(so, ti, t, a) for ti, t in enumerate(texts) for a in (0, 1)], chunksize=1)
  File "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/multiprocessing/pool.py", line 367, in map
    return self._map_async(func, iterable, mapstar, chunksize).get()
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/multiprocessing/pool.py", line 774, in get
    raise self._value
  File "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/multiprocessing/pool.py", line 540, in _handle_tasks
    put(task)
    ~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/multiprocessing/connection.py", line 216, in send
    self._send_bytes(_ForkingPickler.dumps(obj))
                     ~~~~~~~~~~~~~~~~~~~~~^^^^^
  File "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/multiprocessing/reduction.py", line 51, in dumps
    cls(buf, protocol).dump(obj)
    ~~~~~~~~~~~~~~~~~~~~~~~^^^^^
_pickle.PicklingError: Can't pickle <function job at 0x1058b7690>: it's not the same object as attack.job
when serializing tuple item 0
when serializing tuple item 0
when serializing tuple item 3

```

