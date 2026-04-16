"""
Daily scheduler — keeps running and triggers run.py at the configured UTC time.

By default, sends a PREVIEW email for approval instead of publishing directly.
After receiving the preview, approve by running:
  python run.py --publish

Usage:
  python scheduler.py               # daily preview emails (recommended)
  python scheduler.py --auto-post   # daily auto-publish (no approval)

Keep this running in the background (Task Scheduler, screen, or as a service).
"""

import sys
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import config
import run
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

AUTO_POST = "--auto-post" in sys.argv


def job():
    try:
        if AUTO_POST:
            logging.info("Auto-posting mode: generating and publishing...")
            run.run(preview=False)
        else:
            logging.info("Preview mode: generating and sending email for approval...")
            run.run(preview=True)
    except Exception as e:
        logging.error(f"Daily run failed: {e}", exc_info=True)


if __name__ == "__main__":
    mode = "AUTO-POST" if AUTO_POST else "PREVIEW (email approval)"
    scheduler = BlockingScheduler(timezone="UTC")
    scheduler.add_job(
        job,
        trigger=CronTrigger(hour=config.POST_HOUR_UTC, minute=config.POST_MINUTE_UTC),
        id="daily_claudeprofessor",
        name="Daily @claudeprofessor post",
        replace_existing=True,
    )
    logging.info(
        f"Scheduler started [{mode}]. Will run daily at "
        f"{config.POST_HOUR_UTC:02d}:{config.POST_MINUTE_UTC:02d} UTC"
    )
    scheduler.start()
