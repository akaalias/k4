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
import subprocess
import sys
import time
from pathlib import Path

import modal

ROOT = Path(__file__).resolve().parent.parent
REMOTE = "/repo"
CPU = 8
MEMORY_GIB = 4
UNAVAILABLE = 75
DOLLARS_PER_HOUR = CPU * 0.04716 + MEMORY_GIB * 0.00799   # modal.com/pricing, 2026-10-27
MARKER = ROOT / "data" / "remote-run.json"   # while a search runs on Modal; tools/loop_tui.py reads it

# Never shipped: secrets, version control, and the folders no attack reads (they are large).
IGNORE = [".env", ".env.*", ".git", ".venv", "**/__pycache__", "transcripts", "logs", "figures", "design",
          "Kryptos Blender Model", "Unsolved Book Kryptos Chapter", "drafts", ".pytest_cache"]
SECRET = "anthropic"   # Modal secret holding ANTHROPIC_API_KEY, created by Alexis; needed only by judge runs


def _secret_exists():
    try:
        modal.Secret.from_name(SECRET).hydrate()
        return True
    except Exception:  # noqa: BLE001
        return False


USES_JUDGE = __name__ == "__main__" and modal.is_local() and len(sys.argv) > 1 and "ctx.judge" in Path(sys.argv[1]).read_text()
SECRETS = [modal.Secret.from_name(SECRET)] if USES_JUDGE and _secret_exists() else []

app = modal.App("k4-experiment")
image = (modal.Image.debian_slim(python_version="3.14")
         .uv_pip_install("anthropic>=1.15.0", "markdown>=3.11.1")
         .add_local_dir(ROOT, REMOTE, ignore=IGNORE))


@app.function(image=image, cpu=CPU, memory=MEMORY_GIB * 1024, timeout=24 * 3600, secrets=SECRETS)
def search(attack_rel: str, budget: str):
    """Runs _runner.py on the attack file; yields progress, then the result and the files the run changed."""
    t0 = time.time()
    before = {p: p.stat().st_mtime for p in Path(REMOTE).rglob("*") if p.is_file()}
    out = Path("/tmp/raw.json")
    progress = Path(REMOTE) / "data" / "experiment-progress.json"
    proc = subprocess.Popen([sys.executable, f"{REMOTE}/_runner.py", f"{REMOTE}/{attack_rel}", str(out), budget],
                            cwd=REMOTE, env={**os.environ, "PYTHONPATH": REMOTE})
    last = None
    while proc.poll() is None:
        time.sleep(5)
        if progress.exists():
            text = progress.read_text()
            if text != last:
                last = text
                yield {"progress": text}
    changed = {}
    for p in Path(REMOTE).rglob("*"):
        if (p.is_file() and "__pycache__" not in p.parts and p != progress
                and before.get(p) != p.stat().st_mtime and p.stat().st_size < 50_000_000):
            changed[str(p.relative_to(REMOTE))] = p.read_bytes()
    yield {"raw": out.read_text() if out.exists() else None, "files": changed,
           "seconds": time.time() - t0, "exit": proc.returncode}


def main(attack, raw_out, budget):
    attack_rel = str(Path(attack).resolve().relative_to(ROOT))   # an attack file inside the repository
    if USES_JUDGE and not SECRETS:
        print(f"remote_run: this attack calls the judge and Modal has no '{SECRET}' secret; running locally")
        return UNAVAILABLE
    # K4_PROGRESS_FILE redirects the bar, so a test run does not overwrite the loop's (tests/, issue #99)
    progress = Path(os.environ.get("K4_PROGRESS_FILE") or ROOT / "data" / "experiment-progress.json")
    final = None
    try:
        with modal.enable_output(), app.run():
            MARKER.write_text(json.dumps({"pid": os.getpid(), "attack": attack_rel, "cpu": CPU,
                                          "url": f"https://modal.com/apps/alexis-rondeau/main/{app.app_id}", "started": time.time()}))
            for msg in search.remote_gen(attack_rel, budget):
                if "progress" in msg:
                    progress.write_text(msg["progress"])
                else:
                    final = msg
    except Exception as e:  # noqa: BLE001  (billing limit, network, lost container)
        print(f"remote_run: Modal could not run the experiment: {e!r}")
        return UNAVAILABLE
    finally:
        MARKER.unlink(missing_ok=True)
    if final is None or final["raw"] is None:
        print(f"remote_run: the Modal run ended without raw.json (exit {final and final['exit']})")
        return UNAVAILABLE
    for rel, data in final["files"].items():
        dest = ROOT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    raw = json.loads(final["raw"])
    raw["compute"] = {"where": "modal", "cpu": CPU, "python": "3.14", "seconds": round(final["seconds"], 1),
                      "dollars": round(final["seconds"] / 3600 * DOLLARS_PER_HOUR, 3)}
    Path(raw_out).write_text(json.dumps(raw, indent=1))
    print(f"remote_run: done on Modal in {final['seconds'] / 60:.1f} min; {len(final['files'])} files returned")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
