from pydantic import BaseModel
from app.core.enums import StoresEnum

class StorePriceDetails(BaseModel):
    price: float

class CreateGameSchema(BaseModel):
    title: str
    developer: str
    all_time_cheapest_price: float
    prices: dict[StoresEnum, StorePriceDetails]

class UpdateGameSchema(BaseModel):
    title: str | None = None
    developer: str | None = None
    all_time_cheapest_price: float | None = None
    prices: dict[StoresEnum, StorePriceDetails] | None = None

class GameResponseSchema(BaseModel):
    _id: str
    title: str
    developer: str
    all_time_cheapest_price: float
    prices: dict[StoresEnum, StorePriceDetails]
