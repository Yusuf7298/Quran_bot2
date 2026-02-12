import io
import json
import logging
import os
import random
from datetime import time
from collections import defaultdict

from dotenv import load_dotenv

from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)

# ==================== CONFIG ====================
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")  # Set by Render
PORT = int(os.getenv("PORT", 10000))

PRIVATE_CHANNEL_ID = -1003806159829  # Your private channel ID
ADMIN_IDS = {5726141414}  # Replace with your Telegram user ID(s)

DATA_DIR = "data"
STATE_FILE = os.path.join(DATA_DIR, "bot_state.json")

SURAH_COLUMNS = 6
QARI_COLUMNS = 2

os.makedirs(DATA_DIR, exist_ok=True)

# ==================== LOGGING ====================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==================== DATA ====================

SURAH_NAMES = [
    "Al-Fatihah", "Al-Baqarah", "Aal-E-Imran", "An-Nisa", "Al-Ma'idah",
    "Al-An'am", "Al-A'raf", "Al-Anfal", "At-Tawbah", "Yunus", "Hud", "Yusuf",
    "Ar-Ra'd", "Ibrahim", "Al-Hijr", "An-Nahl", "Al-Isra", "Al-Kahf", "Maryam",
    "Ta-Ha", "Al-Anbiya", "Al-Hajj", "Al-Mu’minun", "An-Nur", "Al-Furqan",
    "Ash-Shu'ara", "An-Naml", "Al-Qasas", "Al-Ankabut", "Ar-Rum", "Luqman",
    "As-Sajdah", "Al-Ahzab", "Saba", "Fatir", "Ya-Sin", "As-Saffat", "Sad",
    "Az-Zumar", "Ghafir", "Fussilat", "Ash-Shura", "Az-Zukhruf", "Ad-Dukhan",
    "Al-Jathiyah", "Al-Ahqaf", "Muhammad", "Al-Fath", "Al-Hujurat", "Qaf",
    "Adh-Dhariyat", "At-Tur", "An-Najm", "Al-Qamar", "Ar-Rahman", "Al-Waqi'ah",
    "Al-Hadid", "Al-Mujadila", "Al-Hashr", "Al-Mumtahanah", "As-Saff",
    "Al-Jumu'ah", "Al-Munafiqun", "At-Taghabun", "At-Talaq", "At-Tahrim",
    "Al-Mulk", "Al-Qalam", "Al-Haqqah", "Al-Ma'arij", "Nuh", "Al-Jinn",
    "Al-Muzzammil", "Al-Muddaththir", "Al-Qiyamah", "Al-Insan", "Al-Mursalat",
    "An-Naba", "An-Nazi'at", "Abasa", "At-Takwir", "Al-Infitar", "Al-Mutaffifin",
    "Al-Inshiqaq", "Al-Buruj", "At-Tariq", "Al-A'la", "Al-Ghashiyah", "Al-Fajr",
    "Al-Balad", "Ash-Shams", "Al-Layl", "Ad-Duha", "Ash-Sharh", "At-Tin",
    "Al-Alaq", "Al-Qadr", "Al-Bayyinah", "Az-Zalzalah", "Al-Adiyat", "Al-Qari'ah",
    "At-Takathur", "Al-Asr", "Al-Humazah", "Al-Fil", "Quraysh", "Al-Ma'un",
    "Al-Kawthar", "Al-Kafirun", "An-Nasr", "Al-Masad", "Al-Ikhlas", "Al-Falaq",
    "An-Nas"
]

JUZ_START_SURAH = [
    1, 2, 2, 4, 4, 5, 6, 7, 8, 9,
    11, 12, 14, 15, 17, 18, 21, 23, 25, 27,
    29, 33, 36, 39, 41, 46, 51, 58, 67, 78
]

RECITERS_DATA = {
    "r01": {"name": "Mishary Rashid Alafasy", "start_msg_id": 3},
    "r02": {"name": "Abu Bakr Al-Shatri", "start_msg_id": 119},
    "r03": {"name": "Abdul Basit Abdul Samad", "start_msg_id": 234},
    "r04": {"name": "Abdul Rahman Al-Sudais", "start_msg_id": 349},
    "r05": {"name": "Mohammed Al-Luhaidan", "start_msg_id": 464},
    "r06": {"name": "Sheikh Maher Al-Muaiqly", "start_msg_id": 579},
    "r07": {"name": "Sheikh Saud Al-Shuraim", "start_msg_id": 693},
    "r08": {"name": "Yasser Al-Qureshi", "start_msg_id": 808},
    "r09": {"name": "Sheikh Mohammed Ayyub", "start_msg_id": 923},
    "r10": {"name": "Mahmoud Khalil Al-Hussary", "start_msg_id": 1038},
    "r11": {"name": "Abdullah Awad Al-Johany", "start_msg_id": 1153},
    "r12": {"name": "Abdullah ibn Ali Basfar", "start_msg_id": 1384},
    "r13": {"name": "Sheikh Adel Rayan", "start_msg_id": 1499},
    "r14": {"name": "Abdul Rahman Al Ossi", "start_msg_id": 1614},
    "r15": {"name": "Mohammad Saleh Alim Shah", "start_msg_id": 1729},
    "r16": {"name": "Abdul Muhsin Al Qasim", "start_msg_id": 1844},
    "r17": {"name": "Sheikh Abdul Wadood Haneef", "start_msg_id": 1959},
    "r18": {"name": "Sheikh Yasser Al-Dosari", "start_msg_id": 2074},
    "r19": {"name": "Sheikh Muhammad Jibril", "start_msg_id": 2189},
    "r20": {"name": "Sheikh Idris Abkar", "start_msg_id": 2649},
}

RECITER_PLAYS = defaultdict(int)
USER_FAVORITES = defaultdict(set)

AYAH_OF_THE_DAY = [
    ("إِنَّ مَعَ الْعُسْرِ يُسْرًا", "Indeed, with hardship comes ease.", "94:6"),
    ("فَاذْكُرُونِي أَذْكُرْكُمْ", "So remember Me; I will remember you.", "2:152"),
    ("وَمَن يَتَّقِ اللَّهَ يَجْعَل لَّهُ مَخْرَجًا", "Whoever fears Allah, He will make a way out for him.", "65:2"),
]

LANGUAGES = {
    "en": "English 🇬🇧",
    "ar": "العربية 🇸🇦",
    "am": "አማርኛ 🇪🇹",
    "so": "Soomaali 🇸🇴",
    "om": "Afaan Oromo 🇪🇹"
}

USER_LANG = defaultdict(lambda: "en")

TEXTS = {
    "welcome": {
        "en": "🌙 *Welcome to Quran Audience!*\n\nListen to the Qur’an anytime with one click.\n\nChoose from beautiful reciters and stay connected with Allah’s words.",
        "ar": "🌙 *مرحبًا بك في جمهور القرآن!*\n\nاستمع إلى القرآن في أي وقت بنقرة واحدة.\n\nاختر من القرّاء واستمتع بكلام الله.",
        "am": "🌙 *እንኳን ወደ Quran Audience በደህና መጡ!*\n\nቁርአንን በአንድ ጠቅታ ያዳምጡ።",
        "so": "🌙 *Ku soo dhawoow Quran Audience!*\n\nDhageyso Qur’aanka mar kasta hal gujin.",
        "om": "🌙 *Baga nagaan dhuftan Quran Audience!*\n\nQur’aana yeroo kamiyyuu tuqiinsa tokkoon dhaggeeffadhaa."
    },
    "menu": {
        "en": "📖 *Main Menu*",
        "ar": "📖 *القائمة الرئيسية*",
        "am": "📖 *ዋና ማውጫ*",
        "so": "📖 *Menu-ga Ugu Weyn*",
        "om": "📖 *Menu Ijoo*"
    },
    "choose_surah": {
        "en": "📖 *Choose a Surah:*",
        "ar": "📖 *اختر سورة:*",
        "am": "📖 *ሱራ ይምረጡ:*",
        "so": "📖 *Dooro Suurad:*",
        "om": "📖 *Suurata filadhaa:*"
    },
    "choose_reciter": {
        "en": "🎙️ *Choose a Reciter:*",
        "ar": "🎙️ *اختر قارئًا:*",
        "am": "🎙️ *ቃሪ ይምረጡ:*",
        "so": "🎙️ *Dooro Qari:*",
        "om": "🎙️ *Qaarii filadhaa:*"
    },
    "ayah": {
        "en": "📖 *Ayah of the Day*",
        "ar": "📖 *آية اليوم*",
        "am": "📖 *የዛሬ አያ*",
        "so": "📖 *Aayadda Maanta*",
        "om": "📖 *Aayaa Guyyaa*    "
    },
    "language": {
        "en": "🌐 *Choose your language:*",
        "ar": "🌐 *اختر لغتك:*",
        "am": "🌐 *ቋንቋዎን ይምረጡ:*",
        "so": "🌐 *Dooro luqaddaada:*",
        "om": "🌐 *Afaan kee filadhaa:*"
    },
    "help": {
        "en": (
            "🆘 *Help*\n\n"
            "/start - Start the bot\n"
            "/menu - Show main menu\n"
            "/juz - Browse by Juz\n"
            "/ayah - Ayah of the day\n"
            "/language - Change language\n"
            "/favorites - View favorites\n"
            "/admin - Admin dashboard"
        ),
        "ar": (
            "🆘 *المساعدة*\n\n"
            "/start - بدء البوت\n"
            "/menu - عرض القائمة الرئيسية\n"
            "/juz - تصفح الأجزاء\n"
            "/ayah - آية اليوم\n"
            "/language - تغيير اللغة\n"
            "/favorites - عرض المفضلة\n"
            "/admin - لوحة المشرف"
        ),
        "am": (
            "🆘 *እገዛ*\n\n"
            "/start - ቦቱን ጀምር\n"
            "/menu - ዋና ማውጫ አሳይ\n"
            "/juz - ጀዝ ተመልከት\n"
            "/ayah - የዛሬ አያህ\n"
            "/language - ቋንቋ ቀይር\n"
            "/favorites - የምወዳቸው አሳይ\n"
            "/admin - የአስተዳዳሪ ዳሽቦርድ"
        ),
        "so": (
            "🆘 *Caawimaad*\n\n"
            "/start - Bilow bot-ka\n"
            "/menu - Muuji menu-ga\n"
            "/juz - Baadh juz-yada\n"
            "/ayah - Aayadda maanta\n"
            "/language - Beddel luqadda\n"
            "/favorites - Eeg kuwa aad jeceshahay\n"
            "/admin - Gudiga maamulka"
        ),
        "om": (
            "🆘 *Gargaarsa*\n\n"
            "/start - Bot jalqabi\n"
            "/menu - Ijoo menu agarsiisi\n"
            "/juz - Juz ilaali\n"
            "/ayah - Aayaa guyyaa\n"
            "/language - Afaan jijjiiri\n"
            "/favorites - Filannoo koo\n"
            "/admin - Dashboard admin"
        )
    }
}

USERS = set()

def load_state():
    if not os.path.exists(STATE_FILE):
        return {"users": [], "favorites": {}, "languages": {}}
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception as exc:
        logger.error("Failed to load state: %s", exc)
        return {"users": [], "favorites": {}, "languages": {}}

def save_state():
    data = {
        "users": sorted(USERS),
        "favorites": {str(uid): sorted(list(favs)) for uid, favs in USER_FAVORITES.items()},
        "languages": {str(uid): lang for uid, lang in USER_LANG.items()},
    }
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=True, indent=2)
    except Exception as exc:
        logger.error("Failed to save state: %s", exc)

STATE = load_state()
USERS.update(STATE.get("users", []))
for user_id, lang in STATE.get("languages", {}).items():
    USER_LANG[int(user_id)] = lang
for user_id, favs in STATE.get("favorites", {}).items():
    USER_FAVORITES[int(user_id)] = set(favs)

SOCIALS_INFO = (
    "🌟 Follow for more Islamic reminders:\n\n"
    "Telegram: https://t.me/noorvibes_light\n"
    "May Allah reward you 🤍"
)

CONTACT_INFO = (
    "📬 *Contact Admin:*\n\n"
    "Telegram: @yourusername\n"
    "For support, feedback, or suggestions."
)

# ==================== KEYBOARDS ====================

def build_button_rows(buttons, columns):
    return [buttons[i:i+columns] for i in range(0, len(buttons), columns)]

def track_user(context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    users = context.application.bot_data.setdefault("users", set())
    users.add(chat_id)
    if chat_id not in USERS:
        USERS.add(chat_id)
        save_state()

def get_main_menu_keyboard(lang="en"):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎧 Surahs", callback_data="menu_surahs"),
            InlineKeyboardButton("🎙️ Reciters", callback_data="menu_reciters"),
        ],
        [
            InlineKeyboardButton("📚 Juz", callback_data="menu_juz"),
            InlineKeyboardButton("📖 Ayah", callback_data="menu_ayah"),
        ],
        [
            InlineKeyboardButton("⭐ Favorites", callback_data="menu_favorites"),
            InlineKeyboardButton("🌐 Language", callback_data="menu_language"),
        ],
        [
            InlineKeyboardButton("📢 Share", callback_data="menu_share"),
            InlineKeyboardButton("🆘 Help", callback_data="menu_help"),
        ],
        [
            InlineKeyboardButton("📬 Contact", callback_data="menu_contacts"),
            InlineKeyboardButton("🧹 Clear", callback_data="menu_clear"),
        ],
    ])

def get_reply_menu():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("🏠 Main Menu"), KeyboardButton("▶️ Start")],
            [KeyboardButton("❌ Clear Menu")]
        ],
        resize_keyboard=True
    )

async def send_reply_menu(update: Update):
    await update.message.reply_text("Menu ready.", reply_markup=get_reply_menu())

def get_surah_keyboard(page=0):
    per_page = SURAH_COLUMNS * 4
    start = page * per_page
    end = start + per_page
    buttons = [
        InlineKeyboardButton(f"{i+1}. {SURAH_NAMES[i]}", callback_data=f"play_{i+1}")
        for i in range(start, min(end, len(SURAH_NAMES)))
    ]
    rows = build_button_rows(buttons, SURAH_COLUMNS)
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"page_{page-1}"))
    if end < len(SURAH_NAMES):
        nav.append(InlineKeyboardButton("Next ➡️", callback_data=f"page_{page+1}"))
    if nav:
        rows.append(nav)
    rows.append([InlineKeyboardButton("⬅️ Back", callback_data="menu_main")])
    return InlineKeyboardMarkup(rows)

def get_juz_keyboard():
    buttons = [InlineKeyboardButton(f"Juz {i+1}", callback_data=f"juz_{i+1}") for i in range(30)]
    rows = build_button_rows(buttons, 3)
    rows.append([InlineKeyboardButton("⬅️ Back", callback_data="menu_main")])
    return InlineKeyboardMarkup(rows)

def get_language_keyboard():
    buttons = [
        InlineKeyboardButton(name, callback_data=f"lang_{code}")
        for code, name in LANGUAGES.items()
    ]
    rows = build_button_rows(buttons, 2)
    rows.append([InlineKeyboardButton("⬅️ Back", callback_data="menu_main")])
    return InlineKeyboardMarkup(rows)

# ==================== COMMANDS ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    track_user(context, update.effective_chat.id)
    lang = USER_LANG[user_id]
    text = TEXTS["welcome"][lang]
    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard(lang)
    )
    await send_reply_menu(update)

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    track_user(context, update.effective_chat.id)
    lang = USER_LANG[user_id]
    await update.message.reply_text(
        TEXTS["menu"][lang],
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard(lang)
    )
    await send_reply_menu(update)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(context, update.effective_chat.id)
    lang = USER_LANG[update.effective_user.id]
    await update.message.reply_text(
        TEXTS["help"][lang],
        parse_mode="Markdown"
    )

async def health_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(context, update.effective_chat.id)
    await update.message.reply_text("✅ Bot is alive.")

async def ayah_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(context, update.effective_chat.id)
    ayah_ar, ayah_en, ref = random.choice(AYAH_OF_THE_DAY)
    text = f"📖 *Ayah of the Day*\n\n{ayah_ar}\n\n“{ayah_en}”\n\n— Qur’an {ref}"
    await update.message.reply_text(text, parse_mode="Markdown")

async def juz_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(context, update.effective_chat.id)
    await update.message.reply_text(
        "📚 *Choose a Juz:*",
        parse_mode="Markdown",
        reply_markup=get_juz_keyboard()
    )

async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    track_user(context, update.effective_chat.id)
    lang = USER_LANG[user_id]
    await update.message.reply_text(
        TEXTS["language"][lang],
        parse_mode="Markdown",
        reply_markup=get_language_keyboard()
    )

async def favorites_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    track_user(context, update.effective_chat.id)
    favs = USER_FAVORITES[user_id]
    if not favs:
        await update.message.reply_text("⭐ You have no favorites yet.")
        return
    buttons = [
        InlineKeyboardButton(f"{s}. {SURAH_NAMES[s-1]}", callback_data=f"play_{s}")
        for s in sorted(favs)
    ]
    rows = build_button_rows(buttons, SURAH_COLUMNS)
    rows.append([InlineKeyboardButton("⬅️ Back", callback_data="menu_main")])
    await update.message.reply_text(
        "⭐ *Your Favorites:*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(rows)
    )

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    track_user(context, update.effective_chat.id)
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ You are not authorized to use admin commands.")
        return
    await update.message.reply_text(
        "🛠️ *Admin Dashboard*\n\n"
        "/broadcast <message> — Send message to all users\n"
        "/stats — View bot stats\n"
        "/export — Download bot data\n",
        parse_mode="Markdown"
    )

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    track_user(context, update.effective_chat.id)
    if user_id not in ADMIN_IDS:
        return
    if not context.args:
        await update.message.reply_text("Usage: /broadcast <message>")
        return
    message = " ".join(context.args)
    count = 0
    for chat_id in USERS:
        try:
            await context.bot.send_message(chat_id, message)
            count += 1
        except:
            pass
    await update.message.reply_text(f"✅ Broadcast sent to {count} users.")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    track_user(context, update.effective_chat.id)
    if user_id not in ADMIN_IDS:
        return
    total_users = len(USERS)
    top_reciters = sorted(RECITER_PLAYS.items(), key=lambda x: x[1], reverse=True)[:5]
    text = f"📊 *Bot Stats*\n\n👥 Users: {total_users}\n\n🎙️ Top Reciters:\n"
    for rid, plays in top_reciters:
        text += f"- {RECITERS_DATA[rid]['name']}: {plays} plays\n"
    await update.message.reply_text(text, parse_mode="Markdown")

async def export_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    track_user(context, update.effective_chat.id)
    if user_id not in ADMIN_IDS:
        return
    data = {
        "total_users": len(USERS),
        "users": sorted(list(USERS)),
        "favorites": {str(uid): sorted(list(favs)) for uid, favs in USER_FAVORITES.items()},
        "languages": {str(uid): lang for uid, lang in USER_LANG.items()},
        "reciter_plays": dict(RECITER_PLAYS),
    }
    payload = json.dumps(data, ensure_ascii=True, indent=2).encode("utf-8")
    buffer = io.BytesIO(payload)
    buffer.name = "bot_export.json"
    await update.message.reply_document(document=buffer, filename="bot_export.json")

# ==================== DAILY REMINDER ====================

async def send_daily_reminder(context: ContextTypes.DEFAULT_TYPE):
    ayah_ar, ayah_en, ref = random.choice(AYAH_OF_THE_DAY)
    text = (
        "🌙 *Daily Qur’an Reminder*\n\n"
        f"{ayah_ar}\n\n“{ayah_en}”\n\n— Qur’an {ref}\n\n"
        "Take a moment today to listen to the Qur’an 🤍"
    )
    for chat_id in USERS:
        try:
            await context.bot.send_message(chat_id, text, parse_mode="Markdown")
        except:
            pass

# ==================== CALLBACK HANDLER ====================

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id
    lang = USER_LANG[user_id]
    if query.message:
        track_user(context, query.message.chat_id)

    if data == "menu_main":
        await query.edit_message_text(
            TEXTS["menu"][lang],
            parse_mode="Markdown",
            reply_markup=get_main_menu_keyboard(lang)
        )

    elif data == "menu_surahs":
        await query.edit_message_text(
            TEXTS["choose_surah"][lang],
            parse_mode="Markdown",
            reply_markup=get_surah_keyboard(0)
        )

    elif data == "menu_reciters":
        buttons = [
            InlineKeyboardButton(info["name"], callback_data=f"reciter_{rid}")
            for rid, info in RECITERS_DATA.items()
        ]
        rows = build_button_rows(buttons, QARI_COLUMNS)
        rows.append([InlineKeyboardButton("⬅️ Back", callback_data="menu_main")])
        await query.edit_message_text(
            TEXTS["choose_reciter"][lang],
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(rows)
        )

    elif data.startswith("reciter_"):
        reciter_id = data.replace("reciter_", "")
        context.user_data["selected_reciter"] = reciter_id
        await query.edit_message_text(
            f"🎧 *Reciter Selected:*\n{RECITERS_DATA[reciter_id]['name']}\n\n{TEXTS['choose_surah'][lang]}",
            parse_mode="Markdown",
            reply_markup=get_surah_keyboard(0)
        )

    elif data.startswith("page_"):
        page = int(data.replace("page_", ""))
        await query.edit_message_text(
            TEXTS["choose_surah"][lang],
            parse_mode="Markdown",
            reply_markup=get_surah_keyboard(page)
        )

    elif data == "menu_juz":
        context.user_data["selected_reciter"] = context.user_data.get("selected_reciter", "r01")
        await query.edit_message_text(
            "📚 *Choose a Juz:*",
            parse_mode="Markdown",
            reply_markup=get_juz_keyboard()
        )

    elif data.startswith("juz_"):
        juz_num = int(data.replace("juz_", ""))
        start_surah = JUZ_START_SURAH[juz_num-1]
        end_surah = JUZ_START_SURAH[juz_num] - 1 if juz_num < 30 else 114
        buttons = [
            InlineKeyboardButton(f"{i}. {SURAH_NAMES[i-1]}", callback_data=f"play_{i}")
            for i in range(start_surah, end_surah + 1)
        ]
        rows = build_button_rows(buttons, SURAH_COLUMNS)
        rows.append([InlineKeyboardButton("🔄 Change Reciter", callback_data="menu_reciters")])
        rows.append([InlineKeyboardButton("⬅️ Back", callback_data="menu_main")])
        await query.edit_message_text(
            f"📚 *Juz {juz_num} — Select a Surah:*",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(rows)
        )

    elif data.startswith("play_"):
        surah_num = int(data.replace("play_", ""))
        rec_id = context.user_data.get("selected_reciter", "r01")
        reciter = RECITERS_DATA[rec_id]
        target_id = reciter["start_msg_id"] + (surah_num - 1)

        chat_id = query.message.chat_id
        try:
            await context.bot.copy_message(
                chat_id=chat_id,
                from_chat_id=PRIVATE_CHANNEL_ID,
                message_id=target_id
            )
            await context.bot.send_message(
                chat_id=chat_id,
                text=(
                    f"🎧 *Now Playing:*\n"
                    f"{SURAH_NAMES[surah_num-1]}\n\n"
                    f"Reciter: {reciter['name']}"
                ),
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("⭐ Favorite", callback_data=f"fav_{surah_num}"),
                        InlineKeyboardButton("⬇️ Download", callback_data=f"download_{surah_num}")
                    ],
                    [
                        InlineKeyboardButton("🎙️ Change Reciter", callback_data="menu_reciters"),
                        InlineKeyboardButton("🏠 Main Menu", callback_data="menu_main")
                    ]
                ])
            )
            RECITER_PLAYS[rec_id] += 1
        except Exception as exc:
            logger.error("Audio send failed: %s", exc)
            await context.bot.send_message(chat_id=chat_id, text="❌ Audio not found. Please try again later.")

    elif data.startswith("download_"):
        surah_num = int(data.replace("download_", ""))
        rec_id = context.user_data.get("selected_reciter", "r01")
        reciter = RECITERS_DATA[rec_id]
        target_id = reciter["start_msg_id"] + (surah_num - 1)
        chat_id = query.message.chat_id
        try:
            await context.bot.copy_message(
                chat_id=chat_id,
                from_chat_id=PRIVATE_CHANNEL_ID,
                message_id=target_id
            )
            logger.info(
                "downloaded_surah user_id=%s reciter_id=%s surah=%s",
                user_id,
                rec_id,
                surah_num
            )
        except Exception as exc:
            logger.error("Download failed: %s", exc)
            await context.bot.send_message(chat_id=chat_id, text="❌ Download failed.")

    elif data.startswith("fav_"):
        surah_num = int(data.replace("fav_", ""))
        USER_FAVORITES[user_id].add(surah_num)
        save_state()
        logger.info("favorite_added user_id=%s surah=%s", user_id, surah_num)
        await query.answer("⭐ Added to favorites!")

    elif data == "menu_favorites":
        favs = USER_FAVORITES[user_id]
        if not favs:
            await query.edit_message_text(
                "⭐ You have no favorites yet.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="menu_main")]])
            )
            return
        buttons = [
            InlineKeyboardButton(f"{s}. {SURAH_NAMES[s-1]}", callback_data=f"play_{s}")
            for s in sorted(favs)
        ]
        rows = build_button_rows(buttons, SURAH_COLUMNS)
        rows.append([InlineKeyboardButton("⬅️ Back", callback_data="menu_main")])
        await query.edit_message_text(
            "⭐ *Your Favorites:*",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(rows)
        )

    elif data == "menu_ayah":
        ayah_ar, ayah_en, ref = random.choice(AYAH_OF_THE_DAY)
        text = f"{TEXTS['ayah'][lang]}\n\n{ayah_ar}\n\n“{ayah_en}”\n\n— Qur’an {ref}"
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="menu_main")]])
        )

    elif data == "menu_language":
        await query.edit_message_text(
            TEXTS["language"][lang],
            parse_mode="Markdown",
            reply_markup=get_language_keyboard()
        )

    elif data.startswith("lang_"):
        new_lang = data.replace("lang_", "")
        USER_LANG[user_id] = new_lang
        save_state()
        logger.info("language_changed user_id=%s lang=%s", user_id, new_lang)
        await query.edit_message_text(
            f"✅ Language set to {LANGUAGES[new_lang]}",
            reply_markup=get_main_menu_keyboard(new_lang)
        )

    elif data == "menu_share":
        bot_username = context.bot.username
        if bot_username:
            share_url = f"https://t.me/share/url?url=https://t.me/{bot_username}"
            share_text = f"🔗 *Share this bot:*\n{share_url}"
        else:
            share_text = "🔗 Share this bot by sending its username to your friends."
        await query.edit_message_text(
            share_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="menu_main")]])
        )

    elif data == "menu_help":
        help_text = TEXTS["help"][lang]
        await query.edit_message_text(
            help_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="menu_main")]])
        )

    elif data == "menu_contacts":
        await query.edit_message_text(
            CONTACT_INFO,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="menu_main")]])
        )

    elif data == "menu_clear":
        if query.message:
            await query.message.delete()

# ==================== TEXT HANDLER ====================

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(context, update.effective_chat.id)
    text = update.message.text.lower()
    if text in {"main menu", "menu", "🏠 main menu"}:
        await menu(update, context)
        return
    if text in {"start", "▶️ start"}:
        await start(update, context)
        return
    if text in {"clear menu", "❌ clear menu"}:
        await update.message.reply_text("✅ Menu cleared.", reply_markup=ReplyKeyboardRemove())
        return
    if "surah" in text or "quran" in text:
        await menu(update, context)
    else:
        await update.message.reply_text(
            "🤍 Please use /menu to navigate the bot."
        )

# ==================== ERROR HANDLER ====================

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.exception("Unhandled error: %s", context.error)

# ==================== MAIN (WEBHOOK) ====================

def main():
    if not BOT_TOKEN or not BOT_TOKEN.strip():
        logger.error("BOT_TOKEN is missing. Set it in the environment variables.")
        raise SystemExit(1)

    if not RENDER_EXTERNAL_URL:
        logger.error("RENDER_EXTERNAL_URL is missing. Add it in Render environment variables.")
        raise SystemExit(1)

    application = Application.builder().token(BOT_TOKEN).build()

    # Commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("health", health_command))
    application.add_handler(CommandHandler("ping", health_command))
    application.add_handler(CommandHandler("ayah", ayah_command))
    application.add_handler(CommandHandler("juz", juz_command))
    application.add_handler(CommandHandler("language", language_command))
    application.add_handler(CommandHandler("favorites", favorites_command))
    application.add_handler(CommandHandler("admin", admin_command))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("export", export_command))

    # Callback handler
    application.add_handler(CallbackQueryHandler(handle_callback))

    # Text fallback
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    # Global error handler
    application.add_error_handler(error_handler)

    # Job Queue (Daily Reminder at 7 AM)
    if application.job_queue:
        application.job_queue.run_daily(send_daily_reminder, time(hour=7, minute=0))
    else:
        logger.warning("⚠️ JobQueue not available — daily reminders disabled.")

    print("🚀 Quran Audience Bot is running via webhook...")

    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=f"{RENDER_EXTERNAL_URL}/{BOT_TOKEN}"
    )

if __name__ == "__main__":
    main()

