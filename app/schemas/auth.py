from pydantic import BaseModel
from app.schemas.cart import CartItemSchema
from typing import List

class UserCreateSchema(BaseModel):
    name: str
    email: str
    password: str

class UserLoginSchema(BaseModel):
    email: str
    password: str

class UserResponseSchema(BaseModel):
    id: str
    name: str
    email: str
    admin: bool
    cart_count : int
    cart: List[CartItemSchema]

