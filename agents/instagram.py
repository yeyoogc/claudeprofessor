"""Post carousels to Instagram via Meta Graph API."""
import requests
import config

BASE = config.INSTAGRAM_API_BASE
UID = lambda: config.INSTAGRAM_USER_ID
TOKEN = lambda: config.INSTAGRAM_ACCESS_TOKEN


def _post(endpoint: str, **params) -> dict:
    params["access_token"] = TOKEN()
    resp = requests.post(f"{BASE}/{endpoint}", params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if "error" in data:
        raise RuntimeError(f"Instagram API error: {data['error']}")
    return data


def create_carousel(image_urls: list[str], caption: str) -> str:
    """
    Upload images and publish as carousel post.
    image_urls: list of 3-10 publicly accessible image URLs
    caption: full caption including hashtags
    Returns: published media ID
    """
    if not 2 <= len(image_urls) <= 10:
        raise ValueError(f"Carousel needs 2-10 images, got {len(image_urls)}")

    # Step 1: create a media container for each image
    container_ids = []
    for url in image_urls:
        data = _post(
            f"{UID()}/media",
            image_url=url,
            is_carousel_item="true",
        )
        container_ids.append(data["id"])
        print(f"  Container created: {data['id']} ({url[:60]}...)")

    # Step 2: create the carousel container
    carousel = _post(
        f"{UID()}/media",
        media_type="CAROUSEL",
        children=",".join(container_ids),
        caption=caption,
    )
    carousel_id = carousel["id"]
    print(f"  Carousel container: {carousel_id}")

    # Step 3: publish
    published = _post(f"{UID()}/media_publish", creation_id=carousel_id)
    post_id = published["id"]
    print(f"  Published: {post_id}")
    return post_id
