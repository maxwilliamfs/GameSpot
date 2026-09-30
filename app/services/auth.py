from bson import ObjectId
from bson.errors import InvalidId

from app.core.enums import TokenTypesEnum
from app.core.database import users_collection
from app.schemas.auth import UserCreateSchema,UserLoginSchema,UserResponseSchema, UserUpdateSchema
from app.core.conf import settings
from app.core.secure import bcrypt_context
from fastapi import HTTPException
from jose import jwt
from datetime import timedelta,datetime,timezone
from fastapi.security import OAuth2PasswordRequestForm

async def create(user : UserCreateSchema):
    dual_user = await get_user(user.email)
    if dual_user is None:
        crypt_password = bcrypt_context.hash(user.password)
        result = await users_collection.insert_one({"name": user.name, "email": user.email, "password": crypt_password, "cart_count" : 0, "cart": [], "admin" : False})
        response = UserResponseSchema(
            id=str(result.inserted_id),
            name= user.name,
            email= user.email,
            admin= False,
            cart_count= 0,
            cart= []
        )
        return response.model_dump()
    else:
        raise HTTPException(status_code=400,detail="ERROR: Email already exists!!!!")

async def login(user_login : UserLoginSchema):
    user = await get_user(user_login.email)
    if user is None:
        raise HTTPException(status_code=400,detail="ERRO: Email not found")
    else:
        if bcrypt_context.verify(user_login.password,user.get("password")):
            access_token = await get_token(user.get("_id"),TokenTypesEnum.Access_Token)
            refresh_token_ = await get_token(user.get("_id"),TokenTypesEnum.Refresh_Token, timedelta(days=7))
            return {"access_token" : access_token,
                    "refresh_token" : refresh_token_,
                    "token_type" : "Bearer"}
        else:
            raise HTTPException(status_code=400, detail="ERRO: Invalid password")

async def login_oauth2(form : OAuth2PasswordRequestForm):
    user = await get_user(form.username)
    if user is None:
        raise HTTPException(status_code=400,detail="ERRO: Email not found")
    else:
        if bcrypt_context.verify(form.password,user.get("password")):
            access_token = await get_token(user.get("_id"),TokenTypesEnum.Access_Token)
            return {"access_token" : access_token,
                    "token_type" : "Bearer"}
        else:
            raise HTTPException(status_code=400, detail="ERRO: Invalid password")

async def get_user(email : str):
    user = await users_collection.find_one({"email": email})
    return user

async def id_search(id: str):
    try:
        user = await users_collection.find_one({"_id": ObjectId(id)})
    except InvalidId:
        raise HTTPException(status_code=400, detail="ERRO: Invalid ID")
    if user is None:
        raise HTTPException(status_code=404,detail="ERRO: User not found")
    return user

async def get_token(id_user : ObjectId,type : TokenTypesEnum, time_stamp : timedelta = timedelta(minutes=30)):
    expiration_date = datetime.now(timezone.utc) + time_stamp
    token_dic = {"sub" : str(id_user),"type": type.value, "exp" : expiration_date}
    return jwt.encode(token_dic,settings.SECRET_KEY,settings.ALGORITHM)

async def refresh_token(user):
    access_token = await get_token(user.get("_id"),TokenTypesEnum.Access_Token)
    return {"access_token": access_token,
            "token_type": "Bearer"}

async def search(id: str):
    user = await id_search(id)
    return await model_dumper(user,str(user.get("_id")))

async def update(new_data : UserUpdateSchema, id: str):
    user_db = await id_search(id)
    if user_db is None:
        raise HTTPException(status_code=404, detail="ERROR: User not Found")
    user_dict = new_data.model_dump(exclude_unset=True)
    await users_collection.update_one({"_id" : ObjectId(id)},{"$set" : user_dict})
    response = await id_search(id)
    return await model_dumper(response,id)

async def update_user(new_data : UserUpdateSchema, id: str, user):
    user_db = await id_search(id)
    if id != str(user.get("_id")):
        raise HTTPException(status_code=403, detail="ERRO: Access Blocked!!!")
    if user_db is None:
        raise HTTPException(status_code=404, detail="ERROR: User not Found")
    user_dict = new_data.model_dump(exclude_unset=True)
    await users_collection.update_one({"_id" : ObjectId(id)},{"$set" : user_dict})
    response = await id_search(id)
    return await model_dumper(response,id)


async def model_dumper(user,id : str):
    response = UserResponseSchema(
        id=id,
        name=user.get("name"),
        email=user.get("email"),
        admin=user.get("admin"),
        cart_count=user.get("cart_count",0),
        cart=user.get("cart",[])
    )
    return response.model_dump()
