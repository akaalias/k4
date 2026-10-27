"""ctx.progress writes the running experiment's progress for the loop's terminal bar (issue #97)."""
import json

import _runner


def test_progress_writes_and_throttles(tmp_path, monkeypatch):
    f = tmp_path / "experiment-progress.json"
    monkeypatch.setattr(_runner, "PROGRESS", f)
    monkeypatch.setattr(_runner, "_last_write", [0.0])
    _runner._progress(3, 10, "copies")
    assert json.loads(f.read_text())["done"] == 3
    _runner._progress(4, 10, "copies")            # within a second: skipped
    assert json.loads(f.read_text())["done"] == 3
    _runner._progress(10, 10, "copies")           # the end is always written
    assert json.loads(f.read_text())["done"] == 10
