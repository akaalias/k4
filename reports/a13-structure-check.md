# A13: structure other than English in the 24-of-24 readings

Stage 2, step 3 (issue #75). Assumption A13 (`knowledge/12-assumptions.md`): if the message was masked before it
was enciphered, the right decryption is masked English, its English score sits with the noise, and the reading was
thrown away. This report runs a battery of 14 structure tests (`tools/a13_structure.py`) over readings that put all
24 known letters in place, K4's against the same method's readings of scrambled copies (`tools/a13_check.py`). Data
in `reports/a13-structure-data/`. Rules: `program.md`, "Masked English (A13) and the English score (A6)".

Started 2026-10-18 (power and pass 2 written, then stopped); resumed 2026-10-21.

## A13.1 The battery's power

`power.json` (2026-10-18, complete: 12 masks x 14 tests). Each mask was applied to 20 planted 97-letter passages
of Carter 1923 with the 24 known letters set in place; a plant counts as found by a test when its value is above all
of 200 random texts drawn from K4's letter counts with the known letters set (a per-test level of 1 in 201). Bold:
found in 15 or more of 20.

| mask | base | freq | ioc | sepW | sepR | rev | keep | drop | step | affS | affK | cols | rep | pairs | best |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| none | **20** | **20** | **20** | 0 | 0 | **20** | 14 | **20** | **20** | **20** | **20** | **20** | **17** | **16** | 20 |
| X spaces | **20** | **20** | **20** | **20** | 0 | 6 | 0 | **20** | 0 | **20** | **20** | 6 | **18** | **15** | 20 |
| X every kth | **17** | **20** | **19** | 14 | 10 | 14 | 8 | **20** | **15** | **17** | **17** | **17** | 6 | 14 | 20 |
| message in every nth | 1 | 1 | 1 | 1 | 0 | 3 | **20** | 5 | 6 | 1 | 1 | 8 | 0 | 0 | 20 |
| affine std | 0 | 6 | 4 | 3 | 1 | 1 | 0 | 1 | 1 | **20** | 0 | 1 | 7 | 5 | 20 |
| affine KRYPTOS | 0 | 10 | 12 | 1 | 2 | 1 | 0 | 0 | 0 | 0 | **20** | 0 | 9 | 7 | 20 |
| letter swap | 0 | 9 | 10 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 7 | 4 | 10 |
| columns | **20** | **20** | **20** | 0 | 0 | **20** | **18** | **20** | **20** | **20** | **20** | **20** | 2 | 4 | 20 |
| nulls every nth | **20** | **18** | **15** | 0 | 0 | **20** | 10 | **20** | **20** | **20** | **20** | **20** | 3 | 6 | 20 |
| ring step | **20** | **20** | **20** | 0 | 0 | **20** | **16** | **20** | **20** | **20** | **20** | **20** | 0 | 5 | 20 |
| reversal | **20** | **20** | **20** | 0 | 0 | **20** | **17** | **20** | **20** | **20** | **20** | **20** | 8 | 10 | 20 |
| pair code | 1 | **20** | **20** | 0 | 0 | 1 | 1 | 1 | 2 | 4 | 6 | 3 | **20** | **20** | 20 |

Columns: base = eng_base, freq = freq_sorted, ioc, sepW = sep_words, sepR = sep_regular, rev = eng_reverse,
keep = eng_keep_nth, drop = eng_drop_nth, step = eng_step, affS / affK = eng_affine_std / _kry, cols = eng_columns,
rep = repeats, pairs = base_pairs.

What it says:

- **The one mask this step cannot see is a letter swap** (a one-for-one substitution of the message before the
  keyed stage, Quagmire-style): no test finds it in more than 10 of 20. That mask is the same as a second unknown
  alphabet, which F1.2 (two free alphabets) already covers by consistency, not by English.
- Every other mask is found by at least one test in 20 of 20.
- **The null is flat noise.** Against random letters with K4's counts, English letter frequencies alone lift
  plain quadgrams (base finds columns, reversal and ring-step plants 20 of 20). That null is right for readings a
  setting fixes without a climb (A13.2): those of shuffled copies are flat. It is far too easy for climbed
  readings (A13.3, A13.4), where a copy's reading is English-like junk; there the comparison with the copies'
  own readings carries the verdict, and the power above is an upper bound.
- The plants were whole readings. A13.2's readings leave 3-5 key slots free (11-19% of letters unknown), which
  lowers power a little; not measured.

## A13.2 Readings a setting fixes with no climb

**Pre-registered 2026-10-21, before ranking `pass2.json`.** All 14 tests count, on one set of readings: 14 cells.
A cell flags at an empirical p below 0.05 / 14 = 0.0036. `pass2.json` has 20 copies (p at best 1/21 = 0.048), so a
cell where K4 is above every copy is a candidate only: it is replicated on that test alone against 300 fresh plain
shuffles (seed 2113, p resolution 1/301 = 0.0033), the same pool and readings. Chance alone puts K4 above all 20
copies in about 14/21 = 0.67 cells. Only a replicated flag stops the queue.

**A fix before ranking.** `pass2.json` as written on 2026-10-18 was computed before the battery's guard against
side-by-side separators (a run like QQQQQ is not spacing) was added; K4's sep_regular there was a perfect 0.000 from
a QQQQQ run at 36-40 in one P29 reading. Pass 2 was rerun unchanged with the committed battery (same seed 1302,
2 min 54 s on 8 cores); only that one value moved. The stale file is kept as `pass2-2026-10-18-stale.json`.

Readings per text: K4 24,162; copies 23,814-24,281 (P26-29, standard, KRYPTOS and vocabulary alphabets, all
ordered pairs, three modes).

| test | K4 | copies min | copies max | K4 rank of 21 | K4's best setting |
|---|---|---|---|---|---|
| eng_base | -5.875 | -5.872 | -5.716 | 21 | P29 beau CLOCK / RIDDLE |
| freq_sorted | -2.880 | -2.906 | -2.837 | 10 | P29 beau BERLINCLOCK / HOWARDCARTER |
| ioc | 0.058 | 0.054 | 0.064 | 10 | P29 beau BERLINCLOCK / HOWARDCARTER |
| sep_words | **0.920** | 0.525 | 0.896 | **1** | P28 vig VIRTUALLYINVISIBLE / SHADOWFORCES |
| sep_regular | -0.106 | -0.192 | -0.051 | 8 | P27 vig EAST / MAGNETIC |
| eng_reverse | -6.438 | -6.579 | -6.297 | 13 | P29 beau WONDERFUL / DESPERATELY |
| eng_keep_nth | -4.630 | -4.863 | -4.322 | 12 | P27 beau MYSTERY / DESPARATLY |
| eng_drop_nth | -5.433 | -5.533 | -5.273 | 14 | P29 vig LUCIDMEMORY / WONDERFUL |
| eng_step | -5.712 | -5.982 | -5.615 | 3 | P29 vig PALIMPSEST / COMPASS |
| eng_affine_std | -5.875 | -5.872 | -5.716 | 21 | (identity map) |
| eng_affine_kry | -5.875 | -5.872 | -5.716 | 21 | (identity map) |
| eng_columns | -5.736 | -5.917 | -5.559 | 8 | P29 vig BERLIN / CARTER |
| repeats | 6 | 5 | 7 | 17 | P28 beau MESSAGE / SHADOWFORCES |
| base_pairs | -0.842 | -0.842 | -0.816 | 21 | P28 vig ABSCISSAE / SECRET |

K4 above every copy in 1 of 14 cells (chance expects 0.67). The candidate, sep_words, reads
`VSFXUY.WXEAQXQETLB...EASTNORTHEAST.DKUTYIGYFTK...YBGPUQDNIATVS.BERLINCLOCK...MGZIRSDNBFCBX.FQXKSP`: five X's,
two at the start and three at the end, splitting the text into pieces whose lengths happen to suit English word
lengths. Nothing reads.

**Replication** (`a13_check.py replicate sep_words 300 2113`, 75 s, `replicate-sep_words.json`): 3 of 300 fresh
copies at or above K4 (copies' max 0.932), p = 4/301 = 0.013, above the corrected 0.0036. **Not a flag.** In the
other direction K4 sits last on plain English (eng_base and the affine maps, rank 21 of 21) and on pair codes.

**A13.2 closed, sampled:** no structure test separates K4's no-climb readings at key lengths 26-29 from 20 plain
shuffles' after correction for 14 tests; the one candidate did not replicate (p = 0.013 against 300 copies). Power
against flat noise as in A13.1: every mask but a letter swap is seen in 20 of 20 plants by some test.

## A13.3 The saved 24-of-24 readings against their own search on fresh copies

**Pre-registered 2026-10-21, before pass 1 ran.** The 31 saved readings of 0034 (18, best per period), 0035 (3),
0048 (3), 0120 (2), 0137 (2), 0140, 0142, 0148 (1 each). Copies are the same experiment's frozen `attack.py` run
unchanged on fresh copies built as that experiment built them (`a13_check.py pass1-regen`, seed 1300): 10 plain
shuffles each for 0034, 0035, 0048; 12 decider-passing shuffles each for 0120, 0137, 0140, 0142; 12 shuffles of
the 73 unknown places for 0148. Per experiment and test the statistic is the best value over that text's readings.

All 14 tests count, on 8 experiments: **112 cells**; a cell flags at p < 0.05 / 112 = 0.00045, which needs 2,242
copies with none at or above K4. With 10-12 copies a cell where K4 is above every copy is a candidate only (chance
expects about 112/12 = 9 of them). Each candidate is replicated on that test alone with the experiment's own search
on fresh copies (seed 3113), **sequentially**: copies are drawn until one reaches K4's value, which already puts p at
or above 2/2,243 = 0.0009 and ends the replication as not a flag; a flag needs all 2,242 copies below K4. Only a
flag stops the queue.

**Result (0215 errored; 0216, 0217).** Copies: 10 (0034, 0035, 0048) or 12 per experiment, all readings re-enciphered
by their own frozen code. K4 above every copy in **2 of 112 cells** (chance 9.2): 0034/eng_keep_nth (K4 -4.752; a fresh
copy reached it at copy 6, 0216) and 0034/eng_reverse (K4 -5.458 from its period-71 reading; all 8 fresh copies of 0216
below, then 0217 continued the sequence and fresh copy 14 reached -5.419). **No flag.**

**Power on climbed readings.** Masked Carter passages enciphered under the experiment's own method and climbed by its
own frozen search, found when the mask's own test is above every copy of that experiment:

| search | unmasked | reversal | X between words | X every kth |
|---|---|---|---|---|
| 0142 (one free alphabet, L26) | 2 of 3 | 0 of 3 | 0 of 3 | 0 of 3 |
| 0140 (one free alphabet, L23) | 1 of 3 | 1 of 3 | 0 of 3 | 0 of 3 |
| 0034 (periodic, P71, sliced to that period) | - | 0 of 4 | - | - |

Every planted message itself would have been found by its test; the readings the climbs return are not. A climb fills
the free letters with forward-English junk and overwrites the mask: 1 of 22 masked plants survived. **A13.3: no flag,
but weak for masks** (blocked as a test of masked English: the battery on climbed readings cannot see one). Whether a
masked answer survives F1.5's decider is A6.3.

## A13.4 Readings kept since 2026-10-18 (0199-0214)

**Which experiments kept readings.** K4 24-of-24 readings were saved by 0207 (50), 0212 (10), 0213 (10) and 0214
(10); none by 0199, 0201-0206, 0208-0211 (0200 errored with no record). In those, no setting fits K4 at all (0199,
0201-0206, 0210, 0211) or one fits only with a free alphabet that leaves the reading undetermined (0208, 0209): there
is no K4 reading to test. Noted, not rerun. No experiment saved its copies' readings, only their scores.

**Regeneration** (`a13_check.py pass4`). Each frozen `attack.py` is imported, its search state rebuilt as its
`run()` builds it, and its own per-text search (`search` in 0207, `one_text` in 0212-0214) called on K4 and on the
same 20 seeded copies it used (seeds 2070, 2130, 2140, 2150 onward). Every reading it returns is kept, not only the
saved top ones, with "?" read as unknown and the 24 known letters set in place as the candidates set them (a slipped
known place otherwise reads the carved letter). Check: every saved K4 candidate of 0207, 0212 and 0213 is among the
regenerated readings (50/50, 10/10, 10/10; 0214 checked after the run). Plants are not rerun.

**Pre-registered 2026-10-21, before pass 4 ran.** All 14 tests on 4 experiments: **56 cells**; a cell flags at
p < 0.05 / 56 = 0.00089, which needs 1,123 copies with none at or above K4. With 20 copies, K4 above every copy is a
candidate (chance expects about 56/21 = 2.7); each is replicated on that test alone with the experiment's own search
on fresh copies (its own `shuffled`, seeds 4113 onward), sequentially as in A13.3: it ends at the first copy at or
above K4 (not a flag); a flag needs all 1,123 below.
