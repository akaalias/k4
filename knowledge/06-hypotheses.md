# 06. Hypotheses: what K4 could be, with the evidence

This is the file to argue with. Each family lists what the record says for it and
against it. Experiments should cite the lines here that they test.

## The constraints every hypothesis must respect

1. Letter-for-letter at the final step: Sanborn's N = B, Y = E account, and the
   verifier's positional check.
2. State changes between every adjacent position (QQ to NO, SS to ST, TT to IN).
3. No single-alphabet periodic additive key with period 1-26 or 30-52.
4. The cribs' three E's against the ciphertext's two.
5. Hand-executable in 1990 on a truck ride with paper, a chart and a tableau: "I spent
   hours conceiving of this when driving back from Arizona"; "the last thing I wrote was on
   that drive"; the encryption "was done by himself, during his trip to retrieve the
   petrified tree." The auction lot's "original coding system for K4" and "coding charts"
   mean there were worksheets.
6. Memorable years later with "the correct key word/s" (Scheidt), and recoverable from
   clues on the sculpture itself ("the keys were concealed at the sculpture"; "conveys not
   only the encrypted data, but also the key").
7. Likely one deliberate misspelling, X as a stop, maybe a Q as a question mark, no
   special characters ("special characters don't work").
8. Probably "more than one stage" (Scheidt), "five or six" techniques across the whole
   piece (Sanborn), of which four are known: Morse, keyed Vigenère twice, transposition.
   So K4 adds one or two.

## Family A. Matrix transposition stages, then the tableau

**For.** Sanborn's clearest method statement, CNN 2005, pointing at the tableau: "I used a
matrix code, and then we can possibly use this code to decipher with. So it was a variety
of systems. And sometimes I used double matrixes and triple matrixes in order to develop a
complicated system, and then went back to this table to do the ultimate." He defines a
matrix code as writing the text in rows and reading it top to bottom. His 2003 remark:
"surprised that no one had tried recovering the original matrix and running it through
all the possible shifts." K3 is a matrix (transposition); K1 and K2 are the table. Order
matters: transposition first, keyed substitution last, keeps the final step one-to-one,
which is what he described for BERLIN. The 1990 Post: half by the tableau, half by "a
modern system created for the project." Scheidt: "building layers... mix and match."
Bauer: "firmly rooted in the world of paper and pencil encryption."

**Against.** Bean's statistics favour no transposition (the KRYPTOS-letter closeness and
the repeated-letter closeness survive a transposition only if the transposition is applied
before a substitution that has the closeness property, which this family allows). The NSA
guessed the reverse order. Gillogly and Schridde judged "combined transposition and
polyalphabetic" unlikely after the cribs, but that judgment assumed the cribs constrain
the transposition directly.

**How to test.** The cribs then constrain the substitution stage, not positions. For a
keyed-tableau last stage with period p, the key letter at each crib position is forced;
the transposition stage must bring plaintext letters into those positions such that the
forced key letters form a period-p key. Search small matrix routes (widths 7, 14, 21, 24,
31; the 4x86-style incomplete fills; "double and triple" compositions) against periods
that the forced key letters admit, scoring the key for being a word from the vocabulary.

## Family B. Masked plaintext, then a simple keyed cipher

**For.** Scheidt, five times over twenty years: "I masked the English language"; "the
masking technique may not be known"; "you need to solve the technique first and then go
for the puzzle"; "more than one stage"; "if you can change the language base then it
becomes in my favor." His examples of masks: a different number base ("this is base 2 we
could move to base 16"), an extinct language (refused), "a bit of stego." NPR 2005's
guesses (nulls, phonetic spelling) are a reporter's. Sanborn's "Who says it is even a math
solution?" and "I can employ methods that don't have anything to do with mathematics."

**Against.** Sanborn did not recognize the term "masking technique" in 2019, so the mask
may be Scheidt's name for something Sanborn thinks of differently (a matrix? a visual
system?). A mask that changes the alphabet size would break letter-for-letter at the end.

**How to test.** Stage-one outputs are not English; score them on crib consistency and on
structure (period sweeps, I.C. of residues), not on quadgrams. Candidate masks that keep
26 letters: a keyed monoalphabet applied before a Vigenère (equivalent to Quagmire IV);
abbreviation or vowel-dropping before encryption (changes letter counts: three E's in cribs
means the mask did not drop E's at those positions); nulls inserted at a rule.

## Family C. A key assembled from parts, Scheidt's professional habit

**For.** Constructive Key Management is his life's work: several secret splits combined
into one working key, with labels telling you which parts apply. "Part of the code was
designed to be solved with multiple keys." "The 'key' is the algorithm." "Some of the
code was designed to work with multiple keys." Gillogly in 1999: "Given Scheidt's interest
in key escrow, I'd expect the key to be hidden in there for somebody who knows what to
look for"; in 2013, Scheidt's interest in duress ciphers, "multi-layered ciphers for which
you can give up a key to the enemy that produces credible plaintext." Sanborn: "rife with
mistakes on purpose"; "if it can be deciphered exactly"; and Bean's charitable reading
that there may be two solutions.

**Against.** No specific second component has ever been identified.

**Candidates for the second component.** The extra L's position (row N, first line of
the lower-right plate); the raised YAR (first line of the lower-left plate) and the DYAHR
"1-2-3" spacing Sanborn reportedly mentioned; the Morse E-padding counts; the K2
coordinates as digits (38 57 6.5 77 8 44); the four error coordinates Bauer computed; the
K1-K3 keywords themselves (PALIMPSEST, ABSCISSA, KRYPTOS, and their anagram "P.S. It's as
simple as ABC"); "LAYER TWO."

## Family D. Sanborn's "visual" and "spatial" systems

**For.** "I like to use spatial systems of encoding and decoding" (1999). "Encoding
systems which use pattern, light and shadow." "Visual systems for encoding, which are much
harder for cryptographers to crack because they're individualistic." "Having the letters
sitting there in plain sight is a pretty big clue... I work with light and shadow... smoke
and mirrors." The tableau is "intentionally flipped so it can only be read from the back."
Sanborn's archaeology-by-raking-light habit. "They're important" of the misaligned
letters; "positioning" of the misspellings. "The front-entrance pieces were supposed to
parallel something in the courtyard." "Something that was key is no longer there" (the
USGS marker). The compass dial is "offset... there's a mystery there."

**Against.** Every one of these is interpretive. Scheidt insists the system is a
classical hand cipher, and Sanborn's actual worksheets for K1-K2 are ordinary Vigenère
tables.

**How to test.** Treat the carved object as the key source: read the tableau mirrored;
read the ciphertext through the tableau's grid positions (the K4 lines sit opposite
tableau rows N-Z); use row N's extra L and the HILL column as indices; use the four
misspelling coordinates; use the K3 column key 0362514 as a K4 transposition key.

## Family E. Numeric running key: Gromark, Vimark, LFSR

**For.** Bean's statistical case (one-to-one, cipher alphabet near standard, flat I.C.,
width-21 repeats reproduced by even-base five-digit primers). "Pencil-and-paper field
cipher," "provided agents or pilots in case of capture," "more than one stage" (primer
expansion then substitution). The raised DYAHR as a five-digit primer.

**Against.** Base 10 length 5 is exhausted. Sanborn is an "anathemath." Gromark is
error-prone by hand. The KRYPTOS-letter closeness is explained equally by a keyed
alphabet near the standard one in other systems.

**Open.** Other bases (3-9, 11+), other primer lengths, non-standard expansion rules,
Vimark at base 26, LFSR period 63 or 84, primers derived from YAR, the coordinates, or
the error positions.

## Family F. Keyed periodic systems at the surviving periods

**For.** Cheap, bounded, and nobody has published it. Quagmire I, II, IV with separate
plain and cipher alphabets, progressive key, and periods 27-29 and 53+ all survive the
crib sweep. A period of 31 matches the carved line width but is excluded for additive
single-alphabet systems; separate-alphabet Quagmires at 31 are not yet excluded.

**Against.** A 27-plus letter key is not "can be remembered" unless it is a phrase from
K1-K3, which is a running key, which Gillogly and Schridde found gives nonsense.

## Family G. Something is wrong with the copper

**For.** K2 lost a letter; UNDERGRUUND is a transcription slip; Scheidt never checked K4;
"since he's the one who had the chisel in his hands, there could be some changes"; the NSA
asked outright whether K4 is missing a letter; Bean wonders whether Sanborn "accidentally
made solution impossible." Sanborn: "Whether it's 97, whether it's 100, I seem to like to
manipulate the information."

**Against.** Sanborn is "certain that he got it right" and Scheidt "confident" (2005). The
verifier string is 97 letters.

**How to use.** Not a family to search, but a parameter: every family should be tested
once more with one letter inserted or deleted at each position, and with the "?" included.

## Cross-cutting: where the keys come from

In order: words and anomalies from K1-K3 (IQLUSION, UNDERGRUUND, DESPARATLY, LAYERTWO,
PALIMPSEST, ABSCISSA, WW, the coordinates, "can you see anything," and Carter's absent
reply "wonderful things"); the sculpture's own text (KRYPTOS, the Morse words, HILL, YAR,
DIGETAL); Sanborn's named themes (BERLIN, CLOCK, WELTZEITUHR, ALEXANDERPLATZ, EGYPT,
CARTER, the Wall, SHADOW, TEHb); only then generic lists. Sanborn in 2006: getting K1-K3
right "is crucial"; in 2019: not necessary. Read together: they supply key material, not
the method.

## Open questions nobody has answered

- What is "the most obvious key to the sculpture" that "nobody has picked up on" (2005)?
- What are the "instructions in the earlier text that refer to later text"?
- Why did Sanborn use the same system twice (K1, K2) when he had several? Scheidt: "a
  Jim's call."
- What did Sanborn mean by the misspellings' "orientation" and "positioning"?
- What is the "(CLUE)" in the 2025 open letter: "If they don't, then (CLUE) what's the
  point? Power resides with a secret, not without it"?
- What does "LAYER TWO" designate?
- What did Scheidt's "bit of stego" do?
- Why "directions," which Sanborn said he used intentionally, given EAST and NORTHEAST?
