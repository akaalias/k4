# Kryptos K4 autoresearch report, 0136–0198

Final report of the headless loop started 2026-10-16 18:17 with `tools/run_loop.sh --unattended`
(`STOP_AFTER: family F9`), saved from its terminal output on 2026-10-17. Full log:
`logs/loop-20261016-181735.log`.

The run is complete through F9, the STOP_AFTER family. Every family from F1 to F9 in the ranking was worked through: each item is closed or blocked. Nothing fits K4 better than its scrambled copies anywhere, and no candidate reading came out of any experiment.

## Experiments

**F1 (one keyed stage), 0136–0157**
- **0136** F1.5 step 1: worked out which settings English could ever decide. Autokey lags 85–96 are blocked for good.
- **0137, 0138** design 1 of the free-alphabet decider: plants beat their own scrambled copies only 6 of 12 times, so design 1 fails.
- **0139** design 2 (parallel tempering) passes, 6 of 8.
- **0140, 0142** one free alphabet, Beaufort, key lengths 23 and 26: K4 ranks 9th and 12th of 13 among its own copies. Closed.
- **0143, 0145** measured the two-alphabet decider's power; **0144, 0146** used it: K4 13/13 (L13), 7/13 (L16), 2/13 (L8). Closed.
- **0141, 0153**: errors, rerun as 0142/0143 and 0154.
- **0147–0157** F1.6–F1.11: every variant at the copies' rate. One added-form cell at length 19 survives only with a slip at place 33; its power is 3 of 5, so it is blocked as weak.

**F6 (a move, then the table), 0158–0167**
- Route libraries of up to 116M moves (compiled), each followed by a repeating key.
- K4's shortest fitting key and its lead over the copies were always within the copies' range.
- F6.1/F6.2 (free alphabets after a move) are blocked by cost.

**F12 (Stein's way), 0168–0172**
- **0168** 71 statistics against 1,000 shuffles: nothing outside them.
- **0169** Stein's peak at 13 strands: K1 p 0.0075, about 0.02 allowing for the strand counts scanned; Part II 0.24. A coincidence.
- **0170** six patterns found by eye: none outside the shuffles.
- **0171** two parts with their own keys: copies 0–1 cells, K4 none.
- **0172** probable words in the undecided cells: K4 above every copy in 1 of 10 cells, copies 0–3. Chance.
- F12.7 closed by subsumption; F12.1 blocked (no photographs of the copper at letter resolution).

**F3 (two-part key), 0173–0180**
- **0173** Scheidt's patent sandwich: nothing fits K4 in the 161 of 169 length pairs with 4 or more checks. The copies fit at most 2 settings in 1,000.
- **0174** other combiners (mixed numberings, multiplication): 0 consistent on K4 or copies.
- **0175, 0176, 0178–0180** as the number half of a key: Morse E counts, plate line lengths, directions, misspelt-letter positions, the World Clock's ring, "point". 0 fits on K4 and 20 copies each.
- **0177** the patent with two tables and three keys: 0 at 4 or more checks. K4 124 vs copies 98–130 at 1 or more checks, the same rate.

**F2 (masked plaintext), 0181–0183**
- **0181** text forced by 0057's long keys: no dictionary word on K4; copies have one in 0–32 settings.
- **0182** nulls by any rule reduce to a gap of 0–29 between the known words: K4 is never above the copies.
- **0183** phrase strip with homophones: nothing at key lengths 1–25.

**F4 (Sanborn's visual systems), 0184–0186**
- **0184** paths over the copper's real layout: 23/26 vs copies 22/26.
- **0185** trifid with any cube at periods 16–97: no cube fits K4 or any copy.
- **0186** the copper's anomalies as numbers: 0 fits.

**F10 (self-changing alphabets), 0187–0188**
- **0187** Chaocipher with any word-mixed cipher wheel: 0 fits. The code matches Byrne's published test vector.
- **0188** Wheatstone's cryptograph: 0 fits, even with an inner ring in any order.

**F11 (agency hand systems), 0189–0192**
- **0189** M-94 cylinder in any disc order: 0 fits. The disc alphabets came from [jproc.ca](https://jproc.ca/crypto/m94.html), checked internally; disc B1 also matches a second source.
- **0190** poem code on K1–K3 and the Morse: as the copies.
- **0191** the CIA's key box on K1–K3 and Carter's book: 0 fits; best partial 9/24, which the copies also reach.
- **0192** Friedman's alphabet box, 2.45 billion settings: 0 fits.

**F8 (Hill), 0193–0194**
- **0193** error.
- **0194** Hill 2×2 with the letters numbered in any order: no matrix fits K4 or a copy; each plant fits only its own matrix.

**F5 (Gromark), 0195–0196**
- **0195** other bases, three-term rules and longer lags, 1.55 billion primers: 0 fits.
- **0196** multiplicative rules: 0 fits.

**F9 (substitution, then a move), 0197–0198**
- One code alphabet followed by each of the ~254M moves the project has built since 0106: nothing survives on K4 or any copy.

## What is still open or blocked

- **Free alphabets:** F1.1 and F1.2 residues are blocked by the English bound; F6.1/F6.2 by cost. Chaocipher's free wheel needs a search the known letters cannot drive.
- **Data not to hand:** F12.1 needs photographs of the copper. F4.5's plate order needs Antipodes' layout. F11.1's Jefferson wheel and M-138-A strips need their alphabets. F3.7's "the point" as a place needs a survey.
- **Too few checks:** Hill 3×3 with a free numbering, the patent sandwich with both keys 10–13 long, and the slip-at-33 cell (weak).
- **Out of era:** F10.3 card ciphers date from 1999–2000.
- **By cost:** Gromark base 26 at lag 6.

## Surprises

- Chaocipher's wheels are driven by the carved text alone, so the known letters give 11 exact checks once the cipher wheel's start is guessed.
- In Wheatstone's cryptograph the known words pin the hand's moves exactly, so even a ring in any order fails.
- Hill 2×2 with a free numbering turned out decidable: the equations outnumber the unknowns by 5–7 bits.
- No trifid cube fits even the scrambled copies at any period.

## Mistakes

- **0177** ran only 5 of its 20 copies. `pkill` had stopped an aborted run but not its `_runner.py` child, which kept running and shared the CPU.
- **0193** was killed with the shell it was launched from, then failed on a pickling error in the worker pool. It was rerun as 0194, and long runs now use `nohup`.
- **0191's** first draft numbered key values in the wrong alphabet; a missed plant caught it before the run.
- Wording errors in the 0188 and 0190 figures were found while checking them and fixed.
- **0196's** attack file says "0197" in its first line; the run took 0196.

## Housekeeping at the end of the run

The working tree was clean apart from the other session's files, and `attack.py` was back at HEAD. Issues #13, #14, #15, #16, #17, #18, #20, #21, #53, #57 and #58 were closed; #57 and #58 had been opened during the run for F10 and F11.
