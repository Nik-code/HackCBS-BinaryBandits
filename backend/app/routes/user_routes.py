from fastapi import APIRouter, HTTPException, status
from app.models.user import User
from app.database import database as db
from bson import ObjectId
from datetime import datetime

user_router = APIRouter()

@user_router.post("/", response_model=User)
async def create_user(user: User):
    user.createdAt = datetime.utcnow()
    user.updatedAt = datetime.utcnow()
    user_dict = user.dict(by_alias=True)
    result = db["users"].insert_one(user_dict)
    user_dict["_id"] = result.inserted_id
    return user_dict

@user_router.get("/{user_id}", response_model=User)
async def get_user(user_id: str):
    user = db["users"].find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**user)

@user_router.put("/{user_id}", response_model=User)
async def update_user(user_id: str, user: User):
    user.updatedAt = datetime.utcnow()
    user_dict = user.dict(by_alias=True, exclude_unset=True)
    result = db["users"].update_one({"_id": ObjectId(user_id)}, {"$set": user_dict})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = db["users"].find_one({"_id": ObjectId(user_id)})
    return User(**updated_user)

@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    result = db["users"].delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return None
