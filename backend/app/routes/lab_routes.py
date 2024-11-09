from fastapi import APIRouter, HTTPException, status
from app.models.lab import Lab,CreateLab
from bson import ObjectId
from app.database import database as db

lab_router = APIRouter()

@lab_router.post("/", response_model=Lab)
async def create_lab(lab: CreateLab):
    lab_dict = lab.dict(by_alias=True)
    result = await db["labs"].insert_one(lab_dict)
    lab_dict["_id"] = result.inserted_id
    return lab_dict

@lab_router.get("/{lab_id}", response_model=Lab)
async def get_lab(lab_id: str):
    lab = await db["labs"].find_one({"_id": ObjectId(lab_id)})
    if lab is None:
        raise HTTPException(status_code=404, detail="Lab not found")
    return Lab(**lab)

@lab_router.put("/{lab_id}", response_model=Lab)
async def update_lab(lab_id: str, lab: CreateLab):
    lab_dict = lab.dict(by_alias=True, exclude_unset=True)
    result = await db["labs"].update_one({"_id": ObjectId(lab_id)}, {"$set": lab_dict})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Lab not found")
    updated_lab = await db["labs"].find_one({"_id": ObjectId(lab_id)})
    return Lab(**updated_lab)

@lab_router.delete("/{lab_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lab(lab_id: str):
    result = await db["labs"].delete_one({"_id": ObjectId(lab_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Lab not found")
    return None
