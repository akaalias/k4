"""Where experiments compute (issue #99): data/compute.json picks Modal or the laptop; when Modal cannot run a
search, run_experiment.py runs it locally with every Pool capped at K4_MAX_WORKERS."""
import importlib.util
import json
import multiprocessing as mp
import multiprocessing.context
from pathlib import Path

import pytest

import _runner
import run_experiment

ROOT = Path(__file__).resolve().parent.parent


def test_compute_defaults_to_the_laptop(tmp_path, monkeypatch):
    monkeypatch.setattr(run_experiment, "COMPUTE", tmp_path / "compute.json")
    assert run_experiment.compute_where() == "local"
    (tmp_path / "compute.json").write_text(json.dumps({"where": "modal"}))
    assert run_experiment.compute_where() == "modal"


def test_worker_cap_limits_every_pool(monkeypatch):
    monkeypatch.setattr(multiprocessing.context.BaseContext, "Pool", multiprocessing.context.BaseContext.Pool)
    monkeypatch.setenv("K4_MAX_WORKERS", "4")
    assert _runner._cap_workers() == 4
    with mp.get_context("fork").Pool(8) as pool:
        assert pool._processes == 4
        assert pool.map(abs, [-1, -2]) == [1, 2]


def test_no_cap_without_the_variable(monkeypatch):
    monkeypatch.delenv("K4_MAX_WORKERS", raising=False)
    assert _runner._cap_workers() is None


def test_modal_failure_hands_the_run_back(tmp_path, monkeypatch):
    pytest.importorskip("modal")
    spec = importlib.util.spec_from_file_location("remote_run", ROOT / "tools" / "remote_run.py")
    rr = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rr)

    def broken():
        raise RuntimeError("billing limit reached")
    monkeypatch.setattr(rr.app, "run", broken)
    monkeypatch.setattr(rr, "MARKER", tmp_path / "remote-run.json")
    assert rr.main(str(ROOT / "attack.py"), str(tmp_path / "raw.json"), "inf") == rr.UNAVAILABLE
    assert not (tmp_path / "raw.json").exists()


def test_forced_worker_count_overrides_the_attack(monkeypatch):
    monkeypatch.setattr(multiprocessing.context.BaseContext, "Pool", multiprocessing.context.BaseContext.Pool)
    monkeypatch.delenv("K4_MAX_WORKERS", raising=False)
    monkeypatch.setenv("K4_WORKERS", "3")
    assert _runner._cap_workers() == 3
    with mp.get_context("fork").Pool(8) as pool:
        assert pool._processes == 3


def test_silent_modal_hands_the_run_back(tmp_path):
    """A Modal run that goes quiet (no heartbeat) must not hang the loop: the laptop takes it back."""
    pytest.importorskip("modal")
    import subprocess
    import sys
    script = f"""
import contextlib, importlib.util, sys, time
from pathlib import Path
spec = importlib.util.spec_from_file_location("remote_run", {str(ROOT / "tools" / "remote_run.py")!r})
rr = importlib.util.module_from_spec(spec); spec.loader.exec_module(rr)
rr.SILENCE = 1
rr.MARKER = Path({str(tmp_path)!r}) / "remote-run.json"
class FakeApp:
    app_id = "test"
    def run(self): return contextlib.nullcontext()
rr.app = FakeApp()
rr.modal.enable_output = lambda: contextlib.nullcontext()
class Hang:
    def remote_gen(self, *a):
        time.sleep(120); yield {{}}
rr.search = Hang()
sys.exit(rr.main({str(ROOT / "attack.py")!r}, {str(tmp_path / "raw.json")!r}, "inf"))
"""
    r = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True, timeout=90)
    assert r.returncode == 75, r.stdout + r.stderr
    assert "no word from Modal" in r.stdout


def _aws_run():
    spec = importlib.util.spec_from_file_location("aws_run", ROOT / "tools" / "aws_run.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_aws_is_a_compute_place(tmp_path, monkeypatch):
    monkeypatch.setattr(run_experiment, "COMPUTE", tmp_path / "compute.json")
    (tmp_path / "compute.json").write_text(json.dumps({"where": "aws"}))
    assert run_experiment.compute_where() == "aws"
    assert "aws_run.py" in run_experiment.REMOTE["aws"][1][-1]


def test_aws_package_ships_no_secrets_or_large_folders():
    """The machine gets the code, never .env, .git or the large folders (issue #115)."""
    import io
    import tarfile
    names = tarfile.open(fileobj=io.BytesIO(_aws_run().package_code())).getnames()
    tops = {n.split("/")[1] for n in names if n.count("/") >= 1}
    assert {"kryptos", "tools", "experiments", "_runner.py", "uv.lock"} <= tops
    assert not tops & {".env", ".git", ".venv", "transcripts", "logs", "figures", "Kryptos Blender Model"}
    assert not any("__pycache__" in n for n in names)


def test_aws_budget_reached_hands_the_run_back(tmp_path, monkeypatch):
    rr = _aws_run()
    monkeypatch.setattr(rr, "env_file", lambda: {"AWS_ACCESS_KEY_ID": "x", "AWS_SECRET_ACCESS_KEY": "y"})
    monkeypatch.setattr(rr, "setting", lambda: {"where": "aws", "budget_dollars": 10})
    monkeypatch.setattr(rr, "spend_this_month", lambda where="aws": 10.5)
    assert rr.main(str(ROOT / "attack.py"), str(tmp_path / "raw.json"), "inf") == rr.UNAVAILABLE
    assert not (tmp_path / "raw.json").exists()


def test_aws_without_credentials_hands_the_run_back(tmp_path, monkeypatch):
    rr = _aws_run()
    monkeypatch.setattr(rr, "env_file", lambda: {})
    monkeypatch.delenv("AWS_ACCESS_KEY_ID", raising=False)
    assert rr.main(str(ROOT / "attack.py"), str(tmp_path / "raw.json"), "inf") == rr.UNAVAILABLE


def test_aws_boot_script_fits_and_shuts_down_first():
    rr = _aws_run()
    urls = {k: "https://example.com/" + "x" * 1500 for k in ("code", "secret", "status", "checkpoint", "log", "result")}
    s = rr.boot_script(urls, 1440)
    assert s.splitlines()[2].startswith("shutdown -h +1440")
    assert len(s.encode()) < 16000
