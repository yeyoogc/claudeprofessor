"""
Content generator for @claudeprofessor.
Uses Claude Haiku 4.5 + web_search to find today's Anthropic/Claude news
and generate structured JSON for carousel slides.
Falls back to curated content_bank if ANTHROPIC_API_KEY is not set.
"""

import json
import re
from datetime import date

import config

SYSTEM_PROMPT = """\
You are the content brain for @claudeprofessor, an Instagram account that teaches \
people how to use Claude AI with beautiful educational carousels in Spanish.

Your job:
1. Search the web for the LATEST Claude / Anthropic news from today or this week.
   Focus on: new model releases, new features, API updates, Claude Code updates,
   prompt engineering tips, productivity use cases, comparisons, benchmarks.
2. Pick the single most interesting / viral topic to teach today.
3. Generate a full carousel dataset as JSON.

Template style rules:
- "flat": Lists, prompt collections, quick tips compilations (e.g. "5 tricks", "10 prompts").
- "news": Announcements, product launches, new features, bold comparisons.
- "editorial": Tutorials, how-to deep dives, conceptual explanations.

Output ONLY valid JSON — no markdown fences, no text before or after.
"""

USER_PROMPT = """\
Today is {today}.

Search for the latest Claude / Anthropic news and pick the best topic for today's carousel.

Then output ONLY this JSON (all slide text in SPANISH, titles max 8 words, body max 25 words, tips max 20 words):

{{
  "topic": "one-line topic description in English",
  "template_style": "flat" | "news" | "editorial",
  "bg_query": "3-6 English words for Unsplash photo search",
  "hook": {{
    "tag": "Short Category Name",
    "title": "Catchy title with one <span class=\\"accent\\">accented</span> word",
    "subtitle": "One sentence hook explaining the value (max 20 words)"
  }},
  "slides": [
    {{
      "step_label": "Short Label",
      "title": "Step title with <span class=\\"accent\\">key word</span>",
      "body": "Explanation in 1-2 sentences (max 25 words)",
      "tip": "Quick pro tip with optional <strong>bold</strong> (max 20 words)"
    }},
    {{
      "step_label": "Short Label",
      "title": "Step title with <span class=\\"accent\\">key word</span>",
      "body": "Explanation (max 25 words)",
      "tip": "Pro tip (max 20 words)"
    }},
    {{
      "step_label": "Short Label",
      "title": "Step title with <span class=\\"accent\\">key word</span>",
      "body": "Explanation (max 25 words)",
      "tip": "Pro tip (max 20 words)"
    }},
    {{
      "step_label": "Short Label",
      "title": "Step title with <span class=\\"accent\\">key word</span>",
      "body": "Explanation (max 25 words)",
      "tip": "Pro tip (max 20 words)"
    }}
  ],
  "cta": {{
    "cta_title": "Engaging CTA title (max 10 words) \U0001F9E1",
    "cta_subtitle": "Short subtitle inviting to follow (max 12 words)"
  }},
  "caption": "Engaging Instagram caption in Spanish (2-4 sentences, emojis, references the topic, ends with a question). No hashtags.",
  "hashtags": "#ClaudeAI #AnthropicAI #AITips #PromptEngineering #ClaudeProfessor #LearnAI #AITools #ArtificialIntelligence #AIAssistant #TechTips #MachineLearning #AIProductivity #ChatAI #FutureOfWork #AIHacks"
}}
"""


def _parse_json(text: str) -> dict:
    text = re.sub(r"^```json\s*", "", text.strip())
    text = re.sub(r"\s*```$", "", text).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError(f"Cannot parse JSON from response:\n{text[:500]}")


def _extract_text(response) -> str:
    """Extract final text from a streamed or regular response."""
    parts = []
    for block in response.content:
        if hasattr(block, "text"):
            parts.append(block.text)
    return "".join(parts)


def generate_content() -> dict:
    if not config.ANTHROPIC_API_KEY:
        print("  ANTHROPIC_API_KEY not set. Using curated content bank...")
        from agents.content_bank import get_random_content
        return get_random_content()

    import anthropic

    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    today = date.today().isoformat()

    print("  Calling Claude Haiku 4.5 + web_search...")
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        tools=[{"type": "web_search_20260209", "name": "web_search", "allowed_callers": ["direct"]}],
        messages=[{"role": "user", "content": USER_PROMPT.format(today=today)}],
    )

    text = _extract_text(response)
    if not text:
        print("  No text in response. Using content bank...")
        from agents.content_bank import get_random_content
        return get_random_content()

    data = _parse_json(text)

    required = {"topic", "hook", "slides", "cta", "caption"}
    missing = required - set(data.keys())
    if missing:
        raise ValueError(f"Missing keys in response: {missing}")
    if len(data["slides"]) != 4:
        raise ValueError(f"Expected 4 slides, got {len(data['slides'])}")

    style = data.get("template_style", "editorial")
    if style not in {"flat", "news", "editorial"}:
        style = "editorial"
    data["template_style"] = style
    data.setdefault("bg_query", "artificial intelligence technology abstract")

    print(f"  Topic: {data['topic']}")
    print(f"  Style: {style} | bg_query: {data['bg_query']}")

    return data


if __name__ == "__main__":
    data = generate_content()
    print(json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8", "replace").decode("ascii", "replace"))
