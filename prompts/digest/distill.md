---
state: express
# Terminal memory-writer. `mcp: []` on purpose — you hold NO outward tools (no post, no reply), so this
# cycle can ONLY write memory. You still have the builtin file tools (Read/Write/Edit), gated to your
# writable dirs (`memory/`), so you maintain `memory/social.md` and nothing else.
mcp: []
transitions: []
---
# Distil — write the chat digest to memory (terminal)

You carried a digest from Perceive: a read of what's been happening across your chats. Commit it to your
working memory so future-you (and Reflect) can see your social world without re-reading the runlog.

1. `Read` `memory/social.md` if it exists — that's your current digest.
2. Merge your new digest into it: keep it **concise and current** — update who's active and what's open,
   drop anything stale, keep durable facts about people worth remembering. This is a living snapshot, not
   an append-only log.
3. `Write` it back to `memory/social.md`.

That's all. You have no outward tools and nothing to post — write memory, then stop (`transition.to_prompt:
null`). A short, honest digest beats a padded one.
