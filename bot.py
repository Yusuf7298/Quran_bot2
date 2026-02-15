import logging
from datetime import time
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters
)
from core.config import BOT_TOKEN
from core.reminders import schedule_all_reminders
from core.state import load_state_into
from handlers.admin import admin_command, broadcast, customers_command, export_command, stats
from handlers.callbacks import handle_callback
from handlers.commands import (
    ayah_command,
    favorites_command,
    health_command,
    help_command,
    juz_command,
    language_command,
    menu,
    mystats_command,
    feedback_command,
    search_command,
    settings_command,
    start
)
from handlers.errors import error_handler
from handlers.text import text_handler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    if not BOT_TOKEN or not BOT_TOKEN.strip():
        logger.error("BOT_TOKEN is missing. Set it in the environment variables.")
        raise SystemExit(1)

    load_state_into()

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("health", health_command))
    application.add_handler(CommandHandler("ping", health_command))
    application.add_handler(CommandHandler("ayah", ayah_command))
    application.add_handler(CommandHandler("juz", juz_command))
    application.add_handler(CommandHandler("language", language_command))
    application.add_handler(CommandHandler("favorites", favorites_command))
    application.add_handler(CommandHandler("search", search_command))
    application.add_handler(CommandHandler("mystats", mystats_command))
    application.add_handler(CommandHandler("settings", settings_command))
    application.add_handler(CommandHandler("feedback", feedback_command))
    application.add_handler(CommandHandler("admin", admin_command))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("customers", customers_command))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("export", export_command))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    application.add_error_handler(error_handler)

    if application.job_queue:
        schedule_all_reminders(application.job_queue)
    else:
        logger.warning("⚠️ JobQueue not available — daily reminders disabled.")

    print("🚀 Quran Audience Bot is running via polling...")
    application.run_polling()


if __name__ == "__main__":
    main()
