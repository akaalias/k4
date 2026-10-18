"""Positive control for F1/9 (issue #73): a running key from an unknown English text on vocabulary alphabets (0010).
0010 scored the forced key stretches as English over 63 x 63 plain/cipher alphabets, 248 key alphabets and three
modes (5.9 million stretches), against the same search on three shuffled coppers; the planted key stretch must be
the best overall and score above every shuffled copy's best, which is how a real key would have shown."""
from kryptos.alphabets import keyword_mixed
from kryptos.facts import STANDARD_ALPHABET as STD
from kryptos.plants import english_plant, _letters

ITEM = "F1/9"
EXPERIMENT = "0010"
WHAT = "Running key from another passage of Carter (offset 150,000), plain SHADOW-mixed, cipher standard, key standard, Vigenere, on English from Carter"
OFF = 150000


def plant():
    key = _letters()[OFF:OFF + 97]
    return {"plaintext": english_plant(7342), "key": {"pa": keyword_mixed("SHADOW"), "ca": STD, "ka": STD, "m": "vig", "key": key}}


def found(result, plant):
    b = result.get("bounds", {})
    best = b.get("best_overall", {})
    k = plant["key"]["key"]
    planted = {k[21:34], k[63:74]}
    tops = [r for r in b.get("top_twenty", []) if r["stretch"] in planted]
    nulls = [s for s, _ in b.get("null_control_best", [])]
    ok = best.get("stretch") in planted and nulls and best.get("score", -99) > max(nulls)
    rank = next((i + 1 for i, r in enumerate(b.get("top_twenty", [])) if r["stretch"] in planted), None)
    return ok, (f"best overall {best.get('stretch')} {best.get('score')}; planted {sorted(planted)} ranked {rank} of the top 20"
                f"{' at ' + str(tops[0]['score']) if tops else ''}; shuffled copies' best {nulls}")
