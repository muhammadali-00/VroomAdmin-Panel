from fastapi import APIRouter, HTTPException
from firebase_admin import firestore
from datetime import datetime
import uuid
from pydantic import BaseModel


router = APIRouter()
db = firestore.client()

collection_name = "pricingAndZones"

@router.get("/")
def get_all_pricingandzones():
    docs = db.collection(collection_name).stream()
    return [dict(doc.to_dict(), id=doc.id) for doc in docs]

@router.post("/")
def create_pricingandzones(pricingandzones: dict):
    pricingandzones_id = str(uuid.uuid4())
    pricingandzones["id"] = pricingandzones_id
    pricingandzones["created_at"] = datetime.utcnow()

    # Ensure nested fields are properly formatted
    pricingandzones.setdefault("baseFare", {})
    pricingandzones.setdefault("city", {})
    pricingandzones.setdefault("fare", "pending")
    pricingandzones.setdefault("lastUpdates", {})
    pricingandzones.setdefault("perKM", 0)
    pricingandzones.setdefault("perMinute", 0)
    pricingandzones.setdefault("surgwPricing", 0)
    pricingandzones.setdefault("waitingCharges", 0)
    pricingandzones.setdefault("zoneCoordinates", "")
    pricingandzones.setdefault("zoneName", "")


    db.collection(collection_name).document(pricingandzones_id).set(pricingandzones) # Changed this line
    return {"id": pricingandzones_id, "Pricing and Zone": "pricingandzones created successfully"}


@router.put("/{pricingandzones_id}")
def update_driver(pricingandzones_id: str, updates: dict):
    doc_ref = db.collection(collection_name).document(pricingandzones_id)
    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="Driver not found")
    doc_ref.update(updates)
    return {"message": "Driver updated successfully"}