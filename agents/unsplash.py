"""
Unsplash photo fetcher for news-style carousel backgrounds.
Free tier: 50 requests/hour. Uses deterministic seed per day so carousel is consistent.
"""

import hashlib
import random
import requests
from datetime import date

import config


UNSPLASH_ENDPOINT = "https://api.unsplash.com/search/photos"
FALLBACK_URLS = [
    "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1600&q=85",
    "https://images.unsplash.com/photo-1676277791608-ac54783d753b?w=1600&q=85",
    "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=1600&q=85",
    "https://images.unsplash.com/photo-1618091372796-4f2c3b70ab97?w=1600&q=85",
]


def fetch_bg_image(query: str) -> str:
    """
    Return a public image URL for a background. Uses today's date as seed
    so both hook and cta of the same carousel get the same image.
    Falls back to a curated list if the API fails.
    """
    key = getattr(config, "UNSPLASH_ACCESS_KEY", "") or ""
    if not key:
        return _deterministic_fallback(query)

    try:
        resp = requests.get(
            UNSPLASH_ENDPOINT,
            params={
                "query": query,
                "orientation": "squarish",
                "per_page": 10,
                "content_filter": "high",
            },
            headers={"Authorization": f"Client-ID {key}"},
            timeout=10,
        )
        resp.raise_for_status()
        results = resp.json().get("results", [])
        if not results:
            return _deterministic_fallback(query)

        idx = _daily_seed(query) % len(results)
        photo = results[idx]
        return photo["urls"].get("regular") or photo["urls"]["full"]
    except Exception as e:
        print(f"  Unsplash fetch failed ({e}); using fallback")
        return _deterministic_fallback(query)


def _daily_seed(query: str) -> int:
    from datetime import datetime
    stamp = datetime.now().strftime("%Y-%m-%d-%H")
    h = hashlib.md5(f"{stamp}:{query}".encode()).hexdigest()
    return int(h[:8], 16)


def _deterministic_fallback(query: str) -> str:
    idx = _daily_seed(query) % len(FALLBACK_URLS)
    return FALLBACK_URLS[idx]


if __name__ == "__main__":
    print(fetch_bg_image("artificial intelligence technology"))
