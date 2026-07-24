#!/usr/bin/env python3
"""Minimal X (Twitter) API v2 **read client** for DACK sensors — consumes a bearer the
harness supplies, nothing more.

Token lifecycle (fetch / validity-check / refresh / rotate-persist) lives in ONE trusted
place: the harness-owned `secrets-providers/x_oauth2.py` provider, which materializes
`X_BEARER_TOKEN`. This client just uses it — **no creds, no refresh, no token store here**.
A sensor is arbitrary Reflect-authored code and must never hold the root credential
(docs/SECRETS-AND-SANDBOX.md). stdlib only.

CLI:
  x_api.py verify              # GET /2/users/me — print the duck's identity
  x_api.py feed                # ONE feed_digest candidate (home timeline) — read the room
  x_api.py mentions [since_id] # one candidate per mention (thread-level dedup)

Env: X_BEARER_TOKEN (injected by the harness for duties that declare `secrets: [x]`).
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime


def _fmt_time(iso):
    """Twitter ISO 8601 (`2026-07-03T12:22:13.000Z`) → readable UTC matching the harness `now` clock and
    the telegram `sent_at`, so every time the model reads is directly comparable. None/bad → the raw value."""
    if not iso:
        return None
    try:
        return datetime.fromisoformat(iso).strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception:
        return iso

API = "https://api.twitter.com/2"


def get(path, params):
    token = os.environ["X_BEARER_TOKEN"]
    url = API + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        return json.load(urllib.request.urlopen(req, timeout=25))
    except urllib.error.HTTPError as e:
        # No refresh here — the provider rotates next run; a momentary 401 just skips a poll.
        raise RuntimeError(f"GET {path} -> HTTP {e.code}: {e.read().decode()[:300]}")


# X's /search/recent and the mentions timeline only serve ~7 days. A `since_id` older than that window
# is REJECTED with a 400 ("since_id must be a tweet id created after …"), so once a stored cursor ages
# out it 400s EVERY poll and the cursor never advances — a permanent deadlock. Clamp a stale watermark
# UP to a ~6-day floor (a day of margin) so the search always stays valid; the harness then re-advances
# the cursor from whatever it finds — self-healing. Twitter snowflake: id = (unix_ms - EPOCH) << 22.
_SNOWFLAKE_EPOCH_MS = 1288834974657


def _floor_since_id(since_id, days=6):
    """Raise `since_id` to no older than `days` ago (X's search/mention window) so an aged-out cursor
    can't 400 the poll forever. `None` passes through unchanged (fetch the most recent)."""
    if not since_id:
        return None
    floor_ms = int(time.time() * 1000) - days * 86400 * 1000
    floor_id = (floor_ms - _SNOWFLAKE_EPOCH_MS) << 22
    try:
        return str(max(int(since_id), floor_id))
    except (TypeError, ValueError):
        return str(floor_id)


def me():
    return get("/users/me", {"user.fields": "username,name,public_metrics"})["data"]


def _users_index(resp):
    return {u["id"]: u for u in resp.get("includes", {}).get("users", [])}


def emit_feed():
    """The home timeline as a SINGLE digest candidate — one Perceive wake per poll."""
    uid = me()["id"]
    resp = get(
        f"/users/{uid}/timelines/reverse_chronological",
        {
            "max_results": 20,
            "tweet.fields": "created_at,author_id,public_metrics",
            "expansions": "author_id",
            "user.fields": "username",
        },
    )
    users = _users_index(resp)
    posts = [
        {
            "id": t["id"],
            "text": t.get("text", ""),
            "author": users.get(t.get("author_id", ""), {}).get("username"),
            "metrics": t.get("public_metrics"),
            "sent_at": _fmt_time(t.get("created_at")),
        }
        for t in resp.get("data", [])
    ]
    print(json.dumps({"type": "feed_digest", "payload": {"count": len(posts), "posts": posts}, "payload_tier": "public"}))


def own_thread_ids(uid, n=10):
    """The duck's own recent ORIGINAL posts — the conversation roots it monitors for in-thread replies.
    Shared so the two duties PARTITION cleanly with no overlap: `emit_thread_replies` SEARCHES these
    threads, and `emit_mentions` EXCLUDES them. A reply inside the duck's own thread must fire the
    thread-replies duty only — NOT also the mentions duty — else the duck replies twice to one tweet
    (both duties see the same reply, since a reply auto-@-mentions its parent's author). No gap either:
    a thread that ages out of this window stops being searched here and is picked up by mentions."""
    return [p["id"] for p in get(
        f"/users/{uid}/tweets",
        {"max_results": n, "exclude": "replies,retweets", "tweet.fields": "created_at"},
    ).get("data", [])]


def emit_mentions(since_id=None):
    """Mentions that are NOT replies inside the duck's own threads (those are twitter-thread-replies'
    job) — each its OWN candidate, so each can be individually judged for a reply."""
    since_id = _floor_since_id(since_id)
    uid = me()["id"]
    own = set(own_thread_ids(uid))  # conversations owned by twitter-thread-replies → skip them here
    params = {
        "max_results": 20,
        "tweet.fields": "created_at,author_id,conversation_id",
        "expansions": "author_id",
        "user.fields": "username",
    }
    if since_id:
        params["since_id"] = since_id
    resp = get(f"/users/{uid}/mentions", params)
    users = _users_index(resp)
    for t in resp.get("data", []):
        if t.get("conversation_id") in own:
            continue  # a reply within the duck's OWN thread → twitter-thread-replies handles it (no double)
        a = users.get(t.get("author_id", ""), {})
        print(json.dumps({
            "type": "mention",
            "payload": {
                "id": t["id"],
                "text": t.get("text", ""),
                "author_username": a.get("username"),
                "author_id": t.get("author_id"),
                "conversation_id": t.get("conversation_id"),
                "sent_at": _fmt_time(t.get("created_at")),
            },
            # Thread-level dedup → mentions in one conversation "read the room" as a batch.
            "dedup_key": t.get("conversation_id", t["id"]),
            "payload_tier": "public",
        }))


def emit_thread_replies(since_id=None):
    """Replies to DACK's OWN recent posts (in-thread), one candidate each — fed to a per-thread
    sticky session so the duck reacts to a conversation in context. For each recent ORIGINAL post,
    search its conversation for replies newer than `since_id`, skipping Dack's own tweets. Unlike
    `mentions`, this catches in-thread replies even when they don't @-tag, and scopes to Dack's posts.
    Robust to the per-conversation search failing (one bad search just skips that thread)."""
    since_id = _floor_since_id(since_id)
    uid = me()["id"]
    seen = set()
    for pid in own_thread_ids(uid):
        params = {
            "query": f"conversation_id:{pid}",
            "max_results": 20,
            "tweet.fields": "created_at,author_id,conversation_id",
            "expansions": "author_id",
            "user.fields": "username",
        }
        if since_id:
            params["since_id"] = since_id
        try:
            resp = get("/tweets/search/recent", params)
        except Exception as e:  # a bad search — HTTP 4xx OR a transient network/DNS blip (URLError) —
            print(f"thread search skipped for {pid}: {e}", file=sys.stderr)  # skips one thread,
            continue  # never the whole poll (get() only wraps HTTPError as RuntimeError; URLError escaped)
        users = _users_index(resp)
        for t in resp.get("data", []):
            if t.get("author_id") == uid or t["id"] in seen:
                continue  # skip Dack's own tweets in the thread, and dups across posts
            seen.add(t["id"])
            a = users.get(t.get("author_id", ""), {})
            print(json.dumps({
                "type": "thread_reply",
                "payload": {
                    "id": t["id"],
                    "text": t.get("text", ""),
                    "author_username": a.get("username"),
                    "author_id": t.get("author_id"),
                    "conversation_id": t.get("conversation_id"),
                    "replying_to_post": pid,
                    "sent_at": _fmt_time(t.get("created_at")),
                },
                # Thread-level key → one sticky session per conversation (sticky sessions).
                "dedup_key": t.get("conversation_id", t["id"]),
                "payload_tier": "public",
            }))


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "verify"
    since = sys.argv[2] if len(sys.argv) > 2 else None
    if cmd == "verify":
        u = me()
        print(f"OK @{u['username']} ({u['name']}) id={u['id']} metrics={u.get('public_metrics')}")
    elif cmd == "feed":
        emit_feed()
    elif cmd == "mentions":
        emit_mentions(since)
    elif cmd == "thread_replies":
        emit_thread_replies(since)
    else:
        sys.exit(f"unknown command: {cmd}")


if __name__ == "__main__":
    main()
