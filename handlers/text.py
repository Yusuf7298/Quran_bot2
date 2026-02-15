from datetime import datetime
import urllib.parse

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes

from core.config import ADMIN_IDS, QARI_COLUMNS, RECITERS_DATA, SHARE_MESSAGE, SURAH_NAMES
from core.db import save_feedback
from core.i18n import is_peace_greeting, matches_label, t
from core.keyboards import get_main_menu_keyboard, get_surah_keyboard
from core.reminders import schedule_user_reminder
from core.state import (
    USER_DEFAULT_RECITER,
    USER_FAVORITES,
    USER_LANG,
    USER_LAST_PLAYED,
    ensure_user_favorites,
    save_state,
    track_user
)
from core.utils import build_button_rows, send_surah_audio
from handlers.admin import broadcast
from handlers.commands import (
    ayah_command,
    favorites_command,
    feedback_command,
    help_command,
    juz_command,
    language_command,
    menu,
    mystats_command,
    search_command,
    settings_command,
    start
)
from handlers.admin import admin_command


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    track_user(context, update.effective_chat.id, update.effective_user)
    text = update.message.text.strip()
    text_lower = text.lower()
    user_id = update.effective_user.id
    lang = USER_LANG[user_id]

    if context.user_data.get("awaiting_broadcast") and user_id in ADMIN_IDS:
        context.user_data["awaiting_broadcast"] = False
        if not text:
            await update.message.reply_text(t("broadcast_prompt", lang))
            return
        context.args = text.split()
        await broadcast(update, context)
        return

    if context.user_data.get("awaiting_feedback"):
        context.user_data["awaiting_feedback"] = False
        if not text:
            await update.message.reply_text(t("feedback_prompt", lang))
            return
        is_greeting = is_peace_greeting(text, lang)
        username = update.effective_user.username
        created_at = datetime.utcnow().isoformat(timespec="seconds")
        save_feedback(user_id, username, text, created_at)
        for admin_id in ADMIN_IDS:
            try:
                await context.bot.send_message(
                    admin_id,
                    f"📩 Feedback from {user_id}{f' (@{username})' if username else ''}:\n{text}"
                )
            except Exception:
                pass
        if is_greeting:
            await update.message.reply_text(
                f"{t('peace_response', lang)}\n\n{t('feedback_sent', lang)}"
            )
        else:
            await update.message.reply_text(t("feedback_sent", lang))
        return

    if context.user_data.get("awaiting_search"):
        context.user_data["awaiting_search"] = False
        query = text.strip()
        if not query:
            await update.message.reply_text(t("search_prompt", lang))
            return
        matches = []
        if query.isdigit():
            num = int(query)
            if 1 <= num <= len(SURAH_NAMES):
                matches = [num]
        else:
            for idx, name in enumerate(SURAH_NAMES, start=1):
                if query.lower() in name.lower():
                    matches.append(idx)
        if not matches:
            await update.message.reply_text(t("search_no_results", lang))
            return
        limited = matches[:24]
        buttons = [
            InlineKeyboardButton(f"{i}. {SURAH_NAMES[i - 1]}", callback_data=f"play_{i}")
            for i in limited
        ]
        rows = build_button_rows(buttons, 3)
        rows.append([InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")])
        await update.message.reply_text(
            t("search_results", lang, query=query, count=len(limited), total=len(matches)),
            reply_markup=InlineKeyboardMarkup(rows)
        )
        return

    if context.user_data.get("awaiting_category_name"):
        context.user_data["awaiting_category_name"] = False
        category = text.strip()
        if not category or len(category) > 32:
            await update.message.reply_text(t("category_invalid", lang))
            return
        ensure_user_favorites(user_id)
        if category in USER_FAVORITES[user_id]:
            await update.message.reply_text(t("category_exists", lang))
            return
        USER_FAVORITES[user_id][category] = set()
        pending_surah = context.user_data.pop("pending_fav_surah", None)
        if pending_surah:
            USER_FAVORITES[user_id][category].add(pending_surah)
        save_state()
        if pending_surah:
            await update.message.reply_text(
                f"{t('category_added', lang, category=category)}\n{t('favorite_added', lang)}"
            )
        else:
            await update.message.reply_text(t("category_added", lang, category=category))
        return

    if matches_label(text, "btn_surahs"):
        await update.message.reply_text(
            t("choose_surah", lang),
            parse_mode="Markdown",
            reply_markup=get_surah_keyboard(0, lang)
        )
        return

    if matches_label(text, "btn_reciters"):
        buttons = [
            InlineKeyboardButton(info["name"], callback_data=f"reciter_{rid}")
            for rid, info in RECITERS_DATA.items()
        ]
        rows = build_button_rows(buttons, QARI_COLUMNS)
        rows.append([InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")])
        await update.message.reply_text(
            t("choose_reciter", lang),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(rows)
        )
        return

    if matches_label(text, "btn_juz"):
        await juz_command(update, context)
        return

    if matches_label(text, "btn_ayah"):
        await ayah_command(update, context)
        return

    if matches_label(text, "btn_resume"):
        last = USER_LAST_PLAYED.get(user_id)
        if not last:
            await update.message.reply_text(
                t("resume_empty", lang),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")]
                ])
            )
            return
        rec_id = last.get("reciter", USER_DEFAULT_RECITER.get(user_id, "r01"))
        surah_num = last.get("surah")
        await send_surah_audio(context, update.effective_chat.id, user_id, surah_num, rec_id, lang)
        return

    if matches_label(text, "btn_search"):
        await search_command(update, context)
        return

    if matches_label(text, "btn_favorites"):
        await favorites_command(update, context)
        return

    if matches_label(text, "btn_language"):
        await language_command(update, context)
        return

    if matches_label(text, "btn_settings"):
        await settings_command(update, context)
        return

    if matches_label(text, "btn_my_stats"):
        await mystats_command(update, context)
        return

    if matches_label(text, "btn_share"):
        share_url = "https://t.me/share/url"
        encoded_text = urllib.parse.quote(SHARE_MESSAGE)
        share_text = t("share_this_bot", lang, url=f"{share_url}?text={encoded_text}")
        await update.message.reply_text(
            share_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")]
            ])
        )
        return

    if matches_label(text, "btn_help"):
        await help_command(update, context)
        return

    if matches_label(text, "btn_support"):
        await update.message.reply_text(
            t("socials", lang),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")]
            ])
        )
        return

    if matches_label(text, "btn_feedback"):
        await feedback_command(update, context)
        return

    if matches_label(text, "btn_admin"):
        await admin_command(update, context)
        return

    if text_lower in {"main menu", "menu"} or matches_label(text, "btn_main_menu"):
        await menu(update, context)
        return
    if text_lower == "start" or matches_label(text, "reply_start"):
        await start(update, context)
        return
    if text_lower == "clear menu" or matches_label(text, "reply_clear_menu"):
        await update.message.reply_text(t("menu_cleared", lang), reply_markup=ReplyKeyboardRemove())
        return
    if "surah" in text_lower or "quran" in text_lower:
        await menu(update, context)
    else:
        await update.message.reply_text(t("use_menu", lang))
