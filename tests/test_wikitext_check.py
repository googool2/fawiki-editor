"""Structural checks."""

import pytest

from wikitext_check import check, main

LEAD = "'''عنوان''' متن.<ref>منبع</ref>\n== منابع ==\n{{پانویس}}\n[[رده:آزمایش]]\n"


def codes(text, sev=None):
    return {i.code for i in check(text) if sev is None or i.severity == sev}


def test_clean_article_has_no_errors():
    assert codes(LEAD, "E") == set()


@pytest.mark.parametrize("text,code", [
    ("'''ع''' [[پیوند\n[[رده:x]]", "WC01"),
    ("'''ع''' پیوند]]\n[[رده:x]]", "WC01"),
    ("'''ع''' {{الگو\n[[رده:x]]", "WC02"),
    ("'''ع''' <ref>بی‌پایان\n[[رده:x]]", "WC03"),
    ("'''ع''' </ref>\n[[رده:x]]", "WC03"),
    ("'''ع''' متن<ref>x</ref>\n[[رده:x]]", "WC04"),
    ("'''ع''' متن", "WC05"),
    ("عنوان بدون بولد\n[[رده:x]]", "WC06"),
])
def test_errors(text, code):
    assert code in codes(text, "E")


@pytest.mark.parametrize("text,code", [
    (LEAD + "{{الگوی ساختگی ناموجود}}", "WC07"),
    (LEAD + "{{Cite web|url=x}}", "WC08"),
    (LEAD + "== References ==", "WC09"),
    (LEAD + "== همچنین ببینید ==", "WC09"),
    (LEAD + "[[Category:X]]", "WC10"),
    (LEAD + "=== پرش ===\n===== پرش بیشتر =====", "WC11"),
    (LEAD + "== نامتوازن ===", "WC12"),
    ("'''ع''' <ref>https://example.com</ref>\n{{پانویس}}\n[[رده:x]]", "WC13"),
    (LEAD + "{{مدرک}}", "WC14"),
    ("'''ع''' <ref name=\"a\">x</ref><ref name=\"a\">y</ref>\n{{پانویس}}\n[[رده:x]]", "WC15"),
    (LEAD + " خط با فاصلهٔ آغازین", "WC16"),
    ("'''ع''' متن\n[[رده:x]]", "WC17"),
    (LEAD + "[[en:Foo]]", "WC18"),
    (LEAD + "[[پرونده:مثال.jpg]]", "WC19"),
    (LEAD + "{{جعبه اطلاعات شهر ایران}}", "WC20"),
    (LEAD + "[[پرونده:a.jpg|thumb|متن]]", "WC20"),
])
def test_warnings(text, code):
    assert code in codes(text)


def test_brackets_inside_nowiki_and_comments_ignored():
    text = LEAD + "<nowiki>[[ {{</nowiki> <!-- ]] }} -->"
    assert codes(text, "E") == set()


def test_bold_title_after_infobox_and_image():
    text = ("{{جعبه اطلاعات زندگی‌نامه\n| نام = x\n| زادروز = {{تاریخ تولد و سن|1990|1|1}}\n}}\n"
            "[[پرونده:a.jpg|بندانگشتی|عکس]]\n'''فلانی''' متن.<ref>x</ref>\n{{پانویس}}\n[[رده:x]]")
    assert "WC06" not in codes(text)


def test_redirect_skips_article_checks():
    assert codes("#تغییرمسیر [[کوه دماوند]]", "E") == set()


def test_disambiguation_page_needs_no_bold():
    assert "WC06" not in codes("دماوند ممکن است به موارد زیر اشاره کند:\n{{ابهام‌زدایی}}\n[[رده:x]]")


def test_exit_codes(tmp_path):
    good = tmp_path / "g.wikitext"
    good.write_text(LEAD, encoding="utf-8")
    bad = tmp_path / "b.wikitext"
    bad.write_text("متن", encoding="utf-8")
    assert main([str(good)]) == 0
    assert main([str(bad)]) == 1
    assert main([str(good), "--strict"]) == 0


def test_crlf_input_behaves_like_lf():
    text = "'''ع''' متن.<ref>x</ref>\n== See also ==\n{{پانویس}}\n[[رده:x]]\n"
    lf = [(i.code, i.line) for i in check(text)]
    crlf = [(i.code, i.line) for i in check(text.replace("\n", "\r\n"))]
    assert lf == crlf and ("WC09", 2) in lf
