from pydantic import BaseModel
from app.core.enums import StoresEnum

class StorePriceDetails(BaseModel):
    price: float
    cheapest_price: float

class CreateGameSchema(BaseModel):
    title: str
    developer: str
    all_time_cheapest_price: float
    prices: dict[StoresEnum, StorePriceDetails]

class UpdateGameSchema(BaseModel):
    id: int
    title: str
    developer: str
    all_time_cheapest_price: float
    prices: dict[StoresEnum, StorePriceDetails]

class GameResponseSchema(BaseModel):
    id: str
    title: str
    developer: str
    all_time_cheapest_price: float
    prices: dict[StoresEnum, StorePriceDetails]
