from app.core.database import users_collection
from app.schemas.auth import UserCreateSchema
from app.schemas.auth import UserLoginSchema
from app.core.secure import bcrypt_context
from fastapi import HTTPException

async def create(user : UserCreateSchema):
    dual_user = await get_user(user.email)

    if dual_user is None:
        crypt_password = bcrypt_context.hash(user.password)
        await users_collection.insert_one({"name": user.name, "email": user.email, "password": crypt_password, "cart": []})
    else:
        raise HTTPException(status_code=400,detail="ERRO: Email ja cadastrado")

async def login(user_login : UserLoginSchema):
    user = await get_user(user_login.email)
    if user is None:
        return HTTPException(status_code=400,detail="ERRO: Email nao cadastrado")
    else:
        if bcrypt_context.verify(user_login.password,user.get("password")):
            pass
        else:
            return HTTPException(status_code=400, detail="ERRO: Senha Invalida")

async def get_user(email : str):
    user = users_collection.find_one({"email": email})
    return user

def get_token():
    token = ""
    return token