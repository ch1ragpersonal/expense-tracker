from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="../../.env")

MONGODB_URL = os.getenv("MONGODB_URI")

client = AsyncIOMotorClient(MONGODB_URL)

db = client.expense_tracker


async def get_collection(collection_name: str):
    return db[collection_name]
