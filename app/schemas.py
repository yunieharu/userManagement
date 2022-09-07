from typing import List
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    name: str
    age: int
    gender: str


class UserCreate(BaseModel):
    username: str
    name: str
    age: int
    gender: str


class UserUpdate(BaseModel):
    name: str
    age: int
    gender: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class AuthDetails(BaseModel):
    username: str
    password: str


class AccountCreate(BaseModel):
    username: str
    email: str
    password: str

class AccountForget(BaseModel):
    email: str

class AccountReset(BaseModel):
    token: str
    new_password: str
    confirm_password: str

class TokenCheck(BaseModel):
    token: str
