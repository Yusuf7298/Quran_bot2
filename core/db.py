import json
import logging
import sqlite3

from core.config import DB_FILE

logger = logging.getLogger(__name__)


def get_conn():
    return sqlite3.connect(DB_FILE)


def init_db():
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                language TEXT,
                default_reciter TEXT,
                last_played_surah INTEGER,
                last_played_reciter TEXT,
                username TEXT,
                reminder_time TEXT,
                tz_offset INTEGER,
                first_seen TEXT,
                last_seen TEXT
            )
            """
        )
        ensure_column(conn, "users", "username", "TEXT")
        ensure_column(conn, "users", "reminder_time", "TEXT")
        ensure_column(conn, "users", "tz_offset", "INTEGER")
        ensure_column(conn, "users", "first_seen", "TEXT")
        ensure_column(conn, "users", "last_seen", "TEXT")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS favorites (
                user_id INTEGER,
                category TEXT,
                surah_num INTEGER,
                PRIMARY KEY (user_id, category, surah_num)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS user_stats (
                user_id INTEGER PRIMARY KEY,
                plays INTEGER,
                reciters_json TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS user_activity (
                user_id INTEGER,
                activity_date TEXT,
                PRIMARY KEY (user_id, activity_date)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS surah_stats (
                surah_num INTEGER PRIMARY KEY,
                plays INTEGER
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                message TEXT,
                created_at TEXT
            )
            """
        )
        conn.commit()


def ensure_column(conn, table, column, column_type):
    columns = [row[1] for row in conn.execute(f"PRAGMA table_info({table})")]
    if column not in columns:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {column_type}")


def db_has_users():
    with get_conn() as conn:
        row = conn.execute("SELECT COUNT(*) FROM users").fetchone()
        return row and row[0] > 0


def load_state_from_db():
    data = {
        "users": [],
        "favorites": {},
        "languages": {},
        "default_reciters": {},
        "last_played": {},
        "user_stats": {},
        "user_profiles": {},
        "user_reminders": {}
    }
    with get_conn() as conn:
        for row in conn.execute(
            "SELECT user_id, language, default_reciter, last_played_surah, last_played_reciter, username, reminder_time, tz_offset, first_seen, last_seen FROM users"
        ):
            user_id, language, default_reciter, last_surah, last_reciter, username, reminder_time, tz_offset, first_seen, last_seen = row
            data["users"].append(user_id)
            if language:
                data["languages"][str(user_id)] = language
            if default_reciter:
                data["default_reciters"][str(user_id)] = default_reciter
            if last_surah and last_reciter:
                data["last_played"][str(user_id)] = {
                    "surah": last_surah,
                    "reciter": last_reciter
                }
            profile = {}
            if username:
                profile["username"] = username
            if first_seen:
                profile["first_seen"] = first_seen
            if last_seen:
                profile["last_seen"] = last_seen
            if profile:
                data["user_profiles"][str(user_id)] = profile
            if reminder_time or tz_offset is not None:
                data["user_reminders"][str(user_id)] = {
                    "time": reminder_time,
                    "tz_offset": tz_offset
                }
        for row in conn.execute(
            "SELECT user_id, category, surah_num FROM favorites"
        ):
            user_id, category, surah_num = row
            data["favorites"].setdefault(str(user_id), {}).setdefault(category, []).append(surah_num)
        for row in conn.execute(
            "SELECT user_id, plays, reciters_json FROM user_stats"
        ):
            user_id, plays, reciters_json = row
            reciters = {}
            if reciters_json:
                try:
                    reciters = json.loads(reciters_json)
                except json.JSONDecodeError:
                    reciters = {}
            data["user_stats"][str(user_id)] = {
                "plays": plays or 0,
                "reciters": reciters
            }
    return data


def save_user_state_to_db(
    user_id,
    language,
    default_reciter,
    last_played,
    stats,
    favorites,
    username=None,
    reminder_time=None,
    tz_offset=None,
    first_seen=None,
    last_seen=None
):
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO users (
                user_id,
                language,
                default_reciter,
                last_played_surah,
                last_played_reciter,
                username,
                reminder_time,
                tz_offset,
                first_seen,
                last_seen
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                language=excluded.language,
                default_reciter=excluded.default_reciter,
                last_played_surah=excluded.last_played_surah,
                last_played_reciter=excluded.last_played_reciter,
                username=excluded.username,
                reminder_time=excluded.reminder_time,
                tz_offset=excluded.tz_offset,
                first_seen=COALESCE(users.first_seen, excluded.first_seen),
                last_seen=excluded.last_seen
            """,
            (
                user_id,
                language,
                default_reciter,
                last_played.get("surah") if last_played else None,
                last_played.get("reciter") if last_played else None,
                username,
                reminder_time,
                tz_offset,
                first_seen,
                last_seen
            )
        )
        conn.execute(
            """
            INSERT INTO user_stats (user_id, plays, reciters_json)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                plays=excluded.plays,
                reciters_json=excluded.reciters_json
            """,
            (
                user_id,
                stats.get("plays", 0),
                json.dumps(stats.get("reciters", {}), ensure_ascii=True)
            )
        )
        conn.execute("DELETE FROM favorites WHERE user_id = ?", (user_id,))
        for category, items in favorites.items():
            for surah_num in items:
                conn.execute(
                    "INSERT OR IGNORE INTO favorites (user_id, category, surah_num) VALUES (?, ?, ?)",
                    (user_id, category, surah_num)
                )
        conn.commit()


def migrate_json_to_db(state_json):
    try:
        with open(state_json, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except Exception as exc:
        logger.error("Failed to read JSON state: %s", exc)
        return

    users = set(data.get("users", []))
    users.update(int(uid) for uid in data.get("languages", {}).keys())
    users.update(int(uid) for uid in data.get("favorites", {}).keys())
    users.update(int(uid) for uid in data.get("default_reciters", {}).keys())
    users.update(int(uid) for uid in data.get("last_played", {}).keys())
    users.update(int(uid) for uid in data.get("user_stats", {}).keys())

    for user_id in users:
        uid = str(user_id)
        language = data.get("languages", {}).get(uid, "en")
        default_reciter = data.get("default_reciters", {}).get(uid, "r01")
        last_played = data.get("last_played", {}).get(uid) or {}
        stats = data.get("user_stats", {}).get(uid) or {"plays": 0, "reciters": {}}
        favorites = data.get("favorites", {}).get(uid) or {"Default": []}

        if isinstance(favorites, list):
            favorites = {"Default": favorites}
        favorites = {cat: set(items) for cat, items in favorites.items()}

        save_user_state_to_db(user_id, language, default_reciter, last_played, stats, favorites)


def record_activity(user_id, activity_date):
    with get_conn() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO user_activity (user_id, activity_date) VALUES (?, ?)",
            (user_id, activity_date)
        )
        conn.commit()


def touch_user(user_id, username, language, default_reciter, reminder_time, tz_offset, last_seen):
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO users (
                user_id,
                username,
                language,
                default_reciter,
                reminder_time,
                tz_offset,
                first_seen,
                last_seen
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username=COALESCE(excluded.username, users.username),
                language=COALESCE(excluded.language, users.language),
                default_reciter=COALESCE(excluded.default_reciter, users.default_reciter),
                reminder_time=COALESCE(excluded.reminder_time, users.reminder_time),
                tz_offset=COALESCE(excluded.tz_offset, users.tz_offset),
                first_seen=COALESCE(users.first_seen, excluded.first_seen),
                last_seen=excluded.last_seen
            """,
            (
                user_id,
                username,
                language,
                default_reciter,
                reminder_time,
                tz_offset,
                last_seen,
                last_seen
            )
        )
        conn.commit()


def increment_surah_play(surah_num):
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO surah_stats (surah_num, plays)
            VALUES (?, 1)
            ON CONFLICT(surah_num) DO UPDATE SET
                plays=surah_stats.plays + 1
            """,
            (surah_num,)
        )
        conn.commit()


def save_feedback(user_id, username, message, created_at):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO feedback (user_id, username, message, created_at) VALUES (?, ?, ?, ?)",
            (user_id, username, message, created_at)
        )
        conn.commit()


def get_daily_active(activity_date):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT COUNT(DISTINCT user_id) FROM user_activity WHERE activity_date = ?",
            (activity_date,)
        ).fetchone()
        return row[0] if row else 0


def get_cohort_size(first_seen_date):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT COUNT(*) FROM users WHERE first_seen = ?",
            (first_seen_date,)
        ).fetchone()
        return row[0] if row else 0


def get_retained_users(first_seen_date, activity_date):
    with get_conn() as conn:
        row = conn.execute(
            """
            SELECT COUNT(DISTINCT ua.user_id)
            FROM user_activity ua
            JOIN users u ON u.user_id = ua.user_id
            WHERE u.first_seen = ? AND ua.activity_date = ?
            """,
            (first_seen_date, activity_date)
        ).fetchone()
        return row[0] if row else 0


def get_language_breakdown():
    with get_conn() as conn:
        return conn.execute(
            "SELECT language, COUNT(*) FROM users GROUP BY language"
        ).fetchall()


def get_top_surahs(limit=5):
    with get_conn() as conn:
        return conn.execute(
            "SELECT surah_num, plays FROM surah_stats ORDER BY plays DESC LIMIT ?",
            (limit,)
        ).fetchall()
