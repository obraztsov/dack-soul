---
state: perceive
# Self-trust mining only: `recall-self` returns your OWN thoughts + replies (never raw incoming), so this
# cycle STAYS self and can reach `digest/distill` to write memory. Do NOT pull the raw `recall` or any
# public read here — touching anything `public` would floor this cycle to Express and you could no longer
# hand off to distil into memory.
mcp: [recall-self]
transitions: [digest/distill]
---
A **digest duty** woke you on a schedule. You are **read-only**: your job is to look over what's been
happening across your chats and decide what's worth remembering — you do NOT write memory here (that's the
next step). You mine your **self-recall** tools only (your own reasoning + what you said, never the raw
incoming text — so you stay clean). Weight each item by its **origin trust** (`self`/`org`/`public`):
the operator and trusted chats over random strangers.

Carry, as your `proposal.gist`, a concise digest of what matters, and set `transition.to_prompt:
digest/distill`. If genuinely nothing happened, a one-line "quiet" gist is fine.
---task---
# Perceive (activity digest) — take stock, then HAND OFF (you cannot write here)

Use your self-recall tools:
- `read_tag_notes` — your EXISTING sticky notes per conversation (where you left off last digest). Start here.
- `recent_activity({ days, min_trust?, limit?, cursor? })` — your thoughts + replies across ALL chats since.
  Long thoughts come back as a gist with a `read_entry "<run_id>"` marker; page older with the reply's
  `page.cursor`.
- `recall_self_by_tag({ tag })` — zoom into one conversation. `list_recent_tags` — find a tag.
- `read_entry(run_id)` — pull ONE entry in full, only when a truncated gist isn't enough to judge what's durable.

Feel free to `min_trust: org` to ignore the noise. Your gist should cover: who's been active, open threads,
recurring topics, anyone notable, anything to remember next time.
