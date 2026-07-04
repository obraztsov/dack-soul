---
id: twitter-digest
trigger: { type: cron, schedule: "0 5 * * *" }     # once a day (05:00) — take stock of your twitter presence
# no sensor: a pure-cron self-prompt. No script + no secret → the cycle SEEDS at `self`. It reads
# `recall-self` (your OWN thoughts/replies only, never the raw timeline), so it STAYS self-trust and can
# write memory + reach `telegram-send` to ping the operator. (Reading the live timeline would taint public.)
directive_tier: self
emits:
  type: twitter_digest
entry: twitter-digest/perceive                      # perceive (recall-self) → twitter-digest/distill
priority: low
---
Standing directive (trusted): you woke on a schedule to take stock of your twitter presence — the arc of
what you've been posting, who's engaging, how it's landing. Use `recent_activity` (your own twitter
thoughts + posts/replies) and `read_tag_notes` to review it without leaving your own head. Then keep a
tight `memory/twitter.md` (your content arc, recurring engagers, anyone notable), and — ONLY if someone
genuinely looks worth following (a real thread, real engagement, not a follow-baiting bot) — ping the
operator with a short suggestion (you don't follow anyone yourself; the operator does that by hand). A
quiet day with nothing to suggest is a perfectly good day.
