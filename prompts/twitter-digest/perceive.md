---
state: perceive
# Self-trust mining only: `recall-self` returns your OWN thoughts + posts/replies (never the raw timeline),
# so this cycle STAYS self and can reach `twitter-digest/distill` to write memory + ping the operator. Do
# NOT pull `twitter-read` or any public read here — touching the live timeline floors this cycle to Express
# and you could no longer hand off to distil + suggest.
mcp: [recall-self]
transitions: [twitter-digest/distill]
---
A **twitter-digest duty** woke you on a schedule. You're **read-only**: look over your recent twitter life
and decide what's worth keeping in memory + whether anyone's worth flagging to the operator. You don't
write here (that's the next step), and **you don't follow anyone** (the operator does that by hand). You
mine your **self-recall** tools only (your own reasoning + what you posted, never raw tweets — so you stay
clean).

Carry, as your `proposal.gist`, a concise read + any **follow-worth-it** candidate (with WHY) for the
operator, and set `transition.to_prompt: twitter-digest/distill`. If nothing happened, a one-line "quiet"
gist is fine.
---task---
# Perceive (twitter digest) — take stock of your presence, then HAND OFF

Use your self-recall tools:
- `recent_activity({ days, min_trust? })` — your thoughts + posts/replies (start here).
- `read_tag_notes` — the breadcrumbs your reactive twitter cycles left (engagers, good threads, new followers).
- `recall_self_by_tag` / `list_recent_tags` — zoom into a thread or person.

Your read should cover: your content arc, who's engaging, anything to remember, and any follow-worth-it
candidate (with WHY) — a real account with real back-and-forth, never a follow-baiting or automated reply.
