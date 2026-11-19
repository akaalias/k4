# 0285-f16.8-an-artists-twist-on-k1-k2s-method: F16.8: K1/K2's keyed tableau with a hand-made twist: (a) the key word restarts at each sentence, so each known run sits at its own phase of a dictionary word (or under its own word); (b) enciphering and deciphering alternate (by letter, by known run, by carved line) under a periodic key 1-26; (c) the tableau read from the right or the bottom (reversed alphabets); on the 24 and the 20 official letters; K4 against 50 shuffles, plants

**Family:** 16-simple-hand-methods  
**Parent:** 0171-two-parts-with-their-own-keys  
**Decision:** reverted  
**Run:** 2026-11-19T08:49:23+00:00, 121.7 s, status ran  
**Time by phase:** design 35 s, test 23 s, run 122 s, record 0 s

## In plain words

K1 and K2 were made by looking up each letter on the copper table with a repeating key word. An artist could change that simply: start the key word again at each new sentence, switch between enciphering and deciphering, or read the table from the other side. Each change is tested exactly against the known letters, on the carving and on scrambled copies.

## Walkthrough, by hand

1. Take the KRYPTOS table and the word PALIMPSEST.
2. Under EASTNORTHEAST find the key letters the table needs; write them as steps from the first one.
3. Look for those steps anywhere in PALIMPSESTPALIMPSEST...: if found, the key could have restarted there.
4. Do the same for BERLINCLOCK; a word found in both, at any two places, fits.
5. For alternation: with key length 7, use Vigenere on odd places and its inverse on even ones; the places in the same slot must need the same key letter.
6. Repeat for every word, table, form and on scrambled copies.

## Worked example (generated)

```
KRYPTOS table, Vigenere: the key each known place needs, as steps from the run's first key letter

  places 22-34: key RDUMRIYWOYNKY  steps [0, 9, 20, 17, 0, 14, 1, 22, 4, 1, 18, 25, 1]
  places 64-74: key ELYOIECBAQK  steps [0, 6, 17, 20, 4, 0, 24, 23, 22, 9, 15]

A key word restarted at a sentence break fits when both step lists occur in the word written round and round.
```

## Lineage

Inherits from 0171-two-parts-with-their-own-keys. What changed: F16.8 (issue #123). Prior coverage: restarts at carved lines (0128), one split between the runs with free repeating keys (0171), the tableau by rows and columns as a running key (0017), Vigenere/Beaufort/variant on standard and KRYPTOS alphabets (0005). New here: (a) a dictionary or puzzle key word whose phase restarts unseen between the runs (each run's forced key a cyclic stretch of the same word, any indicator shift), or a different word per run; (b) the form switching between encipher and decipher within one periodic key; (c) the plain, cipher and key alphabets each standard, KRYPTOS or either reversed (the tableau read from the right or from the bottom).

## Hypothesis (domain expert)

Sanborn, 2009 oral history (knowledge/sources/aaa-oral-history-2009-kryptos.md): systems 'that didn't necessarily depend on mathematics' which he could 'modify in a myriad of ways. So that even he would not know what it says'; the plaintext cut 'into strips in sentences'. FT 2025: 'It is a solid system, and I fucked with it' (C-FT, 02-sanborn-said.md). A16 (12-assumptions.md): a standard system plus one amateur's change. Model: c = T(p, k) on a tableau with plain alphabet A_p, cipher alphabet A_c, key numbering A_k, each in {STD, KRY, STD reversed, KRY reversed}, form Vigenere, Beaufort or variant. (a) k_i = W[(phi_r + i) mod L] + s for i in run r, W a word of the dictionary or the puzzle vocabulary, phi_r free per run (restart at an unseen sentence break), s a shift; exact match of each run's forced key (13 or 9, and 11 letters) against every cyclic stretch of every word. (b) one periodic key of length 1-26, the form at each place drawn from a pair (vig/var = encipher/decipher, vig/beau, beau/var) by letter parity, by known run or by carved line (lines 2, 3, 4 = places 5-35, 36-66, 67-97); exact consistency, fit counts against shuffles, the forced key checked for a word. (c) is (a) and (b) over the reversed alphabets. Chance per word and run of 9 or more letters: about L x 26 x 26^-9.

## Prediction

(a) no word matches both runs on K4 (nor on shuffles; plants found); single-run matches rare and as frequent on shuffles. (b) no fit at short key lengths; fits from about 20 up at the shuffles' rate, no key word. (c) as (a) and (b). Zero candidates unless a word fits both runs.

## Method

1. Alphabets STD, KRY and their reverses for plain, cipher and key numbering (64 tables), three forms.
2. (a) For each text and table-form: the forced key on run 1 (22-34; 26-34 without EAST) and run 2 (64-74), as differences from its first letter; looked up in an index of every cyclic stretch of that length of every word (lengths 2-24), also normalised; a word in both runs is a fit.
3. (b) For each table, form pair, pattern and key length 1-26: same-slot places must force the same key letter.
4. K4, 50 shuffles, 6 plants.

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
 "item": "F16.8",
 "alphabets": [
  "std",
  "kry",
  "std_rev",
  "kry_rev"
 ],
 "tables": 64,
 "forms": [
  "vig",
  "beau",
  "var"
 ],
 "words": 234451,
 "a": "each run's forced key against every cyclic stretch of every word of 2-24 letters (dictionary and puzzle), any shift, per key numbering; both runs = same word, phases free",
 "b": "periodic key 1-26, form switching within a pair (vig/var, vig/beau, beau/var) by letter parity, by known run, or by carved line (5-35, 36-66, 67-97); exact",
 "c": "the reversed alphabets (tableau read from the right or the bottom) are in (a) and (b)",
 "prior": "0128 restarts at carved lines; 0171 free keys split between runs; 0017 tableau as running key; 0005 forms and alphabets",
 "summary": {
  "k24": {
   "k4": {
    "a_both": 0,
    "a_single": 0,
    "b_fits": 12,
    "b_shortest": 26
   },
   "copies_max": {
    "a_both": 0,
    "a_single": 0,
    "b_fits": 84,
    "b_shortest": 99
   },
   "copies_median": {
    "a_both": 0,
    "a_single": 0,
    "b_fits": 12,
    "b_shortest": 26
   },
   "copies_min_b_shortest": 26,
   "p_a_single": 1.0,
   "p_b_fits": 0.686,
   "p_b_shortest": 0.843,
   "k4_a_hits": [],
   "k4_b_fits_short": []
  },
  "k20": {
   "k4": {
    "a_both": 0,
    "a_single": 0,
    "b_fits": 960,
    "b_shortest": 25
   },
   "copies_max": {
    "a_both": 0,
    "a_single": 0,
    "b_fits": 1038,
    "b_shortest": 25
   },
   "copies_median": {
    "a_both": 0,
    "a_single": 0,
    "b_fits": 984,
    "b_shortest": 24
   },
   "copies_min_b_shortest": 24,
   "p_a_single": 1.0,
   "p_b_fits": 1.0,
   "p_b_shortest": 1.0,
   "k4_a_hits": [],
   "k4_b_fits_short": []
  }
 },
 "plants": [
  {
   "id": "plant0",
   "known": "k24",
   "word": "PECULATE",
   "found": true
  },
  {
   "id": "plant0",
   "known": "k20",
   "word": "PECULATE",
   "found": true
  },
  {
   "id": "plant1",
   "known": "k24",
   "word": "INSEER",
   "found": true
  },
  {
   "id": "plant1",
   "known": "k20",
   "word": "INSEER",
   "found": true
  },
  {
   "id": "plant2",
   "known": "k24",
   "word": "BALLOONET",
   "found": true
  },
  {
   "id": "plant2",
   "known": "k20",
   "word": "BALLOONET",
   "found": true
  },
  {
   "id": "plant3",
   "known": "k24",
   "word": "CONJUROR",
   "found": true
  },
  {
   "id": "plant3",
   "known": "k20",
   "word": "CONJUROR",
   "found": true
  },
  {
   "id": "plant4",
   "known": "k24",
   "word": "DONKEYWORK",
   "found": true
  },
  {
   "id": "plant4",
   "known": "k20",
   "word": "DONKEYWORK",
   "found": true
  },
  {
   "id": "plant5",
   "known": "k24",
   "word": "BALLADLING",
   "found": true
  },
  {
   "id": "plant5",
   "known": "k20",
   "word": "BALLADLING",
   "found": true
  }
 ],
 "plants_b": [
  {
   "id": "bplant0",
   "known": "k24",
   "pattern": "lines101",
   "pair": [
    "vig",
    "beau"
   ],
   "L": 12,
   "fits": true,
   "shortest_fit": 12,
   "found": true
  },
  {
   "id": "bplant0",
   "known": "k20",
   "pattern": "lines101",
   "pair": [
    "vig",
    "beau"
   ],
   "L": 12,
   "fits": true,
   "shortest_fit": 12,
   "found": true
  },
  {
   "id": "bplant1",
   "known": "k24",
   "pattern": "lines011",
   "pair": [
    "beau",
    "var"
   ],
   "L": 7,
   "fits": true,
   "shortest_fit": 7,
   "found": true
  },
  {
   "id": "bplant1",
   "known": "k20",
   "pattern": "lines011",
   "pair": [
    "beau",
    "var"
   ],
   "L": 7,
   "fits": true,
   "shortest_fit": 7,
   "found": true
  },
  {
   "id": "bplant2",
   "known": "k24",
   "pattern": "runs01",
   "pair": [
    "vig",
    "beau"
   ],
   "L": 7,
   "fits": true,
   "shortest_fit": 7,
   "found": true
  },
  {
   "id": "bplant2",
   "known": "k20",
   "pattern": "runs01",
   "pair": [
    "vig",
    "beau"
   ],
   "L": 7,
   "fits": true,
   "shortest_fit": 7,
   "found": true
  },
  {
   "id": "bplant3",
   "known": "k24",
   "pattern": "runs01",
   "pair": [
    "vig",
    "var"
   ],
   "L": 8,
   "fits": true,
   "shortest_fit": 8,
   "found": true
  },
  {
   "id": "bplant3",
   "known": "k20",
   "pattern": "runs01",
   "pair": [
    "vig",
    "var"
   ],
   "L": 8,
   "fits": true,
   "shortest_fit": 8,
   "found": true
  }
 ],
 "copies": 50,
 "quirks": "the extra L of row N and the four repeated columns change no lookup: not a separate case",
 "exhaustive": true,
 "aws_cost_estimate_dollars": 0.1
}
```

Notes: k24: K4 {'a_both': 0, 'a_single': 0, 'b_fits': 12, 'b_shortest': 26}, copies max {'a_both': 0, 'a_single': 0, 'b_fits': 84, 'b_shortest': 99}; k20: K4 {'a_both': 0, 'a_single': 0, 'b_fits': 960, 'b_shortest': 25}, copies max {'a_both': 0, 'a_single': 0, 'b_fits': 1038, 'b_shortest': 25}; plants (a) 12/12, (b) 8/8


