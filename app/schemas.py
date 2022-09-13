from typing import List
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(..., description="Username of user to login")
    name: str = Field(..., description="Name of user")
    age: int = Field(..., description="Age of user")
    gender: str = Field(..., description="Gender of user")


class UserCreate(BaseModel):
    username: str = Field(..., description="Username of user to login")
    name: str = Field(..., description="Name of user")
    age: int = Field(..., description="Age of user")
    gender: str = Field(..., description="Gender of user")


class UserUpdate(BaseModel):
    name: str = Field(..., description="Name of user")
    age: int = Field(..., description="Age of user")
    gender: str = Field(..., description="Gender of user")


class User(UserBase):
    id: int = Field(..., description="Index of user")

    class Config:
        orm_mode = True


class AuthDetails(BaseModel):
    username: str = Field(..., description="Username of user to login, cant use existed username")
    password: str = Field(..., description="Password of user to login")


class AccountCreate(BaseModel):
    username: str = Field(..., description="Username of user to login, cant use existed username")
    email: str = Field(..., description="Email of user to login, cant use existed email")
    password: str = Field(..., description="Password of user to login")


class AccountForget(BaseModel):
    email: str = Field(..., description="Email of user to login, cant use existed email")


class AccountReset(BaseModel):
    token: str
    new_password: str = Field(..., description="New password")
    confirm_password: str = Field(..., description="Confirm password is the same as new password")


class TokenCheck(BaseModel):
    token: str
