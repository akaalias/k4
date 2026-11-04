"""F15.2: the drafts corpus (issue #118). Guessed 97-letter K4 plaintexts, one set per content hypothesis of
reports/f15.1-content-model.md, the 24 known letters in place.

A language model writes the three free stretches (21, 29 and 23 letters) in words; this script counts the letters and
sends the counts back until every stretch is exact (at most MAX_TURNS turns). Mechanics are drawn per draft from a
seeded generator and recorded with the draft: X stops, misspellings, person and tense, a K3-style ending.

    uv run python tools/f15_drafts.py corpus 50        # 50 drafts per hypothesis, Opus, prompt d1
    uv run python tools/f15_drafts.py heldout 4        # 4 per hypothesis, Sonnet, prompt h1 (plants only)
    uv run python tools/f15_drafts.py dedupe           # writes data/drafts/drafts.jsonl from the raw files

Raw replies go to data/drafts/raw-<set>.jsonl (appended; a rerun skips drafts already written). The judge never sees
the drafts.
"""
import json
import random
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from kryptos.facts import KNOWN  # noqa: E402

OUT = ROOT / "data" / "drafts"
LENS = (21, 29, 23)
MAX_TURNS = 6
SETS = {"corpus": {"model": "claude-opus-5-5", "prompt": "d1", "seed": 1180},
        "heldout": {"model": "claude-sonnet-5-5", "prompt": "h1", "seed": 1181}}

HYPS = {
    "H1": ("a paced location", "The text gives the place of something buried or hidden as a distance and a bearing from a "
           "landmark on the CIA grounds, the way K2 gave coordinates, with the numbers spelled out (a surveyor's note, "
           "paced from a marker)."),
    "H2": ("a meeting at the World Clock", "The text is an agent's instruction or message: where to go, when, what to "
           "look for or carry; the World Clock in Berlin (the Berlin Clock) is the meeting place."),
    "H3": ("Berlin, November 1989", "A witness account of the crowds who gathered at the World Clock in Berlin and "
           "brought down the Wall."),
    "H4": ("two breaches", "The text joins two events: Howard Carter breaching the sealed tomb in Egypt (K3) and the "
           "breaching of the Berlin Wall; a hole, light, people looking through."),
    "H5": ("light and shadow", "A shadow or a beam of light points in a direction at a time told by a clock; something "
           "appears or is revealed when the light falls a certain way."),
    "H6": ("K3 continued", "The text continues K3, which ended with Carnarvon asking CAN YOU SEE ANYTHING: Carter's answer "
           "and what he saw, then a turn to Berlin."),
    "H7": ("a pointer onward", "The text tells the reader where to look next or what follows: something else is hidden, "
           "and these directions lead to it."),
}
PERSONS = {"H1": ["impersonal", "imperative", "they, past tense"], "H2": ["imperative", "you", "he, past tense"],
           "H3": ["I, past tense", "we, past tense", "they, past tense"], "H4": ["I, past tense", "impersonal, past tense"],
           "H5": ["impersonal, present tense", "you", "imperative"], "H6": ["I, past tense"],
           "H7": ["imperative", "you", "impersonal"]}

K1 = "BETWEEN SUBTLE SHADING AND THE ABSENCE OF LIGHT LIES THE NUANCE OF IQLUSION"
K2 = ("IT WAS TOTALLY INVISIBLE HOWS THAT POSSIBLE? THEY USED THE EARTHS MAGNETIC FIELD X THE INFORMATION WAS GATHERED "
      "AND TRANSMITTED UNDERGRUUND TO AN UNKNOWN LOCATION X DOES LANGLEY KNOW ABOUT THIS? THEY SHOULD ITS BURIED OUT THERE "
      "SOMEWHERE X WHO KNOWS THE EXACT LOCATION? ONLY WW THIS WAS HIS LAST MESSAGE X THIRTY EIGHT DEGREES FIFTY SEVEN "
      "MINUTES SIX POINT FIVE SECONDS NORTH SEVENTY SEVEN DEGREES EIGHT MINUTES FORTY FOUR SECONDS WEST X LAYER TWO")
K3 = ("SLOWLY DESPARATLY SLOWLY THE REMAINS OF PASSAGE DEBRIS THAT ENCUMBERED THE LOWER PART OF THE DOORWAY WAS REMOVED "
      "WITH TREMBLING HANDS I MADE A TINY BREACH IN THE UPPER LEFT HAND CORNER AND THEN WIDENING THE HOLE A LITTLE I "
      "INSERTED THE CANDLE AND PEERED IN THE HOT AIR ESCAPING FROM THE CHAMBER CAUSED THE FLAME TO FLICKER BUT PRESENTLY "
      "DETAILS OF THE ROOM WITHIN EMERGED FROM THE MIST X CAN YOU SEE ANYTHING Q")

SYS_D1 = f"""This is for a research project on Kryptos, the public sculpture at CIA headquarters by the artist Jim Sanborn.
Its fourth message, K4, is 97 letters whose plaintext is unpublished. Two words of it are known: EASTNORTHEAST at letters
22-34 and BERLINCLOCK at letters 64-74. We are writing plausible guesses at the whole plaintext ("drafts") to measure
whether such guesses help a search; no guess is claimed to be the answer.

Sanborn's other three messages, as he wrote them (misspellings his own, X as a full stop):
K1: {K1}
K2: {K2}
K3: {K3}

What he has said of K4: it is his own prose; it has a lot to do with secrecy, with finding or opening or discovering
something secret; two events shaped it, his trip to Egypt in 1986 and the fall of the Berlin Wall; the Berlin Clock is
the World Clock in Berlin where the crowds gathered; it is about delivering a message; it leads to something else; it
was checked in 1990 and found not offensive; it is several short sentences.

The layout is fixed:
  part A: exactly 21 letters (letters 1-21)
  EAST NORTHEAST (letters 22-34, fixed)
  part B: exactly 29 letters (letters 35-63)
  BERLIN CLOCK (letters 64-74, fixed)
  part C: exactly 23 letters (letters 75-97)
Only letters A-Z count; spaces are ignored. Part A must lead naturally into EAST NORTHEAST, part B into BERLIN CLOCK.
Count letters carefully, word by word.

Reply with one JSON object on its own line, nothing after it:
{{"a": "<part A in words>", "b": "<part B in words>", "c": "<part C in words>",
 "misspellings": [["<as written>", "<correct>"], ...]}}"""

SYS_H1 = """You are helping test a code-breaking method on the Kryptos sculpture (CIA, 1990). Its last panel hides 97
letters of English; letters 22-34 read EASTNORTHEAST and letters 64-74 read BERLINCLOCK. Write one invented text that
could fill the panel, in the terse, slightly odd style of the sculpture's earlier panels (which use X between sentences,
spell numbers out and contain one deliberate misspelling each; one panel retells Howard Carter opening Tutankhamun's tomb,
another reports something buried at an unknown location at Langley).

Write it as three pieces around the fixed words: first piece exactly 21 letters, then EAST NORTHEAST, second piece
exactly 29 letters, then BERLIN CLOCK, third piece exactly 23 letters. Spaces do not count.

Answer with only this JSON on the last line:
{"a": "...", "b": "...", "c": "...", "misspellings": [["written", "correct"]]}"""


def letters(s):
    return re.sub(r"[^A-Z]", "", s.upper())


def mechanics(rng, h):
    return {"x_stops": rng.choices([0, 1, 2, 3], [0.3, 0.35, 0.25, 0.1])[0],
            "misspellings": rng.choices([0, 1, 2, 3], [0.2, 0.5, 0.2, 0.1])[0],
            "person": rng.choice(PERSONS[h]),
            "question_end": rng.random() < 0.15}


def brief(h, m, k, sset):
    name, desc = HYPS[h]
    lines = [f"Hypothesis {h}, {name}: {desc}",
             f"Voice: {m['person']}.",
             f"Use X as a full stop exactly {m['x_stops']} times (X counts as a letter)." if m["x_stops"] else
             "Do not use X as a stop.",
             f"Include exactly {m['misspellings']} deliberate misspelling(s) of one letter each, as Sanborn did, and list "
             "them." if m["misspellings"] else "No misspellings.",
             "Spell any number out in words."]
    if m["question_end"]:
        lines.append("End with a question, marked as K3 marks it: X before it and Q after it.")
    lines.append(f"This is draft {k + 1} of a set; make it different from an obvious first guess (vary the opening, the "
                 "landmark, the verbs).")
    return "\n".join(lines)


def parse(raw):
    found = re.findall(r"\{.*\}", raw, re.S)
    if not found:
        raise ValueError("no JSON")
    s = found[-1]
    i = s.find('{"a"')
    d = json.loads(s[i:] if i >= 0 else s)
    return d


_lock = threading.Lock()
usage = {"in": 0, "out": 0, "calls": 0, "refusals": 0}


def _client():
    from kryptos.judge import _client as c
    return c()


def one(client, sset, h, k):
    cfg = SETS[sset]
    rng = random.Random(cfg["seed"] * 1000 + list(HYPS).index(h) * 100 + k)
    m = mechanics(rng, h)
    system = SYS_D1 if cfg["prompt"] == "d1" else SYS_H1
    msgs = [{"role": "user", "content": brief(h, m, k, sset)}]
    for turn in range(1, MAX_TURNS + 1):
        kw = {"output_config": {"effort": "medium"}} if "opus" in cfg["model"] else {}
        r = client.messages.create(model=cfg["model"], max_tokens=16000, system=system, messages=msgs, **kw)
        with _lock:
            usage["in"] += r.usage.input_tokens; usage["out"] += r.usage.output_tokens; usage["calls"] += 1
        if r.stop_reason == "refusal":
            with _lock:
                usage["refusals"] += 1
            return {"set": sset, "hyp": h, "k": k, "ok": False, "why": "refusal", "turns": turn}
        raw = "".join(b.text for b in r.content if b.type == "text")
        msgs.append({"role": "assistant", "content": r.content})
        try:
            d = parse(raw)
            parts = [letters(d.get(x, "")) for x in "abc"]
        except (ValueError, json.JSONDecodeError):
            msgs.append({"role": "user", "content": "I could not read the JSON. Reply again with only the JSON line."})
            continue
        got = [len(p) for p in parts]
        if tuple(got) == LENS:
            text = parts[0] + "EASTNORTHEAST" + parts[1] + "BERLINCLOCK" + parts[2]
            assert len(text) == 97 and all(text[q - 1] == c for q, c in KNOWN.items())
            words = " ".join([d["a"].upper(), "EAST NORTHEAST", d["b"].upper(), "BERLIN CLOCK", d["c"].upper()])
            return {"set": sset, "hyp": h, "k": k, "ok": True, "text": text, "words": re.sub(r"\s+", " ", words),
                    "misspellings": d.get("misspellings", []), "mechanics": m, "model": cfg["model"],
                    "prompt": cfg["prompt"], "turns": turn, "at": time.strftime("%Y-%m-%dT%H:%M:%S")}
        fb = "; ".join(f"part {x.upper()} has {g} letters, it must have {n}" for x, g, n in zip("abc", got, LENS) if g != n)
        msgs.append({"role": "user", "content": f"Counted: {fb}. Keep the others as they are, fix only those, and reply "
                                                "with the whole JSON line again."})
    return {"set": sset, "hyp": h, "k": k, "ok": False, "why": "count", "turns": MAX_TURNS}


def generate(sset, per, hyps=None):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"raw-{sset}.jsonl"
    done = set()
    if path.exists():
        for line in path.read_text().splitlines():
            r = json.loads(line)
            if r["ok"]:
                done.add((r["hyp"], r["k"]))
    jobs = [(h, k) for h in (hyps or HYPS) for k in range(per) if (h, k) not in done]
    client = _client()
    t0 = time.time()

    def run(job):
        try:
            res = one(client, sset, *job)
        except Exception as e:  # noqa: BLE001 - record and go on
            res = {"set": sset, "hyp": job[0], "k": job[1], "ok": False, "why": repr(e)[:200]}
        with _lock:
            with path.open("a") as f:
                f.write(json.dumps(res) + "\n")
        return res

    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(run, jobs))
    ok = sum(r["ok"] for r in res)
    price = (4, 20) if "opus" in SETS[sset]["model"] else (2, 10)
    cost = usage["in"] / 1e6 * price[0] + usage["out"] / 1e6 * price[1]
    print(f"{sset}: {ok} of {len(jobs)} drafts exact; {usage['calls']} calls, {usage['refusals']} refusals, "
          f"{usage['in']} in / {usage['out']} out tokens, about ${cost:.2f}, {time.time() - t0:.0f} s")


def dedupe(max_same=0.5):
    """Keep drafts whose 73 free letters agree with every earlier kept draft at under max_same of the places."""
    free = [i for i in range(97) if (i + 1) not in KNOWN]
    kept, dropped = [], 0
    for sset in SETS:
        p = OUT / f"raw-{sset}.jsonl"
        if not p.exists():
            continue
        for line in p.read_text().splitlines():
            r = json.loads(line)
            if not r["ok"]:
                continue
            if any(sum(r["text"][i] == q["text"][i] for i in free) / len(free) >= max_same for q in kept):
                dropped += 1
                continue
            kept.append(r)
    with (OUT / "drafts.jsonl").open("w") as f:
        for i, r in enumerate(kept):
            f.write(json.dumps({"id": f"{r['set'][0]}{i:04d}", **r}) + "\n")
    by = {}
    for r in kept:
        by.setdefault((r["set"], r["hyp"]), 0)
        by[(r["set"], r["hyp"])] += 1
    print(f"kept {len(kept)}, dropped {dropped} near-duplicates (>= {max_same:.0%} of the 73 free letters the same)")
    for k in sorted(by):
        print(" ", k, by[k])


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "dedupe":
        dedupe()
    else:
        generate(cmd, int(sys.argv[2]), sys.argv[3].split(",") if len(sys.argv) > 3 else None)
