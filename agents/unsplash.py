"""
Unsplash photo fetcher for carousel backgrounds.
Free tier: 50 requests/hour.
Falls back to a curated topic-indexed library when API key is missing.
"""

import hashlib
import requests
from datetime import datetime

import config

UNSPLASH_ENDPOINT = "https://api.unsplash.com/search/photos"

# Curated Unsplash photo IDs grouped by topic keyword.
# Format: real Unsplash photo IDs → direct CDN URLs work without auth.
_TOPIC_LIBRARY: dict[str, list[str]] = {
    "ai model": [
        "1620712943543-bcc4688e7485",
        "1677442136019-21780ecad995",
        "1676277791608-ac54783d753b",
        "1675557009591-95bb9b80e3f3",
        "1655720828083-8c67b2b8deae",
    ],
    "code programming": [
        "1461749280684-dccba630e2f6",
        "1498050108023-c5249f4df085",
        "1504639725590-34d0984388bd",
        "1555066931-4365d14bab8c",
        "1542831371-29b0f74f9713",
    ],
    "terminal cli": [
        "1629654297299-c8506221ca97",
        "1607798748738-b15c40d33d57",
        "1461749280684-dccba630e2f6",
        "1542831371-29b0f74f9713",
        "1504639725590-34d0984388bd",
    ],
    "api developer": [
        "1558494949-ef010cbdcc31",
        "1555066931-4365d14bab8c",
        "1551033406-611cf9a28f67",
        "1547954575-855750c57bd3",
        "1517694712202-14dd9538aa97",
    ],
    "chat conversation": [
        "1611606063065-ee7946f0787a",
        "1516321318423-f06f85e504b3",
        "1573164713714-d95e436ab8d6",
        "1557804506-669a67965ba0",
        "1573496359142-b8d87734a5a2",
    ],
    "workflow automation": [
        "1518770660439-4636190af475",
        "1558494949-ef010cbdcc31",
        "1531746790731-6c087fecd65a",
        "1551288049-bebda4e38f71",
        "1563013544-824ae1b704d3",
    ],
    "agent robot": [
        "1677442136019-21780ecad995",
        "1620712943543-bcc4688e7485",
        "1676277791608-ac54783d753b",
        "1535378917042-10a22c5ab303",
        "1485827404703-89b55fcc595e",
    ],
    "data server": [
        "1558494949-ef010cbdcc31",
        "1451187580459-43490279c0fa",
        "1518770660439-4636190af475",
        "1484557985045-edf25e08da73",
        "1490474418585-ba9bad8fd0ea",
    ],
    "dark technology": [
        "1518770660439-4636190af475",
        "1573164713714-d95e436ab8d6",
        "1451187580459-43490279c0fa",
        "1484557985045-edf25e08da73",
        "1465343161283-c1959138ddaa",
    ],
    "productivity work": [
        "1522071820081-009f0129c71c",
        "1484480974693-6ca0a78fb36b",
        "1517245386807-bb43f82c33c4",
        "1497032628192-86f99bcd76bc",
        "1515378791036-0648a3ef77b2",
    ],
    "person typing": [
        "1499750310107-5fef28a66643",
        "1517245386807-bb43f82c33c4",
        "1522071820081-009f0129c71c",
        "1455390582262-044cdead277a",
        "1484480974693-6ca0a78fb36b",
    ],
    "abstract orange": [
        "1618005182384-a83a8bd57fbe",
        "1557682257-2f9c37a3a5f3",
        "1536697246787-1f7ae568d89a",
        "1526374965328-7f61d4dc18c5",
        "1465343161283-c1959138ddaa",
    ],
    "default": [
        "1461749280684-dccba630e2f6",
        "1620712943543-bcc4688e7485",
        "1518770660439-4636190af475",
        "1558494949-ef010cbdcc31",
        "1499750310107-5fef28a66643",
    ],
}

# Keyword → library bucket mapping
_KEYWORD_MAP: list[tuple[list[str], str]] = [
    (["claude code", "cli", "terminal", "command", "hook", "slash"], "terminal cli"),
    (["skill", "plugin", "extension"], "terminal cli"),
    (["mcp", "server", "connector", "protocol", "integration"], "api developer"),
    (["api", "sdk", "developer", "function", "tool use", "tool_use"], "api developer"),
    (["agent", "multi-agent", "agentic", "loop", "autonomous"], "agent robot"),
    (["model", "opus", "sonnet", "haiku", "thinking", "llm", "benchmark"], "ai model"),
    (["chat", "conversation", "message", "prompt"], "chat conversation"),
    (["automation", "workflow", "pipeline", "batch"], "workflow automation"),
    (["data", "database", "vector", "rag", "memory", "storage"], "data server"),
    (["dark", "dramatic", "moody", "night"], "dark technology"),
    (["productivity", "business", "enterprise", "roi", "work"], "productivity work"),
    (["person", "portrait", "face", "lifestyle", "hands"], "person typing"),
    (["abstract", "orange", "gradient", "colorful"], "abstract orange"),
    (["code", "programming", "python", "typescript", "javascript", "software"], "code programming"),
]


def _pick_bucket(query: str) -> str:
    q = query.lower()
    for keywords, bucket in _KEYWORD_MAP:
        if any(kw in q for kw in keywords):
            return bucket
    return "default"


def _seed(query: str) -> int:
    stamp = datetime.now().strftime("%Y-%m-%d-%H")
    h = hashlib.md5(f"{stamp}:{query}".encode()).hexdigest()
    return int(h[:8], 16)


def _fallback(query: str) -> str:
    bucket = _pick_bucket(query)
    photos = _TOPIC_LIBRARY[bucket]
    photo_id = photos[_seed(query) % len(photos)]
    return f"https://images.unsplash.com/photo-{photo_id}?w=1600&q=85"


def fetch_bg_image(query: str) -> str:
    """Return a public Unsplash image URL matching the topic query."""
    key = getattr(config, "UNSPLASH_ACCESS_KEY", "") or ""
    if not key:
        return _fallback(query)

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
            return _fallback(query)

        idx = _seed(query) % len(results)
        photo = results[idx]
        return photo["urls"].get("regular") or photo["urls"]["full"]
    except Exception as e:
        print(f"  Unsplash API failed ({e}); using topic fallback")
        return _fallback(query)


if __name__ == "__main__":
    for q in ["claude code terminal hooks", "mcp server integration", "opus model ai", "agent autonomous loop"]:
        print(f"{q!r}: {fetch_bg_image(q)}")
