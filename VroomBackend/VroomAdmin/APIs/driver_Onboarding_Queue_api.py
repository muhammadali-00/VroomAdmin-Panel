from fastapi import APIRouter, HTTPException
from firebase_admin import firestore
from datetime import datetime
import uuid
from pydantic import BaseModel


router = APIRouter()
db = firestore.client()

collection_name = "driverOnboardingQueue"

@router.get("/")
def get_all_driverOnboardingQueue():
    docs = db.collection(collection_name).stream()
    return [dict(doc.to_dict(), id=doc.id) for doc in docs]

@router.post("/")
def create_driverOnboardingQueue(driverOnboardingQueue: dict):
    driverOnboardingQueue_id = str(uuid.uuid4())
    driverOnboardingQueue["id"] = driverOnboardingQueue_id
    driverOnboardingQueue["created_at"] = datetime.utcnow()

    # Ensure nested fields are properly formatted
    driverOnboardingQueue.setdefault("CNIC", "")
    driverOnboardingQueue.setdefault("appliedOn", "")
    driverOnboardingQueue.setdefault("message", "")
    driverOnboardingQueue.setdefault("backgroundCheck", "")
    driverOnboardingQueue.setdefault("docStatus", "")
    driverOnboardingQueue.setdefault("status", "")
    driverOnboardingQueue.setdefault("driverName", "")
    driverOnboardingQueue.setdefault("insurance", "")
    driverOnboardingQueue.setdefault("license", "")
    driverOnboardingQueue.setdefault("vehiclePapers", "")

    db.collection(collection_name).document(driverOnboardingQueue_id).set(driverOnboardingQueue)
    return {"id": driverOnboardingQueue_id, "message": "driverOnboardingQueue created successfully"}