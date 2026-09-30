from fastapi import APIRouter, Depends
from app.schemas.cart import CartItemInsertSchema
from app.core.secure import verify_token
from app.services.cart import add

cart_router = APIRouter(prefix="/cart",tags=["Carrinho de Compras"])

@cart_router.get("/get/{id}")
async def get_cart():
    pass

@cart_router.post("/insert")
async def insert_games(cart_item_insert : CartItemInsertSchema, user : dict = Depends(verify_token)):
    return await add(user,cart_item_insert)