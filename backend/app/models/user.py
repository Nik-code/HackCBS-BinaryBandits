from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional
from app.models.obj import ObjectIdField
from bson import ObjectId
from typing import List, Optional

# Address Schema
class Address(BaseModel):
    street: str
    city: str
    state: str
    zipCode: str
    country: str
    coordinates: Optional[str] = None

# Profile Schema
class Profile(BaseModel):
    firstName: str
    lastName: str
    dateOfBirth: datetime
    gender: str
    contactNumber: str
    address: Address

# Preferences Schema
class Preferences(BaseModel):
    language: str
    notificationsEnabled: bool
    darkMode: bool

# User Schema (output for fetching user data)
class User(BaseModel):
    userId: ObjectIdField=Field(...,alias="_id")  # Mapping _id to userId
    email: EmailStr
    passwordHash: str
    createdAt: datetime
    updatedAt: datetime
    profile: Profile
    preferences: Optional[Preferences]=None
    currentDiseases: List[str]

    class Config:
        # Ensure ObjectId is serialized correctly
        json_encoders = {
            ObjectId: str  # Convert ObjectId to string for the response
        }



class CreateUser(BaseModel):
    email: EmailStr
    passwordHash: str
    profile: Profile
    preferences: Optional[Preferences]=None
    currentDiseases: List[str]