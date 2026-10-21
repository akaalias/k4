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
