"""Fast rule test: one wrong→right pair per auto-fix rule, plus must-not-change cases.

Run: python -m pytest -q bench/test_rules.py   (or python bench/test_rules.py)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "fawiki-editor" / "scripts"))

from fa_lint import RULE_IDS, lint  # noqa: E402

Z = "‌"
PAIRS = {
    "FA00": ("ﺳﻼﻡ", "سلام"), "FA01": ("ايران", "ایران"), "FA02": ("كتاب", "کتاب"),
    "FA03": ("١٣٩٩", "۱۳۹۹"), "FA04": ("سال 1990", "سال ۱۹۹۰"), "FA05": ("ایـران", "ایران"),
    "FA06": ("۵۰%", "۵۰٪"), "FA07": ("۳.۵ متر", "۳٫۵ متر"), "FA08": ("۱,۰۰۰ نفر", "۱٬۰۰۰ نفر"),
    "FA09": ("متن﻿", "متن"), "FA10": (f"می{Z}{Z}رود", f"می{Z}رود"), "FA11": (f"کتاب {Z}ها", "کتاب ها"),
    "FA12": (f"در{Z}ها", "درها"), "FA13": (f"{Z}کتاب", "کتاب"), "FA14": ("خانۀ من", "خانهٔ من"),
    "FA15": (f"خانه{Z}ی من", "خانهٔ من"), "FA16": (f"خانه{Z}یی", f"خانه{Z}ای"), "FA20": ("می رود", f"می{Z}رود"),
    "FA21": ("کتاب ها", f"کتاب{Z}ها"), "FA22": ("بزرگ ترین", f"بزرگ{Z}ترین"), "FA23": ("رفته اند", f"رفته{Z}اند"),
    "FA30": ("الف,ب", "الف، ب"), "FA31": ("الف;ب", "الف؛ ب"), "FA32": ("چرا?", "چرا؟"),
    "FA33": ("“سلام”", "«سلام»"), "FA40": ("است .", "است."), "FA41": ("( متن)", "(متن)"),
    "FA42": ("است.او", "است. او"), "FA43": ("دو  فاصله", "دو فاصله"), "FA44": ("پایان  ", "پایان"),
    "FA50": ("مساله", "مسئله"),
}
UNCHANGED = ["میز", "میلاد", "جام می ناب", "کتابها", "Windows 10", "COVID-19", "{{الگو|ي 12}}",
             "[[كتاب ها]]", "<ref>ي 12</ref>", "https://x.org/a?b=1,2", "ISBN 978-3-16-148410-0", "بیشترین"]


def test_every_rule_has_a_pair():
    assert set(PAIRS) == RULE_IDS


def test_pairs():
    for rule, (wrong, right) in PAIRS.items():
        assert lint(wrong, {rule}).fixed == right, rule


def test_unchanged():
    for text in UNCHANGED:
        assert lint(text).fixed == text, text


if __name__ == "__main__":
    test_every_rule_has_a_pair()
    test_pairs()
    test_unchanged()
    print(f"ok: {len(PAIRS)} rules, {len(UNCHANGED)} must-not-change cases")
