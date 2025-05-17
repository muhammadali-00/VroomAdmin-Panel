from fastapi import APIRouter, HTTPException
from firebase_admin import firestore
from datetime import datetime
import uuid
from pydantic import BaseModel


router = APIRouter()
db = firestore.client()

collection_name = "promotions"

@router.get("/")
def get_all_promotions():
    docs = db.collection(collection_name).stream()
    return [dict(doc.to_dict(), id=doc.id) for doc in docs]

@router.post("/")
def create_driver(promotions: dict):
    promotions_id = str(uuid.uuid4())
    promotions["id"] = promotions_id
    promotions["created_at"] = datetime.utcnow()

    # Ensure nested fields are properly formatted
    promotions.setdefault("discointType", "")
    promotions.setdefault("expiry", "")
    promotions.setdefault("maxDiscount", 0)
    promotions.setdefault("promoCode", "")
    promotions.setdefault("status", "")
    promotions.setdefault("targetAudience", "")
    promotions.setdefault("usageLimit", 0)
    db.collection(collection_name).document(promotions_id).set(promotions)
    return {"id": promotions_id, "message": "promotions created successfully"}