"""The public site holds back a kept result or a champion until it is listed in data/confirmed.json
(issue #95). The local dashboard shows everything."""
import json

import dashboard

TAG = "0224-a6-replicate-0034-at-27-29-under-the-judge"   # recorded as kept, reverted by the replay


def _root(tmp_path, monkeypatch, confirmed):
    """A root with a champion naming TAG, no replay (so the recorded 'kept' stands) and a confirmed list."""
    (tmp_path / "data").mkdir()
    (tmp_path / "champion.json").write_text(json.dumps({"experiment": TAG, "loss": 4.6, "plaintext": "A" * 97, "key": {}}))
    (tmp_path / "data" / "confirmed.json").write_text(json.dumps({"confirmed": [{"experiment": t} for t in confirmed]}))
    monkeypatch.setattr(dashboard, "ROOT", tmp_path)


def test_public_site_holds_back_an_unconfirmed_champion(tmp_path, monkeypatch):
    _root(tmp_path, monkeypatch, [])
    monkeypatch.setattr(dashboard, "EXPORT", {"base": "/k4", "date": "test"})
    assert dashboard.champion() is None
    row = next(r for r in dashboard.load_results() if r["tag"] == TAG)
    assert row["decision"] == "awaiting review"


def test_public_site_shows_a_confirmed_champion(tmp_path, monkeypatch):
    _root(tmp_path, monkeypatch, [TAG])
    monkeypatch.setattr(dashboard, "EXPORT", {"base": "/k4", "date": "test"})
    assert dashboard.champion()["experiment"] == TAG
    row = next(r for r in dashboard.load_results() if r["tag"] == TAG)
    assert row["decision"] == "kept"


def test_local_dashboard_shows_everything(tmp_path, monkeypatch):
    _root(tmp_path, monkeypatch, [])
    monkeypatch.setattr(dashboard, "EXPORT", {})
    assert dashboard.champion()["experiment"] == TAG
    row = next(r for r in dashboard.load_results() if r["tag"] == TAG)
    assert row["decision"] == "kept"
