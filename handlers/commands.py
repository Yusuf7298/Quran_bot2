import random

from telegram import Update
from telegram.ext import ContextTypes

from core.config import AYAH_OF_THE_DAY, RECITERS_DATA, SURAH_NAMES
from core.i18n import t
from core.keyboards import (
    get_favorites_categories_keyboard,
    get_juz_keyboard,
    get_language_keyboard,
    get_main_menu_keyboard,
    get_reply_menu,
    get_settings_keyboard
)
from core.reminders import schedule_user_reminder
from core.state import (
    USER_LANG,
    USER_LAST_PLAYED,
    USER_STATS,
    get_all_favorites,
    track_user
)
async def send_reply_menu(update: Update):
    lang = USER_LANG[update.effective_user.id]
    await update.effective_chat.send_message(
        "Main menu is Ready",
        reply_markup=get_reply_menu(lang)
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    track_user(context, update.effective_chat.id, update.effective_user)
    lang = USER_LANG[user_id]
    text = t("welcome", lang)
    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard(lang, user_id)
    )
    await send_reply_menu(update)
    if context.application.job_queue:
        schedule_user_reminder(context.application.job_queue, update.effective_chat.id)


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    track_user(context, update.effective_chat.id, update.effective_user)
    lang = USER_LANG[user_id]
    await update.message.reply_text(
        t("menu", lang),
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard(lang, user_id)
    )
    await send_reply_menu(update)
    if context.application.job_queue:
        schedule_user_reminder(context.application.job_queue, update.effective_chat.id)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(context, update.effective_chat.id, update.effective_user)
    lang = USER_LANG[update.effective_user.id]
    await update.message.reply_text(
        t("help", lang),
        parse_mode="Markdown"
    )


async def health_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(context, update.effective_chat.id, update.effective_user)
    lang = USER_LANG[update.effective_user.id]
    await update.message.reply_text(t("bot_alive", lang))


async def ayah_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(context, update.effective_chat.id, update.effective_user)
    lang = USER_LANG[update.effective_user.id]
    ayah_ar, ayah_en, ref = random.choice(AYAH_OF_THE_DAY)
    text = f"{t('ayah', lang)}\n\n{ayah_ar}\n\n“{ayah_en}”\n\n— Qur’an {ref}"
    await update.message.reply_text(text, parse_mode="Markdown")


async def juz_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(context, update.effective_chat.id, update.effective_user)
    lang = USER_LANG[update.effective_user.id]
    await update.message.reply_text(
        t("choose_juz", lang),
        parse_mode="Markdown",
        reply_markup=get_juz_keyboard(lang)
    )


async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    track_user(context, update.effective_chat.id, update.effective_user)
    lang = USER_LANG[user_id]
    await update.message.reply_text(
        t("language", lang),
        parse_mode="Markdown",
        reply_markup=get_language_keyboard(lang)
    )


async def favorites_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    track_user(context, update.effective_chat.id, update.effective_user)
    lang = USER_LANG[user_id]
    await update.message.reply_text(
        t("favorites_categories_title", lang),
        parse_mode="Markdown",
        reply_markup=get_favorites_categories_keyboard(user_id, lang)
    )


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    track_user(context, update.effective_chat.id, update.effective_user)
    lang = USER_LANG[user_id]
    await update.message.reply_text(
        t("settings_title", lang),
        parse_mode="Markdown",
        reply_markup=get_settings_keyboard(lang)
    )


async def feedback_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(context, update.effective_chat.id, update.effective_user)
    lang = USER_LANG[update.effective_user.id]
    context.user_data["awaiting_feedback"] = True
    await update.message.reply_text(t("feedback_prompt", lang))


async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    track_user(context, update.effective_chat.id, update.effective_user)
    lang = USER_LANG[user_id]
    context.user_data["awaiting_search"] = True
    await update.message.reply_text(t("search_prompt", lang))


async def mystats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    track_user(context, update.effective_chat.id)
    lang = USER_LANG[user_id]
    stats = USER_STATS.get(user_id, {"plays": 0, "reciters": {}})
    top_reciter = "—"
    if stats.get("reciters"):
        top_id = max(stats["reciters"], key=stats["reciters"].get)
        top_reciter = RECITERS_DATA.get(top_id, {}).get("name", "—")
    last_played = "—"
    if USER_LAST_PLAYED.get(user_id):
        surah_num = USER_LAST_PLAYED[user_id].get("surah")
        if surah_num:
            last_played = f"{surah_num}. {SURAH_NAMES[surah_num - 1]}"
    favorites_count = len(get_all_favorites(user_id))
    await update.message.reply_text(
        t(
            "user_stats",
            lang,
            plays=stats.get("plays", 0),
            favorites=favorites_count,
            top_reciter=top_reciter,
            last_played=last_played
        ),
        parse_mode="Markdown"
    )
