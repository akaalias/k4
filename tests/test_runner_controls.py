"""The runner must pass the attack's shuffled-copper controls on to the gates (issue #45)."""
import json

import _runner

ATTACK = '''
def run(ctx):
    return {"candidates": [], "bounds": {}, "notes": "", "controls": [-5.1, -5.2, "x", None, -4.9]}
def encrypt(pt, key):
    return pt
def worked_example(ctx, key):
    return ""
'''


def test_controls_reach_the_record(tmp_path):
    attack = tmp_path / "attack.py"
    attack.write_text(ATTACK)
    out = tmp_path / "raw.json"
    _runner.main(str(attack), str(out), 30)
    assert json.loads(out.read_text())["controls"] == [-5.1, -5.2, -4.9]
