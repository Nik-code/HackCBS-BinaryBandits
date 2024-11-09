from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime
from typing import List, Optional
from pydantic import Field
class Education(BaseModel):
    degree: str
    institution: str
    yearOfCompletion: datetime

class Doctor(BaseModel):
    doctorId: str = Field(..., alias="_id")
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
