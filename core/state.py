import logging
from collections import defaultdict
from datetime import datetime
from telegram.ext import ContextTypes
import os
from core.config import REMINDER_GLOBAL_TIME, STATE_FILE
from core.db import (
    db_has_users,
    init_db,
    load_state_from_db,
    migrate_json_to_db,
    record_activity,
    save_user_state_to_db,
    touch_user
)

logger = logging.getLogger(__name__)

USERS = set()
RECITER_PLAYS = defaultdict(int)
USER_FAVORITES = defaultdict(dict)
USER_DEFAULT_RECITER = {}
USER_LAST_PLAYED = {}
USER_STATS = defaultdict(lambda: {"plays": 0, "reciters": {}})
USER_LANG = defaultdict(lambda: "en")
USER_PROFILES = defaultdict(dict)
USER_TZ_OFFSET = defaultdict(int)


def load_state():
    return load_state_from_db()


def save_state():
    for user_id in USERS:
        save_user_state_to_db(
            user_id,
            USER_LANG.get(user_id, "en"),
            USER_DEFAULT_RECITER.get(user_id, "r01"),
            USER_LAST_PLAYED.get(user_id, {}),
            USER_STATS.get(user_id, {"plays": 0, "reciters": {}}),
            USER_FAVORITES.get(user_id, {"Default": set()}),
            USER_PROFILES.get(user_id, {}).get("username"),
            REMINDER_GLOBAL_TIME,
            USER_TZ_OFFSET.get(user_id, 0),
            USER_PROFILES.get(user_id, {}).get("first_seen"),
            USER_PROFILES.get(user_id, {}).get("last_seen")
        )


def ensure_user_favorites(user_id):
    favs = USER_FAVORITES.get(user_id)
    if not favs:
        USER_FAVORITES[user_id] = {"Default": set()}
    elif isinstance(favs, set):
        USER_FAVORITES[user_id] = {"Default": favs}


def get_all_favorites(user_id):
    ensure_user_favorites(user_id)
    all_items = set()
    for items in USER_FAVORITES[user_id].values():
        all_items.update(items)
    return all_items


def track_user(context: ContextTypes.DEFAULT_TYPE, chat_id: int, user=None):
    users = context.application.bot_data.setdefault("users", set())
    users.add(chat_id)
    if chat_id not in USERS:
        USERS.add(chat_id)
        save_state()
    ensure_user_favorites(chat_id)
    USER_DEFAULT_RECITER.setdefault(chat_id, "r01")
    USER_STATS.setdefault(chat_id, {"plays": 0, "reciters": {}})
    USER_TZ_OFFSET.setdefault(chat_id, 0)
    if user and user.username:
        current = USER_PROFILES.get(chat_id, {}).get("username")
        if current != user.username:
            USER_PROFILES[chat_id]["username"] = user.username
            save_state()
    today = datetime.utcnow().date().isoformat()
    USER_PROFILES[chat_id]["last_seen"] = today
    USER_PROFILES[chat_id].setdefault("first_seen", today)
    record_activity(chat_id, today)
    touch_user(
        chat_id,
        USER_PROFILES.get(chat_id, {}).get("username"),
        USER_LANG.get(chat_id, "en"),
        USER_DEFAULT_RECITER.get(chat_id, "r01"),
        REMINDER_GLOBAL_TIME,
        USER_TZ_OFFSET.get(chat_id, 0),
        today
    )


                                                                         

def load_state_into():
    init_db()
    if os.path.exists(STATE_FILE) and not db_has_users():
        migrate_json_to_db(STATE_FILE)
    state = load_state()
    USERS.update(state.get("users", []))
    for user_id, lang in state.get("languages", {}).items():
        USER_LANG[int(user_id)] = lang
    for user_id, favs in state.get("favorites", {}).items():
        user_key = int(user_id)
        if isinstance(favs, list):
            USER_FAVORITES[user_key] = {"Default": set(favs)}
        else:
            USER_FAVORITES[user_key] = {
                cat: set(items) for cat, items in favs.items()
            }
    for user_id, rec in state.get("default_reciters", {}).items():
        USER_DEFAULT_RECITER[int(user_id)] = rec
    for user_id, data in state.get("last_played", {}).items():
        USER_LAST_PLAYED[int(user_id)] = data
    for user_id, stats in state.get("user_stats", {}).items():
        USER_STATS[int(user_id)] = stats
    for user_id, profile in state.get("user_profiles", {}).items():
        USER_PROFILES[int(user_id)] = profile
    for user_id, reminder in state.get("user_reminders", {}).items():
        if reminder.get("tz_offset") is not None:
            USER_TZ_OFFSET[int(user_id)] = reminder.get("tz_offset")
