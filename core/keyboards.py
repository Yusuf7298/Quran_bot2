from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from core.config import ADMIN_IDS, LANGUAGES, QARI_COLUMNS, SURAH_COLUMNS, SURAH_NAMES
from core.i18n import t
from core.state import USER_FAVORITES, ensure_user_favorites
from core.utils import build_button_rows
def get_main_menu_keyboard(lang="en", user_id=None):
    rows = [
        [
            InlineKeyboardButton(t("btn_surahs", lang), callback_data="menu_surahs"),
            InlineKeyboardButton(t("btn_reciters", lang), callback_data="menu_reciters"),
        ],
        [
            InlineKeyboardButton(t("btn_juz", lang), callback_data="menu_juz"),
            InlineKeyboardButton(t("btn_ayah", lang), callback_data="menu_ayah"),
        ],
        [
            InlineKeyboardButton(t("btn_resume", lang), callback_data="menu_resume"),
            InlineKeyboardButton(t("btn_search", lang), callback_data="menu_search"),
        ],
        [
            InlineKeyboardButton(t("btn_favorites", lang), callback_data="menu_favorites"),
            InlineKeyboardButton(t("btn_language", lang), callback_data="menu_language"),
        ],
        [
            InlineKeyboardButton(t("btn_settings", lang), callback_data="menu_settings"),
            InlineKeyboardButton(t("btn_my_stats", lang), callback_data="menu_mystats"),
        ],
        [
            InlineKeyboardButton(t("btn_share", lang), callback_data="menu_share"),
            InlineKeyboardButton(t("btn_help", lang), callback_data="menu_help"),
        ],
        [
            InlineKeyboardButton(t("btn_support", lang), callback_data="menu_support"),
            InlineKeyboardButton(t("btn_feedback", lang), callback_data="menu_feedback"),
        ],
    ]
    if user_id in ADMIN_IDS:
        rows.append([InlineKeyboardButton(t("btn_admin", lang), callback_data="menu_admin")])
    return InlineKeyboardMarkup(rows)


def get_reply_menu(lang="en"):
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(t("btn_main_menu", lang)), KeyboardButton(t("reply_start", lang))],
            [KeyboardButton(t("reply_clear_menu", lang))]
        ],
        resize_keyboard=True
    )


def get_surah_keyboard(page=0, lang="en"):
    per_page = SURAH_COLUMNS * 4
    start = page * per_page
    end = start + per_page
    buttons = [
        InlineKeyboardButton(f"{i + 1}. {SURAH_NAMES[i]}", callback_data=f"play_{i + 1}")
        for i in range(start, min(end, len(SURAH_NAMES)))
    ]
    rows = build_button_rows(buttons, SURAH_COLUMNS)
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton(t("btn_prev", lang), callback_data=f"page_{page - 1}"))
    if end < len(SURAH_NAMES):
        nav.append(InlineKeyboardButton(t("btn_next", lang), callback_data=f"page_{page + 1}"))
    if nav:
        rows.append(nav)
    rows.append([InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")])
    return InlineKeyboardMarkup(rows)


def get_juz_keyboard(lang="en"):
    buttons = [InlineKeyboardButton(f"{t('btn_juz', lang)} {i + 1}", callback_data=f"juz_{i + 1}") for i in range(30)]
    rows = build_button_rows(buttons, 3)
    rows.append([InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")])
    return InlineKeyboardMarkup(rows)


def get_language_keyboard(lang="en"):
    buttons = [
        InlineKeyboardButton(name, callback_data=f"lang_{code}")
        for code, name in LANGUAGES.items()
    ]
    rows = build_button_rows(buttons, 2)
    rows.append([InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")])
    return InlineKeyboardMarkup(rows)


def get_favorites_keyboard(favs, lang="en", category=None):
    rows = []
    for s in sorted(favs):
        rows.append(
            [
                InlineKeyboardButton(f"{s}. {SURAH_NAMES[s - 1]}", callback_data=f"play_{s}"),
                InlineKeyboardButton(
                    t("btn_remove", lang),
                    callback_data=f"unfav_{s}_{category}" if category else f"unfav_{s}"
                )
            ]
        )
    rows.append([InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")])
    return InlineKeyboardMarkup(rows)


def get_settings_keyboard(lang="en"):
    rows = [
        [InlineKeyboardButton(t("btn_set_reciter", lang), callback_data="pref_reciter")],
        [InlineKeyboardButton(t("btn_cache", lang), callback_data="cache_info")],
        [InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")]
    ]
    return InlineKeyboardMarkup(rows)


def get_admin_dashboard_keyboard(lang="en"):
    rows = [
        [InlineKeyboardButton(t("btn_admin_broadcast", lang), callback_data="admin_broadcast")],
        [InlineKeyboardButton(t("btn_admin_stats", lang), callback_data="admin_stats")],
        [InlineKeyboardButton(t("btn_admin_customers", lang), callback_data="admin_customers")],
        [InlineKeyboardButton(t("btn_admin_export", lang), callback_data="admin_export")],
        [InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")]
    ]
    return InlineKeyboardMarkup(rows)


def get_favorites_categories_keyboard(user_id, lang="en"):
    ensure_user_favorites(user_id)
    rows = []
    for category, items in sorted(USER_FAVORITES[user_id].items()):
        rows.append([InlineKeyboardButton(f"{category} ({len(items)})", callback_data=f"favcat_{category}")])
    rows.append([InlineKeyboardButton(t("btn_all_favorites", lang), callback_data="favcat_all")])
    rows.append([InlineKeyboardButton(t("btn_add_category", lang), callback_data="favcat_add")])
    rows.append([InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")])
    return InlineKeyboardMarkup(rows)
