"""Post carousels to Instagram via Meta Graph API."""
import time
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


def _get(endpoint: str, **params) -> dict:
    params["access_token"] = TOKEN()
    resp = requests.get(f"{BASE}/{endpoint}", params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def _wait_until_ready(container_id: str, max_wait: int = 120) -> None:
    """Poll container status until FINISHED or timeout."""
    deadline = time.time() + max_wait
    while time.time() < deadline:
        data = _get(container_id, fields="status_code")
        status = data.get("status_code", "")
        if status == "FINISHED":
            return
        if status == "ERROR":
            raise RuntimeError(f"Container {container_id} failed processing")
        print(f"  Container {container_id} status: {status} — waiting...")
        time.sleep(5)
    raise TimeoutError(f"Container {container_id} not ready after {max_wait}s")


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

    # Step 2: wait for all item containers to finish processing
    for cid in container_ids:
        _wait_until_ready(cid)

    # Step 3: create the carousel container
    carousel = _post(
        f"{UID()}/media",
        media_type="CAROUSEL",
        children=",".join(container_ids),
        caption=caption,
    )
    carousel_id = carousel["id"]
    print(f"  Carousel container: {carousel_id}")

    # Step 4: wait for carousel container to finish processing
    _wait_until_ready(carousel_id)

    # Step 5: publish
    published = _post(f"{UID()}/media_publish", creation_id=carousel_id)
    post_id = published["id"]
    print(f"  Published: {post_id}")
    return post_id
