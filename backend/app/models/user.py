from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional, List

class Address(BaseModel):
    street: str
    city: str
    state: str
    zipCode: str
    country: str
    coordinates: Optional[str] = None

class Profile(BaseModel):
    firstName: str
    lastName: str
    dateOfBirth: datetime
    gender: str
    contactNumber: str
    address: Address

class Preferences(BaseModel):
    language: str
    notificationsEnabled: bool
    darkMode: bool

class User(BaseModel):
    userId:str = Field(..., alias="_id") 
    email: EmailStr
    passwordHash: str
    createdAt: datetime
    updatedAt: datetime
    profile: Profile
    preferences: Preferences
