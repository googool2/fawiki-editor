LLM-written Persian Wikipedia drafts keep getting reverted for the same reasons: Arabic ي/ك,
missing half-spaces, English templates, invented citations.

I built fawiki-editor, a Claude skill that gives the model fa.wiki's own rules plus
deterministic tools:

• 88 real fa.wiki articles, every automatic fix labeled by hand: 0 wrong of 742 (12 wrong of
  759 before the rehearsal taught us four edge cases)
• headless agent runs: 100% of checks passed with the skill vs 77% without
• templates, links, refs and URLs are never touched; undo restores files byte for byte
• CI on Linux, macOS and Windows

Honest part: the first round missed my +20 target because the skill skipped notability
verdicts; I fixed and re-measured it, but it still costs about 2x the tokens. No native fa.wiki editor has reviewed it yet; corrections welcome.

Install in Claude Code:
/plugin marketplace add googool2/fawiki-editor

Link in the first comment.
