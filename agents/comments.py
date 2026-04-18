"""
Comment-to-DM lead magnet system.
Monitors recent posts, detects "PROFESOR" keyword in comments,
sends a public reply + DM with the relevant guide link.
"""

import json
import time
from pathlib import Path

import requests

import config
from agents.humanizer import generate_comment_reply, generate_dm_message

BASE = config.INSTAGRAM_API_BASE
_REPLIED_PATH = Path(__file__).parent.parent / ".replied_comments.json"

# Maps topic keywords (from post captions) to guide URLs
GUIDE_URLS = {
    "skills":       "https://claudeprofessor.page/guides/skills",
    "mcp":          "https://claudeprofessor.page/guides/mcp",
    "modelos":      "https://claudeprofessor.page/guides/modelos",
    "claude code":  "https://claudeprofessor.page/guides/claude-code",
    "opus":         "https://claudeprofessor.page/guides/modelos",
    "routines":     "https://claudeprofessor.page/guides/skills",
    "design":       "https://claudeprofessor.page/guides/claude-code",
}
DEFAULT_GUIDE_URL = "https://claudeprofessor.page/guides/skills"


def _token() -> str:
    return config.INSTAGRAM_ACCESS_TOKEN


def _uid() -> str:
    return config.INSTAGRAM_USER_ID


def _get(endpoint: str, **params) -> dict:
    params["access_token"] = _token()
    resp = requests.get(f"{BASE}/{endpoint}", params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def _post(endpoint: str, **params) -> dict:
    params["access_token"] = _token()
    resp = requests.post(f"{BASE}/{endpoint}", params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if "error" in data:
        raise RuntimeError(f"Instagram API error: {data['error']}")
    return data


def _load_replied() -> set:
    if _REPLIED_PATH.exists():
        return set(json.loads(_REPLIED_PATH.read_text(encoding="utf-8")))
    return set()


def _save_replied(ids: set) -> None:
    _REPLIED_PATH.write_text(json.dumps(list(ids)), encoding="utf-8")


def get_recent_media(limit: int = 10) -> list[dict]:
    """Return list of recent posts: [{id, caption, timestamp}]."""
    data = _get(
        f"{_uid()}/media",
        fields="id,caption,timestamp",
        limit=limit,
    )
    return data.get("data", [])


def get_comments(media_id: str) -> list[dict]:
    """Return comments on a media: [{id, text, username, timestamp, from}]."""
    data = _get(
        f"{media_id}/comments",
        fields="id,text,username,timestamp,from",
    )
    return data.get("data", [])


def reply_to_comment(comment_id: str, message: str) -> str:
    """Post a public reply to a comment. Returns reply ID."""
    data = _post(f"{comment_id}/replies", message=message)
    return data.get("id", "")


def send_dm(ig_user_id: str, message: str) -> bool:
    """Send a DM to a user via Messenger API. Returns True on success."""
    try:
        _post(
            f"{_uid()}/messages",
            recipient=json.dumps({"id": ig_user_id}),
            message=json.dumps({"text": message}),
        )
        return True
    except Exception as e:
        print(f"  DM failed for {ig_user_id}: {e}")
        return False


def _pick_guide_url(caption: str) -> str:
    caption_lower = (caption or "").lower()
    for keyword, url in GUIDE_URLS.items():
        if keyword in caption_lower:
            return url
    return DEFAULT_GUIDE_URL


def process_comments(dry_run: bool = False) -> int:
    """
    Check last 10 posts for comments containing 'profesor'.
    For each new match: reply publicly + send DM with guide.
    Returns count of processed comments.
    """
    replied = _load_replied()
    processed = 0

    media_list = get_recent_media()
    print(f"Checking {len(media_list)} recent posts...")

    for media in media_list:
        media_id = media["id"]
        caption = media.get("caption", "")
        guide_url = _pick_guide_url(caption)

        comments = get_comments(media_id)
        for comment in comments:
            comment_id = comment["id"]
            if comment_id in replied:
                continue

            text = comment.get("text", "").lower()
            if "profesor" not in text:
                continue

            username = comment.get("username", "usuario")
            from_data = comment.get("from", {})
            user_id = from_data.get("id", "")

            print(f"  Match: @{username} on media {media_id}")

            if not dry_run:
                # Public comment reply
                reply_text = generate_comment_reply(username)
                try:
                    reply_id = reply_to_comment(comment_id, reply_text)
                    print(f"    Replied: {reply_id}")
                except Exception as e:
                    print(f"    Reply failed: {e}")

                # DM with guide
                if user_id:
                    dm_text = generate_dm_message(username, guide_url, caption)
                    ok = send_dm(user_id, dm_text)
                    print(f"    DM: {'sent' if ok else 'failed'}")
                else:
                    print("    DM skipped: no user ID in comment data")

                # Rate limit headroom
                time.sleep(2)

            replied.add(comment_id)
            processed += 1

    if not dry_run:
        _save_replied(replied)

    print(f"Done. Processed {processed} new comments.")
    return processed
