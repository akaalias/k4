# 12. Assumptions register

What the project takes for granted: assumptions built so deep into the harness, the scorer
and the order of work that no experiment tests them. Each entry names its source and who
chose it (the creators, the record, or us), how firm it is, what would weaken it, which
results stand on it, and the cheapest check. Started 2026-10-16 (issue #52); entries are
discussed with Alexis one at a time before any becomes loop work.

Firmness: `firm` (the record never contradicts it), `contested` (the record contradicts
itself), `ours` (a working choice with no creator source).

Order of work, decided by Alexis 2026-10-16: nothing here becomes loop work until the current
queue in `order-of-work.md` is exhausted. Then, in this order:

1. A3 first: a positive control for every closed item (plant a message under the item's own
   method and key, run its own search, require it to be found). It says how far the closed
   results can be trusted before anything else is built on them. (Proposed by Claude; Alexis
   delegated the decision, 2026-10-16.)
2. A1: tolerance for slips and missed known letters, together with a tolerant English judge, an
   LLM scoring blind against the scrambled coppers' candidates, with power measured on planted
   damaged English and built in the harness (issue 11). Relaxed tests produce more noisy
   candidates and need a judge that can sort them.
3. A13 and A6, with the same judge.

Not scheduled, recorded so they are not lost: A5, A8, A11 and A12 have no check yet (A11 is
partly answered by F12, Stein's way, which lets observations propose items); three options from
the same discussion stay open: F7's fingerprints as the search itself rather than a check, new
creator material (issue 9: Scheidt's patents, declassified field-cipher manuals), and publishing
the bounded negative result if the sweep ends without a lead.

## The three that carry the most weight

**A1. The encipherment was carried out without a mistake.**
Every exact result ("no setting gives the 24 known letters") assumes Sanborn enciphered all
97 letters by hand with no slip: no wrong tableau row, skipped column or step out of order.
Source: ours, never stated. Firmness: ours, and doubtful. Sanborn: "Saying I was sloppy is
a good way of saying it" (2005); K1-K3 carry known errors (UNDERGRUUND, the letter dropped
from K2, the PALIMPCEST worksheet; `01-facts.md`). Weakened by: the K1-K3 error rate itself,
which puts at least one slip in 97 letters within reach. Stands on it: every `closed · exact`
leaf. Tested so far: one carved letter wrong, missing or extra, through the move library
only (0093, 0094). Cheapest check: rerun the strongest closed families (F1 periodic, F6
move-then-table) allowing one or two of the 24 known letters to miss, or one execution slip,
against scrambled coppers under the same tolerance.

**A2. The known letters stand exactly where stated, letter for letter, at the last step.**
EASTNORTHEAST at 22-34 and BERLINCLOCK at 64-74 are fixed constraints in every test.
Source: Sanborn's clues (2010, 2014, 2020), given as ciphertext strings, not numbers: FLRV is
EAST, QQPRNGKSS NORTHEAST, NYPVTT BERLIN, MZFPK CLOCK (`01-facts.md`), so they do not depend
on where K4 starts (A4). Two parts with different firmness. The plaintext positions are firm:
Sanborn vets claims by position ("What do you have in letter-position 27?", `01-facts.md`).
The alignment, carved letter i becoming plaintext letter i, is contested; F6 already tests
the reading without it (a move first, the known letters defined on the final text), for the
moves in its library. Firmness: contested. "One-to-one" was affirmed
at dinners (2011, 2013) and walked back in 2019 to "97 characters and BERLIN at 64"
(`04-structure.md`, `09-contradictions.md`); Sanborn on his own clues: they "work in a sort
of disinformational way" (2005). Weakened by: any reading where the clue positions hold on
an intermediate text, or only approximately. Stands on it: every result in the record, and
the exclusion of fractionating systems (VIC and straddling checkerboards, fractionated Morse,
Nihilist), which are out only while A2 holds (issue #51). Cheapest check: list which closed
results survive the 2019 reading ("BERLIN at 64" only).

**A3. A negative result is correct.**
"Closed" means our code searched the space and found nothing. The primitives in
`kryptos.ciphers` are verified on K1-K3, but each experiment's enumeration, pruning and
shortcuts are not. A bug that discards the true key looks exactly like a negative result,
and nothing ever checks a negative. Source: ours. Firmness: ours. Of 138 experiments, 19
mention a planted text at all. Stands on it: every `closed` leaf. Cheapest check: a
positive control per closed item: plant a message under that item's method and key, run the
item's own search, and require it to be found.

## The object

**A4. The ciphertext is these 97 letters.**
OBKR...UEKCAR, as transcribed, with the "?" before OBKR outside it. Source: the record.
Firmness: firm in substance, with choices at the edges. Scheidt said 98 (2005); Sanborn
"whether it's 97, whether it's 100" (2005); the "?" shares the carved line. Kobek on the
leaked plaintext: "exactly the right length" (2025), which supports 97. Weakened by: a
reading that counts the "?" or a boundary letter. Stands on it: all position arithmetic,
every period and width. Tested: the "?" as a 98th symbol in the move library (F6).

**A5. K4 is one self-contained message.**
Everything needed is in the 97 letters plus a short key. Source: ours. Firmness: ours. K5
uses a "similar but not identical" system with BERLINCLOCK at the same positions; Sanborn
speaks of a riddle, an act and a location (`09-contradictions.md`). Weakened by: a key or
step drawn from the site, the sculpture's physical layout, or K5. Stands on it: the whole
key-source order (`families.md`). Partly tested: F4 (the plates as a key, the screen).

**A6. The plaintext reads as English to our scorer.**
The leak makes English near certain: "this is in English... It makes semantic sense"
(Kobek, 2025). What is assumed is narrower: that the text looks like Carter's prose to a
quadgram model. Scheidt "masked the English language" (2005, 2015). Firmness: firm that it
is English; ours that it scores as English. Weakened by: masking, abbreviation, spelled
numbers, X separators, deliberate misspellings. Stands on it: every sampled result, every
English climb, F1.5's decider, the scrambled-copper comparison wherever it uses the English
score. See A13.

## The method

**A7. One procedure, applied the same way to all 97 letters.**
Source: ours. Firmness: ours. Sanborn: "five or six" techniques (2005); coding systems he
"could then modify in a myriad of ways" (2009). Weakened by: a method that changes partway
through, a key restarted by a rule, a step applied to part of the text. Stands on it: nearly
every family. Tested: a key restarted at each carved line (F1.4), at every word (0101).

**A8. It is a cipher in the textbook sense: letters and a key in, letters out.**
Source: ours. Firmness: contested. Scheidt: "not mathematical" (2011); Sanborn: "Who says it
is even a math solution?" (2025) and his "visual systems" (2005). Weakened by: a physical,
visual or procedural step with no clean algebra. Stands on it: the whole harness. Partly
tested: F4.

**A9. The method is in the public literature.**
The families are drawn from the textbooks and the ACA's list. The only real limit is that
the creators had the method in 1990: from the literature, from agency practice, or of their
own invention. Source: ours; criterion (4) of the success definition says "a hand procedure
of 1990", which builds it in. Firmness: ours, and weak. Chaocipher (1918) stayed secret
until 2010; hand ciphers kept being invented after 1990. Stands on it: the family map.
Partly addressed: F10, F11 (issue #51). Invented methods cannot be listed; F7's fingerprints
are the check that does not need a name.

**A10. The alphabet is fixed for the whole message.**
Every family uses a fixed alphabet with a changing key. Source: ours. Firmness: ours.
Weakened by: Chaocipher, the Wheatstone cryptograph and every cipher whose table changes
state after each letter. Addressed by F10.

## How we search

**A11. The answer lies where the known letters can decide it.**
Work goes where an exact test exists; what the 24 letters cannot decide is marked
`blocked` and leaves the queue. Source: ours (the order of work ranks by creator statements
and cost). Firmness: ours. Scheidt designed K4 to last ("difficulty nine out of ten"), which
points away from the regions that are easy to check. Stands on it: the order of work.
Nothing in the ranking pulls toward what is hard to check.

**A12. The creator statements we rank by are accurate and are about K4.**
Source: the record. Firmness: contested. `09-contradictions.md` lists more than a dozen
direct contradictions, and two disinformation remarks. C1's "matrix codes... then went back
to this table", the basis for F6's rank, was said pointing at the tableau about the whole
sculpture. Stands on it: the ranking. The same goes for this knowledge base: a distilled,
secondhand record, often through Bean, whose errors pass into every experiment unless the
primary source in `sources/` is opened.

**A13. The right decryption, when we hold it, will look right.** (Alexis, 2026-10-16)
Candidates with all 24 known letters in place and gibberish around them are discarded when
their English score sits inside the scrambled coppers'. If the masking came before the
encryption, the true decryption is masked English: right method, right key, odd text, and a
score like noise. Source: ours. Firmness: ours. Does not touch: the exact results (those
settings never produce the known letters) or the carved text itself (its flat statistics,
`04-structure.md`, rule out English read straight or transposed). Stands on it: every sampled
result, every blocked cell that fits at the coppers' rate, every discarded 24-of-24
candidate. Cheapest check: collect every 24-of-24 candidate from the experiments' `raw.json`
and test for structure other than fluent English (English letter frequencies out of order,
regular X separators, English after a simple unmasking such as reversal, dropping every nth
letter or an affine shift), against the coppers' candidates under the same tests.

**A14. The known words are only content.** (Alexis, 2026-10-16)
EAST, NORTHEAST, BERLIN and CLOCK are treated as words of the message and nothing more.
Source: ours. Firmness: ours. Sanborn: "The final passage will lead in several directions.
The word directions is, I use intentionally" (2010, C16). Other readings: (a) an instruction
for the method, for instance "east, then northeast" as the route through a grid (rows, then
up the diagonals); C16(c) records "directions as instructions" and it has never been tested;
(b) a number: east-northeast is a bearing of 67.5 degrees, point 6 of 32, point 3 of 16;
direction words were tried as keyword alphabets only (C15, 0072); (c) the clock as a
mechanism: the Mengenlehreuhr readings are dead (0079, 0091), and the Weltzeituhr named in
2025 is excluded only as a 24-letter cipher alphabet (0052), not as a rotating offset over 26
letters (C12(b)); (d) a marker where one stage or part of the message ends (see A7); (e) a
pointer outside the text, which is the riddle layer and out of scope unless it feeds the key.
Stands on it: the key-source order and every family's key list. Cheapest check: (b) as
numeric keys, exact and cheap like F3.2; (a) as routes added to the F6 move library.
