# Craig Bauer, Unsolved! (Princeton, 2017), chapter 9 section "The CIA's Cipher Mystery (1990)"

Notes from the page images (not reproduced in the repository). Bauer is editor of
Cryptologia; this chapter restates Bauer, Link and Molle (Cryptologia 2016).

## Facts and framing

- Panel selection reviewed more than 700 slides from 275 artists; Sanborn earned $250,000.
- Dedication given as November 5, 1990. Webster: "I know that all intelligence
  professionals will enjoy the opportunity to tackle the code you've presented us in this
  courtyard."
- At the ceremony Sanborn gave Webster two sealed envelopes: "One had the keywords that
  allowed decipherment, and the other had the plaintext." "I hope you can keep a secret."
- The CIA's posted transcription contains mistakes; the relevant one is the extra L.
- A 16-signature CIA employee petition against the artwork (FOIA) called it "meaningless."
- Gillogly announced June 16, 1999 and found four distinct ciphers.
- K1: Quagmire III, alphabets scrambled by KRYPTOS, key PALIMPSEST; ten cipher alphabets
  listed. "The Q in IQLUSION was an intentional 'error' made by Sanborn."
- K2: Quagmire III, KRYPTOS and ABSCISSA. The S omission: EWJLLAETG should be ESWJLLAETG;
  ID BY ROWS becomes X LAYER TWO. "It was just an incredible coincidence."
- K3: frequencies matched English, so transposition. Bauer's route: ignore the "?",
  write 14 rows of 24, rotate the rectangle 90 degrees right to get 24 rows of 14, rewrite
  as 42 rows of 8, rotate 90 degrees again, read the plaintext. "It's not known which
  method was actually used by Sanborn."
- Stein: "Kryptos was meant to be solved with pencil and paper." Gillogly: "a crack is
  where you find it."
- "It seems likely that [K4] made use of a method completely different from those that
  produced the first three ciphers."

## Bauer's three reasons for matrix (Hill) encryption

1. Intentional errors in previous messages. Coordinates of the four errors in the
   ciphertext grid: (25, 2) for the K in line 2; (24, 6) for the R in line 6; (11, 15)
   and (15, 15) for the L and E in line 15. Eight numbers, twice what a 2x2 needs, not
   enough for a 3x3; twelve if the letter values are included.
2. BERLIN's ciphertext NYPVTT falls on two whole groups of three (NYP, VTT) when K4 is
   split in threes from the start. "This may be a coincidence."
3. HILL down the right-hand edge of the tableau. "Sanborn's clue isn't subtle at all."

## The search (with Greg Link and Dante Molle)

- 2x2: all 157,248 invertible matrices, with numberings A=0, A=1, KRYPTOS K=0, KRYPTOS
  K=1, every shift of the KRYPTOS alphabet (all rows of the right panels) at 0 and 1, every
  shift of the standard alphabet at 0 and 1, and Hill's own 1929 random alphabet
  (KPCOHARNGZEYSMWFLVIQDUXBTJ). BERLIN never appeared, at position or anywhere.
- 3x3: all 1,634,038,189,056 invertible matrices for each alphabet above, about ten hours
  per alphabet. Typically 17,000 to 18,000 matrices per alphabet produced BERLIN in
  position, always surrounded by gibberish. After CLOCK (November 2014), none produced
  BERLINCLOCK.
- Not tested, and named as open: the affine form C = MP + B; chaining modes where a block
  depends on the previous block; 4x4 and larger (over 12 sextillion); a numerical
  assignment that changes along the message "in accordance with the shifting alphabets
  scrambled by the keyword KRYPTOS"; a pair of 2x2 matrices used other than in strict
  alternation (alternation was ruled out). The eight error coordinates would fill a pair
  of 2x2 matrices.
- Bauer: "I'm not ready to rule out matrix encryption. Only a minuscule percentage of
  numerical assignments for the alphabet was tested."

## Bean's critique (2018), for balance

Bauer tested one of five block alignments for each size; the 2x2 alignment of BE with NY
requires dropping the initial O, the 3x3 alignment of BER with NYP requires dropping the
final R; Edkins had done the full 2x2 search in 2004; the key can be recovered row by row
from the cribs instead of brute-forced; the published code is undocumented.
