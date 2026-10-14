from kryptos.facts import K4, KNOWN, CRIBS
from kryptos.gates import run_gates, crib_hits
from kryptos.cribsweep import sweep


def test_cribs_sit_where_sanborn_said():
    assert K4[21:34] == "FLRVQQPRNGKSS"
    assert K4[63:74] == "NYPVTTMZFPK"
    assert len(KNOWN) == 24


def test_ciphertext_itself_fails_crib_gate():
    r = run_gates(K4, K4)
    assert not r.passed and r.failed_at == "cribs"
    # two letters encrypt to themselves: S at 33 and K at 74
    assert r.crib_hits == 2


def test_crib_gate_passes_only_with_all_24():
    pt = list("A" * 97)
    for pos, ch in KNOWN.items():
        pt[pos - 1] = ch
    pt = "".join(pt)
    assert crib_hits(pt) == 24
    r = run_gates(pt, None)
    assert not r.passed and r.failed_at == "reencryption_missing"
    r = run_gates(pt, K4)
    assert r.passed
    r = run_gates(pt, K4[:-1] + "Z")
    assert not r.passed and r.failed_at == "reencryption"


def test_length_and_alphabet_gates():
    assert run_gates("ABC", None).failed_at == "length"
    assert run_gates("a" * 97, None).failed_at == "alphabet"


def test_periodic_additive_periods_excluded():
    """Single-alphabet periodic additive ciphers survive only at 27, 28, 29 and 53+."""
    expected = [27, 28, 29] + list(range(53, 98))
    for key, periods in sweep().items():
        assert periods == expected, key
