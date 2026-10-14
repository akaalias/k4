# 01. Facts: the object

## The installation

Kryptos is a two-part work on the grounds of CIA headquarters, Langley, Virginia.
Commissioned November 1988 through the GSA Art-in-Architecture program for $250,000.
Dedicated November 3, 1990 (the CIA's Intellipedia page says November 1; Webster's
dedication remarks are dated November 5; take November 3 as canonical). Built over two and
a half years in a warehouse in northeast Washington with assistants, chiefly David Sheldon,
using jigsaws to cut every letter through half-inch copper.

**Part one, the entrance.** Two tilted red-granite "pages" flank the walkway from the
parking deck of the New Headquarters Building, with a copper sheet sandwiched between them,
cut with International Morse code. A nearby granite slab carries an engraved compass rose
whose needle points at a lodestone. Sanborn says the dial is deliberately offset from north
("there's a mystery there"). No surveyed bearing exists; estimates range from about 220
degrees to "parallel to the sidewalk." Do not treat "the compass points east-northeast" as
a fact.

**Part two, the courtyard.** In the northwest corner of the courtyard between the New and
Original Headquarters Buildings, outside the cafeteria. An eleven-foot column of petrified
wood (from Holbrook, Arizona) supports an S-shaped screen of four copper plates, about
twelve feet high and twenty feet wide, curling around a small bubbling pool with a pump.
Nearby, a calm reflecting pool lies between two blank granite outcrops and tall grasses.
The K4 section of the screen is, in Sanborn's words to the FT, "largely and purposefully
obscured by a rock," and the stones were placed so that no single photograph captures all
the elements.

**The screen.** Viewed from the courtyard with the petrified tree on the viewer's left, the
left half carries ciphertext (two plates of 14 lines; 869 characters: 865 letters and four
question marks) and the right half carries the tableau (two plates of 14 lines; 867
letters). The letters are cut through, so every letter reads from both sides, mirrored on
one of them. The CIA says the tableau "is intentionally flipped so it can only be read from
the back of the sculpture." The CIA's figure of 1,735 letters does not match the transcript
count of 1,732; work from the transcript.

## The ciphertext side, as carved

```
Upper-left plate (K1 lines 1-2, K2 lines 3-14)
EMUFPHZLRFAXYUSDJKZLDKRNSHGNFIVJ
YQTQUXQBQVYUVLLTREVJYQTMKYRDMFD
VFPJUDEEHZWETZYVGWHKKQETGFQJNCE
GGWHKK?DQMCPFQZDQMMIAGPFXHQRLG
TIMVMZJANQLVKQEDAGDVFRPJUNGEUNA
QZGZLECGYUXUEENJTBJLBQCRTBJDFHRR
YIZETKZEMVDUFKSJHKFWHKUWQLSZFTI
HHDDDUVH?DWKBFUFPWNTDFIYCUQZERE
EVLDKFEZMOQQJLTTUGSYQPFEUNLAVIDX
FLGGTEZ?FKZBSFDQVGOGIPUFXHHDRKF
FHQNTGPUAECNUVPDJMQCLQUMUNEDFQ
ELZZVRRGKFFVOEEXBDMVPNFQXEZLGRE
DNQFMPNZGLFLPMRJQYALMGNUVPDXVKP
DQUMEBEDMHDAFMJGZNUPLGEWJLLAETG

Lower-left plate (K3 lines 1-11, K4 from OBKR)
ENDYAHROHNLSRHEOCPTEOIBIDYSHNAIA     Y, A, R raised about 1 cm
CHTNREYULDSLLSLLNOHSNOSMRWXMNE
TPRNGATIHNRARPESLNNELEBLPIIACAE
WMTWNDITEENRAHCTENEUDRETNHAEOE
TFOLSEDTIWENHAEIOYTEYQHEENCTAYCR
EIFTBRSPAMHHEWENATAMATEGYEERLB
TEEFOASFIOTUETUAEOTOARMAEERTNRTI
BSEDDNIAAHTTMSTEWPIEROAGRIEWFEB
AECTDDHILCEIHSITEGOEAOSDDRYDLORIT
RKLMLEHAGTDHARDPNEOHMGFMFEUHE
ECDMRIPFEIMEHNLSSTTRTVDOHW?OBKR
UOXOGHULBSOLIFBBWFLRVQQPRNGKSSO
TWTQSJQSSEKZZWATJKLUDIAWINFBNYP
VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
```

## K4

```
OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR

 1-10  OBKRUOXOGH
11-20  ULBSOLIFBB
21-30  WFLRVQQPRN
31-40  GKSSOTWTQS
41-50  JQSSEKZZWA
51-60  TJKLUDIAWI
61-70  NFBNYPVTTM
71-80  ZFPKWGDKZX
81-90  TJCDIGKUHU
91-97  AUEKCAR
```

97 letters. Sanborn's count is 97 ("exactly 97 characters", 2019; "a 97-character
phrase", 2020). The "?" before OBKR is on the same carved line; Sanborn told CNN in 2005
"It's a question mark." The 98 figure comes from counting it, and from Scheidt's 2005
"I think there are 98 characters left." On the carved plate K4 occupies the last four
characters of K3's eleventh line and then three full 31-character lines.

### The four clues

| Positions | Ciphertext | Plaintext | Released | How |
|---|---|---|---|---|
| 22-25 | FLRV | EAST | April 2020 privately, public August 24, 2020 | Email to solvers; John Schwartz tweet |
| 26-34 | QQPRNGKSS | NORTHEAST | January 29, 2020 | New York Times, billed as the final clue |
| 64-69 | NYPVTT | BERLIN | November 20, 2010 | New York Times, twentieth anniversary |
| 70-74 | MZFPK | CLOCK | November 20, 2014 | New York Times, 25th anniversary of the Wall's fall |

Twenty-four letters fixed. Sanborn's own verification has always been positional: in 2010
a friend asked claimants "What do you have in letter-position 27?"; in 2026 Paradigm's
verifier hashes the exact string Sanborn typed.

Sanborn's thematic hints, which are not cribs: the plaintext was written in 1988; two
events figure in it, his second trip to Egypt in late 1986 and the fall of the Berlin Wall
in 1989; BERLINCLOCK refers to the World Clock (Weltzeituhr) on Alexanderplatz, "the
gathering place for the crowds that brought down the Berlin wall," not the base-5
Mengenlehreuhr he pointed at in 2014; the codes "from the morse code at the beginning
through K5 are about delivering a message" (open letter, November 2025, via Scientific
American and Popular Mechanics).

## The tableau side

A plain A-Z header row followed by ABCD, then 26 rows labelled A to Z. Row A begins with
the keyed alphabet `KRYPTOSABCDEFGHIJLMNQUVWXZ` followed by its first four letters again;
each later row is the previous one shifted left by one. A footer repeats the header.
Rows are 31 characters (label plus 30 letters), except row N, which carries an extra L at
its end (32 characters). Read down the rightmost column over rows L, M, N, O and it spells
HILL. The extra L is the first line of the lower-right plate; the raised YAR is the first
line of the lower-left plate. Sanborn omitted the extra L from the small replicas he sold.
The NSA noticed the extra L in 1993; the community in 2003.

The sculpture's own text supplies two alphabets: the direct standard A-Z and the
KRYPTOS keyword-mixed sequence. Both were used in K1 and K2 (plain and cipher components
both KRYPTOS-mixed, index letter K, in the NSA's description).

## K1

Keyed Vigenère (Quagmire III), both alphabets KRYPTOS-mixed, key PALIMPSEST, 63 letters.

```
BETWEENSUBTLESHADINGANDTHEABSENCEOFLIGHTLIESTHENUANCEOFIQLUSION
```

"Between subtle shading and the absence of light lies the nuance of iqlusion."
Sanborn's own sentence, "carefully-chosen wording." One misspelling. His 2010 worksheet
shows the key written PALIMPCEST over a correctly spelled ILLUSION; ILLUSION under
PALIMPCEST and IQLUSION under PALIMPSEST both produce the carved MKYRDMFD for that word,
but PALIMPCEST throughout would change five other letters, so the slip (if it was one)
affected only that position. Sanborn's public line: the misspellings are deliberate, and
"it's more the orientation of those letters that's useful there... the positioning."

## K2

Same system, key ABSCISSA, 369 letters plus three literal "?" that pass through
unenciphered and do not consume a key letter. As carved it decrypts to:

```
ITWASTOTALLYINVISIBLEHOWSTHATPOSSIBLE?THEYUSEDTHEEARTHSMAGNETICFIELDXTHEINFORMATIONWASGATHEREDANDTRANSMITTEDUNDERGRUUNDTOANUNKNOWNLOCATIONXDOESLANGLEYKNOWABOUTTHIS?THEYSHOULDITSBURIEDOUTTHERESOMEWHEREXWHOKNOWSTHEEXACTLOCATION?ONLYWWTHISWASHISLASTMESSAGEXTHIRTYEIGHTDEGREESFIFTYSEVENMINUTESSIXPOINTFIVESECONDSNORTHSEVENTYSEVENDEGREESEIGHTMINUTESFORTYFOURSECONDSWESTIDBYROWS
```

The true ending is `WESTXLAYERTWO`. Sanborn dropped one ciphertext letter (an S, between
the final E and W of EWJLLAETG) for visual balance, expected the tail to turn to
gibberish, and was "astounded" that it read ID BY ROWS by chance. Three expert teams
accepted ID BY ROWS for seven to fourteen years. He confirmed X LAYER TWO on April 19,
2006 and "would not reveal anything more." X is his enciphered full stop ("inserted an X
between some sentences, making it harder to crack the code by tabulating letter
frequency"). UNDERGRUUND arises from a ciphertext E on his chart that became R on the
copper. WW is William Webster (confirmed 2005). The coordinates, 38 57 6.5 N, 77 8 44 W,
fall roughly 100 to 174 feet southeast of the screen depending on datum, in or near an
adjacent enclosed courtyard with a tree and a manhole cover; Sanborn has said (dinner,
secondhand) that a half-buried bronze USGS marker there was his pacing reference and has
since been removed. K2 was written to sound like "an interrupted radio transmission."

## K3

Transposition, 336 letters plus the terminal "?". A tightened paraphrase of Howard
Carter's 1923 account of opening Tutankhamun's antechamber, ending on Carnarvon's
unanswered question. Carter's reply, "Yes, wonderful things," is not on the sculpture;
Gillogly flagged it in 1999 as a possible K4 crib.

```
SLOWLYDESPARATLYSLOWLYTHEREMAINSOFPASSAGEDEBRISTHATENCUMBEREDTHELOWERPARTOFTHEDOORWAYWASREMOVEDWITHTREMBLINGHANDSIMADEATINYBREACHINTHEUPPERLEFTHANDCORNERANDTHENWIDENINGTHEHOLEALITTLEIINSERTEDTHECANDLEANDPEEREDINTHEHOTAIRESCAPINGFROMTHECHAMBERCAUSEDTHEFLAMETOFLICKERBUTPRESENTLYDETAILSOFTHEROOMWITHINEMERGEDFROMTHEMISTXCANYOUSEEANYTHINGQ?
```

One misspelling, DESPARATLY. X before the final question, Q after it. The NSA's route:
keyed columnar transposition, incompletely filled 4 x 86, extraction order explained by
KRYPTOS numerically keyed (1 4 7 3 6 2 5) "written in reverse beginning with the R column"
to give 4 1 5 2 6 3 7, with a "seven columns to the left" property. The NSA hedged that
this "may or may not be the way the system was originally set up by Sanborn." Stehle's
formula reproduces it exactly: plaintext[i] = ciphertext[(191 + 192 i) mod 337]. Dunin's
pencil version: rows of 48, every fourth row downward, clean diagonals. Sanborn, shown the
KRYPTOS = 0362514 column key in 2003, "nodded as though he recognized it," said Dunin's
diagonals "must be a by-product of the original matrix system," and was "surprised that no
one had tried recovering the original matrix and running it through all the possible
shifts." K3 is the section where recovering the text and recovering the author's
algorithm came apart.

## The Morse (K0)

On the entrance copper, read from the rock outward, padded with lone dits read as E:

```
E E VIRTUALLY E | E E E E E E INVISIBLE
DIGETAL E E E   | INTERPRETATI(ON? U? T?)   cut off at the stone
E E SHADOW E E  | FORCES E E E E E
LUCID E E E     | MEMORY E
T IS YOUR       | POSITION E                T likely the tail of a longer word
SOS
RQ                                          reads YR upside down
```

DIGETAL is misspelled on the copper. Sanborn implied it was intentional. He and Scheidt
"already seemed to know that INVISIBLE was a Morse code palindrome" (2003 road trip).
Sanborn said the front-entrance pieces "were supposed to parallel something in the
courtyard" and was disappointed, seeing aerial photos, that they appeared not to.

## Sibling works

Antipodes (1992, large version 1997, Hirshhorn): one side repeats the Kryptos text with
differences (UNDERGROUND spelled correctly, so RTBJ becomes ETBJ; no extra L; order of
tableau and text swapped; extra dots and spacing differences), the other side carries
Cyrillic Projector text. Sanborn, 2005: "all the letters are here, at the Hirshhorn. It's
possible that you could crack the whole thing from here, but it's also possible you
couldn't." The Cyrillic Projector (1997, UNC Charlotte) was solved in 2003 by Frank Corr
and Mike Bales: Vigenère-type on Cyrillic, KGB documents on source-handling and Sakharov.
The Code Room cylinder's key was the Russian word for shadow.

## The 2010 worksheets

Sanborn released his K1 and K2 Vigenère worksheets and a BERLIN layout chart to the New
York Times in November 2010 and told NPR that "once the Krypto-philes study it in a
forensic manner, there might be revelations in there. So in a way, I gave more than just
Berlin." At a later dinner he still believed "there's something to be gained if we study
his encryption charts." Images are in `../research_notes/sanborn_charts/`.

## The archive, the leak and the buyer (2025-2026)

Sanborn's private archive sold at RR Auction on November 20, 2025 for $962,500. Lot items
include the handwritten K4 plaintext with a signed letter from Scheidt, "the original
coding system for K4," the K1-K3 coding charts, an unpublished 1988 alternate K1 plaintext
and chart, an unpublished 1988 alternate K4 plaintext and chart "now known as K5," and the
scrambled texts shown to the CIA in 1990. In September 2025 Jarett Kobek and Richard
Byrne assembled the K4 plaintext from five taped-up strips in Sanborn's Smithsonian papers;
Sanborn confirmed it, the papers were sealed to 2075, and the words have not been published.
Kobek: "it took a second or two to realize, oh, this is in English... It's exactly the
right length. It makes semantic sense." Paradigm disclosed itself as buyer on June 12,
2026; it holds an HMAC of a SHA-256 of the string Sanborn typed, charges $1 per check,
has not read the answer, and holds the K5 ciphertext unreleased. K5 is 97 letters, uses a
"similar but not identical" system, and has BERLINCLOCK at the same positions.
