from datetime import datetime, time, timedelta, timezone
import random
from core.config import AYAH_OF_THE_DAY, REMINDER_GLOBAL_TIME, REMINDER_TZ_BY_LANG
from core.i18n import t
from core.ramadan import is_ramadan
from core.state import USER_LANG, USERS


async def send_daily_reminder(context):
    job = context.job
    chat_id = job.data.get("chat_id")
    if not chat_id:
        return
    ayah_ar, ayah_en, ref = random.choice(AYAH_OF_THE_DAY)
    lang = USER_LANG[chat_id]
    tz_offset = REMINDER_TZ_BY_LANG.get(lang, 0)
    user_now = datetime.now(timezone(timedelta(minutes=tz_offset)))
    today = user_now.date()
    is_friday = user_now.weekday() == 4
    ramadan_today = is_ramadan(today)
    try:
        if ramadan_today and is_friday:
            text = t("ramadan_friday_reminder", lang)
        elif ramadan_today:
            text = t("ramadan_reminder", lang)
        elif is_friday:
            text = t("friday_reminder", lang)
        else:
            text = t("daily_reminder", lang, ayah_ar=ayah_ar, ayah_en=ayah_en, ref=ref)
        await context.bot.send_message(chat_id, text, parse_mode="Markdown")
    except Exception:
        pass


def schedule_user_reminder(job_queue, chat_id):
    time_str = REMINDER_GLOBAL_TIME
    lang = USER_LANG[chat_id]
    try:
        hour, minute = [int(part) for part in time_str.split(":", 1)]
    except ValueError:
        hour, minute = 6, 30
    tz_offset = REMINDER_TZ_BY_LANG.get(lang, 0)
    tz = timezone(timedelta(minutes=tz_offset))
    run_time = time(hour=hour, minute=minute, tzinfo=tz)
    job_name = f"reminder_{chat_id}"
    for job in job_queue.get_jobs_by_name(job_name):
        job.schedule_removal()
    job_queue.run_daily(
        send_daily_reminder,
        time=run_time,
        name=job_name,
        data={"chat_id": chat_id}
    )


def schedule_all_reminders(job_queue):
    for chat_id in USERS:
        schedule_user_reminder(job_queue, chat_id)
