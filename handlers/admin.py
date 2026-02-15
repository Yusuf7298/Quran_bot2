import io
import json

from telegram import Update
from telegram.ext import ContextTypes

from datetime import datetime, timedelta

from core.config import ADMIN_IDS, LANGUAGES, RECITERS_DATA, SURAH_NAMES
from core.db import (
    get_cohort_size,
    get_daily_active,
    get_language_breakdown,
    get_retained_users,
    get_top_surahs
)
from core.i18n import t
from core.keyboards import get_admin_dashboard_keyboard
from core.state import (
    RECITER_PLAYS,
    USER_DEFAULT_RECITER,
    USER_FAVORITES,
    USER_LANG,
    USER_LAST_PLAYED,
    USER_PROFILES,
    USER_STATS,
    USERS,
    track_user
)


async def send_admin_dashboard(context: ContextTypes.DEFAULT_TYPE, chat_id: int, lang: str):
    await context.bot.send_message(
        chat_id=chat_id,
        text=t("admin_dashboard", lang),
        parse_mode="Markdown",
        reply_markup=get_admin_dashboard_keyboard(lang)
    )


async def send_stats_message(context: ContextTypes.DEFAULT_TYPE, chat_id: int, lang: str):
    total_users = len(USERS)
    reciter_counts = {}
    for stats_data in USER_STATS.values():
        for rec_id, count in stats_data.get("reciters", {}).items():
            reciter_counts[rec_id] = reciter_counts.get(rec_id, 0) + count
    top_reciters = sorted(reciter_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    text = t("stats_header", lang, total=total_users)
    today = datetime.utcnow().date().isoformat()
    yesterday = (datetime.utcnow().date() - timedelta(days=1)).isoformat()
    dau = get_daily_active(today)
    cohort = get_cohort_size(yesterday)
    retained = get_retained_users(yesterday, today)
    percent = round((retained / cohort) * 100, 1) if cohort else 0
    text += t("stats_dau", lang, count=dau)
    text += t("stats_retention", lang, percent=percent, retained=retained, cohort=cohort)
    text += t("stats_languages", lang)
    for code, count in get_language_breakdown():
        label = LANGUAGES.get(code, code or "unknown")
        text += f"- {label}: {count}\n"
    text += t("stats_top_surahs", lang)
    top_surahs = get_top_surahs(5)
    if not top_surahs:
        text += t("stats_no_surahs", lang)
    else:
        for surah_num, plays in top_surahs:
            surah_name = SURAH_NAMES[surah_num - 1] if 1 <= surah_num <= len(SURAH_NAMES) else str(surah_num)
            text += f"- {surah_num}. {surah_name}: {plays} {t('plays_label', lang)}\n"
    if not top_reciters:
        text += t("stats_no_reciters", lang)
    else:
        for rid, plays in top_reciters:
            reciter_name = RECITERS_DATA.get(rid, {}).get("name", rid)
            text += f"- {reciter_name}: {plays} {t('plays_label', lang)}\n"
    await context.bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")


async def send_customers_message(context: ContextTypes.DEFAULT_TYPE, chat_id: int, lang: str):
    usernames = []
    for uid in sorted(USERS):
        username = USER_PROFILES.get(uid, {}).get("username")
        if username:
            usernames.append(f"- @{username}")
    if not usernames:
        await context.bot.send_message(chat_id=chat_id, text=t("customers_empty", lang))
        return
    header = t("customers_header", lang, total=len(usernames))
    await context.bot.send_message(chat_id=chat_id, text="\n".join([header] + usernames))


async def send_export_data(context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    data = {
        "total_users": len(USERS),
        "users": sorted(list(USERS)),
        "favorites": {
            str(uid): {cat: sorted(list(items)) for cat, items in favs.items()}
            for uid, favs in USER_FAVORITES.items()
        },
        "languages": {str(uid): lang for uid, lang in USER_LANG.items()},
        "reciter_plays": dict(RECITER_PLAYS),
        "default_reciters": {str(uid): rec for uid, rec in USER_DEFAULT_RECITER.items()},
        "last_played": {str(uid): data for uid, data in USER_LAST_PLAYED.items()},
        "user_stats": {str(uid): stats for uid, stats in USER_STATS.items()},
    }
    payload = json.dumps(data, ensure_ascii=True, indent=2).encode("utf-8")
    buffer = io.BytesIO(payload)
    buffer.name = "bot_export.json"
    await context.bot.send_document(chat_id=chat_id, document=buffer, filename="bot_export.json")


async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    track_user(context, update.effective_chat.id, update.effective_user)
    lang = USER_LANG[user_id]
    if user_id not in ADMIN_IDS:
        await update.message.reply_text(t("admin_unauthorized", lang))
        return
    await send_admin_dashboard(context, update.effective_chat.id, lang)


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    track_user(context, update.effective_chat.id, update.effective_user)
    lang = USER_LANG[user_id]
    if user_id not in ADMIN_IDS:
        return
    if not context.args:
        context.user_data["awaiting_broadcast"] = True
        await update.message.reply_text(t("broadcast_prompt", lang))
        return
    message = " ".join(context.args)
    count = 0
    for chat_id in USERS:
        try:
            await context.bot.send_message(chat_id, message)
            count += 1
        except Exception:
            pass
    await update.message.reply_text(t("broadcast_sent", lang, count=count))


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    track_user(context, update.effective_chat.id, update.effective_user)
    lang = USER_LANG[user_id]
    if user_id not in ADMIN_IDS:
        return
    await send_stats_message(context, update.effective_chat.id, lang)


async def customers_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    track_user(context, update.effective_chat.id, update.effective_user)
    lang = USER_LANG[user_id]
    if user_id not in ADMIN_IDS:
        return
    await send_customers_message(context, update.effective_chat.id, lang)


async def export_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    track_user(context, update.effective_chat.id, update.effective_user)
    if user_id not in ADMIN_IDS:
        return
    await send_export_data(context, update.effective_chat.id)
