from fastapi import APIRouter
from app.services.auth import create

auth_routers = APIRouter(prefix="/auth",tags=["Autenticacao"])

@auth_routers.post("/create_account")
async def create_account(name : str,email : str, password : str):
    return await create(name,email,password)