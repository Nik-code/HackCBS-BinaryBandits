from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional
from app.models.obj import ObjectIdField
from bson import ObjectId

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
    _id: ObjectIdField  # Mapping _id to userId
    email: EmailStr
    passwordHash: str
    createdAt: datetime
    updatedAt: datetime
    profile: Profile
    preferences: Preferences

    class Config:
        # Ensure ObjectId is serialized correctly
        json_encoders = {
            ObjectId: str  # Convert ObjectId to string for the response
        }

# User In Create Schema (for registration)
class UserInCreate(BaseModel):
    email: EmailStr
    password: str
    profile: Profile
    preferences: Preferences

# Token Schema (for JWT)
class Token(BaseModel):
    access_token: str
    token_type: str


class CreateUser(BaseModel):
    email: str
    passwordHash: str
    profile: Profile
    preferences: Preferences

class GetUser(BaseModel):
    _id: str  # Mapping _id to userId
    email: EmailStr
    createdAt: datetime
    updatedAt: datetime
    profile: Profile
    preferences: Preferences

    # class Config:
    #     json_encoders = {
    #         ObjectId: str
    #     }
