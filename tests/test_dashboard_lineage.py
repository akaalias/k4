"""The lineage page is built from the records: one node per experiment, edges from `parent`,
one column per family number, linked from the nav and the overview."""
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
    tags = {r["tag"] for r in rows}
    by_num = {r["tag"][:4]: r["tag"] for r in rows}
    for r in rows:
        # a parent named by a slug its tag no longer carries is matched by number (#63)
        p = r["parent"]
        want = p if p in tags else by_num.get(p[:4]) if p else None
        assert by_key[r["tag"]]["parent"] == (want if want != r["tag"] else None)
        assert by_key[r["tag"]]["decision"] == r["decision"]


def test_renamed_parent_resolves_by_number():
    rows = dashboard.load_results()
    renamed = [r for r in rows if r["parent"] and r["parent"] not in {x["tag"] for x in rows}]
    assert renamed, "no record names its parent by an old slug; drop this test"
    par = dashboard.parent_tags(rows)
    for r in renamed:
        assert par[r["tag"]][:4] == r["parent"][:4]


def test_one_column_per_family_number():
    data = dashboard.lineage_data(dashboard.load_results())
    labels = [f["label"].split(" ", 1)[0] for f in data["families"]]
    assert len(labels) == len(set(labels))
    assert sum(f["count"] for f in data["families"]) == len(data["nodes"])
    assert all(0 <= n["fam"] < len(data["families"]) for n in data["nodes"])


def test_lineage_is_linked():
    assert 'href="/lineage"' in dashboard.route("/")
    assert 'href="/lineage" class="on"' in dashboard.route("/lineage")

