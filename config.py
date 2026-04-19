import os
from dotenv import load_dotenv

load_dotenv()

INSTAGRAM_USER_ID = os.environ["INSTAGRAM_USER_ID"]
INSTAGRAM_ACCESS_TOKEN = os.environ["INSTAGRAM_ACCESS_TOKEN"]
IMGBB_API_KEY = os.environ["IMGBB_API_KEY"]
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
POST_HOUR_UTC = int(os.getenv("POST_HOUR_UTC", "12"))
POST_MINUTE_UTC = int(os.getenv("POST_MINUTE_UTC", "0"))

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY", "")
FIGMA_ACCESS_TOKEN = os.getenv("FIGMA_ACCESS_TOKEN", "")

EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_APP_PASSWORD = os.environ["EMAIL_APP_PASSWORD"]
EMAIL_TO = os.environ["EMAIL_TO"]

INSTAGRAM_API_BASE = "https://graph.facebook.com/v21.0"

CLAUDE_BRAND = {
    "coral": "#D97757",
    "cream": "#FAF9F7",
    "dark": "#1A1816",
    "brown": "#8B6F4E",
    "beige": "#E8D5B0",
}

DEFAULT_HASHTAGS = (
    "#ClaudeAI #AnthropicAI #AITips #PromptEngineering #ClaudeProfessor "
    "#LearnAI #AITools #ArtificialIntelligence #AIAssistant #TechTips "
    "#MachineLearning #AIProductivity #ChatAI #FutureOfWork #AIHacks"
)
