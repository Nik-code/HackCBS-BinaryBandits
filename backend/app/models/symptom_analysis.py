from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Message(BaseModel):
    sentBy: str  # Can be "user" or "bot" or similar identifier
    text: str
    sent_at: datetime

class SymptomAnalysis(BaseModel):
    chatId: str = Field(..., alias="_id")  # MongoDB ObjectId
    userId: str  # Foreign key to User.userId
    chatTranscript: List[Message]  # List of messages in the conversation
    diagnosedDisease: List[str]
    preventionTips: List[str]
    summary: str
    timestamp: datetime
