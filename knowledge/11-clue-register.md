# 11. Clue register

Every hint, with its readings and what each reading would mean for an experiment.
Experiments cite entries by number in `hypothesis_expert`. Status is updated by the
loop: `untested`, `tested under reading (x) in 00NN`, `exhausted under reading (x)`.
A clue is not done until every plausible reading has been tried or shown to be
untestable. Quotes are verbatim; sources in `02-sanborn-said.md`, `03-scheidt-said.md`
and `sources/`.

## Method clues

**C1. "I used a matrix code, and then we can possibly use this code [the tableau] to
decipher with... sometimes I used double matrixes and triple matrixes... and then went
back to this table to do the ultimate."** (Sanborn, CNN 2005). Readings: (a) K4 is one
or more columnar or route transpositions followed by keyed-tableau substitution; (b) the
sentence describes the whole sculpture (K3 then K1-K2) and says nothing about K4; (c) the
"matrix" is the KRYPTOS-shifted tableau itself and "double" means two tableau passes.
Experiments: family A searches for (a); (c) means composed Quagmires, which the period
sweep bounds. Status: (c) bounded by 0005 (composed period) and 0014 (two words of total length under 25 cannot compose to the forced key). (a) and (c) together, a repeating key before and after K3's rule, a grid turn, two turns or a column shuffle, key lengths 2-14 each, one alphabet: dead (0080). (a) bounded by 0006: columnar routes (plain, keyed, double plain) before a periodic tableau admit no key shorter than 23; a fixed reshuffle of every row of seven, before or after the tableau, admits none shorter than 25 beyond chance (0070); route transpositions and triple stages untested. (a) with the table on one alphabet in an unknown order, every type-1 move, either order, added or Beaufort form, key lengths 1-26, decided exactly: no fit below length 6, fits from 6 at the scrambled-copper rate (0129, 0130). Double and triple matrixes in mixed readings (each stage rows written, columns read left or right first, up or down; pairs at widths 2-96, triples at 2-24), then or before a periodic key on the standard or KRYPTOS tables: nothing live below 20, at the coppers' rate (0134). Wide triples (any width 25-96, 105.5 million routes): at the coppers' rate (0158). A triple with a keyword grid among plain ones (20.4 million): at the coppers' rate (0162). Move, key, move (844-move library, every pair): at the coppers' rate (0160); key, move, key on two different tables: at the coppers' rate (0161). Every keyword transposition of the field manuals and agent ciphers (disrupted, triangle, interrupted, trapezoid, keyed blanks, row reshuffles, French diagonal, EVA, Chiffre XIII masks, Nihilist square with every key): at the coppers' rate or dead (0164-0167). (c) untested. 2026-10-20: (a) with a 10x10 turning grille (Fleissner) as the matrix, every card, copied out by rows or columns, then or before the table: no card fits with a free key of 1-6 (rows) or 1-4 (columns) letters or any of 200,563 key words (0199, 0201); longer free keys blocked by cost. (a) with one deliberate slip in the keyword columnar (a column read out of place or two swapped; SOE's 'indecipherables'), around every keyword columnar closed so far: at the copies' rate (0202-0204). (a) with two carved slips at the known places, every keyword columnar, Myszkowski, double, rail fence, AMSCO and type-1 route, then or before a periodic key on the tables: shortest fit 18/16 as the copies, readings judged as the copies' (0214).

**C2. "No one has recovered the original matrix... surprised that no one had tried
recovering the original matrix and running it through all the possible 'shifts'."**
(Sanborn, 2003, secondhand). Readings: (a) K3's true matrix is not the NSA's 4x86 but a
different grid whose other "shifts" (rotations, offsets, start positions) produce K4; (b)
"shifts" are the 26 row shifts of the tableau, and the matrix is the K1-K2 worksheet
(the "K1/K2 matrix" he "seemed mystified no one has gotten any thing more from"); (c) a
Hill-style numeric matrix. Experiments: recover every grid that reproduces K3 (widths 7,
8, 14, 21, 24, 28, 42, 48, 86; Bauer's double rotation; Stehle's 192 rule), then apply
each grid's family of shifts to K4 before and after tableau substitution. Status:
0006 covered plain columnar at every width including the K3 widths, before the tableau; 0008 covered reading (a) in full for the K3 rule at every shift and for double grid rotations, before the tableau: no shift admits a tableau key shorter than 22. With a repeating key on both sides of the K3 rule at every shift, key lengths 2-14 each: dead (0080). Three quarter turns at every width triple, then or before a periodic key 1-26: dead (0083). The after-tableau order is weakly bounded by 0007. Reading (b), the sculpture's texts (the K1/K2 block among them) as a running key under each of the 26 shifts of the table, with or without a type-1 move: dead (0117). With up to 3 slips at the known places: dead (0211).

**C3. "I like to use spatial systems of encoding and decoding... pattern, light and
shadow... visual systems... individualistic."** (1999, 2005). Readings: (a) a route
through the carved grid (31-wide lines, the four plates) rather than an abstract matrix;
(b) the tableau read mirrored, as it reads from behind; (c) positions of the physical
anomalies as the key. Experiments: family D. Status: (a) the carved lines laid over the tableau and cipher plates, straight or folded, as a positional key: dead (0089); grid paths (snake, spiral, diagonal) with periodic keys: dead below 21 (0092); hand padding of a 31-wide carved grid: 0082. (b) K4 read from behind, line by line, with periodic keys and autokeys: dead (0108). (c) untested. 2026-10-17: (c) the copper anomalies' places (the ?, K2's dropped S, YAR, the extra L, odd lines) as the number half of a key with an unknown word: dead (0186); paths over the copper's own layout with periodic keys: as copies (0184). 2026-10-20: a grille (a card with holes, Sanborn's light and pattern) as the spatial system: the 10x10 turning grille with the table, no card fits K4 (0199, 0201).

**C4. "I masked the English language... the masking technique may not be known... you
need to solve the technique first and then go for the puzzle... more than one stage."**
(Scheidt, 2005, 2015). Readings: (a) a plaintext transform before a keyed cipher; (b) a
non-standard alphabet or base ("base 16," "Mayan... base 60"); (c) "stego": the English is
hidden inside something readable; (d) the mask is what Sanborn calls a matrix. Family B.
Status: masks that only move or pad letters (reversal, regular nulls, prefix nulls) before a periodic tableau are dead (0023); writing the message into a grid along a snake, spiral or diagonal path and reading it along another, with a periodic key before or after, is dead below period 21 (0092); nulls chosen by letter (every copy of one or two letters outside the cribs) behave like random strike-outs of the same size (0057); masks that change letters by an affine map of either alphabet (decimations, Atbash), before or after a periodic key or ciphertext autokey, are dead (0074); other letter-changing masks untested. 2026-10-20: (a) nulls at both ends (SOE's padding), with periodic or progressive keys: nothing below 26 (0205). 2026-10-25 (A13.3): the 31 saved climbed readings with all 24 known letters, through 14 tests for a mask (reversal, X spacing, nth letters, affine, columns...), against their own searches on fresh copies: no flag (0216, 0217); weak, the climbs overwrite masked plants (1 of 22 found). The slip searches' fixed readings (0207, 0212-0214), same tests: no flag; masked slipped plants found except X every kth letter (0220). 2026-10-27 (A6.3): masked plants through F1.5's design 2 at F1.1 L23: reversal found (7 of 8); X every kth letter and the message in every nth place not found at power (5 and 3 of 8): the free-alphabet sampled closes hold for unmasked or reversed English only (0227).

**C5. "Not mathematical... simple, can be remembered, and executed years later when used
with the correct key word/s... similar to what would be provided agents or pilots in
case of capture."** (Scheidt, 2011). Readings: (a) keyword-driven classical system,
no primers or arithmetic; (b) "key word/s" plural: two keywords, as K1 and K2 each had
KRYPTOS plus one; (c) a duress code: two valid readings. Constraint on every family.
Status: constraint. 'Key word/s' as two words added (one from the puzzle, one from the whole dictionary, 3-24 letters): dead (0115). A keyword table with a running key from any English text (a 'named text'): the forced key is not English under any dictionary keyword table, at stated power (0125). Friedman's key-advance schedules with one key word (run length, CHRISTMAS, EXTINGUISHER, interruptors, fraction digits): dead or at chance (0156); a split key phrase (EMC 59d): no fit (0157).

**C6. "The key is the algorithm... the keys were concealed at the sculpture... conveys not
only the encrypted data, but also the key... part of the code was designed to be solved
with multiple keys."** (Scheidt, 2003, secondhand). Readings: (a) the keyword is
written on the sculpture (KRYPTOS, the Morse words, HILL, DYAHR); (b) the method is
recoverable from the sculpture's layout; (c) the K1-K3 keys are reused in combination.
Family C. Status: 'keys concealed at the sculpture' as a running key from the carved tableau or the Morse is bounded by 0017; as a key read by position, the letter of another plate at the same or the folded place of each K4 letter, by 0089; as a running key joined to any K3-style move before or after the table, by 0090; on an unknown mixed alphabet (any of 26! orders), by 0098; as a keyword in a periodic tableau by 0005 and 0009-0011. Family C otherwise untested.

**C7. "Instructions in the earlier text that refer to later text"; "clues to the last
section are contained in previously deciphered parts... getting those first three sections
correct is crucial"; "it will come back to the first part."** (2005, 2006). Readings: (a)
words in K1-K3 are keys (PALIMPSEST: overwritten; ABSCISSA: the x-axis; LAYER TWO; ID BY
ROWS was wrong but "by rows" was Sanborn's own reading of jargon); (b) the misspellings'
positions are indices; (c) K2's coordinates are numbers for a key; (d) K3's Carter passage
instructs: candle, breach in the upper left corner, widening the hole, "can you see
anything." Key-source rule plus families C and D. Status: as a running key, K1-K3 plaintexts and ciphertexts (0004), the sculpture's own texts (0017) and Carter's book (0021) are dead at every offset; as key words, the K1-K3 vocabulary is dead for periodic keys (0005, 0009-0011). Other readings untested. Ciphertext autokey continuing the carved stream from K3 (every lag 1-200) and the letter above on the plate: at chance (0118). Carter's book as a running key on any one alphabet, every offset both ways: no fit (0154). 2026-10-20 (A1.3): every one of these running keys with up to 7 of the 24 known letters slipped (fixed and keyword tables): no setting on K4 or any copy (0210); with K3-style moves and shifts, up to 3 slips: none (0211).

**C8. "The most obvious key to the sculpture, nobody has picked up on."** (2005). Readings:
(a) KRYPTOS itself used in a way not yet tried (as a transposition key for K4, as it was
for K3; as the K4 Vigenère key at a period other than 7; as a numeric key 1473625);
(b) the tableau's own header A-Z; (c) the word on the entrance, the Morse, the compass;
(d) the title's meaning, "hidden," as a word. Status: KRYPTOS as a periodic tableau key at any period and convention is excluded by 0005; as a transposition key alone, excluded with every other pure transposition by letter counts (0051). As one stage of a double column shuffle (every order of seven columns, KRYPTOS's among them) with a plain or word-keyed second stage and a periodic key: dead (0084). As the column key of a grid with a second key per row (key = column letter + row letter), width 7 and every other width 2-48: dead (0087). That construction does not line doublets up by column after all: simulated at width 7 it makes the doublet column at the chance rate (0096).

**C9. "Having the letters sitting there in plain sight is a pretty big clue."** (2005).
Readings: (a) the ciphertext is already the plaintext in some reading order
(contradicted by the cribs for pure transposition, but not for transposition plus a
light substitution); (b) the tableau letters, including the extra L, are the key.
Status: (a) as pure transposition excluded by letter counts: the cribs need three Es, the copper has two (0051); (b) the tableau letters behind or beside each K4 letter, straight or folded, are not the key (0089); with a light substitution untested.

**C10. "The misspellings... it's more the orientation of those letters that's useful
there... the positioning."** "They're important" (the misaligned YAR). (2003). Readings:
(a) the positions of Q in IQLUSION, U in UNDERGRUUND, A in DESPARATLY (and the missing E),
and the raised YAR, read as indices into the tableau or the K4 text; (b) Bauer's error
coordinates (25,2), (24,6), (11,15), (15,15) as a matrix; (c) "orientation" literally:
the letters' direction, upside down (RQ reads YR). Status: (a) the misspelt letters QUA, the corrections LOE (with and without the dropped E) as a short second key added to any word: best 8 of 24 known letters, against 7-11 on shuffled coppers (0061); index readings untested. 2026-10-17: (a) the misspelt letters' positions, shifts and Bauer's coordinates as numbers with an unknown word: dead (0178).

**C11. "The other 91 characters and their proper order are yet to be determined."**
(NYT 2010 wording). Reading: a reordering step exists. Supports C1(a). Status: noted.

**C11a. NSA 1992: "plain-text auto-key" and "interval 7"; NSA 2007: plaintext and ciphertext
autokey tested without cribs.** Status: 'plain-text auto-key' joined to a K3-rule, grid-turn or columnar move, either order, every lag, one alphabet: dead (0081). 'interval 7' as a structure that lines doublets up in sevens: only ciphertext autokey at lag 1 with a period-7 key raises the doublet column, to 1.5% against 0.1-0.3% by chance (0065); ciphertext autokey at lag 1 with a period-7 key, and at lag 21 with any period, is dead under the cribs (0066). 'plain-text auto-key' is dead at lags 1-25 and 30-52 and gives noise at 26-29 (0003, 0012); 'interval 7' as a period is dead under plain and progressive keys (0005, 0011) and as an autokey lag (0012). The substitution-then-transposition order is weakly bounded by 0007.
and lags 1-96 (0002). Plaintext autokey excluded at lags 1-11 and 30-52, undecided at 13-29 and 53-96, lag 12 consistent under one convention on a single check (0003). Any mixed alphabet at all, unknown: with the sculpture's running keys, no fit (0098); with a periodic key 3, 7 or 21 after or before a type-1 move, at the scrambled-copper rate, one marginal cell at period 3 (0097). Keyword-mixed tables from every dictionary word, periodic key 1-26: nothing below 26 (0109). Any one alphabet at all on both sides, periodic key 1-26, no move, exact: added form dead at every length, Beaufort form alive only at 23 and 26 (0119); at those, K4 climbs no better than coppers, weak test (0120). Two unknown alphabets: consistent at 8 lengths, as coppers (0123, 0124). A running key from any English text on any dictionary keyword table: the forced key is no more English than on coppers, below every planted running key (0125). Autokey (ciphertext and plaintext) on one unknown alphabet, every lag, no move, exact: dead lags closed, the rest at the coppers' rate (0149). 2026-10-20 (A1.4): with up to 2 slips at the known places or one lost step in the chain, ciphertext autokey on every table tried (487,734 setups) fits nowhere below lag 68 (0212); plaintext autokey nowhere below lag 24, its readings at 26-29 judged blind as the copies' (0213). 2026-10-27 (F13.2): 'interval 7' and the width-21 repeats as features of a 17-family classifier with no known letter: K4 names no family against its shuffles; a ciphertext-autokey cell at p 0.001 (0231) did not replicate (0232, p 0.030), its margin coming from segment counts and the width-7 repeats themselves.

**C12. "Delve into that particular clock" (2014) against "the World Clock in Berlin"
(2025).** Readings: (a) the clock is plaintext content only; (b) the Weltzeituhr's
structure (24 time zones on a rotating ring, a compass-rose mosaic on the ground) is a
key: 24-letter alphabet, a rotating offset; (c) the 2014 steer was misdirection. Status:
Mengenlehreuhr readings dead (key schedules from its lamp counts, hours, minutes and time digits at any start and step: best 8 of 24, as shuffled coppers, 0079; joined to any K3-style move before or after the table, no fit, 0091); a cipher on the Weltzeituhr's 24-letter ring is excluded because K4 uses all 26 letters (0052); other Weltzeituhr readings untested. 2026-10-17: (b) the 24-zone ring laid over 26 letters as an offset with an unknown word: dead (0179).

**C13. "Two events... my second trip to Egypt in late 1986, and the fall of the Berlin
Wall."** (2025). Readings: (a) plaintext content: the words EGYPT, WALL, CAIRO, LUXOR,
TUTANKHAMUN, NOVEMBER; (b) keys: the same words. Status: as keyword alphabets for a periodic tableau, periods 1-52, nothing beyond the shuffled-copper rate (0053); other uses untested. Mirrored self-keys: the copper or the message read through a + b i mod 97, the mirror b = -1 included, as its own key: dead (0103, 0104). K4 read from behind the screen, line by line right to left, with periodic keys and autokeys: dead (0108).

**C14. "The codes of Kryptos from the morse code at the beginning through K5 are about
delivering a message."** (2025). Readings: (a) theme only; (b) MESSAGE, DELIVER, TRANSMIT
as keys; (c) K2's "last message" is the hinge. Status: (b) MESSAGE, DELIVER, DELIVERING, TRANSMIT as keyword alphabets for a periodic tableau, periods 1-52: nothing (0053); other uses untested.

**C15. "If they don't, then (CLUE) what's the point? Power resides with a secret, not
without it."** (open letter, August 2025; the FT called it "one final hint"). Readings:
(a) "point" as a compass point: the plaintext states a bearing or direction beyond EAST
NORTHEAST, or the key is a direction word; (b) "point" as the decimal point in K2's "six
point five"; (c) "the point" as the place on the grounds: "find that place"; (d) "point"
as a punctuation mark: the "?" or the X stop, Scheidt's "what's a period"; (e) POWER,
SECRET, RESIDES, WITHOUT as keys; (f) the parenthetical marks only that the sentence is a
clue to K5's theme. Status: (a) and (e) as keyword alphabets (the 32 compass points; POINT, POWER, RESIDES, WITHOUT, DIRECTIONS, BEARING) for a periodic key, ciphertext autokey or both: nothing beyond chance (0072); other readings untested. 2026-10-17: (b) six point five and the coordinates with the point, (d) the four ? and K2's ? and X stops, as numbers with an unknown word: dead (0180); (c) the place on the grounds: blocked without a survey.

**C16. "The final passage will lead in several directions. The word directions is, I use
intentionally."** (2010). Readings: (a) the plaintext contains compass directions (EAST,
NORTHEAST confirmed); (b) more directions follow; (c) "directions" as instructions.
Status: partly confirmed by the cribs. (c) 'directions' as reading routes: each of the 16 compass points as the direction a grid is read, and east then northeast in two stages: at the coppers' rate (0159).

**C17. "Whether it's 97, whether it's 100... I seem to like to manipulate the
information."** (2005). Readings: (a) disinformation; (b) the working text had nulls or
a different length before being cut to 97 (the doublets as nulls: dead, 0075); (c) the "?" counts. Family G. Status: (b) as hand padding of a K3-style grid (blanks at the top, or fillers carried through a second turn) before or after a periodic key: dead below period 22 (0082). Padding chosen separately at each grid stage (blanks at the start or end of the first or last row, or down a side column; dropped between grids or carried as dummies), one or two stages, periodic key 1-26: nothing live below 21, at the coppers' rate (0135). (a) and (b) bounded by 0009 (periodic key stretches) and 0031 (chained autokey, two-word composition): one letter inserted or deleted anywhere revives nothing; ciphertext autokey with one letter wrong, missing or extra is dead too (0068). One letter wrong through any type-1 move with a periodic key: nothing below period 14 (0093). One letter extra or missing, with any single move on 96 or 98 letters and a periodic key: nothing below period 20 (0094). One carved letter wrong at a known place, or missing or extra, through the exact free-alphabet periodic, Gromark, Hill and trifid verdicts: at the coppers' rate or dead (0147, 0150, 0151, 0152). 2026-10-20 (A1.2): two or three known letters slipped with a periodic key: on the sculpture's tables nothing below length 25, readings judged as copies' (0207); one free alphabet dead at 1-7 and 9, two at 1-3 and 9, the rest at the copies' rate and too loose to decide (0208, 0209).
parameter.

**C18. "Scheidt's 'a bit of stego'" and "I think there are 98 characters left."** (2004,
2005). Readings: (a) the plaintext is hidden among nulls; (b) a 98-character working
text including "?"; (c) an even length for a digraphic or 7x14 layout. Status: the 98-character reading is bounded by 0009 for periodic tableau keys; (b) and (c) as a 98-cell grid (7 x 14 among them) turned so the ? comes out first, with periodic keys or either autokey: dead (0086); other families untested.

**C19. "What's a period, because there's more than one sentence in there... special
characters don't work."** (Scheidt, 2015). Readings: (a) K4 has sentence breaks marked
by X or Q as in K2 and K3; (b) the breaks fall at structurally meaningful positions.
Constraint on the scorer: tolerate X and Q. Status: constraint. 2026-10-27 (A6.2): X-stop plants through the sampled searches: F1.1 L23 4 of 4, F1.2 L13 3 of 4, 0125 4 of 4 by quadgrams (0226).

**C20. "Layer two."** (K2, confirmed 2006). Readings: (a) a second layer of encryption
on K4; (b) fold the halves; (c) the second plate; (d) the tableau row two; (e) K5.
Status: (a) as a second stage: types 1 and 2 of directions.md, 0080-0099 and 0110-0116 (moves with periodic, autokey, running and clock keys; Hill with a periodic key), all dead or at chance; as two key words added, dead (0115). (b) the screen folded: dead as a positional key (0089). (c) the second plate as a running key: dead with the sculpture's texts (0017, 0090, 0117). (d) the tableau rows, row two among them, as repeating keys from every start on standard or KRYPTOS tables: at most 6 of 24 known letters, coppers 5-8 (0126, 0128). (e) K5 as key: blocked, no text. Hand schedules of a key word (skip, stutter, back and forth, triangle, square, restart per carved line): dead on standard and KRYPTOS tables (0127, 0128).

**C21. The extra L and HILL.** Readings: (a) Hill cipher (2x2 and 3x3 exhausted under
the alignments tested; affine, chaining, 4x4, shifting numberings, paired 2x2 open); (b)
a marker at row N, the first line of the lower-right plate, matching YAR on the first line
of the lower-left plate; (c) a production error (Sanborn omitted it from replicas; also
missing on Antipodes). Status: (a) 2x2, 3x3 and 4x4 Hill, plain and affine, dead under four numberings, all alignments and both directions (0015), under 124 vocabulary keyword numberings (0044) and under 200 numberings from K1-K3 words and the 2025 letter's words (0055); paired 2x2, chained Hill and larger blocks open. (b) untested. A Hill matrix with a periodic tableau key in either order ('matrix codes', then the table): dead where decidable (0116). 2026-10-17: (a) Hill 2x2 with any numbering of the letters: dead (0194); 3x3 has too few equations. (b) the extra L as a marker: closed by subsumption (0005, 0017, 0089).

**C22. The raised YAR / DYAHR / "1-2-3".** Readings: (a) a Gromark primer; (b) HYDRA
anagram, a keyword; (c) the column-extraction marker for K3 only (NSA's reading); (d)
Sanborn's reported "1-2-3" spacing as an ordering. Status: (a) as a Gromark primer is bounded by 0013 for every two-term lag rule under vocabulary alphabets: no rule fits the known shifts, whatever the primer; with any mixed alphabet at all, base 10, every rule with lags up to 6 and every primer, nothing fits (0069). (b) untested. (d) '1-2-3' as counting-off orders (1-2-3 and YAR's places 4-5-7, every order) before or after a periodic key: nothing below 26 (0166). 2026-10-17: (a) YAR as a primer: every primer enumerated (0076, 0195, 0196), dead. 2026-10-20: Gromark rules in bases 16-26 on the tables built from K1-K3's words: dead (0206).

**C23. The K2 coordinates, the USGS marker "no longer there," "an act I could have
carried out," "buried out there somewhere."** Readings: (a) riddle layer, out of scope;
(b) the digits 38 57 6 5 77 8 44 as a key or matrix; (c) the marker's crosshairs as the
compass-point reading of C15. Status: (b) as an additive digit key beside a word is dead for seven readings of the digits (0024); as a Hill matrix (2x2 and 3x3 from every window of the numbers and digits, both fills, four numberings) it recovers at most 4 of 24 known letters, below the best random matrices (7) (0060).

**C24. The compass rose "offset... there's a mystery there."** Readings: (a) the offset
angle is a shift value; (b) the lodestone direction names a word; (c) riddle layer.
Status: untestable without a surveyed bearing; record as such.

**C25. The Morse: VIRTUALLY INVISIBLE, DIGETAL INTERPRETATI..., SHADOW FORCES, LUCID
MEMORY, T IS YOUR POSITION, SOS, RQ, the E padding; INVISIBLE a palindrome; DIGETAL
misspelled.** Readings: (a) keywords; (b) the E counts as numbers; (c) "digital
interpretation" and "lucid memory" as instructions (binary; recall the key); (d) "RQ/YR"
upside-down as the orientation clue. Status: the Morse plaintexts as a running key, carved or reversed order, are dead (0017); as keywords untested in bounded form. 2026-10-17: (b) the E counts as numbers (runs and totals, both transcriptions) with an unknown word: dead (0175).

**C26. Antipodes differs from Kryptos only by the UUND/RTBJ spelling, the extra L, and
"the order is shifted a little"; "it's possible that you could crack the whole thing
from here, but it's also possible you couldn't."** Readings: (a) the extra L matters;
(b) the plate order matters; (c) the differences are decoys. Status: untested. 2026-10-17: (a) see C21(b); the RTBJ/ETBJ change as a key fragment closed by subsumption (0005, 0178); (b) the plate order blocked without Antipodes' layout.

**C27. The 2010 worksheets: "there might be revelations in there... I gave more than just
Berlin."** Readings: (a) the PALIMPCEST slip shows how he worked, one word at a time
against a repeating key written out underneath; (b) the BERLIN chart's layout shows the
97 as 31-character lines he counted on; (c) his tableau was "slightly different from the
one on Kryptos." Source for (c): Sanborn's email on the NYT page "Original Decoding Charts", 20 Nov 2010 (archived: https://web.archive.org/web/2011id_/http://www.nytimes.com/2010/11/21/us/21codecharts.html). It refers to the K1/K2 charts, and his own example letter works with the carved KRYPTOS alphabet, so the difference was probably the chart's layout, not its alphabet (prior-work report, 2026-10-15); this weakens the reasoning behind 0071. Status: (b) as one key shift per 31-character carved line added to a column word of length 2-31: dead (0088). Status: (c) as an alphabet one swap or one move from KRYPTOS, under a periodic key (periods 1-52) or ciphertext autokey (every lag): nothing beyond chance, no word in 16,671 fragments (0071); as any alphabet at all on both sides (Quagmire III with a free order), periodic key 1-26, no move: no alphabet fits at any length in the added form, only lengths 23 and 26 in the Beaufort form (0119), where an English climb leaves K4 inside the scrambled coppers at low power (0120); as two unknown alphabets (Quagmire IV): consistent only at lengths 8, 13, 16, 19, 20, 23, 24, 26, inside the coppers, the rare length 19 a coincidence of the known letters at about 1 in 40 (0123, 0124); with two or three slips at the known places, one unknown alphabet dead at 1-7 and 9, two at 1-3 and 9, the rest as copies (0208, 0209); one unknown alphabet after or before every type-1 move: no fit below 6, the rest at the coppers' rate (0129, 0130); two unknown alphabets after or before every type-1 move: no fit at lengths 1-2, the rest at the coppers' rate (0133; 0131 and 0132 incomplete); one unknown alphabet (Beaufort 23, 26) and two unknown alphabets (lengths 8, 13, 16) judged by English with a decider whose power was measured against planted texts' own scrambled copies: K4 inside its own copies each time (0140, 0142, 0144, 0146); a carved slip at 33 reviving K1/K2's own system at length 19: decider too weak there (0148); the rest untested; images in `../research_notes/sanborn_charts/`.

**C28. Stein's I.C. peak at m = 13 in both K1 and K2.** Reading: a 13-letter key or
structure overlaid; or an artefact. Status: on K4, a period-13 tableau key is dead under all 24 conventions for a plain periodic key (0005) and for a progressive key at every step (0011).

**C29. "P.S. It's as simple as ABC" (the keyword anagram), PALIMPSEST + ABSCISSA.**
Readings: (a) a joke; (b) a standard-alphabet step; (c) the combined keyword alphabet.
Status: as tableau alphabets for a periodic key, PALIMPSEST and ABSCISSA and every other vocabulary word are bounded by 0010 (forced key stretches read as noise); as key words, bounded by 0005.

**C30. Sanborn 2019: not necessary to know K1-K3 to solve K4; 2013: K5 cannot be solved
without K4.** Reading: the method stands alone; the content chains. Constraint on how
much weight C7 can carry. Status: noted.

## How the loop uses this

Before each experiment, pick the clue entries the hypothesis reads, state the reading by
letter, and after the run update the entry's status with the experiment tag. When all
readings of a clue are exhausted, say so here. Every few pivots, sort this file by
"untested" and start from the top.
