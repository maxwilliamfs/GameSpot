from motor.motor_asyncio import AsyncIOMotorClient
from conf import settings

client = AsyncIOMotorClient(settings.MONGO_URL)
db = client[settings.DATABASE_NAME]
users_collection = db.get_collection("users")
games_collection = db.get_collection("games")
