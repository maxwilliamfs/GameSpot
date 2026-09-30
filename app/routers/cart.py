from fastapi import APIRouter, Depends, status
from app.schemas.cart import CartItemInsertSchema
from app.core.secure import verify_token
from app.services.cart import add,delete,get

cart_router = APIRouter(prefix="/carts",tags=["Carrinho de Compras"])

@cart_router.get("", status_code=status.HTTP_200_OK)
async def get_cart(user = Depends(verify_token)):
    return await get(user)

@cart_router.post("/itens", status_code=status.HTTP_201_CREATED)
async def insert_games(cart_item_insert : CartItemInsertSchema, user : dict = Depends(verify_token)):
    return await add(user,cart_item_insert)

@cart_router.delete("/itens/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_game(game_id : str, user = Depends(verify_token)):
    return await delete(user,game_id)

