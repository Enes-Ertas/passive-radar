import praw
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# Mongo bağlantısı
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["passive-radar"]
collection = db["reddit_posts"]

# Reddit API
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "passive-radar-bot")

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# Subreddit listesi ve zaman sınırı
SUBREDDITS = [
    "turkey", "freelance", "girisim", "yazilim",
    "SideProject", "webdev", "forhire", "startup",
    "reactjs", "remotejs"
]
SINCE = datetime.utcnow() - timedelta(days=1)

def fetch_and_store_posts():
    for subreddit in SUBREDDITS:
        print(f"⏳ Subreddit: {subreddit}")
        for submission in reddit.subreddit(subreddit).new(limit=100):
            created_utc = datetime.utcfromtimestamp(submission.created_utc)
            if created_utc > SINCE:
                post = {
                    "subreddit": subreddit,
                    "title": submission.title,
                    "selftext": submission.selftext,
                    "author": str(submission.author),
                    "created": created_utc,
                    "url": submission.url,
                    "permalink": f"https://reddit.com{submission.permalink}"
                }
                # Duplicate kontrolü (aynı permalink varsa ekleme)
                if not collection.find_one({"permalink": post["permalink"]}):
                    collection.insert_one(post)

    print("✅ Yeni gönderiler MongoDB'ye eklendi.")

if __name__ == "__main__":
    fetch_and_store_posts()
