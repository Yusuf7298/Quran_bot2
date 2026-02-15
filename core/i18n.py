import re

from core.config import LANGUAGES, TEXTS
def t(key, lang, **kwargs):
    text = TEXTS.get(key, {}).get(lang) or TEXTS.get(key, {}).get("en") or ""
    return text.format(**kwargs) if kwargs else text
def matches_label(text, key):
    normalized = text.strip().lower()
    options = {t(key, code).lower() for code in LANGUAGES.keys()}
    options.add(t(key, "en").lower())
    return normalized in options

def is_favorites_message(message_text):
    normalized = message_text.strip()
    for code in LANGUAGES.keys():
        titles = [
            t("favorites_title", code),
            t("favorites_all_title", code),
            t("favorites_categories_title", code),
            t("favorites_category_title", code).replace("{category}", "")
        ]
        for title in titles:
            title_plain = title.replace("*", "")
            if title_plain and title_plain in normalized:
                return True
    return False


_PEACE_GREETINGS = {
    "en": ["salam", "salaam", "assalamu alaikum", "assalamualaikum"],
    "ar": ["السلام عليكم", "السلام عليكم ورحمة الله"],
    "am": ["ሰላም"],
    "so": ["asc", "assalamu alaikum", "salaam"],
    "om": ["salaam", "assalamu alaikum"],
    "tr": ["selam", "selamun aleykum", "selamun aleyküm"]
}


def _normalize_greeting(text):
    cleaned = re.sub(r"[^0-9A-Za-z\u0600-\u06FF\u1200-\u137F\s]", " ", text)
    return " ".join(cleaned.casefold().split())


def is_peace_greeting(text, lang):
    normalized = _normalize_greeting(text)
    for item in _PEACE_GREETINGS.get(lang, []):
        if normalized.startswith(_normalize_greeting(item)):
            return True
    for item in _PEACE_GREETINGS.get("en", []):
        if normalized.startswith(_normalize_greeting(item)):
            return True
    return False
