from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters

from app.config import BOT_TOKEN
from app.telegram.handlers import (
    start_command,
    help_command,
    status_command,
    language_command,
    language_callback,
    process_youtube_url
)

class TelegramBot:
    def __init__(self):
        """Initialize the Telegram bot"""
        self.application = ApplicationBuilder().token(BOT_TOKEN).build()
        self._register_handlers()
    
    def _register_handlers(self):
        """Register message handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", start_command))
        self.application.add_handler(CommandHandler("help", help_command))
        self.application.add_handler(CommandHandler("status", status_command))
        self.application.add_handler(CommandHandler("language", language_command))
        
        # Callback query handler for language selection
        self.application.add_handler(CallbackQueryHandler(language_callback, pattern="^lang_"))
        
        # Message handlers
        self.application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, 
            process_youtube_url
        ))
    
    def run(self):
        """Run the bot"""
        self.application.run_polling()