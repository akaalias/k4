# 0278-f16.1e-running-keys-on-the-20-official-letters: F16.1e: the named running keys (0210: K1-K3 plain and cipher, Carter, the tableau and the other named texts, every offset, both directions, on the standard, KRYPTOS and keyword tables) on the 20 official known letters (EAST set aside), with up to five slips; K4 against 0210's 20 copies, its plants and the judge

**Family:** 16-simple-hand-methods  
**Parent:** 0210-running-keys-with-slips-at-known-places  
**Decision:** error  
**Run:** 2026-11-17T16:25:15+00:00, 98.1 s, status error  
**Time by phase:** test 18 s, run 98 s, record 0 s

## In plain words

A running key takes its key letters from a book or an earlier passage, starting at some page and line. Experiment 210 tried every starting place in every text we named, allowing up to seven slips, and found nothing, but it counted EAST. Here we try again with the 20 letters Sanborn published himself, allowing up to five slips.

## Walkthrough, by hand

1. Take a text, say K3's plaintext, and a starting letter in it.
2. Write the text from there under K4, one letter per place.
3. At each of the 20 official known places, look up on the table what the known letter and the text letter give.
4. Count the places where that is not the carved letter; five or fewer may be slips.
5. Try every starting letter, both directions, every table; read the message wherever a start passes.

## Worked example (generated)

```

```

## Lineage

Inherits from 0210-running-keys-with-slips-at-known-places. What changed: F16.1 (issue #123), fifth part. 0210's attack.py loaded from its record and run with only the 20 official known places (26-34, 64-74). Its pigeonhole index used 8 blocks of 3 known places to be exact for up to 7 slips; 20 places give 6 whole blocks, so the blocks are taken over the first 18 places and the slip limit is 5 (exact for 5 or fewer), each replacement asserted; the bit counts use 20 places. Everything else as recorded: sources, tables, offsets, copies, plants, judge.

## Hypothesis (domain expert)

F1's running-key arm (C7, C9: the earlier texts as instructions or key; Gillogly 1999 and Schridde 2017 found the K1-K3 running keys give nonsense, 05-attacks.md). Model as 0210: c = table(p, key letter from a named text at offset o + i), forward or backward, Vigenere, Beaufort or variant, on the standard, KRYPTOS or keyword tables, 1.36 x 10^9 trials. Criteria revised 2026-11-17 (#124): EAST is second-hand. With 20 checks and up to 5 slips, chance settings stay near 10^-6 per run: any K4 setting would be a lead; the judge reads every setting found.

## Prediction

No setting on K4 or any copy at up to 5 slips; plants found 3 of 3 (their planted offset, no setting on their own copies). Zero candidates.

## Method

1. Load 0210 from its record; give it the 20 official known letters; blocks of 3 over the first 18 places, slip limit 5.
2. Run it as recorded: every source, offset, direction, table and form, through the block index, each hit checked on all 20 places.
3. Readings of every setting found go to quadgrams and the judge, K4's and the copies' together.

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
  File "/opt/repo/_runner.py", line 85, in main
    res = attack.run(ctx) or {}
          ~~~~~~~~~~^^^^^
  File "/opt/repo/attack.py", line 95, in run
    r = m.run(Ctx20(ctx, "0210"))
  File "/opt/repo/experiments/0210-running-keys-with-slips-at-known-places/attack.py", line 260, in run
    srcs = sources()
  File "/opt/repo/experiments/0210-running-keys-with-slips-at-known-places/attack.py", line 110, in sources
    site = json.loads((ROOT / "data" / "site_texts.json").read_text())
                      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/opt/python/cpython-3.14.10-linux-aarch64-gnu/lib/python3.14/pathlib/__init__.py", line 787, in read_text
    with self.open(mode='r', encoding=encoding, errors=errors, newline=newline) as f:
         ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/python/cpython-3.14.10-linux-aarch64-gnu/lib/python3.14/pathlib/__init__.py", line 771, in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/opt/repo/experiments/0210-running-keys-with-slips-at-known-places/data/site_texts.json'

```

