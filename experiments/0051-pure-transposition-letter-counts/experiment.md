# 0051-pure-transposition-letter-counts: Could K4 be its own letters rearranged? A count of the known letters against the carved ones

**Family:** 6-transposition-then-tableau  
**Parent:** 0006-columnar-then-tableau-period-survival  
**Decision:** reverted  
**Run:** 2026-10-15T12:08:30+00:00, 0.1 s, status ran  
**Time by phase:** design 0 s, implement 1 s, test 0 s, run 0 s, record 0 s

## In plain words

If the fourth message were just its own letters shuffled, like an anagram, then every letter of the message would be somewhere on the copper. We know 24 letters of the message. So we count: does the copper have enough Es, enough Ns, enough Rs to spell them? One shortfall is enough to rule out every way of shuffling at once.

## Walkthrough, by hand

1. Write out EASTNORTHEAST and BERLINCLOCK.
2. Count the Es: E-A-S-T-N-O-R-T-H-E-A-S-T has two, B-E-R-L-I-N-C-L-O-C-K has one, so the message needs at least three Es.
3. Count the Es on the copper: OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR has two, at places 45 and 92.
4. Two is less than three, so no rearrangement of the copper can put three Es where the message has them.
5. Check the other letters the same way.

## Worked example (generated)

```
letter  needed by the cribs  on the copper
  A            2                4
  B            1                5
  C            2                2
  E            3                2   short
  H            1                2
  I            1                4
  K            1                8
  L            2                4
  N            2                3
  O            2                5
  R            2                4
  S            2                6
  T            3                6
```

## Lineage

Inherits from 0006-columnar-then-tableau-period-survival. What changed: Every earlier transposition experiment put a substitution (the table) after the reordering. Here the substitution is taken away: if K4 were only a rearrangement of its message, the carved letters would be the message's letters in another order, and the letter counts alone decide it.

## Hypothesis (domain expert)

C9(a) reads 'the letters sitting there in plain sight' as a pure transposition: the ciphertext is a permutation of the plaintext, and C8(d) proposes KRYPTOS as a transposition key. Any permutation preserves the letter multiset, so the 24 crib letters must be a sub-multiset of the 97 carved letters. Count each crib letter against the copper, for the carved 97, for the 98 with the K3 question mark (C18), and for each one-letter deletion (the copper with a spurious letter). If any count fails in every reading, every transposition, keyed or route, single or double, KRYPTOS-keyed or not, is excluded without enumerating keys. Bounds: exact.

## Prediction

At least one crib letter is short on the copper in the 97 and 98 readings and under every one-letter deletion, so pure transposition is excluded; it survives only if one carved letter is wrong and should be that letter. Zero candidates.

## Method

1. Count the 24 known letters by letter.
2. Count the carved letters.
3. List every letter whose need exceeds its supply.
4. Repeat with the question mark added and with each of the 97 letters deleted.
5. Say which single carving error, if any, would make the counts possible.

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
 "family": "pure transposition (any permutation of the 97 carved letters)",
 "need": {
  "E": 3,
  "A": 2,
  "S": 2,
  "T": 3,
  "N": 2,
  "O": 2,
  "R": 2,
  "H": 1,
  "B": 1,
  "L": 2,
  "I": 1,
  "C": 2,
  "K": 1
 },
 "short_carved": {
  "E": [
   3,
   2
  ]
 },
 "short_98_with_question_mark": {
  "E": [
   3,
   2
  ]
 },
 "deletions_that_fit": [],
 "replacements_that_fit": 93,
 "replacement_letters_that_fit": [
  "E"
 ],
 "replacement_examples": [
  "place 1: O to E",
  "place 2: B to E",
  "place 3: K to E",
  "place 4: R to E",
  "place 5: U to E",
  "place 6: O to E"
 ]
}
```

Notes: Crib letters short on the copper: {'E': (3, 2)}; with the question mark: {'E': (3, 2)}; one-letter deletions that fit: 0. A single carved letter changed to E would make the counts fit (93 ways).


