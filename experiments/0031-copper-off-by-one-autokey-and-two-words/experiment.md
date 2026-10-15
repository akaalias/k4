# 0031-copper-off-by-one-autokey-and-two-words: The copper off by one letter: the chained autokey and the two-word tests rerun with a letter dropped or added anywhere

**Family:** 1-keyed-periodic  
**Parent:** 0012-plaintext-autokey-chained-from-cribs  
**Decision:** reverted  
**Run:** 2026-10-15T07:42:15+00:00, 0.8 s, status ran  
**Time by phase:** design 3 s, implement 57 s, test 5 s, run 1 s, record 0 s

## In plain words

The second message on the sculpture was carved with one letter missing, and the artist has been vague about whether the fourth has 97 or 98 letters. So we redo the two sharpest tests from yesterday on every version of the text that has one letter removed, or one unknown letter slipped in, at every possible place. If a single carving slip was hiding the method, one of these versions would suddenly chain together or solve.

## Walkthrough, by hand

1. Suppose the carver dropped a letter right after position 40. Then the carved letters from 41 on are one place early: the true position 65 is the carved 64, and so on.
2. Take lag 13 and the sculpture's alphabet with Vigenere.
3. Position 22 (E) is keyed by position 9, and in turn keys position 35, exactly as before, because the slip is after 40.
4. But position 64 (B) is now keyed by the true position 51, which is the carved 50, and keys the true 77, the carved 76.
5. Chain every known letter through its lag with the corrected numbering and see whether the chain closes without contradiction.
6. Repeat for a slip at every position, and for an extra letter at every position.

## Worked example (generated)

```
variant: the carved letter at 41 deleted; lag 13; KRYPTOS alphabet throughout, Vigenere

chain from the cribs breaks after forcing 28 letters
.....................EASTNORTHEASTB............I............W..BERLINCLOCK............U.........
```

## Lineage

Inherits from 0012-plaintext-autokey-chained-from-cribs. What changed: The one-letter-error parameter applied to two exact tests at once. The carved text is taken with one letter deleted at each of 97 positions or one unknown letter inserted at each of 98, and the chained plaintext autokey (0012) and the two-word linear test (0014, total length up to 20) run on every variant.

## Hypothesis (domain expert)

K2 was carved with a letter dropped, and Sanborn has said 97, 98 and 100 in the same breath (C17, C18, family G). 0009 applied the parameter to the stretch scores only. The two tests most able to decide a family exactly are the chained plaintext autokey, where every crib forces letters up and down the chain, and the two-word composition, where 24 equations fall on a + b unknowns. Each runs here on 195 variants under the 24 conventions (autokey) and the standard and KRYPTOS alphabets with both signs (two words). An inserted unknown letter breaks the autokey chain where it sits and drops the equation at its position; a deleted letter shifts every later position by one. Convention: crib positions are kept as given in the variant's own numbering, since Sanborn's positions refer to the carved text. Bounds: complete for one insertion or deletion anywhere.

## Prediction

No variant makes the autokey chain consistent at any lag up to 25, and no variant makes a word pair of total length up to 20 consistent. Larger closures and longer pairs behave as on the carved text. Zero candidates pass.

## Method

1. Build the 195 variants.
2. Autokey: for each variant, lag and convention, chain forced letters from the cribs, treating an inserted unknown as a wall; reject on conflict; record consistent lags.
3. Two words: for each variant, alphabet pair, sign and length pair with a + b <= 20, solve the crib equations by weighted union-find; record consistent pairs.
4. Submit fully forced autokey texts and vocabulary word matches.

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
 "family": "one-letter error (insert or delete anywhere) x chained plaintext autokey lags 1-25 x two words a + b <= 20",
 "variants": 196,
 "conventions": 24,
 "two_word_pairs": 19,
 "autokey_variants_with_a_consistent_lag": 0,
 "autokey_consistent_cases": {},
 "autokey_fully_forced": 0,
 "two_word_consistent_cases": [],
 "n_two_word_consistent": 0
}
```

Notes: 196 variants. Autokey lags 1-25: 0 variants have a consistent lag, 0 fully forced (97-letter variants only). Two words with a + b <= 20: 0 consistent cases.


