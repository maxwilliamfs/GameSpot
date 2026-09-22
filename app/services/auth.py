from app.core.database import users_collection
from app.schemas.auth import UserCreateSchema
from app.schemas.auth import UserLoginSchema
from app.core.secure import bcrypt_context
from fastapi import HTTPException

async def create(user : UserCreateSchema):
    dual_user = await users_collection.find_one({"email": user.email})

    if dual_user is None:
        crypt_password = bcrypt_context.hash(user.password)
        await users_collection.insert_one({"name": user.name, "email": user.email, "password": crypt_password, "cart": []})
    else:
        raise HTTPException(status_code=400,detail="Erro: Email ja cadastrado")

async def login(user : UserLoginSchema):
    user = await users_collection.find_one({"email": user.email})
    if user is None:
        return HTTPException(status_code=400,detail="Email nao cadastrado")
    else:
        pass