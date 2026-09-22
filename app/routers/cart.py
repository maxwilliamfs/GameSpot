from fastapi import APIRouter

cart_router = APIRouter(prefix="/cart",tags=["Carrinho de Compras"])

@cart_router.get("/")
async def get_cart():
    pass