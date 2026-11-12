from fastapi import HTTPException
import pytest
from bson import ObjectId
from app.core.database import users_collection
from unittest.mock import AsyncMock
from app.services.user import id_search, update, update_password
from app.schemas.user import UserUpdateAdminSchema, UserPasswordUpdateSchema

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
