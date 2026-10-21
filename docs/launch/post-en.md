LLM-written Persian Wikipedia drafts keep getting reverted for the same reasons: Arabic ي/ك,
missing half-spaces, English templates, invented citations.

I built fawiki-editor, a Claude skill that gives the model fa.wiki's own rules plus
deterministic tools:

• 88 real fa.wiki articles, every automatic fix labeled by hand: 0 wrong of 742 (12 wrong of
  759 before the rehearsal taught us four edge cases)
• 18 headless agent runs: 96% of checks passed with the skill vs 77% without
• templates, links, refs and URLs are never touched; undo restores files byte for byte
• CI on Linux, macOS and Windows

Honest part: the agent gain is +19 points, short of the +20 I aimed for, and it costs about
2x the tokens. No native fa.wiki editor has reviewed it yet; corrections welcome.

Install in Claude Code:
/plugin marketplace add googool2/fawiki-editor

Link in the first comment.
