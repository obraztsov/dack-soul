#!/usr/bin/env python3
"""twitter-thread-replies sensor — a PURE PERCEIVER (PRD §5.2).

Emits in-thread replies to DACK's OWN recent posts (one candidate per reply), each keyed by
`conversation_id` so the harness feeds it to a per-thread STICKY session (the duck reacts to a
conversation in context). Same READ-only invariant as the mentions sensor: it only GETs the X API,
never posts or mutates; it PARSES untrusted reply text rather than interpolating it.

Read-scoped env (injected by the harness for duties that declare `secrets: [x]`):
  X_BEARER_TOKEN     — materialized by the `x` secrets provider.
  DACK_THREAD_SINCE_ID — cross-poll watermark (the duty's `cursor:`); only replies newer than this
                         are surfaced, so a thread reply is never re-processed.
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
        since_id = os.environ.get("DACK_THREAD_SINCE_ID") or None
        x_api.emit_thread_replies(since_id=since_id)  # one candidate per reply; conversation dedup_key
    except Exception as e:  # noqa: BLE001 — any failure → non-zero, no rows.
        print(f"fetch failed: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
