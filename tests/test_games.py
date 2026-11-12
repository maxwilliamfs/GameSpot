import pytest
from bson import ObjectId
from fastapi import HTTPException
from app.schemas.games import CreateGameSchema, StorePriceDetails, UpdateGameSchema
from app.core.enums import StoresEnum
from unittest.mock import MagicMock,AsyncMock
from app.services.game import create, id_search, update, delete
from app.core.database import games_collection

@pytest.mark.asyncio
async def test_create_game(mocker):
    store_price_details = StorePriceDetails(price=60)
    prices_ = {}

    for store in StoresEnum:
        prices_[store] = store_price_details

    game = CreateGameSchema(
        title="Hollow Knight: SilkSong",
        developer="Team Chery",
        all_time_cheapest_price=40.0,
        prices=prices_
    )

    id_ = ObjectId()
    mongo_result = MagicMock()
    mongo_result.inserted_id = id_

    mock_insert = mocker.patch.object(
        games_collection,
        "insert_one",
        new_callable=AsyncMock,
        return_value = mongo_result
    )

    result = await create(game)

    expected_result = game.model_dump(mode="json")
    expected_result["_id"] = str(id_)
    assert result == expected_result


@pytest.mark.asyncio
async def test_update_game(mocker):
    fake_id = str(ObjectId())
    old_data = {
        "_id": fake_id,
        "title": "Hollow Knight: SilkSong",
        "developer": "Team Cherry"
    }
    new_data = {
        "_id": fake_id,
        "title": "Hollow Knight: Silksong - Deluxe",
        "developer": "Team Cherry"
    }
    search_mock = mocker.patch(
        "app.services.game.id_search",
        new_callable=AsyncMock,
        side_effect=[old_data,new_data]
    )

    update_mock = mocker.patch.object(
        games_collection,
        "update_one",
        new_callable=AsyncMock
    )
    update_data = UpdateGameSchema(title="Hollow Knight: Silksong - Deluxe")
    expected_update_dict = {"title": "Hollow Knight: Silksong - Deluxe"}

    result = await update(fake_id, update_data)
    update_mock.assert_called_once_with({"_id": ObjectId(fake_id)}, {"$set": expected_update_dict})
    assert result["_id"] == fake_id

@pytest.mark.asyncio
async def test_id_search(mocker):
    fake_id = "123"
    with pytest.raises(HTTPException):
        await id_search(fake_id)

@pytest.mark.asyncio
async def test_delete(mocker):
    fake_id = str(ObjectId())
    search_mock = mocker.patch(
        "app.services.game.id_search",
        new_callable=AsyncMock,
        return_value="game"
    )
    delete_mock = mocker.patch.object(
        games_collection,
        "delete_one",
        new_callable= AsyncMock
    )
    await delete(fake_id)
    delete_mock.assert_called_once_with({"_id" : ObjectId(fake_id)})

@pytest.mark.asyncio
async def test_id_search_invalid(mocker):
    with pytest.raises(HTTPException) as ex:
        await id_search("123")
    assert ex.value.status_code == 400

@pytest.mark.asyncio
async def test_id_search_none(mocker):
    fake_id = str(ObjectId())
    search_mock = mocker.patch.object(
        games_collection,
        "find_one",
        new_callable=AsyncMock,
        return_value=None
    )

    with pytest.raises(HTTPException) as ex:
        await id_search(fake_id)
    assert ex.value.status_code == 404
