#!/usr/bin/env python3
"""twitter-mentions sensor (PRD §5.2) — a PURE PERCEIVER.

Contract:
  - stdin:  trigger payload (empty for cron).
  - stdout: newline-delimited JSON candidates: {type, payload, dedup_key, payload_tier?}.
  - exit:   0 = success; non-zero = logged failure, no rows registered.

INVARIANT (enforced by the harness, restated so it never drifts): this sensor may only
READ. It polls owned mentions and emits them as candidates. It must NEVER post or mutate
state — if it needed a write/wallet credential it would be an action wearing a sensor's
clothes (§5.2). It shares the duck's RW token (we have one key), but **only GETs** — it is
behaviour, not the key, that makes a sensor a sensor.

Python (not shell) deliberately: it handles untrusted tweet text, so it PARSES rather than
string-interpolates (a shell sensor interpolating tweet bodies would itself be an injection
surface BELOW the firebreak, §5.2).

Read-scoped env (injected by the harness, §8.2):
  X_BEARER_TOKEN — materialized by the harness's `x` secrets provider (declare `secrets: [x]`).
  DACK_SINCE_ID  — cross-poll dedup watermark (PRD §10.2): the harness injects the highest
                   mention id it has already seen, so we fetch ONLY newer mentions (X `since_id`)
                   and never re-surface — and never re-reply to — one already handled. Absent on
                   the first poll. Declared via the duty's `cursor:` frontmatter.
"""
import os
import sys

# Reach the shared X API client in the twitter skill (works regardless of cwd).
sys.path.insert(
    0,
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "skills", "twitter", "scripts"),
)
import x_api  # noqa: E402


def main() -> int:
    if not os.environ.get("X_BEARER_TOKEN"):
        print("missing X_BEARER_TOKEN (declare `secrets: [x]` so the harness injects it)", file=sys.stderr)
        return 1
    try:
        # since_id = the harness-injected watermark (None on first poll) → only newer mentions.
        since_id = os.environ.get("DACK_SINCE_ID") or None
        x_api.emit_mentions(since_id=since_id)  # one candidate per mention; thread-level dedup_key
    except Exception as e:  # noqa: BLE001 — any failure → non-zero, no rows.
        print(f"fetch failed: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
