import logging
from app.telegram.bot import TelegramBot

def main():
    """Main function to start the bot"""
    # Set up logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.WARNING  # Only WARNING and above will be shown
    )
    # Suppress httpx INFO logs as well
    logging.getLogger("httpx").setLevel(logging.WARNING)
    
    # Start the bot
    bot = TelegramBot()
    logging.info("Bot started. Press Ctrl+C to stop.")
    bot.run()

if __name__ == "__main__":
    main()