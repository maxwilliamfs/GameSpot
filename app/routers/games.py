from fastapi import APIRouter, Depends, status
from app.schemas.games import CreateGameSchema,UpdateGameSchema
from app.core.secure import verify_admin
from app.services.games import create, update, search, delete

games_router = APIRouter(prefix="/games",tags=["Jogos"])

@games_router.get("/search/{name}", status_code=status.HTTP_200_OK)
async def search_game(name : str):
    return search(name)

@games_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_game(game : CreateGameSchema, admin_user = Depends(verify_admin)):
    return await create(game)

@games_router.put("/update/{game_id}", status_code=status.HTTP_200_OK)
async def update_game(game_id : str, update_data : CreateGameSchema, admin_user = Depends(verify_admin)):
    return await update(game_id,update_data)

@games_router.delete("/delete/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_game(game_id : str, admin_user = Depends(verify_admin)):
    return await delete(game_id)
