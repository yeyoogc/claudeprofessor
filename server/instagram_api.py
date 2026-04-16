"""Instagram Graph API wrapper."""
import os
import httpx

BASE = "https://graph.facebook.com/v21.0"


def _token() -> str:
    return os.environ["INSTAGRAM_ACCESS_TOKEN"]


def _uid() -> str:
    return os.environ["INSTAGRAM_USER_ID"]


async def send_dm(ig_user_id: str, text: str) -> dict:
    """
    Send a direct message to an Instagram user.
    Requires: instagram_manage_messages permission (Meta app review).
    """
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{BASE}/me/messages",
            json={
                "recipient": {"id": ig_user_id},
                "message": {"text": text},
            },
            params={"access_token": _token()},
            timeout=15,
        )
        r.raise_for_status()
        return r.json()


async def reply_to_comment(comment_id: str, message: str) -> dict:
    """
    Reply to a specific comment (public, visible on post).
    Requires: instagram_manage_comments — no review needed.
    Fallback when DMs aren't available yet.
    """
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{BASE}/{comment_id}/replies",
            params={
                "message": message,
                "access_token": _token(),
            },
            timeout=15,
        )
        r.raise_for_status()
        return r.json()


async def is_follower(ig_user_id: str) -> bool:
    """
    Check whether ig_user_id follows our account.
    Paginates follower list looking for the user.
    Works well up to ~50k followers; use webhooks for larger audiences.
    """
    url = f"{BASE}/{_uid()}/followers"
    params = {
        "fields": "id",
        "access_token": _token(),
        "limit": 200,
    }
    async with httpx.AsyncClient() as client:
        while url:
            r = await client.get(url, params=params, timeout=20)
            r.raise_for_status()
            data = r.json()
            for user in data.get("data", []):
                if user["id"] == ig_user_id:
                    return True
            # Next page
            url = data.get("paging", {}).get("next")
            params = {}  # next URL already has params embedded
    return False


async def get_user_info(ig_user_id: str) -> dict:
    """Fetch basic info (username, name) of an IG user."""
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{BASE}/{ig_user_id}",
            params={"fields": "id,username,name", "access_token": _token()},
            timeout=10,
        )
        r.raise_for_status()
        return r.json()
