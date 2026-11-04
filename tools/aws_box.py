"""Runs on the AWS machine, not on the laptop (issue #115). tools/aws_run.py's boot script starts it.

    python tools/aws_box.py /opt/job/job.json

job.json: {"attack": path in the repo, "budget": "inf" or seconds, "workers": n, "urls": {status, checkpoint, result}}.
It runs _runner.py on the attack with K4_WORKERS=n and talks to the laptop only through presigned S3 links:
- status: {"beat", "progress", "load"}, sent when progress changes and at least once a minute (the heartbeat);
- checkpoint: the whole checkpoint file, sent when it grows, so a lost machine loses no finished unit;
- result: a tar.gz with raw.json, meta.json (exit code, seconds) and every file the run created or changed.
Standard library only, so it needs nothing beyond the project's own environment.
"""
import io
import json
import os
import subprocess
import sys
import tarfile
import time
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))


def put(url, data, tries=6):
    """PUT bytes to a presigned link, retrying network trouble; False if it never went through."""
    for i in range(tries):
        try:
            req = urllib.request.Request(url, data=data, method="PUT")
            urllib.request.urlopen(req, timeout=300).read()
            return True
        except Exception as e:  # noqa: BLE001
            print(f"[box] upload failed ({e!r}), retry {i + 1}", flush=True)
            time.sleep(min(60, 2 ** i))
    return False


def main(job_path):
    from kryptos import checkpoint
    job = json.loads(Path(job_path).read_text())
    urls = job["urls"]
    attack = REPO / job["attack"]
    raw = Path("/opt/job/raw.json")
    progress = REPO / "data" / "experiment-progress.json"
    ckpt = checkpoint.path_for(attack, root=REPO)
    before = {p: p.stat().st_mtime for p in REPO.rglob("*") if p.is_file()}
    t0 = time.time()
    env = {**os.environ, "PYTHONPATH": str(REPO), "K4_WORKERS": str(job["workers"])}
    proc = subprocess.Popen([sys.executable, str(REPO / "_runner.py"), str(attack), str(raw), job["budget"]],
                            cwd=REPO, env=env)
    last_prog, last_beat, ck_size = None, 0.0, ckpt.stat().st_size if ckpt.exists() else 0
    while True:
        running = proc.poll() is None
        prog = progress.read_text() if progress.exists() else None
        if prog != last_prog or time.time() - last_beat > 60:
            put(urls["status"], json.dumps({"beat": time.time(), "progress": prog,
                                            "load": os.getloadavg()[0]}).encode(), tries=2)
            last_prog, last_beat = prog, time.time()
        size = ckpt.stat().st_size if ckpt.exists() else 0
        if size > ck_size:
            if put(urls["checkpoint"], ckpt.read_bytes(), tries=2):
                ck_size = size
        if not running:
            break
        time.sleep(5)
    seconds = time.time() - t0
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as t:
        def add(name, data):
            ti = tarfile.TarInfo(name)
            ti.size = len(data)
            t.addfile(ti, io.BytesIO(data))
        add("meta.json", json.dumps({"exit": proc.returncode, "seconds": seconds}).encode())
        if raw.exists():
            add("raw.json", raw.read_bytes())
        for p in REPO.rglob("*"):
            if (p.is_file() and "__pycache__" not in p.parts and ".venv" not in p.parts and p != progress
                    and before.get(p) != p.stat().st_mtime and p.stat().st_size < 50_000_000):
                add("files/" + str(p.relative_to(REPO)), p.read_bytes())
    ok = put(urls["result"], buf.getvalue())
    print(f"[box] run exit={proc.returncode} seconds={seconds:.0f} result {'uploaded' if ok else 'upload FAILED'}",
          flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
