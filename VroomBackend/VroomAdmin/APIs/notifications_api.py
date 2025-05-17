from fastapi import APIRouter, HTTPException
from firebase_admin import firestore
from datetime import datetime
import uuid
from pydantic import BaseModel


router = APIRouter()
db = firestore.client()

collection_name = "notifications"

@router.get("/")
def get_all_notifications():
    docs = db.collection(collection_name).stream()
    return [dict(doc.to_dict(), id=doc.id) for doc in docs]


@router.post("/")
def create_notifications(notifications: dict):
    notifications_id = str(uuid.uuid4())
    notifications["id"] = notifications_id
    notifications["created_at"] = datetime.utcnow()

    # Ensure nested fields are properly formatted
    notifications.setdefault("Title", "")
    notifications.setdefault("attachment", "")
    notifications.setdefault("message", "")
    notifications.setdefault("sendTo", "")
    notifications.setdefault("sentOn", "")
    notifications.setdefault("status", "")
    notifications.setdefault("type", "")
    db.collection(collection_name).document(notifications_id).set(notifications)
    return {"id": notifications_id, "message": "notifications created successfully"}