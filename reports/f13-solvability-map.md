# F13.1: what 97 letters of English can decide with no known letter

Issue #85, 2026-10-27. A desk count, no run. Ruler: 0136's measured redundancy of English, scaled from 73 letters (the
unknown places) to all 97, because a ciphertext-only search reads no known letter.

| Evidence in 97 letters | bits per letter | bits |
|---|---|---|
| quadgram scorer (0136, Carter's book) | 1.785 | 173 |
| quadgram scorer, least predictable tenth of windows | 1.474 | 143 |
| Shannon's upper entropy estimate (a better model's ceiling) | 3.112 | 302 |
| Shannon's lowest estimate (no model can do better) | 3.967 | 385 |

Rule (0136's): a key is decidable by an English test only if its open bits are below the evidence. With no known letter
nothing is fixed, so the open bits are the key bits less the alphabet symmetries (8.3 bits for one free alphabet, 13.0 for
two). The rule is necessary, not sufficient: a climb must also find the best key, and D1 (0228, 0229) showed design 2
finds planted English at 23 only 2 times in 3 on Sanborn-style text even where the bits allow it. Every F13.4 row must
measure its own power on plants without known words.

| Family | Cell (largest member) | Key bits | Decidable | Note |
|---|---|---|---|---|
| F1 | periodic key, length L, standard/KRYPTOS tables (8 classes) | 125.2 | quadgram | decidable to L = 36 (q), 63 (S1), 81 (S0) |
| F1 | periodic key on a dictionary-word alphabet (208,062), L = 26 | 142.9 | quadgram |  |
| F1.1 | one free alphabet + key L = 26 | 202.3 | better model (Shannon upper) | to L = 19 (q), 47 (S1), 64 (S0) |
| F1.2 | two free alphabets + key L = 13 | 224.9 | better model (Shannon upper) | to L = 1 (q), 29 (S1), 47 (S0) |
| F1 | running key from a named text (K1-K3, Carter's book ~1M letters), both directions, 8 tables | 23.9 | quadgram |  |
| F1 | running key from an unknown English text, fixed table | 282.8 | better model (Shannon upper) | key text costs its own entropy: 97 x 2.92 by quadgrams; at Shannon's upper estimate 97 x 1.59 = 154 bits, decidable |
| F1 | plaintext autokey, primer of l letters, fixed tables | 247.4 | better model (Shannon upper) | primer to l = 36 (q) |
| F1.7 | autokey on one free alphabet, lag 30 | 221.1 | better model (Shannon upper) |  |
| F6 | keyword columnar width <= 20 (log2 20!) + periodic key L = 20, fixed tables | 158.1 | quadgram |  |
| F6.1 | one free alphabet after a width-10 columnar, key L = 10 | 148.9 | quadgram |  |
| F6.2 | two free alphabets after a width-10 columnar, key L = 10 | 232.6 | better model (Shannon upper) |  |
| F3 | two dictionary words added (each of ~200k) | 38.2 | quadgram |  |
| F14 | two key-word alphabets (dictionary) + key word | 53.8 | quadgram | the keyed version of F1.2: a few dozen bits |
| F5 | Gromark, free alphabet, base 10, primer 5, one of 364 rules | 105.2 | quadgram |  |
| F8 | Hill 3x3, unknown numbering | 130.7 | quadgram |  |
| F4 | trifid, free 27-cube, period <= 97 | 99.7 | quadgram |  |
| F10 | Chaocipher, two free wheels | 176.8 | better model (Shannon upper) |  |
| F11 | M-94, 25 discs in any order, a row per 25 | 102.3 | quadgram |  |
| - | one-time pad / free key of 97 letters | 455.9 | never | never by construction |

## What it says for F13.4

- **Decidable by quadgrams now** (key under 173 bits): every keyed system on the sculpture's or dictionary tables up to key
  length 36; one free alphabet to key length 19; any move up to a width-20 keyword columnar with a fixed-table key to 20;
  F6.1's one free alphabet after short moves; Gromark, trifid, Hill 3x3 and the M-94 with free parts; every key-word
  system (F3, F14). These are F13.4's rows.
- **Only with a better English model** (173-302 bits): two free alphabets beyond length 1 (F1.2, F6.2), one free alphabet
  at 20-47, plaintext autokey primers 37-63, Chaocipher's two free wheels, a running key from an unknown English text
  (two texts of English in one: 2 x 2.92 bits per letter by quadgrams is more than log2 26). They wait for F13.3.
- **Never** (over 385 bits): a free key as long as the message, two free alphabets beyond length 47, one beyond 64.

Without the 24 known letters (113 bits) most cells the loop has decided exactly move into the 'better model' column: the
known letters, not English, carried those verdicts. F13 can therefore add little where the known letters already
decided; it matters where they may sit or read differently than assumed (A1, A2, A13), which is F13.5's hedge.
