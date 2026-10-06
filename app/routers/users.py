from fastapi import APIRouter, status, Depends
from app.core.secure import verify_token,verify_admin
from app.schemas.user import UserUpdateSchema,UserUpdateAdminSchema,UserPasswordUpdateSchema,UserResponseSchema
from app.services.user import search,update,update_password,delete_admin,delete_user,update_user

users_router = APIRouter(prefix="/users",tags=["Usuarios"])

@users_router.patch("/me", status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
async def user_update(data : UserUpdateSchema, user = Depends(verify_token)):
    return await update_user(data,user)

@users_router.delete("/me",status_code=status.HTTP_204_NO_CONTENT)
async def user_delete(user = Depends(verify_token)):
    await delete_user(user)

@users_router.get("/{id}", status_code=status.HTTP_200_OK,response_model=UserResponseSchema)
async def user_search(id: str, admin = Depends(verify_admin)):
    return await search(id)

@users_router.patch("/{id}", status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
async def admin_update(id: str, data : UserUpdateAdminSchema, admin = Depends(verify_admin)):
    return await update(data,id)

@users_router.patch("/{id}/password", status_code=status.HTTP_200_OK)
async def password_update(id: str,passwordSchema: UserPasswordUpdateSchema, admin = Depends(verify_admin)):
    await update_password(id,passwordSchema)

@users_router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete(id: str, admin = Depends(verify_admin)):
    await delete_admin(id)
