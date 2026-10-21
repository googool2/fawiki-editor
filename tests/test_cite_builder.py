"""cite_builder: offline skeletons, parsing with a fake network, no invented data."""

import json

import pytest

import cite_builder as cb


def test_detect():
    assert cb.detect("https://example.com/a") == ("url", "https://example.com/a")
    assert cb.detect("10.1000/xyz123") == ("doi", "10.1000/xyz123")
    assert cb.detect("https://doi.org/10.1000/ABC") == ("doi", "10.1000/ABC")
    assert cb.detect("ISBN 978-964-8165-81-4") == ("isbn", "978-964-8165-81-4")
    assert cb.detect("۹۷۸-۹۶۴-۸۱۶۵-۸۱-۴")[0] == "isbn"


@pytest.mark.parametrize("bad", ["978-964-8165-81-5", "0-306-40615-3", "hello"])
def test_detect_rejects_bad_input(bad):
    with pytest.raises(ValueError):
        cb.detect(bad)


def test_isbn10_checksum():
    assert cb.normalize_isbn("0-306-40615-2") == "0306406152"


def test_offline_web_skeleton_has_no_invented_fields(capsys):
    assert cb.main(["https://www.example.org/news/1", "--offline", "--access-date", "2026-10-21"]) == 0
    out = capsys.readouterr()
    assert out.out.startswith("{{یادکرد وب")
    assert "| نشانی = https://www.example.org/news/1" in out.out
    assert "| تاریخ بازبینی = 2026-10-21" in out.out
    assert "| عنوان =" in out.out
    for invented in ("وبگاه =", "تاریخ =", "نویسنده", "ناشر"):
        assert invented not in out.out
    assert "TODO required" in out.err and "عنوان" in out.err


def test_offline_json_output(capsys):
    cb.main(["10.1000/xyz123", "--offline", "--json"])
    data = json.loads(capsys.readouterr().out)
    assert data["type"] == "journal"
    assert data["missing_required"] == ["عنوان", "ژورنال"]
    assert "| doi = 10.1000/xyz123" in data["template"]


def test_ref_wrapping(capsys):
    cb.main(["https://example.com", "--offline", "--name", "x1", "--inline"])
    out = capsys.readouterr().out.strip()
    assert out.startswith('<ref name="x1">{{یادکرد وب |') and out.endswith("}}</ref>")


HTML = b"""<html lang="fa"><head><title>Fallback</title>
<meta property="og:title" content="\xd8\xb9\xd9\x86\xd9\x88\xd8\xa7\xd9\x86 \xd8\xae\xd8\xa8\xd8\xb1">
<meta property="og:site_name" content="IRNA">
<meta property="article:published_time" content="2024-05-01T10:00:00Z">
<meta name="author" content="Reporter One">
</head></html>"""


def test_html_metadata_parsing():
    f = cb.lookup("url", "https://www.irna.ir/news/1", lambda u: HTML)
    tpl, missing, _ = cb.build(f, "web", "2026-10-21")
    assert "| عنوان = عنوان خبر" in tpl
    assert "| وبگاه = IRNA" in tpl
    assert "| تاریخ = 2024-05-01" in tpl
    assert "| نویسنده = Reporter One" in tpl
    assert "| کد زبان = fa" in tpl
    assert missing == []


CROSSREF = json.dumps({"message": {
    "title": ["A Study"], "container-title": ["Journal X"], "volume": "12", "issue": "3",
    "page": "17-19", "issued": {"date-parts": [[2020, 6, 7]]}, "type": "journal-article",
    "author": [{"family": "Smith", "given": "Ann"}, {"family": "Lee", "given": "Bo"}],
}}).encode()


def test_crossref_parsing_numbers_authors_with_persian_digits():
    f = cb.lookup("doi", "10.1000/x", lambda u: CROSSREF)
    tpl, missing, _ = cb.build(f, f["_kind"])
    assert tpl.startswith("{{یادکرد ژورنال")
    assert "| نام خانوادگی۱ = Smith" in tpl and "| نام۲ = Bo" in tpl
    assert "| ژورنال = Journal X" in tpl and "| تاریخ = 2020-06-07" in tpl
    assert "| doi = 10.1000/x" in tpl
    assert "تاریخ بازبینی" not in tpl  # no URL -> no access date
    assert missing == []


OPENLIB = json.dumps({"ISBN:9789648165814": {
    "title": "Book", "authors": [{"name": "A. Author"}], "publishers": [{"name": "Pub"}],
    "publish_places": [{"name": "Tehran"}], "publish_date": "2007"}}).encode()


def test_openlibrary_parsing_keeps_hyphenated_isbn():
    f = cb.lookup("isbn", "978-964-8165-81-4", lambda u: OPENLIB)
    tpl, missing, _ = cb.build(f, "book")
    assert "| شابک = 978-964-8165-81-4" in tpl
    assert "| ناشر = Pub" in tpl and "| مکان = Tehran" in tpl and "| سال = 2007" in tpl
    assert missing == []


def test_network_failure_falls_back_to_skeleton(monkeypatch, capsys):
    def boom(url, timeout=15.0):
        raise OSError("no network")
    monkeypatch.setattr(cb, "http_fetch", boom)
    assert cb.main(["https://example.com/x"]) == 1
    out = capsys.readouterr()
    assert "{{یادکرد وب" in out.out and "lookup failed" in out.err


def test_offline_never_calls_network(monkeypatch, capsys):
    def boom(url, timeout=15.0):
        raise AssertionError("network used in --offline mode")
    monkeypatch.setattr(cb, "http_fetch", boom)
    assert cb.main(["https://example.com/x", "--offline"]) == 0
