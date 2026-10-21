#!/usr/bin/env python3
"""Build the README charts as SVG (light + dark) from the benchmark JSON files.

- Colors: blue vs neutral grey (distinguishable with every common color-vision deficiency),
  checked here for WCAG contrast against GitHub's light (#ffffff) and dark (#0d1117)
  backgrounds: >= 3:1 for bars, >= 4.5:1 for text. The script fails if a pair falls short.
- Every bar carries its value; single-series charts have no legend.
- Text-fit guard: label widths are measured with a real font (DejaVu Sans, wider than the
  usual GitHub UI fonts) and the script fails if a label would overflow its slot.

Usage: python bench/charts.py   (reads bench/*.json, writes assets/charts/*.svg)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "charts"
THEMES = {
    "light": {"bg": "#ffffff", "text": "#1f2328", "muted": "#59636e", "grid": "#d1d9e0",
              "a": "#0969da", "b": "#6e7781"},
    "dark": {"bg": "#0d1117", "text": "#e6edf3", "muted": "#9198a1", "grid": "#30363d",
             "a": "#4493f8", "b": "#8b949e"},
}
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"


def _lum(hex_color: str) -> float:
    def ch(c: float) -> float:
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(c1: str, c2: str) -> float:
    a, b = sorted((_lum(c1), _lum(c2)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def check_palette() -> list[str]:
    problems = []
    for name, t in THEMES.items():
        for key, need in (("a", 3), ("b", 3), ("text", 4.5), ("muted", 4.5)):
            r = contrast(t[key], t["bg"])
            if r < need:
                problems.append(f"{name}: {key} {t[key]} on {t['bg']} = {r:.2f} < {need}")
    return problems


try:
    from PIL import ImageFont
    _FONT = ImageFont.truetype("DejaVuSans.ttf", 100)
except (ImportError, OSError):  # pragma: no cover
    _FONT = None


def text_width(s: str, size: float) -> float:
    if _FONT is None:
        return len(s) * size * 0.62  # conservative fallback
    return _FONT.getlength(s) * size / 100


def fit(s: str, size: float, room: float) -> str:
    w = text_width(s, size)
    if w > room:
        raise SystemExit(f"text-fit guard: «{s}» needs {w:.0f}px, has {room:.0f}px")
    return escape(s)


def hbar_chart(title: str, subtitle: str, rows: list[tuple[str, list[float]]], series: list[str],
               unit: str, vmax: float, theme: str, value_labels: list[list[str]] | None = None) -> str:
    t = THEMES[theme]
    colors = [t["a"], t["b"]][: len(series)]
    label_w, width, bar_h, gap, group_gap = 190, 760, 22, 6, 22
    plot_x, plot_w = label_w + 20, width - label_w - 90
    top = 78 + (26 if len(series) > 1 else 0)
    group_h = len(series) * bar_h + (len(series) - 1) * gap
    height = top + len(rows) * (group_h + group_gap) + 10
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
           f'font-family="{FONT}" role="img" aria-label="{escape(title)}">',
           f'<rect width="100%" height="100%" fill="{t["bg"]}" rx="8"/>',
           f'<text x="20" y="32" font-size="18" font-weight="600" fill="{t["text"]}">{fit(title, 18, width - 40)}</text>',
           f'<text x="20" y="56" font-size="13" fill="{t["muted"]}">{fit(subtitle, 13, width - 40)}</text>']
    if len(series) > 1:
        x = 20
        for name, col in zip(series, colors):
            out.append(f'<rect x="{x}" y="{70}" width="12" height="12" rx="2" fill="{col}"/>')
            out.append(f'<text x="{x + 18}" y="{81}" font-size="13" fill="{t["text"]}">{fit(name, 13, 220)}</text>')
            x += 30 + text_width(name, 13) + 20
    for frac in (0, 0.5, 1):
        gx = plot_x + plot_w * frac
        out.append(f'<line x1="{gx:.1f}" y1="{top - 6}" x2="{gx:.1f}" y2="{height - 12}" stroke="{t["grid"]}" stroke-width="1"/>')
    y = top
    for r_i, (label, values) in enumerate(rows):
        out.append(f'<text x="{label_w}" y="{y + group_h / 2 + 5:.1f}" font-size="14" text-anchor="end" '
                   f'fill="{t["text"]}">{fit(label, 14, label_w - 20)}</text>')
        for i, v in enumerate(values):
            by = y + i * (bar_h + gap)
            w = max(plot_w * v / vmax, 2)
            val = value_labels[r_i][i] if value_labels else f"{v:g}{unit}"
            out.append(f'<rect x="{plot_x}" y="{by}" width="{w:.1f}" height="{bar_h}" rx="3" fill="{colors[i]}"/>')
            out.append(f'<text x="{plot_x + w + 8:.1f}" y="{by + bar_h / 2 + 5:.1f}" font-size="13" font-weight="600" '
                       f'fill="{t["text"]}">{fit(val, 13, width - plot_x - w - 12)}</text>')
        y += group_h + group_gap
    out.append("</svg>")
    return "\n".join(out)


def main() -> int:
    problems = check_palette()
    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
    OUT.mkdir(parents=True, exist_ok=True)
    agents = json.loads((ROOT / "bench" / "agents-results.json").read_text(encoding="utf-8"))
    real = json.loads((ROOT / "bench" / "realworld-results.json").read_text(encoding="utf-8"))
    names = {"write": "Write an article", "review": "Review a draft", "translate": "Translate en→fa"}
    rows = [(names[k], [round(100 * v["with_skill"]["pass_rate"]), round(100 * v["without_skill"]["pass_rate"])])
            for k, v in agents["by_task"].items() if "with_skill" in v and "without_skill" in v]
    ov = agents["overall"]
    rows.append(("All tasks", [round(100 * ov["with_skill"]["pass_rate"]), round(100 * ov["without_skill"]["pass_rate"])]))
    reps = max(v["with_skill"]["runs"] for v in agents["by_task"].values())
    versions = list(real["versions"].items())
    wrong_rows = [(("before fixes" if "pre" in k else k), [v["labels"].get("wrong", 0)]) for k, v in versions]
    wrong_labels = [[f"{v['labels'].get('wrong', 0)} of {v['changes']} changes ({v['wrong_pct']:g}%)"] for _k, v in versions]
    for theme in THEMES:
        (OUT / f"agents-{theme}.svg").write_text(hbar_chart(
            "Does it help agents? Checks passed per task",
            f"Headless claude -p runs, same prompt and tools, {reps} reps per task and setting",
            rows, ["with fawiki-editor", "without the skill"], "%", 100, theme), encoding="utf-8")
        (OUT / f"realworld-{theme}.svg").write_text(hbar_chart(
            "Wrong automatic fixes on 88 real fa.wiki articles",
            "Every change labeled by hand (bench/label.py); lower is better",
            wrong_rows, ["wrong"], "", max(1, max(r[1][0] for r in wrong_rows)) * 1.6, theme, wrong_labels),
            encoding="utf-8")
    print(f"wrote {len(list(OUT.glob('*.svg')))} SVG files to {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
