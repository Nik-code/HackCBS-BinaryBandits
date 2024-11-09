# app/schemas.py
from pydantic import BaseModel
from typing import Optional

class ItemCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None

class ItemUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
