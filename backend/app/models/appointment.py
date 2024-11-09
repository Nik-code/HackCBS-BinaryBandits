from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from typing import List, Optional
from app.models.obj import ObjectIdField
from bson import ObjectId

class Prescription(BaseModel):
    diagnostics: Optional[str] = None
    tests: Optional[List[str]] = None
    medication: Optional[List[str]] = None

class Appointment(BaseModel):
    appointmentId: ObjectIdField = Field(..., alias="_id")  # MongoDB ObjectId
    userId: ObjectIdField  # Foreign key to User.userId (patient)
    doctorId: ObjectIdField  # Foreign key to User.userId (doctor)
    scheduledDate: datetime
    status: str  # e.g., "scheduled", "completed", "canceled"
    patientSummary: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime
    prescription: Optional[Prescription] = None

    class Config:
        # Ensure ObjectId is serialized correctly
        json_encoders = {
            ObjectId: str  # Convert ObjectId to string for the response
        }


class CreateAppointment(BaseModel):
    userId: ObjectIdField  # Foreign key to User.userId (patient)
    doctorId: ObjectIdField  # Foreign key to User.userId (doctor)
    scheduledDate: datetime
    status: str  # e.g., "scheduled", "completed", "canceled"
    patientSummary: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime
    prescription: Optional[Prescription] = None

    class Config:
        # Ensure ObjectId is serialized correctly
        json_encoders = {
            ObjectId: str  # Convert ObjectId to string for the response
        }