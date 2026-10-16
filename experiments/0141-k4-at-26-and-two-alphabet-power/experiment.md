# 0141-k4-at-26-and-two-alphabet-power: F1.1 at key length 26 decided with design 2 (K4 against its own copies); design 2 carried to two free alphabets (Quagmire IV) and its power measured at F1.2's lengths 8, 13 and 16

**Family:** 1-keyed-periodic  
**Parent:** 0140-k4-against-its-own-copies-with-the-tempering-climb  
**Decision:** error  
**Run:** 2026-10-16T18:40:34+00:00, 1703.2 s, status error  
**Time by phase:** unattributed 79 s, run 1703 s, record 0 s

## In plain words

Two pieces. First, the carved text is run through the new search for a scrambled alphabet with a 26-letter key, against scrambled copies of itself. Second, the search is extended to two scrambled alphabets, one for the message and one for the carved letters, and tested on planted English at the three key lengths where English could in principle decide, before it is allowed to judge the carved text.

## Walkthrough, by hand

1. Two alphabets: number the message letters by one scrambled order and the carved letters by another; carved place = message place + key value.
2. Two known letters under one key letter must give the same difference, carved place minus message place: at length 8 sixteen such checks.
3. Find one pair of orders that satisfies every check exactly, then shuffle it by swaps that keep the checks.
4. Run sixteen searches side by side over pairs of orders that keep the checks, scoring the whole text as English.
5. Do the same on planted English and on shuffles of it; count how often the planted text wins.

## Worked example (generated)

```

```

## Lineage

Inherits from 0140-k4-against-its-own-copies-with-the-tempering-climb. What changed: F1.1 Beaufort 26 and F1.2. 0140 found design 2 has power at length 26 too (5 of 6 planted texts beat all their own copies), so K4 at 26 now runs against 12 fitting shuffles of itself. In the same run design 2 is carried to two independent alphabets (Quagmire IV: C(c) = P(p) + k), the case F1.2 leaves at lengths 8, 13 and 16 under 0136's bound: compiled tempering over both alphabets, every move keeping the known-letter checks, each run started from an exact witness (0123's decider) randomised by 400 check-keeping swaps; power measured on planted texts against their own fitting shuffles.

## Hypothesis (domain expert)

C27(c), C1(b). L26 one alphabet, Beaufort form (1 check), as 0140 (seed 141): K4 vs 12 shuffles of K4 fitting at 26; measured power 5 of 6 at 6 copies (0140); rule fixed before the run: K4 above all 12 stops the queue for replication, otherwise the cell closes sampled at that power. Quagmire IV (0123's model, two unknown bijections P and C, key length L): 0136 bounds the open bits at 89, 112 and 126 for L 8, 13, 16 against 130 of quadgram evidence; checks 16, 11, 8. Search: replica exchange, 16 replicas, T 0.1 -> 0.002, 10 runs x 625 rounds x 1,000 moves per text (0139's effort); moves swap two places in one alphabet, repaired by a second swap when a check breaks. Power: 4 planted texts per length (Carter windows, seed 1411), each against 5 shuffles of itself fitting that length (0123's decider); null 1/6 per plant; bar fixed before the run: at least 3 of 4 beat all their own copies. A length that passes gets K4 against its own copies in the next run; one that fails stays blocked.

## Prediction

K4 inside its copies at 26 (cell closes at power about 0.8). Two alphabets: power falls with the number of checks and the doubled alphabet freedom: at least 3 of 4 at length 8 (16 checks), fewer than 3 at 13 and 16. No reading.

## Method

1. Draw 12 shuffles of K4 fitting at 26 (one alphabet, Beaufort form); 4 planted Quagmire IV texts at each of 8, 13, 16 and 5 fitting shuffles of each.
2. One-alphabet texts: 0139's search. Two-alphabet texts: the same search over both alphabets from a witness start; the compiled decryption checked against Python on every text.
3. L26: K4's rank. Two alphabets: plants beating all their own copies per length.

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
multiprocessing.pool.RemoteTraceback: 
"""
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/multiprocessing/pool.py", line 125, in worker
    result = (True, func(*args, **kwds))
                    ~~~~^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/multiprocessing/pool.py", line 48, in mapstar
    return list(map(*args))
  File "/Users/alexisrondeau/Workshop/cryptos/attack.py", line 673, in _any
    return _job4(args) if len(args) == 8 else _job(args)
           ~~~~~^^^^^^
  File "/Users/alexisrondeau/Workshop/cryptos/attack.py", line 667, in _job4
    sc, pt, done, ok = climb4(text, KNOWN, L, seed, y0, deadline)
                       ~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/alexisrondeau/Workshop/cryptos/attack.py", line 658, in climb4
    sc, pt, (y, k) = best
            ^^^^^^
TypeError: cannot unpack non-iterable NoneType object
"""

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/Users/alexisrondeau/Workshop/cryptos/_runner.py", line 34, in main
    res = attack.run(ctx) or {}
          ~~~~~~~~~~^^^^^
  File "/Users/alexisrondeau/Workshop/cryptos/attack.py", line 730, in run
    res = pool.map(_any, jobs, chunksize=1)
  File "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/multiprocessing/pool.py", line 367, in map
    return self._map_async(func, iterable, mapstar, chunksize).get()
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/multiprocessing/pool.py", line 774, in get
    raise self._value
TypeError: cannot unpack non-iterable NoneType object

```

