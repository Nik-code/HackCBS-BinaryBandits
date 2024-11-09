from pydantic import BaseModel, Field
from typing import List, Optional

class Test(BaseModel):
    name: str
    cost: float
    availability: bool
    type: str

class Lab(BaseModel):
    labId: str = Field(..., alias="_id")  # MongoDB ObjectId
    labName: str
    labAddress: str
    contactNumber: str
    testsAvailable: List[Test]
