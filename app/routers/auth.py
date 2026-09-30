from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth import login,refresh_token, login_oauth2,update,update_user,update_password,create,search,delete_admin,delete_user
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

@auth_routers.get("/search/{id}", status_code=status.HTTP_200_OK)
async def user_search(id: str, admin = Depends(verify_admin)):
    return await search(id)

@auth_routers.patch("/admin-update/{id}", status_code=status.HTTP_200_OK)
async def admin_update(id: str, data : UserUpdateAdminSchema, admin = Depends(verify_admin)):
    return await update(data,id)

@auth_routers.patch("/admin-password/{id}", status_code=status.HTTP_200_OK)
async def password_update(id: str,password : str, admin = Depends(verify_admin)):
    await update_password(id,password)

@auth_routers.patch("/user-update/{id}", status_code=status.HTTP_200_OK)
async def admin_update(id: str, data : UserUpdateSchema, user = Depends(verify_token)):
    return await update_user(data,id,user)

@auth_routers.delete("/admin-delete/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete(id: str, admin = Depends(verify_admin)):
    await delete_admin(id)

@auth_routers.delete("/user-delete",status_code=status.HTTP_204_NO_CONTENT)
async def user_delete(user = Depends(verify_token)):
    await delete_user(user)