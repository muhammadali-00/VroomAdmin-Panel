from fastapi import APIRouter, HTTPException
from firebase_admin import firestore
from pydantic import BaseModel

router = APIRouter()
db = firestore.client()

collection_name = "transactions"

@router.get("/")
def get_all_transactions():
    docs = db.collection(collection_name).stream()
    return [dict(doc.to_dict(), id=doc.id) for doc in docs]