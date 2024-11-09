from pydantic import BaseModel, Field
from typing import List, Optional
from app.models.obj import ObjectIdField
from bson import ObjectId

class HospitalAddress(BaseModel):
    street: str
    city: str
    state: str
    zipCode: str
    country: str
    coordinates: Optional[str] = None

class Hospital(BaseModel):
    hospitalId: ObjectIdField = Field(..., alias="_id")  # Use MongoDB's ObjectId as ID
    name: str
    address: HospitalAddress
    contactNumber: str
    specializations: List[str]
    rating: Optional[float] = None
    website: Optional[str] = None

    class Config:
        # Ensure ObjectId is serialized correctly
        json_encoders = {
            ObjectId: str  # Convert ObjectId to string for the response
        }


class CreateHospital(BaseModel):
    name: str
    address: HospitalAddress
    contactNumber: str
    specializations: List[str]
    rating: Optional[float] = None
    website: Optional[str] = None