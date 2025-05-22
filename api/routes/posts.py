from fastapi import APIRouter, Query
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
from typing import Optional, List
import os
from datetime import datetime

load_dotenv()

router = APIRouter()

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["passive-radar"]
collection = db["reddit_posts"]

@router.patch("/{post_id}/read")
def mark_as_read(post_id: str):
    result = collection.update_one(
        {"_id": ObjectId(post_id)},
        {"$set": {"is_read": True}}
    )
    return {"modified_count": result.modified_count}

@router.patch("/{post_id}/favorite")
def mark_as_favorite(post_id: str):
    result = collection.update_one(
        {"_id": ObjectId(post_id)},
        {"$set": {"is_favorite": True}}
    )
    return {"modified_count": result.modified_count}

@router.patch("/{post_id}/irrelevant")
def mark_as_irrelevant(post_id: str):
    result = collection.update_one(
        {"_id": ObjectId(post_id)},
        {
            "$set": {
                "is_relevant": False,
                "last_viewed_at": datetime.utcnow()
            }
        }
    )
    return {"modified_count": result.modified_count}

@router.get("/")
def get_posts(
    view: Optional[str] = "unread",
    tags: Optional[str] = None,
    skip: int = 0,
    limit: int = 50
):
    query = {}

    # Klasör bazlı filtreleme
    if view == "unread":
        query["$or"] = [{ "is_read": { "$exists": False } }, { "is_read": False }]
    elif view == "read":
        query["is_read"] = True
    elif view == "favorite":
        query["is_favorite"] = True
    elif view == "rejected":
        query["is_relevant"] = False
    elif view == "recent":
        # Sıralama özel olacak
        pass
    else:
        query["is_relevant"] = True

    # Etiket filtreleme (basit içerik içinde anahtar kelime arama)
    if tags:
        tag_list = [tag.strip().lower() for tag in tags.split(",")]
        regex_conditions = [{"$or": [
            { "title": { "$regex": tag, "$options": "i" } },
            { "selftext": { "$regex": tag, "$options": "i" } }
        ]} for tag in tag_list]
        query["$and"] = regex_conditions if "$and" not in query else query["$and"] + regex_conditions

    # Veriyi getir
    cursor = collection.find(query)

    # Sıralama (recent için last_viewed_at önceliği)
    if view == "recent":
        cursor = cursor.sort("last_viewed_at", -1)
    else:
        cursor = cursor.sort("created", -1)

    # Pagination
    cursor = cursor.skip(skip).limit(limit)

    result = []
    for post in cursor:
        result.append({
            "_id": str(post["_id"]),
            "title": post.get("title", ""),
            "selftext": post.get("selftext", ""),
            "subreddit": post.get("subreddit", ""),
            "permalink": post.get("permalink", ""),
            "created": post.get("created", ""),
            "last_viewed_at": post.get("last_viewed_at", None),
            "is_read": post.get("is_read", False),
            "is_favorite": post.get("is_favorite", False),
        })

    return result
