# reset_relevance.py

import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# MongoDB bağlantısı
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["passive-radar"]
collection = db["reddit_posts"]

# Tüm dokümanlardaki is_relevant alanını kaldır
result = collection.update_many(
    {},
    { "$unset": { "is_relevant": "" } }
)

print(f"✅ {result.modified_count} dokümandan is_relevant alanı kaldırıldı.")
