#!/usr/bin/env python3
"""Synthetic benchmark: messy fa.wiki drafts full of planted errors and traps.

Runs the most aggressive setting (every rule, `fawiki.py apply` with no selection) on copies
in a throwaway folder and checks mechanically:
  1. every planted error is fixed, and the wrong form is gone from prose;
  2. every trap (text that looks wrong but must stay) is byte-identical;
  3. every protected region (templates, links, refs, URLs, ...) is byte-identical;
  4. the template and link inventory is unchanged (structure preserved);
  5. a second apply changes nothing (idempotent);
  6. undo restores each file byte for byte; CRLF files keep CRLF;
  7. wikitext_check finds the planted structural errors, and none in fixed clean drafts;
  8. cite_builder --offline opens no network connection;
  9. speed on a ~0.5 MB article.
Writes bench/RESULTS.md and bench/results.json; exits 1 on any failure.
"""

from __future__ import annotations

import hashlib
import json
import platform
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent / "skills" / "fawiki-editor" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import cite_builder  # noqa: E402
from fa_lint import lint  # noqa: E402
from fawiki_common import __version__, find_protected_spans, try_mwparser  # noqa: E402
from wikitext_check import check  # noqa: E402

Z = "‌"

# --- fixture ------------------------------------------------------------------------
# (article name, text, planted fixes [(wrong, right)], traps [substring that must survive])
ARTICLES = [
    ("biography", (
        "{{جعبه اطلاعات زندگی‌نامه\n| نام = علی ي\n| زادروز = 1950\n| تصویر = Ali 1980.jpg\n}}\n"
        "'''علی نمونه''' (زادهٔ 1950) نویسنده و مترجم ايراني است كه در تهران به دنیا آمد.<ref>{{یادکرد وب"
        " | نشانی = https://example.org/ali?id=12,34 | عنوان = Ali 1950 | تاریخ بازبینی = 2024-01-02}}</ref>\n"
        "او می گوید که کتاب ها و مقاله های زیادی نوشته است , ولی بیشتر آن‌ها چاپ نشده‌اند .\n"
        "مهم ترین اثر او «( سفر )» است.<ref name=\"a\" /> او به میز کارش و میلاد مسیح اشاره کرده و کتابها را دوست دارد.\n"
        "{{عربی}}قال الشاعر: كتاب في يدي{{پایان عربی}}\n"
        "== منابع ==\n{{پانویس}}\n\n[[رده:نویسندگان ایرانی]]\n"),
     [("ايراني", "ایرانی"), ("كه", "که"), ("1950)", "۱۹۵۰)"), ("می گوید", f"می{Z}گوید"),
      ("کتاب ها", f"کتاب{Z}ها"), ("مقاله های", f"مقاله{Z}های"), ("است , ولی", "است، ولی"),
      ("نشده‌اند .", "نشده‌اند."), ("مهم ترین", f"مهم{Z}ترین"), ("«( سفر )»", "«(سفر)»")],
     ["| نام = علی ي", "| زادروز = 1950", "Ali 1980.jpg", "https://example.org/ali?id=12,34",
      "| عنوان = Ali 1950", "2024-01-02", "{{عربی}}قال الشاعر: كتاب في يدي{{پایان عربی}}",
      "میز", "میلاد", "کتابها", "بیشتر"]),
    ("city", (
        "'''شهر نمونه''' مرکز شهرستان نمونه در استان مركزي است و جمعیت آن 12,500 نفر است.\n"
        "{| class=\"wikitable\" style=\"width:50%\"\n|-\n! سال !! align=\"center\" | جمعیت\n|-\n"
        "| style=\"color:red\" | 1390 || 12000\n|}\n"
        "[[پرونده:Map 2010.png|بندانگشتی|نقشهٔ 2010]] [[كتاب|نام ها]] و [[کتاب]]" + Z + "ها در این شهر هست.\n"
        "<math>x^2 + 10, y</math> <nowiki>ي 12 می رود</nowiki> <!-- يادداشت 12 -->\n"
        " پیش‌قالب 12 ي\n"
        "مردم این شهر می‌گویند که 3.5 درصد از زمین‌ها زیر کشت است?\n"
        "== جستارهای وابسته ==\n* [[استان مرکزی]]\n== منابع ==\n{{پانویس}}\n[[رده:شهرها]]\n"),
     [("مركزي", "مرکزی"), ("12,500", "۱۲٬۵۰۰"), ("3.5 درصد", "۳٫۵ درصد"), ("است?", "است؟")],
     ["style=\"width:50%\"", "align=\"center\" |", "style=\"color:red\" |", "[[پرونده:Map 2010.png|بندانگشتی|نقشهٔ 2010]]",
      "[[كتاب|نام ها]]", f"[[کتاب]]{Z}ها", "<math>x^2 + 10, y</math>", "<nowiki>ي 12 می رود</nowiki>",
      "<!-- يادداشت 12 -->", " پیش‌قالب 12 ي"]),
    ("tech", (
        "'''نرم‌افزار نمونه''' برای Windows 10 و iPhone 15 ساخته شد و با COVID-19 و F-16 ربطی ندارد.\n"
        "He said: \"Hello, world? Yes; fine.\" و سپس رفت.\n"
        "نسخهٔ <code>v2.0 ي</code> در سال 2020 منتشر شد ؛ ISBN 978-3-16-148410-0 هم دارد.\n"
        "<syntaxhighlight lang=\"python\">a = 1 ; b = 2 ?</syntaxhighlight> ~~~~ __NOTOC__\n"
        "لباس تر شد و جام می ناب نوشید. حضرت فلانی گفت \"سلام\".\n"
        "[https://example.com/a,b برچسب ي 12]\n[[رده:نرم‌افزار]]\n"),
     [("سال 2020", "سال ۲۰۲۰"), ("شد ؛", "شد؛")],
     ["Windows 10", "iPhone 15", "COVID-19", "F-16", "He said: \"Hello, world? Yes; fine.\"",
      "<code>v2.0 ي</code>", "ISBN 978-3-16-148410-0", "<syntaxhighlight lang=\"python\">a = 1 ; b = 2 ?</syntaxhighlight>",
      "~~~~", "__NOTOC__", "لباس تر شد", "جام می ناب", "حضرت فلانی", "\"سلام\"", "[https://example.com/a,b برچسب ي 12]"]),
]
# Planted structural errors (wikitext_check must report these codes as errors)
BROKEN = ("کوه نمونه بلند است.<ref>بدون پایان\n\n== منابع ==\n{{پانویس}}\n[[پیوند ناقص\n", {"WC01", "WC03", "WC05", "WC06"})
# Warnings that must be reported (never applied)
EXPECTED_WARNINGS = {"tech": {"FW02", "FW03", "FW06"}}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def protected_chunks(text: str) -> list[str]:
    return [text[s:e] for s, e, _k in find_protected_spans(text)]


def inventory(text: str) -> tuple[list, list]:
    mw = try_mwparser()
    if mw:
        code = mw.parse(text)
        return ([str(t) for t in code.filter_templates(recursive=True)],
                [str(lk) for lk in code.filter_wikilinks(recursive=True)])
    return re.findall(r"\{\{[^{}]*\}\}", text), re.findall(r"\[\[[^\[\]]*\]\]", text)


def cli(*args, cwd) -> int:
    return subprocess.run([sys.executable, str(SCRIPTS / "fawiki.py"), *args], cwd=cwd,
                          capture_output=True, text=True, encoding="utf-8").returncode


def run() -> dict:
    checks: list[dict] = []

    def record(name: str, ok: bool, detail: str = "") -> None:
        checks.append({"check": name, "pass": bool(ok), "detail": detail})

    planted = fixed = traps = traps_ok = 0
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for name, text, fixes, trap_list in ARTICLES:
            f = tmp / f"{name}.wikitext"
            f.write_bytes(text.encode("utf-8"))
            original = f.read_bytes()
            code = cli("apply", f.name, cwd=tmp)
            out = f.read_bytes().decode("utf-8")
            record(f"{name}: apply exit 0", code == 0, f"exit {code}")
            for wrong, right in fixes:
                planted += 1
                ok = right in out and wrong not in out
                fixed += ok
                if not ok:
                    record(f"{name}: planted fix «{wrong}» → «{right}»", False)
            for t in trap_list:
                traps += 1
                ok = t in out
                traps_ok += ok
                if not ok:
                    record(f"{name}: trap untouched «{t}»", False)
            record(f"{name}: protected regions byte-identical",
                   protected_chunks(text) == protected_chunks(out))
            record(f"{name}: template/link inventory unchanged", inventory(text) == inventory(out))
            record(f"{name}: idempotent", lint(out).fixed == out)
            res = lint(text)
            want = EXPECTED_WARNINGS.get(name, set())
            got = {w["rule"] for w in res.warnings}
            if want:
                record(f"{name}: warnings reported, not applied", want <= got, f"got {sorted(got)}")
            errors = [i.code for i in check(out) if i.severity == "E"]
            if name != "tech":
                record(f"{name}: no structural errors after fix", not errors, ",".join(errors))
            code = cli("undo", f.name, cwd=tmp)
            record(f"{name}: undo byte-identical", code == 0 and f.read_bytes() == original)
            record(f"{name}: no leftovers after undo",
                   not list(tmp.glob(f"{name}.wikitext.fawiki*")))
        # CRLF
        f = tmp / "crlf.wikitext"
        f.write_bytes("خط ي 12\r\nخط ك\r\n".encode("utf-8"))
        before = f.read_bytes()
        cli("apply", f.name, cwd=tmp)
        after = f.read_bytes()
        record("crlf: line endings kept", after.count(b"\r\n") == 2 and b"\n" not in after.replace(b"\r\n", b""))
        cli("undo", f.name, cwd=tmp)
        record("crlf: undo byte-identical", f.read_bytes() == before)

    record(f"{len(ARTICLES)} articles: all planted fixes applied", fixed == planted, f"{fixed}/{planted}")
    record(f"{len(ARTICLES)} articles: all traps untouched", traps_ok == traps, f"{traps_ok}/{traps}")

    text, want = BROKEN
    got = {i.code for i in check(text) if i.severity == "E"}
    record("broken draft: planted structural errors found", want <= got, f"want {sorted(want)} got {sorted(got)}")

    # offline citation builder must not touch the network
    real_socket = socket.socket

    def no_net(*a, **k):
        raise AssertionError("network used")
    socket.socket = no_net  # type: ignore[assignment]
    try:
        tpl, _missing, _rec = cite_builder.build({"url": "https://example.org/x"}, "web", "2026-01-01")
        import contextlib
        import io
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            rc = cite_builder.main(["https://example.org/x", "--offline", "--json"])
        record("cite --offline: no network", rc == 0 and "{{یادکرد وب" in tpl)
    except AssertionError as e:
        record("cite --offline: no network", False, str(e))
    finally:
        socket.socket = real_socket

    big = "\n\n".join(a[1] for a in ARTICLES) * 60
    t0 = time.perf_counter()
    lint(big)
    secs = time.perf_counter() - t0
    record("speed: ~0.5 MB lints in under 20 s", secs < 20, f"{len(big.encode('utf-8')) / 1e6:.2f} MB in {secs:.2f} s")

    return {
        "version": __version__, "python": platform.python_version(), "os": platform.system(),
        "mwparserfromhell": bool(try_mwparser()), "planted_fixes": f"{fixed}/{planted}",
        "traps_untouched": f"{traps_ok}/{traps}", "lint_seconds_0_5MB": round(secs, 2),
        "passed": sum(c["pass"] for c in checks), "total": len(checks),
        "ok": all(c["pass"] for c in checks), "checks": checks,
    }


def write(results: dict) -> None:
    (HERE / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Synthetic benchmark results", "",
        f"fawiki-editor {results['version']} · Python {results['python']} · {results['os']} · "
        f"mwparserfromhell: {'yes' if results['mwparserfromhell'] else 'no'}", "",
        f"**{'PASS' if results['ok'] else 'FAIL'}: {results['passed']}/{results['total']} checks**", "",
        "| Metric | Value |", "|---|---|",
        f"| Planted errors fixed | {results['planted_fixes']} |",
        f"| Traps left untouched | {results['traps_untouched']} |",
        f"| Lint time, ~0.5 MB | {results['lint_seconds_0_5MB']} s |", "",
        "| Check | Result | Detail |", "|---|---|---|",
    ]
    lines += [f"| {c['check']} | {'pass' if c['pass'] else '**FAIL**'} | {c['detail']} |" for c in results["checks"]]
    (HERE / "RESULTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    r = run()
    write(r)
    for c in r["checks"]:
        if not c["pass"]:
            print(f"FAIL {c['check']} {c['detail']}")
    print(f"{'PASS' if r['ok'] else 'FAIL'} {r['passed']}/{r['total']}  fixes {r['planted_fixes']}  "
          f"traps {r['traps_untouched']}  lint 0.5MB {r['lint_seconds_0_5MB']}s")
    sys.exit(0 if r["ok"] else 1)
