"""Quick test: render carousel for all 3 template styles.

Usage:
  python test_render.py            # renders all 3 styles
  python test_render.py flat       # renders only "flat"
  python test_render.py news
  python test_render.py editorial
"""
import shutil
import sys
from pathlib import Path

from agents.renderer import render_carousel_sync

BASE_CONTENT = {
    "hook": {
        "tag": "Extended Thinking",
        "title": 'Claude puede <span class="accent">pensar</span><br>antes de responder',
        "subtitle": "Activa el modo de razonamiento extendido y obtén respuestas más precisas.",
    },
    "slides": [
        {
            "step_label": "Concepto",
            "title": '¿Qué es <span class="accent">Extended Thinking</span>?',
            "body": "Un modo donde Claude razona paso a paso antes de dar su respuesta final.",
            "tip": "Usa <strong>claude-sonnet-4-20250514</strong> para acceder a esta función.",
        },
        {
            "step_label": "Cómo activarlo",
            "title": 'Actívalo con un <span class="accent">parámetro</span> simple',
            "body": 'Agrega thinking: {type: enabled} en tu llamada a la API.',
            "tip": "El budget_tokens controla <strong>cuánto piensa</strong> Claude.",
        },
        {
            "step_label": "Casos de uso",
            "title": 'Ideal para tareas <span class="accent">complejas</span>',
            "body": "Matemáticas, código, análisis legal y problemas multi-paso.",
            "tip": "No lo uses para tareas simples, es <strong>más lento</strong> pero preciso.",
        },
        {
            "step_label": "Pro tip",
            "title": 'Combina con <span class="accent">System Prompts</span>',
            "body": "Dale contexto en el system prompt y deja que piense profundamente.",
            "tip": "Extended Thinking + contexto = <strong>nivel experto</strong>.",
        },
    ],
    "cta": {
        "cta_title": "¡Aprende más trucos cada día! 🧡",
        "cta_subtitle": "Tips diarios para dominar Claude AI",
    },
    "bg_query": "artificial intelligence abstract orange futuristic",
}

STYLES = ["editorial", "flat", "news"]


def render_one(style: str) -> None:
    content = dict(BASE_CONTENT)
    content["template_style"] = style
    print(f"\n=== Rendering style: {style} ===")
    paths = render_carousel_sync(content)

    # Move renders into output/<style>/ so results don't overwrite
    dest = Path("output") / style
    dest.mkdir(parents=True, exist_ok=True)
    for p in paths:
        target = dest / Path(p).name
        shutil.copy2(p, target)
        print(f"   {target}")


if __name__ == "__main__":
    selected = sys.argv[1:] or STYLES
    for s in selected:
        if s not in STYLES:
            print(f"Unknown style: {s}. Valid: {STYLES}")
            sys.exit(1)
        render_one(s)
    print("\nDone.")
