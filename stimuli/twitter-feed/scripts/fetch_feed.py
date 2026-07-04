#!/usr/bin/env python3
"""twitter-feed sensor — a PURE PERCEIVER.

Reads the duck's home timeline (the accounts it follows) and emits it as a SINGLE
`feed_digest` candidate — one "read the feed" Perceive per poll. Read-only behaviour; it
shares the RW token but only GETs. Untrusted tweet text is parsed, never interpolated.

Read-scoped env (forwarded by the harness):
  X_BEARER_TOKEN — materialized by the harness's `x` secrets provider (declare `secrets: [x]`).
"""
import os
import sys

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
        x_api.emit_feed()  # one feed_digest candidate (all posts batched)
    except Exception as e:  # noqa: BLE001 — any failure → non-zero, no rows.
        print(f"fetch failed: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
