"""Command test: run the CLI end to end in throwaway folders (scan, apply, undo, refusals)."""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "fawiki-editor"
CLI = [sys.executable, str(SKILL / "scripts" / "fawiki.py")]
BAD = (SKILL / "examples" / "article-bad.wikitext").read_bytes()


def run(*args, cwd):
    p = subprocess.run(CLI + list(args), cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                       env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"})
    return p.returncode, p.stdout, p.stderr


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


@pytest.fixture
def work(tmp_path):
    (tmp_path / "a.wikitext").write_bytes(BAD)
    return tmp_path


def test_version(work):
    code, out, _ = run("--version", cwd=work)
    assert code == 0 and out.strip().startswith("fawiki-editor ")


def test_scan_writes_nothing(work):
    before = sha(work / "a.wikitext")
    code, out, _ = run("scan", "a.wikitext", cwd=work)
    assert code == 1 and "#1" in out and "WC03" in out
    assert sha(work / "a.wikitext") == before
    assert sorted(p.name for p in work.iterdir()) == ["a.wikitext"]


def test_report_is_compact(work):
    _, out, _ = run("report", "a.wikitext", cwd=work)
    assert len(out.splitlines()) <= 15


def test_apply_then_undo_is_byte_identical(work):
    before = sha(work / "a.wikitext")
    assert run("apply", "a.wikitext", cwd=work)[0] == 0
    assert sha(work / "a.wikitext") != before
    meta = json.loads((work / "a.wikitext.fawiki.json").read_text(encoding="utf-8"))
    assert meta["original_sha256"] == before and meta["result_sha256"] == sha(work / "a.wikitext")
    assert run("undo", "a.wikitext", cwd=work)[0] == 0
    assert sha(work / "a.wikitext") == before
    assert sorted(p.name for p in work.iterdir()) == ["a.wikitext"]


def test_apply_only_subset(work):
    assert run("apply", "a.wikitext", "--only", "1-2", cwd=work)[0] == 0
    _, out, _ = run("report", "a.wikitext", cwd=work)
    assert "5 change(s)" in out


def test_refusals(work):
    assert run("apply", "a.wikitext", "--only", "99", cwd=work)[0] == 1
    assert run("undo", "a.wikitext", cwd=work)[0] == 1          # nothing to undo
    run("apply", "a.wikitext", cwd=work)
    assert run("apply", "a.wikitext", cwd=work)[0] == 1         # backup exists
    with open(work / "a.wikitext", "a", encoding="utf-8") as f:
        f.write("ویرایش دستی\n")
    assert run("undo", "a.wikitext", cwd=work)[0] == 1          # edited after apply
    assert run("undo", "a.wikitext", "--force", cwd=work)[0] == 0
    (work / "README.wikitext").write_bytes(BAD)
    assert run("apply", "README.wikitext", cwd=work)[0] == 1    # protected name


def test_crlf_preserved(work):
    f = work / "c.wikitext"
    f.write_bytes("خط ي\r\nخط ك\r\n".encode("utf-8"))
    run("apply", "c.wikitext", cwd=work)
    assert f.read_bytes() == "خط ی\r\nخط ک\r\n".encode("utf-8")


def test_cite_and_infobox_forwarding(work):
    code, out, _ = run("cite", "978-964-8165-81-4", "--offline", cwd=work)
    assert code == 0 and "{{یادکرد کتاب" in out
    code, out, _ = run("infobox", "--template", "film", "--skeleton", cwd=work)
    assert code == 0 and "{{جعبه اطلاعات فیلم" in out
