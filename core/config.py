import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")
PORT = int(os.getenv("PORT", 10000))

# Global reminder time in HH:MM for all users.
REMINDER_GLOBAL_TIME = os.getenv("REMINDER_GLOBAL_TIME", "10:00")

# Approximate timezone offsets (minutes) by language.
REMINDER_TZ_BY_LANG = {
    "en": 0,
    "ar": 180,
    "am": 180,
    "so": 180,
    "om": 180,
    "tr": 180
}

PRIVATE_CHANNEL_ID = -1003806159829
ADMIN_IDS = {5726141414}

DATA_DIR = "data"
STATE_FILE = os.path.join(DATA_DIR, "bot_state.json")
DB_FILE = os.path.join(DATA_DIR, "bot_state.db")
AUDIO_CACHE_DIR = "audio_cache"

SURAH_COLUMNS = 6
QARI_COLUMNS = 2

os.makedirs(DATA_DIR, exist_ok=True)

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
    "r01": {"name": "Abdulllah Ali Jaber", "start_msg_id": 2879},
    "r02": {"name": "Abdul Basit Abdul Samad", "start_msg_id": 234},
    "r03": {"name": "Abdul Muhsin Al Qasim", "start_msg_id": 1844},
    "r04": {"name": "Abdul Rahman Al Ossi", "start_msg_id": 1614},
    "r05": {"name": "Abdul Rahman Al-Sudais", "start_msg_id": 349},
    "r06": {"name": "Abdullah Awad Al-Johany", "start_msg_id": 1153},
    "r07": {"name": "Abdullah ibn Ali Basfar", "start_msg_id": 1384},
    "r08": {"name": "Abu Bakr Al-Shatri", "start_msg_id": 119},
    "r09": {"name": "Mahmoud Khalil Al-Hussary", "start_msg_id": 1038},
    "r10": {"name": "Mishary Rashid Alafasy", "start_msg_id": 3},
    "r11": {"name": "Mohammed Al-Luhaidan", "start_msg_id": 464},
    "r12": {"name": "Mohammad Saleh Alim Shah", "start_msg_id": 1729},
    "r13": {"name": "Sheikh Salah Al-Budair", "start_msg_id": 3225},
    "r14": {"name": "Sheikh Maher Al-Muaiqly", "start_msg_id": 579},
    "r15": {"name": "Sheikh Mohammed Ayyub", "start_msg_id": 923},
    "r16": {"name": "Sheikh Abdul Wadood Haneef", "start_msg_id": 1959},
    "r17": {"name": "Sheikh Adel Rayan", "start_msg_id": 1499},
    "r18": {"name": "Sheikh Idris Abkar", "start_msg_id": 2649},
    "r19": {"name": "Sheikh Muhammad Jibril", "start_msg_id": 2189},
    "r20": {"name": "Sheikh Saud Al-Shuraim", "start_msg_id": 693},
    "r21": {"name": "Sheikh Yasser Al-Dosari", "start_msg_id": 2074},
    "r22": {"name": "Waleed Al Naehi", "start_msg_id": 3326},
    "r23": {"name": "Yasser Al-Qureshi", "start_msg_id": 808},
    "r24": {"name": "Yahya Hawwa ", "start_msg_id": 2995},
    "r25": {"name": "Yassen Al-Jazir", "start_msg_id": 3110},
}


AYAH_OF_THE_DAY = [
    ("إِنَّ مَعَ الْعُسْرِ يُسْرًا", "Indeed, with hardship comes ease.", "94:6"),
    ("فَاذْكُرُونِي أَذْكُرْكُمْ", "So remember Me; I will remember you.", "2:152"),
    ("وَمَن يَتَّقِ اللَّهَ يَجْعَل لَّهُ مَخْرَجًا", "Whoever fears Allah, He will make a way out for him.", "65:2"),
    ("اللَّهُ نُورُ السَّمَاوَاتِ وَالْأَرْضِ", "Allah is the Light of the heavens and the earth.", "24:35"),
    ("وَقُل رَّبِّ زِدْنِي عِلْمًا", "And say: My Lord, increase me in knowledge.", "20:114"),
    ("إِنَّ اللَّهَ مَعَ الصَّابِرِينَ", "Indeed, Allah is with the patient.", "2:153"),
    ("وَهُوَ عَلَىٰ كُلِّ شَيْءٍ قَدِيرٌ", "And He is over all things competent.", "57:2"),
    ("رَّبِّ اشْرَحْ لِي صَدْرِي", "My Lord, expand for me my chest.", "20:25"),
    ("وَتَوَكَّلْ عَلَى اللَّهِ", "And rely upon Allah.", "33:3"),
    ("إِنَّ اللَّهَ غَفُورٌ رَّحِيمٌ", "Indeed, Allah is Forgiving and Merciful.", "2:173"),
    ("وَاللَّهُ خَيْرُ الرَّازِقِينَ", "And Allah is the best of providers.", "62:11"),
    ("إِنَّ اللَّهَ يُحِبُّ الْمُحْسِنِينَ", "Indeed, Allah loves those who do good.", "2:195"),
    ("وَاللَّهُ سَمِيعٌ عَلِيمٌ", "And Allah is Hearing and Knowing.", "2:137"),
    ("رَّبَّنَا لَا تُزِغْ قُلُوبَنَا", "Our Lord, let not our hearts deviate.", "3:8"),
    ("إِنَّ رَبِّي قَرِيبٌ مُّجِيبٌ", "Indeed, my Lord is Near and Responsive.", "11:61"),
    ("وَاصْبِرْ وَمَا صَبْرُكَ إِلَّا بِاللَّهِ", "And be patient, and your patience is only through Allah.", "16:127"),
    ("إِنَّ اللَّهَ يُحِبُّ التَّوَّابِينَ", "Indeed, Allah loves those who repent.", "2:222"),
    ("وَاللَّهُ وَلِيُّ الْمُؤْمِنِينَ", "And Allah is the ally of the believers.", "3:68"),
    ("إِنَّ رَحْمَتَ اللَّهِ قَرِيبٌ مِّنَ الْمُحْسِنِينَ", "Indeed, the mercy of Allah is near to the doers of good.", "7:56"),
    ("وَاللَّهُ خَيْرُ الْحَافِظِينَ", "And Allah is the best of protectors.", "12:64"),
    ("إِنَّ اللَّهَ لَا يُضِيعُ أَجْرَ الْمُحْسِنِينَ", "Indeed, Allah does not allow the reward of the good to be lost.", "9:120"),
    ("وَهُوَ مَعَكُمْ أَيْنَ مَا كُنتُمْ", "And He is with you wherever you are.", "57:4"),
    ("فَإِنَّ مَعَ الْعُسْرِ يُسْرًا", "For indeed, with hardship comes ease.", "94:5"),
    ("وَاللَّهُ يُحِبُّ الصَّابِرِينَ", "And Allah loves the patient.", "3:146"),
    ("رَّبِّ اغْفِرْ لِي وَلِوَالِدَيَّ", "My Lord, forgive me and my parents.", "14:41"),
    ("إِنَّ اللَّهَ بِالنَّاسِ لَرَءُوفٌ رَّحِيمٌ", "Indeed, Allah is Kind and Merciful to people.", "2:143"),
    ("وَمَا تَوْفِيقِي إِلَّا بِاللَّهِ", "And my success is only through Allah.", "11:88"),
    ("إِنَّ اللَّهَ مَعَنَا", "Indeed, Allah is with us.", "9:40"),
    ("رَبَّنَا تَقَبَّلْ مِنَّا", "Our Lord, accept from us.", "2:127"),
    ("وَاللَّهُ عَلِيمٌ حَكِيمٌ", "And Allah is Knowing and Wise.", "4:26"),
    ("إِنَّ اللَّهَ لَطِيفٌ خَبِيرٌ", "Indeed, Allah is Subtle and Aware.", "31:16"),
    ("وَاللَّهُ غَالِبٌ عَلَىٰ أَمْرِهِ", "And Allah is predominant over His affair.", "12:21"),
    ("إِنَّ اللَّهَ يُحِبُّ الْمُتَوَكِّلِينَ", "Indeed, Allah loves those who rely upon Him.", "3:159"),
    ("رَّبِّ يَسِّرْ وَلَا تُعَسِّرْ", "My Lord, make it easy and do not make it difficult.", "Adapted supplication"),
    ("وَإِلَى اللَّهِ تُرْجَعُ الْأُمُورُ", "And to Allah all matters are returned.", "2:210"),
    ("إِنَّ اللَّهَ عَلَىٰ كُلِّ شَيْءٍ قَدِيرٌ", "Indeed, Allah is over all things competent.", "2:20"),
    ("رَّبِّ زِدْنِي عِلْمًا", "My Lord, increase me in knowledge.", "20:114"),
    ("وَاللَّهُ يُحِبُّ الْمُقْسِطِينَ", "And Allah loves those who act justly.", "5:42"),
    ("إِنَّ رَبِّي لَسَمِيعُ الدُّعَاءِ", "Indeed, my Lord is the Hearer of supplication.", "14:39"),
    ("وَهُوَ خَيْرُ الْحَاكِمِينَ", "And He is the best of judges.", "7:87"),
    ("إِنَّ اللَّهَ سَرِيعُ الْحِسَابِ", "Indeed, Allah is swift in account.", "3:199"),
    ("رَّبَّنَا أَفْرِغْ عَلَيْنَا صَبْرًا", "Our Lord, pour upon us patience.", "2:250"),
    ("وَاللَّهُ يَعْلَمُ وَأَنتُمْ لَا تَعْلَمُونَ", "And Allah knows, while you do not know.", "2:216"),
    ("إِنَّ اللَّهَ هُوَ الرَّزَّاقُ", "Indeed, Allah is the Provider.", "51:58"),
    ("فَاصْبِرْ إِنَّ وَعْدَ اللَّهِ حَقٌّ", "So be patient; indeed, the promise of Allah is truth.", "30:60"),
    ("وَاللَّهُ خَيْرُ الْمَاكِرِينَ", "And Allah is the best of planners.", "3:54"),
    ("رَبَّنَا عَلَيْكَ تَوَكَّلْنَا", "Our Lord, upon You we rely.", "60:4"),
    ("إِنَّ اللَّهَ عَزِيزٌ حَكِيمٌ", "Indeed, Allah is Exalted in Might and Wise.", "48:7"),
    ("وَاصْفَحِ الصَّفْحَ الْجَمِيلَ", "And overlook with gracious forgiveness.", "15:85"),
    ("إِنَّ اللَّهَ يُحِبُّ الْمُتَّقِينَ", "Indeed, Allah loves the righteous.", "3:76"),
    ("وَهُوَ أَرْحَمُ الرَّاحِمِينَ", "And He is the Most Merciful of the merciful.", "12:64"),
    ("رَّبَّنَا لَا تُحَمِّلْنَا مَا لَا طَاقَةَ لَنَا بِهِ", "Our Lord, do not burden us with what we cannot bear.", "2:286"),
    ("إِنَّ مَعَ الْعُسْرِ يُسْرًا", "Indeed, with hardship comes ease.", "94:6"),
    ("وَاذْكُر رَّبَّكَ إِذَا نَسِيتَ", "And remember your Lord when you forget.", "18:24"),
    ("وَاللَّهُ رَءُوفٌ بِالْعِبَادِ", "And Allah is Kind to His servants.", "3:30"),
    ("إِنَّ اللَّهَ لَا يُخْلِفُ الْمِيعَادَ", "Indeed, Allah does not break His promise.", "3:9"),
]

LANGUAGES = {
    "en": "English 🇬🇧",
    "ar": "العربية 🇸🇦",
    "am": "አማርኛ 🇪🇹",
    "so": "Soomaali 🇸🇴",
    "om": "Afaan Oromo 🇪🇹",
    "tr": "Turkce 🇹🇷"
}

SHARE_MESSAGE = (
    "🌙 Quran Audience Bot\n\n"
    "Listen to the Holy Qur’an anytime with one click 🤍\n\n"
    "🎧 20+ beautiful reciters\n"
    "📖 Browse by Surah or Juz\n"
    "⭐ Save your favorite Surahs\n"
    "🌍 Multi-language support\n"
    "📖 Daily Ayah reminders\n\n"
    "Stay connected with the words of Allah wherever you are.\n\n"
    "🔗 Start listening now https://t.me/QuranQari2026_bot"
)

TEXTS = {
    "welcome": {
        "en": "🌙 *Welcome to Quran Audience!*\n\nListen to the Qur’an anytime with one click.\n\nChoose from beautiful reciters and stay connected with Allah’s words.",
        "ar": "🌙 *مرحبًا بك في جمهور القرآن!*\n\nاستمع إلى القرآن في أي وقت بنقرة واحدة.\n\nاختر من القرّاء واستمتع بكلام الله.",
        "am": "🌙 *እንኳን ወደ Quran Audience በደህና መጡ!*\n\nቁርአንን በአንድ ጠቅታ ያዳምጡ።",
        "so": "🌙 *Ku soo dhawoow Quran Audience!*\n\nDhageyso Qur’aanka mar kasta hal gujin.",
        "om": "🌙 *Baga nagaan dhuftan Quran Audience!*\n\nQur’aana yeroo kamiyyuu tuqiinsa tokkoon dhaggeeffadhaa.",
        "tr": "🌙 *Quran Audience'e hos geldiniz!*\n\nKur'an'i tek bir tikla istediginiz zaman dinleyin.\n\nGuzel kurralardan secin ve Allah'in kelamiyle bagli kalin."
    },
    "menu": {
        "en": "📖 *Main Menu*",
        "ar": "📖 *القائمة الرئيسية*",
        "am": "📖 *ዋና ማውጫ*",
        "so": "📖 *Menu-ga Ugu Weyn*",
        "om": "📖 *Menu Ijoo*",
        "tr": "📖 *Ana Menu*"
    },
    "choose_surah": {
        "en": "📖 *Choose a Surah:*",
        "ar": "📖 *اختر سورة:*",
        "am": "📖 *ሱራ ይምረጡ:*",
        "so": "📖 *Dooro Suurad:*",
        "om": "📖 *Suurata filadhaa:*",
        "tr": "📖 *Bir Sure secin:*"
    },
    "choose_reciter": {
        "en": "🎙️ *Choose a Reciter:*",
        "ar": "🎙️ *اختر قارئًا:*",
        "am": "🎙️ *ቃሪ ይምረጡ:*",
        "so": "🎙️ *Dooro Qari:*",
        "om": "🎙️ *Qaarii filadhaa:*",
        "tr": "🎙️ *Bir kari secin:*"
    },
    "ayah": {
        "en": "📖 *Ayah of the Day*",
        "ar": "📖 *آية اليوم*",
        "am": "📖 *የዛሬ አያ*",
        "so": "📖 *Aayadda Maanta*",
        "om": "📖 *Aayaa Guyyaa*",
        "tr": "📖 *Gunun Ayeti*"
    },
    "language": {
        "en": "🌐 *Choose your language:*",
        "ar": "🌐 *اختر لغتك:*",
        "am": "🌐 *ቋንቋዎን ይምረጡ:*",
        "so": "🌐 *Dooro luqaddaada:*",
        "om": "🌐 *Afaan kee filadhaa:*",
        "tr": "🌐 *Dilinizi secin:*"
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
            "/search - Search surahs\n"
            "/mystats - Your stats\n"
            "/settings - Preferences\n"
            "/feedback - Send feedback\n"
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
            "/search - البحث عن السور\n"
            "/mystats - إحصائياتك\n"
            "/settings - التفضيلات\n"
            "/feedback - إرسال ملاحظات\n"
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
            "/search - ሱራ ፈልግ\n"
            "/mystats - የእርስዎ ስታት\n"
            "/settings - ምርጫዎች\n"
            "/feedback - ግብረመልስ ላክ\n"
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
            "/search - Raadi suurado\n"
            "/mystats - Tirakoobkaaga\n"
            "/settings - Doorbid\n"
            "/feedback - Jawaab celin dir\n"
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
            "/search - Suuraalee barbaadi\n"
            "/mystats - Istaatistika kee\n"
            "/settings - Filannoo\n"
            "/feedback - Yaada ergi\n"
            "/admin - Dashboard admin"
        ),
        "tr": (
            "🆘 *Yardim*\n\n"
            "/start - Botu baslat\n"
            "/menu - Ana menuyu goster\n"
            "/juz - Cuzlere goz at\n"
            "/ayah - Gunun ayeti\n"
            "/language - Dil degistir\n"
            "/favorites - Favorileri gor\n"
            "/search - Sure ara\n"
            "/mystats - Istatistiklerim\n"
            "/settings - Tercihler\n"
            "/feedback - Geri bildirim gonder\n"
            "/admin - Admin paneli"
        )
    },
    "menu_ready": {
        "en": "What would you like to choose?",
        "ar": "ماذا تود أن تختار؟",
        "am": "ምን መምረጥ ትፈልጋለህ?",
        "so": "Maxaad rabtaa inaad doorato?",
        "om": "Maal filachuu barbaadda?",
        "tr": "Ne secmek istersin?"
    },
    "bot_alive": {
        "en": "✅ Bot is alive.",
        "ar": "✅ البوت يعمل.",
        "am": "✅ ቦቱ እየሰራ ነው።",
        "so": "✅ Bot-ku wuu shaqaynayaa.",
        "om": "✅ Bot-ni ni hojjechaa jira.",
        "tr": "✅ Bot aktif."
    },
    "choose_juz": {
        "en": "📚 *Choose a Juz:*",
        "ar": "📚 *اختر جزءًا:*",
        "am": "📚 *ጀዝ ይምረጡ:*",
        "so": "📚 *Dooro Juz:*",
        "om": "📚 *Juz filadhaa:*",
        "tr": "📚 *Bir Cuz secin:*"
    },
    "no_favorites": {
        "en": "⭐ You have no favorites yet.",
        "ar": "⭐ ليس لديك مفضلات بعد.",
        "am": "⭐ እስካሁን ምወዳቸው የለዎትም።",
        "so": "⭐ Wali kuma lihid favorites.",
        "om": "⭐ Hanga amma filannoo hin qabdu.",
        "tr": "⭐ Henuz favoriniz yok."
    },
    "favorites_title": {
        "en": "⭐ *Your Favorites:*",
        "ar": "⭐ *مفضلتك:*",
        "am": "⭐ *የምወዳቸው:*",
        "so": "⭐ *Kuwo aad jeceshahay:*",
        "om": "⭐ *Filannoo kee:*",
        "tr": "⭐ *Favorileriniz:*"
    },
    "admin_unauthorized": {
        "en": "❌ You are not authorized to use admin commands.",
        "ar": "❌ لست مخولاً لاستخدام أوامر المشرف.",
        "am": "❌ የአስተዳዳሪ ትዕዛዞችን ለመጠቀም ፈቃድ የለዎትም።",
        "so": "❌ Looma oggola inaad isticmaasho amarrada admin.",
        "om": "❌ Ajaja admin fayyadamuuf hayyama hin qabdu.",
        "tr": "❌ Admin komutlarini kullanma yetkiniz yok."
    },
    "admin_dashboard": {
        "en": "🛠️ *Admin Dashboard*",
        "ar": "🛠️ *لوحة المشرف*",
        "am": "🛠️ *የአስተዳዳሪ ዳሽቦርድ*",
        "so": "🛠️ *Gudiga Admin*",
        "om": "🛠️ *Dashboard Admin*",
        "tr": "🛠️ *Admin Paneli*"
    },
    "peace_response": {
        "en": "وَعَلَيْكُمُ السَّلَامُ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ\nPeace and Allah's mercy and blessings be upon you.",
        "ar": "وَعَلَيْكُمُ السَّلَامُ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ\nوعليكم السلام ورحمة الله وبركاته.",
        "am": "وَعَلَيْكُمُ السَّلَامُ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ\nሰላም እና የአላህ ምሕረትና በረከት በእናንተ ላይ ይሁን።",
        "so": "وَعَلَيْكُمُ السَّلَامُ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ\nNabad, naxariis iyo barako Eebe ha idinku sugnaato.",
        "om": "وَعَلَيْكُمُ السَّلَامُ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ\nNagaa fi rahmata Rabbii akkasumas barakaan Isaatiin isinii haa ta'u.",
        "tr": "وَعَلَيْكُمُ السَّلَامُ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ\nAllah'in rahmeti ve bereketi uzerinize olsun."
    },
    "broadcast_usage": {
        "en": "Usage: /broadcast <message> or /broadcast then type your message",
        "ar": "الاستخدام: /broadcast <message> أو /broadcast ثم اكتب رسالتك",
        "am": "አጠቃቀም: /broadcast <message> ወይም /broadcast ከዚያ መልእክትዎን ይጻፉ",
        "so": "Isticmaal: /broadcast <message> ama /broadcast ka dib qor fariinta",
        "om": "Fayyadami: /broadcast <message> ykn /broadcast booda ergaa barreessi",
        "tr": "Kullanim: /broadcast <message> veya /broadcast yazip mesaj gonder"
    },
    "broadcast_prompt": {
        "en": "Type the message to broadcast.",
        "ar": "اكتب الرسالة للبث.",
        "am": "ለማስተላለፍ የሚፈልጉትን መልእክት ይጻፉ።",
        "so": "Qor fariinta la baahinayo.",
        "om": "Ergaa dabarfamu barreessi.",
        "tr": "Duyuru mesajini yazin."
    },
    "broadcast_sent": {
        "en": "✅ Broadcast sent to {count} users.",
        "ar": "✅ تم إرسال البث إلى {count} مستخدم.",
        "am": "✅ መልእክቱ ለ{count} ተጠቃሚዎች ተልኳል።",
        "so": "✅ Broadcast-ka waxaa loo diray {count} isticmaale.",
        "om": "✅ Ergaan dabarfame {count} fayyadamtootaaf ergame.",
        "tr": "✅ Duyuru {count} kullaniciya gonderildi."
    },
    "stats_header": {
        "en": "📊 *Bot Stats*\n\n👥 Users: {total}\n\n🎙️ Top Reciters:\n",
        "ar": "📊 *إحصائيات البوت*\n\n👥 المستخدمون: {total}\n\n🎙️ أفضل القرّاء:\n",
        "am": "📊 *የቦት ስታት*\n\n👥 ተጠቃሚዎች: {total}\n\n🎙️ ከፍተኛ ቃሪዎች:\n",
        "so": "📊 *Tirakoobka Bot-ka*\n\n👥 Isticmaalayaal: {total}\n\n🎙️ Qurriyada ugu sarreeya:\n",
        "om": "📊 *Istaatistika Bot*\n\n👥 Fayyadamtoota: {total}\n\n🎙️ Qaariyoota keessaa kanneen ol aanaa:\n",
        "tr": "📊 *Bot Istatistikleri*\n\n👥 Kullanicilar: {total}\n\n🎙️ En iyi kurralar:\n"
    },
    "plays_label": {
        "en": "plays",
        "ar": "تشغيل",
        "am": "ጫወቶች",
        "so": "ciyaarid",
        "om": "taphannaa",
        "tr": "oynatma"
    },
    "stats_dau": {
        "en": "📆 Daily active users: {count}\n",
        "ar": "📆 المستخدمون النشطون اليوم: {count}\n",
        "am": "📆 የዛሬ ንቁ ተጠቃሚዎች: {count}\n",
        "so": "📆 Isticmaalayaasha maanta firfircoon: {count}\n",
        "om": "📆 Fayyadamtoota guyyaa kanaa: {count}\n",
        "tr": "📆 Gunluk aktif kullanici: {count}\n"
    },
    "stats_retention": {
        "en": "📈 D1 retention: {percent}% ({retained}/{cohort})\n",
        "ar": "📈 احتفاظ يوم 1: {percent}% ({retained}/{cohort})\n",
        "am": "📈 የቀን 1 ቆይታ: {percent}% ({retained}/{cohort})\n",
        "so": "📈 D1 hayn: {percent}% ({retained}/{cohort})\n",
        "om": "📈 D1 tursiisaa: {percent}% ({retained}/{cohort})\n",
        "tr": "📈 D1 elde tutma: {percent}% ({retained}/{cohort})\n"
    },
    "stats_languages": {
        "en": "🌍 Languages:\n",
        "ar": "🌍 اللغات:\n",
        "am": "🌍 ቋንቋዎች:\n",
        "so": "🌍 Luqadaha:\n",
        "om": "🌍 Afaanota:\n",
        "tr": "🌍 Diller:\n"
    },
    "stats_top_surahs": {
        "en": "📖 Top Surahs:\n",
        "ar": "📖 أكثر السور تشغيلًا:\n",
        "am": "📖 ከፍተኛ ሱራዎች:\n",
        "so": "📖 Suurado ugu sarreeya:\n",
        "om": "📖 Suuraalee ol aanaa:\n",
        "tr": "📖 En cok dinlenen sureler:\n"
    },
    "stats_no_surahs": {
        "en": "No surah plays yet.\n",
        "ar": "لا يوجد تشغيل للسور بعد.\n",
        "am": "የሱራ ጫወታ ገና የለም።\n",
        "so": "Wali ciyaarid suurad ma jiro.\n",
        "om": "Taphannaa suurataa hanga amma hin jiru.\n",
        "tr": "Henuz sure oynatma yok.\n"
    },
    "stats_no_reciters": {
        "en": "No reciter plays yet.\n",
        "ar": "لا يوجد تشغيل للقراء بعد.\n",
        "am": "የቃሪ ጫወታ ገና የለም።\n",
        "so": "Wali ciyaarid qari ma jiro.\n",
        "om": "Taphannaa qaarii hanga amma hin jiru.\n",
        "tr": "Henuz kari oynatma yok.\n"
    },
    "customers_header": {
        "en": "👥 Customers ({total}):",
        "ar": "👥 العملاء ({total}):",
        "am": "👥 ደንበኞች ({total}):",
        "so": "👥 Macaamiisha ({total}):",
        "om": "👥 Maamiltoota ({total}):",
        "tr": "👥 Musteriler ({total}):"
    },
    "customers_empty": {
        "en": "No customers found.",
        "ar": "لم يتم العثور على عملاء.",
        "am": "ምንም ደንበኞች አልተገኙም።",
        "so": "Ma jiraan macaamiil la helay.",
        "om": "Maamiltoota hin argamne.",
        "tr": "Musteri bulunamadi."
    },
    "daily_reminder": {
        "en": "🌙 *Daily Qur’an Reminder*\n\n{ayah_ar}\n\n“{ayah_en}”\n\n— Qur’an {ref}\n\nTake a moment today to listen to the Qur’an 🤍",
        "ar": "🌙 *تذكير يومي بالقرآن*\n\n{ayah_ar}\n\n“{ayah_en}”\n\n— القرآن {ref}\n\nخذ لحظة اليوم للاستماع إلى القرآن 🤍",
        "am": "🌙 *የዕለቱ ቁርአን ማሳሰቢያ*\n\n{ayah_ar}\n\n“{ayah_en}”\n\n— ቁርአን {ref}\n\nዛሬ ትንሽ ጊዜ አድርጉ ቁርአንን ለመስማት 🤍",
        "so": "🌙 *Xasuusin Qur’aan Maalinle*\n\n{ayah_ar}\n\n“{ayah_en}”\n\n— Qur’aan {ref}\n\nMaanta waqti u hel inaad dhageysato Qur’aanka 🤍",
        "om": "🌙 *Yaadachiisa Qur’aanaa Guyyaa*\n\n{ayah_ar}\n\n“{ayah_en}”\n\n— Qur’aana {ref}\n\nHar'a yeroo xiqqoo fudhadhu Qur’aana dhaggeeffachuuf 🤍",
        "tr": "🌙 *Gunluk Kur'an Hatirlatmasi*\n\n{ayah_ar}\n\n“{ayah_en}”\n\n— Kur'an {ref}\n\nBugun Kur'an dinlemek icin bir an ayirin 🤍"
    },
    "friday_reminder": {
        "en": "🕌 *Friday Reminder*\n\nMake peace upon the Prophet ﷺ and recite Surah Al-Kahf today.",
        "ar": "🕌 *تذكير يوم الجمعة*\n\nصلّوا على النبي ﷺ واقرأوا سورة الكهف اليوم.",
        "am": "🕌 *የዓርብ ማሳሰቢያ*\n\nበነቢዩ ﷺ ላይ ሰላም ይድረስ፣ ዛሬም ሱረቱ አል-ካህፍን ያንብቡ።",
        "so": "🕌 *Xasuusin Jimce*\n\nSalli nabiga ﷺ oo akhri Suurat Al-Kahf maanta.",
        "om": "🕌 *Yaadachiisa Jimaataa*\n\nNabi ﷺ irratti salaatu, har'as Suurata Al-Kahf dubbisaa.",
        "tr": "🕌 *Cuma Hatirlatmasi*\n\nBugun Peygambere ﷺ salavat getirin ve Kehf Suresi okuyun."
    },
    "ramadan_reminder": {
        "en": "🌙 *Ramadan Reminder*\n\nRamadan Mubarak! Remember to recite Qur’an and keep your heart connected to Allah.",
        "ar": "🌙 *تذكير رمضان*\n\nرمضان مبارك! أكثروا من تلاوة القرآن واذكروا الله كثيرًا.",
        "am": "🌙 *የረመዳን ማሳሰቢያ*\n\nረመዳን ሙባራክ! ቁርአንን አብዛኛውን ይነብቡ።",
        "so": "🌙 *Xasuusin Ramadaan*\n\nRamadaan mubaarak! Qur'aanka badso oo Allah xusuusnow.",
        "om": "🌙 *Yaadachiisa Ramadaan*\n\nRamadaan Mubaarak! Qur'aana hedduu dubbadhaa, Rabbiin yaadadhaa.",
        "tr": "🌙 *Ramazan Hatirlatmasi*\n\nRamazan mubarek! Kur'an okuyun ve Allah'i cokca anin."
    },
    "ramadan_friday_reminder": {
        "en": "🌙 *Ramadan + Friday*\n\nRamadan Mubarak! Make peace upon the Prophet ﷺ and recite Surah Al-Kahf today.",
        "ar": "🌙 *رمضان + الجمعة*\n\nرمضان مبارك! صلّوا على النبي ﷺ واقرأوا سورة الكهف اليوم.",
        "am": "🌙 *ረመዳን + ዓርብ*\n\nረመዳን ሙባራክ! በነቢዩ ﷺ ላይ ሰላም ይድረስ፣ ዛሬ ሱረቱ አል-ካህፍን ያንብቡ።",
        "so": "🌙 *Ramadaan + Jimce*\n\nRamadaan mubaarak! Salli nabiga ﷺ oo akhri Suurat Al-Kahf maanta.",
        "om": "🌙 *Ramadaan + Jimaataa*\n\nRamadaan Mubaarak! Nabi ﷺ irratti salaatu, har'as Suurata Al-Kahf dubbisaa.",
        "tr": "🌙 *Ramazan + Cuma*\n\nRamazan mubarek! Peygambere ﷺ salavat getirin ve Kehf Suresi okuyun."
    },
    "reciter_selected": {
        "en": "🎧 *Reciter Selected:*\n{reciter}\n\n{choose_surah}",
        "ar": "🎧 *تم اختيار القارئ:*\n{reciter}\n\n{choose_surah}",
        "am": "🎧 *ቃሪ ተመርጧል:*\n{reciter}\n\n{choose_surah}",
        "so": "🎧 *Qari la doortay:*\n{reciter}\n\n{choose_surah}",
        "om": "🎧 *Qaariin filatameera:*\n{reciter}\n\n{choose_surah}",
        "tr": "🎧 *Kari secildi:*\n{reciter}\n\n{choose_surah}"
    },
    "now_playing": {
        "en": "🎧 *Now Playing:*\n{surah}\n\nReciter: {reciter}",
        "ar": "🎧 *يتم التشغيل الآن:*\n{surah}\n\nالقارئ: {reciter}",
        "am": "🎧 *አሁን በመጫወት ላይ:*\n{surah}\n\nቃሪ: {reciter}",
        "so": "🎧 *Hadda ciyaaraya:*\n{surah}\n\nQari: {reciter}",
        "om": "🎧 *Amma taphachaa jiru:*\n{surah}\n\nQaari: {reciter}",
        "tr": "🎧 *Simdi caliyor:*\n{surah}\n\nKari: {reciter}"
    },
    "juz_select_surah": {
        "en": "📚 *Juz {juz} — Select a Surah:*",
        "ar": "📚 *الجزء {juz} — اختر سورة:*",
        "am": "📚 *ጀዝ {juz} — ሱራ ይምረጡ:*",
        "so": "📚 *Juz {juz} — Dooro Suurad:*",
        "om": "📚 *Juz {juz} — Suurata filadhaa:*",
        "tr": "📚 *Cuz {juz} — Bir Sure secin:*"
    },
    "audio_not_found": {
        "en": "❌ Audio not found. Please try again later.",
        "ar": "❌ لم يتم العثور على الصوت. حاول لاحقًا.",
        "am": "❌ ድምጹ አልተገኘም። እባክዎ ቆይተው ይሞክሩ።",
        "so": "❌ Audio lama helin. Fadlan mar kale isku day.",
        "om": "❌ Sagaleen hin argamne. Maaloo booda irra deebi'aa.",
        "tr": "❌ Ses bulunamadi. Lutfen daha sonra deneyin."
    },
    "download_failed": {
        "en": "❌ Download failed.",
        "ar": "❌ فشل التنزيل.",
        "am": "❌ አውርድ አልተሳካም።",
        "so": "❌ Soo dejintu way fashilantay.",
        "om": "❌ Buusni hin milkoofne.",
        "tr": "❌ Indirme basarisiz."
    },
    "favorite_exists": {
        "en": "Already in favorites.",
        "ar": "موجود بالفعل في المفضلة.",
        "am": "ቀድሞውኑ በምወዳቸው ውስጥ ነው።",
        "so": "Hore ayuu ugu jiray favorites.",
        "om": "Dursee filannoo keessa jira.",
        "tr": "Zaten favorilerde."
    },
    "favorite_added": {
        "en": "⭐ Added to favorites!",
        "ar": "⭐ تمت الإضافة إلى المفضلة!",
        "am": "⭐ ወደ ምወዳቸው ተጨመረ!",
        "so": "⭐ Waxaa lagu daray favorites!",
        "om": "⭐ Filannootaatti dabalame!",
        "tr": "⭐ Favorilere eklendi!"
    },
    "favorite_removed": {
        "en": "❌ Removed from favorites.",
        "ar": "❌ تمت الإزالة من المفضلة.",
        "am": "❌ ከምወዳቸው ተወግዷል።",
        "so": "❌ Waxaa laga saaray favorites.",
        "om": "❌ Filannoota irraa haqame.",
        "tr": "❌ Favorilerden kaldirildi."
    },
    "favorite_missing": {
        "en": "Not in favorites.",
        "ar": "ليس ضمن المفضلة.",
        "am": "በምወዳቸው ውስጥ አይገኝም።",
        "so": "Kuma jiro favorites.",
        "om": "Filannoota keessa hin jiru.",
        "tr": "Favorilerde degil."
    },
    "language_set": {
        "en": "✅ Language set to {language}",
        "ar": "✅ تم تعيين اللغة إلى {language}",
        "am": "✅ ቋንቋ ወደ {language} ተቀናብሯል።",
        "so": "✅ Luqadda waxaa loo dejiyey {language}",
        "om": "✅ Afaan {language}tti qindaa'ee jira",
        "tr": "✅ Dil {language} olarak ayarlandi"
    },
    "share_this_bot": {
        "en": "🔗 *Share this bot:*\n{url}",
        "ar": "🔗 *شارك هذا البوت:*\n{url}",
        "am": "🔗 *ይህን ቦት አጋሩ:*\n{url}",
        "so": "🔗 *La wadaag bot-kan:*\n{url}",
        "om": "🔗 *Bot kana qoodaa:*\n{url}",
        "tr": "🔗 *Bu botu paylas:*\n{url}"
    },
    "share_fallback": {
        "en": "🔗 Share this bot by sending its username to your friends.",
        "ar": "🔗 شارك هذا البوت بإرسال اسمه للمستخدمين الآخرين.",
        "am": "🔗 የቦቱን የተጠቃሚ ስም ለጓደኞችዎ በላክ አጋሩ።",
        "so": "🔗 La wadaag bot-kan adigoo u diraya username-kiisa asxaabtaada.",
        "om": "🔗 Bot kana qoodaa maqaasa fayyadamaa hiruuf.",
        "tr": "🔗 Botun kullanici adini arkadaslarina gondererek paylas."
    },
    "menu_cleared": {
        "en": "✅ Menu cleared.",
        "ar": "✅ تم مسح القائمة.",
        "am": "✅ ማውጫ ተሰርዟል።",
        "so": "✅ Menu-ga waa la tirtiray.",
        "om": "✅ Menuun haqameera.",
        "tr": "✅ Menu temizlendi."
    },
    "use_menu": {
        "en": "🤍 Please use /menu to navigate the bot.",
        "ar": "🤍 رجاءً استخدم /menu للتنقل في البوت.",
        "am": "🤍 እባክዎ /menu ተጠቅመው ቦቱን ይንቀሳቀሱ።",
        "so": "🤍 Fadlan isticmaal /menu si aad u dhex musho bot-ka.",
        "om": "🤍 Maaloo /menu fayyadami bot kana keessatti naanna'uuf.",
        "tr": "🤍 Lutfen botta gezinmek icin /menu kullanin."
    },
    "settings_title": {
        "en": "⚙️ *Preferences*",
        "ar": "⚙️ *التفضيلات*",
        "am": "⚙️ *ምርጫዎች*",
        "so": "⚙️ *Doorbidyo*",
        "om": "⚙️ *Filannoo*",
        "tr": "⚙️ *Tercihler*"
    },
    "reminder_time_prompt": {
        "en": "⏰ Send your reminder time in HH:MM (e.g., 07:30).",
        "ar": "⏰ أرسل وقت التذكير بصيغة HH:MM (مثال 07:30).",
        "am": "⏰ የማሳሰቢያ ሰዓትዎን በHH:MM ላክ (ለምሳሌ 07:30).",
        "so": "⏰ Soo dir waqtiga xasuusinta HH:MM (tusaale 07:30).",
        "om": "⏰ Yeroo yaadachiisummaa HH:MM keessatti ergi (fkn 07:30).",
        "tr": "⏰ Hatirlatma saatini HH:MM formatinda gonder (ornegin 07:30)."
    },
    "reminder_invalid_time": {
        "en": "❌ Invalid time. Please use HH:MM (00:00-23:59).",
        "ar": "❌ وقت غير صالح. استخدم HH:MM (00:00-23:59).",
        "am": "❌ የማይሰራ ሰዓት። HH:MM ተጠቀሙ (00:00-23:59).",
        "so": "❌ Waqti aan sax ahayn. Isticmaal HH:MM (00:00-23:59).",
        "om": "❌ Yeroo sirrii hin taane. HH:MM fayyadami (00:00-23:59).",
        "tr": "❌ Gecersiz saat. HH:MM kullanin (00:00-23:59)."
    },
    "reminder_saved": {
        "en": "✅ Reminder set for {time}.",
        "ar": "✅ تم ضبط التذكير على {time}.",
        "am": "✅ ማሳሰቢያው {time} ተዘጋጅቷል።",
        "so": "✅ Xasuusinta waxaa loo dejiyey {time}.",
        "om": "✅ Yaadachiisni {time} irratti qindaa'eera.",
        "tr": "✅ Hatirlatma {time} icin ayarlandi."
    },
    "feedback_prompt": {
        "en": "💬 Send your feedback or suggestion.",
        "ar": "💬 أرسل ملاحظتك أو اقتراحك.",
        "am": "💬 ግብረመልስዎን ወይም ምክርዎን ይላኩ።",
        "so": "💬 Soo dir jawaab celintaada ama taladaada.",
        "om": "💬 Yaada ykn gorsa kee ergi.",
        "tr": "💬 Geri bildiriminizi veya onerilerinizi gonderin."
    },
    "feedback_sent": {
        "en": "✅ Thanks! Your feedback was sent.",
        "ar": "✅ شكرًا! تم إرسال ملاحظتك.",
        "am": "✅ አመሰግናለሁ! ግብረመልስዎ ተልኳል።",
        "so": "✅ Mahadsanid! Jawaab celintaada waa la diray.",
        "om": "✅ Galatoomi! Yaada kee ergameera.",
        "tr": "✅ Tesekkurler! Geri bildiriminiz gonderildi."
    },
    "resume_empty": {
        "en": "⏯️ No recent surah to resume.",
        "ar": "⏯️ لا توجد سورة حديثة للاستئناف.",
        "am": "⏯️ ለመቀጠል የቅርብ ጊዜ ሱራ የለም።",
        "so": "⏯️ Ma jiro suurad dhawaan la ciyaaray.",
        "om": "⏯️ Suurata dhiyoo itti fufuuf hin jiru.",
        "tr": "⏯️ Devam edilecek yakin sure yok."
    },
    "search_prompt": {
        "en": "🔎 Send a Surah name or number.",
        "ar": "🔎 أرسل اسم السورة أو رقمها.",
        "am": "🔎 የሱራ ስም ወይም ቁጥር ላክ።",
        "so": "🔎 Soo dir magaca ama lambarka suuradda.",
        "om": "🔎 Maqaa yookaan lakkoofsa Suuraa ergi.",
        "tr": "🔎 Sure adi veya numarasi gonderin."
    },
    "search_results": {
        "en": "🔎 Results for \"{query}\" (showing {count}/{total})",
        "ar": "🔎 نتائج \"{query}\" (عرض {count}/{total})",
        "am": "🔎 ውጤቶች ለ\"{query}\" ({count}/{total} ይታያል)",
        "so": "🔎 Natiijooyinka \"{query}\" (muujinaya {count}/{total})",
        "om": "🔎 Bu'aa \"{query}\" ({count}/{total} agarsiisa)",
        "tr": "🔎 \"{query}\" icin sonuclar ({count}/{total} gosteriliyor)"
    },
    "search_no_results": {
        "en": "❌ No surah matched that search.",
        "ar": "❌ لا توجد نتائج مطابقة.",
        "am": "❌ የሚመሳሰል ሱራ አልተገኘም።",
        "so": "❌ Suurad la mid ah lama helin.",
        "om": "❌ Suurata walfakkaataa hin argamne.",
        "tr": "❌ Eslesen sure bulunamadi."
    },
    "default_reciter_set": {
        "en": "✅ Default reciter set to {reciter}.",
        "ar": "✅ تم تعيين القارئ الافتراضي إلى {reciter}.",
        "am": "✅ ነባሪ ቃሪ ወደ {reciter} ተቀናብሯል።",
        "so": "✅ Qari-ga caadiga ah waxaa loo dejiyey {reciter}.",
        "om": "✅ Qaariin durtii gara {reciter}tti qindaa'eera.",
        "tr": "✅ Varsayilan kari {reciter} olarak ayarlandi."
    },
    "category_prompt": {
        "en": "📁 Send a new category name.",
        "ar": "📁 أرسل اسم فئة جديدة.",
        "am": "📁 አዲስ የክፍል ስም ላክ።",
        "so": "📁 Soo dir magaca qeyb cusub.",
        "om": "📁 Maqaa ramaddii haaraa ergi.",
        "tr": "📁 Yeni bir kategori adi gonderin."
    },
    "category_added": {
        "en": "✅ Category added: {category}",
        "ar": "✅ تمت إضافة الفئة: {category}",
        "am": "✅ ክፍል ተጨምሯል: {category}",
        "so": "✅ Qeybta waa lagu daray: {category}",
        "om": "✅ Ramaddii dabalame: {category}",
        "tr": "✅ Kategori eklendi: {category}"
    },
    "category_exists": {
        "en": "❌ Category already exists.",
        "ar": "❌ الفئة موجودة بالفعل.",
        "am": "❌ ክፍሉ አስቀድሞ አለ።",
        "so": "❌ Qeybta horay ayey u jirtaa.",
        "om": "❌ Ramaddiin dursee jira.",
        "tr": "❌ Kategori zaten var."
    },
    "category_invalid": {
        "en": "❌ Invalid category name.",
        "ar": "❌ اسم فئة غير صالح.",
        "am": "❌ የማይሰራ የክፍል ስም።",
        "so": "❌ Magac qeyb aan sax ahayn.",
        "om": "❌ Maqaa ramaddii sirrii hin taane.",
        "tr": "❌ Gecersiz kategori adi."
    },
    "favorites_categories_title": {
        "en": "⭐ *Favorite Categories:*",
        "ar": "⭐ *فئات المفضلة:*",
        "am": "⭐ *የምወዳቸው ክፍሎች:*",
        "so": "⭐ *Qeybaha Favorites:*",
        "om": "⭐ *Ramaddoota Filannoo:*",
        "tr": "⭐ *Favori Kategorileri:*"
    },
    "favorites_category_title": {
        "en": "⭐ *Favorites — {category}:*",
        "ar": "⭐ *المفضلة — {category}:*",
        "am": "⭐ *የምወዳቸው — {category}:*",
        "so": "⭐ *Favorites — {category}:*",
        "om": "⭐ *Filannoo — {category}:*",
        "tr": "⭐ *Favoriler — {category}:*"
    },
    "favorites_all_title": {
        "en": "⭐ *All Favorites:*",
        "ar": "⭐ *كل المفضلة:*",
        "am": "⭐ *ሁሉም የምወዳቸው:*",
        "so": "⭐ *Dhammaan Favorites:*",
        "om": "⭐ *Filannoo Hunda:*",
        "tr": "⭐ *Tum Favoriler:*"
    },
    "pick_category": {
        "en": "📁 Choose a category for this favorite:",
        "ar": "📁 اختر فئة لهذه المفضلة:",
        "am": "📁 ለዚህ ምወደው ክፍል ምረጥ:",
        "so": "📁 U dooro qeybta favorite-kan:",
        "om": "📁 Filannoo kanaaf ramaddii filadhu:",
        "tr": "📁 Bu favori icin bir kategori secin:"
    },
    "user_stats": {
        "en": "📈 *Your Stats*\n\n🎧 Plays: {plays}\n⭐ Favorites: {favorites}\n🎙️ Top reciter: {top_reciter}\n⏯️ Last played: {last_played}",
        "ar": "📈 *إحصائياتك*\n\n🎧 مرات التشغيل: {plays}\n⭐ المفضلة: {favorites}\n🎙️ القارئ المفضل: {top_reciter}\n⏯️ آخر ما تم تشغيله: {last_played}",
        "am": "📈 *የእርስዎ ስታት*\n\n🎧 ጫወቶች: {plays}\n⭐ የምወዳቸው: {favorites}\n🎙️ ዋና ቃሪ: {top_reciter}\n⏯️ መጨረሻ የተጫወተው: {last_played}",
        "so": "📈 *Tirakoobkaaga*\n\n🎧 Ciyaaro: {plays}\n⭐ Favorites: {favorites}\n🎙️ Qari-ga ugu badan: {top_reciter}\n⏯️ Ugu dambeeyay: {last_played}",
        "om": "📈 *Istaatistika kee*\n\n🎧 Taphattoota: {plays}\n⭐ Filannoo: {favorites}\n🎙️ Qaariin ol aanaa: {top_reciter}\n⏯️ Kan dhumaa: {last_played}",
        "tr": "📈 *Istatistikleriniz*\n\n🎧 Oynatmalar: {plays}\n⭐ Favoriler: {favorites}\n🎙️ En iyi kari: {top_reciter}\n⏯️ Son calinan: {last_played}"
    },
    "cache_title": {
        "en": "📦 *Cache*",
        "ar": "📦 *الذاكرة المؤقتة*",
        "am": "📦 *ካሽ*",
        "so": "📦 *Kayd*",
        "om": "📦 *Kaashii*",
        "tr": "📦 *Onbellek*"
    },
    "cache_stats": {
        "en": "📦 Cache files: {count}\n💾 Size: {size_mb} MB",
        "ar": "📦 ملفات الكاش: {count}\n💾 الحجم: {size_mb} م.ب",
        "am": "📦 የካሽ ፋይሎች: {count}\n💾 መጠን: {size_mb} ሜ.ባ",
        "so": "📦 Faylasha kaydka: {count}\n💾 Cabirka: {size_mb} MB",
        "om": "📦 Faayiloota kaashii: {count}\n💾 Gudina: {size_mb} MB",
        "tr": "📦 Onbellek dosyalari: {count}\n💾 Boyut: {size_mb} MB"
    },
    "cache_cleared": {
        "en": "✅ Cache cleared.",
        "ar": "✅ تم مسح الكاش.",
        "am": "✅ ካሽ ተሰርዟል።",
        "so": "✅ Kaydka waa la tirtiray.",
        "om": "✅ Kaashiin haqameera.",
        "tr": "✅ Onbellek temizlendi."
    },
    "contacts": {
        "en": "📬 *Contact Admin:*\n\nTelegram: [Yusuf Mohammed](https://t.me/Cs1At07)\nInstagram: [Yusuf Mohammed](https://instagram.com/kebilad_7488)\n\nEmail:[ym47484988@gmail.com](mailto:ym47484988@gmail.com)\n\nFor support, feedback, or suggestions.",
        "ar": "📬 *تواصل مع المشرف:*\n\nTelegram: [Yusuf Mohammed](https://t.me/Cs1At07)\nInstagram: [Yusuf Mohammed](https://instagram.com/kebilad_7488)\n\nEmail:[ym47484988@gmail.com](mailto:ym47484988@gmail.com)\n\nللدعم أو الملاحظات أو الاقتراحات.",
        "am": "📬 *አስተዳዳሪን አግኝ:*\n\nTelegram: [Yusuf Mohammed](https://t.me/Cs1At07)\nInstagram: [Yusuf Mohammed](https://instagram.com/kebilad_7488)\n\nEmail:[ym47484988@gmail.com](mailto:ym47484988@gmail.com)\n\nለድጋፍ፣ ግብረመልስ ወይም ምክሮች።",
        "so": "📬 *La xiriir Admin:*\n\nTelegram: [Yusuf Mohammed](https://t.me/Cs1At07)\nInstagram: [Yusuf Mohammed](https://instagram.com/kebilad_7488)\n\nEmail:[ym47484988@gmail.com](mailto:ym47484988@gmail.com)\n\nTaageero, jawaab celin, ama talooyin.",
        "om": "📬 *Admin quunnamaa:*\n\nTelegram: [Yusuf Mohammed](https://t.me/Cs1At07)\nInstagram: [Yusuf Mohammed](https://instagram.com/kebilad_7488)\n\nEmail:[ym47484988@gmail.com](mailto:ym47484988@gmail.com)\n\nDeeggarsa, yaada, yookaan gorsaaf.",
        "tr": "📬 *Yonetici iletisim:*\n\nTelegram: [Yusuf Mohammed](https://t.me/Cs1At07)\nInstagram: [Yusuf Mohammed](https://instagram.com/kebilad_7488)\n\nEmail:[ym47484988@gmail.com](mailto:ym47484988@gmail.com)\n\nDestek, geri bildirim veya oneriler icin."
    },
    "socials": {
        "en": "🌟 Follow for more Islamic reminders:\n\nTelegram: [NoorVibes ☪️](https://t.me/noorvibes_light)\nLinkedIn: [Yusuf Mohammed](https://www.linkedin.com/in/yusuf-mohammed-5272572b6)\nInstagram: [Yusuf Mohammed](https://instagram.com/kebilad_7488)\n\nMay Allah reward you 🤍",
        "ar": "🌟 تابع للمزيد من التذكيرات الإسلامية:\n\nTelegram: [NoorVibes ☪️](https://t.me/noorvibes_light)\nLinkedIn: [Yusuf Mohammed](https://www.linkedin.com/in/yusuf-mohammed-5272572b6)\nInstagram: [Yusuf Mohammed](https://instagram.com/kebilad_7488)\n\nجزاك الله خيرًا 🤍",
        "am": "🌟 ተጨማሪ እስላማዊ ማሳሰቢያዎችን ለማግኘት ተከተሉን:\n\nTelegram: [NoorVibes ☪️](https://t.me/noorvibes_light)\nLinkedIn: [Yusuf Mohammed](https://www.linkedin.com/in/yusuf-mohammed-5272572b6)\nInstagram: [Yusuf Mohammed](https://instagram.com/kebilad_7488)\n\nአላህ ይክፈልህ 🤍",
        "so": "🌟 Nala soco xasuusino Islaami ah:\n\nTelegram: [NoorVibes ☪️](https://t.me/noorvibes_light)\nLinkedIn: [Yusuf Mohammed](https://www.linkedin.com/in/yusuf-mohammed-5272572b6)\nInstagram: [Yusuf Mohammed](https://instagram.com/kebilad_7488)\n\nAllaah ha ku ajar siiyo 🤍",
        "om": "🌟 Yaadachiisa Islaamaa dabalataa argachuuf nu hordofaa:\n\nTelegram: [NoorVibes ☪️](https://t.me/noorvibes_light)\nLinkedIn: [Yusuf Mohammed](https://www.linkedin.com/in/yusuf-mohammed-5272572b6)\nInstagram: [Yusuf Mohammed](https://instagram.com/kebilad_7488)\n\nRabbiin si mindeessu 🤍",
        "tr": "🌟 Daha fazla Islami hatirlatma icin takip edin:\n\nTelegram: [NoorVibes ☪️](https://t.me/noorvibes_light)\nLinkedIn: [Yusuf Mohammed](https://www.linkedin.com/in/yusuf-mohammed-5272572b6)\nInstagram: [Yusuf Mohammed](https://instagram.com/kebilad_7488)\n\nAllah razi olsun 🤍"
    },
    "btn_surahs": {
        "en": "🎧 Surahs",
        "ar": "🎧 السور",
        "am": "🎧 ሱራዎች",
        "so": "🎧 Suurado",
        "om": "🎧 Suuraalee",
        "tr": "🎧 Sureler"
    },
    "btn_reciters": {
        "en": "🎙️ Reciters",
        "ar": "🎙️ القرّاء",
        "am": "🎙️ ቃሪዎች",
        "so": "🎙️ Qurri",
        "om": "🎙️ Qaariyoota",
        "tr": "🎙️ Kurralar"
    },
    "btn_juz": {
        "en": "📚 Juz",
        "ar": "📚 أجزاء",
        "am": "📚 ጀዞች",
        "so": "📚 Juz",
        "om": "📚 Juz",
        "tr": "📚 Cuz"
    },
    "btn_ayah": {
        "en": "📖 Ayah",
        "ar": "📖 آية",
        "am": "📖 አያ",
        "so": "📖 Aayad",
        "om": "📖 Aayaa",
        "tr": "📖 Ayet"
    },
    "btn_favorites": {
        "en": "⭐ Favorites",
        "ar": "⭐ المفضلة",
        "am": "⭐ የምወዳቸው",
        "so": "⭐ Favorites",
        "om": "⭐ Filannoo",
        "tr": "⭐ Favoriler"
    },
    "btn_language": {
        "en": "🌐 Language",
        "ar": "🌐 اللغة",
        "am": "🌐 ቋንቋ",
        "so": "🌐 Luqad",
        "om": "🌐 Afaan",
        "tr": "🌐 Dil"
    },
    "btn_share": {
        "en": "📢 Share",
        "ar": "📢 شارك",
        "am": "📢 አጋራ",
        "so": "📢 La wadaag",
        "om": "📢 Qoodi",
        "tr": "📢 Paylas"
    },
    "btn_help": {
        "en": "🆘 Help",
        "ar": "🆘 مساعدة",
        "am": "🆘 እገዛ",
        "so": "🆘 Caawimaad",
        "om": "🆘 Gargaarsa",
        "tr": "🆘 Yardim"
    },
    "btn_support": {
        "en": "🛟 Support",
        "ar": "🛟 دعم",
        "am": "🛟 ድጋፍ",
        "so": "🛟 Taageero",
        "om": "🛟 Deeggarsa",
        "tr": "🛟 Destek"
    },
    "btn_feedback": {
        "en": "💬 Feedback",
        "ar": "💬 ملاحظات",
        "am": "💬 ግብረመልስ",
        "so": "💬 Jawaab celin",
        "om": "💬 Yaada",
        "tr": "💬 Geri bildirim"
    },
    "btn_admin": {
        "en": "🛠 Admin",
        "ar": "🛠 المشرف",
        "am": "🛠 አስተዳዳሪ",
        "so": "🛠 Admin",
        "om": "🛠 Admin",
        "tr": "🛠 Admin"
    },
    "btn_admin_broadcast": {
        "en": "📣 Broadcast",
        "ar": "📣 بث",
        "am": "📣 ስርጭት",
        "so": "📣 Broadcast",
        "om": "📣 Broadcast",
        "tr": "📣 Yayın"
    },
    "btn_admin_stats": {
        "en": "📊 Stats",
        "ar": "📊 إحصائيات",
        "am": "📊 ስታትስ",
        "so": "📊 Stats",
        "om": "📊 Stats",
        "tr": "📊 Istatistik"
    },
    "btn_admin_customers": {
        "en": "👥 Customers",
        "ar": "👥 العملاء",
        "am": "👥 ደንበኞች",
        "so": "👥 Macaamiil",
        "om": "👥 Customers",
        "tr": "👥 Musteriler"
    },
    "btn_admin_export": {
        "en": "⬇️ Export",
        "ar": "⬇️ تصدير",
        "am": "⬇️ ውጣ",
        "so": "⬇️ Dhoofin",
        "om": "⬇️ Export",
        "tr": "⬇️ Disari aktar"
    },
    "btn_contact": {
        "en": "📬 Contact",
        "ar": "📬 تواصل",
        "am": "📬 አግኝ",
        "so": "📬 La xiriir",
        "om": "📬 Quunnamtii",
        "tr": "📬 Iletisim"
    },
    "btn_socials": {
        "en": "🌟 Follow Us",
        "ar": "🌟 تابعنا",
        "am": "🌟 ተከተሉን",
        "so": "🌟 Nala soco",
        "om": "🌟 Nu hordofaa",
        "tr": "🌟 Takip et"
    },
    "btn_resume": {
        "en": "⏯ Resume",
        "ar": "⏯ استئناف",
        "am": "⏯ እንደገና",
        "so": "⏯ Sii wad",
        "om": "⏯ Itti fufi",
        "tr": "⏯ Devam"
    },
    "btn_search": {
        "en": "🔎 Search",
        "ar": "🔎 بحث",
        "am": "🔎 ፈልግ",
        "so": "🔎 Raadi",
        "om": "🔎 Barbaadi",
        "tr": "🔎 Ara"
    },
    "btn_settings": {
        "en": "⚙️ Settings",
        "ar": "⚙️ الإعدادات",
        "am": "⚙️ ቅንብሮች",
        "so": "⚙️ Dejinta",
        "om": "⚙️ Qindaa'ina",
        "tr": "⚙️ Ayarlar"
    },
    "btn_my_stats": {
        "en": "📈 My Stats",
        "ar": "📈 إحصائياتي",
        "am": "📈 ስታቴ",
        "so": "📈 Tirakoobkeyga",
        "om": "📈 Istaatistika koo",
        "tr": "📈 Istatistiklerim"
    },
    "btn_set_reciter": {
        "en": "🎙️ Default Reciter",
        "ar": "🎙️ القارئ الافتراضي",
        "am": "🎙️ ነባሪ ቃሪ",
        "so": "🎙️ Qari-ga caadiga ah",
        "om": "🎙️ Qaarii durtii",
        "tr": "🎙️ Varsayilan kari"
    },
    "btn_cache": {
        "en": "📦 Cache",
        "ar": "📦 الكاش",
        "am": "📦 ካሽ",
        "so": "📦 Kayd",
        "om": "📦 Kaashii",
        "tr": "📦 Onbellek"
    },
    "btn_clear_cache": {
        "en": "🗑 Clear Cache",
        "ar": "🗑 مسح الكاش",
        "am": "🗑 ካሽ አጥፋ",
        "so": "🗑 Tirtir kaydka",
        "om": "🗑 Kaashii haqi",
        "tr": "🗑 Onbellegi temizle"
    },
    "btn_add_category": {
        "en": "➕ Add Category",
        "ar": "➕ إضافة فئة",
        "am": "➕ ክፍል ጨምር",
        "so": "➕ Ku dar qeyb",
        "om": "➕ Ramaddii dabali",
        "tr": "➕ Kategori ekle"
    },
    "btn_all_favorites": {
        "en": "⭐ All Favorites",
        "ar": "⭐ كل المفضلة",
        "am": "⭐ ሁሉም ምወዳቸው",
        "so": "⭐ Dhammaan Favorites",
        "om": "⭐ Filannoo Hunda",
        "tr": "⭐ Tum favoriler"
    },
    "btn_back": {
        "en": "⬅️ Back",
        "ar": "⬅️ رجوع",
        "am": "⬅️ ወደ ኋላ",
        "so": "⬅️ Dib u noqo",
        "om": "⬅️ Deebi'i",
        "tr": "⬅️ Geri"
    },
    "btn_prev": {
        "en": "⬅️ Prev",
        "ar": "⬅️ السابق",
        "am": "⬅️ ቀዳሚ",
        "so": "⬅️ Hore",
        "om": "⬅️ Dura",
        "tr": "⬅️ Onceki"
    },
    "btn_next": {
        "en": "Next ➡️",
        "ar": "التالي ➡️",
        "am": "ቀጣይ ➡️",
        "so": "Xiga ➡️",
        "om": "Itti Aanee ➡️",
        "tr": "Sonraki ➡️"
    },
    "btn_favorite": {
        "en": "⭐ Favorite",
        "ar": "⭐ مفضلة",
        "am": "⭐ ምወደው",
        "so": "⭐ Favorite",
        "om": "⭐ Filannoo",
        "tr": "⭐ Favori"
    },
    "btn_remove": {
        "en": "❌ Remove",
        "ar": "❌ إزالة",
        "am": "❌ አስወግድ",
        "so": "❌ Ka saar",
        "om": "❌ Balleessi",
        "tr": "❌ Kaldir"
    },
    "btn_download": {
        "en": "⬇️ Download",
        "ar": "⬇️ تنزيل",
        "am": "⬇️ አውርድ",
        "so": "⬇️ Soo dejiso",
        "om": "⬇️ Buusi",
        "tr": "⬇️ Indir"
    },
    "btn_change_reciter": {
        "en": "🎙️ Change Reciter",
        "ar": "🎙️ تغيير القارئ",
        "am": "🎙️ ቃሪ ቀይር",
        "so": "🎙️ Bedel Qari",
        "om": "🎙️ Qaarii Jijjiiri",
        "tr": "🎙️ Kari degistir"
    },
    "btn_main_menu": {
        "en": "🏠 Main Menu",
        "ar": "🏠 القائمة الرئيسية",
        "am": "🏠 ዋና ማውጫ",
        "so": "🏠 Menu-ga Ugu Weyn",
        "om": "🏠 Menu Ijoo",
        "tr": "🏠 Ana Menu"
    },
    "reply_start": {
        "en": "▶️ Start",
        "ar": "▶️ ابدأ",
        "am": "▶️ ጀምር",
        "so": "▶️ Bilow",
        "om": "▶️ Jalqabi",
        "tr": "▶️ Baslat"
    },
    "reply_clear_menu": {
        "en": "❌ Clear Menu",
        "ar": "❌ امسح القائمة",
        "am": "❌ ማውጫ አጥፋ",
        "so": "❌ Tirtir Menu",
        "om": "❌ Menu Haqi",
        "tr": "❌ Menuyu temizle"
    }
}
