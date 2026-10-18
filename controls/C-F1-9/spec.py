"""Positive control for F1/9 (issue #73): a running key from an unknown English text (0009).
0009 scored the key stretches forced at 22-34 and 64-74 as English under 24 conventions, on the copper as
carved and with one letter in or out, against English and random calibrations; on the plant the best stretch
on the exact copper must be the planted key and read as English (within 2 sd of English windows)."""
from kryptos.plants import english_plant, _letters

ITEM = "F1/9"
EXPERIMENT = "0009"
WHAT = "Running key from another passage of Carter (offset 150,000), plain standard / cipher standard / key standard, Vigenere, on English from Carter"
OFF = 150000


def plant():
    key = _letters()[OFF:OFF + 97]
    return {"plaintext": english_plant(7341), "key": {"pa": "std", "ca": "std", "ka": "std", "m": "vig", "key": key}}


def found(result, plant):
    b = result.get("bounds", {})
    best = b.get("best_exact_copper", {})
    k = plant["key"]["key"]
    planted = {k[21:34], k[63:74]}
    ok = best.get("stretch") in planted and best.get("z_vs_english", -99) >= -2
    return ok, f"best exact stretch {best.get('stretch')} ({best.get('convention')}, z vs English {best.get('z_vs_english')}); planted {sorted(planted)}"
