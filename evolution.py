"""The research-evolution figure (issue #130): what happened to the research itself.

Ported from Ballpark's autoresearch/evofig.py. The marks are data; this module lays them out.
Time runs left to right on an activity-weighted axis: a busy day is wide, a quiet one narrow.

Five kinds of mark, as on Ballpark's page:
  TRUNK   what the project still does today
  DEAD    tried, then abandoned (above the trunk, grey, ends in a cross)
  SUPER   ran as the mainline, then replaced (below the trunk, accent, ends in a ring)
  MERGES  an insight that changed the project (above, arrow into the trunk)
  INCIDENTS  something broke (pins along the bottom)

Times are local (Berlin), written "MM-DD HH:MM". Lanes are assigned by first fit, so adding a
mark is appending a tuple. Compiled from the chat transcripts, the tickets, the pivots and the
notebook; the loop does not edit this file.
"""
import glob
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).parent

# --- the time axis ---------------------------------------------------------------------------
# Day numbers count from 1 October 2026: 14 = 14 Oct, 32 = 1 Nov, 50 = 19 Nov.
from datetime import date as _date

DAY0 = _date(2026, 9, 30)               # day numbers count from here: 14 = 14 October 2026
FIRST_DAY = 14
LAST_DAY = max(50, (_date.today() - DAY0).days)       # the axis runs to today
GRID_MIN_W = 60
# The axis is weighted by activity, in ten-minute steps: a step is BASE wide, plus PER_MARK for
# every mark that starts or ends in it, plus PER_EXP for every experiment started in it. Busy
# hours spread out, quiet days shrink to a sliver, and nothing is placed by hand.
BASE, PER_MARK, PER_EXP = 0.35, 88.0, 6.0
STEPS = (LAST_DAY + 1 - FIRST_DAY) * 144
CUM = [40.0] * (STEPS + 1)            # filled by _scale()


def T(s):
    """'10-27 11:56' -> fractional day number."""
    mo, d, h, mi = map(int, re.match(r"(\d+)-(\d+) (\d+):(\d+)", s).groups())
    return (_date(2026, mo, d) - DAY0).days + (h * 60 + mi) / 1440.0


def x(day):
    f = max(0.0, min(STEPS - 1e-6, (day - FIRST_DAY) * 144))
    i = int(f)
    return CUM[i] + (f - i) * (CUM[i + 1] - CUM[i])


def _scale(exps):
    w = [BASE] * STEPS
    times = ([T(m[0]) for m in TRUNK + INCIDENTS] + [T(t) for m in DEAD + SUPER + MERGES for t in m[:2]])
    for t, k in [(t, PER_MARK) for t in times] + [(e[0], PER_EXP) for e in exps.values()]:
        i = int((t - FIRST_DAY) * 144)
        if 0 <= i < STEPS:
            w[i] += k
    for i in range(STEPS):
        CUM[i + 1] = CUM[i] + w[i]


def day_label(d):
    t = DAY0 + timedelta(days=d)
    return f"{t.day} {t.strftime('%b')}"


def span_label():
    a, b = DAY0 + timedelta(days=FIRST_DAY), DAY0 + timedelta(days=LAST_DAY)
    return f"{a.day} {a.strftime('%B')} to {b.day} {b.strftime('%B %Y')}"


GAPS = [
    ("10-22 00:00", "10-24 00:00", "two quiet days", "No sessions and no runs on 22 and 23 October."),
    ("11-01 00:00", "11-04 00:00", "three quiet days",
     "The loop had been stopped on 31 October with experiment 267 part-way through on the laptop. Nothing ran until 4 November."),
    ("11-06 00:00", "11-17 00:00", "eleven days away",
     "The loop was stopped on the evening of 5 November. Work resumed on 17 November with a check that the keys and the AWS account still worked."),
]

# (start, name) -- an era runs until the next one starts
ERAS = [
    ("10-14 16:40", "the sweep"),
    ("10-16 08:19", "a ranked order of work"),
    ("10-18 15:35", "checking ourselves"),
    ("10-27 10:00", "deciders and new angles"),
    ("11-17 14:30", "stepping back"),
]

# --- the marks ------------------------------------------------------------------------------
# (when, label, hover text, link or "")
TRUNK = [
    ("10-14 16:40", "The project starts",
     "The brief: apply an autoresearch loop to Kryptos K4. Discuss the harness first, then what solved means, then the inputs.", ""),
    ("10-14 17:16", "Success: the method, no oracle",
     "A reading counts only with the procedure that produces it: the known words in place, English, the carved text back when run forward, a hand method of 1990. No outside checker is used.", ""),
    ("10-14 17:26", "Harness and crib gate",
     "The smallest harness that can run a loop. Every experiment is a structured hypothesis with a plain-words version, and a reading that misses the known letters fails before any English score is computed.", "exp:1"),
    ("10-14 18:40", "Every source read in full",
     "A study pass over Wikipedia's footnotes, the CIA's page, Sanborn's and Scheidt's interviews and the books, written up as a knowledge base the loop's agent reads before it designs anything.", ""),
    ("10-15 16:41", "Beat ten scrambled coppers",
     "Scoring settled on 15 October: a reading is kept only if it beats the same method run on at least ten shuffled copies of the carved text, and the key is charged by the length of its description.", ""),
    ("10-15 17:20", "Prior-attempts database",
     "A deep-research pass over everything tried and published on K4, so each direction is checked against what others have already closed.", ""),
    ("10-16 08:19", "A ranked order of work",
     "One table of open items per family, the families ranked by clue support and cost, each result graded exact, sampled or weak. The loop follows it top down from here.", "/pivot/P4"),
    ("10-16 11:48", "The loop in its own shell",
     "tools/run_loop.sh runs the loop unattended outside the chat, so the site and the harness can be worked on while it runs.", ""),
    ("10-16 19:52", "Assumptions register",
     "Thirteen assumptions the project takes for granted, each with its source, how firm it is and the cheapest check. A16 was added two days later.", "/assumptions"),
    ("10-18 15:12", "Goes public",
     "A public copy of the repository and the site at alexisrondeau.me/k4, regenerated after every experiment. The working repository stays private.", ""),
    ("10-18 15:40", "A control for every closed item",
     "For each of the 82 closed items a message was planted with the item's own method and the item's own search had to find it. 62 passed; 3 failed for lack of power and their items were blocked.", "/controls"),
    ("10-20 13:20", "Slips allowed, a blind judge",
     "The strongest families were rerun allowing one or two of the 24 known letters to miss. A language model judges the readings blind against those of the scrambled copies.", "exp:207"),
    ("10-27 10:15", "Run until solved",
     "The loop works whatever is open, including items added later, and stops only for a reading that passes every gate or an empty backlog.", ""),
    ("10-27 11:40", "Champions held back",
     "The public site announces a kept result only after it has been confirmed by hand. A reading also counts only in the search that found it.", ""),
    ("10-27 11:56", "No time limit",
     "An experiment takes as long as it needs. The harness no longer stops a run at its budget.", ""),
    ("10-29 11:50", "Checkpoints",
     "Each finished unit of a run is saved as it lands, and a rerun resumes from it. A stop or a dropped connection no longer throws the work away.", ""),
    ("11-04 09:50", "AWS spot, 32 cores",
     "Long runs go to a throwaway 32-core spot machine at about $0.60 an hour and fall back to the laptop if the cloud cannot run them.", ""),
    ("11-17 14:47", "Criteria revised",
     "A reviewer with no access to the project checked the success criteria against the official sources. Exact re-encryption and the short-key rule were our own additions and were loosened; EAST weighs less than the other three words.", ""),
    ("11-17 15:30", "Simple hand methods first",
     "Family 16: methods a teacher could show on paper, queued ahead of the large runs, with a preference for no mathematics.", "/pivot/P24"),
]

# (start, end, label, end label, hover text, fixed lane or None)
DEAD = [
    ("10-14 17:11", "10-14 17:14", "Paradigm's checker as the oracle", "dropped",
     "A paid checker confirms a K4 plaintext without asking for a method. Dropped within minutes so the project runs independently. Whether a candidate is ever sent to it was reopened on 17 November and is undecided.", None),
    ("10-15 10:00", "10-15 16:41", "Experiment 34 as champion", "no champion after re-scoring",
     "The first reading with English-looking stretches around the known words. Its key was 383 bits of arbitrary letters. Re-scored under the settled rules, no reading was kept.", None),
    ("10-15 16:30", "10-15 16:41", "100-bit key gate", "dropped the same afternoon",
     "A hard limit on key size, taken from K1-K3's short key words. Its basis did not support a size limit, so the key is charged in the score instead.", None),
    ("10-15 14:16", "10-17 01:00", "The sevens of experiment 56", "within chance (168)",
     "Doubled letters lining up in columns of seven and a repeat at width 21 looked like a fingerprint. The directions gave it a few runs; experiment 168 found the statistic within chance.", None),
    ("10-15 16:57", "10-15 17:15", "Experiment 48 as a solved first layer", "set aside",
     "A reading with all 24 known letters and noise elsewhere: could it be one layer solved, with a second ciphertext left? Set aside the same hour.", None),
    ("10-15 17:30", "11-04 13:42", "A published text holding both known phrases", "none in any archive",
     "K3 paraphrases Howard Carter, so K4 might quote a source too. Two searches, across the Internet Archive, Gutenberg, HathiTrust and Google Books, found no text that pairs EAST NORTHEAST with BERLIN CLOCK.", 5),
    ("10-18 16:20", "10-31 14:09", "Sharp photographs of K4's plate", "none found",
     "K4 is the one section partly hidden behind the stone. Photographs sharp enough to check the plate near the rocks were never found.", 4),
    ("10-27 22:23", "10-30 08:41", "The table-then-move excess", "not a message (260)",
     "Experiments 237 to 239 put K4 above its shuffles under one cipher, and it replicated against 1,000 shuffles. Planted messages keep the excess when the text is rotated; K4's does not.", None),
    ("11-04 13:59", "11-04 20:45", "Drafts in Sanborn's voice as known text", "bar not met (268)",
     "Family 15: read K1-K3 as a guide to K4's content and use 97-letter drafts as extra known plaintext. The drafts found fewer planted messages than English alone, so the family stopped.", None),
    ("11-18 10:53", "11-18 11:20", "Clumps in the blurred picture", "an edge, not a finding",
     "Blurred and grey, K4's letters seemed to clump where K2 and K3 look even. Measured against 20,000 shuffles it was an edge, not a finding.", None),
    ("11-18 11:04", "11-18 11:35", "ALEXANDERPLATZ after the clock", "expected by luck",
     "The world clock stands at Alexanderplatz, so the word was tried as known text after BERLIN CLOCK. Its best match was the size expected by luck from about 16,000 settings.", None),
]

# (start, end, label, end label, hover text)
SUPER = [
    ("10-14 17:16", "11-17 14:47", "The criteria as first written", "→ checked against the official record",
     "For five weeks a reading had to re-encrypt exactly and carry a short key. Both were our own additions. About eleven verdicts that closed a space only because the forced key was not a word are open again."),
    ("10-14 17:24", "10-27 11:56", "Thirty minutes an experiment", "→ as long as it needs",
     "Set on the first day to fail fast. It shaped which tests were designed at all, and experiment 200 ran past its budget and left no record."),
    ("10-14 17:30", "10-16 08:19", "Pivot after five reverts", "→ ranked order of work",
     "Five reverted experiments in a row forced a change of family. It moved the work three times in 118 experiments and cut threads off before they were finished."),
    ("10-14 17:36", "10-27 16:04", "The laptop, 8 cores", "→ Modal",
     "Every search pinned all eight cores of the M1 for two weeks."),
    ("10-14 18:00", "10-16 11:48", "The loop inside the chat", "→ run_loop.sh",
     "The first 118 experiments ran inside chat sessions, which blocked all other work while they ran."),
    ("10-14 18:10", "10-18 15:40", "Closed without a planted answer", "→ a control for every item",
     "Closed meant our code searched and found nothing. No search had been checked against a planted message, so a bug that drops the true key looked like a clean negative."),
    ("10-14 18:20", "10-20 13:20", "Exact letters, strict English", "→ slips allowed, a blind judge",
     "Every exact result assumed Sanborn made no slip, although K1 to K3 carry misspellings and K2 a lost letter."),
    ("10-15 16:56", "10-16 08:19", "Eight directions, swept in order", "→ ranked order of work",
     "Eight types of solution drawn from the differences between K1, K2 and K3. Thirty-nine experiments swept them in one night without building on the ones that had some letters right."),
    ("10-16 11:48", "10-27 10:15", "Stop-after milestones", "→ run until solved",
     "Each loop run was told which family to stop after. More than once it stopped with nothing to do while new items were waiting."),
    ("10-16 18:27", "11-17 15:30", "Large libraries and statistical deciders", "→ simple hand methods first",
     "From experiment 136 the work moved to very large route libraries judged against a handful of shuffles, and to deciders for cells that could not be decided. A teacher's review found this complexity mostly our own doing."),
    ("10-18 15:12", "10-27 11:40", "Kept results published at once", "→ held until confirmed",
     "The public site rebuilt itself after every experiment, whatever the harness had kept."),
    ("10-27 16:04", "10-30 12:36", "Modal, 32 cores", "credit out",
     "Thirty-two rented cores so the laptop stops overheating. The free credit lasted three days."),
    ("10-30 12:50", "11-04 09:50", "The laptop again", "→ AWS spot",
     "Experiment 267 ran about 80 settings an hour on the laptop, with 5,930 to do."),
]

# (when, label, hover text)
INCIDENTS = [
    ("10-14 17:42", "sources not read", "The agent had not taken in Wikipedia's footnotes or the CIA's page, and had missed the hint to try K1 to K3. Work stopped for a full study pass."),
    ("10-15 20:30", "columns in the wrong order", "Ten keyed-columnar records had read their columns in the inverse order. The rerun, experiment 85, was at chance."),
    ("10-16 11:50", "runner drops the controls", "The runner never saved the scrambled-copper controls, so no reading could pass the gate that needs them. Found before the first unattended run."),
    ("10-20 09:55", "200 leaves no record", "Experiment 200 ran past its 60-minute budget and left no record. It was rerun with a faster search as 201."),
    ("10-25 14:56", "a false champion, published", "Experiment 219 was kept by mistake: readings padded with the letter A beat the wrong controls. The public homepage announced a champion."),
    ("10-27 11:30", "a second false champion", "Experiment 224 re-submitted an old reading and beat a smaller set of controls than its own search had. The second mistaken champion in twenty experiments."),
    ("10-27 11:47", "stopped at a time limit", "A run was stopped at its limit and others had their budgets squeezed under the two-hour limit on background commands."),
    ("10-28 09:46", "loop stops, files uncommitted", "The loop stopped and left its attack file, the judge's cache and old drafts uncommitted."),
    ("10-29 11:39", "workers left running", "A killed experiment left its four workers running for 35 minutes, and Modal kept the next run going after the local process had died."),
    ("10-30 12:30", "Modal credit used up", "The month's Modal credit ran out and the long run in hand went back to the laptop."),
    ("10-30 19:15", "the laptop on battery", "On battery experiment 267 fell from about 80 settings an hour to about 10."),
    ("11-04 22:30", "clock skew ends an AWS run", "After a sleep the laptop's clock was briefly off, S3 refused a request, and the run was handed to the laptop after 65 minutes on AWS."),
    ("11-05 13:06", "a finished run cut off", "The laptop slept while AWS finished all 697 units of experiment 271. On waking it saw no heartbeat, ended the machine and started again locally."),
    ("11-17 14:55", "API credit used up", "The judge's API credit had been spent by other projects."),
]

# (raised, landed, label, hover text)
MERGES = [
    ("10-14 16:46", "10-14 17:16", "the method is part of the answer",
     "Is plaintext alone success? Sanborn calls words without a method not solved, so every experiment must record how it got there."),
    ("10-15 16:12", "10-15 16:24", "would it do as well on a scrambled copper?",
     "A search with a free key can fit the known letters to anything. The test is whether it does better on K4 than on shuffled copies of K4."),
    ("10-16 08:15", "10-16 08:19", "eight had letters right: why not build on those?",
     "The lineage looked chaotic: families switched and sixty experiments were thrown at the wall. The answer was a systematic order."),
    ("10-16 11:30", "10-16 11:42", "the value is in what does not work",
     "Before the first share: what the experiments produce is a map of ways that fail. The Learnings page and the site's headline count come from this."),
    ("10-16 19:20", "10-16 19:52", "this is water",
     "What do we believe so deeply that we no longer see it? Among the answers was A13: the true reading may already be among our candidates, masked."),
    ("10-16 19:29", "10-16 19:40", "existed by 1990, to whom?",
     "The families held methods public by 1990. The makers were not the public. Families 10 and 11 added self-changing alphabets and agency hand systems."),
    ("10-16 20:38", "10-16 20:52", "imagine you are David Stein",
     "Stein solved K1 to K3 by hand in 1998. Family 12 works his way: look, quantify, then crib."),
    ("10-16 21:12", "10-16 21:22", "pick up what the pivots cut off",
     "The old pivot rule had forced the search out of threads. They went back on the queue."),
    ("10-18 15:32", "10-18 15:40", "can each search find a planted answer?",
     "Before building on 198 results, find out which of them can be trusted."),
    ("10-18 15:43", "10-18 16:05", "an expert taught it to an amateur",
     "How complex can a method be that Scheidt taught a sculptor to do by hand? It became assumption A16 and a study of hand ciphers agents memorised."),
    ("10-19 16:26", "10-19 16:32", "rather redo it than miss a lead",
     "The controls turned up results that had to be run again. They were."),
    ("10-20 11:06", "10-20 13:20", "why only one slip?",
     "If one wrong letter is allowed, why not two or five?"),
    ("10-24 17:44", "10-24 17:52", "the known words confirm, they need not solve",
     "Most experiments leaned on the known words. Family 13 works from the ciphertext alone and keeps the words sealed until the end."),
    ("10-27 10:29", "10-27 11:02", "Scheidt's own hints deserve attacks",
     "Scheidt spoke of masking and of more than one layer. Family 14 is his mask, keyed by words."),
    ("10-28 13:24", "10-28 13:32", "more experiments, not fewer",
     "Weak tests are run at their stated power and edge results chased. Only money waits for a decision."),
    ("11-04 10:58", "11-04 13:59", "K1 to K3 as a guide to content",
     "Has anyone used what K1 to K3 say to guess what K4 says?"),
    ("11-17 14:35", "11-17 14:47", "did we add requirements of our own?",
     "A fresh pair of eyes on the four criteria, with web sources only."),
    ("11-17 14:32", "11-17 15:30", "too complicated to teach",
     "Many experiments would be hard to do on paper or to teach to a non-cryptographer. A teacher looked at the experiment log alone: what simple, memorable methods were never tried?"),
]

# --- layout ---------------------------------------------------------------------------------
TOP = 78                      # the highest lane above the trunk sits here
LANE_UP, LANE_DOWN = 34, 30
TRUNK_X0 = 52.0
CH, CH_END, CH_UP = 6.5, 5.9, 7.0     # generous letter widths: labels, end labels, small capitals


def _f(v):
    return f"{v + 0.0:.1f}"


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace("'", "&#39;")


def _fit(rows, a, b):
    """First row whose taken spans leave [a, b] free; a new row if none does."""
    for i, row in enumerate(rows):
        if all(b < s or a > e for s, e in row):
            row.append((a, b))
            return i
    rows.append([(a, b)])
    return len(rows) - 1


def _branch_geom(x0, x1):
    s = min(1.0, (x1 - x0) / 45.0)
    return x0 + 15.0 * s, x0 + 24.0 * s


def _span_branch(x0, x1, lab, end):
    _, ex = _branch_geom(x0, x1)
    return x0 - 8, max(ex + 8 + len(lab) * CH, x1 + 11 + len(end) * CH_END) + 14


def _branch(kind, key, x0, y0, x1, lane, lab, endlab, end_mark, labx=None):
    c1, ex = _branch_geom(x0, x1)
    labx = ex + 8 if labx is None else labx
    out = [f"<path class='evo-{kind}' data-k='{key}' d='M{_f(x0)},{y0} C{_f(c1)},{y0} {_f(x0)},{lane} {_f(ex)},{lane} L{_f(x1)},{lane}'/>"]
    if end_mark == "x":
        out.append(f"<g class='evo-end' data-k='{key}'><line x1='{_f(x1 - 4.5)}' y1='{lane - 4.5}' x2='{_f(x1 + 4.5)}' y2='{lane + 4.5}'/>"
                   f"<line x1='{_f(x1 - 4.5)}' y1='{lane + 4.5}' x2='{_f(x1 + 4.5)}' y2='{lane - 4.5}'/></g>")
    else:
        out.append(f"<circle class='evo-endr' data-k='{key}' cx='{_f(x1)}' cy='{lane}' r='5'/>")
    cls = "d" if kind == "dead" else "s"
    out.append(f"<text class='evo-lab {cls}' data-k='{key}' x='{_f(labx)}' y='{lane - 10}'>{_esc(lab)}</text>")
    out.append(f"<text class='evo-endlab {cls}' data-k='{key}' x='{_f(x1 + 11)}' y='{lane + 4}'>{_esc(endlab)}</text>")
    return "".join(out)


def experiment_times():
    """Experiment number -> fractional local day it started, from each record's result.json."""
    out = {}
    for f in glob.glob(str(ROOT / "experiments" / "*" / "result.json")):
        try:
            d = json.loads(Path(f).read_text())
            t = datetime.fromisoformat(d["started"]).astimezone(timezone.utc)
        except Exception:
            continue
        t += timedelta(hours=2 if t < datetime(2026, 10, 25, 1, tzinfo=timezone.utc) else 1)
        day = (t.date() - DAY0).days + (t.hour * 60 + t.minute) / 1440.0
        if FIRST_DAY <= day < LAST_DAY + 1:
            out[int(d["id"])] = (day, d.get("tag", ""), d.get("decision", ""))
    return out


def build():
    """-> (svg, tips, latest_x). tips: key -> {t, d, k, h}."""
    tips = {}
    exps = experiment_times()
    _scale(exps)
    view_w = int(CUM[-1] + 60)
    trunk_x1 = max(x(max([e[0] for e in exps.values()] + [T(TRUNK[-1][0])])) + 60, x(LAST_DAY + 0.5))

    # ---- lanes above the trunk: abandoned branches and insights share them. A mark may not sit
    # where its riser would cross another mark's flat run or label; long branches go on top.
    marks = []
    for i, (a, b, lab, end, tip, top) in enumerate(DEAD):
        x0, x1 = x(T(a)), x(T(b))
        lo, hi = _span_branch(x0, x1, lab, end)
        marks.append(dict(kind="d", i=i, lo=lo, hi=hi, rx=x0 + 6, top=bool(top)))
        tips[f"d{i}"] = {"t": lab, "d": tip, "k": "abandoned"}
    for i, (a, b, lab, tip) in enumerate(MERGES):
        x1 = x(T(b))
        x0 = min(x(T(a)), x1 - 60)
        lo = min(x0, x1 - 26 - len(lab) * CH) - 12
        marks.append(dict(kind="m", i=i, lo=lo, hi=x1 + 12, rx=x1, top=False))
        tips[f"m{i}"] = {"t": lab, "d": tip, "k": "insight"}
    def assign(order):
        lanes, risers, lane_of, forced = [], [], {}, 0

        def ok(li, m, strict=True):
            row = lanes[li] if li < len(lanes) else []
            if any(not (m["hi"] < s or m["lo"] > e) for s, e in row):
                return False
            if any(m["lo"] <= r <= m["hi"] and rl > li for r, rl in risers):
                return False
            return not strict or not any(s - 6 <= m["rx"] <= e + 6 for lj in range(min(li, len(lanes))) for s, e in lanes[lj])

        def put(li, m):
            while len(lanes) <= li:
                lanes.append([])
            lanes[li].append((m["lo"], m["hi"]))
            risers.append((m["rx"], li))
            lane_of[(m["kind"], m["i"])] = li

        for m in order(m for m in marks if not m["top"]):
            li = next((l for l in range(len(lanes) + 1) if ok(l, m)), None)
            if li is None:
                forced += 1
                li = next(l for l in range(len(lanes) + 1) if ok(l, m, strict=False))
            put(li, m)
        base = len(lanes)
        for m in order(m for m in marks if m["top"]):
            put(next(l for l in range(base, len(lanes) + 2) if ok(l, m, strict=False)), m)
        return forced, len(lanes), lanes, lane_of

    # a merge's label lies left of its riser and a branch's lies right, so no single order suits
    # both: try a few and keep the one with the fewest forced crossings, then the fewest lanes
    by = lambda key, rev=False: (lambda ms: sorted(ms, key=key, reverse=rev))
    orders = [by(lambda m: m["rx"]), by(lambda m: m["rx"], True),
              by(lambda m: (m["kind"] == "m", -m["rx"] if m["kind"] == "d" else m["rx"])),
              by(lambda m: (m["kind"] == "d", -m["rx"] if m["kind"] == "d" else m["rx"])),
              by(lambda m: m["hi"] - m["lo"], True), by(lambda m: m["hi"] - m["lo"])]
    forced, _, lanes, lane_of = min((assign(o) for o in orders), key=lambda r: r[:2])

    n_up = len(lanes)
    trunk_y = TOP + LANE_UP * (n_up - 1) + 46
    up = lambda li: trunk_y - 46 - LANE_UP * li

    # ---- lanes below: the replaced rules, first fit; a label slides along its own line to stay
    # clear of the risers of deeper lanes.
    below, sup = [], []
    for i, (a, b, lab, end, tip) in sorted(enumerate(SUPER), key=lambda t: T(t[1][0])):
        x0, x1 = x(T(a)), x(T(b))
        sup.append(dict(i=i, x0=x0, x1=x1, lab=lab, end=end, li=_fit(below, *_span_branch(x0, x1, lab, end))))
        tips[f"s{i}"] = {"t": lab, "d": tip, "k": "superseded"}
    for m in sup:
        lx = _branch_geom(m["x0"], m["x1"])[1] + 8
        w = len(m["lab"]) * CH
        for _ in range(12):
            hit = [o["x0"] for o in sup if o["li"] > m["li"] and lx - 6 <= o["x0"] + 12 <= lx + w + 6]
            if not hit or max(hit) + 34 + w > m["x1"] - 12:
                break
            lx = max(hit) + 34
        m["labx"] = lx
    n_down = len(below)
    down = lambda li: trunk_y + 92 + LANE_DOWN * li
    pin_y = down(n_down - 1) + 44
    pinrow_y = lambda r: pin_y + 28 + 13 * r

    # ---- incidents and trunk labels
    pinrows, pins = [], []
    for i, (a, lab, tip) in sorted(enumerate(INCIDENTS), key=lambda t: T(t[1][0])):
        px = x(T(a))
        w = len(lab) * CH_UP / 2 + 10
        pins.append((i, px, lab, _fit(pinrows, px - w, px + w)))
        tips[f"i{i}"] = {"t": lab, "d": tip, "k": "incident"}
    axis_y = pinrow_y(len(pinrows) - 1) + 44          # the experiments, as the figure's x-axis
    era_y = axis_y + 56
    view_h = era_y + 20

    # a trunk label goes below its node unless a replaced rule leaves the trunk there; then
    # beside the node, and failing that above the trunk
    blocked = [(m["x0"] - 2, m["x0"] + 12) for m in sup]
    blocked_up = ([(x(T(d[0])) - 4, x(T(d[0])) + 26) for d in DEAD] + [(x(T(m[1])) - 8, x(T(m[1])) + 8) for m in MERGES]
                  + [(x(T(g[0])) - 60, x(T(g[1])) + 60) for g in GAPS])
    trows, uprow, tlabs = [[], [], []], [], []
    clear = lambda lo, hi, spans, pad: all(hi + pad < s or lo - pad > e for s, e in spans)
    for i, (a, lab, tip, href) in enumerate(TRUNK):
        px, w = x(T(a)), len(lab) * CH
        opts = (("middle", px - w / 2), ("end", px - 11 - w), ("start", px + 11))
        choice = None
        for anchor, lo in opts:
            row = next((r for r in range(3) if clear(lo, lo + w, trows[r], 8)), None) if clear(lo, lo + w, blocked, 2) else None
            if row is not None:
                trows[row].append((lo, lo + w))
                choice = (anchor, trunk_y + 24 + 15 * row)
                break
        if choice is None:
            for anchor, lo in opts[1:] + opts[:1]:
                if clear(lo, lo + w, blocked_up, 2) and clear(lo, lo + w, uprow, 8):
                    uprow.append((lo, lo + w))
                    choice = (anchor, trunk_y - 15)
                    break
        if choice is None:
            choice = ("middle", trunk_y + 24)
        anchor, ly = choice
        tlabs.append((i, px, lab, anchor, {"middle": px, "end": px - 11, "start": px + 11}[anchor], ly))
        tips[f"t{i}"] = {"t": lab, "d": tip, "k": "kept", "h": href}

    # ---- draw, back to front
    p = []
    for i, (start, name) in enumerate(ERAS):
        d0 = T(start)
        d1 = T(ERAS[i + 1][0]) if i + 1 < len(ERAS) else LAST_DAY + 1
        lo, hi = (0 if i == 0 else x(d0)), (x(d1) if i + 1 < len(ERAS) else view_w)
        if i % 2 == 0:
            p.append(f"<rect class='evo-era' x='{_f(lo)}' y='0' width='{_f(hi - lo)}' height='{view_h}'/>")
        if i:
            p.append(f"<line class='evo-erabound' x1='{_f(lo)}' y1='0' x2='{_f(lo)}' y2='{view_h}'/>")
        ns = sorted(n for n, e in exps.items() if d0 <= e[0] < d1)
        rng = f" · experiments {ns[0]}–{ns[-1]}" if ns else ""
        p.append(f"<text class='evo-eralab' x='{_f(lo + 14)}' y='{era_y}'>{_esc(name + rng)}</text>")

    for d in range(FIRST_DAY, LAST_DAY + 1):
        gx = x(d)
        if x(d + 1) - gx < GRID_MIN_W:
            continue
        p.append(f"<line class='evo-grid' x1='{_f(gx)}' y1='30' x2='{_f(gx)}' y2='{axis_y}'/>")
        p.append(f"<text class='evo-day' x='{_f(gx + 6)}' y='22'>{day_label(d)}</text>")

    # the x-axis: one dot per experiment where it started, a number under every 25th
    p.append(f"<line class='evo-axis' x1='{_f(TRUNK_X0)}' y1='{axis_y}' x2='{_f(trunk_x1)}' y2='{axis_y}'/>")
    last = -1e9
    for n in sorted(exps):
        day, tag, decision = exps[n]
        ex_ = x(day)
        if (n % 25 == 0 or n == 1) and ex_ - last > 96:
            p.append(f"<line class='evo-exptick' x1='{_f(ex_)}' y1='{axis_y}' x2='{_f(ex_)}' y2='{axis_y + 9}'/>")
            p.append(f"<text class='evo-explab' x='{_f(ex_)}' y='{axis_y + 21}'>experiment {n}</text>")
            last = ex_
        p.append(f"<circle class='evo-exp{' kept' if decision == 'kept' else ''}' data-k='e{n}' cx='{_f(ex_)}' cy='{axis_y}' r='3.2'/>")
        title = tag[5:].replace("-", " ") if tag else ""
        tips[f"e{n}"] = {"t": f"Experiment {n}", "d": title, "k": "experiment", "h": f"exp:{n}"}

    p.append(f"<line class='evo-trunk' x1='{_f(TRUNK_X0)}' y1='{trunk_y}' x2='{_f(trunk_x1)}' y2='{trunk_y}'/>")
    for i, (ga, gb, glab, gtip) in enumerate(GAPS):
        g0, g1 = x(T(ga)), x(T(gb))
        p.append(f"<rect class='evo-gap' data-k='gap{i}' x='{_f(g0)}' y='{trunk_y - 14}' width='{_f(g1 - g0)}' height='28'/>")
        p.append(f"<text class='evo-gaplab' data-k='gap{i}' x='{_f((g0 + g1) / 2)}' y='{trunk_y - 21}'>{_esc(glab)}</text>")
        tips[f"gap{i}"] = {"t": glab, "d": gtip, "k": "silence"}

    for i, (a, b, lab, end, tip, _) in enumerate(DEAD):
        p.append(_branch("dead", f"d{i}", x(T(a)), trunk_y, x(T(b)), up(lane_of[("d", i)]), lab, end, "x"))
    for m in sup:
        p.append(_branch("super", f"s{m['i']}", m["x0"], trunk_y, m["x1"], down(m["li"]), m["lab"], m["end"], "endr", m["labx"]))

    for i, px, lab, row in pins:
        ly = pinrow_y(row)
        p.append(f"<path class='evo-pindot' data-k='i{i}' d='M{_f(px)},{pin_y - 5.5} l5.5,5.5 l-5.5,5.5 l-5.5,-5.5 z'/>")
        p.append(f"<line class='evo-pin' data-k='i{i}' x1='{_f(px)}' y1='{pin_y + 7}' x2='{_f(px)}' y2='{ly - 10}'/>")
        p.append(f"<text class='evo-pinlab' data-k='i{i}' x='{_f(px)}' y='{ly}'>{_esc(lab)}</text>")

    for i, (a, b, lab, tip) in enumerate(MERGES):
        lane = up(lane_of[("m", i)])
        x1 = x(T(b))
        x0 = min(x(T(a)), x1 - 60)
        ty = trunk_y - 9
        c2 = min(lane + 16, ty - 7)
        p.append(f"<path class='evo-merge' data-k='m{i}' d='M{_f(x0)},{lane} L{_f(x1 - 22)},{lane} C{_f(x1 - 7)},{lane} {_f(x1)},{c2} {_f(x1)},{ty}'/>")
        p.append(f"<path class='evo-arrow' data-k='m{i}' d='M{_f(x1 - 4.5)},{ty - 2} L{_f(x1)},{ty + 7} L{_f(x1 + 4.5)},{ty - 2} z'/>")
        p.append(f"<circle class='evo-mstart' data-k='m{i}' cx='{_f(x0)}' cy='{lane}' r='3.5'/>")
        p.append(f"<text class='evo-mlab' data-k='m{i}' x='{_f(x1 - 26)}' y='{lane - 9}'>{_esc(lab)}</text>")

    for i, px, lab, anchor, lx, ly in tlabs:
        if anchor == "middle" and ly > trunk_y:
            p.append(f"<line class='evo-tick' x1='{_f(px)}' y1='{trunk_y}' x2='{_f(px)}' y2='{ly - 11}'/>")
        p.append(f"<circle class='evo-node' data-k='t{i}' cx='{_f(px)}' cy='{trunk_y}' r='6'/>")
        p.append(f"<text class='evo-tlab' data-k='t{i}' x='{_f(lx)}' y='{ly}' text-anchor='{anchor}'>{_esc(lab)}</text>")

    head = (f"<svg id='evo-svg' viewBox='0 0 {view_w} {view_h}' width='{view_w}' height='{view_h}' role='img' "
            "aria-label='the research as a branching graph over time'>")
    return head + "".join(p) + "</svg>", tips, x(T(TRUNK[-1][0]))


COUNTS = dict(trunk=len(TRUNK), dead=len(DEAD), super=len(SUPER), merges=len(MERGES), incidents=len(INCIDENTS))
