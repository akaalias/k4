# Priorities

After 118 experiments none has beaten the scrambled coppers. Following up on a result needs a
result that beats chance, and there has been none, so the work is a sweep. From here on the
sweep follows a fixed order, set before any further run:

1. Families are worked in the rank order below. Within a family, open items are taken from the top.
2. A family is left only when every item in its table is `closed` or `blocked`:
    - `closed` means an exact test, or a sampled test with scrambled-copper controls at stated
      power, rules the item out.
    - `blocked` means it cannot be tested with the 24 known letters alone, for example because
      it needs a source text we lack or it leaves no checks. The reason is written down.
3. Reverts no longer force a pivot. A revert that closes an item is progress.
4. Every experiment names the item it works on (for example "F1.2") and the strength it
   reached: exact, sampled or weak. A weak test leaves the item open.
5. A result outside the scrambled-copper range stops the queue. It is replicated against
   fresh controls before anything else, as 0100 was by 0102.
6. The ranking changes only at a family boundary, with the reason in the pivot log.

Per-experiment grades (outcome, strength, whether the known letters were fitted by
construction) are in `grades.tsv`.

## Ranking

| Rank | Family | Clue support | What is left | Cost of what is left | Status |
|---|---|---|---|---|---|
| 1st | F1 one keyed stage, no move | strong: K1 and K2 are Quagmire III on KRYPTOS; Sanborn's "slightly different" tableau (C27c) | unknown (free) alphabets; forced key read as running English on any dictionary alphabet | low to medium | **next** |
| 2nd | F6 a move, then the table | strong: Sanborn's "matrix codes... then went back to this table" (C1) | the same free-alphabet items after each move in the type-1 library; mixed triple turns | medium to high | queued |
| 3rd | F3 two-part key with a combiner | medium: Scheidt's "key word/s" (C5), his CKM habit | combiners other than addition; numeric second parts not yet tried | low | queued |
| 4th | F2 masked plaintext | medium: Scheidt "masked the English language" | loose ends from 0057; nulls placed by a rule | low | queued; mostly blocked |
| 5th | F4 Sanborn's visual systems | medium, vague | routes through the plates as a path, not as a key | medium | queued |
| 6th | F8 Hill | weak: the HILL column only (C21) | 5x5 affine has no checks | none testable | blocked |
| 7th | F5 Gromark | weak: no creator remark | multiplicative feedback, the raised YAR as primer | low | nearly closed |
| 8th | F9 substitution, then a move | against it: Sanborn's NYPVTT to BERLIN mapping | routes outside the 1.86M built; more than 26 symbols | high, unbounded | blocked beyond the route sets |
| - | F7 construction simulation | a tool, not a cipher | run before each family's first open item: does its construction make both fingerprints? | low | standing step |

Why this order: F1 and F6 rest on the two most direct creator statements. Both were tested
almost entirely on the standard, KRYPTOS and puzzle-word alphabets. An unknown alphabet is the
largest axis not yet covered, and it costs less with no move (F1) than after one (F6). F3 and
F2 come next because their remaining items are cheap. The rest are closed or blocked except
for low-value residues.

## F1. One keyed stage, no move

| Item | Status | Strength | Experiments | Next test or reason |
|---|---|---|---|---|
| Periodic key, standard or KRYPTOS alphabets, periods 1-26 and 30-52 | closed | exact | 0005, crib sweep | - |
| Periods 27-29 and 53+ on any alphabet pair the puzzle's words build | closed | exact consistency; the key completion is noise against coppers | 0034, 0035, 0048, 0053 | - |
| Periodic key on alphabets from any dictionary word | closed | exact | 0109 | - |
| Progressive key | closed | exact | 0011, 0042 | - |
| Ciphertext autokey, any lag, any alphabet tried | closed | exact | 0002, 0025, 0064, 0118 | - |
| Plaintext autokey, lags 1-52 | closed | exact | 0003, 0012 | - |
| Plaintext autokey, lags 53-96 | blocked | - | 0012 | too few checks: the known letters force too little |
| Running key from K1-K3, the sculpture's texts, Carter, Sanborn's letters | closed | exact | 0004, 0017, 0021, 0045, 0047, 0078, 0098, 0117 | - |
| Running key from an unknown English text, standard, KRYPTOS or puzzle-word alphabets | closed as far as testable | sampled; best forced stretch equals the coppers | 0009, 0010 | - |
| **F1.1** Free alphabet, the same on both sides (Quagmire III with unknown order), periods 3-26 | **open** (one cell) | exact for the added form at 1-26 and the Beaufort form at 1-22, 24, 25 (0119); Beaufort 23 sampled at low power (plants above every copper 3 of 6, none recovered; K4 inside the coppers, below 10 of 12, 0120); Beaufort 26 blocked (one check; plants 1 of 6) | 0097, 0100, 0102, 0119, 0120 | Beaufort 23 needs a climber that recovers planted text; none at this size does. Left open, not chased further in this pass |
| **F1.2** Two free alphabets (Quagmire IV), periods 3-26 | **open** | weak | 0097 | the same; fewer checks, so state the power before running |
| **F1.3** Forced key stretches read as running English on the 208,062 dictionary alphabets | **open** | not run | 0010 did the puzzle words only | score both stretches under every alphabet and class; compare the best with coppers |
| **F1.4** Hand key schedules other than the Berlin clock and Carter dates | **open** | - | 0079, 0038 | write the list of schedules first (C20(c)-(e)); test each exactly |

## F6. A move, then the table

| Item | Status | Strength | Experiments | Next test or reason |
|---|---|---|---|---|
| Columnar (plain, keyed, double), K3's rule, quarter turns, grid paths, rail fence, AMSCO, Myszkowski, then a periodic key on standard, KRYPTOS or word alphabets | closed | exact | 0006-0008, 0026, 0058, 0080-0086, 0099, 0110-0114 | - |
| The same moves with autokey, running key or clock schedules | closed | exact | 0063, 0081, 0090, 0091 | - |
| Three stages | partly closed | exact for clockwise triples (0083); sampled for mixed stages (0037) | 0037, 0083 | **F6.3** mixed-direction triples, exhaustive at small widths |
| One carved letter wrong, missing or extra, through the move library | closed | exact | 0093, 0094 | - |
| AMSCO at period 23 after the move: 15 distinct check sets against 1-9 on the coppers | noted, not chased | exact | 0114 | within the 4.7 of 52 cells expected outside the range by chance; replicate only if F6 reaches AMSCO again |
| **F6.1** Free alphabet (Quagmire III) after or before each move, periods 3-26 | **open** | weak | 0097 | F1.1's method on each move; begins only after F1.1 |
| **F6.2** Two free alphabets after or before each move | **open** | weak | 0097 | after F1.2 |
| **F6.4** Padding applied separately at each grid stage; nulls dropped between griddings | **open** | partly (0082) | 0082 | list the hand padding rules, test each with a periodic key |

## F3. Two-part key with a combiner

| Item | Status | Strength | Experiments | Next test or reason |
|---|---|---|---|---|
| Two words added, both from the puzzle, or one from the dictionary | closed | exact | 0014, 0043, 0059, 0115 | - |
| A word plus digits from the story (coordinates, dates, counts) | closed | exact | 0024, 0038 | - |
| A word plus the misspelt or raised letters | closed | exact | 0061 | - |
| Column word plus row key | closed | exact | 0087, 0088 | - |
| **F3.1** Combiners other than addition (subtraction both ways is done; table lookup through a second alphabet, multiplication mod 26) | **open** | - | - | exact, cheap |
| **F3.2** Numeric second parts from the Morse (E counts) and the plate layout (line lengths) | **open** | - | 0038 did 17 readings | list the readings, test each exactly |

## F2. Masked plaintext

| Item | Status | Strength | Experiments | Next test or reason |
|---|---|---|---|---|
| Reversal, regular nulls, prefix nulls, affine masks, doublets as nulls, nulls by letter | closed | exact | 0023, 0057, 0074, 0075 | - |
| Message written along grid paths | closed | exact | 0092 | - |
| **F2.1** Forced fragments at periods 24-25 after letter strike-outs not matched against words | **open** | gap in 0057 | 0057 | match them against the dictionary; cheap |
| **F2.2** Nulls placed by a rule (after every X, after each crib word) | **open** | - | - | exact, cheap |
| A code layer, phonetic spelling, another language | blocked | - | - | changes the letters at the known places or needs a codebook we lack |

## F4. Sanborn's visual systems

| Item | Status | Strength | Experiments | Next test or reason |
|---|---|---|---|---|
| Trifid, any cube | closed | exact | 0040 | - |
| The plates as a key by position, straight or folded | closed | exact | 0089 | - |
| Read from behind the screen | closed | exact | 0108 | - |
| **F4.1** A route that follows the plates' physical layout (the S-curve, the 31-letter lines as a grid with K3's last line) | **open** | - | - | build the route set from the Blender model, then test as F6 |

## F8 Hill, F5 Gromark, F9 substitution then a move

| Item | Status | Strength | Experiments | Reason |
|---|---|---|---|---|
| Hill 2-5, plain and affine, any numbering, chained, with a periodic key | closed, except what had too few equations: 5x5 affine (14 of 20 settings undecided, 0105) and 400 of 936 Hill-plus-key settings, mostly 4x4 with long keys (0116) | exact where decided | 0015, 0036, 0044, 0055, 0105, 0116 | the undecided settings are blocked: no checks |
| Gromark, two- and three-term rules, any alphabet, bases 2-26 | closed | exact | 0013, 0028, 0046, 0054, 0069, 0076, 0107 | - |
| **F5.1** Multiplicative feedback; the raised YAR as primer | open, low value | - | - | no creator remark points here |
| One-to-one substitution, then any route in the built sets (1.86M) | closed | exact | 0019, 0106 | - |
| Routes outside every built set | blocked | - | - | unbounded without a hand-method list |
