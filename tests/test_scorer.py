"""Calibration: the true K1-K3 plaintexts must beat their own ciphertexts
by a clear margin even after paying for their keys."""
from kryptos.facts import load_k1, load_k2, load_k3, K4
from kryptos.scorer import english_score, fitness, key_bits_for_words, free_text


def letters(s):
    return "".join(c for c in s if "A" <= c <= "Z")


def test_english_beats_ciphertext_k1_k2_k3():
    for loader, keyname in ((load_k1, "key"), (load_k2, "key"), (load_k3, None)):
        d = loader()
        pt = letters(d.get("plaintext") or d["plaintext_as_carved"])
        ct = letters(d.get("ciphertext") or d["ciphertext_as_carved"])
        e_pt, e_ct = english_score(pt), english_score(ct)
        assert e_pt > e_ct + 1.5, (e_pt, e_ct)
        # pay for the key (KRYPTOS alphabet + keyword) at the same per-letter rate as K4
        key_bits = key_bits_for_words("KRYPTOS", d[keyname]) if keyname else key_bits_for_words("KRYPTOS")
        assert e_pt - key_bits / len(pt) > e_ct, (e_pt, key_bits, e_ct)


def test_k4_free_text_is_73_letters():
    assert len(free_text(K4)) == 73


def test_fitness_penalises_long_keys():
    k1 = load_k1()
    pt = k1["plaintext"]
    pt97 = (pt * 2)[:97]
    short = fitness(pt97, key_bits_for_words("PALIMPSEST"))
    long = fitness(pt97, key_bits_for_words(pt97))
    assert short > long
    assert long < english_score(K4)  # a message-length key is worse than raw ciphertext


def test_loss_is_lexicographic():
    from kryptos.scorer import loss
    from kryptos.facts import KNOWN
    k1 = load_k1()
    pt = (letters(k1["plaintext"]) * 2)[:97]
    # a fully English text missing all cribs must lose to a crib-perfect text of junk
    junk = list("Q" * 97)
    for pos, ch in KNOWN.items():
        junk[pos - 1] = ch
    junk = "".join(junk)
    hits_pt = sum(1 for p, c in KNOWN.items() if pt[p - 1] == c)
    assert loss(junk, 47.0, 24) < loss(pt, 47.0, hits_pt)
    assert loss(junk, 47.0, 24) < 10.0
    assert loss(pt, 47.0, hits_pt) >= 10.0 * (24 - hits_pt)
