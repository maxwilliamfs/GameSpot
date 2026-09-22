#uvicorn app.main:app --reload
from fastapi import FastAPI
from app.routers.auth import auth_routers
from app.routers.games import games_router
from app.routers.cart import cart_router

app = FastAPI()

app.include_router(auth_routers)
app.include_router(cart_router)
app.include_router(games_router)

