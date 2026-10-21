"""Repository-level constraints from the project brief."""

import json
import re
from pathlib import Path

import pytest

from fa_lint import lint

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "fawiki-editor"
TEXT_FILES = [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts
              and "__pycache__" not in p.parts and p.suffix in {".py", ".md", ".json", ".wikitext", ".txt"}]


@pytest.mark.parametrize("path", TEXT_FILES, ids=lambda p: str(p.relative_to(ROOT)))
def test_no_file_over_500_lines(path):
    assert len(path.read_text(encoding="utf-8").splitlines()) <= 500


def test_skill_md_under_400_lines_and_frontmatter():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    assert len(text.splitlines()) < 400
    fm = re.match(r"---\n(.*?)\n---\n", text, re.S).group(1)
    assert re.search(r"^name: fawiki-editor$", fm, re.M)
    desc = re.search(r"description: >-\n(.*?)\n(?=\w)", fm, re.S).group(1)
    desc = " ".join(line.strip() for line in desc.splitlines())
    assert len(desc) <= 1024
    for word in ("ویکی‌پدیا", "ویکی‌فا", "ویکی‌متن", "یادکرد", "جعبه اطلاعات", "شیوه‌نامه",
                 "سرشناسی", "fa.wikipedia.org", "Persian Wikipedia".split()[0]):
        assert word in desc, word
    assert "<" not in desc and ">" not in desc


def test_every_reference_mentioned_in_skill_md_exists():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    for name in re.findall(r"(?:references/)?([a-z-]+\.md)", text):
        if name in ("SKILL.md", "README.md", "research-summary.md"):
            continue
        assert (SKILL / "references" / name).exists() or (SKILL / "examples" / name).exists(), name


def test_readme_fa_passes_fa_lint():
    text = (ROOT / "README.fa.md").read_text(encoding="utf-8")
    res = lint(text, markdown=True)
    assert res.changes == [], [c.__dict__ for c in res.changes]


@pytest.mark.parametrize("path", sorted(ROOT.rglob("*.json")), ids=lambda p: p.name)
def test_json_files_parse(path):
    if ".git" not in path.parts:
        json.loads(path.read_text(encoding="utf-8"))


def test_trigger_evals_balanced():
    items = json.loads((ROOT / "evals" / "triggers.json").read_text(encoding="utf-8"))
    assert len(items) == 10
    assert sum(i["should_trigger"] for i in items) == 5


def test_output_evals_have_acceptance_criteria():
    data = json.loads((ROOT / "evals" / "outputs.json").read_text(encoding="utf-8"))
    assert data["skill_name"] == "fawiki-editor" and len(data["evals"]) == 5
    assert all(e["expectations"] for e in data["evals"])


def test_plugin_manifests():
    plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    assert plugin["name"] == "fawiki-editor" and "skills" not in plugin  # standard skills/ layout
    assert market["plugins"][0]["name"] == plugin["name"] and market["plugins"][0]["source"] == "./"


def test_lint_and_check_scripts_do_not_import_network_modules():
    for name in ("fa_lint.py", "wikitext_check.py", "fawiki_common.py", "infobox_builder.py"):
        src = (SKILL / "scripts" / name).read_text(encoding="utf-8")
        assert not re.search(r"^\s*(?:import|from)\s+(?:urllib|http|socket|requests)", src, re.M), name
