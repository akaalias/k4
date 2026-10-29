"""Checkpoints (issue #105) and stopping a whole run (issue #104)."""
import json
import os
import signal
import subprocess
import sys
import textwrap
import time
from pathlib import Path

import pytest

import _runner
import run_experiment
from kryptos import checkpoint

ROOT = Path(__file__).resolve().parent.parent

# A toy attack: ten units, each sleeps a little; units already saved are skipped and reused.
TOY = textwrap.dedent('''
    import time
    def run(ctx):
        computed = []
        for i in range(10):
            key = f"unit-{i}"
            if key in ctx.saved:
                continue
            time.sleep(DELAY)
            ctx.save(key, i * i)
            computed.append(i)
        values = {k: ctx.saved.get(k) for k in ctx.saved}
        return {"bounds": {"computed": computed, "resumed": sorted(ctx.saved)}, "controls": []}
''')


def toy(tmp_path, delay=0.0):
    a = tmp_path / "attack.py"
    a.write_text(f"DELAY = {delay}\n" + TOY)
    return a


def test_save_and_load_round_trip(tmp_path):
    f = tmp_path / "c.jsonl"
    save = checkpoint.Saver(f)
    save("a", {"score": 1.5})
    save("b", [1, 2])
    with open(f, "a") as h:
        h.write('{"k": "c", "v"')               # a line cut short by a kill
    assert checkpoint.load(f) == {"a": {"score": 1.5}, "b": [1, 2]}
    assert save.count == 2
    with pytest.raises(TypeError):
        save(3, "not a string key")


def test_any_change_to_the_attack_starts_afresh(tmp_path):
    a = tmp_path / "attack.py"
    a.write_text("x = 1\n")
    first = checkpoint.path_for(a, root=tmp_path)
    a.write_text("x = 2\n")
    assert checkpoint.path_for(a, root=tmp_path) != first
    assert first.parent == tmp_path / "data" / "checkpoints"


def test_only_whole_lines_are_sent_home(tmp_path):
    f = tmp_path / "c.jsonl"
    f.write_bytes(b'{"k": "a", "v": 1}\n{"k": "b"')
    data, offset = checkpoint.new_lines(f, 0)
    assert data == b'{"k": "a", "v": 1}\n' and offset == len(data)
    with open(f, "ab") as h:
        h.write(b', "v": 2}\n')
    data, offset2 = checkpoint.new_lines(f, offset)
    assert json.loads(data) == {"k": "b", "v": 2}
    assert checkpoint.new_lines(tmp_path / "missing", 5) == (b"", 5)


def test_runner_skips_saved_units(tmp_path, monkeypatch):
    monkeypatch.setattr(_runner, "PROGRESS", tmp_path / "progress.json")
    a = toy(tmp_path)
    save = checkpoint.Saver(checkpoint.path_for(a, root=tmp_path))
    save("unit-0", 0)
    save("unit-1", 1)
    out = tmp_path / "raw.json"
    _runner.main(str(a), str(out), float("inf"))
    raw = json.loads(out.read_text())
    assert raw["error"] is None
    assert raw["bounds"]["computed"] == list(range(2, 10))
    assert raw["checkpoint"]["resumed"] == 2 and raw["checkpoint"]["saved"] == 8


def test_a_killed_run_resumes_where_it_stopped(tmp_path):
    a = toy(tmp_path, delay=0.3)
    ckpt = checkpoint.path_for(a, root=tmp_path)
    env = {**os.environ, "PYTHONPATH": str(ROOT)}
    cmd = [sys.executable, str(ROOT / "_runner.py"), str(a), str(tmp_path / "raw.json"), "inf"]
    p = subprocess.Popen(cmd, cwd=ROOT, env=env)
    deadline = time.time() + 30
    while len(checkpoint.load(ckpt)) < 3 and time.time() < deadline:
        time.sleep(0.05)
    p.kill()
    p.wait()
    kept = checkpoint.load(ckpt)
    assert 3 <= len(kept) < 10 and not (tmp_path / "raw.json").exists()
    subprocess.run(cmd, cwd=ROOT, env=env, check=True)
    raw = json.loads((tmp_path / "raw.json").read_text())
    assert raw["bounds"]["computed"] == [i for i in range(10) if f"unit-{i}" not in kept]
    assert checkpoint.load(ckpt) == {f"unit-{i}": i * i for i in range(10)}


def test_a_stopped_run_takes_back_its_folder(tmp_path, monkeypatch):
    monkeypatch.setattr(run_experiment, "EXPERIMENTS", tmp_path)
    (tmp_path / "0007-done").mkdir()
    (tmp_path / "0007-done" / "attack.py").write_bytes(b"same")
    (tmp_path / "0007-done" / "result.json").write_text("{}")
    (tmp_path / "0008-stopped").mkdir()
    (tmp_path / "0008-stopped" / "attack.py").write_bytes(b"same")
    assert run_experiment.unfinished_folder(b"same").name == "0008-stopped"
    assert run_experiment.unfinished_folder(b"other") is None


# A process that starts a grandchild and writes its pid, then waits: what a search with workers looks like.
TREE = ("import subprocess, sys, time; c = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)']); "
        "open(sys.argv[1], 'w').write(str(c.pid)); time.sleep(60)")


def alive(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    # a zombie still answers kill 0; ask ps for its state
    state = subprocess.run(["ps", "-o", "stat=", "-p", str(pid)], capture_output=True, text=True).stdout.strip()
    return bool(state) and not state.startswith("Z")


def wait_for(f):
    deadline = time.time() + 20
    while not (f.exists() and f.read_text()) and time.time() < deadline:
        time.sleep(0.05)
    return int(f.read_text())


def test_a_timeout_ends_the_whole_tree(tmp_path):
    f = tmp_path / "pid"
    with pytest.raises(subprocess.TimeoutExpired):
        run_experiment.run_child([sys.executable, "-c", TREE, str(f)], timeout=3)
    grandchild = wait_for(f)
    time.sleep(0.5)
    assert not alive(grandchild)


def test_stopping_the_harness_ends_the_whole_tree(tmp_path):
    """What tools/stop_experiment.sh does: SIGTERM to the harness reaches every process of the search (#104)."""
    f = tmp_path / "pid"
    harness = textwrap.dedent(f'''
        import signal, sys
        sys.path.insert(0, {str(ROOT)!r})
        import run_experiment
        signal.signal(signal.SIGTERM, run_experiment._stop)
        run_experiment.run_child([sys.executable, "-c", {TREE!r}, {str(f)!r}])
    ''')
    h = subprocess.Popen([sys.executable, "-c", harness], cwd=ROOT)
    grandchild = wait_for(f)
    h.send_signal(signal.SIGTERM)
    assert h.wait(timeout=30) == 128 + signal.SIGTERM
    time.sleep(0.5)
    assert not alive(grandchild)
