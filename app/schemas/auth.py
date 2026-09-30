from pydantic import BaseModel
from app.schemas.cart import CartItemSchema
from typing import List

class UserCreateSchema(BaseModel):
    name: str
    email: str
    password: str

class UserUpdateAdminSchema(BaseModel):
    name: str | None = None
    email: str | None = None
    admin: bool | None = None

class UserUpdateSchema(BaseModel):
    name: str | None = None
    email: str | None = None

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

