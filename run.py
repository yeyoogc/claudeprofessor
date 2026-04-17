"""
Daily orchestrator for @claudeprofessor.

Flow (v2 — no Claude Code tokens needed):
  1. Gemini Flash (free) generates structured JSON with slide text + caption
  2. HTML templates are populated with the content
  3. Playwright renders each slide to 1080×1080 PNG
  4. PNGs are uploaded to imgbb for public hosting
  5. Preview email sent → wait for approval → publish to Instagram

Usage:
  python run.py               # generate + post immediately
  python run.py --dry-run     # generate only, print output
  python run.py --preview     # generate + upload + email preview
  python run.py --publish     # publish last previewed carousel to Instagram
"""

import json
import os
import sys
from datetime import date
from pathlib import Path

PREVIEW_FILE = ".last_preview.json"

from agents.content import generate_content
from agents.renderer import render_carousel_sync
from agents.image_host import upload_bytes
from agents.instagram import create_carousel
from agents.notify import send_preview_email
import config


def run(dry_run: bool = False, preview: bool = False, topic_hint: str = None, template_hint: str = None) -> None:
    print(f"[{date.today()}] Starting @claudeprofessor daily post (v2)...")

    # ── Step 1: Generate content ───────────────────────────────────────────
    print("Generating content...")
    data = generate_content(topic_hint=topic_hint, template_hint=template_hint)
    topic = data["topic"]
    caption = data["caption"]
    hashtags = data.get("hashtags", config.DEFAULT_HASHTAGS)
    full_caption = f"{caption}\n\n{hashtags}"

    print(f"Topic: {topic}")

    # ── Step 2: Render HTML templates to PNG ──────────────────────────────
    print("Rendering slides with Playwright...")
    png_paths = render_carousel_sync(data)
    print(f"Generated {len(png_paths)} slides")

    if dry_run:
        print("\n[DRY RUN] Would post:")
        print(f"Caption: {full_caption[:200].encode('ascii', 'replace').decode()}...")
        print(f"Slides: {png_paths}")
        return

    # ── Step 3: Upload slides to public host ─────────────────────────────
    print("Uploading images...")
    hosted_urls = []
    for i, path in enumerate(png_paths, 1):
        print(f"  Slide {i}: uploading...")
        img_bytes = Path(path).read_bytes()
        fname = Path(path).name
        hosted = upload_bytes(img_bytes, filename=fname)
        hosted_urls.append(hosted)
        print(f"  Slide {i}: {hosted}")

    if preview:
        # Save for --publish later
        with open(PREVIEW_FILE, "w") as f:
            json.dump({
                "topic": topic,
                "tag": data.get("hook", {}).get("tag", "Claude AI"),
                "date": date.today().isoformat(),
                "urls": hosted_urls,
                "caption": full_caption,
            }, f)
        send_preview_email(topic, hosted_urls, full_caption)
        print(f"\n[PREVIEW] Email sent. Run `python run.py --publish` to post.")
        return

    # ── Step 4: Post to Instagram ─────────────────────────────────────────
    print("Posting carousel to Instagram...")
    post_id = create_carousel(hosted_urls, full_caption)
    print(f"Done! Post ID: {post_id}")

    # ── Step 5: Update gallery ────────────────────────────────────────────
    posts_file = Path(__file__).parent / "docs" / "posts.json"
    try:
        existing = json.loads(posts_file.read_text()) if posts_file.exists() else []
    except (json.JSONDecodeError, OSError):
        existing = []
    existing.append({
        "id": post_id,
        "topic": topic,
        "tag": data.get("hook", {}).get("tag", "Claude AI"),
        "date": date.today().isoformat(),
        "slides": hosted_urls,
        "caption": full_caption,
        "instagram_id": post_id,
    })
    posts_file.write_text(json.dumps(existing, ensure_ascii=False, indent=2))
    print(f"Gallery updated: {len(existing)} posts total")


def publish_last() -> None:
    if not os.path.exists(PREVIEW_FILE):
        print("No preview found. Run `python run.py --preview` first.")
        sys.exit(1)
    with open(PREVIEW_FILE) as f:
        preview = json.load(f)
    print(f"Publishing: {preview['topic']}")
    post_id = create_carousel(preview["urls"], preview["caption"])
    os.remove(PREVIEW_FILE)
    print(f"Done! Post ID: {post_id}")

    # Append to docs/posts.json for the gallery site
    posts_file = Path(__file__).parent / "docs" / "posts.json"
    try:
        existing = json.loads(posts_file.read_text()) if posts_file.exists() else []
    except (json.JSONDecodeError, OSError):
        existing = []
    existing.append({
        "id": post_id,
        "topic": preview["topic"],
        "tag": preview.get("tag", "Claude AI"),
        "date": preview.get("date", date.today().isoformat()),
        "slides": preview["urls"],
        "caption": preview["caption"],
        "instagram_id": post_id,
    })
    posts_file.write_text(json.dumps(existing, ensure_ascii=False, indent=2))
    print(f"Gallery updated: {len(existing)} posts total")


if __name__ == "__main__":
    if "--publish" in sys.argv:
        publish_last()
    else:
        dry = "--dry-run" in sys.argv
        preview = "--preview" in sys.argv
        run(dry_run=dry, preview=preview)
