"""Shared helpers for the fawiki-editor scripts (stdlib only, no network).

The central piece is `mask()`: it finds every region of wikitext that a prose
linter must never touch and swaps each one for a single private-use
placeholder character. Rules then run on the masked text and `unmask()` puts
the original regions back byte-for-byte.

Protected regions:
  HTML comments, <nowiki>/<pre>/<code>/<math>/<syntaxhighlight>/<ref>... blocks,
  self-closing tags such as <ref name="x"/>, every other HTML tag token,
  templates and parser functions {{...}} (nested), wikilinks [[...]] (nested),
  external links [http://... label], bare URLs, magic words (__TOC__),
  ISBN/PMID/RFC magic links, signatures (~~~~), table syntax lines and cell
  attributes, and lines that start with a space (preformatted text).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

__version__ = "0.2.1"

DATA_DIR = Path(__file__).resolve().parent / "data"

# Supplementary private-use area: one code point per protected span.
PH_BASE = 0xF0000
PH_MAX = 0xFFFFD - PH_BASE
PH_CLASS = "\U000F0000-\U000FFFFD"
PH_RE = re.compile(f"[{PH_CLASS}]")

# Letters that never join to the following letter. A ZWNJ after them is
# redundant (and fa.wiki's نیم‌فاصله page calls it not allowed).
NON_JOINING = "اآأإدذرزژوؤة"
PERSIAN_LETTERS = "آاأإءئؤبپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیةۀ"
ZWNJ = "‌"

# Block-level tags whose whole content is protected.
OPAQUE_TAGS = (
    "nowiki", "pre", "code", "source", "syntaxhighlight", "math", "chem",
    "score", "gallery", "timeline", "templatedata", "graph", "mapframe",
    "maplink", "ref", "references", "poem", "hiero", "inputbox", "imagemap",
    "categorytree", "section", "tt", "kbd", "samp", "var",
)
_OPAQUE_OPEN = re.compile(
    r"<(" + "|".join(OPAQUE_TAGS) + r")\b([^<>]*?)(/?)>", re.IGNORECASE
)
_ANY_TAG = re.compile(r"</?[a-zA-Z][a-zA-Z0-9]*\b[^<>\n]*/?>")
_URL = re.compile(r"(?:https?|ftp|irc|mailto|news):(?://)?[^\s\[\]<>|{}\"«»]+|//[a-z0-9.-]+\.[a-z]{2,}[^\s\[\]<>|{}\"«»]*", re.IGNORECASE)
_EXT_LINK = re.compile(r"\[(?:(?:https?|ftp|irc|mailto|news):|//)[^\]\n]*\]", re.IGNORECASE)
_MAGIC = re.compile(r"__[A-Z؀-ۿ_]+__")
_MAGIC_LINK = re.compile(r"\b(?:ISBN|PMID|RFC)[  ]+[0-9Xx][0-9Xx \-]*[0-9Xx]")
_SIG = re.compile(r"~{3,5}")
_TABLE_LINE = re.compile(r"[ \t]*(?:\{\||\|-|\|\}|\|\+)[^\n]*")
_CELL_START = re.compile(r"[ \t]*[|!]")
_CELL_ATTR = re.compile(
    r"[ \t]*(?:[a-zA-Z][\w:-]*[ \t]*=[ \t]*(?:\"[^\"\n]*\"|'[^'\n]*'|[^\s|'\"]+)[ \t]*)+\|(?!\|)"
)
_LANG_BLOCK = re.compile(
    r"\{\{\s*(?:آغاز\s+)?(عربی|اردو|کردی|پشتو)\s*\}\}.*?\{\{\s*پایان\s+\1\s*\}\}", re.DOTALL
)
# Letters that Persian never uses but Uyghur, Kurdish, Urdu, Pashto, Sindhi and Kazakh do.
# A run of words containing them is another language: folding its ي/ك/ى would corrupt it.
_FOREIGN_LETTERS = "ٹڈڑںےۓھێڵڕۆەېۇۈۋڭڤٶٷٵٸټډړږښګڼۍڄٻڀٺٽٿڃڇڊڌڍڎڏڙڦڱڳڻۅۉۊ"
_AR_LETTER = "\u0620-\u065F\u066E-\u06D3\u06D5\u06EE\u06EF\u06FA-\u06FC\u06FF\u0750-\u077F"
_AR_WORD = re.compile(f"[{_AR_LETTER}][{_AR_LETTER}\u200c\u200d]*")
_FOREIGN = re.compile(f"[{_FOREIGN_LETTERS}]")
_FOLDABLE = re.compile(f"[يكى{_FOREIGN_LETTERS}]")
_CANDIDATE = re.compile(r"<|\{\{|\[|(?:https?|ftp|irc|mailto|news):|//|__|ISBN|PMID|RFC|~~~|\n|\|\||!!")
_CANDIDATE_MD = re.compile(_CANDIDATE.pattern + r"|`|\]\(")


def _match_pair(text: str, i: int, open_s: str, close_s: str) -> int:
    """Return the index just past the balanced closer for the opener at i, or -1."""
    depth, n = 0, len(text)
    while i < n:
        if text.startswith(open_s, i):
            depth += 1
            i += len(open_s)
        elif text.startswith(close_s, i):
            depth -= 1
            i += len(close_s)
            if depth == 0:
                return i
        else:
            i += 1
    return -1


def _para_end(text: str, i: int) -> int:
    j = text.find("\n\n", i)
    return len(text) if j == -1 else j


_MD_FENCE = re.compile(r"(`{3,}|~{3,})[^\n]*\n.*?(?:\n\1[ \t]*(?=\n|$)|\Z)", re.DOTALL)
_MD_CODE = re.compile(r"`[^`\n]+`")
_MD_LINK_TARGET = re.compile(r"\]\([^)\s]+\)")


def _foreign_script_spans(text: str) -> list[tuple[int, int]]:
    """Runs of Arabic-script words in another language (see _FOREIGN_LETTERS).

    A word with a foreign letter starts a run; the run grows over neighbours joined by spaces,
    parentheses or direction marks that contain ي/ك/ى or foreign letters («شەرقىي كوچا باشقارمىسى»,
    «ئارايۇلتۇز (شىڭشىڭشيا) بازىرى»)."""
    if not _FOREIGN.search(text):
        return []
    words = [(m.start(), m.end()) for m in _AR_WORD.finditer(text)]

    def joined(a: int, b: int) -> bool:
        gap = text[a:b]
        return bool(gap) and len(gap) <= 4 and all(c in " ()\u00a0\u200e\u200f" for c in gap)

    runs: list[tuple[int, int]] = []
    for k, (s, e) in enumerate(words):
        if not _FOREIGN.search(text, s, e):
            continue
        lo = hi = k
        while lo > 0 and joined(words[lo - 1][1], words[lo][0]) and _FOLDABLE.search(text, *words[lo - 1]):
            lo -= 1
        while hi + 1 < len(words) and joined(words[hi][1], words[hi + 1][0]) and _FOLDABLE.search(text, *words[hi + 1]):
            hi += 1
        start, end = words[lo][0], words[hi][1]
        if runs and start <= runs[-1][1]:
            runs[-1] = (runs[-1][0], max(end, runs[-1][1]))
        else:
            runs.append((start, end))
    return runs


def _add_foreign_script(text: str, spans: list[tuple[int, int, str]]) -> list[tuple[int, int, str]]:
    extra = []
    for fs, fe in _foreign_script_spans(text):
        pos = fs
        for s, e, _k in spans:  # keep only the parts outside existing spans
            if e <= pos or s >= fe:
                continue
            if s > pos:
                extra.append((pos, s, "foreign-script"))
            pos = max(pos, e)
        if pos < fe:
            extra.append((pos, fe, "foreign-script"))
    return sorted(spans + extra) if extra else spans


def find_protected_spans(text: str, markdown: bool = False) -> list[tuple[int, int, str]]:
    """Return sorted, non-overlapping (start, end, kind) spans to protect.

    With markdown=True, fenced code blocks, `inline code` and link targets
    are protected too (used to lint README.fa.md).
    """
    spans: list[tuple[int, int, str]] = []
    n = len(text)
    i = 0
    at_line_start = True
    while i < n:
        if markdown:
            m = _MD_FENCE.match(text, i) if at_line_start else None
            if m:
                spans.append((i, m.end(), "md-code"))
                i = m.end()
                continue
        if at_line_start:
            at_line_start = False
            m = _TABLE_LINE.match(text, i)
            if m:
                spans.append((i, m.end(), "table"))
                i = m.end()
                continue
            if text.startswith(" ", i) and not text.startswith(" \n", i):
                j = text.find("\n", i)
                j = n if j == -1 else j
                spans.append((i, j, "pre-line"))
                i = j
                continue
            m = _CELL_START.match(text, i)
            if m:
                a = _CELL_ATTR.match(text, m.end())
                end = a.end() if a else m.end()
                spans.append((i, end, "table-cell"))
                i = end
                continue
        m = (_CANDIDATE_MD if markdown else _CANDIDATE).search(text, i)
        if not m:
            break
        i = m.start()
        ch = text[i]
        if ch == "\n":
            i += 1
            at_line_start = True
            continue
        if text.startswith("||", i) or text.startswith("!!", i):
            a = _CELL_ATTR.match(text, i + 2)
            end = a.end() if a else i + 2
            spans.append((i, end, "table-cell"))
            i = end
            continue
        if text.startswith("<!--", i):
            j = text.find("-->", i + 4)
            j = n if j == -1 else j + 3
            spans.append((i, j, "comment"))
            i = j
            continue
        if ch == "<":
            m2 = _OPAQUE_OPEN.match(text, i)
            if m2:
                if m2.group(3) == "/":
                    j = m2.end()
                else:
                    close = re.compile(r"</" + re.escape(m2.group(1)) + r"\s*>", re.IGNORECASE)
                    c = close.search(text, m2.end())
                    j = c.end() if c else _para_end(text, m2.end())
                spans.append((i, j, m2.group(1).lower()))
                i = j
                continue
            m2 = _ANY_TAG.match(text, i)
            if m2:
                spans.append((i, m2.end(), "tag"))
                i = m2.end()
                continue
            i += 1
            continue
        if text.startswith("{{", i):
            m2 = _LANG_BLOCK.match(text, i)
            if m2:  # {{عربی}} … {{پایان عربی}}: foreign-language text, never fold letters
                spans.append((i, m2.end(), "lang-block"))
                i = m2.end()
                continue
            j = _match_pair(text, i, "{{", "}}")
            j = _para_end(text, i) if j == -1 else j
            spans.append((i, j, "template"))
            i = j
            continue
        if text.startswith("[[", i):
            j = _match_pair(text, i, "[[", "]]")
            j = _para_end(text, i) if j == -1 else j
            spans.append((i, j, "link"))
            i = j
            continue
        if markdown and (ch == "`" or text.startswith("](", i)):
            m2 = (_MD_CODE if ch == "`" else _MD_LINK_TARGET).match(text, i)
            if m2:
                spans.append((i, m2.end(), "md-code"))
                i = m2.end()
            else:
                i += 1
            continue
        if ch == "[":
            m2 = _EXT_LINK.match(text, i)
            if m2:
                spans.append((i, m2.end(), "extlink"))
                i = m2.end()
                continue
            i += 1
            continue
        for rx, kind in ((_URL, "url"), (_MAGIC, "magic"), (_MAGIC_LINK, "magiclink"), (_SIG, "signature")):
            m2 = rx.match(text, i)
            if m2 and (kind != "url" or i == 0 or not text[i - 1].isalnum()):
                spans.append((i, m2.end(), kind))
                i = m2.end()
                break
        else:
            i += 1
    return _add_foreign_script(text, spans)


class Masked:
    """Text with protected spans replaced by placeholder characters."""

    def __init__(self, text: str, markdown: bool = False):
        self.original = text
        self.spans = find_protected_spans(text, markdown=markdown)
        if len(self.spans) > PH_MAX:
            raise ValueError("too many protected regions")
        parts, last = [], 0
        self.chunks: list[str] = []
        self.kinds: list[str] = []
        for k, (s, e, kind) in enumerate(self.spans):
            parts.append(text[last:s])
            parts.append(chr(PH_BASE + k))
            self.chunks.append(text[s:e])
            self.kinds.append(kind)
            last = e
        parts.append(text[last:])
        self.text = "".join(parts)
        self._nl = [c.count("\n") for c in self.chunks]

    def unmask(self, masked: str | None = None) -> str:
        src = self.text if masked is None else masked
        return PH_RE.sub(lambda m: self.chunks[ord(m.group()) - PH_BASE], src)

    def line_of(self, masked: str, pos: int) -> int:
        """1-based line number in the original text for a position in `masked`."""
        prefix = masked[:pos]
        extra = sum(self._nl[ord(c) - PH_BASE] for c in PH_RE.findall(prefix))
        return prefix.count("\n") + extra + 1

    def protected(self, kinds: tuple[str, ...] | None = None):
        """Yield (start, end, kind, chunk) for protected spans in the original."""
        for (s, e, kind), chunk in zip(self.spans, self.chunks):
            if kinds is None or kind in kinds:
                yield s, e, kind, chunk


def line_at(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def load_json(name: str):
    with open(DATA_DIR / name, encoding="utf-8") as f:
        return json.load(f)


def read_input(path: str | None) -> str:
    """Read UTF-8 text exactly as stored (CRLF kept, BOM kept for FA09 to report)."""
    import sys

    if path in (None, "-"):
        return sys.stdin.read()
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def write_text_atomic(path: str | Path, text: str) -> None:
    """Write next to the target first, then replace it in one step (no half-written file)."""
    import os
    import tempfile

    path = Path(path)
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def utf8_stdio() -> None:
    """Persian output must not crash on consoles with a legacy code page (Windows)."""
    import sys

    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except (ValueError, OSError):  # pragma: no cover - detached or odd streams
                pass


def try_mwparser():
    """Return the mwparserfromhell module if installed, else None."""
    try:
        import mwparserfromhell  # type: ignore

        return mwparserfromhell
    except ImportError:  # pragma: no cover - depends on environment
        return None
