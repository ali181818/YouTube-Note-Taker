# YouTube Note Taker

A multilingual Telegram bot that processes YouTube video transcripts and provides AI-generated summaries.

## Features

- Extract transcripts from YouTube videos
- Process transcripts using AI models (OpenAI, Anthropic Claude, or Google Gemini)
- Support for multiple languages (currently English and Persian)
- Real-time progress tracking with visual indicators
- User management with activation control
- Message history tracking
- Clean, object-oriented architecture

## Requirements

- Python 3.8+
- Telegram Bot API token
- API keys for at least one of the supported LLM platforms (OpenAI, Anthropic, or Google Gemini)
- Your Telegram user ID for admin notifications

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/ali181818/YouTube-Note-Taker.git
   cd YouTube-Note-Taker
   ```

2. Install required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with the following variables:

   ```
   # Telegram Bot Settings
   TOKEN_BOT=your_telegram_bot_token

   # LLM Settings
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   GEMINI_API_KEY=your_gemini_api_key
   DEFAULT_LLM=GEMINI

   # Admin Settings
   ADMIN_CHAT_ID=your_telegram_user_id
   ```

   > **Tip:** To find your Telegram user ID, you can use [@userinfobot](https://t.me/userinfobot) or [@get_id_bot](https://t.me/get_id_bot) on Telegram. Just start the bot and it will display your user ID.

## Usage

1. Start the bot:

   ```bash
   python main.py
   ```

2. Open Telegram and search for your bot by username

3. Start a conversation with the bot and send YouTube video links

## Bot Commands

- `/start` - Initialize the bot
- `/help` - Display help information
- `/status` - Check your account status
- `/language` - Change the bot language

## Admin Configuration

By default, new users will have their access set to inactive. To activate a user:

1. Find the user's chat ID in the database or the admin notification
2. Use an SQL client to update the user's status:
   ```sql
   UPDATE users SET is_active = 1 WHERE chat_id = user_chat_id;
   ```

Alternatively, you can modify the default in `app/database/models.py` to set `is_active = True` by default.

## Project Structure

```
project/
├── .env                  # Environment variables
├── README.md             # This file
├── main.py               # Entry point
├── requirements.txt      # Python dependencies
├── lang/                 # Language files
│   ├── en.json           # English translations
│   └── fa.json           # Persian translations
├── app/                  # Application code
│   ├── config.py         # Configuration and settings
│   ├── database/         # Database related code
│   │   ├── models.py     # SQLite database models
│   │   └── repository.py # Data access layer
│   ├── services/         # Core services
│   │   ├── youtube_service.py # YouTube API integration
│   │   └── llm_service.py     # LLM integration
│   └── telegram/         # Telegram bot code
│       ├── bot.py        # Bot initialization
│       ├── handlers.py   # Message handlers
│       └── utils.py      # Utility functions
```

## How It Works

1. The user sends a YouTube video link to the bot
2. The bot extracts the video ID using regex
3. The bot fetches the video transcript using the YouTube Transcript API
4. The transcript is processed and formatted for readability
5. The formatted transcript is sent to an LLM (Gemini, OpenAI, or Anthropic)
6. The LLM generates a concise summary of the video content
7. The summary is sent back to the user

Throughout this process, the bot provides real-time progress updates with visual indicators.

## Customization

### Adding New Languages

To add a new language:

1. Create a new JSON file in the `lang` directory (e.g., `de.json` for German)
2. Copy the structure from an existing language file and translate all values
3. Update the language selection keyboard in `app/telegram/handlers.py` to include the new language

### Customizing LLM Prompts

You can modify the default prompt template in `app/config.py` to change how the AI processes transcripts.

### Database Schema

The bot uses SQLite with two main tables:

1. `users` - Stores user information and preferences
2. `messages` - Records message history

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)

## Acknowledgements

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api)
- [pyfreeproxies](https://github.com/Simatwa/pyfreeproxies)
- [litellm](https://github.com/BerriAI/litellm)
