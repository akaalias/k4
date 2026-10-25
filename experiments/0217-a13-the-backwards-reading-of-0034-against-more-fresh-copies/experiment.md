# 0217-a13-the-backwards-reading-of-0034-against-more-fresh-copies: A13.3, replication: 0034's saved readings read backwards, the one candidate 0216 left unresolved, against more fresh copies of the same search, with reversed messages planted through 0034's own climb

**Family:** 1-keyed-periodic  
**Parent:** 0216-a13-the-saved-readings-against-their-own-search-on-fresh-copies-rerun  
**Decision:** reverted  
**Run:** 2026-10-25T12:31:59+00:00, 2172.0 s, status ran  
**Time by phase:** design 234 s, implement 63 s, test 9 s, run 2172 s, record 0 s

## In plain words

An old search (0034) produced 18 readings of K4 with every known letter in place and threw them away as gibberish. One of them reads a little better backwards than any reading the same search made from scrambled copies of the carving, which could mean Sanborn wrote his message backwards before enciphering it, or could be luck. Luck is tested the only honest way: run the same search on more scrambled copies until one of them reads as well backwards. We also hide some backwards messages of our own and see whether this search and test would notice them.

## Walkthrough, by hand

1. Take 0034's reading at period 71 with all 24 known letters in place.
2. Write it backwards and score the backwards text for English: -5.458.
3. Scramble the carved letters, run 0034's search on the scramble, and do the same with each of its 18 readings; keep its best backwards score.
4. If that score reaches -5.458, K4's lead was luck: stop.
5. If not, scramble again and repeat; 2,242 scrambles in a row below K4 would be a real signal.
6. Separately, write a known message backwards, encipher it the 0034 way, run the search, and see whether the backwards score finds it.

## Worked example (generated)

```
0034's reading, period 71 : HUKSALLTHAVICEFFICESAEASTNORTHEASTNATIONANDINATESTINANDATTHERESBERLINCLOCKENSTIONESERTERETOODSLCQ
written backwards:            QCLSDOOTERETRESENOITSNEKCOLCNILREBSEREHTTADNANITSETANIDNANOITANTSAEHTRONTSAEASECIFFECIVAHTLLASKUH
English score of the backwards text: -5.458
a fresh scrambled copy through the same search counts against it when its best backwards score is at or above this
```

## Lineage

Inherits from 0216-a13-the-saved-readings-against-their-own-search-on-fresh-copies-rerun. What changed: A13.3 (Stage 2, step 3, issue #75), the replication 0216 began and its clock cut short. 0216 found K4 above every copy in 2 of 112 cells; 0034/eng_keep_nth met a fresh copy at copy 6, but 0034/eng_reverse (K4 -5.458, the best of its 18 readings read backwards, from period 71) stayed above all 8 fresh copies drawn before the clock (and all 10 of pass 1). Here the same pre-registered sequence continues: fresh copies 8 onward of seed '3113', each a plain shuffle run through 0034's frozen sweep unchanged (24 conventions, periods 27-29 and 53-95 every third, 20 restarts), eight at a time, until one copy's best backwards score is at or above K4's (not a flag), or the clock (unresolved, with its p bound). New: reversed messages planted under 0034's own method at period 71 and climbed by its own climb, to say whether this cell can see a reversal at all.

## Hypothesis (domain expert)

A13 (knowledge/12-assumptions.md), C4(a) (Scheidt 2005, 2015: 'I masked the English language'; a plaintext transform before the keyed stage), reading: the mask is a reversal of the message, the simplest move-only mask (0023 closed it exactly for short periodic keys; here the long periods 53-95 where the known letters leave 47-71 free key slots). Cipher: one periodic tableau key on the standard or KRYPTOS alphabets, 24 conventions, periods 27-29 and 53-95 every third (0034's space), free slots completed by a forward quadgram climb. Statistic: eng_reverse (tools/a13_structure.py), the quadgram score of the reading written backwards, best over a text's 18 readings. The cell was one of 112 pre-registered in reports/a13-structure-check.md (flag at p < 0.05/112, all of 2,242 fresh copies below K4). K4's two best backwards readings (periods 71 and 77, -5.458 and -5.525) both exceed every copy's best so far (-5.553), which is why it needs fresh copies, not argument. Plants measure power: a forward climb pulls the free letters toward forward English, so a reversed message may be destroyed by the very search that should reveal it.

## Prediction

A fresh copy reaches K4's backwards score within the 40 or so copies the clock allows (K4 has led 18 copies, which luck alone does about one time in 19), so the cell is not a flag and A13.3 closes with no flag. The reversed plants are found 0 or 1 times in 4: the forward climb overwrites the free letters, so the backwards test on this search has little power, and a 'nothing found' here says little about reversal. Zero candidates pass gate 4.

## Method

1. K4: 0034's 18 saved readings (24 of 24 known letters), each re-enciphered by 0034's frozen encrypt; the best backwards score.
2. Reversed plants: four messages from Carter's 1923 book, written backwards, the 24 known letters set after the reversal, enciphered under 0034's method with a random convention and a random period-71 key; each climbed by 0034's frozen sweep at period 71 only (a slice: one period of its 18, which can only lower the plant's best); found when its best backwards score is above every 0034 copy's.
3. Fresh copies 8 onward of seed '3113' (copies 0-7 were 0216's), 0034's sweep unchanged, eight at a time on eight cores, until one copy is at or above K4, or 2,242 copies all below (a flag), or the clock.
4. Verdict: caught (not a flag; A13.3 closes), or unresolved with p at most 1/(copies + 1).

## Result

Candidates returned: 3. Passed all gates: 0. Best crib hits among all candidates: 24/24
(EAST 4/4, NORTHEAST 9/9, BERLIN 6/6, CLOCK 5/5).
Best loss: 5.212467831258701 (0 is solved; 10 per missed crib letter; the harness keeps by lowest loss). Best fitness, diagnostic only: None. Champion before this run: none.

| # | gate | cribs | fitness | plaintext | key |
|---|---|---|---|---|---|
| 1 | baseline | 24/24 | -7.598 | `HUKSALLTHAVICEFFICESAEASTNORTHEASTNATIONANDINATESTINANDATTHERESBERLINCLOCKENSTIONESERTERETOODSLCQ` | 0034's saved reading, backwards score -5.458: period 71 key KSDEGWSDMKXVMAYZNVJUIQTELWEHGZUPFHUFMTEZYWBPEPUHJVTJPMDVTVBWFQUOGHTTKPB (47 free slots |
| 2 | baseline | 24/24 | -7.495 | `TOVENOTHESTHERSTTHESAEASTNORTHEASTRERESIDENTERSAREARETOTHERATERBERLINCLOCKSONOFTHISFREETERSINEEDL` | 0034's saved reading, backwards score -5.525: period 77 key HSUPMCUYLTXJVEGYTUVDPMCLWNQHMHLKFGFKQKXYGDAGNLNRQWVRTYNCMWQEKMCBYHITCDFYZDURP (53 free |
| 3 | baseline | 24/24 | -7.722 | `WAROUNTRETHEREATEDINTEASTNORTHEASTERESTOREASTEVERESANDINTHETHESBERLINCLOCKTATTHECONTHESTORATANAME` | 0034's saved reading, backwards score -5.764: period 86 key IZHXAZWDYMNTQMMIWYHMXZPBYXYCCUYQABQYIZDWIOIAPUWFVEZRDSOKLHILUZROGCQPUQMJNAXUQJIHJFLQZY |

### Bounds searched (the negative result this experiment leaves behind)

```
{
 "item": "A13.3",
 "cell": "0034/eng_reverse",
 "pre_registered": "2026-10-21, reports/a13-structure-check.md; replication rule in 0216",
 "k4_value": -5.4582804472186215,
 "k4_period": "period 71 ",
 "k4_readings": 18,
 "k4_reencrypt_ok": true,
 "k4_second": -5.524852191333664,
 "pass1_copies": 10,
 "pass1_max": -5.552742879798134,
 "fresh_in_0216": 8,
 "fresh_in_0216_max": -5.556524387129956,
 "fresh_here": 8,
 "fresh_here_first_index": 8,
 "fresh_here_max": -5.419172888933401,
 "first_copy_at_or_above": 14,
 "verdict": "not a flag",
 "p_bound_if_unresolved": null,
 "fresh_values": [
  {
   "copy": 8,
   "eng_reverse": -5.472861184804262,
   "seconds": 2099.1
  },
  {
   "copy": 9,
   "eng_reverse": -5.494417584500462,
   "seconds": 2103.8
  },
  {
   "copy": 10,
   "eng_reverse": -5.699543319851859,
   "seconds": 2093.7
  },
  {
   "copy": 11,
   "eng_reverse": -5.69373566628631,
   "seconds": 2104.7
  },
  {
   "copy": 12,
   "eng_reverse": -5.7093075085030565,
   "seconds": 2101.6
  },
  {
   "copy": 13,
   "eng_reverse": -5.586167714240313,
   "seconds": 2102.7
  },
  {
   "copy": 14,
   "eng_reverse": -5.419172888933401,
   "seconds": 2102.9
  },
  {
   "copy": 15,
   "eng_reverse": -5.4632880133178015,
   "seconds": 2103.5
  }
 ],
 "search": "0034's frozen sweep unchanged: 24 conventions, periods 27-29 and 53-95 every third, 20 restarts, forward quadgram climb of the free slots",
 "plants": [
  {
   "i": 0,
   "convention": "std/kry/kry/vig",
   "reading_value": -5.733801672211868,
   "plaintext_value": -4.7109401666600945,
   "letters_right": 35,
   "found": false,
   "reading": "AERENTORARECOULDIENTSEASTNORTHEASTINTHEREINTHESTERSTORINGINGINABERLINCLOCKTETESTEMPLEOFTEALLTAPEH"
  },
  {
   "i": 1,
   "convention": "std/std/kry/varbeau",
   "reading_value": -6.034008897625186,
   "plaintext_value": -4.744449294602478,
   "letters_right": 42,
   "found": false,
   "reading": "EVENGTHEALINTHEECASHEEASTNORTHEASTREDINGTHERESTANDREATEDINTHEINBERLINCLOCKTERSPEANETECHISTILEHTHT"
  },
  {
   "i": 2,
   "convention": "kry/kry/std/vig",
   "reading_value": -5.961819047930231,
   "plaintext_value": -4.994601733560607,
   "letters_right": 40,
   "found": false,
   "reading": "ETOGETHEALSEROOMSBEFIEASTNORTHEASTNTHERENTHESANDSOMETERANDINTHEBERLINCLOCKISHINTHERTHECOATTELATON"
  },
  {
   "i": 3,
   "convention": "kry/std/std/varbeau",
   "reading_value": -5.8902599359223045,
   "plaintext_value": -4.805241162387648,
   "letters_right": 29,
   "found": false,
   "reading": "ACLOSERSABOUTSONOUSEOEASTNORTHEASTFTHERETHETHESERINTHESTHATIONOBERLINCLOCKMOREMENBURESTERIANEUVIT"
  }
 ],
 "plants_found": "0 of 4",
 "plant_design": "Carter 1923 written backwards, 24 known letters set after the reversal, random convention, random period-71 key; climbed by 0034's sweep at period 71 only (sliced); found = best backwards score above every pass-1 copy's (-5.553)",
 "plant_seconds": 67.1,
 "seconds": 2171.9
}
```

Notes: 0034/eng_reverse: K4 -5.458; 8 more fresh copies (max -5.419); first at or above: 14; verdict not a flag. Reversed plants found 0 of 4.


