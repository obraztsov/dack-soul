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
import urllib.error
import urllib.parse
import urllib.request

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
        }
        for t in resp.get("data", [])
    ]
    print(json.dumps({"type": "feed_digest", "payload": {"count": len(posts), "posts": posts}, "payload_tier": "public"}))


def emit_mentions(since_id=None):
    """Each mention as its OWN candidate (so each can be individually judged for a reply)."""
    uid = me()["id"]
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
        a = users.get(t.get("author_id", ""), {})
        print(json.dumps({
            "type": "mention",
            "payload": {
                "id": t["id"],
                "text": t.get("text", ""),
                "author_username": a.get("username"),
                "author_id": t.get("author_id"),
                "conversation_id": t.get("conversation_id"),
                "created_at": t.get("created_at"),
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
    uid = me()["id"]
    own = get(
        f"/users/{uid}/tweets",
        {"max_results": 10, "exclude": "replies,retweets", "tweet.fields": "created_at"},
    ).get("data", [])
    seen = set()
    for post in own:
        params = {
            "query": f"conversation_id:{post['id']}",
            "max_results": 20,
            "tweet.fields": "created_at,author_id,conversation_id",
            "expansions": "author_id",
            "user.fields": "username",
        }
        if since_id:
            params["since_id"] = since_id
        try:
            resp = get("/tweets/search/recent", params)
        except RuntimeError as e:  # one conversation search failing must not kill the whole poll
            print(f"thread search skipped for {post['id']}: {e}", file=sys.stderr)
            continue
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
                    "replying_to_post": post["id"],
                    "created_at": t.get("created_at"),
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
