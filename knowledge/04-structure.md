# 04. What the 97 letters and 24 cribs prove and suggest

## Counts

Index of coincidence 0.0361, against 1/26 = 0.0385 and English 0.066. All 26 letters
occur. Frequencies: K 8; S, T, U 6; B, O, W 5; A, F, G, I, L, Q, R, Z 4; D, J, N, P 3;
C, E, H, V, X 2; M, Y 1. Flat, so not a transposition of English and not monoalphabetic.

## The crib map

```
pos  22 23 24 25 | 26 27 28 29 30 31 32 33 34 || 64 65 66 67 68 69 | 70 71 72 73 74
CT    F  L  R  V |  Q  Q  P  R  N  G  K  S  S ||  N  Y  P  V  T  T |  M  Z  F  P  K
PT    E  A  S  T |  N  O  R  T  H  E  A  S  T ||  B  E  R  L  I  N |  C  L  O  C  K
```

Plaintext letters with several ciphertext images: A to K, L; C to M, P; E to F, G, Y;
L to V, Z; N to Q, T; O to F, Q; S to R, S; T to R, S, V. Ciphertext letters with several
plaintext sources: F from E, O; K from A, K; N from H, B; P from R, R, C; Q from N, O;
R from S, T; S from S, T; T from I, N; V from T, L. Two self-encryptions: S at 33, K at
74. P encrypts R at both 28 and 66.

Adjacent doublets in the ciphertext map to non-doublets: QQ at 26-27 is NO, SS at 33-34
is ST, TT at 68-69 is IN. Whatever the key or state is, it changes between every adjacent
position.

The cribs need three E's and the ciphertext has two E's. The cribs need two S's in
EASTNORTHEAST and K4 has six S's, but the E count alone excludes any pure rearrangement of
the ciphertext.

## What the cribs exclude outright

- Monoalphabetic substitution.
- Pure transposition of any route, by position and by letter count.
- Reflector machines (Enigma class), by the two self-encryptions.
- Standard Playfair on vertical pairs at widths 7 or 21, and double-box at 21: Bean shows
  two different plaintext pairs would map to the same ciphertext pair (ZT at width 21, BQ
  at width 7), KK cannot occur in standard Playfair, and 26 letters occur.
- Any periodic additive cipher over one fixed alphabet (Vigenère, Beaufort, variant
  Beaufort; standard or KRYPTOS alphabet) with period 1 to 26 or 30 to 52. Only periods
  27, 28, 29 and 53 to 97 survive. The exclusions come from same-plaintext-different-
  ciphertext and same-ciphertext-different-plaintext pairs at congruent positions, so they
  do not depend on the alphabet. `python -m kryptos.cribsweep` reproduces this.
- The implied Vigenère key fragments under the sculpture's own tableau are gibberish
  under every convention: standard-alphabet Vigenère gives BLZCDCYYGCKAZ at 22-34 and
  MUYKLGKORNA at 64-74; KRYPTOS-alphabet Vigenère gives RDUMRIYWOYNKY and ELYOIECBAQK.
  "Plain keyed Vigenère with an English keyword" is dead unless the period is 27 or more
  and the key is not a word.
- Block ciphers on fixed blocks over all 97 letters without a stated padding or alignment:
  97 is prime. With padding or an offset (drop the first O or the last R; count the "?")
  they are back in play; Bauer notes Scheidt's "98."

## Bean's constraints on an additive numeric key (zero-indexed positions)

From the cribs, for any cipher of the form c = p + k_i over fixed alphabets: k24, k28,
k33 all differ (T goes to V, R, S); k21, k30, k64 all differ (E to F, G, Y); k27 = k65
(R to P twice); k68 differs from k25; k22 from k31; k66 from k70; k26 from k71; k69 from
k72; k23 from k32; and across letters k71 differs from k21, k25 from k26, k24 from k66,
k31 from k73, k29 from k63, k32 from k33, k67 from k68, k27 from k72, k23 from k28.
Twenty-one inequalities and one equality. Random base-10 digits satisfy them about one
time in 91. If Gromark is the system the key does not repeat at period 21 or 42, and the
base is at least 3.

## The width-7 and width-21 observations

At width 7, five of the six horizontal doublets (BB at 19, QQ at 26, SS at 33, ZZ at 47,
TT at 68) start at a position congruent to 5 mod 7, the same column; SS at 43 is the
exception. Schridde estimated the chance at 0.01 to 0.1 percent. The NSA recorded "a
slight interval 7 property" and "roughness at interval 7" and tested plaintext and
ciphertext autokey for it without result; its 1992 hypothesis was substitution followed by
transposition, which would move a plaintext repeat at distance 7, 14 or 21 into the
interval statistic.

At width 21, the 76 vertical bigrams contain 11 repeats (AZ BS IT LS LW PK QZ SN WA ZT
KK), against 9.7 expected for English at that width and about one in 6,750 random
permutations of K4. Bean notes the same property at width 19 turned out to be causal in
Zodiac 340, where the cipher was transposition plus homophonic substitution, but the
cribs kill the seriated-digraph explanation here. A binary Gromark key with a five-digit
primer reproduces such a width-21 property about one time in ten, because an even base
with a five-digit primer has an underlying period-21 structure in the key (Rogot, Deavours,
Blackman). Base-8 five-digit primers that fit the cribs expand with period 84 and have the
property that every column at widths 7 and 21 is all-odd or all-even.

DIAWINFBN at positions 57-65: for five consecutive pairs the letter four positions to the
right is +5 mod 26 under the standard alphabet (Stehle 2000; about 1 in 1,470).

## The "minor differences"

For the ten crib plaintext letters that lie in KRYPTOS, the ciphertext letter sits close
to the plaintext letter in the standard alphabet: S to R 1, T to V 2, O to Q 2, R to P 2,
T to R 2, S to S 0, T to S 1, R to P 2, O to F 9, K to K 0, summing to 21. About one
permutation in 5,520 does this. For repeated crib plaintext letters, the ciphertext images
of each letter are also close (mean distance 3.6, ten of thirteen under five; about one in
240). In the KRYPTOS alphabet, 7 of 13 of those distances are multiples of 5, and with
plaintext numbered on the standard alphabet and ciphertext on the reversed KRYPTOS
alphabet, 13 of 24 plain-minus-cipher values are multiples of 5. Bean reads all this as a
letter-for-letter cipher with no transposition and a cipher alphabet "near" the standard
one, hence Gromark. Materna read it as "KRYPTOS or a derivative is the key."

## Information budget

Twenty-four known letters give about 24 times log2(26), roughly 113 bits of constraint.
A method whose key is under 113 bits and that fits the cribs will have essentially one
solution; a method with a larger key space can fit the cribs by accident. Bean's unicity
estimate for Gromark is about 48 letters, so a 97-letter solution in that family would be
unique. A 7x7 binary Hill matrix over one of 27 alphabets is about 52 bits, which matched
the 11 BERLINCLOCK letters then known and is why Bean expected and found spurious fits.

## Things the structure does not settle

Whether "one-to-one" means no transposition at all. Sanborn's dinner remark (N = B,
Y = E, ...) and his 2019 retreat to "97 characters and BERLIN at 64" leave open a
transposition that happens to keep the crib runs in place, or a transposition applied
before substitution with the cribs defined on the final text. The 2010 Times line "the
other 91 characters and their proper order are yet to be determined" and Sanborn's own
account of "double matrixes and triple matrixes... and then went back to this table" both
keep a reordering step on the table. Note too that if transposition came first and the
tableau last, the crib letters are still "one-to-one" at the final step, which is exactly
what Sanborn described.
