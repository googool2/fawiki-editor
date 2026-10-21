#!/usr/bin/env python3
"""infobox_builder — build a Persian fa.wiki infobox from simple YAML or JSON.

Offline, stdlib only (uses PyYAML if it happens to be installed, otherwise a
small built-in parser for flat "key: value" files with "- item" lists).

Input keys may be the Persian parameter names or the English aliases listed
by --list. Lists become {{فهرست ساده|…}}. Values are copied as given: the
script never fills in data you did not provide.

Usage:
  infobox_builder.py --list                         # supported infoboxes + aliases
  infobox_builder.py --template film --skeleton     # empty box with every param
  infobox_builder.py data.yaml                      # 'template:' key inside the file
  infobox_builder.py data.json --template company --keep-unknown

Example data.yaml:
  template: film
  title: گاو
  director: داریوش مهرجویی
  starring:
    - عزت‌الله انتظامی
    - علی نصیریان
  country: ایران

Exit codes: 0 ok, 1 missing core params (with --strict), 2 bad input.
Parameter names and their confidence: scripts/data/infoboxes.json, references/infoboxes.md.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fawiki_common import load_json, read_input  # noqa: E402

BOXES: dict = load_json("infoboxes.json")["infoboxes"]


def parse_simple_yaml(text: str) -> dict:
    """Parse flat YAML: `key: value`, `key:` followed by `- item` lines, # comments."""
    data: dict = {}
    current: str | None = None
    for n, raw in enumerate(text.splitlines(), 1):
        line = re.sub(r"(^|\s)#(?!\S*[»\]]).*$", "", raw).rstrip()
        if not line.strip():
            continue
        m_item = re.match(r"^\s+-\s+(.*)$", line) or re.match(r"^-\s+(.*)$", line)
        if m_item and current is not None:
            if not isinstance(data.get(current), list):
                data[current] = []
            data[current].append(_unquote(m_item.group(1)))
            continue
        m = re.match(r"^([^:\s][^:]*?)\s*:\s*(.*)$", line)
        if not m:
            raise ValueError(f"line {n}: expected 'key: value', got: {raw!r}")
        key, val = m.group(1).strip(), m.group(2).strip()
        current = key
        data[key] = _unquote(val) if val else []
    return {k: ("" if v == [] else v) for k, v in data.items()}


def _unquote(v: str) -> str:
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


def load_data(text: str, path: str) -> dict:
    if path.endswith(".json") or text.lstrip().startswith("{"):
        return json.loads(text)
    try:
        import yaml  # type: ignore

        return yaml.safe_load(text) or {}
    except ImportError:
        return parse_simple_yaml(text)


def resolve(name: str) -> str:
    """Map a user-supplied infobox name/alias to a key of BOXES."""
    n = name.strip().replace("_", " ")
    for key, box in BOXES.items():
        names = {key, key.replace("_", " "), box["template"], box["template"].replace("جعبه اطلاعات ", "")}
        names |= set(box["select"])
        if n in names or n.lower() in {x.lower() for x in names}:
            return key
    raise KeyError(f"unknown infobox «{name}». Run --list to see supported ones.")


def build(data: dict, key: str, keep_unknown: bool = False) -> tuple[str, list[str], list[str]]:
    """Return (wikitext, missing_core, dropped_keys)."""
    box = BOXES[key]
    params: dict[str, str] = box["params"]
    persian = set(params.values())
    values: dict[str, str] = {}
    dropped: list[str] = []
    for k, v in data.items():
        if k in ("template", "infobox", "الگو"):
            continue
        name = params.get(k, k if k in persian else None)
        if name is None:
            if keep_unknown:
                name = k
            else:
                dropped.append(k)
                continue
        if isinstance(v, list):
            items = [str(x).strip() for x in v if str(x).strip()]
            v = "{{فهرست ساده|" + "|".join(items) + "}}" if len(items) > 1 else (items[0] if items else "")
        values[name] = "" if v is None else str(v).strip()
    order = list(dict.fromkeys(params.values()))
    order += [k for k in values if k not in order]
    width = max(len(p) for p in order)
    lines = ["{{" + box["template"]]
    for p in order:
        if p in values or p in box["core"]:
            lines.append(f"| {p.ljust(width)} = {values.get(p, '')}".rstrip())
    lines.append("}}")
    missing = [p for p in box["core"] if not values.get(p)]
    return "\n".join(lines), missing, dropped


def skeleton(key: str) -> str:
    box = BOXES[key]
    order = list(dict.fromkeys(box["params"].values()))
    width = max(len(p) for p in order)
    return "\n".join(["{{" + box["template"]] + [f"| {p.ljust(width)} =" for p in order] + ["}}"])


def list_boxes() -> str:
    out = []
    for key, box in BOXES.items():
        out.append(f"{key:<15} {{{{{box['template']}}}}}  [confidence: {box['confidence']}]  select: {', '.join(box['select'])}")
        out.append("    " + ", ".join(f"{en}→{fa}" for en, fa in box["params"].items()))
        out.append(f"    core: {', '.join(box['core'])}")
        if box.get("note"):
            out.append(f"    note: {box['note']}")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Build a Persian fa.wiki infobox from YAML/JSON")
    ap.add_argument("file", nargs="?", help="YAML or JSON data file, or - for stdin")
    ap.add_argument("--template", "-t", help="infobox key, alias or full Persian name")
    ap.add_argument("--skeleton", action="store_true", help="print an empty box with all known params")
    ap.add_argument("--list", action="store_true", help="list supported infoboxes")
    ap.add_argument("--keep-unknown", action="store_true", help="keep keys that are not in the schema")
    ap.add_argument("--strict", action="store_true", help="exit 1 when core params are missing")
    a = ap.parse_args(argv)

    if a.list:
        print(list_boxes())
        return 0
    try:
        if a.skeleton:
            if not a.template:
                print("--skeleton needs --template", file=sys.stderr)
                return 2
            print(skeleton(resolve(a.template)))
            return 0
        if not a.file:
            ap.print_usage(sys.stderr)
            return 2
        data = load_data(read_input(a.file), a.file)
        if not isinstance(data, dict):
            raise ValueError("data must be a mapping of parameter: value")
        name = a.template or data.get("template") or data.get("infobox") or data.get("الگو")
        if not name:
            raise ValueError("say which infobox: --template NAME or a 'template:' key")
        key = resolve(str(name))
        text, missing, dropped = build(data, key, a.keep_unknown)
    except (KeyError, ValueError, OSError, json.JSONDecodeError) as e:
        print(str(e).strip("'\""), file=sys.stderr)
        return 2
    print(text)
    box = BOXES[key]
    if box["confidence"] != "V":
        print(f"NOTE: parameter names for {{{{{box['template']}}}}} are [{box['confidence']}] — compare with {box['source']}",
              file=sys.stderr)
    if missing:
        print("missing core params (fill only from reliable sources): " + "، ".join(missing), file=sys.stderr)
    if dropped:
        print("dropped unknown keys (use --keep-unknown to keep): " + ", ".join(dropped), file=sys.stderr)
    return 1 if a.strict and missing else 0


if __name__ == "__main__":
    sys.exit(main())
