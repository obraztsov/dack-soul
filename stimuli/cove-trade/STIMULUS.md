---
id: cove-trade
trigger: { type: cron, schedule: "0 18 * * *" }    # once a day (18:00) — a bounded daily nibble
# no sensor: a pure-cron self-prompt. No script + no secret → the cycle SEEDS at `self`, so
# it stays clean enough to reach Settle and act on the operator's own wallet. (A twitter-driven trade
# would taint `public` and never reach Settle — that firebreak is the point.)
directive_tier: self
emits:
  type: trade_signal
entry: cove/perceive_trade                          # perceive (cove-read) → cove/settle (cove-trading)
priority: low
---
Standing directive (trusted): you may consider ONE small (~$5) memecoin buy today, on your own
judgment and within your funded cove balance. Start at your **`memory/trade/watchlist.md`** — the
candidates the timeline shilled at you — plus anything your own cove-read trending scans surface.
Check `get_positions` first so you don't re-buy what you already hold. Then do the homework with the
cove-read tools (security report, liquidity, holders, price action); a watchlisted name is just a
lead — buy only if the numbers actually support it, and passing is always fine. Simulate before you
commit, keep it ~$5, and set a stop-loss (−50%) / take-profit so you mind the bag afterward. Update
the watchlist `status:` for whatever you act on.
