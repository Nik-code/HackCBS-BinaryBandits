from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from typing import List, Optional

class Prescription(BaseModel):
    diagnostics: Optional[str] = None
    tests: Optional[List[str]] = None
    medication: Optional[List[str]] = None

class Appointment(BaseModel):
    appointmentId: str = Field(..., alias="_id")  # MongoDB ObjectId
    userId: str  # Foreign key to User.userId (patient)
    doctorId: str  # Foreign key to User.userId (doctor)
    scheduledDate: datetime
    status: str  # e.g., "scheduled", "completed", "canceled"
    patientSummary: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime
    prescription: Optional[Prescription] = None
