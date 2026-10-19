# Leo Marks, *Between Silk and Cyanide* (1998): notes for K4

Issue #78 (hand ciphers agents memorized), #80 (bought by Alexis 2026-10-19). Read in the Kindle web reader
by targeted search, not cover to cover: the poem code (pp. 9-11, 31-33), security checks (pp. 16-17),
letter one-time pads and worked-out keys (pp. 247-251), Dutch-section precautions (p. 232). Notes and page
numbers only; the Kindle edition's page numbers.

## What SOE agents actually did

| System | How it worked (Marks) | Letters only | Rememberable | Covered in our record |
|---|---|---|---|---|
| Poem code | Agent picks five words *at random* from a memorized poem, numbers their letters alphabetically, transposes twice (a pair of keys, a different five words for the second); an indicator group at the start says which five words (pp. 11, 31-32) | yes | yes | mostly: 0190 (F11.2) used runs of 1-6 *consecutive* words of K1-K3 and the Morse, not five words chosen anywhere in a text. Pure transposition keeps English letter counts; K4's are flat, so a poem code alone cannot be K4 |
| Worked-out keys (WOK) | Random transposition keys printed on silk, cut away after use (p. 33) | yes | **no**, by design ("keys which the agents could not possibly remember") | not applicable (A16) |
| Letter one-time pad (LOP) | Pad letter over message letter, looked up in a reciprocal 26x26 substitution square (o over l gives q, o over q gives l) (pp. 247-249) | yes | **no** | not applicable; the square itself is a tableau, which F1 covers |
| Security checks | Dummy letters inserted in the body, and *deliberate spelling mistakes at prearranged places*; their absence or change signals capture (p. 16) | yes | yes | partly: F3.5 (0178) uses the misspelt letters' positions; F1.6 / F6/5 test one carved letter wrong, missing or extra |
| Message padding (Dutch section, 1943) | Eight random letters at the beginning and at the end of each message; transposition keys at least 18 letters long (p. 232) | yes | yes | partly: 0023 tested a run of nulls at the start; nulls at both ends together not found in the record |

## What this adds for K4

1. **Deliberate misspellings as a convention.** In SOE practice a misspelling at an agreed place was a
   signal, not a slip. Kryptos has three misspellings (IQLUSION, UNDERGRUUND, DESPARATLY) plus the
   table's extra L, and Sanborn says his work is "rife with mistakes on purpose" (02-sanborn-said.md).
   The record already treats them as possible keys (F3.5); Marks gives the period precedent for that
   reading.
2. **Agents' coding errors had a known shape.** Marks's "indecipherables" came from misnumbering a key,
   misspelling a key word (Bodington's "raping" for "rapping", p. 11), skipping or doubling a column
   ("hatting", pp. 206, 317), or switching from encoding to decoding procedure halfway (p. 17). These
   are procedural errors in a transposition, broader than F6/5's single wrong letter. With Sanborn's
   "mistakes on purpose", a deliberate procedural slip (a skipped column, one misnumbered key digit)
   is a candidate queue item; each is a small, enumerable set around every transposition already tested.
3. **Nulls at both ends.** Eight at each end was taught practice. Cheap to add to F2's null tests.
4. **Five words from anywhere in a text**, not consecutive words: the poem code as agents used it.
   Expensive (combinations of five words from K1-K3's ~200 words), and still blocked by flat letter
   counts unless a substitution stage follows; 0190 covered that combination only for consecutive runs.

None of this is a new family. It refines F2, F6/5 and F11.2.

## Is Kahn's *The Codebreakers* still needed?

For #78, probably not. It was wanted for agent ciphers and grilles. Agent ciphers: Marks covers SOE from the
inside, and the US manuals (TM 11-485, TM 32-220) are already read. Grilles: F6.20's design rests on
Lewis's NSA paper, and Alexis's Kindle library already has Dunin and Schmeh, *Codebreaking: A Practical
Guide* (2020), which covers turning grilles and how they are broken. Check that first.
