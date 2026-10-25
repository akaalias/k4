"""Re-score every recorded candidate under the current gates and say who would be champion.

Records are never edited. The outcome goes to data/replay.json, which the dashboard reads for the
current verdict on each experiment, and champion.json is rewritten to match (the previous champion
is kept in data/champion-history.json).

    uv run python tools/replay_rules.py

Current rules (decided 2026-10-15, issue #23): the original four gates; the key, counted by the
harness and charged by the length of its description (not a gate); the reading's English score
above every shuffled-copper control the experiment recorded (at least 10); among survivors, the
lowest loss wins. Added 2026-10-25 (Alexis, issue #88): a reading must be whole, every letter fixed by
its key; one padded with a filler where the key leaves letters open is never kept.
"""
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from kryptos.scorer import key_bits_of, loss, english_score, free_text  # noqa: E402
from kryptos.gates import undetermined  # noqa: E402


def main():
    per, survivors = {}, []
    files = sorted((ROOT / "experiments").glob("*/result.json"))
    # a reading re-submitted by a later experiment is the same reading: if any record holding it
    # says its key leaves letters open, it is open everywhere (0219 re-submitted 0212-0214's)
    open_readings = {c["plaintext"] for f in files for c in json.loads(f.read_text()).get("candidates", [])
                     if c.get("plaintext") and undetermined(c)}
    for f in files:
        r = json.loads(f.read_text())
        controls = [float(x) for x in r.get("controls", []) if x is not None]
        verdicts = {"baseline": 0, "undetermined": 0, "kept_now": 0}
        best = None
        for c in r.get("candidates", []):
            if not (c.get("gate_passed") or c.get("failed_at") in ("memorable", "baseline")):
                continue
            if undetermined(c) or c["plaintext"] in open_readings:
                verdicts["undetermined"] += 1; continue
            bits = key_bits_of(c.get("key"))
            eng = english_score(free_text(c["plaintext"]))
            if len(controls) < 10 or eng <= max(controls):
                verdicts["baseline"] += 1; continue
            l_ = loss(c["plaintext"], bits, 24)
            verdicts["kept_now"] += 1
            if best is None or l_ < best[0]:
                best = (l_, c, bits)
        if best:
            survivors.append((best[0], r["tag"], best[1], best[2]))
        if any(verdicts.values()) or r.get("decision") == "kept":
            reason = ("passes the current gates" if verdicts["kept_now"] else
                      f"{verdicts['undetermined']} candidate(s) have letters their key leaves open, filled with a placeholder (rule of 2026-10-25, issue #88)"
                      if verdicts["undetermined"] and not verdicts["baseline"] else
                      f"{verdicts['baseline']} candidate(s) fail the shuffled-copper baseline: the record has no set of ten or more controls their English must beat")
            per[r["tag"]] = {"decision_recorded": r.get("decision"), "verdict_now": "kept" if best else "reverted",
                             "reason": reason, **verdicts}
    survivors.sort(key=lambda t: t[0])
    champ = None
    if survivors:
        l_, tag, c, bits = survivors[0]
        champ = {"experiment": tag, "loss": l_, "plaintext": c["plaintext"], "key": c["key"],
                 "key_description": c.get("key_description", ""), "key_bits": bits}
    # keep the old champion in the history before replacing it
    hist_p = ROOT / "data" / "champion-history.json"
    hist = json.loads(hist_p.read_text()) if hist_p.exists() else []
    ch_p = ROOT / "champion.json"
    if ch_p.exists():
        old = json.loads(ch_p.read_text())
        if not hist or hist[-1].get("champion", {}).get("experiment") != old.get("experiment"):
            hist.append({"until": date.today().isoformat(), "rule": "lowest loss, gates without the memorable-key and baseline checks", "champion": old})
    hist_p.write_text(json.dumps(hist, indent=1))
    if champ:
        ch_p.write_text(json.dumps(champ, indent=1))
    elif ch_p.exists():
        ch_p.unlink()
    out = {"date": date.today().isoformat(), "rules": "original gates; English above every shuffled-copper control the experiment ran (10 or more); key charged by the length of its description; every letter fixed by the key (2026-10-25, #88); lowest loss wins",
           "champion": champ["experiment"] if champ else None, "experiments": per}
    (ROOT / "data" / "replay.json").write_text(json.dumps(out, indent=1))
    print("champion now:", out["champion"])
    for tag, v in per.items():
        print(tag, v["decision_recorded"], "->", v["verdict_now"], "|", v["reason"])


if __name__ == "__main__":
    main()
