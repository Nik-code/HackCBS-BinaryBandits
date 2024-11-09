# # app/models.py
# from typing import Optional
# from bson import ObjectId
# from pydantic import BaseModel, Field

# class PyObjectId(ObjectId):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate

#     @classmethod
#     def validate(cls, v, values=None, **kwargs):  # Add additional parameters
#         if not ObjectId.is_valid(v):
#             raise ValueError("Invalid ObjectId")
#         return ObjectId(v)

#     # @classmethod
#     # def __get_pydantic_json_schema__(cls, field_schema):
#     #     field_schema.update(type="string")


from pydantic import BaseModel, Field, EmailStr, constr
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

# Helper for ObjectId compatibility with Pydantic
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)



class ItemModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: Optional[str] = None

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True


# USER MODEL
class Address(BaseModel):
    street: str
    city: str
    state: str
    zipCode: str
    country: str
    coordinates: str

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
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr
    passwordHash: str
    createdAt: datetime
    updatedAt: datetime
    profile: Profile
    preferences: Preferences

# MESSAGE MODEL
class Message(BaseModel):
    sentBy: PyObjectId
    text: str
    sent_at: datetime

# SYMPTOM ANALYSIS MODEL
class SymptomAnalysis(BaseModel):
    chatId: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    userId: PyObjectId
    chatTranscript: List[Message]
    diagnosedDisease: List[str]
    preventionTips: List[str]
    summary: str
    timestamp: datetime

# DOCTOR MODEL
class Education(BaseModel):
    degree: str
    institution: str
    yearOfCompletion: datetime

class Doctor(BaseModel):
    userId: PyObjectId
    specialization: str
    yearsOfExperience: int
    education: List[Education]
    name: str
    email: EmailStr
    passwordHash: str
    username: str
    address: Address
    website: Optional[str] = None
    rating: float
    consultation_fees: float
    availableSlots: List[dict]

# HOSPITAL MODEL
class Hospital(BaseModel):
    hospitalId: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    address: Address
    contactNumber: str
    specializations: List[str]
    rating: float
    website: Optional[str] = None

# LAB MODEL
class LabTest(BaseModel):
    name: str
    cost: float
    availability: bool
    type: str

class Lab(BaseModel):
    labId: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    labName: str
    labAddress: str
    contactNumber: str
    testsAvailable: List[LabTest]

# APPOINTMENT MODEL
class Prescription(BaseModel):
    diagnostics: Optional[str] = None
    tests: Optional[str] = None
    medication: Optional[str] = None

class Appointment(BaseModel):
    appointmentId: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    userId: PyObjectId
    doctorId: PyObjectId
    scheduledDate: datetime
    status: str
    patientSummary: str
    createdAt: datetime
    updatedAt: datetime
    prescription: Optional[Prescription] = None

# PATIENT HISTORY MODEL
class DiagnosisRecord(BaseModel):
    disease: str
    diagnosedBy: str
    diagnosisDate: datetime
    treatment: Optional[str] = None

class PatientHistory(BaseModel):
    historyId: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    userId: PyObjectId
    diagnosisHistory: List[DiagnosisRecord]
    timestamp: datetime

# NOTIFICATION MODEL
class DiseaseOutbreakNotification(BaseModel):
    notificationId: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    location: str
    symptoms: List[str]
    probabilityOfOutbreak: float
    affectedArea: str
    timestamp: datetime

# COMMUNITY SUPPORT MODEL
class NearbyUser(BaseModel):
    userId: PyObjectId
    distance: float

class CommunitySupport(BaseModel):
    communityId: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    disease: str
    nearbyUsers: List[NearbyUser]
    createdAt: datetime

# USER NOTIFICATION MODEL
class Notification(BaseModel):
    notificationId: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    userId: PyObjectId
    message: str
    type: str
    isRead: bool
    timestamp: datetime

