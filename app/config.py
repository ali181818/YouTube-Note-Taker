import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot token
BOT_TOKEN = os.getenv("TOKEN_BOT")

# LLM configurations
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DEFAULT_LLM = os.getenv("DEFAULT_LLM", "GEMINI")

# Admin chat ID
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))

# Database
DATABASE_URL = "sqlite:///bot_database.db"

# Base path for the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Language files
LANG_DIR = BASE_DIR / "lang"

def load_language(lang_code="en"):
    """Load language file"""
    try:
        lang_file = LANG_DIR / f"{lang_code}.json"
        with open(lang_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Fallback to English
        lang_file = LANG_DIR / "en.json"
        with open(lang_file, "r", encoding="utf-8") as f:
            return json.load(f)

# Default prompt template for the LLM

DEFAULT_PROMPT_TEMPLATE = """
You are a Smart Note Taker. Your job is to turn the transcript below into clear, structured, and memorable notes in the same language as the input, without copying large chunks verbatim.

1. What to Extract  
   - Paraphrase core ideas, definitions, and actionable takeaways.  
   - Focus on the most important points—make them stand out.

2. Telegram HTML Parse_Mode Formatting (see https://core.telegram.org/api/entities)  
   - Section titles: prepend an emoji and wrap in `<b>…</b>`.  
   - Bullet lists: start each line with a hyphen and a space.  
   - Emphasis on key terms: wrap in `<u>…</u>` (underline) only when needed.  
   - Code snippets: use `<code>…</code>` **only** for actual code or commands.  
   - Escape HTML characters:  
     - `&` → `&amp;`  
     - `<` → `&lt;`  
     - `>` → `&gt;`

3. Dynamic Section Titles  
   - Translate these titles into the transcript’s language, then use them with an emoji and `<b>` tags:  
     Overview  
     Key Insights  
     Details & Examples  
     Actions & Tips  
     Summary  

4. Note Structure  
   📌 <b>Overview</b>  
   - One or two sentences outlining the topic.

   📝 <b>Key Insights</b>  
   - <b>Title of first key point:</b> concise paraphrase.  
   - <b>Title of second key point:</b> concise paraphrase.

   🔍 <b>Details & Examples</b>  
   - Provide 2–4 highly detailed, specific examples with concrete data or scenarios (for instance: “When X happens, do Y by following these steps…”).

   🎯 <b>Actions & Tips</b>  
   - 2–4 practical steps or mnemonic aids.

   ✏️ <b>Summary</b>  
   - A brief take‑home message or reflection.

5. Length Limit  
   - Keep total output under 4000 characters.
---

Transcript:
{transcript}

---
important: Output must match the Transcript language (English, فارسی, etc.)
"""