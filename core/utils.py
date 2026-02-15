import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from core.config import AUDIO_CACHE_DIR, PRIVATE_CHANNEL_ID, RECITERS_DATA, SURAH_NAMES
from core.i18n import t
from core.db import increment_surah_play
from core.state import RECITER_PLAYS, USER_LAST_PLAYED, USER_STATS, get_all_favorites, save_state
logger = logging.getLogger(__name__)
def build_button_rows(buttons, columns):
    return [buttons[i:i + columns] for i in range(0, len(buttons), columns)]


def cache_stats():
    if not os.path.exists(AUDIO_CACHE_DIR):
        return 0, 0.0
    total_size = 0
    file_count = 0
    for root, _, files in os.walk(AUDIO_CACHE_DIR):
        for name in files:
            file_count += 1
            try:
                total_size += os.path.getsize(os.path.join(root, name))
            except OSError:
                continue
    size_mb = round(total_size / (1024 * 1024), 2)
    return file_count, size_mb


def clear_cache():
    if not os.path.exists(AUDIO_CACHE_DIR):
        return
    for root, _, files in os.walk(AUDIO_CACHE_DIR):
        for name in files:
            try:
                os.remove(os.path.join(root, name))
            except OSError:
                continue


async def send_surah_audio(context, chat_id, user_id, surah_num, rec_id, lang):
    reciter = RECITERS_DATA[rec_id]
    target_id = reciter["start_msg_id"] + (surah_num - 1)
    try:
        await context.bot.copy_message(
            chat_id=chat_id,
            from_chat_id=PRIVATE_CHANNEL_ID,
            message_id=target_id
        )
        await context.bot.send_message(
            chat_id=chat_id,
            text=t(
                "now_playing",
                lang,
                surah=SURAH_NAMES[surah_num - 1],
                reciter=reciter["name"]
            ),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        t("btn_remove", lang) if surah_num in get_all_favorites(user_id) else t("btn_favorite", lang),
                        callback_data=f"unfav_{surah_num}" if surah_num in get_all_favorites(user_id) else f"fav_{surah_num}"
                    ),
                    InlineKeyboardButton(t("btn_download", lang), callback_data=f"download_{surah_num}")
                ],
                [
                    InlineKeyboardButton(t("btn_change_reciter", lang), callback_data="menu_reciters"),
                    InlineKeyboardButton(t("btn_main_menu", lang), callback_data="menu_main")
                ]
            ])
        )
        RECITER_PLAYS[rec_id] += 1
        increment_surah_play(surah_num)
        USER_LAST_PLAYED[user_id] = {"surah": surah_num, "reciter": rec_id}
        USER_STATS[user_id]["plays"] = USER_STATS[user_id].get("plays", 0) + 1
        reciters = USER_STATS[user_id].setdefault("reciters", {})
        reciters[rec_id] = reciters.get(rec_id, 0) + 1
        save_state()
    except Exception as exc:
        logger.error("Audio send failed: %s", exc)
        await context.bot.send_message(chat_id=chat_id, text=t("audio_not_found", lang))
