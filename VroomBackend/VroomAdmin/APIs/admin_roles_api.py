from fastapi import APIRouter, HTTPException
from firebase_admin import firestore
from datetime import datetime
import uuid
from pydantic import BaseModel


adminroles_router = APIRouter()
db = firestore.client()

collection_name = "adminRoles"

class AdminRole(BaseModel):
    roleID: str
    permissions: str
    roleName: str


@adminroles_router.get("/")
def get_all_adminroles():
    docs = db.collection(collection_name).stream()
    return [dict(doc.to_dict(), id=doc.id) for doc in docs]

@adminroles_router.get("/{role_id}")
def get_admin_role(role_id: str):
    doc = db.collection(collection_name).document(role_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Admin not found")
    return doc.to_dict()



@adminroles_router.post("/adminRoles")
async def create_admin_role(adminrole : dict):
    role_id = str(uuid.uuid4())
    adminrole["roleID"] = role_id
    adminrole["created_at"] = datetime.utcnow()

    # Ensure nested fields are properly formatted
    adminrole.setdefault("permissions", {})
    adminrole.setdefault("roleName", {})

    db.collection(collection_name).document(role_id).set(adminrole)
    return {"id": role_id, "message": "Driver created successfully"}

@adminroles_router.put("/{driver_id}")
def update_admin_role(role_id: str, updates: dict):
    doc_ref = db.collection(collection_name).document(role_id)
    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="Driver not found")
    doc_ref.update(updates)
    return {"message": "AdminRole updated successfully"}

@adminroles_router.delete("/{driver_id}")
def delete_admin_role(role_id: str):
    doc_ref = db.collection(collection_name).document(role_id)
    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="Driver not found")
    doc_ref.delete()
    return {"message": "Admin deleted successfully"}

