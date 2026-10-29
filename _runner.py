"""Child process: imports attack.py, runs it under the time budget, re-encrypts
every candidate with the attack's own forward function, writes JSON.
Invoked by run_experiment.py; not meant to be called by hand."""
import importlib.util
import json
import multiprocessing.context
import os
import sys
import time
import traceback
from pathlib import Path
from types import SimpleNamespace

from kryptos import facts, ciphers, scorer, checkpoint


def _judge(texts):
    """The blind English judge (kryptos.judge, issue #76), imported only when an attack calls it."""
    from kryptos import judge
    return judge.judge(texts)


def _cap_workers():
    """Sets how many processes every Pool an attack starts gets (attacks mostly ask for 8), issue #99.
    K4_WORKERS: exactly that many (a Modal run with more cores sets it to its core count).
    K4_MAX_WORKERS: at most that many (the laptop fallback when Modal cannot take a run)."""
    force = int(os.environ.get("K4_WORKERS") or 0)
    cap = int(os.environ.get("K4_MAX_WORKERS") or 0)
    if force <= 0 and cap <= 0:
        return None
    pool = multiprocessing.context.BaseContext.Pool

    def sized(self, processes=None, *a, **kw):
        n = force if force > 0 else min(processes or cap, cap)
        return pool(self, n, *a, **kw)
    multiprocessing.context.BaseContext.Pool = sized
    return force if force > 0 else cap


PROGRESS = Path(__file__).resolve().parent / "data" / "experiment-progress.json"
_last_write = [0.0]


def _progress(done, total, label=""):
    """ctx.progress(done, total, label): how far the run is, for the loop's terminal bar (issue #97).
    Cheap to call often: it writes at most once a second, and always at the end."""
    now = time.time()
    if now - _last_write[0] < 1.0 and done < total:
        return
    _last_write[0] = now
    try:
        PROGRESS.write_text(json.dumps({"done": done, "total": total, "label": str(label)[:80], "updated": now}))
    except OSError:
        pass


def main(attack_path, out_path, budget_s):
    t0 = time.time()
    cap = _cap_workers()
    spec = importlib.util.spec_from_file_location("attack", attack_path)
    attack = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(attack)
    ckpt = checkpoint.path_for(attack_path, root=Path(attack_path).resolve().parent)
    saved = checkpoint.load(ckpt)          # units an earlier run of this same attack.py finished (issue #105)
    save = checkpoint.Saver(ckpt)

    ctx = SimpleNamespace(
        K4=facts.K4,
        KNOWN=facts.KNOWN,
        CRIBS=facts.CRIBS,
        KRYPTOS_ALPHABET=facts.KRYPTOS_ALPHABET,
        STANDARD_ALPHABET=facts.STANDARD_ALPHABET,
        vocabulary=facts.load_vocabulary(),
        ciphers=ciphers,
        english_score=scorer.english_score,
        deadline=t0 + budget_s,
        time_left=lambda: (t0 + budget_s) - time.time(),
        judge=_judge,
        progress=_progress,
        saved=saved,
        save=save,
    )
    out = {"candidates": [], "bounds": {}, "notes": "", "controls": [], "error": None, "worked_example": ""}
    try:
        res = attack.run(ctx) or {}
        out["bounds"] = res.get("bounds", {})
        out["notes"] = res.get("notes", "")
        # gate 4 (issue #23) reads these; dropping them made the shuffled-copper gate unpassable (issue #45)
        out["controls"] = [float(x) for x in res.get("controls", []) if isinstance(x, (int, float))]
        for c in res.get("candidates", [])[:50]:
            pt = c["plaintext"]
            try:
                re_ct = attack.encrypt(pt, c["key"])
            except Exception as e:  # noqa: BLE001
                re_ct = None
                c["encrypt_error"] = repr(e)
            out["candidates"].append({
                "plaintext": pt,
                "key": c["key"],
                "key_bits": float(c.get("key_bits", 0.0)),
                "key_description": c.get("key_description", ""),
                "reencrypted": re_ct,
                "notes": c.get("notes", ""),
            })
        example_key = out["candidates"][0]["key"] if out["candidates"] else None
        try:
            out["worked_example"] = attack.worked_example(ctx, example_key)
        except Exception as e:  # noqa: BLE001
            out["worked_example"] = f"(worked_example failed: {e!r})"
    except Exception:  # noqa: BLE001
        out["error"] = traceback.format_exc()
    out["seconds"] = time.time() - t0
    out["compute"] = {"where": "local", "workers": cap or "as the attack asks"}
    out["checkpoint"] = {"file": ckpt.name, "resumed": len(saved), "saved": save.count}
    if "kryptos.judge" in sys.modules:
        j = sys.modules["kryptos.judge"]
        out["judge"] = {"model": j.MODEL, "prompt": j.PROMPT_VERSION, **j.usage}
    json.dump(out, open(out_path, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], float(sys.argv[3]))
