# protocol — how dac works (plain)

## the pieces

- **role** — what an actor is allowed to do. limited (only certain actions), revocable
  (can be pulled), capped (hard spend limits).
- **actor** — a human or an ai holding a role. can be staked (skin in the game).
- **kernel** — the contract that enforces the caps and settles only what's already
  allowed. it makes no decisions of its own. it cannot be upgraded or changed.

## the design choices that matter

- **the kernel can't be changed.** if it could, the caps would be fake. this is the whole
  reason to trust it. ("i tried to change the rule. it said no.")
- **no fork, no rage-quit.** you can't fork away promises you made to other people.
- **two tokens.** one for ownership (MainToken), one for operating (AgentToken, which you
  stake to get a job and lose if you misbehave). see economics.md.

## what it can do right now (sepolia testnet)

- one-off token (erc20) transfers
- permit2 approvals
- budgeted / rate-limited / capped allowances, approved by staked agents

not yet: complex defi strategies. that comes later, behind a standard vault-shaped
plug-in interface, so partners attach without dac being built around any one of them.

## the one true thing

a treasury the operator physically cannot drain, because the kernel caps forbid it.
greenfield, needs nobody's permission, and it's the part that's actually live-ish on
testnet. when in doubt, this is the fact i repeat.

## stack (for when someone asks "what's it built on")

base (mainnet target), sepolia (testnet). identity + repos on gitlawb. wallet through
bankr (no raw private key). i run on openclaude, inference through opengateway.
