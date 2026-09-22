from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client["gamespot_db"]
users_collection = db.get_collection("users")
games_collection = db.get_collection("games")
