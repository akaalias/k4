"""A blind, tolerant English judge (issue #76, decided by Alexis 2026-10-16 in issue #11).

A language model reads one candidate at a time and says how much of it reads as English, allowing the
damage Sanborn's own plaintexts carry: deliberate misspellings, X between words or sentences, numbers
spelled out, terse notes or directions. It filters candidates. It never certifies a solution.

Blind by construction, not by the caller's care:
- each call sees one text and nothing else: no label, no experiment, no other candidate;
- the 24 known places are always replaced by '#' here, so EASTNORTHEAST and BERLINCLOCK cannot sway it;
- letters a search could not determine are passed as '?' and shown as '?'.

Fixed and recorded: MODEL, PROMPT_VERSION and the prompt text (the API takes no temperature here, so a
score is made repeatable by storing it); every response is appended to
data/judge/responses.jsonl and reused for the same (model, prompt version, masked text).

    from kryptos.judge import judge
    judge(["...97 letters...", ...])    # -> [{"score": 0-100 or None, "reading": "...", "cached": bool}, ...]

Needs ANTHROPIC_API_KEY in the environment or in .env at the repository root (git-ignored). A hard cap
on new calls per process (JUDGE_MAX_CALLS, default 3000) stops a runaway search from spending money.
"""
import hashlib
import json
import os
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from .facts import KNOWN

ROOT = Path(__file__).resolve().parents[1]
STORE = ROOT / "data" / "judge" / "responses.jsonl"
MODEL = os.environ.get("JUDGE_MODEL", "claude-sonnet-5-5")  # chosen by the bench (reports/judge-bench.md)
PROMPT_VERSION = "j3"
MAX_CALLS = int(os.environ.get("JUDGE_MAX_CALLS", "3000"))
WORKERS = 8

SYSTEM = """Context: this is for a hobby project on Kryptos, the public sculpture at CIA headquarters whose fourth
message (K4) is an unsolved puzzle. The strings are candidate decryptions produced by our own search code, scored so
that obvious noise can be discarded.

You judge whether a string of capital letters is English plaintext. You see one string at a time.

The string has no spaces or punctuation. '#' marks letters that are withheld from you; '?' marks letters
nobody knows. Words may run across '#' and '?'. Read the string as a careful cryptanalyst would, and allow
for the way this writer's other messages look:
- deliberate misspellings (one letter changed, e.g. IQLUSION for ILLUSION, UNDERGRUUND, DESPARATLY);
- X used as a full stop or a word break;
- numbers spelled out (THIRTYEIGHT), compass words, terse notes, instructions or directions;
- occasional single wrong letters from a copying slip.

Random letters often contain short words (THE, AND, ON, IS) by chance; do not count those as evidence.
What counts is long runs that read as English words in a sensible order.

You may reason briefly first. End your reply with this JSON on its own line:
{"reading": "<the string split into the English words you see, '?' for stretches you cannot read>",
 "score": <0-100>}
Score scale: 0 random letters; 20 a few short words, likely chance; 50 several real words in a row but
much unreadable; 80 mostly readable English with some damage; 100 fluent English throughout."""

_lock = threading.Lock()
_cache = None
usage = {"calls": 0, "cached": 0, "input_tokens": 0, "output_tokens": 0, "errors": 0}


def mask(text):
    """The text as the judge sees it: '#' at the 24 known places, '?' kept, anything else not A-Z as '?'."""
    t = [c if "A" <= c <= "Z" else "?" for c in text.upper()]
    for q in KNOWN:
        if q - 1 < len(t):
            t[q - 1] = "#"
    return "".join(t)


def _key(masked):
    return hashlib.sha256(f"{MODEL}|{PROMPT_VERSION}|{masked}".encode()).hexdigest()[:24]


def _load():
    global _cache
    if _cache is None:
        _cache = {}
        if STORE.exists():
            for line in STORE.read_text().splitlines():
                r = json.loads(line)
                _cache[r["key"]] = r
    return _cache


def _client():
    import anthropic
    if not os.environ.get("ANTHROPIC_API_KEY"):
        env = ROOT / ".env"
        if env.exists():
            for line in env.read_text().splitlines():
                if line.startswith("ANTHROPIC_API_KEY="):
                    os.environ["ANTHROPIC_API_KEY"] = line.split("=", 1)[1].strip()
    return anthropic.Anthropic(max_retries=6)


_JSON = re.compile(r'\{[^{}]*"score"[^{}]*\}', re.S)


def _parse(s):
    """The last JSON object in the reply that has a score (the model may reason before it)."""
    found = _JSON.findall(s)
    if not found:
        raise ValueError("no JSON verdict in the reply")
    d = json.loads(found[-1])
    return {"reading": str(d.get("reading", "")), "score": max(0, min(100, int(round(float(d["score"])))))}


def _no_thinking():
    """Thinking off. Haiku 5.5 takes "disabled"; Sonnet 5.5 refuses that and takes "between_tools", which with no
    tools means it does not think before replying."""
    return {"type": "disabled"} if "haiku" in MODEL else {"type": "between_tools"}


def _ask(client, masked):
    with _lock:
        if usage["calls"] >= MAX_CALLS:
            raise RuntimeError(f"judge: call cap reached ({MAX_CALLS}); raise JUDGE_MAX_CALLS deliberately")
        usage["calls"] += 1
    last = None
    for attempt in range(3):
        try:
            # thinking off: the same judge on every call; the reading it writes first is its reasoning
            r = client.messages.create(model=MODEL, max_tokens=1500, system=SYSTEM, thinking=_no_thinking(),
                                       messages=[{"role": "user", "content": masked}])
            with _lock:
                usage["input_tokens"] += r.usage.input_tokens
                usage["output_tokens"] += r.usage.output_tokens
            raw = "".join(b.text for b in r.content if b.type == "text")
            out = _parse(raw)
            rec = {"key": _key(masked), "model": MODEL, "prompt": PROMPT_VERSION, "text": masked,
                   "raw": raw, **out, "at": time.strftime("%Y-%m-%dT%H:%M:%S")}
            with _lock:
                STORE.parent.mkdir(parents=True, exist_ok=True)
                with STORE.open("a") as f:
                    f.write(json.dumps(rec) + "\n")
                _load()[rec["key"]] = rec
            return rec
        except (ValueError, KeyError, json.JSONDecodeError) as e:  # unparseable reply: ask again
            last = e
    with _lock:
        usage["errors"] += 1
    raise RuntimeError(f"judge: no parseable reply for {masked[:20]}...: {last!r}")


def judge(texts, workers=WORKERS):
    """Score each text (same order as given). Cached texts cost nothing; new ones are asked in parallel."""
    masked = [mask(t) for t in texts]
    cache = _load()
    todo = sorted({m for m in masked if _key(m) not in cache})
    failed = {}
    if todo:
        client = _client()

        def one(m):
            try:
                _ask(client, m)
            except RuntimeError as e:
                if "call cap" in str(e):
                    raise
                failed[m] = str(e)
        with ThreadPoolExecutor(workers) as ex:
            list(ex.map(one, todo))
    out = []
    for m in masked:
        if m in failed:  # no verdict after three tries: reported as None, never guessed
            out.append({"score": None, "reading": "", "cached": False, "error": failed[m]})
            continue
        r = cache[_key(m)]
        out.append({"score": r["score"], "reading": r["reading"], "cached": m not in todo})
    usage["cached"] += sum(1 for m in masked if m not in todo)
    return out


def known_free_letters(text):
    """How many of the 73 free places carry a determined letter (not '?')."""
    return sum(1 for i, c in enumerate(text, start=1) if i not in KNOWN and "A" <= c <= "Z")


_WORD = re.compile(r"[A-Z]{4,}")


def reading_words(reading):
    """Words of four or more letters in a reading, for reports."""
    return _WORD.findall(reading or "")
