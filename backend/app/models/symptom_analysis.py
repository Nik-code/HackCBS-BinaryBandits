from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.models.obj import ObjectIdField
from bson import ObjectId

class Message(BaseModel):
    sentBy: str  # Can be "user" or "bot" or similar identifier
    text: str
    sent_at: datetime

class SymptomAnalysis(BaseModel):
    chatId: ObjectIdField = Field(..., alias="_id")  # MongoDB ObjectId
    userId: ObjectIdField  # Foreign key to User.userId
    chatTranscript: List[Message]  # List of messages in the conversation
    diagnosedDisease: List[str]
    preventionTips: List[str]
    summary: str
    timestamp: datetime

    class Config:
        # Ensure ObjectId is serialized correctly
        json_encoders = {
            ObjectId: str  # Convert ObjectId to string for the response
        }

class CreateSymptomAnalysis(BaseModel):  # MongoDB ObjectId
    userId: ObjectIdField  # Foreign key to User.userId
    chatTranscript: List[Message]  # List of messages in the conversation
    diagnosedDisease: List[str]
    preventionTips: List[str]
    summary: str
    timestamp: datetime

    class Config:
        # Ensure ObjectId is serialized correctly
        json_encoders = {
            ObjectId: str  # Convert ObjectId to string for the response
        }