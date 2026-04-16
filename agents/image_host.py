"""Upload images to Supabase Storage so Instagram Graph API can access them.

Supabase Storage provides reliable, fast CDN URLs that Meta can read.
Falls back to imgbb if Supabase is unavailable.
"""
import base64
import uuid
import requests
import config

# Supabase Storage config
SUPABASE_URL = "https://twswhlxcsjkcyowzjxjm.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR3c3dobHhjc2prY3lvd3pqeGptIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU0MDQxMzgsImV4cCI6MjA5MDk4MDEzOH0.gCZWiJ5boecdDrqLqPdOSyVLvkLpDBaao1wTKUTgUh8"
BUCKET = "carousel-images"


def upload_bytes(image_bytes: bytes, filename: str = "slide.jpg") -> str:
    """Upload raw image bytes. Returns permanent public URL."""
    # Try Supabase Storage first
    try:
        return _upload_supabase(image_bytes, filename)
    except Exception as e:
        print(f"    Supabase failed ({e}), trying imgbb...")

    # Fallback to imgbb
    return _upload_imgbb(image_bytes)


def _upload_supabase(image_bytes: bytes, filename: str) -> str:
    """Upload to Supabase Storage — reliable CDN, works with Meta."""
    # Generate unique filename to avoid collisions
    unique_name = f"{uuid.uuid4().hex[:12]}_{filename}"
    
    resp = requests.post(
        f"{SUPABASE_URL}/storage/v1/object/{BUCKET}/{unique_name}",
        headers={
            "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
            "apikey": SUPABASE_ANON_KEY,
            "Content-Type": "image/jpeg",
        },
        data=image_bytes,
        timeout=60,
    )
    resp.raise_for_status()
    
    # Return public URL
    public_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET}/{unique_name}"
    return public_url


def _upload_imgbb(image_bytes: bytes) -> str:
    """Upload to imgbb (backup host)."""
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    resp = requests.post(
        "https://api.imgbb.com/1/upload",
        data={"key": config.IMGBB_API_KEY, "image": encoded},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    if not data.get("success"):
        raise RuntimeError(f"imgbb upload failed: {data}")
    return data["data"]["url"]


def upload_from_url(image_url: str) -> str:
    """Download image from URL and re-host. Returns permanent URL."""
    img_data = requests.get(image_url, timeout=30).content
    return upload_bytes(img_data)
