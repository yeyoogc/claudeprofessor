"""
Humanizer: removes AI writing patterns from text.
Based on https://github.com/blader/humanizer (MIT)
Used for auto-replies to Instagram comments and DMs.
"""

import random
import config

HUMANIZER_SYSTEM = """\
You are a writing editor. Rewrite the given text so it sounds completely human — casual, direct, \
specific. Written by a real person who actually knows their stuff.

Remove these AI patterns:
- "Pivotal," "testament," "crucial," "transformative," "groundbreaking," "comprehensive"
- Em dashes as connectors — use commas or a new sentence instead
- Rule of three (listing exactly 3 things feels robotic)
- Vague attributions: "it's worth noting," "it's important to remember"
- Filler: "at the end of the day," "needless to say," "certainly," "absolutely"
- AI vocab: "delve," "leverage," "utilize," "robust," "seamlessly"
- Excessive exclamation marks
- Starting multiple sentences with "The"

Add human qualities:
- Varied sentence lengths. Short ones. Then longer ones that breathe.
- Specific details over vague claims
- Natural imperfections and casual connectors ("honestly," "look," "the thing is")
- Opinions where appropriate
- Spanish if the input is in Spanish

Output ONLY the rewritten text. No commentary, no preamble.
"""

# Varied opening lines for public comment replies
_REPLY_OPENERS = [
    "ey @{u}, mira tu DM",
    "@{u} ya te lo mandé por DM",
    "@{u} te lo acabo de enviar",
    "hola @{u}! revisa tus DMs",
    "@{u} mira el DM que te he mandado",
    "@{u} ahí va 👇",
    "@{u} enviado. échale un ojo al DM",
    "te lo mando ahora @{u}",
]

# DM templates — 4 variants to rotate
_DM_TEMPLATES = [
    """\
Hola! Vi tu comentario.

Aquí tienes la guía: {url}

Tiene todo lo que necesitas para empezar desde cero. Guárdala porque la actualizo cuando salen cosas nuevas.

Si algo no te queda claro, responde aquí y lo vemos.""",

    """\
Hola {u}! Aquí va lo que pediste.

{url}

Es una guía bastante completa, así que tómate tu tiempo con ella. \
Si hay algo que no funciona en tu caso concreto, cuéntame.""",

    """\
Buenas! La guía está aquí:

{url}

Está actualizada con lo último. Cualquier pregunta que tengas, aquí estoy.""",

    """\
Hola! Aquí tienes la guía completa:

{url}

Si ves algo que falta o algo que ya no funciona, me dices. La voy actualizando.""",
]


def humanize(text: str, model: str = "claude-haiku-4-5") -> str:
    """Rewrite text to remove AI patterns."""
    if not config.ANTHROPIC_API_KEY:
        return text
    import anthropic
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    resp = client.messages.create(
        model=model,
        max_tokens=600,
        system=HUMANIZER_SYSTEM,
        messages=[{"role": "user", "content": text}],
    )
    return resp.content[0].text.strip()


def generate_comment_reply(username: str) -> str:
    """Short public reply to comment (max ~100 chars)."""
    opener = random.choice(_REPLY_OPENERS).format(u=username)
    return opener


def generate_dm_message(username: str, guide_url: str, post_caption: str = "") -> str:
    """Full DM message with guide link, humanized."""
    template = random.choice(_DM_TEMPLATES).format(u=username, url=guide_url)
    return humanize(template)
