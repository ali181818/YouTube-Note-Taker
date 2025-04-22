from app.config import load_language

class ProgressTracker:
    """Helper class to track and update progress messages"""
    def __init__(self, context, chat_id, lang_code="en"):
        self.context = context
        self.chat_id = chat_id
        self.message = None
        self.lang = load_language(lang_code)
    
    async def start(self):
        """Start tracking with 0% progress"""
        text = self._format_progress_message(0, self.lang["progress_start"])
        self.message = await self.context.bot.send_message(
            chat_id=self.chat_id,
            text=text
        )
        return self.message
    
    async def update(self, percentage, status_message):
        """Update progress message"""
        text = self._format_progress_message(percentage, status_message)
        if self.message:
            await self.context.bot.edit_message_text(
                chat_id=self.chat_id,
                message_id=self.message.message_id,
                text=text
            )
    
    async def complete(self):
        """Mark as complete and delete the progress message"""
        if self.message:
            await self.message.delete()
            self.message = None
    
    def _format_progress_message(self, percentage, status_message):
        """Format the progress message with emojis and percentage"""
        filled = int(percentage / 20)  # 5 blocks for 100%
        empty = 5 - filled
        
        progress_blocks = "🟩" * filled + "⬜️" * empty
        return f"{progress_blocks} {percentage}%\n{status_message}"