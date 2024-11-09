from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional
from bson import ObjectId
import uuid
from app.models.obj import ObjectIdField
    
class Item2(BaseModel):
    _id: ObjectIdField  # We will return _id as a string
    email: str
    passwordHash: str

    class Config:
        # Ensure ObjectId is serialized correctly
        json_encoders = {
            ObjectId: str  # Convert ObjectId to string for the response
        }

class CreateItem2(BaseModel):
    email: str
    passwordHash: str

class GetItem2(BaseModel):
    _id: str  # We will return _id as a string
    email: str
    passwordHash: str

