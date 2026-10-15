# 0021-running-key-from-carter-tomb-of-tutankhamen: A running key from Howard Carter's book: the text K3 paraphrases, slid past K4 at every offset

**Family:** 1-keyed-periodic  
**Parent:** 0017-running-key-from-the-sculpture-itself  
**Decision:** reverted  
**Run:** 2026-10-15T06:36:02+00:00, 5.9 s, status ran  
**Time by phase:** design 15 s, implement 71 s, test 10 s, run 6 s, record 0 s

## In plain words

The third message retells the moment Howard Carter first looked into Tutankhamun's tomb. The artist has said the earlier messages hold instructions for the last one. One old trick is to use a book as the key: line the book's letters up under the message and add them. We take Carter's own book, every page of it, and slide it along the fourth message at every possible starting point, forwards and backwards, asking whether any position explains all 24 known letters.

## Walkthrough, by hand

1. Open the book at any point, say the words THE TOMB OF TUT ANKH AMEN, and write its letters under the message starting at position 1: T under O, H under B, E under K, and so on.
2. Position 22 of the message is E; the book letter under it is the 22nd letter from where you opened.
3. On the sculpture's table, find the row of that book letter and the column of E; the letter there should be the carved F.
4. If it is not, count one miss and go on to the next known letter.
5. After three misses, give up on this opening and move the book one letter along.
6. Do this for every opening in the book, then with the book read backwards.

## Worked example (generated)

```
book opened at letter 40: TOMBOFTUTANKHAMENHOWARDCARTERANDACMACETHEFIRSTVOLU

pos  plain  book letter  E+key  carved  match
 22    E        R          F      F     yes
 23    A        D          L      L     yes
 24    S        C          I      R     no
 25    T        A          E      V     no
 64    B        O          G      N     no
 65    E        G          X      Y     no
```

## Lineage

Inherits from 0017-running-key-from-the-sculpture-itself. What changed: Key source is Carter's The Tomb of Tut-ankh-Amen, volume one, the book K3 paraphrases, instead of the sculpture's own texts. About 330,000 letters, both directions, every offset.

## Hypothesis (domain expert)

Sanborn: 'I have left instructions in the earlier text that refer to later text' and the K1-K3 answers 'contain clues to the fourth' (C7); K3 is Carter's account of opening the tomb, paraphrased, and the misspelt DESPARATLY and the 'can you see anything' line point at the book itself (knowledge/sources/carter-1923-tomb-of-tutankhamen-vol1.txt, an OCR scan). A running key from a printed book is the classic 1900-1945 hand system Scheidt taught (C5). Test: the book's letters, forward and backward, at every offset, under the 24 conventions, scored by crib mismatches; zero mismatches is a survivor and is decrypted; one or two are reported for the one-letter-error reading (C17) and for OCR damage. About 16 million trials; chance survival is 26 to the minus 24 each, and a near miss at two mismatches has chance about 10 to the minus 28 per trial. Bounds: complete for this text as scanned, both directions.

## Prediction

No offset in either direction explains all 24 known letters, and none comes within two. The best trial has four or more mismatches, which is chance among 16 million trials. Zero candidates pass.

## Method

1. Strip the scan to letters A-Z.
2. For each direction, convention and offset, encrypt the 24 known plaintext letters with the book letters at their positions and count mismatches against the carved letters, stopping at the third mismatch.
3. Keep every trial with two or fewer mismatches.
4. Decrypt and submit any zero-mismatch trial.

## Result

Candidates returned: 0. Passed all gates: 0. Best crib hits among all candidates: 0/24
(no candidates).
Best loss: None (0 is solved; 10 per missed crib letter). Best fitness: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| - | no candidates | | | | |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "running key from Carter 1923 vol. 1 (OCR scan)",
 "letters": {
  "carter vol1 fwd": 284914,
  "carter vol1 bwd": 284914
 },
 "conventions": 24,
 "trials": 13675872,
 "fewest_mismatches": "more than 2",
 "near_misses": [],
 "survivors": 0
}
```

Notes: 13675872 trials; 0 survivors; 0 trials within two mismatches.


