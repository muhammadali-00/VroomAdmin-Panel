from fastapi import APIRouter, HTTPException
from firebase_admin import firestore
from datetime import datetime
import uuid
from pydantic import BaseModel


router = APIRouter()
db = firestore.client()

collection_name = "payments"

@router.get("/")
def get_all_payments():
    docs = db.collection(collection_name).stream()
    return [dict(doc.to_dict(), id=doc.id) for doc in docs]


@router.get("/{payments_id}")
def get_payments(payments_id: str):
    doc = db.collection(collection_name).document(payments_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="payment not found")
    return doc.to_dict()

@router.post("/")
def create_payments(payments: dict):
    payments_id = str(uuid.uuid4())
    payments["payments_id"] = payments_id
    payments["created_at"] = datetime.utcnow()

    # Ensure nested fields are properly formatted
    payments.setdefault("driver", '')
    payments.setdefault("amount", 0)
    payments.setdefault("commission", 0)
    payments.setdefault("payoutStatus", "pending")
    payments.setdefault("rideID", "")


    db.collection(collection_name).document(payments_id).set(payments)
    return {"id": payments_id   , "message": "payments created successfully"}