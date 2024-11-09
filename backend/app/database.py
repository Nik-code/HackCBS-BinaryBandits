from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGO_URL, DATABASE_NAME

client = AsyncIOMotorClient(MONGO_URL)
database = client[DATABASE_NAME]

# Collection reference for items
items_collection = database["items"]