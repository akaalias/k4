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
| 1st | F1 one keyed stage, no move | strong: K1 and K2 are Quagmire III on KRYPTOS; Sanborn's "slightly different" tableau (C27c) | nothing testable within budget: residues blocked by the English bound (0136) or by cost (F1.4, F1.7) | - | done (P7, 2026-10-17): every item closed or blocked |
| 2nd | F6 a move, then the table | strong: Sanborn's "matrix codes... then went back to this table" (C1) | nothing testable within budget: F6.1, F6.2 blocked by cost; the full type-1 library squared for F6.6 not run | low to medium | done (P8, 2026-10-17): every item closed or blocked; reopened 2026-10-20 for F6.20, F6.21 (#78), closed again 2026-10-20 (P17): F6.20 closed for key words and short free keys (0199, 0201), F6.21 closed (0202-0204) |
| 3rd | F12 Stein's way: look, quantify, then crib | strong precedent: the only hand solution of K1-K3 (Stein, 1998, 400 hours, pencil; Studies in Intelligence 1999); Stein on K4: "interesting patterns in here as well" | nothing testable here: F12.1 needs photographs of the copper | - | done (P9, 2026-10-17): F12.1 blocked, F12.2-F12.7 closed |
| 4th | F3 two-part key with a combiner | medium: Scheidt's "key word/s" (C5), his CKM habit | nothing testable here: the sandwich's 8 long length pairs and the stack's few-check cells too weak; 'the point' as a place needs a survey | - | done (P10, 2026-10-17): F3.1-F3.7 closed |
| 5th | F2 masked plaintext | medium: Scheidt "masked the English language" | nothing testable here: a code layer or another language changes the known letters; a free phrase strip is blocked by the English bound | low | done (P11, 2026-10-17): F2.1-F2.3 closed; reopened 2026-10-20 for F2.4 (#78), closed again (0205, P18) |
| 6th | F4 Sanborn's visual systems | medium, vague | nothing testable here: F4.5's shifted plate order needs Antipodes' layout | - | done (P12, 2026-10-17): F4.1-F4.4 closed, F4.5 blocked for the layout |
| 7th | F10 alphabets that change after every letter | weak to medium: no creator remark; Chaocipher (1918) was offered to US agencies and kept secret until 2010; A9, A10 | nothing testable here: Chaocipher's free wheel by cost, decks by date and bound | - | done (P13, 2026-10-17): F10.1-F10.2 closed, F10.3 blocked |
| 8th | F11 agency hand systems, now public | weak to medium: Scheidt's CIA cryptographic background; Scheidt's "key word/s" (C5) for the poem code; A9 | nothing testable here: Jefferson and M-138-A alphabets not to hand; free word picks and free tables too many | - | done (P14, 2026-10-17): F11.1-F11.4 closed; reopened 2026-10-20 for F11.5 (#78): blocked by cost (P19) |
| 9th | F8 Hill | weak: the HILL column only (C21) | nothing testable here: 3x3 with a free numbering has no checks; the older undecided settings have none either | - | done (P15, 2026-10-17): F8.1 closed for 2x2, blocked for 3x3 |
| 10th | F5 Gromark | weak: no creator remark | nothing testable here: base 26 with lag 6 and longer two-term lags blocked by cost | - | done (P16, 2026-10-17): F5.1 and F5.2 closed; reopened 2026-10-19 for F5.3 (#73), closed 2026-10-20 (0206) |
| 11th | F9 substitution, then a move | against it: Sanborn's NYPVTT to BERLIN mapping | nothing testable here: routes outside every built library are unbounded | - | done (2026-10-17): F9.1 closed; STOP_AFTER reached |
| - | F7 construction simulation | a tool, not a cipher | run before each family's first open item: does its construction make both fingerprints? | low | standing step |

Why this order: F1 and F6 rest on the two most direct creator statements. Both were tested
almost entirely on the standard, KRYPTOS and puzzle-word alphabets. An unknown alphabet is the
largest axis not yet covered, and it costs less with no move (F1) than after one (F6). F3 and
F2 come next because their remaining items are cheap. The rest are closed or blocked except
for low-value residues.

Reopened 2026-10-16 (P6, issue #50): most blocked items were blocked for one shared reason, that
no test can judge a cell the known letters leave undecided. F1.5 works on that reason directly. Two
more were blocked only because nobody had written their list (F6.3b, F9.1). Items blocked by missing
information (K5's text, a codebook) stay blocked.

## Stage 2, step 1: a positive control for every closed item (A3, issue #73)

Started 2026-10-18 (issue #52's stage 2). A closed item means our search found nothing on K4; no
search has been checked against a planted answer. Each control plants a message made with the item's
own method and a key inside its space, reruns the closing experiment's saved `attack.py` unchanged on
the planted ciphertext, and requires the plant to be found (`tools/positive_control.py`; specs in
`controls/<ID>/spec.py`; results in `controls.tsv`). Worked example: `controls/C-F1.1`.

Rules:

1. Work the table top down, in family rank order.
2. Pick the experiment that carries the item's verdict, usually the last exact one listed. Plant a key
   strictly inside the space it searched, not at an edge case, and say which key in `WHAT`.
3. `found` reads what the attack returns (`bounds` or candidates) and passes only if the plant is
   identified as the attack would have identified K4's answer: its key length, setting or reading.
4. Run the attack unchanged. If it cannot run within the budget, a control may cut the search to a
   slice that contains the planted key, and must say so: such a pass is `passed, sliced`.
5. A pass marks the row `passed` with the control's ID. A failure marks it `FAILED` and stops the
   queue: find why, fix the method, rerun the control, then rerun the item on K4 as a new experiment.
   The item is `reopened` until both are done.
6. An item whose experiment has a planted text that already went through the same unchanged search
   may cite it (`passed, own plant`, with the experiment number) instead of a new control.
7. Items with several experiments need one control per distinct search the verdict rests on; add
   rows `C-<item>b`, `C-<item>c` when that applies.
8. On a restart: first settle any `FAILED` row (rule 5), then finish `in progress` rows (controls already
   written in `controls/` but not yet in `controls.tsv`; rerun them as they are), then go on with `open` rows.

| Control | Item | What it covers | Experiments | Status | Result |
|---|---|---|---|---|---|
| C-F1-1 | F1/1 | Periodic key, standard or KRYPTOS alphabets, periods 1-26 and 30-52 | 0005, crib sweep | passed | C-F1-1 |
| C-F1-2 | F1/2 | Periods 27-29 and 53+ on any alphabet pair the puzzle's words build | 0034, 0035, 0048, 0053 | passed; blocked above 53 | 27-29: C-F1-2 (0048, judged as 0048 judged K4; first judged on 95/97 recovery, 88 reached), C-F1-2c (0053); 53: C-F1-2b (plant 0.74 above its copies, an unplanted period at most 0.34); 80: C-F1-2d no power (0.03, an unplanted period 0.12), so 0034's climb cannot decide above 53 (0136's bound): blocked |
| C-F1-3 | F1/3 | Periodic key on alphabets from any dictionary word | 0109 | passed | C-F1-3 |
| C-F1-4 | F1/4 | Progressive key | 0011, 0042, 0155 | passed | C-F1-4, C-F1-4b, C-F1-4c |
| C-F1-5 | F1/5 | Ciphertext autokey, any lag, on 1,092 keyword tables (63 vocabulary, 102 K1-K3 words,... | 0002, 0025, 0064, 0118 | passed | C-F1-5, C-F1-5b, C-F1-5c, C-F1-5d |
| C-F1-6 | F1/6 | Plaintext autokey, lags 1-52 | 0003, 0012 | passed | C-F1-6, C-F1-6b |
| C-F1-8 | F1/8 | Running key from K1-K3, the sculpture's texts, Carter, Sanborn's letters (Carter on... | 0004, 0017, 0021, 0045, 0047, 0078, 0098, 0117 | passed | C-F1-8, C-F1-8b, C-F1-8c, C-F1-8d, C-F1-8e, C-F1-8f, C-F1-8g, C-F1-8h |
| C-F1-9 | F1/9 | Running key from an unknown English text, standard, KRYPTOS or puzzle-word alphabets | 0009, 0010 | passed | C-F1-9, C-F1-9b |
| C-F1.1 | F1.1 | Free alphabet, the same on both sides (Quagmire III with unknown order), periods 3-26: the exact search | 0119 | passed | 0119's search finds the planted length 9 (8 s) |
| C-F1.1b | F1.1 | Beaufort lengths 23 and 26, decided by F1.5's design-2 decider (sampled) | 0139, 0140, 0142 | passed, own plant | 0139 (6 of 8 plants above all own copies at 23) and 0140 (5 of 6 at 26), the decider that judged K4 in 0140 and 0142 |
| C-F1.2 | F1.2 | Two free alphabets (Quagmire IV), periods 3-26 | 0097, 0121-0124, 0143-0146 | passed | C-F1.2 (0123 finds the planted length 10); sampled lengths: C-F1.2b |
| C-F1.2b | F1.2 | Lengths 8, 13, 16 decided by design 2 on two free alphabets (sampled) | 0143-0146 | passed, own plant | 0145 (4 of 4 at 8), 0143 (5 of 5 at 13, 4 of 5 at 16) |
| C-F1.3 | F1.3 | Forced key stretches read as running English on the 208,062 dictionary alphabets | 0010, 0125 | passed, own plant | 0125: 20 planted running keys through the same search, 11 beat every copy (the stated power) |
| C-F1.5 | F1.5 | A decider for cells the known letters cannot decide | 0120, 0136-0146 | passed, own plant | 0139, 0140, 0143, 0145 (design 2's plants against their own copies); design 1 failed its own check (0138) and carries no verdict |
| C-F1.4 | F1.4 | Hand key schedules other than the Berlin clock and Carter dates | 0126, 0127, 0128 | passed | C-F1.4 (0128, stutter), C-F1.4b (0127, skip) |
| C-F1.6 | F1.6 | One carved letter wrong, missing or extra, run through the exact unknown-alphabet... | 0147, 0148, 0150, 0151, 0152 | passed | C-F1.6 (0147; rerun: the first plant's restoring variant fell past 0147's 200-entry list), C-F1.6b (0150), C-F1.6c (0151 Hill; rerun after the spec's plant errored), C-F1.6d (0151 trifid) |
| C-F1.7 | F1.7 | Autokey on one unknown alphabet | 0149 | passed | C-F1.7 |
| C-F1.8 | F1.8 | Carter's book as a running key on one unknown alphabet (both directions, every offset,... | 0153 (error), 0154 | passed | C-F1.8 |
| C-F1.9 | F1.9 | Progressive key, per-letter and per-repeat, on keyword-mixed and dictionary tables;... | 0155 | passed | C-F1.9 (per-repeat, Beaufort); C-F1-4c (per-letter) on the same search |
| C-F1.10 | F1.10 | Friedman's keyword-only key-advance schedules (run length by value, CHRISTMAS,... | 0156 | passed | C-F1.10 |
| C-F1.11 | F1.11 | A split key phrase (Elementary Military Cryptography par. 59d) | 0157 | passed | C-F1.11 |
| C-F6-1 | F6/1 | Columnar (plain, keyed, double), K3's rule, quarter turns, grid paths, rail fence,... | 0006-0008, 0026, 0058, 0080-0086, 0099, 0110-0114 | passed | C-F6-1 (0110 keyword columnar), C-F6-1b (0008 K3 rule), C-F6-1c (0099 turns), C-F6-1d (0113 rail fence), C-F6-1e (0114 AMSCO), C-F6-1f (0111 Myszkowski), C-F6-1g (0112 double columnar); 0006/0007/0026/0058/0080/0082/0086 not controlled separately (same tester or covered by F6.4, F6.7) |
| C-F6-2 | F6/2 | The same moves with autokey, running key or clock schedules | 0063, 0081, 0090, 0091 | passed | C-F6-2 (0081 plaintext autokey; rerun twice for the spec's keys into 0081's counts), C-F6-2b (0081 ciphertext autokey), C-F6-2c (0090 running key), C-F6-2d (0091 clock) |
| C-F6-3 | F6/3 | Three stages | 0037, 0083, 0134 | passed | C-F6-3 (0083), C-F6-3b (0134); 0037 sampled, not controlled |
| C-F6.3b | F6.3b | Mixed triples of the four column readings at widths 25-96 | 0037, 0158 | passed | C-F6.3b |
| C-F6-5 | F6/5 | One carved letter wrong, missing or extra, through the move library | 0093, 0094 | passed | C-F6-5 (0093), C-F6-5b (0094: identified by variant, order and length; 0094 does not name the move) |
| C-F6.4 | F6.4 | Padding applied separately at each grid stage; nulls dropped between griddings | 0082, 0135 | passed | C-F6.4 |
| C-F6.5 | F6.5 | Direction words as routes through the grid | 0159 | passed | C-F6.5 |
| C-F6.6 | F6.6 | Move, change, move again | 0160 | passed | C-F6.6 |
| C-F6.7 | F6.7 | Change, move, change with the two keyed stages on different tables | 0161 | passed | C-F6.7 (14 checks; 0161 kept copies' counts only to 8 checks, where they reach 0-4) |
| C-F6.8 | F6.8 | Three-stage routes with a keyword columnar stage | 0037, 0083, 0134, 0162 | passed | C-F6.8 |
| C-F6.9 | F6.9 | Both autokeys with 0084's double columnar routes | 0084, 0085, 0163 | passed | C-F6.9, C-F6.9b (identified by the top survivor's check count, 22 and 14: 0163 does not name routes) |
| C-F6.10 | F6.10 | Padded grids whose blank cells are chosen by a key | 0082, 0135, 0165 | passed | C-F6.10 |
| C-F6.11 | F6.11 | Keyword-disrupted and triangle columnar transpositions | 0164 | passed | C-F6.11, C-F6.11b |
| C-F6.12 | F6.12 | EVA double triangle | 0166 | passed | C-F6.12 |
| C-F6.13 | F6.13 | Chiffre XIII's five-row mask, then its period-5 shifted mixed alphabet | 0166 | passed | C-F6.13 |
| C-F6.14 | F6.14 | Nihilist transposition on a 10 x 10 square with three blanks | 0167 | passed | C-F6.14 |
| C-F6.15 | F6.15 | Sanborn's "1-2-3" spacing of the raised YAR as an ordering | 0166 | passed | C-F6.15 |
| C-F6.16 | F6.16 | Interrupted-key columnar transposition | 0164 | passed | C-F6.16, C-F6.16b |
| C-F6.17 | F6.17 | Trapezoid transposition | 0164 | passed | C-F6.17 |
| C-F6.18 | F6.18 | Letters reshuffled inside each row by a keyword at widths other than 7 | 0070, 0165 | passed | C-F6.18, C-F6.18b |
| C-F6.19 | F6.19 | The French diagonal method | 0165 | passed | C-F6.19 |
| C-F12.2 | F12.2 | Quantify the impressions: K4's statistics by segment and by width (letter counts per... | 0168 (before: 0056 measured two of the patterns) | FAILED: no power; item blocked | C-F12.2: a period-7 Vigenere gives I.C. at 7 at p 0.004, C-F12.2b: two halves on two shifts p 0.01; neither leaves every one of 1,000 shuffles, the item's criterion. The criterion cannot see such structure in 97 letters |
| C-F12.3 | F12.3 | His I.C. peak at m = 13 in both K1 and K2 (C28): real or chance | 0169 (before: 0005, 0011 tested period 13 on K4 only) | not applicable | 0169 reads K1 and K2 from data/, not ctx.K4: a p-value on the published texts, not a search on K4; nothing to plant without editing data files |
| C-F12.4 | F12.4 | A pencil session: K4 written out at the widths that matter, the known letters marked,... | 0170 | FAILED: no power; item blocked | C-F12.4: a period-4 key, spacings divisible by 4 p 0.052; C-F12.4b: a simple substitution, repeated bigrams p 0.022; neither outside every shuffle |
| C-F12.5 | F12.5 | Parts with their own keys (A7): K4 split where F12.2 or F12.4 finds a break, or at the... | 0171 | passed | C-F12.5 |
| C-F12.6 | F12.6 | Probable words, his breakthrough (THE, then KNOW): common English words and the words... | 0172 (before: 0095 dragged riddle words at the live periods only) | FAILED: no power; item blocked | C-F12.6: two free alphabets at 8, the plant's consistent placements 481 against copies 518-780: true placements do not raise the count in an undecided cell |
| C-F12.7 | F12.7 | His K1-K3 method as such: every shift of each column written out, columns scored by... | 0005, 0034 | passed | cites C-F1-1 (0005's search, which the item rests on) |
| C-F3-1 | F3/1 | Two words added, both from the puzzle, or one from the dictionary | 0014, 0043, 0059, 0115 | passed | C-F3-1 (0115), C-F3-1b (0014), C-F3-1c (0059; 0043 is the same code on other alphabets) |
| C-F3-2 | F3/2 | A word plus digits from the story (coordinates, dates, counts) | 0024, 0038 | passed | C-F3-2 (0038; 0024 is the same code) |
| C-F3-3 | F3/3 | A word plus the misspelt or raised letters | 0061 | passed | C-F3-3 |
| C-F3-4 | F3/4 | Column word plus row key | 0087, 0088 | passed | C-F3-4 (0087, with K3's rule as the move), C-F3-4b (0088) |
| C-F3.1 | F3.1 | Combiners other than addition (subtraction both ways is done; table lookup through a... | 0173, 0174 | passed, own plant | 0174: two plants through the full search, found 2/2; 0173: three plants decided in their own cell by the same decide(), live 3/3 (sliced to the cell) |
| C-F3.2 | F3.2 | Numeric second parts from the Morse (E counts) and the plate layout (line lengths) | 0175 (before: 0038 did 17 digit readings) | passed | 0175's own plant (repeating readings) and C-F3.2b (the one-number-per-place branch) |
| C-F3.3 | F3.3 | Direction words as numbers (A14(b)): east-northeast as a bearing (67.5 degrees: 6, 7, 5... | 0176 (before: 0072 used direction words as keyword alphabets) | passed, own plant | 0176: 6 7 5 plus SHADOW through the same scan, found |
| C-F3.4 | F3.4 | Three or more stacked tables (US 6,075,865 with N = 3; Sanborn's "triple matrixes") | 0177 (before: 0043, 0059 two passes) | passed, own plant | 0177: three plants decided in their own cell by the same decide(), live 3/3 (sliced to the cell) |
| C-F3.5 | F3.5 | The misspelt letters' positions as indices (Q in IQLUSION, U in UNDERGRUUND, A in... | 0178 (before: 0061 used the letters) | passed, own plant | 0178: 2 8 5 plus SHADOW, found |
| C-F3.6 | F3.6 | The Weltzeituhr's rotating ring as an offset over 26 letters (C12(b)): 24 zones, the... | 0179 (before: 0052) | passed | 0179's own plant and C-F3.6b (the ring turning through the text, the other branch) |
| C-F3.7 | F3.7 | "Point" read as the decimal point in K2's "six point five", as the place on the... | 0180 (before: 0072) | passed, own plant | 0180: the four ? plus SHADOW, found |
| C-F2-1 | F2/1 | Reversal, regular nulls, prefix nulls, affine masks, doublets as nulls, nulls by letter | 0023, 0057, 0074, 0075 | passed | C-F2-1 (0023 regular nulls), C-F2-1b (0057 nulls by letter), C-F2-1c (0074 affine mask), C-F2-1d (0075 doublet null); periodic arms only, the autokey arms of 0074 and 0075 share the forced-key code |
| C-F2-2 | F2/2 | Message written along grid paths | 0092 | passed | C-F2-2 (0092) |
| C-F2.1 | F2.1 | Forced fragments at periods 24-25 after letter strike-outs not matched against words | 0181 (before: 0057) | passed | C-F2.1 (the forced reading pins the plant; 64 settings with a word against copies 0-3) |
| C-F2.2 | F2.2 | Nulls placed by a rule (after every X, after each crib word) | 0182 | passed | C-F2.2 (gap 7 above every copy; gaps 15 and 23 also give length 8: a period-8 key cannot tell d from d+8) |
| C-F2.3 | F2.3 | A plain component written from a phrase with repeated letters, so a letter can be... | 0183 | passed | C-F2.3 |
| C-F4-1 | F4/1 | Trifid, any cube, periods 2-15 | 0040 | passed | C-F4-1 (0040: the planted period and offset admit cubes, the only setting that does; the 5,000-cube cap stops short of the true cube, so the reading is not returned; first run judged on the reading, FAILED, check matched to 0040's verdict) |
| C-F4-2 | F4/2 | The plates as a key by position, straight or folded | 0089 | passed | C-F4-2 (0089; PATCH drops a K4 self-check) |
| C-F4-3 | F4/3 | Read from behind the screen | 0108 | passed | C-F4-3 |
| C-F4.1 | F4.1 | A route that follows the plates' physical layout (the S-curve, the 31-letter lines as a... | 0184 (before: 0092) | passed | C-F4.1 |
| C-F4.2 | F4.2 | Free trifid cubes at periods above 15 | 0185 (before: 0040 (2-15), 0033) | passed | C-F4.2 (0185's own plant went through solve_setting directly, not the sweep, so a new control) |
| C-F4.3 | F4.3 | The positions of the sculpture's physical anomalies as a key (C3(c)) | 0186 | passed | C-F4.3 |
| C-F4.4 | F4.4 | The extra L and the HILL row as a marker matching YAR on the lower-left plate (C21(b)) | 0005, 0017, 0089, 0186 | passed (cited) | by subsumption: C-F1-1 (0005), C-F1-8b (0017), C-F4-2 (0089), C-F4.3 (0186) |
| C-F10.1 | F10.1 | Chaocipher: two alphabet wheels permuted after every letter (Byrne, 1918; method... | 0187 | passed, own plant | 0187: plants added to the texts and through the same scan_rot as K4: consistent 26, 26, 26 (the 26 rotations), K4 0, copies 0; counts only |
| C-F10.2 | F10.2 | Wheatstone cryptograph or Alberti disk advanced by the plaintext: a 26-letter ring... | 0188 | passed | C-F10.2 (0188's plants were tested against 2,000 rings only, so a new control) |
| C-F11.1 | F11.1 | Strip ciphers and cylinders with published alphabets: M-94's 25 discs, the Jefferson... | 0189 | passed, own plant | 0189: the same consistent_cells() as K4; planted cell found at alignments 2 and 18 |
| C-F11.2 | F11.2 | Poem code: a double transposition keyed by words from a memorized text (SOE), then the... | 0190 | passed | C-F11.2 |
| C-F11.3 | F11.3 | The CIA's own 1970s Polish agent system (Bury, Cryptologia 2007): a key text written... | 0191 | passed, own plant | 0191: plants through the same search, fit once each (K2, K1-K3, Carter), copies 0; counts only |
| C-F11.4 | F11.4 | Friedman's keyed alphabet box (MC III 35b): the alphabet written n times in a... | 0192 | passed, own plant | 0192: plants fit 62 and 26 times, copies 0; counts only |
| C-F8-1 | F8/1 | Hill 2-5, plain and affine, 330 numberings (4 standard, 126 vocabulary, 200 K1-K3... | 0015, 0036, 0044, 0055, 0105, 0116 | passed | C-F8-1 (0015), C-F8-1b (0036 chained), C-F8-1c (0044; 0055's run() is the same), C-F8-1d (0105), C-F8-1e (0116 Hill with a periodic key) |
| C-F8.1 | F8.1 | Hill 2x2 and 3x3 with an unknown letter numbering (any of 26!) | 0193 (error), 0194 | passed, own plant | 0194: three plants through the same pool.map as K4, each the only fit |
| C-F5-1 | F5/1 | Gromark, two- and three-term rules, bases 2-26 (three-term on a free alphabet in base... | 0013, 0028, 0046, 0054, 0069, 0076, 0107 | passed | C-F5-1 (0013), C-F5-1b (0028), C-F5-1c (0046), C-F5-1d (0054, counts only), C-F5-1e (0069), C-F5-1f (0076), C-F5-1g (0107). Gap noted: 0054 tested rules only up to base 15 on its K1-K3-word alphabets; bases 16-26 there look untested |
| C-F5.1 | F5.1 | Multiplicative feedback; the raised YAR as primer | 0196 | passed, own plant | 0196: plants [1, 32]; the 32 at base 26 are the planted primer and its +13 variants, identical at the known places |
| C-F5.2 | F5.2 | Three-term Gromark on a free alphabet in bases 2-9, 11-16 and 26; two-term... | 0195 | passed, own plant | 0195: plants [1, 1], the planted primer each time |
| C-F9-1 | F9/1 | One-to-one substitution, then any route in the built sets (1.86M) | 0019, 0106 | passed | C-F9-1 (0019), C-F9-1b (0106) |
| C-F9.1 | F9.1 | Hand transpositions outside the built route sets | 0197, 0198 (before: 0019, 0106) | passed | 0197's own plant (keyed blanks, one of six builders); 0198 had no plant (the table's 'plants found' was wrong): C-F9.1 (0158 library), C-F9.1b (0162), C-F9.1c (0167), counts only |
| C-F6.20 | F6.20 | Turning grille, every card, by rows and by columns, free keys and key words | 0199, 0201 | passed, own plant | 0199: 4 of 4 plants (two free keys, two key words) found on their own landing maps; 0201: both free-key plants found, the two English key-word plants cut by the clock after K4 and every copy finished; the same run's self-check found 16 of 16 planted words in column mode through the same search |
| C-F6.21 | F6.21 | One slip in the column order around every keyword columnar | 0202, 0203, 0204 | passed, own plant | a planted slip per family through the same run, found at its own slip and length: 2 of 2 (0202), 3 of 3 (0203), 1 of 1 (0204) |
| C-F2.4 | F2.4 | Nulls at both ends, periodic and progressive keys | 0205 | passed, own plant | 0205: two padded messages (8 + 8 and 5 + 11 nulls, sliding keys of 9 and 11) found at their own lengths |
| C-F5.3 | F5.3 | Gromark rules in bases 16-26 on 0054's tables | 0206 | passed, own plant | 0206: a planted base-20 text (rule 7-3) found, the only rule that fits it |

## Stage 2, step 2: slip tolerance (A1, issue #76)

Started 2026-10-20. Every exact verdict assumed Sanborn enciphered all 97 letters without a slip (A1,
`knowledge/12-assumptions.md`); K1-K3 carry one enciphering slip (the letter dropped from K2) and three
misspellings in about 770 letters. This step reruns the strongest closed searches allowing for slips, judged by
the blind English judge (`kryptos/judge.py`, power in `reports/judge-bench.md`). Rules: program.md, "Slip
tolerance and the judge". Work the table top down; the families' rank order still holds inside it.

| Item | Status | Strength | Experiments | Next test or reason |
|---|---|---|---|---|
| **A1.0** One or more slips at the 73 unknown places, in systems where an error stays put (periodic, progressive and running keys; one or two free alphabets) | closed | by argument, no run: such a slip changes none of the 24 checks, so no exact verdict moves; it garbles one letter of the reading, which the judge reads through (bench: damaged classes) | - | - |
| **A1.1** One slip at a known place (k = 1), free alphabets, Gromark, trifid, Hill, and the move library | closed (cited) | exact, already run as "one carved letter wrong" (F1.6: 0147-0152; move library: 0093, 0094); a carved letter wrong at a known place is one failed check | 0093, 0094, 0147-0152 | - |
| **A1.2** Periodic key, k = 2 and 3 known letters wrong: the standard and KRYPTOS tables (8 table classes, as 0005), then one free alphabet (Quagmire III, as 0119) | closed where decidable; blocked beyond the reach | exact. Tables (0207): k = 1-3, lengths 1-26, nothing fits K4 below 25 (copies 24); 24-26 have 5/3/1 checks and fit everywhere; every reading judged with the copies': K4 best 3, copies best 8; 3 plants found (judge 82-88 against at most 6). One free alphabet (0208): K4 dead at 1-7 and 9 with up to 3 slips, fits at 8 and 10-26 as the copies do (3 of 52 cells above every copy, null 0-4); plants at 7 found, at 12 not told from copies. Two free alphabets (0209, the cost allowed it): K4 dead at 1-3 and 9, fits at 4-8 and 10-26 as copies (2 of 26, null 0-2); plants at 3 and 9 found, at 4, 5, 7 not | 0005, 0119, 0123, 0207, 0208, 0209 | reach: one free alphabet to about length 9, two to 3 (and 9). Beyond it `blocked: too short to decide k slips`: the copies fit with 2-3 slips (V10: 20 of 20 copies at k = 3 with one alphabet; 13-20 of 20 from 6 with two), the planted slips are absorbed (plants at 12, and at 4-7 with two alphabets, fit with fewer slips than planted), and the reading is undetermined, so the judge has nothing to read; only F1.5's decider (20-30 min per cell, two alphabets only below 0136's bound) could, blocked by cost as F1.4 |
| **A1.3** Running key from the named texts (K1-K3, the sculpture's texts, Carter, Sanborn's letters, as 0004-0117), k = 1, 2, 3 | closed on fixed and keyword tables; free alphabet blocked | exact. 0210: 0004/0017/0021/0045/0047/0078's sources and tables in one pass, every offset both ways, up to 7 slips (pigeonhole index, 1.36 x 10^9 trials): no setting on K4 or any of 20 copies; 3 plants found (judge 90-96). 0211: 0117's shift and 27,852 moves, both orders, up to 3 slips (compiled): none on K4 or 10 copies; 2 plants found. 0098's free alphabet: not run, measured in design: at k = 1 copies already fit 0.4-1.6% of its 80,676 settings (about 300-1,300 each; K4 2 of a 1,500 sample) with the alphabet and so the reading undetermined | 0004, 0017, 0021, 0045, 0047, 0078, 0098, 0117, 0154, 0210, 0211 | free alphabet (0098, 0154) `blocked: too short to decide k slips`: one slip already lets hundreds of settings fit on every copy, and a fitting free alphabet leaves the reading undetermined, so neither a count nor the judge can tell a slipped plant from them |
| **A1.4** Autokeys and progressive keys (F1/4-F1/6, as 0002, 0003, 0011, 0025, 0064, 0118), k = 1, 2; plaintext autokey with one slip that runs on through the chain | closed | exact. 0212: ciphertext autokey on the union of 0025/0064/0071/0072's tables (487,734 setups), every lag, 2 slips at known places or one lost step: nothing below lag 68 on K4 (copies 67-69), where 6 or fewer checks remain; 0118's copper-primed autokey closed by its own best (5 of 24 matched, so no setting within 2); progressive key on the 8 table classes, 2 slips: nothing below period 25, as copies; K4 judge best 4, copies 12; 5 plants found (60-93). 0213: plaintext autokey on 0025's tables, lags 1-52, 2 chain breaks anywhere or one lost step: nothing below lag 24 (copies 17-24); lags 26-29 read in bulk; K4 judge best 4, copies 12; 3 plants found, one with a slip running on (85, own copies at most 18) | 0002, 0003, 0011, 0012, 0025, 0064, 0118, 0212, 0213 | lags with 2 or fewer checks left after the slips (ciphertext autokey 72-96) are decided by the readings alone; plaintext autokey 53-96 stays blocked by 0136's bound |
| **A1.5** A move, then the table (F6/1's type-1 library, as 0110-0114, 0129), k = 2 known letters wrong | closed on the tables; free alphabet blocked | exact. 0214: every route of 0110-0114 (dictionary keyword columnar, Myszkowski, double columnar, rail fence, AMSCO) and the type-1 library, 1,847,590 distinct landings, both orders, 8 table classes, key lengths 1-26, up to 2 slips (cost estimated first: about 50 s per text, compiled): the shortest key that fits K4 drops to 18 after the move and 16 before it, as the copies (16-18, 16-17); K4 above every copy in 1 of 52 cells (copies 0-3); K4 judge best 6, copies 12; 3 plants found (70-92) | 0110-0114, 0129, 0214 | 0129's free alphabet after a move, not run: with no slip it already fits K4 at the copies' rate from length 6 (thousands of moves from 10), and 0208 showed one free alphabet absorbs 2 slips from about length 10 with no move at all; the reading stays undetermined, so `blocked: too short to decide k slips` |

## Stage 2, step 3: structure other than English in the 24-of-24 readings (A13, issue #75)

Started 2026-10-21 (decided by Alexis; issue #52's order: A3, then A1, then A13 and A6). Readings that put all 24
known letters in place but score like noise were thrown away. If the message was masked before it was
enciphered, the answer may be among them. The battery (`tools/a13_structure.py`, 14 tests) and the driver
(`tools/a13_check.py`) were written on 2026-10-18 and stopped part way (2935dc0); outputs in
`reports/a13-structure-data/`. Rules: program.md, "Masked English (A13) and the English score (A6)". Work the
table top down.

| Item | Status | Strength | Experiments | Next test or reason |
|---|---|---|---|---|
| **A13.1** The battery's power: which masks each of the 14 tests finds on planted masked English (20 plants per mask) | closed | measured, against flat noise | - | `power.json` complete (12 masks x 14 tests), table in `reports/a13-structure-check.md`. Every mask but a **letter swap** is found by some test in 20 of 20 plants; a letter swap (best 10 of 20) is one this step cannot see (it is a second free alphabet, F1.2's ground). The null is flat noise: an upper bound for climbed readings |
| **A13.2** Readings a setting fixes with no climb: repeating key on a fixed alphabet pair at key lengths 26-29, standard, KRYPTOS and vocabulary alphabets, three modes; K4 against 20 plain shuffles | closed | sampled | - | 14 cells, flag at p < 0.0036. `pass2.json` rerun first (the 2026-10-18 file predated the battery's side-by-side separator guard; only K4's sep_regular moved). K4 above every copy in 1 of 14 cells (chance 0.67): sep_words 0.920 against at most 0.896; replicated against 300 fresh shuffles: 3 at or above, p = 0.013, not a flag |
| **A13.3** The 31 saved 24-of-24 readings (8 experiments' `raw.json`) against the same experiment's frozen `attack.py` run unchanged on fresh copies (`a13_check.py pass1-regen`, about 1 h on 8 cores) | blocked (weak for masks); no flag | sampled. 0216: 112 cells (flag at p < 0.05/112), K4 above every copy in 2 (chance 9.2); 0034/eng_keep_nth met a fresh copy at copy 6, 0034/eng_reverse at copy 14 (0217; K4 -5.458, copy -5.419): no flag. Masked plants through the climbs (0140, 0142, 0034): unmasked 3 of 6, reversal 1 of 10, X spacing 0 of 12, though every planted message itself would be found | 0215 (error), 0216, 0217 | weak: the climbs rewrite the free letters as forward English junk, so a masked message does not survive into the reading (1 of 22 masked plants found). The battery on climbed readings cannot see a mask; a mask needs a search that keeps it (A6.3 asks this of F1.5's decider) |
| **A13.4** Readings kept since 2026-10-18 (0199-0214, among them A1's slipped readings): every 24-of-24 reading saved, K4 and copies, through the battery | closed (blind to X every kth letter) | sampled (0220): 0207, 0212, 0213, 0214 regenerated from their frozen code for K4 and their 20 copies (every saved K4 candidate among them; 0199, 0201-0206, 0208-0211 kept no K4 reading: noted). 56 cells, flag at p < 0.05/56: K4 above every copy in 1 (chance 2.7), 0212/sep_regular, met by fresh copy 27: no flag. Masked plants with 2 slips through 0207: unmasked and reversal 12 of 12, X between words 4 of 6, X every kth letter 0 of 6 | 0218 (error), 0219 (kept by mistake, #88), 0220 | an X every kth letter is not seen in these readings (0 of 6), so that mask is not excluded here |
| **A13.5** Unmask and judge: for each test that flags in A13.2-A13.4, undo the mask it found (the reversal, the nth letters, the affine map, the columns) on K4's and the copies' readings alike and judge them blind together | closed | no run: no test flagged in A13.2-A13.4 | - | report written (`reports/a13-structure-check.md`); A13 updated in `knowledge/12-assumptions.md` |

## Stage 2, step 4: does the plaintext score as English? (A6, issue #84)

Started after step 3 (decided by Alexis 2026-10-21). Every sampled verdict compared K4's climbed reading with the
copies' climbed readings by quadgram score. The judge bench (`reports/judge-bench.md`) shows the quadgram scorer
finds 10% of clean English and none of the damaged classes against English-like junk, which is what a climb
returns on a copy. These items check whether the sampled verdicts still stand. Rules: program.md, "Masked English
(A13) and the English score (A6)". Work the table top down.

| Item | Status | Strength | Experiments | Next test or reason |
|---|---|---|---|---|
| **A6.1** Rejudge the sampled verdicts: K4's and every copy's best readings from 0120, 0125, 0140, 0142, 0144, 0146 (then 0034, 0035, 0048, 0037), judged blind in one call per verdict; K4 counts only above every copy | open | sampled | - | Readings not saved are regenerated with the frozen `attack.py` and the same copies' seeds; say which. Estimate judge calls first |
| **A6.2** The climbs' power on Sanborn-style plaintext: plant the judge bench's xstops, k123 and sub3 classes (not clean Carter) through F1.5's design 2 at one length per family (F1.1 L23, F1.2 L13), and through 0125's running-key search; judged by quadgram and by the judge | open | sampled | - | If power falls below the verdict's stated power, the item it closed goes back to `open` (or `blocked` by cost) with the numbers |
| **A6.3** A13's masks through the decider: a plaintext masked by each mask A13.1 can see (reversal, X every kth, nth letters), enciphered and run through design 2 at F1.1 L23 | open | sampled | - | Says whether a masked answer would have been found at all. If not, the sampled closes are `closed for unmasked English` only |

## F13. Ciphertext only: the known words sealed (issue #85)

Drafted 2026-10-24 at Alexis's question: what would we run if no plaintext were known? Queued after Stage 2,
step 4 (A6.1-A6.3), decided by Alexis 2026-10-24. Every search so far prunes settings with the 24 known letters, which carry about
113 bits (24 x log2 26). Without them a search has only English to go on: about 1.78 bits per letter with the
quadgram scorer (0136), about 170 bits over 97 letters. Here the known letters are not read by the search at
all. They stay as gate 2, checked by the harness only after a reading has beaten its copies, so a hit is a
held-out confirmation and no key can be fitted to the known places. Rules: program.md, "Ciphertext only (F13)".
Work the table top down: F13.1 decides how much of F13.4 exists.

| Item | Status | Strength | Experiments | Next test or reason |
|---|---|---|---|---|
| **F13.1** Solvability map: for each family in `families.md`, the key space in bits, against what 97 letters of English decide (0136's 1.78 bits per letter now, Shannon's lowest entropy as the ceiling), with no known letter | open | exact (a count) | - | A desk count, no run: a table of family, key bits, decidable now, decidable with a better judge, never. Write it to `reports/` and cite it in each F13.4 row |
| **F13.2** Cipher-type identification: thousands of 97-letter texts made by each family's own generator (F7's, `kryptos/plants.py`), measured by 0168's 71 statistics and A13's 14 tests; a classifier trained on them names the families K4 resembles | open | sampled | - | Power first: how often it names the right family on held-out plants at 97 letters. 0168 found K4 inside every shuffle on all 71 statistics, so the classifier may be blind; if power is near chance, close with that number |
| **F13.3** A stronger English judge: quadgrams against longer n-grams, a word model and the blind judge, each measured as bits extracted per letter on planted texts the way 0136 measured quadgrams | open | measured | - | Each extra bit per letter moves families from "never" to "decidable" in F13.1. Reuse `reports/judge-bench.md`'s classes, Sanborn-style plaintext included |
| **F13.4** Ciphertext-only solves: hill climbs scored by the F13.3 judge alone, in each family F13.1 marks decidable, K4 against scrambled copies climbed the same way | open | sampled | - | One row per family once F13.1 is written. Plants made without known words must be found at 0120's power bar before K4's result counts |
| **F13.5** Memorable keys scored by English alone: the key-source order (K1-K3 words, the sculpture's text, the Morse, Carter, then a dictionary) through each method already built, no known-letter check | open | exact | - | Where the known letters are exact this is weaker than the checks already run; it matters only if they sit or read differently than assumed (masking, slips, offsets). Cheap; run as a hedge |
| **F13.6** A13's battery on every reading F13.4 and F13.5 produce, not only those that put the 24 letters in place | open | sampled | - | Same multiple-test rule as A13 (program.md) |
| **F13.7** The object: the carved letters checked against photographs, the ?, the line breaks, Antipodes' K4 against Kryptos' | blocked | - | - | Needs sharp photographs of the copper (#81) and Antipodes' layout (F4.5). One wrong carved letter breaks every other item |

## F1. One keyed stage, no move

| Item | Status | Strength | Experiments | Next test or reason |
|---|---|---|---|---|
| Periodic key, standard or KRYPTOS alphabets, periods 1-26 and 30-52 | closed | exact | 0005, crib sweep | - |
| Periods 27-29 and 53+ on any alphabet pair the puzzle's words build | closed at 27-29 and 53; blocked above 53 | exact consistency; the key completion is noise against coppers. Positive controls (#73): a plant is told from its copies at 28 and 53, not at 80 (C-F1-2d) | 0034, 0035, 0048, 0053 | above 53 the climb overfits copies as well as English (0136's bound): only a better English model could decide |
| Periodic key on alphabets from any dictionary word | closed | exact | 0109 | - |
| Progressive key | closed | exact for the periodic step forms tried; per-letter form and periods 26-52 on every dictionary table in F1.9 (0155) | 0011, 0042, 0155 | - |
| Ciphertext autokey, any lag, on 1,092 keyword tables (63 vocabulary, 102 K1-K3 words, 925 near-KRYPTOS, 42 compass words); a free alphabet is F1.7 | closed | exact | 0002, 0025, 0064, 0118 | - |
| Plaintext autokey, lags 1-52 | closed | exact | 0003, 0012 | - |
| Plaintext autokey, lags 53-96 | blocked | exact bound (0136) | 0012, 0136 | lags 85-96 blocked for good: the primer's open bits exceed what 73 letters of English can carry even at Shannon's lowest entropy (0136); lags 53-84 exceed the quadgram scorer's 130 bits, so only a better English model than the harness has could decide them |
| Running key from K1-K3, the sculpture's texts, Carter, Sanborn's letters (Carter on fixed and one keyword-mixed table only; Carter on a free alphabet is F1.8) | closed | exact | 0004, 0017, 0021, 0045, 0047, 0078, 0098, 0117 | - |
| Running key from an unknown English text, standard, KRYPTOS or puzzle-word alphabets | closed as far as testable | sampled; best forced stretch equals the coppers | 0009, 0010 | - |
| **F1.1** Free alphabet, the same on both sides (Quagmire III with unknown order), periods 3-26 | closed | exact for the added form at 1-26 and the Beaufort form at 1-22, 24, 25 (0119); Beaufort 23 and 26 sampled at measured power: F1.5's decider (design 2) puts K4 9th of 13 (23) and 12th of 13 (26) among copies of itself; planted texts beat all their own copies 6 of 8 (23, 0139) and 5 of 6 (26, 0140) | 0097, 0100, 0102, 0119, 0120, 0139, 0140, 0142 | - |
| **F1.2** Two free alphabets (Quagmire IV), periods 3-26 | closed where English can decide; blocked above the bound | exact: no pair fits at 1-7, 9-12, 14, 15, 17, 18, 21, 22, 25 (0123); 8, 13, 16 sampled at measured power: K4 2nd, 13th and 7th of 13 among kept-place copies (0146, 0144); power 4/4, 5/5, 4/5 (0145, 0143) | 0097, 0121-0124, 0143-0146 | 19, 20, 23, 24, 26 blocked by 0136's bound: the key's open bits exceed what the quadgram scorer can read in 73 letters (only a better English model could decide). Length 19 fit is rare (26 of 1,000 coppers, 0124): noted, not a signal |
| **F1.3** Forced key stretches read as running English on the 208,062 dictionary alphabets | closed | sampled at stated power: K4 best -4.94, inside 50 coppers (-5.28 to -4.30) and below all 20 planted running keys (-3.82 to -4.78); 11 of 20 plants beat every copper | 0010, 0125 | - |
| **F1.5** A decider for cells the known letters cannot decide | closed | step 1 exact (0136: bound per cell); step 2 two designs: design 1 (check-keeping climb, 0137) failed its validity check against each plant's own copies (0138: 6/12, bar 9); design 2 (parallel tempering in the check-keeping set, compiled) passed (0139: 6/8; also 0140, 0143, 0145 at other cells), then decided F1.1 and F1.2's cells (0140, 0142, 0144, 0146) | 0120, 0136-0146 | the rule learned: power is measured against each planted text's own scrambled copies, never the target's (0138). Covered cells too costly to run one by one are listed in their own rows (F1.4, F1.7, F6.1, F6.2) |
| **F1.4** Hand key schedules other than the Berlin clock and Carter dates | closed on the standard and KRYPTOS tables; free-alphabet residue blocked by cost | exact. List (NOTEBOOK 2026-10-16): tableau rows as keys (C20(d)); skip, stutter, back and forth, triangle, square, restart per carved line; C20(c) done by 0017/0090/0117; C20(e) K5 blocked (no text). No rule fits K4 on those tables; on free alphabets consistent at the coppers' rate (0127 rank 6 of 31) | 0126, 0127, 0128 | the free-alphabet residue (555 one-alphabet and 1,346 two-alphabet settings consistent on K4) is decidable in principle (0136) and F1.5's decider exists, but each setting costs a power test plus K4 against 12 copies (about 20-30 min): about 900 hours. Blocked by cost, not by principle |
| **F1.6** One carved letter wrong, missing or extra, run through the exact unknown-alphabet tests, then the other exact verdicts on free alphabets | closed (one cell blocked, weak) | exact: periodic one and two free alphabets, 604 variants (0147: K4 above every copper in 2 of 78 cells, null 0-11); Gromark 0069/0076/0107, 605 variants: no fit (0150); trifid, 5,044 variants anywhere: no cube (0151); Hill, 5,044 variants: 257 alive with one check, rank 4 of 11 against copies (0151, 0152) | 0147, 0148, 0150, 0151, 0152 | the one cell 0147 revived by meaning, K1/K2's added form at length 19 with the carved S at 33 a slip, failed the decider's power bar (0148: 3/5, bar 4; one plant recovered exactly): blocked, weak |
| **F1.7** Autokey on one unknown alphabet | closed with no move where dead; fitting lags and the move version blocked by cost | exact (0149): ciphertext and plaintext autokey, three forms, every lag with equations; K4 fits 9-23 lags per kind and form, copies 3-30; rare fits 4 against 0-27 | 0149 | fitting lags (about 100 cells) need F1.5's decider at about an hour each; the move-first version is about 176 million exact searches. Blocked by cost |
| **F1.8** Carter's book as a running key on one unknown alphabet (both directions, every offset, three rules); for every running-key source, whether two unknown alphabets leave any checks | closed (one alphabet); two alphabets blocked by structure | exact (0154): no offset fits K4 or any of 10 copies; 953 of about 1.7 million undecided at the node limit (copies 99-20,675). Two alphabets: the 24 equations leave 0.1 checks on average, at most 4, for Carter, K2, K3 and the cipher panel | 0153 (error), 0154 | two unknown alphabets with a running key cannot be decided by the known letters |
| **F1.9** Progressive key, per-letter and per-repeat, on keyword-mixed and dictionary tables; periods 26-30 against coppers; Kryha's step 3 at 31-52 | closed | exact (0155): 1,040,314 tables x 2 forms x steps 1-25 x periods 1-52; shortest consistent period 25 (copies 24); K4 above every copper in 4 of 104 cells, null 0-5 | 0155 | period 34 noted (K4 40 and 20 consistent pairs against copier maxima 10 and 7), inside the fixed statistic, not chased |
| **F1.10** Friedman's keyword-only key-advance schedules (run length by value, CHRISTMAS, EXTINGUISHER windows, ciphertext and plaintext interruptors, fraction digits) | closed | exact (0156) with 10 copies: no dictionary word fits any word schedule on K4 or the copies; ciphertext interruptor and fraction digits 0 on K4 (copies 0-14); plaintext interruptor inside the runs 160 against 120-7,165 | 0156 | free-alphabet versions are F1.4's residue (blocked by cost) |
| **F1.11** A split key phrase (Elementary Military Cryptography par. 59d) | closed | exact (0157): 29,880 phrases (puzzle-word pairs, K1-K3 word runs split at each boundary) x 3 numberings x 3 rules: best 7 of 24 known letters on K4, copies 7-8, no full hit | 0157 | - |

## F6. A move, then the table

| Item | Status | Strength | Experiments | Next test or reason |
|---|---|---|---|---|
| Columnar (plain, keyed, double), K3's rule, quarter turns, grid paths, rail fence, AMSCO, Myszkowski, then a periodic key on standard, KRYPTOS or word alphabets | closed | exact | 0006-0008, 0026, 0058, 0080-0086, 0099, 0110-0114 | - |
| The same moves with autokey, running key or clock schedules | closed | exact | 0063, 0081, 0090, 0091 | - |
| Three stages | closed | exact for clockwise triples at 2-96 (0083) and every mix of four column readings, triples at widths 2-24 and pairs at 2-96 (0134) | 0037, 0083, 0134 | **F6.3** done: nothing live below 20, at the coppers' rate; mixed triples at widths 25-96 are F6.3b |
| **F6.3b** Mixed triples of the four column readings at widths 25-96 | closed | exact (0158): 105,548,253 distinct routes (compiled, checked against Python); shortest consistent key 18 after (copies 19), 24 before (17); K4 above every copper in 3 of 52 cells, null 0-3 | 0037, 0158 | one setting at 18 (col 93, cw 65, cw 84; KRYPTOS table, Beaufort) noted |
| One carved letter wrong, missing or extra, through the move library | closed | exact | 0093, 0094 | - |
| AMSCO at period 23 after the move: 15 distinct check sets against 1-9 on the coppers | noted, not chased | exact | 0114 | within the 4.7 of 52 cells expected outside the range by chance; replicate only if F6 reaches AMSCO again |
| **F6.1** Free alphabet (Quagmire III) after or before each move, periods 3-26 | **blocked** (closed exact where testable) | exact: every type-1 move, both orders, both forms, lengths 1-26; no fit below 6; fitting cells at the coppers' rate (0129: 7 of 52 cells above every copper, null 0-8; 0130: 0, null 0-10) | 0097, 0129, 0130 | blocked by cost: a decider with measured power exists (F1.5, design 2), but K4 fits about 443,000 (move, length) settings at 20-30 min each (power test plus K4 against copies); reopen only with a cheaper decider |
| **F6.2** Two free alphabets after or before each move | **blocked** (closed exact where testable) | exact at 1-10 for every move, both orders, with undecided counted; per-slot refutation at 11-26 (0133); 97-99% of per-slot survivors fit at 11-26 (0131, 0132); K4 above every copper in 5 of 52 cells, null 2-7 | 0097, 0131, 0132, 0133 | lengths 15-26 blocked by 0136's bound; 3-14 blocked by cost as F6.1 (tens of thousands of fitting settings) |
| **F6.4** Padding applied separately at each grid stage; nulls dropped between griddings | closed | exact: the hand padding rules listed in NOTEBOOK 2026-10-16 (blanks in 8 places per grid, dropped or kept as dummies), one stage at widths 2-96, two at 2-48, periodic key 1-26 either side, 874,572 routes; nothing live below 21, at the coppers' rate (0135) | 0082, 0135 | - |
| **F6.5** Direction words as routes through the grid | closed | exact (0159): the 16 compass points as reading directions at every width, lines either way, and E/ENE/NE in two stages: 110,820 routes; shortest consistent key 21 after, 25 before, as the copies; 1 of 52 cells, null 0-1 | 0159 | - |
| **F6.6** Move, change, move again | closed for a library of 844 moves | exact (0160): column readings at every width and K3's rule at every multiplier, both directions; all 712,336 ordered pairs; shortest consistent key 20 (copies 18); 1 of 26 cells, null 0-2 | 0160 | the full type-1 library squared (776 million pairs) would need the composition compiled; not run |
| **F6.7** Change, move, change with the two keyed stages on different tables | closed | exact (0161): standard then KRYPTOS or the reverse, keys 2-14 each, 844 moves, propagation over the one-to-one links; consistent with 5+ checks K4 388, copies 300-504; every level inside | 0161 | one 9-check setting (inverted two-row turn at width 84, keys 13 and 13) noted; copies' 9-check count not recorded |
| **F6.8** Three-stage routes with a keyword columnar stage | closed | exact (0162): 131 distinct keyword columnars (puzzle, K1-K3 words) and 92 plain readings (widths 2-24), every triple with a keyword stage: 20,370,476 routes; shortest consistent key 20 after, 24 before, as the copies; 0 of 52 cells | 0037, 0083, 0134, 0162 | - |
| **F6.9** Both autokeys with 0084's double columnar routes | closed | exact (0163): 3,284,523 routes x lags 1-96 x after/before x ciphertext/plaintext autokey x std/KRYPTOS x 3 rules; survivors with 5+ checks K4 0, 9, 1, 0 against copies 0-8, 5-21, 0-1, 0-480 | 0084, 0085, 0163 | - |
| **F6.10** Padded grids whose blank cells are chosen by a key | closed | exact (0165): blanks under the first or last key numbers in the last or first row, 181,308 keywords, 1,450,196 routes; shortest consistent key 21 after, 25 before (copies 20, 24); 0 of 52 cells | 0082, 0135, 0165 | - |
| **F6.11** Keyword-disrupted and triangle columnar transpositions | closed | exact (0164): disrupted columnar 327,440 routes, TM 32-220 triangle (19 columns, blanks at end or start) 654,876 routes, 163,720 keywords; shortest consistent keys 23 / 24 (copies 22 / 24); 0 and 1 of 52 cells | 0164 | free-table version not run: after a move free alphabets fit at the copies' rate (F6.1) |
| **F6.12** EVA double triangle | closed | exact (0166): 1,920 19-letter keys (K1-K3 windows, dictionary, puzzle pairs); no key up to 26 after the move on K4 or copies, 25 before as the copies | 0166 | - |
| **F6.13** Chiffre XIII's five-row mask, then its period-5 shifted mixed alphabet | closed | exact (0166), as a parametric family: the source does not give the rule for rows 2 and 4, so every split and row-4 shift for 6,296 keys of 24-31 letters (2,248,512 masks), then the published substitution on an unknown alphabet decided exactly: no mask consistent with 3+ checks on K4 or any copy | 0166 | the documented mask rule (forms 5-9) would need the primary text (scz.bplaced.net §10.1) |
| **F6.14** Nihilist transposition on a 10 x 10 square with three blanks | closed | exact (0167): all 10! keys x 8 blank places x row or column reading x both directions = 116,121,600 routes; shortest consistent key 20 after, 24 before (copies 18, 17); 0 of 52 cells | 0167 | - |
| **F6.15** Sanborn's "1-2-3" spacing of the raised YAR as an ordering | closed | exact (0166): counting off 1-2-3 and 4-5-7 (YAR's places in ENDYAHR) in every order around the text; nothing up to 26 after, 26 before, as the copies | 0166 | other readings of "1-2-3" (C22(d)) not specified by the source |
| **F6.16** Interrupted-key columnar transposition | closed | exact (0164): rows cut by the keyword's numbering (163,720 keywords) or by the digits of 1/d (puzzle words): 332,817 routes; shortest consistent key 23 after (copies 21), 25 before (24); 1 of 52 cells, null 0-3 | 0164 | - |
| **F6.17** Trapezoid transposition | closed | exact (0164): base = keyword length, rows one shorter going up on either side, fewest blanks: 89,708 routes; shortest consistent key 26 after, 25 before (copies 23, 24); 0 of 52 cells | 0164 | - |
| **F6.18** Letters reshuffled inside each row by a keyword at widths other than 7 | closed | exact (0165): widths 2-48 (dictionary and puzzle words; K1-K3 windows for 25-48), 361,698 routes; shortest consistent key 21 after, 25 before (copies 21, 24); 2 of 52 cells, null 0-2 | 0070, 0165 | - |
| **F6.19** The French diagonal method | closed (key-named diagonals) | exact (0165): the diagonals from the tops of the columns numbered 1 to j first, then columns by key order (j up to the key length for puzzle words, 1-3 for dictionary words): 2,264,476 routes; shortest consistent key 22 after, 24 before (copies 20, 24); 1 of 52 cells | 0165 | diagonal sets not named by the key would be an extra agreement with no source: not tested |
| **F6.20** Turning grille (Fleissner): a 10x10 card with 25 holes turned four times holds K4's 97 letters plus 3 empty squares; the grille before or after a periodic key on the KRYPTOS or standard table, both orders (issue #78) | closed for key words and short free keys; long free keys blocked by cost | exact: every card (4^25), turned cw or ccw, empty squares at the end or start, copied out by rows (0199) or by columns (0201; written by columns is the transpose): free keys 1-6 by rows and 1-4 by columns (8 classes), and 200,563 key words of 7-28 letters on 24 conventions: no landing map fits K4 or any of 10 copies; plants found (0201's English key-word plants cut by the clock after every copy finished; self-check 16/16 planted words). F7: grille plus key makes both fingerprints in 0 of 2,000 | 0199, 0200 (error), 0201 | free keys of 7-26 letters (rows) and 5-26 (columns) blocked by cost: 10^8-10^9 nodes per setting at 7 by rows, over 2 x 10^9 at 12; the Abwehr's 13x19 stencil and other fixed stencils not tested (no remembered rule for their holes) |
| **F6.21** A deliberate procedural slip in the transposition: one column skipped or doubled, or one digit of the key's numbering wrong, around every keyword columnar already tested (issue #78) | closed | exact (0202, 0203): one column read out of its place (a misnumbered key; adjacent swaps included) or two swapped, in any one pass, around 0110's dictionary keyword columnar (67.8M slipped routes), 0112's double (135.5M), 0164's interrupted key (51.9M) and trapezoid (26.0M), 0165's row reshuffle (121.7M) and 0190's poem code (3.8M), then or before a periodic key 1-26: shortest consistent keys as the copies; K4 above every copy in 0-2 cells per family except the row reshuffle's 6 (null 1), which 40 fresh copies dissolved (0204: 1 cell, copies 0-2); plants 6 of 6 | 0202, 0203, 0204 | a skipped or doubled column alone changes the length (97 needs a longer message or two compensating slips): not searched; Myszkowski, AMSCO, keyed blanks, triangle, disrupted not on the item's list. A21 in the row reshuffle (rows of 9, 88 settings vs copies' max 54) noted, not chased |

## F12. Stein's way: look, quantify, then crib

Added 2026-10-16 (issue #53). Not a cipher type but a way of working: what David Stein, who
solved K1-K3 by hand in 1998, would do with a few free weeks and today's record. Source:
`knowledge/sources/stein-1999-cracking-the-courtyard-crypto.txt`. He looked before he attacked
("I seemed to see different patterns throughout, but I wanted to quantify these impressions"),
split the text where its statistics changed, read the plaintext for hints about the method, and
when the statistics ran out, guessed probable words. Items F12.2 and F12.4 produce
observations, not verdicts: each observation that stands outside the shuffles becomes a new item,
in this family or the one it points to.

| Item | Status | Strength | Experiments | Next test or reason |
|---|---|---|---|---|
| **F12.1** The 97 letters and the "?" checked against images of the copper (he walked out to feel UNDERGRUUND) | blocked (partly checked) | partial (issue #81): a Library of Congress photo (Highsmith, LCCN 2011631531) taken from behind shows 60 of K4's 97 letters at letter resolution, all agreeing with the transcription (lines 2-4 except their last 10-12 letters); `?OBKR` and 37 letters remain unseen. The NYT 2010 typeset clue also agrees | - | a second image of the plate's other end (A4, A1); reports/k4-photo/ |
| **F12.2** Quantify the impressions: K4's statistics by segment and by width (letter counts per segment, I.C. against period 1-48 as in his Figure 26, positional patterns at widths 7, 21, 31), each against 1,000 shuffles | blocked | sampled (0168): 71 statistics fixed before the run, each against 1,000 shuffles; nothing outside every shuffle (0.14 expected); smallest p the width-7 doublets (0.002), as 0056 | 0168 (before: 0056 measured two of the patterns) | weak: a positive control (#73) planting the structure the test looks for is not told from shuffles or copies (C-F12.2, C-F12.2b); the 'nothing found' says little |
| **F12.3** His I.C. peak at m = 13 in both K1 and K2 (C28): real or chance | closed | sampled (0169): K1 p 0.0075 against 10,000 shuffles within its key columns, about 0.019 allowing for the strand counts scanned (post hoc); Part II 0.24, K4 0.21: chance, nothing overlaid | 0169 (before: 0005, 0011 tested period 13 on K4 only) | - |
| **F12.4** A pencil session: K4 written out at the widths that matter, the known letters marked, every pattern noted before any search code ("the process of discovery is often intuitive as well as analytic") | blocked | sampled (0170): six patterns noted by eye at widths 7-31; none outside 1,000 shuffles; two at p 0.004, found by looking; no new item | 0170 | weak: a positive control (#73) planting the structure the test looks for is not told from shuffles or copies (C-F12.4, C-F12.4b); the 'nothing found' says little |
| **F12.5** Parts with their own keys (A7): K4 split where F12.2 or F12.4 finds a break, or at the known stretches, each part with its own periodic key on the standard or KRYPTOS tables | closed | exact (0171): split between the runs (no break found), each part its own key up to 12 and 10 on 8 table classes; no length fits K4 (copies 0-1 cells) | 0171 | - |
| **F12.6** Probable words, his breakthrough (THE, then KNOW): common English words and the words of K1-K3's plaintexts placed at every position in the cells the 24 known letters cannot decide (F1.1 Beaufort 23 and 26, F1.2's consistent lengths, F6.1, F6.2) | blocked | exact (0172): 60 words x 3,634 placements in the ten undecided cells; K4 above every copy in 1 of 10 cells, copies 0-3: chance; F6.1 and F6.2 have no cells to place words in (blocked by cost) | 0172 (before: 0095 dragged riddle words at the live periods only) | weak: a positive control (#73) planting the structure the test looks for is not told from shuffles or copies (C-F12.6); the 'nothing found' says little |
| **F12.7** His K1-K3 method as such: every shift of each column written out, columns scored by summed log letter frequencies, then a crib | closed | by subsumption, no run: 0005's exact sweeps cover every periodic key on the standard and KRYPTOS tables, which is what the column method finds; the live lengths fit coppers equally (0034) | 0005, 0034 | - |

## F3. Two-part key with a combiner

| Item | Status | Strength | Experiments | Next test or reason |
|---|---|---|---|---|
| Two words added, both from the puzzle, or one from the dictionary | closed | exact | 0014, 0043, 0059, 0115 | - |
| A word plus digits from the story (coordinates, dates, counts) | closed | exact | 0024, 0038 | - |
| A word plus the misspelt or raised letters | closed | exact | 0061 | - |
| Column word plus row key | closed | exact | 0087, 0088 | - |
| **F3.1** Combiners other than addition (subtraction both ways is done; table lookup through a second alphabet, multiplication mod 26). First the sandwich from Scheidt's patent US 6,075,865: c = T2[T1[p + a] + b], two key streams on either side of a fixed keyed alphabet, T1 and T2 from {standard, KRYPTOS, their inverses}, periods up to about 13 each (report `reports/Scheidt patents and field ciphers.md` (issue #9)) | closed | exact: the patent sandwich (0173), 108 table classes, key lengths 1-13 each: nothing fits K4 at the 161 length pairs with 4 or more checks (copies at most 2 in 1,000); the 8 pairs with both keys 10-13 leave 1-2 checks and are blocked; two words added on 61 mixed numberings or multiplied mod 26 (0174): no consistent case on K4 or copies | 0173, 0174 | - |
| **F3.2** Numeric second parts from the Morse (E counts) and the plate layout (line lengths) | closed | exact (0175): 26 readings (Morse E runs and totals in two transcriptions, the line lengths and their departures from 31, K4 line and column on the copper), each value one key number, with an unknown word of 1-24 on 12 table rules: nothing fits K4 or 20 copies | 0175 (before: 0038 did 17 digit readings) | - |
| **F3.3** Direction words as numbers (A14(b)): east-northeast as a bearing (67.5 degrees: 6, 7, 5 or 67, 5), as compass point 6 of 32 or 3 of 16, and the same for EAST and NORTHEAST, as a numeric second part beside a word | closed | exact (0176): 43 readings of east-northeast, east and northeast as degrees, digits, mils and compass points of 32 and 16, with an unknown word of 1-24 on 12 table rules: nothing fits K4 or 20 copies | 0176 (before: 0072 used direction words as keyword alphabets) | - |
| **F3.4** Three or more stacked tables (US 6,075,865 with N = 3; Sanborn's "triple matrixes") | closed | exact (0177): two KRYPTOS-order tables (or inverses) and three keys of 1-10, 144 classes: nothing fits K4 or copies where the known letters give 4 or more checks (780 length triples); 1-3 checks at the copies' rate, too weak | 0177 (before: 0043, 0059 two passes) | - |
| **F3.5** The misspelt letters' positions as indices (Q in IQLUSION, U in UNDERGRUUND, A in DESPARATLY, the missing E, the raised YAR), and their orientation read literally (RQ as YR) (C10(a), C10(c)) | closed | exact (0178): 40 readings of the misspelt letters' places (in word, in plaintext, through K1-K3), the raised YAR, the letters and their shifts, RQ/YR, Bauer's coordinates, with an unknown word of 1-24 on 12 table rules: nothing fits K4 or 20 copies; index readings as a short key are excluded by 0005 | 0178 (before: 0061 used the letters) | - |
| **F3.6** The Weltzeituhr's rotating ring as an offset over 26 letters (C12(b)): 24 zones, the ring's rotation through the day | closed | exact (0179): 56 readings of the 24-zone ring over 26 letters (one zone per letter either way, or one zone every 24 or 4 letters), with an unknown word of 1-24 on 12 table rules: nothing fits K4 or 20 copies | 0179 (before: 0052) | - |
| **F3.7** "Point" read as the decimal point in K2's "six point five", as the place on the grounds, or as a punctuation mark (C15(b)-(d)) | closed | exact (0180): 25 readings (six point five, the coordinates with the point, the four ?, K2's ? and X stops) with an unknown word of 1-24 on 12 table rules: nothing fits K4 or 20 copies; the place reading blocked without a survey | 0180 (before: 0072) | - |

## F2. Masked plaintext

| Item | Status | Strength | Experiments | Next test or reason |
|---|---|---|---|---|
| Reversal, regular nulls, prefix nulls, affine masks, doublets as nulls, nulls by letter | closed | exact | 0023, 0057, 0074, 0075 | - |
| Message written along grid paths | closed | exact | 0092 | - |
| **F2.1** Forced fragments at periods 24-25 after letter strike-outs not matched against words | closed | exact (0181): the forced readings at key lengths 24-25 after every one- or two-letter strike-out hold no dictionary word of 6+ letters on K4; kept-place copies 0-32 settings | 0181 (before: 0057) | - |
| **F2.2** Nulls placed by a rule (after every X, after each crib word) | closed | exact (0182): any rule acts on a repeating or progressive key only through the number of nulls between the runs; every count 0-29, lengths 1-26, steps 0-25, 12 rules: K4 never above the copies (96 checked live cells vs 96-226) | 0182 | - |
| **F2.3** A plain component written from a phrase with repeated letters, so a letter can be enciphered by any of its places: homophones that keep the length | closed | exact (0183), a derivation, not a documented method: 1,196 phrase windows (K1-K3, Morse, Carter's book, famous sentences) as the plain strip, keys 1-26: nothing fits K4 at 1-25; at 26 (1 check) as copies; any phrase at all is a free alphabet with repeats, blocked by the English bound | 0183 | - |
| **F2.4** Nulls at both ends of the message: a run of random letters before and after it (SOE's Dutch section used eight at each end, 1943) (issue #78) | closed | exact (0205): the end run moves nothing, so every pair 0-12 reduces to the start run s; known words at copper places q + s, s 0-12, periodic (as 0023) and progressive keys (per letter and per repeat, steps 1-25), lengths 1-52, 8 table classes: nothing fits below 26 on K4 or any of 10 copies; K4 above every copy in 0 cells (null 0-5); 2 planted padded messages found at their own lengths | 0023, 0205 | - |
| A code layer, phonetic spelling, another language | blocked | - | - | changes the letters at the known places or needs a codebook we lack |

## F4. Sanborn's visual systems

| Item | Status | Strength | Experiments | Next test or reason |
|---|---|---|---|---|
| Trifid, any cube, periods 2-15 | closed | exact | 0040 | periods above 15 are F4.2 |
| The plates as a key by position, straight or folded | closed | exact | 0089 | - |
| Read from behind the screen | closed | exact | 0108 | - |
| **F4.1** A route that follows the plates' physical layout (the S-curve, the 31-letter lines as a grid with K3's last line) | closed | exact (0184): rows, columns, diagonals and spirals from every corner over K4's four lines as carved (starting after K3 and the ?), the lower plate and the whole left side, 73 routes and inverses, then or before a periodic key 1-26: shortest live 23/26 as copies 22/26, 0 of 52 cells above copies; the Blender model not needed (the transcript gives the layout) | 0184 (before: 0092) | - |
| **F4.2** Free trifid cubes at periods above 15 | closed | exact (0185): periods 16-97, every alignment, 4,633 settings: no free cube fits K4 or ten shuffled copies; a plant's cube found | 0185 (before: 0040 (2-15), 0033) | - |
| **F4.3** The positions of the sculpture's physical anomalies as a key (C3(c)) | closed | exact (0186): the ?, K2's omitted S, the raised YAR, the extra L and the odd lines located on the transcript, 22 readings as numbers with an unknown word of 1-24 on 12 table rules: nothing fits K4 or 20 copies | 0186 | - |
| **F4.4** The extra L and the HILL row as a marker matching YAR on the lower-left plate (C21(b)) | closed | by subsumption, no run: as a row or key letter (L, HILL, YARL) a periodic key, dead to 26 (0005); as a start in the tableau, a running key from every start (0017); as a plate laid over K4 (0089); as a place, 0186 | 0005, 0017, 0089, 0186 | - |
| **F4.5** Antipodes' differences: the plate order "shifted a little" and the UUND/RTBJ spelling (C26) | blocked | the spelling (R to E at place 178) as a key fragment is closed by subsumption (0005; 178 in 0178); the shifted order needs Antipodes' K4 line layout, not in the repository | 0178 | a transcript or photographs of Antipodes' K4 section |

## F10. Alphabets that change after every letter

Added 2026-10-16 (issue #51). Every family above uses a fixed alphabet with a changing key
(assumption A10, `knowledge/12-assumptions.md`). These keep the letter-for-letter link the
known letters need, and can be worked by hand.

| Item | Status | Strength | Experiments | Next test or reason |
|---|---|---|---|---|
| **F10.1** Chaocipher: two alphabet wheels permuted after every letter (Byrne, 1918; method disclosed 2010) | closed | exact (0187): the left wheel's start fixes every move from the carved text; each known letter pins the right wheel's start (11 checks); every keyword-mixed left wheel (208,651, rotations equivalent): none fits K4 or 10 copies, plants found; a free left wheel (about 88 bits) blocked by cost | 0187 | - |
| **F10.2** Wheatstone cryptograph or Alberti disk advanced by the plaintext: a 26-letter ring against a 27-place ring, the pointer moved by the distance between plaintext letters (Wheatstone, 1867) | closed | exact (0188): 8 variants; inside each run the hand's steps fix the inner places up to one offset; even a free inner ring fits neither K4 nor 20 copies (K4's QQ at 26-27), nor any word-mixed ring; plants found | 0188 | - |
| **F10.3** A key stream from a deck of cards (Solitaire 1999, Mirdek 2000) | blocked | after 1990 (Solitaire 1999, Mirdek 2000; A9); a free deck is about 237 bits against about 113 bits of known key values; no published known-plaintext attack from 24 outputs | - | a pre-1990 deck method with a keyword-set deck |

## F11. Agency hand systems, now public

Added 2026-10-16 (issue #51). The method had only to be known to its creators in 1990
(assumption A9); Scheidt chaired the CIA's Cryptographic Center until 1989. Systems that turn
letters into digits or Morse (VIC, straddling checkerboards, fractionated Morse, Nihilist) are
left out while the letter-for-letter reading of the known letters holds (A2).

| Item | Status | Strength | Experiments | Next test or reason |
|---|---|---|---|---|
| **F11.1** Strip ciphers and cylinders with published alphabets: M-94's 25 discs, the Jefferson wheel, M-138-A strips where published | closed | exact (0189): M-94, 25 published discs in any order, any row per group of 25, any alignment: no setting fits K4 or 10 copies, plants found; Jefferson's wheel and M-138-A strips blocked (alphabets not to hand) | 0189 | published alphabets of Jefferson's wheel or M-138-A strip sets, if supplied |
| **F11.2** Poem code: a double transposition keyed by words from a memorized text (SOE), then the table | closed | exact (0190): 3,063 phrase keys (1-6 consecutive words of K1-K3 and the Morse, same key twice or split), then or before a periodic key 1-26: shortest live 24/25 as copies 22/25, 0 of 52 cells; free word picks not listed | 0190 | - |
| **F11.3** The CIA's own 1970s Polish agent system (Bury, Cryptologia 2007): a key text written row by row into a box and read out by columns, then a reciprocal 26 x 26 table | closed | exact (0191): K2, K3, K1-K3 and Carter's book as key texts, widths 2-50, column orders incl. vocabulary keywords, Bury's reciprocal and 3 other tables on std/KRYPTOS, every start (732M settings): no fit on K4 or 10 copies, plants found; best partial 9/24 as copies; a free table not run | 0191 | a free table, other key texts (Sanborn's letters) |
| **F11.4** Friedman's keyed alphabet box (MC III 35b): the alphabet written n times in a rectangle, read out by a keyword's column order as the key stream | closed | exact (0192): 163,726 keyword column orders, standard or KRYPTOS alphabet 1-8 times, every start, 8 tables (2.45 billion settings): no fit on K4 or 10 copies, plants found; free tables not run | 0192 | - |
| **F11.5** Poem code as agents used it: five words picked from anywhere in a remembered text (K1-K3's plaintexts), their letters numbered alphabetically as a double transposition key, then the table (issue #78) | blocked | by cost, no run (NOTEBOOK 2026-10-20): K1-K3 hold 163 words; five picked in text order give C(163,5) = 9.0 x 10^8 keys per pass, two passes with different picks (Marks pp. 11, 31-32) 8.1 x 10^17 (59.5 bits). Decidable in principle only where the 24 known letters leave 14 or more checks (short keys), but no known letter's carved place can be fixed without both whole keys, so no constraint search cuts it; enumeration at the measured 0.5 million routes a second would take about 5 x 10^4 years | 0190 (consecutive words only) | a single pass with one five-word key (9.0 x 10^8 keys, about an hour on 8 workers) is feasible but is not the agents' method; the same five words for both passes is not in the source. Reopen if a source gives the indicator rule that fixes which words were picked |

## F8 Hill, F5 Gromark, F9 substitution then a move

| Item | Status | Strength | Experiments | Reason |
|---|---|---|---|---|
| Hill 2-5, plain and affine, 330 numberings (4 standard, 126 vocabulary, 200 K1-K3 words; an unknown numbering is F8.1), chained, with a periodic key | closed, except what had too few equations: 5x5 affine (14 of 20 settings undecided, 0105) and 400 of 936 Hill-plus-key settings, mostly 4x4 with long keys (0116) | exact where decided | 0015, 0036, 0044, 0055, 0105, 0116 | the undecided settings are blocked: no checks. Reopen if F1.5 reaches power and the bound in its step 1 allows |
| **F8.1** Hill 2x2 and 3x3 with an unknown letter numbering (any of 26!) | closed (2x2); blocked (3x3) | exact (0194): 22 equations against 96-98 bits; every invertible 2x2 matrix, both alignments, any one-to-one numbering: none fits K4 or 5 copies, plants recovered; 3x3 is 21-32 bits short of a check | 0193 (error), 0194 | - |
| Gromark, two- and three-term rules, bases 2-26 (three-term on a free alphabet in base 10 only; other bases are F5.2) | closed | exact | 0013, 0028, 0046, 0054, 0069, 0076, 0107 | - |
| **F5.1** Multiplicative feedback; the raised YAR as primer | closed | exact (0196): products of two earlier digits, lags to 6 in bases 2-16 and to 5 in base 26, free alphabet, 4 forms: nothing fits K4 or 10 copies; YAR as a primer subsumed by the full primer sweeps (0076, 0195) | 0196 | - |
| **F5.2** Three-term Gromark on a free alphabet in bases 2-9, 11-16 and 26; two-term free-alphabet rules beyond lag 6 (base 10) and 5 (other bases) | closed | exact (0195): three-term in bases 2-9, 11-16 (lags to 6) and 26 (to 5); two-term base 10 lags 7-8, other bases lag 6; 1.55 billion primers, 4 forms, free alphabet: nothing fits K4 or 10 copies, plants found; base 26 lag 6 and longer two-term lags blocked by cost | 0195 | - |
| **F5.3** Gromark rules in bases 16-25 on 0054's K1-K3-word and 2025-letter alphabet pairs (found by C-F5-1d, #73): 0054 tested rules only where a pair admits base 15 or less, and 0076/0195's free-alphabet sweeps keep the plain side standard and skip bases 17-25 | closed | exact (0206): 0046's test on 0054's 102 tables (10,404 pairs), 3 forms, 364 two- and three-term rules with lags to 13, every base 16-26 a pair admits, six or more checks inside the known runs, then the stream carried to the second run: no rule fits K4 or any of 10 copies; a planted Gromark text (base 20, rule 7-3) found, the only fit; 8,960 cases spot-checked against Python | 0054, 0206 | - |
| One-to-one substitution, then any route in the built sets (1.86M) | closed | exact | 0019, 0106 | - |
| Routes outside every built set | blocked | - | - | unbounded without a hand-method list; F9.1 writes that list |
| **F9.1** Hand transpositions outside the built route sets | closed | exact (0197, 0198): the list of moves built since 0106 with sizes (about 254 million with inverses: 0159, 0164-0167, 0158, 0162, 0184, 0190), each after a one-to-one substitution: no route survives on K4 or 10 copies, plants found | 0197, 0198 (before: 0019, 0106) | - |
