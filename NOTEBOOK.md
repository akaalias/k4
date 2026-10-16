# Lab notebook

One entry per working day, newest first. Each entry says what was decided, what was run,
what was found, and what was left open. Experiment numbers link to the records in
`experiments/`. The families table and the clue register hold the bounds; this notebook
holds the reasoning and the mistakes.

## 2026-10-17

F1 continued (ticket #14), after the run that started on 2026-10-16 (0136-0153 are recorded there).

| # | Item | One line |
|---|---|---|
| 154 | F1.8 | **Carter as a running key on one unknown alphabet, exact (rerun of 0153).** Every offset of Carter's book, both directions, three forms, compiled solver (checked against Python on 300 offsets and a planted text): no offset fits K4 or any of 10 copies; 953 of about 1.7 million undecided on K4 (copies 99-20,675). Two unknown alphabets leave 0.1 checks on average (at most 4) for every running-key source sampled: blocked by structure. Prediction held. |
| 155 | F1.9 | **Progressive keys on a million tables.** Per-letter and per-repeat, steps 1-25, periods 1-52, on the 8 sculpture tables and 0109's dictionary keyword alphabets (1,040,314 tables x 2 forms, compiled). Shortest consistent period 25 on K4 (copies 24). K4 above every copper in 4 of 104 cells (periods 34 and 47), null 0-5: chance. Period 34 noted (K4 40 and 20 against copier maxima 10 and 7), not chased. Kryha's step 3 at 31-52 included. Prediction held. |
| 156 | F1.10 | **Friedman's key-advance schedules, exact, with copies.** Run length by letter value (A=1, A=0), CHRISTMAS expansion, EXTINGUISHER windows 2-5, each with every dictionary word on 12 tables x 2 numberings: no word fits K4 or any copy. Ciphertext interruptor and fraction digits (key letters free): no consistent setting on K4 (copies 0-14). Plaintext interruptor inside the known runs: K4 160, copies 120-7,165. Closed. Prediction held. |
| 157 | F1.11 | **Split key phrase (EMC par. 59d).** 29,880 phrases (pairs of puzzle words; runs of 2-4 K1-K3 words split at each boundary): part one mixes the plain alphabet, part two the cipher alphabet, the whole phrase the key; 3 numberings x 3 rules. Best 7 of 24 on K4, copies 7-8; no full hit anywhere. Closed. Prediction held. **Every F1 item is now closed or blocked.** |

### F6 again (after pivot P7, ticket #13)

| # | Item | One line |
|---|---|---|
| 158 | F6.3b | **Mixed triples at wide widths, exact.** Every triple of the four column readings with a width of 25-96 (63 reading triples), forward and inverse: 105.5 million distinct routes in 209 s (compiled counter, checked against Python). Shortest consistent key on K4 18 after the move (copies 19), 24 before (copies 17); K4 above every copper in 3 of 52 cells, null 0-3: chance. One setting at 18 (rows of 93 read down, then rows of 65 and 84 turned) on the KRYPTOS table, Beaufort form: noted. Prediction held. |
| 159 | F6.5 | **Compass directions as reading routes, exact.** Rows of every width read along each of the 16 compass points (lines either order) and E/ENE/NE in two stages: 110,820 distinct routes, then or before a periodic key. Shortest consistent key 21 after, 25 before, as on the copies; K4 above every copper in 1 of 52 cells, null 0-1. Closed. Prediction held. |
| 160 | F6.6 | **Move, change, move, exact.** 844 distinct moves (column readings at every width, K3's rule at every multiplier, both directions), every ordered pair (712,336), a repeating key 1-26 on the sculpture's tables between them, compiled (11 s). Shortest consistent key 20 on K4 (copies 18); K4 above every copper in 1 of 26 cells, null 0-2. Closed for this library; the full type-1 library squared (776 million pairs) not run. Prediction held. |
| 161 | F6.7 | **Two keyed stages on different tables round a move, exact.** Standard then KRYPTOS or the reverse, keys 2-14 each, 844 moves; each known letter ties a slot of one key to a slot of the other one to one, so propagation decides it. Consistent with 5+ checks: K4 388, copies 300-504; every check level inside. Closed. The two stages' signs make no difference (a free key absorbs them): counts are four-fold. The best K4 setting has 9 checks (inverted two-row turn at width 84, both keys 13); the record kept copies only to 8 checks, so not measured: noted. Prediction held. |
| 162 | F6.8 | **Three stages with a keyword columnar, exact.** 131 distinct keyword columnars (puzzle and K1-K3 words, true key order) and 92 plain readings (widths 2-24); every triple with at least one keyword stage, both directions: 20.4 million routes in 40 s (compiled). Shortest consistent key 20 after, 24 before, as on the copies; K4 above every copper in 0 of 52 cells. Closed. Prediction held. |
| 163 | F6.9 | **Both autokeys with the width-7 double columnars, exact.** 0084's routes (5,040 width-7 orders x 163 plain or word columnars, either first, both directions: 3.3 million) with ciphertext or plaintext autokey at every lag, after or before the move, on the sculpture's tables: survivors with 5+ checks K4 0, 9, 1, 0 against copies 0-8, 5-21, 0-1, 0-480. Closed. Prediction held. |
| 164 | F6.11, F6.16, F6.17 | **Keyword-shaped transpositions from the manuals, exact.** 163,720 keywords (dictionary and puzzle words, one per numbering): Rijmenants's disrupted columnar (327k routes), TM 32-220's triangle under 19 columns (655k), interrupted-key columnar by numbering or 1/d digits (333k), trapezoid either side (90k), then or before a periodic key. Shortest consistent keys 23-26 on K4, 21-24 on copies; K4 above every copper in 0-1 cells per item, nulls up to 2-4. All closed. Prediction held. |
| 165 | F6.10, F6.18, F6.19 | **Keyed blanks, row reshuffles, French diagonal, exact.** Blank cells under the first or last key numbers in the last or first row (1.45 million routes), letters reshuffled within rows at widths 2-48 (362k; K1-K3 windows for 25-48), and the French diagonal with key-named diagonals first (2.26 million), then or before a periodic key: shortest consistent keys 21-22 after, 24-25 before, as the copies; K4 above every copper in 0-2 cells, nulls up to 2-3. Closed. Prediction held. |
| 166 | F6.12, F6.13, F6.15 | **EVA, Chiffre XIII, YAR, exact.** EVA's double triangle under one 19-letter numbering (1,920 keys): no key up to 26 fits after the move, 25 before, as on copies. Chiffre XIII as a parametric family (the source does not give rows 2 and 4's rule, so every split and shift; 2.25 million masks from 24-31-letter K1-K3 windows and puzzle phrases), then its published period-5 substitution on an unknown mixed alphabet, decided exactly: no mask consistent with 3+ checks on K4 or any copy. YAR's "1-2-3" as counting-off orders (1-2-3 and 4-5-7, every order): nothing below 26. All closed. Prediction held. |
| 167 | F6.14 | **Nihilist transposition, exact.** 10 x 10 square, three blanks at each of eight places, one key of every order (10!) for rows and columns, read by rows or columns, both directions: 116 million routes in 226 s (compiled; builder checked against Python). Shortest consistent key 20 after, 24 before (copies 18, 17); K4 above every copper in 0 of 52 cells. Closed. Prediction held. **Every F6 item is now closed or blocked.** |

### F12, Stein's way (after pivot P8, ticket #53)

F12.1 blocked without a run: no image of the copper's K4 section at letter resolution is in the repository (Panel4Grid is a blurred video frame of a worksheet; the Blender model needs Blender); the NYT 2010 typeset clue agrees with the transcription at all 97 places.

| # | Item | One line |
|---|---|---|
| 168 | F12.2 | **K4 measured, 71 statistics against 1,000 shuffles.** Letter counts across 8 segmentations, I.C. at 1-48 alphabets, repeats at widths 7, 21, 31: nothing outside every shuffle (0.14 expected by chance). Smallest p: the width-7 doublet column 0.002, the width-21 repeated vertical bigrams 0.004 (0056's fingerprints), width-7 same-letter vertical repeats 0.008 (the NSA's "interval 7"). No segment break, no I.C. peak. Closed, no new item. Prediction held. |
| 169 | F12.3 | **Stein's peak at 13 alphabets.** Against 10,000 shuffles within each part's key columns: K1 p 0.0075 (local peak 0.0046), Part II p 0.24 (0.048), all of K2 0.09, K1 plaintext 0.86, K4 0.21 (0168). After the run, a look-elsewhere check over Stein's 12 non-key alphabet counts gives K1 p about 0.019. A marginal coincidence in K1 that does not replicate where he saw it again; closed as chance. **Prediction failed for K1** (expected above 0.05). |
| 170 | F12.4 | **A pencil session.** K4 written at widths 7, 8, 13, 14, 21, 24, 31 and looked at; six patterns noted by eye before testing: K in two adjacent width-7 columns (7 of 8, p 0.004), five S's within 12 places (p 0.004), ten repeated bigrams (0.04), their spacings divisible by 4 (0.02), K four times in one column (0.20), U three times two apart (0.20). Nothing outside every shuffle; the two strongest were picked by eye. Closed, no new item. Prediction held. |
| 171 | F12.5 | **Two parts, two keys.** Split between the runs (no break found): each run checks only its own part's key, lengths up to 12 and 10. No length live on K4 in either part on the sculpture's tables (copies 0-1). Closed. Prediction held. |
| 172 | F12.6 | **Probable words in the undecided cells, exact.** 60 words (common English, K1-K3 plaintext words, BERLIN, CLOCK, NORTH...) at every compatible place, 3,634 placements per text, in the ten settings the 24 letters leave open (one alphabet, Beaufort 23 and 26; two alphabets at 8, 13, 16, 19, 20, 23, 24, 26), each decided exactly, K4 and 10 kept-place copies per setting. Share of placements still fitting: K4 0.16-0.77, inside the copies' spread everywhere but two alphabets at 24 (0.71 vs 0.70); cells where a text tops all others: K4 1, copies 0-3. Chance; the 26 setting ran out of time part-way (shares compared). Closed. Prediction held. |

F12.7 closed by subsumption without a run: Stein's column method (every shift of each column, scored by letter frequencies, then a crib) finds periodic keys on a known table; the exact sweeps of 0005 test every such key on the standard and KRYPTOS tables against the 24 letters, and the lengths they leave live (27-29, 53 up) were shown to fit coppers equally (0034). F12 is finished: F12.1 blocked, F12.2-F12.7 closed. Pivot P9 to F3.

### F3 two-part key with a combiner (after pivot P9, ticket #16)

| # | Item | One line |
|---|---|---|
| 173 | F3.1 | **Scheidt's patent sandwich, exact.** c = T2[s2 T1[s1 T0[p] + a] + b], each table standard, KRYPTOS or its inverse, signs both ways (108 classes), keys a and b of length 1-13 each. Each known place ties a slot of a to a slot of b one-to-one; 26 trials decide each group of slots. 161 of 169 length pairs give 4 or more checks: nothing fits K4 there (copies fit at most 2 settings in 1,000, from those pairs' 72 new classes x 20 copies). The 8 pairs with both keys 10-13 long leave 1-2 checks; K4 fits as often as copies there (1+ checks: K4 182, copies 186-213). Three planted texts fit their own cell and decrypt in full. (The per-pair copper rate was measured after the run, with the same code.) Closed; long pairs blocked (too few checks). Prediction held. |

## 2026-10-16

Family F1 under the fixed order of work (order-of-work.md, issue #29), items F1.1 to F1.4, ticket #14.

| # | Item | One line |
|---|---|---|
| 119 | F1.1 | **One free alphabet on both sides, exact.** Every key length 1-26, any of 26! orders, decided exactly by algebra mod 13 and mod 2 with an exhaustive search of the mod-13 solutions: in the added form (Quagmire III proper, and variant Beaufort) no alphabet fits at any length; in the Beaufort form only 23 and 26 fit (7 and 1 checks left). Coppers fit at 0-15 and 1-11 lengths; K4 is at the low end of their range, not outside it. **Prediction failed:** it expected most lengths from 8 up to fit. |
| 120 | F1.1 | **The two surviving lengths, climbed.** One free alphabet, Beaufort form, key lengths 23 and 26: the alphabet and free key values annealed toward English with the 24 known letters held, 20 restarts x 200,000 moves per text. K4 -5.81 at 23 (12 coppers -5.90 to -5.45, K4 below 10 of them) and -5.29 at 26 (-5.33 to -5.01): inside the range. Power: hidden English beat every copper in 3 of 6 trials at 23 and 1 of 6 at 26, and was never recovered (true scores -4.0 to -4.4; the climb got 32-43 letters right, 24 of them given). **Prediction failed on power** (expected 4 and 3 of 6). |
| 121, 122 | F1.2 | **Errors.** The Quagmire IV run crashed writing K4's witness alphabets (letter numbers joined as text); I re-ran without reading the traceback and got the same crash a second time. Both records are kept as errors; fixed and smoke-tested before 0123. |
| 123 | F1.2 | **Two free alphabets, exact.** Any pair of orders (plain and cipher), key lengths 1-26, decided exactly (0119's method, two independent alphabets; the Beaufort form is the same family): K4 fits only at 8, 13, 16, 19, 20, 23, 24, 26. Power stated before the run as the share of 100 coppers rejected per length: 1.0 at 1-5 and 9, 0.6-0.9 at 6-8 and 10, 0.25-0.5 at most lengths 11-24, 0.01 at 26. K4's 8 fitting lengths sit inside the coppers' 5-16. **One cell outside the range:** length 19, where 3 of 100 coppers fit; the queue stopped for 0124. |
| 124 | F1.2 | **Replication of length 19.** 26 of 1,000 fresh coppers fit at 19 (p 0.026); the look-elsewhere p, by the statistic set before the run, is also 0.026, above the 0.01 set to stop; lengths 15 and 17 are as rare (0.028). The mechanism is the known letters: at 19 the known places pair 38 apart and 28 and 66 are both R under P, a check that holds for free; copies keeping the 24 known places' carved letters give K4's verdict every time (200 of 200). Not a signal; queue resumed. **Prediction failed in degree** (expected corrected p above 0.2). |
| 125 | F1.3 | **Forced key as running English, every dictionary table.** The 13 + 11 key letters forced at the known places, under 208,062 keyword alphabets x 3 sides x 3 rules x 2 key alphabets (3.7 million readings per text): K4's best -4.94 ranks 18 of 51 among 50 coppers (-5.28 to -4.30). Twenty planted running keys from Carter score their true windows, -3.82 to -4.78, all above K4; 11 of 20 beat every copper (one copper at -4.30 sets the bar). Closed, sampled at stated power. **Prediction failed on power** (expected fewer than half; noise peaked lower than guessed). |
| 126 | F1.4 | **Hand key schedules, listed then tested; run cut short.** List (below) written first. The run hit its 30-minute budget inside the skip rule: B was tested in part (coverage not recorded) and C-F not at all, though the record shows zeros for them; the tableau rows as keys (A) reproduce 6 of 24 known letters, against 6, 6, 5 on three coppers. In the part done, skip with two free alphabets gave K4 461 consistent settings against 305-449 on ten coppers: replicated in 0127. |
| 127 | F1.4 | **Skip rule replicated, complete.** All 3,729 groupings, 30 fresh coppers: two free alphabets K4 1,135 against 681-1,300 (rank 6 of 31); one free alphabet 373 (B) and 120 (V), inside; standard/KRYPTOS tables 0. The only count K4 leads is settings that put 28 and 66 (R under P) in one slot, by construction. Prediction held. |
| 128 | F1.4 | **The rest of the list.** Stutter, back and forth, triangle and square steps, restart at each carved line (1,325 groupings) on K4 and 30 coppers: no setting fits K4 on the standard or KRYPTOS tables; on free alphabets every cell inside the coppers' range except back-and-forth in the added form, where K4 is low (1 against 2-161, the self-encryption effect of 0119); tableau rows as keys 6 of 24 against 5-8. Prediction held. |

Paragraph on 0126-0128 (F1.4). The list of hand key schedules, written before the tests. From C20 'layer two':
(c) the second plate as a running key, already done with the sculpture's texts (0017, 0090, 0117); (d) the tableau's
row two, taken as every carved tableau row used as a repeating key (A); (e) K5 as key, blocked (no text). Hand rules
for a key word W of unknown letters: (B) skip one letter of W every m letters; (C) use each letter r times; (D) W
forward then backward; (E) step through W by triangle or square numbers; (F) restart W at each carved line of the
plate. Already covered: the Berlin clock (0079), Carter dates (0038), progressive per repeat (0011, 0042), restart at
each word (0101), autokeys, a shift per carved line plus a word (0088). Every rule on the list is dead on the standard
and KRYPTOS tables. On free alphabets the rules leave consistent settings at the coppers' rate, which by 0120 no climb
can tell apart, so that residue is blocked like F1.2's.

Mistakes in 0126: I estimated the run from K4 alone, where the decider takes about 1 ms. On a few copper groupings
it ran to its million-node limit, the clock check broke out of each rule's loop, and the record shows zeros for four
rules it never tested, without recording coverage. 0127 and 0128 lowered the node limit, counted undecided cases,
recorded coverage and ran texts in parallel. Lesson: record coverage in the bounds whenever a loop can stop on the clock.

Paragraph on 0123-0124 (F1.2). Two free alphabets are closed exactly at 18 of the 26 lengths. At the eight that
stay consistent (8, 13, 16, 19, 20, 23, 24, 26) nothing cheaper than an English climb remains, and 0120 showed a climb
on one free alphabet already has weak power at 23 and none at 26; two alphabets add 25 free places, so a climb here
would be weaker still. Recorded blocked, not run. Length 19 was the one result outside the coppers (3 of 100); against
1,000 fresh coppers it is about 1 in 40, and the look-elsewhere statistic I chose was generous to K4 (lengths 15 and 17
are as rare but missed the cut by one copper), so the honest reading is p of a few percent, like 0102's period-3 cell.
It rests on one coincidence in the known letters (R under P at 28 and at 66, 38 apart), which any key repeating every
19 or 38 letters would produce, but which also happens by chance once in 26 tries. Noted in the tree, not chased.

Paragraph on 0120. The climb cannot find a planted answer at these lengths. In dry runs before the run (recorded in
the record's hypothesis) it could not even return to the true alphabet from two swaps away: one swap moves letters in
every slot and changes the forced key values with them, so the landscape is close to random. The pre-registered
"found" criterion (a plant's climbed score above every copper) measures detection, not recovery, and at 23 it was met
3 times in 6 only because English under the cipher climbs a little better than shuffled letters, not because the text
came back. So length 23 is a weak test, about even odds of noticing a true Beaufort-23 message, with K4 near the bottom
of its coppers; length 26 (one check) cannot be decided by any climb this size. Also found while preparing the run:
the harness drops the attack's `controls` list (`_runner.py` never copies it), so the shuffled-copper gate reports
"controls 0" for every candidate; filed as #45, not worked around.

Paragraph on 0119. The added form dies for a reason one can check by hand: S sits under S at 33 and K under K at
74, and with one alphabet on both sides and the key added, a letter that encrypts to itself needs key 0 in its slot.
At every key length from 1 to 26 another known letter shares the slot of 33 or 74 and is not its own carved letter,
so that slot would need key 0 and a non-zero key at once. This is new for free alphabets (0097 tested only lengths 3,
7 and 21, by a relaxation that can refute but not confirm). The first exact solver, a plain search with propagation,
blew up on the dead lengths (product of independent choices); it was replaced before the run by linear algebra mod
13 and mod 2 with an exhaustive search of the mod-13 solutions, and cross-checked on 40 coppers against the plain
search (no fit it found was called dead). The prediction, written before the solver existed, guessed "fewer checks
than free places, so most lengths fit"; it ignored that a one-to-one alphabet packs about 20 letters into 13 residue
classes mod 13, which the known letters make tight.

### F6: a move, then the table (after pivot P5, ticket #13)

F1.1 blocked first: its last cells (Beaufort 23 and 26) can only be judged by an English climb, which 0120 showed
recovers no planted text at that size, so the item was marked blocked rather than tested weakly. Every F1 item is
closed or blocked; pivot P5 to F6, ranking unchanged.

| # | Item | One line |
|---|---|---|
| 129 | F6.1 | **One free alphabet after every move, exact (order A).** 27,852 type-1 moves x key lengths 1-26 x added and Beaufort forms, 0119's decider (38 undecided of about 390,000 settings): no fit below length 6, 3 settings at 6, 64 at 7. On 800 sampled moves K4 is above all 12 coppers in 7 of 52 cells; each copper against the rest 0-8. Chance. Prediction held (it said 1-5 dead; the first fits came at 6). |
| 130 | F6.1 | **The same, order B (table, then move).** 78 undecided of about 500,000. No fit below 6; length 9 dead for every move and 15, 17, 19 nearly so, because with the table first the slots are the message places. K4 above every copper in 0 of 52 cells, null 0-10. Chance. Prediction held. F6.1 closed where dead, blocked where it fits at the coppers' rate. |
| 131 | F6.2 | **Two free alphabets after every move, exact at every length: incomplete.** The run hit its 30-minute budget after 10,625 of 27,852 moves on K4 and finished no copper comparison, so it has no verdict and the item stays open. On the part done: fits from key length 3 (6 moves), and at 26, 7,072 of 7,152 settings passing the per-slot test fit. |
| 132 | F6.2 | **Second attempt, exact at 1-10 and the per-slot test above: incomplete again.** No move was finished for every text, so again no verdict. Measured afterwards: the search has a heavy tail even at short keys (a few settings per thousand ran to 200,000 nodes, up to 21 s each), and the 300-move long-key sample shared the workers. Left behind: on 64 sampled K4 moves, 97-98% of settings passing the per-slot test at 11-26 fit. |
| 133 | F6.2 | **Third attempt, complete.** Every move, both orders, K4 and 10 coppers; exact at key lengths 1-10 with the search capped at 2,000 nodes (undecided 220-302 per text, K4 249, so even), per-slot test at 11-26. No pair of alphabets fits at 1-2 in either order or at 3 with the table first; first fits at 3 (move first, 16 moves) and 4 (table first, 3). K4 above every copper in 5 of 52 cells, each copper against the rest 2-7: chance. F6.2 blocked like F1.2. Prediction held. |
| 134 | F6.3 | **Mixed matrix stages, two and three, exact.** Each stage writes rows and reads the columns one of four ways (clockwise turn, anticlockwise turn, Sanborn's rows-then-columns-down, its reverse): every pair at widths 2-96, every triple at 2-24 (all-clockwise triples were 0083), forward and inverse, 1,762,597 routes, then or before a periodic key 1-26 on the standard or KRYPTOS tables. Nothing live below 20 on K4 (one copper had a setting at 17); K4 above every copper in 2 of 52 cells (period 26, by 0.03%), null 0-2. Chance. Prediction held. F6.3 closed at those widths. |
| 135 | F6.4 | **Hand padding at every grid stage, exact.** The list above: blanks in eight places per grid, dropped or carried as dummies into the second grid; one grid (4 readings, widths 2-96) or two (turn or Sanborn's matrix, widths 2-48); 874,572 distinct routes, then or before a periodic key 1-26 on the standard or KRYPTOS tables. Nothing live below 21 on K4 (coppers reach 20); K4 above every copper in 0 of 52 cells, null 0-2. Chance. Prediction held. F6.4 closed. **Every F6 item is now closed or blocked: STOP_AFTER F6 reached.** |

List for F6.4, written before 0135 ran: the hand ways of padding a grid of 97 letters, per stage. Where the h w - 97
blank cells go: P1 end of the last row (the usual ragged grid, 0008, 0083); P2 start of the first row (0082); P3 start
of the last row; P4 end of the first row; P5/P6 down the last column from the top or the bottom; P7/P8 down the first
column from the top or the bottom (only when there are no more blanks than rows). Between two grids the blanks either
vanish (drop: the second grid gets 97 letters again) or are copied out as dummy letters and struck out at the very end
(keep: the second grid gets h w symbols). Completing the grid with nulls that stay in the carved text is not on the list,
because 97 is prime and every rectangle would leave nulls among the 97 carved letters, which the known places rule out
only case by case; the "?" as the 98th cell is 0086.

Paragraph on 0133. The cell that keeps coming back: two unknown alphabets, the move first, key length 3. 0097 (by a
relaxation), 0100 (50 fresh coppers) and now 0133 (exact, 10 more) all put K4 at or above the top of its coppers there
(16 moves here against 1-12). These are not three independent replications of a signal: K4's count is the same
object each time and only the coppers are fresh, and the cell was first picked out of 52 by looking. 0102 measured it
against 400 shuffles at p 0.043 and against 400 copies keeping the width-21 columns at p 0.10. By the rule fixed before
this run (K4's count of cells above every copper against each copper's count against the rest) it is inside chance,
so the queue did not stop. Recorded as the most persistent marginal cell in F6, not chased.

Mistake in 0131. I timed the two-alphabet decider on 60 moves while 0130 was running and read 0.46 s per move as
"about 0.2 s unloaded", then sized the run on that. The cost is not spread evenly: lengths 1-10 take about 3 ms per
move, 11 and 12 about 0.2 s, and the long lengths more, with rare 60-second searches at the node limit. The workers
stopped on the clock with the coppers' share of moves barely started, and the comparison needs moves done for every
text, so it came out empty. Lesson: time each part of the parameter range separately, unloaded, before sizing a run,
and make the comparison robust to a short run. 0132 repeated the mistake in a new form: I timed 60 K4 moves, saw a mean of 1.2 s on the long sample, and did not look at the shuffled texts' tail at short keys, where one setting in a few hundred costs seconds. 0133 caps the search at 2,000 nodes (undecided counted per text) and groups each move's eleven texts in one worker, so a cut-off still leaves whole moves to compare.

Paragraph on 0129-0130. 0129 and 0130 are one test split in two, because both orders did not fit one 30-minute
budget: the exact decider costs about 7 ms per fitting setting and most settings from length 10 up fit. A random
witness hunt before the search, meant to speed up fits, made them slower (300 failed tries cost more than the search
saved); numpy is not in the environment, so it was dropped rather than vectorised. The comparison with coppers uses a
statistic fixed before the run: the number of cells where K4 is above every copper, against the same count for each
copper against the rest (so a copper's luck sets the bar, not a guessed threshold).

### F1.5, then every family through F9 (after pivot P6, ticket #14 and the family tickets)

| # | Item | One line |
|---|---|---|
| 136 | F1.5 | **Step 1, the bound.** Each blocked cell's key, in bits (symmetries removed), less the 112.8 bits the 24 known letters fix, against what 73 letters of English carry: the harness's quadgram scorer loses 2.92 bits per letter on held-out English (Carter; 2.94 on K1-K3), so it extracts 1.78 bits per letter, 130 bits in all; Shannon's estimates allow 227 or at most 290. One free alphabet (F1.1 at 23 and 26, F6.1 at every length), two free alphabets to length 16 (14 with a move), Hill 5x5 affine and 4x4 with any key: decidable by quadgrams in principle. Two alphabets from 19 (15 with a move) and plaintext autokey lags 53-84: only with a better English model. Autokey lags 85-96: no English test can; blocked for good. Prediction held (it put the last cut at 86). |
| 137 | F1.5 | **Design 1: a climb that never breaks the known letters, in compiled C.** One free alphabet, Beaufort form; every move keeps the seven checks (swap, then repair with a second swap); whole text scored in context; 1,000 restarts x 100,000 moves per text, about 150 times 0120's speed. L23: plants above every K4 copper 10 of 12 (bar 9), K4 rank 9 of 13; L26: 5 of 12, K4 rank 12 of 13. No plant recovered (31-45 letters right). Looked like a pass at 23, pending 0138. |
| 138 | F1.5 | **Design 1 checked against each plant's own copies.** 12 new plants at 23, each against 6 fitting shuffles of itself: 6 of 12 beat all their own copies (luck 1.7, bar 9), but 11 of 12 beat K4's copies. **Design 1 fails;** 0137's power came mostly from the plants' letters differing from K4's. **Prediction failed** (expected 9+). F1.1 Beaufort 23 back to blocked. |
| 139 | F1.5 | **Design 2: parallel tempering.** 16 replicas (T 0.1 to 0.002) exchanging states, the same check-keeping moves, equal compute (10^8 moves per text). 8 plants at 23, each against 6 fitting shuffles of itself: 6 of 8 beat all their own copies (luck 1.1, bar 6). **Passes. Prediction failed** (expected a fail). Still no plant recovered (34-42 letters right). Mistake: the record's "family" and "bar" strings were left as 0138's ("design 1"); the search line is right. |
| 140 | F1.1 | **K4 decided at 23 with design 2.** K4 against 12 fitting shuffles of itself: -4.99, rank 9 of 13 (-5.14 to -4.83). F1.1 Beaufort 23 closed, sampled at power about 0.75 (0139). Design 2's power at 26: 5 of 6 plants beat all their own copies (bar 5) -- **prediction failed** (expected no power with one check). |
| 141 | F1.1, F1.2 | **Error.** K4 at 26 plus two-alphabet power in one run: drawing fully shuffled copies that fit two free alphabets needs 0123's exact decider, minutes per shuffle; the searches hit the deadline, a text with no finished run broke the summary, no result kept. Mistake: I timed the search, not the control generation. |
| 142 | F1.1 | **K4 decided at 26.** K4 -4.99 ranks 12 of 13 among 12 fitting shuffles of itself (-5.05 to -4.69). F1.1 Beaufort 26 closed, sampled at power 5 of 6 (0140). Prediction held. Both F1.1 cells closed. |
| 143 | F1.2 | **Design 2 on two free alphabets, power.** Controls changed for cost: copies keep the carved letters at the 24 known places and shuffle the other 73 (they fit by construction; the exact two-alphabet decider takes minutes per full shuffle). L13: 5 of 5 plants beat all 5 own copies; L16: 4 of 5 (bar 4, luck 0.83). **L8 incomplete**: jobs sorted longest key first, the L8 texts ran last and 27 finished no run before the deadline. Prediction failed in shape (expected 8 strongest, 13 and 16 weak). Mistake: ordering jobs so one cell can be starved; a cell must get its full effort or be dropped from the pre-registered bar. |
| 144 | F1.2 | **K4 decided at 13 and 16 (two free alphabets).** Against 12 kept-place copies of itself: rank 13 of 13 at 13 (-5.12), 7 of 13 at 16 (-4.67). Closed, sampled at 0143's power (5/5, 4/5). Prediction held. |
| 145 | F1.2 | **Two-alphabet power at 8, rerun alone.** 4 plants x 4 kept-place copies, every run finished: 4 of 4 beat all their copies (bar 3, luck 0.8). Prediction held. |
| 146 | F1.2 | **K4 decided at 8 (two free alphabets).** Against 12 kept-place copies: -5.34, rank 2 of 13 (-5.72 to -5.23). Closed, sampled at power 4/4 (0145). Prediction held. F1.5 done: the bound (0136), a decider with measured power (0139, 0140, 0143, 0145), and every F1.1/F1.2 cell under the bound decided: K4 inside its own copies each time. |
| 147 | F1.6 | **One carved letter wrong, exact.** 604 variants per text: each of the 24 carved letters at the known places changed to each other letter, and one letter missing or extra between the runs, read two ways (an error outside the runs moves all known places together and changes no periodic check, so the item's ~150 places reduce to these). One alphabet (added, Beaufort), two alphabets, lengths 1-26, exact. K4 above every copper in 2 of 78 cells (1V:19, 2:19), null 0-11: chance. K1 and K2's own system revives on K4 at length 19 when the S at 33 is changed (25 of the 25 replacement letters), the cell carried to 0148. Prediction held. |
| 148 | F1.6 | **The revived cell judged.** K1 and K2's system (one free alphabet, added form), length 19, place 33's carved letter taken as a slip. Design 2 in the added form: power 3 of 5 plants beat all 4 copies (bar 4) -- fails, so the cell stays blocked as a weak test; K4 7 of 13 among its copies. One planted text was read back exactly (97 of 97): the first full recovery in the project, with 8 checks left after dropping place 33. **Prediction failed** (expected power). Mistake: the record's hypothesis says "4 checks"; it is 8 (23 equations over 15 slots). |
| 149 | F1.7 | **Autokey on one unknown alphabet, no move, exact.** Ciphertext and plaintext autokey, three forms, every lag with equations, propagation solver over the 26 places (checked on planted texts). K4 fits at 9-23 lags per kind and form, the copies at 3-30; rare fits 4 against 0-27: chance. Dead lags closed; fitting ones blocked by cost (English decider about an hour per cell); the move-first version blocked by cost too. Prediction held. |
| 150 | F1.6 | **One-letter errors through free-alphabet Gromark, exact.** 605 variants (600 substitutions at the known places, known places shifted by one, all or BERLINCLOCK alone: a Gromark key depends on absolute position) through 0069, 0076 and 0107 unchanged, 181 rule/base settings x 4 forms: no fit. Prediction held. |
| 151 | F1.6 | **One-letter errors anywhere through Hill and trifid, exact.** 5,044 variants of K4 (every place changed, deleted, or with each letter inserted): no trifid cube under any; Hill alive with a check in 257 (variant, setting) pairs, nearly all 5x5 plain with one check; 70,218 settings open (5x5 affine). Coppers in 0152. |
| 152 | F1.6 | **Hill controls.** The same 5,044 variants of 10 scrambled copies: alive-with-check totals 30-6,384, all 5x5 plain; K4's 257 ranks 4 of 11. Chance. F1.6 complete. Prediction held. |
| 153 | F1.8 | **Error (timeout).** Carter as a running key on one unknown alphabet: the compiled first pass finished, but the second pass on undecided offsets (node limit 400,000) had no clock check and two workers ran past the budget; the harness killed the run at 1,860 s. Mistake, the third of its kind (0025, 0126): every loop that can run long must check the clock. Rerun as 0154. |

Paragraph on 0137-0138. 0137 looked like the first decider with power: ten planted texts in twelve climbed above every scrambled copy of K4. Reading the result, I saw the comparison was unfair. A planted ciphertext differs from K4 in its letters, not only their order (index of coincidence 0.039 against K4's 0.036; shuffles of a plant fit length 23 43% of the time, shuffles of K4 rarely), and the climb rewards those letters. 0138 compared each plant only with shuffles of itself: 6 of 12, against 11 of 12 for the same plants versus K4's copies. The climb does read some English order (6 against the 1.7 luck gives), but at even odds, and never gets a planted text back. Mistake: 0120's bar, which 0137 kept, compares plants with the target's copies; power must be measured against each plant's own copies. 0120's 3 of 6 has the same flaw. Lesson: a power test compares like with like, changing only the property the decider is meant to read.

Paragraph on 0136 and step 2. The bound says which cells a decider could judge, not whether a search can find the key. Before designing step 2 I measured the landscape on planted Beaufort-23 texts (scratch, not a record): the true alphabet scores -4.26 to -4.41 on the full text, one swap away averages -5.2, the level 0120's climb reached from random starts. But a climb that keeps the known letters consistent at every step (swap two letters, repair with a second swap if a check breaks) returns to the exact plaintext from up to about 12 such swaps, and rarely from 15-20; 0120's "cannot return from two swaps" came from its penalty, not from the cell. A random alphabet is about 24 swaps away, so the question for design 1 is the success rate per restart.

## 2026-10-15

Plan for the day: run to experiment 50. Priorities, in order: explain the three statistics
no generator reproduces (the width-7 doublet column, the eleven width-21 vertical repeats,
Bean's closeness), then the untouched families (2 masking, 4 visual), then the one-letter
error reruns of the strongest sweeps. Every diagnostic experiment gets ten or more shuffled
controls. The notebook gets a line per experiment as it lands.

Lesson from 0025: every sweep must check the clock inside its innermost loop that can run long; the harness budget is advisory, not a kill switch.

From 0037: a diagnostic's controls must run at the same trial count as the real search. The record's two controls used 6,000 triples against 200,000, which made a chance result look like a lead; thirteen full-size shuffles put it back inside the noise.

From 0027: the width-7 doublet column is reproduced by nothing, random letters included, so it is either a fluke of about one in 300 or the trace of a construction outside everything simulated. Doublets at 19, 26, 33, 47, 68 are all 5 mod 7; in a period-7 additive system a doublet is a plaintext digraph with a fixed letter difference falling in one column, which is a natural mechanism, but period 7 is dead under every alphabet by the cribs alone (R and C both to P at 66 and 73). Gromark base 2 reproduces the width-21 repeats; 0013 tested only bases 10 and 26, so bases 2 to 9 are 0028.

From 0033: simulated annealing over trifid cubes with crib hits, even at coordinate level, plateaus at about 17 of 24 on a planted cube. A proper trifid solver needs constraint propagation on the cube coordinates, not local search. Built as 0039 and 0040: the equalities plus the all-different rule leave no cube at all for K4, while planted texts are recovered. The lesson generalises: when a cipher's key is a structure the cribs constrain algebraically, solve, do not search.

From 0034: the loss function's key-cost term is too weak. A 95-letter random key with 71 free slots climbed to fit English gives a crib-perfect text that the harness scores at loss 4.4, below the crib gate, and keeps as champion. The text is overfitting, as the identical score on shuffled K4 shows. Per program.md the ruler is not changed mid-run: the case is in issue #11 for a human decision, and the champion stands as a warning until then. Also: the key alphabet does not affect decryption under a fixed plain and cipher alphabet, so the 24 conventions were 8 distinct classes here; the extra 16 were wasted time.

| # | Family | One line |
|---|---|---|
| 21 | 1 | Carter's book as a running key, 13.7 million offsets and conventions: none within two mismatches. |
| 22 | 1 | Porta over 248 alphabet orders: no order separates all 24 crib pairs across the halves. |
| 23 | 2 | Reversal and null padding before a periodic tableau, 648 masks: smallest live period 26; nothing. |
| 24 | 3 | A word plus the K2 coordinate digits, seven readings: shortest consistent word length 26; nothing. |
| 25 | 1 | Both autokeys with 63 keyword-mixed alphabets, 3.4 million cases: nothing; ran 46 minutes because the sweep ignored the clock. |
| 26 | 6 | Two keyed columnar stages from vocabulary word pairs, 15,376 routes, then the tableau: chance. |
| 27 | 7 | Simulator round two: only Gromark base 2 reproduces the width-21 repeats; nothing reproduces the width-7 doublet column. |
| 28 | 5 | Gromark bases 2-9: every vocabulary alphabet triple forces a shift of 15 or more, so bases up to 15 are dead. Clocks batched, so design and implement times are lost. |
| 29 | 1 | Bean's closeness over all alphabet pairs: smallest largest shift 8, same as shuffled K4. Chance. |
| 30 | 1 | Ciphertext as its own key under every index rule, and the message mirrored as key: nothing. |
| 31 | 1 | Copper off by one letter, 195 variants, through the chained autokey and two-word tests: nothing. |
| 32 | 6 | A grid keyed by row, widths 2-48, 63 alphabets: no width survives. |
| 33 | 4 | Trifid: keyword cubes best 7 of 24; the annealer plateaus at 17 even on a planted cube, so free cubes stay open. |
| 34 | 1 | Key completed by English climb at periods 27-29 and 53-95: K4 behaves exactly like shuffled K4. First gate-passing candidates; the harness kept a gibberish period-95 text as champion at loss 4.4. Scorer case filed. |
| 35 | 1 | Key completion at 27-29 with one vocabulary-mixed alphabet: noise, equal to shuffled K4. Design clock polluted by dashboard work, 19 min of it. |
| 36 | 8 | Bauer's open Hill variants, chained and paired, solved exactly: dead. |
| 37 | 6 | Three grid stages, 200,000 sampled triples: best key -3.61 against thirteen shuffles topping at -3.63. Chance by a whisker; the record's own controls were undersized, fixed after the run. |
| 38 | 3 | A word plus seventeen dates and counts from the story: shortest consistent word 26; nothing. |
| 39 | 4 | Trifid solved exactly: the run found no cube at any setting, then crashed writing its own summary. Record kept as an error. |
| 40 | 4 | Rerun of 39 with the summary fixed: no cube is consistent at any period 2-15, on K4 or on shuffled K4. Trifid dead. |
| 41 | 6, 9 | Spirals, snakes and diagonals at every width, both orders: chance before the table, clashes after a swap. |
| 42 | 1 | Progressive key on vocabulary tables, 8.9 million combinations: periods 1-24 dead at every step; nothing. Test clock includes 8 minutes of dry run. |
| 43 | 3 | Two words in two passes on vocabulary tables: nothing below total length 22; chance above. |
| 44 | 8 | Hill under 126 keyword numberings: 4x4 solutions exist without redundancy and all break the partial-block cribs. Dead. |
| 45 | 1 | K1-K3 as running keys on vocabulary tables, 147 million trials: nothing within two mismatches. |
| 46 | 5 | Gromark three-term rules, lags to 13, bases 16-26: nothing. |
| 47 | 1 | Carter and the sculpture texts as running keys with one mixed alphabet, 858 million trials: nothing. |
| 48 | 1 | Both alphabets mixed, key completion at 27-29, every pair reached: noise. Family 1 closed for vocabulary alphabets. |
| 49 | 1 | Shaped long keys from two puzzle words, mirrors and doublings, 272 of them under every alphabet pair: nothing. The record overestimated the key count by a hundredfold. |
| 50 | 3 | The copper off by one letter, through the two-word test on vocabulary tables: survivors at the shuffled-copper rate, nothing below total length 21. |
| 51 | 6 | Pure transposition: the cribs need three Es, the copper has two. Every rearrangement-only reading is dead at once. |
| 52 | 8 | Ciphers on a 5x5 square or a 24-letter ring: K4 uses all 26 letters and has odd length, so Playfair, bifid, four-square, ADFGVX and kin are dead whatever the key. The walkthrough misplaces I by one (17, not 16). |
| 53 | 1 | Periodic keys on tables rebuilt from every K1-K3 word and the 2025 letter's words: nothing. Period 26 runs high only because one equation, places 22 and 74, holds across many alphabets at once. |
| 54 | 5 | Gromark on tables rebuilt from K1-K3 words: every pair forces a shift of at least 16, as scrambled coppers do, so base 10 is out again. |
| 55 | 8 | Hill with letters numbered by alphabets from K1-K3 words: no 2x2 or 3x3 setting fits the known blocks; the 4x4 ones fit only for lack of checks and fail the remaining known letters. |
| 56 | 7 | **Prediction failed.** The width-7 doublet column and width-21 repeats survive the look-elsewhere correction: corrected p 0.005 (0.018 given six doublets) and 0.010 against 10,000 shuffles. Two real fingerprints still lack a construction. |
| 57 | 2 | Filler letters chosen by letter: no different from random strike-outs. Striking letters before BERLINCLOCK makes lengths 24-25 consistent at the chance rate, which the prediction did not foresee; their fragments were not word-checked. |
| 58 | 6 | The table, then a column shuffle keyed by K1-K3 words, once or twice: 355,008 route-convention pairs, a handful live at length 25 and no word fits. The prediction missed those 16, and no control measured their chance rate. |
| 59 | 3 | Two secret words in two passes on tables rebuilt from K1-K3 words: nothing below a combined length of 21, survivors above at chance rates, no word. |
| 60 | 8 | The K2 map reference poured into a Hill number table, every reading: at most 4 of 24 known letters, worse than random tables. |
| 61 | 3 | A puzzle word plus the misspelt letters (QUA, LOE) or the raised YAR as a second short key: best 8 of 24 known letters, no better than scrambled coppers. |
| 62 | 7 | Fake coppers by recipes with a 7 or a 21: none makes both marks. Ciphertext autokey at lag 21 makes the width-21 repeats 27 times more often than chance; nothing tried makes the doublet column. |
| 63 | 6 | Column shuffles before or after the self-feeding autokey: 14.2 million exact checks, no fit, best 9 of 24. |
| 64 | 1 | The self-feeding autokey on tables rebuilt from K1-K3 words, every distance: never closer than three wrong known letters, as scrambled coppers manage. |
| 65 | 7 | **Prediction failed in size.** Recipes built to line doublets up in sevens: only ciphertext autokey at lag 1 with a period-7 key raises the doublet column, to 1.5% of samples against 0.1-0.3% by chance, not the 5% predicted; the other six recipes stay at chance. |
| 66 | 1 | The self-feeding autokey plus a repeating secret word on top, every lag and word length, solved exactly: nothing survives with three or more checks; lag 1 with 7 (the doublet recipe) and lag 21 (the repeat recipe) are dead. The record's case count, 294,912, counts lags with no known letter past them; 221,184 were tested. |
| 67 | 1 | **Prediction failed in detail.** Two earlier carved letters as the key, every pair of distances, with or without a short word: 15 cases survive three checks against 3-12 on scrambled coppers, and one survives four (0-2). Listed after the run, the 16 are scattered with no pattern, and distances 1 and 21 never pass more than one check. Chance, but the record's own prediction said none. |
| 68 | 1 | The self-feeding autokey with one carved letter wrong, missing or extra: no variant at any lag passes three checks, lag 21 has no survivor at all, and the counts sit inside the scrambled coppers'. The substitution tally counts the residuals a replacement letter is fitted to as checks, overstating them by one or two. |
| 69 | 5 | Gromark with any scrambled alphabet at all, every rule up to six digits back and every primer: none fits the known letters, and none fits scrambled coppers; a planted Gromark text is found uniquely. Base-10 Gromark is dead whatever the alphabet. The record's primer count has a typo: 5,432,100, not 5,432,200. |
| 70 | 6 | Every row of seven reshuffled the same way, before or after a repeating secret word, all 5,040 orders: periods up to 24 die, 25-26 survive only as often as on scrambled coppers, and no forced fragment holds a word (checked after the run). Family 6 back to rest. |
| 71 | 1 | A table slightly different from the carved one, as Sanborn said his was: all 925 alphabets one swap or one move from KRYPTOS, with a repeating word or the self-feeding autokey: nothing beyond the scrambled-copper rate and no word in 16,671 fragments. The count was corrected from 975 to 925 before the run. |
| 72 | 1 | The 32 compass points and the words of Sanborn's 'what's the point?' letter as table alphabets, with a repeating word, the self-feeding autokey, or both: everything at the scrambled-copper rate, and no word in 10,671 fragments. |
| 73 | 1 | **Prediction failed in detail.** The message as its own key plus a repeating word: twelve cases pass three checks against 0-6 on scrambled coppers, but they are four coincidences counted at nested periods (ROWS and SEVENTY alphabets at lag 8, each at periods 5, 8, 10, 20, 40), none passes four, and the NSA's lag 7 and the fingerprint lag 21 have nothing. Chance. |
| 74 | 2 | Masks that change letters: the alphabet counted in steps of 3, 5, 7 ... or backwards (Atbash), on both alphabets, before or after a repeating word or the self-feeding autokey: nothing at three checks, periods up to 25 dead, no word. A one-check excess in the plain autokey comes from two-equation lags counted per key alphabet. |
| 75 | 2 | The doubled letters as fillers: QQ, SS and TT inside the known stretches each carry two different known letters, so they are real letters; striking out BB, the second SS or ZZ in any combination changes nothing for a repeating word or the self-feeding autokey. |
| 76 | 5 | Gromark with any scrambled alphabet in every base from 2 to 16 and in base 26 (Scheidt's other number systems, the Berlin clock's fives): no starting number fits in any base, on the copper or on scrambled coppers. Family 5 is closed for two-term rules. |
| 77 | 1 | The two fingerprints joined in one recipe, every row of seven reshuffled plus the self-feeding autokey at every distance, both orders, 31 million exact checks: all at the scrambled-copper rate, nothing passes four checks, and distance 21 never passes three. |
| 78 | 1 | Sanborn's own letters as a running key, the 1989 note to CIA staff, the 1991 dedication pages and the 2025 open letter, at every offset both ways: the best gets 9 of 24 known letters, exactly what scrambled coppers get. |
| 79 | 1 | The Berlin clocks as the key, lit lamps or hours or minutes or the digits of the time, the clock moving on a fixed step per letter from every start minute: the best fit agrees at 8 of 24 known letters, as scrambled coppers do. The prediction's guess of 19-20 mismatches was removed before the run, after a dry run on the copper showed 16; the verdict does not depend on it. |
| 80 | 6 | **Type 1, gap a3.** Change with one repeating word, move by K3's rule, a grid turn, two turns or a column shuffle (26,158 distinct routes), change again with a second word, key lengths 2-14 each, solved exactly: 4.4 million structures, nothing with five or more checks, counts at every level at the scrambled-copper rate. **Prediction failed in detail:** at exactly three checks the copper has 30 cases against 33-46 on the scrambled coppers,  
| 81 | 6 | **Type 1, gap a2.** The same 27,752 routes joined to the plaintext autokey (the NSA's 1992 guess) or the ciphertext autokey, both orders, every lag, one alphabet throughout: nothing passes five checks; counts at the scrambled-copper rate. **Prediction failed in detail:** four settings pass exactly four checks (three with the autokey first, against 0-2 on scrambled coppers), scattered over lags 33, 37 and 49 and wide odd turns; chance. | 
| 82 | 6 | **Type 1, gap a1.** Hand-padded grids: blanks at the start of the top row, or the first grid's blanks carried into the second as fillers and struck out at the end, for one and two quarter turns at every width and for short-row-on-top column shuffles (120,871 distinct routes), with a repeating key of length 1-26 before or after: no period below 22 is live on the copper or on any scrambled copper. **Prediction failed in detail:** with the key after the move, period 23 is live 299 times against 229-283 and period 24 2,166 against 1,289-2,160; checked after the run, the 299 are spread evenly over every padding choice and mostly over grids wider than 70, as on the scrambled coppers. Chance. | 
| 83 | 6 | **Type 1, gap a4.** Three quarter turns at every width 2-96 in each grid (1,714,024 distinct routes, forward and inverse), with a repeating key of length 1-26 after or before: counts at every period at the scrambled-copper rate. **Prediction failed in detail:** one setting is live at period 18 (widths 93, 65 and 84, key after the turns, KRYPTOS alphabet, Beaufort; six checks), where no scrambled copper has anything below 21. Examined after the run: the six checks fix all 18 key letters, VTYPETGCEVGYPLDEPG, no word, and the full decryption reads TQPFJTXZBUAKHSSPRGHQP... and scores -8.85, below noise. About 0.1 such coincidences are expected at six checks over 27 million settings; this is one. | 
| 84 | 6 | **Type 2, first open item.** Double column shuffle with one stage seven columns wide in all 5,040 orders, the other plain at widths 2-30 or keyed by a puzzle word (253 sequences), either stage first: 2,548,223 routes, repeating key 1-26 before or after: nothing live below 21; periods 21 (key after) and 24 (key before) live 3 times each against 0-2 on scrambled coppers. Chance. Building it found issue #26: ten records (0006-0081) passed a keyword's rank list as the column reading sequence, so their 'keyed columnar' read the columns in the inverse order; true keyword columnar was untested there. Also, the library's keyword order drops repeated letters (ABSCISSA reads as ABSCI); 0084 reads word keys both with repeats dropped and on the whole word, ties left to right. | 
| 85 | 6 | **Rerun for issue #26.** Column shuffles keyed by the puzzle's words read in true key order (201 sequences: repeats dropped, or the whole word with ties left to right), once in either direction or twice in every ordered pair (40,771 routes), with a repeating key 1-26 before or after and with both autokeys at every lag in both orders: nothing live below 22; nothing passes five checks; three plaintext-autokey settings at exactly four checks (controls up to 12). The keyword bounds of 0006-0081 now hold for both readings. | 
| 86 | 6 | **Type 2, sub-variant 2.** The ? before OBKR as a 98th symbol: grids of 98 cells read from any corner, once or twice, K3's rule mod 98, seven-column shuffles in all orders, each sending the ? to the front (300,651 routes), with a repeating key 1-26 in three placements, and plaintext or ciphertext autokey on the 14,946 full-grid, one-grid, K3-rule and seven-column routes: nothing live below 21, nothing at four checks. **Prediction failed in detail:** plaintext autokey after the move has 72 settings at three checks against at most 37 on the controls. Examined after the run: they are 34 distinct sets of checks, one set of three landing pairs repeated 12 times by different seven-column orders that land the known letters alike; the controls are lumpy the same way (one has 102 at three checks for the ciphertext autokey before the move). Chance; counting distinct check sets would have shown it at once. | 
| 87 | 3 | **Type 2, sub-variant 4.** A key that is one word's letter for the column plus a second key's letter for the row, on a grid of width 2-48: inside a row the row letter cancels, so this makes doublets pile up in one column by design. Solved exactly: on the copper as carved no width survives (width 7 fails with 14 checks; the first loop already gives 17 against 18 on the KRYPTOS alphabet); after or before each of 0080's 27,754 moves, counts at every level at the scrambled-copper rate and nothing at five checks. Prediction held. | 
| 88 | 3 | **Type 2, continued.** The column word with a second shift that changes every m letters (m 2-50, any offset, word length 2-31), the sculpture's own 31-letter carved lines among them (m = 31, offset 27): 31,994 structures, one combination consistent on K4 at a single check, against 0-230 on the scrambled coppers; nothing at two. The carved-line case dies at every word length (with a 7-letter word places 22 and 29 already need 1 and 23). Prediction held. |
| 89 | 4 | **Type 3.** K4's four carved lines laid over every four lines of the tableau plates and the cipher plates, straight across or folded at the centre, shifted up to four columns, 12 conventions (10,800 overlays): best 5 of 24 known letters, scrambled coppers 5-7. The screen's geometry gives no key. |
| 90 | 6 | **Types 1 and 3 crossed.** Running keys concealed at the sculpture (tableau, Morse, the four ciphertexts, K1-K3, Sanborn's letters, Carter's book) joined to every move of the type-1 library (27,852 distinct routes), move before or after the table, 12 conventions, exact: no full match in either order; no source matches even one whole crib stretch; the deepest partial match is 7 checks, as on scrambled coppers (6-7). The record's family slug is misspelt (6-matrix-...); the dashboard maps it. |
| 91 | 6 | **Type 6.** The Berlin clock schedules of 0079 (six readings, seven steps, every start minute: 60,480) joined to every move of the type-1 library, move before or after the table, 12 conventions, exact: no full match, no whole crib stretch, deepest partial match 7 checks in both K4 and all ten scrambled coppers. The Carter and dedication dates of 0038 are short periodic keys, already covered by 0080 and 0083. |
| 92 | 2 | **Type 4.** The message written into a grid of width 2-96 along one of 30 hand paths (rows, snake rows, columns, snake columns, spirals from each corner either way, diagonals, each reversed) and read out along another, 43,579 distinct routes, with a repeating key 1-26 before or after: nothing below period 21. **Prediction failed in detail:** after the move, periods 22 and 23 sit above the coppers' range (47 and 405 settings against at most 32 and 339); counted as distinct check sets they are 13 and 88 against 8-15 and 74-98, so look-alike routes, not a signal. |
| 93 | 6 | **Type 7 through type 1.** One carved letter wrong: every route of the type-1 library with a repeating key 1-26 before or after, accepting settings that fit all known letters but one: nothing below period 14; the smallest period with at most one miss is 20 after the move (coppers 19-21) and 24 before (24-25). **Prediction failed in detail:** three single periods fall just outside the coppers' range (25 exact after the move, 22 and 24 with one miss); look-alike routes were not collapsed into distinct check sets, as they were for 0092. |
| 94 | 6 | **Type 7, length changes.** One carved letter extra (struck out, 96 letters) or missing (an unknown put back, 98) at every place outside the crib stretches, 149 variants, every single move on the true length (K3's rule, one quarter turn, plain and true-keyword columnar; 96 = 8 x 12, 98 = 7 x 14), periodic key 1-26 before or after: 648,709 settings, nothing below period 20, every period inside the scrambled-copper range. |
| 95 | 1 | **Type 8.** 93 riddle words (spelled numbers, units, compass words, the puzzle's and Sanborn's theme words) dragged across K4 under all 376 crib-consistent single-alphabet periodic keys (periods 27-96, 8 classes), skipping the known stretches: no word reaches 3 agreeing checks (most 2), random strings of the same lengths reach 4. At the live lengths a word meets at most a few fixed key letters, so this test has little power; it rules out only a riddle word sitting where the key is already pinned. A first dry run counted words overlapping the cribs (NORTH inside EASTNORTHEAST) and was fixed before the run. |
| 96 | 7 | **Type 2, joint simulation.** 31 two-stage recipes from experiments 80-88 (repeating key 7, 14 or 21 with a width-7 columnar, a width-7 quarter turn or a K3-rule move, either order; the self-feeding autokey at lag 1 or 21 with a period-7 key, with or without a move; the column-plus-row key), 20,000 samples each from Carter's English: none makes the doublet column and the width-21 repeats together more than 2 times in 20,000. The column peaks at 1.4% (autokey lag 1 + period-7 key, as in 0065), the repeats at 1.5% (any period-7 key, since 21 = 3 x 7). **Prediction failed:** the column-plus-row key at width 7 makes the column in 0.26% of samples, the chance rate, not over 10%. 0087's premise was wrong: the row letter cancels inside a row, so doublets fall as under a plain 7-letter key. The sample size was raised from 4,000 to 20,000 after a dry run, before the run. |
| 97 | 6 | **Type 2 and the type-1 gap, free alphabets.** A repeating key on an unknown mixed alphabet (Quagmire III) or an unknown pair (IV), after or before every move of the type-1 library or none, tested exactly by linear algebra mod 2 and mod 13: at periods 3, 7 and 21 (the divisors 0096 ties to the repeats) the consistent counts sit in the coppers' range everywhere but one cell: Quagmire IV at period 3 after the move, 16 settings against 1-12, 12 distinct equation sets against 1-11 (counted after the run). With ten controls K4 tops them all one time in eleven by chance, and free alphabets leave the plaintext open, so this is marginal, not a lead. Free alphabets are a weak test at 7 and 21: thousands of settings fit on K4 and coppers alike. |
| 98 | 1 | **Types 3 and 5.** The sculpture's running keys of 0090 (tableau, Morse, the four ciphertexts, K1-K3, Sanborn's letters) on an unknown mixed alphabet, any of 26! orders (Quagmire III, K1-K2's system with the table left free), every offset, both directions, three rules, tested exactly mod 2 and mod 13: 80,676 settings, none fits any alphabet on K4; scrambled coppers 0-57. |
| 99 | 6 | **Type 1, last gap in the turn library.** Two quarter turns in mixed senses (clockwise then anticlockwise, the reverse, anticlockwise twice) at every pair of widths 2-96, forward and inverse, 53,743 routes not tested before, with a repeating key 1-26 before or after: nothing below period 20, and every period inside the coppers' range counted both by settings and by distinct check sets. |
| 100 | 6 | **Replication.** The four marginal counts of 0092, 0093 and 0097, as distinct check sets against 50 fresh scrambled coppers: paths at period 22 (p 0.24) and 23 (p 0.48) and one miss at period 22 (p 0.10) were luck. Quagmire IV at period 3 after a move stays above every copper: 12 distinct equation sets against 0-11, p below 0.02. That is not a replication in the strict sense, since K4's count is the same data and only the null is sharper; the cell was the most extreme of 12 in 0097, so corrected it is near 0.24. Listed after the run, the 12 sets are loosely constrained systems spread over different moves. Pinned down in 0102. |
| 101 | 1 | **Interrupted key.** The key word restarted at each plaintext word, using the word breaks the cribs give (five splits of EAST NORTH EAST and BERLIN CLOCK), key lengths 1-26, 8 classes: no length fits on K4 or on any scrambled copper. Offsets 0-3 recur in every word, so known letters always share key letters and the test is exact at every length. **Prediction failed in its exception:** it expected long keys to escape the test; none can. |
| 102 | 6 | **The period-3 excess, settled.** Quagmire IV at period 3 after a move against 400 shuffles: K4's 12 distinct sets has p 0.043 (one shuffle reaches 23), 0.048 after correcting across the four period-3 cells; against 400 copies of K4 with the columns of its 21-wide grid permuted, which keep every pair 21 apart, p 0.10 and the mean rises from 4.8 to 6.2. Not a signal; part of it is the known width-21 repeats. **Prediction failed in detail** (expected above 0.05 and above 0.2). |
| 103 | 1 | **The copper as its own key through K3's rule.** Key for place i = the carved letter at a + b i mod 97, every a and b (the mirror and every decimation; 0002's lags are b = 1), 16 rules: best 7 of 24 known letters alone (coppers 7-9); with a repeating key added, nothing below period 20, period 25 just outside the coppers' range. **Prediction failed in detail:** it put the best at 6. |
| 104 | 1 | **The message as its own key through K3's rule.** Key for place i = the message letter at a + b i mod 97: each known letter fixes its whole cycle of the rule, so the test is exact; no setting of 7,031 maps x 12 rules survives on K4 or on any copper. |
| 105 | 8 | **Affine Hill, letter by letter.** Written as decryption, p = B c + w, every known letter is one equation in one row, partial blocks included; sizes 2-5, plain and affine, every alignment, four numberings, solved mod 2 and mod 13: every setting of size 2-4 dies on K4 and on the coppers, the 4x4 affine case included; 5x5 affine is underdetermined in 14 of 20 settings and dead in the rest. A planted affine Hill text is recovered. |
| 106 | 9 | **Family 9 with every move built so far.** A one-to-one letter swap with the type-1 library, 0092's grid paths, 0099's mixed double turns and 0083's triple turns (1.84 million distinct routes; the swap commutes with the move, so one test covers both orders): no route fits on K4 or on any scrambled copper. |
| 107 | 5 | **Three-term Gromark, free alphabet.** d[i] = d[i-a] + d[i-b] + d[i-c] mod 10 for all 20 rules with c up to 6, every primer (10,631,000), four forms, any mixed alphabet, by 0069's exact digit-difference test: no primer consistent on K4 or on any copper. A planted text is found. |
| 108 | 4 | **The copper read from behind.** Each carved line right to left with the line order kept (the view from the back, where the tableau reads correctly), the line order reversed, and both, with the reading before or after the table: periodic keys dead below 26 in every case, no ciphertext or plaintext autokey lag with three or more checks survives, as on the coppers. A first dry run counted checkless long lags and tautological chain steps as checks; fixed before the run. |
| 109 | 1 | **Keyword tables from the whole dictionary.** Every word of four letters or more in the project dictionary (208,062 distinct keyword alphabets) as the plain alphabet, the cipher alphabet or both, with a repeating key 1-26 and no move, 10 classes per word: nothing consistent below period 26 on K4; the coppers reach 25. K4 is if anything less consistent than chance. |
| 110 | 6 | **Keyword columnar from the whole dictionary.** True keyword column orders from every dictionary word (229,634 distinct orders, repeats dropped or whole word; 459,268 routes with inverses), repeating key 1-26 before or after: nothing below period 21; the one period outside the coppers' range (23 after the move) has K4 below them (228 against 231-296). |
| 111 | 6 | **Myszkowski.** Columns sharing a key letter read together across each row, keyed by every dictionary word with a repeated letter (171,995 distinct keys, ABSCISSA and PALIMPSEST among them; 343,964 routes with inverses), repeating key 1-26 before or after: nothing below period 21; period 25 after the move falls just below the coppers' range (1,499 against 1,540-1,650). |
| 112 | 6 | **The same word twice.** Double keyword columnar with one dictionary word for both passes, the field double transposition (229,634 orders, 459,267 routes), repeating key 1-26 before or after: nothing below period 21, every period inside the coppers' range. |
| 113 | 6 | **Rail fence and redefence.** Zigzag over 2-48 rails from every start phase, rails read in order, reversed, or (up to 6 rails) in every order, 12,784 distinct routes, repeating key 1-26 before or after: nothing below period 21, every period inside the coppers' range. |
| 114 | 6 | **AMSCO.** Cells alternating one and two letters under every dictionary word of 3-15 columns, either cell size first (445,680 settings, 891,360 routes), repeating key 1-26 before or after: nothing below period 22. Period 23 after the move sits above the coppers: 21 settings against 1-15, 15 distinct check sets against 1-9 (counted after the run). The keys are obscure words (ADULTEROUSLY, MATCHLESS, THIOPHOSPHATE), and with 52 cells and ten controls about 4.7 cells should top the range by chance; one does. Noted, not followed. |
| 115 | 3 | **Key word/s.** A puzzle word (171: vocabulary, K1-K3 words, theme words) added to any dictionary word of 3-24 letters, every start of each, 24 table rules (KRYPTOS + ABSCISSA repeats every 56, inside the lengths the cribs allow): subtracting the puzzle word never leaves a key that repeats with any length 3-24, on K4 or on a copper, so no second word is even forced. Two-word sums with one puzzle word are dead. |
| 116 | 8 | **Matrix codes, then the table.** A Hill matrix of size 2-4 with a repeating key of length 1-26 on the table, either order (one numbering: p = B c + a shift per block class), solved row by row mod 2 and mod 13: no setting alive on K4 or any copper; every setting dead for 2x2 at key lengths 1-12, 14 and 16-24, for 3x3 at 1-7, 9, 12-15, 18 and 21, for 4x4 at 1, 2, 4 and 8; the rest partly open (too few equations). A planted text is recovered. |
| 117 | 1 | **'All the possible shifts' (C2(b)).** The sculpture's texts (the K1/K2 block among them) as a running key plus one constant shift of the table, both key numberings, with no move and with every move of the type-1 library before or after the table, tested through difference signatures: no full match, no whole crib stretch; the deepest partial match is 8 checks on K4 and 7-9 on the coppers. |
| 118 | 1 | **Autokey running on from K3.** Ciphertext autokey whose key is the carved letter 1-200 places back in the whole carved stream (K1-K3 and the ? before K4), so every known place is a check, and the letter carved one or two lines above on the plate: best 5 of 24 by distance and 3 by the plate (coppers 5-6 and 2-5). |

### Experiments 80 to 88: types 1 and 2 of directions.md (2026-10-15 night)

Alexis away; worked off type 1 (change plus move) and type 2 (sevens) in order, each checked first against the
prior-work database. All nine reverted; no champion. Run issue #24.

Findings worth keeping:
- **Type 1 is closed for its four cheap gaps.** Two repeating keys around a move, solved as a linear system (0080);
  autokeys of both kinds with K3's rule, grid turns and columnar (0081); hand padding, blanks on top or fillers carried
  through a second turn (0082); every triple quarter turn, 1.7 million routes (0083). All at the scrambled-copper rate.
- **Type 2's open items are closed too.** Double columnar with one width of 7 in all 5,040 orders (0084); the ? as a
  98th symbol in a full 7 x 14 grid, with autokeys (0086); a column word plus a row key, the one construction found that
  lines doublets up by column by design (0087), and the same with a shift per stretch of m letters or per carved
  31-letter line (0088). The width-7 doublet column still has no construction that also fits the cribs.
- **Issue #26:** ten records (0006-0081) read keyword column shuffles by the rank list, the inverse of the key order.
  0085 reran true keyword columnar, single and double, with periodic and autokey keys: chance. The library's keyword
  order also drops repeated letters (ABSCISSA reads as ABSCI); 0084 and 0085 test the whole-word reading as well.

Mistakes:
- Three predictions failed in detail at the margin (0080 low at three checks; 0081 four settings at four checks; 0082
  and 0083 a period just above the control range, 0083 one coincidence at period 18 that decrypts to noise). In each
  case the excess was examined after the run, not before.
- 0086's three-check excess came from 34 distinct check sets repeated by look-alike routes. Counting distinct check
  sets, not settings, should be the default for route sweeps.
- Starting 0085 the first time, `cp` and `rm` prompted interactively and did nothing, so two aborted runs (0085 on
  0084's code, then 0086) were started and killed within seconds and their folders removed before any record was
  written. Use /bin/cp -f and /bin/rm -f.
- Family 6 took seven reverts in a row (0080-0086), past the five-revert pivot rule, because directions.md fixes the
  order of types; noted in the pivot log.
- 0087's phase clock was not ticked, so it shows as unclocked.

Open:
- Type 1 left: the two stages on different alphabets (not linear), two free alphabets at periods 13-26 (needs English
  scoring), turns with one carving error (type 7). Type 2 left: width 7 with two free alphabets, and a joint simulation
  that must make both fingerprints and fit the cribs.
- Next in directions.md: type 3, keys read off the sculpture.


### Experiments 89 to 118: types 3 to 8, the free-alphabet follow-up, then hand routes keyed by the dictionary (2026-10-15 night)

Alexis away overnight, asked to continue past 100. Worked through types 3-8 of directions.md once each, then
followed the one cell that stood out. All eighteen reverted; no champion. Issue #24; issue #28 (source-text search).

Findings worth keeping:
- **Types 3-8 have each had a first exact pass, all at chance.** Keys read off the sculpture by position (0089) or
  as running keys joined to every move (0090, and on an unknown alphabet, 0098); the Berlin clock with every move
  (0091); the message written along grid paths (0092); one wrong, missing or extra carved letter through moves
  (0093, 0094); riddle words dragged under every live periodic key (0095, weak); an interrupted key (0101); the
  copper or the message as its own key through K3's rule (0103, 0104).
- **Type 5 is closed by algebra, not by a run.** Any reading of a cyclic table (by columns, diagonals, mirrored, from
  another start row) is an affine map of the alphabets with the key scaled or shifted; those are covered by 0071 and
  0074, and a diagonal reading only restricts the key to even values.
- **No published text carries both cribs** (issue #28: Internet Archive full text, 44 Gutenberg books, the web).
- **The width-21 repeats have a cheap explanation**: any key repeating every 3, 7 or 21 carved letters, after any
  move, makes them about 50 times more often than chance (0096). On fixed alphabets those periods are dead; on free
  alphabets the test is weak (0097). The one free-alphabet cell above the coppers (Quagmire IV, period 3, after a
  move) went from p < 0.02 against 50 coppers (0100) to 0.043 against 400, and 0.10 against copies that keep
  K4's width-21 columns (0102): not a signal, and partly the repeats themselves.
- **0087's premise was wrong** (0096): a column word plus a row key does not line doublets up by column, because the
  row letter cancels inside a row.
- Family 9 and the affine Hill are closed for every route set built so far (0105, 0106).

Mistakes:
- My wait loops used `pgrep -f run_experiment.py`, which matched their own command lines, so they never ended
  and were killed by hand. Wait on the run log's `decision=` line instead.
- 0089 and 0090 recorded misspelt family slugs (4-visual-systems, 6-matrix-transposition-then-tableau); the
  dashboard maps them. Check `cut -f3 results.tsv | sort -u` before choosing a slug.
- 0090's worked example crashed (the Morse text is shorter than K4), so that record has none; the figure
  rebuilt one from the record's own functions.
- 0092, 0093, 0096, 0101, 0102 and 0103 missed their predictions in detail; 0096's miss is the 0087 correction.
- 0095's first dry run let words overlap the cribs and counted those as checks; fixed before the run.

Open:
- Free alphabets at periods 7 and 21 need a stronger test than consistency (English scoring cannot beat its
  controls; a test on the forced partial alphabets might).
- Routes outside every set built so far; three-term Gromark rules; plaintext masks that change letters by a code.

### Experiments 50 to 64, run in the background (2026-10-15 afternoon)

All fifteen reverted; nothing was kept, and the champion is still experiment 34. Every run
finished well inside the 30-minute budget (longest 0050 at 5 minutes).

Findings worth keeping:
- **The two fingerprints are real (0056).** The width-7 doublet column and the width-21
  repeats survive the look-elsewhere correction over widths 2-48 against 10,000 shuffles:
  corrected p 0.005 (0.018 among six-doublet shuffles) and 0.010. The pre-registered
  prediction said they would not. They still lack a construction.
- **Only ciphertext feedback makes the width-21 mark (0062).** Of fourteen generators, only
  ciphertext autokey at lag 21 raises the repeats well above chance (5.4% against 0.2%);
  none makes the doublet column, and none makes both. Ciphertext autokey stayed dead when
  combined with columnar routes in either order (0063) and on tables rebuilt from K1-K3
  words (0064).
- **Two structural exclusions, no key search needed.** Pure transposition is dead because
  the cribs need three Es and the copper has two (0051). Every cipher with at most 25 output
  letters or an even-length rule (Playfair, bifid, four-square, ADFGVX, a 24-letter
  Weltzeituhr ring) is dead because K4 uses all 26 letters and has 97 (0052).
- **Tables rebuilt from every K1-K3 word and the 2025 letter's words** add nothing for
  periodic keys (0053), Gromark (0054, smallest base 17), Hill (0055), two-word keys (0059)
  or ciphertext autokey (0064). The vocabulary was not the limiting factor.
- The copper off by one letter through the two-word test (0050), filler letters chosen by
  letter (0057), the table then keyed column shuffles from K1-K3 words (0058), the K2
  coordinates as a Hill matrix (0060) and the misspelt letters as a second key (0061): all
  at chance.

Mistakes:
- Walkthrough arithmetic slipped four times and was caught by checking the numbers before
  the run (0053, 0054, 0055, 0056), and once after it: 0052's record puts I at place 16,
  not 17. Checking the walkthrough against the code before running is now routine.
- Two predictions were wrong in detail: 0057 and 0058 expected nothing below period 26
  and got periods 24-25 at chance rates; 0058 ran no control to measure that rate, and
  the forced fragments at 24-25 were not word-checked in 0057.
- 0050's pre-registered count of distinct crib tuples was corrected to "about 50" before
  the run; the measured value is 48.

Open questions:
- What construction makes both fingerprints? Ciphertext feedback at lag 21 plus a stage
  that also lines up doublets at period 7 is the lead; it must still pass the cribs.
- Family 3 has now reverted seven times in a row (0014-0061) and family 6 eleven times;
  both should rest until a new key source appears.
- The scorer decision (key cost, shuffled baseline) is still pending in issue #11; no
  key-completion climbs were run.


### Experiments 65 to 79, run in the background (2026-10-15 evening)

All fifteen reverted; nothing was kept, and the champion is still experiment 34. Every run
finished inside the budget (longest 0077 at 4 minutes). Run issue #22.

Findings worth keeping:
- **The fingerprint constructions are dead under the cribs.** Only one recipe was found that
  lines doublets up in sevens: ciphertext autokey at lag 1 with a period-7 key, and it does so
  weakly (1.5% of samples against 0.1-0.3% by chance, 0065). Tested exactly, ciphertext autokey
  plus a periodic key at any lag and period is dead (0066), and so are lag 1 with period 7 and
  lag 21 at every period. Two-lag letter feedback, the one-stage way to make both marks, is at
  chance (0067); so is ciphertext autokey with one carved letter wrong, missing or extra (0068),
  and every block-of-seven reshuffle joined to it, in both orders (0077). The two fingerprints
  remain real and unexplained.
- **Gromark is closed for two-term rules whatever the alphabet.** With a completely free mixed
  alphabet, base 10 (lags up to 6, 0069) and bases 2-16 and 26 (lags up to 5, 0076) leave no
  consistent primer on K4 or on shuffled coppers; planted texts are recovered. Same-letter cribs
  fix exact digit differences, which makes the test decisive. Family 5 marked
  exhausted-bounded; three-term rules with a free alphabet stay open.
- **New key sources revive nothing:** alphabets one swap or one move from KRYPTOS, the C27(c)
  'slightly different tableau' (0071); the 32 compass points and the 'what's the point?'
  letter's words (0072); plaintext autokey plus a periodic key on 161 word alphabets (0073);
  affine masks, Atbash included (0074); Sanborn's 1989 letter, the 1991 dedication pages and
  the 2025 open letter as running keys (0078, best 15 mismatches as on shuffles); key schedules
  from the Berlin set-theory clock (0079, best 8 of 24 agreeing, as on shuffles).
- **The doublets are real letters.** QQ, SS and TT inside the known stretches carry NO, ST and
  IN, so the doublets cannot be fillers, and striking out the other three changes nothing (0075).
- A block-of-seven reshuffle before or after a periodic key admits no period below 25 beyond
  chance (0070).

Mistakes:
- Pre-registered counts were wrong four times and corrected before the run only once:
  0071's variant count (975 to 925, corrected before), 0066's case count (294,912 counted lags
  with no equations; 221,184 tested), 0069's primer total (5,432,200 for 5,432,100), 0067's
  case count (5.2 million counted cases with no check; 1.93 million tested).
- Two predictions failed in detail at the three-check level, 0067 (15 survivors against 3-12)
  and 0073 (12 against 0-6). Both resolve into scattered or nested coincidences, but a
  prediction should allow for chance survivors at three checks when millions of cases run.
- 0068's substitution tally counts the residuals a replacement letter is fitted to as checks,
  overstating redundancy by one or two.
- 0070's fragments at periods 25-26 were word-checked only after the run.
- 0079's prediction carried a numeric guess (19-20 mismatches) that a dry run on the copper
  showed wrong (16); it was removed before the run and is disclosed here.
- The recorder stopped once on a clue-register match (0071) after writing families.md and the
  notebook; the commit was finished by hand.
- The harness once hung on an interactive cp prompt when restoring attack.py; /bin/cp -f
  avoids it.

Open questions:
- What makes the width-7 doublet column? Every construction with a period-7 element that
  passes the cribs has now failed; one not yet tried is a second, independent stage such as
  nulls placed by a period-7 rule after encryption, or a homophonic substitution.
- The width-21 repeats: ciphertext autokey at lag 21 made them, but it is dead with every
  addition tried (periodic key, second lag, one error, block reshuffle, word alphabets).
- Three-term Gromark with a free alphabet; Hill with a free numbering; Sanborn's own charts
  (C27) beyond the alphabet.
- The scorer decision (key cost, shuffled baseline) is still pending in #11; no
  key-completion climbs were run.

### Scoring settled (2026-10-15, afternoon)

Alexis decided the open scoring questions (issue #23). First version, same afternoon: a hard
gate on key size (100 bits). Withdrawn within the hour. Alexis asked where the requirement came
from: it was criterion 4 of our own success definition ("a key a person could remember"),
justified by K1-K3's short keywords and Sanborn's "words without a method is not solved". Neither
holds up as a basis for a size limit. Three sections are a thin precedent and do not agree (K3
has no keyword), and Sanborn's remark is about showing the method, not the size of the key. A
long key can have a short description: a running key from a named book.

Final rules: (1) the original four gates; (2) a reading must beat the same method on at least
ten shuffled coppers (run() returns "controls"); no controls, no keep; (3) the harness counts the
key by the length of its description (key words a few bits each, a named text and offset a few
bits, arbitrary letters 4.7 bits each) and charges it in the loss, not as a gate; (4) lowest loss
wins. Criterion 4 of the success definition now reads: a hand procedure from 1990, written down
step by step, keyed by something with a short description rather than letters fitted to the
known places; its source is Scheidt's 2011 remark (secondhand, via Bean, C5): "simple, can be
remembered, and executed years later when used with the correct key word/s".

All records re-scored (tools/replay_rules.py, records untouched): no past reading passes the
baseline, because no record carries a set of ten or more controls. Experiment 34 would fail on
its own numbers anyway (its reading -3.70 against a shuffled best of -3.23). Experiment 48's best,
-6.14, beat its smaller control set (-6.36 to -6.88), but that set was not ten full-size runs.
There is no champion. The dashboard now recomputes every loss under the current rules, keeping
each record's own figure as history, so one number shows everywhere.

Lessons: a success criterion has to be a gate or a score in the harness from day one, or the loop
optimises around it; and a criterion needs its source written next to it, or it hardens into a
rule nobody chose.

## 2026-10-14

### Decisions

- Success means a reproducible method, not words: the 97 letters must carry the cribs at
  22-34 and 64-74, read as English, re-encrypt exactly, and come from a memorable key and
  a 1990 hand method. No external oracle. Every experiment leaves a bounded negative.
- Loss is lexicographic: ten points per wrong known letter, then the English deficit,
  then key cost. The crib gate at ten is where a solution first becomes visible.
- Records carry four prose fields written before the run: expert hypothesis, plain-words
  version, prediction, walkthrough. They are not edited after the result; corrections go
  to the families table and the issue thread.
- Phase clock: design, implement, test, with run and record added by the harness, and a
  pause tick for time handed back to a person.

### Built

Harness (`run_experiment.py`, `_runner.py`, gates, scorer, 19 tests), the frozen cipher
library, the knowledge base of 72 sources with a clue register of 30 entries, the families
list, the dashboard, the phase clock. Dashboard changes from review: plain words first on
each record, walkthrough beneath, numeric ids, crib gate explained beside the chart with
the 24-letter strip, axis in loss points with "n wrong" readings, unclocked phases named,
record tables that wrap.

### Experiments 1 to 20, all reverted

| # | Family | One line |
|---|---|---|
| 1 | 1 | Baseline KRYPTOS keyword: 2 of 24 cribs, loss 224.7. |
| 2 | 1 | Ciphertext autokey, every lag, 24 conventions: none. |
| 3 | 1 | Plaintext autokey inside the cribs: lags 1-11 and 30-52 dead. |
| 4 | 1 | Running key from K1-K3, every offset: none. |
| 5 | 1 | Quagmire period sweep: 1-26 and 30-52 dead; survivors force no word. |
| 6 | 6 | 2,905 columnar routes then tableau: no key shorter than 23. |
| 7 | 6 | Tableau then columnar: weak test in this order; nothing at 26-30. |
| 8 | 6 | K3's rule at every shift, double rotations, then tableau: no key shorter than 22. |
| 9 | 1 | Forced key stretches read as noise; one letter inserted or deleted changes nothing. |
| 10 | 1 | Same with 248 vocabulary-mixed alphabets: best equals the shuffled null. |
| 11 | 1 | Progressive key: periods 1-25 and 31-51 dead at every step; period 13 dead. |
| 12 | 1 | Chained plaintext autokey: lags 1-25 and 30-52 dead; 26-29 force noise. |
| 13 | 5 | Gromark-style rules, all lag pairs to 12, bases 10 and 26: none fit the shifts. |
| 14 | 3 | Two words in two passes as linear equations: none under total length 25. |
| 15 | 8 | Hill 2x2 to 4x4, plain and affine, solved exactly: all dead. Playfair dead. |
| 16 | 6 | Forced key under 23,930 routes scored as English: inside the shuffled distribution. |
| 17 | 1 | Running key from the carved tableau, the Morse, the whole panel: none. |
| 18 | 7 | Simulator: no family singled out; width-7 and width-21 anomalies unexplained. |
| 19 | 9 | Substitution then any of 23,931 routes: crib images clash under all. |
| 20 | 1 | Short periods with vocabulary-mixed alphabets: 21 and 42 have no survivor. |

### Findings worth keeping

- The crib-consistency test for tableau systems depends only on the plain and cipher
  alphabets and on Beaufort versus the other modes; the key alphabet drops out. The 24
  conventions are 8 distinct cases for any such sweep (0006).
- Substitution then transposition is the only construction simulated that reproduces the
  width-21 repeats, and it is dead for every enumerable route (0018, 0019). The repeats
  remain unexplained, as does the width-7 doublet column, under every generator including
  random letters.
- A crib-fitted construction passes the crib gate by design (a Hill matrix solved from
  the blocks, a fully chained autokey). The English deficit must carry the verdict, and
  the record must say when the cribs were built in rather than found (0012, 0015).

### Mistakes

- 0007's phases were ticked back to back in one command, so its design time is lost.
- 0016 and 0010 set prediction tolerances from two shuffled controls; the max of two is
  too noisy. Ten or more from now on.
- 0017's record says the carved panel is 869 letters; it is 865.
- 0018's design clock ran across a pause between turns. The pause tick now exists.

### Open at close of day

The three unexplained statistics. Family 2 untouched for want of a concrete mask. Family
4 touched only by the 25-letter-square exclusion. Routes outside the enumerable sets.
Alphabets built from words outside the 61-word vocabulary.
