# 0025-autokeys-with-mixed-alphabets: Both autokeys again, with the tableau built from the puzzle's own words

**Family:** 1-keyed-periodic  
**Parent:** 0012-plaintext-autokey-chained-from-cribs  
**Decision:** reverted  
**Run:** 2026-10-15T06:43:20+00:00, 2737.4 s, status ran  
**Time by phase:** design 0 s, implement 68 s, test 6 s, run 2737 s, record 0 s

## In plain words

An autokey cipher uses the message itself, or the scrambled text itself, as the secret word. We ruled that out yesterday with the sculpture's two alphabets. But the table could have been built from another word, which changes every sum. So we rebuild the table from each word the puzzle knows and run both autokey checks again: for the scrambled-text version the 24 known letters decide at once; for the message version, each known letter reveals another, and the chain either breaks or fills the whole message.

## Walkthrough, by hand

1. Build the alphabet from ABSCISSA: ABSCIDEFGHJKLMNOPQRTUVWXYZ, and use it for both the message letters and the carved letters, Vigenere.
2. Ciphertext autokey, lag 10: the key for position 22 is the carved letter at 12, L.
3. Look up E in the ABSCISSA alphabet, index 5, and L, index 12; add: 17, which is R in that alphabet. The carved letter at 22 is F, so this is a mismatch.
4. Count mismatches over all known letters past position 10; any mismatch kills this lag for this alphabet.
5. Plaintext autokey, lag 10: the key for position 32 is the message letter at 22, E, which we know, so position 32's message letter must be A; it is, so no conflict yet; position 42's letter follows from position 32's, and so on down the chain.

## Worked example (generated)

```
alphabet from ABSCISSA: ABSCIDEFGHJKLMNOPQRTUVWXYZ; used for message, carved text and key; Vigenere

ciphertext autokey, lag 10:
pos  plain  key = carved at pos-10  E+key  carved  match
 22    E         L                  R      F     no
 23    A         B                  B      L     no
 24    S         S                  I      R     no
 64    B         L                  M      N     no
 65    E         U                  A      Y     no

plaintext autokey, lag 10: chain from the cribs breaks after forcing 24 letters
```

## Lineage

Inherits from 0012-plaintext-autokey-chained-from-cribs. What changed: 0002 and 0012 used the standard and KRYPTOS alphabets only. Here the plain and cipher alphabets are the keyword mixings of every vocabulary word, with the key letters read in the standard, KRYPTOS or the same mixed alphabet.

## Hypothesis (domain expert)

Ciphertext autokey, c[i] = E(p[i], c[i-L]), is decided by the cribs alone: at every crib position past the lag the key letter is a known ciphertext letter, so each (lag, convention) gets up to 24 exact checks. Plaintext autokey, c[i] = E(p[i], p[i-L]), is decided by the chained closure of 0012. Both were dead under the standard and KRYPTOS alphabets (0002, 0003, 0012); the NSA's 1992 'plain-text auto-key' guess (C11a) and Scheidt's keyword alphabets (C5) leave the mixed-alphabet case open. Alphabet pool: standard, KRYPTOS and the keyword mixing of each vocabulary word (63); plain and cipher alphabets range over the pool, the key alphabet over standard, KRYPTOS and the plain alphabet itself; three modes; lags 1-96. Ciphertext autokey: zero mismatches is a survivor. Plaintext autokey: a consistent closure with 60 or more forced letters is scored as English on its non-crib runs against ten shuffled controls, and a fully forced text is submitted. Bounds: complete for this pool and these key-alphabet choices.

## Prediction

Ciphertext autokey: no alphabet triple, mode and lag passes all its checks; the best passes about 6 of 24. Plaintext autokey: every lag up to 25 breaks under every triple; closures with 60 or more letters read as noise against the controls. Zero candidates pass.

## Method

1. Build the alphabet pool and the key-alphabet choices.
2. Ciphertext autokey: for each triple, mode and lag, compare the enciphered crib letter with the carved letter at every crib position past the lag; count mismatches.
3. Plaintext autokey: for each triple, mode and lag, chain forced letters from the cribs to closure; reject on conflict; record forced-letter count.
4. Score large closures as English on non-crib runs; repeat on ten shuffles.
5. Submit fully forced texts.

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
 "family": "ciphertext and plaintext autokey with keyword-mixed alphabets",
 "alphabets": 63,
 "key_alphabet_choices": "standard, KRYPTOS, or the plain alphabet",
 "modes": 3,
 "lags": "1-96",
 "trials": 3429216,
 "ciphertext_autokey_best": {
  "mismatches": 99,
  "setting": null
 },
 "ciphertext_autokey_survivors": 0,
 "plaintext_autokey_lags_dead_under_every_triple": [
  1,
  2,
  3,
  4,
  5,
  6,
  7,
  8,
  9,
  10,
  11,
  12,
  13,
  14,
  15,
  16,
  17,
  18,
  19,
  20,
  21,
  22,
  23,
  24,
  33,
  34,
  35,
  36,
  37,
  38,
  39,
  40,
  41,
  42,
  43,
  44,
  45,
  46,
  47,
  48,
  49
 ],
 "plaintext_autokey_best_closures": [
  {
   "score": -6.469,
   "plain": "CARNARVON/keyword",
   "cipher": "SOMEWHERE/keyword",
   "key": "kry",
   "mode": "vig",
   "lag": 29,
   "forced": 82,
   "runs": [
    "STHASNALNGEJFADR",
    "EJJABLYDSMR",
    "FDFIROINMRGOV"
   ]
  },
  {
   "score": -6.488,
   "plain": "LUCIDMEMORY/keyword",
   "cipher": "TWO/keyword",
   "key": "LUCIDMEMORY/keyword",
   "mode": "varbeau",
   "lag": 28,
   "forced": 84,
   "runs": [
    "CXWWLU",
    "TONFYMTOMDK",
    "TRNDINGUZBI"
   ]
  },
  {
   "score": -6.518,
   "plain": "HOWARDCARTER/keyword",
   "cipher": "TUTANKHAMUN/keyword",
   "key": "HOWARDCARTER/keyword",
   "mode": "beau",
   "lag": 28,
   "forced": 84,
   "runs": [
    "HASTKO",
    "IWUWCDRECTV",
    "ICUFINIKIXP"
   ]
  },
  {
   "score": -6.527,
   "plain": "DESPARATLY/keyword",
   "cipher": "SOMEWHERE/keyword",
   "key": "std",
   "mode": "beau",
   "lag": 28,
   "forced": 84,
   "runs": [
    "MENTCG",
    "YDSTOFKMBNA",
    "AZXDIMMGECF"
   ]
  },
  {
   "score": -6.536,
   "plain": "WALL/keyword",
   "cipher": "PALIMPSEST/keyword",
   "key": "std",
   "mode": "varbeau",
   "lag": 28,
   "forced": 84,
   "runs": [
    "BTUMOP",
    "HOMRAVJABAI",
    "NISHDHADEEX"
   ]
  },
  {
   "score": -6.542,
   "plain": "NORTHEAST/keyword",
   "cipher": "LAYER/keyword",
   "key": "kry",
   "mode": "vig",
   "lag": 28,
   "forced": 84,
   "runs": [
    "RETAFJ",
    "HRAEGNLDGUJ",
    "AWISAQOCABX"
   ]
  },
  {
   "score": -6.561,
   "plain": "HOWARDCARTER/keyword",
   "cipher": "BERLINWALL/keyword",
   "key": "kry",
   "mode": "beau",
   "lag": 27,
   "forced": 86,
   "runs": [
    "UCONLGK",
    "SHGRAKHNCJW",
    "HSUESEUHEWY"
   ]
  },
  {
   "score": -6.581,
   "plain": "LOCATION/keyword",
   "cipher": "WALL/keyword",
   "key": "std",
   "mode": "varbeau",
   "lag": 28,
   "forced": 84,
   "runs": [
    "MYBRAL",
    "KAISHEZOBJQ",
    "TLCELMPBUMC"
   ]
  },
  {
   "score": -6.583,
   "plain": "NORTHEAST/keyword",
   "cipher": "CARTER/keyword",
   "key": "NORTHEAST/keyword",
   "mode": "vig",
   "lag": 29,
   "forced": 82,
   "runs": [
    "FTAGLCDSYRLACIFS",
    "SQKELTECABX",
    "YEEDUEBYPECNR"
   ]
  },
  {
   "score": -6.583,
   "plain": "WONDERFUL/keyword",
   "cipher": "SOUTH/keyword",
   "key": "kry",
   "mode": "vig",
   "lag": 29,
   "forced": 82,
   "runs": [
    "TAOSOMDDLOUFEILF",
    "AQGGIROLCAX",
    "PFLCADCOLOBEN"
   ]
  }
 ],
 "plaintext_autokey_fully_forced": 0,
 "shuffled_control_best": [
  -6.608,
  -6.336,
  -6.404,
  -6.472,
  -6.387,
  -6.184,
  -6.257,
  -6.157,
  -6.422,
  -6.442
 ]
}
```

Notes: 3429216 (triple, mode, lag) cases. Ciphertext autokey: best 99 mismatches, 0 survivors. Plaintext autokey: lags dead under every triple [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 33, 34, 35, 36, 37, 38]...; 0 fully forced; best closure -6.469426635667049 vs shuffled -6.157.


