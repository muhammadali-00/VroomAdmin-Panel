from fastapi import APIRouter, HTTPException
from firebase_admin import firestore
from datetime import datetime
import uuid
from pydantic import BaseModel


router = APIRouter()
db = firestore.client()

collection_name = "riderWallet"

class riderWallet(BaseModel):
    balance : int
    lastRecharge : int
    rider : str
    totalTopUps : int


@router.post("/")
def create_riderwallet(riderwallet: dict):
    riderwallet_id = str(uuid.uuid4())
    riderwallet["riderwallet_ID"] = riderwallet_id
    riderwallet["created_at"] = datetime.utcnow()

    # Ensure nested fields are properly formatted
    riderwallet.setdefault("balance", 0)
    riderwallet.setdefault("lastRecharge", 0)
    riderwallet.setdefault("rider", "")
    riderwallet.setdefault("totalTopUps", 0)


    db.collection(collection_name).document(riderwallet_id).set(riderwallet)
    return {"id": riderwallet_id, "message": "riderwallet created successfully"}




@router.get("/")
def get_all_riderwallet():
    docs = db.collection(collection_name).stream()
    return [dict(doc.to_dict(), id=doc.id) for doc in docs]



@router.put("/{riderwallet_id}")
def update_riderwallet_id(riderwallet_id: str, updates: dict):
    doc_ref = db.collection(collection_name).document(riderwallet_id)
    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="riderwallet not found")
    doc_ref.update(updates)
    return {"message": "riderwallet updated successfully"}