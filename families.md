# Hypothesis families (living document)

Status values: `untouched`, `active`, `exhausted-bounded` (with the bound), `parked` (with reason).
Re-read this top to bottom every few pivots and pick the family with the least coverage.

| # | Family | Status | Experiments | Bounds exhausted so far | Notes |
|---|---|---|---|---|---|
| 1 | Keyed periodic systems at crib-surviving periods 27, 28, 29, 53+: Quagmire I-IV, autokey, progressive key | active | 0001 (baseline) | none yet | Start here; cheapest bounded results. The crib sweep shows which periods survive for single-alphabet additive; nobody has run it for Quagmire with separate plain/cipher alphabets, autokey, or progressive key. |
| 2 | Masked plaintext, then a simple keyed cipher | untouched | | | Scheidt's own description. Stage-one output is scored on crib consistency only, since it is not English by design. Candidate masks: nulls, abbreviation, phonetic spelling, changed "language base". |
| 3 | Two-component key with a combiner (Scheidt's CKM habit) | untouched | | | Keyword from the puzzle's vocabulary combined with a second element from the sculpture: the extra L position, the raised YAR, Morse E-padding counts, the K2 coordinates. |
| 4 | Sanborn's "visual systems" | untouched | | | Mirrored tableau reading, routes through the carved grid, the HILL column as an index. Inspiration pool is `research_notes/.../sculpture_physical_form.md`. |
| 5 | Gromark and LFSR variants beyond base 10 | untouched | | | Bean exhausted base-10 length-5 primers. Raised YAR as a possible primer. |

## Dead ends (need a stated reason before re-entry)

| Approach | Why dead | Source |
|---|---|---|
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
