from fastapi import APIRouter, HTTPException
from firebase_admin import firestore
from datetime import datetime
import uuid
from pydantic import BaseModel


router = APIRouter()
db = firestore.client()

collection_name = "drivers"


@router.get("/")
def get_all_drivers():
    docs = db.collection(collection_name).stream()
    return [dict(doc.to_dict(), id=doc.id) for doc in docs]

@router.get("/{driver_id}")
def get_driver(driver_id: str):
    doc = db.collection(collection_name).document(driver_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Driver not found")
    return doc.to_dict()

@router.post("/")
def create_driver(driver: dict):
    driver_id = str(uuid.uuid4())
    driver["driverID"] = driver_id
    driver["created_at"] = datetime.utcnow()

    # Ensure nested fields are properly formatted
    driver.setdefault("documents", {})
    driver.setdefault("personalInfo", {})
    driver.setdefault("status", "pending")
    driver.setdefault("vehicleInfo", {})
    driver.setdefault("wallet", {"balance": 0})

    db.collection(collection_name).document(driver_id).set(driver)
    return {"id": driver_id, "message": "Driver created successfully"}

@router.put("/{driver_id}")
def update_driver(driver_id: str, updates: dict):
    doc_ref = db.collection(collection_name).document(driver_id)
    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="Driver not found")
    doc_ref.update(updates)
    return {"message": "Driver updated successfully"}

@router.delete("/{driver_id}")
def delete_driver(driver_id: str):
    doc_ref = db.collection(collection_name).document(driver_id)
    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="Driver not found")
    doc_ref.delete()
    return {"message": "Driver deleted successfully"}
