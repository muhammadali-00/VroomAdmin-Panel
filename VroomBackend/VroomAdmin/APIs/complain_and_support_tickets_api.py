from fastapi import APIRouter, HTTPException
from firebase_admin import firestore
from datetime import datetime
import uuid
from pydantic import BaseModel


router = APIRouter()
db = firestore.client()

collection_name = "complainandSupportTickets"

@router.get("/")
def get_all_complainandSupportTickets():
    docs = db.collection(collection_name).stream()
    return [dict(doc.to_dict(), id=doc.id) for doc in docs]


@router.post("/")
def create_complainandSupportTickets(complainandSupportTickets: dict):
    complainandSupportTickets_id = str(uuid.uuid4())
    complainandSupportTickets["id"] = complainandSupportTickets_id
    complainandSupportTickets["created_at"] = datetime.utcnow()

    # Ensure nested fields are properly formatted
    complainandSupportTickets.setdefault("status", "")
    complainandSupportTickets.setdefault("date", "")
    complainandSupportTickets.setdefault("subject", "")
    complainandSupportTickets.setdefault("submittedBy", "")
    complainandSupportTickets.setdefault("ticketDetail", "")
    complainandSupportTickets.setdefault("type", "")
    db.collection(collection_name).document(complainandSupportTickets_id).set(complainandSupportTickets)
    return {"id": complainandSupportTickets_id, "message": "complainandSupportTickets created successfully"}