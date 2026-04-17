"""
Batch publisher — posts multiple carousels in sequence.
Usage: python batch_post.py
"""

import time
from run import run

CAROUSELS = [
    {
        "topic_hint": (
            "Claude Design: nueva herramienta de Anthropic lanzada el 17 de abril de 2026. "
            "Crea diseños visuales, slides, prototipos y one-pagers con texto en lenguaje natural. "
            "Powered by Claude Opus 4.7. Puedes refinar con comentarios inline, sliders de ajuste o edición directa. "
            "Exporta en PDF, PPTX, URL, o envía directo a Canva como archivo editable. "
            "Disponible en preview para Pro, Max, Team y Enterprise."
        ),
        "template_hint": "photo",
    },
    {
        "topic_hint": (
            "Claude Opus 4.7: el modelo más potente de Anthropic, lanzado el 16 de abril de 2026. "
            "Novedades clave: Adaptive Thinking (decide cuándo pensar, menos overthinking), "
            "Task Budgets (controla tokens en loops de agentes), mejor en coding (encuentra bugs, revisa código), "
            "mejor en razonamiento en tareas largas y ambiguas. "
            "Mismo precio que 4.6: $5/$25 por millón de tokens. Tokenizador actualizado (1.0-1.35x más tokens)."
        ),
        "template_hint": "dark",
    },
    {
        "topic_hint": (
            "Claude Code Routines: automatización de tareas lanzada el 14 de abril de 2026. "
            "Una routine es una config guardada (prompt + repo + connectors) que se ejecuta automáticamente. "
            "3 tipos de triggers: schedule (cron horario/diario/semanal), API (HTTP POST), GitHub (PR, push, release). "
            "Corre en infraestructura de Anthropic, no necesita tu ordenador encendido. "
            "Límites: Pro 5/día, Max 15/día, Team/Enterprise 25/día."
        ),
        "template_hint": "editorial",
    },
    {
        "topic_hint": (
            "Claude Code v2.1.110: novedades de esta semana en Claude Code. "
            "/tui fullscreen: renderizado sin parpadeos en pantalla completa. "
            "Push notifications: Claude te avisa en el móvil cuando termina una tarea larga. "
            "Nuevo /focus para alternar la vista de foco. "
            "Plugins mejorados: favoritos arriba, disabled ocultos. "
            "disableSkillShellExecution: nueva config de seguridad para skills."
        ),
        "template_hint": "news",
    },
    {
        "topic_hint": (
            "Skills en Claude Code: cómo dar superpoderes reutilizables a Claude. "
            "Un skill es un archivo SKILL.md que Claude lee cuando usas /skill-name. "
            "Puedes crear skills para: frameworks específicos, workflows de tu empresa, estilos de código. "
            "Con Opus 4.7, los skills explícitos funcionan mejor que los basados en hints. "
            "Repositorio awesome-claude-code tiene más de 200 skills de la comunidad. "
            "Claude Code los activa con trigger words en tus prompts."
        ),
        "template_hint": "flat",
    },
]


def main():
    total = len(CAROUSELS)
    for i, carousel in enumerate(CAROUSELS, 1):
        print(f"\n{'='*60}")
        print(f"CAROUSEL {i}/{total}: {carousel['template_hint'].upper()}")
        print(f"{'='*60}")
        try:
            run(
                topic_hint=carousel["topic_hint"],
                template_hint=carousel["template_hint"],
            )
        except Exception as e:
            print(f"ERROR on carousel {i}: {e}")
            continue

        if i < total:
            delay = 45
            print(f"\nEsperando {delay}s antes del siguiente...")
            time.sleep(delay)

    print(f"\n{'='*60}")
    print(f"BATCH COMPLETO: {total} carruseles publicados")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
