# Hypothesis families (living document)

Status values: `untouched`, `active`, `exhausted-bounded` (with the bound), `parked` (with reason).
Re-read this top to bottom every few pivots and pick the family with the least coverage.

| # | Family | Status | Experiments | Bounds exhausted so far | Notes |
|---|---|---|---|---|---|
| 1 | Keyed periodic systems at crib-surviving periods 27, 28, 29, 53+: Quagmire I-IV, autokey, progressive key | active | 0001 (baseline), 0002 | ciphertext autokey excluded (24 conventions x 96 lags) | Start here; cheapest bounded results. The crib sweep shows which periods survive for single-alphabet additive; nobody has run it for Quagmire with separate plain/cipher alphabets, autokey, or progressive key. |
| 2 | Masked plaintext, then a simple keyed cipher | untouched | | | Scheidt's own description. Stage-one output is scored on crib consistency only, since it is not English by design. Candidate masks: nulls, abbreviation, phonetic spelling, changed "language base". |
| 3 | Two-component key with a combiner (Scheidt's CKM habit) | untouched | | | Keyword from the puzzle's vocabulary combined with a second element from the sculpture: the extra L position, the raised YAR, Morse E-padding counts, the K2 coordinates. |
| 4 | Sanborn's "visual systems" | untouched | | | Mirrored tableau reading, routes through the carved grid, the HILL column as an index. Inspiration pool is `research_notes/.../sculpture_physical_form.md`. |
| 5 | Gromark and LFSR variants beyond base 10 | untouched | | | Bean exhausted base-10 length-5 primers. Raised YAR as a possible primer. |
| 6 | Matrix transposition stage(s), then the tableau last (Sanborn, CNN 2005: "double matrixes and triple matrixes... then went back to this table to do the ultimate") | untouched | | | The cribs then constrain the final keyed-substitution stage, not positions; the transposition must deliver plaintext letters into crib positions such that the forced key letters form a short key. See `knowledge/06-hypotheses.md` family A. |
| 7 | Construction simulation: generate test ciphers by candidate systems and ask which reproduce K4's width-7 doublet column and width-21 repeat fingerprint (Oranchak's Zodiac 340 method) | untouched | | | Not a solver; a family-ranking tool. Results feed the patience rules. |

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
| Monoalphabetic substitution | Same ciphertext letter maps to different plaintext letters in the cribs | cribs |
| Pure transposition, any route | Cribs need three E's, K4 has two; letter mismatch at fixed positions | cribs |
| Rotor machines (Enigma class) | K encrypts to K at 74, S to S at 33 | cribs |
| Single-alphabet periodic additive at periods 1-26, 30-52 | Crib consistency sweep | `kryptos/cribsweep.py` |
| Plain Vigenere with an English keyword under the tableau | Implied key fragments are gibberish under every convention | Schridde 2017; sweep |
| All invertible 2x2 Hill matrices | Exhausted | Edkins 2004, Bean 2018 |
| Gromark base-10 length-5 primers | Exhausted (99,999 primers) | Bean 2021 |
| Wichmann-Hill seeds 0-50 | Exhausted | Schridde 2017 |
| Mengenlehreuhr (base-5 Berlin Clock) as key schedule | Sanborn named the Weltzeituhr in 2025; eleven community years spent | Scientific American 2025 |

## Pivot log

| Date | From | To | Reason |
|---|---|---|---|
