from fastapi import APIRouter, HTTPException
from firebase_admin import firestore
from datetime import datetime
import uuid
from pydantic import BaseModel


router = APIRouter()
db = firestore.client()

collection_name = "riders"

class Rider(BaseModel):
    email : str
    phone : str
    actions : str
    joinedDate : str
    riderName : str
    totalRides : int


@router.get("/")
def get_all_riders():
    docs = db.collection(collection_name).stream()
    return [dict(doc.to_dict(), id=doc.id) for doc in docs]

@router.get("/{rider_id}")
def get_rider(rider_id: str):
    doc = db.collection(collection_name).document(rider_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Rider not found")
    return doc.to_dict()

@router.post("/")
def create_driver(rider: dict):

    rider_id = str(uuid.uuid4())
    rider["driverID"] = rider_id
    rider["created_at"] = datetime.utcnow()

    rider.setdefault("Email", {})
    rider.setdefault("Phone", {})
    rider.setdefault("actions", "pending")
    rider.setdefault("joinedDate", {})
    rider.setdefault("riderName", {})
    rider.setdefault("totalRides",{"balance": 0})

    db.collection(collection_name).document(rider_id).set(rider)
    return {"id": rider_id, "message": "Driver created successfully"}