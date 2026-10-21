"""infobox_builder: YAML subset parser, aliases, no invented values."""

import json

import pytest

import infobox_builder as ib


def test_simple_yaml_parser():
    data = ib.parse_simple_yaml("# c\ntemplate: film\ntitle: \"گاو\"\nstarring:\n  - الف\n  - ب\nempty:\n")
    assert data == {"template": "film", "title": "گاو", "starring": ["الف", "ب"], "empty": ""}


def test_yaml_parser_rejects_garbage():
    with pytest.raises(ValueError):
        ib.parse_simple_yaml("not a mapping line")


@pytest.mark.parametrize("name,key", [
    ("film", "film"), ("فیلم", "film"), ("جعبه اطلاعات فیلم", "film"),
    ("person", "biography"), ("زندگی‌نامه", "biography"), ("شرکت", "company"),
])
def test_resolve(name, key):
    assert ib.resolve(name) == key


def test_resolve_unknown():
    with pytest.raises(KeyError):
        ib.resolve("spaceship")


def test_build_maps_english_keys_and_lists():
    text, missing, dropped = ib.build(
        {"title": "گاو", "director": "داریوش مهرجویی", "starring": ["الف", "ب"], "budget": "1"}, "film")
    assert text.startswith("{{جعبه اطلاعات فیلم")
    assert "= {{فهرست ساده|الف|ب}}" in text
    assert "کارگردان" in text and "budget" not in text
    assert dropped == ["budget"]
    assert set(missing) == {"کشور", "زبان"}


def test_build_accepts_persian_keys_and_keep_unknown():
    text, _, dropped = ib.build({"نام": "x", "فیلد تازه": "y"}, "company", keep_unknown=True)
    assert "فیلد تازه" in text and dropped == []


def test_empty_core_params_are_left_blank_not_invented():
    text, missing, _ = ib.build({"name": "x"}, "company")
    assert "| صنعت" in text and text.count("= \n") == 0
    assert "صنعت" in missing


def test_every_schema_is_well_formed():
    for key, box in ib.BOXES.items():
        assert box["template"].startswith(("جعبه اطلاعات", "Infobox"))
        assert box["confidence"] in ("V", "LOW")
        assert set(box["core"]) <= set(box["params"].values()), key
        assert box["source"].startswith("https://fa.wikipedia.org/wiki/")


def test_cli_json_and_skeleton(tmp_path, capsys):
    f = tmp_path / "d.json"
    f.write_text(json.dumps({"template": "book", "name": "کتاب"}, ensure_ascii=False), encoding="utf-8")
    assert ib.main([str(f)]) == 0
    assert "{{جعبه اطلاعات کتاب" in capsys.readouterr().out
    assert ib.main([str(f), "--strict"]) == 1
    assert ib.main(["--template", "album", "--skeleton"]) == 0
    assert ib.main(["--list"]) == 0
