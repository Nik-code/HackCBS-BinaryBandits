from pydantic import BaseModel, Field
from typing import List, Optional
from app.models.obj import ObjectIdField
from bson import ObjectId


class Test(BaseModel):
    name: str
    cost: float
    availability: bool
    type: str

class Lab(BaseModel):
    labId: ObjectIdField = Field(..., alias="_id")  # MongoDB ObjectId
    labName: str
    labAddress: str
    contactNumber: str
    testsAvailable: List[Test]
    class Config:
        # Ensure ObjectId is serialized correctly
        json_encoders = {
            ObjectId: str  # Convert ObjectId to string for the response
        }

class CreateLab(BaseModel):
    labName: str
    labAddress: str
    contactNumber: str
    testsAvailable: List[Test]
