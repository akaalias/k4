"""The blind judge's local parts (issue #76): no API calls here."""
from kryptos import judge
from kryptos.facts import K4, KNOWN


def test_mask_hides_every_known_place_and_keeps_unknowns():
    text = "?" * 5 + K4[5:]
    m = judge.mask(text)
    assert len(m) == 97
    assert all(m[q - 1] == "#" for q in KNOWN)
    assert m[:5] == "?????"
    assert "EASTNORTHEAST" not in m and "BERLINCLOCK" not in m


def test_mask_turns_stray_characters_into_unknowns():
    assert judge.mask("ab1-")[:4] == "AB??"


def test_parse_reads_json_inside_prose_and_clamps():
    assert judge._parse('Here: {"reading": "THE END", "score": 140}') == {"reading": "THE END", "score": 100}
    assert judge._parse('{"reading": "", "score": "7.6"}')["score"] == 8


def test_cache_key_depends_on_model_and_prompt():
    a = judge._key("ABC")
    old = judge.MODEL
    try:
        judge.MODEL = "other-model"
        assert judge._key("ABC") != a
    finally:
        judge.MODEL = old
