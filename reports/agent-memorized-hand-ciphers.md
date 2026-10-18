# Hand ciphers agents and aircrew memorized, 1890-1945, and what they mean for K4

Issue #78. Deep research run 2026-10-18: 5 search angles, 17 sources read, 70 claims extracted, 25 checked
by three independent votes (20 confirmed, 5 refuted). Cross-checked against `order-of-work.md` afterwards.

## The finding

The systems agents and soldiers were actually given are the ones the project has already tested. US Army
doctrine taught substitution, then transposition, each step simple by hand, keyed by remembered words. That
is F1, F6 and F9, closed over 198 experiments. The research adds one family the record never touched:
grille transposition. Everything else either produces digits, which K4 cannot be, or is covered.

This supports A16. If K4 is a doctrine-shaped system, its difficulty lies in the key, in Sanborn's own
change to the system, or in a slip, not in an exotic method.

## What was found

| System | Who used it | Primary source | Keyed by | Letters only | Covered |
|---|---|---|---|---|---|
| Double columnar, with variants: different rectangle sizes, a different key for each pass, varied write-in and read-out directions, nulls in one rectangle only | US Army (TM 11-485, 1944) | TM 11-485, paras 13-14 | a keyword or phrase, numbered alphabetically | yes | yes: F6, the four column readings mixed at every width (0134, 0158), padding per stage (F6.4) |
| Substitution, then transposition: "the most common" combination; two stacked substitutions add little | US Army | TM 11-485, paras 50-51 | keywords | yes | yes: F6 (both orders), F9 |
| Mixed alphabets rebuilt from a remembered word; plain and cipher alphabets paired direct, reversed, or the same mixed sequence in opposite directions | US Army | TM 32-220 (1950; 1970 revision), para 60b | a keyword | yes | yes: the reversed and opposite-direction pairings are the Beaufort and variant forms, run on KRYPTOS, keyword and free alphabets (crib sweep, 0119, 0109) |
| Interrupted keyword transposition | US Army | TM 11-485 | a keyword | yes | yes: F6.16 (0164) |
| Double transposition keyed from a novel or a large book; the same key for both passes (Chetniks), two keys (British Army), daily phrases (Soviet partisans) | WWII guerrilla and army traffic | TICOM I-205 (Marquart, 1947), I-21 (Schubert, 1945) | a remembered text | yes | mostly: F6 double columnar on vocabulary keys; F11.2 poem-code keys from K1-K3 (0190) |
| Grille transposition: a 13x19 stencil, 125 open cells, 15 nulls, read down column 1, up column 2 | Abwehr, Berlin-Rio, 1941 | Lewis, *German Agent Systems* (NSA) | the stencil, plus a page of a key book | yes | **no** |
| Stencil grille, 24x25, 10 open cells a row, read by columns in key order | Wehrmacht (RS44) | secondary (Rijmenants) | a carried stencil | yes | **no** |
| Division Field Code with a numeric additive | US Army, 1942 | TM 11-460 | a printed codebook | no (digits) | not applicable |
| VIC: straddling checkerboard, chain addition, two transpositions | Soviet agents, 1950s | secondary (Abel trial accounts) | a song phrase, a date, a personal number | no (digits) | not applicable |

Plaintext preparation the manuals teach: replace a common digraph with one prearranged letter (Q for German
CH), nulls at the end of one rectangle, numbers spelled out. Agents' security checks (deliberate errors as
proof of freedom) were confirmed only from secondary sources.

## What is new for the queue

**Grille transposition, before or after the tableau.** A grille is a card with holes. The message is
written through the holes, and the card is turned or moved. It is a classic hand system (Fleissner's
turning grille, 1881; the German army, briefly, in 1916; the Abwehr and RS44 in WWII), it gives letters only, and
the record never tested it.

- A 10x10 turning grille holds exactly 100 letters: K4's 97 plus 3 nulls. This is arithmetic, not
  evidence: 10x10 is simply the smallest square grille that holds 97 letters.
- A pure grille keeps English letter counts, and K4's are flat. So a grille can only be one stage, with
  the tableau before or after it, as Sanborn's "matrixes... then went back to this table" suggests.
- Against A16's "can be remembered": a grille is a carried card. It fits only if its holes come from a
  remembered word or rule.
- Decidability: a 10x10 turning grille has 4^25 hole patterns, about 10^15. Too many to list, but the
  24 known letters constrain the pattern cell by cell once the substitution stage is fixed. It needs a
  constraint search, not a sweep. Proposed item: F6.20, the turning grille with a periodic key on the
  KRYPTOS or standard table, both orders, with a positive control.

**Plaintext digraph swaps (CH to one letter).** Low priority. EASTNORTHEAST and BERLINCLOCK contain no
CH, but a swap earlier in the message would move every later letter, and the known words sit where
Sanborn says they sit in the plaintext as delivered.

## Refuted or weak

- "Sanborn confirmed a position-for-position mapping, BERLIN at 64" (Dunin, 2019 lunch, via Rumkin):
  refuted 0-3. The source does not support it. A2's contested status stands.
- "About 40 known letters broke one RS44 grid": refuted 0-3.
- A WWII prisoner-of-war letter code (CBS): refuted 0-3 as described.
- Scheidt's masking quotes rest on NPR's paraphrase (2005) and secondhand accounts.

## Sources

Read: Lewis, *German Agent Systems*, NSA Technical Journal (media.defense.gov); TICOM I-205 and I-21
(archive.org); TM 11-485, *Advanced Military Cryptography* (1944, radionerds.com); TM 32-220 (1950, repo
copy; 1970 revision, archive.org); TM 11-460 (1942, ibiblio and Wayback); Rijmenants on RS44; Wikipedia on
VIC; NPR 2005; Rumkin's K4 page; Plymouth University on MI9 codes.

Not reachable automatically, for Alexis to fetch or buy:

- nsa.gov Friedman Collection pages and PDFs (blocked with 403): Special Text 165, *Elementary Military
  Cryptography*, and Special Text 166, *Advanced Military Cryptography* (1931-1943).
- FM 24-12 and FM 24-16 (Army signal manuals).
- OSS and early CIA agent cipher instructions; escape-and-evasion codes for aircrew.
- Books: Leo Marks, *Between Silk and Cyanide* (SOE agent codes and security checks); David Kahn, *The
  Codebreakers* and *Number One from Moscow*.
