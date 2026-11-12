from types import new_class

from fastapi import HTTPException
import pytest
from bson import ObjectId
from app.core.database import users_collection
from unittest.mock import AsyncMock
from app.services.user import id_search, update, update_password, update_user, delete_user, delete_admin
from app.schemas.user import UserUpdateAdminSchema, UserPasswordUpdateSchema, UserUpdateSchema

@pytest.mark.asyncio
async def test_id_search_invalid(mocker):
    with pytest.raises(HTTPException) as ex:
        await id_search("123")
    assert ex.value.status_code == 400

@pytest.mark.asyncio
async def test_id_search_none(mocker):
    fake_id = str(ObjectId())
    search_mock = mocker.patch.object(
        users_collection,
        "find_one",
        new_callable=AsyncMock,
        return_value=None
    )

    with pytest.raises(HTTPException) as ex:
        await id_search(fake_id)
    assert ex.value.status_code == 404

@pytest.mark.asyncio
async def test_update(mocker):
    new_data = UserUpdateAdminSchema(
        name="Jose Antonio de Oliveira"
    )
    fake_id = ObjectId()
    second_response = {"_id" : fake_id}
    search_mocker = mocker.patch(
        "app.services.user.id_search",
        new_callable=AsyncMock,
        side_effect=[None,second_response]
    )
    update_mocker = mocker.patch.object(
        users_collection,
        "update_one",
        new_callable=AsyncMock
    )
    result = await update(new_data,str(fake_id))
    update_mocker.assert_called_once_with({"_id" : fake_id},{"$set" : {"name" : "Jose Antonio de Oliveira"}})
    assert result["_id"] == str(fake_id)

@pytest.mark.asyncio
async def test_update_password(mocker):
    search_mocker = mocker.patch(
        "app.services.user.id_search",
        new_callable=AsyncMock,
        return_value=None
    )
    hash_mocker = mocker.patch(
        "app.services.user.bcrypt_context.hash",
        return_value="hashed_password"
    )
    update_mocker = mocker.patch.object(
        users_collection,
        "update_one",
        new_callable=AsyncMock,
    )
    new_password = UserPasswordUpdateSchema(
        password="new_password_123"
    )
    fake_id = ObjectId()
    await update_password(str(fake_id),new_password)
    update_mocker.assert_called_once_with({"_id" : fake_id},{"$set" : {"password" : "hashed_password"}})

@pytest.mark.asyncio
async def test_update_user(mocker):
    new_data = UserUpdateSchema(
        name="Jose Antonio de Oliveira"
    )

    fake_id = ObjectId()
    fake_user = {"_id": str(fake_id)}
    fake_return = {"_id": fake_id}
    search_mocker = mocker.patch(
        "app.services.user.id_search",
        new_callable=AsyncMock,
        return_value=fake_return
    )
    update_mocker = mocker.patch.object(
        users_collection,
        "update_one",
        new_callable=AsyncMock
    )
    result = await update_user(new_data,fake_user)
    update_mocker.assert_called_once_with({"_id" : ObjectId(fake_user.get("_id"))},{"$set" : {"name" : "Jose Antonio de Oliveira"}})
    assert result["_id"] == str(fake_id)

@pytest.mark.asyncio
async def test_delete_admin(mocker):
    search_mocker = mocker.patch(
        "app.services.user.id_search",
        new_callable=AsyncMock,
        return_value=None
    )
    fake_id = ObjectId()

    delete_mocker = mocker.patch.object(
        users_collection,
        "delete_one",
        new_callable=AsyncMock
    )
    await delete_admin(str(fake_id))
    delete_mocker.assert_called_once_with({"_id" : fake_id})

@pytest.mark.asyncio
async def test_delete_user(mocker):
    fake_id = ObjectId()
    fake_user = {"_id": str(fake_id)}

    search_mocker = mocker.patch(
        "app.services.user.id_search",
        new_callable=AsyncMock,
        return_value=None
    )
    delete_mocker = mocker.patch.object(
        users_collection,
        "delete_one",
        new_callable=AsyncMock
    )
    await delete_user(fake_user)
    delete_mocker.assert_called_once_with({"_id" : fake_id})