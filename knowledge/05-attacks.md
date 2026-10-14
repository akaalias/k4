# 05. Everything tried against K4, with bounds

Status words. **Excluded**: contradicted by the cribs or the structure. **Exhausted**: the
whole stated key space was searched and the bounds are published. **Explored**: tried
without published bounds; treat as not exhausted. **Open**: untested or barely tested.

## Institutional attempts

| Who | When | What | Outcome |
|---|---|---|---|
| NSA Z Group task force | Nov 1992 | One day on K4 after solving K1-K3 in two days; "given the suspected cryptography, the last section is too short to solve without diverting a great deal of effort from operational problems" | Stopped. Hypotheses recorded: plaintext autokey (if a high-frequency letter is assigned 0); substitution then transposition. "KRYPTOS plays an integral part." |
| NSA analyst, post-2006 summary | 2006-2010 | Plaintext and ciphertext autokey against the interval-7 property; classified methods redacted | "yet to stumble upon something that gives either readable plaintext, or hints at the presence of a second encipherment layer." Asks whether a letter is missing from K4 as one was from K2. "Dozens" at NSA have tried. |
| CIA memo | 1990 | Suggested one-time pad | Unfalsifiable; contradicts Scheidt's "can be remembered with the correct key word/s." |
| David Stein | 1998 | "I haven't spent much time on this portion, but there are interesting patterns in here as well." | Noted an unexplained I.C. peak at m = 13 in both K1 and K2 ("another code overlaid on top of the others, possibly one using a keyword of 13 letters? Or just a coincidence?"). |
| Jim Gillogly | 1999-2005 | "On the order of 20 billion trial decryptions spread over two dozen different systems with perhaps 5 or 10 variations each" by 1999; "at least 100 billion" by 2005; several hundred hours | Nothing. Guessed running key, combined polyalphabetic substitution and transposition, or autokey; "the only likely periodicity appears to be at period 25, but that may well just be chance"; "a probably-spurious Phillips-like distribution." Later suggested Gromark (1999, 2004). |

## Published academic work

| Who | What | Bounds | Outcome |
|---|---|---|---|
| Keith Edkins, Feb 2004 | 2x2 Hill, Kryptos alphabets plus standard, all shifts, both alignments, first 96 and last 96 letters | All 157,248 invertible matrices | Nothing |
| Bauer, Link, Molle, Cryptologia 2016; Bauer, Unsolved! 2017 | 2x2 and 3x3 Hill, C = MP | 2x2: all invertible, numberings A=0, A=1, K=0, K=1, every KRYPTOS shift, every standard shift, Hill's 1929 alphabet. 3x3: all 1.63 trillion invertible matrices per alphabet, ten hours each | 2x2: BERLIN never appears. 3x3: 17,000-18,000 matrices per alphabet give BERLIN in place, none gives BERLINCLOCK. One alignment per size (Bean). Not tested: affine C = MP + B, chaining, 4x4, numbering that shifts with the KRYPTOS rows, pairs of 2x2 other than alternating |
| Christian Schridde, 2017 | 3x3 Hill with A=0 and A=1; keyed alphabets KOMITET, SANBORN, CIPHER; Wichmann-Hill PRNG as key | A=0: contradiction (gcd(20,26) does not divide 23). A=1: candidate mod 13, all 2^9 lifts to mod 26 fail. PRNG seeds 0-50 for each of three seeds, Vigenère variants, checked at 64-69 | Nothing |
| Richard Bean, 2018 | 2x2 Hill with same alphabet both sides, scored by quadgrams; binary 7x7 over sculpture alphabets; 2x2 with different plain and cipher alphabets (Sinkov); Trifid with 27 characters; four-square; keyword-derived alphabets from Friedman's HYDRAULIC routes | 2x2 full; others hill-climbing | Nothing readable. "Transposition followed by Hill: but then saying NYPVTT maps to BERLIN becomes difficult." |
| Richard Bean, HistoCrypt 2021 | Gromark (numeric running key from a primer, lagged Fibonacci expansion, free plain and cipher alphabets found by simulated annealing with hexagram scoring) | Base 10, primer length 5: 99,999 primers, 1,040 pass the 22 crib constraints, 39 pass the Gröbner-basis reduction; each annealed. Base 10 length 4: only 3301, 6740, 9903 possible. Base 8 length 5: four primers incl. 00351 and 00537 (period 84) | "Although many plaintexts close to ordinary English were discovered, none were entirely convincing." Other bases, lengths and expansion rules "difficult to test all the possibilities" |
| Bean talks, 2024-25 | "From Gromark to Autoclave" (Nov 2024); "Kryptos Final Guesses" (Nov 2025) | Not published in detail | Unknown |

## Community searches, as far as they can be reconstructed

| Approach | Who / when | Bounds | Status |
|---|---|---|---|
| Vigenère and Quagmire with English keywords, both alphabets | Kellogg 2017, Schridde 2017, many | word lists, unbounded | Explored; implied keys non-English (MUYKLGKOR under the standard tableau, SYMLWRHZN under the sculpture's) |
| Running key from K1-K3 plaintext or ciphertext | Gillogly 1999, Schridde 2017 | both tableaux | Explored; nonsense key |
| Autokey (plain and cipher) | NSA, Gillogly, Schridde | not bounded | Explored, negative; revisited by Bean 2024 |
| Scott's two-stage: Quagmire III (KRYPTOS, EMUFPHZLRFA) then affine position map y = 77 + 38x mod 97 | 2020 | one keyword pair | Reproduces BERLIN, then PEEK; JAIL at 22; a second Quagmire layer (HXDKZEK) gives nothing. BERLIN depends only on MUFZLR of the keyword. Dead end in that form |
| Mengenlehreuhr base-5 schedules | community 2014-2025 | about eleven years, unbounded | Dead; Sanborn named the World Clock in 2025 |
| 5-bit and 7-bit ASCII with bit transposition | German submitter 2019; Schridde | n/a | Lossy or equivalent to simple substitution; Sanborn reportedly called one "partly correct but mostly wrong" (secondhand) |
| M-94, M-209, fractionated Morse, Trifid, four-square, bifid and conjugated-matrix bifid (DIAWINFBN) | community, Bean | hill-climbing | Explored, nothing |
| Keyword alphabets from HYDRAULIC, KRYPTOS, KOMITET ("The key to Kryptos is komitet," anonymous instant message to Dunin) | community | with Hill or Vigenère | Explored, nothing |
| Folding one half over the other, Jefferson cylinder, book code, candle and shadow readings, sundial, palindromes, rock placement, magnetism, Egyptian references, combining K1-K3 methods | Dunin's FAQ list | n/a | Proposed, none confirmed |
| Morse, compass, lodestone, Antipodes differences as key | community | n/a | No linkage established |
| Dean Wiley's keyword script, 2011 | community | hundreds of suggested keywords: DYAHR, HYDRA, LAYERTWO, KLEPSYDRA, PARASYSTOLE, DIGETAL, LUCID, SHADOW | Nothing |
| Plaintext masking (nulls, abbreviation, phonetic spelling, changed language base) before a keyed cipher | Scheidt's own description | not searchable as stated | Open |
| Keyed periodic systems at periods 27, 28, 29, 53+; Quagmire I-IV with separate alphabets; progressive key | nobody with bounds | | Open; cheap to exhaust with the crib filter |
| Gromark beyond base 10 length 5; Vimark (base 26); LFSR period 63 or 84 | Bean partial | | Open |
| Matrix (transposition) stages then tableau, per Sanborn's 2005 description | nobody formally | | Open |
| Construction-simulation of the width-7 and width-21 properties (Oranchak's Zodiac method) | nobody | | Open |

Paradigm, June 2026: "There has been an explosion in AI-assisted attempts on Kryptos,
but none have succeeded yet." No published machine-learning attack exists.

## Refuted and unverified public claims

Every one fails at least one of: all 24 crib letters at their positions, letter-count
consistency, a reproducible method.

- "GVKMAN IN A JOB" (a 1999-era website; NSA summary): adds EMUFPHZLR to KRYPTOS and reads
  down columns. Not even plaintext.
- Jose's Reagan "Tear Down This Wall" plaintext (2010-2014): 23 English words with BERLIN
  at 64; no method; crosses a sentence break in the source.
- Scott Perry / "James C" (2018): NYPVTT are "placeholders" keyed by RFAEMUFPHZL; nothing
  further produced.
- German 5-bit ASCII submission (2019): see above.
- "Rotes Rathaus chimes" plaintext (January 2024): 99 letters, no key.
- Vigenère keys THEQUICKBROWNFOX (July 2024) and BERLIN (December 2024): check scripts fail.
- Sojourn Cygnus 243-page K4+K5 report (2024): Sanborn "did not verify."
- Zackery Belanger's plaintext and K5 (2025, dearcipher.space): unverified.
- Salcedo Novoa preprint, "14-column transpositions" (2026): self-published, unverified.
- ElodineOfficial/KryptosK4 (2026): Vigenère key LICHT giving "DONOTLOCATETHEBERLINCLOC
  JSEEKNOWTHEWESTWALLOFXXX"; self-described unfinished.
- solvekryptos.com "reconstructed" plaintext (2026): "not independently verified."
- Kobek and Byrne (2025): the words, by archival recovery; no method; unpublished.

Base rate from Sanborn, 2010: "So far, no one has had more than two letters right."
