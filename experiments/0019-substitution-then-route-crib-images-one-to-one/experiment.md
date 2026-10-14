# 0019-substitution-then-route-crib-images-one-to-one: Substitution first, a route last: do the 24 crib images stay one letter to one letter under any route?

**Family:** 9-substitution-then-transposition  
**Parent:** 0018-construction-simulator-fingerprint  
**Decision:** reverted  
**Run:** 2026-10-14T17:39:22+00:00, 1.3 s, status ran  
**Time by phase:** design 27 s, implement 138 s, test 12 s, run 1 s, record 0 s

## In plain words

Suppose each letter of the message was first swapped for another letter, and only then were the letters shuffled into a new order by a grid. The 24 letters we know are then scattered somewhere in the carved text, and each grid tells us where. One rule must hold: one carved letter cannot stand for two different message letters. We check that rule for every grid we have, using the 24 known letters, and count the grids that pass. If none pass, this whole way of building the cipher is out, however the swapping was done.

## Walkthrough, by hand

1. Take the route: write in rows of 7 and read down the columns.
2. The message letter at position 22, the E of EAST, is written at row 4, column 1, and read out 4th: so the carved letter at 4, R, is the swapped E.
3. Position 31, the other E, lands at 32: the carved K.
4. Under a plain swap E must always become the same letter, so R and K already conflict: this route is dead for a plain swap.
5. Under a swap with spare letters, E may have two symbols, so R and K is allowed, but R must then never be the image of another letter.
6. Position 66, the R of BERLIN, lands at 38: the carved T; no conflict.
7. Go through all 24; one clash kills the route.

## Worked example (generated)

```
route: columnar width 7 read down the columns; images of the known letters

plain A: carved images F Z
plain B: carved images H
plain C: carved images K Q
plain E: carved images R S
plain H: carved images B
plain I: carved images P
plain K: carved images K
plain L: carved images J U
plain N: carved images I X
plain O: carved images K V
plain R: carved images T U
plain S: carved images K N
plain T: carved images K U W

homophonic condition: fails; clashes: K from S and T, K from T and O, U from R and T, K from O and C, U from T and L, K from C and K
monoalphabetic condition: fails
```

## Lineage

Inherits from 0018-construction-simulator-fingerprint. What changed: New family, opened by 0018's finding that only substitution followed by transposition reproduces K4's width-21 repeats. The cribs now constrain the ciphertext letters the route sends them to, not the letters at 22-34 and 64-74.

## Hypothesis (domain expert)

Zodiac 340 was a homophonic substitution followed by a transposition, and its width-19 repeats were the trace (knowledge/04-structure.md). K4's eleven width-21 repeats have p about 0.005 under every substitution-last generator and p near 1 under transposition of English (0018). Against: Sanborn's secondhand 'one-to-one mapping' of NYPVTT to BERLIN (knowledge/02-sanborn-said.md, 2011 and 2013 dinners), which says the letters at 64-69 are BERLIN's own images; this family contradicts that reading and is tested because the statistic is the stronger evidence. Model: each plaintext letter goes to one of its symbols (monoalphabetic, or homophonic over the same 26 symbols), then a route T permutes positions. The image of crib position i is ct[T(i)]. Constraint: a ciphertext letter has one plaintext source, so two crib positions with different plaintext letters must have different images; under the stricter monoalphabetic reading, equal plaintext letters must also have equal images. Routes: the 23,930 of 0016 plus the identity. For each route both conditions are checked; survivors are counted against the same test on shuffled K4. A monoalphabetic survivor gets a hill-climb over the unknown letters and a candidate. Bounds: complete for this route set.

## Prediction

Under the homophonic condition, fewer than one route in a hundred survives, about the same rate as on shuffled K4. Under the monoalphabetic condition no route survives. No candidate passes.

## Method

1. Build the route set.
2. For each route, find the ciphertext image of each crib position.
3. Homophonic condition: no ciphertext letter is the image of two different plaintext letters.
4. Monoalphabetic condition: in addition, equal plaintext letters have equal images.
5. Count survivors of each; repeat on five shuffles of K4.
6. For monoalphabetic survivors, hill-climb the unknown mappings by English score and submit the best text.

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
 "family": "substitution (mono or homophonic over 26 symbols) then transposition",
 "routes": 23931,
 "homophonic_survivors": 0,
 "homophonic_survivor_routes": [],
 "monoalphabetic_survivors": 0,
 "monoalphabetic_survivor_routes": [],
 "shuffled_k4_survivors": [
  {
   "homophonic": 0,
   "monoalphabetic": 0
  },
  {
   "homophonic": 0,
   "monoalphabetic": 0
  },
  {
   "homophonic": 0,
   "monoalphabetic": 0
  },
  {
   "homophonic": 0,
   "monoalphabetic": 0
  },
  {
   "homophonic": 0,
   "monoalphabetic": 0
  }
 ]
}
```

Notes: 23931 routes: 0 pass the homophonic condition, 0 the monoalphabetic one; shuffled K4 gives [0, 0, 0, 0, 0] and [0, 0, 0, 0, 0].


