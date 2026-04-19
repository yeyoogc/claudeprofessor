"""
Content generator for @claudeprofessor.
Uses Claude Haiku 4.5 + web_search to find today's Anthropic/Claude news
and generate structured JSON for carousel slides.
Falls back to curated content_bank if ANTHROPIC_API_KEY is not set.
"""

import json
import re
from datetime import date
from pathlib import Path

import config

SYSTEM_PROMPT = """\
You are the content brain for @claudeprofessor, an Instagram account that teaches \
people how to use Claude AI with beautiful educational carousels in Spanish.

Your job:
1. Search the web for FRESH content from multiple sources (see source list below).
2. Pick the single most interesting / viral topic NOT already covered (see covered topics injected in user prompt).
3. Generate a full carousel dataset as JSON.

CONTENT SOURCES to search (rotate through all of them):
- GitHub: trending repos, popular Claude Code skills (search "awesome-claude-code", "site:github.com claude skill"), viral AI tools
- Instagram creators: @soyenriqueochoa, @mrconsejero, @neuralnate posts about Claude/AI
- Anthropic blog & changelog: new Claude features, API updates, pricing
- Twitter/X: viral Claude tips, prompt engineering threads
- YouTube: popular Claude tutorials, AI productivity videos
- Reddit r/ClaudeAI, r/LocalLLaMA: hot posts and community discoveries
- Developer communities: Dev.to, Hashnode, HuggingFace blogs about Claude

TOPIC PRIORITY (pick what's fresh and NOT already covered):
- Viral GitHub skills/repos for Claude Code (highest engagement potential)
- Trending prompts or techniques from other creators
- New Claude features/API updates (only if genuinely new this week)
- Claude Code: hooks, MCP servers, real workflows from the community
- AI Agents: real multi-agent examples people are building
- MCP: specific popular servers (GitHub MCP, Notion MCP, Playwright MCP...)
- Prompt engineering: specific techniques with examples
- Real use cases: coding, writing, analysis, automation with concrete examples
- Comparisons: Claude vs GPT-4o on specific tasks with real results

Template style rules:
- "flat": Lists, prompt collections, quick tips compilations (e.g. "5 tricks", "10 prompts").
- "news": Announcements, product launches, new features, bold comparisons.
- "editorial": Tutorials, how-to deep dives, conceptual explanations.
- "grid": Resource roundups, developer tools, productivity hacks, tool showcases.
- "dark": High-impact announcements, dramatic reveals, power-user secrets.
- "photo": Viral listicle hooks ("36 prompts", "5 secrets"), broad-audience tips.

Output ONLY valid JSON — no markdown fences, no text before or after.
"""

USER_PROMPT = """\
Today is {today}.

ALREADY PUBLISHED — do NOT repeat these topics (pick something completely different):
{published_topics}

Search for fresh content from GitHub trending, other creators (@soyenriqueochoa etc.), \
Anthropic changelog, Reddit, and Twitter. Pick a topic that is NOT in the list above.

Then output ONLY this JSON (all slide text in SPANISH, titles max 8 words, body max 25 words, tips max 20 words):

{topic_section}

{{
  "topic": "one-line topic description in English",
  "template_style": "flat" | "news" | "editorial" | "dark" | "photo",
  "bg_query": "3-8 English keywords describing the SPECIFIC topic for Unsplash image search. Be precise: 'terminal code dark screen', 'api developer python code', 'mcp server integration network', 'claude model benchmark thinking', 'agent autonomous workflow pipeline', 'person typing laptop productivity', etc. Match the actual topic — never generic 'ai robot' or 'technology abstract'. For 'photo' style: person/hands/lifestyle. For 'news'/'dark': dramatic moody version of the topic.",
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
    "cta_title": "Comenta PROFESOR para desbloquear [specific guide related to this topic] (max 10 words, always start with 'Comenta PROFESOR')",
    "cta_subtitle": "Short subtitle saying what they'll get + invite to follow (max 12 words)"
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


def _load_published_topics() -> str:
    posts_path = Path(__file__).parent.parent / "docs" / "posts.json"
    if not posts_path.exists():
        return "None yet."
    try:
        posts = json.loads(posts_path.read_text(encoding="utf-8"))
        if not posts:
            return "None yet."
        lines = [f"- {p['topic']} ({p.get('date', '?')})" for p in posts if p.get("topic")]
        return "\n".join(lines) if lines else "None yet."
    except Exception:
        return "None yet."


def generate_content(topic_hint: str = None, template_hint: str = None) -> dict:
    if not config.ANTHROPIC_API_KEY:
        print("  ANTHROPIC_API_KEY not set. Using curated content bank...")
        from agents.content_bank import get_random_content
        return get_random_content()

    import anthropic

    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    today = date.today().isoformat()
    published_topics = _load_published_topics()

    if topic_hint:
        topic_section = (
            f"IMPORTANT — use EXACTLY this topic for the carousel:\n{topic_hint}\n"
            + (f'Set "template_style" to "{template_hint}".\n' if template_hint else "")
            + "Do NOT search for a different topic. Generate the full JSON based on the information above."
        )
    else:
        topic_section = ""

    print("  Calling Claude Haiku 4.5 + web_search...")
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        tools=[{"type": "web_search_20260209", "name": "web_search", "allowed_callers": ["direct"]}],
        messages=[{"role": "user", "content": USER_PROMPT.format(
            today=today,
            topic_section=topic_section,
            published_topics=published_topics,
        )}],
    )

    text = _extract_text(response)
    if not text:
        print("  No text in response. Using content bank...")
        from agents.content_bank import get_random_content
        return get_random_content()

    data = _parse_json(text)

    # Enforce template if caller requested one
    if template_hint:
        data["template_style"] = template_hint

    required = {"topic", "hook", "slides", "cta", "caption"}
    missing = required - set(data.keys())
    if missing:
        raise ValueError(f"Missing keys in response: {missing}")
    if len(data["slides"]) != 4:
        raise ValueError(f"Expected 4 slides, got {len(data['slides'])}")

    style = data.get("template_style", "editorial")
    if style not in {"flat", "news", "editorial", "grid", "dark", "photo"}:
        style = "editorial"
    data["template_style"] = style
    data.setdefault("bg_query", "artificial intelligence technology abstract")

    print(f"  Topic: {data['topic']}")
    print(f"  Style: {style} | bg_query: {data['bg_query']}")

    return data


if __name__ == "__main__":
    data = generate_content()
    print(json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8", "replace").decode("ascii", "replace"))
