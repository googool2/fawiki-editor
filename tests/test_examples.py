"""The bundled examples behave as documented."""

from pathlib import Path

import pytest

from fa_lint import lint
from wikitext_check import check

EX = Path(__file__).resolve().parent.parent / "skills" / "fawiki-editor" / "examples"
GOOD = (EX / "article-good.wikitext").read_text(encoding="utf-8")
BAD = (EX / "article-bad.wikitext").read_text(encoding="utf-8")

# The ten deliberate errors in article-bad.wikitext: (tool, rule, line)
EXPECTED_BAD = {
    ("fa_lint", "FA01", 2),        # Arabic ي in «ايران»
    ("fa_lint", "FA02", 8),        # Arabic ك in «كوه»
    ("fa_lint", "FA40", 8),        # space before «.»
    ("fa_lint", "FA04", 11),       # Latin digits 5600
    ("fa_lint", "FA21", 11),       # «قله ها» with a space
    ("fa_lint", "FA20", 12),       # «می گویند» without ZWNJ
    ("fa_lint", "FA30", 12),       # Latin comma
    ("wikitext_check", "WC06", 2),  # no bold title in the lead
    ("wikitext_check", "WC03", 12),  # <ref> without </ref>
    ("wikitext_check", "WC05", 19),  # no category
}


def _found_bad():
    found = {("fa_lint", c.rule, c.line) for c in lint(BAD).changes}
    found |= {("wikitext_check", i.code, i.line) for i in check(BAD) if i.severity == "E"}
    return found


def test_bad_article_has_exactly_the_ten_errors():
    assert _found_bad() == EXPECTED_BAD


def test_good_article_is_unchanged_by_fa_lint():
    res = lint(GOOD)
    assert res.fixed == GOOD
    assert res.changes == []
    assert res.warnings == []


def test_good_article_has_no_structural_errors_or_warnings():
    issues = check(GOOD)
    assert [i for i in issues if i.severity in ("E", "W")] == []


def test_fixing_bad_article_clears_all_lint_errors():
    fixed = lint(BAD).fixed
    assert lint(fixed).changes == []


def test_lint_does_not_touch_the_citation_in_bad_article():
    fixed = lint(BAD).fixed
    start = BAD.index("<ref name=")
    end = BAD.index("</ref>") + len("</ref>")
    assert BAD[start:end] in fixed


@pytest.mark.parametrize("name", ["translation-before-after.md"])
def test_translation_example_after_block_is_clean(name):
    text = (EX / name).read_text(encoding="utf-8")
    after = text.split("<!-- AFTER -->", 1)[1].split("```wikitext", 1)[1].split("```", 1)[0]
    assert lint(after).changes == []
    assert [i for i in check(after) if i.severity == "E"] == []
