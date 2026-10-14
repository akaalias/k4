"""Every cipher primitive must reproduce the solved sections before it is trusted on K4."""
from kryptos.facts import load_k1, load_k2, load_k3, KRYPTOS_ALPHABET, STANDARD_ALPHABET
from kryptos.ciphers import (
    keyed_vigenere_encrypt, keyed_vigenere_decrypt, tableau_rows,
    columnar_transposition_encrypt, columnar_transposition_decrypt,
    k3_formula_decrypt, k3_formula_encrypt,
)


def test_k1_decrypts_with_palimpsest():
    k1 = load_k1()
    assert keyed_vigenere_decrypt(k1["ciphertext"], k1["key"]) == k1["plaintext"]
    assert keyed_vigenere_encrypt(k1["plaintext"], k1["key"]) == k1["ciphertext"]


def test_k1_keyword_slip_gives_same_ciphertext_for_iqlusion_only():
    """Sanborn's chart has PALIMPCEST over a correctly spelled ILLUSION; the copper
    reads IQLUSION under PALIMPSEST. Both give MKYRDMFD for that word at offset 55.
    But PALIMPCEST used throughout would change five other letters, so the slip,
    if it was one, affected only the letter under the C."""
    k1 = load_k1()
    offset = k1["plaintext"].index("IQLUSION")
    assert offset == 55
    tail_correct = keyed_vigenere_encrypt("ILLUSION", "PALIMPCEST"[offset % 10:] + "PALIMPCEST"[: offset % 10])
    tail_carved = keyed_vigenere_encrypt("IQLUSION", "PALIMPSEST"[offset % 10:] + "PALIMPSEST"[: offset % 10])
    assert tail_correct == tail_carved == k1["ciphertext"][offset:]
    whole = k1["plaintext"].replace("IQLUSION", "ILLUSION")
    diffs = sum(a != b for a, b in zip(keyed_vigenere_encrypt(whole, "PALIMPCEST"), k1["ciphertext"]))
    assert diffs == 5


def test_k2_as_carved_decrypts_to_idbyrows():
    k2 = load_k2()
    pt = keyed_vigenere_decrypt(k2["ciphertext_as_carved"], k2["key"])
    assert pt == k2["plaintext_as_carved"]
    assert pt.endswith("WESTIDBYROWS")
    assert "UNDERGRUUND" in pt
    assert pt.count("?") == 3


def test_k2_corrected_decrypts_to_layertwo():
    k2 = load_k2()
    pt = keyed_vigenere_decrypt(k2["ciphertext_corrected"], k2["key"])
    assert pt.endswith(k2["plaintext_corrected_ending"])
    assert pt[: len(k2["plaintext_as_carved"]) - 12] == k2["plaintext_as_carved"][:-12]


def test_k2_roundtrip():
    k2 = load_k2()
    assert keyed_vigenere_encrypt(k2["plaintext_as_carved"], k2["key"]) == k2["ciphertext_as_carved"]


def test_k3_formula():
    k3 = load_k3()
    f = k3["formula"]
    assert len(k3["ciphertext"]) == f["n"] == 337
    assert k3_formula_decrypt(k3["ciphertext"], f["a"], f["b"]) == k3["plaintext"]
    assert k3_formula_encrypt(k3["plaintext"], f["a"], f["b"]) == k3["ciphertext"]
    assert "DESPARATLY" in k3["plaintext"]


def test_tableau_shape():
    rows = tableau_rows()
    assert len(rows) == 26
    assert all(len(r) == 30 for r in rows)
    assert rows[0].startswith(KRYPTOS_ALPHABET)
    carved = tableau_rows(carved=True)
    n_row = carved[STANDARD_ALPHABET.index("N")]
    assert len(n_row) == 31 and n_row.endswith("L")
    assert sum(len(r) for r in carved) == 26 * 30 + 1


def test_tableau_hill_column():
    """Rows L, M, N, O: last letter of each reads H, I, L, L on the carved tableau."""
    carved = tableau_rows(carved=True)
    col = "".join(carved[STANDARD_ALPHABET.index(r)][-1] for r in "LMNO")
    assert col == "HILL"


def test_columnar_roundtrip():
    pt = "WECANSEEWONDERFULTHINGS"
    order = [3, 0, 4, 1, 2]
    ct = columnar_transposition_encrypt(pt, order)
    assert len(ct) == len(pt)
    assert columnar_transposition_decrypt(ct, order) == pt
