# passive-radar/gpt_filter/filter_engine.py

import os
import time
from dotenv import load_dotenv
from pymongo import MongoClient
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# MongoDB connection
mongo_uri = os.getenv("MONGO_URI")
mongo_client = MongoClient(mongo_uri)
db = mongo_client["passive-radar"]
collection = db["reddit_posts"]

# GPT prompt template
PROMPT_TEMPLATE = """
You are a bot that only flags actual job offers or developer hiring requests.
Answer YES **only** if the post is explicitly **asking for** or **offering** paid developer work (e.g. “hiring a developer”, “for hire: React engineer”, "freelancer needed", “looking for backend help”).  
Answer NO for any non-technical or sales/marketing/administrative roles and any personal project announcements, showcases, questions.

Title: {title}
Content: {text}
"""


def ask_gpt(title, text):
    prompt = PROMPT_TEMPLATE.format(title=title, text=text)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        message = response.choices[0].message.content
        if message:
            return message.strip().upper()
        else:
            return "ERROR"
    except Exception as e:
        print(f"⚠️ GPT error: {e}")
        return "ERROR"

def filter_posts():
    # Select only posts that haven't been processed before
    posts = collection.find({ "is_relevant": { "$exists": False } })

    for post in posts:
        title = post.get("title", "")
        text = post.get("selftext", "")

        result = ask_gpt(title, text)
        print(f"[{result}] {title[:60]}")

        if result in ["YES", "NO"]:
            collection.update_one(
                { "_id": post["_id"] },
                { "$set": { "is_relevant": result == "YES" } }
            )

        time.sleep(1.2)  # rate limit protection

if __name__ == "__main__":
    filter_posts()
