# 0198-substitution-then-the-compiled-libraries: F9.1, second part: a one-to-one substitution, then each move in the three compiled libraries (mixed matrix triples, keyword triples, Nihilist squares): exact

**Family:** 9-substitution-then-transposition  
**Parent:** 0197-substitution-then-every-newer-move  
**Decision:** reverted  
**Run:** 2026-10-17T01:42:54+00:00, 37.7 s, status ran  
**Time by phase:** design 0 s, implement 0 s, test 0 s, run 38 s, record 0 s

## In plain words

The same check as 0197, letter swaps followed by a shuffle, for the three biggest families of shuffles the project has built: about 240 million of them.

## Walkthrough, by hand

1. Take one of 0158's triples: rows of 30 read by columns, rows of 9 read by reversed columns, rows of 41 read clockwise.
2. Follow each known letter to its carved place.
3. The three Es must all show one carved letter; the other repeated letters likewise; different letters different carved letters.
4. One mismatch kills the route; a route that passes is counted.
5. All three libraries, on K4 and on scrambled copies.

## Worked example (generated)

```
the one-to-one test inserted into each library's C source:
for (int e = 0; e < 24; e++) land[e] = wh[PIDX[e]];
    {   /* one-to-one substitution test (F9.1): survivors counted at period 0, order A */
        for (int t = 0; t < T; t++) {
            int a_[26], b_[26], ok_ = 1;
            for (int x = 0; x < 26; x++) { a_[x] = -1; b_[x] = -1; }
            for (int e = 0; e < 24 && ok_; e++) {
                int c_ = CI[0][t][land[e]], p_ = PI[0][e];
                if (a_[p_] < 0 && b_[c_] < 0) { a_[p_] = c_; b_[c_] = p_; }
                else if (a_[p_] != c_ || b_[c_] != p_) ok_ = 0;
            }
            if (ok_) live[(0 * T + t) * (PMAX + 1) + 0]++;
        }
        return;
    }
```

## Lineage

Inherits from 0197-substitution-then-every-newer-move. What changed: F9.1's list, the three entries 0197 left out because their builders are compiled into their own testers: 0158's mixed matrix triples (three stages of rows-of-w readings, every width 2-96, now including the all-narrow triples 0134 had covered for keys only), 0162's triples with a keyword columnar, 0167's Nihilist square with three blanks at eight places and every key of each order. Each experiment's own C builder is reused unchanged except its per-route test, swapped for 0106's one-to-one test (equal known letters on equal carved letters, different on different); survivors are counted per text. K4 against the same shuffled copies those experiments used.

## Hypothesis (domain expert)

F9 (substitution first, transposition last; the Zodiac 340 construction), A9. Model c = route(sigma(p)), sigma any permutation of 26 letters; 24 known letters with 13 different give 11 equalities and the inequalities. Statistic: surviving routes, K4 against copies.

## Prediction

No route survives on K4 or the copies. Zero candidates.

## Method

1. Load 0158, 0162 and 0167; replace only the per-route test in their C source with the one-to-one test.
2. Run their own job lists through their own workers (8 processes).
3. Read survivors per text from the counter slot the periodic test never uses (period 0).

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
 "family": "one-to-one substitution, then the moves of 0158, 0162 and 0167 (their own builders), exact",
 "per_library": {
  "0158 mixed matrix triples": {
   "routes": 107012733,
   "first_stages_done": 380,
   "first_stages_total": 380,
   "k4": 0,
   "copies": [
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
  },
  "0162 keyword triples": {
   "routes": 20370476,
   "first_stages_done": 223,
   "first_stages_total": 223,
   "k4": 0,
   "copies": [
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
  },
  "0167 Nihilist": {
   "routes": 116121600,
   "jobs_done": 80,
   "jobs_total": 80,
   "k4": 0,
   "copies": [
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
 },
 "routes_total": 243504809,
 "survivors_k4": 0,
 "seconds": 38,
 "exhaustive": "per library as reported (jobs done)"
}
```

Notes: 0158 mixed matrix triples: 107,012,733 routes, survivors K4 0 (copies 0-0); 0162 keyword triples: 20,370,476 routes, survivors K4 0 (copies 0-0); 0167 Nihilist: 116,121,600 routes, survivors K4 0 (copies 0-0)


