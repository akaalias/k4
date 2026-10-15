# 0078-running-key-from-sanborns-own-letters: Sanborn's own letters as the key: his 1989 note to CIA staff, the 1991 dedication pages, and his 2025 open letter

**Family:** 1-keyed-periodic  
**Parent:** 0004-running-key-from-k1-k3  
**Decision:** reverted  
**Run:** 2026-10-15T13:42:15+00:00, 78.6 s, status ran  
**Time by phase:** design 64 s, implement 0 s, test 17 s, run 79 s, record 0 s

## In plain words

A running key is a long text, such as a page of a book, written under the message one letter per place. We have tried the solved messages and Carter's book. Here we try the texts Sanborn himself wrote about the sculpture: his 1989 letter telling CIA staff what he was building, the 1991 pages with the dedication speech, and his 2025 open letter with its 'clue'. Each is slid along the copper at every starting place, forwards and backwards, and the 24 known letters say how close each fits.

## Walkthrough, by hand

1. Write the 1989 letter's letters, DEARAGENCYEMPLOYEESIAMWRITING..., under the copper so that its first letter sits under place 1.
2. Place 22 then has key letter M, the 22nd letter of DEARAGENCYEMPLOYEESIAM.
3. On the sculpture's table with Vigenere, counted from K = 0: known E (11) plus M (18) is 29, which is 3, P; the carved letter is F, so this place misses.
4. Count how many of the 24 known places come out right.
5. Slide the letter one place and repeat, for every offset, both directions and every table.

## Worked example (generated)

```
1989 letter from its first letter under place 1; sculpture's alphabet, Vigenere

place  known  key  would carve  carved
   22      E    M            P       F
   23      A    W            T       L
   24      S    R            A       R
   64      B    U            P       N
```

## Lineage

Inherits from 0004-running-key-from-k1-k3. What changed: Running keys have been tried from K1-K3, Carter's book and the sculpture's own texts. Never from the things Sanborn himself wrote around the sculpture: his December 1989 letter to Agency employees about the work in progress, the 1991 Cryptogram pages with Webster's dedication remarks, and his August 2025 open letter. Each is slid along the copper at every offset, both directions, on the standard, KRYPTOS and vocabulary tables.

## Hypothesis (domain expert)

Family 1, running key from a new source (C6(a) 'the keys were concealed', C7 'instructions in the earlier text', C27: Sanborn's own documents). Texts, letters only, OCR '|' read as I: (1) Sanborn's 15 December 1989 letter to Agency employees ('Dear Agency Employees ... Sincerely, Jim Sanborn'), (2) the 1991 Cryptogram pages carrying Webster's 5 November 1990 dedication remarks and the Cryptolog story (both in sources/sanborn-1989-letter-and-webster-1990-cryptogram.txt), (3) the August 2025 open letter (sources/openletter-2025.txt). Key letter at place i: source[(o + i) mod len], every offset o, source forwards and reversed. Setups: the 24 standard/KRYPTOS conventions, plus each vocabulary word's keyword alphabet on both sides with the key read on it or on the standard alphabet, three modes. Statistic: mismatches among the 24 known letters; survivors are within 3; controls are ten shuffled coppers through the same sweep. OCR errors cost at most a few mismatches near the cribs.

## Prediction

No source, offset, direction and setup comes within three mismatches of the 24 known letters, beyond what the ten shuffled coppers reach; the best is about as close as the best on the shuffles. Zero candidates pass.

## Method

1. Extract the three texts as letters.
2. For each source, direction and offset, read the key letter under each known place.
3. For each setup, count the known places where the carved letter would not come out; keep the fewest and all within three.
4. Repeat on ten shuffled coppers.

## Result

Candidates returned: 0. Passed all gates: 0. Best crib hits among all candidates: 0/24
(no candidates).
Best loss: None (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: 0034-complete-the-key-at-surviving-periods.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| - | no candidates | | | | |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "running key from Sanborn's own letters",
 "sources": {
  "letter 1989": 2179,
  "Cryptogram 1991 (Webster remarks, Cryptolog story)": 4887,
  "open letter 2025": 2228
 },
 "setups": 390,
 "trials": 7249320,
 "k4_fewest_mismatches": 15,
 "k4_within_3": [],
 "k4_within_3_count": 0,
 "controls_fewest": [
  15,
  15,
  16,
  16,
  16,
  15,
  15,
  16,
  16,
  15
 ],
 "controls_within_3": [
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0
 ]
}
```

Notes: Sources letter 1989 (2179 letters), Cryptogram 1991 (Webster remarks, Cryptolog story) (4887 letters), open letter 2025 (2228 letters); 390 setups; 7,249,320 trials. K4: fewest mismatches 15, 0 within 3. Ten shuffled coppers: fewest [15, 15, 16, 16, 16, 15, 15, 16, 16, 15], within 3 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0].


