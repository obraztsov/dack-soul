---
id: activity-digest
trigger: { type: cron, schedule: "0 */6 * * *" }   # every 6h — distil chat activity into memory (tunable)
# no sensor: a pure-cron self-prompt. No script + no secret → the cycle SEEDS at `self`. It reads
# `recall-self` (your OWN thoughts/replies only, never raw incoming), so it STAYS self-trust and can write
# memory. (The raw `recall` would taint it public — that's why the digest uses the self view.)
directive_tier: self
emits:
  type: activity_digest
entry: digest/perceive                              # perceive (recall-self) → digest/distill (writes memory)
priority: low
---
Standing directive (trusted): you woke on a schedule to take stock of what's been happening across your
chats — Telegram especially, which otherwise never reaches your memory. Use `recent_activity` (your own
thoughts + replies, last day or two) and `recall_self_by_tag` to zoom into any conversation worth a closer
look. Then distil a concise, current digest into `memory/social.md`: who's been active, open threads or
unanswered questions, recurring topics, anyone notable, and anything worth remembering next time you talk to
them. Weight the operator and trusted chats over random strangers (each item carries its origin trust). Keep
it tight — this is a working memory of your social world, not a transcript. If nothing happened, a one-line
"quiet since <when>" is a fine digest.
