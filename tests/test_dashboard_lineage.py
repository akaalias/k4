"""The lineage page is built from the records: one node per experiment, edges from `parent`,
one lane per family number, linked from the nav and the overview."""
import json
import re

import dashboard


def _data(html):
    m = re.search(r'<script id="lin-data" type="application/json">(.+?)</script>', html, re.S)
    return json.loads(m.group(1))


def test_lineage_has_every_experiment_and_parent():
    rows = dashboard.load_results()
    html = dashboard.route("/lineage")
    data = _data(html)
    assert [n["key"] for n in data["nodes"]] == [r["tag"] for r in rows]
    by_key = {n["key"]: n for n in data["nodes"]}
    for r in rows:
        assert by_key[r["tag"]]["parent"] == r["parent"]
        assert by_key[r["tag"]]["decision"] == r["decision"]


def test_one_lane_per_family_number():
    data = dashboard.lineage_data(dashboard.load_results())
    labels = [f["label"].split(" ", 1)[0] for f in data["families"]]
    assert len(labels) == len(set(labels))
    assert sum(f["count"] for f in data["families"]) == len(data["nodes"])
    assert all(0 <= n["fam"] < len(data["families"]) for n in data["nodes"])


def test_lineage_is_linked():
    assert 'href="/lineage"' in dashboard.route("/")
    assert 'href="/lineage" class="on"' in dashboard.route("/lineage")

