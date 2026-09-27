from pydantic import BaseModel
from typing import List

class StorePriceSchema(BaseModel):
    store: str
    price: float
    cheapest_price: float

class CreateGameSchema(BaseModel):
    title: str
    developer: str
    all_time_cheapest_price: float
    prices: List[StorePriceSchema]

class UpdateGameSchema(BaseModel):
    id: int
    title: str
    developer: str
    all_time_cheapest_price: float
    prices: List[StorePriceSchema]



