# 0104-the-message-keyed-by-itself-through-k3s-rule: The message as its own key, read through K3's counting rule: key letter for place i is the message letter at a + b i mod 97

**Family:** 1-keyed-periodic  
**Parent:** 0003-plaintext-autokey-chained  
**Decision:** reverted  
**Run:** 2026-10-15T20:13:10+00:00, 5.2 s, status ran  
**Time by phase:** unattributed 1 s, run 5 s, record 0 s

## In plain words

Here the message is its own key: to encrypt a letter, you add another letter of the message, picked by K3's counting rule. Because that rule visits places in a loop, one known letter gives the next one in its loop, and so on all the way round, until the loop comes back to another known letter. If the two disagree, the setting is impossible. We try every start, step and table rule.

## Walkthrough, by hand

1. Choose a = 0, b = 96: place i takes its key from the message letter at place 99 - i.
2. Place 22 is E, carved F: so E plus the key at place 77 gives F, and the message letter at 77 is F minus E.
3. Place 77 in turn takes its key from place 22, which closes the loop: check that it agrees.
4. Longer loops run through many places; a loop with two known letters is a check.
5. Try every start, step and table rule.

## Worked example (generated)

```
a = 0, b = 96 (the mirror): place i takes its key from the message letter at place 99 - i
sculpture's alphabet, Vigenere: carved = message + key

place  known  carved  key place  message letter there = carved - known
   22      E       F         77             R
   23      A       L         76             D
   24      S       R         75             U
   25      T       V         74             M
   64      B       N         35             E
   65      E       Y         34             L
```

## Lineage

Inherits from 0003-plaintext-autokey-chained. What changed: 0003 chained plaintext autokey, where the key for place i is the message letter a fixed distance back. Here the key is the message letter at a + b i mod 97 for every a and b, K3's counting rule, the mirror (b = -1) included. Because the rule is a permutation of the 97 places, each known letter fixes every letter of its cycle, so the test is exact and, where it passes, it decrypts.

## Hypothesis (domain expert)

Companion to 0103 (the copper keyed by itself). Model: c_i = E(p_i, p_{f(i)}), f(i) = a + b i mod 97, b = 1-96 (97 is prime, so f is a permutation), a = 0-96, f without fixed points among the known places; E in 8 classes (plain and cipher alphabets standard or KRYPTOS; Vigenere, Beaufort; key letters numbered on the plain alphabet), plus variant Beaufort via the sign. Propagation: if p_i is known, p_{f(i)} = the key that turns p_i into c_i; if p_{f(i)} is known, p_i = D(c_i, p_{f(i)}). Each cycle of f containing a known place is fixed completely; a contradiction with another known letter on the same cycle kills the setting. Survivors are decrypted on every fixed place and scored. C6, C13 ('mirrors'). Ten shuffled coppers.

## Prediction

No setting survives where a cycle carries two or more known letters; the survivors, if any, are settings whose cycles each hold one known letter, as often on the coppers, and they decrypt to noise. Zero candidates.

## Method

1. For each a, b and class, follow the cycles of f from the known places, filling message letters forward and backward.
2. Stop at the first contradiction.
3. Count surviving settings and their checks on K4 and ten shuffled coppers.
4. Decrypt survivors on every fixed place and score them as English.

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
 "family": "the message as its own key through K3's rule f(i) = a + b i mod 97",
 "maps": 7031,
 "rules": 12,
 "k4_survivors": 0,
 "controls_survivors": [
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
 ],
 "k4_checks_histogram": {},
 "k4_top_survivors": [],
 "controls": "10 shuffled coppers (seed 104), identical search"
}
```

Notes: 7,031 maps x 12 rules. Settings with no contradiction: K4 0, controls [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]. K4 survivors' checks: {}. Full decryptions returned: 0.


