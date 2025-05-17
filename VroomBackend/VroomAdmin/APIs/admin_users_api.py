from fastapi import APIRouter, HTTPException
from firebase_admin import firestore
from datetime import datetime
import uuid
from pydantic import BaseModel


router = APIRouter()
db = firestore.client()

collection_name = "adminUsers"

class AdminUser(BaseModel):
    email: str
    name: str
    role: str
    status: str


@router.get("/")
def get_all_adminusers():
    docs = db.collection(collection_name).stream()
    return [dict(doc.to_dict(), id=doc.id) for doc in docs]

