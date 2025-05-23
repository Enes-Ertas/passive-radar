import praw
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import prawcore

load_dotenv()

# Mongo connection
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

# Subreddit list and time threshold
SUBREDDITS = [

     # GENERAL JOB LISTINGS
    "jobs",                # general job listings
    "jobopenings",         # job opening announcements
    "hiring",              # hiring announcements

    "SideProject", "webdev", "forhire", "startup",
    "reactjs", "remotejs",

    # REMOTE & FREELANCE
    "RemoteWork",          # all remote work listings
    "WorkOnline",          # online job/income opportunities
    "Gigs",                # short-term gigs, gig economy
    "SideHustle",          # side projects, extra earning opportunities

    # TECH & SOFTWARE
    "TechJobs",            # tech industry jobs
    "HireADeveloper",      # developers wanted

    # OTHER
    "digitalnomad",        # digital nomad opportunities
]
SINCE = datetime.utcnow() - timedelta(hours=1)

def fetch_and_store_posts():
    for subreddit in SUBREDDITS:
        print(f"⏳ Subreddit: {subreddit}")
        # prepare: get the generator
        submissions = reddit.subreddit(subreddit).new()
        try:
            # iterate and process submissions here
            for submission in submissions:
                created_utc = datetime.utcfromtimestamp(submission.created_utc)
                if created_utc <= SINCE:
                    break

                post = {
                    "subreddit": subreddit,
                    "title": submission.title,
                    "selftext": submission.selftext,
                    "author": str(submission.author),
                    "created": created_utc,
                    "url": submission.url,
                    "permalink": f"https://reddit.com{submission.permalink}"
                }
                if not collection.find_one({"permalink": post["permalink"]}):
                    collection.insert_one(post)

        except prawcore.exceptions.Forbidden:
            print(f"⚠️ ⚠️ Access restricted, skipping: r/{subreddit}")
            continue
        except Exception as e:
            print(f"⚠️ Unexpected error processing r/{subreddit}: {e}")
            continue

    print("✅ New posts added to MongoDB.")

if __name__ == "__main__":
    fetch_and_store_posts()
