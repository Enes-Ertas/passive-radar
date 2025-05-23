# scheduler.py

from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

# Import functions from your modules
from scraper.reddit_scraper import fetch_and_store_posts
from gpt_filter.filter_engine import filter_posts

def job_cycle():
    start = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{start}] ▶ Starting: Reddit → Filter")

    try:
        # 1) Reddit scraper
        fetch_and_store_posts()
    except Exception as e:
        print(f"⚠️ Reddit scraper error: {e}")

    try:
        # 2) GPT filtreleme
        filter_posts()
    except Exception as e:
        print(f"⚠️ Filtering error: {e}")

    end = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{end}] ✅ Cycle completed.\n")

if __name__ == "__main__":
    sched = BlockingScheduler(timezone="UTC")
    # Her saat başı, dakikası 00'de çalıştır
    sched.add_job(job_cycle, 'cron', minute=0)

    print("🕓 Scheduler started. It will run every hour.")
    sched.start()
