# app/models.py
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, values=None, **kwargs):  # Add additional parameters
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    # @classmethod
    # def __get_pydantic_json_schema__(cls, field_schema):
    #     field_schema.update(type="string")

class ItemModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: Optional[str] = None

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
