from datetime import timedelta
from bson import ObjectId
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.core.enums import TokenTypesEnum
from app.services.auth import id_search, create, login_oauth2, login
import pytest
from app.core.database import users_collection
from app.schemas.user import UserCreateSchema, UserLoginSchema
from unittest.mock import AsyncMock, MagicMock, call


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
    get_mocker = mocker.patch(
        "app.services.auth.get_user",
        new_callable=AsyncMock,
        return_value=None
    )
    fake_password = "Password_hash_123"
    crypt_mocker = mocker.patch(
        "app.services.auth.bcrypt_context.hash",
        return_value= fake_password
    )
    fake_id = ObjectId()
    mongo_result = MagicMock()
    mongo_result.inserted_id = fake_id
    insertion_mocker = mocker.patch.object(
        users_collection,
        "insert_one",
        new_callable=AsyncMock,
        return_value=mongo_result
    )
    result = await create(user_create)
    insertion_mocker.assert_called_once_with({"name": user_create.name, "email": user_create.email, "password": fake_password, "cart_count" : 0, "cart": [], "admin" : False})
    print(result)
    assert result["id"] == str(fake_id)

@pytest.fixture
def user_login():
    user = UserLoginSchema(
        email="Jose123@gmail.com",
        password="Jose12345678"
    )
    return user

#Normal Login

@pytest.mark.asyncio
async def test_login_none(mocker, user_login):
    get_mocker = mocker.patch(
        "app.services.auth.get_user",
        new_callable=AsyncMock,
        return_value=None
    )
    with pytest.raises(HTTPException) as ex:
        await login(user_login)
    assert ex.value.status_code == 400

@pytest.mark.asyncio
async def test_login_invalid_password(mocker, user_login):
    fake_user = {"password" : "password123"}

    get_mocker = mocker.patch(
        "app.services.auth.get_user",
        new_callable=AsyncMock,
        return_value=fake_user
    )
    verify_mocker = mocker.patch(
        "app.services.auth.bcrypt_context.verify",
        return_value=False
    )
    with pytest.raises(HTTPException) as ex:
        await login(user_login)
    assert ex.value.status_code == 400

@pytest.mark.asyncio
async def test_login(mocker, user_login):
    fake_id = ObjectId()
    fake_user = {"password" : "password123", "_id" : fake_id}

    get_mocker = mocker.patch(
        "app.services.auth.get_user",
        new_callable=AsyncMock,
        return_value=fake_user
    )
    verify_mocker = mocker.patch(
        "app.services.auth.bcrypt_context.verify",
        return_value=True
    )
    fake_access_token = "fake_access_token"
    fake_refresh_token = "fake_refresh_token"
    token_mocker = mocker.patch(
        "app.services.auth.get_token",
        new_callable=AsyncMock,
        side_effect=[fake_access_token,fake_refresh_token]
    )
    result = await login(user_login)
    calls = [
        call(fake_id,TokenTypesEnum.Access_Token),
        call(fake_id, TokenTypesEnum.Refresh_Token,timedelta(days=7))
    ]
    token_mocker.assert_has_calls(calls)
    assert result["access_token"] == fake_access_token
    assert result["refresh_token"] == fake_refresh_token
    assert result["token_type"] == "Bearer"

# OAUTH2

@pytest.fixture
def user_login_oauth2():
    user = OAuth2PasswordRequestForm(
        username="Jose123@gmail.com",
        password="Jose12345678"
    )
    return user

@pytest.mark.asyncio
async def test_login_oauth2_none(mocker, user_login_oauth2):
    get_mocker = mocker.patch(
        "app.services.auth.get_user",
        new_callable=AsyncMock,
        return_value=None
    )
    with pytest.raises(HTTPException) as ex:
        await login_oauth2(user_login_oauth2)
    assert ex.value.status_code == 400

@pytest.mark.asyncio
async def test_login_oauth2_invalid_password(mocker, user_login_oauth2):
    fake_user = {"password" : "password123"}

    get_mocker = mocker.patch(
        "app.services.auth.get_user",
        new_callable=AsyncMock,
        return_value=fake_user
    )
    verify_mocker = mocker.patch(
        "app.services.auth.bcrypt_context.verify",
        return_value=False
    )
    with pytest.raises(HTTPException) as ex:
        await login_oauth2(user_login_oauth2)
    assert ex.value.status_code == 400

@pytest.mark.asyncio
async def test_login_oauth2(mocker, user_login_oauth2):
    fake_id = ObjectId()
    fake_user = {"username" : "password123", "_id" : fake_id}

    get_mocker = mocker.patch(
        "app.services.auth.get_user",
        new_callable=AsyncMock,
        return_value=fake_user
    )
    verify_mocker = mocker.patch(
        "app.services.auth.bcrypt_context.verify",
        return_value=True
    )
    fake_access_token = "fake_access_token"
    token_mocker = mocker.patch(
        "app.services.auth.get_token",
        new_callable=AsyncMock,
        return_value=fake_access_token
    )
    result = await login_oauth2(user_login_oauth2)
    token_mocker.assert_called_once_with(fake_id,TokenTypesEnum.Access_Token)
    assert result["access_token"] == fake_access_token
    assert result["token_type"] == "Bearer"
