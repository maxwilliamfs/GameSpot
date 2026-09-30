from bson import ObjectId
from pydantic import BaseModel
from app.core.enums import StoresEnum

class CartItemSchema(BaseModel):
    game_id: str
    title: str
    store: str
    price: float

class CartItemInsertSchema(BaseModel):
    game_id: str
    store: StoresEnum