from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime
from typing import List, Optional
from pydantic import Field
from app.models.obj import ObjectIdField
from bson import ObjectId

class Education(BaseModel):
    degree: str
    institution: str
    yearOfCompletion: datetime

class Doctor(BaseModel):
    doctorId: ObjectIdField=Field(..., alias="_id")
    specialization: str
    yearsOfExperience: int
    education: List[Education]
    name: str
    email: EmailStr
    passwordHash: str
    username: str
    address: dict
    website: Optional[str] = None
    rating: float
    consultation_fees: float
    availableSlots: List[dict]

    class Config:
        # Ensure ObjectId is serialized correctly
        json_encoders = {
            ObjectId: str  # Convert ObjectId to string for the response
        }

# CreateDoc Schema (input for creating a new doctor)
class CreateDoc(BaseModel):
    specialization: str
    yearsOfExperience: int
    education: List[Education]
    name: str
    email: EmailStr
    password: str  # Plain password; will be hashed before storing
    username: str
    address: dict
    website: Optional[str] = None
    consultation_fees: float
    availableSlots: List[dict]

# # GetDoc Schema (output for returning doctor data, excluding passwordHash)
# class GetDoc(BaseModel):
#     doctorId: ObjectIdField=Field(..., alias="_id")
#     specialization: str
#     yearsOfExperience: int
#     education: List[Education]
#     name: str
#     email: EmailStr
#     username: str
#     address: dict
#     website: Optional[str] = None
#     rating: Optional[float] = 0.0  # Make rating optional
#     consultation_fees: float
#     availableSlots: List[dict]

#     class Config:
#         json_encoders = {
#             ObjectId: str
#         }