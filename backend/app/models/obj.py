from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional
from bson import ObjectId
import uuid
# Custom ObjectId field
class ObjectIdField(str):
    """Custom Pydantic type for ObjectId to automatically convert it to a string"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return str(v)  # Convert ObjectId to string
        elif isinstance(v, str):
            return v  # If it's already a string, return it
        raise ValueError("Invalid ObjectId")