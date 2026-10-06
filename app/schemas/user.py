from pydantic import BaseModel, Field, EmailStr
from app.schemas.cart import CartItemSchema
from typing import List

class UserCreateSchema(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=64)

class UserPasswordUpdateSchema(BaseModel):
    password: str = Field(..., min_length=8, max_length=64)

class UserUpdateAdminSchema(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    admin: bool | None = None

class UserUpdateSchema(BaseModel):
    name: str | None = None
    email: EmailStr | None = None

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserResponseSchema(BaseModel):
    _id: str
    name: str
    email: str
    admin: bool
    cart_count : int
    cart: List[CartItemSchema]

