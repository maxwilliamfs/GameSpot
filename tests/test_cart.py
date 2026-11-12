from fastapi import HTTPException
import pytest
from unittest.mock import AsyncMock
from bson import ObjectId
from app.schemas.cart import CartItemInsertSchema, CartItemSchema
from app.services.cart import add, delete
from app.core.enums import StoresEnum
from app.core.database import users_collection

@pytest.fixture
def cart_insert():
    cart = CartItemInsertSchema(
        game_id=str(ObjectId()),
        store=StoresEnum.Steam
    )
    return cart

@pytest.mark.asyncio
async def test_add_cart_invalid_game(mocker, cart_insert):
    search_mocker = mocker.patch(
        "app.services.cart.id_search",
        new_callable=AsyncMock,
        return_value=None
    )
    fake_user = {
        "cart": [
            {"game_id": cart_insert.game_id}
        ]
    }
    with pytest.raises(HTTPException):
        await add(fake_user,cart_insert)

@pytest.mark.asyncio
async def test_add_cart(mocker, cart_insert):
    fake_game = {"prices" : {"Steam" : {"price" : 60}},"title" : "Hollow Knight SilkSong"}
    fake_user = {
        "_id" : ObjectId(),
        "cart": []
    }
    search_mocker = mocker.patch(
        "app.services.cart.id_search",
        new_callable=AsyncMock,
        return_value=fake_game
    )
    update_mocker = mocker.patch.object(
        users_collection,
        "update_one",
        new_callable=AsyncMock
    )
    expected_item = CartItemSchema(
        game_id=cart_insert.game_id,
        title="Hollow Knight SilkSong",
        store=cart_insert.store.value,
        price=60
    ).model_dump()
    await add(fake_user,cart_insert)
    update_mocker.assert_called_once_with({"_id" : fake_user.get("_id")}, {"$inc" : {"cart_count" : 1},"$addToSet" : {"cart" : expected_item}})

@pytest.mark.asyncio
async def test_delete_cart_invalid_game(mocker):
    fake_game_id = ObjectId()
    fake_user = {
        "cart": []
    }
    with pytest.raises(HTTPException):
        await delete(fake_user,str(fake_game_id))

@pytest.mark.asyncio
async def test_delete_cart_invalid_game(mocker):
    pass


# async def delete(user, game_id : str):
#     user_cart = user.get("cart")
#
#     for game in user_cart:
#         if game_id == game.get("game_id"):
#             await users_collection.update_one({"_id" : ObjectId(user.get("_id"))},{"$pull":{"cart" : game},"$inc" : {"cart_count" : -1}})
#             return {"message": "Game removed successfully"}
#
#     raise HTTPException(status_code=404,detail="ERROR: Game not found")