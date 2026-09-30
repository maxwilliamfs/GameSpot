from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth import create
from app.services.auth import login,refresh_token, login_oauth2
from app.schemas.auth import UserCreateSchema
from app.schemas.auth import UserLoginSchema
from app.core.secure import verify_token

auth_routers = APIRouter(prefix="/auth",tags=["Autenticacao"])

@auth_routers.post("/create_account", status_code=status.HTTP_201_CREATED)
async def create_account(user : UserCreateSchema):
    return await create(user)

@auth_routers.post("/login", status_code=status.HTTP_200_OK)
async def login_account(user : UserLoginSchema):
    return await login(user)

@auth_routers.post("/loginOAuth2", status_code=status.HTTP_200_OK)
async def login_account_oath2(form : OAuth2PasswordRequestForm = Depends()):
    return await login_oauth2(form)

@auth_routers.get("/refresh", status_code=status.HTTP_200_OK)
async def refresh(user = Depends(verify_token)):
    return await refresh_token(user)