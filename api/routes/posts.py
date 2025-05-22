# routes/posts.py

from fastapi import APIRouter
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
from typing import Optional, Any, Dict, List
from datetime import datetime
import os

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
        {"$set": {"is_read": True, "last_viewed_at": datetime.utcnow()}}
    )
    return {"modified_count": result.modified_count}


@router.patch("/{post_id}/favorite")
def mark_as_favorite(post_id: str):
    result = collection.update_one(
        {"_id": ObjectId(post_id)},
        {"$set": {"is_favorite": True, "last_viewed_at": datetime.utcnow()}}
    )
    return {"modified_count": result.modified_count}


@router.patch("/{post_id}/irrelevant")
def mark_as_negative(post_id: str):
    result = collection.update_one(
        {"_id": ObjectId(post_id)},
        {"$set": {"is_negative": True, "last_viewed_at": datetime.utcnow()}}
    )
    return {"modified_count": result.modified_count}


@router.get("/")
def get_posts(
    view: Optional[str] = "unread",
    tags: Optional[str] = None,
    skip: int = 0,
    limit: int = 50
) -> List[Dict[str, Any]]:
    # biriktirilecek filtreler
    filter_query: Dict[str, Any] = {}
    tag_clause: Optional[Dict[str, Any]] = None

    # etiket filtresi hazırla
    if tags:
        tag_list = [t.strip().lower() for t in tags.split(",") if t.strip()]
        or_terms = []
        for tag in tag_list:
            or_terms.append({"title": {"$regex": tag, "$options": "i"}})
            or_terms.append({"selftext": {"$regex": tag, "$options": "i"}})
        if or_terms:
            tag_clause = {"$or": or_terms}

    # view'e göre koşulları belirle
    if view == "unread":
        clauses = [
            {"$or": [
                {"is_read": {"$exists": False}},
                {"is_read": False}
            ]},
            {"is_relevant": True},
            {"is_negative": {"$ne": True}},
            {"is_favorite": {"$ne": True}}
        ]
        if tag_clause:
            clauses.append(tag_clause)
        filter_query = {"$and": clauses}

    elif view == "read":
        clauses = [
            {"is_read": True},
            {"is_relevant": True},
            {"is_negative": {"$ne": True}}
        ]
        if tag_clause:
            clauses.append(tag_clause)
        filter_query = {"$and": clauses}

    elif view == "favorite":
        clauses = [
            {"is_favorite": True},
            {"is_relevant": True}
        ]
        if tag_clause:
            clauses.append(tag_clause)
        filter_query = {"$and": clauses}

    elif view == "rejected":
        # reddedilenler: is_relevant = False
        filter_query = {"is_negative": True}
        if tag_clause:
            filter_query = {"$and": [filter_query, tag_clause]}

    elif view == "recent":
        # son etkileşimde bulunanlar
        recent_filter = {
            "$or": [
                {"is_read": True},
                {"is_favorite": True},
                {"is_relevant": False}
            ]
        }
        if tag_clause:
            filter_query = {"$and": [recent_filter, tag_clause]}
        else:
            filter_query = recent_filter

    else:
        # default: sadece ilgili postlar
        filter_query = {"is_relevant": True}
        if tag_clause:
            filter_query = {"$and": [filter_query, tag_clause]}

    # MongoDB sorgusu
    cursor = collection.find(filter_query)

    # sıralama
    if view == "recent":
        cursor = cursor.sort("last_viewed_at", -1)
    else:
        cursor = cursor.sort("created", -1)

    # pagination
    cursor = cursor.skip(skip).limit(limit)

    # sonuçları hazırla
    posts = []
    for doc in cursor:
        posts.append({
            "_id": str(doc["_id"]),
            "title": doc.get("title", ""),
            "selftext": doc.get("selftext", ""),
            "subreddit": doc.get("subreddit", ""),
            "permalink": doc.get("permalink", ""),
            "source": "reddit",
            "created": (doc.get("created").isoformat()
                        if hasattr(doc.get("created"), "isoformat") else doc.get("created", "")),
            "last_viewed_at": (doc.get("last_viewed_at").isoformat()
                               if doc.get("last_viewed_at") else None),
            "is_read": doc.get("is_read", False),
            "is_favorite": doc.get("is_favorite", False),
            "is_relevant": doc.get("is_relevant", True),
        })

    return posts
