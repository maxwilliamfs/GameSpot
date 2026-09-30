from bson import ObjectId

from app.core.database import users_collection
from app.schemas.cart import CartItemInsertSchema, CartItemSchema
from app.services.games import id_search

async def add(user, cart_insert : CartItemInsertSchema):
    game = await id_search(str(cart_insert.game_id))

    store_name = cart_insert.store.value
    prices = game.get("prices")
    price = prices.get(store_name)

    cart_item = CartItemSchema(
        game_id=cart_insert.game_id,
        name=game.get("name"),
        store= store_name,
        price= price
    )
    item_dict = cart_item.model_dump()

    await users_collection.update_one({"_id" : user.get("_id")},
    {"$inc" : {"cart_count" : 1},"addToSet" : {"cart" : cart_item}})

    return item_dict