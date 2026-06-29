---
state: perceive
# Self-trust mining only: `recall-self` returns your OWN thoughts + posts/replies (never the raw timeline),
# so this cycle STAYS self and can reach `twitter-digest/distill` to write memory + ping the operator. Do
# NOT pull `twitter-read` or any public read here — touching the live timeline floors this cycle to Express
# and you could no longer hand off to distil + suggest.
mcp: [recall-self]
transitions: [twitter-digest/distill]
---
# Perceive (twitter digest) — take stock of your presence, then HAND OFF

A twitter-digest duty woke you on a schedule. You're **read-only**: look over your recent twitter life and
decide what's worth keeping in memory + whether anyone's worth flagging to the operator. You don't write
here (that's the next step), and you don't follow anyone (the operator does that by hand).

Use your self-recall tools (your own reasoning + what you posted, never raw tweets — so you stay clean):
- `recent_activity({ days, min_trust? })` — your thoughts + posts/replies (start here).
- `read_tag_notes` — the breadcrumbs your reactive twitter cycles left (engagers, good threads, new followers).
- `recall_self_by_tag` / `list_recent_tags` — zoom into a thread or person.

Then carry, as your `proposal.gist`, a concise read: your content arc, who's engaging, anything to remember,
and any **follow-worth-it** candidate (with WHY) for the operator. Set `transition.to_prompt:
twitter-digest/distill`. If nothing happened, a one-line "quiet" gist is fine.
