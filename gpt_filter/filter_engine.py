# passive-radar/gpt_filter/filter_engine.py

import os
import time
from dotenv import load_dotenv
from pymongo import MongoClient
from openai import OpenAI

# .env dosyasını yükle
load_dotenv()

# OpenAI istemcisi
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# MongoDB bağlantısı
mongo_uri = os.getenv("MONGO_URI")
mongo_client = MongoClient(mongo_uri)
db = mongo_client["passive-radar"]
collection = db["reddit_posts"]

# GPT prompt şablonu
PROMPT_TEMPLATE = """
Aşağıdaki başlık ve içerikte kişi yazılım, web sitesi, mobil uygulama, yapay zekâ entegrasyonu gibi hizmet ihtiyaçlarını mı dile getiriyor?  
Sadece "EVET" ya da "HAYIR" olarak cevap ver.

Başlık: {title}

İçerik: {text}
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
            return "HATA"
    except Exception as e:
        print(f"⚠️ GPT hatası: {e}")
        return "HATA"

def filter_posts():
    # Sadece daha önce işlenmemiş postları seç
    posts = collection.find({ "is_relevant": { "$exists": False } })

    for post in posts:
        title = post.get("title", "")
        text = post.get("selftext", "")

        result = ask_gpt(title, text)
        print(f"[{result}] {title[:60]}")

        if result in ["EVET", "HAYIR"]:
            collection.update_one(
                { "_id": post["_id"] },
                { "$set": { "is_relevant": result == "EVET" } }
            )

        time.sleep(1.2)  # rate limit koruması

if __name__ == "__main__":
    filter_posts()
