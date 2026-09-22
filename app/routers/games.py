from fastapi import APIRouter
from app.core.database import games_collection

games_router = APIRouter(prefix="/games",tags=["Busca de Jogos"])

@games_router.get("/search/{name}")
async def search(name : str):
    cursor = games_collection.find({"titulo" : {"$regex" : name, "$options" : "i"}})
    results = await cursor.to_list(length=20)

    for result in results:
        result["_id"] = str(result["_id"])
    return results


