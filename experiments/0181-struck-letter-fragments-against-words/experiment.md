# 0181-struck-letter-fragments-against-words: F2.1: after striking out every copy of one or two letters, the plaintext a repeating key of 24 or 25 forces outside the known runs, matched against the dictionary

**Family:** 2-masked-then-keyed  
**Parent:** 0057-letter-nulls-outside-the-cribs  
**Decision:** reverted  
**Run:** 2026-10-17T00:27:14+00:00, 1.4 s, status ran  
**Time by phase:** design 0 s, implement 0 s, test 0 s, run 1 s, record 0 s

## In plain words

Perhaps some letters on the copper are fillers: every Q, say, to be ignored. 0057 struck them out and found a repeating secret word of 24 or 25 letters could still fit, but no more often than by chance. Such a long word is mostly fixed by the known letters, so it decrypts most of the rest of the message. We read those decrypted pieces and look for real words, and do the same on scrambled copies.

## Walkthrough, by hand

1. Strike every Q outside the known runs; BERLINCLOCK moves left by the number struck before it.
2. On the sculpture's table, at key length 24, each known letter fixes the key letter of its slot.
3. Every other place in a fixed slot can now be read.
4. Look along those readings, away from the known words, for real words of 6 letters or more.
5. Do the same on scrambled copies.

## Worked example (generated)

```
Q at [26, 27, 39, 42]; struck outside the known runs: [39, 42]; BERLINCLOCK moves from 64-74 to 62-72
```

## Lineage

Inherits from 0057-letter-nulls-outside-the-cribs. What changed: F2.1, the gap 0057 left. 0057 struck every copy of one or two letters outside the known runs (351 masks) and found the smallest repeating key that fits, 24-27, as often as random strike-outs. It did not read what those keys force. Here, for every mask and every setting that fits at length 24 or 25 (12 table rules), the key letters the 24 known letters fix decrypt the other places in the same slots; the runs of forced letters outside the known runs are searched for dictionary words of 6 or more letters. Control: the same masks on ten copies that keep the carved letters at the 24 known places and shuffle the other 73 (each mask strikes the same number of letters).

## Hypothesis (domain expert)

Scheidt: 'I masked the English language' (C2); filler letters by letter are a hand masking device (F2). Model: carved letters of the struck set outside the runs are nulls; the rest is a periodic tableau cipher of period P on standard/KRYPTOS alphabets (Vigenere, Beaufort, variant). At P = 24, 25 the known letters fix most key slots, so most of the message is forced. Statistic: settings whose forced fragments hold a dictionary word of 6+ letters, and the longest such word, K4 against 10 kept-place copies under the same masks.

## Prediction

Settings with a 6+ letter word in the forced fragments: K4 inside the copies' range; the longest word no longer than on copies. Zero candidates.

## Method

1. For each mask (351) and text: strike the letters, renumber the known places.
2. For each of 12 table rules and P = 24, 25: if the forced key values agree, decrypt every place whose slot is forced.
3. Search the forced runs outside the known runs for dictionary words of 6-15 letters.
4. K4 against 10 kept-place copies.

## Result

Candidates returned: 0. Passed all gates: 0. Best crib hits among all candidates: 0/24
(no candidates).
Best loss: None (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| - | no candidates | | | | |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "family": "letter nulls (every copy of one or two letters outside the runs), then a periodic tableau at P 24, 25; forced plaintext outside the runs read for words",
 "masks": 351,
 "rules": 12,
 "periods": [
  24,
  25
 ],
 "min_word": 6,
 "fitting_settings": {
  "k4": 1620,
  "copies": [
   1320,
   1524,
   1416,
   1332,
   1020,
   1620,
   1608,
   1608,
   1584,
   1344
  ]
 },
 "settings_with_a_word": {
  "k4": 0,
  "copies": [
   0,
   10,
   0,
   5,
   0,
   5,
   0,
   32,
   12,
   0
  ]
 },
 "longest_word": {
  "k4": 0,
  "copies": [
   0,
   6,
   0,
   6,
   0,
   6,
   0,
   6,
   7,
   0
  ]
 },
 "k4_examples": [],
 "copies": "10 copies keeping the 24 known places, other 73 shuffled (seed 1810), same masks",
 "exhaustive": true
}
```

Notes: fitting settings K4 1620 (copies 1020-1620); with a 6+ letter word K4 0 (copies 0-32); longest K4 0 (copies 0-7)


