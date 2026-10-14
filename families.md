# Hypothesis families (living document)

Status values: `untouched`, `active`, `exhausted-bounded` (with the bound), `parked` (with reason).
Re-read this top to bottom every few pivots and pick the family with the least coverage.

| # | Family | Status | Experiments | Bounds exhausted so far | Notes |
|---|---|---|---|---|---|
| 1 | Keyed periodic systems at crib-surviving periods 27, 28, 29, 53+: Quagmire I-IV, autokey, progressive key | parked (five bounded sweeps since the pivot; re-enter with a new key source) | 0001-0005, 0009-0012, 0017 | Ciphertext autokey excluded (24 conventions x 96 lags, 0002). Plaintext autokey excluded at lags 1-11 and 30-52; lag 12 consistent in one convention on one check; 13-29 and 53-96 undecided (0003). Running key from K1-K3 plaintexts and ciphertexts, both directions, all cyclic offsets, 24 conventions: 165,216 trials, zero survivors, best 8/24 (0004). Periodic tableau with separate alphabets (Quagmire I-IV): periods 1-26 and 30-52 excluded under all 24 conventions; 1,152 surviving (convention, period) pairs force key fragments that match no vocabulary word or K1-K3 window (0005). The 13-letter key stretch forced by EASTNORTHEAST and the 11-letter stretch forced by BERLINCLOCK, scored as English under all 24 conventions, with the copper exact or with one letter inserted or deleted anywhere: the best of 9,408 stretches is 2.3 standard deviations above noise and 3.0 below English, which is what the best of noise looks like (0009). With plain and cipher alphabets mixed by keyword from any of 61 vocabulary words and key alphabets from all four Friedman mixings (248), 5.9 million stretches: the best, EFORMESTATU at -3.81, equals the best from shuffled K4 letters, -3.80 (0010). The forced key is not a readable word under any alphabet built from the puzzle's vocabulary. Progressive key, per-repeat or per-letter, steps 0-25, periods 1-97, 24 conventions: periods 1-25 and 31-51 die at every step; 26 lives at 10 steps, 30 at 7, 27-29 at all; no fragment matches (0011). Period 13 is dead at every step. Open: alphabets from words outside the vocabulary; Plaintext autokey, chained to closure from the cribs: lags 1-25 and 30-52 dead under all 24 conventions; lags 26-29 force about 60 further letters that read as noise (checked after the run, not in the record); lags 53-96 force too little to decide (0012). Running key from the sculpture's own texts: the carved tableau by rows, by columns and with its index column, the Morse plaintexts in carved and reversed order, and the four ciphertexts as one 865-letter panel, each forward and backward, every cyclic offset, 24 conventions: 162,912 trials, none with fewer than four crib mismatches (0017; the record says 869 letters, the panel is 865). | Start here; cheapest bounded results. The crib sweep shows which periods survive for single-alphabet additive; nobody has run it for Quagmire with separate plain/cipher alphabets, autokey, or progressive key. |
| 2 | Masked plaintext, then a simple keyed cipher | untouched | | | Scheidt's own description. Stage-one output is scored on crib consistency only, since it is not English by design. Candidate masks: nulls, abbreviation, phonetic spelling, changed "language base". |
| 3 | Two-component key with a combiner (Scheidt's CKM habit) | active | 0014 | Two key words in two tableau passes, lengths 2-30 with lcm outside the dead periods, plain and cipher alphabets standard or KRYPTOS, both plaintext signs, both combiner signs: 4,896 cases, 3,498 consistent, but none with total word length under 25, where the 24 cribs leave no redundant check; no survivor's words are in the vocabulary or K1-K3 (0014). | Keyword from the puzzle's vocabulary combined with a second element from the sculpture: the extra L position, the raised YAR, Morse E-padding counts, the K2 coordinates. Open: a numeric second component (coordinates, Morse counts) added to a keyword; combiner other than addition. |
| 4 | Sanborn's "visual systems" | untouched | | | Mirrored tableau reading, routes through the carved grid, the HILL column as an index. Inspiration pool is `research_notes/.../sculpture_physical_form.md`. |
| 5 | Gromark and LFSR variants beyond base 10 | active | 0013 | Running numerical key k[i] = k[i-a] + k[i-b] mod base, every lag pair 1 <= b < a <= 12, bases 10 and 26, plain and cipher alphabets from standard, KRYPTOS and the four Friedman mixings of every vocabulary word (248 each), three modes: 184,512 alphabet triples x 66 rules; zero triples make all 24 shifts digits; zero rules fit the 13 consecutive shifts at 22-34 and the 11 at 64-74 with six or more checks (0013). | Bean exhausted base-10 length-5 primers under free annealed alphabets. Open: free alphabets with other rules, three-term rules, multiplicative LFSRs, the raised YAR as primer (C22). |
| 6 | Matrix transposition stage(s), then the tableau last (Sanborn, CNN 2005: "double matrixes and triple matrixes... then went back to this table to do the ultimate") | active | 0006-0008, 0016 | Columnar routes (plain widths 2-96 in both column directions, forward and inverse; keyed columnar from every vocabulary word, both directions; every double of plain forward columnars at widths 2-50: 2,905 routes) then a periodic tableau with separate alphabets: over 69,720 route/convention pairs the smallest period the cribs allow is 23; no route allows a period under 23; forced fragments for live periods up to 30 match no vocabulary word or K1-K3 window (0006). Reverse order, tableau first then the same 2,905 routes: because the key slots follow plaintext positions, periods 1-25 die on structure alone, 26 survives in 4% of pairs by one coincidence, and no route gives a vocabulary or K1-K3 key at periods 26-30 (0007). The period test has little power in this order; it needs English scoring or longer keys. K3's own rule with every shift (a + b i mod 97, 9,312 rules, both directions) and double rotations of a grid at widths 2-50, before the tableau: 504,600 pairs, smallest live period 22, zero matches (0008). All 23,930 routes with the forced key scored as English at live periods up to 40: best UHAVETHE at -3.55 under a K3 rule at period 40; twelve shuffles of K4 give a maximum of -3.54 and a median of -3.81, so it is chance (0016, with ten extra shuffles run after the record). | The cribs constrain the final keyed-substitution stage, not positions. Note from 0006: the crib-consistency test depends only on the plain and cipher alphabets and on Beaufort versus the other two modes, so the 24 conventions are 8 distinct cases for any sweep of this kind. Next: route transpositions (spirals, boustrophedon, diagonals), K3-shaped grids (C2), and the reverse order (tableau first, transposition last). |
| 8 | Hill and other polygraphic ciphers (the HILL column, Bauer 2016-17; C21) | active | 0015 | Hill 2x2, 3x3 and 4x4, plain and affine, four numberings (standard or KRYPTOS order, 0- or 1-based), every block alignment, matrix encrypting or decrypting, solved exactly from the whole crib blocks by elimination mod 13 and mod 2: all 2x2 and 3x3 settings inconsistent; the twelve consistent 4x4 settings give a singular matrix or break the eight crib letters in partial blocks (0015). Playfair is dead at both alignments: the ciphertext digraphs SS at 33-34, TT at 69-70 and QQ at 26-27 cannot occur in Playfair. | Open: 4x4 affine (needs five whole blocks), paired 2x2, chained Hill, reversed and other numberings, blocks of 5 and up, bifid and trifid. |
| 7 | Construction simulation: generate test ciphers by candidate systems and ask which reproduce K4's width-7 doublet column and width-21 repeat fingerprint (Oranchak's Zodiac 340 method) | active | 0018 | Thirteen generators, 5,000 samples each, ten statistics: no family is singled out; index of coincidence, doublets, top count and singletons fit every polyalphabetic family. The width-7 doublet column has p about 0.002 under every generator including random letters. The width-21 vertical repeats have p about 0.005 under every substitution-last generator and p near 1 under pure transposition and monoalphabetic, so they come from English neighbours kept 21 apart (0018). | Finding: substitution then transposition keeps English adjacency into the ciphertext and is the only construction here that reproduces the width-21 repeats. The cribs do not touch that family at positions 22-34 and 64-74; they constrain the images elsewhere. Opened as family 9. |

Parameter applied to every family once it is otherwise exhausted: the copper may be wrong
by one letter (K2 was). Re-run with one letter inserted or deleted at each position, and
with the "?" counted (family G in `knowledge/06-hypotheses.md`).

## Key sources (cross-cutting: try in this order inside every family)

Sanborn, 2006, on the K2 correction: the answers to the first three passages contain clues to the fourth.
Sanborn, 2005: "I have left instructions in the earlier text that refer to later text." Sanborn, 2009 oral
history: K4 "will come back to the first part". Counterweight, Sanborn to Schmeh, 2019: it is not
necessary to know K1-K3 to solve K4. Read together: K1-K3 supply the key material, not the method.

1. Words and phrases from the K1-K3 plaintexts, especially the anomalies: IQLUSION, UNDERGRUUND,
   DESPARATLY, LAYERTWO, PALIMPSEST, ABSCISSA, the K2 coordinates as digits, WW, "can you see anything".
2. The sculpture's own text: KRYPTOS, the Morse fragments, the HILL column, the raised YAR.
3. Sanborn's named themes: BERLIN, CLOCK, WELTZEITUHR, EGYPT, CARTER, the 1989 wall.
4. Only then generic English word lists.

Every experiment's `bounds` should say which key source it drew from.

## Dead ends (need a stated reason before re-entry)

| Approach | Why dead | Source |
|---|---|---|
| Ciphertext autokey, any lag 1-96, any of 24 alphabet/mode conventions | Exact crib check at every position beyond the lag; zero survivors | experiment 0002 |
| Plaintext autokey at lags 1-25 and 30-52 | Chained closure from the cribs conflicts under every convention; lags 26-29 force 60 letters of noise | experiments 0003, 0012 |
| Running key from K1, K2, K3 plaintext or ciphertext, any offset, either direction | 165,216 trials, zero survivors | experiment 0004 |
| Running key from the carved tableau, the Morse, or the whole right-hand panel, any offset, either direction | 162,912 trials, none within three mismatches | experiment 0017 |
| Periodic tableau with separate alphabets at periods 1-26 and 30-52 | Forced key letters conflict under all 24 conventions | experiment 0005 |
| Periodic tableau at surviving periods keyed by a vocabulary word or a K1-K3 phrase | Forced fragments match nothing in the pool | experiment 0005 |
| Columnar transposition (plain, keyed by vocabulary, or double plain) then a periodic tableau with a key shorter than 23 | Smallest crib-consistent period over 2,905 routes and 24 conventions is 23 | experiment 0006 |
| Periodic tableau with a vocabulary or K1-K3 key of length 26-30, then a columnar transposition from the 0006 route set | Forced fragments match nothing | experiment 0007 |
| K3's transposition rule at any shift, or a double grid rotation, then a periodic tableau with a key shorter than 22 | Smallest crib-consistent period over 21,025 routes is 22 | experiment 0008 |
| Periodic tableau with a readable key under the standard or KRYPTOS alphabets, exact copper or one letter off | Forced key stretches score as noise under all 24 conventions and all 195 one-letter variants | experiment 0009 |
| Periodic tableau with a readable key, alphabets mixed from any vocabulary word by any Friedman mixing | Best forced stretch equals the shuffled-letter null | experiment 0010 |
| Progressive-key periodic tableau at periods 1-25 and 31-51, any step 0-25, either form | Crib collisions conflict under every step and convention | experiment 0011 |
| Gromark-style running numerical key, any two-term lag rule up to 12, base 10 or 26, alphabets built from the vocabulary | The 13 consecutive known shifts obey no such rule | experiment 0013 |
| Two key words of total length 24 or less, composed through two tableau passes, standard or KRYPTOS alphabets | The 24 crib equations are inconsistent for every such pair | experiment 0014 |
| Columnar, K3-rule or double-rotation route, then a periodic tableau with a readable key at periods up to 40 | Best forced key scores inside the shuffled-letter distribution | experiment 0016 |
| Monoalphabetic substitution | Same ciphertext letter maps to different plaintext letters in the cribs | cribs |
| Pure transposition, any route | Cribs need three E's, K4 has two; letter mismatch at fixed positions | cribs |
| Rotor machines (Enigma class) | K encrypts to K at 74, S to S at 33 | cribs |
| Single-alphabet periodic additive at periods 1-26, 30-52 | Crib consistency sweep | `kryptos/cribsweep.py` |
| Plain Vigenere with an English keyword under the tableau | Implied key fragments are gibberish under every convention | Schridde 2017; sweep |
| Hill 2x2, 3x3, 4x4, plain or affine, four numberings, any alignment, either direction | Crib blocks inconsistent, or the solved matrix singular, or partial-block crib letters broken | experiment 0015 (2x2 also Edkins 2004, Bean 2018) |
| Playfair, either alignment | Doubled ciphertext digraphs SS, TT, QQ are impossible in Playfair | ciphertext |
| Gromark base-10 length-5 primers | Exhausted (99,999 primers) | Bean 2021 |
| Wichmann-Hill seeds 0-50 | Exhausted | Schridde 2017 |
| Mengenlehreuhr (base-5 Berlin Clock) as key schedule | Sanborn named the Weltzeituhr in 2025; eleven community years spent | Scientific American 2025 |

## Pivot log

| Date | From | To | Reason |
|---|---|---|---|
| 2026-10-14 | 1 keyed periodic (0009-0012) | 5 Gromark | Family 1 bounded for periodic, progressive and autokey keys under every alphabet the vocabulary can build. |
| 2026-10-14 | 1 keyed periodic | 6 transposition then tableau | Five consecutive reverts in family 1 (0001-0005); program rule. Family 1 keeps its open bounds: plaintext autokey lags 12-29 and 53-96, progressive key. |
