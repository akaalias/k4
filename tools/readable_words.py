"""Find the readable English words in candidate readings, for the word boxes on the dashboard.

A language model (Claude Haiku, through the headless Claude Code CLI) proposes word spans; each
span is then checked here: the letters at those places must spell the word, the word must be in
the system dictionary (or a short list of common two-letter words), and spans may not overlap.
Results are cached in data/readable_words.json, keyed by the 97-letter reading.

    uv run python tools/readable_words.py            # every candidate that passed every gate

These boxes say what a reader can pick out, nothing more: a key-completion climb chooses free key
letters to make the reading look like English, so readable fragments appear by construction.
"""
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "readable_words.json"
MODEL = "claude-haiku-5-5"
TWO = {"AN", "AS", "AT", "BE", "BY", "DO", "GO", "HE", "IF", "IN", "IS", "IT", "ME", "MY", "NO", "OF", "ON", "OR", "SO", "TO", "UP", "US", "WE"}
WORDS = {w.strip().upper() for w in Path("/usr/share/dict/words").read_text().split() if w.strip().isalpha()}

PROMPT = """Return only JSON, no prose. Here is a 97-letter string with no spaces. Mark the stretches a careful reader would accept as real English words, as they would box words in a solved cipher. Do not stretch: letters that do not form a word stay unmarked. Prefer longer genuine words over splitting them; do not mark obscure dictionary words that a reader would not see as English here. Give 0-based start and end (end exclusive), no overlaps, in order.
String: {s}
Format: {{"words":[{{"start":0,"end":3,"word":"ABC"}}]}}"""


def ask(s):
    out = subprocess.run(["claude", "-p", "--model", MODEL, "--output-format", "json", PROMPT.format(s=s)],
                         capture_output=True, text=True, timeout=300)
    res = json.loads(out.stdout)["result"]
    res = res[res.index("{"):res.rindex("}") + 1]
    return json.loads(res)["words"]


def check(s, spans):
    """Keep only spans whose letters spell a dictionary word; drop overlaps."""
    kept, last = [], -1
    for w in sorted(spans, key=lambda w: w["start"]):
        a, b = int(w["start"]), int(w["end"])
        word = s[a:b]
        if a < last or not (0 <= a < b <= len(s)) or len(word) < 2:
            continue
        if (len(word) == 2 and word not in TWO) or (len(word) > 2 and word not in WORDS):
            continue
        kept.append([a, b, word]); last = b
    return kept


def readings():
    for f in sorted((ROOT / "experiments").glob("*/result.json")):
        for c in json.loads(f.read_text()).get("candidates", []):
            if c.get("gate_passed") and c.get("plaintext") and len(c["plaintext"]) == 97:
                yield c["plaintext"]
    ch = ROOT / "champion.json"
    if ch.exists():
        yield json.loads(ch.read_text())["plaintext"]


def words_for(texts):
    """Readable words for each 97-letter text: from the cache, or asked for and cached now.
    Returns {text: [[start, end, word], ...]}. Used by run_experiment.py after every run."""
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    todo = sorted({t for t in texts if t not in cache})
    if todo:
        with ThreadPoolExecutor(4) as ex:
            for t, r in ex.map(lambda t: (t, _safe(t)), todo):
                if r:
                    cache[t] = r
        CACHE.write_text(json.dumps(cache, indent=1))
    return {t: cache[t]["words"] for t in texts if t in cache}


def _safe(s):
    try:
        return {"model": MODEL, "words": check(s, ask(s))}
    except Exception as e:  # noqa: BLE001
        print("readable words failed:", s[:20], e, file=sys.stderr)
        return None


def main():
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    todo = sorted({s for s in readings() if s not in cache})
    print(f"{len(todo)} readings to segment, {len(cache)} cached")

    def one(s):
        try:
            return s, {"model": MODEL, "words": check(s, ask(s))}
        except Exception as e:  # noqa: BLE001
            print("failed:", s[:20], e, file=sys.stderr)
            return s, None

    with ThreadPoolExecutor(4) as ex:
        for s, r in ex.map(one, todo):
            if r:
                cache[s] = r
                print(s[:24], " ".join(w for _, _, w in r["words"]))
                CACHE.write_text(json.dumps(cache, indent=1))


if __name__ == "__main__":
    main()
