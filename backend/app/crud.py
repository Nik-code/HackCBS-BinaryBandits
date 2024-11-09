# app/crud.py
from typing import List, Optional
from .database import items_collection
from .models import ItemModel

async def get_items() -> List[ItemModel]:
    items = await items_collection.find().to_list(100)
    return [ItemModel(**item) for item in items]

async def get_item(item_id: str) -> Optional[ItemModel]:
    item = await items_collection.find_one({"id": item_id})
    if item:
        return ItemModel(**item)

async def create_item(item_data: dict) -> ItemModel:
    result = await items_collection.insert_one(item_data)
    item_data["_id"] = result.inserted_id
    return ItemModel(**item_data)

async def update_item(item_id: str, item_data: dict) -> Optional[ItemModel]:
    result = await items_collection.update_one({"_id": item_id}, {"$set": item_data})
    if result.modified_count == 1:
        updated_item = await get_item(item_id)
        return updated_item

async def delete_item(item_id: str) -> bool:
    result = await items_collection.delete_one({"_id": item_id})
    return result.deleted_count == 1
