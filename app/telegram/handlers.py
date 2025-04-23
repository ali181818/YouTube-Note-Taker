import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from app.database.models import get_db
from app.database.repository import UserRepository, MessageRepository
from app.services.youtube_service import YouTubeService, TextFormatter
from app.services.llm_service import LLMService
from app.config import load_language , ADMIN_CHAT_ID
from app.telegram.utils import ProgressTracker

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command"""
    chat_id = update.effective_chat.id
    user_name = update.effective_user.first_name
    
    # Get or create user in database
    db = get_db()
    user = UserRepository.get_user(db, chat_id)
    
    if not user:
        user = UserRepository.create_user(db, chat_id, user_name, is_active = (chat_id == ADMIN_CHAT_ID))
        # Inform admin about new user
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"New user registered: {user_name} (ID: {chat_id})"
        )
    
    # Load language based on user preference
    lang = load_language(user.language)
    
    await update.message.reply_text(lang["welcome"])

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command"""
    chat_id = update.effective_chat.id
    
    # Get user language preference
    db = get_db()
    user = UserRepository.get_user(db, chat_id)
    lang_code = user.language if user else "en"
    lang = load_language(lang_code)
    await update.message.reply_text(lang["help_message"])

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /status command"""
    chat_id = update.effective_chat.id
    
    # Get user status
    db = get_db()
    user = UserRepository.get_user(db, chat_id)
    
    if not user:
        lang = load_language("en")
        await update.message.reply_text(lang["inactive_user"])
        return
    
    lang = load_language(user.language)
    
    if user.is_active:
        await update.message.reply_text(lang["status_active"])
    else:
        await update.message.reply_text(lang["status_inactive"])

async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /language command"""
    chat_id = update.effective_chat.id
    
    # Get user
    db = get_db()
    user = UserRepository.get_user(db, chat_id)
    lang_code = user.language if user else "en"
    lang = load_language(lang_code)
    
    # Create language selection keyboard
    keyboard = [
        [
            InlineKeyboardButton("English", callback_data="lang_en"),
            InlineKeyboardButton("فارسی", callback_data="lang_fa")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        text=lang["choose_language"],
        reply_markup=reply_markup
    )

async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle language selection callback"""
    query = update.callback_query
    chat_id = query.message.chat_id
    selected_lang = query.data.split("_")[1]
    
    # Update user language preference
    db = get_db()
    user = UserRepository.get_user(db, chat_id)
    
    if user:
        UserRepository.update_user_language(db, chat_id, selected_lang)
    
    # Load selected language
    lang = load_language(selected_lang)
    
    # Determine language name
    language_name = "English" if selected_lang == "en" else "فارسی"
    response = lang["language_selected"].format(language=language_name)
    
    await query.answer()
    await query.edit_message_text(text=response)

async def process_youtube_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process YouTube URLs"""
    chat_id = update.effective_chat.id
    message_id = update.message.message_id
    message_text = update.message.text
    
    # Get user from database
    db = get_db()
    user = UserRepository.get_user(db, chat_id)
    
    if not user:
        # Create user if not exists
        user_name = update.effective_user.first_name
        user = UserRepository.create_user(db, chat_id, user_name)
    
    # Check if user is active
    if not user.is_active:
        lang = load_language(user.language)
        await update.message.reply_text(lang["inactive_user"])
        return
    
    # Store the message
    MessageRepository.create_message(db, message_id, chat_id, message_text)
    
    # Load language
    lang = load_language(user.language)
    
    # Initialize progress tracker
    progress = ProgressTracker(context, chat_id, user.language)
    await progress.start()
    
    try:
        # Extract video ID
        await progress.update(20, lang["extracting_id"])
        video_id = YouTubeService.extract_video_id(message_text)
        
        if not video_id:
            await progress.complete()
            await update.message.reply_text(lang["invalid_url"])
            return
        
        # Get transcript
        try:
            formatted_transcript, used_proxy = await YouTubeService.get_transcript(
                video_id, progress=progress, lang=lang
            )
        except Exception:
            await progress.complete()
            await update.message.reply_text(lang["no_transcript"])
            return

        # Process with LLM
        await progress.update(60, lang["processing_transcript"])
        llm_service = LLMService()
        result = llm_service.process_transcript(formatted_transcript)
        
        # Send result
        await progress.update(80, lang["sending_result"])
        await update.message.reply_text(result, parse_mode="HTML")
        
        # Complete and remove progress message
        await progress.complete()
        
    except Exception as e:
        logger.error(f"Error processing URL: {str(e)}")
        await progress.complete()
        error_message = lang["processing_error"].format(error=str(e))
        await update.message.reply_text(error_message)