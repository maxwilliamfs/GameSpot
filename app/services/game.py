from bson.errors import InvalidId
from fastapi import HTTPException
from bson import ObjectId
from app.schemas.games import CreateGameSchema, GameResponseSchema, UpdateGameSchema
from app.core.database import games_collection

async def id_search(game_id : str):
    try:
        mongo_id = ObjectId(game_id)
        game = await games_collection.find_one({"_id" : mongo_id})
        return game
    except InvalidId:
        raise HTTPException(status_code=400,detail="ERROR: INVALID ID!!!")

async def search(name : str):
    cursor = games_collection.find({"title": {"$regex": name, "$options": "i"}})
    results = await cursor.to_list(length=20)
    for result in results:
        result["_id"] = str(result["_id"])
    return results

async def create(game : CreateGameSchema):
    game_dict = game.model_dump(mode="json")
    result = await games_collection.insert_one(game_dict)
    game_dict["_id"] = str(result.inserted_id)
    return game_dict

async def update(game_id : str, game : UpdateGameSchema):
    game_db = await id_search(game_id)
    if game_db is None:
        raise HTTPException(status_code=404,detail="ERROR: Game not Founded")
    else:
        game_dict = game.model_dump(mode="json",exclude_unset=True)
        await games_collection.update_one({"_id" : ObjectId(game_id)},{"$set" : game_dict})
        response = await id_search(game_id)
        response["_id"] = str(response["_id"])
        return response

async def delete(game_id : str):
    game = await id_search(game_id)
    if game is None:
        raise HTTPException(status_code=404,detail="ERROR: Game not Founded")
    else:
        await games_collection.delete_one({"_id" : ObjectId(game_id)})
        return {"message" : "Game deleted successfully!!!"}