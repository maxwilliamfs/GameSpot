from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth import create,search
from app.services.auth import login,refresh_token, login_oauth2,update,update_user
from app.schemas.auth import UserCreateSchema,UserLoginSchema,UserUpdateSchema,UserUpdateAdminSchema
from app.core.secure import verify_refresh_token, verify_admin, verify_token

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

@auth_routers.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh(user = Depends(verify_refresh_token)):
    return await refresh_token(user)

@auth_routers.get("/search/{id}")
async def user_search(id: str, admin = Depends(verify_admin)):
    return await search(id)

@auth_routers.patch("/admin-update/{id}")
async def admin_update(id: str, data : UserUpdateAdminSchema, admin = Depends(verify_admin)):
    return await update(data,id)

@auth_routers.patch("/user-update/{id}")
async def admin_update(id: str, data : UserUpdateSchema, user = Depends(verify_token)):
    return await update_user(data,id,user)