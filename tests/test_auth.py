from bson import ObjectId
from fastapi import HTTPException
from app.services.auth import id_search, create
import pytest
from app.core.database import users_collection
from app.schemas.user import UserCreateSchema
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_id_search_invalid(mocker):
    with pytest.raises(HTTPException) as ex:
        await id_search("1")
    assert ex.value.status_code == 400

@pytest.mark.asyncio
async def test_id_search_none(mocker):
    search_mocker = mocker.patch.object(
        users_collection,
        "find_one",
        new_callable=AsyncMock,
        return_value=None
    )
    with pytest.raises(HTTPException) as ex:
        await id_search(str(ObjectId()))
    assert ex.value.status_code == 404

@pytest.fixture
def user_create():
    user = UserCreateSchema(
        name="Jose Antonio",
        email="Jose123@gmail.com",
        password="Jose12345678"
    )
    return user

@pytest.mark.asyncio
async def test_create_duplicate(mocker, user_create):
    get_mocker = mocker.patch(
        "app.services.auth.get_user",
        new_callable=AsyncMock,
        return_value="Not None"
    )
    with pytest.raises(HTTPException) as ex:
        await create(user_create)
    assert ex.value.status_code == 400

@pytest.mark.asyncio
async def test_create(mocker, user_create):
    pass

# async def create(user : UserCreateSchema):
#     dual_user = await get_user(user.email)
#     if dual_user is None:
#         crypt_password = bcrypt_context.hash(user.password)
#         result = await users_collection.insert_one({"name": user.name, "email": user.email, "password": crypt_password, "cart_count" : 0, "cart": [], "admin" : False})
#         response = UserResponseSchema(
#             id=str(result.inserted_id),
#             name= user.name,
#             email= user.email,
#             admin= False,
#             cart_count= 0,
#             cart= []
#         )
#         return response.model_dump()
#     else:
#         raise HTTPException(status_code=400,detail="ERROR: Email already exists!!!!")
