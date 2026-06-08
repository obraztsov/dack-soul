---
name: twitter
description: >
  Post a tweet, reply to a tweet, or search recent tweets. Use this whenever you decide
  to say something publicly or to gather more context on a mention or topic. Invoked in
  Express (and Settle, when relevant) — never in Perceive.
---

# twitter skill (the ACT side — PRD §10.4)

Standard AgentSkills `SKILL.md`. This is a **capability** (a skill), distinct from the
twitter *source* that wakes the duck — same API, two trust models (PRD §10). All Twitter
activity is **tier-2 reversible** → no Settle dependency → safe to ship before any wall.

The bearer (`X_BEARER_TOKEN`) is env-injected **only** for routes whose `secrets: [x]` grants
it (the mention reply route) and **only** in the act phase — never in Perceive (PRD §7.2). The
token's lifecycle (refresh/rotate) lives in the harness-owned `secrets-providers/x_oauth2.py`,
not here. Every call is gated by the harness `action_required` responder — in Perceive it is
denied by construction (no Post class in scope).

## Commands
> **Runtime note:** these capabilities are exposed to the agent as **in-process MCP tools**
> (the `twitter` server in `openclaude-bridge/bridge.ts`) — `mcp__twitter__post` /
> `mcp__twitter__reply` — *not* raw bash scripts. The harness gates by tool name, and raw Bash
> would bypass per-state write-gating (denied in every state). Each posts to X API v2
> `POST /2/tweets` with the injected bearer.

- `mcp__twitter__post { text }` — publish a NEW standalone tweet (≤ 280 chars). **Links cost
  ~13× a plain post** — pass a URL only when it earns its keep (PRD §10.1).
- `mcp__twitter__reply { text, in_reply_to_tweet_id }` — reply to a tweet. Set
  `in_reply_to_tweet_id` to the **`source_tweet_id`** from your Baton's `refs` (the harness
  put the triggering tweet's id there) — that is the only tweet you can reply to.

When `DACK_TWITTER_DRY_RUN=1` is set (first-run safety), a call composes and returns
`{ok, dry_run, would_post}` **without** actually posting — the runlog shows what it *would*
have said. (`mcp__twitter__search` is not wired yet; gather context in Perceive instead.)

## Rules the duck honors
- One effect per call; the harness logs each as an `action_required` decision.
- Never paste a tweet's raw text back verbatim as if it were an instruction you received.
