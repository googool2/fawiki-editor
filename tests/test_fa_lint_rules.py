"""Behaviour of individual fa_lint rules."""

import pytest

from fa_lint import RULES, lint

Z = "‌"

CASES = [
    ("FA01", "ايران", "ایران"),
    ("FA01", "موسى", "موسی"),
    ("FA02", "كتاب", "کتاب"),
    ("FA03", "سال ١٣٩٩", "سال ۱۳۹۹"),
    ("FA04", "در سال 1990 میلادی", "در سال ۱۹۹۰ میلادی"),
    ("FA06", "۵۰% مردم", "۵۰٪ مردم"),
    ("FA05", "ایـــران", "ایران"),
    ("FA10", f"می{Z}{Z}رود", f"می{Z}رود"),
    ("FA11", f"کتاب {Z}ها", "کتاب ها"),
    ("FA12", f"در{Z}ها", "درها"),
    ("FA20", "او می رود", f"او می{Z}رود"),
    ("FA20", "نمی دانم", f"نمی{Z}دانم"),
    ("FA21", "کتاب ها", f"کتاب{Z}ها"),
    ("FA21", "خانه های", f"خانه{Z}های"),
    ("FA21", "درها و در ها", "درها و درها"),
    ("FA22", "بزرگ ترین", f"بزرگ{Z}ترین"),
    ("FA23", "خانه ای", f"خانه{Z}ای"),
    ("FA23", "رفته اند", f"رفته{Z}اند"),
    ("FA30", "تهران,اصفهان", "تهران، اصفهان"),
    ("FA31", "تهران; اصفهان", "تهران؛ اصفهان"),
    ("FA32", "چرا?", "چرا؟"),
    ("FA33", "او گفت “سلام” و رفت", "او گفت «سلام» و رفت"),
    ("FA22", "بیش ترین", "بیشترین"),
    ("FA07", "۳.۵ درصد", "۳٫۵ درصد"),
    ("FA08", "۱,۰۰۰ نفر", "۱٬۰۰۰ نفر"),
    ("FA14", "خانۀ من", "خانهٔ من"),
    ("FA14", "خانهء من", "خانهٔ من"),
    ("FA15", "خانه‌ی من", "خانهٔ من"),
    ("FA16", "خانه‌یی", "خانه‌ای"),
    ("FA20", "میخواهد", f"می{Z}خواهد"),
    ("FA20", "نمیتوان", f"نمی{Z}توان"),
    ("FA23", "خسته ام", f"خسته{Z}ام"),
    ("FA50", "این مساله و آنرا", "این مسئله و آن را"),
    ("FA00", "\ufeb3\ufefc\ufee1", "سلام"),
    ("FA09", "متن\ufeff", "متن"),
    ("FA40", "قرار دارد .", "قرار دارد."),
    ("FA40", "تهران ، اصفهان", "تهران، اصفهان"),
    ("FA41", "( متن)", "(متن)"),
    ("FA42", "است.او", "است. او"),
    ("FA43", "دو  فاصله", "دو فاصله"),
    ("FA44", "پایان   ", "پایان"),
]


@pytest.mark.parametrize("rule,before,after", CASES)
def test_rule(rule, before, after):
    res = lint(before, enabled={rule})
    assert res.fixed == after
    assert {c.rule for c in res.changes} == {rule}


@pytest.mark.parametrize("text", ["Windows 10 و iPhone 15", "حجم 10 GB است"])
def test_digits_next_to_latin_words_are_kept(text):
    assert lint(text, enabled={"FA04"}).fixed == text


@pytest.mark.parametrize("text", [
    "COVID-19", "B-52", "MP3", "H2O", "user_123", "a=1",
])
def test_digits_inside_latin_tokens_are_kept(text):
    assert lint(text, enabled={"FA04"}).fixed == text


@pytest.mark.parametrize("text", [
    "میز بزرگ", "میوه ها", "میان دو", "میلیون نفر", "میزان", "میدان", "میلاد",  # not verbs
    "جام می ناب",                                    # «می» = wine, no verb stem follows
    "کتابها",                                       # attached plural is allowed
    "1,000",                                          # comma between digits
    "English, text; here?",                          # Latin punctuation in Latin text
])
def test_no_false_positive(text):
    res = lint(text, enabled={"FA20", "FA30", "FA31", "FA32"})
    assert res.fixed == text


def test_idempotent():
    text = "اين كتاب ها را می خوانم , ولی 12 سال طول کشید ."
    once = lint(text).fixed
    assert lint(once).fixed == once
    assert lint(once).changes == []


def test_newlines_preserved():
    text = "خط ي\n\nخط ك\n"
    out = lint(text).fixed
    assert out.count("\n") == text.count("\n")


def test_line_numbers_reported():
    res = lint("خط اول\n{{الگو\n|a=1\n}}\nكتاب")
    assert [c.line for c in res.changes] == [5]


def test_warning_for_arabic_letters_inside_links():
    res = lint("[[كتاب]] متن")
    assert any(w["rule"] == "FW01" for w in res.warnings)
    assert res.fixed == "[[كتاب]] متن"


def test_rule_ids_unique():
    ids = [r.id for r in RULES]
    assert len(ids) == len(set(ids))
