from bson import ObjectId

from app.core.database import users_collection
from app.schemas.auth import UserCreateSchema
from app.schemas.auth import UserLoginSchema
from app.core.conf import settings
from app.core.secure import bcrypt_context,verify_token
from fastapi import HTTPException, Depends
from jose import jwt
from datetime import timedelta,datetime,timezone
from fastapi.security import OAuth2PasswordRequestForm

async def create(user : UserCreateSchema):
    dual_user = await get_user(user.email)
    if dual_user is None:
        crypt_password = bcrypt_context.hash(user.password)
        await users_collection.insert_one({"name": user.name, "email": user.email, "password": crypt_password, "cart": [], "admin" : False})
    else:
        raise HTTPException(status_code=400,detail="ERRO: Email ja cadastrado")

async def login(user_login : UserLoginSchema):
    user = await get_user(user_login.email)
    if user is None:
        return HTTPException(status_code=400,detail="ERRO: Email nao cadastrado")
    else:
        if bcrypt_context.verify(user_login.password,user.get("password")):
            access_token = await get_token(user.get("_id"))
            refresh_token_ = await get_token(user.get("_id"), timedelta(days=7))
            return {"access_token" : access_token,
                    "refresh_token" : refresh_token_,
                    "token_type" : "Bearer"}
        else:
            return HTTPException(status_code=400, detail="ERRO: Senha Invalida")

async def login_oauth2(form : OAuth2PasswordRequestForm):
    user = await get_user(form.username)
    if user is None:
        return HTTPException(status_code=400,detail="ERRO: Email nao cadastrado")
    else:
        if bcrypt_context.verify(form.password,user.get("password")):
            access_token = await get_token(user.get("_id"))
            return {"access_token" : access_token,
                    "token_type" : "Bearer"}
        else:
            return HTTPException(status_code=400, detail="ERRO: Senha Invalida")

async def get_user(email : str):
    user = await users_collection.find_one({"email": email})
    return user

async def get_token(id_user : ObjectId, time_stamp : timedelta = timedelta(minutes=30)):
    expiration_date = datetime.now(timezone.utc) + time_stamp
    token_dic = {"sub" : str(id_user), "exp" : expiration_date}
    return jwt.encode(token_dic,settings.SECRET_KEY,settings.ALGORITHM)

async def refresh_token(user):
    access_token = await get_token(user.get("_id"))
    return {"access_token": access_token,
            "token_type": "Bearer"}