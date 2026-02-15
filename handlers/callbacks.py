import random
import urllib.parse

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import TimedOut
from telegram.ext import ContextTypes

from core.config import (
    AYAH_OF_THE_DAY,
    JUZ_START_SURAH,
    LANGUAGES,
    ADMIN_IDS,
    PRIVATE_CHANNEL_ID,
    QARI_COLUMNS,
    SURAH_COLUMNS,
    RECITERS_DATA,
    SHARE_MESSAGE,
    SURAH_NAMES
)
from core.i18n import t
from core.keyboards import (
    get_admin_dashboard_keyboard,
    get_favorites_categories_keyboard,
    get_favorites_keyboard,
    get_juz_keyboard,
    get_language_keyboard,
    get_main_menu_keyboard,
    get_settings_keyboard,
    get_surah_keyboard
)
from core.state import (
    USER_DEFAULT_RECITER,
    USER_FAVORITES,
    USER_LANG,
    USER_LAST_PLAYED,
    USER_STATS,
    ensure_user_favorites,
    get_all_favorites,
    save_state,
    track_user
)
from core.utils import build_button_rows, cache_stats, clear_cache, send_surah_audio
from handlers.admin import send_admin_dashboard, send_customers_message, send_export_data, send_stats_message


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try:
        await query.answer()
    except TimedOut:
        # Network hiccup while acknowledging callback; continue handling.
        pass
    data = query.data
    user_id = query.from_user.id
    lang = USER_LANG[user_id]
    if query.message:
        track_user(context, query.message.chat_id, query.from_user)

    if data == "menu_main":
        context.user_data.pop("awaiting_feedback", None)
        await query.edit_message_text(
            t("menu", lang),
            parse_mode="Markdown",
            reply_markup=get_main_menu_keyboard(lang, user_id)
        )

    elif data == "menu_surahs":
        await query.edit_message_text(
            t("choose_surah", lang),
            parse_mode="Markdown",
            reply_markup=get_surah_keyboard(0, lang)
        )

    elif data == "menu_reciters":
        buttons = [
            InlineKeyboardButton(info["name"], callback_data=f"reciter_{rid}")
            for rid, info in RECITERS_DATA.items()
        ]
        rows = build_button_rows(buttons, QARI_COLUMNS)
        rows.append([InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")])
        await query.edit_message_text(
            t("choose_reciter", lang),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(rows)
        )

    elif data.startswith("reciter_"):
        reciter_id = data.replace("reciter_", "")
        context.user_data["selected_reciter"] = reciter_id
        USER_DEFAULT_RECITER[user_id] = reciter_id
        save_state()
        await query.edit_message_text(
            t(
                "reciter_selected",
                lang,
                reciter=RECITERS_DATA[reciter_id]["name"],
                choose_surah=t("choose_surah", lang)
            ),
            parse_mode="Markdown",
            reply_markup=get_surah_keyboard(0, lang)
        )

    elif data.startswith("page_"):
        page = int(data.replace("page_", ""))
        await query.edit_message_text(
            t("choose_surah", lang),
            parse_mode="Markdown",
            reply_markup=get_surah_keyboard(page, lang)
        )

    elif data == "menu_juz":
        context.user_data["selected_reciter"] = context.user_data.get("selected_reciter") or USER_DEFAULT_RECITER.get(user_id, "r01")
        await query.edit_message_text(
            t("choose_juz", lang),
            parse_mode="Markdown",
            reply_markup=get_juz_keyboard(lang)
        )

    elif data == "menu_resume":
        last = USER_LAST_PLAYED.get(user_id)
        if not last:
            await query.edit_message_text(
                t("resume_empty", lang),
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")]])
            )
            return
        rec_id = last.get("reciter", USER_DEFAULT_RECITER.get(user_id, "r01"))
        surah_num = last.get("surah")
        await send_surah_audio(context, query.message.chat_id, user_id, surah_num, rec_id, lang)

    elif data == "menu_search":
        context.user_data["awaiting_search"] = True
        await query.edit_message_text(
            t("search_prompt", lang),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")]])
        )

    elif data == "menu_settings":
        await query.edit_message_text(
            t("settings_title", lang),
            parse_mode="Markdown",
            reply_markup=get_settings_keyboard(lang)
        )

    elif data == "menu_mystats":
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
        await query.edit_message_text(
            t(
                "user_stats",
                lang,
                plays=stats.get("plays", 0),
                favorites=favorites_count,
                top_reciter=top_reciter,
                last_played=last_played
            ),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")]])
        )

    elif data == "pref_reciter":
        buttons = [
            InlineKeyboardButton(info["name"], callback_data=f"pref_reciter_{rid}")
            for rid, info in RECITERS_DATA.items()
        ]
        rows = build_button_rows(buttons, QARI_COLUMNS)
        rows.append([InlineKeyboardButton(t("btn_back", lang), callback_data="menu_settings")])
        await query.edit_message_text(
            t("choose_reciter", lang),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(rows)
        )

    elif data.startswith("pref_reciter_"):
        rec_id = data.replace("pref_reciter_", "")
        USER_DEFAULT_RECITER[user_id] = rec_id
        save_state()
        await query.edit_message_text(
            t("default_reciter_set", lang, reciter=RECITERS_DATA[rec_id]["name"]),
            reply_markup=get_settings_keyboard(lang)
        )

    elif data == "cache_info":
        count, size_mb = cache_stats()
        await query.edit_message_text(
            f"{t('cache_title', lang)}\n\n{t('cache_stats', lang, count=count, size_mb=size_mb)}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t("btn_clear_cache", lang), callback_data="cache_clear")],
                [InlineKeyboardButton(t("btn_back", lang), callback_data="menu_settings")]
            ])
        )

    elif data == "cache_clear":
        clear_cache()
        count, size_mb = cache_stats()
        await query.edit_message_text(
            f"{t('cache_title', lang)}\n\n{t('cache_cleared', lang)}\n{t('cache_stats', lang, count=count, size_mb=size_mb)}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_settings")]])
        )

    elif data == "menu_favorites":
        await query.edit_message_text(
            t("favorites_categories_title", lang),
            parse_mode="Markdown",
            reply_markup=get_favorites_categories_keyboard(user_id, lang)
        )

    elif data.startswith("favcat_"):
        category = data.replace("favcat_", "")
        ensure_user_favorites(user_id)
        pending_surah = context.user_data.get("awaiting_pick_category")
        if pending_surah and category not in {"add", "all"}:
            context.user_data.pop("awaiting_pick_category", None)
            USER_FAVORITES[user_id].setdefault(category, set()).add(pending_surah)
            save_state()
            await query.edit_message_text(
                t("favorite_added", lang),
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")]])
            )
            return
        if category == "add":
            if pending_surah:
                context.user_data["pending_fav_surah"] = pending_surah
            context.user_data["awaiting_category_name"] = True
            await query.edit_message_text(
                t("category_prompt", lang),
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_favorites")]])
            )
        elif category == "all":
            favs = get_all_favorites(user_id)
            if not favs:
                await query.edit_message_text(
                    t("no_favorites", lang),
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")]])
                )
                return
            await query.edit_message_text(
                t("favorites_all_title", lang),
                parse_mode="Markdown",
                reply_markup=get_favorites_keyboard(favs, lang)
            )
        else:
            favs = USER_FAVORITES[user_id].get(category, set())
            if not favs:
                await query.edit_message_text(
                    t("no_favorites", lang),
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_favorites")]])
                )
                return
            await query.edit_message_text(
                t("favorites_category_title", lang, category=category),
                parse_mode="Markdown",
                reply_markup=get_favorites_keyboard(favs, lang, category)
            )

    elif data.startswith("juz_"):
        juz_num = int(data.replace("juz_", ""))
        start_surah = JUZ_START_SURAH[juz_num - 1]
        end_surah = JUZ_START_SURAH[juz_num] - 1 if juz_num < 30 else 114
        buttons = [
            InlineKeyboardButton(f"{i}. {SURAH_NAMES[i - 1]}", callback_data=f"play_{i}")
            for i in range(start_surah, end_surah + 1)
        ]
        rows = build_button_rows(buttons, SURAH_COLUMNS)
        rows.append([InlineKeyboardButton(t("btn_change_reciter", lang), callback_data="menu_reciters")])
        rows.append([InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")])
        await query.edit_message_text(
            t("juz_select_surah", lang, juz=juz_num),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(rows)
        )

    elif data.startswith("play_"):
        surah_num = int(data.replace("play_", ""))
        rec_id = context.user_data.get("selected_reciter") or USER_DEFAULT_RECITER.get(user_id, "r01")
        chat_id = query.message.chat_id
        await send_surah_audio(context, chat_id, user_id, surah_num, rec_id, lang)

    elif data.startswith("download_"):
        surah_num = int(data.replace("download_", ""))
        rec_id = context.user_data.get("selected_reciter") or USER_DEFAULT_RECITER.get(user_id, "r01")
        reciter = RECITERS_DATA[rec_id]
        target_id = reciter["start_msg_id"] + (surah_num - 1)
        chat_id = query.message.chat_id
        try:
            await context.bot.copy_message(
                chat_id=chat_id,
                from_chat_id=PRIVATE_CHANNEL_ID,
                message_id=target_id
            )
        except Exception:
            await context.bot.send_message(chat_id=chat_id, text=t("download_failed", lang))

    elif data.startswith("fav_"):
        surah_num = int(data.replace("fav_", ""))
        ensure_user_favorites(user_id)
        if surah_num in get_all_favorites(user_id):
            await query.answer(t("favorite_exists", lang))
        else:
            context.user_data["awaiting_pick_category"] = surah_num
            context.user_data["pending_fav_surah"] = surah_num
            categories = get_favorites_categories_keyboard(user_id, lang)
            await query.edit_message_text(
                t("pick_category", lang),
                parse_mode="Markdown",
                reply_markup=categories
            )

    elif data.startswith("unfav_"):
        parts = data.replace("unfav_", "").split("_", 1)
        surah_num = int(parts[0])
        category = parts[1] if len(parts) > 1 else None
        ensure_user_favorites(user_id)
        removed = False
        if category and category in USER_FAVORITES[user_id]:
            if surah_num in USER_FAVORITES[user_id][category]:
                USER_FAVORITES[user_id][category].remove(surah_num)
                removed = True
        else:
            for items in USER_FAVORITES[user_id].values():
                if surah_num in items:
                    items.remove(surah_num)
                    removed = True
        if removed:
            save_state()
            await query.answer(t("favorite_removed", lang))
        else:
            await query.answer(t("favorite_missing", lang))

        if query.message and query.message.text:
            if category:
                favs = USER_FAVORITES[user_id].get(category, set())
                if not favs:
                    await query.edit_message_text(
                        t("no_favorites", lang),
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_favorites")]])
                    )
                else:
                    await query.edit_message_text(
                        t("favorites_category_title", lang, category=category),
                        parse_mode="Markdown",
                        reply_markup=get_favorites_keyboard(favs, lang, category)
                    )
            else:
                favs = get_all_favorites(user_id)
                if not favs:
                    await query.edit_message_text(
                        t("no_favorites", lang),
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")]])
                    )
                else:
                    await query.edit_message_text(
                        t("favorites_all_title", lang),
                        parse_mode="Markdown",
                        reply_markup=get_favorites_keyboard(favs, lang)
                    )

    elif data == "menu_ayah":
        ayah_ar, ayah_en, ref = random.choice(AYAH_OF_THE_DAY)
        text = f"{t('ayah', lang)}\n\n{ayah_ar}\n\n“{ayah_en}”\n\n— Qur’an {ref}"
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")]])
        )

    elif data == "menu_language":
        await query.edit_message_text(
            t("language", lang),
            parse_mode="Markdown",
            reply_markup=get_language_keyboard(lang)
        )

    elif data.startswith("lang_"):
        new_lang = data.replace("lang_", "")
        USER_LANG[user_id] = new_lang
        save_state()
        await query.edit_message_text(
            t("language_set", new_lang, language=LANGUAGES[new_lang]),
            reply_markup=get_main_menu_keyboard(new_lang, user_id)
        )

    elif data == "menu_share":
        share_url = "https://t.me/share/url"
        encoded_text = urllib.parse.quote(SHARE_MESSAGE)
        share_text = t("share_this_bot", lang, url=f"{share_url}?text={encoded_text}")
        await query.edit_message_text(
            share_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")]])
        )

    elif data == "menu_help":
        help_text = t("help", lang)
        await query.edit_message_text(
            help_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")]])
        )

    elif data == "menu_support":
        await query.edit_message_text(
            t("socials", lang),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")]])
        )

    elif data == "menu_feedback":
        context.user_data["awaiting_feedback"] = True
        await query.edit_message_text(
            t("feedback_prompt", lang),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")]])
        )

    elif data == "menu_admin":
        if user_id not in ADMIN_IDS:
            await query.edit_message_text(
                t("admin_unauthorized", lang),
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")]])
            )
            return
        await query.edit_message_text(
            t("admin_dashboard", lang),
            parse_mode="Markdown",
            reply_markup=get_admin_dashboard_keyboard(lang)
        )

    elif data == "admin_broadcast":
        if user_id not in ADMIN_IDS:
            await query.edit_message_text(
                t("admin_unauthorized", lang),
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")]])
            )
            return
        context.user_data["awaiting_broadcast"] = True
        await query.edit_message_text(
            t("broadcast_prompt", lang),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_admin")]])
        )

    elif data == "admin_stats":
        if user_id not in ADMIN_IDS:
            return
        await send_stats_message(context, query.message.chat_id, lang)

    elif data == "admin_customers":
        if user_id not in ADMIN_IDS:
            return
        await send_customers_message(context, query.message.chat_id, lang)

    elif data == "admin_export":
        if user_id not in ADMIN_IDS:
            return
        await send_export_data(context, query.message.chat_id)
