from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException

from app.core.secure import bcrypt_context
from app.schemas.user import UserUpdateAdminSchema,UserUpdateSchema,UserResponseSchema,UserPasswordUpdateSchema
from app.core.database import users_collection

async def id_search(id: str):
    try:
        user = await users_collection.find_one({"_id": ObjectId(id)})
    except InvalidId:
        raise HTTPException(status_code=400, detail="ERRO: Invalid ID")
    if user is None:
        raise HTTPException(status_code=404,detail="ERRO: User not found")
    return user

async def search(id: str):
    user = await id_search(id)
    user["_id"] = str(user["_id"])
    return user

async def update(new_data : UserUpdateAdminSchema, id: str):
    user_db = await id_search(id)
    if user_db is None:
        raise HTTPException(status_code=404, detail="ERROR: User not Found")
    user_dict = new_data.model_dump(exclude_unset=True)
    await users_collection.update_one({"_id" : ObjectId(id)},{"$set" : user_dict})
    response = await id_search(id)
    response["_id"] = str(response["_id"])
    return response

async def update_password(id: str, passwordSchema: UserPasswordUpdateSchema):
    user_db = await id_search(id)
    if user_db is None:
        raise HTTPException(status_code=404, detail="ERROR: User not Found")
    crypt_password = bcrypt_context.hash(passwordSchema.password)
    await users_collection.update_one({"_id" : ObjectId(id)},{"$set" : {"password" : crypt_password}})


async def update_user(new_data : UserUpdateSchema, user):
    user_dict = new_data.model_dump(exclude_unset=True)
    result = await users_collection.update_one({"_id" : ObjectId(user.get("_id"))},{"$set" : user_dict})
    user_dict = await id_search(user.get("_id"))
    user_dict["_id"] = str(user["_id"])
    return user_dict

async def delete_admin(id: str):
    user = await id_search(id)
    await users_collection.delete_one({"_id" : ObjectId(id)})

async def delete_user(user):
    user = await id_search(user.get("_id"))
    await users_collection.delete_one({"_id": ObjectId(user.get("_id"))})
