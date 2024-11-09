# app/routers/items.py
from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas import ItemCreateSchema, ItemUpdateSchema
from app.crud import get_items, get_item, create_item, update_item, delete_item
from app.models import ItemModel

router = APIRouter()

@router.get("/", response_model=List[ItemModel])
async def read_items():
    return await get_items()

@router.get("/{item_id}", response_model=ItemModel)
async def read_item(item_id: str):
    item = await get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/", response_model=ItemModel)
async def create_new_item(item: ItemCreateSchema):
    return await create_item(item.dict())

@router.put("/{item_id}", response_model=ItemModel)
async def update_existing_item(item_id: str, item: ItemUpdateSchema):
    updated_item = await update_item(item_id, item.dict(exclude_unset=True))
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@router.delete("/{item_id}", response_model=bool)
async def delete_existing_item(item_id: str):
    success = await delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return success
