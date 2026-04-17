"""
Render HTML slide templates to 1080x1080 JPEG using Playwright.
No external design tools needed — everything is local.
"""

import os
import asyncio
import base64
from pathlib import Path
from playwright.async_api import async_playwright

from agents.unsplash import fetch_bg_image

_MASCOT_DATA_URI: str | None = None

def _mascot_uri() -> str:
    global _MASCOT_DATA_URI
    if _MASCOT_DATA_URI is None:
        p = Path(__file__).parent.parent / "docs" / "img" / "mascot.png"
        if p.exists():
            b64 = base64.b64encode(p.read_bytes()).decode()
            _MASCOT_DATA_URI = f"data:image/png;base64,{b64}"
        else:
            _MASCOT_DATA_URI = ""
    return _MASCOT_DATA_URI

TEMPLATES_ROOT = Path(__file__).parent.parent / "templates"
OUTPUT_DIR = Path(__file__).parent.parent / "output"
VALID_STYLES = {"flat", "news", "editorial", "grid", "dark", "photo"}


def _build_dots_html(total: int, active_index: int) -> str:
    """Generate the carousel dot indicators HTML."""
    dots = []
    for i in range(total):
        cls = "dot active" if i == active_index else "dot"
        dots.append(f'<div class="{cls}"></div>')
    return "\n      ".join(dots)


def _inject_hook(template: str, data: dict, total_slides: int, bg_url: str = "") -> str:
    html = template
    html = html.replace("{{TAG}}", data.get("tag", "Claude AI"))
    html = html.replace("{{TITLE}}", data.get("title", ""))
    html = html.replace("{{SUBTITLE}}", data.get("subtitle", ""))
    html = html.replace("{{TOTAL_SLIDES}}", f"{total_slides:02d}")
    html = html.replace("{{BG_IMAGE_URL}}", bg_url)
    html = html.replace("{{MASCOT_DATA_URI}}", _mascot_uri())
    return html


def _inject_content(template: str, data: dict, slide_idx: int, total_slides: int, bg_url: str = "") -> str:
    html = template
    step_num = slide_idx
    html = html.replace("{{STEP_NUM}}", str(step_num))
    html = html.replace("{{STEP_LABEL}}", data.get("step_label", f"Paso {step_num}"))
    html = html.replace("{{SLIDE_NUM}}", f"{slide_idx + 1:02d}")
    html = html.replace("{{TOTAL_SLIDES}}", f"{total_slides:02d}")
    html = html.replace("{{TITLE}}", data.get("title", ""))
    html = html.replace("{{BODY}}", data.get("body", ""))
    html = html.replace("{{TIP}}", data.get("tip", ""))
    html = html.replace("{{DOTS}}", _build_dots_html(total_slides, slide_idx))
    html = html.replace("{{BG_IMAGE_URL}}", bg_url)
    html = html.replace("{{MASCOT_DATA_URI}}", _mascot_uri())
    return html


def _inject_cta(template: str, data: dict, total_slides: int, bg_url: str = "") -> str:
    html = template
    html = html.replace("{{CTA_TITLE}}", data.get("cta_title", "Síguenos para más tips"))
    html = html.replace("{{CTA_SUBTITLE}}", data.get("cta_subtitle", "Cada día un nuevo truco de Claude AI"))
    html = html.replace("{{SLIDE_NUM}}", f"{total_slides:02d}")
    html = html.replace("{{TOTAL_SLIDES}}", f"{total_slides:02d}")
    html = html.replace("{{DOTS}}", _build_dots_html(total_slides, total_slides - 1))
    html = html.replace("{{BG_IMAGE_URL}}", bg_url)
    html = html.replace("{{MASCOT_DATA_URI}}", _mascot_uri())
    return html


async def _render_html_to_image(html: str, output_path: str, browser) -> str:
    """Render an HTML string to a 1080x1080 JPEG (Instagram-optimized)."""
    context = await browser.new_context(
        viewport={"width": 1080, "height": 1080},
        device_scale_factor=2,  # Retina-quality
    )
    page = await context.new_page()
    await page.set_content(html, wait_until="networkidle")
    # Wait for Google Fonts to load
    await page.evaluate("() => document.fonts.ready")
    await page.screenshot(path=output_path, type="jpeg", quality=95)
    await context.close()
    return output_path


async def render_carousel(content: dict) -> list[str]:
    """
    Render a full carousel from structured content data.
    
    content = {
        "hook": {"tag": "...", "title": "...", "subtitle": "..."},
        "slides": [
            {"step_label": "...", "title": "...", "body": "...", "tip": "..."},
            ... (4 items)
        ],
        "cta": {"cta_title": "...", "cta_subtitle": "..."}
    }
    
    Returns: list of file paths to the generated PNG images.
    """
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Pick template family by content['template_style']
    style = content.get("template_style", "editorial")
    if style not in VALID_STYLES:
        style = "editorial"
    style_dir = TEMPLATES_ROOT / style
    print(f"  Rendering with style: {style}")

    hook_template = (style_dir / "slide_hook.html").read_text(encoding="utf-8")
    content_template = (style_dir / "slide_content.html").read_text(encoding="utf-8")
    cta_template = (style_dir / "slide_cta.html").read_text(encoding="utf-8")

    # News + grid styles use a background/device image from Unsplash
    bg_url = ""
    if style in ("news", "grid", "photo"):
        bg_query = content.get("bg_query", "abstract technology orange")
        bg_url = fetch_bg_image(bg_query)
        print(f"  Background: {bg_url[:80]}...")

    total_slides = 2 + len(content["slides"])  # hook + N content + cta

    # Prepare all HTML pages
    pages = []

    # Slide 1: Hook
    pages.append(_inject_hook(hook_template, content["hook"], total_slides, bg_url))

    # Slides 2-N: Content
    for i, slide_data in enumerate(content["slides"]):
        pages.append(_inject_content(content_template, slide_data, i + 1, total_slides, bg_url))

    # Slide N+1: CTA
    pages.append(_inject_cta(cta_template, content.get("cta", {}), total_slides, bg_url))
    
    # Render all
    output_paths = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for i, html in enumerate(pages, 1):
            path = str(OUTPUT_DIR / f"slide_{i:02d}.jpg")
            await _render_html_to_image(html, path, browser)
            output_paths.append(path)
            print(f"  Rendered slide {i}/{total_slides}: {path}")
        await browser.close()
    
    return output_paths


def render_carousel_sync(content: dict) -> list[str]:
    """Synchronous wrapper for render_carousel."""
    return asyncio.run(render_carousel(content))


if __name__ == "__main__":
    # Quick test with sample data
    test_content = {
        "template_style": "editorial",
        "bg_query": "artificial intelligence abstract orange",
        "hook": {
            "tag": "Extended Thinking",
            "title": 'Claude puede <span class="accent">pensar</span><br>antes de<br>responder',
            "subtitle": "Activa el modo de razonamiento extendido y obtén respuestas mucho más precisas.",
        },
        "slides": [
            {
                "step_label": "Concepto",
                "title": '¿Qué es <span class="accent">Extended Thinking</span>?',
                "body": "Es un modo donde Claude razona paso a paso internamente antes de darte la respuesta final.",
                "tip": "Usa <strong>claude-sonnet-4-20250514</strong> para acceder a esta función.",
            },
            {
                "step_label": "Cómo activarlo",
                "title": 'Actívalo con el <span class="accent">parámetro thinking</span>',
                "body": 'Añade "thinking": {"type": "enabled"} en tu llamada a la API.',
                "tip": "El budget_tokens controla <strong>cuánto piensa</strong> Claude antes de responder.",
            },
            {
                "step_label": "Casos de uso",
                "title": 'Perfecto para <span class="accent">tareas complejas</span>',
                "body": "Matemáticas, código, análisis legal, problemas multi-paso... donde el razonamiento importa.",
                "tip": "No lo uses para tareas simples — es <strong>más lento</strong> pero más preciso.",
            },
            {
                "step_label": "Pro tip",
                "title": 'Combina con <span class="accent">System Prompts</span>',
                "body": "Dale contexto en el system prompt y deja que piense. Los resultados son sorprendentes.",
                "tip": "Extended Thinking + buen contexto = <strong>respuestas de nivel experto</strong>.",
            },
        ],
        "cta": {
            "cta_title": "¡Aprende más trucos de Claude cada día! 🧡",
            "cta_subtitle": "Tips diarios, tutoriales y hacks para dominar la IA.",
        },
    }
    
    paths = render_carousel_sync(test_content)
    print(f"\n✅ Generated {len(paths)} slides!")
    for p in paths:
        print(f"   {p}")
