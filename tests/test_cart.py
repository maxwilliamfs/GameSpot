import pytest
from unittest.mock import AsyncMock

# @pytest.mark.asyncio
# async def test_add_cart(mocker):
#     pass

# async def add(user, cart_insert : CartItemInsertSchema):
#     game = await id_search(str(cart_insert.game_id))
#
#     for games in user["cart"]:
#         if cart_insert.game_id == games["game_id"]:
#             raise HTTPException(status_code=400,detail="This game already exists in this cart!!!")
#
#     store_name = cart_insert.store.value
#     prices = game.get("prices")
#     store = prices.get(store_name)
#
#     cart_item = CartItemSchema(
#         game_id=cart_insert.game_id,
#         title=game.get("title"),
#         store= store_name,
#         price= store.get("price")
#     )
#     item_dict = cart_item.model_dump()
#
#     await users_collection.update_one({"_id" : user.get("_id")},
#     {"$inc" : {"cart_count" : 1},"$addToSet" : {"cart" : item_dict}})
#
#     return item_dict
#
# async def delete(user, game_id : str):
#     user_cart = user.get("cart")
#
#     for game in user_cart:
#         if game_id == game.get("game_id"):
#             await users_collection.update_one({"_id" : ObjectId(user.get("_id"))},{"$pull":{"cart" : game},"$inc" : {"cart_count" : -1}})
#             return {"message": "Game removed successfully"}
#
#     raise HTTPException(status_code=404,detail="ERROR: Game not found")