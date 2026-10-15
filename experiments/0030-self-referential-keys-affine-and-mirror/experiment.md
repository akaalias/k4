# 0030-self-referential-keys-affine-and-mirror: The text as its own key: the ciphertext under every index rule, and the message keyed by itself backwards

**Family:** 1-keyed-periodic  
**Parent:** 0025-autokeys-with-mixed-alphabets  
**Decision:** reverted  
**Run:** 2026-10-15T07:40:37+00:00, 0.3 s, status ran  
**Time by phase:** design 12 s, implement 65 s, test 1 s, run 0 s, record 0 s

## In plain words

An autokey uses the text itself as the secret word, a fixed distance back. We widen that: the key for each letter may be the carved letter at any fixed stride and start, forwards or backwards, or the message letter the same distance from the other end. Because the carved letters are all known, the first kind is checked at every known letter at once. The second kind pairs the two known words with each other in the mirror, which gives a direct check too.

## Walkthrough, by hand

1. Rule: stride 3, start 5. The key for position 1 is the carved letter at 5, for position 2 at 8, and so on, wrapping past 97.
2. Position 22 (E) gets the carved letter at 5 + 3 x 21 = 68, T.
3. On the sculpture's table with Vigenere, E under T gives some letter; compare with the carved F at 22.
4. Do this for all 24 known letters; count the misses; any miss kills the rule.
5. Mirror: with centre 97, position 22 is keyed by position 75, which is not known, but position 24 is keyed by 73, the C of CLOCK, which is known: S under C must give the carved R.
6. Eleven such pairs decide the mirror at once.

## Worked example (generated)

```
ciphertext self-key, stride 3, start 5, KRYPTOS alphabet throughout, Vigenere

pos  plain  key pos  key  E+key  carved  match
 22    E       69     T     I      F     no
 23    A       72     F     N      L     no
 24    S       75     W     P      R     no
 64    B        1     O     G      N     no
 65    E        4     R     F      Y     no

mirror key, centre 97 (position i keyed by position 98-i): position 24 (S) is keyed by 74 (K), 25 (T) by 73 (C), ... 34 (T) by 64 (B)
chain under kry/kry/kry Vigenere: breaks after 24 letters
```

## Lineage

Inherits from 0025-autokeys-with-mixed-alphabets. What changed: Autokey generalised. The key letter for position i is the ciphertext letter at a i + b mod 97 for every a and b, which includes every lag and every mirror of the ciphertext; or the plaintext letter at o - i mod 97, the message read backwards from any point.

## Hypothesis (domain expert)

Sanborn's mirrors and 'spatial systems' (C3) and the NSA's autokey guess (C11a) meet in self-keyed systems. Ciphertext self-key: c[i] = E(p[i], c[(a i + b) mod 97]); since every key letter is a carved letter, all 24 cribs are exact checks for each (a, b) and convention, 9,312 rules x 24 conventions, and a survivor decrypts the whole text at once. Plaintext mirror key: c[i] = E(p[i], p[(o - i) mod 97]) for every o; a crib forces its partner's plaintext letter and the chain closes as in 0012, with up to eleven exact checks where EASTNORTHEAST and BERLINCLOCK mirror onto each other. Survivors with 60 or more forced letters are scored as English against ten shuffled controls; fully forced texts are submitted. Bounds: complete for these rules and 24 conventions.

## Prediction

No ciphertext rule passes all 24 checks; the best passes 5 or 6. No mirror centre keeps the chain consistent beyond chance, and the large closures read as noise. Zero candidates pass.

## Method

1. For each (a, b) with a in 1-96 and b in 0-96 and each convention, encipher each known letter with the carved letter at a i + b and count mismatches.
2. Decrypt any zero-mismatch rule and submit.
3. For each mirror centre o and convention, chain forced plaintext letters from the cribs through the mirror; reject on conflict.
4. Score closures of 60 or more letters as English; repeat on ten shuffles; submit fully forced texts.

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
 "family": "self-referential keys: ciphertext at a i + b, plaintext at o - i",
 "conventions": 24,
 "ciphertext_rules": 223488,
 "ciphertext_best_mismatches": 6,
 "ciphertext_survivors": 0,
 "mirror_centres": 97,
 "mirror_consistent_pairs": 0,
 "mirror_fully_forced": 0,
 "mirror_best_closures": [],
 "shuffled_control_best": [
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null
 ]
}
```

Notes: Ciphertext self-key: 223488 rules, best 6 mismatches, 0 survivors. Mirror key: 0 consistent (centre, convention) pairs, 0 fully forced; best closure None vs shuffled [].


