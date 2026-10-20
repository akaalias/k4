# 0206-gromark-high-bases-on-k1-k3-word-tables: F5.3: Gromark growth rules in bases 16-26 on the tables built from K1-K3's words and the 2025 letter (0054's 10,404 pairs), two- and three-term rules with lags to 13, exact, with scrambled copies and a planted Gromark text

**Family:** 5-gromark  
**Parent:** 0054-gromark-bases-k1-k3-word-alphabets  
**Decision:** reverted  
**Run:** 2026-10-20T11:12:37+00:00, 3.5 s, status ran  
**Time by phase:** test 1 s, run 4 s, record 0 s

## In plain words

Gromark grows a long number key from a few starting digits by adding earlier digits. Experiment 54 built tables from the words of the solved messages and only checked small number bases, which the known letters rule out; the larger bases, 16 to 26, were never checked on those tables. We check them now with every growth rule looking up to 13 digits back.

## Walkthrough, by hand

1. Build a table from a solved-message word, say DESPARATLY, and use it for the plain or cipher side.
2. Read off the shift each known letter needs: 13 shifts in a row over EASTNORTHEAST, 11 over BERLINCLOCK.
3. Choose a base, say 20, and a rule, say each digit is the sum of those 5 and 2 back.
4. Check: shift 6 must equal shift 1 + shift 4 mod 20, and so on along both runs.
5. One failure kills the rule; repeat for every rule, base, table and form.

## Worked example (generated)

```
standard plain alphabet, KRYPTOS cipher alphabet, Vigenere: the forced shifts over EASTNORTHEAST

shifts: 8 17 9 3 7 6 12 8 12 9 0 14 13
largest 17: only bases 18-26 are possible
rule (5, 2) in base 20: shift 6 should be shift 1 + shift 4 = 11; it is 6
```

## Lineage

Inherits from 0054-gromark-bases-k1-k3-word-alphabets. What changed: F5.3, found by the positive control C-F5-1d (#73): 0054 built 102 tables from the solved messages' words and the 2025 letter, found no pair admits a base of 15 or less, and so tested no growth rule; but bases 16-26 are admissible and were never tested on these tables (0046 tested them on the vocabulary's tables, 0076/0195 on a free cipher alphabet with the plain side standard). Here 0046's rule test, unchanged in substance, on 0054's pairs: every two-term rule k[i] = k[i-a] + k[i-b] and three-term rule k[i] = k[i-a] + k[i-b] + k[i-c], lags up to 13, every base 16-26 the pair admits, 3 forms, at least six checks inside the known runs, then the stream carried from EASTNORTHEAST to BERLINCLOCK; on K4, ten scrambled copies and a planted text.

## Hypothesis (domain expert)

C22(a) (Gromark; YAR as primer), Bean's Gromark case (knowledge/05-attacks.md). Model: c = C[P(p) + k_i] (or Beaufort and variant forms), plain and cipher alphabets keyword-mixed from K1-K3 plaintext words and the C13/C14 words (0054's pool: 102 alphabets incl. standard and KRYPTOS), key digits in base B with a lagged rule. Each known letter forces a shift; all must be below B; the rule is tested on the 13 and 11 consecutive forced shifts (13 - a and 11 - a checks), at least six (chance about 26^-6 per set), and survivors must carry their full stream from the first run to the second. Statistic: survivors with six or more checks, and survivors consistent with both runs, K4 against each copy.

## Prediction

No rule with six or more checks survives on K4 beyond the copies' count; none carries to the second run. The planted text is found. Zero candidates.

## Method

1. Rebuild 0054's alphabet pool.
2. For each plain and cipher alphabet and form, the 24 forced shifts; the bases from max(16, largest + 1) to 26.
3. Compiled: every rule (78 two-term, 286 three-term), checked on the consecutive shifts in each run; six or more checks to survive; then carry the stream from the first run to the second.
4. K4, ten copies, a planted text; counts compared.

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
 "family": "Gromark growth rules (two- and three-term, lags to 13) in bases 16-26 on 0054's K1-K3-word and 2025-letter tables",
 "alphabets": 102,
 "pairs": 10404,
 "forms": 3,
 "rules": 364,
 "bases": "max(16, largest forced + 1) to 26",
 "min_checks": 6,
 "k4": {
  "survivors": 0,
  "survivors_both_runs": 0,
  "list": []
 },
 "copies_survivors": [
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
 "copies_survivors_both_runs": [
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
 "plant": {
  "plain": "PART/keyword",
  "cipher": "THIRTY/keyword",
  "form": "vig",
  "base": 20,
  "rule": [
   7,
   3
  ],
  "found": true,
  "survivors": 1,
  "survivors_both_runs": 1
 },
 "spot_check": "8960 (table, base, rule) cases checked against Python",
 "controls": "10 shuffled copies (seed 5300)",
 "seconds": 3,
 "exhaustive": "yes"
}
```

Notes: Survivors with >= 6 checks: K4 0 (both runs 0), copies 0-0 (both runs 0-0). Plant found: True.


