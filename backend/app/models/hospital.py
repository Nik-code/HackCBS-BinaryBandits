from pydantic import BaseModel, Field
from typing import List, Optional

class HospitalAddress(BaseModel):
    street: str
    city: str
    state: str
    zipCode: str
    country: str
    coordinates: Optional[str] = None

class Hospital(BaseModel):
    hospitalId: str = Field(..., alias="_id")  # Use MongoDB's ObjectId as ID
    name: str
    address: HospitalAddress
    contactNumber: str
    specializations: List[str]
    rating: Optional[float] = None
    website: Optional[str] = None
