from http import HTTPMethod

import pytest
from bson import ObjectId
from fastapi import HTTPException

from app.schemas.games import CreateGameSchema, StorePriceDetails, UpdateGameSchema
from app.core.enums import StoresEnum
from unittest.mock import MagicMock,AsyncMock
from app.services.game import create, id_search, update
from app.core.database import games_collection

@pytest.fixture()
def game():
    store_price_details = StorePriceDetails(price=60)
    prices_ = {}

    for store in StoresEnum:
        prices_[store] = store_price_details

    game_test = CreateGameSchema(
    title="Hollow Knight: SilkSong",
    developer="Team Chery",
    all_time_cheapest_price=40.0,
    prices=prices_
    )
    return game_test

@pytest.mark.asyncio
async def test_create_game(game, mocker):
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
async def test_update_game(game,mocker):
    mock_wrong_id = mocker.patch(
        "app.services.game.id_search",
        new_callable=AsyncMock,
        return_value=None
    )
    fake_id = str(ObjectId())
    data = UpdateGameSchema()

    with pytest.raises(HTTPException) as ex:
        await update(fake_id,data)

