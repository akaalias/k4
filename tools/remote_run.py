"""Run one experiment's search on Modal instead of the laptop (issue #99).

    uv run --with modal python tools/remote_run.py ATTACK RAW_OUT BUDGET

run_experiment.py calls this in place of _runner.py when data/compute.json says {"where": "modal"}. A Modal
container (8 physical cores, Python 3.14) gets a copy of the repository without the large folders and without
.env, runs _runner.py there, and sends back raw.json and every file the run created or changed (the judge's
store, reports an attack writes). ctx.progress reaches data/experiment-progress.json as before.

Exit codes: 0 the run finished on Modal (the attack itself may still have failed; raw.json says so);
75 Modal could not run it (no credit, no network, a lost container): run_experiment.py then runs it locally.
"""
import json
import os
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

import modal

ROOT = Path(__file__).resolve().parent.parent
REMOTE = "/repo"
def _setting():
    try:
        return json.loads((ROOT / "data" / "compute.json").read_text())
    except (OSError, ValueError):
        return {}


# Cores per run (data/compute.json "cpu", default 8). Every Pool gets that many processes (K4_WORKERS); the price
# scales with cores, so more cores cost about the same per experiment and finish sooner.
CPU = int(os.environ.get("K4_MODAL_CPU") or _setting().get("cpu", 8)) if modal.is_local() else 8
MEMORY_GIB = max(4, CPU // 4)
UNAVAILABLE = 75
SILENCE = 15 * 60   # seconds without a heartbeat before the laptop takes the run back
DOLLARS_PER_HOUR = CPU * 0.04716 + MEMORY_GIB * 0.00799   # modal.com/pricing, 2026-10-27
# K4_REMOTE_TEST=DIR (parity tests): marker and progress go to DIR and changed files are not written back
TEST_DIR = os.environ.get("K4_REMOTE_TEST")
MARKER = Path(TEST_DIR) / f"remote-run-{os.getpid()}.json" if TEST_DIR else ROOT / "data" / "remote-run.json"

# Never shipped: secrets, version control, and the folders no attack reads (they are large).
IGNORE = [".env", ".env.*", ".git", ".venv", "**/__pycache__", "transcripts", "logs", "figures", "design",
          "Kryptos Blender Model", "Unsolved Book Kryptos Chapter", "drafts", ".pytest_cache"]
SECRET = "anthropic"   # Modal secret holding ANTHROPIC_API_KEY for ctx.judge, created by Alexis 2026-10-27


app = modal.App("k4-experiment")
image = (modal.Image.debian_slim(python_version="3.14")
         .apt_install("gcc")                    # some attacks compile a small C library (ctypes)
         .uv_sync(str(ROOT))                    # the project's locked packages, as on the laptop
         .add_local_dir(ROOT, REMOTE, ignore=IGNORE))


@app.function(image=image, cpu=CPU, memory=MEMORY_GIB * 1024, timeout=24 * 3600, secrets=[modal.Secret.from_name(SECRET)])
def search(attack_rel: str, budget: str, workers: int):
    """Runs _runner.py on the attack file; yields progress, then the result and the files the run changed."""
    t0 = time.time()
    before = {p: p.stat().st_mtime for p in Path(REMOTE).rglob("*") if p.is_file()}
    out = Path("/tmp/raw.json")
    progress = Path(REMOTE) / "data" / "experiment-progress.json"
    sys.path.insert(0, REMOTE)
    from kryptos import checkpoint                 # issue #105: finished units go home as they are saved
    ckpt = checkpoint.path_for(f"{REMOTE}/{attack_rel}", root=REMOTE)
    sent = ckpt.stat().st_size if ckpt.exists() else 0
    proc = subprocess.Popen([sys.executable, f"{REMOTE}/_runner.py", f"{REMOTE}/{attack_rel}", str(out), budget],
                            cwd=REMOTE, env={**os.environ, "PYTHONPATH": REMOTE, "K4_WORKERS": str(workers)})
    last, beat = None, time.time()
    while True:
        running = proc.poll() is None
        if running:
            time.sleep(5)
        msg = {}
        if progress.exists() and progress.read_text() != last:
            last = progress.read_text()
            msg["progress"] = last
        lines, sent = checkpoint.new_lines(ckpt, sent)
        if lines:
            msg["checkpoint"] = lines
        if not msg and time.time() - beat > 60:
            msg["alive"] = True              # the heartbeat the laptop's watchdog waits for
        if msg:
            yield msg
            beat = time.time()
        if not running:
            break
    changed = {}
    for p in Path(REMOTE).rglob("*"):
        if (p.is_file() and "__pycache__" not in p.parts and p != progress
                and before.get(p) != p.stat().st_mtime and p.stat().st_size < 50_000_000):
            changed[str(p.relative_to(REMOTE))] = p.read_bytes()
    yield {"raw": out.read_text() if out.exists() else None, "files": changed,
           "seconds": time.time() - t0, "exit": proc.returncode}


def main(attack, raw_out, budget):
    attack_rel = str(Path(attack).resolve().relative_to(ROOT))   # an attack file inside the repository
    progress = Path(TEST_DIR) / f"progress-{os.getpid()}.json" if TEST_DIR else ROOT / "data" / "experiment-progress.json"
    final = None
    heard = [time.time()]
    sys.path.insert(0, str(ROOT))
    from kryptos import checkpoint
    ckpt = checkpoint.path_for(attack, root=None if TEST_DIR is None else TEST_DIR)

    def stop(signum, frame):
        """Stopped (tools/stop_experiment.sh, issue #104): leaving app.run() stops the Modal app too."""
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, stop)

    def watchdog():
        """Modal can fail without raising (a container that never starts): hand the run back to the laptop."""
        while True:
            time.sleep(min(30, SILENCE))
            if time.time() - heard[0] > SILENCE:
                print(f"remote_run: no word from Modal for {SILENCE // 60} min; running locally", flush=True)
                MARKER.unlink(missing_ok=True)
                os._exit(UNAVAILABLE)
    threading.Thread(target=watchdog, daemon=True).start()
    try:
        with modal.enable_output(), app.run():
            MARKER.write_text(json.dumps({"pid": os.getpid(), "attack": attack_rel, "cpu": CPU,
                                          "url": f"https://modal.com/apps/alexis-rondeau/main/{app.app_id}", "started": time.time()}))
            for msg in search.remote_gen(attack_rel, budget, CPU):
                heard[0] = time.time()
                if "progress" in msg:
                    progress.write_text(msg["progress"])
                if "checkpoint" in msg:
                    ckpt.parent.mkdir(parents=True, exist_ok=True)
                    with open(ckpt, "ab") as f:
                        f.write(msg["checkpoint"])
                if "raw" in msg:
                    final = msg
    except Exception as e:  # noqa: BLE001  (billing limit, network, lost container)
        print(f"remote_run: Modal could not run the experiment: {e!r}")
        return UNAVAILABLE
    finally:
        MARKER.unlink(missing_ok=True)
    if final is None or final["raw"] is None:
        print(f"remote_run: the Modal run ended without raw.json (exit {final and final['exit']})")
        return UNAVAILABLE
    for rel, data in ({} if TEST_DIR else final["files"]).items():
        dest = ROOT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    raw = json.loads(final["raw"])
    raw["compute"] = {"where": "modal", "cpu": CPU, "workers": CPU, "python": "3.14", "seconds": round(final["seconds"], 1),
                      "dollars": round(final["seconds"] / 3600 * DOLLARS_PER_HOUR, 3)}
    Path(raw_out).write_text(json.dumps(raw, indent=1))
    print(f"remote_run: done on Modal in {final['seconds'] / 60:.1f} min; {len(final['files'])} files returned")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
