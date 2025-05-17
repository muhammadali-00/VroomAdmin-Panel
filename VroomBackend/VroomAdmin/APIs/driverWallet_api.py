from fastapi import APIRouter, HTTPException
from firebase_admin import firestore
from datetime import datetime
import uuid
from pydantic import BaseModel


router = APIRouter()
db = firestore.client()

collection_name = "driverWallet"

class driverWallet(BaseModel):
    balance : int
    lastRecharge : int
    rider : str
    totalTopUps : int


@router.post("/")
def create_driverwallet(driverwallet: dict):
    driverwallet_id = str(uuid.uuid4())
    driverwallet["riderwallet_ID"] = driverwallet_id
    driverwallet["created_at"] = datetime.utcnow()

    # Ensure nested fields are properly formatted
    driverwallet.setdefault("balance", 0)
    driverwallet.setdefault("driver", 0)
    driverwallet.setdefault("lastPayout", "")
    driverwallet.setdefault("totalEarnings", 0)


    db.collection(collection_name).document(driverwallet_id).set(driverwallet)
    return {"id": driverwallet_id, "message": "riderwallet created successfully"}




@router.get("/")
def get_all_driverwallet():
    docs = db.collection(collection_name).stream()
    return [dict(doc.to_dict(), id=doc.id) for doc in docs]



@router.put("/{driverwallet_id}")
def update_driverwalletid(driverwallet_id: str, updates: dict):
    doc_ref = db.collection(collection_name).document(riderwallet_id)
    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="driverwallet not found")
    doc_ref.update(updates)
    return {"message": "driverwallet updated successfully"}