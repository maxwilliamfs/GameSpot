from fastapi import APIRouter
from app.services.auth import create
from app.services.auth import login
from app.schemas.auth import UserCreateSchema
from app.schemas.auth import UserLoginSchema

auth_routers = APIRouter(prefix="/auth",tags=["Autenticacao"])

@auth_routers.post("/create_account")
async def create_account(user : UserCreateSchema):
    return await create(user)

@auth_routers.post("/login")
async def login_account(user : UserLoginSchema):
    return await login(user)