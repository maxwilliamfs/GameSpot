#uvicorn app.main:app --reload

#Bibliotecas
from fastapi import FastAPI
from app.routers.auth import auth_routers
from app.routers.deal import deal_router
from app.routers.order import order_router

app = FastAPI()
app.include_router(auth_routers)
app.include_router(deal_router)
app.include_router(order_router)

