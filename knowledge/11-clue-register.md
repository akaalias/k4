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
sweep bounds. Status: (c) bounded by 0005 (composed period) and 0014 (two words of total length under 25 cannot compose to the forced key). (a) and (c) together, a repeating key before and after K3's rule, a grid turn, two turns or a column shuffle, key lengths 2-14 each, one alphabet: dead (0080). (a) bounded by 0006: columnar routes (plain, keyed, double plain) before a periodic tableau admit no key shorter than 23; a fixed reshuffle of every row of seven, before or after the tableau, admits none shorter than 25 beyond chance (0070); route transpositions and triple stages untested. (c) untested.

**C2. "No one has recovered the original matrix... surprised that no one had tried
recovering the original matrix and running it through all the possible 'shifts'."**
(Sanborn, 2003, secondhand). Readings: (a) K3's true matrix is not the NSA's 4x86 but a
different grid whose other "shifts" (rotations, offsets, start positions) produce K4; (b)
"shifts" are the 26 row shifts of the tableau, and the matrix is the K1-K2 worksheet
(the "K1/K2 matrix" he "seemed mystified no one has gotten any thing more from"); (c) a
Hill-style numeric matrix. Experiments: recover every grid that reproduces K3 (widths 7,
8, 14, 21, 24, 28, 42, 48, 86; Bauer's double rotation; Stehle's 192 rule), then apply
each grid's family of shifts to K4 before and after tableau substitution. Status:
0006 covered plain columnar at every width including the K3 widths, before the tableau; 0008 covered reading (a) in full for the K3 rule at every shift and for double grid rotations, before the tableau: no shift admits a tableau key shorter than 22. With a repeating key on both sides of the K3 rule at every shift, key lengths 2-14 each: dead (0080). Three quarter turns at every width triple, then or before a periodic key 1-26: dead (0083). The after-tableau order is weakly bounded by 0007. Reading (b) untested.

**C3. "I like to use spatial systems of encoding and decoding... pattern, light and
shadow... visual systems... individualistic."** (1999, 2005). Readings: (a) a route
through the carved grid (31-wide lines, the four plates) rather than an abstract matrix;
(b) the tableau read mirrored, as it reads from behind; (c) positions of the physical
anomalies as the key. Experiments: family D. Status: untested.

**C4. "I masked the English language... the masking technique may not be known... you
need to solve the technique first and then go for the puzzle... more than one stage."**
(Scheidt, 2005, 2015). Readings: (a) a plaintext transform before a keyed cipher; (b) a
non-standard alphabet or base ("base 16," "Mayan... base 60"); (c) "stego": the English is
hidden inside something readable; (d) the mask is what Sanborn calls a matrix. Family B.
Status: masks that only move or pad letters (reversal, regular nulls, prefix nulls) before a periodic tableau are dead (0023); writing the message into a grid along a snake, spiral or diagonal path and reading it along another, with a periodic key before or after, is dead below period 21 (0092); nulls chosen by letter (every copy of one or two letters outside the cribs) behave like random strike-outs of the same size (0057); masks that change letters by an affine map of either alphabet (decimations, Atbash), before or after a periodic key or ciphertext autokey, are dead (0074); other letter-changing masks untested.

**C5. "Not mathematical... simple, can be remembered, and executed years later when used
with the correct key word/s... similar to what would be provided agents or pilots in
case of capture."** (Scheidt, 2011). Readings: (a) keyword-driven classical system,
no primers or arithmetic; (b) "key word/s" plural: two keywords, as K1 and K2 each had
KRYPTOS plus one; (c) a duress code: two valid readings. Constraint on every family.
Status: constraint.

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
anything." Key-source rule plus families C and D. Status: as a running key, K1-K3 plaintexts and ciphertexts (0004), the sculpture's own texts (0017) and Carter's book (0021) are dead at every offset; as key words, the K1-K3 vocabulary is dead for periodic keys (0005, 0009-0011). Other readings untested.

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
the letters' direction, upside down (RQ reads YR). Status: (a) the misspelt letters QUA, the corrections LOE (with and without the dropped E) as a short second key added to any word: best 8 of 24 known letters, against 7-11 on shuffled coppers (0061); index readings untested.

**C11. "The other 91 characters and their proper order are yet to be determined."**
(NYT 2010 wording). Reading: a reordering step exists. Supports C1(a). Status: noted.

**C11a. NSA 1992: "plain-text auto-key" and "interval 7"; NSA 2007: plaintext and ciphertext
autokey tested without cribs.** Status: 'plain-text auto-key' joined to a K3-rule, grid-turn or columnar move, either order, every lag, one alphabet: dead (0081). 'interval 7' as a structure that lines doublets up in sevens: only ciphertext autokey at lag 1 with a period-7 key raises the doublet column, to 1.5% against 0.1-0.3% by chance (0065); ciphertext autokey at lag 1 with a period-7 key, and at lag 21 with any period, is dead under the cribs (0066). 'plain-text auto-key' is dead at lags 1-25 and 30-52 and gives noise at 26-29 (0003, 0012); 'interval 7' as a period is dead under plain and progressive keys (0005, 0011) and as an autokey lag (0012). The substitution-then-transposition order is weakly bounded by 0007.
and lags 1-96 (0002). Plaintext autokey excluded at lags 1-11 and 30-52, undecided at 13-29 and 53-96, lag 12 consistent under one convention on a single check (0003). Any mixed alphabet at all, unknown: with the sculpture's running keys, no fit (0098); with a periodic key 3, 7 or 21 after or before a type-1 move, at the scrambled-copper rate, one marginal cell at period 3 (0097).

**C12. "Delve into that particular clock" (2014) against "the World Clock in Berlin"
(2025).** Readings: (a) the clock is plaintext content only; (b) the Weltzeituhr's
structure (24 time zones on a rotating ring, a compass-rose mosaic on the ground) is a
key: 24-letter alphabet, a rotating offset; (c) the 2014 steer was misdirection. Status:
Mengenlehreuhr readings dead (key schedules from its lamp counts, hours, minutes and time digits at any start and step: best 8 of 24, as shuffled coppers, 0079; joined to any K3-style move before or after the table, no fit, 0091); a cipher on the Weltzeituhr's 24-letter ring is excluded because K4 uses all 26 letters (0052); other Weltzeituhr readings untested.

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
clue to K5's theme. Status: (a) and (e) as keyword alphabets (the 32 compass points; POINT, POWER, RESIDES, WITHOUT, DIRECTIONS, BEARING) for a periodic key, ciphertext autokey or both: nothing beyond chance (0072); other readings untested.

**C16. "The final passage will lead in several directions. The word directions is, I use
intentionally."** (2010). Readings: (a) the plaintext contains compass directions (EAST,
NORTHEAST confirmed); (b) more directions follow; (c) "directions" as instructions.
Status: partly confirmed by the cribs.

**C17. "Whether it's 97, whether it's 100... I seem to like to manipulate the
information."** (2005). Readings: (a) disinformation; (b) the working text had nulls or
a different length before being cut to 97 (the doublets as nulls: dead, 0075); (c) the "?" counts. Family G. Status: (b) as hand padding of a K3-style grid (blanks at the top, or fillers carried through a second turn) before or after a periodic key: dead below period 22 (0082). (a) and (b) bounded by 0009 (periodic key stretches) and 0031 (chained autokey, two-word composition): one letter inserted or deleted anywhere revives nothing; ciphertext autokey with one letter wrong, missing or extra is dead too (0068). One letter wrong through any type-1 move with a periodic key: nothing below period 14 (0093). One letter extra or missing, with any single move on 96 or 98 letters and a periodic key: nothing below period 20 (0094).
parameter.

**C18. "Scheidt's 'a bit of stego'" and "I think there are 98 characters left."** (2004,
2005). Readings: (a) the plaintext is hidden among nulls; (b) a 98-character working
text including "?"; (c) an even length for a digraphic or 7x14 layout. Status: the 98-character reading is bounded by 0009 for periodic tableau keys; (b) and (c) as a 98-cell grid (7 x 14 among them) turned so the ? comes out first, with periodic keys or either autokey: dead (0086); other families untested.

**C19. "What's a period, because there's more than one sentence in there... special
characters don't work."** (Scheidt, 2015). Readings: (a) K4 has sentence breaks marked
by X or Q as in K2 and K3; (b) the breaks fall at structurally meaningful positions.
Constraint on the scorer: tolerate X and Q. Status: constraint.

**C20. "Layer two."** (K2, confirmed 2006). Readings: (a) a second layer of encryption
on K4; (b) fold the halves; (c) the second plate; (d) the tableau row two; (e) K5.
Status: untested.

**C21. The extra L and HILL.** Readings: (a) Hill cipher (2x2 and 3x3 exhausted under
the alignments tested; affine, chaining, 4x4, shifting numberings, paired 2x2 open); (b)
a marker at row N, the first line of the lower-right plate, matching YAR on the first line
of the lower-left plate; (c) a production error (Sanborn omitted it from replicas; also
missing on Antipodes). Status: (a) 2x2, 3x3 and 4x4 Hill, plain and affine, dead under four numberings, all alignments and both directions (0015), under 124 vocabulary keyword numberings (0044) and under 200 numberings from K1-K3 words and the 2025 letter's words (0055); paired 2x2, chained Hill and larger blocks open. (b) untested.

**C22. The raised YAR / DYAHR / "1-2-3".** Readings: (a) a Gromark primer; (b) HYDRA
anagram, a keyword; (c) the column-extraction marker for K3 only (NSA's reading); (d)
Sanborn's reported "1-2-3" spacing as an ordering. Status: (a) as a Gromark primer is bounded by 0013 for every two-term lag rule under vocabulary alphabets: no rule fits the known shifts, whatever the primer; with any mixed alphabet at all, base 10, every rule with lags up to 6 and every primer, nothing fits (0069). (b) untested.

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
upside-down as the orientation clue. Status: the Morse plaintexts as a running key, carved or reversed order, are dead (0017); as keywords untested in bounded form.

**C26. Antipodes differs from Kryptos only by the UUND/RTBJ spelling, the extra L, and
"the order is shifted a little"; "it's possible that you could crack the whole thing
from here, but it's also possible you couldn't."** Readings: (a) the extra L matters;
(b) the plate order matters; (c) the differences are decoys. Status: untested.

**C27. The 2010 worksheets: "there might be revelations in there... I gave more than just
Berlin."** Readings: (a) the PALIMPCEST slip shows how he worked, one word at a time
against a repeating key written out underneath; (b) the BERLIN chart's layout shows the
97 as 31-character lines he counted on; (c) his tableau was "slightly different from the
one on Kryptos." Source for (c): Sanborn's email on the NYT page "Original Decoding Charts", 20 Nov 2010 (archived: https://web.archive.org/web/2011id_/http://www.nytimes.com/2010/11/21/us/21codecharts.html). It refers to the K1/K2 charts, and his own example letter works with the carved KRYPTOS alphabet, so the difference was probably the chart's layout, not its alphabet (prior-work report, 2026-10-15); this weakens the reasoning behind 0071. Status: (b) as one key shift per 31-character carved line added to a column word of length 2-31: dead (0088). Status: (c) as an alphabet one swap or one move from KRYPTOS, under a periodic key (periods 1-52) or ciphertext autokey (every lag): nothing beyond chance, no word in 16,671 fragments (0071); otherwise untested; images in `../research_notes/sanborn_charts/`.

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
