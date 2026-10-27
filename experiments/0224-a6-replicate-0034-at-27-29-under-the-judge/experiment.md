# 0224-a6-replicate-0034-at-27-29-under-the-judge: A6.1, replication: 0034's completed periodic keys at lengths 27-29, where K4's best judged reading (8) led all 10 copies (best 7), against fresh copies of the same frozen search until one reaches 8 or 80 stay below

**Family:** 1-keyed-periodic  
**Parent:** 0222-rejudge-the-sampled-verdicts-completed-periodic-keys  
**Decision:** kept  
**Run:** 2026-10-27T10:23:51+00:00, 32.3 s, status ran  
**Time by phase:** unattributed 62 s, run 32 s, record 0 s

## In plain words

One old search, rerun on scrambled copies of the carving, gave readings the judge scored a little below the carving's reading (7 against 8 out of 100, both near the bottom of the scale). That is probably luck. The honest check is to scramble again and again, run the same search, and see how soon a scrambled copy does as well.

## Walkthrough, by hand

1. Scramble the 97 carved letters.
2. For key lengths 27, 28 and 29, fix the key letters the known words force, and choose the 3-5 free ones so the rest reads as much like English as possible.
3. Hide the known words and give the three readings to the judge.
4. If the best scores 8 or more, the carving's lead was luck: stop.
5. Otherwise scramble again; 80 scrambles in a row below 8 would be a signal.

## Worked example (generated)

```
0034's reading of K4 at key length 27 (3 free key slots climbed):
  reading      ZWAWFAFIWGMGOGMDROTMAEASTNORTHEASTISTCDAPPUDSFROKLPDGBCUMLDWLBYBERLINCLOCKADHARIUHVWCQFISIQMNGDJK
  judge sees   ZWAWFAFIWGMGOGMDROTMA#############ISTCDAPPUDSFROKLPDGBCUMLDWLBY###########ADHARIUHVWCQFISIQMNGDJK

K4's best of its three readings (27, 28, 29) scored 8; a fresh copy's three readings by the same search must reach 8.
```

## Lineage

Inherits from 0222-rejudge-the-sampled-verdicts-completed-periodic-keys. What changed: A6.1 (Stage 2, step 4, issue #84), the candidate 0222 left (0223 is a mistaken duplicate of 0222: the new code was not written before the run). 0222 judged K4's saved readings of 0034, 0035 and 0048 against 0216's regenerated copies: in the cell 0034 at 27-29 K4's best (8 of 100) was above every one of 10 copies (4-7), the only one of 4 cells where it led (chance 0.36). Pre-registered rule (program.md): a candidate is replicated on that cell alone against fresh copies, enough for the corrected p (0.05 / 4: 80 copies all below K4), before anything else. Fresh plain shuffles (seed 4222), 0034's frozen sweep unchanged at periods 27, 28, 29 (the cell's three readings per text: 24 conventions, 20 restarts each), eight at a time, judged after each batch.

## Hypothesis (domain expert)

A6 (knowledge/12-assumptions.md). Cipher: one periodic key on the standard or KRYPTOS tables, 24 conventions, key lengths 27-29 (C1(c), C27(c): the K1/K2 tableau system at the only lengths 1-52 the known letters leave alive for it; 0005), the 3-5 free key slots completed by a quadgram climb (0034). Statistic: the judge's best score (j3, Sonnet 5.5) over a text's three readings. K4: 8 ('? LEVES SIT MILAN BAC ? AT ? OF ?'). With 3-5 free slots each reading is fixed but for 9-15 letters, so a score of 8 means a few short words, inside what the bench calls chance (20 = a few short words). Sequential: a fresh copy at or above 8 ends it (not a flag); 80 copies all below K4 is a flag (p < 0.0125 corrected for the 4 cells of 0222).

## Prediction

A fresh copy scores 8 or more within the first two batches (16 copies): the 10 copies of 0222 already reached 7 twice, and the judge's scores at this end of the scale move in steps of 2-4. Not a flag. Zero candidates pass gate 4.

## Method

1. Fresh copies: plain shuffles of K4 from random.Random(4222), a search seed each, as tools/a13_check.py's pass 1 drew them.
2. Each through 0034's frozen sweep at periods 27, 28, 29 (24 conventions, 20 restarts), best reading per period.
3. Eight copies at a time on eight cores; the batch's 24 readings judged in one call; each copy's best.
4. Stop at the first copy at or above 8 (not a flag), at 80 copies all below (a flag), or at the clock (unresolved, with p at most 1/(copies + 11)).

## Result

Candidates returned: 3. Passed all gates: 1. Best crib hits among all candidates: 24/24
(EAST 4/4, NORTHEAST 9/9, BERLIN 6/6, CLOCK 5/5).
Best loss: 4.623134929906328 (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: -8.264096778936356. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | pass | 24/24 | -8.264 | `YJAEIVIZKOYDBEACIOSSLEASTNORTHEASTVCACZLEVESITMILANBACMIIXDCHKYBERLINCLOCKATTHIZQLLPDLOFDFOIJGUSM` | saved reading of 0034: period 29 key HYHMKBNENTXBQRMAEROOOXYHANZEF (5 free slots climbed); kry/kry/std/beau |
| 2 | baseline | 24/24 | -8.315 | `RYIHBKSCNNJARISEYUCCTEASTNORTHEASTWHCOFHCGDMXKAATSIXNHCIURRORLDBERLINCLOCKTHEJUFYFLIUAILUSCILVXVL` | saved reading of 0034: period 28 key NZVDMORFNOEEADIAGKSSSUELRXLO (4 free slots climbed); kry/std/std/vig |
| 3 | baseline | 24/24 | -8.715 | `ZWAWFAFIWGMGOGMDROTMAEASTNORTHEASTISTCDAPPUDSFROKLPDGBCUMLDWLBYBERLINCLOCKADHARIUHVWCQFISIQMNGDJK` | saved reading of 0034: period 27 key EFHYHMKUKBNENTXBQRMAEXYHANZ (3 free slots climbed); kry/kry/std/beau |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "item": "A6.1 (replication of 0222's cell 0034 P27-29)",
 "k4_value": 8,
 "copies_in_0222": "10, best 4-7 (0216's regeneration)",
 "fresh_seed": 4222,
 "search": "0034's frozen sweep at periods 27, 28, 29: 24 conventions, 20 restarts, quadgram climb of the 3-5 free slots",
 "fresh_copies": 8,
 "first_copy_at_or_above": 6,
 "verdict": "not a flag",
 "p_bound_if_unresolved": null,
 "flag_rule": "80 fresh copies all below K4 (p < 0.05/4)",
 "copies": [
  {
   "copy": 0,
   "best": 3,
   "by_period": {
    "27": 3,
    "28": 3,
    "29": 3
   },
   "none": 0,
   "best_reading": "OGNJPNCPUSGEDHWJPKFBIEASTNORTHEASTCERSUCWUNHETISNORELPFKEORDSFIBERLINCLOCKERMEGTDGCEFQVYONCLTKOWI"
  },
  {
   "copy": 1,
   "best": 4,
   "by_period": {
    "27": 4,
    "28": 3,
    "29": 3
   },
   "none": 0,
   "best_reading": "XMLSSEWRYAUAISHQZGRXEEASTNORTHEASTONCYCOYESDLWNEKJHOITMVCRHYYERBERLINCLOCKOFYSHUDOLLHRWGOPJFOGRIB"
  },
  {
   "copy": 2,
   "best": 4,
   "by_period": {
    "27": 3,
    "28": 3,
    "29": 4
   },
   "none": 0,
   "best_reading": "TBYFBDVYMDXYPPCVEIOBOEASTNORTHEASTTGUDEIXCYKWKINGHEITYRCABNUXBNBERLINCLOCKETEDELYGXTKPGBIGOVVAZZH"
  },
  {
   "copy": 3,
   "best": 4,
   "by_period": {
    "27": 2,
    "28": 3,
    "29": 4
   },
   "none": 0,
   "best_reading": "MHFIKPXKAWGLTOMVEAHAVEASTNORTHEASTEEYAPENMBUYHAGECUPQCHHHKRASGMBERLINCLOCKFORDTELVXTCOMVQBFOEYEXZ"
  },
  {
   "copy": 4,
   "best": 4,
   "by_period": {
    "27": 4,
    "28": 3,
    "29": 4
   },
   "none": 0,
   "best_reading": "ISYLCZGCRVSUSOJNBRNGOEASTNORTHEASTMIXADXRSHZSTBLAGLAGHEGGGGJRAPBERLINCLOCKEEUUMKPBVQFXRQALLHIMQLX"
  },
  {
   "copy": 5,
   "best": 4,
   "by_period": {
    "27": 4,
    "28": 2,
    "29": 3
   },
   "none": 0,
   "best_reading": "TLSJNAILLWEZELMAENXWREASTNORTHEASTITIIOIHLXJXRHEJBYPLAYIHIFUZAIBERLINCLOCKSVRMARZKTENLEFUMBOPEMYX"
  },
  {
   "copy": 6,
   "best": 8,
   "by_period": {
    "27": 8,
    "28": 3,
    "29": 4
   },
   "none": 0,
   "best_reading": "BMHIHAVEBELDPUSBMPCJLEASTNORTHEASTAKIKNSEVNUPJBTVKIMIWJEEIQFENFBERLINCLOCKREFOKYMZFKNRDHNTYPEISWX"
  },
  {
   "copy": 7,
   "best": 4,
   "by_period": {
    "27": 2,
    "28": 4,
    "29": 3
   },
   "none": 0,
   "best_reading": "TYCZIQUASAGFGXHOXZYSTEASTNORTHEASTRONOMYABAEFJEAHUAIIPUETCIPLDWBERLINCLOCKHOFMWJUKTNKAKPRVOAYYZJM"
  }
 ],
 "judge_texts_sent": 24,
 "judge_calls_estimated": "24 per batch, at most 240",
 "judge_none": 0,
 "seconds": 32,
 "controls": "quadgram scores of the fresh copies' readings by the same search",
 "exhaustive": false
}
```

Notes: not a flag: 8 fresh copies, first at or above K4's 8: copy 6; copies' best scores [3, 4, 4, 4, 4, 4, 8, 4]


