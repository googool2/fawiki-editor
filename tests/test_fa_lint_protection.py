"""The linter must never change a byte inside protected wikitext regions."""

import pytest

from fa_lint import lint
from fawiki_common import Masked, find_protected_spans

# Every sample is full of things the prose rules WOULD change (Arabic ي/ك,
# Latin digits, "می " without ZWNJ, " ها", space before ".", Latin comma).
DIRTY = "ي ك 123 می رود کتاب ها , ."

PROTECTED_SAMPLES = [
    "{{جعبه اطلاعات شخص|نام=" + DIRTY + "|تولد=1990}}",
    "{{الگو|a={{تو در تو|" + DIRTY + "}}|b=[[پیوند|" + DIRTY + "]]}}",
    "{{#if: 1 | " + DIRTY + " }}",
    "[[" + DIRTY + "]]",
    "[[پرونده:Map 2010.png|بندانگشتی|" + DIRTY + " [[تهران]]]]",
    "<ref>" + DIRTY + "</ref>",
    '<ref name="منبع 1">' + DIRTY + "</ref>",
    '<ref name="a" />',
    "<ref name=b/>",
    "<nowiki>" + DIRTY + "</nowiki>",
    "<math>x^2 + 10, y</math>",
    "<syntaxhighlight lang=python>a = 1 ; b = 2 ?</syntaxhighlight>",
    "<!-- " + DIRTY + " -->",
    "https://example.com/path?a=1,2&b=ي",
    "http://fa.wikipedia.org/wiki/كتاب_ها",
    "[https://example.com/2020 " + DIRTY + "]",
    "ISBN 978-3-16-148410-0",
    "__NOTOC__",
    "~~~~",
    '<span style="color:red; width:50%">',
]


@pytest.mark.parametrize("sample", PROTECTED_SAMPLES)
def test_protected_region_is_untouched(sample):
    text = "متن " + sample + " متن"
    res = lint(text)
    assert sample in res.fixed, f"protected region was modified:\n{res.fixed}"


@pytest.mark.parametrize("sample", PROTECTED_SAMPLES)
def test_protected_region_alone_produces_no_change(sample):
    assert lint(sample).fixed == sample


def test_prose_around_protected_regions_is_fixed():
    text = "كتاب ها {{الگو|ي}} می رود [[پیوند ي]] 12 <ref>ي</ref> ."
    out = lint(text).fixed
    assert out == "کتاب‌ها {{الگو|ي}} می‌رود [[پیوند ي]] ۱۲ <ref>ي</ref>."


def test_mask_roundtrip_is_lossless():
    text = "{{a|{{b}}}} [[c|d]] <ref>e</ref> http://f.g/h {| class=x\n| style=y | z\n|}\n ی pre"
    m = Masked(text)
    assert m.unmask() == text


def test_unclosed_template_protects_to_paragraph_end():
    text = "{{الگو|ي 12\nي 12\n\nي 12"
    out = lint(text).fixed
    assert out.startswith("{{الگو|ي 12\nي 12\n\n")
    assert out.endswith("ی ۱۲")


def test_table_attributes_untouched_but_cells_fixed():
    text = '{| class="wikitable" style="width:50%"\n|-\n! سال !! align="center" | عنوان\n|-\n| style="color:red" | 1990 || كتاب ها\n|}'
    out = lint(text).fixed
    assert '{| class="wikitable" style="width:50%"' in out
    assert '| style="color:red" | ۱۹۹۰ || کتاب‌ها' in out
    assert 'align="center" |' in out


def test_preformatted_line_untouched():
    text = "متن\n ي 12 pre\nمتن"
    assert lint(text).fixed == text


def test_markdown_code_protected_only_in_markdown_mode():
    text = "متن `python 3.10 ي` و\n```\nي 12\n```\n"
    assert lint(text, markdown=True).fixed == text


def test_spans_do_not_overlap():
    text = "{{a|[[b|<ref>c</ref>]]}} <ref>{{d}}</ref> [[e|{{f}}]]"
    spans = find_protected_spans(text)
    for (s1, e1, _), (s2, e2, _) in zip(spans, spans[1:]):
        assert e1 <= s2
